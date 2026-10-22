# Engineering record templates

Copy only the relevant template when real work needs it. Replace placeholders from actual evidence; use unknown/pending rather than invented results. Keep solutions separate from an unanswered assignment. These templates add no tasks, assessments or completion claims.

## Engineering ticket

```markdown
# [Task ID] — [Title]
Status: proposed / in progress / awaiting verification / accepted
Dependencies: [accepted task IDs, or none]
## Business Situation
## Business Requirement
## Why It Matters
## Available Inputs
## Expected Output
## Acceptance Criteria
## Your Assignment
## Evidence and review
Attempt paths; actual checks/output; assistance; open gaps; acceptance date if verified.
```

## Design decision

```markdown
# [Decision ID] — [Decision]
Task/attempt: [references]
Date/status: [actual date; proposed/adopted/rejected/postponed]
Problem and constraints:
Alternatives considered by the learner:
Evidence and same-workload comparison:
Decision and reason:
Security/cost/operational effects:
Revisit condition:
```

## Test evidence

```markdown
# [Task ID] — test evidence
Implementation version and environment:
Synthetic input and expected result:
Command/query and actual output:
Acceptance criterion checked:
Changed-input, empty/error and rerun checks where relevant:
Result: passed / failed / not run
Help used and remaining uncertainty:
```

## Incident report

```markdown
# [Incident ID] — [Observed symptom]
Task/run/version; actual date:
Type: labelled simulation / development incident
Business impact and affected range:
Detection and redacted logs/metrics:
Observed timeline (unknown times remain unknown):
Immediate mitigation and verification:
Safe rerun/backfill range and duplicate checks:
Recovery status and remaining risks:
Linked RCA and test evidence:
```

## Root-cause analysis

```markdown
# [Incident ID] — root-cause analysis
Observed symptom and reproduction:
Hypotheses and checks:
Cause: verified / hypothesis, with supporting evidence
Contributing conditions:
Fix and actual validation:
Regression checks, monitoring and prevention:
Unresolved questions and owner/next task:
```

## Pull request review

```markdown
# [Task/PR ID] — review
Business behaviour and acceptance criteria:
Reviewed paths/version:
Correctness, integrity and failure visibility:
Tests actually run and results:
Rerun/recovery, security and cost where relevant:
Required changes versus optional improvements:
Assistance and learner explanation:
Decision: changes needed / awaiting evidence / accepted
```

## Deployment checklist

```markdown
# [Task/version] — deployment or local rehearsal
Environment and authorization scope:
Dependencies and configuration (no secrets):
Preflight tests and data backup/isolated restore evidence:
Planned bounded change and cost/stop conditions:
Rollback procedure and trigger:
Actual execution evidence, or not executed:
Post-change data validation and monitoring:
Cleanup and remaining resources:
Outcome and unresolved work:
```
