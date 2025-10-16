#!/usr/bin/env bash
set -euo pipefail

EGG_PATH=${1:-}
if [[ -z "$EGG_PATH" ]]; then
  echo "Usage: egg_expand.sh <egg.md>" >&2; exit 2
fi
PY=python
command -v "$PY" >/dev/null 2>&1 || PY=py
"$PY" .deia/tools/egg_expand.py "$EGG_PATH"

