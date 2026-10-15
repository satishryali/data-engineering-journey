# Personal Codex commands on every computer

These nine skills preserve the command definitions in the repository's README and
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
| start-timer | Start SQL, Python, dbt, Azure or another study topic |
| pause-timer | Pause |
| resume-timer | Resume a topic |
| finish-study | Finish and save the checkpoint |
| study-status | Study status / Study time |
| todays-schedule | Today's schedule |
| save-checkpoint | Save checkpoint / This is the checkpoint |
| finish-for-today | Finish for today |
| continue-checkpoint | Read the checkpoint and continue |

The installer writes only the nine command folders, skill enablement settings and
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
