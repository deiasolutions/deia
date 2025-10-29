# TASK-002-014: Unified Timeline API - ANALYSIS & SPECIFICATION

**Task ID:** TASK-002-014
**Bot ID:** BOT-002
**Priority:** P1
**Status:** ANALYSIS COMPLETE
**Date:** 2025-10-28T14:45:00Z
**Depends on:** TASK-002-011, TASK-002-012

---

## OBJECTIVE

Design REST API + WebSocket endpoint for unified timeline that merges file-based and WebSocket responses into single chronological view.

**Result:** Commandeer can display all bot interactions (async file tasks + real-time chat) in one conversation timeline.

---

## API SPECIFICATION

### Endpoint 1: REST API Timeline

**Route:** `GET /api/bot/{bot_id}/timeline`

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | int | 100 | Max entries per page |
| offset | int | 0 | Pagination offset |
| source | str | null | Filter: "file" or "websocket" |
| start_time | str | null | ISO timestamp (filter after) |
| end_time | str | null | ISO timestamp (filter before) |
| success | bool | null | Filter: true/false only |

**Response (200 OK):**

```json
{
  "bot_id": "BOT-002",
  "total_count": 150,
  "entries_count": 100,
  "offset": 0,
  "limit": 100,
  "has_more": true,
  "entries": [
    {
      "task_id": "TASK-002-011",
      "bot_id": "BOT-002",
      "source": "file",
      "timestamp": "2025-10-28T14:05:30Z",
      "success": true,
      "response": "HTTP server implementation complete",
      "files_modified": ["src/deia/adapters/bot_http_server.py"],
      "duration_seconds": 1200,
      "error": null
    },
    {
      "task_id": "WS-abc123",
      "bot_id": "BOT-002",
      "source": "websocket",
      "timestamp": "2025-10-28T14:06:15Z",
      "success": true,
      "response": "User asked about timeline, bot explained",
      "files_modified": [],
      "duration_seconds": 2,
      "error": null
    }
  ],
  "timestamp": "2025-10-28T14:07:00Z"
}
```

**Error Responses:**
- 400: Bad parameters (invalid limit, offset, etc.)
- 404: Bot not found
- 500: Server error

---

### Endpoint 2: WebSocket Timeline Streaming

**Route:** `WebSocket /ws/bot/{bot_id}/timeline`

**Connection Message (Client):**

```json
{
  "type": "subscribe",
  "bot_id": "BOT-002",
  "from_timestamp": "2025-10-28T14:00:00Z"  // Optional: only new entries
}
```

**Update Message (Server):**

```json
{
  "type": "update",
  "entry": {
    "task_id": "TASK-002-012",
    "bot_id": "BOT-002",
    "source": "file",
    "timestamp": "2025-10-28T14:06:30Z",
    "success": true,
    "response": "Response tagging complete",
    "files_modified": ["src/deia/adapters/bot_runner.py"],
    "duration_seconds": 600,
    "error": null
  }
}
```

**Heartbeat (Server → every 30 seconds):**

```json
{
  "type": "ping"
}
```

**Heartbeat Response (Client):**

```json
{
  "type": "pong"
}
```

---

## DATA MODEL

### Timeline Entry Format

**Standard JSON structure for all responses:**

```json
{
  "task_id": "TASK-002-011",                    // Unique ID
  "bot_id": "BOT-002",                          // Which bot
  "source": "file|websocket",                   // Where from
  "timestamp": "2025-10-28T14:05:30Z",          // Completion time (UTC)
  "success": true|false,                        // Status
  "response": "Task output text",               // Response content
  "files_modified": ["path/to/file1.py"],       // Files changed
  "duration_seconds": 300,                      // Execution time
  "error": null|"error message"                 // Error if failed
}
```

**Key fields:**
- `timestamp`: ISO 8601 with Z (UTC)
- `source`: Always either "file" or "websocket" (no null)
- `success`: Boolean (true/false, no null)
- `error`: Null if success=true, error message if success=false

---

## PERSISTENCE STRATEGY

### Challenge: WebSocket Responses Currently Lost

When bot sends WebSocket response to client, it's not persisted. Timeline API can't retrieve it later.

### Recommended Solution: Timeline Append-Only Log

**File:** `.deia/bot-logs/BOT-002-timeline.jsonl`

**Format:** One JSON entry per line (JSONL format)

**When to write:**
1. After file task completes → write to timeline.jsonl
2. After WebSocket task completes → write to timeline.jsonl

**Benefits:**
- Simple append-only (no conflicts)
- Easy to parse (one JSON per line)
- Works with existing log infrastructure
- Survives restarts
- Fast sequential reads

**Implementation:**

```python
def persist_timeline_entry(entry):
    """Add entry to timeline log"""
    timeline_file = Path(".deia/bot-logs/BOT-002-timeline.jsonl")

    # Ensure directory exists
    timeline_file.parent.mkdir(parents=True, exist_ok=True)

    # Append entry as JSON line
    with open(timeline_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')
```

---

## IMPLEMENTATION ARCHITECTURE

### Data Flow Diagram

```
┌──────────────────────────────────────┐
│  GET /api/bot/BOT-002/timeline       │
│  WebSocket /ws/bot/BOT-002/timeline  │
└────────────┬─────────────────────────┘
             │
      ┌──────┴──────┬──────────┬───────────────┐
      │             │          │               │
   Read File    Read Timeline  Read Activity   Merge
   Responses    JSONL Log      Log             & Sort
      │             │          │               │
   .deia/hive/  .deia/bot-   .deia/bot-logs  By
   responses/   logs/         activity.jsonl  timestamp
                timeline.jsonl                │
      └──────────────────┬────────────────────┘
                         │
                  ┌──────┴──────┐
                  │             │
              REST API      WebSocket
              Paginate      Stream
              (limit/offset) (broadcast)
                  │             │
              Return 100    Send updates
              with has_more  to clients
```

### Three Data Sources

**Source 1: File Responses**
- Location: `.deia/hive/responses/TASK-002-*.md`
- Format: Markdown with embedded JSON
- Parse: Extract JSON portion
- When to use: Historical data, audit trail

**Source 2: Timeline JSONL Log**
- Location: `.deia/bot-logs/BOT-002-timeline.jsonl`
- Format: One JSON entry per line
- Parse: Line-by-line JSON
- When to use: Primary source (both file + WebSocket)

**Source 3: Activity Log** (optional)
- Location: `.deia/bot-logs/BOT-002-activity.jsonl`
- Format: One activity event per line
- When to use: Lightweight entries if needed

---

## SERVICE ARCHITECTURE

### TimelineService Class

**New module:** `src/deia/services/timeline_service.py`

```python
class TimelineService:
    def __init__(self, bot_id, log_dir, response_dir):
        self.bot_id = bot_id
        self.log_dir = log_dir
        self.response_dir = response_dir
        self.subscribers = set()  # WebSocket clients

    async def get_timeline(self, limit=100, offset=0, filters=None):
        """Get paginated timeline entries"""
        # 1. Read all entries from timeline.jsonl
        # 2. Apply filters (source, time range, success)
        # 3. Sort by timestamp (newest first)
        # 4. Slice for pagination
        # 5. Return with metadata

    async def add_entry(self, entry):
        """Add new entry and broadcast to subscribers"""
        # 1. Save to timeline.jsonl
        # 2. Broadcast to all WebSocket subscribers
        # 3. Log the addition

    async def subscribe(self, websocket, from_timestamp=None):
        """Handle new WebSocket subscriber"""
        # 1. Add to subscribers set
        # 2. Send recent entries (optional: from_timestamp)
        # 3. Start listening for messages
        # 4. Clean up on disconnect

    def _read_timeline_file(self):
        """Read all entries from timeline.jsonl"""
        entries = []
        with open(self.log_dir / f"{self.bot_id}-timeline.jsonl") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        return entries

    def _filter_entries(self, entries, filters):
        """Apply filters: source, time range, success"""
        filtered = entries

        if filters.get('source'):
            filtered = [e for e in filtered
                       if e['source'] == filters['source']]

        if filters.get('start_time'):
            start = datetime.fromisoformat(filters['start_time'])
            filtered = [e for e in filtered
                       if datetime.fromisoformat(e['timestamp']) >= start]

        if filters.get('end_time'):
            end = datetime.fromisoformat(filters['end_time'])
            filtered = [e for e in filtered
                       if datetime.fromisoformat(e['timestamp']) <= end]

        if filters.get('success') is not None:
            filtered = [e for e in filtered
                       if e['success'] == filters['success']]

        return filtered
```

---

## FILTERING EXAMPLES

**Get only file responses:**
```
GET /api/bot/BOT-002/timeline?source=file
```

**Get only WebSocket responses:**
```
GET /api/bot/BOT-002/timeline?source=websocket
```

**Get entries from specific time range:**
```
GET /api/bot/BOT-002/timeline?start_time=2025-10-28T14:00:00Z&end_time=2025-10-28T15:00:00Z
```

**Get only successful responses:**
```
GET /api/bot/BOT-002/timeline?success=true
```

**Get failed responses:**
```
GET /api/bot/BOT-002/timeline?success=false
```

**Combine multiple filters:**
```
GET /api/bot/BOT-002/timeline?source=file&success=true&limit=50&offset=100
```

---

## PAGINATION STRATEGY

**Problem:** Timeline could have 1000+ entries. Don't load all at once.

**Solution:** Pagination with default 100 entries

**Curl examples:**

```bash
# Get first 100 entries
curl http://localhost:8002/api/bot/BOT-002/timeline

# Get next 100 entries
curl http://localhost:8002/api/bot/BOT-002/timeline?offset=100

# Get first 50 entries
curl http://localhost:8002/api/bot/BOT-002/timeline?limit=50

# Get entries 200-250
curl http://localhost:8002/api/bot/BOT-002/timeline?limit=50&offset=200
```

**Response includes:**
- `total_count`: Total entries in timeline
- `entries_count`: Entries in this response
- `offset`: Current offset
- `limit`: Limit requested
- `has_more`: Boolean (true if more entries exist)

---

## PERFORMANCE CONSIDERATIONS

### Memory Management

- Don't load all 1000+ entries into memory at once
- Read file line-by-line when possible
- Cache recent entries (last 50) in memory
- Implement LRU cache for frequently accessed time ranges

### Response Time SLA

- REST API: <500ms for limit=100
- WebSocket broadcast: <1 second latency
- Goal: New entries appear in timeline within 1 second

### WebSocket Scaling

**Multiple clients scenario:**
```
10 clients connected to /ws/timeline
New entry completed
→ Broadcast to all 10 clients simultaneously
→ Each receives within <1 second
```

**Implementation:**
- Use `asyncio.Queue` for broadcast
- `asyncio.gather()` to send to multiple clients
- Graceful cleanup on disconnect

---

## TESTING SCENARIOS

### Test 1: File Task Timeline

```bash
# 1. Queue file task
cat > .deia/hive/tasks/BOT-002/TASK-002-100.md << 'EOF'
# TASK-002-100: Timeline Test Task

**Sprint:** SPRINT-2025-10-28
**Expires:** 2025-10-29T23:59:59Z

Test timeline API
EOF

# 2. Wait for completion
sleep 5

# 3. Query timeline
curl http://localhost:8002/api/bot/BOT-002/timeline

# 4. Verify:
# - Response includes TASK-002-100
# - source: "file"
# - timestamp present
# - success: true/false
```

### Test 2: WebSocket Task Timeline

```bash
# 1. Connect to WebSocket /ws endpoint
# 2. Send: {"type": "task", "command": "test"}
# 3. Query timeline API
# 4. Verify: WS-task appears with source: "websocket"
```

### Test 3: Mixed Timeline

```bash
# 1. Queue file task
# 2. While processing, send WebSocket task
# 3. Query timeline
# 4. Verify: Both appear, sorted by timestamp
```

### Test 4: Pagination

```bash
# 1. Create 250 entries
# 2. GET /timeline?limit=100&offset=0 → First 100
# 3. GET /timeline?limit=100&offset=100 → Next 100
# 4. GET /timeline?limit=100&offset=200 → Last 50
# 5. Verify: has_more flags, no duplicates
```

### Test 5: WebSocket Streaming

```bash
# 1. Open WebSocket /ws/timeline
# 2. Queue file task
# 3. Verify: Receive "update" message before REST API returns
```

---

## INTEGRATION POINTS

**BotRunner modifications needed:**
1. After each task completes, call `timeline_service.add_entry()`
2. Pass both file and WebSocket responses
3. Entry is persisted and broadcast

**HTTP Server modifications needed:**
1. Add TimelineService instance
2. Add GET /api/bot/{bot_id}/timeline endpoint
3. Add WebSocket /ws/bot/{bot_id}/timeline endpoint

---

## COMPLEXITY & EFFORT

**Specification (BOT-002):** ✅ Complete (this document)

**Implementation (Developer):**
- TimelineService class: 2 hours
- REST endpoint: 1 hour
- WebSocket endpoint: 1 hour
- Testing: 1 hour
- **Total: 5 hours**

---

## WHAT ENABLES THIS

**Prerequisites (completed):**
- ✅ TASK-002-011: HTTP server (FastAPI infrastructure)
- ✅ TASK-002-012: Response tagging (source + timestamp)
- ✅ TASK-002-013: Priority queue (ensures responses are persisted)

**Unblocks:**
- Commandeer UI: Can query timeline and display conversation
- Analytics: Can analyze bot behavior over time
- Audit trail: Complete record of all bot interactions
- Timeline filtering/search: Can find specific responses

---

## SUMMARY

✅ **API Specification:** Complete
✅ **Data Model:** Defined
✅ **Persistence Strategy:** Recommended (timeline.jsonl)
✅ **Service Architecture:** Designed
✅ **Implementation Examples:** Provided
✅ **Testing Plan:** Specified

**Ready for developer implementation.**

---

