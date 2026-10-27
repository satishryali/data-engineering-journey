"""Targeted authored-fixture QA; never executes cloud work or learner code."""
import importlib.util
import json
from datetime import datetime
from pathlib import Path
import subprocess
import sys
import unittest

spec=importlib.util.spec_from_file_location('batch3',Path(__file__).with_name('engineering_batch3.py'))
bank=importlib.util.module_from_spec(spec);spec.loader.exec_module(bank)

class CaseQA(unittest.TestCase):
    def case(self,title):return next(c for c in bank.base.CASES if c['title']==title)
    def test_all146_proposals_match_authored_fixtures(self):
        proposals=json.loads((bank.base.OUT/'engineering-promotions3.json').read_text(encoding='utf-8'))['proposals']
        self.assertEqual(len(proposals),146)
        authored={c['title']:c for c in bank.base.CASES}
        self.assertEqual(len(authored),146)
        for item in proposals:
            p=item['problem'];c=authored[p['title']]
            for field in ('task','inputs','expected_output','level'):
                self.assertEqual(p[field],c[field],p['id']+': '+field)
    def test_all146_published_ids_retain_case_contract(self):
        proposals=json.loads((bank.base.OUT/'engineering-promotions3.json').read_text(encoding='utf-8'))['proposals']
        loaded={}
        for item in proposals:
            path=item['source_file']
            if path not in loaded:loaded[path]={p['id']:p for p in json.loads((bank.base.OUT/path).read_text(encoding='utf-8'))['problems']}
            original=item['problem'];current=loaded[path][original['id']]
            self.assertEqual(current['publication_status'],'published')
            for field in ('title','task','inputs','expected_output','level'):
                self.assertEqual(current[field],original[field])
    def test_returns_oracle(self):
        c=self.case('Returns use a separately declared fact grain');i=c['inputs'];e=c['expected_output']
        self.assertEqual(i['sale']['amount']-sum(r['amount'] for r in i['returns']),e['net_amount'])
        self.assertEqual(i['sale']['units']-sum(r['units'] for r in i['returns']),e['net_units'])
    def test_distinct_counts_not_additive(self):
        c=self.case('A distinct-customer aggregate is not additive across stores');rows=c['inputs']['visits']
        self.assertEqual(len({r['customer'] for r in rows}),c['expected_output']['enterprise_distinct'])
        self.assertEqual(sum(len({r['customer'] for r in rows if r['store']==s}) for s in {r['store'] for r in rows}),3)
    def test_dst_oracle(self):
        c=self.case('DST repeated local times need explicit offsets');events=c['inputs']['events']
        a,b=[datetime.fromisoformat(r['at']) for r in events]
        self.assertEqual((b-a).total_seconds()/60,c['expected_output']['elapsed_minutes'])
    def test_capacity_units(self):
        c=self.case('Decimal storage units differ from binary capacity units');i=c['inputs']
        self.assertEqual(i['required_bytes']-i['allocated']['value']*i['allocated']['bytes_per_unit'],c['expected_output']['shortfall_bytes'])
    def test_telemetry_lag(self):
        c=self.case('Telemetry arrival delay differs from data delivery delay');i=c['inputs']
        done=datetime.fromisoformat(i['delivery_completed']);seen=datetime.fromisoformat(i['telemetry_received'])
        self.assertEqual((seen-done).total_seconds()/60,c['expected_output']['telemetry_lag_minutes'])
        self.assertLess(done,datetime.fromisoformat(i['deadline']))
    def test_successful_empty_command(self):
        c=self.case('A command can succeed with an empty result')
        r=subprocess.run([sys.executable,'-c',c['inputs']['program_py']],capture_output=True,text=True,check=False)
        self.assertEqual(r.stdout,c['expected_output']['stdout']);self.assertEqual(r.returncode,0)
    def test_build_context_bytes(self):
        c=self.case('A smaller build context retains all required files');i=c['inputs']
        self.assertEqual(sum(i['context_bytes'][name] for name in i['required_files']),c['expected_output']['required_source_bytes'])
    def test_latest_business_version(self):
        c=self.case('Source version order differs from ingestion order')
        latest=max(c['inputs']['arrivals'],key=lambda r:r['version'])
        self.assertEqual(latest['amount'],c['expected_output']['current_amount'])

if __name__=='__main__':unittest.main(verbosity=2)
