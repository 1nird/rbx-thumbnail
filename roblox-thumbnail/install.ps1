# rxz · roblox-thumbnail installer (Windows)
#   powershell -ExecutionPolicy Bypass -File install.ps1
# Copies this folder to ~/.claude/skills/roblox-thumbnail, backing up an older copy first.

$ErrorActionPreference = "Stop"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$skills = Join-Path $HOME ".claude\skills"
$dst = Join-Path $skills "roblox-thumbnail"

New-Item -ItemType Directory -Force -Path $skills | Out-Null

if (Test-Path $dst) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backup = Join-Path $HOME ".claude\skills-backup-$stamp-roblox-thumbnail"
    Move-Item $dst $backup
    Write-Host "  backed up the old copy to $backup"
}

Copy-Item $here $dst -Recurse
Write-Host "  installed skill roblox-thumbnail -> $dst"

$py = Get-Command py -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python -ErrorAction SilentlyContinue }

if ($py) {
    & $py.Source -c "import PIL" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "  Pillow is missing. Install it with:  $($py.Source) -m pip install pillow"
    }
} else {
    Write-Host ""
    Write-Host "  Python was not found on PATH. Install Python 3.10+ and Pillow."
}

Write-Host ""
Write-Host "Done. Restart your agent, then type:  /roblox-thumbnail"
