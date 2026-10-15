# data-engineering-journey

My practical data engineering learning journey: SQL, Python, PostgreSQL, dbt, Airflow, Docker, Snowflake, PySpark and Azure—with hands-on projects, exercises, revision tracking and tutor checkpoints.

This repository is the durable record of my tutoring, exercises, revision and project work. Chat history is useful context; this checkpoint and actual code are the source of truth.

## Start or resume here

On a new computer or in a new chat, begin with [START-HERE.md](START-HERE.md). It contains the current handoff, exact next step and the records the tutor must verify. Say: **Read START-HERE.md and continue from the checkpoint.**

1. Read AGENTS.md and progress/current.md.
2. Read plan/learning-and-revision-plan.md for the agreed schedule.
3. Inspect tracking/revision-queue.csv and the latest work before selecting a task.
4. After reviewed work, update progress/current.md, progress/session-history.md and the relevant trackers. Never mark a planned topic as completed.

Current assignment: tools/sql/exercises/001-join-preservation/README.md.

## Structure

- plan/: 16-week curriculum and weekly milestones.
- progress/: current checkpoint and concise session handoffs.
- tracking/: study intervals, revision queue and actual review history.
- tools/: notes and exercises organised by skill.
- projects/: integrated pipelines combining tools.
- reference/: supporting tutoring and time-accounting guidance.

Each tool has README.md and notes.md. Add exercise folders as lessons are actually assigned. Store explanations of the problem, attempted code, expected output, mistakes and a changed example. Integrated projects belong in projects/, with one main README and run instructions.

## Across computers

Repository: https://github.com/satishryali/data-engineering-journey

Use the repository root as the working folder on every computer. Its location may differ; all learning-file paths are relative to that root. Work on one computer at a time and use the same branch for the learning record.

### 1. Before leaving the current computer

1. Send `Pause` or `Finish` if a study timer is running. If the end time is uncertain, report that uncertainty; do not count the gap as study.
2. Ask the tutor to save the checkpoint. Confirm that attempts are saved, progress/current.md identifies the exact next step and timer state, and progress/session-history.md contains actual outcomes. Revision trackers should reflect actual attempts only.
3. Review the local changes from the repository root:

```bash
git status
git diff
git branch --show-current
```

4. Stage only the intended files by their paths. For example, if only the two progress files changed:

```bash
git add progress/current.md progress/session-history.md
git diff --cached
git commit -m "Save tutoring checkpoint"
git push
```

Include any changed exercise, plan, instruction or tracker files in the staging step too. The example above does not stage those automatically. Check the staged diff before committing; keep credentials and runtime data out of commits.

5. Confirm that push succeeded. Run `git status` to check for remaining changes or unpushed commits. If push fails, the other computer does not yet have this checkpoint; resolve the failure before switching. If the branch has no upstream, follow Git's suggested upstream command after checking the branch name.

These are instructions for the learner. The assistant saves local files as part of tutoring but only commits or pushes when explicitly asked. Saving a file or making a commit alone does not sync it to another computer.

### 2. Open the project on the other computer

For the first use on that computer, authenticate with your own GitHub account for this private repository, then run:

```bash
git clone https://github.com/satishryali/data-engineering-journey.git
cd data-engineering-journey
```

For an existing checkout, open its repository folder and run:

```bash
git status
git branch --show-current
```

Confirm that there are no uncommitted changes and that the branch matches the one used on the previous computer. Then run:

```bash
git pull --ff-only
git log -1 --oneline
```

If there are local changes, a branch mismatch, a rejected pull or divergent commits, preserve the work and ask for help reconciling it before continuing. Do not discard files or force-push to make the warning disappear. Compare the latest commit and progress/current.md with the checkpoint you saved on the other computer.

### 3. Resume tutoring

Open this checkout in Codex and use the prompt below. The tutor should read the files, state the unfinished step and wait for your attempt. Do not restart the assessment just because the computer or chat changed.

Check tracking/study-log.csv before starting a timer. A copied running row does not prove continued study; resolve its actual stop time or mark it uncertain before starting a new interval. Send `Start SQL` or the appropriate topic when ready. No overlapping timers.

Git transfers tracked files; it does not transfer installed software, database contents, temporary SQL tables, server connections, credentials or reminders. Reconnect to your existing server as needed. For the current SQL exercise, run its setup.sql in the same PostgreSQL connection as your query; the sample tables are temporary. Do not put connection secrets in the repository.

Commit author configuration is separate from GitHub login. An AI can read the repository only if the current chat has access: open the checkout in Codex, use an authorised GitHub connection, or upload current files. Merely naming a repository does not grant access. A normal ChatGPT Project does not automatically execute this AGENTS.md or continually pull a repository; explicitly ask it to read the current files.

## How learning records are maintained

- progress/current.md: one current checkpoint, updated in place with evidence, help used, weak points, exact pending task and timer state.
- progress/session-history.md: append concise dated outcomes after meaningful exchanges, including agreed planning changes. Do not create a separate daily Markdown file by default.
- tools/<skill>/exercises/: preserve prompts, attempts, feedback and changed examples. Keep hints and final solutions separate from unanswered practice.
- tools/<skill>/notes.md: record explanations and lessons from actual work.
- tracking/: record study intervals, actual retrieval attempts and the next review due; never infer completion from a planned date.
- plan/: maintain the agreed curriculum and any deliberate scope changes.

The tutor updates the relevant files after meaningful work and before a handoff. You can also say `Save checkpoint` before closing the chat. Git history preserves committed versions; a fresh chat still needs to read the latest files.

## New tutoring chat prompt

> Act as my data engineering tutor. Read README.md, AGENTS.md, progress/current.md, plan/learning-and-revision-plan.md, tracking/revision-queue.csv and reference/study-tracking.md from this repository. Check the latest session-history entry, revision history, study log and current exercise files. State the current unfinished task and timer state, then resume that step without restarting the assessment. Let me attempt it before showing solutions. Start a timer only when I explicitly signal starting study. Update the checkpoint and trackers from actual results. If you cannot read these files, tell me rather than guessing my progress.

## Time tracking

Follow reference/study-tracking.md. Start/pause/finish messages control recorded intervals. Git does not run a stopwatch, send notifications or update CSVs automatically. Existing Codex reminders remain tied to their original app/chat until separately recreated elsewhere. Current timer migration needs an actual stop time; do not count setup time as SQL practice.

### Excel study-hours report

Open [the Excel tracker](outputs/study-tracker/study-hours.xlsx). Daily shows each day's target, confirmed hours, behind/ahead hours and cumulative totals. Weekly shows Monday–Sunday totals, completion percentage and hours remaining. Sessions preserves the source intervals, including uncertain entries.

Targets are six hours per weekday and ten per weekend day (50 per full week). Tracking starts on 15 October 2026: that first partial week's target is 32 hours; earlier days are not charged. The initial calendar runs through 7 February 2027 and extends when refreshed after that date.

Behind/ahead compares confirmed time with targets for dates before the reporting date. Today's remaining target is shown separately because the day is still in progress. Future dates are not overdue. Unlogged hours mean no confirmed evidence, not proof that no study occurred; uncertain or running intervals are excluded. Hours are decimals: 1.50 means 1 hour 30 minutes. This comparison is for planning, not a requirement to make up missed hours.

tracking/study-log.csv remains the source of truth. The tutor must rebuild the Excel report after timer-log changes, on study-status requests, and at daily handoff. Close the workbook before rebuilding if Excel has locked it. Do not edit session data directly in the generated workbook; supply corrections to the tutor so both records stay consistent. The workbook's reporting date is a fixed IST snapshot, not an automatically advancing clock or live CSV connection.

Refresh from any working folder using Node and the bundled Codex spreadsheet runtime:

```bash
node tracking/update-study-tracker.mjs
```

The example assumes the repository root as working folder. The builder itself resolves data paths relative to its own location. It finds the bundled dependencies under the current user's home; set CODEX_NODE_MODULES to the supplied node_modules directory if the runtime is elsewhere. If node is not on PATH, invoke the node executable in the bundled runtime's dependencies/node/bin directory. A new machine can view the synced workbook in Excel without these authoring dependencies; rebuilding requires them. If unavailable, save the CSV/checkpoint and explicitly report the Excel snapshot as stale until refreshed.

Include the generated workbook and builder in the reviewed files when committing/pushing for another computer. Preview images and local runtime links are ignored.

### Exact phrases to use

| Send this message | Tutor action |
|---|---|
| `Start SQL` | Record the actual start time for SQL and confirm it in IST. Replace SQL with Python, dbt or another topic as needed. |
| `Pause` | Close the active interval at the actual time; the break is excluded. |
| `Resume SQL` | Start a new SQL interval after checking that none is running. |
| `Finish` | Close the active interval and save the checkpoint. |
| `Study status` | Report confirmed daily/weekly time, with running or uncertain time separately labelled. |
| `Study time` | Same as Study status: show today's and this week's confirmed hours and minutes, targets, remaining hours and closed-day shortfall. Show elapsed time in any running interval separately; do not change the timer. |
| `Today's schedule` | Read the checkpoint, agreed plan and revision queue; show today's IST study target, confirmed hours, remaining hours, a manageable set of due reviews and the next tasks in order. Adjust scope to demonstrated progress. Do not start a timer. |
| `Save checkpoint` or `This is the checkpoint` | Save the current learning state without stopping or starting a timer. |
| `Finish for today` | Close the active interval and save a dated end-of-day summary and exact next task. |
| `Read the checkpoint and continue` | Read the latest saved records and resume the pending step; do not start a timer automatically. |

These phrases are convenient shortcuts; equivalent clear instructions are valid too. Quoting or discussing a command is not executing it.

### Checkpoints without a reminder

The tutor must save relevant records after meaningful work without waiting for the learner to request a checkpoint. After saving, briefly confirm: `Checkpoint saved — [what was completed or remains pending]; next: [exact step]; timer: [state].` Do not claim a save before writing the files.

On `Finish` or `Finish for today`, save what was actually attempted, evidence and help used, remaining gaps, the exact next task, revision due and timer state. For the end-of-day summary, report confirmed study totals from the log and distinguish uncertain intervals. Keep dated outcomes in progress/session-history.md and the latest handoff in progress/current.md; a separate daily file is unnecessary.

If the learner leaves without an end-of-day message, the last saved checkpoint remains the handoff. This chat does not run a background midnight job when closed. At the next interaction, check whether the prior study day's closing summary is missing; reconstruct it only from saved evidence, label it as recorded later, and ask for any unknown stop time. Never invent work, an end time or a completed lesson to fill the gap. If there was no recorded activity, do not create a study session just because a date passed.

## Status

Repository prepared on 15 October 2026 for the private GitHub repository above. No exercise has yet been completed independently. February 2027 readiness and 15 LPA are goals, not promised outcomes.
