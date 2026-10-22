import csv
from datetime import date, timedelta
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f'tracking/{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


plan = module('study_plan')
interview = module('interview')


class TargetTests(unittest.TestCase):
    def setUp(self):
        self.settings = plan.config(ROOT)

    def hours(self, start, end):
        return plan.planned(date.fromisoformat(start), date.fromisoformat(end), self.settings)

    def test_date_effective_targets_preserve_history(self):
        self.assertEqual(plan.target('2026-10-14', self.settings), 0)
        self.assertEqual(plan.target('2026-10-21', self.settings), 6)
        self.assertEqual(plan.target('2026-10-22', self.settings), 7)
        self.assertEqual(plan.target('2026-10-24', self.settings), 10)
        self.assertEqual(self.hours('2026-10-12', '2026-10-18'), 32)
        self.assertEqual(self.hours('2026-10-19', '2026-10-25'), 52)
        self.assertEqual(self.hours('2026-10-22', '2026-10-25'), 34)

    def test_ordinary_year_boundary_and_final_partial_week(self):
        self.assertEqual(self.hours('2026-10-26', '2026-11-01'), 55)
        self.assertEqual(self.hours('2026-12-28', '2027-01-03'), 55)
        self.assertEqual(self.hours('2027-01-18', '2027-01-22'), 35)
        self.assertEqual(self.hours('2026-10-22', '2027-01-22'), 729)
        self.assertEqual(plan.summary(ROOT, '2027-01-22')['weekly_target_hours'], 35)

    def test_curriculum_is_contiguous_and_csv_is_only_a_generated_plan(self):
        rows = plan.roadmap_rows(ROOT)
        with (ROOT / 'plan/weekly-learning-plan.csv').open(encoding='utf-8', newline='') as stream:
            generated = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 13)
        previous = date(2026, 10, 21)
        for row, actual in zip(rows, generated):
            start, end = date.fromisoformat(row['start_date_ist']), date.fromisoformat(row['end_date_ist'])
            self.assertEqual(start, previous + timedelta(days=1))
            self.assertEqual(start.weekday(), 3)
            self.assertEqual((end - start).days, 6)
            self.assertEqual(self.hours(start.isoformat(), end.isoformat()), row['target_hours'])
            self.assertEqual(actual, {k: str(v) for k, v in row.items()})
            self.assertEqual(row['status'], 'planned')
            previous = end
        self.assertEqual(previous, date(2027, 1, 20))

    def test_only_completed_dated_intervals_count_and_activities_need_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'tracking').mkdir()
            (root / 'tracking/study-targets.json').write_text(json.dumps(self.settings), encoding='utf-8')
            fields = ['session_id', 'study_date_ist', 'topic', 'start_time_ist', 'end_time_ist', 'elapsed_minutes', 'status', 'notes']
            out = io.StringIO()
            writer = csv.writer(out)
            writer.writerow(fields)
            for ident, day, topic, state in [('a', '2026-10-22', 'Python', 'completed'),
                                            ('b', '2026-10-22', 'Revision SQL', 'completed'),
                                            ('c', '2026-10-22', 'Interview SQL', 'completed'),
                                            ('d', '2026-10-22', 'Python', 'running'),
                                            ('e', '2026-10-22', 'Python', 'needs_confirmation'),
                                            ('f', '2026-10-23', 'Python', 'completed')]:
                writer.writerow([ident, day, topic, day+'T10:00:00+05:30', day+'T11:00:00+05:30' if state=='completed' else '', 60 if state=='completed' else '', state, 'fixture'])
            path = root / 'tracking/study-log.csv'
            path.write_text(out.getvalue(), encoding='utf-8')
            before = path.read_bytes()
            result = plan.summary(root, '2026-10-22')
            self.assertEqual(result['confirmed_today_hours'], 3)
            self.assertEqual(result['confirmed_week_hours'], 3)
            self.assertEqual(result['remaining_today_hours'], 4)
            self.assertEqual(result['closed_day_shortfall_hours'], 18)
            self.assertEqual(result['confirmed_hours_by_explicit_activity'], {'other/unclassified': 1, 'revision': 1, 'interview': 1})
            self.assertEqual(path.read_bytes(), before)


class InterviewTests(unittest.TestCase):
    def test_assessment_metadata_round_trips_through_existing_checkpoint_records(self):
        coach = module('coach')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in ('tracking', 'Notes', 'tools', 'progress'):
                shutil.copytree(ROOT / folder, root / folder,
                                ignore=shutil.ignore_patterns('__pycache__', '.obsidian', 'tests', '*.coach-tmp', '.coach-transaction.json'))
            for name in ('START-HERE.md', 'AGENTS.md', 'README.md'):
                shutil.copy2(ROOT / name, root / name)
            old_history = coach.read_csv(root, 'tracking/revision-history.csv')[1]
            old_time = (root / 'tracking/study-log.csv').read_bytes()
            evidence = 'tools/sql/exercises/002-counting-orders/attempt.sql#interview-fixture'
            rubric = {'question_id': 'INT-SQL-001', 'correctness': 2, 'reasoning': 2,
                      'independence': 1, 'troubleshooting': None, 'communication': 2}
            batch = {'checkpoint_id': 'CP-test-interview-metadata', 'date_ist': '2026-10-22',
                     'kind': 'learning', 'summary': 'Synthetic isolated fixture, not learner evidence.',
                     'evidence_ids': [evidence], 'reviews': [{
                         'review_id': 'REV-test-interview', 'attempt_id': 'ATT-test-interview',
                         'item_id': 'SQL-002', 'topic_ids': ['sql.count.nulls'],
                         'attempt_date_ist': '2026-10-22', 'review_kind': 'application',
                         'result': 'assisted', 'score': 1, 'help_used': True,
                         'notes_used': None, 'hints_used': 1, 'evidence': evidence,
                         'question': 'Fixture query task', 'answer': 'Fixture submitted query',
                         'assessment': rubric}]}
            self.assertTrue(coach.record(root, batch))
            self.assertFalse(coach.record(root, batch))
            saved = coach.read_csv(root, 'tracking/revision-history.csv')[1]
            self.assertEqual(saved[:-1], old_history)
            self.assertEqual(json.loads(saved[-1]['event_json'])['assessment'], rubric)
            self.assertEqual((root / 'tracking/study-log.csv').read_bytes(), old_time)
            self.assertIn('Validated', coach.validate(root))

    def test_all_categories_have_prompts_and_selector_never_returns_answers(self):
        bank = interview.load(ROOT)
        self.assertEqual({q['category'] for q in bank}, set(interview.CATEGORIES))
        for q in bank:
            shown = interview.present(bank, q['id'])
            self.assertNotIn('answer', shown)
            self.assertNotIn('solution', shown)
            self.assertNotIn('hints', shown)
            self.assertNotIn('item_id', shown)
        with self.assertRaisesRegex(ValueError, 'Unknown question'):
            interview.present(bank, 'missing')

    def test_embedded_answer_and_duplicate_ids_are_rejected(self):
        bank = json.loads((ROOT / 'tracking/interview/questions.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'tracking/interview').mkdir(parents=True)
            path = root / 'tracking/interview/questions.json'
            bank['questions'][0]['answer'] = 'Must not be exposed'
            path.write_text(json.dumps(bank))
            with self.assertRaisesRegex(ValueError, 'answers do not belong'):
                interview.load(root)
            del bank['questions'][0]['answer']
            bank['questions'].append(bank['questions'][0])
            path.write_text(json.dumps(bank))
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                interview.load(root)


if __name__ == '__main__':
    unittest.main()
