#!/usr/bin/env bash
set -euo pipefail

usage(){ echo "Usage: llh_hatch.sh -t llh|tag|egg -i id -T title [-o outdir] [--project name] [-f filename] [--force]"; exit 2; }

TYPE=""; ID=""; TITLE=""; OUTDIR=""; PROJECT="${LLH_PROJECT:-}"; FILENAME=""; FORCE=0

# Simple arg parser (short + a few long flags)
if [[ $# -eq 0 ]]; then usage; fi
while [[ $# -gt 0 ]]; do
  case "$1" in
    -t) TYPE="$2"; shift 2;;
    -i) ID="$2"; shift 2;;
    -T) TITLE="$2"; shift 2;;
    -o) OUTDIR="$2"; shift 2;;
    -f) FILENAME="$2"; shift 2;;
    --project) PROJECT="$2"; shift 2;;
    --force) FORCE=1; shift;;
    *) usage;;
  esac
done

[[ -z "$TYPE" || -z "$ID" || -z "$TITLE" ]] && usage

# Template discovery (prefer .deia/templates, fallback to legacy)
TPL=""
case "$TYPE" in
  llh)
    for c in ".deia/templates/llh/minimal-llh.md" "templates/llh/LLH-TEMPLATE.md"; do [[ -f "$c" ]] && TPL="$c" && break; done;;
  tag)
    for c in ".deia/templates/tag/minimal-tag.md" "templates/tag/TAG-TEMPLATE.md"; do [[ -f "$c" ]] && TPL="$c" && break; done;;
  egg)
    for c in ".deia/templates/egg/minimal-egg.md" "templates/egg/EGG-TEMPLATE.md"; do [[ -f "$c" ]] && TPL="$c" && break; done;;
  *) echo "Unknown type: $TYPE"; exit 1;;
 esac
[[ -z "${TPL}" ]] && echo "No template found" >&2 && exit 1

[[ "$TYPE" == "egg" && -z "${FILENAME}" ]] && FILENAME="${ID}.md"

# Canonical segmented output dirs if not provided
if [[ -z "${OUTDIR}" ]]; then
  [[ -z "$PROJECT" ]] && PROJECT="default"
  case "$TYPE" in
    llh) OUTDIR=".projects/${PROJECT}/llhs";;
    tag) OUTDIR=".projects/${PROJECT}/tag-teams";;
    egg) OUTDIR=".projects/${PROJECT}/eggs";;
  esac
fi
mkdir -p "$OUTDIR"
OUTFILE="$OUTDIR/${ID}.md"

if [[ -f "$OUTFILE" ]]; then echo "Refusing to overwrite $OUTFILE" >&2; exit 1; fi

# Large directory guard
COUNT=$(find "$OUTDIR" -maxdepth 1 -type f | wc -l | tr -d ' ')
if [[ "$COUNT" -gt 200 && $FORCE -ne 1 && "${LLH_HATCH_FORCE:-}" != "1" ]]; then
  echo "WARNING: TARGET DIRECTORY HAS $COUNT FILES — consider setting LLH_PROJECT or -o/--project to segment. Proceed? (yes/no)" >&2
  read -r resp3
  if [[ "$resp3" != "yes" ]]; then echo "Aborting due to large directory guard." >&2; exit 2; fi
fi

# HUMAN VALIDATION for Egg hatches unless forced
if [[ "$TYPE" == "egg" && $FORCE -ne 1 && "${LLH_HATCH_FORCE:-}" != "1" ]]; then
  echo "WARNING: EGG LAUNCH — This will create routed content on disk." >&2
  echo "  Target file: $OUTFILE" >&2
  echo "  Intended filename (routing): $FILENAME" >&2
  phrase="I UNDERSTAND THIS WILL CREATE CONTENT FOR $ID"
  echo "Type the exact phrase to proceed: \"$phrase\"" >&2
  read -r resp
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ"); mkdir -p .deia/telemetry
  if [[ "$resp" != "$phrase" ]]; then
    ev="{\"ts\":\"$ts\",\"type\":\"builder_confirm\",\"lane\":\"Process\",\"actor\":\"Whisperwing\",\"data\":{\"kind\":\"$TYPE\",\"id\":\"$ID\",\"status\":\"denied\"}}"
    echo "$ev" >> .deia/telemetry/rse.jsonl
    echo "Human validation failed; aborting. Use --force or LLH_HATCH_FORCE=1 to bypass." >&2
    exit 2
  else
    ev="{\"ts\":\"$ts\",\"type\":\"builder_confirm\",\"lane\":\"Process\",\"actor\":\"Whisperwing\",\"data\":{\"kind\":\"$TYPE\",\"id\":\"$ID\",\"status\":\"accepted\"}}"
    echo "$ev" >> .deia/telemetry/rse.jsonl
  fi
fi

NAME=$(echo "$ID" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%d")
ACTOR="claude-anthropic-bee-queen"

sed -e "s/{{ID}}/$ID/g" \
    -e "s/{{NAME}}/$NAME/g" \
    -e "s/{{DATE}}/$DATE/g" \
    -e "s/{{ACTOR}}/$ACTOR/g" \
    -e "s/{{ENTITY_TYPE}}/$TYPE/g" \
    "$TPL" > "$OUTFILE"

echo "? Hatched $TYPE: $OUTFILE"

# Validate
if [[ -f ".deia/tools/llh_validate.py" ]]; then
  echo "  Validating..."
  if python .deia/tools/llh_validate.py "$OUTFILE" > /dev/null 2>&1; then
    echo "  ? Validation passed"
  else
    echo "  ! Validation failed (file created but may need manual fixes)"
  fi
fi

# Log to RSE
RSE_EVENT="{\"ts\":\"$DATE\",\"event\":\"${TYPE}_hatched\",\"actor\":\"$ACTOR\",\"target\":\"$ID\",\"note\":\"Builder v0.2\"}"
echo "$RSE_EVENT" >> .deia/telemetry/rse.jsonl