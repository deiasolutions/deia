# DEIA Hive Protocol (LLM-agnostic)

For new drones, start here: `instructions/00-STARTUP-INSTRUCTIONS.md`
Quick boot summary: `.deia/DRONE-START.md`

- Single source of truth under `.deia/`.
- Any agent (Claude, Codex) can read/write these files and run the CLI.

## Files
- `.deia/hive-recipe.json` — Queen + Drones definition (UTF-8, no BOM)
- `.deia/instructions/BOT-0000X-instructions.md` — Auto-generated per bot
- `.deia/handoffs/*.md` — Handoff docs per task
- `.deia/reports/*` — Optional status mirrors
 
Telemetry & Workers
- `.deia/bot-logs/` — Activity and telemetry JSONL per agent (Queen/Drone/Worker)
- `.deia/tools/telemetry.ps1|.sh` — Append telemetry events (tokens, durations)
- `.deia/tools/worker-log.ps1|.sh` — Log worker (.py) invocations and counts

## Heartbeat Format
- `- 2025-10-13T10:32Z [<instance-id>] <short status>`

## Workflow
1) Launch hive (no queen registration):
   `deia hive launch .deia/hive-recipe.json --no-queen`
2) Queen updates "Current Task" in each drone instruction file
3) Drone appends heartbeats and produces a handoff doc, linking it back
4) Queen reviews handoff and assigns next task

## Logging (optional)
- `deia log --from-file <transcript>` → `.deia/sessions/`
