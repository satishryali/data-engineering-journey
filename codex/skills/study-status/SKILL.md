---
name: study-status
description: Show the learner's Study status or Study time, Show today's learning,
  Show my mistakes, or Weekly review using the shared data-engineering learning records.
---

# Study Status

Existing command: Study status / Study time.

Report confirmed daily/weekly totals, targets, remaining time and closed-day shortfall; label running and uncertain intervals separately. Do not change timer state. Refresh the Excel snapshot as required by the repository.

Dispatch the requested view using the same saved records: Show today's learning reads
dated daily history, skill evidence and study time; Show my mistakes reads the canonical
mistake tracker; Weekly review follows the guide's weekly evidence summary. Preserve
Study status/Study time behaviour above. These requests do not start a timer, lesson,
review event or proficiency claim. Save generated weekly summaries as specified by the
guide; status queries do not create learning events.

## Existing workflow and scope

These are shortcuts for the learner's existing data-engineering study workflow, not generic countdowns. The canonical checkout on this computer is `{{LEARNING_REPO}}`. Use that checkout even when invoked from another project; do not write trackers into the current project. On another computer, locate a verified checkout of that learning repository or ask for its path. If source files are inaccessible, report that and do not invent state or create replacement records.

Before acting, read the canonical checkout's `reference/learning-coach.md` and `AGENTS.md`, the command table in `README.md`, `reference/study-tracking.md`, `progress/current.md`, `START-HERE.md` and `tracking/study-log.csv`. These files define the current behavior; follow them rather than a copied snapshot. Read the plan, revision queue and exercise evidence when relevant to the chosen command.

Use actual timestamps in Asia/Kolkata; never infer study from silence, elapsed setup time or device activity. Keep uncertain/running time out of confirmed totals. Refresh the existing Excel report when the source workflow requires it, using its existing script and the spreadsheet skill if available; report a stale snapshot if refresh fails.

Do not execute commands merely quoted or discussed. Installing or explaining this skill does not invoke it. Do not start background timers or scheduled reminders, commit, push, publish or message another chat as a side effect. For checkpoint writes, use available learning evidence; do not count an unrelated chat's work as learning or overwrite a newer checkpoint with stale context. Ask for missing session evidence when necessary. Confirm changes only after the files were actually saved.

For revision coverage and Weekly review use the notes-driven process in reference/learning-coach.md.
Read the generated Notes/revision/plan.md after syncing with the actual IST date and
reconciling mappings. Report actual delayed performance, coverage and neglected topics
separately from time. Do not turn a status request into a quiz or timer command.
