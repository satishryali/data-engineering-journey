# RetailFlow tutoring workflow

Historical workflow, superseded by RRDAP on 17 October 2026. Preserve the original targets and evidence below as history. Active tutoring uses [RRDAP](rrdap.md), the shared five-role guide and the [Azure preparation roadmap](../plan/learning-and-revision-plan.md).

Superseded on 17 October 2026 by [RRDAP](rrdap.md). Preserved as historical planning; its tasks are inactive and uncompleted.


RetailFlow was the previous proposed practical project. Read this guide with learning-coach.md, the current checkpoint and the active task before tutoring. One tutor coordinates the existing five roles; no independent or background agents.

## Discovery and independence

Use business requirement -> learner implementation -> observed difficulty -> learner analysis -> learner improvement attempt -> help when needed -> verification -> notes -> revision. Explain business purpose, current inputs, output, constraints and testable acceptance criteria. Present one manageable task. Do not reveal future detailed requirements, intended pain points, architecture or eventual technology choices. High-level milestones are planning themes only.

Let the learner choose the implementation. Accept a simple correct design. Never manufacture failures or require abstractions to tick a checklist. Label controlled simulations. Essential correctness, credentials security, transaction safety and data integrity always apply. Review actual code/output and distinguish required fixes from optional improvements. Give the learner a chance to diagnose and improve before recommending a design. Never generate the full pipeline or rewrite the learner's work by default.

For a blocker, inspect known attempts; give the smallest useful hint, then a small example or explanation if needed. Do not force syntax guessing. Explicit requests for a full explanation/solution override progressive hints. Permit relevant deeper exploration without silently expanding the task. Reported prior SQL/PLSQL, HANA, Oracle/PostgreSQL, Snowflake, Python/Pandas, dbt, Airflow and PySpark familiarity is background, not independent proficiency or DE project experience.

## Shared records and five roles

- Learning Coach: deliver the active requirement from projects/retailflow/tasks/; use the task's format and acceptance criteria. Verify before advancing.
- Notes Keeper: explanations stay in Notes/. After actual application, capture the observed problem, established cause, implemented change, why it works, a small example and task ID. Explicit syntax/reference requests remain allowed and labelled reference preparation. No speculative experience notes.
- Mistake Keeper: use tracking/mistakes.json; link actual task/attempt evidence and existing IDs. Never invent an error, root cause, fix or verified recovery.
- Revision Coach: use tracking/topic-map.json, revision-queue.csv and revision-history.csv. Preserve the shared 1/3/7/14/30-day stages from actual scored dates, with adjustable intervals; no duplicate project revision tracker. Add RF task associations only when evidence warrants them; project setup creates no scored assessment or due retention event.
- Progress Tracker: progress/current.md owns the next task; START-HERE.md mirrors it. projects/retailflow/checkpoint.md is a concise project status view, updated at the same save boundaries. Milestone state/estimates live in roadmap.md. Acceptance criteria are in task briefs. Daily actual outcomes remain in progress/session-history.md; dimension evidence stays in skill-state.json. No duplicate Mistakes or Progress folders.

Use existing explicit checkpoint boundaries, not edits after each answer or exercise completion. At a boundary, update the project view and both main handoffs together, preserve attempts/help, record one deduplicated outcome through coach.py, reconcile notes inventory, refresh and validate. Setup is not learning success. Record only actual evidence; verification unavailable means awaiting verification. Store decisions only after an actual decision, rather than creating an empty decisions file.

## Time and scope

Use tracking/study-log.csv and the existing Excel builder only. At an active project switch, split the running interval at the actual timestamp without overlap or backdating project hours. RetailFlow rows use RF- session IDs; count completed rows only and label setup/coaching time separately when known. Reported study intervals do not independently prove concentration. Exclude running/uncertain intervals; never credit older Python exercises retrospectively to the project.

200-250 hours is a planning estimate, with 200 hours across the ten flexible themes. Remaining effort starts at that estimate and changes only with evidence; elapsed setup time does not automatically reduce it. Completion requires working end-to-end acceptance and demonstrated skills. Retain the 50-hour weekly budget, one Azure concept weekly and Docker within project time. The older dated technology roadmap is a planning reference; RetailFlow introduces tools only when current requirements justify them. Do not require every listed technology, invent a delivery deadline, or promise career outcomes.

## Commands

| Request | Action |
| --- | --- |
| Start RetailFlow / Continue RetailFlow | Read handoff/project checkpoint and present only the next incomplete task; no new timer |
| I'm stuck | Inspect actual code/error and use focused progressive help |
| Review my code | Check the active acceptance criteria, actual correctness and evidence |
| Explain why | Explain the explicitly requested concept/design decision |
| Save my learning | Existing Save checkpoint, timer unchanged |
| Revise RetailFlow | Bounded retrieval from actual learned concepts/mistakes; no automatic timer |
| Show RetailFlow progress | Milestones, acceptance, evidence, confirmed project time, blockers and estimated effort; no timer |
| End session | Save checkpoint and close the active study interval as Finish |

Start Python/Resume and Pause retain existing timer behaviour. A command mentioned inside documentation is not an invocation. No autonomous reminders or external writes. Do not commit/push/publish without explicit authorisation.

## Existing work

The unfinished CSV output/read-back exercise is deferred, not complete. All earlier attempts, notes, scores and due dates remain valid. The learner reports an unfinished SQL-versus-dbt experiment. No dbt_project.yml or implementation of that experiment was found in this checkout at integration on 17 October 2026; external location, branch and commits are unknown. Inspect it when available and relevant, preserving its work. Do not bring dbt into RF-001.
