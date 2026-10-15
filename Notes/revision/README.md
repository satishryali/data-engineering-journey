# Revision workflow

Use the [five-role learning coach](../../reference/learning-coach.md) and
[tracker operations](../../tracking/README.md). The five responsibilities belong
to one tutor; no background agents or notifications are configured.

## One source for each state

- tracking/revision-queue.csv owns stages and next-review dates.
- tracking/revision-history.csv owns actual answered assessment events.
- tracking/topic-map.json owns stable concepts, prerequisites, source versions and
  many-to-many links to broad exercises. Relationships do not transfer scores.
- topics.json, reviews.jsonl and mistakes.md here are generated views; refresh them
  with `python tracking/coach.py refresh` from the repository root.
- The original topics, empty answered-review history and full old instructions are
  preserved unchanged under tracking/legacy/. Original IDs and dates remain there.

The old diagnostic-dict-001 fallback question remains unanswered and deferred.
The learner's later PY-002 dictionary read/update/print request in progress/current.md
controls the next task. A saved notebook has not yet been assessed against that task.
Do not restart assessment or begin teaching during setup.

## Teaching and saving

Retrieve before explaining. Ask one meaningful task and wait; mix explanations,
prediction, debugging, reconstruction and applications. Use progressive hints and
record notes consulted, assistance and uncertainty. [Recall questions](questions.md)
are separate from worked explanations. Source-note errors are not learner mistakes.

Ordinary feedback stays conversational. Save at task completion, pause/topic switch,
Save checkpoint, Finish or Finish for today, not after every answer. Timer events
are immediate. Stable attempt/review/checkpoint IDs prevent duplicate records.
Checkpoint-only commands never change timers. See the shared guide for recovery.

## One date rule

Stages 0-4 use 1/3/7/14/30 days from the actual latest scored assessment date in IST.
First scored assessment sets stage 0. Delayed score 0/1 or assistance resets to stage 0;
independent 2 retains stage and independent 3 advances one stage, capped at 4.
Unknown help is not independence; an unscored event preserves the schedule.
Immediate correction never changes the delayed schedule or proves retention.
Existing valid queue dates remain unchanged. Unassessed concepts have no invented dates.

Prioritise weak prerequisites and spread overdue reviews across manageable sessions,
usually 15-20 minutes unless requested otherwise. Changed source notes affect only
linked concepts; preserve history. No date, reminder or attendance proves completion.

## Requests

Start revision; Revise [topic]; Show progress; I have 5 minutes; Practise coding;
Stop and save. Also: Start today's learning; Show my mistakes; Show today's learning;
Weekly review; Save checkpoint. Status/planning and task selection do not start timers.
Reminders are optional and separate; do not invent a notification time.
