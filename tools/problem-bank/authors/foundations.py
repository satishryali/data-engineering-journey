"""Resumable explicit-authoring batch. This does not invent missing target problems.

Each row is an authored input/output contract, not a domain-name substitution.
Rerunning preserves IDs deterministically and writes only this author's files.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BANK = ROOT / 'tools' / 'problem-bank'
VERSION = '2026.10.26.2'
ROWS = {}

def add(tool, level, title, task, inputs, output, edge):
    ROWS.setdefault(tool, []).append((level, title, task, inputs, output, edge))

def author(tool, text):
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        level, title, task, inputs, output, edge = line.split('|')
        add(tool, int(level), title, task, inputs, output, edge)

# The two miniature deliveries in each contract are synthetic fixtures. Outputs
# are expected, not claims that the learner has executed or mastered anything.
author('python', r'''
0|Read a parcel label|A warehouse operator needs the parcel ID from one supplied record. Return only parcel_id; do not print the complete record.|record={parcel_id:P7,weight_kg:2}|P7|Changing weight must not change the returned ID.
0|Tell an empty delivery from one record|An ingestion desk needs a simple arrival indicator. Return the number of records in the supplied list.|records=[{id:A}]|1; records=[] gives 0|An empty list is a valid arrival with zero records.
0|Copy an external reference exactly|A supplier reconciliation needs the original reference text. Return reference without numeric conversion.|reference='00041'|'00041'|Leading zeros must survive.
0|Produce one audit line|An operator wants a readable arrival line. Produce the exact text shown using file and row count.|file=orders.csv; rows=3|'orders.csv: 3 rows'|For zero rows produce 'orders.csv: 0 rows'.
0|Inspect one expected header|Before reading a delivery, tell the operator whether its first column is order_id. Return a boolean.|headers=['order_id','amount']|true|An empty header list returns false without an exception.
1|Remove transport whitespace|Supplier account codes have accidental spaces around them. Return a cleaned code, preserving internal spaces and case.|code='  AC 17  '|'AC 17'|A string of only spaces becomes an empty string.
1|Convert a whole-unit quantity|A warehouse export stores quantity as text. Return an integer for a valid whole-number input.|quantity='12'|12|Zero is valid; do not silently accept '2.5'.
1|Calculate a line value|A buyer wants the value in cents of one shipment line. Return units multiplied by unit_cents.|units=3; unit_cents=125|375|Zero units produce zero cents.
1|Choose the shipment status|Mark a parcel oversized when weight_kg is strictly greater than 20. Otherwise mark standard.|weights=[20,20.1,0]|['standard','oversized','standard']|Exactly 20 belongs to standard.
1|Keep records in arrival order|An audit asks for invoice IDs from a list of records. Return the IDs in their original order.|records=[{id:I2},{id:I1}]|['I2','I1']|Do not sort or remove repeated IDs.
1|Sum returned units|A returns desk needs the total returned units across records. Return one integer.|records=[{units:2},{units:3}]|5|Empty input produces zero.
1|Keep in-stock items|A pick list must contain SKU codes whose available units are greater than zero.|records=[{sku:A,available:0},{sku:B,available:4}]|['B']|Negative inventory is excluded, not changed to positive.
1|Find a missing required value|Mark an order invalid if customer is missing or an empty string. Return valid or missing_customer.|records=[{id:1,customer:''},{id:2,customer:C1},{id:3}]|['missing_customer','valid','missing_customer']|A missing key must not crash the batch.
1|Preserve null measurements|A sensor null means not measured. Return all non-null values including legitimate zero readings.|readings=[0,null,4]|[0,4]|Do not treat zero as missing.
1|Count a delivery category|Count only records whose channel is web; channel matching is case-sensitive.|records=[{channel:web},{channel:store},{channel:web}]|2|WEB is not web under this contract.
2|Keep rejection reasons next to rows|For stock adjustments, reject zero deltas and keep nonzero deltas. Return valid IDs plus rejected ID/reason pairs.|rows=[{id:A,delta:2},{id:B,delta:0}]|valid=['A']; rejected=[{id:B,reason:zero_delta}]|Preserve input order within each output.
2|Recognize repeated identifiers|A courier feed may resend the same parcel. Return IDs occurring more than once, once each in first-duplicate order.|ids=['A','B','A','C','B']|['A','B']|Three copies still produce one duplicate ID.
2|Resolve a lookup miss|Attach region from the supplied customer mapping; use UNKNOWN for an unmapped customer.|rows=[{id:1,customer:C1},{id:2,customer:C9}]; regions={C1:west}|[{id:1,region:west},{id:2,region:UNKNOWN}]|Do not drop unmatched records.
2|Split source file names|A landing report needs names ending exactly in .csv. Return accepted and ignored file names.|names=['a.csv','b.txt','c.csv.tmp']|accepted=['a.csv']; ignored=['b.txt','c.csv.tmp']|A partial suffix is not a match.
2|Compare control totals|Finance supplies expected_count and expected_cents. Return pass only if both match observed rows.|rows=[{cents:10},{cents:15}]; expected_count=2; expected_cents=25|pass|Correct total with wrong count must fail.
2|Normalize a country code safely|Trim country text and convert it to uppercase; null becomes null. Preserve the original beside the normalized value.|countries=[' in ',null,'Us']|[{raw:' in ',clean:IN},{raw:null,clean:null},{raw:Us,clean:US}]|Blank text is empty, not null.
2|Find new order IDs|Compare arrival IDs with already-loaded IDs. Return unseen arrivals in arrival order.|arrival=['B','C','A']; loaded=['A','B']|['C']|An empty loaded collection makes all arrivals new.
2|Calculate per-store units|The replenishment desk needs units summed by store. Return store totals without retaining unrelated fields.|rows=[{store:S1,units:2},{store:S2,units:1},{store:S1,units:3}]|{S1:5,S2:1}|The same store can occur in separated records.
2|Apply bounded discounts|Apply a discount in cents without allowing a negative payable value.|price_cents=120; discount_cents=150|0|A negative discount is rejected instead of increasing price silently.
2|Separate absent and blank fields|For three customer records, label email as absent, blank, or provided. Preserve IDs.|rows=[{id:A},{id:B,email:''},{id:C,email:x@example.test}]|[{id:A,state:absent},{id:B,state:blank},{id:C,state:provided}]|Null is a fourth state named null.
3|Read quoted supplier names|A CSV company field can contain a comma inside quotes. Read rows and return company names unchanged.|CSV text: id,company\n1,"North, Ltd"\n2,South|['North, Ltd','South']|A quoted newline remains part of the same field.
3|Check header membership before records|Require order_id and cents headers, tolerate extra columns, and report missing header names alphabetically.|headers=['order_id','comment']|missing=['cents']; no row processing|An empty file reports both required headers missing.
3|Export fixed column order|Write a CSV report with columns id,cents regardless of source key order; exclude internal_note.|rows=[{cents:12,internal_note:x,id:A}]|CSV text: id,cents\nA,12|Values containing commas must round-trip correctly.
3|Keep original line numbers|A validation report must name the physical source row. Reject noninteger units, counting the header as line1.|CSV text: id,units\nA,2\nB,bad|rejected=[{line:3,id:B,reason:invalid_units}]|Do not renumber only the rejected rows.
3|Parse a vendor date contract|Accept dates written YYYY-MM-DD only; reject invalid calendar dates. Return ISO dates and rejected input strings.|dates=['2026-02-28','2026-02-30','28/02/2026']|accepted=['2026-02-28']; rejected=['2026-02-30','28/02/2026']|Leap-day validity depends on the year.
3|Reconcile delivered and invoiced parcels|Find parcel IDs delivered but not invoiced, and invoiced but not delivered.|delivered=['P1','P2']; invoiced=['P2','P3']|uninvoiced=['P1']; unmatched_invoice=['P3']|A repeated delivered event must not duplicate the discrepancy.
3|Validate monetary precision|Accept nonnegative money text with at most two decimal places and return integer cents without binary rounding.|amounts=['1.20','0','2.345','-1']|accepted_cents=[120,0]; rejected=['2.345','-1']|Do not round forbidden precision into validity.
3|Separate refund direction|Sales and refunds arrive with nonnegative cents. Convert refunds to negative signed values and reject unknown types.|rows=[{type:sale,cents:100},{type:refund,cents:30},{type:other,cents:2}]|signed=[100,-30]; rejected_types=['other']|A negative source amount is rejected before applying direction.
3|Produce a validation summary|Deliver counts of accepted and rejected rows plus rejection counts by reason.|outcomes=['accepted','missing_id','invalid_units','missing_id']|{accepted:1,rejected:3,reasons:{missing_id:2,invalid_units:1}}|Summary counts must reconcile to input count.
3|Make a predictable report name|Name the output from an explicit business date and store, without using the machine clock.|date=2026-10-25; store=S3|'sales_S3_2026-10-25.csv'|Reject a store containing directory separators.
4|Read several daily files deterministically|Combine CSV delivery rows in filename order, then row order. Return each row with source_file.|files={b.csv:[{id:B}],a.csv:[{id:A}]}|[{id:A,source_file:a.csv},{id:B,source_file:b.csv}]|Directory enumeration order must not affect output.
4|Detect overlapping file deliveries|Two filenames may contain the same delivery_id. Report collisions before combining any row.|files={a.csv:{delivery:D1},copy.csv:{delivery:D1},b.csv:{delivery:D2}}|collisions={D1:['a.csv','copy.csv']}; processing_blocked=true|Identical content still counts as an ambiguous duplicate delivery.
4|Reconcile different source identifiers|Use an explicit supplier-to-internal SKU mapping. Return mapped stock and unmapped supplier SKUs separately.|rows=[{sku:V1,units:2},{sku:V9,units:1}]; mapping={V1:A}|mapped=[{sku:A,units:2}]; unmapped=['V9']|Two supplier codes may legitimately map to one internal SKU.
4|Read a nested API response|Extract order IDs from response.data.orders without treating metadata as records.|response={data:{orders:[{id:A},{id:B}]},meta:{count:2}}|['A','B']|An absent orders property is a contract error, not an empty delivery.
4|Follow a finite page chain|Read supplied page responses until next_cursor is null. Keep records in page order.|pages={start:{ids:[A],next_cursor:c2},c2:{ids:[B,C],next_cursor:null}}|['A','B','C']; requested=['start','c2']|A repeated cursor must stop with cycle_detected.
4|Respect an API retry delay|A local fake API returns 429 with Retry-After=2 then 200. Record a two-second planned delay and return the second response rows.|responses=[{status:429,retry_after:2},{status:200,rows:[A]}]|rows=['A']; planned_delays=[2]|Use an injected fake clock; do not actually wait during tests.
4|Join daily feeds at the right grain|Combine an order header with its line rows and retain orders with no lines in a separate report.|headers=[{order:O1},{order:O2}]; lines=[{order:O1,sku:A},{order:O1,sku:B}]|joined=[{order:O1,sku:A},{order:O1,sku:B}]; empty_orders=['O2']|Do not multiply lines by duplicate headers; report those first.
4|Compare a source schema with a baseline|Report added and missing fields separately from type changes. Row ordering is irrelevant.|baseline={id:string,cents:integer}; incoming={id:string,cents:string,currency:string}|added=['currency']; missing=[]; type_changes=['cents']|Do not infer integer types from a single numeric-looking string.
4|Read a compressed delivery|Read supplied gzip bytes containing CSV records and return row IDs. Also report corrupt compression separately.|fixture construction: gzip-compress UTF-8 text 'id\nA\nB\n'|ids=['A','B']; status=ok|Truncated gzip input returns corrupt_input and publishes no output.
4|Keep a source hash ledger|Compute SHA-256 for supplied file bytes and associate it with the original filename. Equal bytes must have equal hashes.|files={a.csv:UTF8('abc'),b.csv:UTF8('abc')}|two ledger rows; equal digests; digest length64|Filenames must not influence the content digest.
5|Create a bounded ingestion command|Build a command accepting input/output paths. Validate all rows before writing the accepted report and rejection report.|input CSV: id,units\nA,2\nB,bad; output directory is temporary|accepted.csv contains A,2; rejected.csv contains B with invalid_units; exit0|Invalid command arguments exit nonzero without creating output files.
5|Load through a supplied database adapter|Parse a checked batch and call an injected adapter once with accepted rows. Return submitted count.|CSV: id,cents\nA,25\nB,30; adapter records calls|one adapter call with [{id:A,cents:25},{id:B,cents:30}]; count2|An empty valid batch does not call the adapter.
5|Record a successful batch manifest|Write a manifest containing batch ID, input digest, accepted count, rejected count and output filenames.|batch=B1; accepted=2; rejected=1; input digest supplied as abc123|manifest matches B1/abc123/2/1 and names both outputs|Do not include machine-specific absolute paths in the manifest.
5|Avoid reprocessing an unchanged delivery|Use the supplied completed-digest ledger to skip an already-successful file even if renamed.|incoming={file:renamed.csv,digest:H1}; completed_digests=['H1']|status=skipped; adapter_calls=0|A failed prior run with H1 does not qualify for skipping.
5|Process only changed source records|Compare incoming updated_at values with stored values per record ID. Emit new and later records only.|incoming=[{id:A,version:2},{id:B,version:1},{id:C,version:1}]; stored={A:1,B:1}|emitted IDs=['A','C']|An older version must not overwrite the newer stored version.
5|Preserve deletion events|Build an incremental output preserving delete operations rather than losing them as missing records.|events=[{id:A,op:update,cents:20},{id:B,op:delete}]|upserts=[{id:A,cents:20}]; deletes=['B']|A delete does not require cents.
5|Parameterize a database write|Pass values separately from the SQL statement through a fake DB-API cursor, preserving a quote in a customer name.|row={id:A,name:"O'Neil"}; cursor records statement and parameters|name stored exactly; statement does not contain the name; params do|Do not execute against any real shared database.
5|Connect validation to quality gates|Block publication if more than 10 percent of rows are rejected; retain the rejection report either way.|input_count=20; rejected_count=3|publication=blocked; rejection_report=retained|Exactly 10 percent is allowed under this contract.
5|Expose a reusable transformation|Separate a pure row transformation from file orchestration. Demonstrate the transformation without filesystem access.|row={quantity:'2',unit_cents:'15'}|transformed={quantity:2,unit_cents:15,line_cents:30}|Transforming a row must not modify the original object.
5|Run a three-step local pipeline|Connect read, validate and export stages with a shared run ID and counts returned from each stage.|input rows=[{id:A,units:1},{id:B,units:0}]; reject nonpositive units|read=2; accepted=1; rejected=1; output IDs=['A']; same run_id across logs|Do not report exported count before the write succeeds.
6|Recover from an interrupted output write|Write through a temporary sibling file and publish only after successful completion. Inject failure after one row.|old final output contains OLD; new rows=[A,B]; fail_after=1|final remains OLD; run failed; temporary file not treated as complete|Retry without failure produces A,B exactly once.
6|Rollback a partially loaded batch|With a fake transactional adapter, fail the second insert and demonstrate rollback of the whole batch.|initial IDs=['OLD']; new IDs=['A','B']; second insert fails|final IDs=['OLD']; rollback_count=1; commit_count=0|A subsequent retry commits A and B once each.
6|Bound retry attempts|Retry only transient adapter failures up to three total attempts. Return final outcome and observed attempt count.|responses=['transient','transient','success']|status=success; attempts=3|A permanent validation failure is attempted once.
6|Avoid advancing a failed watermark|Process records newer than cursor10, but update the durable cursor only after output commit.|cursor=10; events=[{seq:11},{seq:12}]; output commit fails|cursor remains10; run=failed|Successful retry advances cursor12.
6|Quarantine a broken file without losing good files|Process files independently; malformed headers quarantine the offending file and allow other valid files to finish.|a.csv headers=id,units; b.csv headers=wrong; c.csv headers=id,units|a and c complete; b quarantined; overall status=partial|Do not count b as a successful empty file.
6|Resume a paginated extraction|Persist the next cursor after each committed page. Fail during page2 and restart with the supplied state.|page1=A next=c2 committed; page2=B interrupted before commit|restart requests c2; final IDs=['A','B']; A not reloaded|Do not persist cursor after an uncommitted page.
6|Distinguish corrupt data from unavailable source|Classify a timeout as retriable and malformed CSV as quarantine, recording separate outcomes.|events=[{file:a,error:timeout},{file:b,error:invalid_csv}]|a=retriable; b=quarantine|Do not retry malformed CSV forever.
6|Record a truthful failed run|A pipeline reads12 rows and fails before export. Write a failed run record with observed counts and an error category.|run=R4; read=12; accepted=10; export raises IOError|status=failed; read12; accepted10; exported0; error=output_io|Do not fill unknown timing or count fields with invented values.
6|Detect an abandoned batch lease|Use an injected clock to prevent two workers owning one batch; an expired lease can be taken over.|batch=B1; owner=w1; expiry=100; now=101; requester=w2|owner=w2; acquisition=granted|At now99 a second owner is denied.
6|Reconcile target state after uncertain commit|Adapter reports a connection loss after commit might have happened. Query target by batch ID before retrying.|batch=B1; target batch ledger says committed count2|status=reconciled; inserts=0; target_count2|When ledger says absent, retry the original idempotent batch.
7|Handle an optional added field|Allow incoming currency while preserving the required id,cents contract. Default absent currency to INR and record schema version.|rows=[{id:A,cents:10},{id:B,cents:20,currency:USD}]|[{id:A,cents:10,currency:INR},{id:B,cents:20,currency:USD}]|A missing required cents field still fails validation.
7|Reprocess a late arrival window|Re-read two days before the saved watermark and reconcile by ID/version to capture late events.|watermark=2026-10-10; lookback_days=2; late event date=2026-10-09 id=A version2|extraction begins2026-10-08; A version2 applied once|A repeated scan must leave the same target state.
7|Resolve event-time ties deterministically|Choose the latest event by event_time and sequence within a parcel. Explain and test the tie rule.|events=[{id:P,time:10,seq:1,state:packed},{id:P,time:10,seq:2,state:sent}]|state(P)=sent|Equal time and sequence with conflicting state is quarantined.
7|Convert explicit time zones safely|Normalize two offset-aware timestamps representing the same instant to UTC. Reject naive timestamps.|timestamps=['2026-10-26T10:00:00+05:30','2026-10-26T04:30:00+00:00']|both become '2026-10-26T04:30:00+00:00'|No host-local timezone assumption is allowed.
7|Mask personal data in operational logs|Log a rejected customer's ID and reason while excluding raw email and token from every log line.|row={id:C1,email:person@example.test,token:secret}; reason=invalid_country|logs contain C1 and invalid_country; email/token absent|Error exception text must also be checked for leakage.
7|Validate a configuration override|Merge defaults with one environment override and validate batch_size as a positive integer before any I/O.|defaults={batch_size:100,mode:append}; override={batch_size:25}|effective={batch_size:25,mode:append}|Unknown configuration keys produce a helpful error.
7|Route multi-tenant records|Write each tenant's rows only beneath its own output directory; reject path traversal tenant codes.|rows=[{tenant:T1,id:A},{tenant:T2,id:B},{tenant:'../x',id:C}]|T1 output A; T2 output B; C rejected|Resolved output paths must remain inside the temporary output root.
7|Honor cancellation between batches|Stop starting new chunks after cancellation while preserving committed chunks and resumable position.|chunks=[[A],[B],[C]]; cancel after first commit|committed=['A']; next_chunk=1; status=cancelled|Cancellation must not mark the overall delivery complete.
7|Reconcile decimal and currency contracts|Keep currency totals separate and reject unsupported precision according to currency metadata.|rows=[{currency:JPY,amount:'12'},{currency:INR,amount:'1.25'},{currency:JPY,amount:'1.5'}]|totals={JPY:12,INR:1.25}; one JPY precision rejection|Never add amounts across currencies without an explicit conversion rate.
7|Compare code versions on the same delivery|Run old/new transformations against identical immutable input and report changed outputs by ID.|old A=10 B=20; new A=10 B=21; same input digest|differences=[{id:B,old:20,new:21}]|Do not overwrite the production output during comparison.
8|Stream a large CSV aggregation|Generate one million two-column rows and total cents without keeping all records in memory.|generator produces ids1..1000000 with cents1|total_cents=1000000; measured peak memory below64MiB|Include an empty-input check and measurement method.
8|Avoid repeated reference scans|Attach region to100000 orders using a supplied10000-customer reference. Compare operation counts with a baseline.|customers C1..C10000; all orders reference C10000|all regions correct; reference inspected at most110000 times|Show count evidence rather than a hardware-specific timing promise.
8|Bound concurrent requests|Use a fake API with tracked active calls; retrieve20 independent pages while limiting simultaneous calls to3.|pages1..20; fake API tracks in_flight|20 results exactly once; max_in_flight<=3|A page failure is visible and does not silently disappear.
8|Respect downstream backpressure|Connect a fast producer to a slow fake writer using a bounded buffer. Demonstrate cancellation on writer failure.|100 produced records; capacity5; writer fails at10|buffer never exceeds5; pipeline terminates; first10 commits recorded|No worker may remain blocked indefinitely after failure.
8|Choose a measured chunk size|Compare chunk sizes1,10,100 for1000 rows using an adapter with a per-call cost counter.|adapter cost=5 per call plus1 per row|costs=6000,1500,1050; identical target rows|Report the higher rollback work caused by larger chunks.
8|Aggregate beyond a memory limit|Create100000 groups from generated events under a32MiB budget using temporary storage if needed.|events yield each key twice with units1|100000 output groups each total2|Temporary resources are removed after success and failure.
8|Profile a serialization bottleneck|Instrument parse, transform and serialize stages separately, using an injected deterministic timer.|stage elapsed values parse2 transform1 serialize7 seconds|report identifies serialize as70percent of10 seconds|Do not claim optimizing transform removes the measured serialization cost.
8|Bound a lookup cache|Read a repeating customer stream using an at-most100-entry cache and report cache misses.|stream C1..C101 repeated twice; capacity100; LRU eviction contract|cache size<=100; evictions and misses reproducible|Verify values remain correct after eviction and re-fetch.
8|Merge sorted deliveries incrementally|Combine two sorted event iterators into one sorted output without materializing either entire source.|left=[1,4,7]; right=[2,4,6]|[1,2,4,4,6,7]|Keep equal keys from both sources; bounded buffering required.
8|Reduce redundant file reads|Build a count-and-digest report in one streaming pass per file and prove reads are not duplicated.|fake file yields3 chunks and records read calls|one pass; correct digest; row count matches baseline|Handle a final line without a newline.
9|Make deployment configuration reproducible|Provide a pinned dependency specification and a clean-environment smoke command using only synthetic fixtures.|clean temporary environment; one valid and one rejected row|documented command exports1 row and1 rejection with exit0|No credentials or local absolute paths in the package.
9|Expose operational health without false success|Return healthy only if the last successful commit is within15minutes and no run is currently failed.|now=12:30; last_success=12:00; latest_run=failed|health=unhealthy; reasons=[stale_success,latest_failure]|A fresh heartbeat alone must not imply successful data delivery.
9|Implement a dry-run contract|A dry run validates inputs and reports planned changes without mutating data, manifests or cursors.|target A=1; incoming A=2 B=1; dry_run=true|planned updates1 inserts1; target A=1; cursor unchanged|Logs must clearly distinguish planned counts from committed counts.
9|Provide a reproducible rollback drill|Deploy transformationv2 with a changed output contract, then restorev1 using a retained immutable input.|v1 A=10; v2 A=20; source digest fixed|rollback produces A=10; audit links both versions and source digest|Do not deletev2 evidence during rollback.
9|Define run-level service indicators|Calculate successful delivery ratio and95th percentile latency from a supplied run ledger; exclude cancelled runs from denominator.|runs success10s success20s failed30s cancelled5s; nearest-rank percentile|success_ratio=2/3; p95 completed_run_latency=30s|State whether failed runs are included in the latency population.
9|Restore from saved state|Delete a sandbox target after snapshotting target rows and cursor. Restore and prove replay is idempotent.|snapshot rows A,B cursor2; source includes A1 B2 C3|restored then replayed target A,B,C; cursor3|Snapshot and cursor must come from one consistent boundary.
9|Document and test a restart runbook|Give another operator commands to recover an injected mid-batch failure in an isolated fixture.|failure after committing batch1 before batch2|second operator reaches identical target as clean run; no duplicate IDs|Runbook must identify evidence used to decide the restart point.
9|Rotate credentials without exposing them|Use a fake secret provider returning versionv1 thenv2; reconnect after authentication failure usingv2.|fake connection rejectsv1 after rotation;v2 succeeds|one refresh; successful retry; no secret values in logs|Permanent authorization denial must not trigger unlimited rotation retries.
9|Gate a release on contract tests|Create a local release check comparing required output columns with a consumer contract before promoting artifacts.|consumer requires id,cents; candidate produces id,amount|release blocked; missing cents and unexpected amount reported|No candidate artifact may replace the last approved output.
9|Budget extraction requests|Stop a run before it exceeds a supplied request budget; persist the resume cursor and report partial completion.|budget3; five pages each with one record|three pages committed; next_cursor=page4; status=budget_paused|A budget pause is not an extraction failure or a complete delivery.
10|Build an independent parcel ingestion service|Independently implement a file-to-database parcel feed with validation, reruns and recovery, defending one design tradeoff.|three CSV deliveries: duplicate parcel event, malformed units, later correction; fake DB adapter|corrected state retained once; rejection traceable; restart equals clean run|Demonstrate failure after write before acknowledgment without revealing a worked solution.
10|Design a bounded CDC consumer|Implement create/update/delete processing with ordering, resumability and a changed-input test written before code.|events A:create1 A:update2 A:delete3 B:create4; replay2..4|target contains only B; cursor4; replay unchanged|Explain behavior for out-of-order deletes and demonstrate the chosen contract.
10|Recover a partitioned month-end feed|Build and defend a pipeline that repairs one missing daily partition without republishing the whole month.|30 dated partitions; day17 missing; day18 late correction; frozen close date|day17 repaired; day18 correction audited; unaffected partitions byte-identical|Provide an explicit policy for changes arriving after close.
10|Migrate a pipeline under live contract pressure|Support consumersv1 andv2 during a staged schema migration, then retirev1 after demonstrated compatibility checks.|v1 id,cents;v2 id,amount_minor,currency; two overlapping consumers|both consumers receive valid data during overlap; rollback demonstrated|Do not silently infer a currency absent from an authoritative contract.
10|Defend a memory-constrained backfill|Independently backfill a generated10million-record source under128MiB and a configurable request budget.|source with duplicates, late versions, one corrupt partition and intermittent timeouts|deterministic final state; explicit quarantines; resumable progress; measured memory evidence|Document a failed approach and why the selected alternative meets the contract.
''')
author('sql', r'''
0|Read one supplier code|A receiving clerk needs only the supplier_code column from a one-row delivery table. Return one column named supplier_code.|delivery(supplier_code,units):('V1',3)|supplier_code: V1|Do not return units or rename the supplier code value.
0|Keep a leading-zero account reference|An invoice lookup needs an account reference stored as text. Return it unchanged.|accounts(account_ref TEXT):('0007')|account_ref: '0007'|Do not cast the reference to a number.
0|Label one constant report field|A dashboard export requires a literal source_system column alongside each parcel_id.|parcels(parcel_id):('P1')|parcel_id=P1, source_system=carrier|The output column name must be source_system.
0|Recognize zero rows|An empty delivery table is a legitimate result. Query its id column and explain the observed row count.|deliveries(id): empty|zero result rows with id column|Do not invent a placeholder delivery row.
0|Select two named columns|A privacy-limited export needs customer_id and region, excluding email.|customers(customer_id,region,email):('C1','west','x@example.test')|customer_id=C1, region=west|Column order must follow the export contract.
1|Find positive stock|The pick desk needs SKU codes with strictly positive on_hand.|stock(sku,on_hand):('A',0),('B',4),('C',-2)|B|Zero and negative stock are both excluded.
1|Use an inclusive boundary|A courier wants parcels weighing at least20kg.|parcels(id,weight):('A',19),('B',20),('C',21)|B,C ordered by id|Exactly20 is included.
1|Combine two business conditions|Return paid web orders only.|orders(id,channel,status):(1,'web','paid'),(2,'store','paid'),(3,'web','new')|id1|A row satisfying only one condition must be excluded.
1|Handle a null arrival time|Operations needs shipment IDs whose arrived_at is unknown.|shipments(id,arrived_at):('A',NULL),('B','2026-10-26')|A|An empty string is not automatically SQL NULL.
1|Sort a deterministic queue|Return parcels by priority descending and id ascending within tied priority.|parcels(id,priority):('B',2),('A',2),('C',1)|A,B,C|Tied priorities require an explicit second ordering key.
1|Limit a dispatch preview|Show the first two parcels by scheduled_minute then id.|parcels(id,scheduled_minute):('C',2),('B',1),('A',1)|A,B|The same fixture must produce stable results across runs.
1|Calculate invoice line cents|Return id and units multiplied by unit_cents as line_cents.|lines(id,units,unit_cents):('L1',3,125),('L2',0,50)|L1:375; L2:0|Use integer cents and the requested column alias.
1|Filter a date interval|Select events on2026-10-25 using an inclusive lower and exclusive upper timestamp boundary.|events(id,ts):('A','2026-10-25 00:00'),('B','2026-10-26 00:00')|A|The next day's midnight must be excluded.
1|Match a prefix literally|Find warehouse codes starting with WH- while excluding codes that merely contain it later.|warehouses(code):('WH-N'),('XWH-N'),('WH-S')|WH-N,WH-S|Decide and state case-sensitivity for your dialect.
1|Classify a delayed shipment|Return late when delay_minutes>0, on_time when0, and unknown forNULL.|shipments(id,delay_minutes):('A',2),('B',0),('C',NULL)|A:late; B:on_time; C:unknown|Unknown must not fall through to on_time.
2|Distinguish row count from measured count|Report total records and number with a known temperature.|readings(id,temp):(1,0),(2,NULL),(3,5)|rows=3; measured=2|A zero measurement is counted as known.
2|Aggregate units by warehouse|Return units per warehouse sorted by code.|stock(warehouse,units):('W1',2),('W2',4),('W1',3)|W1:5; W2:4|Separated rows for one warehouse belong in one result.
2|Filter aggregated inventory|Return only warehouses with total available units greater than5.|stock(warehouse,units):('W1',3),('W1',3),('W2',5)|W1:6|A warehouse with total exactly5 is excluded.
2|Preserve all-null group meaning|Report sum and nonnull count for each sensor, leaving the sumNULL when all readings areNULL.|readings(sensor,value):('S1',NULL),('S1',NULL),('S2',0)|S1:sumNULL,count0; S2:sum0,count1|Do not replace unknown totals with zero in this contract.
2|Count distinct delivered parcels|A status feed repeats events. Count distinct parcel IDs per delivery date.|events(day,parcel):('2026-10-25','P1'),('2026-10-25','P1'),('2026-10-25','P2')|2026-10-25:2|Do not count each status event as a parcel.
2|Attach a product category|Join invoice lines to their one-row-per-SKU product reference.|lines(id,sku):('L1','A'),('L2','B'); products(sku,category):('A','food'),('B','tools')|L1:food; L2:tools|Verify the reference key is unique before trusting row counts.
2|Report unknown foreign keys|Find invoice lines whose SKU is absent from the product reference.|lines(id,sku):('L1','A'),('L2','X'); products(sku):('A')|L2:X|Do not lose the line identifier in the rejection result.
2|Keep unused warehouse locations|List every location and its item count including empty locations.|locations(id):('A'),('B'); items(id,location):('I1','A')|A:1; B:0|The placeholder from an outer join is not an item.
2|Apply fallback supplier names|Return display_name if known, otherwise supplier_code, preserving blank display names as blank.|suppliers(code,display_name):('A',NULL),('B','')|A:A; B:''|NULL and an empty string have different meanings.
2|Compare two batch memberships|Find parcel IDs appearing in the new batch but not the prior batch.|new_batch(id):('A'),('B'),('B'); old_batch(id):('A')|B once|State whether repeated incoming identifiers are distinct membership or event counts.
3|Reconcile order and payment grain|Report order value beside total paid without multiplying the order value by payment count.|orders(id,cents):('O1',100); payments(order_id,cents):('O1',40),('O1',60)|O1:order_cents100,paid_cents100|Add a second order with no payments and retain it with paid0.
3|Build a daily refund-adjusted report|Summarize signed cents by day, with refunds subtracting from sales.|events(day,kind,cents):('D1','sale',100),('D1','refund',30)|D1:70|Unknown kinds must be reported separately instead of treated as sales.
3|Find repeated business keys|Return customer source IDs occurring more than once with their row counts.|customers(source_id):('A'),('B'),('A')|A:2|A unique source ID must not appear.
3|Check a batch quality threshold|For each batch report rejected fraction and flag it when strictly above10percent.|batch_rows(batch,valid):('B1',true) repeated9; ('B1',false) once|B1:0.1,allowed|Use numeric division; exactly10percent is allowed.
3|Select the latest supplier price|Return the last effective price on or before the report date for each SKU.|prices(sku,day,cents):('A','2026-10-01',100),('A','2026-11-01',120); report_day2026-10-26|A:100|Future prices must not leak into the report.
3|Audit a many-to-many mapping|Detect source codes mapping to multiple active target codes before joining facts.|mapping(source,target,active):('X','A',true),('X','B',true),('Y','C',true)|ambiguous source X count2|An inactive historical mapping must not create active ambiguity.
3|Report missing daily partitions|Given an explicit expected_dates table, find dates with no successful delivery.|expected_dates(day):('D1'),('D2'),('D3'); deliveries(day,status):('D1','success'),('D2','failed')|D2,D3|A failed delivery does not satisfy completeness.
3|Compare subtotal to control total|For each batch report observed cents, declared cents and difference.|rows(batch,cents):('B1',20),('B1',30); controls(batch,cents):('B1',60)|B1:observed50,declared60,difference-10|Also report controls for a batch with zero observed rows.
3|Find customers returning after inactivity|Return customers with a purchase on report_day but none in the previous30calendar days.|purchases(customer,day):('A','2026-10-26'),('A','2026-09-01'),('B','2026-10-26'),('B','2026-10-20')|A|Today's purchase must not disqualify the customer.
3|Keep the first invoice occurrence|Deduplicate source invoices by earliest arrived_at and then ingestion_id.|invoices(id,arrived_at,ingestion_id):('I1',10,2),('I1',10,1),('I2',11,3)|I1 ingestion1; I2 ingestion3|The tie-breaking rule must be deterministic.
4|Union two source channels without erasing events|Combine web and store sale events, retaining a source label and duplicate values.|web(id,cents):('A',10); store(id,cents):('A',10)|two rows with sources web/store|Equal IDs in different source systems are not automatically duplicates.
4|Bridge timezone boundaries in a daily report|Group UTC timestamps by a fixed business timezone ofAsia/Kolkata.|events(id,ts_utc):('A','2026-10-25T20:00Z'),('B','2026-10-26T02:00Z')|business_day2026-10-26:count2|Do not group by the rawUTC date.
4|Count unmatched records on both sides|Reconcile source and target IDs, reporting source_only,target_only and matched.|source(id):('A'),('B'); target(id):('B'),('C')|source_only A; target_only C; matched B|Assert no ID appears in two discrepancy classes.
4|Resolve an effective-dated dimension|Attach the customer region valid at event time using closed-open validity intervals.|events(customer,day):('C1','2026-10-10'); regions(customer,start_day,end_day,region):('C1','2026-10-01','2026-10-10','west'),('C1','2026-10-10',NULL,'east')|C1 on2026-10-10:east|Exactly one active dimension row must match each event.
4|Pivot bounded warehouse statuses|Produce one row per warehouse with pending,shipped and failed counts.|events(warehouse,status):('W1','pending'),('W1','shipped'),('W1','shipped')|W1:pending1,shipped2,failed0|Unknown statuses are counted in a separate other column.
4|Unpivot a fixed daily metric export|Turn open_count and closed_count columns into metric_name/metric_value rows.|daily(day,open_count,closed_count):('D1',3,2)|D1,open,3; D1,closed,2|Do not discard a metric whose value is zero.
4|Apply ordered exception rules|Assign hold reason credit_hold before missing_address when both are true.|orders(id,credit_hold,address):('A',true,NULL),('B',false,NULL)|A:credit_hold; B:missing_address|Return one primary reason according to the written precedence.
4|Compare snapshots with null-safe changes|Identify customers whose region changed, includingNULL-to-value and value-toNULL.|old(id,region):('A',NULL),('B','west'); new(id,region):('A','east'),('B',NULL)|A,B|NULL-toNULL must not count as a change.
4|Reconcile different data types before joins|Match text customer codes to numeric source keys only where the text is a valid nonnegative integer.|text_keys(code):('001'),('bad'); numeric_keys(id):(1)|matched001->1; rejectedbad|Do not let invalid casts abort the complete reconciliation.
4|Check unit conversion at a boundary|Convert stock into base units using SKU-specific conversion factors before aggregating.|stock(sku,qty,unit):('A',2,'box'),('A',3,'each'); factors(sku,unit,factor):('A','box',10),('A','each',1)|A:23base_units|A missing conversion factor is an error, not factor1.
5|Calculate running warehouse balance|Return inventory balance after each movement ordered by movement_time then movement_id.|movements(id,time,delta):(1,10,5),(2,10,-2),(3,11,4)|balances3rows:5,3,7|Tied timestamps must not merge into one peer-group total.
5|Compare each event with its predecessor|Report state changes per parcel, excluding repeated identical statuses.|events(parcel,seq,state):('P',1,'packed'),('P',2,'packed'),('P',3,'sent')|seq1 andseq3|Retain the first observed state explicitly.
5|Find top products with ties|Return all products tied for the highest sales per category.|sales(category,sku,cents):('food','A',100),('food','B',100),('food','C',50)|food:A100,B100|Do not discard a tied winner with an arbitrary row limit.
5|Compute trailing three-day units|Using one row per day including zero days, calculate units over current plus two preceding calendar days.|daily(day,units):('D1',1),('D2',0),('D3',4),('D4',2)|D1:1,D2:1,D3:5,D4:6|Explain why three observed rows differ from three dates if dates are missing.
5|Calculate share of warehouse sales|Return each store's fraction of its region total and preserve zero-total regions withNULL share.|sales(region,store,cents):('R1','A',30),('R1','B',70),('R2','C',0)|R1A0.3; R1B0.7; R2CNULL|Do not divide by zero.
5|Build a reorder recommendation|Combine item stock, seven-day demand and supplier lead days to flag stock below demand-rate times lead time.|stock(sku,units):('A',5); demand(sku,seven_day_units):('A',14); supplier(sku,lead_days):('A',3)|A:daily_demand2,reorder_threshold6,reordertrue|A missing lead time is flagged unknown, not zero.
5|Prepare idempotent staging changes|Classify staged keys as insert,update,unchanged against a target snapshot.|stage(id,cents):('A',20),('B',10),('C',30); target(id,cents):('A',10),('B',10)|A:update,B:unchanged,C:insert|Reject duplicate staged keys before classification.
5|Identify watermark-eligible events|Extract sequence IDs greater than the last committed cursor and return a proposed next cursor separately.|events(seq):(10),(11),(12); committed_cursor10|extracted11,12; proposed_cursor12|An empty extract retains cursor10 rather thanNULL.
5|Compute a cohort retention matrix|For a two-month fixture, label customers by first purchase month and count those purchasing next month.|purchases(customer,month):('A','2026-01'),('A','2026-02'),('B','2026-01'),('C','2026-02')|Jan cohort size2 next_month_active1; Feb size1|Repeated purchases in one month count one active customer.
5|Build a report with explicit grain checks|Return one row per order combining header,aggregated lines and payments, with reconciliation flags.|order O1 header100; lines40,60; payments100; orderO2 header50 lines50 payments0|O1 totals100/100/100 balanced; O2 totals50/50/0 unpaid|Joining raw lines directly to raw payments must not multiply totals.
6|Detect overlapping dimension intervals|Find two validity intervals for the same customer that overlap.|regions(customer,start_day,end_day):('C1',1,5),('C1',4,8),('C2',1,4),('C2',4,9)|C1 intervalpair only|Adjacent closed-open intervals do not overlap.
6|Find missing sequence ranges|Identify gaps between committed source sequence numbers without treating duplicate numbers as extra gaps.|sequences(n):(1),(2),(2),(5),(7)|missing_ranges3..4 and6..6|Do not assume the first observed number must be1 unless specified.
6|Identify unbalanced ledger transfers|Each transfer must have signed postings summing to zero in each currency.|postings(transfer,currency,cents):('T1','INR',100),('T1','INR',-100),('T2','INR',50)|T2 INR imbalance50|Never net different currencies together.
6|Separate failed attempts from failed batches|A batch can fail then succeed. Report batches whose latest attempt is failed, using attempt number.|runs(batch,attempt,status):('B1',1,'failed'),('B1',2,'success'),('B2',1,'failed')|B2|A historical failure must not override a later success.
6|Find orphaned loaded rows|Report target rows referencing a batch with no committed batch-ledger entry.|target(id,batch):('A','B1'),('B','B2'); ledger(batch,status):('B1','committed'),('B2','started')|B|Started is not committed.
6|Repair a misordered incremental report|Use sequence as authoritative order even when arrival timestamps are out of order.|events(seq,arrived,state):(2,10,'sent'),(1,11,'packed')|latest_state=sent fromseq2|Report the arrival-order inversion as audit evidence.
6|Surface malformed metric denominators|Compute failure rate only when processed_count>0; distinguish no_data from zero failures.|runs(id,processed,failed):('A',0,0),('B',10,0),('C',10,2)|A:no_data,NULL; B:0; C:0.2|A zero-row run must not appear as100percent reliable.
6|Find duplicate natural keys with conflicting values|Differentiate identical repeated rows from conflicting duplicates using id and cents.|stage(id,cents):('A',10),('A',10),('B',10),('B',20)|A:identical_duplicate; B:conflict|Preserve counts so reviewers can see all repeated arrivals.
6|Isolate a faulty join multiplier|Diagnose why a report totals400 when the order header is100; provide corrected totals and multiplicity evidence.|one order100; two line rows; two payment rows|rawjoin4rows; corrected order_total100|Removing duplicates after summing is not a valid general repair.
6|Reconcile deletes in a snapshot feed|Find target IDs absent from a complete current snapshot, but block deletion for an incomplete snapshot.|target A,B; snapshot A; controls complete=true thenfalse|complete=true deletesB; complete=false deletesnone and blocked|Missing source rows alone do not prove a deletion when completeness is unknown.
7|Sessionize application activity|Start a new session when the gap exceeds30minutes, not when it equals30.|events(user,minute):('U1',0),('U1',30),('U1',61)|sessions:1,1,2|Partition sessions independently per user.
7|Track consecutive inventory outages|Group consecutive calendar dates with zero stock and report outage start,end,length.|daily(day,units):(1,0),(2,0),(3,4),(4,0)|outages1..2 length2 and4..4 length1|A missing date is reported as unknown, not silently considered zero.
7|Traverse a bounded bill of materials|Expand parts to depth2 and multiply component quantities along each path.|BOM(parent,child,qty):('A','B',2),('B','C',3)|A needs B2 andC6|Report cycles rather than recurse forever.
7|Detect circular dependency metadata|Return dependency cycles in a three-task pipeline graph.|edges(task,depends_on):('A','B'),('B','C'),('C','A'),('D','E')|cycle includesA,B,C; D,E not circular|Make traversal termination explicit.
7|Allocate cents without losing the remainder|Split100cents across three equal recipients, assigning remainder by recipient ID.|recipients(id):('A'),('B'),('C'); total100|A34,B33,C33|Allocated cents must sum exactly100.
7|Merge overlapping maintenance windows|Produce unioned intervals for one system and total downtime without double counting.|windows(start,end):(1,4),(3,6),(8,9)|merged1..6,8..9; duration6|Touching intervals can merge under a stated closed-open policy.
7|Reconstruct effective customer history|From ordered change events, return start and end boundaries for each distinct region state.|events(customer,seq,region):('C',1,'west'),('C',2,'west'),('C',3,'east')|west valid1..3; east valid3..open|Repeated unchanged states must not create artificial history rows.
7|Attribute conversions within a bounded window|Assign each purchase to the last prior campaign click within7days, breaking same-time ties by click_id.|purchaseP day10; clicksC1 day2,C2 day5,C3 day11|P attributedC2|A future click and an older-than7day click cannot receive credit.
7|Evaluate hierarchical access rules|Determine accessible warehouse IDs from explicit grants and denials, with denial taking precedence.|grants userU warehousesA,B; denies userU warehouseB|U accessibleA only|Do not infer access from an unrelated user's grant.
7|Compare revision versions as sets and values|Report inserted,deleted and changed order rows between two model releases.|v1 A10 B20;v2 A11 C30|changedA10->11;deletedB;insertedC|Equal IDs with equal values belong to no difference category.
8|Measure a selective predicate plan|On a generated100000-row fixture, compare plans before and after a suitable index for a selective lookup.|events id1..100000; query id99999; localPostgreSQL|identical row99999; recorded EXPLAIN plans and elapsed measurements|Do not require a particular plan node on tiny or differently configured systems.
8|Compare sargable time filters|Compare a date-function filter with a timestamp range using an index and identical day boundaries.|one million generated UTC timestamps; report day2026-10-25|identical rows; plan evidence for both variants|Boundary tests include midnight and next-day midnight.
8|Spot skew in grouping workloads|Profile per-customer event counts before designing an optimization; quantify the largest key share.|1000events:900 forC1 and100 spread over100customers|largest_share0.9; distinct_customers101|Averages alone must not conceal the hot customer.
8|Reduce pre-join volume safely|Compare joining raw line rows with joining per-order aggregates while preserving the requested grain.|10000orders each10lines; one customer per order|10000final order rows; identical totals; intermediate cardinalities reported|Do not aggregate away a required line-level attribute.
8|Compare pagination correctness under inserts|Demonstrate offset and key-based continuation behavior after a new low-key row arrives.|initial IDs10,20,30,40; firstpage10,20; theninsert5|key_continuation returns30,40 without repeats|Discuss the separate handling of late low-key arrivals.
8|Check partition pruning empirically|Create monthly sandbox partitions and query one month using explicit bounds.|three monthly partitions; two rows each; selectOctober2026|onlyOctober rows; EXPLAIN evidence recorded|Correctness must hold even if the optimizer chooses an unexpected scan.
8|Compare exact and sampled diagnostics|Estimate a null rate from a reproducible sample and compare with exact whole-table count.|generated100000rows withNULL every10throw; fixed sample seed|exact_null_rate0.1; sample estimate and error reported|An estimate must never be labelled an exact acceptance count.
8|Benchmark materialized reuse|Compare repeated expensive reporting with a cached result and include refresh cost and staleness.|generated sales fixture; three repeated reports; one later sale|same prechange totals; cached result stale untilrefresh; timing evidence|A faster stale result must not be presented as current.
8|Find an accidental cross join before execution|Estimate join output using fixture cardinalities and compare with EXPLAIN estimates.|orders1000rows; currencies3rows; missing join condition|logical output3000rows; expected intended grain1000|Run only in a bounded sandbox, not a production-sized source.
8|Preserve numeric accuracy during optimization|Compare numeric-cent aggregation with a proposed floating-point optimization on cancellation-heavy data.|amounts=[10000000000000000,1,-10000000000000000] repeated10|exact_total10; alternative error measured|Reject an optimization that violates required exact cents.
9|Version a reporting contract|Provide old and new views during a column rename and prove both return the same business values.|base(id,amount_minor):('A',25);v1 expects cents;v2 expects amount_minor|v1 A25 andv2 A25; compatibility tests pass|Existing consumers must not break before the agreed retirement boundary.
9|Audit row-level access in a sandbox|Implement and test tenant-isolated reads using two low-privilege test roles.|rows tenantT1 A,tenantT2 B; rolesr1 forT1,r2 forT2|r1 seesA only;r2 seesB only|Testing only as table owner does not demonstrate isolation.
9|Build a data freshness indicator|Report stale when the latest committed event is more than15minutes old, using a supplied clock.|now12:30; latest_committed12:10; newer_uncommitted12:29|stale=true; lag20minutes|Uncommitted arrival metadata cannot establish successful freshness.
9|Define and validate a rollback query|Before a bounded repair, save affected rows and demonstrate restoring them in a sandbox transaction.|target A10 B20; repairA to11; savedbeforeimageA10|repairA11; rollbackA10; Bunmodified|The restoration predicate must not touch unrelated IDs.
9|Verify an incremental model against full rebuild|Compute a target via a full source replay and via two incremental batches, including a correction.|batch1 A10 B20;batch2 A11 C30|both targets A11 B20 C30|Comparison includes keys,values and row counts, not totals alone.
9|Design a migration lock drill|Use two sandbox sessions to observe a blocked schema change and enforce a short lock timeout.|session1 holds conflicting lock;session2 ALTER with short timeout|session2 times out;session1 data unaffected; retry after release succeeds|Never conduct the drill on a shared database.
9|Check restore completeness at reporting grain|Compare a restored database with source control totals at date and currency grain.|controls D1 INR100,D1 USD50; restore D1 INR150|reportmissingUSD50 andINRdifference50|A matching all-currency total is insufficient evidence.
9|Publish an operational reconciliation view|Combine source count,target count,rejection count and committed batch status into one explainable view.|source10,target8,rejected2,statuscommitted|balanced=true; delivered8; rejected2|A started batch with the same counts is not marked delivered.
9|Test a scheduled report retry|Make a sandbox report refresh idempotent under a repeated run ID.|runR1 writes reportdayD1 twice; sourceunchanged|one logical report version forR1; totals unchanged|A genuinely changed input must create a traceable different revision.
9|Protect sensitive query exports|Design a public report view omitting email and token while retaining allowed aggregates.|customers idC1,email,token; sales C1=100|public output total100; no email/tokencolumns|Check view definition and result schema, not only a screenshot.
10|Independently build a warehouse reconciliation suite|Design SQL checks for a sales mart spanning headers,lines,payments and refunds; defend grain and failure decisions.|seed six orders including partialpayment,duplicateline,unknownSKU andrefund|each injected issue surfaced; unaffected order totals correct; reusable checkoutputs|No supplied solution query; reviewer changes one fixture after submission.
10|Independently model and query shipment state|From out-of-order state events, produce current state and daily transitions with replay and late-arrival handling.|events packed1,sent3,latepacked2,delivered4 plus replay3|currentdelivered; deterministic transitionhistory; no repeatedeventcounts|Explain event ordering authority and show a conflicting-tie test.
10|Independently optimize a bounded warehouse report|Build a multi-source report then improve its measured plan while preserving exact output.|generated100000orders,1000000lines,skewedcustomers; resourcebudgetsupplied|before/after outputs equal; reproducible timings/plans; bottleneck justified|No claim of scalability without actual measurements and stated environment.
10|Design a temporal customer mart migration|Independently migrate an overwrite-only customer dimension to history while preserving current consumers.|snapshotCwest thenCeast; factF1 beforechange,F2 afterchange|F1west,F2east; currentvieweast; rollback and ambiguitychecks|Do not fabricate historical regions that the source never recorded.
10|Defend a month-end close pipeline|Implement SQL close reports, late adjustments and reconciliation with a frozen reporting boundary.|Octoberclosed100; latercorrection+5; Novemberopen20|frozenOctober100; explicitadjustment5; currentoperationalOctober105|Describe separate financial and operational views and test an independent change.
''')
author('postgresql', r'''
0|Confirm the sandbox database identity|Before loading anything, return the current database and current user from a learner-owned sandbox session.|A local disposable PostgreSQL database; no production credentials|one row naming the actual sandbox database and role|Stop if the connection points to a shared or production environment.
0|Inspect an existing table definition|Use the supplied sandbox table to report column names,types and nullability without changing data.|CREATE TABLE parcel(id TEXT NOT NULL, weight NUMERIC); one row P1,2|id:text:notnull; weight:numeric:nullable; rowcount remains1|Inspection must not modify the table or its rows.
0|Read a stored zero value|Query a sandbox metric table and distinguish a known zero from aNULL.|metrics(id TEXT,value INTEGER) rows A0,BNULL|A:value0; B:valueNULL|Do not replace unknown measurements automatically.
0|Explain a connection failure safely|Given a fake connection error, identify connection-refused versus authentication-failed and report the category.|two supplied messages: connection refused; password authentication failed|categories network_listener and authentication respectively|Never include passwords in diagnostic output.
0|Discover the server version|Read the sandbox server version and record it beside an executed smoke query.|A learner-owned PostgreSQL connection; SELECT1 allowed|actual version string and scalar1|Do not claim a version from a screenshot or documentation default.
1|Create a bounded landing table|Create a temporary parcel landing table with text IDs and integer units, then insert two supplied rows.|rows P1units2,P2units0|two stored rows with exact IDs and units|Temporary table disappears when its session ends.
1|Preserve supplier reference text|Store and retrieve a leading-zero supplier reference in an appropriate sandbox column.|reference00017|round-trip value00017 with length5|The reference must not be numerically normalized.
1|Set a useful default timestamp|Create an audit table whose omitted received_at is filled by the server; explicitly supplied timestamps survive.|insertA withouttime;insertB with2026-10-01T00:00Z|A hasnonnull received_at;B retains suppliedinstant|Compare against transaction timing bounds instead of inventing an exact current time.
1|Reject missing mandatory identifiers|Create a sandbox table requiring parcel_id and demonstrate rejection ofNULL while accepting P1.|inserts parcel_idNULL thenP1 in separate controlled transactions|NULL attemptfails;P1 exists; finalcount1|Show the failed attempt without leaving the session in an aborted transaction.
1|Keep separate schemas for landing and reporting|Create sandbox schemas landing and mart with same-named deliveries tables and query them explicitly.|landing.deliveries containsA;mart.deliveries containsB|explicit reads returnA andB respectively|Do not rely on a changing search_path to select the intended source.
2|Enforce nonnegative stock|Add a constraint rejecting negative units while permitting zero and positive values.|attemptunits-1,0,2|minus1rejected;0and2accepted|Test NULL separately and document whether it is permitted.
2|Enforce a natural delivery key|Store at most one row per source_system and delivery_id while allowing the same delivery_id from another source.|rows(web,D1),(web,D1),(store,D1)|twoaccepted logicalkeys; repeatedwebD1rejected|A delivery ID alone is not globally unique.
2|Load a small CSV through the client|Import supplied UTF-8 CSV into a temporary table without server-side access to arbitrary files.|CSV id,units\nP1,2\nP2,3|rowcount2;sumunits5|Preserve the input fixture and executed import command for review.
2|Reject an unknown warehouse reference|Use a foreign-key contract so stock cannot reference a warehouse absent from the parent table.|warehousesW1;stockA->W1 andB->W9|Aaccepted;Brejected;nostockforW9|Loading parent and child rows in the wrong order must be demonstrated separately.
2|Define exact money storage|Store amounts with two decimal places and demonstrate the chosen behavior for extra precision.|amount1.20;extra_precision1.235;negative-1.00|1.20round-trips; observedprecisionbehavior documented; explicitnegativepolicytested|Do not assume a NUMERIC scale alone rejects excess source precision.
3|Load parent and child rows atomically|Create a shipment and its package records in one transaction; roll back if one package is invalid.|shipmentS1;packagesP1units2,P2units-1|shipmentS1andbothpackagesabsentafterrollback|A later valid retry creates one shipment and two valid packages.
3|Use a savepoint for one recoverable row|Load three sandbox rows, recover from a duplicate middle key with a savepoint, and commit the other two.|existingA;incomingB,A,C|finalA,B,C; duplicateAreported|Do not silently skip errors outside the explicitly permitted duplicate-key case.
3|Return generated target identifiers|Insert two source customers into a table with generated IDs and return source-to-generated mappings.|sourcecodesC1,C2; targetidentitycolumn|two distinct generatedIDs mapped toC1,C2|Do not infer generated IDs from the previous maximum value.
3|Record a batch ledger with loaded rows|Commit imported rows and their successful batch-ledger entry together.|batchB1rowsA,B; injectfailurebeforeledgerinsert|failureleavesnobatchrows; successrecordsB1count2|A started ledger row is not a committed success.
3|Create a read-only consumer role|Grant a sandbox reporting role SELECT on one view while denying writes to its base table.|basecontainsA10;view exposesid,cents|rolecanreadA10;INSERTandUPDATEdenied|Verify using the reporting role instead of assuming grants work.
4|Stage before validating a typed load|Load raw text into staging, separate malformed quantities, then insert only valid typed rows.|rawA,'2';B,'bad';C,'0'|targetA2,C0;rejectBinvalid_units|An invalid cast inB must not abort validation forAandC.
4|Make a delivery upsert idempotent|Apply insert-or-update semantics on a unique source key; repeat the same batch.|targetA10;incomingA12,B20;repeatincoming|targetA12,B20;count2afterbothruns|An older source version must not overwrite a newer one.
4|Apply explicit deletion events|Process deletion markers using a staged batch while retaining an audit trail.|targetA,B;eventsdeleteA,upsertC|targetB,C;audithasdeleteA|Absence from an incomplete batch is not a deletion.
4|Compare source and loaded totals|Build a reconciliation query at batch and currency grain after a load.|sourceB1INR100,B1USD20;targetB1INR120|INRdifference20;USDmissing20|Do not combine currencies to claim balance.
4|Validate schema ownership on deployment|Deploy a table and read view under an owner role, then verify consumer privileges survive the deployment.|rolesowner,reader;schemafixture;twoconsecutive deployments|readerSELECTworksafterboth;readerDDLdenied|Do not grant superuser privileges to solve an ownership issue.
5|Run a bounded local file-to-table pipeline|Create a reproducible local load command that stages,validates,commits and reports one batch.|CSV A2,Bbad,C3;temporaryschema|targetA2,C3;rejectionB;batchledgeraccepted2rejected1|A repeated command leaves two logicaltargetrows.
5|Advance a committed extraction cursor|Use a cursor table and target writes in one transaction.|cursor10;incomingseq11,12;injectfailureafterfirstinsert|failureleavescursor10;successleavescursor12andtworows|Cursor update before durable target writes is forbidden.
5|Refresh a reporting materialization|Create a materialized daily report, add a sale, demonstrate staleness and refresh it.|initialsales100;addition25|report100before refresh;125after refresh|Document what readers can see during the chosen refresh approach.
5|Record row-level source lineage|Keep source_file,source_row and batch_id alongside accepted target records.|a.csv row2 A10; b.csv row2 B20;batchB1|Apoints toa.csv:2;Bpoints tob.csv:2;bothB1|Do not substitute target row position for source row number.
5|Use a consistent snapshot for reconciliation|Read source count and sum from one transaction snapshot while another session inserts a row.|initialtworowssum30;session2insertthirdrow20|consistentreportcount2sum30orcount3sum50accordingtochosen snapshot|Demonstrate why separate uncontrolled reads can describe different states.
6|Recover an aborted transaction explicitly|Cause a sandbox constraint error, inspect session behavior, then rollback and execute a valid statement.|transaction insertsinvalidnegativeunits;thenSELECT1|errorobserved;rollbackperformed;SELECT1succeedsafterrecovery|Do not claim the connection is usable while it remains transaction-aborted.
6|Bound a blocked loader|Hold a row lock in session1; session2 updates it with a short lock timeout and reports a retriable outcome.|oneinventoryrowA10;session1locksA|session2timesoutwithoutpartialupdate;retryafterrelease succeeds|All lock drills run only in disposable sessions.
6|Prevent duplicate concurrent batch claims|Have two sandbox workers claim the same batch under a uniqueness/transaction contract.|batchB1;twoworkersstarttogether|exactlyoneclaimowner;oneboundedalready_claimedoutcome|Do not infer safety from sequential runs only.
6|Retry a serialization conflict safely|Use two sandbox transactions that conflict underSERIALIZABLE and retry the entire losing transaction.|twoindependentreservationattempts;capacity1|atmostonereservation; serializationfailurecapturedandretriedboundedly|Do not retry only the finalstatement from a failed transaction.
6|Restore a deleted sandbox table from backup|Dump a small sandbox schema, remove its test data and restore into a fresh schema/database.|two tableswithforeignkey;rowsAandB|restoredrowcounts,valuesandforeignkeychecksmatchbeforebackup|Never run destructive restore commands against an unverifieddatabase.
7|Partition events by business month|Create a sandbox range-partitioned event table and route boundary rows.|events2026-10-31T23:59and2026-11-01T00:00inexplicittimezone|rowslandinOctoberandNovemberpartitionsrespectively|An out-of-range event follows an explicitreject/defaultpartitionpolicy.
7|Evolve an added optional column safely|Add currency with a stagedbackfill and preserve the old consumer view.|existingA100;newrowB200USD;oldconsumerexpect id,cents|oldviewstillworks;existingrowcurrencysetbyexplicitbusinessrule;BUSDpreserved|Do not claim historicalcurrencyisinferredfrommissingdata.
7|Prevent overlapping price validity|Enforce or validate nonoverlappingeffectivepriceintervals perSKU.|A1..5cents10;A4..8cents20;B1..5cents30|overlapAblocked/reported;Bindependent|Adjacentclosed-openintervalsareallowed.
7|Extract fields from versioned JSON events|Store raw JSON, extract version1and2contracts into a typed reporting view, rejectunknownversions.|v1{id:A,cents:10};v2{id:B,amount_minor:20};v9{id:C}|typedA10,B20;Creportedunsupportedversion|Rawpayloadremainsavailableforreprocessing.
7|Separate tenant access using row policies|Create two tenant roles and test isolation under actualnonownerconnections.|rowsT1:A,T2:B;rolesr1,r2|r1seesAonly;r2seesBonly|Explainowner/superuserbypasswheninterpretingtestresults.
8|Measure an index for incremental extraction|Generate100000events and compare a cursor-rangequerywith/without anappropriateindex.|seq1..100000;extractseq>99990|tenidenticalrows;EXPLAINANALYZEplansandtimingsrecorded|Do not promiseanindexscanregardlessofplannerstatistics.
8|Inspect a slow join with real cardinalities|Generate skewedorders and examine estimatedversusactualjoinrows.|10000orders;9000forcustomerC1;customerreferenceunique|final10000rows;estimated/actualevidenceperimportantnode|Refreshingstatisticsmustnotchangequerycorrectness.
8|Compare bulk and rowwise local loading|Load the samesynthetic100000rowsrowwiseandthroughaclientbulkpath,recordingcostsandvalidation.|generatedid1..100000units1|bothrowcount100000sumunits100000;timingandmethodrecorded|Includecommitcostanddonotclaimcross-machinebenchmarkgenerality.
8|Measure vacuum-related operational evidence|Update sandbox rows repeatedly and inspect table/dead-tuple statistics before and aftermaintenance.|disposabletable10000rowsupdated5times|statisticsandmaintenancecommandsrecorded;logicalvaluesunchanged|Statisticsareestimatesandmayneedrefresh/wait;donotfabricateexactdeadtuplenumbers.
8|Evaluate a composite index ordering|Compare queryplans fortenant+timefiltersagainsttwocandidateindexorders.|100tenants;1000timestampspertenant;one-tenantrecentwindowquery|samequeryoutput;plansandindexsizesrecorded;choicejustified|Also testatime-onlyquerytorevealthechosenindexlimitation.
9|Deploy and rollback a bounded migration|Apply a versionedcolumn/viewmigration,runconsumerchecks,andrestoreoldcontract.|v1viewid,cents;v2viewid,amount_minor;oneoldconsumer|forwardandrollbackchecksreproduceA25; migrationledgeraccurate|Arollbackmustpreserverowswrittenaftertheforwardmigrationunderastatedpolicy.
9|Test backup recovery point evidence|Create a consistent logicalbackup,addaseparatepostbackupevent,restoretoafreshsandboxandcompare.|beforebackupA;afterbackupB|restorecontainsAandnotB;recoveryboundarydocumented|Do notclaimPITRfromalogicaldumpalone.
9|Monitor loader transactions and lag|Build a sandbox operationalqueryshowingrunningtransactionageandlastcommittedbatchtime.|fakebatchledgerlastcommit12:00;clock12:30;controlledlongtransaction|lag30minutes;longtransactionvisiblewithactualsessionevidence|Nootheruser'ssensitivestatementtextshouldbeexported.
9|Enforce least-privilege batch execution|Run aloadwitharolelimitedtostaging,targetandledgeroperationsneededbythecontract.|loaderrole;targetA;unrelatedprivate.table|loadandledgercommitsucceed;unrelatedreadandDDLdenied|Do notuseownercredentialsforthepermissionacceptancechecks.
9|Rehearse a safe partition-retention operation|Detach anexpiredsandboxpartitiononlyaftercheckingrowcountsandabackupmanifest.|Septemberpartition2rows;Octoberpartition3rows;Septemberexpired|Septemberdetachedandrecoverable;October3rowsunchanged|Keepadefiniteverifieddatabase/schemaallowlistforthedrill.
10|Independently build an idempotent relational loader|Implement staging,qualitychecks,upserts,ledger,cursorandfailure recoveryinadisposableschema.|batch1A10B20;batch2A11Cbad;failureaftertargetwritebeforecommit|targetA11B20;Crejected;restartsunchanged;ledgercountsreconcile|Reviewerinjectsduplicatekeysandachangedcursorafterinitialsubmission.
10|Independently engineer a concurrent reservation feed|Designcapacity-safeprocessingofduplicateandconcurrentreservationevents.|capacity2;threeconcurrentuniqueeventsplusreplayofthefirst|atmost2activeacceptedreservations; replaydoesnotconsumecapacity|Provideobservedconcurrencytestsanddefendisolation/lockingchoices.
10|Independently operate a temporal warehouse slice|Createcustomerhistory,facts,latecorrectionhandlingandread-onlyconsumerswitharecoverydrill.|customerchangeswesttoeast;factsbefore/after;one latecorrection|as-ofjoincorrect;currentviewcorrect;rollback/replaydemonstrated|Explainwhathistorycannotberecoveredfromavailableevidence.
10|Independently tune and defend an ingestion workload|Implementandmeasureabulkloadplusincrementalqueryonageneratedmillion-rowfixture.|specifiedlocalmemorybudget;skewedkeys;duplicatebatch;selectiveextract|correctcountsandreplay;plans,memory,timingandtradeoffevidence|Anunmeasuredoptimizationclaimdoesnotmeetacceptance.
10|Independently recover a damaged reporting environment|Restoreadisposablesalesmartanditsrole/viewcontractsfromknownartifactsafterinjecteddamage.|backupcontainsA,B;newerbatchCretainedinrawsource;viewandgrantremoved|restoredA,B;replayedConce;readeraccessworks;reconciliationspass|Distinguishprovenrecoverypointfromunrecoverablemissingrawdata.
''')

author('python', r'''
0|Read one product description|A catalog feed contains one JSON-like product record. Return its description exactly, including punctuation.|product={sku:A,description:'Tea, green'}|'Tea, green'|A comma in the description must not create two fields.
0|Recognize a boolean source flag|A catalog operator needs to distinguish the literal boolean false from missing data. Return the supplied active value unchanged.|product={sku:A,active:false}|false|Do not convert the boolean to text or treat it as absent.
0|List the keys of one record|A support engineer inspects an unfamiliar product record. Return its field names in insertion order.|record={sku:A,description:Tea,active:true}|['sku','description','active']|Do not return values or reorder keys alphabetically in this contract.
1|Decode a UTF-8 product description|A supplier sends UTF-8 bytes. Decode them strictly and return the original accented text.|bytes=[99,97,102,195,169]|'café'|Invalid UTF-8 must be reported instead of silently replaced.
1|Parse one JSON object|Read one JSON text document and return its SKU value. Keep numeric-looking SKU text unchanged.|JSON text: {"sku":"0017","units":2}|'0017'|A JSON array is the wrong top-level contract and must be rejected.
1|Keep Unicode identifiers distinct|Compare two supplied SKU strings exactly; do not lowercase or strip accents without a business rule.|left='cafe'; right='café'|equal=false|Document that visually similar Unicode text may still be different identifiers.
2|Validate JSON value types|Require units to be an integer, excluding booleans even though Python treats bool as an integer subclass.|rows=[{sku:A,units:2},{sku:B,units:true},{sku:C,units:'2'}]|accepted=['A']; rejected=['B','C']|Explicit conversion is a separate contract; do not silently coerce these values.
2|Inspect nested optional metadata|Read product metadata.color when metadata is an object; absent metadata means unknown and malformed metadata is rejected.|rows=[{sku:A,metadata:{color:red}},{sku:B},{sku:C,metadata:'red'}]|colors={A:red,B:unknown}; rejected=['C']|A malformed nested object must not masquerade as absent metadata.
2|Keep JSON numeric precision at ingestion|Parse JSON decimal prices into an exact representation and report their sum as decimal text.|JSON text: [{"price":0.1},{"price":0.2}]|'0.3'|Do not accept an inexact binary sum as the exact monetary result.
3|Read one JSON object per line|Process a newline-delimited product feed, preserving line numbers when one document is malformed.|text lines: {"sku":"A"}\nnot-json\n{"sku":"C"}|accepted=['A','C']; rejected=[{line:2,reason:invalid_json}]|A bad line must not corrupt the following valid document.
3|Serialize a product export deterministically|Write UTF-8 JSON with sorted keys and a documented compact separator policy so equal objects produce equal bytes.|records with keys inserted in opposite orders: {sku:A,units:2} and {units:2,sku:A}|serialized bytes identical for both objects|Do not claim semantic equivalence requires raw supplier bytes to be identical.
3|Distinguish numeric strings from numeric values|A consumer requires price_text while units must remain numeric. Export each field with its required JSON type.|product={sku:A,price_text:'1.20',units:2}|JSON types sku:string,price_text:string,units:number; values preserved|A round trip must preserve '1.20' rather than '1.2'.
4|Read a ZIP product bundle safely|Extract only regular CSV files from a supplied ZIP into a temporary root, rejecting unsafe paths.|ZIP entries products.csv,notes.txt,../escape.csv|products.csv extracted; notes ignored; unsafe entry rejected|No resolved output path may escape the temporary root.
4|Honor an explicit bundle manifest|Process only files named in a supplier bundle manifest and report missing and unlisted files separately.|manifest=['products.jsonl','prices.jsonl']; archive=['products.jsonl','notes.txt']|missing=['prices.jsonl']; unlisted=['notes.txt']; publication blocked|Do not process an arbitrary file just because its extension looks useful.
4|Resolve relative source references safely|A manifest refers to a schema file relative to the bundle root. Resolve it without depending on the current working directory.|bundle_root=/temporary/bundle; reference=schemas/product.json|resolved path stays under bundle_root and names schemas/product.json|Absolute and traversal references outside the root are rejected.
5|Build a catalog contract report|Validate JSONL records for SKU,units and metadata shape; export accepted JSONL plus a line-numbered reject report.|line1 A units2; line2 B unitstrue; line3 C units0|accepted A,C; rejected B invalid_units_type; read3accepted2rejected1|Preserve original raw text for rejection evidence without logging unrelated sensitive fields.
5|Apply a supplied transformation registry|Choose one of two explicit product contract versions and dispatch to its registered transformation; reject unknown versions.|v1 {sku:A,qty:2};v2 {sku:B,units:3};v3 {sku:C}|normalized Aunits2,Bunits3; v3 rejected|Do not dynamically execute code supplied inside the input document.
5|Retain raw and normalized catalog artifacts|Save immutable raw JSONL and normalized output under the same run ID, linking both digests in a manifest.|rawAunits'2'; declared version permits conversion; runR1|raw bytes preserved; normalized Aunits2; manifest links both digests|A normalized export must never overwrite the raw evidence.
6|Detect a duplicate JSON property|Reject a product object containing the same property name twice instead of accepting an ambiguous last value.|JSON text: {"sku":"A","units":2,"units":9}|rejected reason duplicate_property:units|A normal object with one units property remains accepted.
6|Bound record size before parsing|Stop reading an individual JSONL record after a configured byte limit and quarantine it without exhausting memory.|max_line_bytes=32; supplied small line and a100-byte line|small line processed; large line rejected oversized_record|The limit applies to bytes, not Unicode character count.
6|Resume a byte-addressed JSONL feed|Persist a byte offset only at a fully committed record boundary and resume after a simulated failure.|UTF-8 lines A,café,C; commit firsttwo; fail beforethirdcommit|restart reads C only; no split multibyte character; no duplicate A|Do not use text character indexes as byte offsets.
7|Apply forward-compatible metadata rules|Preserve unknown metadata keys while validating known keys under a versioned contract.|product={sku:A,metadata:{color:red,supplier_tag:x}}|normalized metadata retains color and supplier_tag|Unknown top-level required-contract violations still produce explicit failures.
7|Detect canonicalization collisions|A business proposes case-insensitive SKU normalization. Report collisions before enforcing it.|SKUs=['ab','AB','cd']|collision normalizedAB maps to ['ab','AB']; publication blocked|Do not silently choose one product's values to resolve the collision.
7|Manage producer and consumer schema versions|Validate a bundle against a selected contract version and emit the contract identifier with every manifest.|producer schema2 has optionalcolor; consumer accepts schema1and2|schema2 accepted and recorded; schema3 blocked with unsupported_version|Passing one record does not prove the complete bundle schema is compatible.
8|Stream oversized JSONL bundles|Generate500000 bounded product records and validate them without loading the complete bundle into memory.|generator yields SKU1..500000 units1 with every100th unitsbad|accepted495000;rejected5000; measured peak below64MiB|Produce exact counts without retaining all rejected raw records in memory.
8|Avoid repeated serialization work|Compute output byte count and digest from the exact bytes written in one pass.|three normalized product objects; fake serializer counts calls|one serialization per object; reported bytes/digest equal output file|Do not hash a second representation that differs in whitespace or Unicode policy.
8|Measure compression as a pipeline tradeoff|Compare uncompressed and gzip catalog exports on the same generated source, recording byte size,CPU time and round-trip equality.|100000 repetitive product descriptions|both round trips identical; sizes and measured compression/decompression times recorded|Do not choose compression on size alone when runtime limits matter.
9|Maintain a contract compatibility release gate|Test a candidate catalog exporter against v1 and v2 consumer fixtures before release.|candidate removes sku; both consumers require sku|release blocked with missing sku evidence for both consumers|Keep the last approved artifact and record the failing candidate version.
9|Operate a retention policy for raw bundles|In a sandbox, delete only raw bundles older than the configured cutoff that have verified archive manifests.|bundleA old archived;B old unarchived;C recent archived|A eligible;B blocked;C retained; dry-run report lists decisions|Execution must verify resolved paths stay in the configured temporary root.
9|Prove a catalog replay across code versions|Replay one immutable bundle through an approved and candidate transformation and compare by SKU,field and rejection reason.|A inputunits2; candidate mapsunitsincorrectly3; B invalid inboth|difference Aunits2->3; B rejection unchanged|A matching accepted row count is insufficient evidence of compatibility.
10|Independently build a versioned product bundle processor|Implement safe ZIP ingestion,manifest validation,JSONL normalization,rejections,replay and contract versioning.|bundle contains Unicode,duplicateJSONproperties,missingmanifestfile,andaversion2record|unsafe/ambiguous inputs rejected; good rows preserved; replay deterministic; provenance complete|Reviewer replaces one metadata schema and injects a truncated bundle after submission.
10|Independently defend a catalog schema migration|Run old/new product consumers through a staged contract migration while retaining raw evidence and rollback.|old units text;new units integer; ambiguous '2.5'; optional metadata addition|both supported consumers receive valid artifacts; ambiguous record rejected; rollback demonstrated|Explain the boundary between permitted conversion and silent data repair.
10|Independently repair a corrupted bundle history|Recover a catalog from archived raw bundles,verified manifests and corrections after deleting the sandbox target.|day1 A2;day2 A3 Bbad;day3 B4; one manifest digest mismatch|targetA3B4 only from verified inputs; mismatch quarantined; recovery evidence retained|Do not regenerate or trust the mismatched archive without an authoritative replacement.
''')

author('sql', r'''
0|Read one support ticket subject|A data platform support export needs just the subject of a supplied ticket.|tickets(id,subject):('T1','Missing daily sales')|subject='Missing daily sales'|Do not expose the requester's email in this result.
0|Keep a severity label unchanged|An incident record contains severity as text. Return it exactly before introducing any ranking rule.|incidents(id,severity):('I1','P2')|severity=P2|Do not assume lexical sorting defines business severity.
0|Inspect a known run identifier|A support analyst needs the run ID column from a supplied pipeline-run fixture.|runs(run_id,status):('R007','failed')|run_id=R007|Leading zeros inside the identifier must survive.
1|Find unresolved support tickets|Return tickets with resolved_atNULL, ordered by ticket ID.|tickets(id,resolved_at):('A',NULL),('B','2026-10-25'),('C',NULL)|A,C|A null resolved_at means unresolved under this contract, not missing source ingestion.
1|Compare a literal underscore in pipeline names|Select pipeline names beginning exactly daily_ where the underscore is a literal character.|pipelines(name):('daily_sales'),('dailyXsales'),('daily_orders')|daily_orders,daily_sales|Do not let a pattern wildcard match dailyXsales.
1|Choose a displayed incident owner|Use the assigned owner when known; otherwise display UNASSIGNED.|incidents(id,owner):('A',NULL),('B','Sam')|A:UNASSIGNED;B:Sam|A supplied blank owner remains blank unless a separate cleanup rule says otherwise.
2|Count incident severities conditionally|Produce counts for P1,P2 and other severities in one result.|incidents(severity):('P1'),('P2'),('P2'),('P3')|p1=1,p2=2,other=1|NULL severity is counted in other explicitly.
2|Find tickets with no status events|Return tickets absent from a supplied event table.|tickets(id):('A'),('B'); events(ticket,state):('A','new')|B|Repeated events forA must not affect ticketB's classification.
2|Keep an unknown service match|List all incidents and attach service name when known, retaining unknown service IDs for follow-up.|incidents(id,service_id):('A','S1'),('B','S9'); services(id,name):('S1','orders')|A:orders;B:NULL with service_idS9|Do not silently drop an incident because reference data is incomplete.
3|Calculate elapsed incident duration|Compute resolution duration in whole elapsed minutes for resolved incidents; leave unresolved durationNULL.|A opened10:00 resolved10:45;B opened11:00 unresolved|A:45;B:NULL|Negative elapsed durations are flagged as invalid source chronology.
3|Apply service-specific response targets|Join severity target minutes and determine whether first response met the target.|ticketA severityP1 opened10:00 responded10:20; targetP1=15|A:response20,target15,breached=true|Missing target metadata produces unknown rather than an automatic pass.
3|Separate automation and human responses|For first-human-response reporting, ignore bot events while preserving tickets with no human response.|ticketA events botminute1,humanminute8;ticketB botminute2only|A:first_human8;B:NULL|A bot event cannot satisfy the human-response SLA.
4|Reconcile tickets across support platforms|Use an explicit cross-system mapping to attach vendor case IDs and retain missing mappings.|internalA,B;mappingA->V7;vendorV7,V9|A matchedV7;B internal_only;V9 vendor_only|Do not assume equal-looking IDs imply a mapping.
4|Count affected runs without a join explosion|Report distinct affected runs and linked tickets per incident using separate grains.|incidentI1 linkedrunsR1,R2; linkedticketsT1,T2,T3|I1:runs2,tickets3|Joining both raw bridges creates6rows and must not inflate counts.
4|Apply an effective-dated support calendar|Attach the support-team timezone/calendar effective on ticket open date.|teamT usesUTCuntilOct1,Asia/KolkatafromOct1;ticketopensOct2|ticket usesAsia/Kolkata calendar|Future calendar changes must not alter an already-frozen historical assignment.
5|Measure a reopen rate|A resolved ticket later returning to open is reopened. Count each ticket once, regardless of repeated reopen events.|A states open,resolved,open,resolved,open;B open,resolved|reopened_tickets1;ever_resolved2;rate0.5|A never-resolved ticket is not reopened.
5|Calculate time spent in each incident state|Use ordered state changes to derive elapsed intervals through a supplied observation end time.|I1 openminute0,pausedminute10,openminute20,resolvedminute35;end40|open25minutes;paused10;resolved5|Use the explicit observation boundary for the final state.
5|Create an incident-to-run impact report|Connect incidents to affected runs and their rejected row counts without duplicating a run linked more than once.|I1linksR1,R1,R2;runsR1rejected2,R2rejected3|I1affected_runs2,rejected_rows5|Repeated bridge rows are audited rather than counted as extra impact.
6|Find impossible support state transitions|Report a resolution preceding ticket creation and two state events sharing an authoritative sequence.|Acreated10resolved9;Beventsseq1open,seq1resolved|A invalid_chronology;B ambiguous_sequence|Do not silently pick a preferred state for conflicting equal sequence events.
6|Exclude maintenance from operational incident time|Subtract the union of overlapping approved maintenance intervals from an incident duration.|incident0..60;maintenance10..30and20..40|maintenance30;chargeable30|Overlapping maintenance must not be subtracted twice.
6|Surface missing monitoring intervals|Given expected5-minute checks, report missing intervals separately from successful checks.|expectedminutes0,5,10,15;observed0success,10failed,15success|minute5 missing;minute10 failed|A missing observation is not the same as a passing check.
7|Compute business-hour response time|Use an explicit calendar table of open minutes to measure a ticket across overnight closure.|supportopenMon09:00..17:00,Tue09:00..17:00;ticketMon16:30..Tue09:30|business_elapsed60minutes|Do not count calendar elapsed minutes during the closed night.
7|Attribute a shared incident without double counting|Report per-service impact and unique overall affected runs when one run belongs to two impacted services.|I1servicesS1,S2;S1runR1;S2runsR1,R2|S1count1;S2count2;overall2|The sum of service counts is not the unique overall count.
7|Compute incident percentiles with a declared convention|Calculate median and95th percentile duration and state discrete versus interpolated semantics.|durationsminutes=[1,2,3,4,100]; nearest-rank convention|median3;p95100|A different percentile function must be justified by its actual convention.
8|Inspect report fan-out before optimization|Measure intermediate rows in a ticket-event-audit report and reduce them before expensive aggregation.|10000tickets;10eventsand5auditrowsperticket|naivejoin500000rows;correctreport10000rowswithunmultipliedmetrics|An optimization must preserve ticket and event/audit grains.
8|Measure range-based incident lookup|Compare a query selecting active incidents during an interval with an indexed alternative on a bounded fixture.|100000syntheticintervals;lookupwindow1000..1010|identicaloverlapresults;plansandtimingsrecorded|Use an explicit closed-open overlap rule at interval endpoints.
8|Explain a misleading average incident duration|Compare mean,median,p95 and maximum on a skewed incident-duration distribution before recommending a metric.|durations=[1,1,1,1,96]|mean20;median1;nearest-rankp9596;max96|Do not discard the long incident as an outlier without a business rule.
9|Publish an SLA report with traceable exclusions|Produce numerator,denominator and explicitly classified exclusions for a frozen reporting period.|ticketsAmet,Bbreached,Cmissingtarget,Doutsideperiod|eligible2;met1;rate0.5;excludedCunknown_target,Doutside_period|A percentage without its eligible population does not pass acceptance.
9|Keep a historical incident report reproducible|Store a report boundary,calendar version and source high watermark so a later rerun explains changes.|reportOct25calendarv1cursor100;latercalendarv2andnewseq101|originalsnapshotreportreproduced;newrevisionseparatelyidentified|Do not silently replace frozen historical results with current definitions.
9|Audit a monitoring rule rollout|Compare old and candidate breach rules against identical incidents before promoting the candidate.|oldthreshold15;newthreshold10;durations8,12,20|onlyduration12changespass_to_breach;countold1new2|Retain rule versions and per-incident classification differences.
10|Independently build a support analytics mart|Design incident,ticket,run-impact and calendar reporting with precise grains and replayable reports.|fixturesincludeoverlappingmaintenance,reopens,missingtargets,sharedrunimpact|allinjectedcaseshandled;ratesanddurationsreconcile;independentreviewfixturepasses|Defend which unknowns are excluded,reported or block publication.
10|Independently investigate a false SLA improvement|Determine why a reported success rate improved after a migration and produce a corrected comparable metric.|oldreport100eligible80met;newreportdrops20breachedticketswithmissingmapping|correctedeligible100met80;reportednew100percentexposedascoverageerror|Provide row-level reconciliation evidence instead of assuming genuine improvement.
10|Independently design a reliable incident-close report|Create a frozen month-end incident report with late-event adjustments and verified consumer access.|closedreportOct100incidents;lateeventchangestworesolutions;newNovincidents3|originalclosepreserved;twoexplicitadjustments;Novemberisolated|Reviewer changes a timezone/calendar boundary and expects a bounded rerun.
''')

author('postgresql', r'''
0|Read one device reading|A telemetry operator needs device_id and reading from a supplied sandbox table.|readings(device_id TEXT,reading INTEGER):('D1',7)|one row D1,7|Return stored values without inventing a unit conversion.
0|Inspect the session timezone|Read the sandbox session timezone and record it before interpreting timestamps.|A learner-owned disposable PostgreSQL session|actual timezone setting returned|Do not infer the session setting from the operating system timezone.
0|Read a named result column|A downstream checker expects a result column named reading_count from a scalar count query.|readings(device_id):('D1'),('D2')|reading_count=2|Check the returned column name as well as its value.
1|Store a known sensor instant|Insert an offset-aware timestamp into a timestamp-with-time-zone column and read its UTC representation.|deviceD1 instant2026-10-26T10:00:00+05:30|UTC instant2026-10-26T04:30:00Z|Changing session display timezone must not change the stored instant.
1|Use an explicit schema search path|Demonstrate which of two same-named readings tables is selected under a controlled search_path.|schemaa.readings contains1; schemab.readings contains2|patha,b selects1; qualifiedb.readings selects2|Reset the session setting after the sandbox exercise.
1|Inspect a SQL error code|Cause a unique-key violation in a temporary readings table and report its SQLSTATE safely.|existing deviceD1 sequence1; duplicate insert|SQLSTATE23505; duplicate rejected|Record the category without exposing connection credentials.
2|Store raw JSON telemetry|Insert a JSONB payload and retrieve an integer temperature and a missing-field check.|payload={device:'D1',temp:0}|temp0; humidity missing=true|A present JSON null and an absent key must be distinguishable.
2|Expand a batch array with positions|Store a bounded integer array and return its elements with original ordinal positions.|array=[5,0,8]|(1,5),(2,0),(3,8)|Zero values and repeated values must be retained.
2|Validate a telemetry status domain|Define an allowed status contract accepting ok and warning while rejecting an unknown status.|attemptstatusesok,warning,banana|ok and warning accepted; banana rejected|Document how adding a future valid status changes the schema contract.
3|Generate a reproducible telemetry fixture|Create a temporary100-row source using a deterministic generator rather than a checked-in large file.|sequence1..100; reading=sequence modulo10|count100; minsequence1; maxsequence100; sumreading450|Running fixture setup twice must not accumulate200rows.
3|Use a generated line value column|Create a stored derived value from units and unit_cents, demonstrating update behavior.|rowA units2 unit_cents15; then units3|initialline_cents30; afterupdate45|The application must not separately write a conflicting derived value.
3|Check JSON measurement types|Validate raw JSON temperature is numeric and not text before inserting typed readings.|payloads D1temp0,D2temp'0',D3missingtemp|D1 accepted;D2wrong_type;D3missing_measurement|A JSON boolean must not be accepted as a numeric measurement.
4|Parameterize a repeated device query|Prepare or parameterize a query for one device ID and reuse it for two IDs, preserving an embedded quote.|devices D1,D'2 with known readings|each requested device returns only its own records; quote preserved|Never concatenate the device value into executable SQL.
4|Join JSON telemetry with a relational registry|Extract device_id from JSONB and match a unique registry row; report unregistered devices.|payloads D1temp10,D9temp20;registryD1regionwest|D1 west10;D9 unregistered|Registry duplication must be detected before telemetry totals are trusted.
4|Keep a per-device extraction position|Use a cursor table keyed by device so one delayed device does not advance another's position.|cursorsD1=10,D2=5;incomingD1seq11,D2seq6|proposedD1=11,D2=6; both committed atomically with their writes|A failed D2 batch must not claim D2 cursor6 committed.
5|Expose a stable telemetry function contract|Create a SQL function returning readings for a device within closed-open time bounds.|D1 readings at10:00,10:05,10:10;request10:00..10:10|two readings10:00and10:05|Specify return column names and test an empty interval.
5|Store device corrections as separate versions|Keep raw reading versions and expose the latest authoritative version per device and sequence.|D1seq1version1value10;version2value12|rawcount2;currentvalue12|A repeated identical version is idempotent; a conflicting same version is rejected.
5|Deliver telemetry and audit together|Use a transaction to insert typed readings and one audit entry with accepted/rejected counts.|rawD1valid,D2invalid; injectfailurebetweenreadingandaudit|failure commits neither; success readingD1 plusauditaccepted1rejected1|An audit row alone cannot stand for a successful reading commit.
6|Keep failed audit hooks from lying about success|Create a sandbox audit mechanism and inject its failure to observe transactional behavior.|reading insert invokes audit write; audit write forced to fail|reading and audit both absent after rollback|Do not catch and ignore the audit error while claiming complete transactional logging.
6|Use advisory locking for one maintenance owner|Have two sandbox sessions compete for a named device-maintenance lock and release it explicitly.|sessionsAandB try same logicaldevicekey|one owner; second fails or waits according to bounded contract; release enables next owner|A lock does not replace data constraints or durable run evidence.
6|Consume a work queue without duplicate claims|With two workers, claim pending sandbox work rows under a transaction-safe queue contract.|queuejobs1..4;twoworkersclaimtwoeach|allfourjobsclaimedonce; no duplicateownership|Crash one worker before commit and show its uncommitted claims remain recoverable.
7|Handle transactional change notifications|Demonstrate a notification delivered after commit and absent after rollback, treating it as a wake-up hint.|listener active;txn1notifiesandcommits;txn2notifiesandrollsback|listenerreceivestxn1only; durablequeueholdsactualwork|Do not use notifications as the sole durable record of unprocessed work.
7|Enforce nonoverlapping device reservations|Use a PostgreSQL interval representation and a suitable constraint or validation contract for reservations.|D1reservations[10,20),[20,30),[15,25);D2[15,25)|firsttwoD1allowed;overlappingthirdD1rejected;D2allowed|State any required supported extension and provide a validation fallback if unavailable.
7|Separate valid time from arrival time|Store when a measurement applies and when it arrived; query by each independently.|D1 eventtime10:00arrived10:20;D2eventtime10:10arrived10:11|eventorderD1,D2;arrivalorderD2,D1|A late arrival must not be relabelled as a later event time.
8|Compare JSONB and typed filter plans|Generate100000 payloads, expose a frequent filter as a typed representation, and compare correctness and measured plans.|deviceIDsD1..D100 repeated; temp0..99|same selected reading keys; query plans,size,timing evidence recorded|Include the cost of populating and maintaining the typed representation.
8|Measure queue contention under load|Run bounded concurrent sandbox workers on1000jobs and record throughput,waiting and claim uniqueness.|1000jobs;workers1then4;fixedfakeprocessingcost|alljobscompletedonce;measuredelapsedandcontentionevidence|Higher worker count is not assumed faster without observations.
8|Inspect prepared query behavior under skew|Compare repeated selective and nonselective device queries with plan evidence under a skewed fixture.|Dhot owns90percent of100000rows; Dcold owns10rows|both correct; measured plans and row estimates captured|Do not assume one cached plan is best for both selectivities.
9|Apply a statement time budget|Execute a deliberately expensive sandbox query under a short statement timeout and demonstrate recovery.|controlled sandbox query plus statement_timeout50ms|query cancelled with timeout category; connection usable after required rollback|Do not conduct the timeout drill on a shared workload.
9|Prove tenant telemetry isolation through views and roles|Expose only authorized device readings through a controlled reporting interface and verify with low-privilege sessions.|tenantT1deviceD1;T2deviceD2;separatereaderroles|each reader sees its own device only; direct base access denied|A superuser test cannot prove the consumer isolation contract.
9|Archive telemetry with recoverable manifests|Move an old sandbox telemetry partition to an archive workflow, recording schema,rowcount,digest and boundary.|oldpartition100rows;currentpartition20rows|archivemanifestcomplete;olddatarestorable;current20rowsunchanged|A reported archive success requires a demonstrated restore check.
10|Independently implement a durable telemetry work queue|Build ingestion,transactional claiming,retries,audit,timeout handling and idempotent completion in a sandbox.|100jobs;duplicatedelivery;workercrashbeforecommit;onepermanentbadpayload|validjobscompleteonce;badpayloadquarantined;crashedworkrecoverable;countsreconcile|Reviewer changes worker concurrency after the first successful run.
10|Independently build a temporal device warehouse|Implement raw JSON retention,typed readings,corrections,event/arrival times and authorized reporting.|D1lateevent;versioncorrection;D2unknownregistry;two tenants|currentandhistoricalreportsfollowstatedcontracts;unknownsvisible;isolationtested|Demonstrate a changed fixture without copying an earlier solution.
10|Independently defend telemetry operability|Deploy a bounded telemetry slice with retention,restore,role checks and measured load behavior.|generatedmillionreadings;oldpartition;consumerrole;timeoutandrestorefaultdrills|correctreports;recoveryproven;accessverified;measuredplansandlimitsdocumented|Explain observed limitations rather than claiming production readiness from a small demonstration.
''')

# Repair shorthand fixture spacing used while drafting. These are presentation
# edits, never generation of extra exercises or synthetic completion evidence.
READABILITY = {
 'currentoperationalOctober':'current operational October',
 'rowswithunmultipliedmetrics':'rows with unmultiplied metrics',
 'identicaloverlapresults':'identical overlap results',
 'plansandtimingsrecorded':'plans and timings recorded',
 'originalsnapshotreportreproduced':'original snapshot report reproduced',
 'newrevisionseparatelyidentified':'new revision separately identified',
 'allinjectedcaseshandled':'all injected cases handled',
 'ratesanddurationsreconcile':'rates and durations reconcile',
 'independentreviewfixturepasses':'independent review fixture passes',
 'percentexposedascoverageerror':'percent exposed as coverage error',
 'originalclosepreserved':'original close preserved',
 'twoexplicitadjustments':'two explicit adjustments',
 'observedprecisionbehavior':'observed precision behavior',
 'explicitnegativepolicytested':'explicit negative policy tested',
 'andbothpackagesabsentafterrollback':'and both packages absent after rollback',
 'failureleavesnobatchrows':'failure leaves no batch rows',
 'readerSELECTworksafterboth':'reader SELECT works after both',
 'timesoutwithoutpartialupdate':'times out without partial update',
 'serializationfailurecapturedandretriedboundedly':'serialization failure captured and retried boundedly',
 'valuesandforeignkeychecksmatchbeforebackup':'values and foreign-key checks match before backup',
 'rowslandinOctoberandNovemberpartitionsrespectively':'rows land in October and November partitions respectively',
 'existingrowcurrencysetbyexplicitbusinessrule':'existing row currency set by explicit business rule',
 'allfourjobsclaimedonce':'all four jobs claimed once',
 'durablequeueholdsactualwork':'durable queue holds actual work',
 'measuredelapsedandcontentionevidence':'measured elapsed and contention evidence',
 'archivemanifestcomplete':'archive manifest complete',
 'crashedworkrecoverable':'crashed work recoverable',
 'currentandhistoricalreportsfollowstatedcontracts':'current and historical reports follow stated contracts',
 'measuredplansandlimitsdocumented':'measured plans and limits documented',
 'Novemberisolated':'November isolated','badpayloadquarantined':'bad payload quarantined',
 'countsreconcile':'counts reconcile','validjobscompleteonce':'valid jobs complete once',
 'unknownsvisible':'unknowns visible','isolationtested':'isolation tested',
 'correctreports':'correct reports','recoveryproven':'recovery proven','accessverified':'access verified',
 'olddatarestorable':'old data restorable','current20rowsunchanged':'current 20 rows unchanged',
 'oneowner':'one owner','atmost2':'at most 2','nobatchrows':'no batch rows',
 'targetrows':'target rows','identicalrows':'identical rows',
 'perdevice':'per device','readerDDLdenied':'reader DDL denied',
 'statement_timeout50ms':'statement_timeout=50ms','querycancelled':'query cancelled',
 'currentandhistorical':'current and historical','currentvalue':'current value',
 'listenerreceivestxn1only':'listener receives txn1 only','eachreader':'each reader',
 'alljobscompletedonce':'all jobs completed once','no duplicateownership':'no duplicate ownership',
 'firsttwoD1allowed':'first two D1 allowed','overlappingthirdD1rejected':'overlapping third D1 rejected',
 'readeraccessworks':'reader access works','rowcount':'row count','sumunits':'sum units',
 'underSERIALIZABLE':'under SERIALIZABLE', 'finalstatement':'final statement',
 'unverifieddatabase':'unverified database','explicitreject/defaultpartitionpolicy':'explicit reject/default-partition policy',
 'stagedbackfill':'staged backfill','historicalcurrencyisinferredfrommissingdata':'historical currency is inferred from missing data',
 'nonoverlappingeffectivepriceintervals perSKU':'nonoverlapping effective price intervals per SKU',
 'Adjacentclosed-openintervalsareallowed.':'Adjacent closed-open intervals are allowed.',
 'Explainowner':'Explain owner','Generate100000events':'Generate 100000 events',
 'cursor-rangequerywith/without':'cursor-range query with/without','skewedorders':'skewed orders',
 'source-to-generated':'source-to-generated','tworowssum30':'two rows, sum 30',
 '0and2accepted':'0 and 2 accepted', 'minus1rejected':'minus 1 rejected',
 'currentview':'current view', 'as-ofjoin':'as-of join',
 'typedA10,B20':'typed A10, B20', 'Creportedunsupportedversion':'C reported unsupported version',
 'Rawpayloadremainsavailableforreprocessing.':'Raw payload remains available for reprocessing.',
 'version1and2contracts':'version 1 and 2 contracts', 'rejectunknownversions':'reject unknown versions',
 'actualnonownerconnections':'actual nonowner connections',
 'r1seesAonly;r2seesBonly':'r1 sees A only; r2 sees B only',
 'owner/superuserbypasswheninterpretingtestresults':'owner/superuser bypass when interpreting test results',
 'anappropriateindex':'an appropriate index', 'tenidenticalrows':'ten identical rows',
 'EXPLAINANALYZEplansandtimingsrecorded':'EXPLAIN ANALYZE plans and timings recorded',
 'promiseanindexscanregardlessofplannerstatistics':'promise an index scan regardless of planner statistics',
 'estimatedversusactualjoinrows':'estimated versus actual join rows',
 'final10000rows;estimated/actualevidenceperimportantnode':'final 10000 rows; estimated/actual evidence per important node',
 'Refreshingstatisticsmustnotchangequerycorrectness.':'Refreshing statistics must not change query correctness.',
 'Load the samesynthetic100000rowsrowwiseandthroughaclientbulkpath,recordingcostsandvalidation.':'Load the same synthetic 100000 rows rowwise and through a client bulk path, recording costs and validation.',
 'bothrowcount100000sumunits100000;timingandmethodrecorded':'both row count 100000, sum units 100000; timing and method recorded',
 'Includecommitcostanddonotclaimcross-machinebenchmarkgenerality.':'Include commit cost and do not claim cross-machine benchmark generality.',
 'before and aftermaintenance':'before and after maintenance',
 'disposabletable10000rowsupdated5times':'disposable table: 10000 rows updated 5 times',
 'statisticsandmaintenancecommandsrecorded;logicalvaluesunchanged':'statistics and maintenance commands recorded; logical values unchanged',
 'Statisticsareestimatesandmayneedrefresh/wait;donotfabricateexactdeadtuplenumbers.':'Statistics are estimates and may need refresh/wait; do not fabricate exact dead tuple numbers.',
 'queryplans fortenant+timefiltersagainsttwocandidateindexorders':'query plans for tenant+time filters against two candidate index orders',
 '100tenants;1000timestampspertenant;one-tenantrecentwindowquery':'100 tenants; 1000 timestamps per tenant; one-tenant recent-window query',
 'samequeryoutput;plansandindexsizesrecorded;choicejustified':'same query output; plans and index sizes recorded; choice justified',
 'Also testatime-onlyquerytorevealthechosenindexlimitation.':'Also test a time-only query to reveal the chosen index limitation.',
 'versionedcolumn/viewmigration,runconsumerchecks,andrestoreoldcontract':'versioned column/view migration, run consumer checks, and restore old contract',
 'oneoldconsumer':'one old consumer',
 'forwardandrollbackchecksreproduceA25; migrationledgeraccurate':'forward and rollback checks reproduce A25; migration ledger accurate',
 'Arollbackmustpreserverowswrittenaftertheforwardmigrationunderastatedpolicy.':'A rollback must preserve rows written after the forward migration under a stated policy.',
 'consistent logicalbackup,addaseparatepostbackupevent,restoretoafreshsandboxandcompare':'consistent logical backup, add a separate post-backup event, restore to a fresh sandbox and compare',
 'beforebackupA;afterbackupB':'before backup A; after backup B',
 'restorecontainsAandnotB;recoveryboundarydocumented':'restore contains A and not B; recovery boundary documented',
 'Do notclaimPITRfromalogicaldumpalone.':'Do not claim PITR from a logical dump alone.',
 'operationalqueryshowingrunningtransactionageandlastcommittedbatchtime':'operational query showing running transaction age and last committed batch time',
 'fakebatchledgerlastcommit12:00;clock12:30;controlledlongtransaction':'fake batch ledger: last commit 12:00; clock 12:30; controlled long transaction',
 'lag30minutes;longtransactionvisiblewithactualsessionevidence':'lag 30 minutes; long transaction visible with actual session evidence',
 "Nootheruser'ssensitivestatementtextshouldbeexported.":"No other user's sensitive statement text should be exported.",
 'Run aloadwitharolelimitedtostaging,targetandledgeroperationsneededbythecontract.':'Run a load with a role limited to staging, target and ledger operations needed by the contract.',
 'loaderrole;targetA;unrelatedprivate.table':'loader role; target A; unrelated private.table',
 'loadandledgercommitsucceed;unrelatedreadandDDLdenied':'load and ledger commit succeed; unrelated read and DDL denied',
 'Do notuseownercredentialsforthepermissionacceptancechecks.':'Do not use owner credentials for the permission acceptance checks.',
 'Detach anexpiredsandboxpartitiononlyaftercheckingrowcountsandabackupmanifest.':'Detach an expired sandbox partition only after checking row counts and a backup manifest.',
 'Septemberpartition2rows;Octoberpartition3rows;Septemberexpired':'September partition 2 rows; October partition 3 rows; September expired',
 'Septemberdetachedandrecoverable;October3rowsunchanged':'September detached and recoverable; October 3 rows unchanged',
 'Keepadefiniteverifieddatabase/schemaallowlistforthedrill.':'Keep a definite verified database/schema allowlist for the drill.',
 'Implement staging,qualitychecks,upserts,ledger,cursorandfailure recoveryinadisposableschema.':'Implement staging, quality checks, upserts, ledger, cursor and failure recovery in a disposable schema.',
 'batch1A10B20;batch2A11Cbad;failureaftertargetwritebeforecommit':'batch 1: A10 B20; batch 2: A11 Cbad; failure after target write before commit',
 'targetA11B20;Crejected;restartsunchanged;ledgercountsreconcile':'target A11 B20; C rejected; restarts unchanged; ledger counts reconcile',
 'Reviewerinjectsduplicatekeysandachangedcursorafterinitialsubmission.':'Reviewer injects duplicate keys and a changed cursor after initial submission.',
 'Designcapacity-safeprocessingofduplicateandconcurrentreservationevents.':'Design capacity-safe processing of duplicate and concurrent reservation events.',
 'capacity2;threeconcurrentuniqueeventsplusreplayofthefirst':'capacity 2; three concurrent unique events plus replay of the first',
 'atmost2activeacceptedreservations; replaydoesnotconsumecapacity':'at most 2 active accepted reservations; replay does not consume capacity',
 'Provideobservedconcurrencytestsanddefendisolation/lockingchoices.':'Provide observed concurrency tests and defend isolation/locking choices.',
 'Createcustomerhistory,facts,latecorrectionhandlingandread-onlyconsumerswitharecoverydrill.':'Create customer history, facts, late-correction handling and read-only consumers with a recovery drill.',
 'customerchangeswesttoeast;factsbefore/after;one latecorrection':'customer changes west to east; facts before/after; one late correction',
 'correct;rollback/replaydemonstrated':'correct; rollback/replay demonstrated',
 'Explainwhathistorycannotberecoveredfromavailableevidence.':'Explain what history cannot be recovered from available evidence.',
 'Implementandmeasureabulkloadplusincrementalqueryonageneratedmillion-rowfixture.':'Implement and measure a bulk load plus incremental query on a generated million-row fixture.',
 'specifiedlocalmemorybudget;skewedkeys;duplicatebatch;selectiveextract':'specified local memory budget; skewed keys; duplicate batch; selective extract',
 'correctcountsandreplay;plans,memory,timingandtradeoffevidence':'correct counts and replay; plans, memory, timing and tradeoff evidence',
 'Anunmeasuredoptimizationclaimdoesnotmeetacceptance.':'An unmeasured optimization claim does not meet acceptance.',
 'Restoreadisposablesalesmartanditsrole/viewcontractsfromknownartifactsafterinjecteddamage.':'Restore a disposable sales mart and its role/view contracts from known artifacts after injected damage.',
 'backupcontainsA,B;newerbatchCretainedinrawsource;viewandgrantremoved':'backup contains A,B; newer batch C retained in raw source; view and grant removed',
 'restoredA,B;replayedConce;readeraccessworks;reconciliationspass':'restored A,B; replayed C once; reader access works; reconciliations pass',
 'Distinguishprovenrecoverypointfromunrecoverablemissingrawdata.':'Distinguish proven recovery point from unrecoverable missing raw data.',
}

def readable(value):
    for before, after in READABILITY.items():
        value = value.replace(before, after)
    return value

def main():
    base = json.loads((ROOT / 'tools' / 'curriculum.json').read_text(encoding='utf-8-sig'))
    base_by_tool = {tool: [p for p in base['problems'] if p['tool_id'] == tool] for tool in ROWS}
    expected_targets = {'python':450, 'sql':450, 'postgresql':180}
    prefixes = {'python':'PY','sql':'SQL','postgresql':'PG'}
    docs = {
        'python':['https://docs.python.org/3/library/index.html','https://docs.python.org/3/library/csv.html'],
        'sql':['https://www.postgresql.org/docs/current/queries.html'],
        'postgresql':['https://www.postgresql.org/docs/current/tutorial.html','https://www.postgresql.org/docs/current/admin.html'],
    }
    checkpoint = {'schema_version':1,'author':'foundations','version':VERSION,
                  'status':'partial_expansion_targets_unmet','generated_at':'2026-10-26',
                  'method':'Explicit authored task contracts; no Cartesian scenario substitutions.',
                  'documentation_checked':['https://docs.python.org/3/library/csv.html',
                    'https://www.postgresql.org/docs/current/tutorial.html',
                    'https://www.postgresql.org/docs/current/queries.html'],
                  'resume':'Append distinct task contracts to foundations.py, preserving all previous rows and IDs; rerun and validate. Do not fill target gaps by copying templates.',
                  'tools':{}}
    all_ids = {p['id'] for p in base['problems']}
    for tool, entries in ROWS.items():
        seed_count = len(base_by_tool[tool])
        problems = []
        previous = f'RLP-{prefixes[tool]}-001'
        previous_level = 0
        for offset, row in enumerate(entries, seed_count+1):
            level,title,task,inputs,output,edge = [readable(x) if isinstance(x,str) else x for x in row]
            pid = f'RLP-{prefixes[tool]}-{offset:03d}'
            assert pid not in all_ids, pid
            if level == 0 and previous_level > 0:
                previous,previous_level = f'RLP-{prefixes[tool]}-001',0
            assert previous_level <= level <= previous_level+1, (pid,previous_level,level)
            kind = 'initial' if offset == seed_count+1 else 'bridge' if level > previous_level else 'transfer'
            p = {'id':pid,'tool_id':tool,'title':title,'level':level,
                 'prerequisites':[previous], 'scenario':task,
                 'task':task+' Produce the specified result and preserve the implementation plus observed evidence for review.',
                 'inputs':{'fixture_contract':inputs, 'environment':'Synthetic fixtures only; use a learner-owned disposable environment when a database is needed.'},
                 'expected_output':{'contract':output},
                 'constraints':['Use only the supplied synthetic fixture or its stated deterministic generator.',edge,
                    'Keep source inputs unchanged; use temporary sandbox resources for writes.'],
                 'acceptance_criteria':['Demonstrate this expected behavior: '+output,
                    'Demonstrate the boundary or failure check: '+edge,
                    'Submit the relevant code or SQL, observed result and assistance disclosure; an expected result alone is not execution evidence.'],
                 'estimated_minutes':10 if level==0 else min(180,15+level*12),
                 'engineering_relevance':f'{title} is a bounded responsibility in a real ingestion, transformation or warehouse operation. After review, explain where this contract fits upstream/downstream and one remaining limitation.',
                 'official_docs':docs[tool], 'verification':{'kind':'artifact_review'},
                 'topic_id':None, 'published_version':VERSION,
                 'independent_prerequisites':[], 'learning_objective':title,
                 'difficulty':f'level_{level}',
                 'progressive_hints':[
                    'Trace the smallest supplied fixture by hand and write the required output shape before changing code.',
                    'Focus on this specific boundary in your attempt: '+edge,
                    'Reduce the failing case to the smallest input, compare expected with observed behavior, then rebuild the bounded task one checked step at a time.'],
                 'challenge_kind':kind,'skill_prerequisites':[] if level==0 else [f'level_{level-1}_bounded_{tool}_tasks'],
                 'sequence':level*1000+offset,
                 'authoring_batch':'foundations-explicit-001'}
            problems.append(p)
            all_ids.add(pid)
            previous,previous_level = pid,level
        assert len({p['title'].casefold() for p in problems}) == len(problems)
        assert len({p['task'] for p in problems}) == len(problems)
        assert len({json.dumps(p['inputs'],sort_keys=True) for p in problems}) == len(problems)
        assert all(p['prerequisites'][0] in all_ids for p in problems)
        data = json.dumps(problems,indent=2,ensure_ascii=False)+'\n'
        destination = BANK / f'{tool}.json'
        if destination.exists():
            prior = json.loads(destination.read_text(encoding='utf-8'))
            incoming = {p['id']:p for p in problems}
            for saved in prior:
                if saved['id'] not in incoming or incoming[saved['id']]['title'] != saved['title']:
                    raise ValueError('Refusing ID deletion/reassignment: '+saved['id']+'. Append a new authored branch instead of inserting into published rows.')
        destination.write_text(data,encoding='utf-8')
        checkpoint['tools'][tool] = {'existing':seed_count,'new_published':len(problems),
            'actual_published':seed_count+len(problems),'target':expected_targets[tool],
            'remaining':expected_targets[tool]-seed_count-len(problems),
            'next_id':f'RLP-{prefixes[tool]}-{seed_count+len(problems)+1:03d}',
            'sha256':hashlib.sha256(data.encode()).hexdigest(),
            'levels':{str(n):sum(p['level']==n for p in problems) for n in range(11)}}
    (BANK / 'authors' / 'foundations-checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(checkpoint['tools'],indent=2))

if __name__ == '__main__':
    main()
