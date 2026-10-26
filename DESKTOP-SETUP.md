# Desktop setup guide

Use this guide to set up the learning coach on another Windows computer.
Run the commands below in **PowerShell**.

## 1. Install the required software

- Install Git.
- Install Python 3.11 or newer. Enable the option to add Python to PATH.
- Install Codex and sign in with your account.
- Sign in to GitHub with the account that can access this repository.

Open a new PowerShell window and check:

```powershell
git --version
python --version
```

Both commands should show a version. If `python` is unavailable, try `py --version`.
If that works, use `py` instead of `python` in the commands below.

## 2. Download the repository

Open PowerShell in the folder where you want to keep your learning repository.
You do not need the same folder path as the other computer.

```powershell
git clone https://github.com/satishryali/data-engineering-journey.git
cd data-engineering-journey
```

If the repository already exists on this computer, open its folder instead. Run:

```powershell
git status
git branch --show-current
```

Check that the working tree is clean and the branch is `main`. Then update it:

```powershell
git pull --ff-only
```

If Git reports local edits, conflicts or a different branch, preserve the files and
ask Codex to help reconcile them before continuing. Do not clone inside an existing checkout.

## 3. Install the learning skills

### First create Python on this computer

Virtual environments contain paths to a local Python installation. Do not copy
`.venv` between computers or put it in Git/Google Drive. Git transfers the setup
script and package list; each computer creates its own environment.

From the repository root, run:

```powershell
& ./codex/setup-python.ps1
```

This finds a local Python 3.11+ installation, creates `.venv`, installs
`requirements-study.txt`, checks dependencies and verifies the notebook kernel and
Faker imports. Existing working environments are reused. It does not run notebook
cells, change learner code, register a system kernel or start a timer. Optional
RecallLab packages can be installed with `-IncludeRecallLab`.

If an old/copied environment cannot run, close its notebook kernels and terminals,
then run:

```powershell
& ./codex/setup-python.ps1 -Recreate
```

The old directory is moved to an ignored `.venv.backup-...` directory, never deleted.
If Python is not found, install Python first or supply its actual path:

```powershell
& ./codex/setup-python.ps1 -PythonExecutable 'C:/your/local/Python/python.exe' -Recreate
```

Replace that example with the installed Python path on the laptop, not a path from
the desktop. A missing Python installation must be installed on each computer.

Open [data-engineering.code-workspace](data-engineering.code-workspace) in VS Code.
It recommends Python/Jupyter extensions and points to this checkout's `.venv`
without a desktop-specific path. If VS Code remembers an older interpreter, run
**Python: Select Interpreter**, choose **Enter interpreter path**, then select
`.venv/Scripts/python.exe` inside this checkout.

For notebooks, also choose **Select Kernel > Select Another Kernel > Python
Environments > .venv**. Notebook kernels have their own selection. Do not select
the unavailable desktop kernel saved in old notebook metadata. Verify without
running an exercise:

```powershell
& ./.venv/Scripts/python.exe ./codex/verify-python-env.py
```

Activation is optional. Direct interpreter commands work even if PowerShell blocks
`Activate.ps1`; do not change the system execution policy just to activate a venv.
If setup itself is blocked, use a process-only invocation:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./codex/setup-python.ps1
```

[Python's environment guide](https://docs.python.org/3/library/venv.html) explains
why environments are recreated; [VS Code's kernel guide](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management)
shows the separate notebook selection.

### Then install the learning skills

From the repository folder, run:

```powershell
& ./.venv/Scripts/python.exe codex/install_commands.py --keep-other-skills
```

- This installs 15 skills, including the five learning roles and GitHub utility.
- It records this computer's repository path in the installed skills.
- `--keep-other-skills` avoids adding disable rules for your other skills. Existing
  overrides outside the installer's managed section are preserved.
- The installer reports its backup location and any changes it makes.
- It does not start a timer, create learning results, commit or push.

The five learning roles are responsibilities of one tutor. They are not separate
background agents, and no additional agent service is needed.

## 4. Open Codex and check the skills

Fully close and reopen Codex. Open the downloaded `data-engineering-journey` folder.
Type `/` in the chat and search for these entries:

| Skill | What it does |
| --- | --- |
| Learning Coach | Continues the saved learning task |
| Notes Keeper | Maintains simple notes from actual learning |
| Mistake Keeper | Tracks observed mistakes and follow-up practice |
| Revision Coach | Chooses manageable revision from your notes |
| Progress Tracker | Reports actual learning and study progress |
| GitHub Agent | Reviews, commits and pushes when you ask |

The other nine skills cover timers, status, schedules, checkpoints and finishing study.

## 5. Verify the saved learning records

In PowerShell, from the repository folder, run:

```powershell
python tracking/coach.py validate
git log -1 --oneline
```

Validation should succeed. The latest commit should match the one pushed from the
other computer. Counts can change as new notes and actual review attempts are saved.

Then send this message in Codex:

```text
Read START-HERE.md and continue from the checkpoint.
```

The tutor should read your saved records and identify the pending task. This does
not start a study timer. Send `Start Python`, `Start SQL` or another explicit topic
command when ready to track study time.

## 6. Find your notes and revision plan

- [Current handoff](START-HERE.md)
- [Current learning checkpoint](progress/current.md)
- [Revision plan and dates](Notes/revision/plan.md)
- [What the agent does](agenet-action.md)
- [Detailed skill setup](codex/README.md)

If you use Obsidian, open this repository's `Notes` folder as the vault.
The revision plan shows the date when it was last generated. Ask for `Today's schedule`
or `Start revision` to have the tutor refresh planning using the actual IST date.

## 7. Switch between computers

For the timer, install the repository's [Pomodoro setup](codex/pomodoro/README.md#continue-on-a-laptop-during-power-cuts)
once on the laptop:

```powershell
& ./codex/pomodoro/Setup-Laptop.ps1
```

Reload VS Code, run **Pomodoro: Configure Sync Folder**, select the existing
`Pomodoro-Sync` folder in My Drive and choose **Join existing shared history**.
Do not create another baseline. Reload again; use **Pomodoro: Continue Session
Here** when switching computers. Google Drive must be signed in on each computer.
Wait for Drive sync to finish. The laptop resumes from the last uploaded snapshot;
an abrupt shutdown can leave an older snapshot. A real two-computer handoff still
needs verification after laptop setup. Git sync of code/records is separate.

Before leaving one computer:

1. Send `Finish for today` or pause and send `Save checkpoint`.
2. Ask `$github-agent commit and push the changes`.
3. Wait for confirmation that the push succeeded.

On the other computer, open the repository and run:

```powershell
git status
```

Once the checkout is clean and on `main`, run:

```powershell
git pull --ff-only
python codex/install_commands.py --keep-other-skills
```

Restart Codex if skills changed, then ask it to read `START-HERE.md` again.
Use one computer at a time for learning-record updates. Git transfers saved files;
it does not transfer unsaved chat work or automatically merge two active sessions.

## Common setup problems

| Problem | What to do |
| --- | --- |
| `git` or `python` is not recognised | Reopen PowerShell after installation. Check PATH or try `py` for Python. |
| Clone or pull says access denied | Sign in to GitHub on this desktop and confirm repository access. |
| Skills do not appear | Confirm the installer succeeded, fully restart Codex and search by skill name. Natural requests still work with the checkout open. |
| Installer reports an existing edited skill | Ask Codex to inspect the conflicting file. After deciding to replace it, rerun with `--keep-other-skills --replace-existing`; the installer backs it up. |
| Repository folder was moved | Rerun the installer from its new location to update the installed paths. |
| Git says author identity is unknown when committing | Configure your own name and email with `git config user.name "Your Name"` and `git config user.email "YOUR_GITHUB_EMAIL"` from the repository folder. GitHub sign-in is separate. |
| Excel refresh reports missing runtime dependencies | Keep the CSV records; ask Codex to configure the workbook runtime described in README.md. Report the workbook as stale until refreshed. |

The existing Excel workbook can be opened without the authoring runtime. Rebuilding it
needs Node.js and the `@oai/artifact-tool` runtime used by
`tracking/update-study-tracker.mjs`; these are separate from the Python skill installer.

Database connections, credentials, installed tools and temporary SQL tables need setup
on each computer. Keep credentials outside Git. Do not copy account or authentication
files into this repository.
