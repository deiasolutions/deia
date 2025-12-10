param(
  [int]$Threshold = 800,
  [string[]]$Paths = @('.deia/instructions/*-instructions.md'),
  [string]$JsonReport = ''
)

function Get-TokenCount([string]$text) {
  if ([string]::IsNullOrWhiteSpace($text)) { return 0 }
  return ($text -split "\s+").Count
}

$files = @()
foreach ($pattern in $Paths) {
  $files += Get-ChildItem -Path $pattern -File -ErrorAction SilentlyContinue
}

if (-not $files) {
  Write-Output "No files matched patterns: $($Paths -join ', ')"
  exit 0
}

$results = @()
foreach ($f in $files) {
  $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
  $tokens = Get-TokenCount $content
  $chars = ($content).Length
  $status = if ($tokens -gt $Threshold) { 'WARN' } else { 'OK' }
  $results += [pscustomobject]@{ File=$f.FullName; Tokens=$tokens; Chars=$chars; Threshold=$Threshold; Status=$status }
}

# Output table
$fmt = '{0,-80} {1,8} {2,8} {3,6}'
Write-Output ($fmt -f 'File','Tokens','Chars','Status')
Write-Output ($fmt -f ('-'*60),'-------','-----','------')
foreach ($r in $results) {
  Write-Output ($fmt -f $r.File, $r.Tokens, $r.Chars, $r.Status)
}

$over = ($results | Where-Object { $_.Tokens -gt $Threshold }).Count
Write-Output "`nFiles: $($results.Count); Over threshold: $over (>$Threshold tokens)"

if ($JsonReport) {
  $dir = Split-Path -Parent $JsonReport
  if ($dir) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  ($results | ConvertTo-Json -Depth 5) | Set-Content -Path $JsonReport -Encoding UTF8
  Write-Output "JSON report written: $JsonReport"
}

exit 0

