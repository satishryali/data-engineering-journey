# Current tutoring checkpoint

Last updated: 15 October 2026 (IST).

## Goal and background

India data engineering job switch targeted for February 2027; salary aspiration about 15 LPA. Electrical engineering education; four years software support and one year development. Notice period: 90 days. Learner is considering resignation on 30 November 2026; resignation and last working date are not confirmed. February remains a target rather than a confirmed joining date.

Study target: 50 hours weekly (weekdays six hours each, weekends ten each). Azure selected. Main track: SQL/Python, PostgreSQL, dbt, Airflow, intermediate Docker, PySpark fundamentals and selected Snowflake work. Power BI and PL/SQL are supporting skills.

Learner reconfirmed the 50-hour target. Reports required tools available on their server and willingness to install more; environment has not yet been verified. No Azure or Snowflake access; willing to pay when needed. Begin locally and revisit access for the relevant lessons.

## Evidence so far

- Initial revenue SQL used correct table keys, SUM and a completed-status filter.
- It used INNER JOIN and lost customers without orders; omitted GROUP BY; used MONTH() in PostgreSQL; did not restrict the year or replace a missing total with zero.
- Python cleaning and dbt/pipeline assessment not attempted; learner reported not knowing the remaining answers.
- No project completion or independent lesson success has been demonstrated. Do not assume all listed technologies are working skills.

## Current lesson

SQL: preserving unmatched customers with LEFT JOIN. The learner has not yet answered the simplified prediction/exercise. See tools/sql/exercises/001-join-preservation/README.md.

Latest prompt already presented: using customers (1, Asha), (2, Ravi), (3, Meera) and orders (101, 1), (102, 1), (103, 2), predict the INNER JOIN output row count and whether Meera appears, with a reason. No answer received and no hint given for this simplified task. The query is in tools/sql/exercises/001-join-preservation/README.md; attempt.sql remains a blank template.

Exact next action: wait for the learner's prediction, or briefly restate those two questions in a new chat. Review that answer before asking the learner to modify the query to preserve every customer and predict Meera's order_id. Give a hint only if needed. Do not begin the full revenue aggregation until this is understood.

## Revision

SQL-001 is in learning state, awaiting correction; no first independent success date. Schedule actual retrieval reviews after demonstrated learning. No need to restart the entire assessment.

## Timer and platform setup

A SQL interval began at 08:11:20 IST on 15 October 2026. Subsequent messages concerned platform access and repository setup. The actual stop/pause time was not supplied. The migrated row is needs_confirmation and is excluded from confirmed totals. Ask for the actual end time before closing it; do not charge the whole setup gap to SQL study.

No new timer has started. Learner said they will start it and was told to send "Start SQL" when ready. Follow reference/study-tracking.md on that explicit signal; do not infer a running interval from readiness or repository-maintenance messages.

## Portability

Cross-computer entry point: START-HERE.md. It summarises current status, the exact pending prediction, timer uncertainty, agreed commands and required reading. Keep its status and next step aligned with this checkpoint after meaningful work; underlying code and trackers remain authoritative.

This repository is now the canonical tutoring record: https://github.com/satishryali/data-engineering-journey (private). Files previously produced beside the original checkout are historical snapshots. Original-chat reminders use the local checkout; remote/cloud chats need repository access and current checkpoints. Read this file after pulling before resuming, and push reviewed checkpoint updates after finishing. Git does not migrate or run the existing reminders.

Learner explicitly requested durable Markdown handoffs so closing a context window or changing computers does not lose the current step. Maintain this checkpoint and session history after substantive exchanges. Learner authorised committing and pushing the latest changes on 15 October 2026. Verify actual sync using Git status and the remote branch; another computer needs the latest synced files before resuming.

Agreed record structure: update this single checkpoint in place, append dated session-history entries, preserve work in exercise folders, and maintain skill notes plus CSV trackers. No separate daily Markdown file is needed. Create additional exercise/project files as actual work requires them.

Schedule command: `Today's schedule` shows the current IST date's target, confirmed/remaining hours, due reviews and ordered tasks from the checkpoint and plan without starting a timer. Today's proposed sequence (15 October): pending SQL join prediction; preservation query, reconstruction and changed example; grouping/missing totals only if ready; Python cleaning baseline; retrieval and handoff. These are conditional tasks, not recorded completions or a fixed clock timetable.

Time-report command: `Study time` is an alias for `Study status`; report confirmed daily/weekly hours and minutes against targets, remaining hours and closed-day shortfall, with any running/uncertain intervals separate. It does not start or stop the timer.

Learner requested clear timer/checkpoint commands and checkpoints without reminders. README.md now defines the phrases and end-of-day procedure. Save after meaningful work; Finish for today closes any active interval and saves a daily summary. If the learner leaves silently, reconcile a missing closing summary at the next interaction from evidence only; no background midnight execution. This exchange is setup only; current SQL prediction and timer state remain unchanged.

Excel hours tracker added at outputs/study-tracker/study-hours.xlsx, generated by tracking/update-study-tracker.mjs from tracking/study-log.csv. Refresh after log changes, status requests and daily handoff. Initial IST reporting date: 15 October 2026; targets start that date (32-hour first partial week, then 50-hour weeks). Shows daily/weekly confirmed hours, closed-day behind/ahead and today's remaining target. Initial confirmed hours: zero; today remaining: six; earlier uncertain interval excluded. No new timer started; SQL prediction still awaits an answer. Workbook and documentation are included in the authorised repository sync.
