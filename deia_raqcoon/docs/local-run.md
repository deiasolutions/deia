# Local Run (Portable by Design)

## Local First
Run all services locally with file-based coordination and SQLite storage.

## Hosting Ready
All host-specific settings are isolated to config and runtime bindings:
- Host: 127.0.0.1 (local) or 0.0.0.0 (hosted)
- Storage: SQLite by default, swap to Postgres later
- UI: served locally or as a static build

## Planned Entrypoints
- `runtime/server.py` for API + WebSocket
- `runtime/worker.py` for lane execution (terminal, local LLM)

## Quick Start (Local)
From repo root:
```
python deia_raqcoon/runtime/run_server.py
```

## CLI Bee Commands (Optional Overrides)
Use env vars to point to custom CLI commands:
- `DEIA_CLAUDE_CMD` (default: `claude`)
- `DEIA_CLAUDE_ARGS` (default: empty)
- `DEIA_CODEX_CMD` (default: `codex`)
- `DEIA_CODEX_ARGS` (default: empty)

Default URL:
- http://127.0.0.1:8010
