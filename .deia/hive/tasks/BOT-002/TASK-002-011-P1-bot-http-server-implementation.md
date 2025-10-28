# TASK-002-011: Bot HTTP Server - Port-Based Communication

**Task ID:** TASK-002-011
**Bot ID:** BOT-002
**Priority:** P1
**Created:** 2025-10-28
**Timeout:** 600 seconds

---

## OBJECTIVE

Implement HTTP/WebSocket server for BOT-002 to accept port-based communication. This enables BOT-002 to receive tasks via HTTP POST and respond via WebSocket, complementing the existing file-queue system.

---

## BACKGROUND

**Current State:**
- BOT-002 uses file-queue only (tasks from `.deia/hive/tasks/BOT-002/`)
- All responses written to file (`/deia/hive/responses/`)
- No HTTP or WebSocket support

**Desired State:**
- BOT-002 listens on assigned port (e.g., 8002)
- Accepts HTTP POST `/api/task` for immediate tasks
- Accepts WebSocket `/ws` for streaming responses
- Maintains both file and port channels
- Priority: WebSocket tasks execute before file queue

**Why This Matters:**
- Enables real-time interaction via Commandeer dashboard
- Keeps async file queue for offline operation
- Allows mixing real-time + batch work

---

## IMPLEMENTATION REQUIREMENTS

### 1. Create New Module: `src/deia/adapters/bot_http_server.py`

This module provides a lightweight HTTP/WebSocket server embedded in BotRunner.

**Specification:**
- Use FastAPI (already a dependency)
- No blocking - use async/await
- Share response writer with file-queue system
- Implement these endpoints:

#### Endpoint: GET `/status`
Returns bot status as JSON
```json
{
  "bot_id": "BOT-002",
  "status": "idle|processing",
  "uptime_seconds": 3600,
  "tasks_processed": 10,
  "current_task": "TASK-002-011" or null
}
```

#### Endpoint: POST `/api/task`
Accepts a task and queues it (WebSocket priority)
Request body:
```json
{
  "task_id": "INTERACTIVE-001",
  "command": "Do something",
  "priority": "immediate"
}
```
Response:
```json
{
  "status": "queued",
  "task_id": "INTERACTIVE-001",
  "message": "Task queued for execution"
}
```

#### Endpoint: WebSocket `/ws`
Streaming endpoint for real-time interaction
- Accept connection
- Receive JSON messages with task
- Send JSON responses as they complete
- On disconnect: save any pending task to file queue

Message format (client -> server):
```json
{
  "type": "task",
  "command": "your instruction here"
}
```

Response format (server -> client):
```json
{
  "type": "response",
  "content": "response text",
  "success": true,
  "timestamp": "2025-10-28T14:00:00Z"
}
```

### 2. Modify: `src/deia/adapters/bot_runner.py`

Add port binding support:

**In `__init__`:**
- Add parameter: `port: int = None`
- Store: `self.port = port`
- Store: `self.http_server = None`

**Add method: `start_http_server()`**
- Create FastAPI app using bot_http_server module
- Bind to `0.0.0.0:{self.port}`
- Run in background thread (non-blocking)
- Return: success/failure

**In `run()` main loop:**
- Call `self.start_http_server()` at startup (after CLI subprocess starts)
- Check both WebSocket queue AND file queue in polling loop
- WebSocket queue first (priority)

**Modify: `run_once()`**
- Add WebSocket queue check
- Get next task from either source
- Execute task
- Pass response to BOTH sinks (WebSocket + file)

### 3. Modify: `run_single_bot.py`

Add command-line flag:
```bash
python run_single_bot.py BOT-002 --port 8002 --mode hybrid
```

Changes:
- Add `--port` argument to argparse
- Pass port to BotRunner.__init__
- Document in help: "Port for HTTP/WebSocket server (optional, requires --mode hybrid)"

### 4. Modify: `.deia/hive/tasks/BOT-002/BOT-002-LAUNCH-MISSION.md`

Update documentation:
- Document port assignment from ServiceRegistry
- Show example: BOT-002 on port 8002
- Explain WebSocket priority over file queue
- Show how Commandeer can connect via WebSocket

---

## ACCEPTANCE CRITERIA

✅ **HTTP Server Running:**
- [ ] Bot starts with `--port 8002`
- [ ] GET `/status` returns valid JSON with bot_id and status
- [ ] Server stays alive during file queue processing

✅ **HTTP Task Endpoint:**
- [ ] POST `/api/task` accepts task JSON
- [ ] Task gets queued (before file queue in priority)
- [ ] Returns success JSON with task_id

✅ **WebSocket Support:**
- [ ] WebSocket `/ws` accepts connections
- [ ] Client can send task JSON
- [ ] Server sends response JSON back
- [ ] On client disconnect: any pending task saved to file queue

✅ **Priority Queue Working:**
- [ ] WebSocket task queued → executes immediately
- [ ] File task queued → executes after WebSocket tasks
- [ ] Both sources feed to execution engine
- [ ] No tasks lost or skipped

✅ **Response Writing:**
- [ ] WebSocket responses sent to client in real-time
- [ ] File responses written to `.deia/hive/responses/` (for audit)
- [ ] Response includes source tag (will be added in TASK-002-012)

✅ **Error Handling:**
- [ ] Invalid JSON returns error response
- [ ] Missing fields handled gracefully
- [ ] Server doesn't crash on bad input
- [ ] Errors logged to error log

✅ **Documentation:**
- [ ] Code includes docstrings
- [ ] Endpoint specs documented
- [ ] Launch mission updated with port info
- [ ] Example usage shown

---

## IMPLEMENTATION NOTES

### Architecture Pattern

```
┌─────────────────────────────────────┐
│ BotRunner (main loop)               │
├─────────────────────────────────────┤
│ - Runs Claude CLI subprocess        │
│ - Polls both queues                 │
│ - Executes tasks                    │
│ - Writes responses                  │
└─────────────────────────────────────┘
         ↑                    ↑
    File Queue          HTTP/WebSocket
   (async)              (real-time)
         │                    │
         └────────┬───────────┘
                  │
            run_once() method
            (unified execution)
```

### Threading Model

- **Main thread:** Claude CLI subprocess + file queue polling
- **HTTP thread:** FastAPI server (handles /status, /api/task, /ws)
- **Async handling:** Use `asyncio` for WebSocket queue, non-blocking

### Queue Implementation

For WebSocket queue, use:
- `asyncio.Queue` (thread-safe, async)
- Size limit: 100 tasks (prevent memory explosion)
- Drop oldest if queue full? Or block? → **Return 429 Too Busy**

---

## TESTING APPROACH

After implementation, verify with:

```bash
# 1. Start BOT-002 with port
python run_single_bot.py BOT-002 --port 8002 --mode hybrid

# 2. Test /status endpoint
curl http://localhost:8002/status

# 3. Test POST /api/task
curl -X POST http://localhost:8002/api/task \
  -H "Content-Type: application/json" \
  -d '{"command": "hello"}'

# 4. Test WebSocket (use wscat or similar)
wscat -c ws://localhost:8002/ws
# Then type: {"type": "task", "command": "test"}

# 5. Verify file responses still created
ls .deia/hive/responses/TASK-*
```

---

## DELIVERABLES

1. ✅ New file: `src/deia/adapters/bot_http_server.py`
2. ✅ Modified: `src/deia/adapters/bot_runner.py`
3. ✅ Modified: `run_single_bot.py`
4. ✅ Updated: `.deia/hive/tasks/BOT-002/BOT-002-LAUNCH-MISSION.md`
5. ✅ Test results: confirm all acceptance criteria met
6. ✅ Response file: include implementation notes and issues found

---

## RESOURCES

**Reference files:**
- `COMMUNICATION-MODES-FRAMEWORK.md` - Architecture overview
- `HYBRID-MODE-DESIGN.md` - Priority queue design
- Existing `bot_runner.py` - Current implementation

**Libraries available:**
- FastAPI (web framework)
- asyncio (async/await)
- websockets (already used in Commandeer)

---

## FOLLOW-UP TASKS

This task enables:
- TASK-002-012: Response tagging (add source and timestamp)
- TASK-002-013: Priority queue logic refinement
- TASK-002-014: Timeline API endpoint

---

**Priority:** P1 (blocks timeline implementation)
**Status:** Ready for execution
**Assigned to:** BOT-002

