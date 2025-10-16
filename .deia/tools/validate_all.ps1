$ErrorActionPreference='Stop'
$paths = @()
if (Test-Path '.projects') { $paths += (Get-ChildItem -Path .projects -Recurse -File -Include *.md -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match '\\(llhs|tag-teams|eggs)\\' } | Select-Object -ExpandProperty FullName) }
if (Test-Path '.deia/llhs') { $paths += (Get-ChildItem -Path .deia/llhs -File -Include *.md -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName) }
if (Test-Path '.deia/tag-teams') { $paths += (Get-ChildItem -Path .deia/tag-teams -File -Include *.md -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName) }
if (Test-Path '.deia/eggs') { $paths += (Get-ChildItem -Path .deia/eggs -File -Include *.md -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName) }
$paths = $paths | Select-Object -Unique
if (-not $paths -or $paths.Count -eq 0) { Write-Host 'No LLH/TAG/Egg files found.'; exit 0 }
$py = (Get-Command python -ErrorAction SilentlyContinue).Source; if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
& $py '.deia/tools/llh_validate.py' @paths

