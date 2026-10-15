# Start here: tutoring handoff

Last updated: 15 October 2026 (IST). Update this file in place at checkpoint boundaries.

## Message for another computer

> Read START-HERE.md, AGENTS.md and progress/current.md from this checkout, verify the trackers and current exercise files, then continue the exact pending task. Do not restart the assessment or start a timer without my explicit instruction. Tell me if files are unavailable.

## Finished for today - 15 October 2026

Daily handoff saved at the learner's explicit Finish for today request. No interval was running; the last confirmed stop remains 14:59:45 IST. Confirmed today and this week: 2h48m34s (SQL 1h30m56s; Python 1h17m38s). Today's six-hour target has 3h11m26s unfilled, with no catch-up debt assumed. Partial-week target: 32h; remaining 29h11m26s. Closed-day shortfall before today: 0h. The 08:11:20 SQL interval still needs its actual stop time and is excluded. Excel refreshed for 15 October from the unchanged CSV.

SQL-001 initial reasoning/output succeeded, with spelling help retained; SQL-002 needed COUNT/NULL, join-key and grouping hints. SQL-003 totals and Python cleaner remain unfinished. Dictionary/list explanations and coach setup are reference/administration, not new assessed success. No new learner attempt or delayed review occurred in this chat. Preserve all prior attempts, mistakes, skill states and review dates.

Exact next task: Starting with order = {"order_id": 101, "amount": "500"}, print the amount, change it to the string "750", then print the dictionary. Submit code/output together.

Use tools/python/exercises/001-record-cleaning/dictionary-refresher.md; no loops/conversion/exception handling yet. Resume only on an explicit timer command. Early practice for SQL-001/002/003 and PY-001 remains due 16 October; select a manageable set after the dictionary prerequisite. GitHub contains commit a70f3fb; this daily handoff is local and has not been pushed.

## Current status and exact next step

- All timers paused at 14:59:45 IST on 15 October. Latest Python/Jupyter dictionary interval 14:14:07–14:59:45 lasted 45m38s. Completed today/week: 2h48m34s (SQL 1h30m56s; Python 1h17m38s). At finish: 3h11m26s of the six-hour target unfilled. The old 08:11:20 interval is needs_confirmation and excluded; never infer its duration.
- Active learning task is PY-002 dictionary foundations, requested after difficulty with the cleaner. Use tools/python/exercises/001-record-cleaning/dictionary-refresher.md. Tutor has explained keys/values, retrieval and what items() yields. The selected refresher is not yet assessed; practice/Dictionaries.ipynb contains general practice but does not establish completion or independent proficiency.
- Next learner attempt: starting with order = {"order_id": 101, "amount": "500"}, print the amount, change it to the string "750", then print the dictionary. Submit code/output together. No loops, conversions or exception handling yet. No notebook code/output submitted during the latest block; All timers paused; await explicit resume before starting another interval.
- PY-001 cleaner is deferred, not solved. Preserve attempt.py and snapshots in attempts/. Earlier hints covered record access, lists and int()/ValueError. Expected valid/rejected output shape was supplied on request, not the implementation. feedback.md records reviewed evidence. No Python proficiency or success anchor established.
- SQL-001 initial join-preservation learning completed with independent reasoning and changed outputs; reconstruction spelling help recorded. SQL-002 initial counting/grouping practice completed with COUNT/NULL, join-key and grouping assistance. Both need early retrieval on 16 October.
- SQL-003 is deferred at setup: SUM NULL rule taught after a Nila-zero error; no totals query/output yet. The learner's old-table insert syntax error is preserved. Later use exercise 003's separate revenue_* setup or first verify actual schema. tools/postgresql/setup.sql is the learner's scratch history, including ALTER/invalid attempts, not a clean setup script; don't run it wholesale.
- Python/SQL failed attempts are intentional evidence, not repository defects to repair automatically. No integrated pipeline is complete.

## Required reading and records

1. AGENTS.md and README.md: teaching, command definitions, syncing and Excel instructions.
2. progress/current.md and latest progress/session-history.md entries: evidence, assistance, constraints and handoff.
3. plan/learning-and-revision-plan.md and weekly-learning-plan.csv: curriculum, not completion evidence.
4. tracking/revision-queue.csv and revision-history.csv: actual learning/reviews. No spaced review has yet been attempted.
5. tracking/study-log.csv and reference/study-tracking.md: intervals and uncertain time.
6. Active dictionary-refresher.md plus cleaner attempt.py/feedback.md. Don't overwrite learner attempts with solutions.

Source code, actual output and trackers take precedence over summaries; reconcile disagreements. Use repository-relative paths and the current IST date.

## Working preferences

- One meaningful bounded task per attempt, with prediction/code/output together. Avoid repeated trivial confirmation cycles. Use smaller questions or worked examples for demonstrated gaps; the dictionary refresher is explicitly requested.
- Batch Markdown/learning records at task completion, pause/topic switch, Save checkpoint or Finish. Do not write files after every ordinary answer/hint. Timer events are logged immediately. Save checkpoint before closing or changing devices; interim conversation work is not yet persisted.
- Keep one current checkpoint, appended concise block history and separate exercise attempts/hints. Record independent, assisted and needs_guidance honestly; no proficiency inferred from familiarity or hours.
- No background/parallel record writer or automatic midnight save is running. Reconcile missing day-end summaries later from evidence only.
- Study budget: six-hour weekdays, ten-hour weekend days, 50h per full Monday-Sunday week, breaks separate. Tracking started 15 October; first partial week 32h. No catch-up debt or guaranteed mastery/job/salary.
- Background/constraints: India February 2027 job-switch target, 15 LPA aspiration, four years support plus one development. Notice period 90 days; considering resignation 30 November, unconfirmed. Tools reportedly on server; no Azure/Snowflake access yet, willing to pay when needed. Begin locally.

## Commands and time reporting

Start Python / Start SQL / Start [topic]: start one interval. Pause closes it for a break. Resume [topic] starts a new interval. Finish ends a session and checkpoints; Finish for today also saves the daily summary. Combined pause SQL/start Python is valid with one shared timestamp and no overlap.

Study time / Study status reports completed daily/weekly totals, targets and remaining time, with running/uncertain time separate. Today's schedule shows ordered tasks without starting a timer. Save checkpoint / This is the checkpoint saves without changing timers. Read the checkpoint and continue resumes the learning context only. Discussing commands does not execute them.

Excel: outputs/study-tracker/study-hours.xlsx, current snapshot 15 October, completed 2h48m34s. Rebuild from tracking/study-log.csv with tracking/update-study-tracker.mjs after log changes, status requests and daily handoff. Exclude running/uncertain time from confirmed totals; closed-day shortfall is separate from today's remaining target. Follow spreadsheet skill for workbook authoring; flag stale snapshots if refresh unavailable.

ClockIt octech.clockit v1.9.0 is installed only on the original computer. Local ignored workspace settings disable auto-start/cloud and select CSV. No importer or tested focus alert is configured; no reminder scheduled. Learner prefers tutor-managed tracking. Do not promise automatic alerts without a working mechanism and agreed duration.

## Switching computers and maintaining this handoff

Pause/finish and save before switching. Review and commit/push intended files, then clone or pull the same branch into a clean checkout on the other computer (README.md has commands). Resolve conflicts without discarding attempts. Reconnect to the server; Git does not transfer credentials, installed tools, databases, temporary tables or reminders. Recreate local ClockIt settings if needed.

At checkpoints replace stale status/next step here and in progress/current.md; append one concise block outcome to session-history.md and update actual trackers. Commit/push only when explicitly authorised. Learner authorised this sync on 15 October; verify actual outcome in Git/remote rather than assuming success.

## Five-role setup and next session

Read reference/learning-coach.md alongside AGENTS.md. Learning Coach, Notes Keeper,
Mistake Keeper, Revision Coach and Progress Tracker are coordinated responsibilities
of one tutor. Use the canonical tracking files; Notes/revision JSON/JSONL and mistake
index are generated views. tracking/legacy preserves the original concept records,
dates and deferred diagnostic-dict-001. Keep the selected PY-002 task above; no restart.

Say **Start today's learning**. This selects the next bounded task without starting a
timer. Status/planning requests also leave timers unchanged. Setup is administrative,
not a completed lesson/review. No commit or push is authorised for this setup.

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

## Notes-driven revision setup - 15 October 2026

The requested Revision Coach upgrade is saved locally. Same five roles; no quiz, study
interval or completed review was created. The generated Notes/revision/plan.md maps
53 learning sections to 20 stable concepts, excluding two navigation/reference sections
and documented non-learning files. Four concepts were added as unassessed (lists: basics,
changes, records; dictionary removal). Existing IDs, attempts, mistakes, skill evidence,
review history and due dates are preserved. Initial diagnostic slots run from 16 October
at most one per suitable session; these are adjustable plans, not completed reviews.
Concept assessment counts remain zero; historical SQL exercise evidence stays separate.

Start revision / Today's schedule / Weekly review / Save checkpoint now synchronise
notes and use the generated plan. Material changes flag affected concepts; formatting
does not reset progress. New sections need mappings, and questionable source claims
need official verification before teaching. No background monitor exists.

Next suitable 15-minute block: about five minutes for the pending dictionary read/update/
print task and up to ten minutes for a due SQL COUNT/NULL reconstruction, if readiness
and available time allow. Ask one task at a time without answers; teach missing basics
first. Start today's learning does not start a timer; all timers remain stopped.

Exact next task: Starting with order = {"order_id": 101, "amount": "500"}, print the amount, change it to the string "750", then print the dictionary. Submit code/output together.

The earlier end-of-day summary remains valid. This setup and subsequent handoff updates
are local and uncommitted; no push was requested.
