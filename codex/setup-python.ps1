param(
    [string]$PythonExecutable = '',
    [switch]$Recreate,
    [switch]$IncludeRecallLab
)
$ErrorActionPreference = 'Stop'
$repository = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$environmentPath = [IO.Path]::GetFullPath((Join-Path $repository '.venv'))
$environmentPython = Join-Path $environmentPath 'Scripts/python.exe'

function Invoke-CheckedPython([string]$Executable, [string[]]$Arguments) {
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Python command failed with exit code $LASTEXITCODE. See the error above." }
}

# An activated shell may still refer to a copied or broken environment. Discover a
# base interpreter independently; callers can always supply its exact local path.
if (-not $PythonExecutable) {
    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($launcher) {
        $PythonExecutable = (& $launcher.Source -3 -c 'import sys; print(sys.executable)' | Out-String).Trim()
        if ($LASTEXITCODE -ne 0) { throw 'The Python launcher failed. Install Python 3.11+ or pass -PythonExecutable with its full path.' }
    } else {
        $candidate = Get-Command python.exe -ErrorAction SilentlyContinue
        if (-not $candidate) { throw 'Install Python 3.11+ first, reopen PowerShell, then rerun this script.' }
        $PythonExecutable = $candidate.Source
    }
}
$baseExecutable = (& $PythonExecutable -c 'import sys; print(sys._base_executable)' | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $baseExecutable)) {
    throw 'Choose a working local Python installation with -PythonExecutable. A copied .venv cannot supply it.'
}
$PythonExecutable = $baseExecutable
Invoke-CheckedPython $PythonExecutable @('-c', 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)')

if ($Recreate -and (Test-Path -LiteralPath $environmentPath)) {
    # Resolve/check both paths before moving a directory. Never delete old files.
    if ([IO.Path]::GetDirectoryName($environmentPath) -ne $repository -or [IO.Path]::GetFileName($environmentPath) -ne '.venv') {
        throw 'Unexpected environment path. Nothing moved.'
    }
    if ((Get-Item -LiteralPath $environmentPath -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw 'The environment is a link. Preserve it and resolve its target before recreating.'
    }
    $basePrefix = (& $PythonExecutable -c 'import sys; print(sys.base_prefix)' | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $basePrefix.StartsWith($environmentPath, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Choose a Python installation outside .venv before recreating it.'
    }
    $backup = $environmentPath + '.backup-' + (Get-Date -Format 'yyyyMMdd-HHmmssfff')
    if ([IO.Path]::GetDirectoryName($backup) -ne $repository) { throw 'Unexpected backup path. Nothing moved.' }
    Move-Item -LiteralPath $environmentPath -Destination $backup
    Write-Output "Previous environment preserved at $backup"
}
if (-not (Test-Path -LiteralPath $environmentPath)) {
    Invoke-CheckedPython $PythonExecutable @('-m', 'venv', $environmentPath)
}
if (-not (Test-Path -LiteralPath $environmentPython)) {
    throw 'The existing .venv is incomplete. Close notebook kernels/old terminals and rerun with -Recreate.'
}
try {
    $prefix = (& $environmentPython -c 'import sys; print(sys.prefix)' | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or [IO.Path]::GetFullPath($prefix) -ne $environmentPath) { throw 'Interpreter does not belong to this checkout.' }
    Invoke-CheckedPython $environmentPython @('-c', 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)')
} catch {
    throw 'The existing .venv cannot run here. Close notebook kernels/old terminals and rerun with -Recreate and a working -PythonExecutable.'
}
Invoke-CheckedPython $environmentPython @('-m', 'pip', 'install', '--disable-pip-version-check', '-r', (Join-Path $repository 'requirements-study.txt'))
if ($IncludeRecallLab) {
    Invoke-CheckedPython $environmentPython @('-m', 'pip', 'install', '--disable-pip-version-check', '-r', (Join-Path $repository 'apps/recalllab/requirements.txt'))
}
Invoke-CheckedPython $environmentPython @('-m', 'pip', 'check')
Invoke-CheckedPython $environmentPython @((Join-Path $PSScriptRoot 'verify-python-env.py'))
Write-Output ''
Write-Output 'Open data-engineering.code-workspace in VS Code.'
Write-Output 'Run Python: Select Interpreter and choose this checkout''s .venv/Scripts/python.exe.'
Write-Output 'In each notebook use Select Kernel > Select Another Kernel > Python Environments > .venv.'
Write-Output 'No activation is needed for direct .venv/Scripts/python.exe commands.'
