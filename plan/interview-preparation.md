# Interview preparation

Target: independent interview and pipeline-building evidence review on **20 January 2027**, alongside the [authoritative roadmap](learning-and-revision-plan.md). Foundation, transformation and Azure demonstrations are planned for November 15, December 6 and December 27. Apply now to suitable SQL/PLSQL, ETL and Python Data Engineer roles, describing existing employment and educational projects truthfully. All categories start from existing evidence or unassessed; this setup creates no results.

## Weekly routine

Use the existing eight weekly revision/interview hours, without adding another time budget.

| Day | Interview portion of the revision block |
| --- | --- |
| Monday | 20 minutes SQL coding with an unfamiliar small input |
| Tuesday | 20 minutes Python coding and test explanation |
| Wednesday | 20 minutes current technology; PySpark once prerequisites permit |
| Thursday | 20 minutes pipeline troubleshooting and architecture reasoning |
| Friday | 20 minutes project discussion and truthful experience explanation; inspect one target job description |
| Saturday | 45 minutes mixed interview, then feedback within the 90-minute block |
| Sunday | 30 minutes changed-input retry and weekly evidence/gap review within the 90-minute block |

The rest remains available for due retrieval and reconstruction. Before Azure topics have been introduced, use relevant foundation questions or a short unscored diagnostic. Do not force an advanced mock from the calendar alone. In January, replace the Saturday interview portion with a **75-minute timed mock**: 25 coding, 15 architecture, 15 troubleshooting, 10 project, 10 behavioural/experience. Reserve the other 15 minutes for priority due retrieval; feedback can use Sunday's block. Time measures performance only if a timer actually records it; never invent elapsed time.

## Question bank and selection

[questions.json](../tracking/interview/questions.json) contains reusable tutor-authored prompts with stable IDs, category, difficulty (foundation/intermediate/advanced), prerequisites, task/scenario/input/expected result, suggested time and official source references. Sources support topic coverage, not a claim that an employer asked the question. No answers are stored with prompts. Hints and worked solutions are given separately only after an attempt or explicit request; preserve the original attempt first.

`python tracking/interview.py question --id INT-SQL-001` prints a prompt without saving an assessment or starting a timer. `python tracking/interview.py validate` checks category coverage and schema. Select one question using current evidence and prerequisite readiness. Questions can be adapted to changed input; retain question ID plus the actual presented wording. Do not present the bank's future project scenarios as current RRDAP requirements.

## Evidence and rubric

For each actual attempt, retain question/variant, actual answer/code/output, date, source paths, help, hints, notes consulted, and measured timing if known. Rate the observed dimensions 0–3 or null if not assessed:

| Dimension | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Correctness | Cannot meet core result | Partial result, major errors | Correct core with missed edge case | Correct result and relevant edge cases |
| Reasoning | No usable explanation | Major gaps | Sound core, incomplete tradeoff | Explains choices, assumptions and alternatives |
| Independence | Unable after help | Substantial guidance | Minor help; record it | Explicit no hints, notes or help |
| Troubleshooting | Cannot isolate failure | Guesses without checks | Finds cause with incomplete verification | Uses evidence, verifies fix and regression |
| Communication | Cannot describe approach | Unclear sequence | Understandable with missing context | Clear purpose, approach, results and limits |

Do not average these into mastery. A correct answer with help is assisted. Unknown help stays unknown. Existing skill dimensions remain explaining, reading_predicting, modifying, building and debugging; map only what was actually observed, rather than introducing a competing score system. Communication/reasoning can support explaining; runnable independent implementation can support building; troubleshooting can support debugging. Preserve the rubric as optional `assessment` metadata in the existing review event's lossless `event_json`.

At an existing checkpoint boundary, record through `coach.py record`: stable attempt/review IDs, nonempty actual question/answer, exact item and related concept IDs, review kind, result, nullable score/help and source evidence. Reuse existing item identities; register a genuinely new assessed item with topic-map/queue before recording, with no invented earlier dates. Planning prompts are never answered reviews. Apply the shared 1/3/7/14/30-day rule from the latest actual scored date. Immediate correction is not delayed retention.

## Readiness review

Report all 16 bank categories with actual assessed dimensions, latest evidence/help, delayed variants and remaining gaps. Use `unassessed`, `needs_guidance`, `assisted` or `independent` at the observed dimension level. A practical readiness signal is independently handling changed coding tasks, explaining a small architecture, diagnosing a failure and defending actual project decisions on separate occasions. It is a judgement from evidence, not a guaranteed pass rate or a date-based badge.

Explain professional work honestly: describe database development/support responsibilities as employment, RRDAP as an educational simulation, and cloud runs only if actually executed. Behavioural answers can use real support incidents with sensitive details removed. Never invent production Azure experience.
