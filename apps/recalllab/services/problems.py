"""Problem-first practice, using the existing durable journal and checkpoint bridge.

Only trusted curriculum SQL fixtures execute. Python and external systems need an
explicit human review of artifacts; a learner's `/solved` declaration is not a pass.
"""
from datetime import date, timedelta
import copy
import sqlite3
import time
import uuid

from services import curriculum
from services.evaluation import sql_assessment


def run_problem_sql(query, specification):
    """Run SELECT against disposable, published fixtures with bounded resources."""
    if not query.strip() or len(query) > 12000:
        return {'passed': False, 'error': 'Enter a SELECT query up to 12,000 characters.', 'fixtures': []}
    results = []
    for case in specification.get('cases', []):
        db = sqlite3.connect(':memory:')
        try:
            db.enable_load_extension(False)
            db.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 100000)
            db.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 12000)
            db.setlimit(sqlite3.SQLITE_LIMIT_COLUMN, 50)
            db.setlimit(sqlite3.SQLITE_LIMIT_EXPR_DEPTH, 50)
            db.setlimit(sqlite3.SQLITE_LIMIT_COMPOUND_SELECT, 5)
            # The setup comes only from the published local curriculum, never a submission.
            db.executescript(case['setup'])
            tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            safe_functions = {'count', 'sum', 'avg', 'min', 'max', 'coalesce', 'ifnull', 'nullif',
                              'round', 'lower', 'upper', 'trim', 'length', 'abs', 'total'}
            def authorize(action, arg1, arg2, database, trigger):
                if action == sqlite3.SQLITE_READ:
                    return sqlite3.SQLITE_OK if arg1 in tables and database in ('main', None) else sqlite3.SQLITE_DENY
                if action == sqlite3.SQLITE_FUNCTION:
                    return sqlite3.SQLITE_OK if (arg2 or '').lower() in safe_functions else sqlite3.SQLITE_DENY
                return sqlite3.SQLITE_OK if action == sqlite3.SQLITE_SELECT else sqlite3.SQLITE_DENY
            db.set_authorizer(authorize)
            deadline = time.monotonic() + .4
            db.set_progress_handler(lambda: time.monotonic() > deadline, 100)
            cursor = db.execute(query)
            actual = [list(row) for row in cursor.fetchmany(101)]
            columns = [c[0] for c in cursor.description or []]
            expected = case['expected']
            ordered = specification.get('order_matters', True)
            matched = actual == expected if ordered else sorted(actual, key=repr) == sorted(expected, key=repr)
            matched = matched and len(actual) <= 100 and columns == case.get('expected_columns', columns)
            results.append({'passed': matched, 'actual': actual, 'expected': expected,
                            'actual_columns': columns, 'expected_columns': case.get('expected_columns', columns)})
        except (sqlite3.Error, ValueError) as error:
            return {'passed': False, 'error': str(error), 'fixtures': results}
        finally:
            db.close()
    return {'passed': bool(results) and all(r['passed'] for r in results), 'error': None, 'fixtures': results}


class Problems:
    def __init__(self, journal, catalog=None, records=None):
        self.journal = journal
        self.catalog = catalog
        self.records = records
        self._ids_cache = None

    def _catalog(self):
        return {'curriculum': self.catalog} if self.catalog is not None else {}

    def attempts(self):
        canonical = self.records.events() if self.records is not None else []
        merged = {a['attempt_id']:a for a in canonical if a.get('kind') == 'problem'}
        merged.update({a['attempt_id']:a for a in self.journal.effective_attempts() if a.get('kind') == 'problem'})
        return sorted(merged.values(), key=lambda a:(a['attempt_date_ist'],a.get('timestamp',''),a['attempt_id']))

    @staticmethod
    def verified(attempt):
        return attempt.get('correct') is True and attempt.get('evaluation') in ('sql_fixtures', 'human_review')

    def _ids(self):
        if self._ids_cache is not None:
            completed, independent = self._ids_cache
            return set(completed), set(independent)
        verified = [a for a in self.attempts() if self.verified(a)]
        independent, assisted_dates = set(), {}
        for a in verified:
            ident = a['problem_id']
            if a.get('help_used') is True:
                assisted_dates[ident] = a['attempt_date_ist']
            if a.get('result') == 'independent' and a.get('help_used') is False and a.get('notes_used') is False and a.get('hints_used') == 0:
                prior_help = assisted_dates.get(ident)
                if not prior_help or (a.get('independent_followup') and a['attempt_date_ist'] > prior_help):
                    independent.add(ident)
        completed = {a['problem_id'] for a in verified}
        self._ids_cache = (completed, independent)
        return set(completed), set(independent)

    def progress(self, tool_id):
        completed, independent = self._ids()
        counts = curriculum.progress_counts(tool_id, completed, independent, **self._catalog())
        ids = {p['id'] for p in curriculum.published_problems(tool_id, **self._catalog())}
        counts.update(completed=len(completed & ids), independent=len(independent & ids), total=len(ids))
        counts['independent_followups'] = self.independent_followups(tool_id)
        counts['milestone'] = counts['completed'] if counts['completed'] and counts['completed'] % 10 == 0 else None
        return counts

    def hint(self, problem_id, independent_followup=False):
        problem = self.independent_problem(problem_id) if independent_followup else curriculum.get_problem(problem_id, **self._catalog())
        if not problem:
            raise ValueError('Unknown published problem.')
        hints = problem.get('progressive_hints', [])
        key = 'problem-help:' + problem_id + (':followup' if independent_followup else ':initial')
        state = self.journal.get('drafts', key, {'hints_used': 0})
        count = state['hints_used']
        if count >= len(hints):
            return 'Share your smallest failing input, actual output or error, and expected result for focused review.'
        state['hints_used'] = count + 1
        self.journal.put('drafts', key, state)
        return hints[count]

    def next_problem(self, tool_id, diagnostic=False, job_ready=False):
        if diagnostic:
            options = self.acceleration_options(tool_id)
            return options[0] if options else None
        completed, independent = self._ids()
        data = self.catalog or curriculum.load_curriculum()
        allowed = set(data.get('job_ready_pathway', {}).get('problem_ids', [])) if job_ready else None
        return curriculum.select_next_problem(tool_id, completed, independent, curriculum=data, allowed_ids=allowed)

    def acceleration_options(self, tool_id):
        completed, independent = self._ids()
        return [dict(p, diagnostic_attempt=True) for p in curriculum.published_problems(tool_id, **self._catalog())
                if p.get('diagnostic') is True and p['id'] not in completed]

    def diagnostic_problem(self, problem_id):
        problem = curriculum.get_problem(problem_id, **self._catalog())
        if not problem or problem.get('diagnostic') is not True:
            raise ValueError('This published problem is not an entry diagnostic.')
        return dict(problem, diagnostic_attempt=True)

    def submit(self, problem_id, how_solved, assistance_sources, evidence, results,
               explanation='', token=None, independent_followup=False, diagnostic=False,
               changed_input='', changed_expected=''):
        problem = curriculum.get_problem(problem_id, **self._catalog())
        if not problem:
            raise ValueError('Unknown published problem.')
        if independent_followup:
            problem = self.independent_problem(problem_id)
            if problem.get('needs_chosen_input'):
                if not changed_input.strip() or not changed_expected.strip():
                    raise ValueError('State the exact changed input and its expected result before submitting independent reconstruction.')
                problem['inputs']['chosen_changed_input'] = changed_input.strip()
                problem['expected_output'] = changed_expected.strip()
        if diagnostic:
            problem = self.diagnostic_problem(problem_id)
        completed, independent = self._ids()
        missing, missing_independent = curriculum.missing_prerequisites(problem, completed, independent, **self._catalog())
        if missing and not diagnostic:
            raise ValueError('Verify prerequisite problems first: ' + ', '.join(sorted(missing)))
        if missing_independent and not diagnostic:
            raise ValueError('Provide independent evidence for prerequisite problems first: ' + ', '.join(sorted(missing_independent)))
        if not all(isinstance(v, str) and v.strip() for v in (how_solved, evidence, results)):
            raise ValueError('Explain how you solved it and provide code/artifacts plus actual results.')
        if not isinstance(assistance_sources, (list, tuple)) or not assistance_sources or not all(isinstance(s,str) and s.strip() for s in assistance_sources):
            raise ValueError('Declare sources of help, or explicitly choose none / unknown.')
        sources = [s.strip() for s in assistance_sources]
        normalized = {s.lower() for s in sources}
        if 'none' in normalized and len(normalized) != 1:
            raise ValueError('None cannot be combined with a source of help.')
        help_used = False if normalized == {'none'} else None if normalized == {'unknown'} else True
        hint_key = 'problem-help:' + problem_id + (':followup' if independent_followup else ':initial')
        hints_used = self.journal.get('drafts', hint_key, {}).get('hints_used', 0)
        if hints_used:
            help_used = True
            sources = [s for s in sources if s.lower() != 'none'] + ['RecallLab progressive hints']
        payload = dict(kind='problem', code_submission=True, item_id=problem_id, problem_id=problem_id,
                       tool_id=problem['tool_id'], curriculum_version=(self.catalog or curriculum.load_curriculum())['version'],
                       question=problem['task'], answer=evidence.strip(), how_solved=how_solved.strip(),
                       assistance_sources=sources, submitted_results=results.strip(), explanation=explanation,
                       dimension='building', help_used=help_used, notes_used=help_used, hints_used=hints_used,
                       evaluation='manual_pending', score=None, correct=None, result='unknown',
                       evaluation_status='awaiting_artifact_review',
                       feedback='Awaiting a human review of the implementation, actual results, edge cases and acceptance criteria.')
        payload['independent_followup'] = bool(independent_followup)
        payload['diagnostic_attempt'] = bool(diagnostic)
        payload['problem_snapshot'] = {key:copy.deepcopy(value) for key,value in problem.items() if key not in ('verification','followup')}
        payload['problem_snapshot']['curriculum_version'] = payload['curriculum_version']
        if independent_followup:
            payload['followup_inputs'] = problem['inputs']
            payload['question'] = problem['task'] + '\nChanged input: ' + str(problem['inputs'])
        specification = problem.get('verification', {})
        if specification.get('kind') == 'sql':
            tests = run_problem_sql(evidence, specification)
            payload.update(sql_assessment(tests, help_used, notes_used=help_used))
            payload['feedback'] = ('All published SQL fixtures passed. ' if tests['passed'] else
                                   f'{sum(bool(f["passed"]) for f in tests["fixtures"])}/{len(specification.get("cases", []))} SQL fixtures passed. ')
            payload['feedback'] += 'Compare actual rows, column names and edge cases; explain why the query meets the business requirement.'
            if tests.get('error'):
                payload['feedback'] += ' ' + tests['error']
            if diagnostic and tests['passed']:
                # A grouped result cannot prove the separate skills that a diagnostic
                # may waive. Preserve executed results, then require criterion review.
                payload.update(evaluation='manual_pending', score=None, correct=None, result='unknown',
                               evaluation_status='awaiting_diagnostic_review',
                               feedback=payload['feedback'] + ' A human must verify every diagnostic criterion, including the separate prerequisite skills, before acceleration.')
        payload['independent_followup_required'] = help_used is True
        saved = self.journal.save(self.journal.session(), token or 'problem-' + uuid.uuid4().hex, payload)
        self._ids_cache = None
        return saved

    def review(self, attempt_id, reviewer, verification, feedback, score, acceptance_checked=False):
        attempt = next((a for a in self.attempts() if a['attempt_id'] == attempt_id), None)
        if not attempt:
            raise ValueError('Unknown problem attempt.')
        if score == 3 and not acceptance_checked:
            raise ValueError('Review actual artifacts, expected output, edge cases and every acceptance criterion before verifying.')
        self.journal.assess(attempt_id, dict(reviewer=reviewer, verification=verification, feedback=feedback, score=score))
        self._ids_cache = None
        return next(a for a in self.attempts() if a['attempt_id'] == attempt_id)

    def feedback(self, attempt):
        failures = [a for a in self.attempts() if a['problem_id'] == attempt['problem_id'] and a.get('correct') is False]
        text = attempt['feedback']
        if self.verified(attempt):
            problem = curriculum.get_problem(attempt['problem_id'], **self._catalog())
            if problem:
                text += ' Pipeline connection: ' + problem['engineering_relevance']
            if attempt.get('evaluation') == 'sql_fixtures':
                text += ' Limitation: passing these disposable SQLite fixtures does not verify PostgreSQL-specific behavior, larger inputs or operational reruns.'
            else:
                text += ' Limitation: this is an attested human review of submitted artifacts; repeatable execution and changed-input evidence remain important for operational use.'
        if len(failures) > 1:
            text += ' Recurring difficulty on this problem: compare the failed cases and practise a changed example after correction.'
        return text

    def independent_followups(self, tool_id=None):
        completed, independent = self._ids()
        followups = {}
        canonical_ids = {a['attempt_id'] for a in self.records.events()} if self.records is not None else set()
        queue = {r['item_id']:r for r in self.records.csv('revision-queue.csv')} if self.records is not None else {}
        for a in self.attempts():
            if self.verified(a) and a.get('help_used') is True and a['problem_id'] not in independent and (tool_id is None or a['tool_id'] == tool_id):
                canonical_due = queue.get(a['problem_id'], {}).get('next_review_date_ist') if a['attempt_id'] in canonical_ids else None
                followups[a['problem_id']] = dict(problem_id=a['problem_id'],
                    due_date=canonical_due or (date.fromisoformat(a['attempt_date_ist']) + timedelta(days=1)).isoformat(),
                    task='Attempt a similar changed-input problem independently; preserve the original assisted completion.',
                    schedule_status='Canonical review queue date.' if canonical_due else 'Provisional local follow-up; canonical review queue owns the saved schedule after checkpoint.',
                    source_attempt_id=a['attempt_id'])
        return list(followups.values())

    def independent_problem(self, problem_id):
        """Expose a published changed input without revealing an implementation."""
        problem = copy.deepcopy(curriculum.get_problem(problem_id, **self._catalog()))
        if not problem:
            raise ValueError('Unknown published problem.')
        followup = problem.get('followup')
        if not followup or not followup.get('task') or followup.get('inputs') == problem.get('inputs'):
            # This is a reviewed variant, never an extra published problem or a
            # fabricated executable fixture. The learner states its exact contract.
            problem['inputs'] = {'baseline':problem['inputs'],
                'variant_requirement':'Choose a changed input that exercises a different boundary under this same business requirement. State it and its exact expected output before implementing.'}
            problem['task'] += ' Independently reconstruct a changed-input case. Preserve the earlier attempt and verify the new expected output with a reviewer.'
            problem['needs_chosen_input'] = True
            problem['verification'] = {'kind':'artifact_review'}
            problem['independent_followup'] = True
            return problem
        for key in ('inputs', 'expected_output', 'task', 'verification'):
            if key in followup:
                problem[key] = followup[key]
        problem['independent_followup'] = True
        return problem
