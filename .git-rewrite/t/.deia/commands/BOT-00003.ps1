param()
$ErrorActionPreference = 'Stop'
# Set repo root (script lives in .deia/commands; go up two levels)
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\\..')).Path
Set-Location $repo

function Get-PyExe {
  foreach ($n in 'python','py') { if (Get-Command $n -ErrorAction SilentlyContinue) { return $n } }
  throw "Python not found on PATH (tried 'python' and 'py')"
}

& .\.deia\tools\heartbeat.ps1 -BotId BOT-00003 -Message 'Working repo-health-actions' | Out-Null
$py = Get-PyExe
$ts = Get-Date -Format 'yyyyMMdd-HHmm'
# Suppress benign Python runtime warning noise that PowerShell treats as errors
$docOut = & $py -W ignore::RuntimeWarning -m deia.cli doctor docs 2>&1
$docPath = ".\\.deia\\reports\\doctor-docs-$ts.txt"
New-Item -ItemType Directory -Force -Path .\.deia\reports | Out-Null
Set-Content $docPath -Value $docOut -Encoding UTF8
& .\.deia\tools\heartbeat.ps1 -BotId BOT-00003 -Message ("Doc audit saved: " + $docPath) | Out-Null
Write-Output ("[BOT-00003] " + $docPath)

# Telemetry end with duration
try {
  if (-not $t0) { $script:t0 = Get-Date }
  $dur = [int](([datetime]::Now - $script:t0).TotalMilliseconds)
  & .\.deia\tools\telemetry.ps1 -AgentId BOT-00003 -Role drone -Event session_end -Message 'repo-health-actions' -DurationMs $dur | Out-Null
} catch {}
