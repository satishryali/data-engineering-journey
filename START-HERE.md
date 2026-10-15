# Start here: tutoring handoff

Last updated: 15 October 2026 (IST). Update this file in place at checkpoint boundaries.

## Message for another computer

> Read START-HERE.md, AGENTS.md and progress/current.md from this checkout, verify the trackers and current exercise files, then continue the exact pending task. Do not restart the assessment or start a timer without my explicit instruction. Tell me if files are unavailable.

## Current status and exact next step

- All timers are paused. Latest Python interval ended 12:48:53 IST on 15 October. Completed today/week: 1h57m23s (SQL 1h30m56s; Python 26m27s). Remaining today: 4h2m37s toward six hours. The old 08:11:20 interval is needs_confirmation and excluded; never infer its duration.
- Active learning task is PY-002 dictionary foundations, requested after difficulty with the cleaner. Use tools/python/exercises/001-record-cleaning/dictionary-refresher.md. Tutor has explained keys/values, retrieval and what items() yields. No refresher attempt yet.
- Next learner attempt: starting with order = {"order_id": 101, "amount": "500"}, print the amount, change it to the string "750", then print the dictionary. Submit code/output together. No loops, conversions or exception handling yet. Wait for explicit Resume Python before starting another study interval.
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

Excel: outputs/study-tracker/study-hours.xlsx, current snapshot 15 October, completed 1h57m23s. Rebuild from tracking/study-log.csv with tracking/update-study-tracker.mjs after log changes, status requests and daily handoff. Exclude running/uncertain time from confirmed totals; closed-day shortfall is separate from today's remaining target. Follow spreadsheet skill for workbook authoring; flag stale snapshots if refresh unavailable.

ClockIt octech.clockit v1.9.0 is installed only on the original computer. Local ignored workspace settings disable auto-start/cloud and select CSV. No importer or tested focus alert is configured; no reminder scheduled. Learner prefers tutor-managed tracking. Do not promise automatic alerts without a working mechanism and agreed duration.

## Switching computers and maintaining this handoff

Pause/finish and save before switching. Review and commit/push intended files, then clone or pull the same branch into a clean checkout on the other computer (README.md has commands). Resolve conflicts without discarding attempts. Reconnect to the server; Git does not transfer credentials, installed tools, databases, temporary tables or reminders. Recreate local ClockIt settings if needed.

At checkpoints replace stale status/next step here and in progress/current.md; append one concise block outcome to session-history.md and update actual trackers. Commit/push only when explicitly authorised. Learner authorised this sync on 15 October; verify actual outcome in Git/remote rather than assuming success.
