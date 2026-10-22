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
             'evidence': 'tools/sql/exercises/001-join-preservation/attempt.sql#test-attempt',
             'question': 'Synthetic test prompt, not learner evidence.', 'answer': 'Synthetic test answer.'}
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
        # Isolate assessed state from the learner's growing real history.
        fields, _ = coach.read_csv(self.root, 'tracking/revision-history.csv')
        (self.root / 'tracking/revision-history.csv').write_text(coach.csv_text(fields, []), encoding='utf-8')
        registry = coach.note_revision.sync(self.root, coach.read_json(self.root, 'tracking/topic-map.json'), '2026-10-17')
        (self.root / 'tracking/topic-map.json').write_text(coach.dump(registry), encoding='utf-8')
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
        baseline = set(coach.status(self.root, '2026-10-20')['source_changes_to_inspect'])
        prior = (self.root / 'tracking/revision-queue.csv').read_bytes()
        path = self.root / 'Notes/Python/Concepts/dictionaries.md'
        with path.open('a', encoding='utf-8') as stream:
            stream.write('\nChanged source in an isolated fixture.\n')
        changed = coach.status(self.root, '2026-10-20')['source_changes_to_inspect']
        registry = coach.read_json(self.root, 'tracking/topic-map.json')
        last = coach.note_revision.sections(path.read_text(encoding='utf-8'))[-1]['key']
        expected = next(s['topic_ids'] for f in registry['note_inventory'] if f['path'] == path.relative_to(self.root).as_posix() for s in f.get('sections', []) if s['key'] == last)
        self.assertEqual(set(changed), baseline | set(expected))
        self.assertEqual((self.root / 'tracking/revision-queue.csv').read_bytes(), prior)

    def test_new_notes_and_unmapped_sections_are_visible_and_fail_validation(self):
        path = self.root / 'Notes/Python/Concepts/new-note.md'
        path.write_text('# New learning\nA new practical concept.\n', encoding='utf-8')
        state = coach.status(self.root, '2026-10-16')
        self.assertTrue(any('new-note.md' in gap for gap in state['coverage_gaps']))
        registry = coach.note_revision.sync(self.root, coach.read_json(self.root, 'tracking/topic-map.json'), '2026-10-16')
        with self.assertRaisesRegex(ValueError, 'Map or explain'):
            coach.note_revision.check(self.root, registry)

    def test_formatting_change_does_not_flag_reassessment_or_reset_dates(self):
        baseline = coach.status(self.root, '2026-10-16')['source_changes_to_inspect']
        path = self.root / 'Notes/Python/Concepts/lists.md'
        original = path.read_text(encoding='utf-8')
        path.write_text(original.replace('Lists allow repeated values.', 'Lists allow   repeated\nvalues.'), encoding='utf-8')
        self.assertEqual(coach.status(self.root, '2026-10-16')['source_changes_to_inspect'], baseline)
        registry = coach.note_revision.sync(self.root, coach.read_json(self.root, 'tracking/topic-map.json'), '2026-10-16')
        self.assertFalse(any(t.get('needs_reassessment') for t in registry['topics']))

    def test_initial_slots_and_pending_prompts_are_not_assessments(self):
        before = (self.root / 'tracking/revision-history.csv').read_bytes()
        state = coach.status(self.root, '2026-11-20')
        self.assertEqual(state['revision_coverage']['topics_assessed'], 0)
        self.assertEqual(state['revision_coverage']['topics_practised_on_delayed_review'], 0)
        self.assertTrue(state['neglected_topics'])
        self.assertLessEqual(len(state['proposed_revision']), 2)
        proposed_ids = [s['id'] for s in state['proposed_revision']]
        self.assertLessEqual(sum(i in {t['id'] for t in coach.read_json(self.root, 'tracking/topic-map.json')['topics']} for i in proposed_ids), 1)
        self.assertEqual((self.root / 'tracking/revision-history.csv').read_bytes(), before)

    def test_delayed_state_requires_actual_independent_concept_evidence(self):
        self.batch['reviews'] = [review(item_id='sql.join.preservation', topic_ids=['sql.join.preservation'], review_kind='diagnostic')]
        coach.record(self.root, self.batch)
        later = copy.deepcopy(self.batch)
        later.update(checkpoint_id='CP-test-later', date_ist='2026-10-21',
                     evidence_ids=['tools/sql/exercises/001-join-preservation/attempt.sql#later'])
        later['reviews'] = [review(review_id='R-later', attempt_id='A-later', item_id='sql.join.preservation',
                                  topic_ids=['sql.join.preservation'], attempt_date_ist='2026-10-21', evidence=later['evidence_ids'][0])]
        coach.record(self.root, later)
        registry = coach.read_json(self.root, 'tracking/topic-map.json')
        state = coach.note_revision.snapshot(self.root, registry,
            coach.read_csv(self.root, 'tracking/revision-queue.csv')[1],
            coach.read_csv(self.root, 'tracking/revision-history.csv')[1],
            coach.read_json(self.root, 'tracking/mistakes.json'), '2026-10-21')
        self.assertEqual(state['coverage']['topics_assessed'], 1)
        self.assertEqual(state['coverage']['topics_practised_on_delayed_review'], 1)
        self.assertEqual(next(t for t in state['topics'] if t['id']=='sql.join.preservation')['state'], 'Demonstrated on delayed review')

    def test_new_content_in_previously_empty_tool_note_is_not_excluded(self):
        path = self.root / 'tools/azure/notes.md'
        path.write_text('# Azure storage\nBlob storage practical notes.\n', encoding='utf-8')
        state = coach.status(self.root, '2026-10-16')
        self.assertTrue(any('tools/azure/notes.md' in gap for gap in state['coverage_gaps']))

    def test_material_change_flags_only_mapped_concept_and_preserves_history(self):
        path = self.root / 'Notes/Python/Concepts/lists.md'
        path.write_text(path.read_text(encoding='utf-8').replace('Lists allow repeated values.', 'Lists allow repeated values. Added new material.'), encoding='utf-8')
        registry = coach.note_revision.sync(self.root, coach.read_json(self.root, 'tracking/topic-map.json'), '2026-10-16')
        flagged = [t['id'] for t in registry['topics'] if t.get('needs_reassessment')]
        self.assertEqual(flagged, ['py.list.basics'])

    def test_fenced_code_headings_are_not_learning_sections(self):
        sections = coach.note_revision.sections('# Topic\n```python\n# code comment\nprint(1)\n```\n## Next\nContent\n')
        self.assertEqual([s['heading'] for s in sections], ['Topic', 'Topic / Next'])

    def test_pending_question_cannot_be_recorded_as_a_review(self):
        self.batch['reviews'][0]['answer'] = ''
        before = (self.root / 'tracking/revision-history.csv').read_bytes()
        with self.assertRaisesRegex(ValueError, 'answered question'):
            coach.record(self.root, self.batch)
        self.assertEqual((self.root / 'tracking/revision-history.csv').read_bytes(), before)

    def test_first_concept_attempt_cannot_claim_delayed_retention(self):
        self.batch['reviews'] = [review(item_id='sql.join.preservation', topic_ids=['sql.join.preservation'])]
        with self.assertRaisesRegex(ValueError, 'prior dated attempt'):
            coach.record(self.root, self.batch)


if __name__ == '__main__':
    unittest.main()
