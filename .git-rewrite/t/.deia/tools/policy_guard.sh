#!/usr/bin/env bash
set -euo pipefail

# Guard for ROTG-2 do-not-erase policy within .deia local commons
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCK_FILE="${SCRIPT_DIR}/../ROTG-2-RESPECT-DO-NOT-ERASE.lock"

if [[ -f "${LOCK_FILE}" ]]; then
  echo "ROTG-2 lock active: edits to '.deia' are prohibited. Respect do-not-erase." 1>&2
  exit 3
fi

echo "No active ROTG-2 locks detected."
exit 0

