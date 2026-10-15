# Five-role learning coach

One tutor speaks with the learner. These are exactly five coordinated responsibilities,
not independent agents, background workers or a new service. Python helpers only run
when invoked. No lesson, timer, reminder, commit or push is started by setup.

Notes Keeper follows [the learner's note-writing style](note-style.md): short headings,
simple words and more small examples with output, matching the existing personal notes.

| Role | Owns | Required behaviour |
| --- | --- | --- |
| Learning Coach | Conversation and task selection | Read the checkpoint; explain why first; give one meaningful bounded task combining prediction/code/output/reasoning when useful. Avoid repetitive confirmations. Respect prerequisites, available time and demonstrated ability. Use progressive hints; follow a worked example with reconstruction or a changed problem. Never solve the learner's active attempt file without permission. |
| Notes Keeper | Explanations in `Notes/` | Inspect existing notes before adding material. Link related concepts rather than repeat them. Include purpose, simple explanation, a runnable example with expected behaviour, applications, pitfalls and separate recall prompts. Capture meaningful learner questions at checkpoint boundaries. Preserve useful original wording; explain targeted corrections. Verify uncertain claims using official sources; source-note errors are not learner mistakes. Do not write ahead of actual study. |
| Mistake Keeper | `tracking/mistakes.json` | Record important observed misconceptions, approach/debugging gaps and environment problems separately. Minor slips need tracking only when useful or recurring. Keep stable IDs, dated source attempts, assistance, cause confidence, follow-up and review links. Count distinct observed attempts, not mentions. Repetition of an explanation does not verify a correction. |
| Revision Coach | Queue and actual review events | Retrieve before explaining; ask one meaningful task and wait. Mix prediction, debugging, reconstruction, explanations and applications. Record hints, notes consulted and unknown assistance honestly. Distinguish initial learning, immediate correction and delayed retrieval. Prioritise weak prerequisites; spread overdue reviews across manageable sessions. Preserve valid history when source notes change. |
| Progress Tracker | Checkpoint, daily history, skill evidence and weekly summaries | Separate hours from learning outcomes. Track explaining, reading/predicting, modifying, building and debugging separately. Use unassessed, needs_guidance, assisted or independent with evidence. Delayed retention is separate. Report unassessed areas and manageable next steps; roadmap dates and attendance never prove learning. |

## Sources of truth

| State | Authoritative source | Other views |
| --- | --- | --- |
| Current pending task and context | `progress/current.md` | `START-HERE.md` is its concise handoff; update together |
| Daily actual outcomes | `progress/session-history.md` | Status/weekly summaries cite its sections; no separate daily files |
| Study intervals | `tracking/study-log.csv` | Existing Excel builder/report unchanged; running/uncertain time excluded |
| Topic identities, source versions and exercise/concept relationships | `tracking/topic-map.json` | Stable concept IDs retained from the notes inventory; a broad exercise can map to many concepts |
| Review stage and due dates | `tracking/revision-queue.csv` | Existing exercise IDs retained; concept rows have their own state |
| Answered assessment events | `tracking/revision-history.csv` | Stable `review_id`; event kind distinguishes initial, immediate and delayed work |
| Important mistakes | `tracking/mistakes.json` | `Notes/revision/mistakes.md` is generated; do not edit it independently |
| Skill dimensions and retention evidence | `tracking/skill-state.json` | Status and weekly summaries reference the same observations |
| Checkpoint deduplication | `tracking/checkpoint-index.json` | Stores IDs, hashes and evidence keys, not a second daily narrative |
| Explanations | `Notes/` | `tools/sql/notes.md` and `tools/python/notes.md` link to the vault |

`Notes/revision/topics.json`, `reviews.jsonl` and `mistakes.md` are generated compatibility
views. Run `python tracking/coach.py refresh`; never maintain a second schedule there.
Original notes-revision JSON/JSONL and its instructions are preserved byte-for-byte in
`tracking/legacy/`. No old ID, original timestamp, hash, pending question or history was
discarded. See `tracking/legacy/README.md` for the migration and many-to-many mapping.

An exercise result must **not** be copied to every linked concept. Record only the
concepts actually assessed. Broad SQL/Python rows retain their dates and evidence;
the ten previously unassessed notes concepts stay unassessed with no invented dates.
The older `diagnostic-dict-001` remains in the archive, deferred by the learner's
later request for the simpler PY-002 read/update/print exercise. A notebook exists
but has not been assessed as completing that specific task. Do not restart assessment.

## Session and checkpoint cycle

At start, read AGENTS, this guide, checkpoint/handoff, recent daily history, the plan,
queue, mistakes, skill evidence and relevant source attempts/feedback. Resolve conflicting
pending prompts using actual evidence and the latest learner instruction. Briefly state
one next task. Planning/status requests never silently start a timer; ask for an explicit
study-start signal separately. `Start today's learning` resumes the task without a timer.

During teaching, respond conversationally. Keep interim answers and feedback in context;
do not interrupt every answer with file edits. If evidence is missing or a claim is
uncertain, say so rather than assigning proficiency. Do not expose worked answers in
the retrieval prompt. `Notes/revision/questions.md` holds unanswered prompts separately
from explanations. Do not assess topics merely because their notes exist.

At task completion, pause/topic switch, Save checkpoint, Finish or Finish for today:

1. Preserve actual attempts, output, questions and help used. Give distinct attempt IDs
   to distinct submissions; include a section anchor for combined historical files.
2. Update only relevant notes, mistakes, actual review events and skill dimensions.
3. Update current checkpoint and handoff consistently; preserve the exact pending task.
4. Append one concise daily block for this evidence, using a stable checkpoint ID.
5. Regenerate derived views and validate references. Confirm only files actually saved.

Timers are the exception: record actual start/pause/finish timestamps immediately using
`reference/study-tracking.md`, prevent overlaps, and reuse the existing Excel report.
Checkpoint-only commands never change time state. `Finish` closes the interval plus
checkpoint; `Finish for today` also records the daily handoff. `Stop and save` ends the
teaching exchange and saves; close a running interval only if the learner clearly means
to stop study. Do not reinterpret a status query as a timer instruction.

Repeated saves with the same checkpoint ID/evidence must be no-ops. Do not append another
daily block for old evidence, count the same mistake observation twice or resubmit a
review under a new ID. A genuine new attempt gets a new attempt ID. The helper rejects
conflicting reuse of IDs and repeated evidence batches. Unchanged source-note hashes do
not create reassessment work. Changed hashes flag content review, never reset all history.

## One scheduling rule

All intervals run from the **actual latest scored assessment date in IST**, not the
original learning date or a missed due date. Stages 0–4 mean 1, 3, 7, 14 and 30 days.
Existing valid queue dates are preserved during migration.

- First scored initial learning/diagnostic/application: stage 0, due next day.
- Delayed score 0/1 or any known assistance: stage 0, due next day.
- Independent delayed score 2: keep stage; independent delayed score 3: advance one
  stage, capped at 4. Independence requires explicit no hints, no notes and no help.
- Unknown assistance is not false. It cannot advance a stage; use early practice when
  scored evidence is incomplete. Unscored events preserve the unknown score and do not
  change the schedule. Record what is known rather than manufacture a score.
- Immediate correction never advances/resets the delayed stage or moves a due date.
  Same-day correction is not delayed retention. A delayed event must occur on a later
  date than the item's previous dated attempt. No automatic mastery or 60-day extension.

Use scores 0=major gap/unable, 1=partial/substantial help, 2=independent but incomplete,
3=independent with sound reasoning/application. Scores describe the event; separate
result/help fields prevent an assisted correct answer being labelled independent.

Due is a planning signal, not completion. Select a few important weak prerequisites,
keep revision around 15–20 minutes unless the learner requests otherwise, and shorten
scope when time is limited. Unassessed inventory is not an overdue backlog.

## Requests

| Learner phrase | Action |
| --- | --- |
| Start today's learning | Read checkpoint and select the next bounded task; no automatic timer |
| Start revision / Revise [topic] / I have 5 minutes | Select a manageable retrieval task; wait for an answer; no automatic timer |
| Show my mistakes | Show relevant open/practising mistakes and evidence, without starting a lesson |
| Show today's learning | Summarise the dated daily history and confirmed study time; label missing records/uncertainty |
| Weekly review | Summarise actual work, dimension-specific independence, recurring gaps, delayed reviews, unassessed areas and a manageable next focus |
| Save checkpoint | Batch the current learning evidence without changing timers |
| Show progress / Practise coding / Stop and save | Preserve the prior revision commands with this shared save policy |

The skill picker includes five entries: Learning Coach, Notes Keeper, Mistake Keeper,
Revision Coach and Progress Tracker. Invoke them as `$learning-coach`, `$notes-keeper`,
`$mistake-keeper`, `$revision-coach` and `$progress-tracker`; type `/` to search by name.
All existing nine slash skills remain. These entry points are not additional roles.
No installation is required for these natural
requests when this repository is open in Codex. The skills also read this guide after
their ordinary portable installer update; no separate role workers or agent processes exist.

## Small helper, validation and interrupted updates

Requires only Python 3.11+ already used by the command installer:

```bash
python tracking/coach.py validate
python tracking/coach.py refresh
python tracking/coach.py status --date 2026-10-15
python tracking/coach.py record --event /path/to/checkpoint.json
python tracking/coach.py weekly --week 2026-10-12 --as-of 2026-10-15
python -m unittest discover -s tracking/tests -v
```

The tutor prepares the event; the learner need not fill forms. Event shape is documented
in `tracking/README.md`. The helper does not judge answers, edit attempt files, start
timers, rebuild Excel, browse sources or generate notes from unstudied material.

It validates a complete batch before writing, then records the planned writes in the
ignored `tracking/.coach-transaction.json`. Writes replace complete files atomically.
`python tracking/coach.py recover` completes an interrupted batch; it refuses to replace
files edited independently since the transaction started. Recover before manual edits,
switching computers, or Git operations. Do not commit a half-applied batch. Derived-view
refresh can be rerun. Work on one computer/writer at a time; no background locking service.

A weekly summary is generated on request or at the next session after a week closes,
from saved evidence. The helper includes exact dated checkpoint blocks, source references,
confirmed time, actual delayed events and skill observations; the tutor writes a concise
evidence-based interpretation and next-week focus. Label retrospective reconstruction and
partial weeks explicitly. No missing interval is inferred from silence. Existing historical
prose remains valid evidence even before checkpoint IDs were introduced.

There is no continuous monitoring, midnight job, notification or background agent.
Reminders are optional and separate; no notification time or learning result is invented.

## Notes drive revision

Keep the same five roles. `tracking/topic-map.json` now also owns `note_inventory`:
each note file is either excluded with a reason, or split into direct content under
headings. Every included section has `topic_ids`; related sections reuse IDs. Empty
container headings and headings inside code fences are not learning sections. Images,
app configuration, indexes, generated views, administrative instructions, empty tool
note templates and link-only tool notes are excluded with reasons. A new substantive
tool note must be mapped even when it used to be an empty template.

At Start revision, Today's schedule, Weekly review and checkpoint boundaries:

1. Run `python tracking/coach.py notes-sync --date YYYY-MM-DD` with the actual IST date.
   This inventories files and flags gaps/changed sections; it never judges learning.
2. Inspect new content and affected source headings. Add a useful concept to the same
   topic-map/CSV queue only when no existing concept fits. Preserve IDs and older hashes.
   Add each section's topic mapping and the topic's `note_sections` backlink. Exclude
   only with a specific reason. New concepts get `not_attempted`, blank actual review/
   success/due fields, prerequisites and a proposed `initial_assessment_date_ist`.
3. Spread initial slots over suitable sessions: at most one new diagnostic concept,
   usually five minutes, alongside about ten minutes of weak/due practice. Dates are
   adjustable planning slots, not overdue retention or proof of learning. Replan missed
   slots; never restart the course or dump the backlog. Current slots start 16 October,
   one per day; prerequisite readiness and learner time take precedence.
4. Refresh and validate. New/unmapped sections fail coverage validation. The helper
   detects content changes conservatively, ignores ordinary prose wrapping/spacing,
   and flags only mapped concepts. Formatting never resets scores or dates. Inspect
   flags: a wording change need not require reassessment. Keep content-change history;
   after inspection clear `changed` on the inventory section and the topic's
   `needs_reassessment` only when justified by inspection or actual reassessment.
5. Read relevant notes privately, check questionable technical claims against official
   docs before teaching, and choose a bounded task. Existing source issues in logging,
   paths, Vault and dbt seeds still need checking when those lessons arise. They are
   not observed learner mistakes. No continuous monitoring is running.

`Notes/revision/plan.md` shows due today, overdue, upcoming reviews, initial slots,
weak topics, section mappings/exclusions, evidence/help and coverage gaps. Its date is
fixed to the last planning/checkpoint run. Run notes-sync on a later day before using it.
`coach.py status --date ...` also reports bounded candidates without changing timers.

Use these displayed concept states (derived from exact-item review evidence):

- Unassessed: no scored non-immediate concept assessment yet.
- Learning with help: latest scored assessment was incorrect/assisted/incomplete help evidence.
- Applied independently: latest scored initial/application assessment was independently
  successful, with explicit no hints, notes or help.
- Demonstrated on delayed review: latest scored delayed assessment was independently
  successful on a later date than a previous attempt for this exact item.

Retain scores, help, notes, hints and dimension evidence alongside these broad labels.
They describe demonstrated performance, not a memory probability. An immediate answer
never promotes delayed status. A later failed/assisted assessment shows a current gap;
historical successes remain in history. Unknown/unscored evidence does not invent success.
Do not copy historical exercise outcomes to concept rows. Current concept counts can be
zero while SQL exercise evidence is independently demonstrated in some dimensions.

Count mapped learning sections, topics assessed, topics actually practised on a delayed
review, and topics needing help separately. Delayed practice can be incorrect or assisted;
it does not mean retained. Weekly review also reports actual delayed scores/help,
repeated mistakes and neglected topics. Neglect means a missed initial slot or at least
30 days since successful independent application (a planning heuristic). The last date,
prerequisites, due date and recurring mistakes inform selection. The helper suggests
at most two targets, substitutes a weak prerequisite for a blocked broad exercise, and
avoids assigning its linked concept as another copy of the same task. Tutor judgement
and the learner's selected pending task remain authoritative.

Reserve one small diagnostic slot in suitable sessions so uncovered notes receive
practice. If notes outgrow that capacity, report counts and the minimum sessions needed;
reduce scope together. No promise that unlimited notes fit a fixed daily interval.

Command integration:
- Start revision: synchronise mappings, inspect notes/state, choose a task and wait for
  the learner's attempt without showing answers. Teach missing understanding first.
- Today's schedule: include a bounded revision block beside the pending learning task.
- Weekly review: include coverage, delayed performance, recurring mistakes and neglected topics.
- Save checkpoint: save actual answered events with nonempty `question` and `answer`,
  then synchronise note mappings and generated views; pending prompts cannot be events.

All existing timer behaviour, checkpoint deduplication and 1/3/7/14/30-day scheduling
rules remain. Planning dates never occupy `next_review_date_ist` until actual scored
learning warrants a follow-up. No timer, quiz or review is started by this setup.
