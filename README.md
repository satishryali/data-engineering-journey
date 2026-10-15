# data-engineering-journey

My practical data engineering learning journey: SQL, Python, PostgreSQL, dbt, Airflow, Docker, Snowflake, PySpark and Azure—with hands-on projects, exercises, revision tracking and tutor checkpoints.

This repository is the durable record of my tutoring, exercises, revision and project work. Chat history is useful context; this checkpoint and actual code are the source of truth.

## Start or resume here

1. Read AGENTS.md and progress/current.md.
2. Read plan/learning-and-revision-plan.md for the agreed schedule.
3. Inspect tracking/revision-queue.csv and the latest work before selecting a task.
4. After reviewed work, update progress/current.md, progress/session-history.md and the relevant trackers. Never mark a planned topic as completed.

Current assignment: tools/sql/exercises/001-join-preservation/README.md.

## Structure

- plan/: 16-week curriculum and weekly milestones.
- progress/: current checkpoint and concise session handoffs.
- tracking/: study intervals, revision queue and actual review history.
- tools/: notes and exercises organised by skill.
- projects/: integrated pipelines combining tools.
- reference/: supporting tutoring and time-accounting guidance.

Each tool has README.md and notes.md. Add exercise folders as lessons are actually assigned. Store explanations of the problem, attempted code, expected output, mistakes and a changed example. Integrated projects belong in projects/, with one main README and run instructions.

## Across computers

Repository: https://github.com/satishryali/data-engineering-journey

On another computer:

```bash
git clone https://github.com/satishryali/data-engineering-journey.git
cd data-engineering-journey
```

If already cloned, run `git pull --ff-only` before starting a session. After reviewed work, commit and push your checkpoint and exercises. Avoid editing the same trackers concurrently on two machines; resolve conflicts before continuing. Authenticate with your own GitHub account to access this private repository.

Git does not sync until you push and pull. Commit author configuration is separate from GitHub login. An AI can read the repository only if the current chat has access: open the checkout in Codex, use an authorised GitHub connection, or upload current files. Merely naming a repository does not grant access. A normal ChatGPT Project does not automatically execute this AGENTS.md or continually pull a repository; explicitly ask it to read the current files.

## New tutoring chat prompt

> Act as my data engineering tutor. Read README.md, AGENTS.md, progress/current.md, plan/learning-and-revision-plan.md and tracking/revision-queue.csv from this repository. State the current unfinished task, then continue with one small exercise. Let me attempt it before showing solutions. Update the checkpoint and trackers from actual results. If you cannot read these files, tell me rather than guessing my progress. Do not repeat the whole roadmap or restart the course.

## Time tracking

Follow reference/study-tracking.md. Start/pause/finish messages control recorded intervals. Git does not run a stopwatch, send notifications or update CSVs automatically. Existing Codex reminders remain tied to their original app/chat until separately recreated elsewhere. Current timer migration needs an actual stop time; do not count setup time as SQL practice.

## Status

Repository prepared on 15 October 2026 for the private GitHub repository above. No exercise has yet been completed independently. February 2027 readiness and 15 LPA are goals, not promised outcomes.
