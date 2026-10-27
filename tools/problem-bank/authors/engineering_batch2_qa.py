"""Independent checks of deterministic fixture/oracle consistency.

These tests validate authored cases, not learner work or cloud execution.
"""
import importlib.util
from collections import Counter
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
import subprocess
import sys
import unittest

spec=importlib.util.spec_from_file_location('batch2',Path(__file__).with_name('engineering_batch2.py'))
bank=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bank)

class FixtureOracleTests(unittest.TestCase):
    def case(self,tool,title):
        return next(c for c in bank.CASES if c['tool_id']==tool and c['title']==title)

    def test_required_identifiers(self):
        c=self.case('data-quality','A whitespace-only key is missing under this contract')
        bad=[r['row'] for r in c['inputs']['rows'] if not (r['order_id'] or '').strip()]
        self.assertEqual(bad,c['expected_output']['failing_rows'])

    def test_zero_and_missing_units(self):
        c=self.case('data-quality','Zero units and missing units are different')
        good=[r['id'] for r in c['inputs']['rows'] if type(r['units']) is int and r['units']>=0]
        self.assertEqual(good,c['expected_output']['passing_ids'])

    def test_source_scoped_duplicates(self):
        c=self.case('data-quality','Duplicate business keys ignore delivery sequence numbers')
        counts=Counter((r['source'],r['event']) for r in c['inputs']['rows'])
        self.assertEqual([list(k) for k,n in counts.items() if n>1],c['expected_output']['duplicate_business_keys'])
        self.assertEqual(len(counts),c['expected_output']['distinct_business_events'])

    def test_multiple_failures(self):
        c=self.case('data-quality','A row can violate two rules')
        issues={}
        for r in c['inputs']['rows']:
            reasons=[]
            if r['id'] is None:reasons.append('id_missing')
            if r['amount']<0:reasons.append('amount_negative')
            if reasons:issues[str(r['row'])]=reasons
        self.assertEqual(issues,c['expected_output']['issues'])

    def test_join_multiplication(self):
        c=self.case('data-quality','A parent present twice is a cardinality failure')
        rows=[(o,d) for o in c['inputs']['orders'] for d in c['inputs']['customers'] if o['customer']==d['id']]
        self.assertEqual(len(rows),c['expected_output']['would_be_joined_row_count'])

    def test_exact_cents(self):
        c=self.case('data-quality','Reconciliation uses exact cents')
        source=sum(map(Decimal,c['inputs']['source_amounts']))
        target=sum(map(Decimal,c['inputs']['target_amounts']))
        self.assertEqual(str(source-target),c['expected_output']['difference'])

    def test_manifest(self):
        c=self.case('data-quality','An unlisted temporary file does not complete a region')
        self.assertEqual(sorted(set(c['inputs']['expected'])-set(c['inputs']['delivered'])),c['expected_output']['missing'])

    def test_schema_required_fields(self):
        c=self.case('data-quality','A missing optional column is compatible but a missing key is not')
        required=set(c['inputs']['contract']['required'])
        self.assertFalse(required-set(c['inputs']['schemas']['A']))
        self.assertEqual(sorted(required-set(c['inputs']['schemas']['B'])),c['expected_output']['B']['missing_required'])

    def test_quality_publication_gate(self):
        c=self.case('data-quality','A quality gate preserves the last good report')
        blocked=any(r['severity']=='block' and not r['passed'] for r in c['inputs']['checks'])
        self.assertTrue(blocked)
        self.assertEqual(c['inputs']['published_before'],c['expected_output']['published_after'])

    def test_rejection_denominators(self):
        c=self.case('data-quality','A replay should not inflate the rejection rate denominator')
        rows=c['inputs']['delivery_rows']
        unique={r['event']:r for r in rows}
        self.assertEqual(len(rows),c['expected_output']['delivery_rows'])
        self.assertEqual(len(unique),c['expected_output']['distinct_events'])
        self.assertEqual(sum(not r['valid'] for r in rows),1)

    def test_fixed_clock_boundary(self):
        c=self.case('data-quality','A fixed clock removes a midnight flaky test')
        start=datetime.fromisoformat(c['inputs']['loaded_at'])
        now=datetime.fromisoformat(c['inputs']['assessment_at'])
        self.assertEqual((now-start).total_seconds()/60,c['expected_output']['age_minutes'])
        self.assertGreater(((now+timedelta(seconds=1))-start).total_seconds()/60,c['inputs']['maximum_age_minutes'])

    def test_corrected_assessment_link(self):
        c=self.case('data-quality','A correction links to the prior failed quality report')
        self.assertEqual(c['inputs']['correction']['replaces'],c['inputs']['original']['assessment_id'])
        self.assertEqual(c['inputs']['correction']['replaces'],c['expected_output']['Q2_replaces'])

    def test_ist_boundary(self):
        c=self.case('data-quality','UTC midnight is not the IST day boundary')
        ist=timezone(timedelta(hours=5,minutes=30))
        actual={r['id']:datetime.fromisoformat(r['utc']).astimezone(ist).date().isoformat() for r in c['inputs']['events']}
        self.assertEqual(actual,c['expected_output']['business_dates'])

    def test_distribution_sample_sizes(self):
        c=self.case('data-quality','Distribution warnings need enough observations')
        self.assertLess(sum(c['inputs']['samples']['small'].values()),50)
        self.assertEqual(sum(c['inputs']['samples']['large'].values()),100)
        change=abs(Decimal('0.9')-Decimal('0.1'))
        self.assertEqual(format(change,'.2f'),c['expected_output']['large_north_share_change'])

    def test_sample_uniqueness_limit(self):
        c=self.case('data-quality','A sampled uniqueness check misses an unsampled duplicate')
        full=Counter(r['key'] for r in c['inputs']['rows'])
        sample=Counter(r['key'] for r in c['inputs']['rows'] if r['position'] in c['inputs']['sample_positions'])
        self.assertEqual([k for k,n in full.items() if n>1],c['expected_output']['full_duplicate_keys'])
        self.assertEqual([k for k,n in sample.items() if n>1],[])

    def test_cross_partition_uniqueness(self):
        c=self.case('data-quality','A changed partition still needs a cross-partition key check')
        counts=Counter(r['key'] for r in c['inputs']['unchanged_partition']+c['inputs']['changed_partition'])
        self.assertEqual([k for k,n in counts.items() if n>1],c['expected_output']['global_duplicate_keys'])

    def test_order_grain_total(self):
        c=self.case('data-modelling','A header amount cannot be summed once per line')
        self.assertEqual(sum(r['amount'] for r in c['inputs']['headers']),c['expected_output']['order_revenue'])
        self.assertEqual(len(c['inputs']['lines']),c['expected_output']['line_count'])

    def test_promotion_allocation(self):
        c=self.case('data-modelling','Two promotions require a declared allocation rule')
        links=c['inputs']['promotion_links']
        self.assertEqual(sum(Decimal(r['weight']) for r in links),Decimal(1))
        actual={r['promotion']:format(Decimal(100)*Decimal(r['weight']),'.2f') for r in links}
        self.assertEqual(actual,c['expected_output']['promotion_revenue'])

    def test_stock_units(self):
        c=self.case('data-modelling','Case quantities retain original units')
        factors={r['unit']:r['factor_to_each'] for r in c['inputs']['conversion']}
        self.assertEqual(sum(r['quantity']*factors[r['unit']] for r in c['inputs']['receipts']),c['expected_output']['quantity_each'])

    def test_half_open_history(self):
        c=self.case('data-modelling','A region change at midnight has one valid version')
        actual={}
        for e in c['inputs']['events']:
            matched=[r for r in c['inputs']['history'] if r['customer']==e['customer'] and r['from']<=e['at'] and (r['to'] is None or e['at']<r['to'])]
            self.assertEqual(len(matched),1)
            actual[e['id']]=matched[0]['region']
        self.assertEqual(actual,c['expected_output']['event_regions'])

    def test_ending_balances(self):
        c=self.case('data-modelling','Month-end balances are not monthly transaction sums')
        latest={}
        for r in sorted(c['inputs']['snapshots'],key=lambda r:r['date']):latest[r['account']]=r['balance']
        self.assertEqual(latest,c['expected_output']['month_end_by_account'])
        self.assertEqual(sum(latest.values()),c['expected_output']['combined_balance'])

    def test_historical_fx(self):
        c=self.case('data-modelling','A historical exchange rate is part of lineage')
        rates={r['date']:r for r in c['inputs']['rates']}
        actual={r['id']:format(Decimal(r['usd'])*Decimal(rates[r['date']]['rate']),'.2f') for r in c['inputs']['sales']}
        self.assertEqual(actual,c['expected_output']['inr_by_sale'])

    def test_shell_stream_fixture_program(self):
        c=self.case('shell','A failure on stderr must not enter the data report')
        result=subprocess.run([sys.executable,'-c',c['inputs']['program_py']],capture_output=True,text=True,check=False)
        self.assertEqual(result.stdout,c['expected_output']['stdout'])
        self.assertEqual(result.stderr,c['expected_output']['stderr'])
        self.assertEqual(result.returncode,c['expected_output']['exit_code'])

    def test_shell_failed_producer(self):
        c=self.case('shell','Pipeline status propagates a failing producer')
        result=subprocess.run([sys.executable,'-c',c['inputs']['producer_py']],capture_output=True,text=True,check=False)
        self.assertEqual(result.returncode,c['expected_output']['producer_exit'])

    def test_json_lengths(self):
        import json
        c=self.case('shell','Newlines inside JSON strings survive structured parsing')
        rows=json.loads(c['inputs']['json_text'])
        self.assertEqual({r['id']:len(r['note']) for r in rows},c['expected_output']['note_lengths'])

    def test_integrated_correction_replay(self):
        c=self.case('integrated-pipelines','A versioned correction and new order share one incremental run')
        target={r['id']:dict(r) for r in c['inputs']['target']}
        for replay in range(2):
            for r in c['inputs']['changes']:
                if r['id'] not in target or r['version']>target[r['id']]['version']:target[r['id']]=dict(r)
        self.assertEqual(sorted(target.values(),key=lambda r:r['id']),c['expected_output']['final_rows'])
        self.assertEqual(sum(r['amount'] for r in target.values()),c['expected_output']['final_total'])

    def test_proposal_validation(self):
        items,state=bank.proposals()
        self.assertEqual(len(items),200)
        self.assertEqual(bank.validate(items,state),[])

if __name__=='__main__':unittest.main(verbosity=2)
