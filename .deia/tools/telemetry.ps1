param(
  [Parameter(Mandatory=$true)][string]$AgentId,
  [Parameter(Mandatory=$true)][ValidateSet('queen','drone','worker')][string]$Role,
  [Parameter(Mandatory=$true)][string]$Event,
  [string]$Message = '',
  [int]$PromptTokens = 0,
  [int]$CompletionTokens = 0,
  [int]$DurationMs = 0,
  [hashtable]$Meta
)
$ts = (Get-Date).ToUniversalTime().ToString('o')
$logDir = Join-Path (Resolve-Path '.').Path '.deia/bot-logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$file = Join-Path $logDir ("$AgentId-activity.jsonl")
$total = $PromptTokens + $CompletionTokens
$payload = [ordered]@{
  ts=$ts; agent_id=$AgentId; role=$Role; event=$Event; message=$Message;
  duration_ms=$DurationMs; prompt_tokens=$PromptTokens; completion_tokens=$CompletionTokens; total_tokens=$total;
  meta=$Meta
}
$json = ($payload | ConvertTo-Json -Depth 5 -Compress)
Add-Content -Path $file -Value $json -Encoding UTF8
Write-Output "Telemetry appended: $json"
