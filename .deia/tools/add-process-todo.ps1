param(
  [Parameter(Mandatory=$true)][string]$Title,
  [string]$Details = ''
)

$ErrorActionPreference='Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo

$todos = '.\.deia\guides\PROCESS-TODOS.md'
if (-not (Test-Path $todos)) { New-Item -ItemType File -Path $todos | Out-Null }

$ts = Get-Date -Format 'yyyy-MM-dd'
$entry = "- [ ] $Title — Added: $ts"
if ($Details) { $entry += "`r`n  - $Details" }

# Append to Open Items
$content = Get-Content $todos -Raw
if ($content -match '## Open Items') {
  $content = $content -replace '(?ms)(## Open Items\s*)','$1'+$entry+"`r`n"
} else {
  $content += "`r`n## Open Items`r`n$entry`r`n"
}
Set-Content $todos -Value $content -Encoding UTF8

# Update board announcement and bump rev
$board = '.\.deia\bot-status-board.json'
if (Test-Path $board) {
  $j = Get-Content $board -Raw | ConvertFrom-Json
  $now = (Get-Date).ToUniversalTime().ToString('o')
  if (-not $j.announcements) { $j | Add-Member -NotePropertyName announcements -NotePropertyValue @() }
  $ann = [pscustomobject]@{ timestamp=$now; from='BOT-00001'; priority='INFO'; title='Process TODO Updated'; message=$Title; documentation='.deia/guides/PROCESS-TODOS.md' }
  $j.announcements = @($ann) + @($j.announcements)
  $j.last_updated = $now; $j.rev = $now
  ($j | ConvertTo-Json -Depth 15) | Set-Content $board -Encoding UTF8
  $evt = @{timestamp=$now; type='process_todo_update'; queen_id='BOT-00001'; title=$Title} | ConvertTo-Json -Compress
  Add-Content -Path '.\.deia\hive-log.jsonl' -Value $evt -Encoding UTF8
}

Write-Output "TODO added and board announcement posted: $Title"
