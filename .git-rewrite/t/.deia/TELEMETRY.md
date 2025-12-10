# Telemetry (Local, Opt-in)

Purpose: track per-agent activity (Queen/Drone/Worker) including durations and token usage, without changing core code.

Where data lives
- JSON Lines per agent: `.deia/bot-logs/<AGENT_ID>-activity.jsonl`
- Event schema:
  ```json
  {
    "ts": "2025-10-13T10:40:22Z",
    "agent_id": "BOT-00002",
    "role": "drone|queen|worker",
    "event": "heartbeat|task_start|task_done|log|worker_call",
    "message": "short note",
    "duration_ms": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "meta": {"task": "id-or-slug", "worker": "name", "status": "ok"}
  }
  ```

Helpers
- PowerShell: `.deia/tools/telemetry.ps1`
- POSIX: `.deia/tools/telemetry.sh`

Examples
```
# Queen logs session start
pwsh -c ".\\.deia\\tools\\telemetry.ps1 -AgentId BOT-00001 -Role queen -Event session_start -Message 'Queen coordinating'"

# Drone logs tokens for a response
bash ./.deia/tools/telemetry.sh BOT-00002 drone log "Answer ready" 120 480
```

Notes
- Tokens may come from your model response metadata; otherwise estimate.
- This is local-only. Share sanitized summaries if needed.
