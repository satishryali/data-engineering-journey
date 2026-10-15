# Current tutoring checkpoint

Last updated: 15 October 2026 (IST).

## Goal and constraints

India data engineering switch targeted February 2027, about 15 LPA aspiration (not guaranteed). Electrical engineering education; four years support plus one development, separate from data engineering project experience. Notice period 90 days; considering resignation 30 November, resignation/last date unconfirmed.

Target 50 study hours/week: six weekdays, ten weekends; breaks separate. Azure one weekly concept; Docker within project hours. Tools reportedly on server, not independently verified; no Azure/Snowflake access, willing to pay later. Adapt scope to actual progress/sustainable time.

## Evidence so far

- SQL-001: join-preservation prediction/query reasoning and changed-example outputs correct independently; reconstruction spelling help recorded. Initial success 15 October, early retrieval 16 October; no retained-mastery claim.
- SQL-002: initial counting/grouping practice completed with COUNT/NULL, join-key and grouping-grain hints. Correct supplied changed/duplicate-name outputs. Unaided retrieval 16 October; independent-success anchor unset.
- SQL-003: Asha total 1000 correct; Nila-zero prediction wrong. After rule explanation, correctly answered COUNT=0/SUM=NULL on all-NULL input. No totals query/output yet; setup deferred.
- PY-001: cleaner attempts show dictionary key/value, record access, accumulation and conversion gaps. Reviewed earlier run produced empty valid dict and overwritten invalid entry. Tutor gave items()/record access, list and int()/ValueError hints. Learner revised but still struggled; no correct cleaner/function demonstrated. Expected output shape supplied on request; implementation not given.
- PY-002: dictionary refresher requested. Tutor explained one record, keys/values, access and items() pairs. No learner refresher attempt yet. No integrated project complete; initial revenue date/year/filter gaps remain unassessed.

## Exact next task — dictionaries in Jupyter

Use tools/python/exercises/001-record-cleaning/dictionary-refresher.md. Starting from order = {"order_id": 101, "amount": "500"}, learner prints amount, updates it to string "750" and prints dictionary, submitting code/output together. No loops/conversion/exception handling yet. All timers paused at 14:59:45 IST; await explicit resume. No notebook code/output submitted during this block. Use progressive help from this demonstrated gap, then reconstruction/changed record and eventually return to cleaner. Do not restart SQL or the whole course.

Preserve cleaner attempt.py and attempts/002-pause-draft.py, 003-pause-draft.py. feedback.md holds prior help. Latest draft mutates order_id, retains items loop/type errors and calls value(); not run/reviewed with learner yet. Do not overwrite it with tutor solution. New dictionary exercise attempt can use a separate file when learner begins.

## Deferred SQL

Resolve exercise 003 setup before totals query. Supplied invalid INSERT into old orders(amount) had unfinished VALUES/WHERE syntax. Exact statement/error in exercise 003 attempt.sql. Provided original orders schema lacks amount; newly found tools/postgresql/setup.sql contains learner scratch ALTER/attempts, so actual live schema must be verified rather than assumed. Don't run scratch file wholesale.

Later run tools/sql/exercises/003-customer-totals/setup.sql in one connection for separate temporary revenue_customers/revenue_orders, share result/error, then learner writes customer-ID/name/SUM report preserving all customers and leaving unmatched totals NULL. No COALESCE/date/status solution given yet. Earlier sample last reported five customers/five orders; temporary state may vanish on reconnect.

## Timer and Excel

All timers paused at 14:59:45 IST on 15 October. Latest Python interval 14:14:07–14:59:45: 45m38s, dictionary practice in Jupyter. Completed today/week 2h48m34s (SQL 1h30m56s, Python 1h17m38s). Remaining today 3h11m26s toward six hours. Resume starts a new row. Older 08:11:20 interval needs_confirmation, stop unknown and excluded. Never infer study from silence or count overlapping intervals.

tracking/study-log.csv is authoritative. Excel outputs/study-tracker/study-hours.xlsx refreshed 15 October to completed 2h48m34s, excluding uncertain/running time. Rebuild with tracking/update-study-tracker.mjs after log changes, status requests and daily handoff; flag stale if unavailable. First partial week 32h from 15 October, full weeks 50h. Closed-day shortfall separate from today's remaining target.

ClockIt octech.clockit v1.9.0 installed locally; ignored settings disable auto-start/cloud and select CSV. Learner prefers tutor-managed message-controlled tracking. No importer/tested focus alert/reminder configured; duration/delivery still unagreed. Don't promise an alert without setup.

## Pacing, records and handoff

One meaningful bounded task at a time; combine prediction/code/output, review actual work and use micro-questions only for gaps. Dictionary refresher explicitly requested. Avoid repeated trivial confirmations; don't infer proficiency from preference/familiarity/time.

Batch learning records at task completion, pause/topic switch, explicit Save checkpoint, Finish or Finish for today; no file writes after each ordinary answer/hint. Timer events recorded immediately. Interim work stays in conversation until checkpoint. Save before closing/switching devices; no background/parallel writer or midnight execution. Preserve attempts and assistance history; no spaced review attempted today (revision-history.csv unchanged).

Queue: SQL-001 retrieval, SQL-002 unaided reconstruction, SQL-003 SUM/NULL and PY-001 early practice due 16 October; PY-002 no success/review date yet. Prioritise dictionary foundations before the full cleaner; do not dump the whole queue at once. Schedule is flexible around actual learning, not elapsed dates.

START-HERE.md is the entry point; README.md has commands/sync/Excel instructions. Latest explicit request: commit and push current changes. Last previous verified push 9481e9e; Git history/remote will establish this sync's actual outcome. Commit/push only on instruction; keep secrets/runtime data out. Use repo-relative paths and read current files on every new device/chat.
