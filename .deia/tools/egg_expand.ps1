param(
  [Parameter(Mandatory=$true)][string]$Path
)
$ErrorActionPreference='Stop'
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $py) { Write-Error 'Python not found' }
& $py '.deia/tools/egg_expand.py' $Path

