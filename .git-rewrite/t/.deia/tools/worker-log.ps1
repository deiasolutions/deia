param(
  [Parameter(Mandatory=$true)][string]$Worker,
  [Parameter(Mandatory=$true)][string]$Invoker,
  [string]$Result = 'ok',
  [string]$Args = ''
)
$ts = (Get-Date).ToUniversalTime().ToString('o')
$base = (Resolve-Path '.').Path
$logDir = Join-Path $base '.deia/bot-logs'
$repDir = Join-Path $base '.deia/reports'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
New-Item -ItemType Directory -Force -Path $repDir | Out-Null
$jsonl = Join-Path $logDir 'worker-usage.jsonl'
$line = @{ts=$ts; worker=$Worker; invoker=$Invoker; result=$Result; args=$Args} | ConvertTo-Json -Compress
Add-Content -Path $jsonl -Value $line -Encoding UTF8

# Aggregate count file
$agg = Join-Path $repDir 'worker-usage.json'
if (Test-Path $agg) {
  $counts = Get-Content $agg -Raw | ConvertFrom-Json
} else {
  $counts = @{}
}
if (-not $counts.ContainsKey($Worker)) { $counts[$Worker] = 0 }
$counts[$Worker] = [int]$counts[$Worker] + 1
($counts | ConvertTo-Json -Compress) | Set-Content -Path $agg -Encoding UTF8
Write-Output "Worker logged: $Worker (count=$($counts[$Worker]))"
