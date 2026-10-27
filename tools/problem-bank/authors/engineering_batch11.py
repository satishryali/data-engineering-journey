"""Remaining early and bridge cases for three engineering tracks."""
import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('engineering_base11', Path(__file__).with_name('engineering_batch2.py'))
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.CASES = []
C = base.C

# Ten distinct first observations in a warehouse modelling context.
C('data-modelling','A customer row has one customer identity',0,'Identify the grain and key of the supplied customer record.',{'row':{'customer_id':'C1','name':'Corner Shop'}},{'grain':'one customer','key':'customer_id'},'The name is a display label and can change.')
C('data-modelling','An order header differs from an order line',0,'Name the grain of each supplied record.',{'header':{'order_id':'O1'},'line':{'order_id':'O1','line_no':1}},{'header_grain':'one order','line_grain':'one order line'},'Do not model line number alone as a global key.')
C('data-modelling','A shipment row records one dispatch event',0,'Identify what the supplied source row represents.',{'row':{'shipment_id':'S1','order_id':'O1','sent_units':2}},{'grain':'one shipment event','key':'shipment_id'},'The order may have another shipment later.')
C('data-modelling','A date value is not a transaction identity',0,'Identify the identifier and date role in a supplied sale.',{'sale':{'sale_id':'S1','business_day':'2026-10-20'}},{'key':'sale_id','date_role':'business day'},'Many sales may share one business day.')
C('data-modelling','A product key is separate from its category',0,'Classify the supplied two fields.',{'product':{'sku':'P1','category':'stationery'}},{'product_key':'sku','descriptive_field':'category'},'Several products can belong to one category.')
C('data-modelling','A warehouse code identifies a location',0,'Locate the dimension identity needed for a stock fact.',{'movement':{'event':'M1','sku':'P1','warehouse':'W2','units':3}},{'location_code':'W2','event_key':'M1'},'An event identity and a location identity serve different roles.')
C('data-modelling','A payment row keeps its own key and invoice reference',0,'Distinguish the supplied payment event from its parent invoice.',{'payment':{'payment_id':'P1','invoice_id':'I1','amount':10}},{'payment_key':'P1','invoice_reference':'I1'},'Two payments may reference one invoice.')
C('data-modelling','A return row points to a sale without becoming a sale',0,'Name the two identities in the supplied record.',{'return':{'return_id':'R1','sale_id':'S1','units':1}},{'event_key':'R1','sale_reference':'S1'},'Keep return and sale as distinct event types.')
C('data-modelling','A supplier identifier cannot be inferred from a product name',0,'Identify the supplied explicit supplier key.',{'item':{'supplier_id':'SUP1','product_name':'Notebook'}},{'supplier_key':'SUP1'},'A product name might be sold by multiple suppliers.')
C('data-modelling','A snapshot date labels a state observation',0,'Identify the state grain of the supplied record.',{'snapshot':{'sku':'P1','warehouse':'W1','day':'2026-10-20','on_hand':10}},{'grain':['sku','warehouse','day'],'observed_balance':10},'A balance snapshot is not a stock-change event.')

C('data-modelling','A second line does not create another order',1,'Count orders and lines in the supplied tiny fixture.',{'lines':[{'order':'O1','line':1},{'order':'O1','line':2}]},{'order_count':1,'line_count':2},'Do not infer two orders from two line records.')
C('data-modelling','A product with no sales remains in the catalog',1,'Describe the relationship between supplied product and empty sale list.',{'products':[{'sku':'P1'}],'sales':[]},{'catalog_products':1,'sales_count':0},'No sales is not proof the product record should be removed.')
C('data-modelling','One shipment can contain two order lines',2,'Model the supplied shipment with two line references.',{'shipment':'S1','lines':[{'order':'O1','line':1,'units':1},{'order':'O1','line':2,'units':2}]},{'shipment_count':1,'shipment_line_count':2,'shipped_units':3},'Shipment header amount must not be duplicated by each line.')
C('data-modelling','Two customers with the same postcode stay distinct',2,'Preserve source customer identity in a geographic grouping.',{'customers':[{'id':'C1','postcode':'1000'},{'id':'C2','postcode':'1000'}]},{'customer_count':2,'postcode_group_count':1},'A postcode is a grouping attribute, not a customer key.')
C('data-modelling','A cancelled invoice does not add active receivables',3,'Build an invoice-state report from the supplied fixture.',{'invoices':[{'id':'I1','amount':100,'status':'active'},{'id':'I2','amount':50,'status':'cancelled'}]},{'active_receivables':100,'cancelled_invoice_count':1},'Retain cancelled history while excluding it from active balance.')
C('data-modelling','A customer order count includes customers with zero orders',3,'Build a complete customer count report.',{'customers':['C1','C2'],'orders':[{'id':'O1','customer':'C1'}]},{'counts':{'C1':1,'C2':0}},'An inner join would erase the zero-order customer.')
C('data-modelling','Two stores share a local receipt number',4,'Merge source receipt files using store-qualified identities.',{'store_A':[{'receipt':'1','amount':10}],'store_B':[{'receipt':'1','amount':20}]},{'logical_receipts':2,'total':30},'The store namespace is part of receipt identity.')
C('data-modelling','A currency reference file is required for conversion',4,'Mark an invoice unresolved when its currency has no supplied conversion.',{'invoices':[{'id':'I1','currency':'USD','amount':10},{'id':'I2','currency':'EUR','amount':10}],'rates':{'USD':80}},{'converted_ids':['I1'],'unresolved_ids':['I2']},'Do not reuse USD rate for EUR.')
C('data-modelling','A correction and a delete both change current orders',5,'Apply the supplied versioned operations to a keyed target.',{'target':[{'id':'A','amount':10},{'id':'B','amount':20}],'operations':[{'id':'A','op':'upsert','amount':12},{'id':'B','op':'delete'}]},{'current_ids':['A'],'total':12},'Preserve raw operation history and make replay idempotent.')
C('data-modelling','A customer dimension retains a stable key through renaming',5,'Apply a display-name change to one customer identity.',{'versions':[{'id':'C1','name':'Old','version':1},{'id':'C1','name':'New','version':2}]},{'customer_count':1,'current_name':'New','history_versions':2},'Name changes do not create unrelated customers.')
C('data-modelling','A late invoice arrives after its report day',6,'Repair the prior-day report with the retained source invoice.',{'report_day':1,'published_total':10,'late_invoice':{'id':'I2','effective_day':1,'arrival_day':3,'amount':5}},{'corrected_day1_total':15,'day3_new_invoice_total':0},'Do not use arrival day as invoice effective day.')
C('data-modelling','An orphan line blocks complete invoice publication',6,'Classify an invoice line whose header is missing from the delivery.',{'headers':['I1'],'lines':[{'id':'L1','invoice':'I1','amount':10},{'id':'L2','invoice':'I9','amount':5}]},{'valid_lines':['L1'],'orphan_lines':['L2'],'complete_publication_allowed':False},'Do not attach L2 to I1 merely to include its amount.')
C('data-modelling','A backdated customer tier change affects one earlier sale',7,'Join sales to the supplied customer-tier history at each sale time.',{'tiers':[{'name':'standard','from':1,'to':5},{'name':'gold','from':5,'to':None}],'sales':[{'id':'A','at':4},{'id':'B','at':5}]},{'sale_tiers':{'A':'standard','B':'gold'}},'A latest-tier join would misclassify A.')
C('data-modelling','A voided payment leaves an audit event but no net cash',7,'Model a payment and its linked void.',{'payment':{'id':'P1','amount':40},'void':{'id':'V1','payment':'P1','effective':True}},{'net_applied_cash':0,'audit_events':2},'Do not erase either source event to achieve zero.')
C('data-modelling','A row-limit shortcut can miss a later correction',8,'Assess a proposed first-two-row current-state query.',{'arrivals':[{'id':'A','version':1,'amount':10},{'id':'B','version':1,'amount':5},{'id':'A','version':2,'amount':12}],'shortcut_rows':2},{'shortcut_A':10,'required_A':12,'shortcut_valid':False},'Performance changes must preserve current-version semantics.')
C('data-modelling','A wide product report cannot answer event chronology',8,'Evaluate a product total against a first-sale timestamp request.',{'sales':[{'at':1,'amount':10},{'at':2,'amount':20}],'stored_product_total':30},{'total_correct':True,'first_sale_recoverable_from_total':False},'Retain necessary detail if consumers need event order.')

# Eight simple quality observations with distinct source contracts.
C('data-quality','A record without a customer reference is incomplete',0,'Check the required customer field in a single order.',{'order':{'id':'O1','customer':None},'required':['id','customer']},{'valid':False,'missing':['customer']},'Do not fill a missing customer with the order ID.')
C('data-quality','A zero-unit shipment fails the positive-units contract',0,'Check one outbound shipment row.',{'shipment':{'id':'S1','units':0},'rule':'Shipment units must be positive.'},{'valid':False,'failed_rule':'positive_units'},'This rule differs from an order amount that may validly be zero.')
C('data-quality','An unknown status is visible as an exception',0,'Classify a single order state.',{'status':'in-flight','allowed':['accepted','held','cancelled']},{'valid':False,'unknown_status':'in-flight'},'Do not infer that in-flight means accepted.')
C('data-quality','A missing file is not a zero-row delivery',0,'Inspect the supplied source path state.',{'required_file':'orders.csv','exists':False},{'delivery_status':'missing','verified_rows':None},'No file bytes exist to validate as an empty table.')
C('data-quality','A delivered header names two required fields',0,'Check a tiny file header.',{'header':'order_id,amount','required':['order_id','amount']},{'missing_columns':[],'header_valid':True},'This confirms only the header, not the values or delivery completeness.')
C('data-quality','A string amount has to parse before addition',0,'Classify the supplied one-row amount.',{'row':{'id':'A','amount':'12.50'}},{'numeric_value':'12.50','parse_valid':True},'Retain the raw text and avoid binary floating-point rounding claims.')
C('data-quality','A malformed UTF-8 byte blocks text parsing',0,'Decode the supplied tiny byte sequence safely.',{'hex':'ff','encoding':'utf-8'},{'decode_valid':False,'accepted_rows':0},'Do not replace invalid bytes silently under a strict source contract.')
C('data-quality','A run has a source name before validation starts',0,'Capture the source identity from the supplied manifest.',{'manifest':{'file':'north-orders.csv','business_day':'2026-10-20'}},{'source_file':'north-orders.csv','business_day':'2026-10-20'},'A manifest observation is not proof the file contents passed validation.')
C('data-quality','A required amount keeps exactly two decimal digits',1,'Validate two supplied monetary strings.',{'amounts':['12.50','12.5'],'contract':'Exactly two fractional decimal digits.'},{'valid':['12.50'],'invalid':['12.5']},'Do not rewrite the source representation before recording the contract failure.')
C('data-quality','A CSV row with too many fields violates its header',2,'Parse and classify the supplied two-row delivery.',{'csv':'id,amount\nA,10\nB,20,extra\n'},{'valid_ids':['A'],'invalid_ids':['B'],'reason':'extra_field'},'Do not silently discard the extra field.')
C('data-quality','A returned amount reconciles to its linked sale',3,'Check a simple sales-and-return report.',{'sale':{'id':'S1','amount':50},'return':{'sale':'S1','amount':20},'published_net':50},{'expected_net':30,'report_valid':False},'A valid return reduces net sales under the supplied rule.')

# Eight Airflow first observations plus the remaining small steps.
C('airflow','A DAG run can be pending',0,'Read the queued run-state record and decide whether execution has started or produced completion evidence.',{'run_id':'R1','state':'queued'},{'started':False,'completed':False},'Queued work cannot verify data output.')
C('airflow','A DAG run can be actively running',0,'Read the running run-state record and distinguish observed execution from final completion.',{'run_id':'R2','state':'running'},{'started':True,'completed':False},'A running task has not yet passed downstream checks.')
C('airflow','A successful task belongs to one run',0,'Capture the exact scope of the supplied task result.',{'dag_id':'orders','run_id':'R1','task_id':'extract','state':'success'},{'successful_task_identity':['orders','R1','extract']},'Do not extend the success claim to a different run or task.')
C('airflow','A DAG has three named tasks',0,'Read the supplied parsed task inventory.',{'dag_id':'orders','tasks':['extract','validate','publish']},{'task_count':3,'task_ids':['extract','validate','publish']},'A parsed inventory does not prove task executions.')
C('airflow','A logical date is recorded separately from start time',0,'Read the supplied scheduler metadata.',{'logical_day':'2026-10-20','started_at':'2026-10-21T00:01:00Z'},{'business_day':'2026-10-20'},'Do not overwrite the logical interval with observed start time.')
C('airflow','A task log records an error without a success result',0,'Classify the supplied task observation.',{'task_id':'load','state':'failed','log_tail':'source missing'},{'task_success':False,'observed_error':'source missing'},'An error message is a diagnosis clue, not a verified recovery.')
C('airflow','A paused DAG has a visible configuration state',0,'Report the supplied training DAG state.',{'dag_id':'orders','paused':True},{'scheduling_enabled':False},'This does not imply already queued runs never execute.')
C('airflow','A task try number counts attempts',0,'Read one supplied task-instance record.',{'task_id':'load','try_number':2,'state':'up_for_retry'},{'attempt_number':2,'completed':False},'Up for retry is not a passing result.')
C('airflow','A dependency prevents report before load',1,'Set the required edge for the two-task training DAG.',{'tasks':['load','report'],'rule':'Report uses loaded output.'},{'edge':['load','report']},'Source-code ordering alone is not dependency enforcement.')
C('airflow','A skipped task differs from a successful task',2,'Summarize supplied task states for one run.',{'task_states':{'validate':'success','publish':'skipped'}},{'validated':True,'published':False},'Skipped publication is a distinct outcome, even when validation succeeded.')

def main():
    previously_proposed = set()
    for number in (8, 9, 10):
        path = base.OUT / f'engineering-promotions{number}.json'
        if path.exists():
            previously_proposed.update(item['original_draft_id'] for item in json.loads(path.read_text(encoding='utf-8'))['proposals'])
    items, states = base.proposals(exclude_ids=previously_proposed)
    errors = base.validate(items, states)
    if errors:
        raise ValueError(errors)
    for item in items:
        item['problem']['authoring']['batch'] = 'engineering-batch11'
    counts = {tool: sum(item['problem']['tool_id'] == tool for item in items) for tool in states}
    wrapper = {'schema_version': 1, 'proposal_version': '2026.10.27.engineering-batch11',
               'publication_status': 'unregistered_proposals', 'proposals': items,
               'counts': {'proposed_promotions': len(items), 'published_added': 0, 'by_technology': counts},
               'validation': {'structural_errors': errors, 'runtime_claim': 'Learner implementations remain unverified.'}}
    path = base.OUT / 'engineering-promotions11.json'
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(wrapper, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    temporary.replace(path)
    checkpoint = {'state': 'prepared_not_published', 'proposed': len(items), 'published_added': 0,
                  'counts': counts, 'proposal_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                  'source_files_sha256': {tool: hashlib.sha256(state['path'].read_bytes()).hexdigest() for tool, state in states.items()},
                  'errors': errors}
    (base.OUT / 'authors/engineering-batch11-checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(checkpoint, indent=2))

if __name__ == '__main__':
    main()
