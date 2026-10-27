"""Case-specific promotions. Never changes registered problem files.

Every case supplies a technical counterexample, a concrete expected result and
an acceptance contract. Only currently draft IDs can be proposed for promotion.
The parent publisher reviews and atomically merges the proposals in a versioned
release. Publishing this proposal file does not publish any learning problem.
"""
import hashlib
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'tools/problem-bank'
CASES = []

def C(tool, title, level, task, fixture, expected, constraint):
    CASES.append(dict(tool_id=tool,title=title,level=level,task=task,inputs=fixture,
                      expected_output=expected,constraint=constraint))

C('data-modelling','Optional shipment date is not an empty string',1,
  'Define and populate an order table that distinguishes an unshipped order from a shipped order. Show a query counting unshipped orders.',
  {'orders':[{'order_id':'O1','ordered_on':'2026-10-20','shipped_on':None},{'order_id':'O2','ordered_on':'2026-10-20','shipped_on':'2026-10-21'}]},
  {'unshipped_order_ids':['O1'],'unshipped_count':1},'Represent unknown dates as null; do not invent a shipment date or use an empty date string.')
C('data-modelling','Customer identity cannot be inferred from display name',1,
  'Model these customers and orders so equal display names do not merge two customers. Produce spend by customer ID.',
  {'customers':[{'customer_id':'C1','name':'North Store'},{'customer_id':'C2','name':'North Store'}], 'orders':[{'order_id':'O1','customer_id':'C1','amount':10},{'order_id':'O2','customer_id':'C2','amount':20}]},
  {'spend_by_customer':{'C1':10,'C2':20},'customer_rows':2},'Names are mutable labels, and each supplied customer ID is a different business entity.')
C('data-modelling','A header amount cannot be summed once per line',2,
  'Separate order headers from order lines and calculate both order revenue and line count without multiplying the header amount.',
  {'headers':[{'order_id':'O1','amount':30},{'order_id':'O2','amount':10}], 'lines':[{'order_id':'O1','line_id':1},{'order_id':'O1','line_id':2},{'order_id':'O2','line_id':1}]},
  {'order_revenue':40,'order_count':2,'line_count':3},'The header amount is an order-level measure. Do not split it arbitrarily across lines.')
C('data-modelling','A repeated local order number is not a global key',2,
  'Define keys for a merged order relation and retain both supplied records. Demonstrate that a replay of source A order 1 is rejected or updates only that source record.',
  {'orders':[{'source':'A','order_id':'1','amount':12},{'source':'B','order_id':'1','amount':19}], 'replay':{'source':'A','order_id':'1','amount':12}},
  {'logical_order_count':2,'amount_total':31,'source_A_order_count':1},'Source namespaces are independent; the same number from B is not a duplicate of A.')
C('data-modelling','Two promotions require a declared allocation rule',3,
  'Represent a sale linked to two promotions and report allocated revenue by promotion using the supplied weights.',
  {'sales':[{'sale_id':'S1','amount':100}], 'promotion_links':[{'sale_id':'S1','promotion':'A','weight':'0.75'},{'sale_id':'S1','promotion':'B','weight':'0.25'}]},
  {'promotion_revenue':{'A':'75.00','B':'25.00'},'allocated_total':'100.00'},'Weights for a sale must sum to 1. Reject a second test where they sum to 1.25.')
C('data-modelling','Order date and ship date play different roles',3,
  'Model one date dimension used for both order and shipment dates. Produce separate counts by each role.',
  {'orders':[{'order_id':'O1','order_date':'2026-10-20','ship_date':'2026-10-21'},{'order_id':'O2','order_date':'2026-10-21','ship_date':None}]},
  {'ordered_by_date':{'2026-10-20':1,'2026-10-21':1},'shipped_by_date':{'2026-10-21':1},'unshipped':1},'A missing ship date must not be silently mapped to the order date.')
C('data-modelling','Case quantities retain original units',4,
  'Combine two stock receipts into base units while retaining source quantities and unit identities.',
  {'receipts':[{'receipt_id':'R1','quantity':2,'unit':'case'},{'receipt_id':'R2','quantity':5,'unit':'each'}], 'conversion':[{'unit':'case','factor_to_each':12},{'unit':'each','factor_to_each':1}]},
  {'quantity_each':29,'receipt_count':2,'source_quantities_preserved':True},'A receipt with unit pallet and no conversion must be unresolved, not treated as factor 1.')
C('data-modelling','Conflicting source mappings stay unresolved',4,
  'Build a source-customer mapping and detect an ambiguous source key before joining facts.',
  {'mapping':[{'source':'A','local_id':'1','warehouse_id':'W1'},{'source':'A','local_id':'1','warehouse_id':'W2'},{'source':'B','local_id':'1','warehouse_id':'W3'}], 'facts':[{'fact_id':'F1','source':'A','local_id':'1','amount':10},{'fact_id':'F2','source':'B','local_id':'1','amount':20}]},
  {'ambiguous_keys':[['A','1']],'safe_fact_ids':['F2'],'unresolved_fact_ids':['F1']},'Do not choose an arbitrary first mapping or multiply F1 into two facts.')
C('data-modelling','A region change at midnight has one valid version',5,
  'Store customer-region history with half-open validity and enrich the two supplied events as of event time.',
  {'history':[{'customer':'C1','region':'north','from':'2026-10-01T00:00:00Z','to':'2026-10-21T00:00:00Z'},{'customer':'C1','region':'west','from':'2026-10-21T00:00:00Z','to':None}], 'events':[{'id':'E1','customer':'C1','at':'2026-10-20T23:59:59Z'},{'id':'E2','customer':'C1','at':'2026-10-21T00:00:00Z'}]},
  {'event_regions':{'E1':'north','E2':'west'},'matches_per_event':1},'The exact boundary belongs to the new version; never join both versions.')
C('data-modelling','Snapshot rows distinguish no activity from missing delivery',5,
  'Model daily ending inventory for a product when the second day has no movements but its delivery is confirmed complete.',
  {'opening':{'product':'P1','on_hand':10},'days':[{'date':'2026-10-20','complete':True,'movements':[3,-2]},{'date':'2026-10-21','complete':True,'movements':[]},{'date':'2026-10-22','complete':False,'movements':[]}]},
  {'published_snapshots':[{'date':'2026-10-20','on_hand':11},{'date':'2026-10-21','on_hand':11}],'unresolved_dates':['2026-10-22']},'An incomplete day must not acquire a fabricated complete snapshot.')
C('data-modelling','Late customer details repair one unresolved fact',6,
  'Load the fact with an explicit unresolved relationship, then apply the late customer record without changing fact identity or amount.',
  {'fact':{'fact_id':'F9','customer_source_id':'C9','amount':25},'initial_customers':[],'late_customer':{'source_id':'C9','name':'Late Customer','warehouse_key':109}},
  {'after_repair':{'fact_id':'F9','customer_key':109,'amount':25},'fact_rows':1},'Retain source customer identity so the unresolved fact can be repaired; replay the customer arrival and keep one fact.')
C('data-modelling','An overlapping historical interval blocks enrichment',6,
  'Detect an overlapping customer-history pair before publishing enriched sales. Return the conflicting interval and affected event.',
  {'history':[{'key':1,'customer':'C1','from':'2026-10-01','to':'2026-10-22'},{'key':2,'customer':'C1','from':'2026-10-21','to':None}], 'events':[{'id':'E1','customer':'C1','date':'2026-10-21'}]},
  {'conflicting_keys':[1,2],'affected_event_ids':['E1'],'publication_allowed':False},'Do not hide the overlap with DISTINCT or an arbitrary latest-row rule.')
C('data-modelling','Month-end balances are not monthly transaction sums',7,
  'Implement the supplied month-end balance rule and contrast it with an invalid sum across balance snapshots.',
  {'snapshots':[{'account':'A1','date':'2026-10-29','balance':100},{'account':'A1','date':'2026-10-31','balance':120},{'account':'A2','date':'2026-10-30','balance':50}], 'rule':'Use latest available balance on or before October 31 for each account.'},
  {'month_end_by_account':{'A1':120,'A2':50},'combined_balance':170,'invalid_snapshot_sum':270},'A2 has no October 31 row; its latest earlier balance is still included under this explicit rule.')
C('data-modelling','A historical exchange rate is part of lineage',7,
  'Convert two USD sales to INR using the supplied effective daily rates and preserve the rate identity used for each fact.',
  {'sales':[{'id':'S1','date':'2026-10-20','usd':'10.00'},{'id':'S2','date':'2026-10-21','usd':'10.00'}],'rates':[{'id':'FX1','date':'2026-10-20','rate':'80.00'},{'id':'FX2','date':'2026-10-21','rate':'81.00'}]},
  {'inr_by_sale':{'S1':'800.00','S2':'810.00'},'total_inr':'1610.00','rate_ids':{'S1':'FX1','S2':'FX2'}},'Never use the latest rate for both dates or overwrite the retained source currency amount.')
C('data-modelling','An aggregate omitting channel cannot answer channel totals',8,
  'Evaluate the supplied daily aggregate against a requested date-and-channel report. Show the smallest correct aggregate grain.',
  {'facts':[{'date':'2026-10-20','channel':'store','amount':10},{'date':'2026-10-20','channel':'web','amount':20}], 'existing_aggregate':[{'date':'2026-10-20','amount':30}],'request_fields':['date','channel','amount']},
  {'required_grain':['date','channel'],'correct_rows':[{'date':'2026-10-20','channel':'store','amount':10},{'date':'2026-10-20','channel':'web','amount':20}],'existing_aggregate_sufficient':False},'Do not invent a channel allocation from the date-only aggregate.')
C('data-modelling','A date predicate must survive aggregate reconciliation',8,
  'Create a bounded daily aggregate and compare a one-day query with raw detail. Record actual query-plan evidence if the training engine supports it.',
  {'facts':[{'date':'2026-10-20','amount':10},{'date':'2026-10-20','amount':15},{'date':'2026-10-21','amount':90}],'requested_date':'2026-10-20'},
  {'one_day_total':25,'aggregate_rows':2,'full_period_total':115},'Correctness is mandatory before any pruning or performance claim; a tiny fixture does not prove scale benefits.')

C('pipeline-reliability','A failed first read cannot create a success marker',0,
  'Run a tiny local reader with the supplied nonexistent input path and report its status without writing a success marker.',
  {'input_path':'owned_scratch/missing.csv','initial_files':[],'success_marker':'owned_scratch/SUCCESS'},
  {'status':'failed','reason':'input_missing','success_marker_exists':False},'Create only the owned scratch directory; do not read or remove unrelated files.')
C('pipeline-reliability','A header-only file is a confirmed empty delivery',1,
  'Handle the supplied present header-only input under the stated empty-delivery policy.',
  {'input_csv':'order_id,amount\n','policy':'Present and syntactically valid empty delivery succeeds with zero accepted rows.'},
  {'status':'succeeded_empty','accepted':0,'rejected':0},'A missing file remains a failure; do not map both conditions to zero success.')
C('pipeline-reliability','A second delivery reuses a committed input digest',2,
  'Apply the supplied replay policy using the source digest and committed run ledger.',
  {'ledger':[{'digest':'digest-A','state':'committed','output':'batch-A.json'}],'incoming':{'digest':'digest-A','rows':[{'id':'O1','amount':10}]},'policy':'Skip a delivery whose digest is already committed.'},
  {'action':'skip_committed','additional_target_rows':0,'ledger_entries':1},'Do not deduplicate on filename alone; a renamed file with the same digest is the same delivery.')
C('pipeline-reliability','Only a temporary failure earns another attempt',3,
  'Implement the supplied bounded retry classification over the two deterministic attempt sequences.',
  {'maximum_attempts':3,'temporary_case':['source_unavailable','ok'],'permanent_case':['required_key_missing'],'retryable':['source_unavailable']},
  {'temporary_case':{'attempts':2,'status':'succeeded'},'permanent_case':{'attempts':1,'status':'failed'}},'Use no actual sleeps in the test; inject a delay callback and record requested delays.')
C('pipeline-reliability','A truncated copy fails before transformation',4,
  'Validate a copied file against its supplied manifest size and checksum before allowing transformation.',
  {'manifest':{'file':'orders.csv','bytes':24,'sha256':'expected-digest'},'observed':{'file':'orders.csv','bytes':12,'sha256':'different-digest'},'transform_calls':0},
  {'status':'copy_invalid','transform_calls':0,'violations':['byte_count','checksum']},'Report both discrepancies and retain the copied artifact for diagnosis rather than replacing the expected manifest.')

C('data-quality','A whitespace-only key is missing under this contract',1,
  'Validate required order identifiers after trimming surrounding spaces and report defective row numbers.',
  {'rows':[{'row':1,'order_id':'O1'},{'row':2,'order_id':'   '},{'row':3,'order_id':None}],'rule':'A required identifier must contain at least one non-whitespace character.'},
  {'failing_rows':[2,3],'passing_rows':[1]},'Preserve original source values in the error report; do not rewrite source input.')
C('data-quality','Zero units and missing units are different',1,
  'Check the supplied required nonnegative integer-unit rule without relying on truthiness.',
  {'rows':[{'id':'A','units':0},{'id':'B','units':None},{'id':'C','units':-1},{'id':'D','units':2}]},
  {'passing_ids':['A','D'],'failing_ids':['B','C']},'Zero is a valid quantity; booleans are not accepted as unit integers in an additional probe.')
C('data-quality','Duplicate business keys ignore delivery sequence numbers',2,
  'Detect repeated business events using source and event ID, even when ingestion sequence differs.',
  {'rows':[{'source':'A','event':'1','sequence':100},{'source':'A','event':'1','sequence':101},{'source':'B','event':'1','sequence':102}]},
  {'duplicate_business_keys':[['A','1']],'affected_sequences':[100,101],'distinct_business_events':2},'Do not classify B event 1 as a duplicate of A event 1.')
C('data-quality','A row can violate two rules',2,
  'Run required-ID and nonnegative-amount checks and retain every applicable reason per source row.',
  {'rows':[{'row':1,'id':None,'amount':-4},{'row':2,'id':'O2','amount':5}]},
  {'issues':{'1':['id_missing','amount_negative']},'accepted_rows':[2]},'Do not stop after the first rule or count a doubly invalid row twice in the rejected-row total.')
C('data-quality','A parent present twice is a cardinality failure',3,
  'Check dimension-key uniqueness before joining the supplied orders to customer regions.',
  {'orders':[{'id':'O1','customer':'C1','amount':10}],'customers':[{'id':'C1','region':'north'},{'id':'C1','region':'west'}]},
  {'join_allowed':False,'duplicate_customer_ids':['C1'],'would_be_joined_row_count':2},'A post-join DISTINCT must not hide the ambiguous region relationship.')
C('data-quality','Reconciliation uses exact cents',3,
  'Compare source and target totals at the declared two-decimal currency precision.',
  {'source_amounts':['0.10','0.20'],'target_amounts':['0.29'],'precision':'0.01'},
  {'source_total':'0.30','target_total':'0.29','difference':'0.01','passed':False},'Do not use a broad floating-point tolerance that accepts a one-cent loss.')
C('data-quality','An unlisted temporary file does not complete a region',4,
  'Validate the required complete-file manifest against the delivered directory listing.',
  {'expected':['north.csv','south.csv'],'delivered':['north.csv','south.csv.tmp','notes.txt']},
  {'missing':['south.csv'],'unexpected':['south.csv.tmp','notes.txt'],'complete':False},'Only exact manifest filenames satisfy delivery completeness.')
C('data-quality','A missing optional column is compatible but a missing key is not',4,
  'Evaluate both schemas against the supplied versioned contract.',
  {'contract':{'required':{'order_id':'string','amount':'decimal'},'optional':{'channel':'string'}},'schemas':{'A':{'order_id':'string','amount':'decimal'},'B':{'amount':'decimal','channel':'string'}}},
  {'A':{'compatible':True},'B':{'compatible':False,'missing_required':['order_id']}},'Do not treat the absence of a nullable optional field as a broken required field.')
C('data-quality','A quality gate preserves the last good report',5,
  'Implement publication only after every blocking check passes and demonstrate the failing batch.',
  {'published_before':{'run':'good-1','total':30},'candidate':{'run':'bad-2','total':999},'checks':[{'name':'key_not_null','severity':'block','passed':False},{'name':'freshness','severity':'warn','passed':True}]},
  {'published_after':{'run':'good-1','total':30},'candidate_status':'rejected'},'Retain the failed candidate report but do not replace the published consumer artifact.')
C('data-quality','A replay should not inflate the rejection rate denominator',5,
  'Compute per-delivery quality metrics and an explicitly deduplicated business-event metric.',
  {'delivery_rows':[{'delivery':'D1','event':'E1','valid':True},{'delivery':'D1','event':'E2','valid':False},{'delivery':'D2','event':'E1','valid':True}]},
  {'delivery_rejection_rate':'1/3','distinct_event_rejection_rate':'1/2','delivery_rows':3,'distinct_events':2},'Label both denominators; do not silently switch between delivered rows and unique events.')
C('data-quality','A fixed clock removes a midnight flaky test',6,
  'Replace the supplied moving-time assumption with an injected assessment instant and test freshness at its boundary.',
  {'loaded_at':'2026-10-20T23:30:00Z','assessment_at':'2026-10-21T00:00:00Z','maximum_age_minutes':30,'boundary_rule':'Age <= 30 minutes passes.'},
  {'age_minutes':30,'passed':True,'at_one_second_later':False},'Tests must not read the current system date or sleep until a time boundary.')
C('data-quality','A correction links to the prior failed quality report',6,
  'Persist the supplied correction as a new quality assessment linked to the original failure.',
  {'original':{'assessment_id':'Q1','delivery':'D1','status':'failed','bad_key':'O1'},'correction':{'assessment_id':'Q2','delivery':'D1-corrected','replaces':'Q1','rows':[{'id':'O1','amount':10}]}},
  {'retained_assessments':['Q1','Q2'],'Q2_status':'passed','Q2_replaces':'Q1'},'Do not rewrite the historical failed assessment as if the original input had passed.')
C('data-quality','UTC midnight is not the IST day boundary',7,
  'Check the expected IST business-date assignment of the supplied UTC events.',
  {'events':[{'id':'A','utc':'2026-10-20T18:29:59Z'},{'id':'B','utc':'2026-10-20T18:30:00Z'}],'reporting_timezone':'Asia/Kolkata'},
  {'business_dates':{'A':'2026-10-20','B':'2026-10-21'}},'Use timezone-aware timestamps and include the exact boundary in a regression test.')
C('data-quality','Distribution warnings need enough observations',7,
  'Apply the supplied two-part drift rule to both samples.',
  {'baseline':{'north':90,'south':10},'samples':{'small':{'north':1,'south':9},'large':{'north':10,'south':90}},'rule':{'minimum_sample_rows':50,'absolute_share_change_greater_than':'0.50'}},
  {'small':'insufficient_sample','large':'warning','large_north_share_change':'0.80'},'A drift warning is separate from deterministic row acceptance and must not be called proof of corruption.')
C('data-quality','A sampled uniqueness check misses an unsampled duplicate',8,
  'Compare the specified sample with the full dataset and report the limitation honestly.',
  {'rows':[{'position':1,'key':'A'},{'position':2,'key':'B'},{'position':3,'key':'C'},{'position':4,'key':'C'}],'sample_positions':[1,2]},
  {'sample_duplicate_keys':[],'full_duplicate_keys':['C'],'sample_proves_global_uniqueness':False},'Do not promote a passing sample into a claim that the complete dataset is unique.')
C('data-quality','A changed partition still needs a cross-partition key check',8,
  'Validate the changed partition against retained keys in the other partition.',
  {'unchanged_partition':[{'day':'2026-10-19','key':'O1'}],'changed_partition':[{'day':'2026-10-20','key':'O1'},{'day':'2026-10-20','key':'O2'}],'key_scope':'global across days'},
  {'global_duplicate_keys':['O1'],'partition_local_duplicate_keys':[],'publication_allowed':False},'Scanning only the changed partition is insufficient for a globally unique business key.')

C('airflow','A downstream validator must not run before extraction',1,
 'Implement the supplied two-task training DAG contract and demonstrate the dependency with one run.',
 {'tasks':['extract','validate'],'required_edge':['extract','validate'],'extract_output':{'records':2}},
 {'task_order':['extract','validate'],'validate_input_records':2},'Use a supported installed Airflow version; preserve actual task-instance evidence instead of claiming that a drawn edge proves execution.')
C('airflow','A runtime input path selects the actual file',1,
 'Read the supplied runtime parameter inside a training task and return the selected record count.',
 {'files':{'a.json':[{'id':'A'}],'b.json':[{'id':'B'},{'id':'C'}]},'runs':[{'input_path':'a.json'},{'input_path':'b.json'}]},
 {'counts_by_run':[1,2]},'Do not hard-code a.json or perform the read at DAG module import time.')
C('airflow','The interval end belongs to the next run',2,
 'Build a training extraction task that filters events by the run data interval.',
 {'interval':{'start':'2026-10-20T00:00:00Z','end':'2026-10-21T00:00:00Z'},'events':[{'id':'A','at':'2026-10-20T00:00:00Z'},{'id':'B','at':'2026-10-20T23:59:59Z'},{'id':'C','at':'2026-10-21T00:00:00Z'}]},
 {'selected_ids':['A','B'],'excluded_ids':['C']},'Use a half-open [start,end) interval and record logical interval separately from actual task start time.')
C('airflow','One configured retry means at most two executions',2,
 'Configure a training task with one retry and a deterministic attempt fixture that fails once then succeeds.',
 {'airflow_retries':1,'attempt_results':['temporary_failure','ok'],'retry_delay_seconds':1},
 {'task_executions':2,'final_status':'success'},'Do not set an unbounded retry loop inside the task; use Airflow task attempt evidence.')
C('airflow','A second task run replaces its own dated result',3,
 'Make the supplied interval-specific publication idempotent and rerun the same interval task.',
 {'interval_start':'2026-10-20T00:00:00Z','records':[{'id':'O1','amount':10},{'id':'O2','amount':20}],'output_key':'daily/2026-10-20.json'},
 {'after_first_run':{'count':2,'total':30},'after_replay':{'count':2,'total':30}},'The rerun must not append two additional logical orders or overwrite the neighboring interval.')
C('airflow','Task logs may name a connection but not its password',3,
 'Configure a training task to refer to the supplied connection identity and produce a sanitized diagnostic record.',
 {'connection_id':'training_orders','fake_connection':{'host':'localhost','password':'FAKE_PASSWORD_FOR_TEST'},'run_id':'manual_test'},
 {'log_contains':['training_orders','manual_test'],'log_must_not_contain':['FAKE_PASSWORD_FOR_TEST']},'Use fake credentials only; connection resolution and logging must not commit or print a password.')
C('airflow','A missing manifest file blocks mapped processing',4,
 'Validate the manifest before expanding file-processing work in a training DAG.',
 {'manifest':['north.json','south.json'],'present_files':['north.json'],'expected_complete':True},
 {'validation_status':'failed','missing':['south.json'],'processing_task_executions':0},'Do not turn a missing regional delivery into a successful empty region.')
C('airflow','Passing an artifact reference avoids bulk task messages',4,
 'Have a producer task write the supplied rows to an owned training artifact and return a small reference for its consumer.',
 {'rows':[{'id':'A'},{'id':'B'}],'artifact_path':'owned_training/run-1/orders.json','message_contract':{'allowed':['path','record_count'],'forbidden':['rows']}},
 {'message':{'path':'owned_training/run-1/orders.json','record_count':2},'consumer_count':2},'The consumer must read the referenced artifact; do not place the complete row list in the task message.')
C('airflow','A two-day backfill writes two separate outputs',5,
 'Execute a bounded training backfill for both supplied intervals and reconcile each output.',
 {'days':{'2026-10-19':[{'id':'A','amount':5}],'2026-10-20':[{'id':'B','amount':7}]},'output_pattern':'daily/{logical_date}.json'},
 {'outputs':{'daily/2026-10-19.json':{'count':1,'total':5},'daily/2026-10-20.json':{'count':1,'total':7}}},'Do not use current wall-clock date to name historical backfill output.')
C('airflow','A pool caps active database writers',5,
 'Put four bounded training writer tasks in a pool with two slots and record observed task overlap.',
 {'writer_tasks':['load_a','load_b','load_c','load_d'],'pool_slots':2,'slots_per_task':1},
 {'all_writers_complete':True,'maximum_observed_concurrent_writers_lte':2},'Use actual task start/end evidence; task count is not the same as concurrent task count.')
C('airflow','A failed mapped item can be repaired without duplicate good output',6,
 'Reproduce one failed file task, repair that input and rerun using the stated per-file target identity.',
 {'files':{'a.json':[{'id':'A','amount':10}],'b.json':[{'id':'B','amount':'bad'}]},'corrected_b':[{'id':'B','amount':20}],'target_key':['source_file','id']},
 {'final_keys':[['a.json','A'],['b.json','B']],'total':30,'good_file_logical_rows':1},'Retain the original failing log and prove the good-file output was not duplicated.')
C('airflow','Failure reporting runs even when publication is blocked',6,
 'Configure separate publication and run-report tasks for the supplied upstream failure.',
 {'tasks':['extract','validate','publish','report'],'fixture_status':{'extract':'success','validate':'failed'},'requirements':{'publish':'must not run','report':'must run and record failure'}},
 {'publish_executed':False,'report_status':'succeeded','reported_pipeline_outcome':'failed'},'Choose supported trigger rules deliberately; a successful reporting task does not make the failed data delivery successful.')
C('airflow','A producer for the wrong interval is not ready',7,
 'Gate a consumer on completion of its matching producer interval rather than the latest successful producer run.',
 {'consumer_interval':'2026-10-20','producer_runs':[{'interval':'2026-10-19','status':'success'},{'interval':'2026-10-20','status':'failed'}]},
 {'consumer_ready':False,'required_interval':'2026-10-20'},'Do not satisfy a date-specific dependency with any historical success.')
C('airflow','Concurrent intervals must not share one mutable output name',7,
 'Repair the supplied overlapping-run output collision using a documented interval-specific artifact contract.',
 {'runs':[{'id':'R1','interval':'2026-10-19','amount':10},{'id':'R2','interval':'2026-10-20','amount':20}],'bad_output_path':'latest.json'},
 {'interval_outputs':{'2026-10-19':10,'2026-10-20':20},'cross_interval_overwrites':0},'Preserve both interval results even when the second run completes first.')
C('airflow','Empty dynamic mapping has an explicit no-data outcome',8,
 'Test an empty manifest in a bounded mapped training DAG and document installed-version behavior.',
 {'manifest':[],'empty_delivery_confirmed':True,'business_policy':'Publish a no-data outcome, never a fabricated record.'},
 {'processed_files':0,'business_outcome':'confirmed_empty','fabricated_records':0},'Record actual Airflow task states and version; do not assume an empty mapped task behaves like a one-item task.')
C('airflow','Batching must account for the last partial file group',8,
 'Replace one-task-per-file scheduling with groups of three for the supplied seven-file manifest and verify coverage.',
 {'files':['f1','f2','f3','f4','f5','f6','f7'],'maximum_files_per_group':3},
 {'groups':[['f1','f2','f3'],['f4','f5','f6'],['f7']],'group_count':3,'covered_files':7},'Each file must appear exactly once. Any scheduler-overhead claim needs a separate measured benchmark.')

C('dbt','A staging alias is the consumer contract',1,
 'Create a staging model renaming the two raw fields to the supplied names and query its schema.',
 {'raw_rows':[{'ord_no':'O1','amt':'12.50'}],'output_columns':['order_id','amount']},
 {'rows':[{'order_id':'O1','amount':'12.50'}],'columns':['order_id','amount']},'Do not retain accidental raw aliases in the public staging output; record the adapter used.')
C('dbt','A required identifier test catches a seeded null',1,
 'Configure a not-null test for the model identifier and run it on the supplied seed fixture.',
 {'model':'stg_orders','rows':[{'order_id':'O1'},{'order_id':None}],'tested_column':'order_id'},
 {'test_status':'fail','failing_rows':1},'Show the executed test result, not only a YAML declaration.')
C('dbt','An allowed-status test exposes a new upstream code',2,
 'Add an allowed-values check to the supplied staging model and show its failing value.',
 {'rows':[{'id':'O1','status':'accepted'},{'id':'O2','status':'held'}],'allowed':['accepted','cancelled']},
 {'failing_ids':['O2'],'failing_statuses':['held']},'Do not silently change held to accepted to make the test pass.')
C('dbt','A source reference must follow the selected schema',2,
 'Configure the raw source for two isolated training targets and demonstrate that each model reads its own source.',
 {'targets':{'dev':{'source_schema':'raw_dev','rows':[{'id':'D'}]},'review':{'source_schema':'raw_review','rows':[{'id':'R'}]}}},
 {'dev_output_ids':['D'],'review_output_ids':['R']},'Do not hard-code raw_dev into model SQL or copy review rows into development.')
C('dbt','A singular test returns invalid shipment rows',3,
 'Write a singular data test for shipment before ordering and run the supplied fixture.',
 {'rows':[{'id':'O1','ordered':'2026-10-20','shipped':'2026-10-21'},{'id':'O2','ordered':'2026-10-20','shipped':'2026-10-19'},{'id':'O3','ordered':'2026-10-20','shipped':None}]},
 {'failing_ids':['O2'],'test_status':'fail'},'A null shipment is allowed for an unshipped order; the test query must return violating rows.')
C('dbt','An orphan relationship test is independent of key uniqueness',3,
 'Run a relationship check for the supplied order customer IDs while retaining valid unmatched evidence.',
 {'orders':[{'id':'O1','customer_id':'C1'},{'id':'O2','customer_id':'C9'}],'customers':[{'customer_id':'C1'}]},
 {'orphan_order_ids':['O2'],'relationship_test_status':'fail'},'Do not drop O2 inside staging to hide the failing relationship.')
C('dbt','A missing mapping remains visible in the mart build',4,
 'Apply the supplied seed mapping and expose unmapped raw statuses for quality review.',
 {'orders':[{'id':'O1','raw_status':'A'},{'id':'O2','raw_status':'X'}],'mapping':[{'raw_status':'A','status':'accepted'}]},
 {'mapped':[{'id':'O1','status':'accepted'}],'unmapped_ids':['O2']},'Unmapped rows cannot be counted as accepted sales or silently disappear from reconciliation.')
C('dbt','Freshness warning and model build success are separate',4,
 'Assess source freshness at the fixed supplied instant and run a small valid model without conflating the two outcomes.',
 {'loaded_at':'2026-10-20T10:00:00Z','assessment_at':'2026-10-20T12:00:00Z','warn_after_minutes':60,'error_after_minutes':180,'rows':[{'id':'O1','amount':10}]},
 {'source_freshness':'warn','model_build':'success','output_count':1},'Capture the supported dbt artifacts and assessment instant; avoid tests using the current clock.')
C('dbt','An incremental correction updates one existing key',5,
 'Build an initial incremental relation, then apply the supplied new and corrected source rows using a unique-key contract.',
 {'initial':[{'id':'O1','amount':10},{'id':'O2','amount':20}],'next_batch':[{'id':'O1','amount':12},{'id':'O3','amount':5}]},
 {'final_rows':[{'id':'O1','amount':12},{'id':'O2','amount':20},{'id':'O3','amount':5}],'final_total':37},'A replay of next_batch must not add rows; record adapter-supported incremental strategy.')
C('dbt','An unchanged snapshot input does not create another version',5,
 'Capture the supplied customer change and repeat the exact second snapshot input.',
 {'snapshot_inputs':[[{'id':'C1','region':'north','updated_at':'2026-10-20T00:00:00Z'}],[{'id':'C1','region':'west','updated_at':'2026-10-21T00:00:00Z'}],[{'id':'C1','region':'west','updated_at':'2026-10-21T00:00:00Z'}]]},
 {'historical_versions':2,'current_region':'west'},'Record actual validity columns for the installed snapshot configuration; do not fabricate snapshot timestamps.')
C('dbt','A late correction falls inside the explicit lookback',6,
 'Implement the stated incremental lookback and compare the result with a scratch full rebuild.',
 {'last_processed_date':'2026-10-20','lookback_days':2,'target':[{'id':'O1','date':'2026-10-19','amount':10}],'source':[{'id':'O1','date':'2026-10-19','amount':14},{'id':'O2','date':'2026-10-21','amount':5}]},
 {'incremental_rows':[{'id':'O1','date':'2026-10-19','amount':14},{'id':'O2','date':'2026-10-21','amount':5}],'full_refresh_equal':True},'Keep unique-key upsert semantics across the lookback; an inclusive reread is not permission to append duplicates.')
C('dbt','A scoped full refresh must not rebuild an unrelated mart',6,
 'Select only the damaged training model for full refresh and verify the unrelated relation remains untouched.',
 {'graph':{'stg_orders':[],'fct_orders':['stg_orders'],'dim_products':[]},'damaged_model':'fct_orders','unrelated_marker':{'dim_products':'keep-marker'}},
 {'rebuilt_models':['fct_orders'],'unrelated_marker_after':'keep-marker'},'Capture actual selection output and state which dependencies already exist; do not claim no rebuild without checking.')
C('dbt','An added nullable column needs incremental/full parity',7,
 'Evolve the supplied incremental target with a nullable sales channel and compare with a full rebuild under the chosen documented schema-change policy.',
 {'old_target':[{'id':'O1','amount':10}],'new_source':[{'id':'O1','amount':10,'channel':None},{'id':'O2','amount':20,'channel':'web'}]},
 {'final_rows':[{'id':'O1','amount':10,'channel':None},{'id':'O2','amount':20,'channel':'web'}],'full_refresh_equal':True},'Do not assume the adapter backfills historical values automatically; document the observed behavior.')
C('dbt','A public model can retain the old two-column interface',7,
 'Provide a compatible v1 model and a v2 model for the supplied contract change and execute both consumer queries.',
 {'rows':[{'id':'O1','gross':100,'credit':20}],'v1_fields':['order_id','amount'],'v1_amount_definition':'gross','v2_fields':['order_id','gross_amount','net_amount']},
 {'v1':[{'order_id':'O1','amount':100}],'v2':[{'order_id':'O1','gross_amount':100,'net_amount':80}]},'Do not silently redefine the v1 amount as net revenue.')
C('dbt','An append-only optimization is wrong for source corrections',8,
 'Compare the supplied append-only proposal with the required keyed correction behavior and create a parity check.',
 {'target':[{'id':'O1','amount':10}],'source_correction':[{'id':'O1','amount':12}],'proposed_filter':'only keys not already in target'},
 {'proposal_total':10,'required_total':12,'parity_passed':False},'Measure performance only after preserving the documented correction semantics.')
C('dbt','A preaggregation must retain grouping dimensions',8,
 'Evaluate whether the supplied faster aggregate can satisfy a date-and-region mart query and implement a correct bounded alternative.',
 {'facts':[{'date':'2026-10-20','region':'north','amount':10},{'date':'2026-10-20','region':'south','amount':20}],'proposed_group_by':['date'],'required_group_by':['date','region']},
 {'correct_rows':[{'date':'2026-10-20','region':'north','amount':10},{'date':'2026-10-20','region':'south','amount':20}],'proposed_aggregate_sufficient':False},'Output parity precedes any materialization or runtime comparison.')

C('snowflake','The current schema controls an unqualified scratch table',1,
 'Use two isolated training schemas containing the supplied table name and query each with an explicit context.',
 {'schemas':{'train_a':{'orders':[{'id':'A'}]},'train_b':{'orders':[{'id':'B'}]}},'table_name':'orders'},
 {'train_a_ids':['A'],'train_b_ids':['B']},'Record active database, schema, role and warehouse; never use an existing production-like schema.')
C('snowflake','Quoted CSV descriptions occupy one column',1,
 'Load the supplied staged CSV using an explicit supported file format and inspect its fields.',
 {'csv':'id,description,amount\nO1,"blue, large",12.50\nO2,plain,5.00\n','header_rows':1},
 {'row_count':2,'O1_description':'blue, large','amount_total':'17.50'},'Keep the malformed-format failure evidence if an initial attempt splits the quoted comma.')
C('snowflake','VARIANT missing and JSON null require an explicit policy',2,
 'Extract an optional region under the stated reporting contract from both supplied JSON shapes.',
 {'json_rows':[{'id':'A','customer':{'region':'north'}},{'id':'B','customer':{'region':None}},{'id':'C','customer':{}}],'policy':'Report a missing or JSON-null region as SQL null.'},
 {'regions':{'A':'north','B':None,'C':None}},'Use supported Snowflake JSON semantics and demonstrate the actual extracted SQL values.')
C('snowflake','Flatten retains parent identity for empty line arrays',2,
 'Produce line-grain rows from the supplied nested arrays and separately account for orders with no lines.',
 {'orders':[{'id':'O1','lines':[{'sku':'P1'},{'sku':'P2'}]},{'id':'O2','lines':[]}]},
 {'line_rows':[{'order_id':'O1','sku':'P1'},{'order_id':'O1','sku':'P2'}],'orders_without_lines':['O2']},'Do not fabricate a product line for O2 or silently call the two-line output a complete two-order report.')
C('snowflake','The reporting role can read but not mutate',3,
 'Configure isolated training loader and reporter roles against one scratch relation and test the required operations.',
 {'permissions':{'loader':['insert','select'],'reporter':['select']},'attempts':[{'role':'reporter','operation':'select'},{'role':'reporter','operation':'insert'}]},
 {'reporter_select':'allowed','reporter_insert':'denied'},'Use an authorized training account; if role administration is unavailable, label local permission simulation and do not claim a real grant test.')
C('snowflake','A load report records rejected source rows',3,
 'Run a bounded training load using the supplied bad numeric record and retain its load outcome and rejection evidence.',
 {'csv':'id,amount\nO1,10.00\nO2,not-number\n','target_schema':{'id':'string','amount':'number(12,2)'},'policy':'Reject malformed numeric data; never coerce it to zero.'},
 {'malformed_id':'O2','malformed_value':'not-number','fabricated_zero_rows':0},'Record the chosen documented load error policy and actual loaded/rejected counts.')
C('snowflake','A manifest limits which staged files enter a batch',4,
 'Load only the complete files listed in the supplied daily manifest and reconcile totals.',
 {'manifest':['north.csv','south.csv'],'stage':{'north.csv':[{'id':'N1','amount':10}],'south.csv':[{'id':'S1','amount':20}],'south.csv.tmp':[{'id':'X','amount':999}]}},
 {'loaded_ids':['N1','S1'],'amount_total':30,'excluded_ids':['X']},'Do not use a broad file pattern that includes the temporary file.')
C('snowflake','Filename lineage distinguishes equal local IDs',4,
 'Load the supplied staged rows while retaining their file identity and source row position.',
 {'files':{'a.csv':[{'id':'1','amount':10}],'b.csv':[{'id':'1','amount':20}]}},
 {'rows':2,'lineage_keys':[['a.csv',1],['b.csv',1]],'amount_total':30},'A local business ID is not enough to trace the two supplied source rows.')
C('snowflake','A deterministic merge rejects ambiguous source matches',5,
 'Detect multiple source versions for one target key before applying a keyed correction.',
 {'target':[{'id':'O1','amount':10}],'source':[{'id':'O1','version':2,'amount':12},{'id':'O1','version':3,'amount':15}],'rule':'Use highest version; reject tied highest versions with conflicting values.'},
 {'target_after':[{'id':'O1','version':3,'amount':15}],'source_rows_applied':1},'Add a tied-version conflicting-value probe that blocks the merge rather than choosing an arbitrary source row.')
C('snowflake','A consumed stream batch must be reconciled with its target',5,
 'Implement a bounded stream-to-target training change application and replay the target write by its business key.',
 {'baseline':[{'id':'O1','amount':10}],'changes':[{'id':'O1','amount':12},{'id':'O2','amount':5}],'target_key':'id'},
 {'target_rows':[{'id':'O1','amount':12},{'id':'O2','amount':5}],'target_total':17,'replay_total':17},'Record actual stream consumption behavior and transaction scope; simulation cannot establish Snowflake delivery guarantees.')
C('snowflake','Reloading a renamed delivery needs business-key reconciliation',6,
 'Replay the same business records from a differently named staged file and keep one logical target record per order.',
 {'first_file':{'name':'batch_a.csv','rows':[{'id':'O1','amount':10}]},'renamed_delivery':{'name':'batch_a_copy.csv','rows':[{'id':'O1','amount':10}]}},
 {'logical_target_count':1,'logical_total':10,'delivery_files_observed':2},'Do not assume filename-based load history alone proves business-level deduplication.')
C('snowflake','Recover a bounded dropped scratch table with retention evidence',6,
 'Rehearse restoring a deliberately disposable table within configured retention and compare its fixture rows.',
 {'scratch_table':'training_restore_orders','before_drop':[{'id':'O1','amount':10}],'required_total':10},
 {'restored_ids':['O1'],'restored_total':10},'Record account-supported retention and actual recovery command. If unavailable, report the missing prerequisite instead of claiming recovery.')
C('snowflake','A late lower source version cannot undo a newer correction',7,
 'Apply changes in the supplied arrival order under a monotonic source-version rule.',
 {'initial':[{'id':'O1','version':1,'amount':10}],'arrivals':[{'id':'O1','version':3,'amount':15},{'id':'O1','version':2,'amount':12}]},
 {'final':[{'id':'O1','version':3,'amount':15}],'ignored_stale_versions':[2]},'Arrival time is not the source version; show a replay check for version 3.')
C('snowflake','A masked contact field differs by role without changing totals',7,
 'Configure a supported training masking policy on synthetic email while preserving business measures.',
 {'rows':[{'id':'C1','email':'example@example.invalid','amount':10}],'roles':['authorized','reporter'],'reporter_email':'REDACTED'},
 {'authorized_email':'example@example.invalid','reporter_email':'REDACTED','total_for_each_role':10},'Use synthetic contacts and authorized training features only; record unsupported account capabilities explicitly.')
C('snowflake','A broad projection can scan unneeded reporting fields',8,
 'Compare a required-field query with a broad projection on a bounded synthetic training table and collect actual query profile evidence.',
 {'required_fields':['id','amount'],'extra_fields':['large_payload'],'query_requirement':'sum amount by id','scale_generation':{'rows':10000,'payload_characters':1000}},
 {'result_parity_required':True,'profile_evidence_required':['query_id','rows','bytes_scanned_or_supported_scan_metric'],'fabricated_savings_allowed':False},'This exercise has no promised speedup; report observed metrics and cache conditions honestly.')
C('snowflake','A warehouse comparison must hold the query and input constant',8,
 'Run the same bounded query under two permitted training warehouse settings and create a reproducible measurement report.',
 {'query':'SELECT SUM(amount) FROM training_benchmark_orders','fixture':{'rows':10000,'amount_each':'1.00'},'trials_per_setting':2,'warehouse_settings':['permitted_small','permitted_larger']},
 {'sum_for_all_trials':'10000.00','report_fields':['setting','query_id','elapsed','cache_conditions','metering_observation']},'Use a cost-bounded authorized sandbox; do not represent synthetic prices or elapsed time as actual account cost.')

C('git','The index retains the first edit after a second working edit',1,
 'In a disposable repository, reproduce the supplied index and working-tree states and report their different file content before committing anything.',
 {'baseline_files':{'config.txt':'workers=1\n'},'setup_steps':[{'edit':'config.txt','content':'workers=2\n'},{'stage':'config.txt'},{'edit':'config.txt','content':'workers=3\n'}]},
 {'HEAD_content':'workers=1\n','index_content':'workers=2\n','working_content':'workers=3\n'},'The review must inspect all three states without discarding either edit.')
C('git','An ignore rule does not remove an already tracked artifact',1,
 'Set up the tracked fixture, add the ignore rule and show why the generated file is still tracked. Correct the tracking while preserving the local file.',
 {'committed_files':{'generated/report.csv':'id\nA\n','src.txt':'keep\n'},'new_ignore_rule':'generated/'},
 {'generated_file_tracked_after_fix':False,'generated_file_exists_locally':True,'src_tracked':True},'Do not delete the local report or untrack unrelated source files.')
C('git','Creating a branch does not create an independent uncommitted copy',2,
 'Reproduce the supplied clean baseline and uncommitted edit, create a new local branch, and identify which content is committed versus only working-tree state.',
 {'baseline_commit':{'file':'config.txt','content':'region=north\n'},'uncommitted_edit':'region=west\n','new_branch':'training-region'},
 {'new_branch_HEAD_content':'region=north\n','working_content':'region=west\n','new_commit_count':0},'Use a disposable repository and preserve the edit; do not infer that branch creation committed it.')
C('git','A moved mapping file needs its consumer reference changed',2,
 'Rename the supplied tracked mapping and update the local consumer configuration in the same reviewed change.',
 {'files':{'mapping/status.csv':'raw,status\nA,accepted\n','config.json':{'mapping':'mapping/status.csv'}},'new_mapping_path':'reference/status.csv'},
 {'tracked_mapping_path':'reference/status.csv','config_mapping':'reference/status.csv','obsolete_path_exists':False},'A rename without the configuration update is an incomplete pipeline change.')
C('git','A revert creates a new correction instead of erasing history',3,
 'Build the supplied two-commit history and undo only the faulty amount multiplier with a new local commit.',
 {'commits':[{'label':'base','files':{'rate.txt':'1\n'}},{'label':'bad','files':{'rate.txt':'10\n'}}],'desired_content':'1\n'},
 {'final_rate':'1\n','original_bad_commit_retained':True,'commits_after_revert':3},'Do not reset away the bad commit or rewrite the original two commits.')
C('git','Independent configuration changes can be reviewed in separate commits',3,
 'Separate the supplied two-file edits into two local commits with no unrelated content.',
 {'baseline':{'source.txt':'a.csv\n','timeout.txt':'10\n','unrelated.txt':'keep\n'},'edits':{'source.txt':'b.csv\n','timeout.txt':'20\n'},'required_commit_groups':[['source.txt'],['timeout.txt']]},
 {'commit_file_sets':[['source.txt'],['timeout.txt']],'unrelated_content':'keep\n'},'The final tree must contain both edits while each commit changes only its own responsibility.')
C('git','Both branches add legitimate regions to the same line',4,
 'Construct the supplied branching fixture, merge it locally, and resolve the conflict to satisfy all three regional requirements.',
 {'base':{'regions.txt':'north\n'},'branch_a':{'regions.txt':'north,west\n'},'branch_b':{'regions.txt':'north,south\n'},'required_regions':['north','west','south']},
 {'resolved_regions':['north','west','south'],'duplicate_regions':0,'conflict_markers_remaining':0},'Do not choose one branch wholesale and lose the other required region.')
C('git','A content fix follows a renamed source file',4,
 'Merge one local branch that renames the mapping with another that corrects its status value.',
 {'base':{'old/status.csv':'A,pending\n'},'rename_branch':{'rename':['old/status.csv','new/status.csv']},'fix_branch':{'old/status.csv':'A,accepted\n'}},
 {'final_files':{'new/status.csv':'A,accepted\n'},'old_path_exists':False},'Inspect the resulting tree; a clean merge status alone does not establish the required path and content.')
C('git','A cherry-picked fix must not bring an unrelated feature',5,
 'Build the supplied linear feature history and apply only its standalone correctness fix to the maintenance branch.',
 {'base':{'parse.txt':'strip=false\n','feature.txt':'off\n'},'feature_commits':[{'label':'feature','files':{'feature.txt':'on\n'}},{'label':'fix','files':{'parse.txt':'strip=true\n'}}],'maintenance_base':'base'},
 {'maintenance_files':{'parse.txt':'strip=true\n','feature.txt':'off\n'}},'Review actual changed files on maintenance; do not merge the entire feature branch.')
C('git','Two worktrees keep different branches and separate edits',5,
 'Create two disposable worktrees from the supplied baseline on distinct branches and edit only one working directory.',
 {'baseline':{'config.txt':'mode=base\n'},'branches':['task-a','task-b'],'task_a_edit':'mode=a\n'},
 {'task_a_working_content':'mode=a\n','task_b_working_content':'mode=base\n','HEADs_initially_equal':True},'Keep worktree paths under the owned training root and never reuse the journey checkout for this fixture.')
C('git','A detached local commit can be recovered by its file content',6,
 'In an owned training repository, create the supplied detached commit, leave it by checking out the baseline branch, and recover it onto a named branch.',
 {'baseline':{'recover.txt':'base\n'},'detached_commit':{'recover.txt':'valuable-fix\n'},'recovered_branch':'recovered-training-fix'},
 {'recovered_branch_content':'valuable-fix\n','baseline_branch_content':'base\n','valuable_commit_reachable':True},'Record actual local commit IDs before and after recovery; no remote or history rewriting is required.')
C('git','Aborting a conflicted merge restores the pre-merge tree',6,
 'Construct the supplied text conflict, begin the merge, then abort and verify the original branch tree.',
 {'base':{'mode.txt':'base\n'},'current_branch':{'mode.txt':'current\n'},'other_branch':{'mode.txt':'other\n'},'premerge_clean':True},
 {'post_abort_content':'current\n','merge_in_progress':False,'current_branch_unchanged':True},'Begin with the declared clean fixture so the expected abort result is unambiguous.')
C('git','A rebase must retain both timeout and worker changes',7,
 'Replay the feature branch onto the supplied updated base and resolve any conflict without losing either requirement.',
 {'base':{'config.txt':'timeout=10;workers=1\n'},'updated_base':{'config.txt':'timeout=20;workers=1\n'},'feature':{'config.txt':'timeout=10;workers=2\n'}},
 {'final_configuration':{'timeout':20,'workers':2},'feature_based_on_updated_base':True},'Use only a disposable local history; validate semantics after conflict resolution rather than treating rebase success as sufficient.')
C('git','A binary replacement needs identity and consumer evidence',7,
 'Review the supplied small binary fixture replacement through digests and a deterministic consumer check.',
 {'before_hex':'00010203','after_hex':'00010204','consumer_rule':'Last unsigned byte is the fixture format version.','expected_after_version':4},
 {'before_bytes':4,'after_bytes':4,'content_changed':True,'after_format_version':4},'Do not call a same-size replacement unchanged; create only these synthetic bytes.')
C('git','Bisect identifies the first zero-dropping transform',8,
 'Create the supplied six-commit training history and use a repeatable test to locate the first bad revision.',
 {'commits':[{'label':'c1','drop_zero':False},{'label':'c2','drop_zero':False},{'label':'c3','drop_zero':True},{'label':'c4','drop_zero':True},{'label':'c5','drop_zero':True},{'label':'c6','drop_zero':True}],'fixture_amounts':[0,2],'test_contract':'The transform retains two records, including zero.'},
 {'first_bad_label':'c3','first_bad_output_count':1,'last_good_label':'c2','last_good_output_count':2},'Map fixture labels to actual local commit IDs and retain the test command used for bisect decisions.')
C('git','A clean clone exposes an untracked mapping dependency',8,
 'Reproduce a transform configuration that references an untracked local mapping and repair repository reproducibility.',
 {'tracked_files':{'config.json':{'mapping':'mapping.csv'}},'untracked_files':{'mapping.csv':'A,accepted\n'},'consumer_requirement':'The configured mapping exists in a fresh local clone.'},
 {'initial_clean_clone_check':'fail','repaired_clean_clone_check':'pass','mapping_reproducible':True},'Use a small synthetic mapping or a tracked generation step; do not commit production lookup data.')

C('shell','Header counting must exclude a trailing blank line',1,
 'Count business data rows in the supplied simple text fixture using the stated blank-line rule.',
 {'input':'id,amount\nA,10\nB,20\n\n','rules':{'header_lines':1,'ignore_blank_lines':True}},
 {'data_rows':2},'This is a simple unquoted CSV fixture; do not claim a line counter correctly parses arbitrary multiline CSV.')
C('shell','A literal bracket in a filename is not a wildcard',1,
 'Read the supplied owned file with a literal bracketed name and prove the neighboring filename was not read.',
 {'files':{'day [1].txt':'correct\n','day 1.txt':'wrong\n'},'requested_path':'day [1].txt'},
 {'content':'correct\n','files_read':['day [1].txt']},'Use the supported shell literal-path or quoting semantics and preserve both fixtures.')
C('shell','A failure on stderr must not enter the data report',2,
 'Run the supplied tiny program and capture its two streams separately.',
 {'program_py':'import sys\nprint("rows=2")\nprint("warning=synthetic", file=sys.stderr)\n','expected_exit':0},
 {'stdout':'rows=2\n','stderr':'warning=synthetic\n','exit_code':0},'Do not concatenate stderr into a machine-readable data artifact.')
C('shell','A missing configuration value cannot resolve to the current directory',2,
 'Validate the required input-directory setting before any file scan using the supplied empty configuration.',
 {'configuration':{'INPUT_DIRECTORY':''},'current_directory_files':['unrelated.csv'],'required_setting':'INPUT_DIRECTORY'},
 {'exit_code_nonzero':True,'files_scanned':0,'error_contains':'INPUT_DIRECTORY'},'Do not substitute the working directory or print environment values unrelated to this fixture.')
C('shell','One failed file makes the batch command fail',3,
 'Process all three supplied files, retain per-file results and return an overall failure when any required input is invalid.',
 {'files':{'a.txt':'10\n','b.txt':'bad\n','c.txt':'20\n'},'rule':'Each file must contain one integer.'},
 {'statuses':{'a.txt':'pass','b.txt':'fail','c.txt':'pass'},'overall_exit_nonzero':True},'Do not stop before reporting c.txt, and do not hide b.txt failure behind the last successful command.')
C('shell','A relative output is rooted in the selected run directory',3,
 'Run the supplied bounded job twice using separate run directories and retain both outputs.',
 {'runs':[{'run_id':'R1','count':1},{'run_id':'R2','count':2}],'output_name':'result.json'},
 {'outputs':{'R1/result.json':{'count':1},'R2/result.json':{'count':2}}},'Do not change a process-global working directory in parallel workers or overwrite a shared result.json.')
C('shell','Newlines inside JSON strings survive structured parsing',4,
 'Read the supplied JSON fixture and emit only its record IDs and actual note character counts.',
 {'json_text':'[{"id":"A","note":"line1\\nline2"},{"id":"B","note":"comma, kept"}]'},
 {'ids':['A','B'],'note_lengths':{'A':11,'B':11}},'Use a structured JSON parser rather than splitting records by commas or line breaks.')
C('shell','A bounded scan rejects a parent-directory escape',4,
 'Validate supplied manifest paths against the owned scratch root before reading any file.',
 {'root':'owned_scratch','manifest':['input/a.csv','../outside.csv'],'inside_files':{'input/a.csv':'id\nA\n'}},
 {'accepted_paths':['input/a.csv'],'rejected_paths':['../outside.csv'],'outside_reads':0},'Resolve paths before checking containment; do not perform deletion or access outside the scratch root.')
C('shell','Atomic publication preserves the old file on an interrupted write',5,
 'Implement the supplied temporary-write and publish contract and inject failure before final replacement.',
 {'published_before':'count=2\n','candidate':'count=3\n','failure_point':'after_partial_temporary_write_before_replace'},
 {'published_after_failure':'count=2\n','success_marker_exists':False},'Temporary and final files must be on the same intended filesystem; preserve failure evidence in owned scratch space.')
C('shell','A run report uses observed command durations',5,
 'Wrap the supplied deterministic stage functions with an injected monotonic clock and emit elapsed durations.',
 {'clock_readings_seconds':[100.0,100.4,101.0,101.7],'stages':['extract','load']},
 {'elapsed_seconds':{'extract':0.4,'load':0.7}},'Use elapsed-time subtraction, not wall-clock formatted timestamps; permit normal numeric comparison tolerance.')
C('shell','Pipeline status propagates a failing producer',6,
 'Run the supplied failing producer through a successful consumer and ensure the wrapper reports the producer failure.',
 {'producer_py':'import sys\nprint("partial")\nsys.exit(7)\n','consumer_py':'import sys\nprint(len(sys.stdin.read()))\n'},
 {'producer_exit':7,'consumer_exit':0,'wrapper_exit_nonzero':True},'Use the actual supported shell status semantics; a successful consumer is not proof that upstream work succeeded.')
C('shell','Cleanup is limited to the current run manifest',6,
 'Delete only the owned temporary files listed for R1 and report the remaining files.',
 {'owned_root':'owned_scratch','files':['R1.tmp','R2.tmp','important.txt'],'R1_manifest':['R1.tmp']},
 {'deleted':['R1.tmp'],'remaining':['R2.tmp','important.txt']},'Validate containment and exact manifest membership before deletion; never use a broad recursive wildcard.')
C('shell','An invalid UTF-8 sequence is not silently dropped',7,
 'Decode the supplied byte fixtures under the explicit UTF-8 policy and retain a diagnostic for invalid input.',
 {'valid_hex':'636166c3a9','invalid_hex':'636166ff','policy':'Decode UTF-8 strictly.'},
 {'valid_text':'caf\u00e9','invalid_status':'decode_failed'},'Do not use an ignore-errors decoder that silently changes customer names.')
C('shell','A fake token is redacted from a failing command log',7,
 'Create structured diagnostic output for the supplied failure while redacting only the fake credential.',
 {'event':{'command':'load','run':'R1','token':'FAKE_TOKEN_123','error':'connection refused'}},
 {'safe_event':{'command':'load','run':'R1','token':'REDACTED','error':'connection refused'},'fake_token_occurrences_in_log':0},'Preserve actionable run and error context; never scan or print real environment secrets.')
C('shell','Bounded parallel work includes the final partial group',8,
 'Process five supplied jobs with at most two active workers and retain exactly one result per job.',
 {'jobs':[1,2,3,4,5],'worker_limit':2,'operation':'square'},
 {'results':{'1':1,'2':4,'3':9,'4':16,'5':25},'maximum_active_workers_lte':2},'Measure active worker overlap or use a testable bounded executor; group count alone does not prove the limit.')
C('shell','Streaming aggregation preserves the final line without a newline',8,
 'Aggregate the supplied newline-delimited numeric records without requiring a terminal newline and without reading the complete file into one string.',
 {'file_text':'10\n20\n30','terminal_newline':False},
 {'count':3,'sum':60},'Use an iterator/stream; record a bounded larger fixture separately before claiming memory improvement.')

C('docker','Runtime configuration changes output without a rebuild',1,
 'Package the supplied tiny program in an existing trusted local Python training image and run it with both configurations.',
 {'app_py':'import os\nprint("region=" + os.environ["REGION"])\n','runs':[{'REGION':'north'},{'REGION':'south'}]},
 {'stdout_by_run':['region=north\n','region=south\n'],'required_image_builds':1},'Record the actual local base-image identity; no cloud deployment or remote push is required.')
C('docker','A mounted report survives the disposable container',1,
 'Run the supplied writer against an owned host output directory and inspect the output after the container is removed.',
 {'app_py':'from pathlib import Path\nPath("/output/result.txt").write_text("count=2\\n")\n','container_output':'/output/result.txt','host_directory':'owned_scratch/reports'},
 {'host_result_content':'count=2\n','result_exists_after_container_removal':True},'Mount only the owned report directory; do not rely on the removed writable container layer for persistence.')
C('docker','The build context must exclude a fake credential file',2,
 'Build a tiny training image from the supplied context while excluding private.env and keeping the required application file.',
 {'context_files':{'app.py':'print("ready")\n','private.env':'TOKEN=FAKE_BUILD_SECRET\n','README.txt':'training only\n'},'required_in_image':['app.py'],'forbidden_in_image':['private.env']},
 {'app_runs':True,'private_env_in_image':False,'fake_secret_in_image_history':False},'Do not copy then delete the fake secret in a later image layer; inspect the resulting image evidence.')
C('docker','A relative input path depends on the configured working directory',2,
 'Repair the supplied image layout so its existing relative-path reader opens the intended fixture.',
 {'image_files':{'/app/read.py':'from pathlib import Path\nprint(Path("input.txt").read_text().strip())\n','/app/input.txt':'orders=2\n'},'broken_workdir':'/','command':['python','/app/read.py']},
 {'stdout':'orders=2\n','missing_file_error':False},'Keep the reader and fixture in the supplied paths; fix the image/run configuration rather than hard-coding a host path.')
C('docker','A non-root writer needs only its output directory writable',3,
 'Run the supplied synthetic report writer as UID 10001 and prepare permissions only for its owned output path.',
 {'runtime_uid':10001,'write_path':'/output/result.json','root_config_path':'/app/config.json','report':{'count':2}},
 {'report_written':True,'effective_uid':10001,'config_writable_by_worker':False},'Do not grant world-write access to the complete image filesystem or switch the task back to root.')
C('docker','A container failure must reach the host caller',3,
 'Package the supplied program and demonstrate that the caller observes its failing exit status.',
 {'app_py':'import sys\nprint("invalid order ID", file=sys.stderr)\nsys.exit(9)\n','bad_wrapper':'python app.py; echo finished'},
 {'container_exit_code':9,'stderr_contains':'invalid order ID'},'Do not hide the program status with a successful trailing shell command.')
C('docker','Service-to-service access uses the training network identity',4,
 'Connect the supplied two-service Compose fixture so the client contacts the server through the service network rather than its own localhost.',
 {'services':{'api':{'internal_port':8080,'response':{'count':2}},'etl':{'broken_url':'http://localhost:8080/count'}},'required_api_name':'api'},
 {'etl_received':{'count':2},'required_host_port_publications':0},'Use an isolated local network; document the corrected URL and preserve a failed-before client log.')
C('docker','A running database process is not yet a ready dependency',4,
 'Gate a bounded local training client on the supplied readiness sequence and retain its actual connection attempts.',
 {'dependency_probe_sequence':['not_ready','not_ready','ready'],'client_requirement':'Begin load only after a successful readiness probe.','maximum_probes':4},
 {'probes':3,'client_loads':1,'load_before_ready':False},'Record a supported health/readiness mechanism; an arbitrary sleep is not proof that the dependency is usable.')
C('docker','An idempotent batch container has stable rerun output',5,
 'Run a tiny batch container twice against an owned persisted target using the supplied logical record key.',
 {'deliveries':[[{'id':'O1','amount':10}],[{'id':'O1','amount':10}]],'target_key':'id','persisted_target':'owned training volume'},
 {'final_rows':[{'id':'O1','amount':10}],'logical_total':10},'Persist target state outside the disposable container; do not count separate delivery attempts as separate orders.')
C('docker','Image identity belongs in the result manifest',5,
 'Run the supplied bounded transformation and write an output manifest referencing the actual running image identity and source digest.',
 {'input_rows':[{'id':'O1','amount':10}],'input_identity':'synthetic-input-A','manifest_required_fields':['image_identity','input_identity','record_count','amount_total']},
 {'manifest':{'input_identity':'synthetic-input-A','record_count':1,'amount_total':10},'image_identity_matches_inspection':True},'Use observed image identity instead of a mutable tag alone; do not invent a digest value.')
C('docker','Read-only input is still readable but cannot be overwritten',6,
 'Mount the supplied input read-only and separate the writable report directory, then demonstrate both access boundaries.',
 {'input_content':'id,amount\nO1,10\n','input_mount':'/input','output_mount':'/output','attempts':['read /input/orders.csv','write /input/orders.csv','write /output/result.txt']},
 {'read_input':'allowed','overwrite_input':'denied','write_report':'allowed','source_unchanged':True},'Use owned synthetic mounts only and retain the actual permission-failure evidence.')
C('docker','A restarted worker reconstructs from the durable input',6,
 'Interrupt a training container after a partial temporary output and restart from the same durable input under an atomic-publication contract.',
 {'input_rows':[{'id':'A','amount':10},{'id':'B','amount':20}],'failure_after_rows':1,'old_published_total':5,'temporary_output':'/output/current.tmp'},
 {'published_after_failure':5,'published_after_recovery':30,'final_row_count':2},'An incomplete temporary file is not a published result; retain a final reconciliation after restart.')
C('docker','A reviewed digest mismatch blocks a mutable-tag release',7,
 'Validate a local training deployment manifest against its observed image identity before running the release.',
 {'reviewed':{'tag':'etl:training','digest':'sha256:reviewed'},'observed':{'tag':'etl:training','digest':'sha256:changed'}},
 {'release_allowed':False,'reason':'image_identity_mismatch'},'The digest strings are synthetic policy fixtures, not executable image references; perform a separate actual-image check when running a real container.')
C('docker','Read-only root needs an explicit temporary-write path',7,
 'Run a training worker with a read-only root filesystem and permit only its stated temporary and report writes.',
 {'worker_writes':['/tmp/training-buffer','/output/result.json'],'forbidden_write':'/app/config.json','required_effective_uid':10001},
 {'buffer_write':'allowed','report_write':'allowed','config_write':'denied','effective_uid':10001},'Avoid broad writable host mounts; record actual mount and runtime-user configuration.')
C('docker','Dependency cache reuse must not freeze changed application code',8,
 'Compare two builds where dependencies are unchanged but the supplied application output changes.',
 {'requirements':'No third-party dependencies.','app_v1':'print("version=1")\n','app_v2':'print("version=2")\n','expected_dependency_contract':'unchanged'},
 {'v1_stdout':'version=1\n','v2_stdout':'version=2\n','stale_application_reuse_allowed':False},'Any cache-speed claim requires observed build evidence; correctness must hold for both cold and warm builds.')
C('docker','A bounded memory test distinguishes a limit from a measured peak',8,
 'Execute a small generated file transformation with an explicit training memory limit and report the observed resource evidence.',
 {'synthetic_rows':10000,'amount_each':1,'configured_memory_limit_MiB':256,'required_report_fields':['configured_limit','observed_peak_or_unavailable','exit_code','row_count','sum']},
 {'row_count':10000,'sum':10000,'configured_limit_MiB':256,'fabricated_peak_allowed':False},'If the runtime does not expose a reliable peak, report unavailable; do not present the configured limit as actual memory consumption.')

C('azure','A resource name is not its globally scoped identity',1,
 'Compare the supplied same-name resources and select the one belonging to the required training subscription and resource group.',
 {'resources':[{'subscription':'train-a','group':'rg-orders','name':'storders'},{'subscription':'train-b','group':'rg-orders','name':'storders'}],'required_subscription':'train-a'},
 {'selected':{'subscription':'train-a','group':'rg-orders','name':'storders'},'distinct_resources':2},'Use synthetic descriptions only; do not change CLI subscription context without checking its actual identity.')
C('azure','Tags identify an owned resource but do not grant data access',1,
 'Assess the supplied ownership tags and access result without treating a tag as a permission.',
 {'resource':{'tags':{'owner':'learner','environment':'training'}},'request':{'actor':'reporter','action':'write_data','result':'denied'}},
 {'ownership_known':True,'write_authorized':False},'The conclusion must separate inventory metadata from the authorization decision.')
C('azure','Management read success does not imply blob data read access',2,
 'Classify the two supplied operations and explain the narrower missing capability.',
 {'operations':[{'name':'read_storage_account_metadata','plane':'management','result':'success'},{'name':'read_blob_contents','plane':'data','result':'denied'}]},
 {'management_access_confirmed':True,'blob_read_access_confirmed':False,'missing_capability':'scoped blob data read'},'Do not recommend owner-level access merely because a data-plane read failed.')
C('azure','A local estimate uses units consistently',2,
 'Calculate a synthetic training cost estimate from the supplied rates and usage.',
 {'rates':{'compute_per_hour':'2.00','storage_per_GiB_day':'0.01'},'usage':{'compute_hours':3,'storage_GiB':10,'days':2},'currency':'synthetic training-units'},
 {'compute':'6.00','storage':'0.20','total':'6.20'},'These are synthetic exercise rates, not actual Azure prices or a real account bill.')
C('azure','A regional residency constraint filters an otherwise valid plan',3,
 'Validate both supplied environment proposals against the dataset residency requirement.',
 {'allowed_regions':['centralindia'],'plans':{'A':{'storage_region':'centralindia','compute_region':'centralindia'},'B':{'storage_region':'centralindia','compute_region':'eastus'}}},
 {'A':'allowed','B':'blocked','B_violations':['compute_region']},'Validate processing location as well as storage location; no resource provisioning is required.')
C('azure','A review endpoint cannot write to the baseline storage account',3,
 'Validate the environment-to-endpoint mapping before the supplied synthetic writer runs.',
 {'environment':'review','configured_endpoint':'https://baseline.example.invalid','expected_endpoint':'https://review.example.invalid'},
 {'writer_started':False,'configuration_status':'environment_mismatch'},'Use nonresolving synthetic endpoints and fail before sending any network request.')
C('azure','One correlation ID links a multi-service request',4,
 'Reconstruct the supplied synthetic request timeline across identity, storage and compute.',
 {'events':[{'at':1,'service':'identity','correlation':'R1','status':'ok'},{'at':2,'service':'storage','correlation':'R2','status':'ok'},{'at':3,'service':'storage','correlation':'R1','status':'denied'},{'at':4,'service':'compute','correlation':'R1','status':'not_started'}],'request':'R1'},
 {'R1_timeline':['identity:ok','storage:denied','compute:not_started'],'first_failure':'storage'},'Do not attribute R2 success to R1 or infer compute execution from a planned stage.')
C('azure','An exact naming rule catches invalid storage-account names locally',4,
 'Implement the supplied storage naming contract as a local configuration check.',
 {'rule':'3 through 24 lowercase ASCII letters or digits only.','names':['storders01','StOrders','ab','st-orders']},
 {'valid':['storders01'],'invalid':['StOrders','ab','st-orders']},'This validates the stated syntax only; do not claim a syntactically valid name is globally available.')
C('azure','A managed identity reference replaces a fake embedded credential',5,
 'Refactor the supplied local workload configuration into an identity reference and scoped data requirement.',
 {'before':{'endpoint':'https://training.example.invalid','password':'FAKE_STATIC_PASSWORD'},'identity':'training-loader','required_operation':'write curated orders'},
 {'after_required_fields':['endpoint','identity_reference'],'embedded_password_fields':0,'required_access_scope':'curated orders write'},'A config refactor does not prove a real managed-identity token was acquired; label the actual verification performed.')
C('azure','A teardown inventory excludes a shared dependency',5,
 'Construct the exact owned-resource teardown list from the supplied deployment inventory.',
 {'resources':[{'id':'A','owner':'this-training-run'},{'id':'B','owner':'other-team'},{'id':'C','owner':'this-training-run'}],'run_owner':'this-training-run'},
 {'eligible_for_teardown':['A','C'],'preserved':['B']},'Produce a local plan only; do not execute resource deletion as part of this exercise.')
C('azure','A partial deployment retries the failed owned resource',6,
 'Prepare an idempotent recovery plan for the supplied partial deployment without replacing successful unrelated resources.',
 {'deployment':[{'resource':'storage','owner':'training','status':'succeeded'},{'resource':'job','owner':'training','status':'failed','error':'invalid_parameter'},{'resource':'shared-network','owner':'other-team','status':'succeeded'}]},
 {'repair_scope':['job'],'preserve':['storage','shared-network'],'required_precheck':'correct invalid parameter'},'A retry plan is not evidence of an actual deployed recovery; distinguish plan from executed sandbox results.')
C('azure','A quota shortfall cannot be solved by assuming approval',6,
 'Revise the bounded training plan using the supplied capacity limit and report its reduced concurrency.',
 {'available_units':2,'requested_workers':5,'units_per_worker':1,'job_count':5},
 {'maximum_parallel_workers':2,'minimum_worker_groups':3,'quota_increase_assumed':False},'Do not silently exceed the quota or claim an unrequested quota increase is granted.')
C('azure','Private DNS resolution is part of endpoint reachability',7,
 'Diagnose the supplied synthetic private-endpoint access fixture and identify the inconsistent resolution.',
 {'expected_private_ip':'10.1.0.5','dns_result':'203.0.113.5','public_access_enabled':False,'client_subnet':'10.1.0.0/24'},
 {'private_path_ready':False,'inconsistency':'DNS resolves public address','required_validation':'resolve intended private endpoint from the client network'},'This is an address-resolution fixture; do not claim that a successful DNS result alone proves authorization or complete connectivity.')
C('azure','Configuration drift preserves an explicitly approved exception',7,
 'Compare intended and actual synthetic settings, distinguishing approved from unapproved drift.',
 {'desired':{'public_access':False,'retention_days':30},'actual':{'public_access':True,'retention_days':45},'approved_exceptions':{'retention_days':45}},
 {'unapproved_drift':['public_access'],'approved_drift':['retention_days']},'Do not overwrite every difference blindly; produce an auditable local change plan.')
C('azure','A cost comparison must normalize the same workload',8,
 'Compare the supplied two synthetic compute offers for the same three-unit workload.',
 {'work_units':3,'offers':{'A':{'units_per_hour':1,'cost_per_hour':2},'B':{'units_per_hour':3,'cost_per_hour':4}}},
 {'A':{'hours':3,'cost':6},'B':{'hours':1,'cost':4}},'Synthetic rates exclude startup and other services; document those omissions rather than calling the result an actual Azure bill.')
C('azure','Idle-looking resources need an ownership and dependency check',8,
 'Evaluate the supplied low-utilization inventory and identify which resource can be proposed for cleanup review.',
 {'resources':[{'id':'A','recent_usage':0,'owner':'learner','referenced_by':[]},{'id':'B','recent_usage':0,'owner':'other-team','referenced_by':[]},{'id':'C','recent_usage':0,'owner':'learner','referenced_by':['monthly-job']}]},
 {'cleanup_review_candidates':['A'],'preserve_pending_review':['B','C']},'Produce evidence-backed recommendations only; zero recent usage is not standing authorization to delete a resource.')

C('cloud-security','A public endpoint is not a credential',1,
 'Classify the supplied synthetic client configuration and prepare a sanitized shareable diagnostic view.',
 {'endpoint':'https://training.example.invalid','client_id':'training-loader','client_secret':'FAKE_SECRET_ABC'},
 {'shareable':{'endpoint':'https://training.example.invalid','client_id':'training-loader','client_secret':'REDACTED'}},'Only fake values are supplied; do not inspect or print real credentials from the environment.')
C('cloud-security','A reporter cannot inherit the loader write permission',1,
 'Evaluate the supplied role assignment against the required reporting capability and remove the excessive permission in the local policy fixture.',
 {'required':{'reporter':['read:curated']},'actual':{'reporter':['read:curated','write:curated']}},
 {'excess':['write:curated'],'after':['read:curated']},'Retain reporting reads; do not solve excessive write access by disabling all reporting access.')
C('cloud-security','A resource-scoped grant must not authorize its sibling',2,
 'Implement a local authorization test for the supplied resource-scoped reader grant.',
 {'grant':{'principal':'reporter','action':'read','resource':'curated/orders'},'requests':[{'resource':'curated/orders','action':'read'},{'resource':'raw/customers','action':'read'},{'resource':'curated/orders','action':'write'}]},
 {'decisions':['allow','deny','deny']},'Match both action and resource; an identity match alone does not authorize the operation.')
C('cloud-security','A redacted URL retains its useful path but loses the fake token',2,
 'Sanitize the supplied structured request log without losing the operation path or run identity.',
 {'event':{'run':'R1','url':'https://example.invalid/orders?token=FAKE_QUERY_TOKEN','status':403}},
 {'safe_event':{'run':'R1','url':'https://example.invalid/orders?token=REDACTED','status':403},'secret_occurrences':0},'Use structured URL parsing; test a second query parameter so unrelated diagnostic values are preserved.')
C('cloud-security','A build identity cannot deploy a reporting release',3,
 'Check the supplied deployment request against a separated build and deploy capability model.',
 {'roles':{'builder':['write:artifact'],'deployer':['read:artifact','write:release']},'request':{'role':'builder','action':'write:release'}},
 {'authorized':False,'missing_permission':'write:release'},'Do not add deployment capability to the builder merely to make this request succeed.')
C('cloud-security','A curated report excludes raw customer contact fields',3,
 'Generate the supplied reporting projection from synthetic personal and business fields.',
 {'raw':[{'customer_id':'C1','email':'synthetic@example.invalid','phone':'FAKE_PHONE','region':'north','amount':10}],'required_report_fields':['region','amount']},
 {'report':[{'region':'north','amount':10}],'personal_fields_in_report':[]},'Keep business totals unchanged while removing unneeded identifiers; use only the supplied fake contact values.')
C('cloud-security','Inherited access can violate a direct-role review',4,
 'Expand the supplied role graph and report the effective excessive permission.',
 {'direct_grants':{'analyst':['read:curated'],'writers':['write:curated']},'inherits':{'analyst':['writers']}},
 {'effective_analyst_permissions':['read:curated','write:curated'],'excess':['write:curated']},'Do not certify least privilege from direct grants alone; preserve the required read permission after the proposed fix.')
C('cloud-security','An unresolved secret reference cannot become an empty password',4,
 'Test the client behavior when its configured fake-secret reference is absent from the local secret provider fixture.',
 {'configuration':{'secret_reference':'training/db-password'},'fake_provider':{},'requested_operation':'load'},
 {'client_started':False,'status':'secret_reference_missing','password_logged':False},'Do not use a default password, print unrelated provider entries or silently continue unauthenticated.')
C('cloud-security','Audit events carry the same run identity as publication',5,
 'Join the supplied synthetic access and publication events by their exact run identity and report an unaudited publication.',
 {'access_events':[{'run':'R1','actor':'loader','action':'publish','allowed':True}],'publications':[{'run':'R1','output':'day1'},{'run':'R2','output':'day2'}]},
 {'audited_outputs':['day1'],'unaudited_outputs':['day2']},'A recent R1 access event does not authorize or audit R2 automatically.')
C('cloud-security','A storage policy check identifies each failed property',5,
 'Validate both supplied synthetic storage configurations against the declared data-protection policy.',
 {'policy':{'public_access':False,'encryption_required':True},'resources':{'A':{'public_access':False,'encryption_required':True},'B':{'public_access':True,'encryption_required':False}}},
 {'A':'pass','B_violations':['public_access','encryption_required']},'Report all failing properties and their resource identity without making any external configuration change.')
C('cloud-security','Rotation revokes the old fake token after the cutover',6,
 'Implement the supplied local credential-provider transition and test old and new tokens at the fixed post-cutover instant.',
 {'old_token':'FAKE_OLD','new_token':'FAKE_NEW','cutover':'2026-10-20T10:00:00Z','assessment_at':'2026-10-20T10:00:01Z'},
 {'old_authorized':False,'new_authorized':True,'token_values_in_logs':False},'A client configuration update alone is insufficient; the old token must fail in the provider fixture.')
C('cloud-security','A denied read is repaired with scoped read access',6,
 'Diagnose the supplied authorization failure and produce the minimal corrected policy fixture.',
 {'principal':'reporter','required_operation':{'action':'read','resource':'curated/orders'},'current_grants':[],'forbidden_grants':['owner','write:*']},
 {'new_grant':{'action':'read','resource':'curated/orders'},'required_read_passes':True,'unrelated_write_passes':False},'Do not grant broad ownership or wildcard writes as a recovery shortcut.')
C('cloud-security','Expiry at the exact boundary is denied',7,
 'Test a local fake-token validator under the supplied exclusive-expiry contract.',
 {'expires_at':'2026-10-20T10:00:00Z','probes':['2026-10-20T09:59:59Z','2026-10-20T10:00:00Z','2026-10-20T10:00:01Z'],'rule':'Valid only while assessment instant is earlier than expires_at.'},
 {'authorized':[True,False,False]},'Use injected timezone-aware assessment instants rather than waiting for real token expiry.')
C('cloud-security','Development credentials cannot select a production-like target',7,
 'Validate the supplied identity-to-environment policy before the local synthetic client starts.',
 {'identity_environment':'dev','target_environment':'production-like','allowed_pairs':[['dev','dev'],['review','review']]},
 {'client_started':False,'reason':'cross_environment_access'},'Do not treat possession of any valid token as authorization for every environment.')
C('cloud-security','An authorization cache has a measurable revocation window',8,
 'Evaluate the supplied local permission cache timeline and then reduce the policy to the stated maximum stale-access window.',
 {'cached_allow_at_seconds':0,'revoked_at_seconds':10,'cache_ttl_seconds':60,'probe_at_seconds':20,'required_maximum_stale_seconds':5},
 {'original_cached_decision':'allow','original_policy_compliant':False,'required_new_ttl_lte_seconds':5},'The exercise tests the local cache policy only; do not claim real cloud token revocation is immediate.')
C('cloud-security','Retention keeps the incident-hold record beyond ordinary expiry',8,
 'Apply the supplied synthetic audit retention rule and produce an exact eligible-expiry list.',
 {'assessment_day':40,'retention_days':30,'records':[{'id':'A','created_day':0,'incident_hold':False},{'id':'B','created_day':0,'incident_hold':True},{'id':'C','created_day':20,'incident_hold':False}]},
 {'eligible_to_expire':['A'],'retained':['B','C']},'Produce a local plan or act only on owned synthetic files; preserve held incident evidence.')

C('cicd','A test exit code blocks packaging',1,
 'Implement the supplied small local validation workflow so a failed test prevents the dependent package step.',
 {'steps':[{'name':'test','exit_code':1},{'name':'package','depends_on':['test']}],'artifact_before':False},
 {'test_status':'failed','package_executed':False,'artifact_after':False},'A workflow file alone is not execution evidence; demonstrate the failing local or existing-framework run.')
C('cicd','A missing output artifact fails a successful command',1,
 'Add an explicit artifact-existence gate after the supplied zero-exit build result.',
 {'build_exit_code':0,'expected_artifact':'dist/etl.zip','actual_files':['build.log']},
 {'release_eligible':False,'reason':'artifact_missing'},'Exit code zero is necessary but not enough when the required artifact was never produced.')
C('cicd','A runtime mismatch is detected before tests',2,
 'Validate the required runtime against the supplied worker runtime before executing build steps.',
 {'required_runtime':{'language':'python','major':3,'minor':11},'observed_runtime':{'language':'python','major':3,'minor':9}},
 {'build_started':False,'reason':'unsupported_runtime'},'Use recorded runtime evidence; do not silently edit the supported version contract to fit the worker.')
C('cicd','A cold dependency cache still produces a correct artifact',2,
 'Test the supplied training build with a missing cache and compare its artifact contract with a warm-cache run.',
 {'source_version':'v1','cache_cases':['absent','present'],'required_output':{'count':2,'total':30}},
 {'absent_cache_result':{'count':2,'total':30},'present_cache_result':{'count':2,'total':30}},'A cache is an optimization, not the only source of an untracked required build input.')
C('cicd','An integration check catches a wrong target schema',3,
 'Run the supplied pipeline fixture in an isolated review target and detect the misconfigured baseline schema before writes.',
 {'environment':'review','configured_schema':'baseline','expected_schema':'review_run_1','input':[{'id':'O1','amount':10}]},
 {'writes_started':False,'check_status':'failed','reason':'target_schema_mismatch'},'Do not execute a write to the baseline target as part of discovering the error.')
C('cicd','Machine-readable results account for a skipped test',3,
 'Create a test-result summary from the supplied case outcomes without counting skipped cases as passed.',
 {'cases':[{'id':'T1','status':'pass'},{'id':'T2','status':'fail'},{'id':'T3','status':'skip'}]},
 {'passed':1,'failed':1,'skipped':1,'release_eligible':False},'Keep per-case identity; do not turn a three-case run into three passed checks.')
C('cicd','A schema-contract change requires its downstream consumer test',4,
 'Select checks for the supplied component dependency graph and changed model interface.',
 {'components':{'stage':[],'mart':['stage'],'report':['mart'],'unrelated':[]},'changed_component':'mart','changed_interface':True},
 {'required_checks':['mart','report'],'unrelated_required':False},'Do not select only the changed file while omitting its supported consumer.')
C('cicd','A review deployment uses a unique owned output path',4,
 'Deploy two local synthetic review runs without overwriting their results or the baseline.',
 {'reviews':[{'run':'R1','total':10},{'run':'R2','total':20}],'baseline':{'total':99},'root':'owned_scratch'},
 {'review_totals':{'R1':10,'R2':20},'baseline_total_after':99},'Derive an isolated path or schema from each run identity and retain both result manifests.')
C('cicd','Promotion reuses the tested artifact instead of rebuilding it',5,
 'Validate the supplied test and promotion manifests before declaring a release.',
 {'tested':{'source':'C1','artifact_digest':'digest-A'},'promotion':{'source':'C1','artifact_digest':'digest-B'}},
 {'promotion_allowed':False,'reason':'untested_artifact'},'The same source ID does not prove a separately rebuilt artifact is identical to the one tested.')
C('cicd','A schema migration preserves the old nullable-field consumer',5,
 'Rehearse the supplied additive migration in a scratch relation and execute both old and new consumer fixtures.',
 {'before':[{'id':'O1','amount':10}],'new_column':{'name':'channel','nullable':True},'old_consumer_fields':['id','amount'],'new_consumer_fields':['id','amount','channel']},
 {'old_consumer':[{'id':'O1','amount':10}],'new_consumer':[{'id':'O1','amount':10,'channel':None}]},'Do not make channel required without a data backfill and a revised compatibility plan.')
C('cicd','A failing smoke test restores the prior local release',6,
 'Implement the supplied bounded deployment transition with rollback after the new artifact fails its smoke check.',
 {'active_before':'artifact-A','candidate':'artifact-B','candidate_smoke':'fail','prior_smoke':'pass'},
 {'active_after':'artifact-A','release_B_status':'failed','rollback_verified':True},'Retain candidate failure evidence; restoration must be checked rather than inferred from a rollback command exit.')
C('cicd','A failed migration is not marked as applied',6,
 'Simulate the supplied transactional scratch migration failure and verify both schema and migration ledger remain consistent.',
 {'initial_columns':['id','amount'],'migration':'add channel then fail before commit','ledger_before':[]},
 {'columns_after':['id','amount'],'ledger_after':[],'migration_status':'failed'},'Use a training engine supporting the stated transactional DDL or explicitly document and test an alternative recovery contract.')
C('cicd','An old consumer retains gross revenue during a net-revenue rollout',7,
 'Release compatible v1 and v2 report interfaces for the supplied revenue definition change.',
 {'order':{'gross':100,'credits':20},'v1_contract':'amount means gross','v2_contract':'gross_amount and net_amount are separate fields'},
 {'v1':{'amount':100},'v2':{'gross_amount':100,'net_amount':80}},'Do not silently reinterpret the v1 field during deployment.')
C('cicd','A fake deployment token must not enter the artifact',7,
 'Package the supplied small project while injecting the fake credential only into the bounded release step.',
 {'source_files':{'app.py':'print("ready")\n'},'fake_release_token':'FAKE_RELEASE_TOKEN','artifact_required_files':['app.py']},
 {'artifact_contains':['app.py'],'artifact_contains_token':False,'logs_contain_token':False},'Use a local release simulation or authorized existing framework; no external publication is required.')
C('cicd','Two test workers cannot both own the same scratch schema',8,
 'Run the supplied independent tests with isolated mutable targets and compare with the colliding proposal.',
 {'tests':[{'id':'A','writes':10},{'id':'B','writes':20}],'bad_target':'review_shared','required_worker_limit':2},
 {'isolated_results':{'A':10,'B':20},'shared_target_collision_allowed':False},'Use distinct per-test targets; a faster test run that corrupts shared state is not a valid optimization.')
C('cicd','Release retention preserves the active rollback artifact',8,
 'Apply the supplied artifact-retention policy while retaining the active and previous tested release.',
 {'artifacts':[{'id':'A','age_days':50},{'id':'B','age_days':40},{'id':'C','age_days':1}],'active':'C','rollback':'B','ordinary_retention_days':30},
 {'eligible_to_expire':['A'],'retained':['B','C']},'Produce an exact local cleanup plan; do not delete an artifact needed for the documented rollback.')

C('integrated-pipelines','A one-file sales summary retains its raw input',1,
 'Build a local CSV-to-JSON report command for the supplied complete delivery and prove the input file is unchanged.',
 {'input_csv':'order_id,amount\nO1,10.00\nO2,20.00\n','report_fields':['order_count','amount_total'],'input_policy':'Immutable raw delivery.'},
 {'report':{'order_count':2,'amount_total':'30.00'},'raw_digest_unchanged':True},'Keep the command bounded to this one file and one report; no scheduler or cloud service is required.')
C('integrated-pipelines','A malformed amount has an explicit rejected-row artifact',1,
 'Extend a tiny local order reader to write a valid-order report and a rejection artifact under the supplied business rule.',
 {'input_csv':'order_id,amount\nO1,10.00\nO2,bad\n','rule':'Amounts must parse as a two-decimal currency value.'},
 {'accepted_ids':['O1'],'rejected':[{'id':'O2','reason':'invalid_amount'}],'report_total':'10.00','accounted_rows':2},'Preserve the original bad amount in rejection evidence and do not substitute zero.')
C('integrated-pipelines','A missing lookup remains visible through a relational load',2,
 'Read the supplied files, load accepted order facts into a disposable relational target, and report unresolved customer relationships.',
 {'orders':[{'id':'O1','customer':'C1','amount':10},{'id':'O2','customer':'C9','amount':20}],'customers':[{'id':'C1','region':'north'}],'policy':'Retain unresolved orders and identify them separately.'},
 {'stored_order_count':2,'resolved_ids':['O1'],'unresolved_ids':['O2'],'amount_total':30},'Use source IDs for traceability; do not drop O2 in an inner join.')
C('integrated-pipelines','A round-trip database load preserves exact cents',2,
 'Read the supplied decimal strings, load them into a training relational table, and query a reconciled report.',
 {'orders':[{'id':'O1','amount':'0.10'},{'id':'O2','amount':'0.20'}],'required_currency_precision':2},
 {'stored_count':2,'report_total':'0.30'},'Preserve decimal semantics across file parsing, storage and reporting rather than rounding an arbitrary float tolerance.')
C('integrated-pipelines','Cancelled orders stay auditable but leave accepted revenue',3,
 'Create a staged order relation and a daily accepted-revenue report with explicit reconciliation to all source rows.',
 {'orders':[{'id':'O1','date':'2026-10-20','status':'accepted','amount':10},{'id':'O2','date':'2026-10-20','status':'cancelled','amount':99},{'id':'O3','date':'2026-10-20','status':'accepted','amount':20}]},
 {'staged_count':3,'accepted_order_count':2,'accepted_revenue':30,'cancelled_count':1},'Do not erase the cancelled source record merely because it does not contribute revenue.')
C('integrated-pipelines','A report date is a parameter rather than the machine date',3,
 'Implement a file-to-database-to-report command for one explicitly requested business date.',
 {'requested_date':'2026-10-20','orders':[{'id':'A','date':'2026-10-20','amount':10},{'id':'B','date':'2026-10-21','amount':90}],'output_name':'daily/2026-10-20.json'},
 {'report':{'date':'2026-10-20','count':1,'total':10},'excluded_ids':['B']},'Inject or ignore wall-clock date; a historical rerun must reproduce the same date-specific result.')
C('integrated-pipelines','A two-source pipeline preserves overlapping order IDs',4,
 'Ingest both supplied source deliveries, retain source identity in the target and reconcile per-source and overall reports.',
 {'source_A':[{'order_id':'1','amount':10}],'source_B':[{'order_id':'1','amount':20}],'business_key':['source','order_id']},
 {'target_rows':2,'source_totals':{'A':10,'B':20},'overall_total':30},'A source-local identifier collision is not a replay; demonstrate that replaying A alone does not duplicate A.')
C('integrated-pipelines','Pagination detects a repeated cursor before an endless loop',4,
 'Consume the supplied API-response fixture files as a bounded ingestion source and reject the repeated continuation cursor.',
 {'pages':{'start':{'records':[{'id':'A'}],'next':'c1'},'c1':{'records':[{'id':'B'}],'next':'c1'}},'maximum_pages':5},
 {'fetched_cursors':['start','c1'],'status':'cursor_loop_detected','complete_delivery_published':False},'Preserve the two fetched pages and do not treat the loop as a complete successful source delivery.')
C('integrated-pipelines','A versioned correction and new order share one incremental run',5,
 'Apply the supplied change batch to a small relational current-state target and reconcile the run manifest.',
 {'target':[{'id':'O1','version':1,'amount':10},{'id':'O2','version':1,'amount':20}],'changes':[{'id':'O1','version':2,'amount':25},{'id':'O3','version':1,'amount':5}]},
 {'final_rows':[{'id':'O1','version':2,'amount':25},{'id':'O2','version':1,'amount':20},{'id':'O3','version':1,'amount':5}],'final_total':50,'inserted_keys':1,'updated_keys':1},'Replay the same changes and retain the same target state; record separate delivery and business-row counts.')
C('integrated-pipelines','The watermark advances only after durable target success',5,
 'Connect extraction, target loading and run-state persistence with the supplied commit policy and injected load failure.',
 {'watermark_before':100,'source':[{'id':'A','position':101},{'id':'B','position':102}],'load_outcome':'failed','policy':'Advance only after durable target commit.'},
 {'watermark_after':100,'run_status':'failed','next_retry_source_positions':[101,102]},'Do not infer successful delivery from extraction completion or update the watermark in a finally block.')
C('integrated-pipelines','A committed load with a lost acknowledgement is reconciled before replay',6,
 'Simulate target commit followed by failed run-status acknowledgement, then retry using the supplied stable delivery identity.',
 {'delivery_id':'D1','source':[{'id':'O1','amount':10}],'state_after_failure':{'target':[{'id':'O1','amount':10,'delivery_id':'D1'}],'run_ledger':'unknown'}},
 {'target_after_retry':[{'id':'O1','amount':10,'delivery_id':'D1'}],'ledger_after':'committed','duplicate_rows':0},'Use observed target and delivery identity to resolve ambiguity; an unknown ledger state is not proof that no write happened.')
C('integrated-pipelines','A poison row is isolated under an explicit partial-delivery policy',6,
 'Build a bounded ingestion run that quarantines the supplied malformed record while retaining valid outputs and truthful run status.',
 {'rows':[{'id':'A','amount':10},{'id':'B','amount':'bad'},{'id':'C','amount':20}],'policy':'Publish valid rows, retain rejected rows, and report partial_success.'},
 {'published_ids':['A','C'],'rejected_ids':['B'],'published_total':30,'run_status':'partial_success'},'Do not report full success or retry the permanent bad amount indefinitely.')
C('integrated-pipelines','A Spark rewrite matches the small-data reference including zero',7,
 'Implement the existing local transformation in PySpark and compare row identities and totals with the supplied trusted baseline.',
 {'rows':[{'id':'A','amount':0,'status':'accepted'},{'id':'B','amount':10,'status':'accepted'},{'id':'C','amount':99,'status':'cancelled'}],'rule':'Retain all accepted rows, including zero amounts.'},
 {'accepted_ids':['A','B'],'accepted_count':2,'accepted_total':10,'reference_parity':True},'A matching sum alone is insufficient because losing A would leave the same sum.')
C('integrated-pipelines','A Delta current-state update rejects a stale arrival',7,
 'Build a training Delta current-state target and apply the supplied out-of-order source versions with retained raw lineage.',
 {'baseline':[{'id':'O1','version':1,'amount':10}],'arrival_order':[{'id':'O1','version':3,'amount':15},{'id':'O1','version':2,'amount':12}],'raw_policy':'Retain every arrival unchanged.'},
 {'curated':[{'id':'O1','version':3,'amount':15}],'raw_arrivals':2,'stale_arrivals_ignored':1},'Record actual supported Spark and Delta versions; a local dictionary simulation cannot prove Delta transaction behavior.')
C('integrated-pipelines','A hot-key optimization must preserve every fact row',8,
 'Measure a bounded Spark join baseline and compare one chosen optimization for the supplied skewed synthetic generator.',
 {'generator':{'hot_customer':'C1','hot_order_rows':9000,'other_customers':1000,'rows_per_other_customer':1,'amount_per_order':1},'dimension_rule':'One dimension row per customer.'},
 {'joined_order_count':10000,'joined_amount_total':10000,'required_measurements':['task_distribution','elapsed_or_supported_execution_metrics']},'Do not add duplicate dimension keys or remove hot-customer rows to make the workload appear faster.')
C('integrated-pipelines','A partition lookback corrects an older business day',8,
 'Optimize the supplied incremental pipeline with an explicit two-day lookback and compare its result with a complete scratch rebuild.',
 {'assessment_date':'2026-10-22','lookback_start':'2026-10-20','target':[{'id':'A','day':'2026-10-19','amount':5},{'id':'B','day':'2026-10-20','amount':10}],'source_in_lookback':[{'id':'B','day':'2026-10-20','amount':12},{'id':'C','day':'2026-10-22','amount':3}]},
 {'final_rows':[{'id':'A','day':'2026-10-19','amount':5},{'id':'B','day':'2026-10-20','amount':12},{'id':'C','day':'2026-10-22','amount':3}],'total':20,'full_rebuild_equal':True},'Retain A without rereading it, update B rather than append it, and record actual scanned scope.')
C('integrated-pipelines','An Azure release rehearsal isolates review data and identity',9,
 'Rehearse a bounded training pipeline release using separate review storage paths and a scoped review identity. Execute consumer contract checks before preparing promotion.',
 {'raw_rows':[{'id':'O1','amount':10},{'id':'O2','amount':20}],'review_prefix':'review/R1/','baseline_prefix':'baseline/','review_identity_permissions':['read:review/R1/raw','write:review/R1/curated'],'consumer_contract':['order_count','amount_total']},
 {'review_report':{'order_count':2,'amount_total':30},'baseline_writes':0,'review_contract_passes':True},'Use an authorized cost-bounded Azure sandbox for real execution; a local simulation is useful rehearsal but does not verify Azure identity or deployment.')
C('integrated-pipelines','Pipeline availability and data freshness are different SLO outcomes',9,
 'Operate a prepared training pipeline with the supplied daily deadline and run evidence, then generate an actionable unsent alert artifact.',
 {'deadline':'2026-10-20T06:00:00Z','run':{'id':'R1','technical_status':'success','completed_at':'2026-10-20T06:20:00Z','published_business_date':'2026-10-19'},'required_business_date':'2026-10-20','owner':'training-operator'},
 {'technical_success':True,'freshness_slo_met':False,'alert_fields':['run_id','owner','required_business_date','actual_business_date','lateness','evidence_reference']},'Prepare the alert payload locally; do not send an external message. A successful process exit cannot establish timely business delivery.')
C('integrated-pipelines','Independent Azure delivery survives correction replay and one failed load',10,
 'Independently implement a bounded Azure raw-to-curated-to-report pipeline from this business brief. Preserve immutable raw deliveries, validate rows, maintain keyed current state, test a failed target load, replay the correction batch, and defend the operating design.',
 {'business':'A distributor needs one reliable daily current-order revenue report before dispatch.','baseline':[{'id':'O1','version':1,'amount':'10.00'},{'id':'O2','version':1,'amount':'20.00'}],'next_delivery':[{'id':'O1','version':2,'amount':'25.00'},{'id':'O3','version':1,'amount':'5.00'},{'id':'O4','version':1,'amount':'bad'}],'required_capabilities':['ADLS Gen2 raw and curated storage','ADF orchestration','Databricks/PySpark transformation','Delta current-state target','quality and run evidence'],'fault_injection':'Fail one load before durable commit, recover, then replay the complete next delivery.','operational_bounds':{'synthetic_data_only':True,'explicit_cost_cap':True,'no_secret_in_code':True}},
 {'current_ids':['O1','O2','O3'],'current_total':'50.00','rejected_ids':['O4'],'post_replay_total':'50.00','failed_run_retained':True,'independent_evidence_required':['implementation','actual execution artifacts','assistance disclosure','recovery test','design explanation']},'Use a permitted training subscription and record actual versions, cost boundary and cleanup plan. Assistance is welcome but independent mastery needs a separately reviewed fresh attempt; simulations do not satisfy this Azure implementation assessment.')

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()

def proposals(exclude_ids=()):
    by_tool = {}
    for case in CASES:
        tool = case['tool_id']
        if tool not in by_tool:
            path = OUT/f'{tool}.json'
            data = json.loads(path.read_text(encoding='utf-8'))
            by_tool[tool] = {'path':path,'data':data,'used':set(exclude_ids)}
    result = []
    for number, case in enumerate(CASES,1):
        state = by_tool[case['tool_id']]
        original = next((p for p in state['data']['problems']
                         if p.get('publication_status') == 'draft'
                         and p['level'] == case['level']
                         and p['id'] not in state['used']),None)
        if original is None:
            raise ValueError(f'No unused same-level draft slot for {case["tool_id"]}: {case["title"]}')
        state['used'].add(original['id'])
        problem = deepcopy(original)
        problem.update({
            'title':case['title'], 'level':case['level'], 'difficulty':f'level_{case["level"]}',
            'scenario':f'The data delivery team must resolve a concrete operational case: {case["title"].lower()}. '
                       'The supplied synthetic artifacts describe the exact business or operating boundary to preserve.',
            'task':case['task'], 'inputs':case['inputs'], 'expected_output':case['expected_output'],
            'constraints':[case['constraint'],'Preserve the original attempt and observed execution evidence; disclose AI, documentation and other assistance.',
                           'Use only synthetic data and owned disposable training resources.'],
            'acceptance_criteria':[
                'The supplied fixture produces the exact expected logical outcome, with unordered record collections compared by their business identity.',
                case['constraint'],
                'Supply implementation or configuration, actual commands or test probes, and observed results sufficient to check each expected field.',
                'State which checks actually ran. A local policy simulation does not establish real cloud or orchestration execution.'
            ],
            'learning_objective':case['title'],
            'progressive_hints':[
                'First identify the exact supplied artifact and the observable before-and-after result required by this case.',
                'Keep the rest of the fixture fixed while checking this boundary: '+case['constraint'],
                'Use the linked official documentation for your installed version. Add an observation or failing test that would expose the incorrect result before changing the implementation.'
            ],
            'engineering_relevance':f'This case exercises {case["tool_id"]} work needed to deliver trustworthy data: {case["title"].lower()}. '
                                    'After verification, explain the consequence of the incorrect behavior for a pipeline consumer.',
            'publication_status':'published', 'draft_reason':None,
            'challenge_kind':'skill_build','activity_mode':'case_specific_technical_challenge',
            'published_version':'pending-versioned-release',
            'verification':{'kind':'artifact_review','evidence_required':['implementation_or_configuration','actual_result','assistance_disclosure'],
                            'note':'Case oracle supplied; tutor must review actual implementation and safely run applicable tests. No learner completion or cloud execution is inferred.'},
            'authoring':{'batch':'engineering-batch2','case_number':number,
                         'replaces_generic_candidate':True,'specific_fixture':True,
                         'review_scope':'Authored technical fixture and explicit expected result; runtime verification of learner work remains required.'},
        })
        problem.pop('transfer_of',None)
        if case['tool_id']=='integrated-pipelines' and case['level']==10:
            problem['estimated_minutes']=480
        problem['followup']={
            'task':'After a delay, reconstruct this case independently with the supplied fixture and explain the outcome without referring to your prior implementation.',
            'inputs':deepcopy(case['inputs']),'expected_output':deepcopy(case['expected_output']),
            'constraints':[case['constraint'],'Disclose assistance. Independent mastery needs reviewed code, results and reasoning, not self-report.'],
            'verification':{'kind':'artifact_review'},
        }
        result.append({'source_file':state['path'].name,'original_draft_id':original['id'],
                       'original_draft_sha256':digest(original),'problem':problem})
    return result, by_tool

def validate(items, by_tool):
    errors = []
    seen_ids, seen_contracts = set(),set()
    original_ids = set()
    published_ids = set()
    all_problems = []
    seed = json.loads((ROOT/'tools/curriculum.json').read_text(encoding='utf-8'))
    all_problems.extend(seed['problems'])
    for state in by_tool.values(): all_problems.extend(state['data']['problems'])
    for p in all_problems:
        original_ids.add(p['id'])
        if p.get('publication_status','published')=='published':published_ids.add(p['id'])
    proposed_ids = {i['problem']['id'] for i in items}
    for item in items:
        p=item['problem']
        if p['id'] in seen_ids:errors.append(p['id']+': repeated proposed ID')
        seen_ids.add(p['id'])
        contract=digest({k:p[k] for k in ['task','inputs','expected_output','acceptance_criteria','constraints']})
        if contract in seen_contracts:errors.append(p['id']+': repeated technical contract')
        seen_contracts.add(contract)
        if p['id'] not in original_ids:errors.append(p['id']+': unstable ID')
        if not p['inputs'] or not p['expected_output']:errors.append(p['id']+': empty contract')
        if len(p['progressive_hints'])!=3:errors.append(p['id']+': missing hints')
        if any(c in p['title'] for c in ['\u00e2','\ufffd']):errors.append(p['id']+': title encoding corruption')
        for dep in p['prerequisites']:
            if dep not in published_ids|proposed_ids:errors.append(p['id']+': unpublished prerequisite '+dep)
    # No proposal is permitted to modify any already published contract.
    for tool,state in by_tool.items():
        by_id={p['id']:p for p in state['data']['problems']}
        for item in items:
            if item['problem']['tool_id']!=tool:continue
            original=by_id[item['original_draft_id']]
            if original.get('publication_status')!='draft':errors.append(original['id']+': source is published')
            if digest(original)!=item['original_draft_sha256']:errors.append(original['id']+': stale draft hash')
    # Simulate merge in memory and verify that the ordered published progression
    # stays nondecreasing with a maximum same-tool step of one level.
    replacements={i['problem']['id']:i['problem'] for i in items}
    for tool,state in by_tool.items():
        merged=[replacements.get(p['id'],p) for p in state['data']['problems']]
        published=[p for p in merged if p.get('publication_status')=='published']
        for before,after in zip(published,published[1:]):
            if not before['level']<=after['level']<=before['level']+1:
                errors.append(after['id']+': difficulty order violation')
    return errors

def main():
    items,by_tool=proposals()
    errors=validate(items,by_tool)
    if errors:raise ValueError(errors)
    counts={tool:sum(i['problem']['tool_id']==tool for i in items) for tool in by_tool}
    wrapper={'schema_version':1,'proposal_version':'2026.10.26.engineering-batch2',
             'publication_status':'unregistered_proposals','proposals':items,
             'counts':{'proposed_promotions':len(items),'published_added':0,'by_technology':counts},
             'validation':{'schema_errors':0,'duplicate_contracts':0,'published_prerequisite_errors':0,
                           'difficulty_order_errors':0,'runtime_claim':'No learner solution or cloud deployment was executed by generation.'}}
    path=OUT/'engineering-promotions.json'
    temporary=path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(wrapper,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    temporary.replace(path)
    checkpoint={'proposal_version':wrapper['proposal_version'],'state':'prepared_not_published',
                'proposed_promotions':len(items),'published_added':0,'by_technology':counts,
                'proposal_file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'registered_files_sha256':{tool:hashlib.sha256(state['path'].read_bytes()).hexdigest() for tool,state in by_tool.items()},
                'validation_errors':errors,
                'remaining_after_publication':'Recompute against the versioned manifest only after atomic merge; these proposals do not alter current denominators.'}
    (OUT/'authors/engineering-batch2-checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'prepared':len(items),'published_added':0,'by_technology':counts,'errors':errors},indent=2))

if __name__=='__main__':main()
