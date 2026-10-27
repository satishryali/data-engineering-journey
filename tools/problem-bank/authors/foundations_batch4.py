"""Fourth append-only batch: testing Python ETL and parsing SQL source contracts.

All fixture contracts are explicitly authored. This script writes only new
unregistered batch4 files and preserves IDs on deterministic reruns.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from functools import lru_cache

ROOT=Path(__file__).resolve().parents[3]
BANK=ROOT/'tools/problem-bank'
ROWS={}

def author(tool,text):
    for row in text.strip().splitlines():
        if row.strip():
            level,title,task,fixture,expected,boundary=row.split('|')
            ROWS.setdefault(tool,[]).append((int(level),title,task,fixture,expected,boundary))

author('python',r'''
0|Check one observed transformation result|A pipeline reviewer needs one executable check that a supplied pure transformation produced the expected integer result.|Supplied transform returns6 for input units2,unit_cents3.|One passing executable check compares observed6 with expected6.|Writing the expected number in a comment is not an executed check.
0|Make a deliberately failing smoke check visible|Demonstrate how a local smoke check exposes an incorrect output before it reaches a consumer.|Supplied faulty transform returns5 where the contract requires6.|Check fails with expected6 and observed5 visible; local test command exits nonzero.|Preserve the failed result; do not change the expected value merely to make the test pass.
1|Discover two local ETL checks|Place two independent local checks so one documented standard-library test command discovers and runs both.|CheckA validates a sale result6; checkB validates an empty batch result0.|Runner reports2executed checks and both pass.|Importing a module without discovering its checks is not evidence that they ran.
1|Keep a caller's input unchanged|Test a transformation's promise that it will not modify the input record supplied by another stage.|Input={id:A,units:'2'}; normalized output requires integer units2.|Output units2; original input still has text'2' and the same other fields.|A shallow alias of the original object is not an independent before-image.
1|Compare complete structured output|Check an export row's full required shape rather than only its row count.|Expected={id:A,cents:10,currency:INR}; faulty output omits currency.|The check fails and identifies missing currency.|A one-row output does not prove that the row has the required values or fields.
1|Test an explicit exception category|A validator rejects a negative batch size before doing any I/O. Verify that exact failure boundary.|batch_size=-1; fake reader records calls.|Expected validation exception raised; reader calls0.|Catching every exception and calling the test successful hides unrelated implementation failures.
2|Cover all sides of an inclusive threshold|Write bounded checks around the exact rejection-rate threshold used by an ETL gate.|Rule allows rejection fraction<=0.1; cases9/100,10/100,11/100.|First two allowed; third blocked.|A test far above the threshold does not check whether the boundary itself is correct.
2|Check missing,blank and null separately|Create a table-driven check for a required source identifier under a supplied validation contract.|Records omitid,haveid='',haveid=NULL,haveid='A'.|Reasons absent_id,blank_id,null_id,accepted respectively.|Do not collapse distinguishable source failures into one invented generic expected reason.
2|Verify deterministic output ordering|Test that a report uses its declared sort keys independently of incoming row order.|RowsBpriority1,Apriority1,Cpriority2; output priority descending thenidascending.|Expected orderC,A,B for each supplied input permutation.|Compare ordered outputs when order is contractual; converting both sides to sets would hide a defect.
2|Keep test cases independent|A batch counter must reset between runs. Demonstrate the defect caused by shared mutable fixture state and isolate each test.|First run processes2rows; separate second run processes1row.|Each isolated result reports2and1; test execution order does not change outcomes.|Do not make a test pass only by forcing another test to run first.
3|Test a CSV round trip with quoted fields|Verify a CSV writer and reader preserve a customer name containing a comma and a newline.|Record{id:A,name:'North, Ltd\nBranch2'}.|Round trip returns exactly one record with the original complete name.|Counting physical newlines is not a valid record-count oracle for quoted CSV.
3|Use a temporary workspace for ETL checks|Run a file-export check entirely inside a generated temporary directory.|One input rowAunits2; exporter creates accepted.csv.|Expected artifact exists during the check and its contents match; temporary workspace removed afterward.|A test must not overwrite the learner's actual exercise or persistent output files.
3|Capture a warning without printing private rows|Verify a validator emits a safe warning for one invalid country while omitting email and token values.|Row{id:C1,country:INVALID,email:person@example.test,token:dummy}.|Captured warning containsC1 and invalid_country; raw email/token absent.|Inspect captured exception text and debug output as well as the main warning.
3|Freeze the business clock in an age check|Inject a fixed clock so an age-based expiry check is reproducible on another day.|As-of2026-10-26; lotexpires2026-10-25.|Outcome expired with age1day under the declared rule.|The expected result must not depend on the actual date the test is executed.
4|Replace a source transport at its boundary|Test API ingestion through an injected transport that returns one valid and one invalid record.|Fake response itemsAunits2,Bunits'bad'; no live endpoint configured.|AcceptedA2; rejectedBinvalid_units; live request count0.|Patching an unrelated helper does not prove the source boundary was isolated.
4|Verify ordered adapter interactions|A pipeline must begin,write and commit in order,then publish its success marker.|Fake adapter and marker writer record an ordered event log.|Observed order begin,write,commit,publish_marker.|Checking that all four calls occurred without checking order misses publication before durable commit.
4|Simulate a target failure without a real database|Inject a write failure and verify rollback plus truthful failed status.|Fake target begins transaction; firstwrite succeeds; secondwrite raises.|Rollback once; commit0; success marker0; failed status retained.|A test that only checks an exception was raised misses leaked partial state or false-success artifacts.
4|Test a configuration environment override safely|Apply one temporary environment override during a check and restore the prior process environment afterward.|Defaultbatch_size100; temporary LAB_BATCH_SIZE='25'.|Effective25inside check; original environment restored afterward.|Do not leave test-specific environment settings active for unrelated checks.
5|Check full and incremental builds against one oracle|Compare a complete source rebuild with two incremental applications including a correction.|Batch1A10,B20; batch2A11,C30; full latest-state oracleA11,B20,C30.|Both paths produce the same keys and values as the oracle.|Equal row counts or equal grand totals alone do not establish state equality.
5|Test idempotency under exact replay|Apply an explicit event batch twice and compare final state plus audit classifications.|E1receiptA10,E2issueA3; replayE1/E2.|FinalA7after both runs; second run reports2replays and0new events.|A new event with the same amount but a different authoritative ID must not be skipped automatically.
5|Verify a restart checkpoint after a crash|Fail a staged pipeline after a committed chunk and reconstruct it from durable state.|Chunks[A,B],[C,D]; firstchunk committed; crash beforesecondcommit.|Restart begins secondchunk; finalA,B,C,D once each; checkpoint finalchunkcomplete.|An in-memory counter lost on restart is not a durable checkpoint.
5|Build one command that tests a mini-pipeline contract|Provide a local test command covering ingestion,validation,export and restart for a bounded fixture.|InputA2,Bbad,C3; one injected output failure; temporary output root.|Command checks acceptedA/C,rejectedB,failed-attempt evidence and successful restart; nonzero if any assertion fails.|A test report claiming all checks passed must retain the actual runner output.
6|Check failure at every durable boundary|Inject one failure at each of read-complete,write-started and pre-commit boundaries of a small pipeline.|Two-row batchA,B; old committed outputOLD.|Every failed case preserves the promised old state; only successful run publishesA,B.|Do not test only the easiest failure location and extrapolate recovery to every boundary.
6|Test resource cleanup on exceptional exit|Verify the source handle and target adapter close after a transformation raises.|Fake source/target track opened/closed; middle row raises validation-internal-error.|Both resources closed; run failed; internal error distinguished from a normal row rejection.|Closing only on the happy path leaves the operational contract untested.
6|Prevent a retry check from hanging|Use an injected fake clock and an attempt limit to test permanent transient failure deterministically.|Adapter always returns transient_failure; maxattempts3; delays1and2seconds.|Exactly3attempts; planned delay total3seconds; finalfailure; no real waiting.|A test must not sleep indefinitely waiting for a success that the fixture never returns.
6|Expose a swallowed exception as a false-success defect|A supplied faulty wrapper catches an output error and returns success. Write a check that rejects it.|Writer raises IOError; wrapper returns{status:success,exported:10}.|Contract check fails because no commit occurred; corrected wrapper returns failed with exported0orunknown as justified.|Do not change the failure fixture into a successful write to avoid diagnosing the defect.
7|Check a useful transformation invariant|For nonnegative integer units,verify partitioned batch totals equal the whole-batch total across reproducible generated inputs.|Seeded generator creates100bounded batches; each split at a deterministic position.|For every batch,total(left)+total(right)=total(whole),including empty parts.|Document the invariant's input domain; it does not automatically hold for nonadditive metrics or floating approximations.
7|Test monotonic authoritative versions|For one entity,processing an older version after a newer one must not regress state.|Aversions1value10,3value30,2value20; several declared arrival orders.|FinalAvalue30version3for each order; staleversionsclassified.|Equal-version conflicting payloads need a separate ambiguity check rather than silently using the last arrival.
7|Create a consumer contract check before refactoring|Capture the consumer-required output schema and semantics,then evaluate a candidate implementation.|Consumer requires idTEXT,centsINTEGER,currencyTEXT; candidate emits amountFLOATinstead ofcents.|Candidate rejected with missingcents and wrongcontract evidence.|A visually similar CSV preview does not establish type or column compatibility.
7|Test concurrent ownership with a synchronization barrier|Verify only one worker claims a batch when two workers reach the claim boundary together.|Two fake workers share batchB1and a controlled barrier; claim store enforces oneowner.|Exactly oneowner; loser getsalready_claimed; no doublecommit.|Two sequential calls are not evidence that the concurrent race is handled.
8|Measure test fixture memory as well as pipeline memory|Build a large test generator and show the fixture itself does not allocate the entire source.|One million deterministic records; pipeline and fixture measured under64MiB.|Exact count1000000; observed peak below64MiB; fixture construction included in measurement.|Measuring only transformation memory after allocating a huge fixture hides the true test resource cost.
8|Use operation counts to catch an accidental quadratic path|Instrument a customer-reference lookup used for10000orders against1000customers.|All orders reference a known customer; reference access counter supplied.|Correct matches; bounded lookup work linear in input/reference size under the declared method.|Do not impose an arbitrary elapsed-millisecond threshold that flakes across machines.
8|Prove a performance change preserves exact outputs|Compare an old and optimized transform on adversarial monetary and missing-value fixtures.|Amounts include0,largecents,NULLand refundevents; authoritative expected outputs supplied.|Both implementations match exact oracle or candidate is blocked; observed timings kept separately.|A faster incorrect result is not an accepted optimization.
8|Bound the scope of a smoke test|Separate a quick deployment check from a larger generated regression suite and state what each proves.|Smoke usesA2andBbad; regression includes10000rows,duplicates andfailureinjection.|Both commands executable; smoke result labelled bounded; regression evidence reported independently.|A passing two-row smoke test is not reported as proof of large-volume or concurrency behavior.
9|Make test output a reproducible release artifact|Record code version,fixture digest,command,runtime version and actual result for a local release check.|One fixtureA2,Bbad; supplied codeversionV1; runner output captured.|Artifact linksV1andfixture digest to executed checks and finalexitcode.|Do not write a successful exit code before the command has actually finished.
9|Gate a release on expected failure coverage|A release requires correct happy-path behavior plus rollback,redaction and changed-input checks.|Candidate passes happy-path but rollback case leaks one targetrow.|Release blocked with rollback evidence; passing checks retained.|A high pass percentage does not override a failed required integrity contract.
9|Restore test isolation after a failed run|Kill or fail a sandbox check midway and verify its cleanup policy before rerunning unrelated checks.|Owned temporary fileR1and fake worker active; unrelated fileR2mustremain.|R1owned resources cleaned or explicitly reported; R2unchanged; next test does not inherit stale state.|Cleanup must verify ownership and root containment rather than deleting every matching filename.
9|Audit assistance and independent review evidence separately|Design a verification record that preserves passing code checks without inventing independent mastery.|Solution passes all fixtures; learner reports significant AI help; no independent changed-case yet.|Verified completion eligible; independent mastery pending; later independent transfer scheduled.|Passing automated checks and an assistance disclosure do not themselves demonstrate independent reconstruction.
10|Independently build a failure-injection ETL test suite|Create and run a bounded suite for one file-to-target pipeline with explicit correctness,replay,recovery and privacy contracts.|Three synthetic batches; malformedrow;duplicateevent;targetfault;tokenbearingrow; changedreviewfixture.|Executed checks expose each injected defect; corrected pipeline passes; evidence links fixture/code versions.|Reviewer alters one failure boundary after the initial successful submission.
10|Independently defend a test oracle for incremental state|Build an independent reference implementation or manually justified oracle for a versioned incremental feed and compare it with the production path.|Creates,updates,deletes,replays,lateversions andequal-versionconflicts.|State comparisons identify every intended conflict and match the oracle for valid histories.|Copying the production implementation into the expected-value calculation is not an independent oracle.
10|Independently verify concurrent pipeline safety|Test claim ownership,transactional publication,cancellation and recovery under controlled overlapping workers.|Two workers; sharedbatch; injectedcommitfailure; cancellation whilequeued.|One logicalcommit; no leakedworker/permit; restart equals cleanstate; observed overlap evidence.|Explain which interleavings were tested and which remain unproven.
10|Independently validate a pipeline contract migration|Build compatibility tests across old/new producer and consumer contracts,including rollback and newsourceevents during the test.|Oldcents;newamount_minor/currency;oneunsupportedversion;latevalidrecord.|Supported contracts work; unsupportedblocked; rollback preserves latevaliddata; measured checks recorded.|Do not declare compatibility solely from equal column counts.
10|Independently diagnose false confidence in a passing suite|Investigate a supplied suite that passes despite a wrong currency total and skipped failure checks,then repair its evidence gaps.|Suite compares onlycounts;candidate swapsA10/B20toA20/B10;rollback test skipped.|New checks catch value swap; required skipped check preventsrelease; corrected suite result truthful.|A rewritten test suite is not evidence the original learner solution had been independently correct.
10|Independently create a portable engineering assessment harness|Package a bounded ETL brief,syntheticfixtures,hidden changedcase entrypoint,resourcebudgets and reproducible testcommands.|Brief includes validation,replay,rollback,privacy andrestart; grader changes one fixture.|Harness runs in a clean temporary root; checks are meaningful; results preserve assistance and independent evidence dimensions.|Designing the harness and independently solving its tasks are separate achievements.
''')

author('sql',r'''
0|Inspect one raw feed line before parsing|A staging analyst needs the unchanged raw text of one vendor event before deciding how to interpret it.|raw_feed(source_row,raw_text):(2,'A;002;ready')|source_row2 and exact raw_text'A;002;ready'.|A raw staging preview must not silently normalize leading zeros or separators.
0|Measure an empty source string|Distinguish an empty text field from SQL NULL before applying a parsing contract.|raw_values(id,value):('A',''),('B',NULL)|A character_length0; B character_lengthNULL.|An empty value and an absent measurement are not interchangeable evidence.
1|Extract a fixed vendor prefix|A vendor event reference consists of a three-character source prefix followed by its local code. Return both parts.|refs='SAP0007','WEB12'|SAP/local0007; WEB/local12.|A reference shorter than3characters is rejected rather than accepted with a truncated prefix.
1|Remove only a declared transport padding character|Trim trailing spaces from a fixed-width status field while preserving leading spaces and internal separators.|status=' READY  '|normalized=' READY'.|A global trim would violate the contract by removing the meaningful leading space.
1|Find a literal percent sign in a source code|Select source codes containing a literal percent character under the declared query dialect.|codes='A%1','AB1','100percent'|'A%1'only.|The pattern wildcard must not turn this into a match for every code.
1|Keep a source code's internal whitespace|Normalize only outer transport whitespace around a department code.|codes='  NORTH  EAST  'and'NORTH EAST'|first='NORTH  EAST'; second='NORTH EAST'; remain distinct.|Do not collapse internal spaces without an authoritative identity rule.
2|Validate a numeric token before casting|Classify a raw quantity token as a permitted nonnegative whole number before converting it.|tokens='12','0','-1','1.5','x'|12and0accepted as integers; others rejected with invalid_quantity.|A bad token must not abort the complete batch by triggering an uncontrolled cast.
2|Keep repeated delimiters as missing fields|Split a vendor line with exactly three semicolon-separated fields,retaining an empty middle value.|raw='A;;ready'|field1A;field2empty;field3ready; missing_quantity flagged.|Removing empty tokens would shift ready into the wrong field.
2|Detect a delimiter-count contract failure|Require exactly two delimiters in a three-field unquoted transport format.|lines'A;2;ready','A;2','A;2;ready;extra'|firstvalid;secondfield_count2;thirdfield_count4.|Do not apply this simple count rule to a quoted format where delimiters may appear inside fields.
2|Classify a source-date token without guessing formats|Accept only valid ISO calendar dates in a staged token.|tokens'2026-10-26','2026-02-30','26/10/2026'|firstaccepted;secondinvalid_calendar_date;thirdunsupported_format.|A permissive conversion function's automatic normalization does not establish source validity.
3|Parse a known log envelope with an optional tail|A vendor line contains severity,reference and an optional free-text note after the first two delimiters.|raw='WARN;A7;customer;requested retry'|severityWARN;referenceA7;note'customer;requested retry'.|Only the first two delimiters define the envelope; later delimiters belong to the note.
3|Validate a tagged money field|Parse a token whose explicit contract is three-letter currency,colon,nonnegative two-decimal amount.|tokens'INR:1.20','USD:0.00','INR:1.234','1.20'|firsttwoaccepted as120and0minorunits; lattertwo rejected.|Do not infer a missing currency from the analyst's locale.
3|Preserve the original token beside its normalized value|Normalize outer whitespace and case for an approved country field while retaining raw evidence.|rawcountry=' in '; secondrowrawNULL|firstraw' in ',cleanIN; secondrawNULL,cleanNULL.|A normalized field cannot replace raw evidence needed to explain a rejection or source defect.
3|Detect a source-reference normalization collision|Before adopting case-insensitive matching,report distinct raw identifiers mapping to one normalized code.|rawrefs'ab','AB','cd'|normalizedABhasrawrefsab,AB; collision blocks automatic merge.|Do not resolve the collision by selecting whichever record arrived last.
4|Expand a JSON event array with ordinality|Turn a bounded JSON array into event rows while retaining original array positions.|documentitems=[{id:B},{id:A},{id:B}]|positions1B,2A,3B.|Repeated IDs may be separate positions; deduplication requires a separate event-identity contract.
4|Distinguish missing JSON keys from JSON null|Classify a document field as absent,presentnull or presentvalue before typed staging.|documents{}, {qty:null}, {qty:0}|absent_qty,present_null,known_zero respectively.|A text extraction returning SQLNULL for multiple cases must not erase the source distinction.
4|Compare numeric and textual JSON values|Require a JSON quantity to be numeric,not numeric-looking text or boolean.|docs{qty:2},{qty:'2'},{qty:true}|firstaccepted; secondwrong_type_text; thirdwrong_type_boolean.|Do not silently coerce the other types under this contract.
4|Reassemble child records into a deterministic JSON export|Aggregate each order's lines in explicitline_idorder and include empty arrays for orders without lines.|ordersO1,O2;linesO1L2units3,O1L1units2|O1items[L1units2,L2units3];O2items[].|Array order must not depend on an unspecified scan order or aggregation plan.
5|Build a raw-to-typed vendor staging report|Parse the declared three-field unquoted format,validate ID and integer units,and retain reasons by source row.|row2'A;2;ready';row3'B;x;ready';row4';3;ready'|acceptedA2; rejectedrow3invalid_units,row4missing_id; counts1/2.|A malformed record remains traceable to raw text and source row.
5|Separate document-level and item-level rejection|Process a JSON envelope only if its required batch ID is valid,then classify individual item quantities.|docB1itemsA2,Bbad; seconddocmissingbatchwithitemC3|B1acceptA/rejectB; seconddocblocked beforeitempublication.|A rejected envelope is not an empty successful business batch.
5|Build a source-quality metric at the correct denominator|Report invalid item fraction separately from malformed document fraction.|10documents;1malformed;9validdocumentscontain90itemswith9invalid.|document_failure_rate0.1; item_invalid_rate0.1among90observeditems.|The malformed document's unknown item count is not guessed or added to the item denominator.
5|Compare a parsed incremental feed with a full typed rebuild|Rebuild latest state from all raw events and compare with two parsed incremental applications.|rawA:v1:10,B:v1:20 thenA:v2:11,C:v1:30; definedenvelopecontract.|Both targetsA11version2,B20version1,C30version1.|Compare entity keys,versions and values,not only record counts or total amounts.
6|Detect duplicate properties before losing raw JSON evidence|Show why an ambiguous raw object must be rejected before a representation discards duplicate keys.|rawtext'{"id":"A","qty":2,"qty":9}' plus a normal object.|Ambiguous object duplicate_propertyqty rejected by a supported raw-validation step; normalobject accepted.|If the database representation already discarded the duplicate,report that limitation and preserve the raw input for an appropriate validator.
6|Report invalid encoding separately from bad JSON syntax|Classify a supplied transport-validation result independently of the SQL parser's item rules.|rowAtransportinvalid_utf8;rowBvalidUTF8butinvalidJSON;rowCvalidJSONqtybad.|Aencoding_error;Bjson_syntax_error;Citem_validation_error.|Do not force undecodable bytes into a text column and claim their original form survived.
6|Reject an unapproved parser version|Require the declared record-schema version to choose the parser even when the payload resembles an earlier format.|version1'A;2;ready';version9'A;2;ready'|version1accepted;version9unsupported_versionblocked.|A familiar separator layout is not proof of compatible semantics.
6|Surface an unparseable fraction rather than returning zero|A supplied faulty report uses a conversion fallback of0for malformed quantities. Produce a report that preserves unknowns and rejection counts.|tokens'2','bad','0'|knownsum2; accepted2; rejected1; badtokennotcountedaszerobusinessquantity.|A plausible grand total does not prove the malformed source was handled correctly.
7|Parse a versioned nested shipment contract|Normalize two declared JSON versions into one typed line contract while retaining source version.|v1shipmentidS1,lines[{sku:A,qty:2}];v2idS2,items[{product:B,units:3}].|typedS1/A2v1,S2/B3v2.|Conflicting fields within one declaredversion are rejected instead of mixing both adapters.
7|Apply tenant-specific time interpretation explicitly|Parse offset-free vendor timestamps only using a supplied tenant timezone mapping and retain the raw token.|T1UTC,T2Asia/Kolkata;bothraw'2026-10-26 10:00'.|T1instant10:00Z;T2instant04:30Z; rawtext retained.|An unknown tenant timezone blocks instant conversion rather than using the database session default.
7|Match semi-structured events to effective parser rules|Select a versioned parsing rule by source and effective event date,keeping its rule ID in lineage.|sourceV1usesruleR1beforeOct10,R2fromOct10;eventOct9.|Event bindsR1; rule identity retained with parsed result.|A later parser-rule edit must not silently rewrite an already frozen historical output.
7|Avoid duplicate facts when expanding independent arrays|A document has order lines and delivery attempts,which are separate grains. Produce both outputs without multiplying them.|orderO1linesL1,L2;attemptsD1,D2,D3.|Two line facts and three attempt facts; order summarylinecount2,attemptcount3.|A direct cross expansion yields6rows and is not the intended fact grain.
8|Measure an indexed parsed-field projection|Compare a repeated JSON-path filter with a supported typed/indexed projection on a generatedfixture.|100000events;knowncustomerC7has100matches;samefiltercontract.|Same100eventkeys;actualplans,timings,indexsizeandprojectionmaintenanceobservations.|Include the cost of deriving and maintaining the projection; do not report read speed alone as the full tradeoff.
8|Compare guarded casts with repeated parsing|Measure parsing each raw token once into checked staging versus repeated conversions in several reports.|100000rawrows;1percentinvalidquantities;threereports.|Samevalid/rejectedsets andbusinessmetrics;parse/evaluationcardinalitiesandplansrecorded.|A cached intermediate must retain the parser-version boundary rather than mixing stale normalized data.
8|Bound JSON expansion before reporting|Reject or quarantine an envelope whose item array exceeds a configured allowedsize before producing an unbounded fact expansion.|docA10items;docB100000items;maximum1000.|Aprocessed;Boversized_envelopereported;no100000rowpublication.|The size cap is a business/operational contract,not proof every large document is corrupt.
8|Measure text-normalization selectivity and collisions|Profile a generatedsource before indexing a normalizedkey and compare lookupplans without droppingcollisions.|100000references;knowncase-collisionpairs;explicituppercasecontract.|Collisionreportretained;matchingkeysunchanged;actualplansandtimingsreported.|A faster normalizedlookup does not authorize merging distinctrawidentities.
9|Publish a parser contract with explicit raw retention|Version the expectedenvelope,typedcolumns,rejectionreasons andrawretentionlink for one source release.|sourcecontractV2requiresid,units,currency;candidateomitsrawlineage.|Releaseblockedmissingrawlineage;requiredtypedcontractandfixturechecksreported.|A parser that outputs correct samplevalues still needs the required diagnostic lineage contract.
9|Check a sanitized staging review view|Expose source row,reason and safe identifiers while excluding raw tokens and personalcontactfields.|rawrowcontainsidA,emailperson@example.test,tokenDUMMY;reasoninvalid_units.|ReviewviewidA,sourcerow,reason;email/tokenabsent;authorizedrawaccessseparate.|A UI preview hiding columns is not proof that the view or role blocks direct access.
9|Reproduce a frozen parsed report under a later rule|Retain raw inputs and parserversion so an oldreport can be rebuilt after a parsingrule changes.|raw'001';R1preservesastext;R2interpretsnumeric1;oldreportusesR1.|Oldreportstill'001';R2candidate1reportedasseparaterevision.|Do not overwrite stable business identifiers merely because a newer parser converts them differently.
9|Gate a parser rollout with adversarial fixtures|Run requiredfixtures covering quotes,emptytokens,unknownversions,oversizedarrays andprivacy before release.|Candidatepassesnormalrowsbutdropsanemptyrequiredtokenandlogsasecret.|Releaseblockedwithbothdefects;otherpassingchecksretained.|A highoverallpasspercentage does not override a failed required correctness or privacy contract.
10|Independently build a versioned raw-to-typed SQL staging layer|Implement explicit sourcecontracts,rawlineage,typedoutputs,rejections anddeterministicreplay.|DelimitedandJSONsources;unknownversion;badquantity;null/absentfields;latecorrection.|Validfactsreplaycorrectly;everyrejecttraceable;schema/versionsretained;changedcasehandled.|Reviewer changes an envelope field after submission without prescribing a query strategy.
10|Independently diagnose a silent parsing-loss incident|Investigate why a report's counts andmoney changed after a parserupgrade.|Oldcodes'001'and'1'distinct;candidatecastsbothto1anddropsmalformedrowswithoutrejects.|Identitycollisionandmissingcoveragequantified;safeversionedrepairplan;rawproofretained.|Do not merge records to force the candidate's counts to match its own assumptions.
10|Independently migrate nested event contracts|Support old/new nestedJSONcontracts during overlap and keep separate line/attempt grains.|v1lines;v2items;twoindependentchildarrays;unsupportedv9;rollbackrequired.|Supportedfactsconsistent;noCartesianmultiplication;v9blocked;consumercontractsandrollbacktested.|An equalgrandtotal is insufficient if row identities or childgrains changed.
10|Independently optimize a semi-structured warehouse slice|Compare rawpathqueries,validatedstaging andindexedprojections on a generatedboundedworkload.|Millionrawrecords;skewedkeys;invalidtokens;requiredexactmoney andprivacycontracts.|Correctoutputs/rejectsets equal;actualplans/runtime/storage;tradeoffsdefended.|Do not hide projectionmaintenancecost or classify unknownsourcecounts as measuredzero.
10|Independently restore parser-versioned reporting evidence|Recover an oldreport andcurrentreport from rawfixtures,versionedrules andretainedlineage after targetloss.|R1preservesleadingzeros;R2approvednewformat;onecorruptrawartifact;readerviewcontract.|Recoverableversionsreproduced;corruptartifactquarantined;gapsexplicit;readeraccessverified.|Missingrawdata cannot be reconstructed merely from a knownaggregatecontroltotal.
10|Independently design an adversarial source-contract assessment|Build andsolve a boundedbusinesscase for a vendorfeed that changesformats,containsambiguousrecords andneeds recovery.|Briefdefinesrawretention,typedconsumer,privacy,replay,versionselection andresourcebudget.|WorkingSQLartifacts;observedcontract/failurechecks;assistancehistory;independentchangedfixtureevidence.|Assessment design and independently demonstrated implementation remain separate learning evidence.
''')

def prose_formatter():
    words=set('a i an the and or before after second first third complete commit final chunk stale versions classified amount float instead failure injection changed review fixture unsupported blocked synthetic fixtures raw null accepted normalized has refs document publication defined envelope contract row valid json qty bad token not counted as zero business quantity generated same filter index size projection maintenance observations evaluation cardinalities plans recorded collisions explicit uppercase collision report retained matching keys unchanged actual timings reported lookup distinct identities expected rejection reasons retention link candidate omits lineage release missing required typed checks personal contact fields contains authorized access separate passes normal but drops empty logs secret with both defects other passing high overall percentage deterministic delimited sources facts replay correctly every reject traceable case handled identity coverage quantified safe versioned repair plan proof nested two independent child arrays rollback supported consistent cartesian multiplication consumer tested validated staging indexed bounded workload million records exact money privacy tradeoffs defended cost unknown source counts current corrupt artifact reader view recoverable reproduced quarantined verified known aggregate control total contains ambiguous brief defines selection resource budget working sql artifacts observed assistance history evidence'.split())
    proposal=json.loads((BANK/'foundations-draft-promotions.json').read_text(encoding='utf-8'))
    for entry in proposal['proposals']:
        p=entry['problem']
        text=' '.join((p['task'],p['inputs']['fixture_contract'],p['expected_output']['contract'],*p['constraints']))
        words.update(w.lower() for w in re.findall(r'\b[A-Za-z]{2,18}\b',text))
    for entries in ROWS.values():
        for row in entries:
            words.update(w.lower() for w in re.findall(r'\b[A-Za-z]{2,18}\b',row[1]))
    @lru_cache(None)
    def segmented(token):
        if token.lower() in words:return token
        @lru_cache(None)
        def visit(start):
            if start==len(token):return []
            options=[]
            for end in range(start+1,len(token)+1):
                part=token[start:end]
                if part.lower() in words:
                    rest=visit(end)
                    if rest is not None:options.append([part]+rest)
            return min(options,key=len) if options else None
        result=visit(0)
        return ' '.join(result) if result else token
    def plain(text):
        for old,new in {
            'versionconflicts':'version conflicts','normalizedABhasrawrefsab':'normalized AB has raw refs ab',
            'rowCvalidJSONqtybad':'row C valid JSON with invalid qty','andbusinessmetrics':'and business metrics',
            'droppingcollisions':'dropping collisions','andindexedprojections':'and indexed projections',
            'oneowner':'one owner','doublecommit':'double commit','testcommands':'test commands',
            'emailperson@example.test':'email person@example.test','tokenDUMMY':'token DUMMY',
            'rowcounts':'row counts','rowcount':'row count','rawrow':'raw row','samefilter':'same filter',
            'onecorrupt':'one corrupt','noCartesian':'no Cartesian','faultchecks':'fault checks',
            'firsttwo':'first two','secondrow':'second row','rawNULL':'raw NULL',
            'oldreport':'old report','currentreport':'current report','sourcecontract':'source contract',
            'rawlineage':'raw lineage','typedcontract':'typed contract','badtoken':'bad token',
            'validrows':'valid rows','oldcents':'old cents','newamount':'new amount','latevalid':'late valid',
            'cleanstate':'clean state','expected6':'expected 6','observed5':'observed 5',
            'one-row':'one-row','quantitytoken':'quantity token','rawtext':'raw text',
        }.items():text=text.replace(old,new)
        text=re.sub(r'[A-Za-z]{15,}',lambda match:segmented(match.group()),text)
        return re.sub(r'([,;])(?=[A-Za-z])',r'\1 ',text)
    return plain

def main():
    base=json.loads((ROOT/'tools/curriculum.json').read_text(encoding='utf-8'))
    metadata={'python':('PY',322),'sql':('SQL',308)}
    checkpoint={'status':'new_append_only_content_frozen','tools':{}}
    plain=prose_formatter()
    for tool,entries in ROWS.items():
        prefix,start=metadata[tool]
        existing=[p for p in base['problems'] if p['tool_id']==tool]
        for suffix in ('','-batch2','-batch3'):
            existing+=json.loads((BANK/f'{tool}{suffix}.json').read_text(encoding='utf-8'))
        assert max(int(p['id'].rsplit('-',1)[1]) for p in existing)==start-1
        published=[p for p in existing if p.get('publication_status','published')=='published']
        latest={level:max((p for p in published if p['level']==level),key=lambda p:p['id']) for level in range(11)}
        problems=[];previous=None
        for number,(level,title,task,fixture,expected,boundary) in enumerate(entries,start):
            task,fixture,expected,boundary=map(plain,(task,fixture,expected,boundary))
            parent=previous if previous and previous['level'] in (level,level-1) else latest[max(0,level-1)]
            pid=f'RLP-{prefix}-{number:03d}'
            p={'id':pid,'tool_id':tool,'title':title,'level':level,'difficulty':f'level_{level}',
               'scenario':task,'task':task,'learning_objective':title,
               'inputs':{'fixture_contract':fixture,'environment':'Synthetic fixtures and learner-owned disposable targets only.'},
               'expected_output':{'contract':expected},'constraints':[boundary,'Preserve raw inputs,actual attempts and unrelated files.'],
               'acceptance_criteria':['Demonstrate this output: '+expected,'Verify this boundary: '+boundary,
                    'Submit actual implementation,observed outputs and all help used; expected results are not execution evidence.'],
               'prerequisites':[parent['id']],'independent_prerequisites':[],
               'skill_prerequisites':[] if level==0 else [f'{tool} bounded level {level-1}'],
               'progressive_hints':['Trace the smallest fixture and state the required output grain before coding.',
                    'Check this boundary separately: '+boundary,
                    'Reduce the first failing fixture,compare expected with observed results,and reconstruct the task one checked step at a time.'],
               'engineering_relevance':f'{title} is a bounded data-platform responsibility. After review,connect it to an upstream producer and downstream consumer,and identify one limitation.',
               'estimated_minutes':10 if level==0 else min(180,15+12*level),
               'official_docs':['https://docs.python.org/3/library/unittest.html'] if tool=='python' else ['https://www.postgresql.org/docs/current/functions-json.html','https://www.postgresql.org/docs/current/functions-string.html'],
               'verification':{'kind':'artifact_review'},'challenge_kind':'initial' if level==0 else 'transfer',
               'topic_id':None,'publication_status':'published','published_version':'2026.10.26.5',
               'sequence':level*1000+number,'authoring_batch':'foundations-explicit-004'}
            problems.append(p);previous=p;latest[level]=p
        assert len({p['id'] for p in problems})==len(problems)
        assert len({p['task'] for p in problems})==len(problems)
        path=BANK/f'{tool}-batch4.json'
        if path.exists():assert json.loads(path.read_text(encoding='utf-8'))==problems,'Existing batch4 content changed'
        content=json.dumps(problems,indent=2,ensure_ascii=False)+'\n'
        path.write_text(content,encoding='utf-8')
        checkpoint['tools'][tool]={'new':len(problems),'first_id':problems[0]['id'],'last_id':problems[-1]['id'],
            'total_if_all_prior_promotions_publish':start-1+len(problems),'target':450,
            'remaining_if_all_prior_promotions_publish':450-(start-1+len(problems)),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (BANK/'authors/foundations-batch4-checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(checkpoint,indent=2))

if __name__=='__main__':main()
