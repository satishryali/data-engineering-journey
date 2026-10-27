"""Further connected inventory and integrated delivery cases."""
import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('engineering_base8', Path(__file__).with_name('engineering_batch2.py'))
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.CASES = []
C = base.C

C('data-modelling','One stock receipt records a signed change',0,'Identify the inventory effect of this single received pallet.',{'receipt':{'id':'R1','sku':'P1','location':'A','units':5}},{'stock_change':5,'grain':'one receipt event'},'Do not confuse an event change with an end-of-day balance.')
C('data-modelling','A sale event reduces available stock',0,'Classify the inventory direction of the supplied sale.',{'sale':{'id':'S1','sku':'P1','location':'A','units':2}},{'stock_change':-2},'Retain the positive sold-units field in raw evidence while deriving a negative stock movement.')
C('data-modelling','An opening balance and one receipt form a closing balance',1,'Calculate a product-location balance from the supplied opening state.',{'opening':7,'receipt_units':3},{'closing':10},'A receipt adds to the opening balance; it is not the balance itself.')
C('data-modelling','An unshipped order does not consume shipped stock',1,'Keep ordered and physically shipped units distinct.',{'order':{'id':'O1','ordered_units':5,'shipped_units':0},'opening_stock':8},{'closing_physical_stock':8,'open_order_units':5},'Do not reduce physical stock for an order with no shipment under this contract.')
C('data-modelling','Two receipt lines for one SKU remain separate source events',2,'Aggregate received units while preserving each receipt identity.',{'receipts':[{'id':'R1','sku':'P1','units':2},{'id':'R2','sku':'P1','units':3}]},{'total_received':5,'receipt_count':2},'A SKU is an aggregation key, not an event identity.')
C('data-modelling','A correction references the receipt it changes',2,'Represent a receipt correction without creating a second independent delivery.',{'original':{'id':'R1','units':5},'correction':{'original_id':'R1','corrected_units':4}},{'current_received_units':4,'source_versions':2},'Do not sum 5 and 4 as nine received units.')
C('data-modelling','A product-location report keeps identical SKUs separate',3,'Calculate closing balances for the same product at two warehouses.',{'opening':{'A/P1':10,'B/P1':5},'sales':[{'location':'A','sku':'P1','units':3}]},{'closing':{'A/P1':7,'B/P1':5},'enterprise_P1':12},'The warehouse location is part of the balance grain.')
C('data-modelling','A returned item has an explicit restock state',3,'Compute available inventory after two returns with different inspection results.',{'opening':10,'returns':[{'id':'R1','units':2,'restockable':True},{'id':'R2','units':1,'restockable':False}]},{'available_after_returns':12,'quarantined_units':1},'A physical return does not automatically become available stock.')
C('data-modelling','A supplier file and a warehouse file use different product codes',4,'Apply only the supplied approved SKU mapping when joining receipts to inventory.',{'supplier_receipts':[{'supplier_sku':'X1','units':5},{'supplier_sku':'X9','units':2}],'mapping':{'X1':'P1'},'warehouse_skus':['P1']},{'matched_units':5,'unmatched_supplier_codes':['X9']},'Do not guess X9 from its appearance or discard the unmatched receipt silently.')
C('data-modelling','A movement file references a missing location',4,'Reconcile the received location codes against the warehouse catalog.',{'locations':['A','B'],'movements':[{'id':'M1','location':'A','units':2},{'id':'M2','location':'C','units':3}]},{'valid_movement_ids':['M1'],'unresolved_movement_ids':['M2']},'Do not assign location C to A simply to make totals match.')
C('data-modelling','A current balance is rebuilt from ordered movement identities',5,'Apply a small movement ledger and a repeated delivery.',{'opening':10,'movements':[{'id':'M1','delta':3},{'id':'M2','delta':-2}],'replay_id':'M1'},{'closing':11,'logical_movement_count':2},'A replay of M1 must not add another three units.')
C('data-modelling','A day-end snapshot is linked to its movement cutoff',5,'Calculate a declared snapshot at movement sequence 2.',{'opening':10,'movements':[{'sequence':1,'delta':3},{'sequence':2,'delta':-2},{'sequence':3,'delta':5}],'snapshot_cutoff':2},{'snapshot_balance':11,'latest_balance':16},'A later movement must not leak into the earlier snapshot.')
C('data-modelling','A lost stock movement is recovered from retained raw evidence',6,'Rebuild a flawed current balance from the supplied immutable movement list.',{'opening':10,'raw_movements':[{'id':'M1','delta':3},{'id':'M2','delta':-2}],'flawed_balance':13},{'recovered_balance':11,'missing_applied_id':'M2'},'Do not edit raw movement M2 to make the flawed balance appear correct.')
C('data-modelling','A duplicate transfer inbound is repaired without changing outbound history',6,'Reconcile an interrupted transfer whose inbound event was replayed twice.',{'opening':{'A':10,'B':5},'events':[{'id':'T1-out','location':'A','delta':-3},{'id':'T1-in','location':'B','delta':3},{'id':'T1-in','location':'B','delta':3}]},{'closing':{'A':7,'B':8},'duplicate_event_id':'T1-in'},'Do not compensate by deleting the valid outbound side; deduplicate event identity.')
C('data-modelling','A transfer cannot commit only one side',7,'Validate a supplied transfer state before publishing location balances.',{'transfer':'T2','events':[{'side':'out','location':'A','units':2}],'required_sides':['out','in']},{'publish_ready':False,'missing_sides':['in']},'An enterprise total would appear to shrink if the inbound side is missing.')
C('data-modelling','A stock correction distinguishes physical count from sale',7,'Model a cycle-count adjustment with its reason and effect.',{'ledger_balance':10,'physical_count':8,'reason':'cycle_count','event_id':'C1'},{'adjustment_delta':-2,'closing_balance':8,'sale_units_created':0},'Do not fabricate a customer sale to explain an inventory correction.')
C('data-modelling','A monthly inventory sum is not a month-end balance',8,'Assess an aggregate over supplied daily balances.',{'daily_balances':[{'day':1,'balance':10},{'day':2,'balance':12},{'day':3,'balance':8}]},{'month_end_balance':8,'invalid_sum':30},'Inventory balance is semi-additive across time.')
C('data-modelling','A partition-local unique check misses a cross-day event replay',8,'Check movement identity across two date partitions.',{'partitions':{'day1':['M1'],'day2':['M1']},'identity_scope':'global'},{'duplicate_ids':['M1'],'partition_only_valid':False},'A date partition is physical storage layout, not a new business identity namespace.')
C('data-modelling','A balance API release retains its unit contract',9,'Check the supplied consumer against a proposed stock-unit change.',{'consumer_requires':'each','proposed_output':{'amount':2,'unit':'case'},'case_size':12},{'compatible_without_conversion':False,'required_each':24},'A numerically plausible 2 is wrong for a consumer expecting individual units.')
C('data-modelling','A history purge must preserve an active recall investigation',9,'Select eligible synthetic movement events under the supplied retention policy.',{'today':100,'age_limit':30,'events':[{'id':'M1','day':1,'hold':True},{'id':'M2','day':1,'hold':False},{'id':'M3','day':90,'hold':False}]},{'eligible':['M2'],'preserve':['M1','M3']},'Produce an exact plan only; no real movement history may be deleted.')
C('data-modelling','Independent stock ledger reconciles transfers and returns',10,'Implement a bounded product-location ledger and report after receipt, transfer and inspected return.',{'opening':{'A/P1':10,'B/P1':5},'events':[{'id':'E1','kind':'receipt','location':'A','units':3},{'id':'T1','kind':'transfer','from':'A','to':'B','units':4},{'id':'R1','kind':'return','location':'B','units':2,'restockable':True}]},{'closing':{'A/P1':9,'B/P1':11},'enterprise_P1':20},'Show actual schema, event application, replay and failure tests; transfer must conserve enterprise stock.')
C('data-modelling','Independent inventory snapshots recover a faulty cutoff',10,'Build and test day-end snapshots from retained movement identities.',{'opening':10,'events':[{'id':'M1','day':1,'delta':3},{'id':'M2','day':2,'delta':-2}],'incorrect_day1_snapshot':11},{'correct_snapshots':{'1':13,'2':11},'bad_snapshot_retained_for_audit':True},'Prove cutoff logic, correction publication, replay safety and consumer query results.')

def main():
    items, states = base.proposals()
    errors = base.validate(items, states)
    if errors:
        raise ValueError(errors)
    for item in items:
        item['problem']['authoring']['batch'] = 'engineering-batch8'
    counts = {tool: sum(item['problem']['tool_id'] == tool for item in items) for tool in states}
    wrapper = {'schema_version': 1, 'proposal_version': '2026.10.27.engineering-batch8',
               'publication_status': 'unregistered_proposals', 'proposals': items,
               'counts': {'proposed_promotions': len(items), 'published_added': 0, 'by_technology': counts},
               'validation': {'structural_errors': errors, 'runtime_claim': 'Learner implementations remain unverified.'}}
    path = base.OUT / 'engineering-promotions8.json'
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(wrapper, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    temporary.replace(path)
    checkpoint = {'state': 'prepared_not_published', 'proposed': len(items), 'published_added': 0,
                  'counts': counts, 'proposal_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                  'source_files_sha256': {tool: hashlib.sha256(state['path'].read_bytes()).hexdigest() for tool, state in states.items()},
                  'errors': errors}
    (base.OUT / 'authors/engineering-batch8-checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(checkpoint, indent=2))

if __name__ == '__main__':
    main()
