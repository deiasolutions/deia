# Launch CLAUDE-CODE-002 with clean environment (no ANTHROPIC_API_KEY conflict)

Write-Host "[LAUNCH] Removing ANTHROPIC_API_KEY from environment..." -ForegroundColor Yellow
$env:ANTHROPIC_API_KEY = $null
Remove-Item Env:\ANTHROPIC_API_KEY -ErrorAction SilentlyContinue

Write-Host "[LAUNCH] Verifying removal..." -ForegroundColor Yellow
if ($env:ANTHROPIC_API_KEY) {
    Write-Host "[ERROR] ANTHROPIC_API_KEY still set to: $env:ANTHROPIC_API_KEY" -ForegroundColor Red
    Write-Host "[ERROR] You need to remove it from System Environment Variables" -ForegroundColor Red
    Write-Host "[ERROR] Go to: System Properties -> Environment Variables -> Delete ANTHROPIC_API_KEY" -ForegroundColor Red
    exit 1
} else {
    Write-Host "[OK] ANTHROPIC_API_KEY cleared" -ForegroundColor Green
}

Write-Host "[LAUNCH] Changing to project directory..." -ForegroundColor Yellow
Set-Location "C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions"

Write-Host "[LAUNCH] Starting Claude Code for bot 002..." -ForegroundColor Green
Write-Host "[LAUNCH] First action: Read .deia\handoffs\CLAUDE-CODE-002-LAUNCH-2025-10-24.md" -ForegroundColor Cyan
Write-Host ""

& claude
