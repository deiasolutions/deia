param(
  [string]$BaseUrl = "http://localhost:8000"
)

Write-Host "Smoke check → $BaseUrl" -ForegroundColor Cyan

function Test-Endpoint($path) {
  $url = "$BaseUrl$path"
  try {
    $resp = Invoke-RestMethod -Method GET -Uri $url -TimeoutSec 10 -ErrorAction Stop
    Write-Host "OK $path" -ForegroundColor Green
    return @{ ok=$true; body=$resp }
  } catch {
    Write-Host "FAIL $path : $($_.Exception.Message)" -ForegroundColor Red
    return @{ ok=$false; err=$_.Exception.Message }
  }
}

$ok = $true
$root = Test-Endpoint "/"
if (-not $root.ok) { $ok = $false }

$health = Test-Endpoint "/health"
if (-not $health.ok) { $ok = $false }

$ready = Test-Endpoint "/ready"
if (-not $ready.ok) { $ok = $false }

if ($ok) {
  Write-Host "Smoke check PASSED" -ForegroundColor Green
  exit 0
} else {
  Write-Host "Smoke check FAILED" -ForegroundColor Red
  exit 1
}

