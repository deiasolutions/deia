param(
  [Parameter(Mandatory=$true)][string]$EggPath,
  [Parameter(Mandatory=$true)][ValidateSet('llh','tag','egg')][string]$Type,
  [Parameter(Mandatory=$true)][string]$Id,
  [Parameter(Mandatory=$true)][string]$Title,
  [string]$Project,
  [string]$Filename,
  [switch]$Force
)
$ErrorActionPreference='Stop'
# 1) Expand egg (Rule 3 — work on a copy)
& (Join-Path '.deia/tools' 'egg_expand.ps1') -Path $EggPath | Out-Null
# 2) Hatch entity into segmented project
$args = @('-Type', $Type, '-Id', $Id, '-Title', $Title)
if ($Project) { $args += @('-Project', $Project) }
if ($Filename) { $args += @('-Filename', $Filename) }
if ($Force) { $args += @('-Force') }
& (Join-Path '.deia/tools' 'llh_hatch.ps1') @args
# 3) Validate
& python '.deia/tools/llh_validate.py' (".projects/{0}/{1}/{2}.md" -f ($Project ? $Project : 'default'), ($Type -eq 'llh' ? 'llhs' : ($Type -eq 'tag' ? 'tag-teams' : 'eggs')), $Id) 2>$null | Out-Null
# Log
$evt = [PSCustomObject]@{ ts=(Get-Date).ToUniversalTime().ToString('o'); type='builder_launch'; lane='Process'; actor='Whisperwing'; data=@{ egg=$EggPath; type=$Type; id=$Id; project=($Project ? $Project : 'default') } } | ConvertTo-Json -Compress
$teleDir = '.deia/telemetry'; if (!(Test-Path $teleDir)) { New-Item -ItemType Directory -Path $teleDir | Out-Null }
Add-Content -Path (Join-Path $teleDir 'rse.jsonl') -Value $evt

