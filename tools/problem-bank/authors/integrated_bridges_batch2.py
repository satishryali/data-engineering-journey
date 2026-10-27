"""Author the second connected integrated-pipeline bridge batch.

Each compact row is an explicit case, not a Cartesian template expansion.
The output is append-only by ID and is not automatically published.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BANK = ROOT / 'tools/problem-bank'
OUT = BANK / 'integrated-bridges-batch2.json'
CHECKPOINT = BANK / 'authors/integrated-bridges-batch2-checkpoint.json'
ROWS = []


def add(block):
    for line in block.strip().splitlines():
        if not line.strip():
            continue
        cells = line.split('|')
        if len(cells) != 6:
            raise ValueError(f'Expected 6 authored fields, found {len(cells)}: {line}')
        level, title, task, fixture, expected, boundary = cells
        ROWS.append((int(level), title, task, fixture, expected, boundary))


add(r'''
0|Read a supplier batch label|A receiving clerk wants the supplier's literal batch label before any loading; display it.|label='BX-09'; received_at='2026-10-27T08:00Z'|batch_label='BX-09'|Do not substitute the receipt timestamp for the batch label.
0|Notice an empty header cell|A CSV intake screen previews its header and must report a blank third heading.|header='batch_id,sku,'|headings=3; blank_heading_position=3|A trailing delimiter is evidence of a blank heading, not a finished two-column header.
0|Keep a leading-zero store code|A lake folder preview uses the supplied store code exactly as text.|store_code='0042'; business_day='2026-10-26'|store_code='0042'|Integer conversion changes the location's business key.
0|Name the requested API page|A source request log must show the page that operations asked for.|request={endpoint:'orders',page:1}|requested_page=1|Do not infer the page from an unrelated response body.
0|Distinguish present from processed|A warehouse intake file has appeared but no transformation has run; state both facts.|landing=['north.csv']; transform_runs=[]|present=true; processed=false|File visibility alone cannot set a processed marker.
0|Keep one source record unchanged|A staging preview must retain the original one-row text for later diagnosis.|raw='S1,SKU-A,0\n'|raw_preserved='S1,SKU-A,0\n'|Do not normalize away the zero or terminal newline in raw evidence.
0|Identify one expected landing path|A store sends a dated delivery and support needs its intended landing location.|store='0042'; day='2026-10-26'; name='stock.csv'|path='store=0042/day=2026-10-26/stock.csv'|The load run date is not the declared business date.
0|Count one acknowledged extract|A database export returns one record; record the count before writing elsewhere.|extract=[{order_id:'O1'}]|extracted=1; written=0|Extraction count is not evidence of a successful sink write.
''')

add(r'''
1|Parse a quoted store label|An uploaded CSV has a store name with a comma; return exactly its two fields.|line='"Market, North",0042'|fields=['Market, North','0042']|A blind comma split corrupts the location key.
1|Reject a missing item key at intake|A supplier sends one identified SKU and one blank SKU; separate them before loading.|rows=[{sku:'A',units:2},{sku:'',units:3}]|accepted=['A']; rejected_count=1|A rejected row must retain its original position.
1|Retain a negative return quantity|A returns feed uses negative units to represent a return; show it as signed data.|record={event:'R1',units:-2,type:'return'}|R1.units=-2|Do not silently clamp all negative units to zero.
1|Distinguish a zero-byte file from an absent file|A manifest lists an empty control file and a missing data file.|expected=['control.txt','stock.csv']; listed={control.txt:0}|empty=['control.txt']; missing=['stock.csv']|A visible zero-byte file is not the same as a missing path.
1|Preserve exact invoice cents|A payment extract uses integer minor units; show the recorded amount.|record={invoice:'I1',cents:105}|I1.cents=105|Do not interpret 105 cents as 105 whole currency units.
1|Report a non-success source response|A sales API returns 429 with a retry header; report its state without accepting rows.|request_page=2; response={status:429,retry_after_seconds:30,body:'busy'}|state='rate_limited'; accepted=0; retry_after=30|An HTTP 429 is neither an empty successful page nor permission to retry immediately.
1|Keep a null warehouse zone|A goods receipt lacks zone assignment; keep it visible as unknown.|record={receipt:'G1',zone:null}|G1.zone=null; rows=1|Unknown zone must not be mislabeled as zone zero.
1|Verify the declared encoding|A partner labels a tiny file UTF-8; decode and preserve the non-ASCII name.|bytes_utf8='caf\u00e9'; declared_encoding='UTF-8'|text='caf\u00e9'|Replacement characters are a data-quality failure.
1|Read an extract upper bound|A database source records its maximum extract ID before a run.|source_ids=[10,11,12]; prior_bound=9|captured_upper_bound=12|A subsequent arrival with ID 13 belongs to another extract window.
1|Report one sink acknowledgement|A PostgreSQL insert acknowledges one row; pair it with the source record identity.|source_id='O1'; insert_returning=['O1']|acknowledged=['O1']; pending=[]|A successful connection alone is not a row acknowledgement.
1|Label an optional phone field|A reporting export includes an optional phone column with an empty value.|row={customer:'C1',phone:''}|customer='C1'; phone_state='empty'|Do not invent a phone number or drop the customer.
1|Inspect one Spark schema field|A notebook displays its input schema before transformation; report the unit type.|schema={order_id:string,units:integer}; rows=1|units_type='integer'|One successful row count does not prove the intended schema.
''')

add(r'''
2|Match a copy to its source name|A copy run lists source and landing objects; show the source-to-sink mapping.|source='supplier/a.csv'; landed='raw/day=26/a.csv'|mapping={source:'supplier/a.csv',landed:'raw/day=26/a.csv'}|Do not replace the source name with the landing path in lineage.
2|Compare two extract windows|A database export reads IDs after 10 through a captured bound of 13.|ids=[9,11,12,13,14]; lower=10; upper=13|exported=[11,12,13]|ID 14 arrived after the window was captured.
2|Separate source and transformation failures|A run copied one file successfully but parsing failed; report the failing stage.|copy='Succeeded'; parse='Failed'; publish='NotStarted'|failing_stage='parse'; published=false|A green copy result does not make the whole pipeline successful.
2|Join a receipt to its supplier|A receipt carries supplier code P2 and a tiny reference table supplies its name.|receipts=[{id:'G1',supplier:'P2'}]; suppliers={P2:'North Goods'}|G1.supplier_name='North Goods'|Keep G1 even if another receipt has an unknown supplier.
2|Check a per-file count before union|Two extracts contain one and two records; compare each manifest count first.|A={declared:1,rows:['A1']}; B={declared:2,rows:['B1','B2']}|A.valid=true; B.valid=true; combined=3|Combined count alone can hide offsetting per-file errors.
2|Keep two event namespaces distinct|A file and an API both send ID 5; create source-scoped identities.|file=[{id:'5'}]; api=[{id:'5'}]|keys=['file/5','api/5']; count=2|Bare ID 5 is not globally unique.
2|Detect a bad renamed column|A supplier changes quantity to qty in one file; report the missing contract field.|required=['sku','quantity']; observed=['sku','qty']|missing=['quantity']; accepted=0|Do not guess a renamed field without an approved mapping.
2|Keep a late receipt's event date|A file arrives after midnight but carries the previous store business day.|event_day='2026-10-26'; arrival_day='2026-10-27'|partition_day='2026-10-26'|Arrival day cannot silently redate the receipt.
2|Compare copied bytes with manifest|An ADF copy produces a file shorter than the declared object.|manifest_bytes=15; landing_bytes=12; copy_status='Succeeded'|verified=false; downstream_started=false|Activity success cannot override byte-count evidence.
2|Check a product lookup miss|A sales row references an absent product; keep it unresolved, not priced at zero.|sale={id:'S2',sku:'Z'}; product_prices={A:10}|unresolved=['S2']; priced=[]|No product match is not proof of a zero price.
2|Merge exact cents from two channels|Two channel extracts supply amounts in integer cents; reconcile by channel.|web=[105]; store=[95,100]|web=105; store=195; total=300|Do not parse integer cents as floating currency.
2|Expose a page gap|An API response list contains pages 1 and 3 after a requested three-page extract.|requested=[1,2,3]; returned=[1,3]|missing_pages=[2]; complete=false|Do not publish a partial extract as a complete day.
2|Preserve a source correction flag|A supplier marks one new row and one correction; carry the operation marker into staging.|rows=[{id:'A',op:'insert'},{id:'B',op:'update'}]|operations={A:'insert',B:'update'}|Do not treat the correction as a second independent B event.
2|Keep a distinct file checksum per delivery|Two identically named files land on different days; preserve their day and digest.|files=[{day:'26',name:'stock.csv',digest:'aa'},{day:'27',name:'stock.csv',digest:'bb'}]|delivery_keys=['26/stock.csv/aa','27/stock.csv/bb']|Filename alone is insufficient for source identity.
''')

add(r'''
3|Load a receipt with source lineage|Write one validated receipt to PostgreSQL and query its source file.|receipt={id:'G1',units:2}; source='north.csv'|stored={id:'G1',units:2,source:'north.csv'}|The reported source must be the original file, not the table name.
3|Reject one invalid unit without losing its neighbor|A two-row delivery has one numeric and one text quantity.|rows=[{id:'G1',units:2},{id:'G2',units:'many'}]|accepted=['G1']; quarantine=['G2']; reason='units_type'|Do not coerce the word many into an invented count.
3|Keep the staging and final row counts|An intake job stages three rows and validates two.|staged=['G1','G2','G3']; rejected=['G3']|staged=3; accepted=2; rejected=1|A final count of two alone does not explain the third source row.
3|Prevent a duplicate import on rerun|The same source object is delivered twice with unchanged checksum.|deliveries=[{name:'a.csv',digest:'abc'},{name:'a.csv',digest:'abc'}]|processed_objects=1; receipt_rows=1|Keep two run attempts without duplicating the business row.
3|Reconcile a simple customer total|Two receipts for one customer and none for another feed a report.|customers=['C1','C2']; receipts=[{customer:'C1',units:2},{customer:'C1',units:3}]|C1=5; C2=0|Do not hide C2 with an inner join.
3|Commit a validated batch atomically|A two-row batch has a negative sale rejected by its table constraint.|before=['S0']; batch=[{id:'S1',amount:5},{id:'S2',amount:-1}]|after=['S0']; committed_new=0|A partially inserted S1 is not acceptable for this atomic batch.
3|Land one API response with a request ledger|A successful response is saved with its requested page and status.|request={page:2}; response={status:200,events:[{id:'E2'}]}|landing_events=['E2']; request_page=2; status=200|The ledger must not rely on parsing page number from E2.
3|Compare database and lake row identities|A small extract lands as a file; prove both sides contain the same keys.|database_ids=['O1','O2']; landed_ids=['O2','O1']|same_id_set=true; row_count=2|Equal counts with different IDs would not pass.
3|Keep a rejected price's original text|A malformed price is quarantined while another sale proceeds.|rows=[{id:'S1',price:'2.50'},{id:'S2',price:'2..5'}]|accepted=['S1']; rejected={id:'S2',raw:'2..5'}|Never store a guessed numeric value for S2.
3|Publish a confirmed empty day|A signed manifest says zero records and the header-only file exists.|manifest_count=0; file='id,units\n'|status='confirmed_empty'; published_rows=0|A missing file would be a different status.
3|Create a source-aware sales key|Two shops use order number 9; store each without collision.|orders=[{shop:'A',id:'9'},{shop:'B',id:'9'}]|stored_keys=['A/9','B/9']|A unique constraint on bare order ID would reject valid data.
3|Keep old and amended source rows|A supplier corrects receipt G1 units from 2 to 3.|versions=[{id:'G1',v:1,units:2},{id:'G1',v:2,units:3}]|history=2; current_units=3|Do not erase v1 from source audit history.
3|Verify a copied file's content count|A copy tool reports two source rows and two sink rows; query the destination.|copy={source_rows:2,sink_rows:2}; destination=['A','B']|verified_rows=2; copy_reconciled=true|A success flag with only one queried row must fail verification.
3|Preserve null versus zero in a sales aggregate|One amount is zero and one is unknown; show distinct states.|sales=[{id:'S1',amount:0},{id:'S2',amount:null}]|known_total=0; unknown_count=1|Do not make unknown count disappear through coalescing.
3|Associate a run ID with a load|A support engineer must find which run inserted G1.|load={run_id:'R17',source:'a.csv',ids:['G1']}|G1.run_id='R17'; G1.source='a.csv'|A global latest-run ID is not stable lineage for a prior row.
3|Protect a one-row lookup table|A duplicate product key appears in reference data before joining sales.|products=[{sku:'A',price:10},{sku:'A',price:11}]; sale={sku:'A',units:1}|join_blocked=true; duplicate_product_key='A'|Choosing an arbitrary price would produce an unreliable sale value.
''')

add(r'''
4|Map two vendor quantity names|An ADF landing flow receives quantity from one vendor and pieces from another; produce a shared typed column.|A=[{id:'A1',quantity:2}]; B=[{id:'B1',pieces:3}]|rows=[{id:'A1',units:2},{id:'B1',units:3}]|Retain the vendor-specific source field names in lineage.
4|Reconcile a file with its PostgreSQL extract|A daily customer extract is written to ADLS; compare keys, not just counts.|pg_ids=['C1','C2']; lake_ids=['C1','C3']|reconciled=false; missing=['C2']; unexpected=['C3']|Two rows on each side are insufficient evidence of equality.
4|Prevent a join from multiplying receipts|A product reference contains two current rows for SKU A; identify why one receipt becomes two.|receipt={sku:'A',units:2}; products=[{sku:'A',category:'food'},{sku:'A',category:'grocery'}]|join_rows=2; publication_allowed=false|Do not use DISTINCT to conceal an unresolved reference conflict.
4|Build a dated landing layout|Three vendor files for two business days need predictable ADLS locations.|files=[{vendor:'A',day:'26',name:'x.csv'},{vendor:'A',day:'27',name:'y.csv'},{vendor:'B',day:'26',name:'z.csv'}]|paths=['vendor=A/day=26/x.csv','vendor=A/day=27/y.csv','vendor=B/day=26/z.csv']|Do not partition by upload time when the file declares a business day.
4|Keep a source partition when querying|A Spark read combines two vendor partitions and returns only vendor B's keys.|A=['A1']; B=['B1','B2']; filter_vendor='B'|ids=['B1','B2']; count=2|Do not infer vendor from the order ID prefix.
4|Preserve a raw copy beside a parsed table|A landing object contains one invalid row; retain bytes and a typed accepted table.|raw='id,units\nG1,2\nG2,two\n'|raw_rows=2; accepted=['G1']; rejected=['G2']|A typed table must not replace the raw source evidence.
4|Attach ADF and notebook run IDs|An ADF copy starts a Databricks transform; make G1 traceable through both.|copy_run='C18'; notebook_run='N23'; source_id='G1'|lineage={G1:['C18','N23']}|A single latest-run value cannot explain this historical row.
4|Load a Delta table with one correction|A new source version changes G1 units and adds G2; maintain one current row per key.|current=[{id:'G1',units:2}]; incoming=[{id:'G1',units:3},{id:'G2',units:1}]|current=[{id:'G1',units:3},{id:'G2',units:1}]|The corrected G1 must not become a second current business row.
4|Compare a table's version and contents|A Delta write increments the version; verify its actual row keys.|before_version=4; after_version=5; expected_ids=['G1','G2']; observed_ids=['G1','G2']|version_advanced=true; keys_match=true|Version advancement alone does not prove the right data landed.
4|Record an API cursor alongside landing|An API uses a continuation token; save the page and successor token without exposing credentials.|page=1; response_ids=['E1']; next_cursor='cursor-2'|ledger={page:1,ids:['E1'],next_cursor:'cursor-2'}|A pagination cursor is operational state, not an API secret token.
4|Apply a store time zone to a source instant|A shop in California reports an event near UTC midnight; calculate its local business date.|event_utc='2026-10-27T01:00:00Z'; zone='America/Los_Angeles'|local_day='2026-10-26'|Do not partition this sale by the UTC calendar date.
4|Stage a slowly changing supplier label|A supplier's display name changes while its stable ID remains P1.|old={id:'P1',name:'North Goods'}; new={id:'P1',name:'Northern Goods'}|stable_supplier_id='P1'; labels=2|Display name must not become the supplier key.
4|Verify a two-table reporting grain|A report has one customer row and two order rows; keep totals at customer grain.|customers=['C1']; orders=[{id:'O1',customer:'C1',cents:100},{id:'O2',customer:'C1',cents:200}]|customer_total_cents=300; customer_rows=1|Joining detail without grouping can duplicate a customer result.
4|Separate storage permission from data validity|A file has valid columns but the training identity cannot read the ADLS path.|schema_valid=true; read_result='403'; path='landing/north.csv'|status='access_denied'; parsed_rows=0|Do not label a permission failure as an invalid CSV.
4|Report a skipped child activity|ADF copy failed, so the Databricks transform did not start; keep both states.|copy='Failed'; transform='Skipped'|pipeline='Failed'; transform_attempts=0|A skipped transform is not an empty successful transform.
4|Compare declared and inferred Spark type|A quantity column contains '2' and 'bad'; verify against required integer schema.|raw_values=['2','bad']; required_type='integer'|valid=[2]; rejected=['bad']; declared_type='integer'|Do not accept inferred string type as the target contract.
4|Write a small coverage report|Two regions are expected; one has no deliveries but is complete.|manifest={north:'complete',south:'complete'}; rows={north:['G1'],south:[]}|north=1; south=0; complete_regions=2|A confirmed empty region must remain visible in coverage.
''')

add(r'''
5|Assemble a file-to-PostgreSQL mini-pipeline|A supplier file has one good and one malformed receipt; land, validate, load and reconcile.|raw='id,units\nG1,2\nG2,x\n'; expected_rows=2|source=2; stored=['G1']; quarantine=['G2']|Show actual table and rejection records, not only a script exit code.
5|Combine database and API customer activity|PostgreSQL orders and API returns must form one customer activity result.|orders=[{id:'O1',customer:'C1',cents:500}]; returns=[{id:'R1',customer:'C1',cents:100}]|C1.net_cents=400; source_events=2|A return reduces value but is not a duplicate order.
5|Publish a two-day lake-to-Delta slice|Two dated landing objects become one Delta reporting table with day lineage.|day26=['G1']; day27=['G2']|table_ids=['G1','G2']; day_counts={26:1,27:1}|Do not lose the business day when combining files.
5|Track one extraction watermark after commit|A database extract reads changes through ID 12; advance its bound only after sink verification.|prior_bound=10; changed=[11,12]; sink_ids=[11,12]|new_bound=12; loaded=2|Do not advance to 12 before both rows are durable.
5|Run a small ADF-to-notebook handoff|A copy delivers a checked object and passes its exact path to a Databricks task.|copy={status:'Succeeded',path:'raw/day=26/a.csv',rows:2}; notebook_input='raw/day=26/a.csv'|handoff_valid=true; transformed_rows=2|Notebook input must be the copy's produced path, not a hard-coded prior day.
5|Reconcile daily sales across three layers|A raw file, curated table and report should agree on valid cents.|raw=[100,200,'bad']; curated=[100,200]; report_total=300|source=3; accepted=2; rejected=1; report_cents=300|A matching report total does not explain an untracked rejected row.
5|Build an explicit run ledger|A two-stage job should preserve copy and transform outcomes plus counts.|copy={id:'C1',rows:2}; transform={id:'T1',accepted:1,rejected:1}|ledger={copy:'C1',transform:'T1',source:2,accepted:1,rejected:1}|Do not overwrite the copy run ID with the transform ID.
5|Make the second delivery idempotent|The same delivery file is replayed after a lost acknowledgement; show one business result and two attempts.|file_digest='abc'; attempts=['R1','R2']; rows=['G1','G2']|business_rows=2; attempt_history=2|A retry must not duplicate G1 or G2.
5|Build a source-quality decision gate|A file has 90 accepted and 10 rejected rows against a maximum rejection ratio of 5 percent.|source=100; rejected=10; max_ratio=0.05|publish=false; observed_ratio=0.10|Do not publish solely because some valid rows exist.
5|Publish customer totals with missing customers|Customer dimension C2 has no valid sales; a daily model must retain it.|customers=['C1','C2']; sales=[{customer:'C1',cents:300}]|totals={C1:300,C2:0}; rows=2|Do not invent a C2 sale to force the zero result.
5|Load a product correction with history|A supplier revises one product category; keep as-of and current views.|versions=[{sku:'A',category:'food',day:'01'},{sku:'A',category:'grocery',day:'20'}]|as_of_10='food'; current='grocery'; history=2|Current category must not rewrite the historical day-10 report.
5|Compare two scheduling orders|A daily reporting job must wait for complete landing and a successful transform.|landing='complete'; transform='Failed'; report='NotStarted'|publish=false; reason='transform_failed'|A complete landing alone does not satisfy the reporting dependency.
5|Route rejected rows into a review table|A bank transfer source includes one malformed currency code; valid rows continue with quarantine.|rows=[{id:'T1',currency:'INR'},{id:'T2',currency:'???'}]|accepted=['T1']; review=['T2']; source_count=2|The review table must retain the original currency value.
5|Capture a pipeline's actual output path|A parameterized day run writes a new curated path; record it for consumers.|business_day='2026-10-26'; output='curated/day=2026-10-26/sales.parquet'|published_path='curated/day=2026-10-26/sales.parquet'|Do not announce a path until reconciliation and durable write complete.
5|Compare a local and Spark result on one slice|The same two-row transformation runs locally and in Spark; compare keys and cents.|source=[{id:'A',cents:100},{id:'B',cents:200}]; local_total=300; spark_total=300|same_keys=true; same_total=true|Do not claim performance superiority from this tiny correctness check.
5|Keep a verified empty API page|An API returns 200 with zero events and an end cursor; record completion.|response={status:200,events:[],next:null}; requested_page=3|page3='confirmed_empty'; pagination_complete=true|A timeout on page 3 would not prove an empty result.
5|Create a small restart point|A job finishes file A but fails before file B; record exactly what can restart.|A={digest:'aa',status:'committed'}; B={digest:'bb',status:'failed'}|resume_files=['B']; preserve_files=['A']|A full replay may occur but must never duplicate A's business rows.
''')

add(r'''
6|Recover after a partial PostgreSQL commit|A receipt batch fails on its second row; inspect and restore the agreed atomic outcome.|before=['G0']; attempted=['G1','G2']; observed_after=['G0','G1']; expected_atomic=true|recovered_after=['G0']; failed_attempt_preserved=true|Do not mark the batch complete while G2 is absent.
6|Retry an ADF copy without duplicate sink rows|A failed copy landed its first object before timeout; retry should reconcile both.|source=['a.csv','b.csv']; first_sink=['a.csv']; retry_sink=['a.csv','b.csv']|sink_files=2; duplicate_files=0; retry_count=1|Do not delete a verified prior-day file while recovering this run.
6|Hold a watermark after a Delta merge error|The source has versions 11 and 12, but the merge failed on 12.|prior_watermark=10; staged=[11,12]; durable=[11]|watermark_after_failure=10; retry_candidates=[11,12]|Even a partly durable write cannot justify skipping version 11 during recovery.
6|Restore a missing quarantine record|A valid row loaded but an invalid source row was lost from review storage.|source=['G1','G2']; loaded=['G1']; quarantine=[]; G2.units='bad'|reconciled=false; recovered_quarantine=['G2']|Do not claim source=accepted+rejected until the rejection is durable.
6|Distinguish a transient API outage from empty data|The final API page times out twice then succeeds with no events.|attempts=['timeout','timeout',{status:200,events:[],next:null}]|confirmed_empty=true; attempts=3|The first two timeouts must remain failed attempts, not zero-row successes.
6|Recover a malformed partition day only|A Spark job discovers one bad schema in day 27 while day 26 remains valid.|day26={schema:'v1',ids:['G1']}; day27={schema:'broken',ids:['G2']}|day26_preserved=true; day27_quarantined=true|Do not erase the good prior partition during isolation.
6|Rebuild a failed report from durable source rows|A report write failed after curated sales committed; rerun only the report result.|curated_ids=['S1','S2']; report_ids=['S1']; expected_total=2|report_ids_after=['S1','S2']; curated_unchanged=true|Do not re-ingest source events just to repair a downstream report.
6|Repair a late product correction safely|A product correction arrived after yesterday's report; rebuild affected rows only.|sales=[{id:'S1',sku:'A',day:'26'},{id:'S2',sku:'B',day:'26'}]; corrected_sku='A'|recomputed=['S1']; unchanged=['S2']|Do not overwrite unrelated product B history.
6|Refuse a duplicate source version conflict|Two files claim the same supplier event and version but different units.|A={id:'G1',v:2,units:3}; B={id:'G1',v:2,units:4}|current_unchanged=true; conflict='G1/v2'|Last-writer-wins is not an agreed correction rule.
6|Recover from an incompatible Delta constraint change|A new nonnull warehouse constraint rejects an existing valid row with unknown warehouse; test a compatible recovery in scratch.|prior=[{id:'G1',warehouse:null}]; candidate_constraint='warehouse_not_null'; restore_target='scratch'|scratch_rows=1; G1.warehouse=null; candidate_published=false|Do not erase G1 merely to make the proposed constraint pass.
6|Re-run a missed dated file without double counting|A manifest lists days 26 and 27, but day 27 was absent in first run.|first={day26:['G1'],day27:[]}; later_day27=['G2']|final=['G1','G2']; day26_count=1|Do not mark day 27 confirmed empty when the file was missing.
6|Handle a permission failure after successful copy|ADF copied a file, but Databricks cannot read it due to ACL settings.|copy='Succeeded'; notebook_read='403'; sink_path='raw/day=26/a.csv'|pipeline='Failed'; parsed_rows=0; issue='read_permission'|Do not rewrite source schema to address an access-denied response.
6|Retry a rate-limited API page after its window|A source gives 429 with a 30-second window; a later permitted attempt succeeds.|first={status:429,retry_after:30}; second={at_second:31,status:200,ids:['E2']}|accepted=['E2']; early_attempts=0|Do not hammer the API before its advertised retry window.
6|Recover a mismatched customer report count|Customer totals query returns one row although the dimension has two customers.|customers=['C1','C2']; observed_report=['C1']; sales=[{customer:'C1',cents:5}]|repaired_report={C1:5,C2:0}|Do not convert the missing C2 report row into evidence of no customer.
6|Protect a sink after checksum mismatch|A landed object's digest differs from its signed manifest; hold downstream work.|manifest_digest='aaa'; landed_digest='bbb'; prior_sink=['G0']|sink_after=['G0']; held_object=true|Do not parse or publish bytes that failed the source integrity check.
6|Reconcile a notebook timeout with table state|A notebook call times out after a possible commit; inspect the table before retry.|call='timeout'; target_before=['G0']; target_after=['G0','G1']; source=['G1']|retry_plan='idempotent_check'; final_ids=['G0','G1']|Unknown acknowledgement is not proof that no write occurred.
6|Preserve an error ledger during correction|A bad row is corrected and accepted in a later run; keep both run outcomes.|run1={id:'G2',units:'x',status:'rejected'}; run2={id:'G2',units:2,status:'accepted'}|current_units=2; attempt_history=2|Deleting the first error hides the reason for the re-delivery.
''')

add(r'''
7|Normalize two regional time zones for one report|New York and Kolkata shops report local close times; map each to its own business day.|events=[{shop:'NY',local:'2026-11-01T01:30',offset:'-04:00'},{shop:'IN',local:'2026-11-01T01:30',offset:'+05:30'}]|store_day={NY:'2026-11-01',IN:'2026-11-01'}; utc_instants_differ=true|Ambiguous fall-back times need recorded offsets, not naive timestamp strings.
7|Evolve an optional supplier column|A new source sends region while old files do not; keep both contract versions valid.|old={id:'G1',units:2}; new={id:'G2',units:3,region:'west'}|G1.region=null; G2.region='west'; count=2|Required id and units remain required in both versions.
7|Handle a renamed supplier code with mapping history|A supplier code changed from P1 to P9; preserve identity and source values.|mapping=[{source:'P1',canonical:'SUP-A',valid_to:'26'},{source:'P9',canonical:'SUP-A',valid_from:'27'}]|canonical_ids=['SUP-A']; raw_codes=['P1','P9']|Do not rewrite the historical raw code to P9.
7|Join sales to time-valid prices|A price changes on day 20; two sales on days 10 and 26 need different prices.|prices=[{sku:'A',from:'01',cents:100},{sku:'A',from:'20',cents:120}]; sales=[{day:'10',sku:'A'},{day:'26',sku:'A'}]|priced_cents=[100,120]|Current price cannot revalue an old sale.
7|Delay publication during partial backfill|A 3-day repair has built days 1 and 2 but failed on day 3; readers see last good set.|published={days:[1,2,3],version:'old'}; candidate={days:[1,2],version:'new'}|reader_version='old'; candidate_published=false|A partly rebuilt range must not replace the complete published range.
7|Resolve late cancellation against prior sale|An order appears then is cancelled a day later; keep both events and current net.|events=[{id:'O1',type:'sale',cents:100},{id:'O1',type:'cancel',cents:-100}]|event_count=2; net_cents=0; current='cancelled'|Do not delete the sale event to achieve zero net.
7|Keep two distinct key namespaces through merge|Retail and wholesale systems each use order 7; a Delta merge must retain both.|rows=[{source:'retail',id:'7',cents:100},{source:'wholesale',id:'7',cents:200}]|business_rows=2; total_cents=300|Matching only on numeric ID would overwrite a valid order.
7|Prove reference-table uniqueness before fanout|A country mapping unexpectedly has two matches for one source code; block its join.|orders=[{id:'O1',country:'IN'}]; country_map=[{code:'IN',name:'India'},{code:'IN',name:'Bharat'}]|publish=false; duplicate_lookup_key='IN'|A doubled count after joining cannot be accepted as genuine source growth.
7|Carry a deletion through the report|A privacy-approved account deletion arrives after its earlier sale; preserve authorized audit totals separately.|customer='C1'; event='delete'; live_customers=['C1']; live_orders=['O1']|live_customers=[]; live_orders_redacted=true; audit_count=1|Do not leave personal data in a debug or quarantine table.
7|Detect overlapping API cursor windows|Two pages overlap on event E2; deduplicate by source event identity, not page number.|page1=['E1','E2']; page2=['E2','E3']|current_events=['E1','E2','E3']; fetched_rows=4|Keep page-level fetch counts for diagnosis while avoiding duplicate business events.
7|Separate warehouse closure from late arrivals|A day-26 report is closed, then a late day-26 sale arrives on day 28.|closed_day='26'; late_event={id:'S9',business_day:'26',arrival_day:'28'}|repair_required_for='26'; unrelated_day_28_unchanged=true|Do not assign the sale to day 28 to avoid a repair.
7|Coordinate two sinks without false success|A pipeline writes Delta successfully but PostgreSQL serving load fails.|delta='Succeeded'; postgres='Failed'; report_marker='NotWritten'|pipeline='Failed'; report_available=false|One durable sink does not imply complete publication to consumers.
7|Track source schema versions per file|Two vendor files use v1 and v2 schema; record which parser handled each.|files=[{name:'a.csv',schema:'v1'},{name:'b.csv',schema:'v2'}]|parser_map={a.csv:'v1',b.csv:'v2'}|Do not infer old schema solely from the file date.
7|Resolve a duplicate event with conflicting payload|The same source event ID occurs twice with different amounts and no version field.|events=[{id:'E1',cents:100},{id:'E1',cents:120}]|published_E1=false; conflict_count=1|First-writer or last-writer choice requires a business rule not supplied here.
7|Keep correction lineage across batch boundaries|A corrected source row arrives in the next day's file but belongs to the earlier business day.|first={id:'O1',day:'26',cents:100,batch:'B1'}; correction={id:'O1',day:'26',cents:110,batch:'B2'}|current_day26_cents=110; source_batches=['B1','B2']|Do not move O1 to day 27 because B2 arrived then.
7|Validate regional completeness independently|North and south have separate manifests; south is incomplete despite matching combined totals.|north={expected:2,observed:3}; south={expected:2,observed:1}|north_valid=false; south_valid=false; combined=4|Matching aggregate total hides offsetting regional errors.
7|Publish a versioned contract for consumers|A report adds optional return_count while old consumers still request sales_cents.|v1={sales_cents:300}; v2={sales_cents:300,return_count:1}|v1_consumer_sales_cents=300; v2_return_count=1|Do not rename or remove sales_cents during a compatible addition.
''')

add(r'''
8|Measure a skewed store join|One store accounts for most orders; compare join plans against the same result.|orders_per_store={A:99000,B:500,C:500}; stores=['A','B','C']|joined_rows=100000; A_share=0.99; plan_metrics_recorded=true|A changed plan is useful only if output keys and totals stay equal.
8|Bound memory during a large CSV extract|A 500000-row synthetic export exceeds a 64 MB whole-file reader budget.|generated_rows=500000; peak_budget_mb=64; methods=['whole','streamed']|counts_equal=true; streamed_peak_at_most_64mb=true|Record measured peak memory, not a guess based on code style.
8|Compare full and incremental backfill costs|Only 20 of 100000 events changed; measure both routes and reconcile final keys.|baseline=100000; changed=20; strategies=['full','incremental']|final_count=100000_both; changed_applied=20; timings_recorded=true|An apparently faster result with missing keys is invalid.
8|Verify pruning on a dated lake query|A report requests one day from 30 partitioned days; inspect input-file evidence.|days=30; requested='2026-10-26'; files_per_day=4|returned_day='2026-10-26'; scanned_files_at_most=4|Correct rows alone cannot establish that partition pruning occurred.
8|Test small-file compaction against row identity|A landing result has 200 tiny files for 2000 rows; compact only after key reconciliation.|before={files:200,rows:2000}; candidate={files:8,rows:2000}|same_key_set=true; after_files=8; duration_recorded=true|Do not delete raw source files to make the curated file count smaller.
8|Measure a hot-key aggregation|One SKU dominates a Spark aggregate; record skew and a measured alternate plan.|events_per_sku={A:900000,B:50000,C:50000}; expected_total=1000000|aggregate_count=1000000; skew_measured=true; plan_comparison_recorded=true|No optimization can change the grouped cents or missing-key count.
8|Estimate a full versus selective reprocess|A year of 365 dated objects has three corrected days; compare work units.|objects=365; corrected_days=['03-01','06-10','10-26']|selective_objects=3; full_objects=365; output_reconciled=true|The smaller read is valid only if cross-day dependencies were checked.
8|Measure Delta merge match cardinality|A merge source repeats a business key twice; measure and repair source uniqueness first.|target=[{id:'G1',units:1}]; source=[{id:'G1',units:2},{id:'G1',units:3}]|merge_blocked=true; duplicate_source_key='G1'|Do not arbitrarily choose one update to make the merge complete.
8|Benchmark compression without losing bytes|Two supported storage encodings hold the same synthetic curated rows; compare size and scan time.|rows=100000; formats=['parquet_plain','parquet_compressed']|same_keys=true; sizes_measured=true; scan_times_measured=true|A smaller file with changed decimal values fails the benchmark.
8|Compare parallel API fetch within rate limits|A source permits two concurrent pages and 10 calls per minute; measure serial versus bounded fetch.|pages=[1,2,3,4]; concurrency_limit=2; per_minute_limit=10|all_pages_once=true; max_concurrency_at_most_2=true; timings_recorded=true|Faster fetching cannot violate the provider's stated limits.
8|Quantify a relational index decision|A 100000-row order table supports one frequent customer lookup; compare measured query plans.|orders=100000; queried_customer='C7'; candidate_index='customer_id'|same_result_ids=true; before_after_plans_recorded=true|Do not claim improvement from index existence alone.
8|Bound a large backfill by day|A 90-day repair must run in bounded day groups with a 10-day maximum batch.|days=90; max_days_per_batch=10|batch_count_at_least=9; all_days_once=true|No task may process 11 days under the stated limit.
8|Measure warehouse serving latency after rewrite|A revised SQL report joins curated tables differently; compare actual rows, totals and timings.|baseline={rows:1000,cents:90000}; candidate={rows:1000,cents:90000}|same_keys=true; same_cents=true; timings_recorded=true|Matching row count without matching keys is insufficient.
8|Test cache use on a repeated Spark read|A report computes count and exact cents from the same 1M-row frame; measure cached versus uncached runs.|rows=1000000; metrics=['count','cents']; approaches=['cached','uncached']|both_counts=1000000; cents_equal=true; timings_recorded=true|Cache memory cost belongs in the comparison.
8|Measure storage layout for a selective region read|A region-filtered query reads a partitioned and an unpartitioned candidate layout.|regions=10; rows=100000; requested='west'|same_west_ids=true; bytes_scanned_recorded=true; latency_recorded=true|A narrow query must not silently omit west records.
''')

add(r'''
9|Gate publication on independent reconciliation|A daily job copies 100 rows, rejects two and loads 98; verify its marker and changed-input failure.|source=100; accepted=98; rejected=2; sink=98|publish=true; altered_sink_97_publishes=false|An activity's success label cannot override inconsistent counts.
9|Trace a failed order across ADF and Databricks|Order O7 passed copy C7 but failed transform N7; assemble a redacted support trace.|order='O7'; copy='C7'; notebook='N7'; notebook_state='Failed'|trace=['O7','C7','N7']; fault_stage='transform'|Never include linked-service secrets or personal data in the trace.
9|Prove an ADLS least-privilege boundary|A training principal can read its landing partition but cannot read archived partner data.|principal='training-reader'; allow='landing/day=26'; deny='archive/partner-x'|allow_read=true; deny_read=false|Do not grant account-wide access merely to pass the positive test.
9|Restore a historical customer dimension snapshot|An erroneous update changed C1's valid-from date; restore a dated dimension view into scratch and compare both versions.|good={C1:{name:'North',valid_from:'01'}}; current={C1:{name:'North',valid_from:'20'}}; scratch='dimension_restore'|scratch.C1.valid_from='01'; current.C1.valid_from='20'|Do not overwrite the live customer dimension during restore verification.
9|Set a value-drift alert with equal row counts|Two runs have equal source and sink counts, but one sink loses 100 cents; alert on amount reconciliation.|runs=[{source_count:2,sink_count:2,source_cents:300,sink_cents:300},{source_count:2,sink_count:2,source_cents:300,sink_cents:200}]|alerts=[false,true]; drift_cents=100|Equal row counts cannot suppress a monetary mismatch.
9|Block an over-budget cloud backfill|A proposed 30-day reprocess exceeds the agreed training budget before resources start.|budget_units=10; estimate_units=15; proposed_days=30|started=false; reason='over_budget'|Do not provision billable resources just to prove the block.
9|Rehearse a consumer-safe version rollback|A candidate table drops one valid customer; hold it and retain the prior published version.|prior_customers=['C1','C2']; candidate=['C1']; required=['C1','C2']|candidate_published=false; reader_customers=['C1','C2']|Keep candidate failure evidence for diagnosis.
9|Write a restart runbook for an unknown ADF timeout|Copy acknowledgement is missing; the sink may already have G1. Define the required inspections and demonstrate safe rerun.|copy='timeout'; sink_possible=['G1']; source=['G1','G2']|final_ids=['G1','G2']; duplicate_ids=[]; inspected_before_retry=true|A timeout cannot be treated as proof of no side effects.
9|Verify retention without losing current data|A policy archives raw files after 30 days while curated day-26 remains queryable.|raw_age_days={day26:31,day27:1}; curated_days=['day26','day27']|raw_day26_archived=true; curated_day26_queryable=true|Do not delete the only reconstructible source copy.
9|Publish a data contract with failure examples|A new store feed requires store_id, event_id and cents; show acceptance and rejection outcomes.|good={store_id:'S1',event_id:'E1',cents:0}; bad={store_id:'',event_id:'E2',cents:10}|good_accepted=true; bad_rejected='store_id_required'|Zero cents remains a valid known value.
9|Prove monitoring across late arrival|A day was marked complete before a delayed correction arrives; alert and repair status must be observable.|day26={published:true,rows:2}; late={id:'E3',day:'26'}|repair_open=true; published_version_unchanged_until_reconciled=true|Do not silently mutate a closed report without a tracked repair.
9|Test a credential rotation rehearsal|A source secret rotates, but operational evidence must show only health and version identifiers.|before_secret_version='v1'; after_secret_version='v2'; probe_status=200|connector_healthy=true; visible_secret_values=0|Do not copy actual secret material into run logs or screenshots.
9|Verify disaster-recovery row coverage|A scratch restore from a dated backup is compared with the expected manifest and run history.|backup_ids=['G1','G2']; manifest_count=2; restore_ids=['G1','G2']|restore_verified=true; count=2; keys_match=true|A completed restore command without key checks is insufficient.
9|Release a pipeline change behind a quality gate|A candidate transformation passes unit tests but changes a daily total; prevent promotion.|tests='pass'; prior_total=300; candidate_total=290; expected_total=300|promoted=false; discrepancy=10|Test status alone cannot override business reconciliation.
''')

add(r'''
10|Independently reconcile a three-source retail day|A file, API and PostgreSQL extract describe one store day with one malformed return; build and defend the result.|file=[{id:'F1',cents:200}]; api=[{id:'A1',cents:-50},{id:'A2',cents:'bad'}]; pg=[{id:'P1',cents:100}]|accepted=['F1','A1','P1']; rejected=['A2']; net_cents=250|Preserve three source identities, rejection evidence and rerun safety without a supplied implementation plan.
10|Independently recover a split publication|Delta shows the new day but PostgreSQL serving data is old after a failed handoff; restore consistency.|delta_day26=['O1','O2']; serving_day26=['O1']; prior_published=['O0']|serving_after=['O1','O2']; published_after=['O1','O2']; failed_run_retained=true|Consumers must not see a completion marker until both serving layers reconcile.
10|Independently handle an unfamiliar source schema change|A partner renames sku to item_key and adds a nullable warehouse; prove compatible and incompatible cases.|v1={sku:'A',units:2}; v2={item_key:'B',units:3,warehouse:null}; bad={item_key:'',units:1}|accepted=['A','B']; rejected=1; lineage_versions=['v1','v2']|Do not guess a missing key or erase original field names.
10|Independently repair a lost business-day partition|A late repair reveals day 26 absent from a three-day report despite a complete source manifest.|manifest={25:2,26:1,27:2}; published={25:2,27:2}|restored_day26=1; final_total=5; other_days_unchanged=true|A manually patched aggregate is not verified source-to-report recovery.
10|Independently defend a dual-write design choice|Two candidate designs produce the same result but differ in restart and cost evidence; choose using measured data.|A={correct:true,restart:'tested',cost:8}; B={correct:true,restart:'unknown',cost:5}; budget=10|decision_reasoned=true; B_missing_evidence='restart'|Do not declare the cheaper candidate production-ready without recovery proof.
10|Independently trace a duplicate total through joins|A daily total doubles after a product mapping update; locate row multiplication and verify a correction.|sales=[{id:'S1',sku:'A',cents:100}]; mappings=[{sku:'A',category:'food'},{sku:'A',category:'grocery'}]|wrong_total=200; corrected_total=100; conflict_documented=true|DISTINCT on output rows is not a business rule for conflicting mappings.
10|Independently price a shipment with dated freight tariffs|A carrier raises its per-kilogram rate while a prior shipment remains billable under its old contract; prove dated and current views.|tariffs=[{carrier:'P1',from:'01',cents_per_kg:20},{carrier:'P1',from:'20',cents_per_kg:25}]; shipment={carrier:'P1',day:'10',kg:3}|shipment_charge_cents=60; current_rate_cents_per_kg=25; history=2|Applying today's tariff to a past shipment overbills the customer.
10|Independently prove a restart from unknown commit state|A notebook call times out after a possible merge; inspect, replay and show exactly-once business rows.|before=['G0']; source=['G1','G2']; timeout_after_possible_commit=true|final=['G0','G1','G2']; duplicates=0; attempts_preserved=true|Do not assume either that the timeout committed or that it rolled back.
10|Independently design a least-privilege pipeline rehearsal|An unfamiliar feed needs raw write, curated read and archive denial; validate all three with synthetic objects.|principal='pipeline-training'; raw='landing/a.csv'; curated='curated/a.parquet'; archive='archive/other'|raw_write=true; curated_read=true; archive_read=false|No account-wide owner grant may be used to make the test pass.
10|Independently investigate a cost regression|A 10-day backfill doubles cloud cost after a layout change; compare measured input and output before deciding.|before={files:40,rows:100000,cost:8}; after={files:400,rows:100000,cost:16}|same_key_set=true; cost_regression=8; cause_evidence_recorded=true|Do not declare file count the cause without measured execution evidence.
10|Independently defend a complete Azure delivery|Build an isolated ADF, ADLS, Databricks and Delta path for one sales day, including a bad row and a rerun.|raw=[{id:'S1',cents:100},{id:'S2',cents:'bad'}]; replay_same_file=true|source=2; accepted=['S1']; rejected=['S2']; rerun_duplicates=0|Show actual service configuration, observed data, counts and failure history; a diagram alone does not pass.
10|Independently assess operational readiness|An unfamiliar pipeline has a good first run, failed replay and no restore proof; evaluate readiness through tests.|first={source:2,sink:2}; replay={status:'Failed',sink:3}; restore='untested'|ready=false; defects=['rerun_duplicates','restore_unproven']|A passing happy-path run cannot establish production readiness.
''')


DOCS = [
    'https://www.postgresql.org/docs/current/tutorial-sql.html',
    'https://spark.apache.org/docs/latest/api/python/getting_started/quickstart_df.html',
    'https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-overview',
    'https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction',
    'https://docs.databricks.com/aws/en/delta/merge',
]


def make():
    previous = 'RLP-JOBBR-080'
    previous_level = 0
    authored = []
    for number, (level, title, task, fixture, expected, boundary) in enumerate(ROWS, 81):
        if level < previous_level or level > previous_level + 1 or not 0 <= level <= 10:
            raise ValueError('Non-gradual progression: ' + title)
        ident = f'RLP-JOBBR-{number:03d}'
        prereqs = [] if number == 81 else [previous]
        if level >= 4:
            prereqs += ['RLP-PY-011', 'RLP-SQL-008', 'RLP-PG-004']
        if level >= 6:
            prereqs += ['RLP-PYSPARK-001', 'RLP-DELTA-LAKE-001']
        if level >= 9:
            prereqs += ['RLP-ADF-001', 'RLP-ADLS-001', 'RLP-DATABRICKS-001']
        prereqs = list(dict.fromkeys(prereqs))
        authored.append({
            'id': ident, 'tool_id': 'integrated-pipelines', 'title': title,
            'level': level, 'difficulty': f'level_{level}',
            'learning_objective': task,
            'scenario': 'A distributor is connecting source intake to dependable store reporting. ' + task,
            'task': task, 'inputs': {'fixture_contract': fixture},
            'expected_output': {'contract': expected},
            'constraints': [boundary, 'Use synthetic data and an isolated owned target; keep credentials out of evidence.'],
            'acceptance_criteria': [
                'Observed result matches: ' + expected,
                'Demonstrate the boundary: ' + boundary,
                'Submit the actual implementation or configuration, observed output, assistance and one changed-input check.'
            ],
            'prerequisites': prereqs, 'independent_prerequisites': [],
            'skill_prerequisites': [] if level == 0 else [f'integrated pipeline level {level - 1}'],
            'progressive_hints': [
                'Start from the supplied source and identify exactly which evidence the requested output needs.',
                'Check the failure boundary before publishing: ' + boundary,
                'Compare the observed result with ' + expected + '; keep the failed attempt for review.'
            ],
            'engineering_relevance': title + ' is one bounded intake-to-reporting responsibility; after verification, explain its downstream effect and the remaining operational limit.',
            'estimated_minutes': [8, 12, 15, 20, 25, 35, 45, 55, 70, 90, 120][level],
            'official_docs': DOCS, 'verification': {'kind': 'artifact_review'},
            'challenge_kind': 'bridge' if level > previous_level else 'transfer',
            'published_version': '2026.10.27.3',
            'authoring_batch': 'integrated-bridges-explicit-002',
            'sequence': 20000 + number,
        })
        previous, previous_level = ident, level
    return authored


def main():
    authored = make()
    if OUT.exists():
        prior = json.loads(OUT.read_text(encoding='utf-8'))
        registered = 'tools/problem-bank/integrated-bridges-batch2.json' in json.loads(
            (ROOT / 'tools/curriculum.json').read_text(encoding='utf-8')).get('problem_files', [])
        if registered and prior != authored:
            raise ValueError('Refusing reassignment of registered problem IDs or content')
    ids = [row['id'] for row in authored]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate IDs')
    if len({row['title'].casefold() for row in authored}) != len(authored):
        raise ValueError('Duplicate titles')
    OUT.write_text(json.dumps(authored, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    CHECKPOINT.write_text(json.dumps({
        'status': 'authored_unregistered', 'published_additions': 0,
        'authored_count': len(authored), 'levels': dict(Counter(row['level'] for row in authored)),
        'first_id': ids[0], 'last_id': ids[-1],
        'source_sha256': hashlib.sha256(OUT.read_bytes()).hexdigest(),
        'next_id': f'RLP-JOBBR-{81 + len(authored):03d}',
    }, indent=2) + '\n', encoding='utf-8')
    print(f'Authored {len(authored)} unregistered integrated problems: {ids[0]}..{ids[-1]}')


if __name__ == '__main__':
    main()
