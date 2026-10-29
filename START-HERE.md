# Start here - concurrency notes saved, 29 October 2026 IST

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
