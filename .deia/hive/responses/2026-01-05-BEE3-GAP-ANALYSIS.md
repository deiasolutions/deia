# BEE3: Gap Analysis & Bug Report

**Analyst:** BEE-003
**Date:** 2026-01-05
**Status:** Complete

---

## 1. Missing Endpoints

Endpoints in spec but NOT in server.py:

| Endpoint | Method | Spec Source | Priority |
|----------|--------|-------------|----------|
| /api/spec/plan | POST | spec-in-to-code-out.md Phase 1 | High |
| /api/tasks/run | POST | spec-in-to-code-out.md Phase 2 | High |
| /api/tasks/verify | POST | spec-in-to-code-out.md Phase 2 | High |

**Notes:**
- All MVP endpoints from mvp-checklist.md are implemented
- Missing endpoints are from Phase 1-2 (Spec Intake + Execution Loop)

---

## 2. Missing Files

Files mentioned in spec that don't exist:

| File Path | Purpose | Spec Source |
|-----------|---------|-------------|
| schemas/spec.json | Spec schema definition | Phase 1: Spec Intake |
| runtime/spec_parser.py | Markdown/spec to JSON parser | Phase 1: Spec Intake |
| runtime/task_graph.py | Task dependency graph builder | Phase 1: Spec Intake |
| runtime/executor.py | Task execution loop | Phase 2: Execution Loop |
| runtime/verifier.py | Test runner hook | Phase 2: Verification |
| runtime/git_flow.py | Patch assembly + commit pipeline | Phase 3: Git Automation |
| runtime/telemetry.py | Cost/token tracking | Phase 4: Observability |

**Existing Files (for context):**
- `schemas/task_file.json` - EXISTS
- `runtime/server.py` - EXISTS (main API)
- `runtime/store.py` - EXISTS (message persistence)
- `runtime/flights.py` - EXISTS (flight tracking)
- `runtime/minder.py` - EXISTS (periodic ping)
- `runtime/launcher.py` - EXISTS (repo root preflight)
- `runtime/pty_bridge.py` - EXISTS (PTY sessions)

---

## 3. Unconnected Code

Functions/classes that exist but aren't wired up:

| Item | File | Issue |
|------|------|-------|
| `decide_route()` | core/router.py | Defined but NEVER called from server.py |
| `run_minder()` | runtime/minder.py | Standalone script, not integrated with server startup |
| KB injection | kb/store.py | `preview_injection()` exists but NOT used when creating tasks |

**Details:**

### Router Never Used (Critical)
The routing logic in `core/router.py:12-19` (`decide_route()`) is completely disconnected:
- `POST /api/tasks` creates tasks but doesn't call the router
- Tasks are written directly to files without lane/provider routing
- The intent field is captured but never processed

### Minder Not Integrated
`runtime/minder.py` is a standalone script that must be run separately:
- Has `if __name__ == "__main__": run_minder()` pattern
- Not started automatically when server runs
- No thread/process management in server.py

### KB Injection Missing
When creating tasks via `POST /api/tasks`:
- `kb_entities` list is accepted in `TaskRequest`
- But `write_task()` just stores entity IDs, doesn't inject content
- `preview_injection()` exists but only used by `/api/kb/preview`

---

## 4. Incomplete Implementations

Code exists but is a stub/placeholder:

| Item | File | What's Missing |
|------|------|----------------|
| WebSocket /api/ws | server.py:424-432 | Only echoes input, no real messaging |
| PTY session cleanup | pty_bridge.py | Sessions removed on explicit stop, not auto-cleanup on disconnect |
| Gate check incomplete | server.py:356 | `allow_flight_commits` gate exists but NOT checked in git_commit |

**Details:**

### WebSocket Echo-Only
```python
# server.py:424-432
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)  # Just echoes!
    except WebSocketDisconnect:
        return
```
- No message broadcasting
- No channel routing
- No integration with MessageStore
- No real-time updates to UI

### Gate Check Incomplete
```python
# server.py:348-370
@app.post("/api/git/commit")
def git_commit(request: GitCommitRequest) -> Dict:
    # Checks these:
    if not _gates.get("allow_q33n_git", False): ...
    if not _gates.get("pre_sprint_review", False): ...
    # BUT NOT this:
    # if not _gates.get("allow_flight_commits", False): ...
```

---

## 5. Logic Bugs

Code that won't work as written:

| Bug | File:Line | Issue | Severity |
|-----|-----------|-------|----------|
| Task routing bypassed | server.py:279-291 | Tasks created without routing, `intent` field ignored | High |
| KB entities not injected | server.py:287 | Entity IDs stored but content never retrieved/injected | High |
| Missing flight gate | server.py:356-359 | `allow_flight_commits` gate defined but not enforced | Medium |
| PTY memory leak risk | pty_bridge.py:77-86 | `stop()` removes session but exception may leave orphans | Low |

---

## Bug Hunting Checklist Results

- [x] **Router unused**: Does `decide_route()` get called?
  - Finding: **NO.** `decide_route()` in `core/router.py:12` is never imported or called by server.py. Task creation bypasses routing entirely.

- [x] **Minder not scheduled**: Does `minder.py` have scheduled execution?
  - Finding: **NO.** Minder is a standalone script with `if __name__ == "__main__"` block. Not integrated with server startup. Must be run separately via `python -m deia_raqcoon.runtime.minder`.

- [x] **PTY cleanup**: Are sessions cleaned up on disconnect?
  - Finding: **PARTIAL.** Sessions are cleaned up when `stop()` is called explicitly. But if client disconnects without calling stop, session stays in memory with `alive=False`.

- [x] **WebSocket functionality**: Is `/api/ws` doing anything useful?
  - Finding: **NO.** WebSocket endpoint only echoes received text. No broadcasting, no channel support, no MessageStore integration.

- [x] **Git gate check**: Does commit check `allow_flight_commits`?
  - Finding: **NO.** `git_commit` checks `allow_q33n_git` and `pre_sprint_review` but NOT `allow_flight_commits`. Gate is defined but never enforced.

- [x] **Task archival**: Is `complete_task` working correctly?
  - Finding: **YES.** `complete_task()` in `task_files.py:46-62` correctly:
    - Loads task JSON
    - Updates status to "completed"
    - Adds `completed_at` timestamp
    - Moves to archive directory

- [x] **KB injection**: Is it actually used when creating tasks?
  - Finding: **NO.** Task creation accepts `kb_entities` list but:
    - Only stores entity IDs in task JSON
    - Never calls `preview_injection()` to get content
    - KB content never injected into task payload

---

## 6. MVP Checklist Status

For each MVP item, current status:

### 1) Runtime + API

| Category | Item | Status | Notes |
|----------|------|--------|-------|
| Runtime | FastAPI app | DONE | server.py exists and runs |
| Runtime | WebSocket /api/ws | PARTIAL | Exists but echo-only |
| REST | GET /api/health | DONE | |
| REST | GET /api/config | DONE | |
| REST | POST /api/bees/launch | DONE | |
| REST | POST /api/messages | DONE | |
| REST | GET /api/messages | DONE | |
| REST | GET /api/channels | DONE | |
| REST | POST /api/tasks | DONE | Missing routing integration |
| REST | GET /api/tasks/response | DONE | |
| REST | GET /api/git/status | DONE | |
| REST | POST /api/git/commit | DONE | Gate check incomplete |
| REST | POST /api/git/push | DONE | |
| REST | POST /api/flights/start | DONE | |
| REST | POST /api/flights/end | DONE | |
| REST | POST /api/flights/recap | DONE | |
| REST | GET /api/flights | DONE | |
| REST | GET /api/flights/recaps | DONE | |

### 2) CLI Bee Launch

| Item | Status | Notes |
|------|--------|-------|
| Preflight repo root | DONE | launcher.py |
| Prompt if not at root | DONE | Returns status="prompt" |
| chdir before launch | DONE | CLIAdapter changes cwd |
| Claude Code adapter | DONE | registry.py |
| Codex adapter | DONE | registry.py |

### 3) Task File Loop

| Item | Status | Notes |
|------|--------|-------|
| Write tasks to .deia/hive/tasks/{bot-id}/ | DONE | task_files.py |
| Read responses from .deia/hive/responses/ | DONE | latest_response() |
| Task file schema | DONE | schemas/task_file.json |
| Archive/complete tasks | DONE | complete_task() |

### 4) KB Injection

| Item | Status | Notes |
|------|--------|-------|
| KB entity types: RULE + SNIPPET | DONE | kb/store.py |
| Delivery: cache_prompt + task_file | PARTIAL | Mode stored but not used |
| Injection preview | DONE | preview_injection() |
| **Actual injection into tasks** | MISSING | Entity IDs stored, content not injected |

### 5) UI Wiring

| Item | Status | Notes |
|------|--------|-------|
| Landing page | UNKNOWN | UI not reviewed |
| Project hub | UNKNOWN | UI not reviewed |
| Chat dashboard | UNKNOWN | UI not reviewed |
| Operator mode | UNKNOWN | UI not reviewed |
| KB editor | UNKNOWN | UI not reviewed |
| Git browser | UNKNOWN | UI not reviewed |

### 6) Logging + Cost

| Item | Status | Notes |
|------|--------|-------|
| Per-message metadata | DONE | lane, provider, token_count stored |
| Session summary | DONE | get_summary() aggregates |
| Flight start/end + recap | DONE | FlightStore |
| Minder stub | PARTIAL | Exists but not integrated |

---

## 7. Priority Ranking

What to fix/build first for MVP:

### Critical (Blocks MVP)

1. **Wire up router.py** - Tasks must be routed by intent
2. **Implement KB injection** - Tasks need actual KB content, not just IDs
3. **Make WebSocket functional** - Real-time updates required for chat UI

### High (Core functionality)

1. **Integrate minder with server** - Auto-start on server launch
2. **Add allow_flight_commits gate check** - Complete gate enforcement
3. **Build /api/spec/plan endpoint** - Phase 1 spec intake

### Medium (Important but not blocking)

1. **Build /api/tasks/run endpoint** - Phase 2 execution loop
2. **Build /api/tasks/verify endpoint** - Phase 2 verification
3. **Add PTY auto-cleanup** - Clean up disconnected sessions

### Low (Nice to have)

1. **Create runtime/telemetry.py** - Enhanced cost tracking
2. **Create runtime/git_flow.py** - Patch assembly automation
3. **Improve WebSocket with channels** - Multi-room messaging

---

## 8. Recommended Next Steps

Ordered list of what to tackle:

1. **Wire router into task creation** (1-2 hours)
   - Import `decide_route` in server.py
   - Call router when creating tasks
   - Store routing decision in task payload

2. **Implement KB injection into tasks** (2-3 hours)
   - Call `preview_injection()` when creating task
   - Inject content based on delivery_mode
   - Add injected content to task file

3. **Make WebSocket functional** (3-4 hours)
   - Add message broadcasting
   - Integrate with MessageStore
   - Add channel/room support

4. **Integrate minder with server startup** (1 hour)
   - Add background thread for minder
   - Make interval configurable
   - Add shutdown handling

5. **Complete gate enforcement** (30 min)
   - Add `allow_flight_commits` check to git_commit
   - Document gate meanings

6. **Build Phase 1 spec intake** (4-6 hours)
   - Create schemas/spec.json
   - Build spec_parser.py
   - Build task_graph.py
   - Add /api/spec/plan endpoint

---

## Summary

**MVP Status:** ~70% complete

**Working Well:**
- Basic API structure
- Task file loop
- Flight tracking
- CLI bee launch with repo-root discipline
- KB entity storage

**Needs Fixing:**
- Router completely disconnected
- KB injection not happening
- WebSocket is just an echo server
- Gate enforcement incomplete

**Biggest Gap:**
The routing system exists (`core/router.py`) but is never used. This is a fundamental architectural piece that's been implemented but not wired in. Every task bypasses routing and goes directly to file storage.
