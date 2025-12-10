param(
  [int]$Threshold = 800,
  [switch]$BumpBoard = $true
)

$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path '.').Path
$reportJson = Join-Path $repo '.deia/reports/instruction-token-lint.json'
$alertsMd = Join-Path $repo (".deia/reports/instruction-token-alert-" + (Get-Date -Format 'yyyyMMdd-HHmm') + '.md')

# Run lint
& (Join-Path $repo '.deia/tools/instruction-token-lint.ps1') -Threshold $Threshold -JsonReport $reportJson | Out-String | Write-Output

$data = Get-Content $reportJson -Raw | ConvertFrom-Json
$over = @($data | Where-Object { $_.Tokens -gt $Threshold })

if ($over.Count -gt 0) {
  # Write alert report
  $sb = New-Object System.Text.StringBuilder
  [void]$sb.AppendLine("# Instruction Token Alert")
  [void]$sb.AppendLine("Threshold: $Threshold tokens")
  [void]$sb.AppendLine("")
  foreach ($r in $over) {
    [void]$sb.AppendLine("- ``$($r.File)`` → $($r.Tokens) tokens (chars=$($r.Chars))")
  }
  $sb.ToString() | Set-Content -Path $alertsMd -Encoding UTF8
}

if ($BumpBoard) {
  $board = Join-Path $repo '.deia/bot-status-board.json'
  if (Test-Path $board) {
    $j = Get-Content $board -Raw | ConvertFrom-Json
    $now = (Get-Date).ToUniversalTime().ToString('o')
    $j.last_updated = $now
    $j.rev = $now
    ($j | ConvertTo-Json -Depth 12) | Set-Content $board -Encoding UTF8
    # Log
    $evt = @{timestamp=$now; type='nightly_instruction_lint'; queen_id='BOT-00001'; file=$board; over=$($over.Count); threshold=$Threshold} | ConvertTo-Json -Compress
    Add-Content -Path (Join-Path $repo '.deia/hive-log.jsonl') -Value $evt -Encoding UTF8
  }
}

Write-Output ("Nightly instruction lint done. Over threshold: " + $over.Count)

