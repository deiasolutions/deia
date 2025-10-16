# Worker Protocol (Python helpers)

Workers are lightweight Python scripts for small tasks (no LLM tokens).
They can read an `.md` instruction to perform multi-step actions.

Counting and logging
- Every invocation should be logged and counted.
- Log JSONL to `.deia/bot-logs/worker-usage.jsonl` with fields:
  - `ts`, `worker`, `args`, `invoker` (queen/drone id), `result` (ok|fail)
- Maintain an aggregate count in `.deia/reports/worker-usage.json`.

Helpers
- PowerShell: `.deia/tools/worker-log.ps1`
- POSIX: `.deia/tools/worker-log.sh`

Example
```
# Log a run from Drone-Dev
pwsh -c ".\\.deia\\tools\\worker-log.ps1 -Worker cleanup_paths -Invoker BOT-00002 -Args 'src/**/*.py' -Result ok"

# POSIX
bash ./.deia/tools/worker-log.sh cleanup_paths BOT-00002 ok "src/**/*.py"
```

Complex tasks via markdown
- Place an instruction file under `.deia/working/workers/<name>.md` describing steps.
- Workers read the `.md` and execute the checklist.
- Link worker runs in handoffs and instruction files, including counts.
