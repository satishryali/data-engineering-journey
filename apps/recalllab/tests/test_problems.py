"""Disposable journal tests: problem evidence never writes real learner progress."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from unittest.mock import Mock
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.journal import Journal
from services.problems import Problems, run_problem_sql
from services.records import now


SQL = {'kind': 'sql', 'cases': [
    {'setup': 'CREATE TABLE sales(id INTEGER,amount INTEGER);INSERT INTO sales VALUES(1,25),(2,40);',
     'expected': [[1,25],[2,40]], 'expected_columns': ['id','amount']},
    {'setup': 'CREATE TABLE sales(id INTEGER,amount INTEGER);INSERT INTO sales VALUES(3,NULL);',
     'expected': [[3,None]], 'expected_columns': ['id','amount']}], 'order_matters': True}
PROBLEMS = {
    'T-001': {'id':'T-001','tool_id':'python','task':'Read one sale','inputs':{'id':1,'amount':25},
              'expected_output':'Sale 1 amount 25','prerequisites':[], 'verification':{'kind':'artifact_review'}},
    'T-002': {'id':'T-002','tool_id':'python','task':'Read several sales','inputs':[{'id':1,'amount':25}],
              'expected_output':'One sale','prerequisites':['T-001'], 'verification':{'kind':'artifact_review'}},
    'S-001': {'id':'S-001','tool_id':'sql','task':'Return all sales','prerequisites':[], 'verification':SQL}}


class ProblemTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.journal = Journal(Path(self.folder.name) / 'journal.sqlite3')
        self.service = Problems(self.journal)
        patches = [
            patch('services.problems.curriculum.get_problem', side_effect=lambda ident, **kw: PROBLEMS.get(ident)),
            patch('services.problems.curriculum.published_problems', side_effect=lambda tool, **kw: [p for p in PROBLEMS.values() if p['tool_id']==tool]),
            patch('services.problems.curriculum.progress_counts', return_value={}),
            patch('services.problems.curriculum.select_next_problem', side_effect=lambda tool, done, independent, **kw: next((p for p in PROBLEMS.values() if p['tool_id']==tool and p['id'] not in done and set(p['prerequisites']) <= set(done)), None))]
        for item in patches:
            item.start()
            self.addCleanup(item.stop)

    def submit(self, ident='T-001', help_sources=None, **kwargs):
        return self.service.submit(ident, 'I traced the input and compared output',
            help_sources or ['none'], 'print(record)', 'Observed sale 1 amount 25', **kwargs)

    def review(self, attempt, score=3):
        return self.service.review(attempt['attempt_id'], 'Tutor', 'Inspected artifacts; changed empty input returned no rows',
                                   'All acceptance criteria met; retain the input types.', score, acceptance_checked=True)

    def test_solved_requires_actual_evidence_and_help_declaration(self):
        with self.assertRaises(ValueError):
            self.service.submit('T-001', 'Used a loop', [], 'code', 'output')
        with self.assertRaises(ValueError):
            self.service.submit('T-001', 'Used a loop', ['none'], 'code', '')
        with self.assertRaises(ValueError):
            self.service.submit('T-001', 'Used a loop', ['none','Copilot'], 'code', 'output')
        self.assertEqual(self.journal.attempts(), [])

    def test_pending_artifacts_never_count_and_block_prerequisites(self):
        attempt = self.submit()
        self.assertEqual(attempt['problem_snapshot']['task'], PROBLEMS['T-001']['task'])
        self.assertEqual(attempt['evaluation'], 'manual_pending')
        self.assertEqual(self.service.progress('python')['completed'], 0)
        with self.assertRaises(ValueError):
            self.submit('T-002')
        with self.assertRaises(ValueError):
            self.service.review(attempt['attempt_id'], 'Tutor', 'Observed output', 'Correct', 3)

    def test_verified_independence_unlocks_next_and_counts_once(self):
        first = self.submit()
        self.review(first)
        counts = self.service.progress('python')
        self.assertEqual((counts['completed'],counts['independent'],counts['total']), (1,1,2))
        self.assertEqual(self.service.next_problem('python')['id'], 'T-002')
        self.review(self.submit())
        self.assertEqual(self.service.progress('python')['completed'], 1)

    def test_assistance_completion_is_not_independence_and_followup_is_durable(self):
        attempt = self.submit(help_sources=['Copilot','official documentation'])
        saved = self.review(attempt)
        self.assertEqual(saved['result'], 'assisted')
        counts = self.service.progress('python')
        self.assertEqual((counts['completed'],counts['independent']), (1,0))
        self.assertEqual(counts['independent_followups'][0]['source_attempt_id'], attempt['attempt_id'])
        self.assertEqual(Problems(Journal(self.journal.path)).progress('python')['completed'], 1)

    def test_unknown_help_never_claims_independence(self):
        self.review(self.submit(help_sources=['unknown']))
        self.assertEqual(self.service.progress('python')['independent'], 0)

    def test_independent_prerequisite_blocks_assisted_only_completion(self):
        self.review(self.submit(help_sources=['Copilot']))
        advanced = dict(PROBLEMS['T-002'], independent_prerequisites=['T-001'])
        with patch.dict(PROBLEMS, {'T-002':advanced}):
            with self.assertRaisesRegex(ValueError, 'independent evidence'):
                self.submit('T-002')

    def test_only_published_diagnostic_can_be_attempted_before_prerequisites(self):
        with self.assertRaises(ValueError):
            self.submit('T-002', diagnostic=True)
        diagnostic = dict(PROBLEMS['T-002'], diagnostic=True, diagnostic_covers=['T-001'])
        with patch.dict(PROBLEMS, {'T-002':diagnostic}):
            self.review(self.submit('T-002', diagnostic=True))
            counts = self.service.progress('python')
            self.assertEqual((counts['completed'],counts['independent']), (1,1))
            self.assertEqual(self.service.attempts()[0]['problem_id'], 'T-002')

    def test_failure_and_retries_preserve_success_and_feedback(self):
        self.review(self.submit())
        self.review(self.submit(), 0)
        failed = self.review(self.submit(), 0)
        self.assertIn('Recurring difficulty', self.service.feedback(failed))
        self.assertEqual(self.service.progress('python')['completed'], 1)
        self.assertEqual(len(self.journal.attempts()), 3)

    def test_submission_idempotence_and_export_restore(self):
        first = self.submit(token='stable')
        self.assertEqual(self.submit(token='stable')['attempt_id'], first['attempt_id'])
        self.review(first)
        target = Journal(Path(self.folder.name) / 'restored.sqlite3')
        target.restore_export(self.journal.export())
        self.assertEqual(Problems(target).progress('python')['completed'], 1)

    def test_sql_executes_changed_fixtures_and_records_failures(self):
        self.assertTrue(run_problem_sql('SELECT id,amount FROM sales ORDER BY id', SQL)['passed'])
        self.assertFalse(run_problem_sql('SELECT 1 AS id,25 AS amount UNION ALL SELECT 2,40', SQL)['passed'])
        submitted = self.service.submit('S-001','Selected all sales',['none'],
                                       'SELECT id,amount FROM sales ORDER BY id','1,25;2,40')
        self.assertTrue(submitted['correct'])
        self.assertEqual(self.service.progress('sql')['completed'], 1)

    def test_sql_diagnostic_needs_review_of_skills_beyond_query_output(self):
        diagnostic = dict(PROBLEMS['S-001'], diagnostic=True, diagnostic_covers=['SQL-BASIC'])
        with patch.dict(PROBLEMS, {'S-001':diagnostic}):
            attempt = self.service.submit('S-001','Selected sales',['none'],
                'SELECT id,amount FROM sales ORDER BY id','Observed rows',diagnostic=True)
            self.assertTrue(attempt['test_evidence']['passed'])
            self.assertEqual(attempt['evaluation'], 'manual_pending')
            self.assertEqual(self.service.progress('sql')['completed'], 0)
            self.review(attempt)
            self.assertEqual(self.service.progress('sql')['independent'], 1)

    def test_sql_cannot_write_attach_or_load_extensions(self):
        for query in ('DELETE FROM sales', "ATTACH DATABASE 'test.sqlite' AS external", "SELECT load_extension('bad')", 'SELECT * FROM sqlite_master'):
            with self.subTest(query=query):
                self.assertFalse(run_problem_sql(query, SQL)['passed'])

    def test_empty_fixture_never_passes(self):
        self.assertFalse(run_problem_sql('SELECT 1', {'cases':[]})['passed'])

    def test_canonical_evidence_preserves_cross_device_progress_without_sqlite(self):
        self.review(self.submit())
        canonical = self.service.attempts()
        journal = Journal(Path(self.folder.name) / 'other-device.sqlite3')
        records = Mock()
        records.events.return_value = canonical
        records.csv.return_value = []
        service = Problems(journal, records=records)
        self.assertEqual(service.progress('python')['completed'], 1)
        duplicate = Problems(self.journal, records=records)
        self.assertEqual(len(duplicate.attempts()), 1)

    def test_assisted_followup_requires_changed_input_on_a_later_date(self):
        self.review(self.submit(help_sources=['Copilot']))
        self.review(self.submit())
        self.assertEqual(self.service.progress('python')['independent'], 0)
        followup = dict(PROBLEMS['T-001'], followup={'task':'Read changed sale 9',
            'inputs':{'id':9,'amount':40}, 'expected_output':'Sale 9 amount 40'})
        with patch.dict(PROBLEMS, {'T-001':followup}):
            self.review(self.submit(independent_followup=True))
            self.assertEqual(self.service.progress('python')['independent'], 0)
            with patch('services.journal.now', return_value=now()+timedelta(days=1)):
                later = self.submit(independent_followup=True)
                self.review(later)
            self.assertEqual(self.service.progress('python')['independent'], 1)


class ProblemCheckpointTests(unittest.TestCase):
    def test_checkpoint_registers_exercise_schedules_help_and_preserves_existing_records(self):
        import test_recalllab as fixtures
        from services.bridge import end_session
        from services.records import load_coach
        fixture = fixtures.BridgeTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        original = {r['item_id']:r for r in fixture.records.csv('revision-queue.csv')}
        problem = dict(PROBLEMS['S-001'], title='Synthetic published SQL sales task')
        service = Problems(fixture.journal)
        with patch('services.curriculum.get_problem', return_value=problem):
            attempt = service.submit('S-001','Selected the sale rows',['Copilot'],
                'SELECT id,amount FROM sales ORDER BY id','Observed two rows')
            self.assertTrue(attempt['correct'])
            end_session(fixture.records,fixture.journal,fixture.session)
            history = fixture.records.csv('revision-history.csv')
            row = next(r for r in fixture.records.csv('revision-queue.csv') if r['item_id']=='S-001')
            self.assertEqual(row['next_review_date_ist'], (now().date()+timedelta(days=1)).isoformat())
            end_session(fixture.records,fixture.journal,fixture.session)
            self.assertEqual(history,fixture.records.csv('revision-history.csv'))
            after = {r['item_id']:r for r in fixture.records.csv('revision-queue.csv')}
            for ident, value in original.items():
                self.assertEqual(value, after[ident])
            session = fixture.journal.session()
            service.submit('S-001','Attempted query',['none'],'SELECT 1','Observed one row')
            end_session(fixture.records,fixture.journal,session)
            mistakes = fixture.records.json('tracking/mistakes.json')['mistakes']
            mistake = next(m for m in mistakes if 'S-001' in m.get('exercise_ids',[]))
            self.assertEqual(mistake['topic_ids'], [])
            self.assertIn('Validated',load_coach(fixture.root).validate(fixture.root))


if __name__ == '__main__':
    unittest.main()
