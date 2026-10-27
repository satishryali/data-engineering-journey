import copy
from datetime import date, timedelta
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from services.records import ROOT, Records, load_coach, metrics, level, is_revision
from services.questions import question, evaluate, daily_queue
from services.journal import Journal
from services.bridge import end_session
from services.sql_runner import run_sql
from components.calendar import heatmap
from components.learning import next_task


class JournalMigrationTests(unittest.TestCase):
    def test_legacy_sessions_table_is_migrated_without_losing_rows(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'legacy.sqlite3'
            db = sqlite3.connect(path)
            db.execute('CREATE TABLE sessions(id TEXT PRIMARY KEY, created TEXT NOT NULL, state TEXT NOT NULL DEFAULT \'open\')')
            db.execute('INSERT INTO sessions VALUES(?,?,?)', ('RL-' + 'a' * 32, '2026-10-17T10:00:00+05:30', 'open'))
            db.commit(); db.close()

            journal = Journal(path)
            with journal.db() as migrated:
                columns = {row['name'] for row in migrated.execute('PRAGMA table_info(sessions)')}
                version = migrated.execute('PRAGMA user_version').fetchone()[0]
            self.assertIn('batch', columns)
            self.assertEqual(version, Journal.SCHEMA_VERSION)
            self.assertEqual(journal.session(), 'RL-' + 'a' * 32)


class ReadTests(unittest.TestCase):
    def test_pending_task_is_plain_text_not_a_broken_local_link(self):
        task = next_task(Records())
        self.assertNotIn('](', task)

    def test_heatmap_uses_date_effective_study_targets(self):
        values = {'seconds': 6*3600, 'events': [], 'revisions': [], 'coding': [], 'intervals': []}
        self.assertEqual(level((date(2026,10,21), values), 'All Learning'), 4)
        self.assertEqual(level((date(2026,10,22), values), 'All Learning'), 3)
        values['seconds'] = 7*3600
        self.assertEqual(level((date(2026,10,22), values), 'All Learning'), 4)
        values['seconds'] = 10*3600
        self.assertEqual(level((date(2026,10,24), values), 'All Learning'), 4)

    def test_study_and_initial_practice_are_not_revision_activity(self):
        records = Records()
        initial = [dict(attempt_date_ist='2026-10-17', review_kind=kind) for kind in
                   ('initial_learning', 'diagnostic', 'application', 'immediate_correction')]
        with patch.object(records, 'events', return_value=initial):
            activity = records.activity(date(2026, 10, 17))
        self.assertGreater(metrics(activity)['hours'], 0)
        self.assertEqual(metrics(activity, 'Revision Only')['active_days'], 0)
        self.assertEqual(metrics(activity, 'Revision Only')['attempts'], 0)
        self.assertIsNone(metrics(activity, 'Revision Only')['hours'])
        for kind in ('initial_learning', 'diagnostic', 'application', 'immediate_correction'):
            self.assertFalse(is_revision({'review_kind': kind}))
        self.assertTrue(is_revision({'review_kind': 'delayed', 'score': 0}))
        self.assertTrue(is_revision({'practice_context': 'revision', 'score': None}))

    def test_revision_and_coding_use_separate_events_not_study_hours(self):
        d = date(2026, 10, 17)
        initial = {'review_kind': 'initial_learning'}
        failed_review = {'review_kind': 'delayed', 'score': 0}
        values = {'seconds': 36000, 'events': [initial, failed_review],
                  'revisions': [failed_review], 'coding': [], 'intervals': []}
        self.assertEqual(metrics({d:values}, 'Revision Only')['attempts'], 1)
        self.assertEqual(level((d, values), 'Coding Practice'), 0)
        values['revisions'] = []
        self.assertEqual(level((d, values), 'Revision Only'), 0)
        self.assertGreater(level((d, values), 'All Learning'), 0)

    def test_dashboard_uses_real_counts_and_functional_links(self):
        from components.dashboard import dashboard
        with tempfile.TemporaryDirectory() as tmp:
            r = Records()
            j = Journal(Path(tmp)/'journal.sqlite3')
            day = date(2026, 10, 17)
            rendered = dashboard(r, j, day, {'session_minutes':20, 'study_thresholds':[.25,.5,1,1.25], 'attempt_thresholds':[1,3,5,8]})
            self.assertIn('Make room for what stays.', rendered)
            self.assertIn(f'{metrics(r.activity(day))["hours"]:.1f} hrs', rendered)
            self.assertIn('Unassessed', rendered)
            self.assertIn('view=Today%27s+Session', rendered)
            self.assertIn('view=Notes+Browser', rendered)
            self.assertIn('note=Notes%2FPython', rendered)
            self.assertEqual(rendered.count('class="day"'),365)

    def test_reading_does_not_mutate_records_and_variants_change_daily(self):
        r = Records()
        paths = list((ROOT / 'tracking').glob('*.csv')) + list((ROOT / 'tracking').glob('*.json'))
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        a = r.activity(date(2026, 10, 17))
        self.assertEqual(len(a), 365)
        self.assertEqual(min(a), date(2025, 10, 18))
        self.assertGreater(metrics(a)['hours'], 0)
        self.assertLessEqual(len(daily_queue(r, 20, date(2026, 10, 17))), 2)
        for row in r.csv('revision-queue.csv'):
            one = question(r, row['item_id'], date(2026, 10, 17))
            two = question(r, row['item_id'], date(2026, 10, 18))
            self.assertNotEqual(one.prompt, two.prompt)
            self.assertEqual(one, question(r, row['item_id'], date(2026, 10, 17)))
            self.assertTrue(one.sources)
        self.assertEqual(before, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})

    def test_paths_cannot_escape_notes(self):
        r = Records()
        for path in ('../secret.md', 'tracking/mistakes.json', 'Notes/../AGENTS.md', 'Notes/.obsidian/workspace.json'):
            with self.assertRaises(ValueError):
                r.path(path, notes_only=True)

    def test_calendar_levels_and_boundaries(self):
        d = date(2026, 10, 17)
        empty = {'seconds': 0, 'events': [], 'coding': [], 'intervals': []}
        extra = dict(empty, seconds=13*3600)
        self.assertEqual(level((d, empty), 'All Learning'), 0)
        self.assertEqual(level((d, extra), 'All Learning'), 5)
        self.assertEqual(level((d-timedelta(days=1), dict(empty, seconds=7.6*3600)), 'All Learning'), 5)
        html = heatmap(Records().activity(date(2027, 1, 3)), 'Revision Only')
        self.assertEqual(html.count('class="day"'), 365)
        self.assertIn('2026-01-04', html)
        self.assertIn('2027-01-03', html)
        self.assertIn('aria-label', html)

    def test_help_and_manual_semantics(self):
        q = question(Records(), 'py.dict.access', date(2026, 10, 17))
        answer = json.dumps(q.expected)
        self.assertEqual(evaluate(q, answer, False)['result'], 'independent')
        self.assertEqual(evaluate(q, answer, False, True)['result'], 'assisted')
        self.assertEqual(evaluate(q, answer, False, False, 1)['result'], 'assisted')
        self.assertNotEqual(evaluate(q, answer)['result'], 'independent')
        self.assertIsNone(evaluate(q, answer)['score'])
        self.assertEqual(evaluate(q, '[]', False)['score'], 0)
        with self.assertRaises(ValueError):
            evaluate(q, ' ')
        manual = question(Records(), 'py.records.cleaning')
        self.assertIsNone(evaluate(manual, 'def clean_orders(rows): pass', False)['score'])


class SQLTests(unittest.TestCase):
    def test_multiple_output_fixtures_not_query_strings(self):
        query = 'SELECT c.customer_id,c.name,COUNT(o.order_id) FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id GROUP BY c.customer_id,c.name ORDER BY c.customer_id'
        self.assertTrue(run_sql(query)['passed'])
        self.assertFalse(run_sql(query.replace('COUNT(o.order_id)', 'COUNT(*)'))['passed'])
        self.assertTrue(run_sql('SELECT c.customer_id,o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id ORDER BY c.customer_id,o.order_id', 'join')['passed'])
        self.assertTrue(run_sql(query.replace('COUNT(o.order_id)', 'SUM(o.amount)'), 'sum')['passed'])

    def test_sql_external_access_writes_and_resource_abuse_denied(self):
        for query in ["ATTACH DATABASE 'sensitive.db' AS x", 'DROP TABLE customers',
                      "SELECT load_extension('malicious')", "SELECT readfile('secret')", 'SELECT * FROM sqlite_master',
                      'SELECT randomblob(1000000000)', 'PRAGMA database_list',
                      'WITH RECURSIVE x(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM x) SELECT * FROM x',
                      'SELECT 1; SELECT 2']:
            result = run_sql(query)
            self.assertFalse(result['passed'], query)
            self.assertTrue(result['error'], query)


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ('tracking', 'Notes', 'tools', 'progress'):
            shutil.copytree(ROOT / folder, self.root / folder, ignore=shutil.ignore_patterns('__pycache__', 'node_modules', '.obsidian', 'tests', '*.coach-tmp', '.coach-transaction.json'))
        for file in ('START-HERE.md', 'AGENTS.md'):
            shutil.copy2(ROOT / file, self.root / file)
        self.records = Records(self.root)
        self.journal = Journal(self.root / 'apps/recalllab/data/recalllab.sqlite3')
        self.session = self.journal.session()
        self.protected = {str(p): p.read_bytes() for p in [self.root/'progress/current.md', self.root/'START-HERE.md', self.root/'tracking/study-log.csv']}

    def payload(self, item='py.dict.access', score=3):
        return dict(item_id=item, question='Synthetic test question, not learner evidence.', answer='Synthetic test answer',
                    feedback='Fixture assessed output', score=score, result='independent' if score else 'needs_guidance',
                    dimension='reading_predicting', hints_used=0, notes_used=False, help_used=False,
                    task_variant='test-only', evaluation='exact_output')

    def test_durable_submit_duplicate_and_checkpoint_replay(self):
        a = self.journal.save(self.session, 'token', self.payload())
        self.assertEqual(a, self.journal.save(self.session, 'token', self.payload()))
        restarted = Journal(self.journal.path)
        self.assertEqual(restarted.attempts()[0], a)
        self.assertEqual(restarted.session(), self.session)
        self.assertIn('Recorded', end_session(self.records, restarted, self.session))
        before = (self.root / 'tracking/revision-history.csv').read_bytes()
        self.assertIn('Already', end_session(self.records, restarted, self.session))
        self.assertEqual(before, (self.root / 'tracking/revision-history.csv').read_bytes())
        coach = load_coach(self.root)
        self.assertIn('Validated', coach.validate(self.root))
        for p, content in self.protected.items():
            self.assertEqual(Path(p).read_bytes(), content)
        with self.assertRaises(ValueError):
            self.journal.save(self.session, 'other', self.payload())

    def test_interrupted_transaction_retry_is_exactly_once(self):
        self.journal.save(self.session, 'token', self.payload())
        coach = load_coach(self.root)
        original = coach.os.replace
        calls = 0
        def interrupted(src, dst):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError('Simulated partial canonical write')
            return original(src, dst)
        with patch('services.bridge.load_coach', return_value=coach), patch.object(coach.os, 'replace', side_effect=interrupted):
            with self.assertRaises(OSError):
                end_session(self.records, self.journal, self.session)
        self.assertEqual(self.journal.sessions()[0]['state'], 'pending')
        self.assertIn('Recorded', end_session(self.records, self.journal, self.session))
        ids = [e['attempt_id'] for e in self.records.events()]
        self.assertEqual(ids.count(self.journal.attempts()[0]['attempt_id']), 1)

    def test_manual_submission_preserves_due_and_failed_attempt_recommends_note(self):
        before = {r['item_id']: r for r in self.records.csv('revision-queue.csv')}
        self.journal.save(self.session, 'token', dict(self.payload('py.records.cleaning'), score=None, result='unknown', help_used=None, evaluation='manual_pending'))
        end_session(self.records, self.journal, self.session)
        after = {r['item_id']: r for r in self.records.csv('revision-queue.csv')}
        self.assertEqual(before['py.records.cleaning']['next_review_date_ist'], after['py.records.cleaning']['next_review_date_ist'])
        session = self.journal.session()
        self.journal.save(session, 'fail', self.payload(score=0))
        end_session(self.records, self.journal, session)
        recs = self.records.recommendations(self.records.events()[-1:])
        self.assertTrue(recs)
        self.assertTrue(recs[0]['heading'])
        self.assertTrue(self.records.path(recs[0]['path']).exists())

    def test_journal_backup_and_drafts_survive_restart(self):
        self.journal.put('drafts', 'x', {'answer': 'unfinished'})
        backup = self.journal.backup()
        self.assertEqual(Journal(backup).get('drafts', 'x')['answer'], 'unfinished')
        self.assertEqual(json.loads(self.journal.export())['drafts'][0]['key'], 'x')

    def test_delayed_score_uses_coach_stage_and_actual_assessment_date(self):
        from services.records import now
        item = 'py.records.cleaning'
        before = next(r for r in self.records.csv('revision-queue.csv') if r['item_id'] == item)
        a = self.journal.save(self.session, 'delayed', self.payload(item))
        end_session(self.records, self.journal, self.session)
        event = next(e for e in self.records.events() if e['attempt_id'] == a['attempt_id'])
        self.assertEqual(event['review_kind'], 'delayed')
        coach = load_coach(self.root)
        stage, due = coach.schedule(int(before['review_stage']), before['next_review_date_ist'], event, before['last_attempt_date'])
        after = next(r for r in self.records.csv('revision-queue.csv') if r['item_id'] == item)
        self.assertEqual(int(after['review_stage']), stage)
        self.assertEqual(after['next_review_date_ist'], due)

    def test_failed_validation_after_commit_retries_without_duplicate_history(self):
        self.journal.save(self.session, 'validation-crash', self.payload())
        coach = load_coach(self.root)
        with patch('services.bridge.load_coach', return_value=coach), patch.object(coach, 'validate', side_effect=OSError('After commit crash')):
            with self.assertRaises(OSError):
                end_session(self.records, self.journal, self.session)
        before = (self.root / 'tracking/revision-history.csv').read_bytes()
        end_session(self.records, self.journal, self.session)
        self.assertEqual(before, (self.root / 'tracking/revision-history.csv').read_bytes())

    def test_overlapping_same_day_attempts_never_become_delayed(self):
        self.journal.save(self.session, 'first', self.payload())
        self.journal.save(self.session, 'second', self.payload())
        end_session(self.records, self.journal, self.session)
        events = self.records.events()[-2:]
        self.assertEqual([e['review_kind'] for e in events], ['diagnostic', 'immediate_correction'])

    def test_empty_session_and_conflicting_submit_do_not_mutate_history(self):
        before = (self.root/'tracking/revision-history.csv').read_bytes()
        with self.assertRaises(ValueError):
            end_session(self.records, self.journal, self.session)
        self.journal.save(self.session, 'token', self.payload())
        with self.assertRaises(ValueError):
            self.journal.save(self.session, 'token', dict(self.payload(), answer='Changed answer'))
        self.assertEqual(before, (self.root/'tracking/revision-history.csv').read_bytes())


if __name__ == '__main__':
    unittest.main()
