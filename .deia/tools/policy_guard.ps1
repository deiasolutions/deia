$ErrorActionPreference = 'Stop'

# Guard for ROTG-2 do-not-erase policy within .deia local commons
$lockFiles = @(
  Join-Path $PSScriptRoot '..' 'ROTG-2-RESPECT-DO-NOT-ERASE.lock'
)

$activeLocks = $lockFiles | Where-Object { Test-Path $_ }
if ($activeLocks.Count -gt 0) {
  Write-Error "ROTG-2 lock active: edits to '.deia' are prohibited. Respect do-not-erase."
  exit 3
}

Write-Output "No active ROTG-2 locks detected."
exit 0

