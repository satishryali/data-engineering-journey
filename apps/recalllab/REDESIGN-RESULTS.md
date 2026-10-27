# Recall Lab redesign results

Implemented in the existing Streamlit app, 26 October 2026. No framework migration,
production dependency additions, deployment, commit or push. Existing uncommitted
code-history/journal/roadmap fixes were retained. Learning records were not edited.

## Changed pages

| Page | Result |
| --- | --- |
| Dashboard | Revision hero and primary action first; manageable queue, actual outcome metrics, recommended notes, weak areas, secondary annual activity and collapsed learning plan |
| Today's Session | Persistent pause/resume, submitted-attempt/attestation gate for reveal, separate difficulty self-report, native shortcuts, calm completion, bounded new plans |
| Question Bank | Consistent searchable question cards and explicit no-match state; original practice routes preserved |
| Coding Challenges | Problem/editor split, adjustable pane proportions, mobile stacking, monospace editor; real SQLite feedback, disabled Python execution, human assessment and merged code history retained |
| Notes Browser | Shared readable typography, code/table treatment, section navigation, guarded links and original source content retained |
| Mistakes & Weak Topics | Search, actual corrections/assistance, observed recurrence, actual next dates and direct practice links |
| Progress & Analytics | Restrained metric cards, readable concept coverage instead of raw JSON, useful evidence table, original outcomes/charts retained |
| Revision Calendar | Shared shell, responsive scrolling calendar, actual dates, metric filters and recorded-day evidence retained |
| Search Notes | Consistent input/results, useful starting/no-match state and guarded source links |
| Settings | Daily task limit with persistence, shared form styling, existing recovery/backup/import and optional-local-AI controls retained |
| Learning Roadmap | Shared shell, typography, table and source detail styling; planned status preserved |
| Project | Shared reading layout and original RRDAP checkpoint/acceptance criteria preserved |
| Interview Practice | Shared focused prompt styling, original selector and evidence boundaries preserved |

Shared design: charcoal surfaces, mint action accent, SVG icons, 40px minimum native
buttons, visible focus, reduced-motion rules, responsive mobile navigation and tables.
The app uses existing native Streamlit controls. Coding pane proportions use a width
slider; the editor is a styled native textarea rather than a new IDE dependency.

## Verification

| Executed check | Result |
| --- | --- |
| `python -m unittest discover -s apps/recalllab/tests -v` | 54 tests passed |
| `python -m unittest discover -s tracking/tests -v` | 27 tests passed |
| Real Chromium, all 13 routes at 1440×1000 and 390×844 | 26 checks passed, no page exceptions or viewport horizontal overflow |
| Revision CTA visible above the fold at both widths | Passed |
| Annual calendar preserves 365 cells | Passed |
| Browser interaction scenarios on a disposable checkout | 18 checks passed |
| Pre-migration backup restores original rows/schema; future schema refused unchanged | 2 focused tests passed, included in 54 |
| Protected canonical CSV/JSON and main checkpoint/handoff SHA-256 comparison | Unchanged |
| `git diff --check` | Passed |

Browser interaction checks covered starting from the home CTA, disabled blank
submission, draft/reload recovery, pause/reload/resume, submit, attestation-gated
reveal, difficulty/reload persistence, next task, complete local plan, real passing
SQL fixtures, empty/populated search, note code rendering, preferences/reload and
keyboard focus. Checkbox interaction was also exercised using keyboard Space.
Canonical checkpoint completion/recovery, manual assessment, safe SQL rejection,
same-day versus delayed scheduling and journal import conflicts are covered by the
automated app tests; synthetic browser attempts were never submitted to live records.

Screenshots were captured from the actual running app and visually inspected.
Visual inspection found and corrected a heading span selector, low-size dashboard
labels and deferred-widget capture timing. Desktop and phone screenshots for every
page are in [screenshots](screenshots/); [browser-results.json](screenshots/browser-results.json)
records each viewport check. Additional session pause/feedback/completion and passing
SQL screenshots use clearly synthetic QA answers in a disposable checkout.

Representative views:

- [Dashboard desktop](screenshots/dashboard-desktop.png)
- [Dashboard mobile](screenshots/dashboard-mobile.png)
- [Focused session](screenshots/today-s-session-desktop.png)
- [Coding workspace](screenshots/coding-challenges-desktop.png)
- [SQL fixtures passed](screenshots/coding-sql-passed-desktop.png)
- [Notes](screenshots/notes-browser-desktop.png)
- [Mistakes](screenshots/mistakes-weak-topics-desktop.png)
- [Analytics](screenshots/progress-analytics-desktop.png)

## Start locally

From the repository root, with the existing installed Python/Streamlit:

```powershell
Set-Location apps/recalllab
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
```

Open **http://127.0.0.1:8501**. Launching from the app directory loads its updated
native theme config. The existing live server on 8501 was also checked after the
redesign and renders the new dashboard. If restarting, stop the existing server
first so the port is available. Installation steps remain in [README](README.md).

Optional repeat browser smoke check against an explicitly disposable instance:

```powershell
python apps/recalllab/tests/browser_redesign.py --url http://127.0.0.1:8502
```

Playwright/Chromium are development-only prerequisites for this optional command.
Set the test server's RECALLLAB_ROOT and RECALLLAB_DATA to scratch copies before
running it. The app/coach suites create their own disposable fixtures.

## Limits and deliberate boundaries

- Python execution remains disabled until a verified contained runner exists.
  Saved source/human review and contained SQLite SELECT challenges work.
- The authoritative 1/3/7/14/30-day scheduler remains in place. This is not FSRS.
  Self-rated difficulty does not mutate scores or due dates. See the documented
  [research and future migration requirements](REDESIGN-QA.md).
- Existing source-note inventory changes still need tutor inspection/mapping.
  The sidebar keeps that notice visible in a details panel; the redesign does not
  rewrite notes, reset review dates or invent evidence to clear it.
- The optional Ollama service was not contacted. No Python runner, external model,
  cloud deployment, PostgreSQL/PySpark execution or automatic interview grader added.
- Browser QA used Chromium at the stated widths. Keyboard and reduced-motion checks
  are not a complete screen-reader or cross-browser accessibility certification.
- Streamlit AppTest bare-mode warnings and existing dependency deprecation warnings
  do not fail checks. Research fetch limitations are recorded in the audit.
