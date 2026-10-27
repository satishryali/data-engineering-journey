"""Explicit second author batch: append-only contracts, not a target-filling template.

Keep row order stable after publication. Each row specifies a distinct practical
operation or deliberately changed transfer contract; expected outputs are fixtures,
not claimed execution evidence or learner results.
"""
import hashlib
import json
from pathlib import Path
import re
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[3]
BANK = ROOT / 'tools' / 'problem-bank'
VERSION = '2026.10.26.2'
ROWS = {}

def author(tool, text):
    for line in text.strip().splitlines():
        if line.strip():
            level,title,task,inputs,output,edge = line.split('|')
            ROWS.setdefault(tool, []).append((int(level),title,task,inputs,output,edge))

# Connected local-file operational checks, from inspecting one path to defending
# a sandboxed repair utility. Input fixtures intentionally use no real user files.
author('python', r'''
0|Read a configured file name|An operator supplies a source filename as configuration. Return it unchanged for the run preview.|source_name='arrivals_2026-10-25.csv'|'arrivals_2026-10-25.csv'|Preview must not open,create or modify the named file.
0|Recognize a supplied file extension|A landing preview needs the last suffix of one filename, including its dot.|name='orders.backup.csv'|'.csv'|A filename without a suffix returns an empty string.
0|Read the last component of a source path|A support report needs the filename part of an explicitly supplied path, without reading the file.|path='/sandbox/landing/orders.csv'|'orders.csv'|Do not assume the current working directory supplies missing path components.
0|Inspect one file size|Create a temporary file from the supplied bytes and return its size in bytes.|file bytes=[65,66,67,10]|4|A newline byte contributes to size even though it is not a data record.
0|Tell a file from a directory|A landing checklist must label two supplied temporary paths as file or directory.|fixture has input.csv as a file and archive as a directory|input.csv:file; archive:directory|Do not decide from a dot in the name alone.
0|Read an explicit batch-size setting|A run preview receives a positive batch_size integer. Return the value without processing a batch.|configuration={batch_size:25}|25|Previewing configuration is not evidence that25records were processed.
1|Join a temporary directory and filename|Build an input path from an explicit root and basename using platform-aware path handling.|root is a temporary directory; name='orders.csv'|result refers to orders.csv directly beneath that root|Do not hard-code the original repository's Windows path.
1|Handle a final line without a newline|Count logical data lines in a small text feed including a final unterminated line.|UTF-8 text='A\nB'|2|The absence of a final newline must not discardB.
1|Skip a specified transport preamble|Read a feed with exactly two preamble lines followed by a CSV header. Return the header fields.|text='vendorX\nexport26\nid,units\nA,2\n'|['id','units']|Do not skip arbitrary additional lines that might be real data.
1|Normalize a Windows line ending|Read a small text file using universal newline behavior and return records without carriage returns.|bytes encode'A\r\nB\r\n'|['A','B']|Do not remove an embedded carriage return from a quoted data field in a CSV parser.
1|Create a report directory once|Create a nested temporary output directory and demonstrate that repeating setup succeeds.|relative directory='reports/daily' under a temporary root|directory exists after both setup calls; no duplicate sibling directory|An existing file at the same path must produce an explicit error.
1|Select a configured run mode|Accept only dry_run or apply from a supplied configuration; reject an unknown mode before any file write.|modes=['dry_run','apply','repair_everything']|first two accepted; third rejected unknown_mode|Case conversion is not automatic under this contract.
2|Reject an absolute child path|A file picker accepts a relative path beneath its configured temporary root. Reject an absolute supplied child path.|child='sub/orders.csv' then child='/outside/orders.csv'|first accepted; second rejected absolute_child|Do not let a joining operation silently replace the configured root.
2|Exclude temporary producer files|List ready CSV files while excluding producer suffixes .partial and .tmp even when.csv appears earlier.|names=['a.csv','b.csv.partial','c.csv.tmp','d.txt']|ready=['a.csv']; others ignored|The producer completion rule is explicit; file age is not proof of readiness.
2|Report file permissions separately from absence|Wrap a supplied fake reader to distinguish permission-denied from file-not-found outcomes.|fake reader returns PermissionError forA and FileNotFoundError forB|A:permission_denied;B:missing_file|Do not claim changing a path fixes a permission problem.
2|Choose a bounded file subset|Select at most two ready files in deterministic filename order and return the remaining names separately.|ready=['c.csv','a.csv','b.csv']; max_files=2|selected=['a.csv','b.csv']; remaining=['c.csv']|A negative file limit is rejected before listing or processing files.
2|Detect case-insensitive filename collisions|Before exporting for a case-insensitive consumer, report names whose case-folded values collide.|names=['Sales.csv','sales.csv','stock.csv']|collision group=['Sales.csv','sales.csv']|Do not overwrite one file merely because the development filesystem permits both.
2|Check a required output directory is empty|A one-time delivery requires an empty staging directory; list blocking entries if it is not empty.|temporary staging contains old.csv and .marker|blocked entries=['.marker','old.csv']|Hidden marker files count as entries and must not be ignored.
3|Parse a fixed-width account export|Read a record with account in positions1..5 and units in positions6..8, preserving leading account zeros.|line='00017012'|account='00017'; units=12|A record with the wrong byte length is rejected instead of sliced silently.
3|Read a tab-delimited escaped note|Parse a supplied TSV feed where a quoted note contains a tab. Return the intact note.|text='id\tnote\nA\t"first\tsecond"\n'|A note contains one embedded tab between first and second|A plain split on tab must not turn the note into an extra column.
3|Validate a supplied trailer count|A flat-file trailer declares the number of detail records. Validate it before publishing details.|lines=['H:vendor','D:A','D:B','T:2']|details A,B; declared2; observed2; pass|The header and trailer do not count as detail records.
3|Identify a UTF-8 byte-order mark|Read a supplied UTF-8-with-BOM CSV so the first header is id rather than a hidden BOM plus id.|bytes startEFBBBF then UTF-8'id,units\nA,2'|headers=['id','units']; acceptedA2|Only a recognized transport BOM is removed; field text is preserved.
3|Parse a bounded XML delivery|Read a small synthetic XML feed and return each item ID and quantity, rejecting missing required attributes.|XML '<items><item id="A" qty="2"/><item qty="3"/></items>'|acceptedA2; one missing_id rejection|Input must not allow external entity resolution or arbitrary network/file access.
3|Check a file's declared encoding|Decode using an explicit allowed encoding from the manifest and reject unknown encoding names.|bytes=[99,97,102,233]; manifest encoding='latin-1'|text='café'|Do not silently retry many encodings until one produces plausible-looking text.
4|Preserve a relative directory tree in lineage|Read two same-named files under different subdirectories and retain root-relative source paths.|north/orders.csv containsA; south/orders.csv containsB|A lineage north/orders.csv; B lineage south/orders.csv|Basenames alone are insufficient to distinguish these sources.
4|Check file-size completeness against a manifest|Compare expected byte sizes with observed temporary files before opening record parsers.|manifest a.csv4bytes,b.csv8bytes; observed a.csv4,b.csv5|a complete; b size_mismatch; delivery blocked|Matching size is only a transport check, not proof of semantic validity.
4|Protect against a symbolic-link escape|A local repair utility accepts regular files inside a root and rejects links resolving outside it.|root has safe.csv and a symbolic link pointing to an external fixture|safe accepted; external link blocked with resolved-path evidence|If symlink creation is unavailable, inject a resolver and label that test simulated.
4|Route matching header and detail files|Pair each invoice detail file with exactly one header file using a batch key in a supplied manifest.|batchB1 headerh1/detaild1; batchB2 detaild2 only|B1 ready; B2 blocked missing_header|Do not pair by directory enumeration position.
4|Compare semantic rows across file formats|Reconcile a CSV and JSON export containing the same ID/units records despite differing field order.|CSV A2,B3; JSON [{units:3,id:B},{units:2,id:A}]|no semantic differences after declared key-based comparison|Raw-byte inequality alone does not imply different business records.
4|Bound recursive directory discovery|Discover ready files no deeper than two directories below the root and report ignored deeper paths.|root/a.csv; root/x/b.csv; root/x/y/c.csv; root/x/y/z/d.csv|max_depth2 includes a,b,c; ignoresd|Define root files as depth0 and do not follow directory links.
5|Create an export with a completion marker|Publish data first, then a marker containing its digest and row count. Consumer reads only marked exports.|rowsA,B; injected failure before marker|unmarked output not consumable; success marker count2 and matching digest|A stale marker from an earlier output must not certify newly written bytes.
5|Stage a multi-file report as one release|Create accepted,rejected and manifest artifacts in a versioned temporary release directory before moving a pointer.|validA; invalidB; current releaseR0|new releaseR1 has all3artifacts; pointer changes only after checks|Failure while writing one artifact leaves pointerR0 unchanged.
5|Copy accepted source files with proof|Copy a temporary source into a sandbox archive, verify byte count and digest, then mark archived.|source bytes'ABC\n'; archive destination inside temporary root|archive bytes identical; digest/count match; status archived|Do not delete the source as part of this exercise.
5|Make a local report deterministic across machines|Produce an export using explicit UTF-8,newline policy,column order and business date.|rowsA café units2; explicit date2026-10-25|same documented output bytes independent of host newline/default encoding|Do not use the machine clock as an implicit report date.
5|Build a bounded file-inspection CLI|Accept one sandbox root and produce counts of ready,temporary and unsupported files without modifying any.|filesa.csv,b.csv.tmp,c.xml; accepted formatcsv|ready1;temporary1;unsupported1; exit0|An invalid root exits nonzero with a concise error category.
5|Attach artifact sizes to a run summary|After successful writes, report each artifact's bytes and total bytes using actual filesystem observations.|two output files containing3and5bytes|artifact sizes3,5; total8|Do not calculate size from Unicode character counts.
6|Detect a file that changes during reading|Use supplied before/after metadata and digest evidence to reject a source modified mid-read.|before size10,mtime100; after size12,mtime101|status unstable_source; no committed report|A retry reads a fresh consistent snapshot rather than appending to the partial result.
6|Handle a full output disk safely|Inject an ENOSPC-like write failure and retain a failed run record without publishing a completion marker.|new report rowsA,B; writer fails afterA|status output_full; no complete marker; prior release intact|Do not classify the failure as malformed input data.
6|Clean only this run's temporary files|After an injected failure, remove files carrying the current run's owned paths while retaining another run's files.|runR1 tempa; runR2 tempb; failR1|R1ownedtempremoved;R2tempremains|Verify every cleanup target is within the intended temporary root.
6|Make an archive retry idempotent|If the destination already has identical verified bytes, return already_archived rather than creating another copy.|sourcehashH1; destinationhashH1|already_archived; no extra archive file|An existing destination with different bytes is a collision, not a successful retry.
6|Recover a stale local completion marker|Detect when marker digest does not match its data file and block the consumer.|marker claimsH1; currentdatahashH2|blocked digest_mismatch; neither file silently rewritten|The repair action requires authoritative source bytes, not trusting the newest timestamp.
6|Report partial-copy evidence accurately|Inject copy failure after2of5bytes and distinguish copied_bytes from verified_archive_bytes.|source5bytes; copy stops after2|copied_bytes2; verified_archive_bytes0; statusfailed|A partial destination must not be counted as a completed archive.
7|Prevent two local writers racing on one release|Use an explicit single-writer claim contract and show two workers cannot publish the same release concurrently.|workersW1,W2; releaseR1; injected synchronization barrier|one publisher; other reports already_claimed; final manifest coherent|An existence check followed by an unprotected create is insufficient evidence of exclusivity.
7|Apply path length and name restrictions|Validate portable output names before writing a cross-platform bundle.|namesgood.csv,CON.csv,part:name.csv; consumerWindows contract|good allowed; reserved/colon names rejected with reasons|Do not rename files silently because the manifest references original names.
7|Separate file identity from path identity|Detect a rename of identical source bytes and record a new observed path without reloading the business delivery.|ledgerdigestH1pathold.csv; incomingdigestH1pathnew.csv|no reload; lineage recordsnew.csv as additional observation|Different bytes at the old name remain a different input version.
7|Define a stable file readiness window|Require unchanged size and mtime across two explicit polls before queueing a producer file.|poll1size10mtime1;poll2size12mtime2;poll3size12mtime2|notreadyafterpoll2;readyafterpoll3|Label this heuristic and retain final digest validation; stable metadata is not a producer transaction.
7|Check a multi-artifact consumer contract|Require data,manifest and schema versions to agree before selecting a release.|data version2; manifest version2; schema version1|releaseblocked inconsistent_contract_version|Checking filenames alone does not establish contract compatibility.
7|Resolve a local repair plan without side effects|Produce a plan of safe copies,collisions and blocked paths before an explicit apply phase.|sourceaH1->destabsent; sourcebH2->destH3; sourcec->outside_root|copya; collisionb; blockedc; no filesystem mutation|The apply phase must recheck conditions that may have changed since planning.
8|Measure directory discovery costs|Compare repeated recursive scans with a single inventory reused for several checks using an injected listing counter.|temporarytree100directories; three independent reports|identical report results; listing calls measured for both approaches|Do not replace a fresh inventory with stale data without an explicit snapshot boundary.
8|Copy a large file with bounded memory|Generate a128MiB source and copy it using bounded buffers while recording actual peak memory and digest.|128MiB deterministic byte generator; memory budget32MiB|archive digest equals source; measured peak under32MiB|Do not materialize the source bytes just to generate the test fixture.
8|Compare small-file bundling tradeoffs|Package1000small synthetic reports into a bundle and compare file-open count,size and extraction costs.|1000files each100bytes; a fixed timestamp policy|all member bytes preserved; operation counts and byte sizes recorded|A bundle is not assumed faster when consumers need only one member.
8|Calculate throughput from bytes and elapsed time|Report bytes_per_second from actual committed bytes and an injected timer; distinguish attempted bytes.|attempted1200; committed1000; elapsed2seconds|committed_throughput500bytes/sec; attempted_throughput600 separately|Zero elapsed time yields unknown throughput, not infinity or a fabricated value.
8|Avoid unbounded rejected-record retention|Stream a generated feed with one million rejected rows into a rejection artifact and keep only a bounded sample in memory.|1000000invalidrows; sample_limit5|rejected_count1000000; sample_count5; full reject artifact count1000000|A bounded sample must not be presented as the complete rejection evidence.
8|Bound parallel compression workers|Compress independent sandbox files with at most2active workers and preserve deterministic manifests.|six files; instrumented worker pool limit2|maxactive<=2; six verified outputs; deterministic manifest ordering|Worker completion order must not reorder the logical manifest unpredictably.
9|Design a filesystem preflight gate|Check root containment,available configured storage budget and writable staging before a release starts.|planned_bytes1000; allowedbudget800; valid temporaryroot|blocked storage_budget; no output artifacts created|Do not report the configured budget as a measurement of actual free disk space.
9|Maintain artifact retention with legal holds|Plan removal of expired sandbox releases while retaining held releases regardless of age.|R1expirednohold;R2expiredheld;R3recent|R1eligible;R2held;R3retained|A held release's linked raw artifacts must also remain recoverable.
9|Verify a portable restore bundle|Restore a report bundle into a different temporary directory using only relative manifest paths.|bundle withdata,schema,manifest,digests; originalabsolute_rootunavailable|restored bytes and consumer checks match; no dependency onoriginalroot|Reject absolute paths embedded in the restore manifest.
9|Record artifact provenance for incident response|Given a bad consumer output, traverse manifest links to source digest,transform version and run ID.|outputO1 linksmanifestM1;M1 sourceH1 codeV2 runR4|report identifiesH1,V2,R4 and checks linked artifacts exist|A broken link is reported as missing evidence, not filled from filename guesses.
9|Rehearse release rollback with concurrent readers|Use a versioned release pointer and instrumented readers while switchingR1toR2andback.|R1twofilesconsistentA;R2twofilesconsistentB|each reader sees one complete release; rollback returnsR1|Readers must not combine one artifact fromR1andonefromR2.
9|Specify a safe repair approval artifact|Generate a human-reviewable repair plan with exact source/destination/digest evidence and an expiry,then test stale-plan rejection.|plan expects desthashH1; beforeapplydestchangesH2|applyblocked stale_plan; no overwrite|Approval of a plan cannot authorize a different computed destination or changed bytes.
10|Independently build a safe file repair utility|Build a sandbox utility that inventories,plans,copies,verifies and reports repairs with dry-run,root containment and idempotent retries.|three goodfiles;onecollision;oneunsafe path;onepartialcopyfault|goodfilesverified;collision/unsafe blocked;retryrecoverswithoutduplicatearchives|Reviewer changes one destination after the dry-run plan to test race handling.
10|Independently create a portable report release system|Implement multi-artifact staging,completion manifests,consumer selection,rollback and restore from a different directory.|two releases; failure whilebuildingsecond; twoconcurrentreaders|no partialreleaseconsumed;oldrelease remains usable;restoredartifactsverify|Defend the limits of the chosen local filesystem atomicity assumptions.
10|Independently recover corrupted local delivery evidence|Recover a sandbox delivery from immutable raw bytes and linked manifests after a marker mismatch and missing export.|rawA2B3 verified; exportmissing; markerclaimswrongdigest|rebuild matches authoritativeinput; mismatch retained as incident evidence|Do not overwrite the bad evidence before recording the diagnostic facts.
10|Independently handle a constrained multi-file backfill|Process10000generatedsmallfiles within a measured memory/file-handle budget and produce traceable reports.|oneunstablefile,onebadencoding,oneunsafe manifest reference,rerun|acceptedresults deterministic;issues classified;rerun doesnotduplicate;limits measured|Reviewer adds a new file during discovery and expects the stated snapshot policy.
10|Independently defend a cross-platform archive migration|Move a synthetic archive between two root layouts while preservingrelativepaths,Unicode,data digests,holds and contracts.|archive hascase-collisionnames,Unicodepaths,heldrelease,onecorruptmember|safe artifacts restored; collisions and corruption blocked; held artifacts retained|Explain which platform behaviors were directly tested and which were simulated.
10|Independently engineer a bounded producer-consumer handoff|Design a local file handoff with ready-state evidence,consistent snapshots,consumer retries and cleanup ownership.|producer writespartialfile thencompletes; consumercrashes afterreading; secondrunstarts|no partialdataaccepted; replayidempotent; runownedtempscleaned; sourceevidencepreserved|Do not claim exactly-once behavior without demonstrating the target-state contract.
''')

# A connected subscription/revenue journey uses its own declared temporal and
# accounting contracts. It does not merely rename the sales seed fixtures.
author('sql', r'''
0|Read a plan's monthly price|A subscription support clerk needs the monthly price in cents of one supplied plan.|plans(plan_code,monthly_cents):('BASIC',900)|monthly_cents900|Do not convert cents to a formatted currency string in this result.
0|Keep a trial flag as a boolean|A subscriber record contains a literal boolean trial flag. Return it unchanged.|subscribers(id,is_trial):('S1',true)|is_trial=true|Booleantrue is not a date or a text label.
0|Read one billing period boundary|A billing preview needs the explicit period_start from one supplied subscription.|subscriptions(id,period_start):('S1','2026-10-01')|period_start2026-10-01|Do not substitute the query execution date.
0|Read a nullable cancellation date|Inspect a subscription that has no cancellation date and preserveNULL in the result.|subscriptions(id,cancelled_on):('S1',NULL)|S1,cancelled_onNULL|An unknown date must not be replaced by today's date.
0|Select a consumer-approved subscription key|Return public_subscription_id while excluding internal_notes from a customer-facing lookup.|subscriptions(public_subscription_id,internal_notes):('SUB7','manual-review')|public_subscription_idSUB7|No internal_notes column or content may appear in the result.
0|Inspect an empty invoice result|A new subscriber has no invoices yet. Return its invoice IDs from an empty fixture.|invoices(id,subscriber_id):empty|zero rows with an invoice id column|Do not fabricate an invoice with amount0.
1|Select active subscriptions at a date|Return subscriptions started on/before a supplied date and not cancelled on/before it.|AstartOct1cancelNULL;BstartOct1cancelOct10;CstartNov1;asofOct20|Aonly|Cancellation is exclusive of service from the cancellation date onward under this contract.
1|Find prices outside a supported range|Return plans whose monthly_cents is negative or exceeds100000.|plans A0,B900,C-1,D100001|C,D|NULL price is reported separately as missing,not forced into the range.
1|Build a human-readable invoice reference|Combine a fixed INV- prefix with a text external reference without removing zeros.|external_ref='00042'|invoice_ref='INV-00042'|The final reference is text even though its suffix contains digits.
1|Find subscriptions ending within seven days|Return end dates at least report_day and strictly earlier than report_day+7days.|reportOct20;endsOct19,Oct20,Oct26,Oct27|Oct20andOct26|The next window's first dayOct27is excluded.
1|Label paid and unpaid invoices|Classify payment_status='paid' as paid,explicit'open' as unpaid,andNULL as unknown.|invoices Apaid,Bopen,CNULL|Apaid,Bunpaid,Cunknown|An unrecognized status must produce unsupported_status,not unpaid.
1|Compare an invoice amount with a threshold|Return invoices above a supplied integer-cent approval threshold.|invoicecents A999,B1000,C1001;threshold1000|Conly|Avoid floating-point currency conversion before comparing exact cents.
2|Keep a defined whitespace cleanup boundary|Trim customer display names but preserve invoice reference text exactly.|display_name='  Asha  ';invoice_ref=' 007 '|display_name='Asha';invoice_ref=' 007 '|A cleanup rule for one field must not silently propagate to business identifiers.
2|Compare subscription counts by plan|Count subscribers per plan,including a plan with no subscribers.|plansBasic,Pro,Enterprise; subscriptionsBasicA,BasicB,ProC|Basic2,Pro1,Enterprise0|Do not count an outer-join placeholder as a subscriber.
2|Separate zero-charge and unknown-charge invoices|Count invoices with knownzero,knownpositive andNULL charges.|invoices A0,B10,CNULL,D0|zero2;positive1;unknown1|A zero invoice is a valid known value,not missing data.
2|Flag an invoice without line items|Return invoices that exist but have no detail lines.|invoicesI1,I2;linesI1L1,I1L2|I2|A line with units0still exists and must not be mistaken for no line.
2|Find plans used by every required region|Return plan codes offered in both required regionsnorthandsouth.|offersBasicnorth,Basicsouth,Pronorth;requirednorth,south|Basic|Adding a third required region changes the qualifying plans;do not hard-code the count2.
2|Detect subscribers with conflicting home countries|Return subscriber IDs associated with more than one distinctnonnull home country.|addressesAIN,AIN,BIN,BUS,CNULL|B|Repeated identical addresses do not create a conflict.
3|Allocate a prepaid amount across service days|Compute a daily integer-cent allocation for a three-day prepaid service,putting remainder on earliest dates.|total100cents;servicedaysOct1,Oct2,Oct3|Oct134,Oct233,Oct333|Daily allocations sum exactly to100and never use fractional cents.
3|Calculate bounded proration|Prorate a3000cent monthly price for10active days in an explicit30day billing period,using a stated rounding rule.|monthly3000;active_days10;period_days30|prorated1000cents|Reject active_daysgreaterthanperiod_daysinstead of silently capping.
3|Separate invoices and credit notes|Report gross invoice cents,credit cents and net cents per subscriber without treating a credit as a second sale.|documents S1invoice100,S1credit30,S1invoice50|S1gross150,credits30,net120|An unknown document kind is surfaced separately.
3|Apply a free-trial billing boundary|Bill only service dates after the trial's exclusiveendboundary.|serviceOct1..Oct5;trialendsOct4exclusive;dailyprice10|billableOct4,Oct5;total20|State whether the trial end instant itself is trial or paid time.
3|Reconcile invoice and line tax totals|Compare invoice tax control totals with summed line tax at invoice grain.|I1declaredtax12;lines5,7;I2declaredtax10;lines4,5|I1balanced;I2difference-1|Do not hide differences by rounding a summed control again.
3|Find expired discounts still being applied|Return invoice lines whose discount was applied outside its closed-open valid date interval.|discountDvalidOct1..Oct10;linesOct9discountD,Oct10discountD|Oct10lineinvalid_discount_period|The validity test uses service date,not ingestion date.
4|Match subscription plan history to invoice service dates|Attach the price effective at each line's service date,not today's plan price.|planBasic900untilOct15,1200fromOct15;linesOct14,Oct15|Oct14price900;Oct15price1200|Overlapping plan history rows must block ambiguous pricing.
4|Reconcile payment gateway and billing references|Use an explicit gateway reference mapping and report unmatched records on each side.|invoiceI1->gatewayG1;invoiceI2unmapped;gatewayG1,G9|I1matched;I2billing_only;G9gateway_only|A failed gateway payment does not count as settled money.
4|Compare original and corrected invoice lines|Report inserted,removed and amount-changed lines for the same immutable invoice revision pair.|v1 L110,L220;v2 L111,L330|L1changed10to11;L2removed;L3added30|Compare at linekeygrain,not only invoice total.
4|Combine signed account movements across sources|Combine invoice charges,payments and credits with explicit sign conventions into one account ledger.|invoice100;payment40;credit10|movements+100,-40,-10;balance50|Do not deduplicate equal-valued independent movements.
4|Attach an explicit exchange-rate version|Convert one USD invoice using the documented rate effective on service day and retain the rate ID.|USD100minorunits;rateR1=80INRperUSD;servicedayrateR1|INR8000minorunits;rate_idR1|A missing rate blocks conversion;do not use today's rate silently.
4|Build a subscriber coverage discrepancy report|Reconcile an authoritative subscriber registry with invoice coverage for a period.|registryA,B,C;invoiceA,ADuplicate,D|Acovered;B,Cmissinginvoice;Dunknownsubscriber;duplicateAidentified|A duplicate invoice does not compensate for a missing subscriber.
5|Calculate subscription expansion and contraction|Compare recurring monthly cents between two explicit snapshots at subscriber grain.|oldA100,B200,C50;newA150,B100,D80|Aexpansion50;Bcontraction100;Cchurn50;Dnew80|A missing snapshot row is meaningful only when snapshot completeness is verified.
5|Derive a monthly account balance|Return openingbalance plus periodcharges minus settledpayments and credits.|opening50;charges100;payments70;credits10|closing70|Unsettled payment attempts are excluded from settledpayments.
5|Find a subscriber's first paid invoice|Return the earliest paid invoice by paid_at and invoice_id,excluding zero-charge trial invoices.|I1zeroOct1;I2paid100Oct2;I3paid200Oct3|I2|A later refund does not retroactively make an invoice unpaid under this bounded definition.
5|Calculate overdue aging buckets|Bucket unpaid invoices by dayslate using explicit boundaries0,1..30,31..60,61plus.|asofOct31;dayslate0,1,30,31,60,61|current1;1to30count2;31to60count2;61pluscount1|A future due date belongs to not_due rather than a negative aging bucket.
5|Find customer lifetime net collections|Sum settledpayments minus actualrefunds per subscriber while excluding failedattempts.|S1settled100,failed50,refund20;S2settled40|S1net80;S2net40|Multiple status events for one payment must not count as multiple settled payments.
5|Produce a report-ready accrual schedule|Expand a prepaid contract into monthly service allocations across two explicit billing months.|contract6000cents;Oct15days,Nov15days;equal per-day allocation|Oct3000;Nov3000;total6000|Use an authoritative calendar table rather than assuming every month has30days.
6|Detect invoice version reversals|Find incoming invoice revisions older than the current authoritative revision and block overwrites.|targetI1version3cents100;incomingI1version2cents90|stale_revisionI1;targetremains100|A higher arrival timestamp does not make a lower revision authoritative.
6|Audit refund amounts exceeding settled payments|Identify payments with total acceptedrefunds greater than settledcents.|P1settled100refunds60,50;P2settled50refund20|P1excess11? no:excess10;P2valid|Rejected refund attempts are not included in accepted refund totals.
6|Identify duplicated service-date billing|Find subscriber/date/charge-kind keys billed more than once across accepted invoice versions.|AOct1baseI1,AOct1baseI2,AOct1addonI3|duplicateAOct1base;addonindependent|Do not mark legitimately different charge kinds as duplicate base billing.
6|Detect inconsistent cancellation timelines|Report a reactivation preceding its cancellation or a cancellation before initial service start.|Astart10cancel9;Bcancel20reactivate19|Ainvalid_cancellation;Binvalid_reactivation|Equal boundaries follow an explicitly stated ordering policy.
6|Explain an apparent negative overdue balance|Reconcile an invoice with overpayment and distinguish credit balance from a dataerror.|invoice100;settledpayment120|outstanding-20;classificationcustomer_credit20|Do not clamp the balance to0and discard the20cent liability.
6|Validate invoice close completeness|Block financial close if required invoice controls are missing even when observed totals reconcile.|periodexpectedbatchesB1,B2;B1balanced;B2absent|closeblocked missingB2|A partial set of balanced batches is not complete period coverage.
7|Resolve overlapping promotional eligibility|Apply only the highest-priority eligiblepromotion with deterministic ties,reporting the others as notselected.|subscriberAeligibleD1priority2,D2priority1,D3priority2;tiebydiscount_id|D1selected;D2,D3notselected|A larger monetary discount does not override the declared businesspriority.
7|Apply tiered usage pricing|Price the first100units at10cents and additionalunits at8cents without applying the cheaper rate to allunits.|usage120units|100*10+20*8=1160cents|Boundary100costs1000;usage0costs0.
7|Calculate moving collection conversion|For each cohortday,compare subscribers billed with those paying within7days,including cohorts notyetmature.|cohortOct1A,B;ApaidOct5;Bunpaid;reportOct10|Oct1eligible2,paidwithin7days1,conversion0.5|A cohort less than7daysold is labelled immature rather than scored as a finalfailure.
7|Allocate a payment across oldest invoices|Allocate150cents against invoicesI1=100dueearlier,I2=100duelater in FIFOorder.|payment150;I1dueOct1;I2dueOct2|I1allocated100;I2allocated50;unallocated0|Equal due dates require a deterministic invoice_id tiebreaker.
7|Model invoice lineage through reversals|Follow an invoice's reversal and replacement chain and identify the active unreversed document.|I1reversedbyR1;I2replacesI1;I2notreversed|activeI2;historyincludesI1,R1,I2|Detect a circular replacementreference rather than recursing indefinitely.
7|Measure net revenue retention by a fixed cohort|Compute ending recurringrevenue from the same startingcohort,excluding newly acquiredsubscribers.|startA100,B100;endA150,B0,C200new|starting200;endingcohort150;NRR0.75|NewcustomerCmust not inflate existingcohort retention.
8|Reduce invoice-line scans with bounded reuse|Compare three revenue reports that rescan the same generatedlines against a shared bounded intermediate.|100000lines;threeaggregationsbyplan,region,month|identical businessresults; scans/intermediatecosts andplansrecorded|Include intermediate materializationcost and do not assume reuse is alwaysfaster.
8|Measure distinct-count cost at the right grain|Compare counting raw paymentstatus events with first reducing to one paymentrecord under a declaredlateststatuscontract.|10000payments each10statusevents|correctsettledpaymentcountmatches; input/intermediatecardinalitiesreported|A countdistinctpaymentID alone is wrong if the lateststatusisfailed.
8|Optimize an aging report without changing boundaries|Compare candidateplans for unpaid invoices duebeforeasof while retaining allagingbucketedges.|generated100000invoices;asofdate;edgecases0,1,30,31,60,61|all edgeclassificationsidentical;actualplansandtimingsrecorded|Do not change currentunpaidstatus to historicalpaidstatus just to useanindex.
8|Quantify currency conversion rounding differences|Compare rounding perline with rounding afterinvoiceaggregation under a suppliedrate.|twolines1centUSD each;rate0.5INRperUSD;roundhalfup|perlineINR2minorunits;invoicelevelINR1minorunit|Choose the businessrequiredpolicy and retain the observed1unitdifference.
8|Inspect heavy-subscriber skew in billing joins|Profile usageevent counts before joining eachsubscriber'spricingterms.|100000events;subscriberHOT90000;others10000|hotshare0.9;distinctcounts and plan/cardinalityevidence|Do not infer balancedwork from evenly distributed subscriberreference rows.
8|Bound recursive replacement traversal|Compare a cycle-safe traversaltoadepthbudget with an unrestrictedproposal on a syntheticchain.|invoicechainlength1000;maxdepth100;onecyclefixture|chainreportsdepth_budget_exceeded;cyclefixtureterminateswithcycleevidence|A truncated chain must not be labelled fullyreconciled.
9|Publish a versioned financial metric contract|Create explicit grosscharges,netcollections andrecurringrevenue definitions with traceable sourcefilters.|invoice100;settled80;refund10;monthlyplan90|grosscharges100;netcollections70;recurring90|These are different metrics;do not label one revenue without its definition.
9|Reconcile a billing release against an approved snapshot|Compare candidatefinancialreports at subscriber,invoice,currency andperiodgrain before release.|approvedA100INR,B200INR;candidateA110INR,B190INR|overalltotalunchanged;A+10,B-10reported;releaseblocked unexplaineddifferences|A matching grandtotal does not satisfy reconciliation.
9|Maintain close and adjustment ledgers|Keep a closedmonth's amounts immutable while posting latecorrections as separatelylinkedadjustments.|Octoberclosed100;Novemberlatecredit20forOctober|Octoberclose100;linkedadjustment-20;currentoperationalnet80|An adjustment must retain originalperiod and postingperiod separately.
9|Validate a subscription model rollback|Demonstrate returning to an approvedmodel version after a failedcandidate while preservingnewsourceevents.|approvedv1;candidatev2bad;newpaymentP3arrivesduringtest|v1restored;P3retainedandreplayedonce;candidateevidenceretained|Rollback of code must not silently rollback legitimate newbusinessdata.
9|Audit a billing data retention exception|Plan removal of expired detailrows while retaining invoices under dispute or legalhold.|I1expiredordinary;I2expireddisputed;I3expiredheld;I4recent|I1eligible;I2,I3,I4retained with reasons|Aggregate retention alone is insufficient if a hold requires row-level evidence.
9|Gate an independent billing assessment|Create a fixture-driven assessment checklist requiring code,observedoutputs,assistance disclosure andchanged-inputtest.|submitted querymatchesonefixture;nochangedinputorhelpdisclosure|assessmentpending,notindependentlymastered|Completion of the checklist itself does not count as a verified learnerproblem solution.
10|Independently build a subscription revenue mart|Implement subscriberhistory,usagepricing,invoices,payments,credits andperiodreports withreconciliation.|fixtureincludesplanchange,trial,overpayment,latecreditandduplicates|declaredmetricsreconcile;issuestraceable;incrementalreplayequalsfullrebuild|Reviewer adds a tiedeffectiveprice record after firstsubmission.
10|Independently investigate a billing leakage incident|Find unbilledservice,duplicatecharges andunappliedpayments across a boundedperiod,then quantifyseparately.|Aservice10nobill;Btwobasecharges;Csettledpaymentunmapped|eachclass identified with sourcekeys;financialimpact separated;safe repairplan|Do not add different issueamounts into one lossfigure without checking overlap.
10|Independently defend a prepaid allocation engine|Build day/monthallocations with exactcents,partialperiods,cancellations andclosedperiodadjustments.|contract10001cents;servicecrossesthreemonths;midperiodcancel;latecorrection|allocationssumexactly;closedperiodpreserved;refund/adjustmentpolicytested|No workingsolution or prescribeddata structure is supplied.
10|Independently migrate billing currency contracts|Support integer-minorunit anddecimalmajorunitconsumers during a stagedmigration acrosscurrency precisions.|INR2decimal,JPY0decimal;legacytextamounts;oneambiguousprecision|exactroundtripsforvalidrecords;ambiguousrecordsblocked;bothconsumercontractstested|Do not infer currency from a numericamount's formatting.
10|Independently prove revenue report reproducibility|Rebuild a frozenfinancialreport from immutableinputs,versionedrules andcalendar metadata,then explainalaterrevision.|closedOctober;latercredit;changedpricingrule;retainedrawbatches|originalreportreproduced;newrevisiondifferencesattributedtospecificsources/rules|A similargrandtotal is not proof of reproducing the originalreport.
10|Independently tune a billing workload under correctness gates|Build andoptimize a generatedmillion-rowbillingreport while preservinggrain,decimalprecision,permissions andidempotentreplay.|skewedusage,latepayments,duplicateevents,limitedresourcebudget|verifiedequaloutputs;measuredplans/runtime;accesschecks;restartdrill|Explain a rejected optimization and the concrete contract it would violate.
''')

# Database operator progression: distinct psql, catalog, data-contract, migration,
# recovery and observability exercises beyond the first relational loader branch.
author('postgresql', r'''
0|Show NULL explicitly in a psql preview|Configure a sandbox psql result display so a SQL NULL is visibly different from an empty string.|one result row with null_value=NULL and blank_value=''|NULL is shown with an explicit chosen marker; blank remains blank|This changes display only,not stored business values.
0|Read the psql client version|Record the actual local psql client version from its version command without making a database change.|local psql client or clearly labelled unavailable-client environment|actual version output or explicit client_unavailable evidence|Client version is separate from the server version and must not be substituted for it.
0|List schemas without changing them|Use a sandbox metadata command or catalog query to list visible schemas.|sandbox has public and learner_stage schemas|both schema names visible; no schema created or deleted by inspection|Visibility depends on the connected role; record which role was used.
0|Inspect a view's output columns|Return names and data types of an existing sandbox view before querying its rows.|view report_output has id TEXT and total_cents BIGINT|columns id:text,total_cents:bigint in that order|Do not infer the view contract from one sample row's values.
0|Run one statement from a SQL file|Save a one-statement synthetic smoke script and execute it through psql in a sandbox.|script contains SELECT 7 AS smoke_value|one result smoke_value7 and successful client exit|The script must not depend on the repository's original absolute path.
0|Inspect a sequence name|List the sequence associated with a supplied identity column using supported metadata.|temporary sandbox table arrivals has a generated identity key|actual associated sequence name or supported identity metadata returned|Do not guess sequence names from naming conventions.
0|Redact a connection preview|Create a diagnostic preview of a supplied synthetic PostgreSQL connection URI,masking its password.|URI contains user learner,password dummysecret,host localhost,database lab|preview retains host/database/user and replaces password with a mask|Neither success nor error logs may include dummysecret.
0|Show statement timing in a sandbox|Enable client timing,run a scalar query and retain the observed result plus timing display.|sandbox SELECT 1|result1 and actual timing text recorded|Timing is an observation of this environment,not a general performance guarantee.
1|Comment a staging column|Add a descriptive comment to a sandbox column and retrieve it through metadata.|column raw_orders.source_row stores original physical source row number|retrieved comment explains source-row meaning|A comment does not enforce the claimed data contract; distinguish documentation from constraints.
1|Qualify an identifier containing uppercase letters|Create and query a bounded sandbox table whose exact quoted name includes uppercase letters.|table exact name "DailyFeed" with one row A|quoted query returns A; observed unquoted-name behavior documented|Do not claim quoted and unquoted identifiers are interchangeable.
1|Read a server configuration value without altering it|Inspect statement_timeout in the current sandbox session.|one PostgreSQL connection with a known session setting|actual setting and unit returned|Reading a setting must not change global server configuration.
1|Distinguish session and transaction settings|Set a local transaction setting and prove it reverts after commit.|initial statement_timeout0; inside transaction LOCAL timeout100ms|inside100ms; after commit0|Use a disposable session and do not modify server-wide defaults.
1|List only one schema's tables|Return ordinary table names in learner_stage while excluding views and other schemas.|learner_stage has table arrivals,view summary;public has table arrivals|only learner_stage.arrivals returned|A repeated name in another schema must not contaminate the inventory.
1|Check an exact stored string length|Store an identifier with a leading zero and inspect its character length and byte length.|identifier='00é' encoded UTF-8|character_length3; octet_length4|Character count and byte count serve different contracts.
1|Observe temporary table lifetime|Create a temporary sandbox table,read it,then open a second independent session.|session1 temp table contains A;session2 has no such temp table|session1 reads A;session2 cannot see session1 temporary table|Do not confuse a temporary table with a durable checkpoint store.
1|Inspect default expressions without inserting|Read a sandbox column's configured default expression through metadata.|column ingested_at defaults to current timestamp|metadata exposes the default expression; table remains empty|Inspecting a default does not evaluate or insert that value.
2|Stop a script after the first SQL error|Configure psql to return a nonzero exit and avoid later statements after a deliberate sandbox error.|script inserts A,executes invalid statement,then would insert B|script nonzero; B absent; actual state of A explained by transaction mode|Do not imply stop-on-error automatically rolls back earlier autocommitted statements.
2|Pass a text variable safely through psql|Use psql variable quoting correctly for a text value containing an apostrophe.|variable customer_name="O'Neil"; SELECT returns it as data|exact text O'Neil returned; no extra statement executed|Use a synthetic value and distinguish identifier quoting from SQL literal quoting.
2|Demonstrate rollback under explicit transaction control|Run a script containing two valid writes and one failing write inside one explicit transaction.|temporary target empty; write A; invalid write; write B|after rollback target empty; error exit retained|The lesson must preserve observed failure evidence,not hide it with a silent retry.
2|Define the meaning of a unique nullable key|Create a sandbox UNIQUE nullable column and observe duplicate NULL behavior before choosing a contract.|attempt NULL,NULL,'A','A' under default UNIQUE semantics|two NULLs accepted; repeated A rejected|If nulls must also be unique,state and test a supported alternative explicitly.
2|Add a not-valid constraint in a sandbox|Add a CHECK constraint using a supported staged-validation workflow and inspect its validation state.|existing units=-1 and2; add CHECK units>=0 NOT VALID|new negative inserts blocked; existing bad row remains until repaired; constraint not yet validated|Do not label the entire table valid before successful validation.
2|Inspect a numeric scale round trip|Store decimal text in numeric and inspect value and chosen output formatting separately.|input amount='1.200'; numeric column unrestricted precision|numeric value equals1.2; scale/format observation recorded separately|Storage formatting is not a business guarantee of original raw text preservation.
2|Distinguish timestamp types experimentally|Insert the same naive text into timestamp-without-zone and compare with an explicit zoned instant.|naive2026-10-26 10:00; zoned2026-10-26T10:00+05:30|naive retains wall time; zoned represents04:30UTC|Do not convert an unknown local timezone into a known UTC instant without a source rule.
2|Inspect function permissions|Check whether a low-privilege sandbox role can execute one harmless scalar function.|function lab_add_one(integer); test role reader|actual EXECUTE privilege outcome recorded; allowed call returns3 for2|Function permissions are distinct from direct table privileges.
3|Validate an existing constraint after repair|Repair the bounded negative-unit fixture,validate its pending check constraint,and prove its new state.|table has A=-1,B=2; explicit authorized repair sets A=0|all units nonnegative; constraint validated; A0,B2|Retain the before-image and repair statement as evidence of what changed.
3|Observe sequence gaps after rollback|Insert a row using an identity default,roll it back,then insert another row.|empty sandbox identity table; first insert rolled back|one committed row; generated key may have a gap; actual keys recorded|Do not promise gapless business invoice numbering from an ordinary sequence.
3|Reset an imported identity sequence safely|Import explicit keys into a sandbox table and align the sequence before the next generated insert.|import IDs10and20; next generated insert follows synchronization|generated ID greater than20 and no collision|Perform the adjustment in a verified disposable table,not an unrelated production sequence.
3|Export an explicit NULL representation|Create a client CSV export with a documented NULL marker and demonstrate round-trip distinction.|rows A NULL,B empty-string,C literal'NULL'|reimport preserves all three distinct values under declared export options|Do not choose a marker without checking whether literal data can equal it.
3|Store binary source evidence exactly|Store a bounded byte sequence in bytea and return its hex representation for an audit check.|bytes=[0,10,255]|hex000aff; round-trip bytes identical|Do not decode arbitrary binary bytes as UTF-8 text.
3|Use an enum's migration contract deliberately|Create a sandbox status enum,add one allowed value and demonstrate old/new insertion behavior.|initial statuses new,loaded; candidate needs quarantined|quarantined invalid before migration and valid after supported migration|Document relevant transaction/version restrictions from the actual supported server.
3|Compare collation-sensitive text ordering|Record ordering of a small Unicode fixture under explicit available collations without assuming host defaults.|stringsA,a,é,z; inspect available sandbox collations|actual order for two available explicit collations and their names recorded|If only one comparison collation is available,report the limitation rather than inventing an order.
3|Create a stable SQL validation function|Write an immutable SQL function that classifies integer units as valid,zero,negative or missing.|inputs2,0,-1,NULL|valid,zero,negative,missing respectively|Use an explicit NULL-handling contract; do not accidentally bypass missing classification.
4|Compare schemas using catalog metadata|Report added,removed and type-changed columns between two sandbox staging schemas.|v1 idTEXT,unitsINTEGER;v2 idTEXT,unitsBIGINT,currencyTEXT|addedcurrency; removednone; typechangedunits|Column order changes are reported separately from field presence/type changes.
4|Inspect dependencies before dropping a view|List downstream sandbox objects depending on a candidate view before a safe migration.|baseview v1 feeds reportview v2|dependency report names v2; unrestricted drop blocked without CASCADE|Do not use CASCADE to avoid understanding consumer impact.
4|Copy data between explicitly named schemas|Transfer a bounded validated subset from staging to target using explicit column lists.|staging A2,B-1;target empty; accept units>=0|target A2 only; B appears in rejection evidence|Do not rely on SELECT star matching target column order.
4|Compare JSON and JSONB raw-text preservation|Store one supplied JSON document in json and jsonb and compare semantic equality with textual representation.|text has deliberate spaces and key order: {"b": 2, "a": 1}|semantic values match; actual textual representations observed and explained|Do not use JSONB as proof that original source bytes were preserved.
4|Reconcile an array to a reference table|Expand a shipment's item-code array and flag codes absent from a relational item reference.|shipmentS1items[A,X,A]; referenceA|positions1and3Aknown;position2Xunknown|Repeated item codes may be meaningful positions; do not deduplicate without a rule.
4|Generate a complete date spine in PostgreSQL|Use a deterministic bounded date generator to fill a daily reporting calendar.|start2026-10-01,end2026-10-03 inclusive; observed facts onlyOct1|calendar hasOct1,Oct2,Oct3;missing fact datesOct2,Oct3|An absent fact date is labelled missing before a business rule decides whether zero is appropriate.
4|Validate cross-table row counts before a join|Inspect unique and total key counts in both sides of a proposed registry-to-fact join.|registry D1,D1,D2;facts D1,D2|registry duplicate D1 flagged; join publication blocked|A declared primary key in documentation is insufficient if the actual fixture lacks that constraint.
4|Round-trip interval-valued configuration|Store a retention interval and calculate a cutoff using a supplied timestamp.|retention='7 days';asof2026-10-26T12:00Z|cutoff2026-10-19T12:00Z|Explain that a calendar month interval is not generally a fixed30day duration.
5|Build an audit trigger with explicit grain|Create a sandbox trigger recording one audit row per changed target row and test an update affecting two rows.|target A1,B2; update increments both; audit initially empty|two target changes;two audit rows with old/new values|A no-op update follows an explicit audit policy tested separately.
5|Handle no-op upserts explicitly|Apply incoming rows only when business values differ and return inserted/changed/unchanged counts.|target A10,B20;stage A10,B21,C30|inserted1,changed1,unchanged1; target A10,B21,C30|Do not use physical transaction metadata as an undocumented business change contract.
5|Return a structured validation result|Create a SQL function returning accepted flag and reason rather than swallowing data errors.|units input2,-1,NULL|2trueNULL;-1false negative;NULLfalse missing|Unexpected internal errors must remain distinguishable from normal invalid rows.
5|Use a parameterized server cursor for extraction|Read a bounded sandbox query in chunks through a suitable database client and record fetch sizes.|10orderedrows; fetchsize3|chunks3,3,3,1;all10rows once in order|Demonstrate the cursor/transaction lifetime and close resources after failure.
5|Refresh a materialized report under reader load|Test a supported refresh strategy with two sandbox sessions and document reader behavior.|materialized summary10;new base row5; concurrent reader|eventual summary15; observed blocking/availability documented|If concurrent refresh is chosen,meet and test its required unique-index conditions.
5|Build a bounded database health query|Return connection identity,server time,last successful batch and failure count from a supplied ledger.|ledger successR1at12:00,failedR2at12:10; suppliedasof12:20|last_success12:00; failures1; actual connection identity reported|Server reachability alone is not proof that data delivery is healthy.
5|Validate a migration before marking it applied|Run a sandbox migration followed by schema and smoke checks before adding its applied ledger row.|migration adds requiredcolumn; injected validation failure|failed validation leaves no applied ledger row and no partially accepted migration|An executed DDL statement is not automatically a successful application release.
5|Record source-to-target key mapping atomically|Insert new natural keys,obtain generated IDs and write mapping entries in one transaction.|sourcecodesV1,V2; empty target and mapping; injected mapping failure|failure leaves no committed target/mapping pairs; success yields two consistent mappings|Do not reconstruct mappings from row insertion order or guessed ID ranges.
6|Reproduce and classify a deadlock|Use two disposable sessions locking two rows in opposite order,record the deadlock victim and retry policy.|rowsA,B;session1locksAthenB;session2locksBthenA|one transaction receives deadlock error; surviving state consistent; bounded retry demonstrated|Use controlled synchronization and short timeouts,not uncontrolled blocking sleeps.
6|Cancel a long sandbox query|Start a controlled expensive statement,identify its own backend,and cancel only that sandbox statement.|one known sandbox backend running a bounded slow query|query cancelled; connection recoverable after needed transaction cleanup|Verify backend/database/user identity before invoking cancellation.
6|Distinguish cancelled from terminated sessions|Compare query cancellation with terminating a separate owned sandbox session.|two disposable sessions with recorded backend IDs|cancel leaves connection recoverable; terminate closes that specific session|Never target sessions belonging to other users or databases.
6|Recover a failed concurrent index build|Inject or reproduce a bounded failed index-build attempt and inspect validity before cleanup/retry.|sandbox table; candidate index with deliberate conflicting prerequisite|invalid/unusable artifact detected if created; safe retry yields valid index|Do not assume an index name in the catalog means the index is valid or being used.
6|Avoid blocking when a work row is already locked|Attempt to claim a locked sandbox work row using a no-wait contract and classify the outcome.|session1locksjob1;session2requestsjob1withNOWAIT|session2 gets bounded lock-unavailable outcome; no duplicate claim|Do not treat lock contention as malformed business data.
6|Make retry backoff external to database locks|Demonstrate releasing a failed transaction before an injected retry delay.|first attempt transient conflict; fake clock delay2seconds; retry succeeds|rollback before delay; no open lock-holding transaction during delay|Use an injected clock for tests and record actual ordering evidence.
6|Find a transaction left idle after a client failure|Create a disposable idle-in-transaction session,identify it through metadata,and clean it up.|owned session begins transaction then stops issuing statements|own backend reported idle-in-transaction; rollback/close removes it|Do not terminate unrelated idle sessions to make the diagnostic pass.
6|Handle an unavailable extension honestly|Attempt a supported capability check for a nonessential extension and choose the explicit fallback path.|sandbox role cannot install extension; fixture has a pureSQL validation fallback|status extension_unavailable; fallback results correct; no elevated grant requested|Do not label the extension-backed implementation tested when only the fallback ran.
7|Enforce a deferred consistency boundary|Use a supported deferrable constraint so a valid multi-row transaction can finish while invalid finalstate fails.|two related rows updated temporarily outofsync but valid atcommit; secondcase invalidatcommit|validcasecommits;invalidcaserollsback|Deferred checks move timing,not the requirement for a consistent committed state.
7|Move ownership without losing consumer access|Transfer a bounded schema object's ownership under an explicit deployment-role policy and recheck access.|ownerold->ownernew;readerSELECTprivilege;oneview|newownercorrect;readerstillworks;unrelatedrolesunchanged|Test default privileges for newly created future objects separately from existing grants.
7|Separate security-definer function risks|Create a harmless sandbox security-definer function with a fixed safe search_path and test a shadow-object attack fixture.|trusted function reads trusted.table; caller creates same-name untrusted table|function reads trusted object only; caller cannot redirect it|Keep function privileges narrow and do not use superuser ownership as a shortcut.
7|Model a point-in-time configuration lookup|Store versioned pipeline configuration and resolve one version at an explicit run timestamp.|configC1valid1..10;C2valid10..open;runat10|run bindsC2 and stores that version ID|A later configuration edit must not silently change an already-bound historical run.
7|Handle a renamed enum value as a compatibility change|Migrate a status label while supporting a documented old consumer representation during overlap.|stored statusloaded;new labelcommitted;oldconsumerexpectsloaded|new storage/view contract committed;compatibilityview returnsloaded; tests explicit|Do not assume renaming a stored label is transparent to clients comparing text.
7|Build an exclusion report before enforcing a constraint|Find overlapping resource intervals and ambiguous NULL resources before deploying a strict constraint.|R1[1,5),R1[4,7),R2[1,5),NULL[2,3)|R1overlap flagged;NULLresource separatelyclassified;R2clean|Do not delete conflicting history merely to make the new constraint install successfully.
7|Control a cross-database import boundary|Transfer a small exported fixture between two owned disposable databases with manifest/schema checks.|sourceexport id,units;target requires idTEXT,unitsINTEGER|two validrows imported; manifest matches; no implicit crossdatabasejoin claimed|Use client export/import or an explicitly available capability; disclose which path was tested.
7|Validate a compatibility view during table replacement|Replace a sandbox physical table behind a stable consumer view while preserving permissions and column contracts.|oldtableA10;newtableA10B20;viewid,cents;readerrole|reader sees expected contract and new rows after switch; rollback tested|Dependency replacement must be explicit; do not rely on object names alone.
8|Measure partial index usefulness|Compare plans and index sizes for a frequently queried pending subset versus a full index.|100000jobs;100pending;querypendingorderedbyid|identical100pendingrows;actualplans,sizeandtimingrecorded|Also test a nonpendingquery to show the partial index's scope limitation.
8|Measure a covering index tradeoff|Compare a bounded lookup before/after an index including required payload columns.|generatedorders100000;filtercustomeranddate;returncents|same result;plan and indexsize/writecost observations recorded|Do not claim index-only access without inspecting actual execution evidence.
8|Measure expression index contract matching|Compare a normalized-email lookup with a supported expression index under an explicit casefoldrule.|syntheticaccounts100000;querylower(email)=knownvalue|same matchingkeys;plans/timingsreported;expressiondefinitiondocumented|Do not alter the identity rule for Unicode emails merely to improve a query plan.
8|Assess extended statistics on correlated columns|Build a correlated warehouse/region fixture and compare estimates before/after supported statistics.|region stronglydetermineswarehouse; boundedtwocolumnfilter|actualresultunchanged;estimatechangesandstatisticsdefinitionrecorded|Improved estimates are not automatically a measured runtime improvement.
8|Estimate an index's write amplification|Load the same generatedfixture into sandbox tables with0,1and3indexes and record elapsedtime/storage.|100000rows withidenticalconstraints;threeindexconfigurations|correctrowcounts;actualwriteelapsedandstoragemetricscompared|Separate integrityconstraints from optionalperformanceindexes in the interpretation.
8|Measure sorting under an explicit memory budget|Compare a bounded sort plan under two session-localwork_mem values,recording spill evidence.|generated100000wide rows;sorton declaredkeys;two memorybudgets|same deterministicorder;actualsortmethod/tempI/O/timingobserved|work_mem is peroperation behavior,not a global total-memory guarantee.
8|Compare join strategies without forcing a conclusion|Inspect two valid relational formulations on a bounded fixture and compare actual plans,including skew.|10000parents;100000children;selectiverange|identicalrows;actualjoinplans/cardinality/timingsreported|Do not claim one join algorithm is universally superior from one fixture.
8|Benchmark a filtered aggregate against repeated scans|Compute several conditional run metrics in one boundedquery and compare with repeatedqueries.|100000runrows withsuccess,failed,cancelled statuses|metricvaluesidentical;querycount/plans/elapsedrecorded|Maintain the exact same cancelled-run denominator policy in both versions.
9|Package a database migration smoke suite|Provide a local command validating schema,permissions,representativerows androllback metadata afterdeployment.|sandboxmigration addsnewreportview;testsreaderroleandoneknownrow|one command returnsnonzeroonanyfailedcheck;successfulrunrecordsallchecks|Tests must execute against a disposable database identified in their output.
9|Document a recovery privilege boundary|Test which restore operations a dedicated sandboxrestorer can perform without superuserrights.|ownedtargetschema;restorerrole;sampledumpwithtablesanddata|supportedrestoreworks;unsupportedownership/grantstepsreportedexplicitly|Do not solve a failedrestore by granting blanket administrativeprivileges.
9|Reconcile catalog and migration ledger drift|Compare expectedtables/columns/indexes from a versionedmanifest with actualsandboxmetadata.|ledger saysv2;actualmissingindexandextraoptionalcolumn|missingindex andextracolumnreported;v2notassumedhealthy|Distinguish intentionalcompatibleextras from release-blocking omissions.
9|Prove rollback of a permissions migration|Apply a boundedgrantchange,verifyreaderbehavior,thenrestoretheapprovedprivilegecontract.|reader initiallySELECTviewonly;candidate accidentallyallowsbasetablewrite|candidatecheckfails;rollbackremoveswrite;originalreadstillworks|Record privilege evidence under the affectedrole,not only catalog assertions.
9|Test connection pool session-state hygiene|Using an available client or explicitfakepool,reuseconnections across two borrowers and reset sessionstate.|borrower1setssearch_path;borrower2expectsdefault|borrower2 doesnotinheritunexpectedpath;resetmechanismevident|Label fakepool tests as simulated and do not claim a specific pool library was integration-tested.
9|Choose a durable backup validation checklist|Execute a sandbox logicalbackupandrestore with object,data,sequence androle/viewchecks.|two relatedtables,identitysequence,consumer view and readergrant|restoreddata,relationships,nextgeneratedIDandconsumerchecks pass|A dumpfile's existence or byte size alone does not prove recoverability.
9|Establish a measured database service budget|Record a boundedload's querylatency,connections,tempstorage and committedthroughput against suppliedlimits.|generatedworkload;maxconnections4;tempbudget64MiB;latencytarget supplied|actualmeasurements andeachpass/failreported;unmeasureditems labelledunknown|Do not transform a benchmark result into an employment or production-readiness guarantee.
9|Audit sensitive metadata in operational exports|Produce a sanitized operationalsnapshot excluding querytext,connectionsecrets and rawpersonaldata.|sessionmetadata includesquerywithsyntheticemail;allowedfields pid,state,duration|exportcontainsallowedfieldsonly;email/secretsabsent|Check exception anddebuglogs as well as the intendedexportfile.
10|Independently build a migration verification tool|Implement a sandboxcataloginventory,versionedcontractcomparison,permissionchecks andnonzerofailureexit.|candidate hasmissingconstraint,wrongviewtype,overbroadgrant;baselinevalid|eachfaultdetected;baselinepasses;restoredmigrationrechecked|Reviewer adds anunexpectedcompatiblecolumn and expects the stated driftpolicy.
10|Independently recover a database after a failed deployment|Restore anapprovedschema/view/rolecontract while retaining validnewsourceevents andaccurate migrationhistory.|v1valid;v2failsmidmigration;newbatcharrives;backupavailable|v1consumerworks;newbatchreplayedonce;failedv2evidenceretained|Explain exactly which state came frombackup,rawreplay andmanualapprovedrepair.
10|Independently defend a safe concurrent loader|Implement transactionboundaries,deadlock/serializationretries,claimownership,audit andresourcebudgets.|two concurrentworkers;duplicatebatch;injecteddeadlock;malformedrecord|validtargetexactlymatchescleanreference;badrowtraceable;boundedretry/connections|Demonstrate observed concurrency,not only sequential unit tests.
10|Independently operate a typed and raw JSON warehouse|Retain rawbytes,validateJSONcontracts,maintaintypedprojections,applycorrections andevolveaconsumerview.|multipleversions;duplicateJSONproperties;unknownfields;latecorrection|rawauditintact;ambiguousrecordsblocked;typedreportsreplayable;consumercompatibilitychecked|Defend why each normalization is permitted by the actual producercontract.
10|Independently prove least-privilege recoverability|Deploy,load,report,back up andrestore a boundedmart using separatedsandboxroles.|owner,loader,reader,restorer;twotables,oneview,batchledger|eachrole canperformonlyintendedoperations;restoreverified;denialsrecorded|A successfulowner/superuserrun doesnot meet the role-isolation acceptancecriteria.
10|Independently optimize a constrained PostgreSQL mart|Tune a generatedmillion-rowwarehousequery while preserving exactmetrics,replay,permissions andlate-eventhandling.|skewedkeys;correlatedcolumns;memorybudget;requiredconsumercontracts|equaloutputs;measuredplans/resources;tradeoffsdefended;noinvariantregressions|Reviewer changes one selectivefilter to expose overly specialized assumptions.
10|Independently rehearse a data-platform incident runbook|Diagnose and recover controlledlockcontention,staleledger,invalidindex andmissinggrant faults.|fourdisposablefaultfixtures;knownhealthyreference|eachfaultclassified;boundedrecovery;healthchecksanddatareconciliationpass|Do not silently repair unrelatedobjects or discardfailureevidence.
10|Independently design a reproducible local warehouse assessment|Create andsolve an originalboundedwarehousecase with explicitfixtures,contracts,faultinjection andchanged-inputreview.|providedbusinessbrief includescustomers,events,latecorrections,privacyandrecovery|workingimplementation;observedchecks;assistancehistory;independentchangedinputevidence|Designing the assessment doesnot itself demonstrate the learner's independent solution.
''')

EXTRA_WORDS = '''
sandbox catalog inventory versioned contract comparison permission checks and nonzero failure exit
fixture fixtures approved compatible incompatible compatibility baseline unexpected omissions
source sources target targets bytes byte count counts checksum digest metadata field fields
elapsed committed throughput input output disk budget root temporary path paths current previous
concurrent readers workers work worker no unsafe ambiguous safely repair repairs corrupt corruption
partially partial complete completeness altered unchanged changed changes during still then only
late event events single multiple wrong missing schema schemas object objects columns column
query queries measured plans runtime integer decimal precision permissions permission exact metrics
replay idempotent retry retries restart run rollback recovery recoverable restored restore original
archive archived verified invalid valid good bad accepted rejected report reports result results
manifest manifests consumer consumers publisher producer producercontract business rule rules policy
cleanup owned hold held retention relative absolute external contained containment protected
logical physical reference authoritative observations observation newest old stale linked provenance
after before between below above each per more less than at most zero one two three four five six
received sent start end unknown present absent deployed deployment migration migrations health healthy
units cents quantity generated sourcebytes filefiles some supported unsupported index invalidindex
credit credits invoice invoices subscriptions subscriber subscribers old new recurring revenue gross
collections collection payments payment settled failed attempted attempts refund refunds version versions
closed period financial reproducible reproducibility different difference differences business days dates
highest priority ties tie grant grants denied denial denials isolation constraint constraints enum value
least privilege role roles restorer loader reader owner superuser runbook cleanup smoke environment
details null empty numeric boolean zoned naive text effective ends inclusive exclusive month monthly
statement statementtime prepared connection connections pool fake fakepool reset resource resources limits
record recorded records evidence related unrelated insert inserted update updated delete deleted ledger
run runs history repair plan planned observed tested test tests true false lower upper local performance
identical same rate rates cases case shape roundtrip roundtrips storage tempfile temporaryfile handles
body bytes committedthroughput exactmetrics million row rows unbounded bounded sequence identity next
transient permanent retrybudget contention waiting lock locking locks locksafety deadlock serialization
classification classificationerror code codes timeline process processed request requests require required
columnorder identifiers identifier stored table tables view views name names raw typed typedprojections
boundaries bound boundary size sizes total totals aggregate aggregation aggregates formulas calculation
fractional minorunit minorunits majorunit majorunits serviceday service serviceperiod migrationhistory
unexpected compatible released release releases consumercontract consumercontracts simulated labelled
explicit explicitly optional mandatory inputdata businessdata lateevent lateevents midperiod cancelled
crosses three months frozen closes close originalreport ownedtargetschema secret secrets sensitive sanitize
public private sanitized operations operation allowed allowable privilegecontract denialsrecorded
task assessment assessed candidate changes defects defects faults fault failures error errors exception
matched matching match equal sums sum reporting sourcekeys sourcefilter sourcefilters restorable library
buffer buffers materialization overhead percentile median mean sampled sample samplelimit newline
uncompressed compressed compression compress decoding encoding Unicode Unicodepaths corruptmember
opening closing balance overdue balances outstanding liability open positive negative constraints
fully reconciled line linekey grain account accounts delay fakeclock snapshots snapshot authoritativeinput
validrows imported setup available unavailable flags statements querytext ownership objecttypes owners
preparedstatement preparedstatements restorefile dumpfile logicalbackup backup backups recoverypoint
default exactamount regular transport aware until timezone zones metadata columns datatypes types type
duration durations minute minutes seconds allocated allocation FIFO oldest newer latest supports sourcekeys
compare comparable comparison comparablemetric independently independentlymastered demonstrates demonstrated
invariant invariants regressions optimization optimize selective nonselective filter filters handling
workload skew skewed correlated rows cardinality estimates estimate querycount cardinalities denominator
individual independently readerrole testrole healthyreference sourceevents eventhandling datareconciliation
nonowner actual timing measuredelapsed temporarystorage throughput legitimate acceptedrefunds
'''.split()

def vocabulary():
    words = {w.lower() for w in EXTRA_WORDS}
    base = json.loads((ROOT/'tools/curriculum.json').read_text(encoding='utf-8-sig'))
    for p in base['problems']:
        for value in (p['title'],p['scenario'],p['task']):
            words.update(w.lower() for w in re.findall(r'[A-Za-z]{2,18}', value))
    # Previously reviewed prose and the newly authored natural-language titles
    # supply spelling, not new content. Do not learn the compressed fixture text.
    for tool in ROWS:
        for p in json.loads((BANK/f'{tool}.json').read_text(encoding='utf-8')):
            words.update(w.lower() for w in re.findall(r'\b[A-Za-z]{2,18}\b',p['scenario']))
        for row in ROWS[tool]:
            words.update(w.lower() for w in re.findall(r'\b[A-Za-z]{2,18}\b',row[1]))
    return words

def make_readable(words):
    corrections={
        'retryrecoverswithoutduplicatearchives':'retry recovers without duplicate archives',
        'partialreleaseconsumed':'partial release consumed','authoritativeinput':'authoritative input',
        'generatedsmallfiles':'generated small files','runownedtempscleaned':'run-owned temps cleaned',
        'sourceevidencepreserved':'source evidence preserved','regionsnorthandsouth':'regions north and south',
        'daysgreaterthanperiod':'days greater than period','Dunknownsubscriber':'D unknown subscriber',
        'duplicateAidentified':'duplicate A identified','classificationcustomer':'classification customer',
        'acquiredsubscribers':'acquired subscribers','correctsettledpaymentcountmatches':'correct settled payment count matches',
        'allagingbucketedges':'all aging bucket edges','edgeclassificationsidentical':'edge classifications identical',
        'actualplansandtimingsrecorded':'actual plans and timings recorded','historicalpaidstatus':'historical paid status',
        'traversaltoadepthbudget':'traversal to a depth budget','unrestrictedproposal':'unrestricted proposal',
        'cyclefixtureterminateswithcycleevidence':'cycle fixture terminates with cycle evidence',
        'unexplaineddifferences':'unexplained differences','currentoperationalnet':'current operational net',
        'retainedandreplayedonce':'retained and replayed once','independentlymastered':'independently mastered',
        'incrementalreplayequalsfullrebuild':'incremental replay equals full rebuild',
        'andunappliedpayments':'and unapplied payments','allocationssumexactly':'allocations sum exactly',
        'closedperiodpreserved':'closed period preserved','explainalaterrevision':'explain a later revision',
        'newrevisiondifferencesattributedtospecificsources':'new revision differences attributed to specific sources',
        'invalidcaserollsback':'invalid case rolls back','expressiondefinitiondocumented':'expression definition documented',
        'estimatechangesandstatisticsdefinitionrecorded':'estimate changes and statistics definition recorded',
        'actualwriteelapsedandstoragemetricscompared':'actual write elapsed and storage metrics compared',
        'integrityconstraints':'integrity constraints','optionalperformanceindexes':'optional performance indexes',
        'representativerows':'representative rows','supportedrestoreworks':'supported restore works',
        'grantstepsreportedexplicitly':'grant steps reported explicitly','administrativeprivileges':'administrative privileges',
        'intentionalcompatibleextras':'intentional compatible extras','rollbackremoveswrite':'rollback removes write',
        'originalreadstillworks':'original read still works','doesnotinheritunexpectedpath':'does not inherit unexpected path',
        'resetmechanismevident':'reset mechanism evident','committedthroughput':'committed throughput',
        'actualmeasurements':'actual measurements','newbatchreplayedonce':'new batch replayed once',
        'andmanualapprovedrepair':'and manually approved repair','andresourcebudgets':'and resource budgets',
        'validtargetexactlymatchescleanreference':'valid target exactly matches clean reference',
        'andevolveaconsumerview':'and evolve a consumer view','separatedsandboxroles':'separated sandbox roles',
        'acceptancecriteria':'acceptance criteria','datareconciliation':'data reconciliation',
        'discardfailureevidence':'discard failure evidence','workingimplementation':'working implementation',
        'acceptedrefunds':'accepted refunds','additionalunits':'additional units','assistancehistory':'assistance history',
        'badrowtraceable':'bad row traceable','baselinepasses':'baseline passes','consumercontracts':'consumer contracts',
        'consumerworks':'consumer works','correctrowcounts':'correct row counts','denialsrecorded':'denials recorded',
        'duebeforeasof':'due before asof','duplicatecharges':'duplicate charges','eachfaultdetected':'each fault detected',
        'eligiblepromotion':'eligible promotion','eventhandling':'event handling','evidenceretained':'evidence retained',
        'expectedtables':'expected tables','faultinjection':'fault injection','firstsubmission':'first submission',
        'historicalpaidstatus':'historical paid status','historyincludes':'history includes',
        'issuestraceable':'issues traceable','learnerproblem':'learner problem','logicalbackup':'logical backup',
        'migrationhistory':'migration history','monthallocations':'month allocations','netcollections':'net collections',
        'newownercorrect':'new owner correct','notassumedhealthy':'not assumed healthy','ownedtempremoved':'owned temp removed',
        'partialperiods':'partial periods','periodcharges':'period charges','postingperiod':'posting period',
        'prescribeddata':'prescribed data','privilegecontract':'privilege contract','producercontract':'producer contract',
        'rawauditintact':'raw audit intact','rawpersonaldata':'raw personal data','readerstillworks':'reader still works',
        'similargrandtotal':'similar grand total','sourcefilters':'source filters','specificsources':'specific sources',
        'superuserrights':'superuser rights','syntheticchain':'synthetic chain','targetremains':'target remains',
        'timingsreported':'timings reported','tradeoffsdefended':'tradeoffs defended','typedprojections':'typed projections',
        'unbilledservice':'unbilled service','unitdifference':'unit difference','unmeasureditems':'unmeasured items',
        'workingsolution':'working solution','chainreportsdepth':'chain reports depth','NewcustomerCmust':'New customer C must',
        'Cmissinginvoice':'C missing invoice','actualsortmethod':'actual sort method',
    }
    @lru_cache(None)
    def segment(token):
        lower = token.lower()
        if lower in words:
            return token
        @lru_cache(None)
        def parts(start):
            if start == len(token):
                return []
            best = None
            for end in range(start+2,len(token)+1):
                if lower[start:end] in words:
                    rest = parts(end)
                    if rest is not None:
                        candidate = [token[start:end]]+rest
                        if best is None or len(candidate)<len(best): best=candidate
            return best
        result=parts(0)
        return ' '.join(result) if result is not None else token
    def readable(text):
        # A fixture often uses A10 or Oct1 as compact notation. Keep those
        # identifiers intact; split only recognized concatenated prose words.
        for before,after in sorted(corrections.items(),key=lambda pair:-len(pair[0])):
            text=text.replace(before,after)
        text = re.sub(r'\b[A-Za-z]{7,}\b',lambda m:segment(m.group()),text)
        text = text.replace('P1excess11? no:excess10','P1 excess10')
        return text
    return readable

def main():
    base=json.loads((ROOT/'tools/curriculum.json').read_text(encoding='utf-8-sig'))
    known={p['id']:p for p in base['problems']}
    starts={}
    previous_content={}
    for tool in ROWS:
        previous_content[tool]=(BANK/f'{tool}.json').read_bytes()
        for p in json.loads(previous_content[tool]): known[p['id']]=p
        starts[tool]=max(int(p['id'].rsplit('-',1)[1]) for p in known.values() if p['tool_id']==tool)+1
    readable=make_readable(vocabulary())
    prefixes={'python':'PY','sql':'SQL','postgresql':'PG'}
    targets={'python':450,'sql':450,'postgresql':180}
    docs={'python':['https://docs.python.org/3/library/pathlib.html','https://docs.python.org/3/library/io.html'],
          'sql':['https://www.postgresql.org/docs/current/queries.html','https://www.postgresql.org/docs/current/functions.html'],
          'postgresql':['https://www.postgresql.org/docs/current/app-psql.html','https://www.postgresql.org/docs/current/admin.html']}
    checkpoint={'schema_version':1,'version':VERSION,'author':'foundations-batch2',
                'status':'partial_expansion_targets_unmet','tools':{},
                'method':'Explicit distinct task contracts; deterministic prose spacing does not create new problems.',
                'resume':'Append new explicit task rows preserving existing row order and IDs; never substitute planned counts for published arrays.'}
    for tool,rows in ROWS.items():
        previous=f'RLP-{prefixes[tool]}-001'
        previous_level=0
        problems=[]
        for index,row in enumerate(rows,starts[tool]):
            level,title,task,inputs,output,edge=[readable(x) if isinstance(x,str) else x for x in row]
            pid=f'RLP-{prefixes[tool]}-{index:03d}'
            if level==0 and previous_level>0:previous,previous_level=f'RLP-{prefixes[tool]}-001',0
            assert pid not in known,pid
            assert previous in known,previous
            assert previous_level<=level<=previous_level+1,(pid,level,previous_level)
            p={'id':pid,'tool_id':tool,'title':title,'level':level,'prerequisites':[previous],
               'scenario':task,'task':task+' Keep the implementation and observed result for review.',
               'inputs':{'fixture_contract':inputs,'environment':'Synthetic data in a learner-owned disposable sandbox only.'},
               'expected_output':{'contract':output},
               'constraints':[edge,'Keep original input evidence; perform writes only in verified temporary/sandbox resources.'],
               'acceptance_criteria':['Observe this output/behavior: '+output,
                    'Demonstrate this specific boundary/failure check: '+edge,
                    'Submit code/configuration,observed checks and assistance disclosure; expected output alone is not proof of execution.'],
               'estimated_minutes':10 if level==0 else min(180,15+level*12),
               'engineering_relevance':f'{title} is one bounded operational responsibility in a real data platform. After review, connect its output contract to a producer/consumer and identify one remaining limitation.',
               'official_docs':docs[tool],'verification':{'kind':'artifact_review'},
               'topic_id':None,'published_version':VERSION,'independent_prerequisites':[],
               'learning_objective':title,'difficulty':f'level_{level}',
               'progressive_hints':['Trace the smallest supplied fixture and identify exactly which observable behavior must change.',
                    'Check this contract boundary in your attempt: '+edge,
                    'Isolate one failing case,compare expected with observed behavior,and rebuild the bounded task one checked step at a time.'],
               'challenge_kind':'bridge' if level>previous_level else 'initial' if level==0 else 'transfer',
               'skill_prerequisites':[] if level==0 else [f'level_{level-1}_bounded_{tool}_operations'],
               'sequence':level*1000+index,'authoring_batch':'foundations-explicit-002'}
            problems.append(p)
            known[pid]=p
            previous,previous_level=pid,level
        assert len({p['title'].casefold() for p in problems})==len(problems)
        assert len({p['task'] for p in problems})==len(problems)
        destination=BANK/f'{tool}-batch2.json'
        if destination.exists():
            old=json.loads(destination.read_text(encoding='utf-8'))
            assert problems[:len(old)]==old,'Published batch content changed; preserve old rows/IDs.'
        content=json.dumps(problems,indent=2,ensure_ascii=False)+'\n'
        destination.write_text(content,encoding='utf-8')
        total=starts[tool]-1+len(problems)
        checkpoint['tools'][tool]={'previous_published':starts[tool]-1,'new_published':len(problems),
            'actual_published':total,'target':targets[tool],'remaining':targets[tool]-total,
            'next_id':f'RLP-{prefixes[tool]}-{total+1:03d}',
            'sha256':hashlib.sha256(content.encode()).hexdigest(),
            'levels':{str(level):sum(p['level']==level for p in problems) for level in range(11)}}
        assert (BANK/f'{tool}.json').read_bytes()==previous_content[tool],'Earlier batch changed.'
    (BANK/'authors/foundations-batch2-checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(checkpoint['tools'],indent=2))

if __name__=='__main__':main()
