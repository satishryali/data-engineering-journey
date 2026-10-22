# RRDAP engineering simulation

This is educational project practice, not employment or a production Azure claim. Use [RRDAP's workflow](rrdap.md), [current task](../projects/rrdap/tasks/RDS-001.md) and [phase roadmap](../projects/rrdap/roadmap.md). One tutor coordinates the five roles. Start with a business requirement and independent learner implementation; introduce a new operational problem only when relevant. Do not reveal future intended failures or prescribe architecture during an active task.

Use small consistent fictional retail inputs. No million-row generation, resource installation or cloud spending is required by this framework. Set a bounded workload/cost limit before an authorized experiment. Keep secrets outside Git. Cloud deployment needs explicit authorization; local rehearsal is labelled as such.

## Development loop

1. Issue a bounded business ticket with acceptance criteria and dependencies on accepted tasks.
2. Learner chooses design and implementation; preserve actual attempts.
3. Review actual diff, output, data-quality checks and help used. Separate essential fixes from optional improvements.
4. Verify acceptance and a changed-input case. Add reruns/backfills, performance, incident investigation and monitoring progressively when the current requirement warrants them.
5. Record a decision only when a decision was actually made; incident reports only for an actual or explicitly labelled simulated incident.
6. Rehearse CI/test/deployment/rollback within authorized scope. Never mark a deployment or recovery verified without evidence.
7. Save evidence through existing checkpoint boundaries. Keep task completion in project evidence and dimension-specific learning in canonical trackers.

Task briefs under `projects/rrdap/tasks/` own requirements and dependency IDs. The project roadmap owns phase state; current.md owns the next task. Tests/decisions/incidents are evidence, not another proficiency or time ledger. Create records only when used, from [templates](../projects/rrdap/templates/engineering-records.md); link ticket/attempt/commit/run IDs. No new RDS ticket is assigned by adding these templates.

For measured performance compare the same workload and correctness before/after; include runtime, resource use and limitations. For failures keep redacted logs, impact, detection, verified cause or hypothesis, mitigation, regression checks, safe rerun/backfill scope and monitoring evidence. Security and cost decisions include identity/scope, data sensitivity, bounded resource use and cleanup. Preserve working data and restore backups in isolation.
