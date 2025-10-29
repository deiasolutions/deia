# TASK-002-015: WebSocket Streaming Responses - SPECIFICATION

**Task ID:** TASK-002-015
**Bot ID:** BOT-002
**Priority:** P1
**Status:** ANALYSIS COMPLETE
**Date:** 2025-10-28T14:50:00Z
**Depends on:** TASK-002-011, 012, 014

---

## OBJECTIVE

Design WebSocket streaming protocol so multiple clients receive real-time task updates as they complete. Enables Commandeer dashboard to show live progress without polling.

---

## PROTOCOL SPECIFICATION

### Client → Server Messages

#### 1. Subscribe to Updates

```json
{
  "type": "subscribe",
  "bot_id": "BOT-002",
  "filters": {
    "source": "file|websocket",    // Optional
    "status": "in_progress|completed|failed",  // Optional
    "success": true|false          // Optional
  }
}
```

**Example: Only file tasks**
```json
{
  "type": "subscribe",
  "bot_id": "BOT-002",
  "filters": { "source": "file" }
}
```

#### 2. Unsubscribe

```json
{
  "type": "unsubscribe",
  "bot_id": "BOT-002"
}
```

#### 3. Heartbeat (Keep-Alive)

```json
{
  "type": "ping"
}
```

---

### Server → Client Messages

#### 1. Subscription Confirmed

```json
{
  "type": "subscribed",
  "bot_id": "BOT-002",
  "message": "Connected to BOT-002 timeline",
  "initial_entries": [
    {
      "task_id": "TASK-002-010",
      "source": "file",
      "timestamp": "2025-10-28T14:00:00Z",
      "success": true,
      "response": "Session summary complete"
    },
    {
      "task_id": "TASK-002-011",
      "source": "file",
      "timestamp": "2025-10-28T14:05:00Z",
      "success": true,
      "response": "HTTP server implementation complete"
    }
  ]
}
```

#### 2. Task Started

```json
{
  "type": "task_started",
  "task_id": "TASK-002-012",
  "bot_id": "BOT-002",
  "source": "file",
  "timestamp": "2025-10-28T14:05:00Z"
}
```

#### 3. Progress Update (Long-Running Tasks)

```json
{
  "type": "progress",
  "task_id": "TASK-002-012",
  "percent": 50,
  "message": "Processing files... (50% complete)",
  "elapsed_seconds": 30,
  "timestamp": "2025-10-28T14:05:30Z"
}
```

#### 4. Task Completed

```json
{
  "type": "task_completed",
  "task_id": "TASK-002-012",
  "bot_id": "BOT-002",
  "source": "file",
  "success": true,
  "response": "Response tagging implementation complete",
  "files_modified": ["src/deia/adapters/bot_runner.py"],
  "duration_seconds": 300,
  "timestamp": "2025-10-28T14:10:00Z"
}
```

#### 5. Task Failed

```json
{
  "type": "task_failed",
  "task_id": "TASK-002-012",
  "bot_id": "BOT-002",
  "error": "Timeout after 300 seconds",
  "timestamp": "2025-10-28T14:15:00Z"
}
```

#### 6. Heartbeat Response

```json
{
  "type": "pong",
  "timestamp": "2025-10-28T14:15:30Z"
}
```

#### 7. Error Response

```json
{
  "type": "error",
  "message": "Invalid bot_id",
  "error_code": 400
}
```

---

## ARCHITECTURE

### Data Flow

```
Task Completion
      ↓
BotRunner._write_response()
      ↓
TimelineService.add_entry()
      ↓
  Save to timeline.jsonl
      ↓
  Filter for each subscriber
      ↓
  Broadcast to all subscribed clients
      ↓
Commandeer Dashboard receives update
```

### Integration Points

**1. BotRunner modification (when response written):**

```python
def _write_response(self, response_dict, source="file"):
    # ... existing response writing ...

    # NEW: Notify timeline service
    if self.timeline_service:
        entry = {
            "task_id": response_dict.get("task_id"),
            "bot_id": self.bot_id,
            "source": source,
            "success": response_dict.get("success", False),
            "response": response_dict.get("response", ""),
            "files_modified": response_dict.get("files_modified", []),
            "duration_seconds": response_dict.get("duration_seconds"),
            "error": response_dict.get("error"),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        # Async call to add entry and broadcast
        asyncio.create_task(self.timeline_service.add_entry(entry))
```

**2. TimelineService class:**

```python
class TimelineService:
    def __init__(self, bot_id, log_dir):
        self.bot_id = bot_id
        self.log_dir = log_dir
        self.subscribers = {}  # {websocket: filters}

    async def add_entry(self, entry):
        """Add to timeline and broadcast to subscribers"""
        # Save to timeline.jsonl
        await self._save_entry(entry)

        # Broadcast to all subscribers
        await self._broadcast_update(entry)

    async def subscribe(self, websocket, filters):
        """Register new subscriber"""
        self.subscribers[websocket] = filters

        # Send recent entries
        recent = await self._get_recent_entries(limit=50)
        await websocket.send_json({
            "type": "subscribed",
            "bot_id": self.bot_id,
            "initial_entries": recent
        })

    async def unsubscribe(self, websocket):
        """Remove subscriber"""
        self.subscribers.pop(websocket, None)

    async def _broadcast_update(self, entry):
        """Send to all matching subscribers"""
        dead_clients = []

        for client_ws, filters in self.subscribers.items():
            # Apply filters
            if not self._matches_filters(entry, filters):
                continue

            try:
                await client_ws.send_json({
                    "type": "task_completed",
                    "entry": entry
                })
            except Exception as e:
                logger.error(f"Broadcast failed: {e}")
                dead_clients.append(client_ws)

        # Remove dead connections
        for ws in dead_clients:
            self.subscribers.pop(ws, None)

    def _matches_filters(self, entry, filters):
        """Check if entry matches subscription filters"""
        if not filters:
            return True

        if filters.get('source') and entry['source'] != filters['source']:
            return False

        if filters.get('success') is not None:
            if entry['success'] != filters['success']:
                return False

        return True
```

---

## FILTERING STRATEGY

**Client specifies filters when subscribing:**

```json
// Only file queue tasks
{
  "type": "subscribe",
  "filters": { "source": "file" }
}

// Only successful tasks
{
  "type": "subscribe",
  "filters": { "success": true }
}

// Only failed tasks
{
  "type": "subscribe",
  "filters": { "success": false }
}

// Multiple filters combined
{
  "type": "subscribe",
  "filters": {
    "source": "file",
    "success": true
  }
}
```

**Server-side filtering:**

```python
def _matches_filters(self, entry, filters):
    """Check if entry should be sent to this subscriber"""

    # No filters = send everything
    if not filters:
        return True

    # Check source filter
    if 'source' in filters:
        if entry['source'] != filters['source']:
            return False

    # Check success filter
    if 'success' in filters:
        if entry['success'] != filters['success']:
            return False

    # Check status filter (if implemented)
    if 'status' in filters:
        status = 'completed' if entry['success'] else 'failed'
        if status != filters['status']:
            return False

    return True
```

---

## PROGRESS STREAMING

**For long-running tasks (>10 seconds):**

Bot can send intermediate progress updates:

```python
async def execute_long_task(self, task):
    """Example: long task with progress updates"""
    task_id = task["task_id"]
    start_time = time.time()
    total_work = 100

    for step in range(total_work):
        # Do work...
        elapsed = time.time() - start_time

        # Send progress every 10 steps
        if step % 10 == 0 and step > 0:
            percent = int(step / total_work * 100)
            await self.timeline_service.send_progress(
                task_id=task_id,
                percent=percent,
                message=f"Processing {step}/{total_work}",
                elapsed_seconds=elapsed
            )

        # If task takes too long, can cancel
        if elapsed > task.get("timeout", 300):
            raise TimeoutError("Task exceeded timeout")

    # Task complete
    result = {"success": True, "output": "Done"}
    await self._write_response(result, source="file")
```

**TimelineService.send_progress():**

```python
async def send_progress(self, task_id, percent, message, elapsed_seconds):
    """Send progress update to subscribers"""
    update = {
        "type": "progress",
        "task_id": task_id,
        "percent": percent,
        "message": message,
        "elapsed_seconds": elapsed_seconds,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    # Broadcast only to subscribers watching this task_id
    for ws in self.subscribers:
        try:
            await ws.send_json(update)
        except:
            pass  # Client will reconnect
```

---

## CONNECTION MANAGEMENT

### Subscribe Flow

```
1. Client: WebSocket /ws/bot/BOT-002/timeline
2. Client: Send subscribe message
3. Server: Add to subscribers
4. Server: Send "subscribed" with initial entries
5. Server: Start broadcasting updates
6. Client: Receives messages as tasks complete
```

### Keep-Alive (Heartbeat)

```
30 seconds:
  Client sends: { "type": "ping" }
  Server responds: { "type": "pong" }

60 seconds no heartbeat:
  Server closes connection
  Client reconnects
```

### Graceful Disconnect

```
Client sends: { "type": "unsubscribe" }
Server removes from subscribers
Connection stays open or closes (optional)
```

---

## PERFORMANCE TARGETS

| Metric | Target | Why |
|--------|--------|-----|
| Broadcast latency | <100ms | Real-time feel |
| Message size | <1KB | Lightweight |
| Max subscribers | 100+ | Scale to many dashboards |
| Heartbeat interval | 30s | Keep connection alive |
| Reconnection time | <5s | Fast recovery |

**Example response time:**
```
Task completes at: 14:05:30.000
Server broadcasts at: 14:05:30.050 (50ms)
Client receives at: 14:05:30.080 (80ms total)
Target: <100ms ✓
```

---

## ERROR HANDLING

### Client Disconnect

```python
try:
    while True:
        message = await websocket.receive_text()
        # Process message
except WebSocketDisconnect:
    self.subscribers.pop(websocket, None)
    logger.info("Client disconnected, removed from subscribers")
```

### Broadcast Failure

```python
try:
    await client_ws.send_json(message)
except Exception as e:
    logger.error(f"Send failed: {e}")
    # Remove dead client
    dead_clients.append(client_ws)
    # Client will reconnect if needed
```

### Queue Overflow

```python
if len(self.pending_updates) > 1000:
    logger.warning("Update queue full - consider polling API")
    # Old clients may miss updates
    # They can use REST API to catch up
```

---

## TESTING SCENARIOS

### Test 1: Single Subscriber

```
1. Connect WebSocket client
2. Subscribe to BOT-002
3. Queue file task
4. Verify: Client receives task_completed message
5. Verify: Message arrives <100ms after task completes
```

### Test 2: Multiple Subscribers

```
1. Connect 3 WebSocket clients
2. All subscribe to BOT-002
3. Queue file task
4. Verify: All 3 clients receive update
5. Verify: No message loss or duplicates
```

### Test 3: Filtered Subscription

```
1. Client A subscribes to source=file
2. Client B subscribes to source=websocket
3. Queue file task + send WebSocket task
4. Verify: A only gets file update
5. Verify: B only gets WebSocket update
```

### Test 4: Disconnect and Reconnect

```
1. Client connected, receiving updates
2. Client network drops
3. Task completes offline
4. Client reconnects and re-subscribes
5. Verify: Client receives recent entries from timeline API
```

### Test 5: Long-Running Task

```
1. Start 60-second task
2. Task sends progress at 25%, 50%, 75%
3. Verify: Client receives progress messages
4. Verify: Timing is accurate
```

### Test 6: Heartbeat Keep-Alive

```
1. Connect client
2. No activity for 60 seconds
3. Client sends ping every 30 seconds
4. Verify: Connection stays alive
5. Verify: Server responds with pong
```

---

## CLIENT EXAMPLE (JavaScript)

```javascript
const ws = new WebSocket('ws://localhost:8002/ws/bot/BOT-002/timeline');

ws.onopen = async (event) => {
  // Subscribe with filters
  ws.send(JSON.stringify({
    type: 'subscribe',
    bot_id: 'BOT-002',
    filters: {
      source: 'file',
      success: true
    }
  }));

  // Heartbeat every 30 seconds
  setInterval(() => {
    ws.send(JSON.stringify({ type: 'ping' }));
  }, 30000);
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  switch (message.type) {
    case 'subscribed':
      console.log('Connected!', message.initial_entries);
      break;

    case 'task_completed':
      console.log('Task done:', message.entry.task_id);
      updateUI(message.entry);
      break;

    case 'progress':
      console.log(`Progress: ${message.percent}%`);
      updateProgress(message.percent, message.message);
      break;

    case 'task_started':
      console.log('Task started:', message.task_id);
      break;

    case 'task_failed':
      console.error('Task failed:', message.error);
      break;

    case 'pong':
      console.log('Heartbeat OK');
      break;
  }
};

ws.onerror = (event) => {
  console.error('WebSocket error:', event);
};

ws.onclose = (event) => {
  console.log('WebSocket closed - will reconnect');
  // Implement reconnect logic
};
```

---

## IMPLEMENTATION CHECKLIST

- [ ] TimelineService class created
- [ ] add_entry() saves and broadcasts
- [ ] subscribe() adds to subscribers and sends initial entries
- [ ] unsubscribe() removes from subscribers
- [ ] _broadcast_update() filters and sends to all clients
- [ ] Progress message support
- [ ] Heartbeat/ping-pong implemented
- [ ] Error handling for dead connections
- [ ] BotRunner integration (calls timeline_service.add_entry())
- [ ] Response format matches specification
- [ ] All message types implemented
- [ ] Tests pass for all scenarios

---

## COMPLEXITY & EFFORT

**Specification (BOT-002):** ✅ Complete (this document)

**Implementation (Developer):**
- TimelineService class: 1.5 hours
- WebSocket handlers: 1 hour
- BotRunner integration: 30 minutes
- Testing: 1 hour
- **Total: 4 hours**

---

## BENEFITS

✅ Real-time updates to Commandeer dashboard
✅ No polling needed (efficient)
✅ Multiple clients can subscribe simultaneously
✅ Filtering reduces unnecessary messages
✅ Progress updates for long tasks
✅ Graceful error handling
✅ Scalable to many subscribers

---

## SUMMARY

✅ **Message Protocol:** Complete specification
✅ **Architecture:** Data flow defined
✅ **Filtering:** Implementation detailed
✅ **Error Handling:** Strategies provided
✅ **Testing:** Scenarios specified
✅ **Client Example:** JavaScript provided

**Ready for developer implementation.**

---

