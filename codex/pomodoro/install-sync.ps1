param([string]$ExtensionPath)
$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding($false)
$manifestPath = Join-Path $ExtensionPath 'package.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($manifest.publisher -ne 'kumodh' -or $manifest.name -ne 'pomodoro-code-timer' -or $manifest.version -ne '1.0.0' -or $manifest.journeyPomodoroCustomization -ne 2) {
    throw 'Sync requires Pomodoro Code 1.0.0 with the daily-target customization.'
}
$sourcePath = Join-Path $ExtensionPath 'out/extension.js'
$source = [IO.File]::ReadAllText($sourcePath).Replace("`r`n", "`n")
$marker = '// journey-drive-sync-v1'
if (-not $source.Contains($marker)) {
    $anchor = '    statusBarItem.show();'
    if (-not $source.Contains($anchor)) { throw 'Unsupported extension activation. No sync changes written.' }
    $hook = @'
    // journey-drive-sync-v1
    require('./sync-vscode').attach({ context, vscode, timer: timerInstance, stats: statsManager,
        refresh: () => updateStatusBar(timerInstance.getTimeRemaining()) });
    statusBarItem.show();
'@
    $source = $source.Replace($anchor, $hook)
    $menuAnchor = '    const choice = await vscode.window.showQuickPick(items, {'
    if (-not $source.Contains($menuAnchor)) { throw 'Unsupported extension menu. No sync changes written.' }
    $menu = @'
    items.push({ label: '$(cloud) Configure Sync Folder', description: 'Connect a shared Google Drive timer folder.', command: 'pomodoro.configureSync' });
    if (vscode.workspace.getConfiguration('pomodoro').get('syncFolder', '')) {
        items.push({ label: '$(arrow-swap) Continue Session Here', description: 'Take over from the last synced snapshot. Keep the other computer stopped.', command: 'pomodoro.continueHere' });
    }
    const choice = await vscode.window.showQuickPick(items, {
'@
    $source = $source.Replace($menuAnchor, $menu)
}
$changed = $source -ne [IO.File]::ReadAllText($sourcePath).Replace("`r`n", "`n")
foreach ($name in @('sync.js', 'sync-vscode.js')) {
    $target = Join-Path $ExtensionPath "out/$name"
    if (-not (Test-Path -LiteralPath $target)) { $changed = $true }
    elseif ((Get-FileHash -LiteralPath $target).Hash -ne (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot $name)).Hash) { $changed = $true }
}
$properties = $manifest.contributes.configuration.properties
if ($properties.PSObject.Properties.Name -notcontains 'pomodoro.syncFolder') {
    $changed = $true
    $properties | Add-Member -NotePropertyName 'pomodoro.syncFolder' -NotePropertyValue ([pscustomobject]@{
        type = 'string'; default = ''; scope = 'machine'; description = 'Local absolute path to the shared Drive timer folder. Configure through Pomodoro: Configure Sync Folder. Empty disables sync. Do not use the Git repository.'
    })
}
foreach ($command in @(
    @{ command = 'pomodoro.configureSync'; title = 'Pomodoro: Configure Sync Folder' },
    @{ command = 'pomodoro.continueHere'; title = 'Pomodoro: Continue Session Here' }
)) {
    if ($manifest.contributes.commands.command -notcontains $command.command) {
        $changed = $true
        $manifest.contributes.commands += [pscustomobject]$command
    }
}
if (-not $changed) { Write-Output 'Drive sync support already installed. No files changed.'; return }
$backup = Join-Path $ExtensionPath ('journey-sync-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmssfff'))
New-Item -ItemType Directory -Path $backup | Out-Null
Copy-Item -LiteralPath $manifestPath -Destination $backup
Copy-Item -LiteralPath (Join-Path $ExtensionPath 'out') -Destination $backup -Recurse
[IO.File]::WriteAllText($sourcePath, $source, $utf8)
foreach ($name in @('sync.js', 'sync-vscode.js')) {
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Destination (Join-Path $ExtensionPath "out/$name")
}
[IO.File]::WriteAllText($manifestPath, ($manifest | ConvertTo-Json -Depth 30), $utf8)
Write-Output "Drive sync support installed, disabled until configured. Backup: $backup"
Write-Output 'Reload after pausing/finishing the current timer. Run Pomodoro: Configure Sync Folder.'
