## SQL stored-procedure reference saved - 12 November 2026 IST

<!-- CP-20261112-sql-procedure-reference -->
Prepared requested stored-procedure reference: PostgreSQL and Oracle creation/calls, IN/OUT/INOUT parameters, missing-order errors, caller-owned rollback, functions versus cursors, cleanup and permissions. Official documentation checked; examples show expected output only, with separate unanswered recall prompts. No live database execution, learner attempt, assessment, review completion, timer change or RDS-001 acceptance. Added one unassessed concept with an adjustable initial diagnostic slot; existing review dates preserved. Next: Lesson 4 source inspection: list raw base tables, then inspect raw_hosts columns and sample rows before writing src_hosts.

[Stored procedure notes](Notes/SQL/stored-procedures.md). Earlier pending work remains below.

## SQL cursor reference saved - 10 November 2026 IST

<!-- CP-20261110-sql-cursor-reference -->
Created requested SQL cursor notes: PostgreSQL DECLARE/FETCH/CLOSE, batches, position, transaction lifetime and memory limits; Oracle explicit and FOR loops; distinction from Python cursors. Runnable examples with expected output and separate unanswered recall prompts. Official documentation checked; no live database execution, learner attempt, scored review, timer change or task acceptance. Reused unassessed pg.cursor.results mapping and preserved existing review dates. Next: Lesson 4 source inspection: list raw base tables, then inspect raw_hosts columns and sample rows before writing src_hosts.

[Cursor notes](Notes/SQL/cursors.md). Earlier pending work remains below.

## CROSS JOIN details saved - 9 November 2026 IST

<!-- CP-20261109-cross-join-details -->
Expanded the requested CROSS JOIN reference with every-pair output, row-count multiplication, empty inputs, duplicates, NULL values, WHERE filtering, INNER JOIN comparison and practical uses. Tutor-prepared reference with expected output only; no SQL execution, learner attempt, score, review-date change, task acceptance or timer change. Existing SQL concept mappings reused; content expansion flagged for future assessment. Next: Lesson 4 source inspection: list raw base tables, then inspect raw_hosts columns and sample rows before writing src_hosts.

[SQL notes](Notes/SQL/learning-notes.md#cross-join-every-combination). Earlier pending work remains below.

## SQL join reference saved - 5 November 2026 IST

<!-- CP-20261105-sql-join-reference -->
Prepared requested SQL join reference: INNER, LEFT, RIGHT, FULL OUTER, CROSS and self joins, matching keys, repeated matches, NULLs and ON versus WHERE, with small PostgreSQL examples and expected output. Reference preparation only; no learner attempt, execution, score, review schedule or timer change. Existing SQL concepts reused. Next: Lesson 4 source inspection: list raw base tables, then inspect raw_hosts columns and sample rows before writing src_hosts.

[SQL notes](Notes/SQL/learning-notes.md). Earlier pending work remains below.

## dbt connection and project follow-up saved - 4 November 2026 IST

<!-- CP-20261104-dbt-followup-notes -->
Saved dbt Lessons 2-3 follow-up notes from the chat: connection fields, default/overridden/missing targets, source versus destination, object creation, project names/version, seeds, analyses, generated files, test failure storage, and table materialization. Learner restated the destination-schema role; other examples and commands were tutor explanations. Read-only TESTING inspection verified project metadata and absent target folder. No dbt/database execution, scored assessment, mistake event, task acceptance or timer change. Existing concept IDs and review schedules preserved.

Next: Lesson 4 source inspection: list raw base tables, then inspect raw_hosts columns and sample rows before writing src_hosts.

[Updated lesson notes](Notes/dbt/Index.md); [session evidence](progress/dbt/2026-11-04-followup.md).

## dbt Lessons 1-3 notes saved - 4 November 2026 IST

<!-- CP-20261104-dbt-lessons-01-03-notes -->
Saved the requested three lesson notes under Notes/dbt with an index and separate answer-free recall prompts. Three lessons are not three verified study days. Learner explained dbt/PostgreSQL/Airflow roles and answered profile/target/schema questions. Tutor refined execution responsibilities and schema-creation permissions. Learner identified model dependency; materialization and YAML version/purpose needed explanation. Immediate predictions: not_null fails for 1/NULL; unique passes. Help beyond the conversation is unknown; no independent model execution, scored review or delayed retention claimed. Five note concepts have unassessed diagnostic planning slots only; older review schedules preserved. Project-local log inspected in the TESTING checkout shows successful connection check at 18:38:48 on 4 November, superseding the older pending-connection summary. No fresh connection/test execution during this save.

Next: Lesson 4 source inspection: list raw base tables, then inspect raw_hosts columns and sample rows before writing src_hosts. Lesson 3 predictions were reviewed; materializations and tests remain practical work for later lessons. Airbnb plan has 40 lessons (36 practical plus 4 extensions), separate from preserved RRDAP/API/Python work. Timer unchanged by this notes-only save; read canonical study-log.csv before any timer action.

Notes: [dbt index](Notes/dbt/Index.md). Project location: C:/Users/SATISH/GIT/TESTING/dbt_practice/airbnb_dbt.

## dbt study started - 4 November 2026 IST

<!-- CP-20261104-dbt-start -->
Study interval DBT-20261104T184454 started at 18:44:54 IST on the learner's explicit start instruction. Running time is excluded from confirmed totals. Earlier uncertain intervals remain excluded; no overlap with a running session.

Learner selected dbt on the laptop with PostgreSQL at 192.168.1.195 on the reported home server. Tutor explained dbt debug and profile/target selection. Logs showed an initial password authentication failure, then debug invoked from the parent folder with an internal missing-profile error. Correct project directory identified as C:/Users/SATISH/GIT/TESTING/dbt_practice/airbnb_dbt. No later successful connection output or independent assessment verified. Course name/link not supplied. No credentials copied into learning records.

Exact next step: run dbt debug inside the airbnb_dbt project directory and inspect the connection result; supply the course name/link to align the next practical task. Earlier API, Python and RDS-001 work stays pending.

# Start here - API paused for SQL, 3 November 2026 IST

## AI fine-tuning notes saved, 3 November 2026 IST

<!-- CP-20261103-finetuning-memory-notes -->
Saved requested fine-tuning terminology, quantization and RAM/VRAM explanations from this conversation. Desktop hardware inspected: i7-12700K, 16 GB RAM and RTX 3050 with 6 GB VRAM verified by nvidia-smi. Learner reports using Qwen3 4B; no model benchmark, training run, independent concept assessment or answered epoch prompt supplied. Three new concepts receive unassessed diagnostic planning slots only; existing review dates and timers preserved. API/SQL, pathlib, reminder collector and RDS-001 pending work remain unchanged.

[Explanation note](Notes/AI/fine-tuning-and-model-memory.md); [unanswered recall questions](Notes/revision/fine-tuning-questions.md).

Optional AI follow-up: explain why a four-bit 4B model keeps its parameter count and needs more runtime memory than its download size, stating help used.

## API paused; SQL selected - 3 November 2026 IST

Saved the 12-lesson API course and paused API-L01 after tutor explanation; the request/response exercise is unanswered. Learner reports Python study finished and SQL study now; no SQL task/output, duration, independent assessment or review event supplied. No running study-log row; timers unchanged. Next API step: Resume API-L01 by answering the saved order request/response task.

[API course](plan/api-lessons.md); [session evidence](progress/api/2026-11-03-session.md).
Earlier pathlib follow-up and RDS-001 remain pending. SQL task not specified in this chat.

## API course prepared, 3 November 2026 IST

[12 API lessons](plan/api-lessons.md) are ready as a separate learning sequence, from
request/response basics to reliable ingestion and a small local API. Course entry:
API-L01, interpret the fictional order request/response and change its query.
Say "Teach API lesson 1" to begin without starting a timer. Preparation only: no
lesson attempted, assessment or review-date change. The existing pathlib follow-up
and RDS-001 remain pending; the course does not replace their saved work.

## pathlib follow-up notes saved, 3 November 2026 IST

<!-- CP-20261103-pathlib-followup-notes -->
Expanded the existing pathlib note from this chat: path object versus open file, pathlib classes, Windows separators/raw strings, directly defined relative paths, cwd versus resolve, and same-location file/folder collisions with mkdir. Tutor explanations supplied; collision behaviour checked in a temporary directory. No new learner execution, independent score, delayed review or timer event. Existing notebook evidence and py.paths.imports review dates preserved; RDS-001 unchanged. Next: Using an existing notebook path, print its full address, parent, name, stem, suffix, is_file and is_dir; share the output and explain where relative paths start, stating any help used.

## pathlib notes saved, 3 November 2026 IST

<!-- CP-20261103-pathlib-notes -->
Saved pathlib notes covering absolute/relative paths, cwd/resolve, joining, path properties, existence/type checks, mkdir parameters, text reading/writing, searches, changed addresses and relative_to. Working notebook outputs show practice; its inconsistent earlier backslash cell is preserved without claiming successful execution. Tutor examples/help supplied; other assistance unknown. No independent score, delayed review, timer event or RDS-001 acceptance. Existing concept py.paths.imports reused; review dates preserved. Next: Using an existing notebook path, print its full address, parent, name, stem, suffix, is_file and is_dir; share the output and explain where relative paths start, stating any help used.

Notes: [pathlib](Notes/Python/Concepts/pathlib.md). Evidence: [saved practice](progress/pathlib/2026-11-03-session.md).

Earlier JSON, concurrency, AI and RDS-001 pending work is preserved below.


## JSON notes saved, 30 October 2026 IST

<!-- CP-20261030-json-notes -->
JSON notes saved, 30 October 2026: JSON versus dictionaries/text/files, four conversion functions, nested access, useful formatting/number options, invalid JSON and completed CSV-to-JSON conversion. Saved notebook and orders.json show integer IDs, float amounts, four records and earlier order total 650. Tutor examples and feedback supplied; extra help unknown, no independent or delayed score. Decimal parsing was explained but not demonstrated in learner code; changed-customer follow-up unverified. Two concepts mapped with unassessed diagnostic planning slots only. Existing review dates, timers and RDS-001 acceptance unchanged.

Notes: [JSON](Notes/Python/Concepts/json.md). Evidence: [saved practice](progress/json/2026-10-30-session.md).

Next: Choose one next JSON task on missing fields and invalid values, or explicitly switch to pandas; no new exercise has been selected.

Previous concurrency, AI and RRDAP pending tasks are preserved below; no completion is implied.

## Python concurrency notes saved, 29 October 2026 IST

<!-- CP-20261029-concurrency-notes -->
Saved guided concurrency/API practice and explanations are summarized in [the attempt handoff](progress/concurrency/2026-10-29-session.md). Notes: [threads](Notes/Python/Concepts/multithreading.md), [processes and GIL](Notes/Python/Concepts/processes-and-gil.md), [async and await](Notes/Python/Concepts/async-await.md), and [API requests](Notes/Python/Concepts/api-requests.md). [Recall questions](Notes/revision/concurrency-questions.md) are unanswered. No independent review score, retention due date, RDS-001 acceptance or timer event was added. The AI reminder collector and RDS-001 remain separately pending.

Next: Compare two scheduled async jobs using await asyncio.sleep(2) and time.sleep(2); share code, output, and why timing differs.

## AI reminder checkpoint, 28 October 2026 IST

<!-- CP-20261028-ai-reminder-baseline -->
AI reminder baseline and guided collector saved. Four learner-reported outputs for the same soak-nuts reminder failed exact field extraction, including fresh-session time=daily; these are model errors, not learner misconceptions or a general benchmark. Latest learner code collects task, time and recurrence, prints the first two and discards recurrence.upper(); no collector execution output or corrected attempt supplied. Tutor supplied initial input/strip code and later hints. Learner explicitly requests one step at a time and writes all project code. Notes cover inference versus training, prompting, LoRA, baseline checking and input-target data generation; all three AI concepts remain unassessed with planning slots only. No training, mobile deployment, notification or dataset generation completed. Timer and confirmed hours unchanged. RRDAP RDS-001 and earlier Python follow-up remain pending. Next: Update the recurrence input to retain a lowercase answer and display task, time and recurrence; run with YES and share the actual output.

Evidence: [AI session and attempts](progress/ai-reminder/2026-10-28-session.md); [Obsidian explanation note](Notes/AI/reminder-model-basics.md). The source project remains C:/GIT/AI/FineTuning/reminder_assistant/collect_example.py; its exact inspected snapshot is preserved in the learning repository. Phone Android version is unverified. No learner project file was edited. Resume the AI collector for this chat; preserved RRDAP work below is a separate task.


## RecallLab bank expansion, 27 October 2026

Infrastructure status: **4,213 published problems** meet all 4,200 allocated targets; 243 drafts remain excluded. [Actual counts and verification limits](apps/recalllab/BANK-EXPANSION.md) are recorded separately. This adds no learner completion, score, review date or study time; the exact pending Python and RDS-001 tasks below remain unchanged.

## Current planning revision, 26 October 2026

Job-readiness assessment is now **20 January 2027**, superseding the January 22 dates in older entries below. Foundation, PySpark and Azure demonstrations target November 15, December 6 and December 27. [The existing roadmap](plan/learning-and-revision-plan.md) remains authoritative. RecallLab Tools implementation creates no learner evidence, study time or RDS-001 acceptance. Continue the exact pending Python/RRDAP work below; implementation state is in [the app handoff](apps/recalllab/HANDOFF.md).

<!-- CP-20261026-dataclass-special-method-notes -->
Dataclass and special-method reference notes saved, 26 October 2026. Added Notes/Python/Concepts/dataclasses.md and special-methods.md with one standalone example per method; updated objects-and-printing.md, Python index and separate recall prompts. Inspected practice/Dataclass/dataclass.ipynb and its saved outputs (string order_id, equality, reversed __lt__, negative __len__, item access); assistance/independent understanding unknown. Attached snapshots were inaccessible and unchanged. No scored review, timer change or task acceptance. Two new concepts remain unassessed with adjustable initial slots, not retention due dates. Examples were not rerun during the original note save. Publishing verification on 26 October refreshed the note inventory and passed coach validation; no learner assessment was added. Next Python step: practise one method at a time, starting with __repr__ and __str__, and explain actual output/help used. Earlier returned-summary verification remains pending; RDS-001 remains the pending project task.

Morning study reported, 26 October 2026: three Pomodoro sessions completed on another computer. Recorded as POM-20261026-OTHER-MORNING-1 through -3; topic, duration and exact IST times not supplied, so confirmed hours are unchanged. These are reported completions, separate from local extension counts; no timer or learning assessment started. Confirm the topic and interval times when available. Continue the existing pending Python verification and RDS-001 task.


Decimal notes saved, 25 October 2026: added Notes/Python/Concepts/decimal-money.md with matching import syntax, CSV string conversion, integer quantities, Decimal totals and default half-even versus explicit half-up rounding. Four tutor examples executed. Latest learner code now returns counts, uses Decimal for prices, and collects results outside before one combined write; no output supplied and outside printing is not shown. This supersedes the earlier global-list/no-return snapshot; no independent assessment or acceptance claimed. Next Python step: print each returned dictionary and verify the original reports plus counts against actual inputs. No timer or existing review-date change. RDS-001 remains the pending project task.

Function-result logic notes saved, 25 October 2026: added Notes/Python/Logic/collect-function-results-write-once.md with simple traces for per-call lists, dictionary update versus append, return versus print, and writing one combined batch report. Both tutor examples executed. Latest learner snapshot uses a global results list and rewrites the full growing list; no return/outside print or execution output, so the original task is not accepted. Immediate Python follow-up: return each input counts dictionary without global state, retain the three original reports, print outside, and collect returned dictionaries for one combined write. No timer, scored review or due-date change. RDS-001 remains the pending project task.

Order-summary logic note saved, 24 October 2026: created Notes/Python/Logic/order-summary-after-loop.md with grouping by status, running totals, order count versus quantity and writing after the loop. Tutor worked example executed in memory. Learner split-file read-back output supplied; final summary implementation/output still unverified. Optional immediate Python follow-up: reconstruct the changed-input recall task and show the summary, stating help used. No timer or review completion recorded; RDS-001 remains the pending project task.

Two-context-manager notes saved, 24 October 2026: added copying a CSV with two files in one with statement, automatic closing, and separate write-then-read blocks for the same file. Tutor explanation and unanswered recall prompt only; no learner attempt assessed, timer change or review-date change. Pending project action remains unchanged.

Python notes saved, 24 October 2026: learner asked whether repeated dictionary keys overwrite values and how to keep several CSV rows. Added update-versus-append examples and an answer-free recall task. The supplied completed-orders CSV has three data rows (1001, 1003, 1004), not five. Explanations are tutor-supplied; no independent collection attempt, score, review completion or study time recorded. Optional Python follow-up: try the collection example and explain its row count. Prior Docker clock times remain unresolved; no timer is running. RDS-001 stays the pending project task.

Learner chose Docker study today. Three completed 25-minute Pomodoros and three 5-minute breaks were reported; `DOC-20261022-POM1` through `DOC-20261022-POM3` in `tracking/study-log.csv` total 75 minutes of reported focus, pending exact IST start/end times and excluded from confirmed hours. Breaks are excluded. No Docker work/output has been supplied. No timer is running. Confirm interval times, then continue the learner's Docker work. RDS-001 stays the pending RRDAP project task; no acceptance or review status changed. Excel snapshot refreshed for 22 October.

## Current state

Planning updated **22 October 2026**: [single Azure interview roadmap](plan/learning-and-revision-plan.md), 13 weeks from 22 October plus 21â€“22 January buffer, assessment **22 January 2027**. Date-effective 7-hour weekdays/10-hour weekends = 55 hours/full week; historical targets preserved. This transition week is 52 h. Today/week confirmed logged hours **0**, prior overall confirmed **11h09m05s**, uncertain interval excluded. No learning assessment, acceptance, review-date change or new timer from this infrastructure upgrade. Excel refreshed for 22 October. Start interview practice and Show my weaknesses use the existing five roles/records. [RecallLab](apps/recalllab/README.md) was found in a newer remote commit and integrated; shared schedule, roadmap/project/interview views added while preserving revision/coding/persistence. No public deployment.

**Real-Time Retail Distribution & Analytics Platform (RRDAP)** is active, replacing RetailFlow. **RDS-001 Product Catalogue** is in progress: Faker/commerce generator and a 1,000-record CSV found under projects/rrdap/Test; PostgreSQL loading and SQL verification remain pending. PostgreSQL is available per learner report; task connection unverified. Read [main checkpoint](progress/current.md), [project checkpoint](projects/rrdap/checkpoint.md), [current task](projects/rrdap/tasks/RDS-001.md) and [tutoring workflow](reference/rrdap.md).

## Exact next task

RDS-001: Propose an approach or independently implement the 1,000-product PostgreSQL catalogue, then submit code and SQL verification against the six acceptance criteria.

## Timer and handoff

Study timer **paused since 17 October at 21:27:54 IST**. **RDS-20261017T205651** closed: **20:56:51-21:27:54 = 31m03s**. Historical 17 October confirmed **6h39m08s**; first partial week **11h09m05s / 32h target**. RRDAP confirmed closed time **2h44m34s**; prior RetailFlow/Python time separate. No running timer; do not count the gap as study. Exact next task unchanged.

RetailFlow files/history preserved as superseded; RF-001 uncompleted. Earlier CSV output/read-back and SQL-003 remain deferred. Preserve actual attempts, notes, mistakes, skill evidence and review schedules; project setup adds no scored learning. New notebooks inspected for requested notes; saved outputs show practice, with assistance unknown. [Python notes](Notes/Python/Index.md) now include CSV writing, file methods, objects and random, plus targeted dictionary/CSV reading updates. Examples ran in scratch space; no scored review, completed project task or changed timer.

One tutor coordinates five roles. Give one business task; learner designs/codes/debugs. No future pain-point spoilers or forced technologies. November 30 first end-to-end flow is a stretch target; long-term volume objectives require measured capacity. Lab/service availability is user-reported, not verified. No large datasets, services or pipeline implementation generated.

Use Start Distribution Project / Continue Distribution Project to load the next task without another timer. Save my learning saves; End session saves and closes the study interval. Existing timer commands and explicit checkpoint boundaries remain. Update both main handoffs and project checkpoint together; canonical trackers remain shared. No background agents. The current upgrade request authorizes its scoped feature branch/PR only; future study publishing or deployments still need authorization.

Faker follow-up: [Faker notes](Notes/Python/Concepts/faker.md) capture customer generation, locale, commerce provider, the price-argument issue and extra CSV blank rows. Learner notebook/data preserved; no task acceptance, independent score or timer change.

## AI notes saved, 28 October 2026

[AI notes](Notes/AI/Index.md) and [session evidence](progress/ai-reminder/2026-10-28-session.md) capture today's reminder-model exploration and collector practice. No independent assessment or training completed.

Next AI task: Update the recurrence input to retain a lowercase answer and display task, time and recurrence; run with YES and share the actual output.

Earlier Python follow-ups and RDS-001 remain pending.
