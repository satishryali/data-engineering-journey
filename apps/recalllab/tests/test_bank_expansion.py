"""Publication/command regressions use copies and synthetic submissions only."""
from copy import deepcopy
import ast
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from datetime import timedelta

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from services.curriculum import load_curriculum, get_problem, select_next_problem, pathway_status, validate_curriculum
from services.bank_validation import audit
from services.journal import Journal
from services.problems import Problems
from services.records import now


class BankExpansionTests(unittest.TestCase):
    def setUp(self):
        self.data=load_curriculum()

    def test_all_original_stable_problems_are_preserved(self):
        base=json.loads((Path(__file__).resolve().parents[3]/'tools/curriculum.json').read_text(encoding='utf-8'))
        by_id={p['id']:p for p in self.data['problems']}
        self.assertEqual(len(base['problems']),53)
        for original in base['problems']:
            for key,value in original.items(): self.assertEqual(by_id[original['id']][key],value)

    def test_actual_counts_do_not_treat_targets_as_problems(self):
        report=audit(self.data)
        self.assertEqual(report['published_total'],len(self.data['problems']))
        self.assertEqual(sum(report['technology_counts'].values()),len(self.data['problems']))
        self.assertEqual(report['allocated_target_total'],4200)
        self.assertEqual(report['quantity_complete'],len(self.data['problems'])>=4200 and report['remaining_target_problems']==0)

    def test_missing_fields_broken_dependencies_and_duplicates_are_reported(self):
        damaged=deepcopy(self.data)
        del damaged['problems'][0]['learning_objective']
        damaged['problems'][0]['prerequisites']=['ABSENT']
        damaged['problems'].append(deepcopy(damaged['problems'][0]))
        report=audit(damaged)
        self.assertFalse(report['schema_valid'])
        self.assertTrue(report['missing_fields'])
        self.assertTrue(report['duplicates'])
        self.assertTrue(report['broken_prerequisites_and_structure'])

    def test_numeric_task_padding_is_flagged_for_inspection(self):
        damaged=deepcopy(self.data)
        one=damaged['problems'][0]
        two=deepcopy(one)
        one['task']='Read delivery 101 and return its id.'
        two.update(id='NUMERIC-PADDING',task='Read delivery 202 and return its id.',inputs={'new':202})
        damaged['problems'].append(two)
        self.assertTrue(audit(damaged)['similar_task_candidates'])

    def test_curated_pathway_is_dependency_closed_and_smaller_than_full_bank(self):
        report=audit(self.data)
        self.assertEqual(report['job_ready_pathway_errors'],[])
        self.assertLess(report['job_ready_pathway_count'],len(self.data['problems']))
        ids=self.data['job_ready_pathway']['problem_ids']
        status=pathway_status(ids,ids,self.data)
        self.assertEqual(status['target_date'],'2027-01-20')
        self.assertEqual(len(status['assessments']),4)
        self.assertTrue(all(a['eligible'] for a in status['assessments']))
        self.assertFalse(any(a['eligible'] for a in pathway_status([],[],self.data)['assessments']))

    def test_all_three_hints_persist_as_assistance_even_when_declared_none(self):
        with tempfile.TemporaryDirectory() as folder:
            journal=Journal(Path(folder)/'journal.sqlite3')
            problem=next(p for p in self.data['problems'] if p['id']=='RLP-PY-001')
            flow=Problems(journal,catalog=self.data)
            self.assertEqual(flow.hint(problem['id']),problem['progressive_hints'][0])
            restarted=Problems(Journal(journal.path),catalog=self.data)
            self.assertEqual(restarted.hint(problem['id']),problem['progressive_hints'][1])
            attempt=restarted.submit(problem['id'],'Synthetic reviewed test approach',['none'],'# Synthetic implementation','Synthetic output')
            self.assertEqual(attempt['hints_used'],2)
            self.assertTrue(attempt['help_used'])
            reviewed=restarted.review(attempt['attempt_id'],'Test reviewer','Synthetic actual checks','Synthetic feedback',3,acceptance_checked=True)
            self.assertTrue(reviewed['correct'])
            self.assertEqual(restarted.progress('python')['independent'],0)

    def test_missing_declared_file_is_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'tools').mkdir()
            (root/'tools/curriculum.json').write_text(json.dumps({'problem_files':['tools/problem-bank/missing.json']}),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Missing published problem file'):
                load_curriculum(root)

    def test_new_authored_task_requires_exact_changed_case_for_independent_retry(self):
        data=deepcopy(self.data)
        task=next(p for p in data['problems'] if p['id']=='RLP-PY-001')
        task.pop('followup',None)
        with tempfile.TemporaryDirectory() as folder:
            journal=Journal(Path(folder)/'variants.sqlite3')
            flow=Problems(journal,catalog=data)
            first=flow.submit(task['id'],'Synthetic approach',['Copilot'],'synthetic implementation','synthetic observed result')
            flow.review(first['attempt_id'],'Test reviewer','Synthetic observed check','Synthetic correct result',3,acceptance_checked=True)
            with self.assertRaisesRegex(ValueError,'exact changed input'):
                flow.submit(task['id'],'Reconstructed',['none'],'synthetic implementation','synthetic changed result',independent_followup=True)
            with patch('services.journal.now',return_value=now()+timedelta(days=1)):
                changed=flow.submit(task['id'],'Reconstructed',['none'],'synthetic implementation','synthetic changed result',
                    independent_followup=True,changed_input='Synthetic different record 19',changed_expected='Synthetic expected record 19')
                self.assertEqual(changed['problem_snapshot']['inputs']['chosen_changed_input'],'Synthetic different record 19')
                self.assertEqual(changed['evaluation'],'manual_pending')
                flow.review(changed['attempt_id'],'Test reviewer','Verified both changed input and result','Synthetic review',3,acceptance_checked=True)
            self.assertEqual(flow.progress('python')['completed'],1)
            self.assertEqual(flow.progress('python')['independent'],1)

    def test_identical_authored_followup_requires_a_new_case(self):
        problem = next(p for p in self.data['problems']
                       if p.get('followup') and p['followup'].get('inputs') == p['inputs'])
        variant = Problems(None,catalog=self.data).independent_problem(problem['id'])
        self.assertTrue(variant['needs_chosen_input'])
        self.assertNotEqual(variant['inputs'],problem['inputs'])
        self.assertEqual(variant['verification']['kind'],'artifact_review')

    def test_beginner_dbt_and_airflow_have_real_supplied_starters(self):
        dbt=get_problem('RLP-DBT-002',self.data)
        files=dbt['inputs']['starter_files']
        seed=list(csv.DictReader(io.StringIO(files['seeds/orders_seed.csv'])))
        self.assertEqual([row['order_id'] for row in seed],['O1','O2'])
        self.assertIn("ref('orders_seed')",files['models/stg_orders.sql'])
        self.assertLess(len(str(dbt['inputs'])),1200)
        airflow=get_problem('RLP-AIRFLOW-002',self.data)
        source=airflow['inputs']['starter_files']['dags/training_delivery_log.py']
        ast.parse(source)
        self.assertIn('delivery=D1 rows=1',source)
        self.assertIn('training_delivery_log',source)
        self.assertLess(len(str(airflow['inputs'])),1200)

    def test_advanced_completion_does_not_hide_eligible_earlier_problem(self):
        small={'version':'2026.10.27.7','problems':[
            {'id':'LOW','tool_id':'demo','level':0,'prerequisites':[],'independent_prerequisites':[]},
            {'id':'HIGH','tool_id':'demo','level':10,'prerequisites':[],'independent_prerequisites':[]}]}
        self.assertEqual(select_next_problem('demo',{'HIGH'},{'HIGH'},small)['id'],'LOW')


if __name__=='__main__': unittest.main()
