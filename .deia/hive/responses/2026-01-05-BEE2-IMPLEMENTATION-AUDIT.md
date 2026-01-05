# BEE2: Implementation Audit Report

**Auditor**: BEE-002 (Claude Instance 2)
**Date**: 2026-01-05
**Status**: Complete

---

## 1. Endpoint Inventory

Every route in `runtime/server.py`:

| Method | Path | Handler | Request Model | What It Does |
|--------|------|---------|---------------|--------------|
| GET | /api/health | `health()` | None | Returns `{"status": "ok"}` |
| GET | /api/config | `config()` | None | Returns cwd, repo_root, repo_status from preflight check |
| POST | /api/bees/launch | `launch_bee()` | `LaunchRequest` | Launches CLI tool (claude-code/codex) in new console at repo root |
| POST | /api/pty/start | `start_pty()` | `PTYStartRequest` | Starts PTY session with CLI tool |
| POST | /api/pty/send | `send_pty()` | `PTYSendRequest` | Sends data to PTY session |
| GET | /api/pty/read | `read_pty()` | Query: session_id, max_chars | Reads output from PTY session buffer |
| POST | /api/pty/stop | `stop_pty()` | `PTYStopRequest` | Stops PTY session |
| POST | /api/messages | `post_message()` | `MessageRequest` | Adds message to MessageStore |
| GET | /api/messages | `get_messages()` | Query: channel_id | Retrieves messages, optionally filtered by channel |
| GET | /api/summary | `get_summary()` | None | Returns message summary (counts, tokens, by provider/lane) |
| GET | /api/channels | `get_channels()` | None | Returns unique channel IDs from messages |
| GET | /api/kb/entities | `get_kb_entities()` | None | Lists all KB entities from kb.json |
| POST | /api/kb/entities | `create_kb_entity()` | `KBEntityRequest` | Creates/upserts KB entity |
| PUT | /api/kb/entities/{entity_id} | `update_kb_entity()` | `KBEntityRequest` | Updates KB entity by ID |
| POST | /api/kb/preview | `kb_preview()` | `KBPreviewRequest` | Returns formatted preview of KB entities |
| POST | /api/tasks | `create_task()` | `TaskRequest` | Writes task JSON file to `.deia/hive/tasks/{bot_id}/` |
| POST | /api/tasks/complete | `complete_task_endpoint()` | `TaskCompleteRequest` | Archives completed task |
| GET | /api/tasks/response | `get_latest_response()` | Query: task_id, repo_root | Gets latest response file path |
| GET | /api/git/status | `git_status()` | Query: repo_root | Runs `git status -sb` |
| GET | /api/gates | `get_gates()` | None | Returns current gate flags |
| POST | /api/gates | `update_gates()` | `GatesUpdateRequest` | Updates gate flags |
| POST | /api/git/commit | `git_commit()` | `GitCommitRequest` | Runs `git commit -am` (gate-protected) |
| POST | /api/git/push | `git_push()` | `GitPushRequest` | Runs `git push` (gate-protected) |
| POST | /api/flights/start | `start_flight()` | `FlightStartRequest` | Starts flight tracking session |
| POST | /api/flights/end | `end_flight()` | `FlightEndRequest` | Ends flight tracking session |
| POST | /api/flights/recap | `add_flight_recap()` | `FlightRecapRequest` | Adds recap text to flight |
| GET | /api/flights | `list_flights()` | None | Lists all flights |
| GET | /api/flights/recaps | `list_recaps()` | Query: flight_id | Lists recaps, optionally filtered by flight |
| WebSocket | /api/ws | `websocket_endpoint()` | N/A | Echo websocket (receives text, sends back same text) |

**Total Endpoints: 27** (26 REST + 1 WebSocket)

---

## 2. Module Function Map

### core/__init__.py
- Empty docstring only: `"""Core package."""`
- **Called by**: N/A (package marker)

### core/router.py
- `RouteDecision` (dataclass): Fields: `lane`, `provider`, `delivery`
- `decide_route(task: Dict) -> RouteDecision`: Returns routing decision based on intent
  - "design"/"planning" -> lane=llm, provider=default, delivery=cache_prompt
  - "code" -> lane=terminal, provider=cli, delivery=task_file
  - else -> lane=llm, provider=default, delivery=cache_prompt
- **Called by**: **UNUSED** - not imported anywhere in server.py or other modules

### core/task_files.py
- `_timestamp() -> str`: Returns formatted timestamp `%Y-%m-%d-%H%M%S`
- `task_dir(repo_root, bot_id) -> Path`: Returns `.deia/hive/tasks/{bot_id}`
- `response_dir(repo_root) -> Path`: Returns `.deia/hive/responses`
- `archive_dir(repo_root, bot_id=None) -> Path`: Returns `.deia/hive/archive[/bot_id]`
- `_infer_bot_id(task_path) -> Optional[str]`: Extracts bot_id from task path
- `write_task(repo_root, bot_id, payload) -> Path`: Creates task JSON file
- `complete_task(repo_root, task_path, completion_note=None) -> Optional[Path]`: Marks task complete, moves to archive
- `latest_response(repo_root, task_id=None) -> Optional[Path]`: Finds latest response .md file
- **Called by**: server.py imports `complete_task`, `latest_response`, `write_task`

### adapters/__init__.py
- Empty docstring only: `"""Adapter package."""`
- **Called by**: N/A (package marker)

### adapters/base.py
- `AdapterResult` (dataclass): Fields: `success`, `output`, `metadata` (optional)
- `BaseAdapter` (class): Base class with `name = "base"` and abstract `send(payload)` method
- **Called by**: cli_adapter.py imports `AdapterResult`

### adapters/cli_adapter.py
- `CLILaunchResult` (dataclass): Fields: `success`, `pid`, `error` (optional)
- `CLIAdapter` (class):
  - `__init__(executable, args=None, new_console=True)`: Initializes adapter
  - `_resolve_executable() -> Optional[str]`: Resolves executable path (checks PATH via `which`)
  - `launch(repo_root, env=None) -> CLILaunchResult`: Spawns subprocess in new console
  - `send(payload) -> AdapterResult`: Returns failure (CLI doesn't send directly)
- **Called by**: registry.py imports `CLIAdapter`

### adapters/registry.py
- `get_cli_adapter(tool: str) -> CLIAdapter`: Factory for CLI adapters
  - "claude-code" -> uses DEIA_CLAUDE_CMD env var (default: "claude")
  - "codex" -> uses DEIA_CODEX_CMD env var (default: "codex")
  - else -> uses tool name directly
- `get_cli_command(tool: str) -> list[str]`: Returns command list for PTY
  - Same logic as get_cli_adapter but returns list instead of adapter
- **Called by**: server.py imports `get_cli_adapter`, `get_cli_command`

### kb/__init__.py
- Empty docstring only: `"""Knowledge base package."""`
- **Called by**: N/A (package marker)

### kb/store.py
- `KB_PATH`: Constant `Path(__file__).parent / "kb.json"`
- `ALLOWED_TYPES`: `{"RULE", "SNIPPET"}`
- `ALLOWED_DELIVERY`: `{"cache_prompt", "task_file", "both"}`
- `load_entities() -> List[Dict]`: Reads kb.json
- `save_entities(entities) -> None`: Writes kb.json
- `upsert_entity(entity) -> Dict`: Creates/updates entity with validation
- `list_entities() -> List[Dict]`: Returns all entities
- `preview_injection(entity_ids) -> str`: Formats selected entities for injection
- **Called by**: server.py imports `list_entities`, `preview_injection`, `upsert_entity`

### runtime/__init__.py
- Empty docstring only: `"""Runtime package."""`
- **Called by**: N/A (package marker)

### runtime/server.py
- Main FastAPI application
- See Endpoint Inventory above for all handlers
- **Called by**: run_server.py references `deia_raqcoon.runtime.server:app`

### runtime/launcher.py
- `RepoPreflight` (dataclass): Fields: `status`, `message`, `repo_root` (optional), `cwd` (optional)
- `is_repo_root(path) -> bool`: Checks if `.deia` directory exists
- `find_repo_root(start) -> Optional[Path]`: Walks up to find nearest repo root
- `preflight_repo_root(cwd) -> RepoPreflight`: Returns status: "ok", "prompt", or "error"
- **Called by**: server.py imports `preflight_repo_root`

### runtime/flights.py
- `FlightStore` (class): SQLite-backed flight/recap storage
  - `__init__(db_path=None)`: Creates `.deia/raqcoon_flights.db`
  - `_init_schema()`: Creates `flights` and `recaps` tables
  - `start_flight(flight_id, title) -> Dict`: INSERT OR REPLACE flight
  - `end_flight(flight_id) -> Dict`: Updates ended_at timestamp
  - `add_recap(flight_id, recap_text) -> Dict`: INSERTs recap
  - `list_flights() -> List[Dict]`: SELECT all flights
  - `list_recaps(flight_id=None) -> List[Dict]`: SELECT recaps
- **Called by**: server.py imports `FlightStore`

### runtime/minder.py
- `run_minder(api_base, channel_id, interval_seconds, author, message) -> None`: Infinite loop POSTing pings to /api/messages
- Has `if __name__ == "__main__"` block for direct execution
- **Called by**: **UNUSED** - standalone script only

### runtime/store.py
- `MessageStore` (class): SQLite-backed message storage
  - `__init__(db_path=None)`: Creates `.deia/raqcoon_messages.db`
  - `_init_schema()`: Creates `messages` table with indexes
  - `_ensure_columns(columns)`: Migration helper for schema evolution
  - `add_message(channel_id, author, content, lane, provider, token_count) -> Dict`: INSERTs message
  - `get_messages(channel_id=None, limit=200) -> List[Dict]`: SELECT messages
  - `get_summary() -> Dict`: Aggregate stats (total, by_provider, by_lane)
- **Called by**: server.py imports `MessageStore`

### runtime/pty_bridge.py
- `PTYSession` (dataclass): Fields: `session_id`, `process`, `buffer`, `lock`, `alive`
  - `append_output(data)`: Thread-safe buffer append
  - `read_buffer(max_chars=4000) -> str`: Thread-safe buffer read with truncation
- `PTYBridge` (class):
  - `__init__()`: Initializes sessions dict
  - `start(command, cwd, env) -> PTYSession`: Spawns winpty process, starts reader thread
  - `_reader_loop(session)`: Background thread reading from PTY
  - `send(session_id, data) -> bool`: Writes to PTY
  - `read(session_id, max_chars) -> str`: Reads from buffer
  - `stop(session_id) -> bool`: Terminates PTY session
- **Called by**: server.py imports `PTYBridge`

### runtime/run_server.py
- Entry point script to run uvicorn server on 127.0.0.1:8010
- **Called by**: Direct execution (`python run_server.py`)

### deia_raqcoon/__init__.py
- Empty docstring only: `"""DEIA RAQCOON package."""`
- **Called by**: N/A (package marker)

---

## 3. Import Graph

```
server.py
├── adapters.registry
│   ├── get_cli_adapter
│   └── get_cli_command
├── kb.store
│   ├── list_entities
│   ├── preview_injection
│   └── upsert_entity
├── runtime.launcher
│   └── preflight_repo_root
├── core.task_files
│   ├── complete_task
│   ├── latest_response
│   └── write_task
├── runtime.store
│   └── MessageStore
├── runtime.flights
│   └── FlightStore
└── runtime.pty_bridge
    └── PTYBridge

adapters/registry.py
└── adapters.cli_adapter
    └── CLIAdapter

adapters/cli_adapter.py
└── adapters.base
    └── AdapterResult

runtime/minder.py
└── requests (external)
    └── POST to /api/messages

runtime/pty_bridge.py
└── winpty (external)
    └── PtyProcess
```

---

## 4. Stub/Placeholder Detection

| Function | File | Why It's a Stub |
|----------|------|-----------------|
| `decide_route` | core/router.py | Only handles 3 intent cases (design/planning, code, default). No KB lookup, no dynamic routing based on context. Comment says "Simple routing stub to be expanded." |
| `websocket_endpoint` | server.py | Echo-only websocket - receives text and sends it back unchanged. No real message routing/broadcasting logic. |
| `BaseAdapter.send` | adapters/base.py | Raises NotImplementedError - abstract method template only |
| `CLIAdapter.send` | adapters/cli_adapter.py | Always returns failure with message "CLI adapter does not send messages directly" |

---

## 5. Dead/Orphaned Code

| Function/Class | File | Notes |
|----------------|------|-------|
| `RouteDecision` | core/router.py | Defined but `decide_route` is never called |
| `decide_route` | core/router.py | **NEVER IMPORTED** - not used anywhere in server.py |
| `run_minder` | runtime/minder.py | Standalone script only - not integrated into server |
| `BaseAdapter` | adapters/base.py | Abstract base class never subclassed meaningfully (CLIAdapter doesn't inherit) |
| `AdapterResult` | adapters/base.py | Only used in CLIAdapter.send() which always fails |
| `task_dir` | core/task_files.py | Defined but `write_task` reimplements the same logic inline |
| `response_dir` | core/task_files.py | Only used by `latest_response` |
| `archive_dir` | core/task_files.py | Only used by `complete_task` |
| `_infer_bot_id` | core/task_files.py | Only used internally by `complete_task` |

---

## 6. Configuration

| Variable | Default | Used In |
|----------|---------|---------|
| `DEIA_CLAUDE_CMD` | `"claude"` | registry.py (get_cli_adapter, get_cli_command) |
| `DEIA_CLAUDE_ARGS` | `""` | registry.py (get_cli_adapter, get_cli_command) |
| `DEIA_CODEX_CMD` | `"codex"` | registry.py (get_cli_adapter, get_cli_command) |
| `DEIA_CODEX_ARGS` | `""` | registry.py (get_cli_adapter, get_cli_command) |

**Hardcoded Configuration:**
| Value | Location | Purpose |
|-------|----------|---------|
| `127.0.0.1:8010` | run_server.py | Server host:port |
| `http://127.0.0.1:8010` | minder.py | Default API base URL |
| `600` (seconds) | minder.py | Default minder ping interval |
| `200` | store.py | Default message fetch limit |
| `4000` | pty_bridge.py, server.py | Default PTY read max_chars |

---

## 7. Data Models (Pydantic)

All request/response models in server.py:

| Model | Fields | Used By |
|-------|--------|---------|
| `LaunchRequest` | `tool: str`, `cwd: Optional[str]`, `confirm: bool` | POST /api/bees/launch |
| `PTYStartRequest` | `tool: str`, `repo_root: str` | POST /api/pty/start |
| `PTYSendRequest` | `session_id: str`, `data: str` | POST /api/pty/send |
| `PTYStopRequest` | `session_id: str` | POST /api/pty/stop |
| `MessageRequest` | `channel_id: str`, `author: str`, `content: str`, `lane: Optional[str]`, `provider: Optional[str]`, `token_count: Optional[int]` | POST /api/messages |
| `TaskRequest` | `bot_id: str`, `task_id: Optional[str]`, `intent: str`, `title: str`, `summary: str`, `kb_entities: List[str]`, `delivery_mode: str`, `repo_root: Optional[str]` | POST /api/tasks |
| `TaskCompleteRequest` | `path: str`, `repo_root: Optional[str]`, `completion_note: Optional[str]` | POST /api/tasks/complete |
| `GitCommitRequest` | `repo_root: Optional[str]`, `message: str` | POST /api/git/commit |
| `GitPushRequest` | `repo_root: Optional[str]`, `remote: str`, `branch: Optional[str]` | POST /api/git/push |
| `GatesUpdateRequest` | `allow_q33n_git: Optional[bool]`, `pre_sprint_review: Optional[bool]`, `allow_flight_commits: Optional[bool]` | POST /api/gates |
| `KBEntityRequest` | `id: str`, `type: str`, `title: str`, `summary: str`, `tags: List[str]`, `delivery_mode: str`, `load_mode: str`, `attachments: Optional[List[str]]` | POST/PUT /api/kb/entities |
| `KBPreviewRequest` | `entity_ids: List[str]` | POST /api/kb/preview |
| `FlightStartRequest` | `flight_id: str`, `title: str` | POST /api/flights/start |
| `FlightEndRequest` | `flight_id: str` | POST /api/flights/end |
| `FlightRecapRequest` | `flight_id: str`, `recap_text: str` | POST /api/flights/recap |

---

## 8. Global State

Singletons and module-level state:

| Variable | Type | Purpose |
|----------|------|---------|
| `app` | `FastAPI` | Main application instance |
| `_message_store` | `MessageStore` | In-memory + SQLite message storage |
| `_flight_store` | `FlightStore` | In-memory + SQLite flight/recap storage |
| `_pty_bridge` | `PTYBridge` | PTY session manager (dict of sessions) |
| `_gates` | `Dict` | Feature gates for git operations |
| `KB_PATH` | `Path` | Path to kb.json (in kb/store.py) |
| `ALLOWED_TYPES` | `set` | Valid KB entity types |
| `ALLOWED_DELIVERY` | `set` | Valid delivery modes |

**Gate Flags (default all False):**
- `allow_q33n_git`: Must be True to allow git commit/push
- `pre_sprint_review`: Must be True to allow git commit
- `allow_flight_commits`: Currently unused

---

## Summary Statistics

- **Total Python Files**: 14 (including __init__.py files)
- **Total REST Endpoints**: 26
- **Total WebSocket Endpoints**: 1
- **Total Pydantic Models**: 15
- **Total Classes**: 9 (including dataclasses)
- **Dead/Orphaned Functions**: ~9 functions never called from main server
- **Stubs Identified**: 4 placeholder/minimal implementations
- **External Dependencies**: FastAPI, Pydantic, uvicorn, requests, winpty, sqlite3

---

**Report Complete** - Ready for Bee 3 gap analysis
