param()
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo

function Get-PyExe {
  foreach ($n in 'python','py') { if (Get-Command $n -ErrorAction SilentlyContinue) { return $n } }
  throw "Python not found on PATH (tried 'python' and 'py')"
}

& .\.deia\tools\heartbeat.ps1 -BotId BOT-00002 -Message 'Working link-fix-v1' | Out-Null
$py = Get-PyExe
$out = & $py .\.deia\tools\link_fix.py 2>&1
$suggestPath = ($out | Select-String -Pattern 'Suggestions written:\s*(.+)$').Matches.Groups[1].Value.Trim()
if (-not $suggestPath) { $suggestPath = '.\\.deia\\reports\\link-fix-latest.md' }
& .\.deia\tools\worker-log.ps1 -Worker link_fix -Invoker BOT-00002 -Args 'suggest' -Result ok | Out-Null
& .\.deia\tools\heartbeat.ps1 -BotId BOT-00002 -Message ("Suggestions written: " + $suggestPath) | Out-Null
Write-Output ("[BOT-00002] " + $suggestPath)

# Telemetry end with duration
try {
  if (-not $t0) { $script:t0 = Get-Date }
  $dur = [int](([datetime]::Now - $script:t0).TotalMilliseconds)
  & .\.deia\tools\telemetry.ps1 -AgentId BOT-00002 -Role drone -Event session_end -Message 'link-fix-v1' -DurationMs $dur | Out-Null
} catch {}
