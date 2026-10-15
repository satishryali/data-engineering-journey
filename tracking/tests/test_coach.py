import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('coach', REPO / 'tracking/coach.py')
coach = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coach)


def review(**changes):
    event = {'review_id': 'R-test-001', 'attempt_id': 'A-test-001', 'item_id': 'SQL-001',
             'topic_ids': ['sql.join.preservation'], 'attempt_date_ist': '2026-10-20',
             'review_kind': 'delayed', 'result': 'independent', 'score': 3,
             'help_used': False, 'notes_used': False, 'hints_used': 0,
             'evidence': 'tools/sql/exercises/001-join-preservation/attempt.sql#test-attempt'}
    event.update(changes)
    return event


class SchedulingTests(unittest.TestCase):
    def test_intervals_use_actual_review_date_not_missed_due_date(self):
        self.assertEqual(coach.schedule(0, '2026-10-16', review(), '2026-10-15'),
                         (1, '2026-10-23'))
        self.assertEqual(coach.schedule(4, '2026-10-16', review(), '2026-10-15'),
                         (4, '2026-11-19'))

    def test_unknown_and_immediate_are_not_retention(self):
        event = review(score=None, result='unknown', help_used=None, notes_used=None, hints_used=None)
        self.assertEqual(coach.schedule(None, None, event), (None, None))
        self.assertIsNone(event['help_used'])
        self.assertEqual(coach.schedule(2, '2026-10-22', review(review_kind='immediate_correction')),
                         (2, '2026-10-22'))
        with self.assertRaisesRegex(ValueError, 'Same-day'):
            coach.schedule(0, '2026-10-16', review(attempt_date_ist='2026-10-15'), '2026-10-15')

    def test_first_score_two_and_assistance(self):
        self.assertEqual(coach.schedule(None, None, review(review_kind='diagnostic')), (0, '2026-10-21'))
        self.assertEqual(coach.schedule(2, '2026-10-16', review(score=2)), (2, '2026-10-27'))
        self.assertEqual(coach.schedule(2, '2026-10-16', review(result='assisted', help_used=True)), (0, '2026-10-21'))


class RecordTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / 'checkout'
        self.root.mkdir()
        for folder in ('tracking', 'Notes', 'tools', 'progress'):
            shutil.copytree(REPO / folder, self.root / folder,
                            ignore=shutil.ignore_patterns('__pycache__', 'node_modules', '.obsidian', 'tests', '*.coach-tmp', '.coach-transaction.json'))
        for name in ('START-HERE.md', 'AGENTS.md', 'README.md'):
            shutil.copy2(REPO / name, self.root / name)
        # Each test starts with a fresh index, without touching real study records.
        (self.root / 'tracking/checkpoint-index.json').write_text(coach.dump({'schema_version': 1, 'checkpoints': []}), encoding='utf-8')
        self.batch = {'checkpoint_id': 'CP-test-001', 'date_ist': '2026-10-20',
                      'kind': 'learning', 'summary': 'Fixture outcome, not real study.',
                      'evidence_ids': [review()['evidence']], 'reviews': [review()]}

    def test_duplicate_checkpoint_and_review_prevention(self):
        before_time = (self.root / 'tracking/study-log.csv').read_bytes()
        self.assertTrue(coach.record(self.root, self.batch))
        daily = (self.root / 'progress/session-history.md').read_bytes()
        self.assertFalse(coach.record(self.root, self.batch))
        self.assertEqual((self.root / 'progress/session-history.md').read_bytes(), daily)
        self.assertEqual(len(coach.read_csv(self.root, 'tracking/revision-history.csv')[1]), 1)
        self.assertEqual((self.root / 'tracking/study-log.csv').read_bytes(), before_time)
        duplicate = copy.deepcopy(self.batch)
        duplicate['checkpoint_id'] = 'CP-test-002'
        with self.assertRaisesRegex(ValueError, 'already checkpointed'):
            coach.record(self.root, duplicate)
        self.assertIn('Validated', coach.validate(self.root))

    def test_unknown_fields_remain_unknown_and_mapping_does_not_transfer_scores(self):
        self.batch['reviews'] = [review(result='unknown', score=None, help_used=None,
                                        hints_used=None, notes_used=None, extra_context={'unknown': None})]
        queue_before = {r['item_id']: r for r in coach.read_csv(self.root, 'tracking/revision-queue.csv')[1]}
        coach.record(self.root, self.batch)
        row = coach.read_csv(self.root, 'tracking/revision-history.csv')[1][0]
        event = json.loads(row['event_json'])
        self.assertIsNone(event['help_used'])
        self.assertIsNone(event['score'])
        self.assertIsNone(event['extra_context']['unknown'])
        after = {r['item_id']: r for r in coach.read_csv(self.root, 'tracking/revision-queue.csv')[1]}
        self.assertEqual(queue_before['sql.join.preservation'], after['sql.join.preservation'])
        self.assertEqual(after['SQL-001']['next_review_date_ist'], queue_before['SQL-001']['next_review_date_ist'])

    def test_invalid_mapping_and_setup_outcomes_rejected_before_writes(self):
        original = (self.root / 'tracking/revision-history.csv').read_bytes()
        self.batch['reviews'][0]['topic_ids'] = ['py.dict.access']
        with self.assertRaisesRegex(ValueError, 'mapping'):
            coach.record(self.root, self.batch)
        self.assertEqual((self.root / 'tracking/revision-history.csv').read_bytes(), original)
        self.batch['kind'] = 'setup'
        with self.assertRaisesRegex(ValueError, 'Setup cannot'):
            coach.record(self.root, self.batch)

    def test_mistake_recurrence_counts_distinct_attempts_and_preserves_unknowns(self):
        entry = copy.deepcopy(coach.read_json(self.root, 'tracking/mistakes.json')['mistakes'][0])
        entry['cause']['extra_unknown'] = None
        items = []
        coach.upsert_mistake(items, entry)
        coach.upsert_mistake(items, entry)
        self.assertEqual(items[0]['recurrence_count'], entry['recurrence_count'])
        incoming = copy.deepcopy(entry)
        incoming['observations'] = [dict(entry['observations'][0], attempt_id='new-attempt', observed_date_ist='2026-10-16')]
        coach.upsert_mistake(items, incoming)
        self.assertEqual(items[0]['recurrence_count'], entry['recurrence_count'] + 1)
        self.assertEqual(items[0]['first_observed'], '2026-10-15')
        self.assertEqual(items[0]['latest_observed'], '2026-10-16')
        self.assertIsNone(items[0]['cause']['extra_unknown'])

    def test_interrupted_write_recovers_without_duplicate_events(self):
        replace = coach.os.replace
        calls = []
        def interrupted(source, target):
            calls.append(target)
            if len(calls) == 2:
                raise OSError('simulated interruption')
            return replace(source, target)
        with patch.object(coach.os, 'replace', side_effect=interrupted):
            with self.assertRaises(OSError):
                coach.record(self.root, self.batch)
        self.assertTrue((self.root / coach.JOURNAL).exists())
        self.assertTrue(coach.recover(self.root))
        self.assertFalse(coach.recover(self.root))
        self.assertFalse(coach.record(self.root, self.batch))
        self.assertEqual(len(coach.read_csv(self.root, 'tracking/revision-history.csv')[1]), 1)
        self.assertIn('Validated', coach.validate(self.root))

    def test_recovery_preserves_concurrent_edits(self):
        with patch.object(coach.os, 'replace', side_effect=OSError('interruption')):
            with self.assertRaises(OSError):
                coach.record(self.root, self.batch)
        queue = self.root / 'tracking/revision-queue.csv'
        edited = queue.read_bytes() + b'\n'
        queue.write_bytes(edited)
        with self.assertRaisesRegex(ValueError, 'Concurrent edit'):
            coach.recover(self.root)
        self.assertEqual(queue.read_bytes(), edited)

    def test_immediate_correction_cannot_verify_mistake(self):
        mistake = copy.deepcopy(coach.read_json(self.root, 'tracking/mistakes.json')['mistakes'][0])
        mistake['status'] = 'verified_on_delayed_independent_practice'
        mistake['verification_review_id'] = 'R-test-001'
        evidence = review()['evidence']
        mistake['observations'] = [dict(mistake['observations'][0], attempt_id='new-correction-attempt', observed_date_ist='2026-10-20', evidence=evidence)]
        self.batch['mistakes'] = [mistake]
        self.batch['reviews'][0].update(item_id='SQL-002', topic_ids=['sql.count.nulls'], review_kind='immediate_correction')
        original = (self.root / 'tracking/mistakes.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'delayed independent'):
            coach.record(self.root, self.batch)
        self.assertEqual((self.root / 'tracking/mistakes.json').read_bytes(), original)

    def test_source_change_flags_only_affected_topics_without_resetting_state(self):
        prior = (self.root / 'tracking/revision-queue.csv').read_bytes()
        path = self.root / 'Notes/Python/Concepts/dictionaries.md'
        with path.open('a', encoding='utf-8') as stream:
            stream.write('\nChanged source in an isolated fixture.\n')
        changed = coach.status(self.root, '2026-10-20')['source_changes_to_inspect']
        self.assertEqual(set(changed), {'py.dict.access', 'py.dict.mutate'})
        self.assertEqual((self.root / 'tracking/revision-queue.csv').read_bytes(), prior)


if __name__ == '__main__':
    unittest.main()
