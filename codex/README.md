# Personal Codex commands on every computer

## Five-role tutoring coordination

The skill picker has five separate role entries:

| Menu entry | Explicit invocation |
| --- | --- |
| Learning Coach | `$learning-coach` |
| Notes Keeper | `$notes-keeper` |
| Mistake Keeper | `$mistake-keeper` |
| Revision Coach | `$revision-coach` |
| Progress Tracker | `$progress-tracker` |

Type `/` to find these by name in the skill picker (or use `/skills` where that
command is supported). Learning Coach selects the saved pending task without starting a timer.
The nine existing commands also consult `reference/learning-coach.md`. Learning Coach, Notes Keeper,
Mistake Keeper, Revision Coach and Progress Tracker are responsibilities of one tutor,
not extra running agents. The five skills are individual entry points to those same roles.
With this checkout open, say Start today's
learning; Start revision; Show my mistakes; Show today's learning; Weekly review; or
Save checkpoint. These requests require no installation. Task selection/status never
starts a timer. Run the existing installer after pulling updates to refresh global skills.

Start interview practice and Show my weaknesses route through the existing Learning
Coach and shared guide; they add no command folders or timer system. Today's schedule
uses date-effective targets and the 13-week Azure roadmap targeting 22 January 2027.
Refresh installed command copies with the existing installer when ready; this repository
upgrade does not change unrelated global skill settings.

## GitHub utility

**GitHub Agent** is an additional picker entry for Git operations, separate from the
five tutoring roles. To publish the learning repository's changes, say:

```text
$github-agent review, commit and push the current changes
```

It reviews the intended files, runs relevant checks, commits and pushes to the verified
configured remote when asked. Creating/installing the skill does not publish anything.
It preserves existing learning/time records and does not publish automatically on saves.
GitHub authentication must already be configured separately on each computer.

The fifteen skills preserve the command definitions in the repository's README and
reference/study-tracking.md. Git stores their portable source here. The installer
places them in your user skill folder so they work from any project.

## First setup on another computer

Install Git, Python 3.11 or newer, and Codex. Sign in to Codex on that computer.
Clone the learning repository (or use your existing checkout):

```bash
git clone https://github.com/satishryali/data-engineering-journey.git
cd data-engineering-journey
python codex/install_commands.py
```

On macOS/Linux, use `python3` if `python` is unavailable. Fully close and reopen
Codex, then type `/` to search for a command. `$start-timer SQL` is also an explicit
invocation. Menu visibility must be checked on each computer.

| Command | Existing action |
| --- | --- |
| learning-coach | Start the coordinated five-role coach from the saved checkpoint |
| notes-keeper | Maintain existing learning notes from actual evidence |
| mistake-keeper | Show and maintain observed mistakes and follow-up tasks |
| revision-coach | Select one meaningful retrieval task |
| progress-tracker | Show evidence-based daily or weekly learning progress |
| github-agent | Review, commit and push changes when explicitly requested |
| start-timer | Start SQL, Python, dbt, Azure or another study topic |
| pause-timer | Pause |
| resume-timer | Resume a topic |
| finish-study | Finish and save the checkpoint |
| study-status | Study status / Study time |
| todays-schedule | Today's schedule |
| save-checkpoint | Save checkpoint / This is the checkpoint |
| finish-for-today | Finish for today |
| continue-checkpoint | Read the checkpoint and continue |

The installer writes only the fifteen command folders, skill enablement settings and
its installation manifest/backups. By default it disables other installed local
and cached plugin skills to match the personal-command-only preference. Built-in
commands such as `/model` remain. Plugin connections remain installed. New plugins
or updated plugin versions may add skill paths: rerun the installer to apply the
preference to the current inventory. To avoid adding disable overrides, use
`python codex/install_commands.py --keep-other-skills`; pre-existing overrides
outside the installer's managed block are preserved.

Existing conflicting or manually edited command files are not silently replaced.
Review them first; `--replace-existing` backs them up before replacing them.
The installer reports backup locations under your local Codex home. It preserves
unrelated configuration, account credentials and plugin settings. The repository
does not include your Codex configuration or authentication files.

## When moving between computers

1. Pause or finish study and save the checkpoint in the current learning chat.
2. Review, commit and push the intended learning records. This installer does not
   commit or push, and this setup commit does not include unrelated pending work.
3. On the other computer, check `git status`; once your checkout is clean, run:

```bash
git pull --ff-only
python codex/install_commands.py
```

4. Restart Codex if command files/settings changed. Use `continue-checkpoint` to
   load the saved learning state. It does not start a study timer.

Rerunning installation without changes is safe. If you move the checkout, rerun
the installer to update the installed commands' learning-repository path. It
requires no administrator access and does not start timers, create reminders,
change learning records or synchronize chats. Work on one computer at a time;
Git changes still need to be committed, pushed and pulled.

Skills are kept under `codex/skills`, rather than `.agents/skills` in this checkout,
to avoid duplicate project and global command entries after installation.

## Verification and recovery

Run the isolated installer checks with:

```bash
python -m unittest discover -s codex/tests -v
```

Backups are under `~/.codex/study-commands-backups` (or your configured
`CODEX_HOME`). To undo a setup, restore that backup's `config.toml` and any backed-up
skill folders; remove newly installed command folders only if you no longer want
them. Keep account credentials out of Git.

Official references: [skills and local installation](https://learn.chatgpt.com/docs/build-skills)
and [slash commands](https://learn.chatgpt.com/docs/reference/slash-commands).
