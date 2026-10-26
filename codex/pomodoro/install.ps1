param(
    [string]$ExtensionPath = (Join-Path $env:USERPROFILE '.vscode/extensions/kumodh.pomodoro-code-timer-1.0.0'),
    [string]$SettingsPath = (Join-Path $PSScriptRoot '../../.vscode/settings.json')
)
$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding($false)
$manifestPath = Join-Path $ExtensionPath 'package.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($manifest.publisher -ne 'kumodh' -or $manifest.name -ne 'pomodoro-code-timer' -or $manifest.version -ne '1.0.0') {
    throw 'This customization supports kumodh.pomodoro-code-timer 1.0.0 only.'
}
$marker = 'journeyPomodoroCustomization'
if ($manifest.PSObject.Properties.Name -contains $marker) {
    & (Join-Path $PSScriptRoot 'upgrade.ps1') -ExtensionPath $ExtensionPath -SettingsPath $SettingsPath
    & (Join-Path $PSScriptRoot 'install-sync.ps1') -ExtensionPath $ExtensionPath
    return
}
function Replace-Required([string]$text, [string]$old, [string]$new) {
    if (-not $text.Contains($old)) { throw "Unsupported extension source: missing $old" }
    return $text.Replace($old, $new)
}
$extension = [IO.File]::ReadAllText((Join-Path $ExtensionPath 'out/extension.js')).Replace("`r`n", "`n")
$timer = [IO.File]::ReadAllText((Join-Path $ExtensionPath 'out/timer.js')).Replace("`r`n", "`n")
$extension = Replace-Required $extension 'timerInstance.onPhaseComplete = async (phase) => {' 'timerInstance.onPhaseComplete = async (phase, completed) => {'
$extension = Replace-Required $extension 'await handlePhaseComplete(phase);' 'if (completed) await handlePhaseComplete(phase);'
$extension = Replace-Required $extension '(0, audio_1.playAlert)();' 'void playSound();'
$start = $extension.IndexOf('function getTodayKey() {')
$end = $extension.IndexOf('async function showQuickPickMenu()', $start)
if ($start -lt 0 -or $end -lt 0) { throw 'Cannot locate stats functions.' }
$statsFunctions = @'
function getTodayKey() {
    return (0, stats_1.todayKey)();
}
function statsText() {
    const counts = statsManager.getSummary();
    const target = vscode.workspace.getConfiguration('pomodoro').get('weeklyTarget', 110);
    return `Today (IST): ${counts.today} | This week (Mon-Sun): ${counts.week}/${target} | Overall: ${counts.overall} | Remaining this week: ${Math.max(0, target - counts.week)}`;
}
function showStats() {
    vscode.window.showInformationMessage(statsText());
}
async function playSound() {
    try {
        await (0, audio_1.playAlert)();
    } catch (error) {
        vscode.window.showWarningMessage(`Pomodoro sound failed: ${error.message}`);
    }
}
'@
$extension = $extension.Substring(0, $start) + $statsFunctions + "`n" + $extension.Substring($end)
$extension = Replace-Required $extension "label: '`$(checklist) Show Daily Statistics'," "label: '`$(checklist) Show Session Statistics',"
$extension = Replace-Required $extension "description: 'Show total completed sessions for today.'," 'description: statsText(),'
$extension = Replace-Required $extension "vscode.commands.registerCommand('pomodoro.stats', () => {" "vscode.commands.registerCommand('pomodoro.testSound', () => playSound()), vscode.commands.registerCommand('pomodoro.stats', () => {"
$extension = Replace-Required $extension "    const choice = await vscode.window.showQuickPick(items, {" "    items.push({ label: '`$(unmute) Test Sound', description: 'Play the completion alert.', command: 'pomodoro.testSound' });`n    const choice = await vscode.window.showQuickPick(items, {"
$extension = Replace-Required $extension '        if (enableCelebration) {' '        updateStatusBar(timerInstance.getTimeRemaining());
        if (enableCelebration) {'
$extension = Replace-Required $extension "    }`n}`nfunction handleStateChange()" "    }`n    statusBarItem.tooltip += '\n' + statsText();`n}`nfunction handleStateChange()"
$timer = Replace-Required $timer 'this.transitionPhase();' 'this.transitionPhase(false);'
# Only natural expiry counts as a completed focus session; skip still changes phase.
$timer = Replace-Required $timer "if (this.timeRemaining === 0) {`n            this.transitionPhase(false);" "if (this.timeRemaining === 0) {`n            this.transitionPhase(true);"
$timer = Replace-Required $timer 'transitionPhase() {' 'transitionPhase(completed = true) {'
$timer = Replace-Required $timer '            this.workCyclesCompleted++;' '            if (completed) this.workCyclesCompleted++;'
$timer = Replace-Required $timer "this.phase = this.workCyclesCompleted % this.config.longBreakInterval === 0 ? 'longBreak' : 'shortBreak';" "this.phase = completed && this.workCyclesCompleted % this.config.longBreakInterval === 0 ? 'longBreak' : 'shortBreak';"
$timer = Replace-Required $timer 'this.onPhaseComplete?.(prevPhase);' 'this.onPhaseComplete?.(prevPhase, completed);'
$manifest.contributes.commands += [pscustomobject]@{ command = 'pomodoro.testSound'; title = 'Pomodoro: Test Sound' }
$manifest.contributes.configuration.properties | Add-Member -NotePropertyName 'pomodoro.weeklyTarget' -NotePropertyValue ([pscustomobject]@{
    type = 'integer'; default = 110; minimum = 1; description = 'Completed focus session target for each Monday-Sunday week (IST).'
})
$manifest | Add-Member -NotePropertyName $marker -NotePropertyValue 1
# Prepare all content before mutation. Preserve both extension and settings originals.
$settings = [IO.File]::ReadAllText([IO.Path]::GetFullPath($SettingsPath)) | ConvertFrom-Json
$values = @{ 'pomodoro.enableAudio' = $true; 'pomodoro.enableNotifications' = $true; 'pomodoro.sessionDuration' = 25; 'pomodoro.shortBreakDuration' = 5; 'pomodoro.weeklyTarget' = 110 }
foreach ($key in $values.Keys) { $settings | Add-Member -NotePropertyName $key -NotePropertyValue $values[$key] -Force }
$backupPath = Join-Path $ExtensionPath ('journey-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $backupPath | Out-Null
Copy-Item -LiteralPath $manifestPath -Destination $backupPath
Copy-Item -LiteralPath (Join-Path $ExtensionPath 'out') -Destination $backupPath -Recurse
Copy-Item -LiteralPath $SettingsPath -Destination (Join-Path $backupPath 'workspace-settings.json')
[IO.File]::WriteAllText((Join-Path $ExtensionPath 'out/extension.js'), $extension, $utf8)
[IO.File]::WriteAllText((Join-Path $ExtensionPath 'out/timer.js'), $timer, $utf8)
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'stats.js') -Destination (Join-Path $ExtensionPath 'out/stats.js')
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'audio.js') -Destination (Join-Path $ExtensionPath 'out/audio.js')
[IO.File]::WriteAllText([IO.Path]::GetFullPath($SettingsPath), ($settings | ConvertTo-Json -Depth 30), $utf8)
[IO.File]::WriteAllText($manifestPath, ($manifest | ConvertTo-Json -Depth 30), $utf8)
Write-Output "Customized Pomodoro. Original files: $backupPath"
& (Join-Path $PSScriptRoot 'upgrade.ps1') -ExtensionPath $ExtensionPath -SettingsPath $SettingsPath
& (Join-Path $PSScriptRoot 'install-sync.ps1') -ExtensionPath $ExtensionPath
Write-Output 'Reload VS Code when no timer is running to activate the changes.'
