param(
  [int]$WindowHours = 24
)

$ErrorActionPreference='Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo

$cut = (Get-Date).AddHours(-$WindowHours)
$logs = Get-ChildItem .\.deia\bot-logs\*-activity.jsonl -ErrorAction SilentlyContinue
$modelsPath = '.\.deia\telemetry\models.json'
$models = @{}
if (Test-Path $modelsPath) { $models = Get-Content $modelsPath -Raw | ConvertFrom-Json }

$stats = @{}
foreach ($f in $logs) {
  $lines = Get-Content $f.FullName -ErrorAction SilentlyContinue
  foreach ($line in $lines) {
    try { $j = $line | ConvertFrom-Json } catch { continue }
    if (-not $j.ts) { continue }
    $t = [datetime]::Parse($j.ts)
    if ($t -lt $cut) { continue }
    $id = $j.agent_id
    if (-not $stats.ContainsKey($id)) {
      $m = $null; if ($models.PSObject.Properties.Name -contains $id) { $m = $models.$id.model }
      $stats[$id] = [pscustomobject]@{
        agent_id=$id; model=$m; events=0; tokens=0; sessions=@(); first=$t; last=$t
      }
    }
    $s = $stats[$id]
    $s.events += 1
    if ($j.total_tokens) { $s.tokens += [int]$j.total_tokens }
    if ($t -lt $s.first) { $s.first=$t }
    if ($t -gt $s.last) { $s.last=$t }
    if ($j.event -eq 'session_end' -and $j.duration_ms) { $s.sessions += [int]$j.duration_ms }
  }
}

$outDir = '.\\.deia\\reports'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$file = Join-Path $outDir ("telemetry-summary-" + (Get-Date -Format 'yyyyMMdd-HHmm') + '.md')

$lines = @('# Telemetry Summary', "", "**Window:** last $WindowHours hour(s)", "")
foreach ($key in $stats.Keys) {
  $s = $stats[$key]
  $avg = ($s.sessions.Count -gt 0) ? [int]($s.sessions | Measure-Object -Average).Average : 0
  $lines += "## $($s.agent_id) ($($s.model))"
  $lines += "- Events: $($s.events)"
  $lines += "- Total tokens: $($s.tokens)"
  $lines += "- Avg session duration: $avg ms"
  $lines += "- Active: $($s.first.ToString('HH:mm')) - $($s.last.ToString('HH:mm'))"
  $lines += ""
}

Set-Content $file -Value ($lines -join "`r`n") -Encoding UTF8
Write-Output "Summary written: $file"

exit 0

