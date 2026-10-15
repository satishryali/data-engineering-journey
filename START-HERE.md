# Start here: tutoring handoff

Last updated: 15 October 2026 (IST). Maintain this one file in place; do not create a new device-specific copy.

## Message to use on another computer

> Read START-HERE.md and the linked checkpoint, instructions and trackers from this checkout. Verify the current learning and timer state, then continue the exact pending step. Do not restart the assessment or start a timer without my explicit instruction. If you cannot access the files, tell me what is missing.

## Current status

- Learning framework and Excel tracker are prepared. No exercise has been completed independently; the integrated pipeline is planned, not built.
- Active task: SQL-001, preserving customers without orders. The simplified prediction has been presented but not answered; no hint has been given for it. tools/sql/exercises/001-join-preservation/attempt.sql is still a blank template.
- No new study timer is running. The old interval starting at 08:11:20 IST on 15 October 2026 is needs_confirmation; actual stop time is unknown and its duration is excluded from confirmed totals. Never count the setup gap as SQL study.
- Excel snapshot: outputs/study-tracker/study-hours.xlsx, dated 15 October 2026, has zero confirmed hours. Read the current study log before reporting new totals; refresh a stale snapshot.
- Learner authorised committing and pushing the latest changes on 15 October 2026. Verify actual sync using Git status and the remote branch rather than assuming another computer has the latest edits.

## Exact next teaching step

Ask the learner to predict this query's row count and whether Meera appears, explaining why. Wait for the attempt before giving feedback or answers.

Customers (customer_id, name): (1, Asha), (2, Ravi), (3, Meera).
Orders (order_id, customer_id): (101, 1), (102, 1), (103, 2).

```sql
SELECT c.name, o.order_id
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id;
```

After reviewing the prediction, ask the learner to change the query to preserve every customer and predict Meera's order_id. Use progressive hints only if needed, then reconstruction and changed input. Introduce grouping, missing totals and dates in separate later steps when ready. Python cleaning baseline is still pending. Do not put solutions in the learner's attempt file.

## What the new tutor must read

1. [AGENTS.md](AGENTS.md): tutoring and record-maintenance rules.
2. [Current checkpoint](progress/current.md) and latest entries in [session history](progress/session-history.md): evidence, decisions and exact pending task.
3. [Agreed plan](plan/learning-and-revision-plan.md) and [weekly plan](plan/weekly-learning-plan.csv): curriculum, not proof of completion.
4. [Revision queue](tracking/revision-queue.csv) and [revision history](tracking/revision-history.csv): SQL-001 remains in learning state; no first independent success or completed retrieval review.
5. [Study log](tracking/study-log.csv) and [time-tracking rules](reference/study-tracking.md): actual intervals and uncertainty.
6. [Current exercise](tools/sql/exercises/001-join-preservation/README.md), setup.sql and attempt.sql in that folder.
7. [README.md](README.md): sync commands, learner message definitions and Excel refresh instructions.

This is the entry-point summary. Code, interval logs and attempt evidence remain authoritative. If records disagree, reconcile them before recording new results; do not infer progress from dates.

## Agreed background and constraints

- India job-switch target: February 2027; salary aspiration about 15 LPA. Neither is guaranteed. Prior experience: four years software support and one year development; do not label it data engineering project experience.
- Notice period: 90 days. Learner is considering resignation on 30 November 2026; resignation and last working date are unconfirmed.
- Study target: six hours each weekday and ten each weekend day, 50 hours per full Monday–Sunday week, with breaks separate. Tracking begins 15 October; first partial week is 32 hours. Compare closed-day targets separately from today's remaining time.
- Tools reportedly available on learner's server; environment not yet verified. No Azure or Snowflake access; learner willing to pay when needed. Begin locally. Keep credentials out of the repo.
- Teach one small step at a time and assess actual code, output and reasoning. Preserve attempts and distinguish independent, assisted and needs_guidance. Do not restart after missed days or force a large revision backlog.

## Learner messages

| Message | Meaning |
|---|---|
| Today's schedule | Show target, remaining time, manageable due reviews and ordered tasks; no timer change. |
| Start SQL / Start Python / Start [topic] | Start one interval at the actual IST timestamp; check for overlap first. |
| Pause | Close the interval for a break. |
| Resume SQL / Resume [topic] | Start a new interval after the break. |
| Study time / Study status | Report confirmed daily/weekly time, targets and shortfall; running/uncertain time separately. |
| Save checkpoint / This is the checkpoint | Save learning state without changing the timer. |
| Finish | Close the current session, refresh Excel and save progress; studying may resume later today. |
| Finish for today | Also save the day's summary and exact next task. |
| Read the checkpoint and continue | Read the saved records and resume; no automatic timer start. |
| Commit and push the latest changes | Explicit request to review, commit and push the intended repository changes. |

Discussing or quoting these messages does not execute them. Save checkpoints after meaningful work without waiting for a reminder. This chat does not update files in the background when closed; reconcile a missing day-end summary at the next interaction using actual evidence.

## Switching computers

1. On the old computer, pause/finish any active timer, save the checkpoint and review Git changes. Commit and push the intended files yourself or explicitly ask the assistant to do it.
2. On the new computer, clone the private repo or check for local changes and the correct branch before `git pull --ff-only`. Preserve and reconcile conflicting work before editing. Full commands are in README.md.
3. Open the synced checkout in Codex and send the message at the top of this file. All paths are repository-relative; no original Windows location is required.
4. Git does not transfer installed tools, databases, temporary tables, credentials or reminders. Reconnect to the server. For the SQL sample, run setup.sql in the same PostgreSQL connection as the query.

## Maintaining this handoff

At each meaningful checkpoint, update Current status and Exact next teaching step here alongside progress/current.md, then append actual outcomes to progress/session-history.md. Keep this file concise as work advances; replace stale status rather than appending daily copies. Record attempts, reviews and time in their own files. Refresh the Excel snapshot from tracking/study-log.csv using tracking/update-study-tracker.mjs after log changes, status requests and daily handoff; flag it stale if refresh is unavailable. Do not commit or push without authorisation.
