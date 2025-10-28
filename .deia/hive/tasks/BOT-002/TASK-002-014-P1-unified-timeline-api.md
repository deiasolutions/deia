# TASK-002-014: Unified Timeline API Specification

**Task ID:** TASK-002-014
**Bot ID:** BOT-002
**Priority:** P1
**Created:** 2025-10-28
**Timeout:** 300 seconds
**Depends on:** TASK-002-011, TASK-002-012

---

## OBJECTIVE

Design and specify a unified timeline REST API endpoint that merges both file-based and WebSocket responses into a single chronological view. This enables Commandeer dashboard to display all bot interactions (async + real-time) in one place.

---

## BACKGROUND

**Current State:**
- File queue responses written to `.deia/hive/responses/TASK-*.md`
- WebSocket responses only sent to client (not persisted for timeline)
- No unified view combining both sources

**Desired State:**
- REST API endpoint: `GET /api/bot/{bot_id}/timeline`
- Returns paginated list of all responses (file + WebSocket)
- Sorted chronologically with source tags
- WebSocket streaming version for real-time updates
- Supports filtering by source (file or websocket)

**Why It Matters:**
- Commandeer can display unified conversation view
- Audit trail of all bot interactions
- No context loss between async and real-time work
- Enables analytics and monitoring

---

## IMPLEMENTATION REQUIREMENTS

### 1. REST API Endpoint

**Endpoint:** `GET /api/bot/{bot_id}/timeline`

**Query Parameters:**
- `limit` (default 100): Max entries to return
- `offset` (default 0): Pagination offset
- `source` (optional): Filter by "file" or "websocket"
- `start_time` (optional): ISO timestamp for filtering
- `end_time` (optional): ISO timestamp for filtering

**Response Format:**

```json
{
  "bot_id": "BOT-002",
  "total_count": 1500,
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
      "response": "Implementation complete...",
      "files_modified": ["bot_runner.py"],
      "duration_seconds": 1200
    },
    {
      "task_id": "WS-abc123",
      "bot_id": "BOT-002",
      "source": "websocket",
      "timestamp": "2025-10-28T14:06:15Z",
      "success": true,
      "response": "User asked: hello, bot responded: Hi there!",
      "files_modified": [],
      "duration_seconds": 2
    }
  ],
  "timestamp": "2025-10-28T14:07:00Z"
}
```

**Status Codes:**
- 200: Success
- 400: Bad parameters
- 404: Bot not found
- 500: Server error

---

### 2. WebSocket Streaming Endpoint

**Endpoint:** `WebSocket /ws/bot/{bot_id}/timeline`

**Subscribe to real-time updates:**

Client subscribes and receives new timeline entries as they complete.

**Initial Connection Message:**

```json
{
  "type": "subscribe",
  "bot_id": "BOT-002",
  "from_timestamp": "2025-10-28T14:00:00Z" (optional)
}
```

**Server Response Format:**

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
    "files_modified": ["bot_runner.py"],
    "duration_seconds": 600
  }
}
```

**Heartbeat (every 30 seconds):**

```json
{
  "type": "ping"
}
```

---

### 3. Data Sources for Timeline

**Source 1: File Responses**
- Read from `.deia/hive/responses/TASK-002-*.md`
- Parse markdown + JSON format
- Extract: task_id, source="file", timestamp, success, response
- Sort by timestamp

**Source 2: WebSocket Responses**
- Currently not persisted (problem!)
- Option A: Save to file queue when task completes
- Option B: Save to separate log (bot_timeline.jsonl)
- **Recommendation:** Option A (use existing file infrastructure)

**Source 3: Activity Log (optional)**
- `.deia/bot-logs/BOT-002-activity.jsonl`
- Alternative source for timeline entries
- More lightweight than full responses

---

### 4. Timeline Entry Format

**Standard format for both sources:**

```json
{
  "task_id": "TASK-002-011",           // Unique identifier
  "bot_id": "BOT-002",                 // Which bot
  "source": "file|websocket",          // Where it came from
  "timestamp": "2025-10-28T14:05:30Z", // When it completed (UTC)
  "success": true|false,               // Did it succeed?
  "response": "...",                   // What was the output
  "files_modified": ["path/to/file"],  // Any files changed
  "duration_seconds": 300,             // How long it took
  "error": null|"error message"        // If failed, why?
}
```

---

### 5. Persistence Strategy

**Problem:** WebSocket responses currently lost after sent to client

**Solution Options:**

**Option A: Persist to timeline.jsonl** (Recommended)
```
.deia/bot-logs/BOT-002-timeline.jsonl

Each line: JSON timeline entry
Append-only log
One entry per task/response
```

**Option B: Persist to file responses**
```
Keep existing `.deia/hive/responses/TASK-002-*.md` files
Add WebSocket responses with WS- prefix
e.g., WS-2025-10-28-14-05-30.md
```

**Option C: Save to database**
```
sqlite: .deia/bot-logs/BOT-002-timeline.db
Table: timeline_entries
Indexed by timestamp
```

**Recommendation:** Option A (timeline.jsonl)
- Simple append-only format
- No database needed
- Works with existing log infrastructure
- Can be easily parsed
- Survives restarts

---

### 6. Implementation Architecture

```
┌─────────────────────────────────┐
│  API Endpoint: GET /timeline    │
│  WebSocket: /ws/timeline        │
└──────────┬──────────────────────┘
           │
      ┌────┴─────┬────────┬────────────┐
      │           │        │            │
  Read File    Read WS   Read Activity Merge & Sort
  Responses    Log       Log           by timestamp
      │           │        │            │
      └────────────┴────────┴────────────┘
                   │
            ┌──────┴──────┐
            │             │
        Paginate      Stream
        (REST)       (WebSocket)
           │             │
        Return 100   Broadcast to
        with pagination clients
```

---

### 7. Filtering & Search

**Supported filters:**

```python
# By source
GET /api/bot/BOT-002/timeline?source=file
GET /api/bot/BOT-002/timeline?source=websocket

# By time range
GET /api/bot/BOT-002/timeline?start_time=2025-10-28T14:00:00Z&end_time=2025-10-28T15:00:00Z

# By success/failure
GET /api/bot/BOT-002/timeline?success=true
GET /api/bot/BOT-002/timeline?success=false

# Combined
GET /api/bot/BOT-002/timeline?source=file&success=true&limit=50&offset=100
```

---

### 8. Performance Considerations

**Large timeline handling:**
- Don't load all 1000+ entries at once
- Paginate: limit=100, offset=N
- Index by timestamp in database (if using DB)
- Cache recent entries (last 50) in memory

**WebSocket scaling:**
- Multiple clients subscribed to same timeline
- Broadcast updates to all subscribers
- Use asyncio.Queue for updates
- Clean up disconnected clients

**Metrics to track:**
- Timeline size growth rate
- API response time (should be <500ms)
- WebSocket subscription count
- Update latency (when does new entry appear?)

---

### 9. Testing Scenarios

**Test 1: File-only timeline**
```
Queue file task → Wait for response → GET /timeline
Verify: Response appears with source="file"
```

**Test 2: WebSocket-only timeline**
```
Send via WebSocket → GET /timeline
Verify: Response appears with source="websocket"
```

**Test 3: Mixed timeline**
```
Queue file task while WebSocket active
GET /timeline → Should show both, sorted by timestamp
```

**Test 4: Pagination**
```
GET /timeline?limit=10&offset=0 → Get first 10
GET /timeline?limit=10&offset=10 → Get next 10
Verify: No duplicates, correct ordering
```

**Test 5: WebSocket streaming**
```
Open WebSocket connection
Queue file task
Verify: WebSocket receives update in real-time
```

---

### 10. Code Structure Recommendations

**New module:** `src/deia/services/timeline_service.py`

```python
class TimelineService:
    def __init__(self, bot_id, response_dir, log_dir):
        self.bot_id = bot_id
        self.response_dir = response_dir
        self.log_dir = log_dir
        self.subscribers = set()  # WebSocket clients

    async def get_timeline(self, limit=100, offset=0, filters=None):
        """Get paginated timeline"""
        # Read files/logs
        # Filter and sort
        # Return paginated

    async def add_entry(self, entry):
        """Add entry and broadcast to subscribers"""
        # Save to timeline.jsonl
        # Broadcast to WebSocket subscribers

    async def subscribe(self, websocket):
        """Handle WebSocket subscription"""
        # Add to subscribers
        # Send initial entries
        # Listen for messages
```

---

## ACCEPTANCE CRITERIA

✅ **REST API Working:**
- [ ] GET /api/bot/BOT-002/timeline returns 200
- [ ] Response includes pagination info (total_count, offset, limit)
- [ ] Entries are sorted by timestamp (newest first or oldest first?)
- [ ] Response format matches specification

✅ **Filtering:**
- [ ] source parameter filters correctly
- [ ] time range filtering works
- [ ] Success/failure filtering works
- [ ] Multiple filters can combine

✅ **Pagination:**
- [ ] limit parameter controls response size
- [ ] offset parameter works
- [ ] has_more indicates if more data exists
- [ ] No missing or duplicate entries

✅ **WebSocket Streaming:**
- [ ] /ws/bot/BOT-002/timeline accepts connections
- [ ] Sends initial timeline on connect
- [ ] Broadcasts new entries to subscribers
- [ ] Handles disconnections cleanly

✅ **Data Persistence:**
- [ ] New responses automatically added to timeline
- [ ] Both file and WebSocket responses included
- [ ] Timestamps are accurate
- [ ] Source tags are correct

✅ **Performance:**
- [ ] API response time <500ms for limit=100
- [ ] WebSocket broadcast <1 second latency
- [ ] No memory leaks with many subscribers
- [ ] Handles large timelines (1000+ entries)

---

## DELIVERABLES

1. **Specification document** (.deia/hive/responses/TASK-002-014-timeline-api-analysis.md)
2. **Code examples:**
   - REST endpoint implementation
   - WebSocket handler
   - Timeline service class
3. **API documentation:**
   - Endpoint specs with curl examples
   - WebSocket message format
   - Filter examples
4. **Data model:**
   - Timeline entry JSON schema
   - Storage format (jsonl)
   - Database schema (if using DB)

---

## DEPENDENCIES

**Depends on:**
- TASK-002-011: HTTP server (for REST + WebSocket infrastructure)
- TASK-002-012: Response tagging (for source field and timestamps)

**Blocks:**
- Commandeer UI timeline display (needs this API)
- Timeline filtering/search features
- Analytics dashboard

---

## EFFORT ESTIMATE

**Specification (BOT-002):** 1-2 hours
**Implementation (Developer):** 3-4 hours

---

**Status:** Ready for analysis by BOT-002
**Assigned to:** BOT-002
**Priority:** P1

