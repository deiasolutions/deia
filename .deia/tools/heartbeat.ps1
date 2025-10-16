param(
  [string]$BotId = "BOT-00002",
  [Parameter(Mandatory=$true)][string]$Message
)
$ts = (Get-Date).ToString('s')
$instr = Join-Path (Resolve-Path '.').Path ".deia/instructions/$BotId-instructions.md"
$line = "- $ts [$BotId] $Message"
Add-Content -Path $instr -Value $line -Encoding UTF8
Write-Output "Heartbeat appended: $line"