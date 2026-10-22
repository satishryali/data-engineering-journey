# data-engineering-journey

My practical data engineering learning journey: SQL, Python, PostgreSQL, dbt, Airflow, Docker, Snowflake, PySpark and Azure—with hands-on projects, exercises, revision tracking and tutor checkpoints.

This repository is the durable record of my tutoring, exercises, revision and project work. Chat history is useful context; this checkpoint and actual code are the source of truth.

## Start or resume here

On a new computer or in a new chat, begin with [START-HERE.md](START-HERE.md). It contains the current handoff, exact next step and the records the tutor must verify. Say: **Read START-HERE.md and continue from the checkpoint.**

1. Read AGENTS.md and progress/current.md.
2. Read plan/learning-and-revision-plan.md for the agreed schedule.
3. Inspect tracking/revision-queue.csv and the latest work before selecting a task.
4. After reviewed work, update progress/current.md, progress/session-history.md and the relevant trackers. Never mark a planned topic as completed.

Current project: [RRDAP](projects/rrdap/README.md), [RDS-001 Product Catalogue](projects/rrdap/tasks/RDS-001.md). Setup complete; awaiting the learner's approach. RetailFlow is superseded with all files/history preserved. Earlier CSV output/read-back remains deferred, not complete. See progress/current.md for timer state and evidence.

Say **Start Distribution Project** or **Continue Distribution Project** to load the next incomplete task without starting another timer. **Save my learning**, **Revise Distribution Project**, **Show Distribution Project progress** and **End session** use the [RRDAP workflow](reference/rrdap.md).

## Structure

- plan/: authoritative 13-week Azure interview curriculum and generated weekly milestones, 22 October 2026–22 January 2027.
- progress/: current checkpoint and concise session handoffs.
- tracking/: study intervals, revision queue and actual review history.
- tools/: notes and exercises organised by skill.
- projects/: integrated pipelines combining tools.
- reference/: supporting tutoring and time-accounting guidance.
- Notes/: Obsidian vault with Python notes, images and revision records; open this folder directly in Obsidian. See [vault setup and Git sync](Notes/README.md).

Each tool has README.md and notes.md. Add exercise folders as lessons are actually assigned. Store explanations of the problem, attempted code, expected output, mistakes and a changed example. Integrated projects belong in projects/, with one main README and run instructions.

## Codex commands on every computer

Your five role entries (Learning Coach, Notes Keeper, Mistake Keeper, Revision Coach and Progress Tracker), GitHub Agent utility, nine existing personal commands and portable installer are tracked in [codex/README.md](codex/README.md).
After cloning or updating this repository on another computer, run:

```bash
python codex/install_commands.py
```

Restart Codex to load the commands and personal-skill visibility preference. The installer
uses this checkout's actual path, backs up local changes, and leaves credentials and
study records untouched. See the linked guide for the full computer-switching workflow.

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

The [five-role learning coach](reference/learning-coach.md) coordinates Learning Coach,
Notes Keeper, Mistake Keeper, Revision Coach and Progress Tracker through one conversation.
Say **Start today's learning** to resume the genuine pending task without starting a timer.
You can also say **Start revision**, **Show my mistakes**, **Show today's learning**,
**Weekly review** or **Save checkpoint**. Your existing timer/checkpoint commands remain.
No new installation, dashboard, API or background agents are required.

The guide and [tracker operations](tracking/README.md) identify authoritative records.
The two former review systems now share the CSV queue/history; Notes/revision is generated.
Historical IDs, evidence and the old pending diagnostic are preserved in tracking/legacy.

- progress/current.md: one current checkpoint, updated in place with evidence, help used, weak points, exact pending task and timer state.
- progress/session-history.md: append one concise dated outcome per practical task or session block, including relevant planning changes; avoid an entry for every answer. Do not create a separate daily Markdown file by default.
- tools/<skill>/exercises/: preserve prompts, attempts, feedback and changed examples. Keep hints and final solutions separate from unanswered practice.
- Notes/: canonical Obsidian explanations and separate recall prompts; tools/<skill>/notes.md links to the relevant vault notes.
- tracking/: record study intervals, actual retrieval attempts and the next review due; never infer completion from a planned date.
- plan/: maintain the agreed curriculum and any deliberate scope changes.

The tutor batches learning-record updates at the explicit command boundaries in [Checkpoint commands](reference/checkpoints.md), including Pause, Resume, Start [topic], topic switches and save/finish/handoff requests. An exercise completion or done reply alone does not save records. Ordinary teaching replies do not trigger Markdown edits. Interim attempts stay in the active conversation until the next checkpoint, where code/evidence/help and actual outcomes are consolidated. Timer start/stop timestamps are still recorded immediately. Say `Save checkpoint` before closing the chat or changing computers: uncheckpointed exchanges are not yet durable repository records. No background or parallel writer is running. Git history preserves committed versions; a fresh chat must read the latest files.

## New tutoring chat prompt

> Act as my data engineering tutor. Read README.md, AGENTS.md, progress/current.md, plan/learning-and-revision-plan.md, tracking/revision-queue.csv and reference/study-tracking.md from this repository. Check the latest session-history entry, revision history, study log and current exercise files. State the current unfinished task and timer state, then resume that step without restarting the assessment. Let me attempt it before showing solutions. Start a timer only when I explicitly signal starting study. Update the checkpoint and trackers from actual results. If you cannot read these files, tell me rather than guessing my progress.

## Time tracking

Follow reference/study-tracking.md. Start/pause/finish messages control recorded intervals. Git does not run a stopwatch, send notifications or update CSVs automatically. Existing Codex reminders remain tied to their original app/chat until separately recreated elsewhere. Current timer migration needs an actual stop time; do not count setup time as SQL practice.

### Excel study-hours report

Open [the Excel tracker](outputs/study-tracker/study-hours.xlsx). Daily shows each day's target, confirmed hours, behind/ahead hours and cumulative totals. Weekly shows Monday–Sunday totals, completion percentage and hours remaining. Sessions preserves the source intervals, including uncertain entries.

Targets come from [study-targets.json](tracking/study-targets.json): six-hour weekdays before 22 October 2026, seven-hour weekdays from that date, ten-hour weekends throughout. The new full-week target is **55 focused hours**. Tracking starts 15 October: historical partial week 32 h; transition week 19–25 October 52 h; final preparation partial week 18–22 January 35 h. The preparation report runs through **22 January 2027** and extends for later reporting dates. Earlier dates, targets and recorded hours stay intact.

The [single authoritative roadmap](plan/learning-and-revision-plan.md) defines thirteen Thursday–Wednesday curriculum weeks plus 21–22 January verification buffer. Weekly hour reports remain Monday–Sunday. Weekdays allocate 1.5 h learning, 2 h practice, 2 h project, 0.5 h debugging/tests and 1 h revision/interviews. Weekend days allocate 2/2.5/3/1/1.5 h respectively. Actual learning evidence, help and project acceptance determine progress.

Use **Start interview practice** for one question without a timer or exposed answer; **Show my weaknesses** for observed gaps. [Interview preparation](plan/interview-preparation.md) uses the existing review history and skill model. [Engineering simulation](reference/engineering-simulation.md) adds reusable templates without solving RDS-001. [RecallLab](apps/recalllab/README.md) retains revision, coding, notes and persistence, and now exposes schedule, roadmap, project and interview views using the same authorities. It remains local; no public deployment was performed.

Behind/ahead compares confirmed time with targets for dates before the reporting date. Today's remaining target is shown separately because the day is still in progress. Future dates are not overdue. Unlogged hours mean no confirmed evidence, not proof that no study occurred; uncertain or running intervals are excluded. Hours are decimals: 1.50 means 1 hour 30 minutes. This comparison is for planning, not a requirement to make up missed hours.

tracking/study-log.csv remains the source of truth. The tutor must rebuild the Excel report after timer-log changes, on study-status requests, and at daily handoff. Close the workbook before rebuilding if Excel has locked it. Do not edit session data directly in the generated workbook; supply corrections to the tutor so both records stay consistent. The workbook's reporting date is a fixed IST snapshot, not an automatically advancing clock or live CSV connection.

Refresh from any working folder using Node and the bundled Codex spreadsheet runtime:

```bash
node tracking/update-study-tracker.mjs
```

The example assumes the repository root as working folder. The builder itself resolves data paths relative to its own location. It finds the bundled dependencies under the current user's home; set CODEX_NODE_MODULES to the supplied node_modules directory if the runtime is elsewhere. If node is not on PATH, invoke the node executable in the bundled runtime's dependencies/node/bin directory. A new machine can view the synced workbook in Excel without these authoring dependencies; rebuilding requires them. If unavailable, save the CSV/checkpoint and explicitly report the Excel snapshot as stale until refreshed.

Include the generated workbook and builder in the reviewed files when committing/pushing for another computer. Preview images and local runtime links are ignored.

### VS Code timer extension

ClockIt: Session manager (extension ID `octech.clockit`, installed version 1.9.0) is installed on the current computer. On another computer install it from Extensions or run `code --install-extension octech.clockit`. Installation does not migrate its local state.

Before activation, set these workspace settings to keep tracking manual and exports local:

```json
{
  "clockit.autoStartOnLaunch": false,
  "clockit.cloud.enabled": false,
  "clockit.enabledSinks": ["csv"]
}
```

They are currently in .vscode/settings.json, which is ignored by Git; recreate them on each computer. Merge these keys into existing settings rather than replacing unrelated configuration.

After activation, use the ClockIt CSV/folder control in the status bar to open its menu: Start time, Stop time, Pause/Resume time and Set focus timer. The installed version registers the focus/pause controls but does not list them separately in its Command Palette contributions. Start and stop are available as `Clockit: Start Time` and `Clockit: Stop Time`. If the controls do not appear, use `Developer: Reload Window`. Set focus timer takes the block duration and is intended to notify on expiry; notification delivery has not yet been tested on this computer.

No extension session or focus countdown was started during installation. The chat CSV remains authoritative until export integration is built and verified. ClockIt exports have a different schema; do not append them directly to tracking/study-log.csv or count the same period twice. Keep setup and off-editor study separate from automatic editor-activity measurements.

### Chat timer and checkpoint commands

| Send this message | Tutor action |
|---|---|
| `Start SQL` | Record the actual start time for SQL, save any unsaved learning context and update the handoff; confirm in IST. Replace SQL with Python, dbt or another topic as needed. |
| `Pause` | Close the active interval at the actual time; exclude the break and save a checkpoint. |
| `Resume SQL` | Start a new SQL interval after checking that none is running; save any unsaved learning context and update the handoff. |
| `Finish` | Close the active interval and save the checkpoint. |
| `Study status` | Report confirmed daily/weekly time, with running or uncertain time separately labelled. |
| `Study time` | Same as Study status: show today's and this week's confirmed hours and minutes, targets, remaining hours and closed-day shortfall. Show elapsed time in any running interval separately; do not change the timer. |
| `Today's schedule` | Read the checkpoint, agreed plan and revision queue; show today's IST study target, confirmed hours, remaining hours, a manageable set of due reviews and the next tasks in order. Adjust scope to demonstrated progress. Do not start a timer. |
| `Save checkpoint` or `This is the checkpoint` | Save the current learning state without stopping or starting a timer. |
| `Finish for today` | Close the active interval and save a dated end-of-day summary and exact next task. |
| `Read the checkpoint and continue` | Read the latest saved records and resume the pending step; do not start a timer automatically. |

These phrases are convenient shortcuts; equivalent clear instructions are valid too. Quoting or discussing a command is not executing it.

### Checkpoints without a reminder

The tutor saves at the checkpoint commands in [Checkpoint commands](reference/checkpoints.md), without waiting for an extra reminder. Done replies and ordinary teaching exchanges stay in conversation until that boundary. Batch the evidence since the last checkpoint instead of editing files after each response. After an actual save, briefly confirm the pending step and timer state. Do not claim a save before writing files. Timer events are recorded when they happen; routine explanations do not change the timer.

On `Finish` or `Finish for today`, save what was actually attempted, evidence and help used, remaining gaps, the exact next task, revision due and timer state. For the end-of-day summary, report confirmed study totals from the log and distinguish uncertain intervals. Keep dated outcomes in progress/session-history.md and the latest handoff in progress/current.md; a separate daily file is unnecessary.

If the learner leaves without an end-of-day message, the last saved checkpoint remains the handoff. This chat does not run a background midnight job when closed. At the next interaction, check whether the prior study day's closing summary is missing; reconstruct it only from saved evidence, label it as recorded later, and ask for any unknown stop time. Never invent work, an end time or a completed lesson to fill the gap. If there was no recorded activity, do not create a study session just because a date passed.

## Status

Repository prepared on 15 October; roadmap upgraded on 22 October 2026 for Azure Data Engineer assessment on 22 January 2027. RRDAP/RDS-001 remains active and unaccepted. SQL/Python evidence, deferred tasks and actual review dates remain in the checkpoint/trackers. The roadmap and hours establish planning, not interview readiness or a career outcome.

## Notes-driven revision

Open [the generated revision plan](Notes/revision/plan.md) for upcoming reviews,
initial assessment slots and notes coverage. The existing five-role coach maps note
sections to stable concepts and uses actual answered attempts to update learning state.
New notes are checked at planning/checkpoint boundaries; no background monitor runs.
