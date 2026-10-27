"""Focused oracle checks and all-case contract/hash validation for 200 proposals."""
import ast
import csv
import hashlib
import importlib.util
import io
import json
from datetime import datetime,timedelta,timezone
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('batch4',Path(__file__).with_name('engineering_batch4.py'))
bank=importlib.util.module_from_spec(spec);spec.loader.exec_module(bank)

class CaseQA(unittest.TestCase):
    def case(self,title):return next(c for c in bank.base.CASES if c['title']==title)
    def test_all200_match_authored_contracts(self):
        data=json.loads((bank.base.OUT/'engineering-promotions4.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data['proposals']),200)
        authored={c['title']:c for c in bank.base.CASES};self.assertEqual(len(authored),200)
        for item in data['proposals']:
            p=item['problem'];c=authored[p['title']]
            for key in ('task','inputs','expected_output','level'):self.assertEqual(p[key],c[key])
    def test_original_draft_hashes_or_published_contracts(self):
        data=json.loads((bank.base.OUT/'engineering-promotions4.json').read_text(encoding='utf-8'))
        files={}
        for item in data['proposals']:
            f=item['source_file']
            if f not in files:files[f]={p['id']:p for p in json.loads((bank.base.OUT/f).read_text(encoding='utf-8'))['problems']}
            current=files[f][item['original_draft_id']]
            if current['publication_status']=='draft':self.assertEqual(bank.base.digest(current),item['original_draft_sha256'])
            else:
                for field in ('title','task','inputs','expected_output'):self.assertEqual(current[field],item['problem'][field])
    def test_utf8_key_bytes(self):
        c=self.case('A key has a maximum encoded length');i=c['inputs']
        bad=[s for s in i['keys'] if len(s.encode('utf-8'))>i['maximum_bytes']]
        self.assertEqual(bad,c['expected_output']['rejected'])
    def test_multiline_csv_records(self):
        c=self.case('CSV embedded newlines do not create extra business records')
        rows=list(csv.DictReader(io.StringIO(c['inputs']['csv'])))
        self.assertEqual(len(rows),c['expected_output']['data_records'])
        self.assertEqual(rows[0]['note'],c['expected_output']['A_note'])
    def test_weighted_average(self):
        c=self.case('Weighted averages need their denominators');rows=c['inputs']['stores']
        actual=sum(Decimal(r['average'])*r['count'] for r in rows)/sum(r['count'] for r in rows)
        self.assertEqual(format(actual,'.2f'),c['expected_output']['overall_average'])
    def test_transfer_conservation(self):
        c=self.case('Transfer movements pair two locations without creating stock');i=c['inputs']
        end=dict(i['opening']);end[i['transfer']['from']]-=i['transfer']['units'];end[i['transfer']['to']]+=i['transfer']['units']
        self.assertEqual(end,c['expected_output']['ending']);self.assertEqual(sum(end.values()),sum(i['opening'].values()))
    def test_allocated_revenue_failure(self):
        c=self.case('A rollup over a many-to-many bridge preserves weight sums');i=c['inputs']
        amount=sum(Decimal(r['weight'])*i['sale_amount'] for r in i['links'])
        self.assertEqual(format(amount,'.2f'),c['expected_output']['allocated_total'])
    def test_rounding_stages(self):
        c=self.case('Currency rounding occurs at the declared stage');values=list(map(Decimal,c['inputs']['line_amounts']))
        line_first=sum(v.quantize(Decimal('.01'),rounding=ROUND_HALF_UP) for v in values)
        final_first=sum(values).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
        self.assertEqual(format(line_first,'.2f'),c['expected_output']['required_total'])
        self.assertEqual(format(final_first,'.2f'),c['expected_output']['round_after_sum_total'])
    def test_twenty_five_hour_interval(self):
        c=self.case('A timezone-aware interval can span a nonstandard local clock duration');i=c['inputs']
        a=datetime.fromisoformat(i['interval_start']);b=datetime.fromisoformat(i['interval_end'])
        self.assertEqual((b-a).total_seconds()/3600,c['expected_output']['duration_hours'])
        selected=[r['id'] for r in i['events'] if a<=datetime.fromisoformat(r['at'])<b]
        self.assertEqual(selected,c['expected_output']['selected'])
    def test_syntax_check_fixture(self):
        c=self.case('A syntax check fails before packaging malformed source')
        with self.assertRaises(SyntaxError):ast.parse(c['inputs']['app_py'])
    def test_regional_encoding(self):
        c=self.case('A malformed regional encoding has an explicit partial outcome')
        north=bytes.fromhex(c['inputs']['regions']['north']['hex']).decode('utf-8')
        rows=list(csv.DictReader(io.StringIO(north)))
        self.assertEqual(sum(int(r['amount']) for r in rows),c['expected_output']['north_total'])
        with self.assertRaises(UnicodeDecodeError):bytes.fromhex(c['inputs']['regions']['south']['hex']).decode('utf-8')
    def test_margin_units(self):
        c=self.case('A line-margin report preserves price and cost units');rows=c['inputs']['lines']
        revenue=sum(r['units']*r['unit_price'] for r in rows);cost=sum(r['units']*r['unit_cost'] for r in rows)
        self.assertEqual(revenue,c['expected_output']['revenue']);self.assertEqual(cost,c['expected_output']['cost']);self.assertEqual(revenue-cost,c['expected_output']['margin'])
    def test_regional_timezones(self):
        c=self.case('Regional files share one explicit business-date conversion');i=c['inputs'];totals={}
        ist=timezone(timedelta(hours=5,minutes=30))
        for rows in i['files'].values():
            for r in rows:
                day=datetime.fromisoformat(r['at']).astimezone(ist).date().isoformat();totals[day]=totals.get(day,0)+r['amount']
        self.assertEqual(totals,c['expected_output']['daily_totals'])
    def test_multi_source_fulfillment(self):
        c=self.case('Independent multi-source fulfillment keeps namespace and history');i=c['inputs'];rows=[]
        for source,orders in i['orders'].items():
            for o in orders:
                shipped=sum(s['units'] for s in i['shipments'] if s['source']==source and s['order']==o['id'])
                rows.append({'source':source,'order':o['id'],'ordered':o['units'],'shipped':shipped,'outstanding':o['units']-shipped})
        self.assertEqual(rows,c['expected_output']['rows'])
    def test_finance_conversion(self):
        c=self.case('Independent finance reconciliation preserves currencies and credits');i=c['inputs'];result={}
        for invoice in i['invoices']:
            credit=sum(Decimal(r['amount']) for r in i['credits'] if r['invoice']==invoice['id'])
            value=Decimal(invoice['amount'])-credit
            if invoice['currency']=='USD':value*=Decimal(i['usd_inr_rate'])
            result[invoice['id']]=format(value,'.2f')
        self.assertEqual(result,c['expected_output']['net_inr_by_invoice'])
        self.assertEqual(format(sum(map(Decimal,result.values())),'.2f'),c['expected_output']['net_inr_total'])
    def test_manifest_hash(self):
        path=bank.base.OUT/'engineering-promotions4.json'
        checkpoint=json.loads((bank.base.OUT/'authors/engineering-batch4-checkpoint.json').read_text(encoding='utf-8'))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),checkpoint['proposal_sha256'])

if __name__=='__main__':unittest.main(verbosity=2)
