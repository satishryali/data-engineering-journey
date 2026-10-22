# RecallLab record authority

RecallLab is a local browser interface in this checkout. It is not a second tutor or scheduler.

| State | Authority | App use |
| --- | --- | --- |
| Due dates and stages | tracking/revision-queue.csv | Read; change only through coach.record |
| Answered assessments | tracking/revision-history.csv | Read; end-session checkpoint through coach.record |
| Concept identity, prerequisites, note sections | tracking/topic-map.json | Read and check live inventory; preserve mappings |
| Observed mistakes | tracking/mistakes.json | Read; append only explicitly observed gaps through coach.record |
| Skill dimensions | tracking/skill-state.json | Read; append only assessed dimensions through coach.record |
| Confirmed time | tracking/study-log.csv | Read only, split closed intervals at IST midnight; never start timers |
| Target policy and curriculum | tracking/study-targets.json; plan/learning-and-revision-plan.md | Shared study_plan helper; CSV is generated, no completion inferred |
| Interview prompts and outcomes | tracking/interview/questions.json; canonical review event_json | Read-only prompt view; tutor records actual rubric/evidence through existing checkpoint API |
| Active project/task | progress/current.md, START-HERE.md, projects/rrdap | Read only; revision does not replace RDS-001 |
| Notes | Notes/ | Render original Markdown read only; no copied vault |
| Checkpoint identity/recovery | tracking/checkpoint-index.json, coach transaction | Reuse record/recover/refresh/validate |
| Drafts, pending submissions, preferences | ignored data/recalllab.sqlite3 | SQLite transactions, explicit checkpoint bridge, export/backup |
| Submitted evidence | apps/recalllab/evidence/*.json | Immutable, tracked on an intentional Git save; never execute |

The bridge freezes one batch before canonical writes. It locks the local writer, recovers the coach transaction, writes immutable evidence, calls record, refreshes and validates, then marks the local session recorded. Retrying after a crash reuses the exact batch and IDs. No UI callback edits CSV/JSON authorities directly. Opening pages and generating questions have no learning side effects.

Risks: older tests copied changing live history and assumed zero events (six baseline failures); fixtures must explicitly clear history in their temporary copy. The stale notes inventory was resolved on 18 October using the existing notes-sync helper: the only new path was excluded Obsidian graph.json configuration, with no changed learning sections. Validation passes and protected learning records stayed unchanged. The app still reports future coverage warnings; checkpoint writes synchronize via the existing helper without inventing mappings or resetting reviews. Single-computer/writer operation is required by the coach. Git synchronization remains intentional. SQLite drafts do not travel through Git.

Python execution is disabled: no verified containment component is installed. Python source is journaled and remains unscored until an explicit human review with verification evidence. Manual annotations retain original source/help, are immutable once saved and enter canonical history at session completion. They never become executable test evidence or delayed retrieval. SQL uses a disposable in-memory SQLite database, SELECT-only authorizer, bounded instructions/input/results, no extensions or external databases. It tests SQLite-compatible SQL fixtures, not PostgreSQL-specific semantics.

Optional loopback-only Ollama explanations are disabled by default and require explicit local-note-sharing opt-in plus a post-submission request. External endpoints/redirects are denied. Model responses are unverified operational cache entries and never scores. Offline questions and evaluation always work. The later learner-provided screenshot defines the compact dashboard styling.

Routing has one allowlisted root URL format. Sidebar changes synchronize URL/state; source Markdown/wiki links become guarded Notes Browser links rather than new Markdown pathnames. SQLite stores frozen question plans, cursor and page preferences. A completed report can be reconstructed from the canonical review payloads and session-history block; its local presentation cache is not a second schedule. The bridge makes a consistent frozen-batch backup and can reconstitute missing attempt evidence after a validated pending-journal import. Conflicts are refused without replacing local data. Closed study intervals are unioned before IST-day splitting; revision events never add overlapping or invented minutes.
