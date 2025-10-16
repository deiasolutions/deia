#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 8 ]]; then
  echo "Usage: builder_launch.sh --egg <egg.md> --type llh|tag|egg --id <id> --title <title> [--project name] [--filename name] [--force]" >&2
  exit 2
fi

EGG=""; TYPE=""; ID=""; TITLE=""; PROJECT="${LLH_PROJECT:-}"; FILENAME=""; FORCE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --egg) EGG="$2"; shift 2;;
    --type) TYPE="$2"; shift 2;;
    --id) ID="$2"; shift 2;;
    --title) TITLE="$2"; shift 2;;
    --project) PROJECT="$2"; shift 2;;
    --filename) FILENAME="$2"; shift 2;;
    --force) FORCE=1; shift;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

# 1) Expand egg
.deia/tools/egg_expand.sh "$EGG" >/dev/null

# 2) Hatch
CMD=(.deia/tools/llh_hatch.sh -t "$TYPE" -i "$ID" -T "$TITLE")
[[ -n "$PROJECT" ]] && CMD+=(--project "$PROJECT")
[[ -n "$FILENAME" ]] && CMD+=(-f "$FILENAME")
[[ "$FORCE" -eq 1 ]] && CMD+=(--force)
"${CMD[@]}"

# 3) Validate
KIND_DIR=$([[ "$TYPE" == "llh" ]] && echo 'llhs' || ([[ "$TYPE" == "tag" ]] && echo 'tag-teams' || echo 'eggs'))
python .deia/tools/llh_validate.py ".projects/${PROJECT:-default}/${KIND_DIR}/${ID}.md" >/dev/null 2>&1 || true

# Log
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EV="{\"ts\":\"$TS\",\"type\":\"builder_launch\",\"lane\":\"Process\",\"actor\":\"Whisperwing\",\"data\":{\"egg\":\"$EGG\",\"type\":\"$TYPE\",\"id\":\"$ID\",\"project\":\"${PROJECT:-default}\"}}"
mkdir -p .deia/telemetry
echo "$EV" >> .deia/telemetry/rse.jsonl

echo "✓ Launch complete for $TYPE: $ID (project ${PROJECT:-default})"

