#!/usr/bin/env bash
set -euo pipefail
BOT_ID="${1:-BOT-00002}"
shift || true
if [ "$#" -eq 0 ]; then
  echo "Usage: heartbeat.sh <BOT_ID> <message>" >&2
  exit 1
fi
MSG="$*"
TS="$(date -Iseconds)"
INSTR=".deia/instructions/${BOT_ID}-instructions.md"
echo "- ${TS} [${BOT_ID}] ${MSG}" >> "$INSTR"
echo "Heartbeat appended: ${TS} [${BOT_ID}] ${MSG}"