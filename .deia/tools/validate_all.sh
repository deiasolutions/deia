#!/usr/bin/env bash
set -euo pipefail

FILES=()
while IFS= read -r -d '' f; do FILES+=("$f"); done < <(find .projects -type f \( -path '*/llhs/*' -o -path '*/tag-teams/*' -o -path '*/eggs/*' \) -name '*.md' -print0 2>/dev/null || true)
[[ -d .deia/llhs ]] && while IFS= read -r -d '' f; do FILES+=("$f"); done < <(find .deia/llhs -type f -name '*.md' -print0 2>/dev/null || true)
[[ -d .deia/tag-teams ]] && while IFS= read -r -d '' f; do FILES+=("$f"); done < <(find .deia/tag-teams -type f -name '*.md' -print0 2>/dev/null || true)
[[ -d .deia/eggs ]] && while IFS= read -r -d '' f; do FILES+=("$f"); done < <(find .deia/eggs -type f -name '*.md' -print0 2>/dev/null || true)

if [[ ${#FILES[@]} -eq 0 ]]; then echo 'No LLH/TAG/Egg files found.'; exit 0; fi

PY=python; command -v "$PY" >/dev/null 2>&1 || PY=py
"$PY" .deia/tools/llh_validate.py "${FILES[@]}"

