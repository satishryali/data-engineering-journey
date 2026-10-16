# Checkpoint commands

Learner preference, 16 October 2026: save the learning history at clear checkpoints, not after each answer, hint or completed exercise. One tutor does this when the command arrives; no background writer is running.

## Commands that save

| Command or clear request | Checkpoint action | Timer action |
| --- | --- | --- |
| Pause / Pause timer / Pause time | Save all meaningful unsaved work and the exact pending step | Close the active interval immediately |
| Resume Python / Resume [topic] | Save any unsaved context and update the active topic/handoff | Start a fresh interval; exclude the break |
| Start Python / Start SQL / Start [topic] | Save any unsaved context and update the active topic/handoff | Start only if no interval is running |
| Pause SQL and start Python | Save the outgoing topic and incoming next step together | Close/open at one timestamp, without overlap |
| Switch to [topic] / Let's do [topic] now | Save the outgoing work and new pending task | Do not silently start a timer; resolve an active timer's topic if needed |
| Save checkpoint / This is the checkpoint / Save our progress | Save the unsaved learning history | Leave timer unchanged |
| Finish / Finish this session | Save session evidence and handoff | Close the active interval |
| Finish for today / Done for today | Save checkpoint and daily summary | Close the active interval |
| Stop and save | Save and end the teaching exchange | Close an interval only when stopping study is clear |
| I'm closing this chat / I'm switching computers | Save the handoff before leaving | Close a timer if stopping study is clear; otherwise ask only about its actual stop |

Recognise natural-language equivalents by intent. A quoted command or discussion of commands does not execute it. An ambiguous standalone stop needs clarification; an ordinary done means an exercise submission, not Finish for today.

## What to preserve

- Meaningful tasks, actual attempts, code/output, questions and explanations since the last checkpoint.
- Mistakes and corrections, help supplied, notes consulted when known, and what remains unverified.
- Completed, partial and pending work; exact next task; current timer and confirmed study time.
- New preferences and decisions that a future tutor needs.

Use progress/current.md and START-HERE.md for the concise current handoff; append one outcome block to progress/session-history.md. Preserve attempt snapshots and important overwritten drafts separately. Keep explanations in Notes and update the canonical mistakes, skill and review trackers only when evidence supports it. Run the shared notes inventory/refresh/validate workflow. These are useful learning records, not a claim of a verbatim chat export.

Save only new evidence since the last checkpoint. Never re-score or duplicate old attempts, mistakes or daily history. On a resume/start with no new learning, update the handoff and timer state without appending a second learning outcome. Timer timestamps are still written immediately and Excel refreshed after log changes.

## Commands that do not save learning history

Ordinary answers, done, check now, hints, explanations and successful exercise reviews stay in the conversation until a checkpoint. Do not edit learning trackers after each one.

Study status/time, Today's schedule, Show progress, Show my mistakes, Show today's learning and Weekly review are information requests, not implicit session checkpoints. Required report or revision-plan refreshes may still run. Start today's learning, Read the checkpoint and continue, Start revision and Practise coding load/select work without starting a timer or checkpointing every task. If explicitly switching away from ongoing work, use the topic-switch checkpoint rule.

An explicit request to create/update a note, change instructions, or save a file authorises that requested write immediately. Preserve its administrative handoff without inventing learning success; this exception does not authorise unrelated per-answer tracker writes.

Saving locally does not commit or push. Future AI sessions must read the repository handoff; a different computer needs the latest files transferred through the learner's authorised Git workflow.
