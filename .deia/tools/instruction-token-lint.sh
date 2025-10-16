#!/usr/bin/env bash
set -euo pipefail

THRESHOLD=${1:-800}
shift || true

# Default search path if none provided
if [ "$#" -eq 0 ]; then
  set -- .deia/instructions/*-instructions.md
fi

files=()
for p in "$@"; do
  for f in $p; do
    [ -f "$f" ] && files+=("$f") || true
  done
done

if [ ${#files[@]} -eq 0 ]; then
  echo "No files matched patterns: $*"
  exit 0
fi

printf '%-80s %8s %8s %6s\n' "File" "Tokens" "Chars" "Status"
printf '%-80s %8s %8s %6s\n' "------------------------------------------------------------" "-------" "-----" "------"

over=0
count=0
for f in "${files[@]}"; do
  # approximate tokens by word count
  TOKENS=$(tr -s '[:space:]' ' ' < "$f" | wc -w | awk '{print $1}')
  CHARS=$(wc -c < "$f" | awk '{print $1}')
  STATUS="OK"
  if [ "$TOKENS" -gt "$THRESHOLD" ]; then STATUS="WARN"; over=$((over+1)); fi
  printf '%-80s %8s %8s %6s\n' "$f" "$TOKENS" "$CHARS" "$STATUS"
  count=$((count+1))
done

echo
echo "Files: $count; Over threshold: $over (>$THRESHOLD tokens)"

exit 0

