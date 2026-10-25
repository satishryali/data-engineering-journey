# Pomodoro customization

Local customization for **Pomodoro Code** (`kumodh.pomodoro-code-timer` 1.0.0).
The installer backs up the original extension and workspace settings before changing them.
It preserves unrelated settings and existing daily session history.

- Focus: 25 minutes. Short break: 5 minutes. Sound and notifications enabled for both.
- The status bar shows completed / daily target alongside the timer; hover for remaining counts.
- **Pomodoro: Test Sound** plays the same completion alert.
- **Pomodoro: Show Stats**, or **Show Session Statistics** in the timer menu, shows
  today / daily target, sessions remaining today, this week / 110, overall,
  and sessions remaining this week. Weekdays target 14; Saturdays and Sundays target 20.
- Today changes at midnight IST. Weeks start Monday at midnight IST. Old history
  stays saved. A session is counted on the date its focus timer finishes.
- Breaks, resets and skipped phases do not count as completed focus sessions.
- The existing 15-minute long break after four completed focus sessions is preserved.
  Automatic starting of the next phase keeps its existing setting.
- Counts belong to the local VS Code profile. They do not automatically sync across
  computers, create confirmed study hours, or establish learning proficiency.
- This workspace starts displayed tracking on **25 October 2026 (IST)** with **3 reported
  completed sessions**, corrected to **4 reported sessions** after a fourth completion
  before the first customization reload. Earlier history stays stored but is excluded from displayed totals.
  The starting count is applied once per local profile; reloads preserve subsequent completions.
  Increasing `pomodoro.initialCompletedCount` corrects that baseline once and preserves
  later timer increments. Apply code changes with a reload after any running break finishes.
  The first week contains only the starting Sunday; 110 is the full-week target.

From the repository root in PowerShell:

```powershell
& ./codex/pomodoro/install.ps1
```

After installation, finish/pause any running Pomodoro and run **Developer: Reload Window**.
Reloading restarts the extension; its countdown is not persisted. Try **Pomodoro: Test Sound**
to verify audibility with your selected Windows audio device and volume.
Sound process success alone cannot confirm that a human heard it.

This is a local patch, not a Marketplace update. Reinstalling/updating the extension
can replace it. The installer refuses unsupported versions, upgrades the earlier customization,
and makes repeat installation a no-op. On another computer install version 1.0.0, then run the installer there.
The workspace must already have a valid `.vscode/settings.json` JSON file.

To undo: with VS Code closed, restore `package.json` and `out/` from the printed
`journey-backup-*` folder in the extension directory. Restore `workspace-settings.json`
to `.vscode/settings.json` only after preserving any newer unrelated edits.

## Verification

Run the installer against a disposable copy of the original extension and a disposable
settings file using `-ExtensionPath` and `-SettingsPath`. Then run:

```powershell
node codex/pomodoro/test.cjs PATH_TO_CUSTOMIZED_COPY
```

The integration test loads the real patched timer/extension with mocked VS Code,
storage and sound. It does not start a real study interval or add live session counts.
