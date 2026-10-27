"""Small connected cross-technology distribution contracts, kept outside other agents' files.

Append rows only. Stable JOBBR IDs are guarded against reassignment. A solution to
any one exercise must still be executed or reviewed; authored outputs are targets.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'tools/problem-bank/integrated-bridges.json'
CHECKPOINT = ROOT/'tools/problem-bank/authors/integrated-bridges-checkpoint.json'
ROWS=[]

def add(block):
    for line in block.strip().splitlines():
        if line.strip():
            level,title,task,fixture,expected,boundary=line.split('|')
            ROWS.append((int(level),title,task,fixture,expected,boundary))

add(r'''
0|Name the delivery|A dock operator needs the delivery identifier before processing. Return it without trimming meaningful zeros.|delivery={id:'0007',arrived:'2026-10-26'}|'0007'|The ID remains text; converting to integer changes identity.
0|Count one landing row|An ingestion preview counts rows before any store write. Report the number of supplied data records.|records=[{delivery:'0007',sku:'A'}]|1|The CSV header is not a data record.
0|Check a required column|A partner contract needs delivery_id in its supplied header. Report whether it is present.|headers=['delivery_id','sku','units']|present=true|A column named delivery is not delivery_id.
0|Distinguish zero from absent|A stock intake preview must show zero received units without calling the value missing.|records=[{sku:'A',units:0}]|A:0 units; missing=false|Zero is a valid quantity in this preview.
0|Keep one original source name|A support note must retain the exact external file name for traceability.|name='partner_2026-10-26.csv'|partner_2026-10-26.csv|Do not replace this with a generated output file name.
0|Confirm one processing boundary|A run preview says whether a source file is visible without starting the load.|available=['A.csv']; requested='A.csv'|visible=true; loaded_rows=0|Finding a file does not prove it was processed.
1|Keep a quoted product name intact|A partner CSV contains a comma inside a quoted product name. Return the two parsed fields.|line='"A, small",2'|['A, small','2']|Splitting at every comma would create a third field.
1|Reject a missing delivery key|A landing check separates one bad record while preserving its original text.|rows=[{id:'D1',sku:'A'},{id:'',sku:'B'}]|accepted=['D1']; rejected=[{row:2,reason:'missing_id'}]|The valid first record must not be dropped with the second.
1|Keep price text until conversion|A source sends price as decimal text. Return its exact monetary value and show the original.|price='10.20'|original='10.20'; decimal='10.20'|Binary floating-point display is not money evidence.
1|Compare a manifest count|A two-row source must match its signed manifest row count before loading.|manifest_count=2; rows=[{id:'D1'},{id:'D2'}]|count_match=true|A header-only delivery with manifest_count=2 fails.
1|Identify a failed API response|A tiny source API returns a server error. Keep the requested page number and record the failure.|request_page=3; status=503; body='temporary'|page=3; state='failed'; accepted_rows=0|An HTTP response with 503 is not a successful empty page.
1|Use the declared business date|A delivery carries its business date separately from file modification time.|delivery_date='2026-10-25'; modified_date='2026-10-26'|reported_business_date='2026-10-25'|Modification time cannot silently redefine the business day.
2|Reconcile two source row counts|Two independent sources report the same store-day; count both without conflating their records.|POS=[{id:'P1'}]; web=[{id:'W1'},{id:'W2'}]|POS=1; web=2; combined=3|A local ID from each source can be equal without being one event.
2|Make a composite event identity|Two partners both send event 7. Preserve source identity when finding duplicates.|events=[{source:'A',id:'7'},{source:'B',id:'7'},{source:'A',id:'7'}]|distinct=2; duplicate={source:'A',id:'7'}|B/7 is not a duplicate of A/7.
2|Keep unknown price separate from zero|A two-source reconciliation must retain one unknown price and one explicit zero.|rows=[{id:'A',price:null},{id:'B',price:'0.00'}]|unknown=['A']; zero=['B']|Do not substitute zero for the unknown amount.
2|Record one source mapping|An operational source calls the key item_code; reporting calls it sku. Record the mapping and one row.|source={item_code:'S9',units:2}|reported={sku:'S9',units:2}|Keep source field lineage so a changed source name is diagnosable.
2|Calculate exact combined cents|Two feeds supply cents as integer strings. Produce a source-aware total.|POS=[{cents:'105'}]; web=[{cents:'95'}]|POS=105; web=95; combined=200|Do not parse cents as a fractional currency unit.
2|Reject a mislabelled page|An API page 2 response carries metadata page=1. Refuse publication of that page.|requested=2; response={page:1,events:[{id:'E2'}]}|published=0; error='page_mismatch'|An event row cannot make mismatched page metadata acceptable.
2|Compare a file checksum|A manifest records SHA-256 for source bytes; verify the exact bytes before parsing.|source_bytes='A\n'; manifest_sha256='06f961b802bc46ee168555f066d28f4f0e9afdf3f88174c1ee6f9de004fc30a0'|checksum_matches=true|Changing the line ending must make this checksum comparison fail.
3|Load a disposable accepted batch|Load two accepted delivery rows to an isolated relational table and verify by query.|rows=[{id:'D1',units:2},{id:'D2',units:0}]|stored_ids=['D1','D2']; stored_count=2|A second run must not create duplicate delivery IDs.
3|Keep rejected records queryable|One quantity is invalid, while one valid record must load. Save the original rejection with reason.|rows=[{id:'D1',units:2},{id:'D2',units:'bad'}]|stored=['D1']; rejected=[{id:'D2',reason:'units_invalid'}]|A warning log alone does not preserve the rejected source row.
3|Protect a database transaction|A two-row batch has an invalid second row. Demonstrate rollback of both new rows.|existing=['D0']; batch=[{id:'D1',units:2},{id:'D2',units:-1}]|final=['D0']; new_rows=0|The earlier D0 must survive the failed batch.
3|Keep customers without accepted deliveries|A report must show both customers even when one has no accepted delivery.|customers=['C1','C2']; deliveries=[{customer:'C1',units:2}]|C1=2; C2=0|A filtering join must not silently remove C2.
3|Reconcile a skipped source|A source manifest lists three files, one missing. Report readiness before any consolidated load.|expected=['A.csv','B.csv','C.csv']; present=['A.csv','C.csv']|ready=false; missing=['B.csv']; published=0|Partial input cannot be reported as a complete daily delivery.
3|Record source lineage in a row|Two accepted records from two files enter one table. Keep the source file for each.|A.csv=[{id:'D1'}]; B.csv=[{id:'D2'}]|D1.source='A.csv'; D2.source='B.csv'|The output file name is not the row's original source.
3|Test exact decimal sum|A daily summary must reconcile two exact monetary values after relational loading.|amounts=['0.10','0.20']|total='0.30'|A value of 0.30000000000000004 is not an accepted report amount.
3|Preserve a business correction|An amended delivery replaces its earlier value without duplicating the business event.|rows=[{id:'D1',version:1,units:2},{id:'D1',version:2,units:3}]|current_D1_units=3; current_event_count=1|Keep both source versions available for audit.
4|Choose an inspectable lake path|A business-day feed lands under store and date partition keys. Produce exact planned path.|store='S1'; day='2026-10-25'; file='D1.csv'|store=S1/day=2026-10-25/D1.csv|A run timestamp must not replace the declared business day.
4|Check a landing file before copy|A source metadata record says 10 bytes; landing has 9. Stop the downstream copy.|manifest_bytes=10; landed_bytes=9|copy_started=false; error='size_mismatch'|Do not label an incomplete object a successful empty file.
4|Keep source and sink counts|A copy activity sees two source rows but reports one sink row. Preserve both counts.|copy_run={source_rows:2,sink_rows:1,status:'Succeeded'}|reconciled=false; discrepancy=1|A green activity status cannot override the count mismatch.
4|Read a typed two-row frame|A transformation stage receives two delivery rows with typed units. Report the selected schema and count.|rows=[{id:'D1',units:2},{id:'D2',units:0}]|schema={id:string,units:integer}; count=2|Do not silently infer units as string from one malformed row.
4|Keep a null partner field|One partner has no region yet. Retain its record while projecting the shared fields.|rows=[{id:'D1',region:null},{id:'D2',region:'north'}]|rows=2; D1.region=null|Dropping records with unknown region changes accepted-row count.
4|Attach one run identifier|A copy run and a transformation run describe the same delivery. Record their IDs together.|copy_run='C17'; transform_run='T28'; delivery='D1'|lineage={delivery:'D1',copy:'C17',transform:'T28'}|One generic success flag cannot replace both run IDs.
4|Inspect a Delta table version|After an accepted append, record table version and exact current row count.|before_version=4; after_version=5; rows=['D1','D2']|version=5; row_count=2|A later version number alone does not verify row content.
4|Mark unavailable cloud execution|A learner lacks an authorized storage training account. Record the environment limit honestly.|training_account_available=false|execution='environment_blocked'; verified_cloud_rows=null|A local diagram cannot be called an executed Azure storage task.
5|Build one accepted source-to-report slice|Move two valid records through an authorized small lake, transform and reporting sink. Reconcile each boundary.|source_ids=['D1','D2']; amounts=[10,20]|landed=2; transformed=2; report_total=30|Do not count a source row as transformed before output inspection.
5|Join a product lookup in transformation|Two deliveries use a small product lookup. Retain every accepted delivery in a report.|deliveries=[{id:'D1',sku:'A'},{id:'D2',sku:'B'}]; products=[{sku:'A',category:'food'},{sku:'B',category:'home'}]|D1.category='food'; D2.category='home'; rows=2|A duplicated product key must be detected before a join multiplies rows.
5|Run a parameterized day twice|One orchestrated day is rerun after success. Report exactly one business result for the date.|day='2026-10-25'; input_ids=['D1','D2']; runs=['R1','R2']|business_rows=2; run_history=2|Preserve both operational runs without duplicating business rows.
5|Keep an empty day visible|A day has a valid header-only delivery. Publish an explicit zero-row result with successful processing history.|day='2026-10-25'; source_header='id,amount\n'; data_rows=[]|published_rows=0; completion_status='confirmed_empty'|Unknown missing input and confirmed empty are different states.
5|Compare file and table totals|A mini-pipeline writes an analytical table from two source files. Verify exact source/table sums.|file_A_amounts=[2,3]; file_B_amounts=[5]|source_total=10; table_total=10; difference=0|Success requires both count and amount reconciliation.
5|Write a tiny failure ledger|A pipeline accepts D1 and rejects D2. Persist one concise run outcome for later support.|D1={units:2}; D2={units:'bad'}|accepted=1; rejected=1; D2.reason='units_invalid'|Do not store credentials or raw personal data in the outcome record.
5|Use one justified compute boundary|A tiny feed can be handled locally; describe and measure the same output using a supported alternative.|rows=2; local_output=['D1','D2']; candidate_runtime='existing Spark training session'|both_outputs=['D1','D2']; measured_runtime_recorded=true|Do not claim Spark is faster without actual comparable measurements.
5|Publish a validated two-table result|Create customers and deliveries reporting tables; verify one customer with no delivery.|customers=['C1','C2']; deliveries=[{id:'D1',customer:'C1',units:2}]|customer_rows=2; delivery_rows=1; C2.units=0|Do not invent a delivery record for C2 to make totals easier.
6|Recover from a failed second file|File A loads, file B fails validation. Demonstrate rerun without duplicating A.|A=['D1']; B=[{id:'D2',units:'bad'}]; corrected_B=[{id:'D2',units:2}]|after_failure=['D1']; after_recovery=['D1','D2']|A successful A must remain while the bad B is repaired.
6|Do not advance a watermark on failure|A load for version 2 fails after version 1 is committed. Show the stored watermark and retry.|watermark=1; incoming_versions=[2]; first_run='sink_failure'|after_failure_watermark=1; after_retry_watermark=2|Advancing to 2 before durable write would lose the version.
6|Handle a partial copy report|A copy activity stops after one of two rows. Reconcile and prevent downstream publication.|source_ids=['D1','D2']; copied_ids=['D1']; status='Failed'|published=0; missing=['D2']|A subsequent retry must not duplicate D1 in the sink.
6|Quarantine a wrong data type|One feed record has units='two'. Keep valid rows and an explicit rejection with the original value.|rows=[{id:'D1',units:2},{id:'D2',units:'two'}]|accepted=['D1']; rejected=['D2']; raw_bad_value='two'|Do not coerce the word two to an inferred number.
6|Restore a prior good table version|An incorrect test write appears after a good Delta version. Demonstrate isolated recovery and verify count.|good_version=7; good_ids=['D1','D2']; bad_version=8; bad_ids=['D1']|restored_ids=['D1','D2']; verified_count=2|Preserve original history; do not simply report that version 7 exists.
6|Retry an expired source token safely|An API page request fails authentication before returning rows. Retry only after a new permitted token is supplied.|page=2; first_status=401; second_status=200; second_ids=['E3']|accepted_after_first=0; accepted_after_retry=['E3']|Never place either token in the saved run evidence.
6|Distinguish missing from empty after outage|A directory exists but one expected file is absent. Report missing input rather than an empty business day.|expected='south.csv'; listed=['north.csv']; manifest_count=0|delivery_status='missing_source'; published=false|A manifest count of zero does not prove the missing file was delivered.
6|Replay a corrected version once|A failed row is corrected in a second file delivery. Preserve the source history and one current business row.|first={id:'D2',units:'bad',version:1}; second={id:'D2',units:2,version:2}|source_versions=2; current_rows=1; current_units=2|Do not overwrite the first rejection evidence.
7|Keep late data in its business day|A delivery arrives after midnight UTC but belongs to the previous IST store day.|event_utc='2026-10-25T18:20:00Z'; reporting_zone='Asia/Kolkata'|business_day='2026-10-25'|Processing date on October 26 does not change the event day.
7|Resolve two source schemas explicitly|One source names units quantity; another names it pieces. Produce one typed common result.|A={id:'D1',quantity:2}; B={id:'D2',pieces:3}|rows=[{id:'D1',units:2},{id:'D2',units:3}]|Keep the source field mapping in lineage for later debugging.
7|Detect a multi-file key collision|Two distinct files repeat the same source-local ID but describe one partner. Quarantine the collision for review.|A={partner:'P1',id:'7',units:2}; B={partner:'P1',id:'7',units:5}|accepted_business_keys=0; conflict_key='P1/7'|Choosing the last file arbitrarily is not an agreed conflict rule.
7|Keep two partner namespaces distinct|Two different partners each use shipment ID 7. Merge without losing either.|A={partner:'P1',id:'7'}; B={partner:'P2',id:'7'}|business_rows=2; keys=['P1/7','P2/7']|Bare shipment ID is insufficient as a global business key.
7|Make a schema update compatible for a day|A new optional region field appears while one older source still lacks it. Show both outputs.|old={id:'D1',units:2}; new={id:'D2',units:3,region:'north'}|D1.region=null; D2.region='north'; rows=2|A missing required id would still fail; optional does not mean all fields optional.
7|Protect a consumer during a backfill|A corrected day is being rebuilt while readers expect last good data. Define and verify publication behavior.|published_day={day:'2026-10-24',rows:2}; rebuilding_day={day:'2026-10-25',rows:1,status:'unfinished'}|reader_sees_2026-10-24=2; reader_sees_2026-10-25=0|No reader may see an unfinished partially rebuilt day.
7|Reconcile foreign-key coverage|One sale refers to a missing product; separate valid sales from unresolved references.|sales=[{id:'S1',sku:'A'},{id:'S2',sku:'Z'}]; products=['A']|valid=['S1']; unresolved=['S2']; orphan_count=1|A failed lookup is not evidence that product Z has zero price.
7|Preserve a cancelled delivery event|A source sends an accepted and later cancellation version. Represent history and current outcome.|versions=[{id:'D1',status:'accepted',version:1},{id:'D1',status:'cancelled',version:2}]|history=2; current_status='cancelled'; active_deliveries=0|Deleting the earlier event would hide what was cancelled.
8|Measure a skewed join before tuning|One product has many sales while others have one. Measure the join and explain one tested change.|sales_per_sku={A:10000,B:1,C:1}; products={A:'food',B:'home',C:'home'}|joined_rows=10002; A_share_above_99_percent=true; measured_plan=true|No optimization is accepted without equal output counts before and after.
8|Bound a file-reader memory experiment|A large synthetic source exceeds a small memory budget with whole-file reading. Compare a bounded reader.|generated_rows=100000; memory_budget_mb=64|same_accepted_count=true; peak_memory_within_64mb=true|Report actual measured peak; do not infer it from code style alone.
8|Quantify rerun work instead of claiming speed|Compare a full reload with a changed-ID rerun on the same synthetic fixture.|baseline_rows=10000; changed_ids=['D9','D10']; methods=['full','incremental']|business_rows=10000_both; changed_ids_applied=2; timings_recorded=true|A faster run with missing rows is not an improvement.
8|Check a partition-pruning claim|A day filter should inspect the expected day partition, not every historical file.|days=['2026-10-01','2026-10-02','2026-10-03']; query_day='2026-10-02'|returned_day='2026-10-02'; partition_scan_evidence_recorded=true|Correct output alone does not prove pruning occurred.
8|Test a storage layout change by measured input|Compare two file layouts for the same 1,000 synthetic rows before choosing one.|layout_A=100_tiny_files; layout_B=4_files; records=1000|reconciled_rows_A=1000; reconciled_rows_B=1000; run_times_recorded=true|Do not merge source history destructively to improve a benchmark.
8|Report precision during aggregate scale|A million generated ten-cent amounts should reconcile exactly in minor units.|rows=1000000; cents_per_row=10|total_cents=10000000|A floating total rounded at display time is not proof of exact intermediate values.
8|Limit a skewed backfill's resource use|A backfill day has most rows; measure one bounded partition plan against a stated limit.|days={quiet:1000,busy:100000}; max_task_rows=25000|busy_processed_in_bounded_tasks=true; final_rows=101000|No task may exceed the stated row limit in the demonstrated plan.
9|Keep a publish marker tied to reconciliation|A run should publish success only after all source, sink and rejected counts reconcile.|source=3; accepted=2; rejected=1; sink=2|success_marker=true; source_equals_accepted_plus_rejected=true|Changing sink count to 1 must withhold the marker.
9|Correlate a failed delivery across services|A copy and transformation run share delivery D7. Produce one redacted investigation trace.|delivery='D7'; copy_run='C7'; transform_run='T7'; transform_status='Failed'|trace_ids=['D7','C7','T7']; root_stage='transform'|Do not expose tokens or customer personal data in the trace.
9|Enforce a least-privilege read boundary|A training identity may read one landing path but not an archive path. Verify both outcomes.|identity='reader1'; allowed='landing/D7.csv'; denied='archive/D7.csv'|allowed_read=true; denied_read=false|Do not broaden archive access merely to make a test pass.
9|Demonstrate an isolated restore|A saved analytical version is restored to a separate training target and reconciled.|backup_ids=['D1','D2']; live_ids=['D1','D2','D3']; restore_target='scratch_restore'|restored_ids=['D1','D2']; live_ids_after=['D1','D2','D3']|Never overwrite the live source while testing the backup.
9|Set a useful reconciliation alert|An alert must fire for a real count mismatch and stay quiet on a complete run.|runs=[{source:3,accepted:2,rejected:1,sink:2},{source:3,accepted:2,rejected:1,sink:1}]|alert_for_run2=true; alert_for_run1=false|A success status alone must not suppress a count discrepancy.
9|Require an explicit cost ceiling|A cloud training run records a budget before starting and refuses a candidate plan over it.|budget_units=10; proposed_plan_cost=12|start_allowed=false; reason='budget_exceeded'|No paid resource may be provisioned merely to verify this planning outcome.
9|Rehearse a small rollback decision|A new transformation returns one fewer accepted row than prior version. State the gate and demonstrate safe rollback.|previous_ids=['D1','D2']; candidate_ids=['D1']; expected_ids=['D1','D2']|candidate_published=false; reader_ids=['D1','D2']|Keep the candidate run evidence rather than erasing the failed comparison.
10|Independently handle three source contracts|Build an unfamiliar bounded pipeline merging file, API and database extracts into one typed result with rejection evidence.|file=[{id:'F1',units:2}]; api=[{id:'A1',units:3}]; db=[{id:'B1',units:'bad'}]|accepted=['F1','A1']; rejected=['B1']; accepted_units=5|Keep all three source identities and no code or answer is provided in advance.
10|Independently diagnose a lost partition|An unfamiliar published result is short by one delivery day. Reconstruct the minimum evidence and verify a correction.|manifest_days=['24','25']; published_days=['24']; source_rows={24:2,25:1}|missing_day='25'; corrected_rows=3|A manually inserted summary count is not a verified partition recovery.
10|Independently protect a changed key contract|A partner changes from bare ID to source-scoped ID. Demonstrate compatibility and replay with historical rows.|old=['7']; new=[{source:'A',id:'7'},{source:'B',id:'7'}]|current_source_keys=['A/7','B/7']; historical_unmapped=['7']|Do not silently assign the old row to partner A.
10|Independently prove recoverability after failure|A controlled failure occurs after a source read and before table commit. Rebuild the smallest correct slice and show rerun safety.|source_ids=['D1','D2']; failed_after_read=true; previous_table=['D0']|after_failure=['D0']; after_retry=['D0','D1','D2']|Preserve the failed run and show actual table evidence before and after.
10|Independently defend an architecture choice|Two proven approaches meet the same small contract. Compare correctness, measured cost and operational recovery, then choose one.|approach_A={correct:true,seconds:4,recovery:tested}; approach_B={correct:true,seconds:2,recovery:untested}|selected='A_or_B_with_explicit_tradeoff'; missing_evidence_B='recovery'|Do not claim B is production-ready solely because a small test was faster.
10|Independently investigate a duplicate daily total|A new report doubles one source total. Locate the multiplication using the supplied row keys and verify the repaired result.|orders=[{id:'O1',amount:10}]; lines=[{order:'O1',line:1},{order:'O1',line:2}]|wrong_total=20; corrected_total=10; cause_explained_with_evidence=true|Do not hide the issue with DISTINCT over a genuinely duplicated order key.
10|Independently recover a mixed-version day|A day has old and corrected product category assignments. Produce an as-of result and current result with audit history.|category_versions=[{sku:'A',category:'food',valid_from:'2026-10-01'},{sku:'A',category:'grocery',valid_from:'2026-10-20'}]; sale={sku:'A',day:'2026-10-10'}|sale_as_of='food'; current_category='grocery'; history_rows=2|A current-only overwrite would make the dated sale report wrong.
''')

DOCS = [
    'https://www.postgresql.org/docs/current/tutorial.html',
    'https://spark.apache.org/docs/latest/api/python/getting_started/quickstart_df.html',
    'https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-overview',
    'https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction',
]

def make():
    result=[]
    previous=None
    previous_level=0
    for number,(level,title,task,fixture,expected,boundary) in enumerate(ROWS,1):
        if not 0 <= level <= 10 or level < previous_level or level > previous_level+1:
            raise ValueError('Non-gradual level progression: '+title)
        ident=f'RLP-JOBBR-{number:03d}'
        dependencies=[previous] if previous else []
        if level >= 4:
            dependencies += ['RLP-PY-011','RLP-SQL-008','RLP-PG-004']
        if level >= 6:
            dependencies += ['RLP-PYSPARK-001','RLP-DELTA-LAKE-001']
        if level >= 9:
            dependencies += ['RLP-ADF-001','RLP-ADLS-001','RLP-DATABRICKS-001']
        dependencies=list(dict.fromkeys(dependencies))
        result.append({
            'id':ident,'tool_id':'integrated-pipelines','title':title,'level':level,
            'difficulty':f'level_{level}','learning_objective':task,
            'scenario':'An Indian distributor is making its daily delivery data reliable for store operations and reporting. '+task,
            'task':task,'inputs':{'fixture_contract':fixture},'expected_output':{'contract':expected},
            'constraints':[boundary,'Use synthetic records and an owned isolated target; keep credentials out of evidence.'],
            'acceptance_criteria':['Observed result matches: '+expected,'Demonstrate the boundary: '+boundary,
                'Submit actual implementation or configuration, observed output, assistance and one changed-input check.'],
            'prerequisites':dependencies,'independent_prerequisites':[],
            'skill_prerequisites':[] if level==0 else [f'integrated pipeline level {level-1}'],
            'progressive_hints':['Trace the smallest source event and write the required output before choosing an implementation.',
                'Locate the exact boundary in the task: '+boundary,
                'Compare the observed result with '+expected+' and preserve any failed attempt before correcting it.'],
            'engineering_relevance':title+' is one bounded source-to-reporting responsibility. After verification, explain its upstream/downstream effect and what this small demonstration leaves unproven.',
            'estimated_minutes':[8,12,15,20,25,35,40,50,70,90,120][level],
            'official_docs':DOCS,'verification':{'kind':'artifact_review'},
            'challenge_kind':'bridge' if level>previous_level else 'initial' if number==1 else 'transfer',
            'published_version':'2026.10.26.3','authoring_batch':'integrated-bridges-explicit-001',
            'sequence':level*1000+number,
        })
        previous,previous_level=ident,level
    return result

def main():
    authored=make()
    if OUT.exists():
        old=json.loads(OUT.read_text(encoding='utf-8'))
        by_id={p['id']:p for p in authored}
        for prior in old:
            if prior['id'] not in by_id or prior['title']!=by_id[prior['id']]['title']:
                raise ValueError('Refusing ID reassignment or deletion: '+prior['id'])
    if len({p['id'] for p in authored}) != len(authored):
        raise ValueError('Duplicate JOBBR ID')
    OUT.write_text(json.dumps(authored,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    content=OUT.read_bytes()
    CHECKPOINT.write_text(json.dumps({'status':'authored_unregistered','published_additions':0,
        'prepared_distinct_contracts':len(authored),'source_sha256':hashlib.sha256(content).hexdigest(),
        'next_id':f'RLP-JOBBR-{len(authored)+1:03d}',
        'note':'Authoring is not learner verification. Register only after shared bank validation.'},indent=2)+'\n',encoding='utf-8')
    print('Prepared',len(authored),'distinct integrated contracts; unregistered.')

if __name__=='__main__':
    main()
