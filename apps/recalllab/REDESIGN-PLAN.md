# Recall Lab redesign

## Evidence and scope

The existing Streamlit 1.66 app has 13 routes: Dashboard, Today's Session,
Question Bank, Coding Challenges, Notes Browser, Mistakes & Weak Topics,
Progress & Analytics, Revision Calendar, Search Notes, Settings, Learning
Roadmap, Project and Interview Practice. SQLite owns local drafts and plans;
the coach owns canonical assessment and scheduling. Preserve both contracts.
Existing uncommitted fixes cover code history, journal recovery, roadmap reading
and tests; retain them. Do not modify learner attempts or learning records.

Current design puts the calendar and four colorful summary cards above revision.
Typography reaches 9–12px, uses numerous competing accents, and compresses
navigation. Coding is a vertical form. Secondary pages use inconsistent default
widget styling. The app already provides guarded note rendering, SQL fixtures,
human assessment, transactional submission and recoverable checkpointing.

## Design and implementation

- Charcoal surfaces, warm white text, one mint accent, restrained semantic colors.
- Clear workspace shell, readable navigation and responsive page introductions.
- Revision hero first, bounded queue next; activity and evidence below.
- Focused recall with attempt-gated reference, durable pause/resume and honest
  self-ratings separate from assessed scores. Limit new daily work without
  truncating saved plans or moving canonical due dates.
- Coding problem/editor columns; retain real SQLite tests and disabled Python
  execution. Preserve code history and human review.
- Consistent notes, mistakes, tables, settings, empty states, keyboard focus and
  reduced-motion support across all routes.
- Keep the shared 1/3/7/14/30-day rule. No FSRS migration: scheduling authority
  and sparse scored history do not justify changing the model in a visual upgrade.

## Acceptance checklist

- [x] All 13 routes render and preserve existing controls and working links.
- [x] First screen prominently offers Start Today's Revision.
- [x] Stored evidence drives counts; unknown outcomes remain unassessed.
- [x] Attempt, reveal, submit, next, pause/resume and restart work.
- [x] Notes/search/filter, mistakes, code history and settings remain usable.
- [x] SQL tests remain contained; Python execution stays honestly disabled.
- [x] Desktop/mobile screenshots inspected for clipping and overflow.
- [x] Focus indicators, keyboard navigation and reduced motion supported.
- [x] Scheduling/persistence/UI regression suites pass using disposable records.
- [x] Learning records and existing local database remain intact.
- [x] Startup commands, source research and limitations documented.

Parallel ownership: dashboard agent owns dashboard.py/dashboard.css; recall agent
owns session_ui.py/sessions.py and focused tests; QA owns its report/tests. Main
agent owns shared theme/foundation.css, app.py, integration, browser QA and documentation. No shared
file is edited by two agents.
