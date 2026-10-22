# Completion audit

## Preserve

The current local app has ten pages, a real fixed-square annual heatmap, correct revision-versus-learning classification, read-only record readers, offline questions, stable submitted IDs, durable SQLite transactions, immutable evidence, checkpoint freeze/replay through coach.record/recover/refresh/validate, controlled SQLite fixtures, and safety-disabled Python execution. Existing canonical learning records and active RRDAP/timer state must remain untouched by engineering tests.

## Defects and gaps

- Sidebar routing mutates session state without synchronizing the URL. Old note/view parameters can reappear on refresh or another URL update. Query handling, next_route, and widget navigation are separate paths. Centralize them.
- App links use `?view=...`, inheriting the current pathname. Ordinary Markdown links are rendered unmodified, allowing a `.md` pathname to become the base for calendar links. Use root-absolute application links and rewrite internal Markdown/wiki note links safely.
- Date/filter widgets do not persist their own values to the URL or durable local page preferences.
- Daily revision is a single concept picker, not a frozen, varied, bounded session with progress/next-task/completion. Daily examples vary input but not sufficiently the task format. Store the actual question plan and selected task; use past variants and keep the existing scheduler as sole date authority.
- Manual Python/text submissions remain permanently pending without an in-app manual assessment workflow. Add explicit human review with observed verification evidence; retain original submissions and unknown help. Never enable unrestricted code execution.
- SQL is all-or-nothing in the UI and code history is hidden under Settings. Show fixture-level and partial outcomes and history in Coding Challenges.
- Note recommendations select first mapped sections and do not preserve a completed-session report. Rank actual failures, choose source-specific sections, and show the attempt and a changed follow-up. Notes browser lacks heading navigation and concept/mistake/exercise relationships.
- Local backups exist but JSON export cannot be imported. Add validated, idempotent, conflict-preserving import and recreate immutable evidence on frozen-batch replay. Imported data remains pending until explicit checkpoint completion.
- Completed study intervals are summed independently; overlapping intervals could inflate totals. Merge overlapping closed intervals before reporting time. Never infer revision duration from study time/counts.
- Dashboard's primary action must say Start Today's Revision and expose real due/overdue/weak counts and a suitable coding link. Keep accuracy, help and activity separate.

## Integrity constraints

No second scheduler, no direct UI CSV/JSON mutations, no automatic Git writes, no fake test assessments in live data, no project/timer edits. Human evaluation is labelled manual evidence; AI can offer explanations only, never a correctness score. SQLite holds operational plans/drafts/journals/assessment annotations; canonical assessed events remain in repository trackers at an explicit session-completion checkpoint.

## Verification plan

Test all routes, stale-note-to-coding transitions, root URLs from arbitrary Markdown paths, refresh/date/filter/draft restoration, deterministic format variation, plan replay and history avoidance, honest manual/unknown-help/partial evaluation, note-heading extraction and safe links, submission/annotation immutability, backup/import conflicts, interrupted writes, overlapping time, correct calendar categories, and canonical checkpoint preservation. Use disposable checkout copies. Browser-check desktop/narrow layouts and real navigation without submitting fake learner evidence.
