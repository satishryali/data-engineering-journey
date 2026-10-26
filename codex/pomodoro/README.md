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
- Counts belong to the local VS Code profile until you configure the optional
  [two-computer sync](#continue-on-a-laptop-during-power-cuts). Neither mode creates
  confirmed study hours or establishes learning proficiency.
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
Reloading restarts the extension; without optional sync its countdown is not persisted. Try **Pomodoro: Test Sound**
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

For sessions completed on another computer, set `pomodoro.externalCompletedSessions`
in local workspace settings, for example `{"2026-10-26": 3}`. Each date stores the
total reported external completions for that IST day, added to local completions in
daily, weekly and overall statistics. Reusing the same value does not add it again.
Keep the original tracking start date and baseline unchanged. Install the update,
then reload after any running timer ends.

Run the installer against a disposable copy of the original extension and a disposable
settings file using `-ExtensionPath` and `-SettingsPath`. Then run:

```powershell
node codex/pomodoro/test.cjs PATH_TO_CUSTOMIZED_COPY
```

The integration test loads the real patched timer/extension with mocked VS Code,
storage and sound. It does not start a real study interval or add live session counts.

## Continue on a laptop during power cuts

Git still transfers your code and saved learning records. Google Drive transfers only
the small timer-data folder described below. Do not move the Git repository, VS Code
profile, databases or credentials into that folder.

### Set up once

1. Install [Google Drive for desktop](https://support.google.com/drive/answer/10838124)
   on both Windows computers and sign in to the same Google account.
2. Create an empty folder named `Pomodoro-Sync` in **My Drive**. Make it available
   offline on both computers, or use Drive's mirroring mode. Wait for Drive to finish
   syncing. The local paths may differ between computers.
3. On both computers, update this repository and install Pomodoro Code **1.0.0**:

   ```powershell
   code --install-extension kumodh.pomodoro-code-timer@1.0.0
   & ./codex/pomodoro/install.ps1
   ```

   The installer backs up the extension before patching. Sync starts disabled. Pause
   or finish any current timer, then run **Developer: Reload Window**.
4. On the original desktop, run **Pomodoro: Configure Sync Folder** in the Command
   Palette. Select `Pomodoro-Sync`, then **Create shared history from this computer**.
   This copies the currently displayed daily counts, including the initial baseline
   and reported external sessions, once. Older local history stays untouched. Check
   those displayed totals first; creation preserves them, it cannot verify reports.
5. Wait for `baseline.json` to arrive on the laptop. On the laptop, run the same
   configuration command, choose its copy of `Pomodoro-Sync`, then **Join existing
   shared history**. Joining does not add that laptop's local counts again. Any
   genuine historical sessions missing from the desktop's displayed totals need
   reconciliation before creating the shared history.
6. Reload both VS Code windows. Run **Pomodoro: Continue Session Here** on the
   computer you are using. Confirm Drive has finished syncing when prompted.

The folder path is saved in that computer's VS Code user settings as
`pomodoro.syncFolder`. It is not added to workspace settings or Git. Reinstall the
patch if a Marketplace update replaces it. Keep this patched extension at 1.0.0.

If the new code has not been pushed through Git yet, copy this directory to the
laptop (or use the prepared `Pomodoro-Setup.zip` in My Drive), extract it, and run
`Setup-Laptop.ps1` from PowerShell. It installs the extension and patch without
changing a repository's settings. Then follow its instructions to join the existing
`Pomodoro-Sync` folder. Google Drive alone does not install extensions on the laptop.

### When power fails

Open VS Code on the laptop. Wait for Google Drive to finish syncing, then run
**Pomodoro: Continue Session Here**. It resumes the latest saved phase and remaining
time. Leave the desktop timer stopped. When returning to the desktop, pause the
laptop timer, wait for Drive to finish on both, then take over on the desktop.

The timer saves on control changes and about every five seconds while running.
It freezes the saved remaining time during a shutdown: the gap is not counted as
work, and no completion is inferred because a clock deadline passed. Break phase
and long-break cycle position transfer too. Reopening VS Code observes the shared
state; it does not automatically run a second timer. Start/resume/reset/skip are
blocked on observers until explicit takeover.

Drive sync is **eventually consistent**, not instant. A sudden power loss can leave
the laptop with an older snapshot if the newest one was not uploaded. Internet on
the laptop cannot retrieve data that never left the desktop. There is no guaranteed
maximum sync delay or global lock: if both machines run during a connection delay,
both can temporarily believe they control the timer. Keep one active computer;
the old controller stops when it sees a newer takeover. Computer clocks do not
decide ownership. Distinct completion IDs prevent the same transferred focus session
from being counted twice, including duplicate/conflict copies of its completion.

If the folder is unavailable or its data is invalid, the timer pauses and reports an
error instead of silently starting a separate history. Wait for Drive to recover,
then use Continue Session Here. Preserve conflicting baseline files for inspection;
do not delete history to dismiss a warning. Disable sync by clearing the machine's
`pomodoro.syncFolder` setting and reloading after pausing; the shared files stay
saved, while the original local profile history becomes visible again.

Shared files contain counts and timer snapshots, with random window/session IDs.
No Google password, API key or study code is stored there. Local writes are handed
to the Drive client; the extension cannot confirm Google's upload status. Check
the Drive app before switching. This feature does not sync unsaved code or chats,
update the canonical study CSV, or convert Pomodoro counts into confirmed hours.

### Check the installation

Both commands run against a disposable customized extension copy:

```powershell
node codex/pomodoro/test.cjs PATH_TO_CUSTOMIZED_COPY
node codex/pomodoro/sync.test.cjs PATH_TO_CUSTOMIZED_COPY
```

The sync tests cover two simulated computers, takeover, retained remaining time,
duplicate completions, delayed replicas, invalid files, actual timer transitions,
reset/skip and recovery after a completion was saved before the next phase. They
do not test Google's upload latency or a physical power cut. After setup, verify
one paused handoff between the two real computers before relying on it.
