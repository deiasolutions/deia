# Task: BOT-001 - Implement Missing Backend API Endpoints

**Date:** 2025-10-26
**Priority:** CRITICAL (Blocks entire chat system)
**Owner:** BOT-001
**Dependency:** None (can start immediately)
**Estimated Time:** 2 hours (actual: ~30 min at project velocity)

---

## Context

The port 8000 chat interface frontend is waiting for 6 API endpoints that don't exist. Without these, the chat system is non-functional. This task implements all missing endpoints.

**Reference:** See `.deia/reports/PORT-8000-NEW-UX-CODE-REVIEW.md` for full analysis

---

## What's Broken

Frontend calls these endpoints, but they don't exist:

1. `GET /api/bots` - List running bots
2. `POST /api/bot/launch` - Launch new bot
3. `POST /api/bot/stop/{botId}` - Stop bot
4. `GET /api/bots/status` - Status updates (polling)
5. `GET /api/chat/history` - Load chat message history
6. `POST /api/bot/{botId}/task` - Send command to bot

---

## Task Breakdown

### Task 1: Implement `GET /api/bots` Endpoint
**Estimate:** 15 min | **Success:** Bot list displays

**Requirements:**
- Endpoint: `GET /api/bots`
- Returns JSON with bot list
- Format: `{"bots": {"BOT-001": {"status": "running", "port": 8001}, ...}}`
- Calls: Bot service/registry to get active bots
- Error handling: Handle missing service gracefully

**Implementation Plan:**
1. Check what bot service exists (e.g., `AgentStatusTracker`, bot registry, etc.)
2. Create FastAPI route: `@app.get("/api/bots")`
3. Query bot service for active bots
4. Return formatted JSON
5. Add error handling

**Test:**
```bash
curl http://localhost:8000/api/bots
# Should return: {"bots": {...}}
```

---

### Task 2: Implement `POST /api/bot/launch` Endpoint
**Estimate:** 30 min | **Success:** Bot launches from UI

**Requirements:**
- Endpoint: `POST /api/bot/launch`
- Body: `{"bot_id": "BOT-001"}`
- Returns: `{"success": true, "bot_id": "BOT-001"}` or `{"success": false, "error": "reason"}`
- Calls: Bot launcher service to start new bot
- Validates bot_id format
- Error handling: Invalid ID, already running, service errors

**Implementation Plan:**
1. Create FastAPI route: `@app.post("/api/bot/launch")`
2. Parse JSON body, extract bot_id
3. Validate format (e.g., must match "BOT-\d{3}")
4. Check if already running
5. Call bot launcher service
6. Return success/error response
7. Add comprehensive error messages

**Test:**
```bash
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id": "BOT-001"}'
# Should return: {"success": true, "bot_id": "BOT-001"}
```

---

### Task 3: Implement `POST /api/bot/stop/{botId}` Endpoint
**Estimate:** 20 min | **Success:** Bot stops from UI

**Requirements:**
- Endpoint: `POST /api/bot/stop/{botId}`
- Path param: botId (e.g., "BOT-001")
- Returns: `{"success": true}` or `{"success": false, "error": "reason"}`
- Calls: Bot stop/shutdown service
- Error handling: Bot not running, service errors

**Implementation Plan:**
1. Create FastAPI route: `@app.post("/api/bot/stop/{bot_id}")`
2. Extract bot_id from path
3. Call bot stop service
4. Return success/error
5. Add error handling

**Test:**
```bash
curl -X POST http://localhost:8000/api/bot/stop/BOT-001
# Should return: {"success": true}
```

---

### Task 4: Implement `GET /api/bots/status` Endpoint
**Estimate:** 15 min | **Success:** Status polling works

**Requirements:**
- Endpoint: `GET /api/bots/status`
- Returns: Same as `/api/bots` OR enhanced version
- Option A: Alias to `/api/bots`
- Option B: Enhanced with more status details
- Called every 5 seconds by frontend

**Implementation Plan:**
1. Option A (simpler): Reuse `/api/bots` logic
2. Option B (better): Add more status detail:
   - CPU usage
   - Memory usage
   - Uptime
   - Last activity
3. Return JSON with detailed status
4. Add caching to avoid excessive queries

**Test:**
```bash
curl http://localhost:8000/api/bots/status
# Should return: {"bots": [{...status info...}]}
```

---

### Task 5: Implement `GET /api/chat/history` Endpoint
**Estimate:** 20 min | **Success:** Chat history loads on bot select

**Requirements:**
- Endpoint: `GET /api/chat/history`
- Query params: `bot_id` (required), `limit=100` (optional)
- Returns: `{"messages": [{"role": "user/assistant", "content": "...", "timestamp": "..."}, ...]}`
- Calls: Chat history service/database
- Error handling: Bot not found, DB errors

**Implementation Plan:**
1. Create FastAPI route: `@app.get("/api/chat/history")`
2. Extract query parameters: bot_id, limit
3. Validate bot_id exists
4. Query chat history service
5. Return messages with timestamps
6. Sort by timestamp (oldest first)
7. Add error handling

**Test:**
```bash
curl "http://localhost:8000/api/chat/history?bot_id=BOT-001&limit=50"
# Should return: {"messages": [...]}
```

---

### Task 6: Implement `POST /api/bot/{botId}/task` Endpoint
**Estimate:** 20 min | **Success:** Chat commands send to bots

**Requirements:**
- Endpoint: `POST /api/bot/{botId}/task`
- Body: `{"command": "some command"}`
- Returns: `{"success": true, "response": "response text"}` OR `{"success": false, "error": "error message"}`
- Calls: Bot task/command execution service
- Executes command on specific bot
- Error handling: Bot not running, command errors, invalid format

**Implementation Plan:**
1. Create FastAPI route: `@app.post("/api/bot/{bot_id}/task")`
2. Extract bot_id and command from request
3. Validate bot_id exists and is running
4. Call bot task service with command
5. Wait for response (or return task ID)
6. Return response or error
7. Add timeout handling

**Test:**
```bash
curl -X POST http://localhost:8000/api/bot/BOT-001/task \
  -H "Content-Type: application/json" \
  -d '{"command": "echo hello"}'
# Should return: {"success": true, "response": "hello"}
```

---

## General Requirements for All Endpoints

### Request Validation:
- [ ] Validate JSON format
- [ ] Check required fields present
- [ ] Handle malformed requests gracefully

### Error Handling:
- [ ] Try/catch around service calls
- [ ] Log errors with context
- [ ] Return meaningful error messages (not stack traces)
- [ ] Use appropriate HTTP status codes

### Response Format:
- [ ] All responses JSON
- [ ] Include `success` field (bool)
- [ ] Include `error` field if unsuccessful
- [ ] Include `timestamp` for tracking

### Security:
- [ ] Validate input (no path traversal, code injection)
- [ ] Rate limiting (consider for future)
- [ ] CORS headers if needed
- [ ] Logging for audit trail

### Testing:
- [ ] Each endpoint has unit test
- [ ] Test success case
- [ ] Test error cases
- [ ] Test validation
- [ ] Integration test with frontend

---

## Success Criteria

✅ All 6 endpoints exist and respond
✅ Each endpoint calls correct service
✅ Frontend can communicate with each endpoint
✅ Bot list displays in UI
✅ Can launch/stop bots from UI
✅ Chat history loads on bot select
✅ Can send commands to bots
✅ Status updates every 5 seconds
✅ Error messages are clear
✅ Logging shows all requests/responses

---

## Implementation Order

1. Start with `GET /api/bots` (simplest, unblocks others)
2. Then `/api/bot/launch` and `/api/bot/stop` (core functionality)
3. Then `/api/chat/history` (needed for full experience)
4. Then `/api/bots/status` (for polling)
5. Finally `/api/bot/{botId}/task` (commands)

---

## Integration with Frontend

Frontend files expecting these endpoints:
- `BotList.js:18` - calls `GET /api/bots`
- `BotLauncher.js:119` - calls `POST /api/bot/launch`
- `BotList.js:84` - calls `POST /api/bot/stop`
- `app.js:114` - calls `GET /api/bots/status` (polling)
- `ChatPanel.js:48` - calls `GET /api/chat/history`
- `ChatPanel.js:107` - calls `POST /api/bot/{botId}/task`

---

## Questions for Q33N

Before starting, clarify:

1. **Bot Service APIs:** What methods are available on `AgentStatusTracker`, bot launcher, bot registry?
   - How do we list running bots?
   - How do we launch a new bot?
   - How do we stop a bot?
   - How do we send a command to a bot?

2. **Chat History:** Where is chat history stored?
   - Database? Files? Memory?
   - What service provides access to it?

3. **Command Routing:** How do we send commands to bots?
   - Through what service/API?
   - Synchronous or async?
   - How do we get responses?

---

## Status Tracking

**When Starting:** Mark as IN PROGRESS
**When Complete:** Post completion file: `.deia/hive/responses/deiasolutions/bot-001-backend-api-endpoints-complete.md`

**File format:**
```markdown
# BOT-001 Task Complete: Backend API Endpoints

- Status: COMPLETE
- Time: X minutes (estimated Y minutes)
- Velocity: X min / Y min = Zx
- Tests: X/X passing
- Issues: (none if fully working)

## Endpoints Completed:
1. ✅ GET /api/bots
2. ✅ POST /api/bot/launch
3. ✅ POST /api/bot/stop/{botId}
4. ✅ GET /api/bots/status
5. ✅ GET /api/chat/history
6. ✅ POST /api/bot/{botId}/task

## Next Steps:
BOT-003 implements frontend fixes
```

---

**Q33N Note:** This unblocks the entire chat system. These endpoints are the critical path to a working version. Focus and velocity are key.

Good luck, BOT-001. We're counting on you! 🚀
