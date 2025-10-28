# TASK-002-015: WebSocket Streaming Responses Specification

**Task ID:** TASK-002-015
**Bot ID:** BOT-002
**Priority:** P1
**Created:** 2025-10-28
**Timeout:** 300 seconds
**Depends on:** TASK-002-011, TASK-002-012, TASK-002-014

---

## OBJECTIVE

Design streaming response protocol for WebSocket so clients connected to BOT-002 receive real-time updates as tasks complete. This enables Commandeer dashboard to show live progress without polling.

---

## BACKGROUND

**Current State:**
- WebSocket accepts tasks via POST /api/task
- Responses returned only to HTTP client or WebSocket that sent it
- No broadcasting to multiple clients
- No streaming of long-running operations

**Desired State:**
- Multiple clients can subscribe to task updates
- New responses broadcast to all subscribed clients
- Long-running tasks stream progress updates
- Clients can filter which updates they want
- Clean connection management (subscribe/unsubscribe)

**Use Case:**
```
Commandeer Dashboard (port 6666) connects via WebSocket
├─ Subscribe to BOT-002 updates
├─ Receive: TASK-002-011 started
├─ Receive: [progress] 50% complete
├─ Receive: [progress] 100% complete
└─ Receive: TASK-002-011 completed
```

---

## MESSAGE PROTOCOL

### Client Messages

**Subscribe to updates:**
```json
{
  "type": "subscribe",
  "bot_id": "BOT-002",
  "filters": {
    "source": "file",          // optional: file or websocket
    "status": "in_progress"    // optional: pending, in_progress, completed, failed
  }
}
```

**Unsubscribe:**
```json
{
  "type": "unsubscribe",
  "bot_id": "BOT-002"
}
```

**Heartbeat (client → server):**
```json
{
  "type": "ping"
}
```

---

### Server Messages

**Subscription confirmed:**
```json
{
  "type": "subscribed",
  "bot_id": "BOT-002",
  "message": "Connected to timeline for BOT-002",
  "initial_entries": [
    { "task_id": "...", "status": "completed", ... },
    { "task_id": "...", "status": "completed", ... }
  ]
}
```

**Task started:**
```json
{
  "type": "task_started",
  "task_id": "TASK-002-011",
  "bot_id": "BOT-002",
  "source": "file",
  "timestamp": "2025-10-28T14:05:00Z"
}
```

**Progress update (for long tasks):**
```json
{
  "type": "progress",
  "task_id": "TASK-002-011",
  "percent": 50,
  "message": "50% complete - processing files...",
  "timestamp": "2025-10-28T14:05:30Z"
}
```

**Task completed:**
```json
{
  "type": "task_completed",
  "task_id": "TASK-002-011",
  "bot_id": "BOT-002",
  "source": "file",
  "success": true,
  "response": "Implementation complete",
  "files_modified": ["bot_runner.py"],
  "duration_seconds": 1200,
  "timestamp": "2025-10-28T14:25:00Z"
}
```

**Task failed:**
```json
{
  "type": "task_failed",
  "task_id": "TASK-002-011",
  "bot_id": "BOT-002",
  "error": "Timeout after 300 seconds",
  "timestamp": "2025-10-28T14:35:00Z"
}
```

**Heartbeat (server → client):**
```json
{
  "type": "pong"
}
```

**Error:**
```json
{
  "type": "error",
  "message": "Invalid bot_id",
  "error_code": 400
}
```

---

## STREAMING IMPLEMENTATION

### Architecture

```
Task Completes
      ↓
BotRunner._write_response()
      ↓
TimelineService.add_entry()  ← NEW
      ↓
   Broadcast to WebSocket handlers
      ↓
   Send to all subscribed clients
      ↓
Commandeer Dashboard receives update
```

### Integration Points

**1. In BotRunner.py (when response complete):**
```python
def _write_response(self, response_dict, source="file"):
    # ... existing response writing ...

    # NEW: Notify timeline service of new entry
    if self.timeline_service:
        await self.timeline_service.add_entry({
            "task_id": response_dict["task_id"],
            "source": source,
            "success": response_dict["success"],
            "response": response_dict.get("output"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            # ... other fields
        })
```

**2. New TimelineService class:**
```python
class TimelineService:
    def __init__(self):
        self.subscribers = set()  # Set of WebSocket connections

    async def add_entry(self, entry):
        """Add entry and broadcast to subscribers"""
        # Save to persistent storage
        await self._save_entry(entry)

        # Broadcast to all subscribed clients
        await self._broadcast_update(entry)

    async def subscribe(self, websocket, filters):
        """Handle new WebSocket subscription"""
        self.subscribers.add(websocket)
        # Send recent entries
        # Listen for messages

    async def _broadcast_update(self, entry):
        """Send update to all subscribed clients"""
        for client in self.subscribers:
            try:
                await client.send_json({
                    "type": "task_completed",
                    "entry": entry
                })
            except Exception as e:
                logger.error(f"Failed to send to client: {e}")
                self.subscribers.discard(client)
```

---

## PROGRESS STREAMING

**For long-running tasks, enable progress updates:**

When task takes >10 seconds, bot can send intermediate progress:

```python
async def execute_long_task(self, task):
    start = time.time()
    total_steps = 100

    for i in range(total_steps):
        # Do work...
        elapsed = time.time() - start

        # Send progress every 10 steps
        if i % 10 == 0:
            await self.timeline_service.send_progress(
                task_id=task["task_id"],
                percent=int(i / total_steps * 100),
                message=f"Processing step {i}/{total_steps}",
                elapsed_seconds=elapsed
            )

    # Send final completion
    await self._write_response(result, source=source)
```

---

## FILTERING & SUBSCRIPTION

**Client can filter what updates they receive:**

```python
# Subscribe to only file queue tasks
{
  "type": "subscribe",
  "filters": { "source": "file" }
}

# Subscribe to only failed tasks
{
  "type": "subscribe",
  "filters": { "success": false }
}

# Subscribe to in-progress tasks only
{
  "type": "subscribe",
  "filters": { "status": "in_progress" }
}
```

**Server filters before sending:**
```python
async def _broadcast_update(self, entry, filters=None):
    for client in self.subscribers:
        if not self._matches_filters(entry, client.filters):
            continue  # Skip this client

        await client.send_json({...})
```

---

## CONNECTION MANAGEMENT

### Subscribe
1. Client opens WebSocket to /ws/bot/BOT-002/timeline
2. Client sends subscribe message with filters
3. Server responds with "subscribed" + recent entries
4. Server starts broadcasting updates

### Stay Connected
1. Client periodically sends ping (heartbeat)
2. Server responds with pong
3. If no heartbeat for 60 seconds, server closes connection
4. If server fails to send, removes client from subscribers

### Unsubscribe
1. Client sends unsubscribe message
2. Server removes from subscribers
3. Server closes connection (or keeps alive for other operations)

---

## PERFORMANCE REQUIREMENTS

| Metric | Target | Notes |
|--------|--------|-------|
| Broadcast latency | <100ms | From task complete to client receive |
| Message size | <1KB | Keep updates lightweight |
| Max subscribers | 100+ | Should scale to many dashboards |
| Heartbeat interval | 30 seconds | Keeps connection alive |
| Reconnection time | <5 seconds | Re-subscribe and catch up |

---

## TESTING SCENARIOS

**Test 1: Single subscriber**
```
Dashboard connects → Task completes → Update received
Expected: Update arrives <100ms after task complete
```

**Test 2: Multiple subscribers**
```
3 dashboards subscribe → Task completes → All 3 receive update
Expected: All updates delivered, no missing clients
```

**Test 3: Filtered subscription**
```
Dashboard subscribes to source=file only
Queue WebSocket + file task
Expected: Only file task update received
```

**Test 4: Disconnect recovery**
```
Dashboard disconnects mid-stream
Task completes offline
Dashboard reconnects
Expected: Dashboard receives recent entries from timeline API
```

**Test 5: Long-running task**
```
Task takes 60 seconds
Bot sends progress updates
Expected: Dashboard sees: started → 25% → 50% → 75% → completed
```

---

## FAILURE HANDLING

**If broadcast fails:**
```python
try:
    await client.send_json(message)
except:
    # Client connection died
    # Remove from subscribers
    self.subscribers.discard(client)
    # Client will reconnect if needed
```

**If client disconnects:**
```python
try:
    while True:
        data = await websocket.receive_text()
        # Handle message
except WebSocketDisconnect:
    self.subscribers.discard(websocket)
    logger.info("Client disconnected, removed from subscribers")
```

**If update queue overflows:**
```python
if len(self.pending_updates) > 1000:
    # Too many queued updates
    # Oldest clients will re-sync via API
    logger.warning("Update queue full, clients should poll API")
```

---

## ACCEPTANCE CRITERIA

✅ **Message Protocol:**
- [ ] subscribe message format correct
- [ ] task_completed message includes all fields
- [ ] progress message format correct
- [ ] error messages documented

✅ **Broadcasting:**
- [ ] All subscribed clients receive updates
- [ ] Latency <100ms
- [ ] No duplicate messages
- [ ] No message loss

✅ **Filtering:**
- [ ] Filters correctly applied
- [ ] Only matching updates sent
- [ ] Multiple filters work together

✅ **Connection Management:**
- [ ] Clients can subscribe/unsubscribe
- [ ] Heartbeat keeps connection alive
- [ ] Dead connections detected and removed
- [ ] Reconnection works

✅ **Progress Streaming:**
- [ ] Long tasks send progress updates
- [ ] Progress percent increments correctly
- [ ] Message updates are meaningful

✅ **Integration:**
- [ ] BotRunner calls timeline_service.add_entry()
- [ ] New entries appear in WebSocket stream
- [ ] File and WebSocket tasks both broadcast
- [ ] Responses include source tag

---

## DELIVERABLES

1. **Message protocol specification**
2. **TimelineService class design**
3. **WebSocket handler implementation**
4. **Integration points in BotRunner**
5. **Test scenarios with expected results**
6. **Client example code (JavaScript)**

---

## DEPENDENCIES

**Requires:**
- TASK-002-011 (HTTP/WebSocket server infrastructure)
- TASK-002-012 (Response tagging with source field)
- TASK-002-014 (Timeline API for fallback)

---

**Status:** Ready for analysis by BOT-002
**Assigned to:** BOT-002
**Priority:** P1

