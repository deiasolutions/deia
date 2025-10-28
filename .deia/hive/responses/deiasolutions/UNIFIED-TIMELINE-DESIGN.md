# UNIFIED TIMELINE ARCHITECTURE

**Purpose:** Design for Commandeer UI to display mixed file-based and WebSocket/chat responses in single conversation timeline

**Status:** Design Complete
**Date:** 2025-10-28

---

## 1. DATA MODEL

### Timeline Entry Schema

Each timeline entry represents either a file-based response or a chat/WebSocket response:

```typescript
interface TimelineEntry {
    // Identity
    entry_id: string;              // Unique: TASK-ID or CHAT-ID
    timestamp: string;             // ISO 8601: "2025-10-28T14:18:30Z"

    // Source Information
    source: "file" | "chat";       // Where did this come from?
    bot_id: string;                // Which bot generated it

    // For File-Based Responses
    task_id?: string;              // TASK-002-001 (if source === "file")
    priority?: "P0" | "P1" | "P2"; // Task priority

    // For Chat Responses
    sender?: string;               // "Q33N" or "BOT-002" (if source === "chat")
    sender_type?: "user" | "bot";  // Who is speaking

    // Content
    content: string;               // Response text/markdown

    // Status
    success?: boolean;             // Did task succeed? (file only)
    duration_seconds?: number;     // How long did task take? (file only)

    // Metadata
    files_modified?: string[];     // Which files changed?
    error?: string;                // If something went wrong
}
```

### Timeline Collection

```typescript
interface Timeline {
    entries: TimelineEntry[];      // All entries, sorted by timestamp
    bot_id: string;                // Which bot's timeline
    first_entry: string;           // Oldest timestamp
    last_entry: string;            // Newest timestamp
    total_entries: number;         // Count
    file_responses: number;        // Count of file source
    chat_responses: number;        // Count of chat source
}
```

### Distinguishing File vs Chat Responses

| Attribute | File-Based | Chat-Based |
|-----------|-----------|-----------|
| `source` | "file" | "chat" |
| `task_id` | TASK-002-001 | null |
| `sender` | null | "Q33N" or "BOT-002" |
| `sender_type` | null | "user" or "bot" |
| Priority | P0/P1/P2 | null |
| Duration | Seconds | null |

### Timestamp Ordering

**Rule:** Timeline entries sorted by `timestamp` (ascending = oldest first)

```
Timeline (sorted by timestamp):
[14:18:00] File response (TASK-002-001, P1)
[14:18:15] Chat message (Q33N user)
[14:18:30] File response (TASK-002-002, P1)
[14:18:45] Chat response (BOT-002 bot)
[14:19:00] File response (TASK-002-003, P2)
```

---

## 2. RETRIEVAL ARCHITECTURE

### API Endpoint Design

#### Option A: REST Polling (Simple, Synchronous)

```http
GET /api/bot/{bot_id}/timeline
GET /api/bot/{bot_id}/timeline?after=2025-10-28T14:00:00Z
GET /api/bot/{bot_id}/timeline?limit=50&offset=0
```

**Response:**
```json
{
    "bot_id": "BOT-002",
    "entries": [
        {
            "entry_id": "TASK-002-001",
            "timestamp": "2025-10-28T14:18:00Z",
            "source": "file",
            "task_id": "TASK-002-001",
            "priority": "P1",
            "bot_id": "BOT-002",
            "content": "Checkin complete: BOT-002 operational",
            "success": true,
            "duration_seconds": 45
        },
        {
            "entry_id": "CHAT-001",
            "timestamp": "2025-10-28T14:18:15Z",
            "source": "chat",
            "sender": "Q33N",
            "sender_type": "user",
            "content": "Good. Now verify the framework."
        }
    ],
    "total_entries": 50,
    "first_entry": "2025-10-28T14:00:00Z",
    "last_entry": "2025-10-28T14:25:00Z"
}
```

**Pros:** Simple, easy to implement
**Cons:** Polling lag, potential missed messages

#### Option B: WebSocket Streaming (Real-Time, Preferred)

```
GET /ws/bot/{bot_id}/timeline
```

**Connection:** Establishes WebSocket, receives streaming timeline events

**Message Format:**
```json
{
    "type": "timeline_event",
    "event_type": "entry_added",
    "entry": {
        "entry_id": "TASK-002-002",
        "timestamp": "2025-10-28T14:18:30Z",
        "source": "file",
        ...
    }
}
```

**Events:**
- `entry_added` - New response arrived
- `entry_updated` - Response status changed (e.g., task completed)
- `timeline_snapshot` - Initial full timeline on connect
- `entry_error` - Error in timeline entry

**Pros:** Real-time, no polling, efficient
**Cons:** Requires WebSocket implementation

#### Option C: Hybrid (REST + WebSocket)

1. **Initial load:** REST GET to fetch existing timeline
2. **New entries:** WebSocket stream for live updates
3. **Best of both:** Full history + real-time updates

**RECOMMENDED:** This approach

---

### Implementation Steps (Retrieval)

**In BotService (`.src/deia/services/bot_service.py`):**

1. **Add timeline endpoint:**
```python
@app.get("/api/bot/{bot_id}/timeline")
async def get_timeline(bot_id: str, after: Optional[str] = None):
    """Get conversation timeline for bot"""
    # Read response files from .deia/hive/responses/
    # Parse each response file
    # Extract timeline entries
    # Sort by timestamp
    # Return as TimelineEntry array
```

2. **Add WebSocket handler:**
```python
@app.websocket("/ws/bot/{bot_id}/timeline")
async def timeline_websocket(bot_id: str, websocket: WebSocket):
    """Stream timeline events via WebSocket"""
    # Send initial timeline snapshot
    # Monitor for new response files
    # Stream new entries as they appear
    # Handle client disconnect
```

3. **File monitoring:**
```python
async def watch_response_files(bot_id: str):
    """Monitor .deia/hive/responses/ for new files"""
    # Use os.stat or watchdog library
    # Detect new response files
    # Parse and extract timeline entries
    # Broadcast to connected WebSocket clients
```

---

## 3. DISPLAY ORDER

### Should File Responses Appear in Timeline?

**YES** - File-based responses are first-class timeline entries.

Rationale:
- Users need to see task completions
- Provides context for chat messages
- Enables complete conversation history
- Supports audit trail / accountability

### Handling Async vs Real-Time

**Timeline merges both:**
- File responses: Added when response file appears (async)
- Chat responses: Added immediately (real-time)
- Both sorted by timestamp (unified view)

**Example:**

```
Async (File-Based Tasks):
┌─────────────────────────┐
│ 14:18:00 TASK-002-001   │
│ 14:18:30 TASK-002-002   │
│ 14:19:00 TASK-002-003   │
└─────────────────────────┘

Real-Time (Chat):
┌─────────────────────────┐
│ 14:18:15 Q33N message   │
│ 14:18:45 BOT response   │
│ 14:19:15 Q33N message   │
└─────────────────────────┘

Unified Timeline:
┌─────────────────────────┐
│ 14:18:00 FILE: Task 1   │
│ 14:18:15 CHAT: Q33N     │
│ 14:18:30 FILE: Task 2   │
│ 14:18:45 CHAT: BOT      │
│ 14:19:00 FILE: Task 3   │
│ 14:19:15 CHAT: Q33N     │
└─────────────────────────┘
```

### Example Unified Timeline (Commandeer UI Display)

```
BOT-002 Timeline
═════════════════════════════════════════════════════════════

📄 14:18:00 [P1] TASK-002-001: Checkin
   "Checkin complete: BOT-002 operational"
   ✅ Success | 45 seconds

💬 14:18:15 Q33N (You)
   "Good. Now verify the framework."

📄 14:18:30 [P1] TASK-002-002: Verify Framework
   "Framework verified: 3 modes correctly defined"
   ✅ Success | 30 seconds

   Changes:
   - Updated COMMUNICATION-MODES-FRAMEWORK.md
   - Added clarification on polling interval

💬 14:18:45 BOT-002
   "Framework check complete. Found 3 modes clearly
    defined. Minor improvements needed on error handling
    docs. Ready for next task."

📄 14:19:00 [P1] TASK-002-003: Inventory Audit
   "Bot inventory & communications audit complete"
   ✅ Success | 60 seconds

   Changes:
   - Updated BOT-INVENTORY-AND-COMMUNICATIONS.md
   - Documented all 4 running systems

💬 14:19:15 Q33N (You)
   "Excellent work. Update the ScrumMaster protocol next."

📄 14:19:30 [P2] TASK-002-004: Launch Doc Template
   "Bot launch template created"
   ✅ Success | 30 seconds

   New file:
   - Created BOT-LAUNCH-DOC-TEMPLATE.md

═════════════════════════════════════════════════════════════
Total: 7 entries | 4 file responses | 3 chat messages
```

---

## 4. IMPLEMENTATION STEPS

### Phase 1: Data Preparation (Bot Runner)

**Status:** ✅ COMPLETE (TASK-002-006)

What's needed:
- ✅ Tag file responses with `source: "file"`
- ✅ Add ISO timestamp to all responses
- ✅ Add bot_id to response JSON
- ✅ Response format: JSON with required fields

**Code location:** `src/deia/adapters/bot_runner.py::run_once()`

### Phase 2: API Endpoint (BotService)

**Status:** PENDING

```python
# In src/deia/services/bot_service.py

@app.get("/api/bot/{bot_id}/timeline")
async def get_timeline(bot_id: str, limit: int = 50, offset: int = 0):
    """
    Get conversation timeline for bot.

    Returns:
        TimelineEntry[] sorted by timestamp
    """
    response_dir = Path(f".deia/hive/responses")

    # Find all response files for this bot
    response_files = [
        f for f in response_dir.glob("*.md")
        if bot_id in f.name
    ]

    # Parse each file
    entries = []
    for file in response_files:
        try:
            content = json.loads(file.read_text())
            entry = {
                "entry_id": content.get("task_id"),
                "timestamp": content.get("timestamp"),
                "source": content.get("source", "file"),
                "bot_id": content.get("bot_id"),
                "task_id": content.get("task_id"),
                "priority": content.get("priority"),
                "content": content.get("response"),
                "success": content.get("success"),
                "duration_seconds": content.get("duration_seconds"),
                "files_modified": content.get("files_modified"),
                "error": content.get("error")
            }
            entries.append(entry)
        except:
            continue

    # Sort by timestamp
    entries.sort(key=lambda e: e["timestamp"])

    # Apply pagination
    entries = entries[offset:offset+limit]

    return {
        "bot_id": bot_id,
        "entries": entries,
        "total_entries": len(entries)
    }
```

### Phase 3: WebSocket Handler (BotService)

**Status:** PENDING

```python
@app.websocket("/ws/bot/{bot_id}/timeline")
async def timeline_websocket(bot_id: str, websocket: WebSocket):
    """Stream timeline events via WebSocket"""

    # Send initial snapshot
    initial_timeline = await get_timeline(bot_id, limit=100)
    await websocket.send_json({
        "type": "timeline_snapshot",
        "entries": initial_timeline["entries"]
    })

    # Monitor for new responses
    watch_task = asyncio.create_task(
        watch_response_files(bot_id, websocket)
    )

    # Keep connection open
    try:
        while True:
            # Receive heartbeat/ping from client
            await websocket.receive_text()
    except:
        watch_task.cancel()
        await websocket.close()
```

### Phase 4: Commandeer UI Integration

**Status:** PENDING

```javascript
// In Commandeer UI (React/Vue/whatever)

async function loadTimeline(botId) {
    // Option A: Initial REST load
    const response = await fetch(`/api/bot/${botId}/timeline`);
    const timeline = await response.json();

    // Option B: WebSocket stream for live updates
    const ws = new WebSocket(`/ws/bot/${botId}/timeline`);

    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);

        if (message.type === "timeline_snapshot") {
            // Initial load
            displayTimeline(message.entries);
        } else if (message.type === "entry_added") {
            // New entry arrived
            addTimelineEntry(message.entry);
        }
    };
}

function displayTimeline(entries) {
    return entries.map(entry => {
        if (entry.source === "file") {
            return `
                <div class="timeline-entry file">
                    <span class="icon">📄</span>
                    <span class="timestamp">${formatTime(entry.timestamp)}</span>
                    <span class="task">[${entry.priority}] ${entry.task_id}</span>
                    <span class="content">${entry.content}</span>
                    <span class="status">${entry.success ? '✅' : '❌'}</span>
                </div>
            `;
        } else if (entry.source === "chat") {
            return `
                <div class="timeline-entry chat ${entry.sender_type}">
                    <span class="icon">💬</span>
                    <span class="timestamp">${formatTime(entry.timestamp)}</span>
                    <span class="sender">${entry.sender}</span>
                    <span class="content">${entry.content}</span>
                </div>
            `;
        }
    });
}
```

---

## 5. INTEGRATION POINTS

### Bot Runner Changes
- **File:** `src/deia/adapters/bot_runner.py`
- **Method:** `run_once()`
- **Change:** Add response tagging (DONE in TASK-002-006)

### BotService Changes
- **File:** `src/deia/services/bot_service.py`
- **Add:** GET `/api/bot/{bot_id}/timeline`
- **Add:** WebSocket `/ws/bot/{bot_id}/timeline`

### Commandeer UI Changes
- **Display:** Unified timeline component
- **Connect:** REST API or WebSocket client
- **Render:** Mixed file + chat entries

---

## SUMMARY

✅ **Data Model:** TimelineEntry schema defined
✅ **Retrieval:** REST API + WebSocket design specified
✅ **Display Order:** File + chat responses merged by timestamp
✅ **Example:** Real timeline shown with mixed entries
✅ **Implementation:** Code locations and pseudocode provided

**Ready for Commandeer UI implementation.**

