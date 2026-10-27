"""Validate source-bound proposal freezes and selected nontrivial case oracles."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
BANK = HERE.parent

def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class ProposalQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = [load(f'engineering_batch{n}') for n in range(5, 13)]
        cls.wrappers = [json.loads((BANK / f'engineering-promotions{n}.json').read_text(encoding='utf-8')) for n in range(5, 13)]

    def test_all_authored_cases_match_frozen_proposals(self):
        for module, wrapper in zip(self.modules, self.wrappers):
            cases = module.base.CASES
            self.assertEqual(len(cases), len(wrapper['proposals']))
            for case, entry in zip(cases, wrapper['proposals']):
                problem = entry['problem']
                for field in ('title', 'task', 'inputs', 'expected_output', 'level'):
                    self.assertEqual(problem[field], case[field], problem['id'])
                self.assertEqual(problem['tool_id'], case['tool_id'])
                self.assertEqual(len(problem['progressive_hints']), 3)

    def test_source_hashes_and_checkpoint_hashes(self):
        for n, wrapper in zip(range(5, 13), self.wrappers):
            proposal_path = BANK / f'engineering-promotions{n}.json'
            checkpoint = json.loads((HERE / f'engineering-batch{n}-checkpoint.json').read_text(encoding='utf-8'))
            self.assertEqual(hashlib.sha256(proposal_path.read_bytes()).hexdigest(), checkpoint['proposal_sha256'])
            for tool, digest in checkpoint['source_files_sha256'].items():
                source_path = BANK / f'{tool}.json'
                current_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
                source_by_id = {p['id']: p for p in json.loads(source_path.read_text(encoding='utf-8'))['problems']}
                proposed = [entry for entry in wrapper['proposals'] if entry['problem']['tool_id'] == tool]
                if all(source_by_id[entry['original_draft_id']]['publication_status'] == 'draft' for entry in proposed):
                    self.assertEqual(current_hash, digest)
            for entry in wrapper['proposals']:
                by_id = {p['id']: p for p in json.loads((BANK / entry['source_file']).read_text(encoding='utf-8'))['problems']}
                original = by_id[entry['original_draft_id']]
                if original['publication_status'] == 'draft':
                    self.assertEqual(self.modules[0].base.digest(original), entry['original_draft_sha256'])
                else:
                    for field in ('title', 'task', 'inputs', 'expected_output', 'level'):
                        self.assertEqual(original[field], entry['problem'][field])

    def test_no_cross_batch_duplicate_contract_or_id(self):
        entries = [entry for wrapper in self.wrappers for entry in wrapper['proposals']]
        ids = [entry['problem']['id'] for entry in entries]
        self.assertEqual(len(ids), len(set(ids)))
        contracts = [self.modules[0].base.digest({field: entry['problem'][field] for field in
                     ('task', 'inputs', 'expected_output', 'acceptance_criteria', 'constraints')}) for entry in entries]
        self.assertEqual(len(contracts), len(set(contracts)))

    def test_cloud_security_access_boundaries(self):
        cases = {case['title']: case for case in self.modules[1].base.CASES}
        reader = cases['A storage reader cannot infer write access']
        self.assertEqual([r for r in reader['inputs']['requested'] if r in reader['inputs']['permissions']], reader['expected_output']['allowed'])
        scope = cases['A release inventory names every data destination']
        unapproved = sorted(set(scope['inputs']['configured']) - set(scope['inputs']['approved']))
        self.assertEqual(unapproved, scope['expected_output']['unapproved_destinations'])

    def test_integrated_customer_and_version_oracles(self):
        cases = {case['title']: case for case in self.modules[1].base.CASES}
        keys = cases['Two customer sources have local ID collisions']
        self.assertEqual(sum(len(v) for v in keys['inputs']['customers'].values()), keys['expected_output']['customers_count'])
        latest = cases['A late delete supersedes an older correction']
        version = max(latest['inputs']['arrivals'], key=lambda r: r['version'])
        self.assertEqual(version['op'], 'delete')
        self.assertEqual(version['version'], latest['expected_output']['latest_A_version'])

    def test_dbt_snowflake_and_cicd_boundary_cases(self):
        cases = {case['title']: case for case in self.modules[0].base.CASES}
        dbt = cases['An order discount is not deducted once per line']
        self.assertEqual(sum(r['amount'] for r in dbt['inputs']['lines']) - dbt['inputs']['header']['discount'], dbt['expected_output']['net'])
        snow = cases['A source namespace remains part of deletion identity']
        remaining = [r for r in snow['inputs']['target'] if (r['source'], r['id']) != (snow['inputs']['delete']['source'], snow['inputs']['delete']['id'])]
        self.assertEqual(sum(r['amount'] for r in remaining), snow['expected_output']['remaining_total'])
        ci = cases['Parallel checks preserve a bounded connection budget']
        self.assertEqual(ci['inputs']['available_connections'] // ci['inputs']['connections_per_worker'], ci['expected_output']['maximum_safe_workers'])

    def test_model_quality_and_airflow_oracles(self):
        cases = {case['title']: case for case in self.modules[2].base.CASES}
        model = cases['A repeated order line is detected by a composite key']
        duplicate = [(r['order'], r['line']) for r in model['inputs']['lines']]
        self.assertEqual(duplicate.count(tuple(model['expected_output']['duplicate_identity'])), 2)
        quality = cases['A daily total reconciles to accepted detail only']
        accepted = sum(r['amount'] for r in quality['inputs']['rows'] if r['status'] == 'accepted')
        self.assertEqual(accepted, quality['expected_output']['expected_accepted_total'])
        airflow = cases['More workers than database connections is unsafe']
        maximum = airflow['inputs']['available_connections'] // airflow['inputs']['connections_per_worker']
        self.assertEqual(maximum, airflow['expected_output']['maximum_safe_workers'])
        self.assertFalse(airflow['expected_output']['proposal_safe'])

    def test_stock_model_transfer_conservation(self):
        cases = {case['title']: case for case in self.modules[3].base.CASES}
        transfer = cases['Independent stock ledger reconciles transfers and returns']
        original = sum(transfer['inputs']['opening'].values())
        received = sum(e['units'] for e in transfer['inputs']['events'] if e['kind'] in ('receipt', 'return'))
        self.assertEqual(original + received, transfer['expected_output']['enterprise_P1'])
        self.assertEqual(sum(transfer['expected_output']['closing'].values()), transfer['expected_output']['enterprise_P1'])

    def test_quality_and_orchestration_batch9(self):
        cases = {case['title']: case for case in self.modules[4].base.CASES}
        quality = cases['A fulfilment report cannot ship more units than ordered']
        self.assertEqual(quality['inputs']['shipped']['O1'] - quality['inputs']['ordered']['O1'], quality['expected_output']['O1_excess'])
        orchestration = cases['A report fan-in waits for both regional loaders']
        edges = orchestration['expected_output']['required_edges']
        self.assertEqual({edge[0] for edge in edges}, set(orchestration['inputs']['loaders']))
        self.assertEqual({edge[1] for edge in edges}, {orchestration['inputs']['report']})

    def test_invoice_and_quality_batch10(self):
        cases = {case['title']: case for case in self.modules[5].base.CASES}
        invoice = cases['A credit is a separate financial event']
        self.assertEqual(invoice['inputs']['invoice']['amount'] - invoice['inputs']['credit']['amount'], invoice['expected_output']['net_receivable'])
        duplicate = cases['A duplicate detection preserves source line numbers']
        observed = [r['line'] for r in duplicate['inputs']['rows'] if r['id'] == duplicate['expected_output']['duplicate_id']]
        self.assertEqual(observed, duplicate['expected_output']['source_lines'])

    def test_final_advanced_and_early_oracles(self):
        early = {case['title']: case for case in self.modules[6].base.CASES}
        shipment = early['One shipment can contain two order lines']
        self.assertEqual(sum(line['units'] for line in shipment['inputs']['lines']), shipment['expected_output']['shipped_units'])
        advanced = {case['title']: case for case in self.modules[7].base.CASES}
        finance = advanced['Independent financial reconciliation checks gross, credits and net']
        self.assertEqual(finance['expected_output']['gross'] - finance['expected_output']['credits'], finance['expected_output']['net'])
        model = advanced['Independent inventory fact model reconciles a two-sided transfer']
        self.assertEqual(sum(model['expected_output']['closing'].values()), model['expected_output']['enterprise_total'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
