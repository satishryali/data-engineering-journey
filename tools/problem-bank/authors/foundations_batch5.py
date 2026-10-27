"""Append-only Python and SQL problem batch 5 with authored fixtures and outcomes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
BANK = ROOT / "tools/problem-bank"
ROWS: dict[str, list[tuple[int, str, str, str, str, str]]] = {}


def author(tool: str, text: str) -> None:
    rows = []
    for source_line, raw in enumerate(text.strip().splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("|")
        if len(parts) != 6:
            raise ValueError(f"{tool} line {source_line}: expected 6 fields, got {len(parts)}")
        level, title, scenario, fixture, expected, boundary = (part.strip() for part in parts)
        rows.append((int(level), title, scenario, fixture, expected, boundary))
    ROWS[tool] = rows


author("python", r'''
0|Read a delivery event identifier|A courier feed preview needs to show one supplied event ID before processing its payload.|event={'id':'EV7','status':'picked_up'}|EV7|Reading the ID does not prove the status is valid.
0|Read a supplied event status|An operator wants the original status text from a single courier event.|event={'id':'EV7','status':'picked_up'}|picked_up|Preserve source spelling instead of silently changing the status.
0|Read an event source name|A multi-courier inbox must retain which provider sent a sample record.|event={'id':'EV7','provider':'north'}|north|Do not infer the provider from the event ID.
0|Read the declared event version|A receiver previews one envelope before deciding how to interpret it.|envelope={'version':1,'payload':{'id':'EV7'}}|1|A version value is metadata, not evidence that parsing succeeded.
0|Count a supplied batch|A shift report first needs the number of event records handed to the processor.|events=[{'id':'EV7'},{'id':'EV8'}]|2|Count records, not the number of dictionary fields.
0|Keep the source sequence position|A reviewer needs the one-based position of an event in its incoming batch.|events=[{'id':'EV7'},{'id':'EV8'}]|EV7 position 1; EV8 position 2|Sequence position is diagnostic metadata, not a replacement for event ID.
0|Echo a declared source file name|A local import preview must show which input file the operator selected.|source_file='courier-monday.csv'|courier-monday.csv|Do not claim the file exists merely because its name was supplied.
0|Separate one event from its payload|A receiver displays the envelope ID and nested delivery ID as distinct values.|envelope={'id':'MSG4','payload':{'delivery_id':'D9'}}|message MSG4; delivery D9|The message ID and business delivery ID have different meanings.
1|List event IDs in arrival order|A dispatcher reviews IDs from a small batch without sorting them.|events=[{'id':'EV9'},{'id':'EV2'},{'id':'EV5'}]|['EV9','EV2','EV5']|Arrival order must remain visible.
1|Find an event by exact ID|A support case names one event and expects its original record.|events=[{'id':'EV2','status':'picked_up'},{'id':'EV3','status':'delivered'}]; lookup='EV3'|{'id':'EV3','status':'delivered'}|An absent ID has a distinct not-found result.
1|Count events with one declared status|A shift report asks how many events are exactly delivered.|statuses=['delivered','picked_up','delivered']|delivered count 2|Case variants are not silently equivalent under this source contract.
1|Keep only one provider's events|A courier operations preview isolates north events while preserving their order.|events=[('EV1','north'),('EV2','south'),('EV3','north')]|['EV1','EV3']|The source list must remain unchanged.
1|Detect a missing delivery ID|A consumer cannot route an event with no delivery ID.|events=[{'delivery_id':'D1'},{'status':'picked_up'}]|first accepted; second missing_delivery_id|An absent key differs from an empty string.
1|Detect a blank delivery ID|A provider sent an ID field containing only spaces.|events=[{'delivery_id':'D1'},{'delivery_id':'  '}]|D1 accepted; second blank_delivery_id|Retain the raw blank value for diagnosis.
1|Retain an event timestamp as text|A raw inbox records provider time before interpreting time zones.|event={'id':'EV1','occurred_at':'2026-10-26T08:00:00+05:30'}|same timestamp text linked to EV1|Do not relabel local time as UTC.
1|Print a bounded event preview|An operator requests the first two events from an incoming list.|ids=['EV1','EV2','EV3']; preview_limit=2|['EV1','EV2']; total count 3|A preview is not the complete batch.
2|Separate accepted and rejected event IDs|A courier feed needs distinct lists based on required delivery ID validation.|EV1 delivery D1; EV2 missing delivery; EV3 delivery D3|accepted EV1,EV3; rejected EV2|Neither output list may duplicate an event.
2|Count events by provider|A shared inbox summary must show the contribution of each courier.|providers=['north','south','north']|north 2; south 1|Do not merge provider labels by a guessed alias.
2|Detect duplicate message IDs in one batch|A provider resent the same transport message within a single file.|message IDs MSG1,MSG2,MSG1|first MSG1 and MSG2 accepted; last MSG1 duplicate_message|Transport identity differs from delivery identity.
2|Keep distinct delivery IDs without losing order|A support export needs one ID per delivery in first-seen order.|delivery IDs D2,D1,D2,D3|[D2,D1,D3]|Sorting would hide arrival order.
2|Sort events by timestamp with stable ties|An analyst wants a time-ordered view of a small valid event batch.|EV2 at 09:00; EV1 at 08:00; EV3 at 09:00|EV1,EV2,EV3|Equal timestamps retain their input order.
2|Parse an explicit integer attempt number|A retry feed marks each event with an attempt token.|attempt tokens '1','02','bad'|1,2 accepted; bad rejected invalid_attempt|Do not turn malformed text into attempt zero.
2|Compare an event with a delivery state|A support check asks whether a delivered event is already reflected in a state record.|event EV1 delivery D1 status delivered; state D1 delivered|matching_status true|The comparison does not establish that EV1 caused the state.
2|Attach source row numbers to rejects|A file reviewer needs to locate a malformed event in its original CSV.|header row 1; data rows EV1,blank-ID,EV3|reject source row 3|Physical row numbering includes the header.
3|Validate an allowed status vocabulary|A provider contract allows picked_up, in_transit and delivered only.|EV1 picked_up; EV2 lost; EV3 delivered|EV1 and EV3 accepted; EV2 unknown_status|Keep the unknown raw status for contract review.
3|Reject a delivery event before pickup|A simple state rule forbids delivered before picked_up for the same delivery.|D1 events delivered then picked_up|first event rejected invalid_transition; second establishes picked_up|Arrival order is part of this bounded rule.
3|Preserve repeated status events|A provider may emit the same status twice with different message IDs.|D1 picked_up MSG1; D1 picked_up MSG2|two raw events; one current picked_up state; repeat classified|Do not discard evidence by conflating state with event history.
3|Find the latest valid event per delivery|A dispatch screen needs one current status after validating a short ordered feed.|D1 picked_up at 08:00; D1 delivered at 09:00; D2 picked_up at 08:30|D1 delivered; D2 picked_up|Do not choose a malformed later event as current state.
3|Identify a timestamp tied across event IDs|A courier investigation needs deterministic handling of equal occurrence times.|D1 EV1 in_transit and EV2 delivered both 09:00|tie reported with both IDs; no arbitrary winner|Input arrival order is not automatically an authoritative event order.
3|Measure delay against a promised time|A delivery desk compares actual completion against a promised UTC instant.|D1 promised 10:00Z; delivered 10:07Z|late by 7 minutes|A missing delivery event is unknown, not zero minutes late.
3|Choose a configured lateness threshold|A shift supervisor considers a delivery late only after its 5-minute grace period.|D1 delivered 10:04Z; D2 delivered 10:06Z; promise 10:00Z|D1 on_time; D2 late|Exactly 5 minutes is on time under this rule.
3|Keep cancellation separate from delivery|A dashboard must not count cancelled orders as delivered or unresolved.|D1 delivered; D2 cancelled; D3 picked_up|delivered 1; cancelled 1; in_progress 1|Cancellation is a distinct terminal state.
4|Join events to a delivery reference|A courier feed includes delivery IDs and a small authoritative delivery table.|events D1,D9; reference D1 customer C1|D1 enriched C1; D9 unmatched_reference|An unmatched event is retained for review.
4|Compare feed and reference coverage|An operator needs both orphan events and deliveries with no event.|events D1,D9; reference D1,D2|orphan event D9; no-event delivery D2|A one-sided join misses one of these gaps.
4|Check provider ownership at event time|Only the assigned courier may submit a delivery update.|D1 assigned north; events EV1 north, EV2 south|EV1 allowed; EV2 provider_mismatch|A familiar delivery ID is not sufficient authorization evidence.
4|Bind events to a versioned status map|Two providers use different raw labels for the same canonical event.|north 'DONE' map N1 to delivered; south 'complete' map S1 to delivered|both canonical delivered with map IDs N1,S1|Retain raw labels and map version for replay.
4|Reconcile a daily event file and manifest|A source manifest declares how many records should have arrived.|manifest 3 data rows; file has EV1,EV2|observed 2; missing 1; batch incomplete|Do not publish a complete-day claim from an incomplete file.
4|Merge two files with separate source rows|A daily inbox combines morning and evening drops.|am.csv rows EV1,EV2; pm.csv row EV3|three events with file and physical row lineage|Row 2 in two files does not identify the same source position.
4|Resolve a duplicate across two files|A transport message appears in both morning and evening drops.|am.csv MSG1; pm.csv MSG1 and MSG2|one processing result for MSG1; duplicate lineage includes both files|Do not erase the duplicate source evidence.
4|Compare state and event histories|A published delivery state appears older than its accepted event stream.|state D1 picked_up; accepted events D1 picked_up then delivered|state_lag D1; expected delivered|A disagreement is diagnostic until the state update process is checked.
5|Build a small event validation pipeline|A local batch must validate IDs, statuses and timestamps and write accepted and rejected outputs.|EV1 valid; EV2 blank ID; EV3 unknown status|accepted EV1; rejects EV2 blank_id, EV3 unknown_status|Preserve each original record and reason.
5|Publish a daily delivery status report|A validated event feed becomes one current status per delivery plus coverage counts.|D1 picked_up then delivered; D2 picked_up; D3 cancelled|three current rows; counts delivered1,in_progress1,cancelled1|The report grain is delivery, not event.
5|Build an arrival-versus-occurrence report|A late provider submission makes an old event arrive after a newer one.|D1 delivered occurred10:00 received10:01; picked_up occurred09:00 received11:00|occurrence order picked_up then delivered; arrival delay for late event 2 hours|Retain both clocks and explain which determines business state.
5|Export a replayable delivery snapshot|A customer-facing snapshot must identify the exact source cutoff.|events through message MSG3; D1 delivered; D2 picked_up|snapshot states plus source cutoff MSG3 and record counts|A naked output file without a cutoff cannot prove its input boundary.
5|Build a provider exception report|Operations needs actionable counts and samples by provider and reject reason.|north one blank ID; south two unknown statuses|north blank_id1; south unknown_status2; bounded samples linked to source|Samples must not be presented as total population.
5|Produce a courier SLA report|Join completed delivery events to promises and classify late results.|D1 promise10:00 delivery10:06; D2 promise11:00 delivery10:59; grace5 minutes|D1 late; D2 on_time; report late1 of completed2|Do not include incomplete deliveries in the completed denominator.
5|Build a delivery coverage manifest|A run exports accepted events, rejects and delivery states with shared run ID.|input 4; accepted3; rejected1; state rows2|manifest input4=accepted3+rejected1; state rows2; same run ID|State rows need not equal event rows.
5|Replay one corrected provider file|A provider resends corrected MSG2 while unchanged MSG1 remains stable.|first batch MSG1 valid, MSG2 bad; correction MSG2 valid with revision2|MSG1 unchanged; MSG2 accepted revision2; old rejection retained|A corrected message is not a second business delivery event.
6|Recover from a truncated CSV record|A courier file ends halfway through a quoted note after valid earlier rows.|EV1 valid; EV2 has unclosed quoted note|EV1 preserved; EV2 parse_error with source location; file completeness uncertain|Do not treat an incomplete physical file as a fully accepted batch.
6|Retry a transient provider lookup|Delivery ownership reference service fails once and succeeds on retry.|D1 event; lookup attempt1 timeout, attempt2 returns north|event processed once under north; retry count2 retained|A retry must not duplicate the business event.
6|Quarantine a permanently unknown provider|An incoming event declares a provider absent from configured contracts.|EV1 provider mystery; known north,south|EV1 quarantined unknown_provider; raw envelope retained|Retrying the same unknown contract indefinitely is not recovery.
6|Recover after accepted file write fails|A run writes rejects but its accepted output write fails before manifest publication.|input EV1 valid, EV2 invalid; accepted write raises disk error|previous release remains selected; incomplete run marked failed|A rejects file alone does not make the run complete.
6|Detect a changed source file on retry|An operator retries a file path whose bytes changed since the failed run.|path day.csv first digest A, retry digest B|content_changed reported; old attempt A and new B separately identified|File path equality does not imply input identity.
6|Resume a partly processed batch safely|A 100-row feed fails after durable processing of row 60.|checkpoint source digest X and next row61; retry same digest X|rows1-60 not duplicated; remaining40 processed; total100|A checkpoint for a different digest cannot be reused.
6|Classify a provider rate-limit response|An API returns a retry-after interval before any page content.|page2 returns 429 with retry-after 30s; page1 already durable|page2 pending retry; page1 preserved; no empty-page completion claim|The throttle response is not an empty data page.
6|Handle an invalid status-map version|A batch refers to an unavailable map version while a newer map exists.|event raw DONE requires N1; only N2 loaded|pending_missing_map_N1; raw event retained|Substituting N2 silently would alter historical meaning.
7|Separate event time from publication time|A provider corrects yesterday's event today and a consumer needs both views.|EV1 occurred Oct25 published Oct26; correction published Oct27|as-published Oct26 and current corrected views differ with version IDs|Do not rewrite the old published view without an explicit revision.
7|Handle out-of-order state transitions|An old pickup event arrives after a delivered event has already been published.|D1 delivered occurred10:00 received10:01; pickup occurred09:00 received11:00|history includes both; current delivered stays stable; late arrival flagged|Blind arrival-order state updates would regress D1.
7|Distinguish correction from competing claim|Two messages assert different delivery times for the same business event.|MSG1 says D1 delivered10:00; MSG2 says D1 delivered10:03 without correction reference|conflict_requires_review; both claims retained|A later arrival is not automatically an authorized correction.
7|Honor a provider-scoped identity|Two couriers reuse transport message number 100.|north MSG100 D1; south MSG100 D2|two distinct transport identities; no false duplicate|Message IDs are unique only within their declared scope.
7|Track delivery reassignment over time|A delivery changes assigned courier before a later status update.|D1 north until10:00; south from10:00; event north09:59; south10:01|both events authorized by their effective assignment|Using current owner for all historical events rejects valid history.
7|Reconcile competing source clocks|A provider event carries occurred_at and device local time with an explicit offset.|occurred09:00Z; device14:30+05:30; received09:04Z|device and occurred agree; four-minute transport lag|A clock disagreement must remain visible rather than silently choosing a timestamp.
7|Protect customer details in exception exports|A rejected courier event includes a customer phone number needed only in raw quarantine.|EV1 invalid status, phone 9990001111|review export has event ID and reason, no phone; restricted raw retains phone|Hiding phone in a UI is insufficient if exported bytes still contain it.
7|Estimate state uncertainty under a feed gap|The 10:00 manifest is missing between valid 09:00 and 11:00 files.|D1 picked_up09:00; missing10:00 batch; D1 delivered11:00|11:00 current delivered; earlier interval coverage marked unknown|A known final state does not prove all intermediate transitions arrived.
8|Measure event lookup strategies|A generated feed repeatedly looks up delivery reference records.|100000 events; 1000 delivery refs; same expected enrichments|scan and indexed lookup outputs equal; comparisons, time and memory measured|A faster lookup that drops unmatched events is invalid.
8|Bound a de-duplication window|A streaming processor sees many transport IDs under a 24-hour retry contract.|seeded 100000 messages; duplicate within24h; same ID after window|within-window duplicate suppressed; later ID classified under documented expiry; peak state measured|Expiry can admit old duplicates if source violates the retry contract.
8|Stream reject evidence without unbounded memory|A million-row malformed feed must produce reason counts and a bounded sample.|1000000 rows; every tenth row invalid; sample cap20|100000 rejects counted; sample <=20; measured peak below budget|A sample cap must not cap the actual reject count.
8|Benchmark partitioned daily state rebuilds|A year of events needs one-day correction without scanning all partitions.|365 daily partitions; correction affects day120 and dependent state|correct final state; touched partitions and elapsed work measured against full rebuild|Dependency across later days may require more than one partition.
8|Compare compression for replay bundles|A replayable courier batch is stored compressed under an explicit resource budget.|100000 synthetic events; plain and compressed representations|round-trip byte equality; size, compression and read time measured|Do not compare compressed and plain data with different fields.
8|Profile skewed delivery IDs|One test delivery produces 90 percent of events and slows grouping.|100000 events; D1 has90000; remaining10000 spread|same state/count results; skew and peak group size reported|Uniform synthetic IDs would conceal the hot-key behavior.
8|Measure failure recovery overhead|A batch processor checkpoints every 1000 or 10000 rows and fails at row55000.|100000 events; injected failure; two checkpoint policies|same final events; replayed rows, elapsed time and checkpoint bytes reported|A faster normal run alone cannot choose the recovery policy.
9|Gate a provider contract rollout|A new payload version adds optional stop_code and changes status spelling.|V1 fixture and V2 fixture; candidate parser drops V1 raw status|release blocked with V1 regression; V2 behavior recorded|Passing only the new fixture does not protect current consumers.
9|Define a delivery-state service level objective|Operations wants a measurable freshness claim tied to source and publication clocks.|source latest10:00; published cutoff09:50; target lag<=5 minutes|freshness lag10 minutes; objective breached; incomplete-source flag separate|A recent file modification time is not an event freshness measure.
9|Audit access to restricted courier rejects|A support role needs reasons but not personal fields; a privileged reviewer may inspect raw.|one rejected row includes phone; two roles|support query omits phone; privileged access logged; direct export checked|Testing only the application screen leaves storage access unverified.
9|Restore a frozen delivery snapshot|A target table is lost after the original feed and map versions were retained.|raw batch digest X; map N1; snapshot cutoff MSG50; current map N2|snapshot reproduces old states under N1 and cutoff MSG50|Current map N2 cannot substitute for a frozen rule.
9|Rehearse provider outage failover|The north feed stops while south continues and a report is due.|north last complete09:00; south complete10:00; report10:05|south reported current; north marked stale with last complete cutoff|Do not report a combined complete network total.
9|Investigate a false delivery improvement|A dashboard improves after a parser starts dropping malformed late events.|old late20 of100; candidate late10 of90 with10 rejected late events|coverage loss exposed; comparable late count restored before claim|A lower rate with a changed denominator is not proof of improvement.
9|Design retention for replay dependencies|Old event batches have legal holds and snapshots reference status maps.|batch B1 held; map N1 used by B1; B2 expired unlinked|B1 and N1 retained; B2 eligible for deletion|Deleting a tiny map can make retained events unreplayable.
10|Independently build a multi-provider delivery receiver|Implement ingestion, validation, scoped identity and current-state output from a bounded business brief.|north and south events; repeated message IDs; bad status; reassignment; correction|valid current states, traceable rejects, stable replay and source coverage|Reviewer supplies a late event after initial submission.
10|Independently recover a broken publication|Reconstruct a courier report after a failure between output writes and manifest publication.|approved release R0; candidate R1 half written; raw and map versions retained|R0 remains selected; R1 diagnosed; safe R1 retry verified|A newest timestamp is not a complete-release guarantee.
10|Independently defend an event-time policy|Choose and implement rules for occurrence, arrival, correction and publication time.|out-of-order pickup; repeated local hour; delayed correction; report cutoff|each view reproducible; ambiguous clocks rejected or disambiguated|Document where the source contract cannot establish an authoritative order.
10|Independently optimize a skewed courier workload|Design a bounded-memory processing plan while preserving exact event semantics.|million synthetic events; hot D1; 24-hour duplicate window; 64 MiB memory target|correct states/rejects; measured peak and runtime; recovery demonstrated|An optimized path must match an independent small reference oracle.
10|Independently audit a claimed SLA gain|Investigate a new report whose late rate falls after provider and parser changes.|old/new raw feeds; missing provider day; altered grace period; rejects|comparable cohort, rule and coverage effects separated with evidence|Do not infer business improvement from unequal populations.
10|Independently migrate courier payload versions|Support V1 and V2 concurrently and retire V1 through an evidenced rollout.|V1/V2 envelopes; unknown V3; rollback requirement; personal data field|both supported versions correct; V3 quarantined; rollback and privacy tested|A version rollout must not silently reinterpret old raw events.
10|Independently design a delivery incident drill|Create and solve a realistic fault case for on-call replay and consumer recovery.|brief includes incomplete file, transient lookup, stale state and held snapshot|working recovery artifacts, observed checks and explicit remaining uncertainty|Designing a drill and independently solving it require separate evidence.
''')

author("sql", r'''
0|Read one stock movement ID|A warehouse clerk needs to locate one known movement row in a small relational table.|movement(id,sku,units): (M1,S1,3)|M1|Selecting the ID does not establish stock balance.
0|Read one movement quantity|A receiving preview displays the exact units recorded for one movement.|movement: (M1,S1,3)|3|Keep the recorded units separate from available stock.
0|Read the movement type|A preview must show whether the recorded movement was a receipt or issue.|movement: (M1,S1,3,receipt)|receipt|Do not infer type from the sign of units.
0|Return all movement IDs|An operator wants the IDs of two known rows without grouping.|movements M1 receipt 3 and M2 issue 1|M1,M2|Output order is unspecified unless requested.
0|Show a named output column|A simple report must label the selected stock keeping unit as sku.|movement: (M1,S1,3)|one row with sku=S1|A column alias changes presentation, not stored data.
0|Read the storage location|A location-specific report starts from the location recorded on a movement.|movement: (M1,S1,L1,3)|L1|Location is a business key, not free-form display text.
0|Read a supplied reservation ID|A reservation lookup must distinguish its ID from the order it serves.|reservation: (R1,O7,S1,2)|R1|An order can contain more than one reservation.
0|Read one order line key|A picker identifies an order line using both order and line number.|order_line: (O7,2,S1,3)|order O7, line 2|Order ID alone does not identify this line.
0|Preview the source table name|A learner prepares a report from the stated movement table.|tables movement and reservation; report source movement|movement|Naming a table does not prove a query ran.
1|Filter receipts from movements|An inventory clerk wants only receipt records.|M1 receipt3; M2 issue1; M3 receipt2|M1,M3|A string contains match is not the declared equality rule.
1|Filter one SKU exactly|A warehouse report selects S1 without accidentally including S10.|rows S1 units3; S10 units4|S1 row only|Do not use a prefix search for an exact SKU.
1|Filter one location exactly|A stock review isolates movements at L1.|M1 L1; M2 L2; M3 L1|M1,M3|Another location must not leak into the result.
1|Sort movement IDs for review|A support export requires deterministic ascending IDs.|source order M3,M1,M2|M1,M2,M3|A table scan's accidental order is not a sorting contract.
1|Show newest timestamp first|A shift lead reviews most recently recorded movement times.|M1 08:00; M2 09:00; M3 08:30|M2,M3,M1|Specify how equal timestamps will be handled later.
1|Count all movement rows|A file-to-table check needs the number of loaded rows.|three movement rows including one with NULL note|3|Counting a nullable note would undercount.
1|Count distinct SKU values|A manager asks how many SKUs appear in a movement sample.|SKUs S1,S1,S2|2|Distinct SKUs are not movement rows.
1|Find missing reference IDs|A data steward looks for movement rows with no source reference.|M1 ref X; M2 ref NULL; M3 ref Y|M2|SQL NULL requires null-specific comparison.
1|Find an explicit zero-unit movement|A review separates a recorded zero from an absent quantity.|M1 units0; M2 units NULL; M3 units2|M1 only|NULL does not equal numeric zero.
2|Sum received units for one SKU|A receiving report totals only S1 receipt units.|S1 receipts3,4; S1 issue2; S2 receipt8|S1 received 7|Issued units do not belong in this receipt total.
2|Sum issued units for one SKU|A fulfillment report totals issued S1 units.|S1 issues2,1; S1 receipt7|S1 issued 3|Do not count receipts as issues.
2|Compute a bounded net movement|A small reconciliation compares S1 receipts and issues.|S1 receipt7, issue2, issue1|S1 net +4|A net movement is not necessarily current stock without an opening balance.
2|Group movement counts by type|A loader report shows how many rows of each declared type arrived.|receipt M1,M3; issue M2|receipt2; issue1|Rows with an unknown type require separate validation.
2|Group received units by SKU|A warehouse report needs receipt totals per SKU.|S1 receipts3,4; S2 receipt5; S1 issue1|S1 7; S2 5|Grouping by movement ID would defeat the SKU total.
2|Keep order lines above a quantity threshold|A picking queue filters lines with required units greater than two.|O1 line1 units2; O1 line2 units3|O1 line2|The threshold is strict greater-than, not greater-or-equal.
2|Return distinct active locations|A location picker shows each non-null location once.|locations L1,L1,L2,NULL|L1,L2|NULL is missing location, not a real location name.
2|Count reservations with known SKU|An audit counts reservation rows where a SKU is supplied.|R1 S1; R2 NULL; R3 S2|known SKU reservations 2|Unknown SKU rows remain in total row count.
2|Find a reservation quantity mismatch|A picker compares one line's requested units and reserved units.|O7 line1 requests3; reservation R1 holds2|short by1|This single-row comparison assumes no other reservation for the line.
3|Join reservations to their order lines|A picker report needs order, line, SKU and reserved units.|O7 line1 S1 requests3; R1 references O7 line1 holds2|one joined row O7/1/S1/2|Join on both order ID and line number.
3|Keep lines with no reservation|An exception report must retain unreserved order lines.|O7 line1 has R1; O7 line2 has none|line2 appears with missing reservation|An inner join would hide the exception.
3|Sum multiple reservations per line|A line can be reserved in two warehouse locations.|O7 line1 requests5; R1 L1 holds2; R2 L2 holds2|reserved4; short1|Do not compare each reservation separately against full requested units.
3|Avoid multiplying line quantities|A fulfillment total joins one order line to two reservation rows.|line O7/1 requests5; R1 and R2 reference it|requested total5; reservation rows2|Summing requested units after the one-to-many join would yield10.
3|Find reservations with no order line|A data-quality report looks for orphan reservations.|R1 refers O7/1 existing; R2 refers O9/1 absent|orphan R2|A dangling reservation must remain visible.
3|Report short and over-reserved lines|An operator needs both insufficient and excessive reservations.|line A requests5 holds4; line B requests2 holds3|A short1; B over1|Do not clamp over-reservation to zero and hide it.
3|Count distinct orders with shortages|Management asks how many orders are affected, not how many lines.|O1 lines1,2 short; O2 line1 short|2 orders; 3 short lines|Order and line grains differ.
3|Filter groups with total reserved units|A high-volume picker report selects lines with at least five reserved units.|line A reservations2+3; line B reservations1+2|A only|Filter the grouped total, not each input reservation row.
3|Label an unreserved line explicitly|A consumer needs zero reserved units for valid unreserved lines.|O7/2 requests3; no reservation rows|reserved0; short3|Zero is computed only after preserving the missing joined row.
4|Join reservation to stock by SKU and location|A pickability report compares reserved units with stock at the assigned location.|R1 S1/L1 holds3; stock S1/L1 4, S1/L2 9|R1 local stock4|Joining only on SKU would duplicate or misassign stock.
4|Keep stock with no reservation|Operations wants unused stock locations in the same coverage review.|stock S1/L1 4; S2/L1 8; reservation only S1/L1|S2/L1 unreserved8|A reservation-led inner join hides unreserved stock.
4|Detect missing stock keys|A reservation references a SKU/location not present in the stock snapshot.|R1 S1/L9 holds2; stock only S1/L1|R1 missing_stock_key|Missing snapshot data is not certified zero stock.
4|Aggregate reservation demand before joining stock|Several reservations share one SKU/location balance.|stock S1/L1 5; reservations R1=3,R2=4 at S1/L1|demand7; deficit2|A row-by-row comparison would miss the aggregate conflict.
4|Compare two stock snapshots by key|A daily inventory review needs added, removed and changed SKU/location balances.|yesterday S1/L1=5,S2/L1=2; today S1/L1=4,S3/L1=1|S1 changed -1; S2 missing today; S3 new|A missing key must not be reported as a measured zero balance.
4|Attach product descriptions without changing grain|A picker report adds catalog descriptions to reserved lines.|R1 S1 units2; catalog S1 name Widget|one R1 row with Widget|Duplicate catalog keys would multiply reservation rows and need diagnosis.
4|Compare receipt and issue ledgers|A reconciliation separates movement types for the same SKU and date.|S1 day1 receipt5, issue2; S2 receipt3|S1 net3; S2 net3|Keep receipt and issue subtotals visible with net.
4|Find unmatched shipment confirmations|A carrier file cites order lines that may not exist in picking.|confirmation O1/1; confirmation O9/2; picking has O1/1|O9/2 unmatched confirmation|Do not silently drop external confirmations.
4|Reconcile the complete key set|A review combines order lines, reservations, stock and confirmations for a small day.|O1/1 reserved; O2/1 unreserved; orphan R9; unmatched confirmation O9/2|four separately classified coverage cases|A single inner join cannot expose every missing side.
5|Build a daily reservation coverage query|A warehouse dashboard needs one row per order line with requested, reserved and shortage values.|O1/1 requests5 holds2+2; O1/2 requests1 holds none|O1/1 short1; O1/2 short1; two rows|The query must not duplicate an order line because of reservation detail.
5|Build a per-location demand report|A replenishment planner compares location demand and snapshot stock.|S1/L1 stock5 reservations2+4; S1/L2 stock3 reservation1|L1 deficit1; L2 spare2|Keep SKU and location in every grouping key.
5|Create an order fulfillment summary|A support agent asks whether all lines of an order have enough reservation.|O1 line1 requests2 holds2; line2 requests3 holds1; O2 line1 requests1 holds1|O1 not_ready; O2 ready|One ready line cannot make a mixed order ready.
5|Create a stock movement roll-forward|A daily check starts with opening stock and applies receipts and issues.|S1 opening10; receipt5; issue3|closing12 with subtotals10,5,3|This reconciliation requires a dated opening balance.
5|Produce a shipment discrepancy table|A carrier confirmation and picker record disagree on shipped units.|O1/1 picked3 confirmed2; O2/1 picked1 confirmed1|O1/1 discrepancy -1; O2/1 match|Use the line key; one order may have multiple lines.
5|Publish an exception reason summary|An operations report counts unmatched stock, short reservations and orphan confirmations separately.|one of each exception; two valid lines|three reason counts each1; valid lines retained|The reasons may apply at different grains and must be labeled.
5|Build a repeatable as-of stock view|A historical report uses movements through an explicit inclusive cutoff.|opening10; receipt Oct1 +5; issue Oct2 -3; cutoff Oct1|as-of Oct1 balance15|The current date must not shift the historical cutoff.
5|Create a bounded reconciliation test query|A release check compares computed closing stock to a supplied control balance.|S1 computed12 control12; S2 computed4 control5|S1 pass; S2 discrepancy -1|A grand-total match could conceal offsetting SKU errors.
5|Expose source completeness with stock totals|A report joins counts from the movement file manifest before certifying totals.|manifest3 rows; loaded2 rows totaling5|loaded2 of3; stock total marked incomplete|A plausible numeric total is not complete evidence.
6|Detect a duplicated movement load|A rerun inserted the same source movement twice under different target row IDs.|source event M1 appears twice; M2 once|M1 duplicated by source identity; certified net excludes second copy|Target surrogate IDs do not prove source uniqueness.
6|Quarantine an unknown movement type|A provider sends a movement type that cannot be assigned a stock sign.|M1 receipt3; M2 adjustment_unknown2|M1 contributes +3; M2 reported unknown_type|Do not assume every unrecognized type is a receipt.
6|Detect a balance below zero|An issue would make the stock roll-forward negative under the supplied opening balance.|opening2; issue3|computed -1; negative_stock_exception|Do not clamp the value to zero and hide the evidence.
6|Identify a missing opening balance|A daily movement ledger exists but the starting stock snapshot is absent.|S1 receipt5; no opening balance row|S1 closing_unknown; movement_net +5 visible|Movement net is not a replacement opening balance.
6|Separate invalid units from valid zero|A source quantity field may be NULL, zero or positive.|M1 NULL receipt; M2 zero receipt; M3 three receipt|M1 missing_units; M2 valid zero; M3 +3|COALESCE on raw units would erase the missing-value fault.
6|Detect a reservation referencing a cancelled line|An order-line state changed after reservation creation.|O1/1 cancelled; reservation R1 holds2|R1 cancelled_line_exception|A valid join key does not make a reservation business-valid.
6|Recover a report from a duplicate join key|The product reference unexpectedly has two active rows for S1.|R1 S1 units2; catalog S1 has names Widget and Widget-New|reference_conflict S1; no certified one-row enrichment|DISTINCT can hide the conflicting source records.
6|Flag a late movement after snapshot close|A carrier posts an Oct1 stock issue on Oct3 after Oct1 was published.|Oct1 snapshot balance10; late issue -2 occurred Oct1 received Oct3|Oct1 frozen10; correction proposal8 with late-event lineage|Arrival date and effective stock date differ.
6|Keep a failing reconciliation visible|A generated query produces a nonzero control difference for one SKU.|S1 computed9 control10; S2 computed5 control5|S1 failed -1; S2 passed|Do not change the control value to make every check green.
7|Resolve effective catalog assignments|A SKU changes warehouse ownership on an effective date.|S1 owned L1 until Oct10, L2 from Oct10; movements Oct9 and Oct10|Oct9 assigned L1; Oct10 L2|A current catalog join misclassifies historical movements.
7|Separate reservation and shipment time axes|A line was reserved yesterday and shipped today; both metrics are required.|O1/1 reserved Oct1 3; shipped Oct2 2|Oct1 reserved3; Oct2 shipped2|A single date filter cannot represent both event types without labels.
7|Handle partial shipment across confirmations|A carrier confirms one order line in two separate packages.|O1/1 picked5; confirmations C1=2,C2=3|confirmed5; two package records|One-to-many confirmations must be aggregated before line comparison.
7|Find competing active reservation versions|Two updates claim to be current for the same reservation at one time.|R1 V1 holds2 active Oct1-5; V2 holds3 active Oct4-8; as-of Oct4|overlap_conflict R1; no certified current quantity|Ordering by latest update hides a validity overlap.
7|Compare as-known and corrected stock|A late backdated movement changes today's recomputation but not an earlier published report.|issue -2 effective Oct1 recorded Oct3; report published Oct2|as-known Oct2 excludes issue; corrected view includes -2|Validity and recorded-time cutoffs are both required.
7|Trace stock to source lineage|A disputed closing balance must list its opening snapshot and contributing movements.|opening10 from SNAP1; M1 receipt5; M2 issue3|closing12 with SNAP1,M1,M2 lineage|A number alone cannot explain a disputed stock balance.
7|Separate physical, reserved and available quantities|A warehouse has stock on hand and reservations; a report must show each metric.|S1/L1 physical10; reservations4|physical10; reserved4; available6|Available is not physical stock and may be negative under an exception.
7|Handle returns with explicit direction|A returned item adds salable stock only after inspection approval.|R1 return2 pending; R2 return3 approved|approved return +3; pending2 excluded from salable balance|A return receipt is not always available inventory.
7|Calculate a bounded service fill rate|A day has requested lines, fulfilled lines and cancelled lines.|10 requested lines; 7 fulfilled; 1 cancelled; 2 unfilled|fill rate 7/9 for non-cancelled demand|State the denominator; 7/10 answers a different question.
8|Inspect a stock lookup query plan|A large movement table is queried by SKU, location and date range.|generated 100000 movements; selective S1/L1/day filter|correct rows plus actual plan, timing and index use reported|An index is useful only if observed on the relevant workload.
8|Compare grouped roll-forward strategies|A planner recomputes balances from many movements and daily pre-aggregates.|100000 movements; daily aggregate table; same opening snapshots|same per-SKU/day balances; timings and refresh cost measured|Pre-aggregation that misses late movements is not equivalent.
8|Measure reservation join fanout|A report is slow because one line has many reservation updates.|100000 lines; hot line has1000 updates; current-only contract|one current row per line; fanout counts and plan measured|Do not remove history rows without preserving auditability.
8|Test a partial index for open reservations|Most reservations are closed but pickers query only open ones.|100000 reservations; 1000 open; query by SKU/location|same open rows; index size, plan and update cost recorded|An index on status alone may not match the actual filter.
8|Profile a selective shortage filter|A query finds rare shortages after aggregating reservation demand.|100000 lines; 100 shortages; two reservations per line|same100 shortage line keys; actual plan and memory recorded|Pushing a row-level filter before aggregation can change results.
8|Compare window and grouped current-state queries|A stock reference table has effective versions per key.|100000 versions; nonoverlapping intervals; as-of cutoff|same one version per key; plans, time and tie checks reported|Equal totals can hide different version choices.
8|Bound a recursive movement trace|An audit follows correction links in a finite chain.|M1 corrected by M2 corrected by M3; malformed cycle M4-M5-M4|M1 terminal M3; cycle flagged and bounded|A recursive query must not loop indefinitely.
8|Measure materialized report staleness|A daily stock summary is cached while new movements arrive.|summary refreshed09:00; issue -2 at09:05; query09:10|cached and live balances differ by2; age10 minutes reported|A faster cached query cannot claim live correctness.
8|Compare partition pruning on stock history|A dated movement table spans many months but report reads one month.|12 monthly partitions; October query; same rows in unpartitioned oracle|matching rows; actual scanned partitions and plan measured|Partition count alone does not prove pruning occurred.
9|Define a warehouse report contract|A stock report needs explicit grain, dates, types and completeness semantics.|candidate spec says total stock but omits location and pending returns|release blocked until grain/location/return policy stated|A correct sample total cannot resolve an ambiguous metric contract.
9|Gate a reservation query change|A candidate optimization passes most fixtures but misses split reservations.|line O1/1 requests5; holds2+2; candidate checks each row separately|candidate blocked; shortage1 retained|Required split-reservation behavior overrides average speed gain.
9|Audit report role access|Support may read shortage counts but not supplier prices in a joined warehouse view.|view includes count and confidential cost; support role query|support sees count only; direct table/view access tested|A hidden column in an application does not enforce database permissions.
9|Version a late-movement correction|An approved correction affects one prior stock date and dependent later balances.|Oct1 issue -2 posted Oct3; Oct1 and Oct2 snapshots published|revision IDs, affected dates and old/new balances recorded|Do not overwrite frozen snapshots without preserving old results.
9|Rebuild stock after target loss|A mart is deleted but opening snapshot and source movements remain.|opening SNAP1=10; receipt M1=5; issue M2=3; mart missing|restored balance12 with matching source IDs|Restoration from current product labels alone is insufficient lineage.
9|Reconcile source and target controls|A release process requires per-file and per-SKU row and unit controls.|file A three rows units7; target two rows units5|release blocked with row gap1 and unit gap2|A passing overall control from another file cannot mask this gap.
9|Investigate a false fill-rate gain|The new query excludes unfulfilled lines after an inner join.|old 7 fulfilled of9 active; candidate 7 of7|coverage defect identified; comparable rate remains7/9|Do not publish a 100 percent fill claim from filtered demand.
9|Plan retention for frozen stock reports|A held audit report depends on an old opening snapshot and movement corrections.|report R1 held; SNAP1 and correction M3 referenced; unlinked old SNAP0|SNAP1 and M3 retained; SNAP0 eligible after other checks|Keeping the report output alone may not permit reproduction.
9|Rehearse rollback of a stock rule|A candidate treats pending returns as available and is rolled back.|approved available6; candidate available8 from pending return2|approved6 restored; pending return still recorded for future approval|Code rollback must not delete legitimate new source events.
10|Independently build a reservation-aware stock mart|Produce dated stock, demand, availability and traceable exceptions for a bounded warehouse.|two SKUs, split reservations, returns, missing opening, late issue|correct grain and balances; unknowns visible; replay stable|Reviewer adds a second reservation after initial submission.
10|Independently diagnose an inventory discrepancy|Investigate a stock gap with duplicate loads, a missing manifest row and a late issue.|source files, snapshots, target and controls disagree by several units|causes quantified separately; safe correction plan and proof|Do not adjust a balance merely to force a control match.
10|Independently migrate SKU-location ownership|A warehouse changes ownership rules while old movements and reports remain auditable.|old/new effective catalog, overlapping bad rule, frozen historical report|overlap blocked; old report reproducible; new rule applied prospectively|A present-day catalog join is not historical truth.
10|Independently tune a high-volume pick query|Optimize rare-shortage lookup on skewed reservations under correctness gates.|million lines; hot SKU; split reservations; memory and latency budgets|same shortage keys as oracle; actual plans and measured resources|Performance evidence must include index maintenance tradeoffs.
10|Independently recover a frozen warehouse report|Restore lost target results from held opening snapshots, movements and versioned business rules.|one corrupt source file; late correction; old and current report versions|recoverable balances verified; corrupt gap explicit; old/current separated|A known aggregate does not reconstruct missing row identities.
10|Independently audit a service-level claim|Assess a claimed pick-rate improvement after order cancellation and SQL join changes.|old/new demand, cancellation records, missing confirmations|comparable cohort, denominator and coverage effects demonstrated|A lower exception rate may reflect dropped cases.
10|Independently design a warehouse incident drill|Create and solve a case covering data loss, wrong stock, reservations and access boundaries.|business brief with raw lineage, frozen report, recovery target and privacy rule|working SQL artifacts, fault results and unresolved uncertainty reported|Writing a drill and independently handling a changed fixture are distinct evidence.
10|Independently defend a temporal stock model|Explain and implement effective time, recorded time and publication cutoff for one correction history.|backdated receipt, later correction, report before correction, current report|both reports reproducible with exact source versions|One timestamp cannot answer all historical questions.
10|Independently validate a production query rollout|Run correctness, performance, permission and rollback checks before a stock-report query change.|candidate query; split reservations; skew; confidential cost; rollback artifact|all required checks observed; candidate blocked on any critical regression|A passing unit fixture cannot substitute for an end-to-end release gate.
''')


def problem(tool: str, prefix: str, number: int, row: tuple, parent: str) -> dict:
    level, title, scenario, fixture, expected, boundary = row
    pid = f"RLP-{prefix}-{number:03d}"
    method = "Python implementation" if tool == "python" else "SQL query or script"
    return {
        "id": pid, "tool_id": tool, "title": title, "level": level,
        "difficulty": f"level_{level}", "sequence": level * 1000 + number,
        "scenario": scenario,
        "task": f"Using the supplied fixture, produce the stated result for this data engineering task: {scenario}",
        "learning_objective": title,
        "inputs": {"fixture_contract": fixture,
                   "environment": "Use only synthetic data and learner-owned disposable resources."},
        "expected_output": {"contract": expected},
        "constraints": [boundary, "Retain original source rows and identify the output grain."],
        "acceptance_criteria": [
            f"Show the actual {method}, its execution result and how the result matches: {expected}",
            f"Check this business boundary with a separate case: {boundary}",
            "State any assistance used; an expected answer without executed evidence does not verify completion."
        ],
        "prerequisites": [parent], "independent_prerequisites": [],
        "skill_prerequisites": [],
        "progressive_hints": [
            f"Find the smallest source row or key in this fixture; name the output grain for {title.lower()}.",
            f"Work through the stated boundary using one changed row: {boundary}",
            "Compare each intermediate row and count with the expected result, then isolate the first mismatch."
        ],
        "engineering_relevance": f"Warehouse event and stock pipelines need {title.lower()} so operators can trust published results and diagnose exceptions.",
        "estimated_minutes": min(180, 10 + level * 13),
        "official_docs": (["https://docs.python.org/3/library/csv.html",
                           "https://docs.python.org/3/library/datetime.html"] if tool == "python" else
                          ["https://www.postgresql.org/docs/current/queries.html"]),
        "verification": {"kind": "artifact_review"},
        "challenge_kind": "initial", "topic_id": None,
        "publication_status": "published", "published_version": "2026.10.27.6",
        "authoring_batch": "foundations-explicit-005",
        "followup": {"inputs": "Learner receives a changed row/key and boundary value after submitting the first solution.",
                     "expected_output": "Predict the changed result before rerunning; review observed output and assistance separately."}
    }


def main() -> None:
    published = json.loads((ROOT / "tools/curriculum.json").read_text(encoding="utf-8"))
    checkpoint = {"status": "new_append_only_content_frozen", "tools": {}}
    for tool, prefix, start, target in (("python", "PY", 366, 85), ("sql", "SQL", 352, 99)):
        rows = ROWS[tool]
        assert len(rows) == target, (tool, len(rows))
        assert [row[0] for row in rows] == sorted(row[0] for row in rows)
        existing = [p for p in published["problems"] if p["tool_id"] == tool]
        for suffix in ("", "-batch2", "-batch3", "-batch4"):
            existing.extend(json.loads((BANK / f"{tool}{suffix}.json").read_text(encoding="utf-8")))
        assert max(int(p["id"].rsplit("-", 1)[1]) for p in existing) == start - 1
        latest = {level: max((p for p in existing if p["level"] == level),
                             key=lambda p: int(p["id"].rsplit("-", 1)[1]))["id"]
                  for level in range(11)}
        result = []
        previous = None
        for number, row in enumerate(rows, start):
            level = row[0]
            parent = (previous["id"] if previous is not None and
                      previous["level"] in (level, level - 1) else latest[max(0, level - 1)])
            item = problem(tool, prefix, number, row, parent)
            result.append(item)
            latest[level] = item["id"]
            previous = item
        assert len({p["id"] for p in result}) == target
        assert len({p["title"].casefold() for p in result}) == target
        destination = BANK / f"{tool}-batch5.json"
        content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if destination.exists() and destination.read_text(encoding="utf-8") != content:
            raise RuntimeError(f"Frozen batch would change: {destination}")
        destination.write_text(content, encoding="utf-8")
        checkpoint["tools"][tool] = {
            "new": target, "first_id": result[0]["id"], "last_id": result[-1]["id"],
            "total_if_registered": start + target - 1, "target": 450,
            "sha256": hashlib.sha256(destination.read_bytes()).hexdigest()
        }
    path = BANK / "authors/foundations-batch5-checkpoint.json"
    content = json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") != content:
        raise RuntimeError(f"Frozen checkpoint would change: {path}")
    path.write_text(content, encoding="utf-8")
    sys.path.insert(0, str(ROOT / "apps/recalllab"))
    from services.curriculum import load_curriculum
    from services.bank_validation import audit
    combined = load_curriculum(ROOT)
    known = {p["id"] for p in combined["problems"]}
    for tool in ("python", "sql"):
        for item in json.loads((BANK / f"{tool}-batch5.json").read_text(encoding="utf-8")):
            if item["id"] not in known:
                combined["problems"].append(item)
                known.add(item["id"])
    for technology in combined["technologies"]:
        technology["published_total"] = sum(p["tool_id"] == technology["id"] for p in combined["problems"])
    report = audit(combined)
    defects = {key: len(report[key]) for key in (
        "missing_fields", "duplicates", "similar_task_candidates",
        "broken_prerequisites_and_structure", "job_ready_pathway_errors")}
    print(json.dumps({"combined_published_total": report["published_total"],
                      "python": report["technology_counts"].get("python"),
                      "sql": report["technology_counts"].get("sql"),
                      "defects": defects}, indent=2))
    if any(defects.values()):
        raise RuntimeError("Combined bank audit found defects")
    print(content)


if __name__ == "__main__":
    main()
