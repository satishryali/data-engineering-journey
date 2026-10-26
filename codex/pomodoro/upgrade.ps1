param(
    [string]$ExtensionPath,
    [string]$SettingsPath
)
$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding($false)
$manifestPath = Join-Path $ExtensionPath 'package.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($manifest.journeyPomodoroCustomization -eq 2) {
    if ($manifest.contributes.configuration.properties.PSObject.Properties.Name -notcontains 'pomodoro.externalCompletedSessions') {
        Copy-Item -LiteralPath $manifestPath -Destination ($manifestPath + '.backup-' + (Get-Date -Format 'yyyyMMdd-HHmmssfff'))
        $manifest.contributes.configuration.properties | Add-Member -NotePropertyName 'pomodoro.externalCompletedSessions' -NotePropertyValue ([pscustomobject]@{
            type = 'object'; default = @{}; additionalProperties = @{ type = 'integer'; minimum = 0 }; description = 'Reported completions on other computers, keyed by IST date YYYY-MM-DD. Added to local counts in the display.'
        })
        [IO.File]::WriteAllText($manifestPath, ($manifest | ConvertTo-Json -Depth 30), $utf8)
    }
    $installedStats = Join-Path $ExtensionPath 'out/stats.js'
    $newStats = Join-Path $PSScriptRoot 'stats.js'
    if ((Get-FileHash -LiteralPath $installedStats).Hash -ne (Get-FileHash -LiteralPath $newStats).Hash) {
        $statsBackup = $installedStats + '.backup-' + (Get-Date -Format 'yyyyMMdd-HHmmssfff')
        Copy-Item -LiteralPath $installedStats -Destination $statsBackup
        Copy-Item -LiteralPath $newStats -Destination $installedStats
        Write-Output "Statistics correction installed. Backup: $statsBackup"
        Write-Output 'Reload VS Code after the running break or timer ends to activate it.'
    } else {
        Write-Output 'Daily-target customization already installed. No files changed.'
    }
    return
}
if ($manifest.journeyPomodoroCustomization -ne 1) { throw 'Install customization v1 before this upgrade.' }
$sourcePath = Join-Path $ExtensionPath 'out/extension.js'
$source = [IO.File]::ReadAllText($sourcePath).Replace("`r`n", "`n")
$old = 'statsManager = new stats_1.StatsManager(context.globalState);'
if (-not $source.Contains($old)) { throw 'Unsupported stats initialization.' }
$source = $source.Replace($old, @'
const journeyConfig = vscode.workspace.getConfiguration('pomodoro');
    statsManager = new stats_1.StatsManager(context.globalState, {
        startDate: journeyConfig.get('trackingStartDate', ''),
        initialCount: journeyConfig.get('initialCompletedCount', 0)
    });
'@)
$start = $source.IndexOf('function statsText() {')
$end = $source.IndexOf('function showStats()', $start)
if ($start -lt 0 -or $end -lt 0) { throw 'Unsupported stats display.' }
$display = @'
function statsText() {
    const config = vscode.workspace.getConfiguration('pomodoro');
    return (0, stats_1.formatSummary)(statsManager.getSummary(), getTodayKey(), {
        weekdayTarget: config.get('weekdayTarget', 14),
        weekendTarget: config.get('weekendTarget', 20),
        weeklyTarget: config.get('weeklyTarget', 110)
    });
}
'@
$source = $source.Substring(0, $start) + $display + "`n" + $source.Substring($end)
$tooltipLine = "    statusBarItem.tooltip += '\n' + statsText();"
if (-not $source.Contains($tooltipLine)) { throw 'Unsupported status bar display.' }
$source = $source.Replace($tooltipLine, @'
    const counts = statsManager.getSummary();
    const daily = (0, stats_1.dailyTarget)(getTodayKey(), config.get('weekdayTarget', 14), config.get('weekendTarget', 20));
    statusBarItem.text += ` | ${counts.today}/${daily}`;
    statusBarItem.tooltip += '\n' + statsText();
'@.Replace("'\\n'", "'\n'"))
$properties = $manifest.contributes.configuration.properties
$definitions = @{
    'pomodoro.weekdayTarget' = @{ type = 'integer'; default = 14; minimum = 1; description = 'Completed focus sessions each Monday-Friday (IST).' }
    'pomodoro.weekendTarget' = @{ type = 'integer'; default = 20; minimum = 1; description = 'Completed focus sessions each Saturday and Sunday (IST).' }
    'pomodoro.trackingStartDate' = @{ type = 'string'; default = ''; pattern = '^$|^\d{4}-\d{2}-\d{2}$'; description = 'First displayed tracking date in IST. Older history is retained.' }
    'pomodoro.initialCompletedCount' = @{ type = 'integer'; default = 0; minimum = 0; description = 'Reported completed count on the tracking start date, applied once per local profile.' }
}
foreach ($key in $definitions.Keys) { $properties | Add-Member -NotePropertyName $key -NotePropertyValue ([pscustomobject]$definitions[$key]) -Force }
$manifest.journeyPomodoroCustomization = 2
$settings = Get-Content -LiteralPath $SettingsPath -Raw | ConvertFrom-Json
$values = @{ 'pomodoro.weekdayTarget' = 14; 'pomodoro.weekendTarget' = 20; 'pomodoro.trackingStartDate' = '2026-10-25'; 'pomodoro.initialCompletedCount' = 3 }
foreach ($key in $values.Keys) {
    if ($settings.PSObject.Properties.Name -notcontains $key) { $settings | Add-Member -NotePropertyName $key -NotePropertyValue $values[$key] }
}
$backup = Join-Path $ExtensionPath ('journey-daily-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmssfff'))
New-Item -ItemType Directory -Path $backup | Out-Null
Copy-Item -LiteralPath $manifestPath -Destination $backup
Copy-Item -LiteralPath (Join-Path $ExtensionPath 'out') -Destination $backup -Recurse
Copy-Item -LiteralPath $SettingsPath -Destination (Join-Path $backup 'workspace-settings.json')
[IO.File]::WriteAllText($sourcePath, $source, $utf8)
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'stats.js') -Destination (Join-Path $ExtensionPath 'out/stats.js')
[IO.File]::WriteAllText($manifestPath, ($manifest | ConvertTo-Json -Depth 30), $utf8)
[IO.File]::WriteAllText([IO.Path]::GetFullPath($SettingsPath), ($settings | ConvertTo-Json -Depth 30), $utf8)
Write-Output "Daily targets installed; history retained. Backup: $backup"
Write-Output 'Reload VS Code when no timer is running to activate the changes.'
