"""Curriculum contract tests: actual totals, bounded progression and evidence gates."""
from copy import deepcopy
from contextlib import closing
from pathlib import Path
import sqlite3
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from services import curriculum as c


class CurriculumTests(unittest.TestCase):
    def setUp(self): self.data = c.load_curriculum()

    def test_published_bank_is_valid_and_original_folder_ids_survive(self):
        self.assertEqual(c.validate_curriculum(self.data), [])
        original = {p.name for p in (c.REPO_ROOT / 'tools').iterdir() if p.is_dir() and (p/'README.md').exists()}
        self.assertTrue(original <= {t['id'] for t in self.data['technologies']})
        self.assertEqual([m['date'] for m in self.data['milestones']],
                         ['2026-11-15','2026-12-06','2026-12-27','2027-01-20'])

    def test_every_technology_has_bounded_start_and_explicit_unpublished_advanced_stages(self):
        for t in self.data['technologies']:
            with self.subTest(tool=t['id']):
                problems = c.published_problems(t['id'], self.data)
                self.assertGreaterEqual(len(problems), 1)
                self.assertEqual(problems[0]['level'], 0)
                self.assertEqual(t['stages'][-1]['status'], 'published' if any(p['level']==10 for p in problems) else 'planned')
                self.assertEqual(t['published_total'], len(problems))
                for p in problems:
                    self.assertTrue(p['progressive_hints'])
                    if p.get('followup'):
                        if not p['followup'].get('task') or p['inputs'] == p['followup'].get('inputs'):
                            from services.problems import Problems
                            self.assertTrue(Problems(None,catalog=self.data).independent_problem(p['id'])['needs_chosen_input'])
                        else:
                            self.assertNotEqual(p['inputs'],p['followup']['inputs'])

    def test_counts_are_actual_not_stage_targets_or_duplicate_events(self):
        counts = c.progress_counts('python', ['RLP-PY-001','RLP-PY-001','other'], ['RLP-PY-001','RLP-PY-002'], self.data)
        self.assertEqual((counts['completed'],counts['independent'],counts['total']), (1,1,len(c.published_problems('python',self.data))))
        self.assertEqual(c.overall_progress([], [], self.data)['completed'],0)

    def test_selection_is_sequential_and_cross_tool_prerequisites_apply(self):
        self.assertEqual(c.select_next_problem('python', curriculum=self.data)['id'], 'RLP-PY-001')
        next_python=c.select_next_problem('python',['RLP-PY-001'],curriculum=self.data)
        self.assertTrue(c.prerequisites_met(next_python,['RLP-PY-001'],[],self.data))
        self.assertEqual(next_python['level'],1)
        self.assertFalse(c.prerequisites_met(c.get_problem('RLP-PYSPARK-001',self.data),[],[],self.data))
        foundations = [f'RLP-PY-{i:03d}' for i in range(1,8)] + [f'RLP-SQL-{i:03d}' for i in range(1,6)]
        self.assertEqual(c.select_next_problem('pyspark',foundations,curriculum=self.data)['id'],'RLP-PYSPARK-001')

    def test_unknown_ids_or_assisted_diagnostic_do_not_accelerate(self):
        self.assertEqual(c.prerequisite_coverage(['unknown'],self.data),set())
        self.assertEqual(c.select_next_problem('python',['RLP-PY-003'],[],self.data)['id'],'RLP-PY-001')
        self.assertEqual(c.select_next_problem('python',[],['RLP-PY-003'],self.data)['id'],'RLP-PY-001')

    def test_independent_diagnostic_waives_skills_without_inventing_completions(self):
        done=['RLP-PY-003']
        self.assertEqual(c.diagnostic_problem('python',self.data)['id'],'RLP-PY-003')
        next_problem=c.select_next_problem('python',done,done,self.data)
        self.assertNotIn(next_problem['id'],{'RLP-PY-001','RLP-PY-002','RLP-PY-003'})
        self.assertTrue(c.prerequisites_met(next_problem,done,done,self.data))
        counts=c.progress_counts('python',done,done,self.data)
        self.assertEqual((counts['completed'],counts['independent']),(1,1))

    def test_independent_prerequisite_cannot_be_satisfied_by_assisted_completion(self):
        task=c.get_problem('RLP-PY-002',self.data)
        task['independent_prerequisites']=['RLP-PY-001']
        self.assertFalse(c.prerequisites_met(task,['RLP-PY-001'],[],self.data))
        self.assertTrue(c.prerequisites_met(task,['RLP-PY-001'],['RLP-PY-001'],self.data))

    def test_cycles_missing_prerequisites_and_level_jumps_fail_validation(self):
        invalid=deepcopy(self.data)
        invalid['problems'][0]['prerequisites']=['RLP-PY-002']
        self.assertTrue(any('cyclic' in e for e in c.validate_curriculum(invalid)))
        invalid=deepcopy(self.data)
        invalid['problems'][1]['level']=4
        self.assertTrue(any('bridge' in e for e in c.validate_curriculum(invalid)))
        invalid['problems'][1]['prerequisites']=['missing']
        self.assertTrue(any('unknown prerequisite' in e for e in c.validate_curriculum(invalid)))

    def test_prompt_excludes_hidden_verifier_cases_and_future_metadata(self):
        prompt=c.learner_prompt(c.get_problem('RLP-SQL-001',self.data))
        self.assertNotIn('verification',prompt)
        self.assertNotIn('followup',prompt)
        self.assertNotIn('diagnostic_covers',prompt)
        self.assertIn('expected_output',prompt)

    def test_reference_queries_pass_every_supplied_sql_fixture(self):
        queries=[
            'SELECT sale_id, amount FROM sales ORDER BY sale_id',
            'SELECT sale_id, amount FROM sales WHERE amount >= 25 ORDER BY sale_id',
            'SELECT COUNT(*) AS sale_count FROM sales',
            'SELECT COALESCE(SUM(amount),0) AS total_amount FROM sales',
            'SELECT customer_id,SUM(amount) AS total_amount FROM sales GROUP BY customer_id ORDER BY customer_id',
            'SELECT sale_id,name,amount FROM sales JOIN customers USING(customer_id) ORDER BY sale_id',
            'SELECT c.customer_id,COUNT(s.sale_id) AS sale_count FROM customers c LEFT JOIN sales s USING(customer_id) GROUP BY c.customer_id ORDER BY c.customer_id',
            'SELECT c.customer_id,COUNT(s.sale_id) AS sale_count,COALESCE(SUM(s.amount),0) AS total_amount FROM customers c LEFT JOIN sales s USING(customer_id) GROUP BY c.customer_id ORDER BY c.customer_id']
        originals=[c.get_problem(f'RLP-SQL-{number:03d}',self.data) for number in range(1,9)]
        for p, query in zip(originals,queries):
            for case in p['verification']['cases']:
                with self.subTest(problem=p['id'],fixture=case['setup']):
                    with closing(sqlite3.connect(':memory:')) as db:
                        db.executescript(case['setup'])
                        rows=db.execute(query)
                        self.assertEqual([list(r) for r in rows],case['expected'])
                        self.assertEqual([r[0] for r in rows.description],case['expected_columns'])


if __name__ == '__main__': unittest.main()
