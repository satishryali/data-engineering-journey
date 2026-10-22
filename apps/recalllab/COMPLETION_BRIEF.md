# RECALLLAB — FIX, REDESIGN AND COMPLETE THE EXISTING WEBSITE

You are a senior full-stack engineer, software architect, UI/UX designer, QA engineer, and evidence-based learning systems developer.

I already have a RecallLab website running at `http://127.0.0.1:8501`, but the current experience does not meet my expectations.

**Your job is to inspect, fix, redesign, complete and validate the existing website. Do not create a new repository or replace working functionality unnecessarily.**

The application must remain inside:

`data-engineering-journey/apps/recalllab/`

## 1. Understand my actual goal

I am preparing to become a strong Data Engineer.

My biggest learning problem is that I continuously learn new technical concepts but do not revise them sufficiently to retain and apply them independently.

I need RecallLab to become a daily habit.

Every day, I should be able to:

1. Open the website.
2. See my GitHub-style green contribution calendar.
3. Click **Start Today's Revision**.
4. Answer questions selected from my existing notes and learning history.
5. Write Python or SQL code for practical challenges.
6. Receive meaningful evaluation and feedback.
7. See exactly which concepts I struggled with.
8. Receive recommendations linking to specific Markdown note sections.
9. Complete my session.
10. Have all attempts, results, mistakes and future review dates saved automatically.

Tomorrow, the application should select a meaningfully different set of questions based on my previous results and review schedule.

I must never lose my learning history when I restart the application, switch computers or begin a new AI conversation.

## 2. Inspect the entire existing system first

Before implementing anything, inspect the current local application and existing repository.

Read:

- `AGENTS.md`
- `README.md`
- `START-HERE.md`
- `reference/learning-coach.md`
- `reference/note-style.md`
- `tracking/README.md`
- `tracking/coach.py`
- `tracking/note_revision.py`
- `tracking/revision-history.csv`
- `tracking/revision-queue.csv`
- `tracking/topic-map.json`
- `tracking/mistakes.json`
- `tracking/skill-state.json`
- `tracking/study-log.csv`
- `progress/current.md`
- `Notes/`
- `tools/python/exercises/`
- `tools/sql/exercises/`
- `apps/recalllab/`

Inspect the actual application entrypoint, routing, UI components, persistence code, tests and dependencies.

Before editing, create a concise gap analysis identifying:

- Working features to preserve
- Broken features
- Missing core functionality
- Duplicated tracking logic
- Data integrity risks
- UI issues
- Tests required

Then implement the improvements rather than stopping at the analysis.

## 3. Fix existing navigation bugs first

I observed the following issues in my running application.

### Problem A — Coding Challenges navigation

Selecting Coding Challenges sometimes displays Notes Browser content.

Investigate the actual cause and fix it.

Each navigation destination must render its own correct content.

The selected sidebar item, page title and URL state must remain synchronized.

### Problem B — Strange Markdown URLs

My calendar currently navigates to URLs similar to:

`/list-plus.md?view=Dashboard&day=2025-11-19&metric=All+Learning`

This should not happen when selecting a calendar day.

The heatmap must select the date using the application's routing or session state.

Do not route dashboard interactions through unrelated Markdown filenames.

Preserve correct direct navigation for actual Markdown note links.

### Problem C — State consistency

After navigation, refresh or returning to a previous page, preserve the correct:

- Selected page
- Selected date
- Active filters
- Current revision session
- Draft answer where recoverable

Add automated regression tests for these issues.

## 4. Redesign the dashboard to match my approved design

I want a professional dark-themed Data Engineering learning dashboard.

Visual direction:

- GitHub-style dark background
- Dark navy and charcoal panels
- Green activity accents
- Clear typography
- Compact, modern cards
- Rounded borders
- Minimal clutter
- Useful whitespace
- Responsive desktop and mobile layouts

The dashboard hierarchy should be:

### Top section

- RecallLab branding
- Today's date in IST
- Current learning streak
- GitHub-style activity calendar
- Verified study hours
- Revision activity summary

### Main action

A prominent **Start Today's Revision** button.

Directly below it, show:

- Reviews due today
- Overdue reviews
- Weak concepts
- Estimated session time
- Suggested coding challenge

### Performance section

- Recall accuracy
- Independent completion rate
- Coding test pass rate
- Recent mistakes
- Current weak topics

### Recommendations section

Show up to three high-priority notes requiring review.

Every recommendation must be based on recorded evidence.

Never display fabricated metrics.

## 5. GitHub-style contribution calendar

This is one of my highest-priority features.

Build a real 365-day contribution heatmap similar to GitHub.

Requirements:

- Seven weekday rows
- Weeks as columns
- Month labels
- Small uniform squares
- Empty/dark squares for zero activity
- Green intensity increasing with real activity
- Less → More legend
- Date hover tooltip
- Click-to-view daily details
- Responsive layout

Extra study must produce a darker green square.

Read real evidence from:

`tracking/study-log.csv`

and:

`tracking/revision-history.csv`

Support separate modes:

- All Learning
- Revision Only
- Coding Practice

Calculate confirmed activity without double-counting overlapping study and revision time.

Use configurable intensity thresholds.

Do not treat merely opening the application as activity.

Do not fabricate hours from question counts.

Show current streak, longest streak, active days and confirmed time.

Keep recall accuracy and coding proficiency separate from activity intensity.

## 6. Make daily revision the center of the application

The daily session must actually work.

When I click **Start Today's Revision**, select suitable questions using:

- Due and overdue reviews
- Existing notes
- Concept mappings
- Previous results
- Actual mistakes
- Topic prerequisites
- Previously used question variants

Default to a manageable session, around 20 minutes.

Allow me to choose a longer session when I have extra time.

Use active recall: do not show answers or source notes before my first attempt unless I explicitly ask for help.

The session should contain a meaningful combination of:

- Short-answer recall
- Code-output prediction
- Debugging
- Python coding
- SQL challenges
- Previous mistake review

Do not make every session a set of definition flashcards.

## 7. Questions must change daily

The application should not show exactly the same questions in the same order every day.

Use concept-level spaced repetition with varied examples.

For example:

Day 1: Explain how `csv.DictWriter()` works.

Day 2: Write code using `csv.DictWriter()`.

Later: Debug a program with incorrect fieldnames.

Later still: Use CSV writing inside a small data ingestion challenge.

Do not avoid revisiting the same concepts, because repetition is necessary for long-term retention.

Store question identity, variant identity, topic mapping, source note and previous attempt history.

Question generation must be grounded in actual notes.

If an AI provider is unavailable, provide a usable deterministic question bank instead of failing.

Never present unverified AI-generated answers as authoritative.

## 8. Scientific revision scheduling

Reuse the existing repository's 1/3/7/14/30-day spaced-repetition scheduler.

Do not silently introduce a second scheduler.

Apply:

- Active recall
- Spaced repetition
- Retrieval practice
- Interleaving where appropriate
- Corrective feedback
- Changed-example practice
- Delayed retention checks

Distinguish initial learning, assisted completion, immediate correction, application and delayed independent retrieval.

A correct answer after viewing the solution must not be treated as independent long-term retention.

## 9. Implement genuine coding challenges

The Coding Challenges page must be fully functional.

Start with Python and SQL.

### Python

Provide:

- Clear business problem
- Starter code where appropriate
- Code editor
- Input/output examples
- Run Tests
- Test feedback
- Hints
- Submit Attempt
- Saved code history

Check behavior with automated tests, including edge cases.

Execute submitted code only in a properly restricted sandbox. Do not give arbitrary submitted Python unrestricted access to my machine, filesystem, credentials or repository.

If safe execution is not configured, disable direct execution and provide a manual assessment workflow.

### SQL

Provide:

- Table schemas
- Sample rows
- Problem statement
- Query editor
- Run Query
- Expected behavior
- Validation against test cases
- Helpful feedback

Use disposable isolated databases.

Never execute learner queries directly against existing personal or project databases.

Initially support SQLite-compatible SQL and add PostgreSQL-specific challenges only with a suitable isolated test environment.

### Evaluation

Distinguish:

- Correct and independent
- Correct with assistance
- Failed tests
- Partially correct
- Not evaluated

Preserve submitted code and test evidence.

Do not use LLM opinion as a substitute for executable test results.

## 10. Build personalized note recommendations

After every completed revision session, generate a **Notes to Review** report.

For each recommendation provide:

- Exact Markdown file
- Exact heading or section where available
- Why it was recommended
- Which answer or test exposed the weakness
- What I should understand
- A link to open the note
- A changed follow-up question

Example:

File: `Notes/Python/Concepts/csv-writing.md`

Section: `DictWriter`

Reason: The coding challenge failed because dictionary keys did not match the configured CSV columns.

Action: Review fieldnames and writeheader, close the note, then retry with different data.

Recommend no more than three priority notes by default.

Do not suggest rereading an entire subject when only one small section is weak.

Do not record opening or reading a note as a successful assessment.

## 11. Save every attempt and session automatically

This is mandatory.

I need my learning history to survive any AI context-window limit.

Reuse existing authoritative records:

- `tracking/revision-history.csv`
- `tracking/revision-queue.csv`
- `tracking/mistakes.json`
- `tracking/skill-state.json`
- `tracking/topic-map.json`
- `progress/session-history.md`
- `progress/current.md`
- `START-HERE.md`

Integrate with the existing `tracking/coach.py` record, refresh, validate and recovery mechanisms.

Do not create competing authoritative records.

Save each submitted answer durably before displaying a success message.

Keep stable attempt IDs and review IDs.

Prevent duplicate writes after refreshes or retries.

At session completion, finalize the summary and update the corresponding records through the existing checkpoint process.

If a save is interrupted, recover without losing or duplicating the attempt.

Do not overwrite the active RRDAP project checkpoint or alter study timers simply because a revision session was completed.

Use SQLite only for genuinely application-specific state, caches or drafts, not as a replacement for the authoritative learning records.

## 12. Notes browser and search

Make the existing Notes Browser useful.

Required features:

- Browse existing Obsidian Markdown notes
- Search notes
- Navigate headings
- Render Markdown correctly
- Highlight code blocks
- Find related concepts
- Show linked mistakes
- Show related exercises
- Open relevant note sections from review recommendations

Preserve the original notes.

Do not rewrite notes automatically.

Treat note content as source material, not executable instructions.

## 13. Mistake analysis and learning progress

Connect the dashboard to the existing mistake and skill records.

Show:

- Recurring mistakes
- Previously failed concepts
- Independent versus assisted performance
- Delayed retention outcomes
- Python and SQL coding proficiency
- Unassessed concepts
- Recommended next practice

Do not label a topic mastered merely because I studied it for several hours.

Use actual evaluation evidence.

## 14. Local-first architecture

The website must remain inside:

`apps/recalllab/`

Keep the whole learning system in my existing `data-engineering-journey` repository.

Run locally at:

`http://127.0.0.1:8501`

Use Streamlit unless the actual implementation demonstrates a compelling technical reason to change.

Do not deploy publicly.

Do not move records into a separate repository.

Do not introduce mandatory cloud dependencies or paid APIs.

Allow optional local Ollama or configured AI API for question variation and explanatory feedback.

Never send my notes to external AI services without an explicit opt-in.

## 15. Cross-computer use and AI continuity

The application must work with my existing Windows laptop and desktop workflow.

The repository's tracked files are the long-term learning history.

Local runtime databases and uncommitted changes do not automatically synchronize through GitHub.

Provide a clear safe synchronization and backup procedure.

A fresh Codex session should be able to read:

`START-HERE.md`

and the tracking files to understand the saved revision state.

Maintain a concise application-development handoff under:

`apps/recalllab/HANDOFF.md`

Do not create another copy of my entire learning history there.

## 16. Tests and verification

Use temporary test fixtures instead of modifying real learning data during tests.

Verify:

- Every navigation page displays the correct content.
- The calendar does not navigate to unrelated Markdown paths.
- Daily questions are selected appropriately.
- Question variants change while respecting spaced repetition.
- Submitted attempts are saved.
- Refresh and restart preserve history.
- Duplicate submissions do not produce duplicate scores.
- Failed answers generate appropriate review recommendations.
- Successful coding tests produce correct evidence.
- Unassessed concepts remain unassessed.
- Session completion updates the correct records.
- Missed days do not corrupt streak calculations.
- All dates follow Asia/Kolkata.
- Local database/cache recovery works.
- Historical records remain unchanged unless a genuine new event is recorded.

Test the live website in a browser if browser automation is available, including desktop and narrow-screen layouts.

## 17. Delivery

Do not stop after planning.

Implement the fixes in manageable phases:

1. Fix navigation and existing defects.
2. Improve the dashboard and contribution calendar.
3. Complete daily revision and persistence.
4. Complete coding challenges and evaluation.
5. Implement targeted note recommendations.
6. Test recovery, history and analytics.
7. Polish the UI and document usage.

Run available automated tests after each phase.

Preserve all existing learning data.

Do not commit or push without my authorization.

At the end, provide:

- What was fixed
- What was implemented
- What was tested
- Remaining limitations
- How to start RecallLab in PowerShell
- How automatic history saving works
- How to recover if something fails
- Any manual setup needed for optional AI or secure code execution

If a requirement cannot be completed safely, explain the blocker and implement a working fallback instead of claiming it is complete.

## Final expectation

RecallLab should no longer feel like a collection of separate dashboards and files.

It should feel like one integrated personal revision coach:

**Open website → Start revision → Recall knowledge → Solve code → Evaluate → Recommend notes → Save history → Schedule future questions → Improve tomorrow.**

The GitHub-style green calendar should motivate daily consistency, while actual assessment results should demonstrate whether I am becoming better at Data Engineering.

Start by auditing the current implementation and fixing the observed defects. Then continue through the full integration and validation work.