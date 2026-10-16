# Start here - 16 October 2026 (IST)

## Current state

Python paused at **12:00:15 IST**. Today's intervals: 09:40:20-10:27:42 (47m22s), 10:34:47-10:51:42 (16m55s), 11:30:47-12:00:15 (29m28s). Confirmed today **1h33m45s**, target 6h, remaining **4h26m15s**. Partial week **4h22m19s / 32h**. Breaks excluded. Old 15 October 08:11:20 interval needs confirmation and is excluded. Excel refreshed for 16 October; CSV is authoritative.

## Reviewed Python work

- Dictionary/list/conversion/copy foundations and per-record ValueError handling practised with guidance; earlier snapshots and feedback preserve failures/help.
- Notebook now defines working clean_orders(orders): local fresh lists, parameter-based loop, copied output records, integer conversion, invalid original/reason retention and both returned lists.
- Saved output checks original five orders (3 valid, 2 rejected), unchanged original input, different input (401 -> integer 75), blank/spaces/zero, repeated calls and empty input. Guided success; no independent reconstruction or delayed retention claim.
- CSV reading uses import csv, with open and csv.DictReader. Five input rows yield 3 valid and 2 rejected as detailed in review. order_id remains a string intentionally. Original notebook uses an absolute Windows path; adjust to the actual working folder on another machine.
- Pending CSV writing is not a completed pipeline. Historical attempt.py is not the current working solution and must not be repaired automatically.

Evidence: tools/python/exercises/10-16-2026 Dict.ipynb; immutable snapshot attempts/012-function-and-csv-pause.ipynb and attempts/012-function-and-csv-review.md under tools/python/exercises/001-record-cleaning; source files/orders.csv under that exercise.

## Exact next task

Write valid_orders.csv with columns order_id,amount and rejected_orders.csv with columns order_id,amount,reason from the CSV cleaner results. Use csv.DictWriter, writeheader(), writerows(), mode "w" and newline="". Leave source orders.csv unchanged. Read both outputs back using DictReader and display contents; submit code/output and help used. This task is assigned, not completed.

## Reviews and teaching

Use a bounded SQL-002 COUNT/NULL review after the current Python block; SQL-001/002/003 remain due 16 October. Python cleaner/functions/CSV assisted application review due 17 October. Do not dump the whole queue. No delayed review has been answered. Follow actual queue/history and notes-driven revision mappings. Missing prediction/help declarations are not independence.

One meaningful task at a time. Preserve attempts and keep hints separate. Explain simply with small examples. Follow reference/checkpoints.md: ordinary done replies/reviews do not save trackers; pause/resume/start-study, explicit topic switches, save/finish and device/session handoffs consolidate only meaningful new evidence. Explicit requested note/config writes remain authorised. Resume starts a new interval only on an explicit command. No background agents or timer alerts.

## Goal and durable records

India data engineering role-switch target February 2027, 15 LPA aspiration, neither guaranteed. Plan: 16 weeks 19 October-7 February, six-hour weekdays/ten-hour weekends (50h full week), one Azure concept weekly; Docker inside project hours. Prior experience four years support plus one development, separate from DE project experience. 90-day notice; possible 30 November resignation unconfirmed. No Azure/Snowflake access confirmed; begin locally.

Read AGENTS.md, reference/learning-coach.md, reference/checkpoints.md, plan/learning-and-revision-plan.md, current checkpoint/handoff, recent progress/session-history.md, tracking queues/mistakes/skill-state and actual attempts. Use repository-relative paths. Notes/ contains explanations; Notes/New Syntax/ is the requested useful-syntax collection. Canonical CSV/JSON trackers own evidence/schedules; generated Notes/revision views do not create success.

No commit/push is authorised by this checkpoint. Save before switching devices; transfer latest files through an authorised Git sync. Git does not transfer databases, installed tools or credentials.
