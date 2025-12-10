param(
  [Parameter(Mandatory=$true)][ValidateSet('llh','tag','egg')]$Type,
  [Parameter(Mandatory=$true)][string]$Id,
  [Parameter(Mandatory=$true)][string]$Title,
  [string]$OutDir,
  [string]$Filename,
  [switch]$Force,
  [string]$Project
)
$ErrorActionPreference='Stop'
$root = (Get-Location)
$candidates = @()
switch ($Type) {
  'llh' { $candidates = @('.deia/templates/llh/minimal-llh.md','templates/llh/LLH-TEMPLATE.md') }
  'tag' { $candidates = @('.deia/templates/tag/minimal-tag.md','templates/tag/TAG-TEMPLATE.md') }
  'egg' { $candidates = @('.deia/templates/egg/minimal-egg.md','templates/egg/EGG-TEMPLATE.md') }
}
$tplPath = $null
foreach ($rel in $candidates) {
  $p = Join-Path $root $rel
  if (Test-Path $p) { $tplPath = $p; break }
}
if (-not $tplPath) { Write-Error ("Template not found in candidates: {0}" -f ($candidates -join ', ')) }
# Canonical output dirs; prefer project segmentation under .projects/<project>
if (-not $OutDir -or [string]::IsNullOrWhiteSpace($OutDir)) {
  $segRoot = '.projects'
  if (-not $Project -or [string]::IsNullOrWhiteSpace($Project)) { $Project = 'default' }
  switch ($Type) {
    'llh' { $OutDir = (Join-Path (Join-Path $segRoot $Project) 'llhs') }
    'tag' { $OutDir = (Join-Path (Join-Path $segRoot $Project) 'tag-teams') }
    'egg' { $OutDir = (Join-Path (Join-Path $segRoot $Project) 'eggs') }
  }
}
$outDirAbs = Join-Path $root $OutDir
New-Item -ItemType Directory -Force -Path $outDirAbs | Out-Null
$date = (Get-Date).ToString('yyyy-MM-dd')
$content = Get-Content -Path $tplPath -Raw
if ($Type -eq 'egg' -and [string]::IsNullOrWhiteSpace($Filename)) { $Filename = "$Id.md" }
$out = $content.Replace('{{ID}}',$Id).Replace('{{TITLE}}',$Title).Replace('{{DATE}}',$date).Replace('{{FILENAME}}',$Filename)
$outFile = Join-Path $outDirAbs ("$Id.md")
if (Test-Path $outFile) { Write-Error "Refusing to overwrite existing file: $outFile" }

# HUMAN VALIDATION for Egg hatches (safety): require explicit confirmation unless forced
if ($Type -eq 'egg' -and -not $Force -and $env:LLH_HATCH_FORCE -ne '1') {
  Write-Warning "EGG LAUNCH WARNING: This will create routed content (Egg) on disk."
  Write-Host    ("  Target file: {0}" -f $outFile)
  Write-Host    ("  Intended filename (routing): {0}" -f $Filename)
  $phrase = "I UNDERSTAND THIS WILL CREATE CONTENT FOR $Id"
  Write-Host ("Type the exact phrase to proceed: `"{0}`"" -f $phrase) -ForegroundColor Yellow
  $resp = Read-Host 'Confirm phrase'
  if ($resp -ne $phrase) {
    $evt = [PSCustomObject]@{ ts=(Get-Date).ToUniversalTime().ToString('o'); type='builder_confirm'; lane='Process'; actor='Whisperwing'; data=@{ kind=$Type; id=$Id; status='denied' } } | ConvertTo-Json -Compress
    $teleDir = '.deia/telemetry'; if (!(Test-Path $teleDir)) { New-Item -ItemType Directory -Path $teleDir | Out-Null }
    Add-Content -Path (Join-Path $teleDir 'rse.jsonl') -Value $evt
    Write-Error "Human validation failed. Aborting Egg hatch. Use -Force or set LLH_HATCH_FORCE=1 to bypass."
  }
  else {
    $evt = [PSCustomObject]@{ ts=(Get-Date).ToUniversalTime().ToString('o'); type='builder_confirm'; lane='Process'; actor='Whisperwing'; data=@{ kind=$Type; id=$Id; status='accepted' } } | ConvertTo-Json -Compress
    $teleDir = '.deia/telemetry'; if (!(Test-Path $teleDir)) { New-Item -ItemType Directory -Path $teleDir | Out-Null }
    Add-Content -Path (Join-Path $teleDir 'rse.jsonl') -Value $evt
  }
}
Set-Content -Path $outFile -Value $out -Encoding UTF8
# Log RSE
$evt = [PSCustomObject]@{ ts=(Get-Date).ToUniversalTime().ToString('o'); type='builder_done'; lane='Process'; actor='Whisperwing'; data=@{ kind=$Type; id=$Id; path=$outFile } } | ConvertTo-Json -Compress
$teleDir = '.deia/telemetry'; if (!(Test-Path $teleDir)) { New-Item -ItemType Directory -Path $teleDir | Out-Null }
Add-Content -Path (Join-Path $teleDir 'rse.jsonl') -Value $evt
Write-Host "Hatched: $outFile"
# Directory size guard: warn/confirm if target dir is very large
try {
  $fileCount = (Get-ChildItem -Path $outDirAbs -File -ErrorAction SilentlyContinue | Measure-Object).Count
} catch { $fileCount = 0 }
if ($fileCount -gt 200 -and -not $Force -and $env:LLH_HATCH_FORCE -ne '1') {
  Write-Warning ("TARGET DIRECTORY HAS {0} FILES — consider setting -Project to segment under .projects/<project>." -f $fileCount)
  $resp2 = Read-Host 'Proceed anyway? (yes/no)'
  if ($resp2 -ne 'yes') { Write-Error 'Aborting due to large directory guard.' }
}

# Preconditions: if Project is set, ensure an egg workspace exists (egg.md under the project tree)
if ($Project -and -not $Force -and $env:LLH_HATCH_FORCE -ne '1') {
  $projRoot = Join-Path $root (Join-Path '.projects' $Project)
  $hasEgg = $false
  if (Test-Path (Join-Path $projRoot 'egg.md')) { $hasEgg = $true }
  else {
    try {
      $eggs = Get-ChildItem -Path $projRoot -Filter 'egg.md' -Recurse -Depth 2 -ErrorAction SilentlyContinue
      if ($eggs -and $eggs.Count -gt 0) { $hasEgg = $true }
    } catch {}
  }
  if (-not $hasEgg) {
    Write-Warning "No egg.md found under .projects/$Project/. Please expand an egg first (Rule 3) or confirm to proceed."
    $resp3 = Read-Host 'Proceed without egg workspace? (yes/no)'
    if ($resp3 -ne 'yes') { Write-Error 'Aborting due to missing egg workspace.' }
  }
}
