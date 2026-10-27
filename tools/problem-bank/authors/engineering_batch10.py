"""One additional case per level in modelling, quality and Airflow."""
import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('engineering_base10', Path(__file__).with_name('engineering_batch2.py'))
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.CASES = []
C = base.C

C('data-modelling','One invoice row has an invoice identity',0,'Identify the grain and business key of the supplied invoice record.',{'invoice':{'invoice_id':'I1','customer':'C1','amount':100}},{'grain':'one invoice','business_key':'invoice_id'},'Do not assume this single invoice row is one customer.')
C('data-modelling','A credit is a separate financial event',1,'Represent the supplied linked credit without changing the original invoice.',{'invoice':{'id':'I1','amount':100},'credit':{'id':'C1','invoice':'I1','amount':20}},{'gross_invoice':100,'credit_amount':20,'net_receivable':80},'Preserve both invoice and credit identities.')
C('data-modelling','Two credits cannot exceed the linked invoice',2,'Check the business relationship before producing a net-invoice view.',{'invoice':{'id':'I1','amount':100},'credits':[{'id':'C1','amount':60},{'id':'C2','amount':50}]},{'credit_total':110,'over_credited':True,'excess':10},'Do not clip the net amount to zero without reporting the invalid credit relationship.')
C('data-modelling','An invoice line tax is computed at declared grain',3,'Calculate invoice tax from two taxable line amounts under the supplied policy.',{'lines':[{'id':1,'taxable':50},{'id':2,'taxable':20}],'tax_rate':'0.10','policy':'Apply rate to total taxable amount.'},{'taxable_total':70,'tax':'7.00'},'Do not apply an order-level tax twice after joining lines to an invoice header.')
C('data-modelling','A payment file links to a separate invoice file',4,'Reconcile supplied payment references against known invoice IDs.',{'invoices':[{'id':'I1','amount':100}],'payments':[{'id':'P1','invoice':'I1','amount':40},{'id':'P2','invoice':'I9','amount':20}]},{'matched_payments':['P1'],'unmatched_payments':['P2'],'applied_amount':40},'Retain P2 as an exception; do not attach it to I1.')
C('data-modelling','An invoice correction uses the higher approved version',5,'Build a current invoice model from raw versions and one replay.',{'raw':[{'id':'I1','version':1,'amount':100},{'id':'I1','version':2,'amount':90}],'replay_version':2},{'current_amount':90,'current_invoice_count':1,'retained_raw_versions':2},'Do not sum both versions or create a second current invoice on replay.')
C('data-modelling','A failed payment load leaves invoice state reconcilable',6,'Recover from a partial payment batch while keeping source payment identities.',{'invoice_amount':100,'target_payments':[{'id':'P1','amount':40}],'source_batch':[{'id':'P1','amount':40},{'id':'P2','amount':20}]},{'final_applied':60,'remaining':40,'P1_target_rows':1},'Do not append P1 again during recovery.')
C('data-modelling','A backdated credit changes historical net balance',7,'Apply a late credit to its effective invoice period.',{'invoice':{'id':'I1','day':1,'amount':100},'credit':{'id':'C1','effective_day':1,'arrival_day':3,'amount':20}},{'corrected_day1_net':80,'day3_new_invoice_amount':0},'Keep arrival and business-effective dates distinct.')
C('data-modelling','A preaggregate cannot reconstruct payment chronology',8,'Assess a total-paid aggregate against a first-payment-time question.',{'payments':[{'at':1,'amount':40},{'at':2,'amount':20}],'stored_aggregate':{'total_paid':60}},{'aggregate_sufficient_for_first_payment':False,'first_payment_at':1},'Do not invent the first timestamp from an amount total.')
C('data-modelling','An invoice export release keeps its currency label',9,'Validate a proposed change against a consumer expecting amount and currency.',{'consumer_columns':['invoice_id','amount','currency'],'candidate_columns':['invoice_id','amount'],'sample_amount':100},{'compatible':False,'missing_columns':['currency']},'A number without its currency is ambiguous to the consumer.')
C('data-modelling','Independent receivables model reconciles invoices and payments',10,'Implement an executable invoice-payment-credit model with correction and rerun.',{'invoice':{'id':'I1','amount':100},'payments':[{'id':'P1','amount':40}],'credits':[{'id':'C1','amount':20}]},{'remaining_receivable':40,'post_replay_remaining':40},'Show schema, event identity, actual query, correction/replay, invalid-reference test and consumer evidence.')

C('data-quality','A file with only a header is visibly empty',0,'Classify a confirmed present file under the supplied source contract.',{'file_exists':True,'csv':'order_id,amount\n'},{'status':'valid_empty','data_rows':0},'A missing file must not be reported as this valid empty delivery.')
C('data-quality','A malformed decimal is not a valid zero',1,'Validate the supplied amount texts.',{'amounts':['0.00','N/A'],'decimal_policy':'Dot decimal with two fractional digits.'},{'valid':['0.00'],'invalid':['N/A']},'Do not coerce N/A to zero to make a total computable.')
C('data-quality','A duplicate detection preserves source line numbers',2,'Identify all rows sharing the same business key.',{'rows':[{'line':2,'id':'O1'},{'line':3,'id':'O2'},{'line':4,'id':'O1'}]},{'duplicate_id':'O1','source_lines':[2,4]},'Report physical source lines rather than output array offsets.')
C('data-quality','An accepted-only summary excludes quarantined rows',3,'Reconcile a report to accepted input only.',{'accepted':[{'id':'A','amount':10}],'quarantined':[{'id':'B','amount':20}],'report_total':30},{'correct_total':10,'report_valid':False},'A numeric parse may succeed for quarantined B, but its failed status still excludes publication.')
C('data-quality','A file schema check catches duplicate header names',4,'Validate an incoming supplier header before typed parsing.',{'header':'sku,units,units','required':['sku','units']},{'schema_valid':False,'duplicate_columns':['units']},'Choosing the first or last units column silently changes meaning.')
C('data-quality','A target checksum check follows the actual write',5,'Verify the supplied target observation against the source ledger.',{'source_ids':['A','B'],'observed_target_ids':['A'],'write_status':'success'},{'delivery_verified':False,'missing_target_ids':['B']},'A success return code is not enough to prove full target contents.')
C('data-quality','A repair does not erase its earlier failed assertion',6,'Reconcile before-and-after test evidence for one corrected row.',{'attempt1':{'id':'A','status':'failed','reason':'bad_amount'},'attempt2':{'id':'A','status':'passed'}},{'current_status':'passed','failed_attempt_retained':True},'The correction changes current status but not historical evidence.')
C('data-quality','A correction must share a known source identity',7,'Validate a supplied correction against retained raw order IDs.',{'known_orders':['O1'],'correction':{'order':'O9','amount':12}},{'correction_applied':False,'unknown_order':'O9'},'Do not create a new O9 order through a correction-only channel.')
C('data-quality','An approximate percentile cannot enforce a hard maximum',8,'Assess a percentile summary against an all-row latency limit.',{'latency_seconds':[1,1,1,100],'reported_p50':1,'maximum_allowed':10},{'all_rows_pass':False,'violating_values':[100]},'A central percentile can hide a severe outlier.')
C('data-quality','A quality incident lists exact affected outputs',9,'Map an invalid rule version to published artifacts.',{'outputs':[{'id':'P1','rule':'v1'},{'id':'P2','rule':'v2-bad'},{'id':'P3','rule':'v2-bad'}]},{'affected_output_ids':['P2','P3'],'unaffected_output_ids':['P1']},'Do not mark every output bad simply because the current rule is bad.')
C('data-quality','Independent test suite rejects both key and amount defects',10,'Build a runnable contract suite for the supplied valid and invalid order rows.',{'rows':[{'id':'A','amount':'10.00'},{'id':None,'amount':'5.00'},{'id':'B','amount':'bad'}]},{'accepted_ids':['A'],'key_fail_rows':[2],'amount_fail_rows':[3]},'Supply actual test runs, clear exception outputs, rerun safety and a changed input challenge.')

C('airflow','A DAG identifier is distinct from its Python filename',0,'Read the supplied file metadata and name the DAG.',{'file':'daily_orders.py','dag_id':'warehouse_orders'},{'dag_id':'warehouse_orders'},'A file name alone is not the scheduler DAG identifier.')
C('airflow','A task without a run has no completion evidence',1,'Classify the supplied training DAG inventory.',{'task_ids':['extract','load'],'dag_runs':[]},{'tasks_defined':2,'completed_runs':0},'A graph definition is not a run result.')
C('airflow','A task dependency is directional',2,'Inspect the supplied two-task edge and identify which task waits.',{'edge':['extract','load']},{'upstream':'extract','downstream':'load'},'The inverse edge would make extraction wait for loading.')
C('airflow','A branch result names only one chosen path',3,'Route the supplied zero-invalid quality result.',{'invalid_count':0,'branches':['publish','quarantine']},{'chosen':'publish','unchosen':'quarantine'},'Do not run both branches for a single exclusive decision.')
C('airflow','A cross-DAG dependency matches the same interval',4,'Check whether the supplied upstream success satisfies the report run.',{'upstream':{'day':'2026-10-19','state':'success'},'report_day':'2026-10-20'},{'dependency_satisfied':False},'Successful work for yesterday does not satisfy today.')
C('airflow','A load task and report task share one committed artifact',5,'Validate the supplied artifact handoff for a logical run.',{'load':{'run':'R1','artifact_digest':'A'},'report':{'run':'R1','artifact_digest':'B'}},{'handoff_valid':False,'mismatch':'artifact_digest'},'Matching run labels cannot repair a changed artifact identity.')
C('airflow','A failed callback cannot mark the business run successful',6,'Inspect supplied task and callback results.',{'task_state':'failed','failure_callback_state':'success','published_report':False},{'business_run_success':False,'callback_observed':True},'The callback succeeding merely records/handles failure.')
C('airflow','A repaired prior interval should not trigger an unrelated day',7,'Select the exact logical run for a late file.',{'late_file_business_day':'2026-10-20','current_scheduler_day':'2026-10-23'},{'repair_run_day':'2026-10-20','unrelated_current_day_replayed':False},'Use data interval identity, not arrival-day convenience.')
C('airflow','Dynamic mapping preserves one status per source file',8,'Assess a mapped loader result before fan-in publication.',{'files':['a.csv','b.csv','c.csv'],'states':['success','failed','success']},{'all_sources_succeeded':False,'failed_files':['b.csv']},'Two out of three successes cannot publish a complete three-file report.')
C('airflow','A new DAG release checks an old queued run contract',9,'Gate supplied v2 activation against a still-pending v1 run.',{'queued':{'run':'R1','contract':'v1'},'candidate':'v2','compatibility_test':'missing'},{'safe_to_activate_without_review':False,'pending_run':'R1'},'A queued run may execute under the newly loaded code; establish its behavior deliberately.')
C('airflow','Independent DAG proves data result after a retry',10,'Implement a tiny scheduled pipeline with one injected extract failure and a successful bounded retry.',{'orders':[{'id':'A','amount':10}],'first_extract':'temporary_error','second_extract':'success'},{'attempts':2,'published_total':10,'logical_rows':1},'Provide actual task states and persisted report, not only a green DAG screenshot.')

def main():
    previously_proposed = set()
    for number in (8, 9):
        path = base.OUT / f'engineering-promotions{number}.json'
        if path.exists():
            previously_proposed.update(item['original_draft_id'] for item in json.loads(path.read_text(encoding='utf-8'))['proposals'])
    items, states = base.proposals(exclude_ids=previously_proposed)
    errors = base.validate(items, states)
    if errors:
        raise ValueError(errors)
    for item in items:
        item['problem']['authoring']['batch'] = 'engineering-batch10'
    counts = {tool: sum(item['problem']['tool_id'] == tool for item in items) for tool in states}
    wrapper = {'schema_version': 1, 'proposal_version': '2026.10.27.engineering-batch10',
               'publication_status': 'unregistered_proposals', 'proposals': items,
               'counts': {'proposed_promotions': len(items), 'published_added': 0, 'by_technology': counts},
               'validation': {'structural_errors': errors, 'runtime_claim': 'Learner implementations remain unverified.'}}
    path = base.OUT / 'engineering-promotions10.json'
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(wrapper, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    temporary.replace(path)
    checkpoint = {'state': 'prepared_not_published', 'proposed': len(items), 'published_added': 0,
                  'counts': counts, 'proposal_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                  'source_files_sha256': {tool: hashlib.sha256(state['path'].read_bytes()).hexdigest() for tool, state in states.items()},
                  'errors': errors}
    (base.OUT / 'authors/engineering-batch10-checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(checkpoint, indent=2))

if __name__ == '__main__':
    main()
