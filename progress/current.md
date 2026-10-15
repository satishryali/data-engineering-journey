# Current tutoring checkpoint

Last updated: 15 October 2026 (IST).

## Goal and background

India data engineering job switch targeted for February 2027; salary aspiration about 15 LPA. Electrical engineering education; four years software support and one year development. Notice period and February joining-versus-offer deadline not yet confirmed.

Study target: 50 hours weekly (weekdays six hours each, weekends ten each). Azure selected. Main track: SQL/Python, PostgreSQL, dbt, Airflow, intermediate Docker, PySpark fundamentals and selected Snowflake work. Power BI and PL/SQL are supporting skills.

## Evidence so far

- Initial revenue SQL used correct table keys, SUM and a completed-status filter.
- It used INNER JOIN and lost customers without orders; omitted GROUP BY; used MONTH() in PostgreSQL; did not restrict the year or replace a missing total with zero.
- Python cleaning and dbt/pipeline assessment not attempted; learner reported not knowing the remaining answers.
- No project completion or independent lesson success has been demonstrated. Do not assume all listed technologies are working skills.

## Current lesson

SQL: preserving unmatched customers with LEFT JOIN. The learner has not yet answered the simplified prediction/exercise. See tools/sql/exercises/001-join-preservation/README.md.

Exact next action: ask for the INNER JOIN output row count, whether Meera appears and why; then ask the learner to modify the query to keep her and predict her order_id. Give a hint only if needed. Do not begin the full revenue aggregation until this is understood.

## Revision

SQL-001 is in learning state, awaiting correction; no first independent success date. Schedule actual retrieval reviews after demonstrated learning. No need to restart the entire assessment.

## Timer and platform setup

A SQL interval began at 08:11:20 IST on 15 October 2026. Subsequent messages concerned platform access and repository setup. The actual stop/pause time was not supplied. The migrated row is needs_confirmation and is excluded from confirmed totals. Ask for the actual end time before closing it; do not charge the whole setup gap to SQL study.

## Portability

This repository is now the canonical tutoring record: https://github.com/satishryali/data-engineering-journey (private). Files previously produced beside the original checkout are historical snapshots. Original-chat reminders use the local checkout; remote/cloud chats need repository access and current checkpoints. Read this file after pulling before resuming, and push reviewed checkpoint updates after finishing. Git does not migrate or run the existing reminders.
