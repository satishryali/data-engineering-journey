---
name: mistake-keeper
description: Show or maintain the learner's evidence-backed mistake tracker, distinguish recurring gaps from source-note errors, and plan targeted follow-ups through the five-role workflow.
---

# Mistake Keeper

This is the Mistake Keeper entry in the shared five-role workflow, not a separate
background worker. Use the installed learning checkout `{{LEARNING_REPO}}`, even when
invoked from another project. If unavailable, ask for a verified checkout; never invent
mistakes or write records into an unrelated project.

Read `AGENTS.md`, `reference/learning-coach.md`, `progress/current.md`,
`tracking/mistakes.json`, `tracking/topic-map.json` and relevant actual attempts and
feedback. `Notes/revision/mistakes.md` is generated; do not edit it independently.

Without a specific request, show relevant open/practising mistakes, their evidence
and a manageable follow-up. Do not begin an assessment or alter a timer merely because
this skill was selected.

At checkpoint boundaries, record only important observed gaps with stable mistake IDs,
original first/latest dates, distinct attempt IDs, evidence, expected behaviour,
confirmed/hypothesised cause, supplied correction/help, follow-up and review links.
Separate conceptual gaps, debugging/approach issues, environment problems and useful
recurring syntax slips. Preserve learner wording or label paraphrases. Historical
entries retain their original observation date and source, not the setup date.

Count recurrence by distinct observed attempts, not repeated mentions or saves. Use
the existing coach helper's duplicate-safe updates and regenerate the readable index.
Do not mark a mistake verified without relevant delayed independent practice; repeating
an explanation or correcting source notes is insufficient. Keep unknown values unknown.

Do not start/stop timers, manufacture review events, fix intentionally incorrect learner
attempt files, commit, push, create reminders or message another chat as a side effect.
