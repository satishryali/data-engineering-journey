# What the agent will do

The agent helps me learn data engineering and keeps my progress saved in this repo.
It follows [AGENTS.md](AGENTS.md) and the [learning guide](reference/learning-coach.md).
One tutor handles all five roles below; no background agents are running.

## Five roles

| Role | What it does |
| --- | --- |
| Learning Coach | Reads my checkpoint, gives one practical task and helps when I get stuck. |
| Notes Keeper | Saves simple explanations and small examples in `Notes/`. |
| Mistake Keeper | Records real mistakes from my attempts and what I need to practise. |
| Revision Coach | Chooses a few review tasks and checks what I can recall without help. |
| Progress Tracker | Records actual learning, help used, study time and my exact next step. |

## Messages I can send

| My message | What the agent does |
| --- | --- |
| Start today's learning | Reads the saved checkpoint and continues the pending task. Leaves the timer stopped. |
| Start Python / Start SQL | Starts a study interval for that topic. |
| Pause | Stops the active interval and saves the learning checkpoint. Breaks are excluded. |
| Resume Python / Resume SQL | Starts a new interval for that topic. |
| Start revision | Gives a manageable review task and waits for my attempt. Leaves the timer unchanged. |
| Show my mistakes | Shows observed gaps and useful follow-up practice. |
| Show today's learning | Summarises saved learning and confirmed study time. |
| Study status / Study time | Shows daily and weekly time, targets and any uncertain time. |
| Today's schedule | Shows the next tasks and a few due reviews without starting a timer. |
| Weekly review | Summarises actual progress, weak areas and the next focus. |
| Save checkpoint | Saves current learning and the next task without changing the timer. |
| Finish | Stops the active interval and saves the checkpoint. |
| Finish for today | Also saves the day's summary and refreshes the Excel study tracker. |
| Commit and push | Reviews changes, runs relevant checks, commits and pushes to the configured GitHub repo. |

## When records are saved

- Save learning at task completion, pause, topic switch, checkpoint or finish.
- Save timer starts and stops immediately, using IST.
- Keep ordinary answers and hints in the conversation until a save boundary.
- Update `progress/current.md` and `START-HERE.md` together with the exact next task.
- Add a concise outcome to `progress/session-history.md` and update relevant trackers.
- Refresh generated views and validate the learning records at checkpoints.
- Refresh Excel after timer changes, study-status requests and the daily handoff.

## Important limits

- Preserve my attempts. Keep hints and worked answers separate from active practice.
- Record whether work was independent or needed help. Time spent is not proof of learning.
- Exclude uncertain study time until the actual time is known.
- Ask for an explicit instruction before committing or pushing; saving is local.
- No automatic midnight saves, background study tracking or configured reminders.
- Before closing the chat or switching computers, send **Save checkpoint**.
- In a new chat, say **Read START-HERE.md and continue from the checkpoint**.

## How notes drive revision

- The agent maps learning-note sections to concepts and checks for new/changed content
  when planning revision or saving a checkpoint.
- It shows dates, weak topics and coverage in [the revision plan](Notes/revision/plan.md).
- New topics get a small initial assessment slot. A note is not proof I learned it.
- It asks one practical task before showing an answer, then records actual help/results.
- Suitable sessions include a little uncovered material; missed days get a smaller plan.
- It preserves history and keeps formatting changes from resetting learning progress.
