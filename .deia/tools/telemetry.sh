#!/usr/bin/env bash
set -euo pipefail
AGENT_ID="${1:?agent id}"
ROLE="${2:?role: queen|drone|worker}"
EVENT="${3:?event}"
MESSAGE="${4:-}"
PROMPT_TOKENS="${5:-0}"
COMPLETION_TOKENS="${6:-0}"
DURATION_MS="${7:-0}"
shift $(( $# > 7 ? 7 : $# )) || true
TS="$(date -Iseconds --utc 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)"
LOG_DIR=".deia/bot-logs"
mkdir -p "$LOG_DIR"
FILE="$LOG_DIR/${AGENT_ID}-activity.jsonl"
TOTAL=$((PROMPT_TOKENS+COMPLETION_TOKENS))
META="{}"
printf '{"ts":"%s","agent_id":"%s","role":"%s","event":"%s","message":"%s","duration_ms":%s,"prompt_tokens":%s,"completion_tokens":%s,"total_tokens":%s,"meta":%s}\n' \
  "$TS" "$AGENT_ID" "$ROLE" "$EVENT" "$MESSAGE" "$DURATION_MS" "$PROMPT_TOKENS" "$COMPLETION_TOKENS" "$TOTAL" "$META" >> "$FILE"
echo "Telemetry appended to $FILE"
