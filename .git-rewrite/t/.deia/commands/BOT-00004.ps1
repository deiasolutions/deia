param()
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo

# Read the single launch file as the prompt
$launchFile = ".\.deia\instructions\LAUNCH-BOT-00004-15MIN.md"
if (-not (Test-Path $launchFile)) { throw "Launch file not found: $launchFile" }
$prompt = (Get-Content -Raw $launchFile) + "`n`nRespond only with: BOT-00004 Ready."

# Try Ollama first
$oll = Get-Command ollama -ErrorAction SilentlyContinue
if ($oll) {
  try { Start-Service Ollama -ErrorAction SilentlyContinue | Out-Null } catch {}
  $out = & ollama run llama3 "$prompt" 2>&1
  Write-Host $out
  exit 0
}

# Fallback: llama.cpp main.exe in current folder
if (Test-Path .\main.exe) {
  $model = Read-Host 'Enter full path to your model.gguf'
  if (-not (Test-Path $model)) { Write-Host "Model not found: $model"; exit 1 }
  $out = & .\main.exe -m "$model" -p "$prompt" 2>&1
  Write-Host $out
  exit 0
}

Write-Host "No Llama runner found. Install Ollama then rerun this file:" -ForegroundColor Yellow
Write-Host "  winget install Ollama.Ollama"
exit 1

