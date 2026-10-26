param(
    [string]$ExtensionPath = (Join-Path $env:USERPROFILE '.vscode/extensions/kumodh.pomodoro-code-timer-1.0.0')
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath (Join-Path $ExtensionPath 'package.json'))) {
    $codeCommand = Get-Command code.cmd -ErrorAction SilentlyContinue
    if (-not $codeCommand) { throw 'Install VS Code first, then run this setup again.' }
    & $codeCommand.Source --install-extension kumodh.pomodoro-code-timer@1.0.0
    if ($LASTEXITCODE -ne 0) { throw 'Pomodoro extension installation failed.' }
}
# The portable installer does not need or change a repository's workspace settings.
$temporarySettings = Join-Path ([IO.Path]::GetTempPath()) ('journey-pomodoro-setup-' + [guid]::NewGuid().ToString() + '.json')
try {
    [IO.File]::WriteAllText($temporarySettings, '{}', (New-Object System.Text.UTF8Encoding($false)))
    & (Join-Path $PSScriptRoot 'install.ps1') -ExtensionPath $ExtensionPath -SettingsPath $temporarySettings
} finally {
    if (Test-Path -LiteralPath $temporarySettings) { Remove-Item -LiteralPath $temporarySettings }
}
Write-Output ''
Write-Output 'Laptop extension is ready. To connect it:'
Write-Output '1. Pause/finish any current timer, then run Developer: Reload Window in VS Code.'
Write-Output '2. Run Pomodoro: Configure Sync Folder from the Command Palette.'
Write-Output '3. Select My Drive/Pomodoro-Sync and choose Join existing shared history.'
Write-Output '4. Reload again, then use Pomodoro: Continue Session Here when ready to study.'
Write-Output 'Do not create another baseline. Wait until Google Drive finishes syncing before switching computers.'
