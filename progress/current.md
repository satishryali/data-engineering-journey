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
- PY-002: dictionary refresher requested. Tutor explained one record, keys/values, access and items() pairs. The selected refresher has not yet been assessed. practice/Dictionaries.ipynb now contains general dictionary practice; do not infer completion of the selected task or independence from its presence. No integrated project complete; initial revenue date/year/filter gaps remain unassessed.

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

START-HERE.md is the entry point; README.md has commands/sync/Excel instructions. Latest explicit request: implement the five-role coach without committing or pushing. Git history records prior syncs; setup changes remain local until separately authorised. Commit/push only on instruction; keep secrets/runtime data out. Use repo-relative paths and read current files on every new device/chat.

## Five-role coordination — setup only, 15 October 2026

Use reference/learning-coach.md. Exactly five roles coordinate one conversation; no
independent/background agents exist. CSV queue/history own dates/events; topic-map
links broad exercise and concept IDs without transferring scores. Notes/revision
views are generated; original state and diagnostic-dict-001 are preserved in tracking/legacy.
That older diagnostic is deferred by the later explicit PY-002 request. Setup records
historical evidence only: no new lesson, success, review or timer event occurred.
The saved notebook is available but has not been reviewed against the pending task.
Eight historical mistake entries and dimension-specific observations cite original
15 October evidence; no mistake is verified on delayed independent practice.

Natural entry phrase: Start today's learning. Select the existing task without an
automatic timer. All old slash commands remain. Ordinary answers are saved at checkpoint
boundaries; timer events remain immediate. Weekly summaries are generated on demand or
at the next session after week end, with partial/later-reconstruction labels.

Lists reference requested via Notes Keeper: Notes/Python/Concepts/lists.md and separate
Notes/revision/list-questions.md are saved. This is reference preparation only; no list
assessment or review date was recorded. The selected dictionary task and timer state
remain unchanged.

Note-writing preference: use reference/note-style.md. Match the learner's short
headings and bullets, simple words and more small examples with output. The lists
reference was rewritten in this style; no new assessment, timer change or review date.

Notes Keeper style specification expanded: reference/note-style.md now defines
why/input/code/output/explanation, examples for different behaviours, output verification
labels and evidence-based doubts/mistake links. Apply to future notes; existing notes
were not rewritten for this request. One dictionary style preview is awaiting learner
feedback; it is a tutor example, not an assessed attempt. Pending task/timers unchanged.
