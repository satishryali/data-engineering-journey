# Shared learning records

Read [the five-role guide](../reference/learning-coach.md) for ownership and session
behaviour. The learner talks to one tutor; these files reduce repeated administration.

- `revision-queue.csv`: authoritative due dates/stages for exercise and concept IDs.
- `revision-history.csv`: actual answered events; original columns retained, with IDs,
  event kind, nullable score/help and a lossless `event_json` payload added.
- `topic-map.json`: concept identities, prerequisites, source hashes/history and associated
  exercise IDs. Association is not evidence that all concepts were assessed.
- `mistakes.json`: important observed mistakes with distinct attempt observations.
- `skill-state.json`: dimension-specific observations. Read latest dated observations in
  append order; unobserved dimensions are unassessed. Delayed retention comes only from
  actual delayed events in review history, not from initial-learning observations.
- `study-log.csv`: authoritative time source. Existing Excel script/report unchanged.
- `checkpoint-index.json`: duplicate-prevention index; daily prose remains in
  `progress/session-history.md`. IDs/hash/evidence key are not proficiency records.
- `legacy/`: original notes-revision records and instructions, retained unchanged.

## Saving a checkpoint

The tutor prepares a JSON event in a temporary local file and runs:

```bash
python tracking/coach.py record --event /path/to/event.json
python tracking/coach.py validate
```

Required fields:

```json
{
  "checkpoint_id": "CP-unique-session-block",
  "date_ist": "2026-10-16",
  "kind": "learning",
  "summary": "A concise factual outcome, assistance used and exact next step.",
  "evidence_ids": ["path/to/saved-attempt.py#distinct-attempt-id"],
  "reviews": [],
  "mistakes": [],
  "skill_updates": []
}
```

This example is a schema, not a recorded session. Every evidence path must exist inside
the checkout. Stable attempt anchors identify a submission; the tutor verifies the actual
code/output and cited section. Preserve attempts before saving, never replace them with
a tutor answer. `kind: setup` forbids learning/review/skill/mistake outcomes.

For an actual answered review, add an object to `reviews` with:

| Field | Meaning |
| --- | --- |
| review_id, attempt_id | Stable event and actual attempt identities |
| item_id | The exact exercise **or** concept row being assessed |
| topic_ids | Related concept IDs, checked against topic-map; no automatic schedule propagation |
| attempt_date_ist | Actual attempt date, never a planned due date |
| review_kind | initial_learning, diagnostic, application, immediate_correction or delayed |
| result | independent, assisted, needs_guidance or unknown |
| score | 0–3, or null when not assessed; no invented scores |
| help_used, notes_used | true, false or null for unknown |
| hints_used | Nonnegative count or null for unknown |
| evidence | One of the batch's evidence IDs |
| question, answer, feedback | Actual saved prompt, answer and feedback when available |
| timestamp | Optional actual timezone-aware timestamp; must agree with IST date |

Original fields and extra supplied fields are retained in `event_json`. A single task can
provide evidence for multiple concepts: use a separately identified assessment per
actually assessed item, retaining the shared attempt reference. Do not copy a broad result
to every linked concept. The same item/attempt cannot be recorded twice under new IDs.

`mistakes` contains full new mistake objects or updates keyed by `mistake_id`; use the
schema of existing entries. New observations carry distinct `attempt_id`, original
`observed_date_ist`, `evidence` and a labelled paraphrase/observation. Cause confidence
is confirmed or hypothesis. Status is open, practising, or
verified_on_delayed_independent_practice; verification additionally requires a relevant
independent delayed `verification_review_id`. A correction alone cannot verify it.

`skill_updates` appends observations with observation_id, item_id, dimension, state,
observed_date_ist, evidence and help_used (possibly null). Dimensions are explaining,
reading_predicting, modifying, building and debugging. State is unassessed,
needs_guidance, assisted or independent. Keep earlier observations to show changes.

For a changed task/context, also supply **both** `checkpoint_text` and `handoff_text`
(complete updated Markdown), with an identical `next_task` phrase in each. This makes
the two handoff updates one recoverable batch. Notes are edited deliberately before
the batch; include their evidence references rather than arbitrary write paths in JSON.

## Validation, weekly summaries and recovery

```bash
python tracking/coach.py refresh
python tracking/coach.py validate
python tracking/coach.py status --date 2026-10-15
python tracking/coach.py weekly --week 2026-10-12 --as-of 2026-10-15
python -m unittest discover -s tracking/tests -v
```

The weekly command requires a Monday start and labels partial or retrospectively
reconstructed summaries. It reuses the study log and dated observations/reviews, linking
daily history instead of duplicating every exchange. It does not create learning events.
The tutor supplements the saved evidence with a concise next-week focus where warranted.

An interrupted record/refresh leaves ignored `tracking/.coach-transaction.json` containing
only the proposed known record files and their prior hashes. Run `python tracking/coach.py
recover` before continuing or using Git. It completes the same batch idempotently and
refuses to overwrite concurrent edits. Resolve conflicts against preserved evidence;
never discard an interrupted event just to make validation pass. Work on one computer
at a time. No automatic monitoring or notifications are provided.
