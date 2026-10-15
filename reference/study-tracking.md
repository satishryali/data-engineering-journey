# Study time tracking

Timezone: Asia/Kolkata (IST, UTC+05:30).
Log: tracking/study-log.csv relative to the repository root.
Weekly target: 50 hours, Monday to Sunday in IST.

Excel report: outputs/study-tracker/study-hours.xlsx. Source remains tracking/study-log.csv; refresh with tracking/update-study-tracker.mjs after log changes, study-status requests and daily handoff. README.md documents the workflow. Six-hour weekdays and ten-hour weekends start on 15 October 2026; first partial week is 32 hours. Behind/ahead uses closed days only, with today's remaining hours separate. Refresh the fixed IST reporting date; do not treat a stale snapshot as today's totals.

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

Start today's learning and Start revision select work but do not start a timer.
Show my mistakes, Show today's learning and Weekly review are status/planning requests;
they do not start or stop intervals. Use the five-role workflow in learning-coach.md
for notes, mistakes and checkpoint saves. The CSV and existing Excel reporting remain unchanged.

Start SQL / Start Python / Start dbt / Start Azure: begin a session.
Pause / Finish: close the active interval.
Resume [topic]: start a new interval.
Study status: report daily and weekly totals.

Study time: alias for Study status. Show confirmed hours and minutes for today and the Monday–Sunday week, their targets, remaining hours and closed-day shortfall. Separately show elapsed time in any running interval and uncertain intervals. This is a read/status command and does not change the timer; refresh the Excel report as for Study status.

Today's schedule: show the IST daily target, confirmed/remaining hours, due reviews and next tasks from the checkpoint and agreed plan. Do not start a timer. Refresh the Excel snapshot if its reporting date is stale before using it for today's figures.

Finish for today: close the active interval and save the end-of-day checkpoint with confirmed daily/weekly totals and any uncertain intervals separately labelled.
Save checkpoint / This is the checkpoint: save learning state only; do not change the timer.

Finish also saves a checkpoint. Follow README.md for the complete command table and missing end-of-day summary procedure. Discussing these phrases does not start or stop an interval.

A CSV does not tick continuously. Timestamps allow elapsed time to be calculated when the assistant next runs. Timed notifications use the app's existing scheduled reminders. Tracking requires access to this log; a different chat without that access cannot automatically update it.
