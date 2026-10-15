# Study time tracking

Timezone: Asia/Kolkata (IST, UTC+05:30).
Log: tracking/study-log.csv relative to the repository root.
Weekly target: 50 hours, Monday to Sunday in IST.

## Session rules

- Begin only when the learner explicitly signals starting study. Use the clock tool for the actual timestamp, convert to IST, and append one running row. Never start overlapping sessions.
- Store timestamps in ISO 8601 with +05:30 offset. Use a unique session ID; leave end_time_ist and elapsed_minutes empty while running.
- On pause or finish, obtain the actual time, close the running row, calculate elapsed_minutes from the timestamps, and set status to completed. Notes can distinguish pause from finish. Preserve all prior records.
- Resume starts a new row; breaks between rows are not counted. Never infer active study from computer activity or message silence.
- If the learner supplies a different actual stop time, record the corrected interval and explain the correction in notes. If a forgotten timer is uncertain, mark needs_confirmation and exclude it from confirmed totals until resolved.
- On a status request, report completed time plus separately labelled elapsed time for the running interval. Recorded intervals measure reported study sessions, not independently verified concentration.
- Split intervals crossing IST midnight at midnight so daily totals remain correct.
- Sum completed rows for confirmed daily and Monday-to-Sunday weekly totals; present hours and minutes and progress toward 50 weekly hours. Do not add running or needs_confirmation rows to confirmed totals.
- If a running row is stale at a later check-in, ask for its actual stop time rather than silently counting the gap. Do not fabricate attendance, completion, or study time.

## Learner messages

Start SQL / Start Python / Start dbt / Start Azure: begin a session.
Pause / Finish: close the active interval.
Resume [topic]: start a new interval.
Study status: report daily and weekly totals.

A CSV does not tick continuously. Timestamps allow elapsed time to be calculated when the assistant next runs. Timed notifications use the app's existing scheduled reminders. Tracking requires access to this log; a different chat without that access cannot automatically update it.
