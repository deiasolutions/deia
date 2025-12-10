param(
  [string]$BotId = 'BOT-00004',
  [string]$TaskId = 'llama-brief-v1',
  [switch]$StartTask = $true
)

$ErrorActionPreference = 'Stop'

Write-Host "[1/6] Joining hive as $BotId..."

# Find python executable (python or py)
$pyExe = $null
foreach ($name in @('python','py')) {
  $cmd = Get-Command $name -ErrorAction SilentlyContinue
  if ($cmd) { $pyExe = $cmd.Name; break }
}
if (-not $pyExe) { throw "Python not found on PATH (neither 'python' nor 'py')." }

# Prefer module execution to avoid quoting issues
$joinOut = & $pyExe -m deia.cli hive join .deia/hive-recipe.json --role $BotId 2>&1
Write-Host $joinOut

# Parse Instance ID
$instanceId = $null
$m = [regex]::Match($joinOut, 'Instance ID:\s*([A-Za-z0-9_-]+)')
if ($m.Success) { $instanceId = $m.Groups[1].Value }
if (-not $instanceId) {
  # fallback: short random hex
  $instanceId = -join ((48..57 + 97..102) | Get-Random -Count 8 | ForEach-Object {[char]$_})
  Write-Warning "Could not parse Instance ID from join output. Using generated: $instanceId"
}

Write-Host "[2/6] Updating CLAIMED BY in instructions..."
$instr = Join-Path (Resolve-Path '.').Path ".deia/instructions/$BotId-instructions.md"
if (-not (Test-Path $instr)) { throw "Instruction file not found: $instr" }
$raw = Get-Content $instr -Raw
$now = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

# Ensure CLAIMED BY block reflects the claimed identity
$raw = $raw -replace '\*\*Instance ID:\*\*\s*UNCLAIMED', "**Instance ID:** $instanceId"
$raw = $raw -replace '\*\*Claimed at:\*\*\s*[^\r\n]*', "**Claimed at:** $now"
$raw = $raw -replace '\*\*Last check-in:\*\*\s*[^\r\n]*', "**Last check-in:** $now"
$raw = $raw -replace '\*\*Status:\*\*\s*[^\r\n]*', "**Status:** ACTIVE"
Set-Content -Path $instr -Value $raw -Encoding UTF8

Write-Host "[3/6] Sending Ready heartbeat..."
& (Join-Path (Resolve-Path '.').Path '.deia/tools/heartbeat.ps1') -BotId $BotId -Message 'Ready' | Out-Null

Write-Host "[4/6] Starting telemetry (session_start)..."
& (Join-Path (Resolve-Path '.').Path '.deia/tools/telemetry.ps1') -AgentId $BotId -Role 'drone' -Event 'session_start' -Message $TaskId | Out-Null

if ($StartTask) {
  Write-Host "[5/6] Announcing task start ($TaskId) via heartbeat..."
  & (Join-Path (Resolve-Path '.').Path '.deia/tools/heartbeat.ps1') -BotId $BotId -Message ("Working " + $TaskId) | Out-Null
}

# Final status
Write-Host "[6/6] Done. $BotId is claimed (Instance ID: $instanceId) and Ready."
Write-Host "Next: Llama reads task materials and writes brief to .deia/reports as instructed."

exit 0
