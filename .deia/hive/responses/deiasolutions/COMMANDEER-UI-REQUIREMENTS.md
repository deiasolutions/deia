# COMMANDEER UI REQUIREMENTS

**Purpose:** Specification for unified timeline display in Commandeer UI

**Audience:** Frontend developers implementing Commandeer chat interface

**Status:** Requirements Complete
**Date:** 2025-10-28

---

## 1. UI COMPONENTS

### Timeline Container

```
┌─────────────────────────────────────────────────────────┐
│ BOT-002 Conversation Timeline                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ [Timeline entries sorted by timestamp, oldest first]    │
│                                                          │
│ [Auto-scroll to newest entry]                           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Entry Type 1: File Response (Async Task)

```
┌──────────────────────────────────────────────────────┐
│ 📄 14:18:30 [P1] TASK-002-001: Checkin             │
├──────────────────────────────────────────────────────┤
│                                                       │
│ Checkin complete: BOT-002 operational                │
│                                                       │
│ ✅ Success | 45 seconds                             │
│                                                       │
│ [View Full Response] [Expand]                        │
│                                                       │
└──────────────────────────────────────────────────────┘
```

**Components:**
- Icon: 📄 (file/document)
- Timestamp: ISO time, human-readable (14:18:30)
- Priority badge: [P1] (color-coded: red for P0, orange for P1, gray for P2)
- Task ID: TASK-002-001
- Description: From task file
- Content: Response text (first 100 chars, clickable to expand)
- Success indicator: ✅ or ❌
- Duration: "45 seconds"
- Actions: [View Full] [Expand Details] [View File]

### Entry Type 2: Chat Input (User Message)

```
┌──────────────────────────────────────────────────────┐
│ 💬 14:18:15 Q33N (You)                              │
├──────────────────────────────────────────────────────┤
│                                                       │
│ Good. Now verify the framework.                       │
│                                                       │
└──────────────────────────────────────────────────────┘
```

**Components:**
- Icon: 💬 (chat bubble)
- Timestamp: ISO time, human-readable
- Sender: "Q33N" or user name
- User indicator: "(You)"
- Content: Chat message as typed
- Simple, minimal styling (less visual weight than bot response)

### Entry Type 3: Chat Response (Streaming)

```
┌──────────────────────────────────────────────────────┐
│ 💬 14:18:45 BOT-002 (Streaming)                      │
├──────────────────────────────────────────────────────┤
│                                                       │
│ Adding structured logging to the module...          │
│                                                       │
│ [🔴 Working] [Files: 2 modified]                     │
│                                                       │
│ [Cancel] [View Full]                                 │
│                                                       │
└──────────────────────────────────────────────────────┘
```

**Components:**
- Icon: 💬 (chat bubble)
- Timestamp: ISO time
- Sender: "BOT-002" or bot name
- Status: "(Streaming)" or "(Complete)"
- Content: Streaming response text (updated in real-time)
- Status indicator: 🔴 Working, 🟢 Complete, 🔺 Warning
- Files modified count (live update)
- Actions: [Cancel] [View Full Response]

### Timestamps

**Display format:**
- Short form: "14:18:30" (for timeline density)
- Long form: "2025-10-28 14:18:30 UTC" (on hover or details)
- Relative: "5 seconds ago" (optional, nice-to-have)

**Time zone:** UTC (as specified in ISO timestamp)

### Source Indicators

Visual distinction between file and chat:

| Source | Icon | Background | Alignment |
|--------|------|------------|-----------|
| File task | 📄 | Light gray | Left |
| Chat input | 💬 | Light blue | Right |
| Chat response | 💬 | Light green | Left |

---

## 2. TIMELINE VIEW EXAMPLE

### Full Timeline Display

```
BOT-002 Unified Conversation
═══════════════════════════════════════════════════════════════

📄 14:18:00 [P1] TASK-002-001: Checkin                    ✅ 45s
  "Checkin complete: BOT-002 operational"
  [View Full]

💬 14:18:15 Q33N (You)
  "Good. Now verify the framework."

📄 14:18:30 [P1] TASK-002-002: Verify Framework           ✅ 30s
  "Framework verified: 3 modes clearly defined"

  Changes: 3 files modified
  [View Files] [View Full]

💬 14:18:45 BOT-002
  "Framework review complete. Found all 3 modes clearly
  documented. Identified minor improvements needed on
  error handling specification. Ready for next task."

📄 14:19:00 [P1] TASK-002-003: Inventory Audit            ✅ 60s
  "Bot inventory & communications audit complete"

  Changes: BOT-INVENTORY-AND-COMMUNICATIONS.md updated
  - BOT-001 status: Idle
  - BOT-002 status: Running
  - Documentation: Complete

  [View Files] [View Full]

💬 14:19:15 Q33N (You)
  "Excellent work. Update the ScrumMaster protocol next."

💬 14:19:30 BOT-002 (Streaming) 🔴
  "Creating comprehensive ScrumMaster protocol document...

   Adding sections:
   - Bot status monitoring
   - Task queueing procedures
   - Response reading guidelines
   - Error handling procedures

   [🔴 Working - 15 seconds]"

  [Cancel] [View Full]

═══════════════════════════════════════════════════════════════
Total: 7 entries | 4 file responses | 3 chat interactions
```

---

## 3. INTERACTION FEATURES

### Can User Pause/Interrupt?

**YES** - User can pause bot via UI

**Implementation:**
```
[Pause Bot] button → Creates `.deia/hive/controls/BOT-002-PAUSE`
[Resume] button → Deletes pause file
```

**Effect:**
- Bot finishes current task
- Waits until pause file removed
- No new tasks started while paused

**UI indication:**
```
⏸️ BOT PAUSED

Current task (TASK-002-001) running...
Bot will pause after task completes.

[Resume] [Cancel Task]
```

### Can User Queue New Tasks While Bot Working?

**YES** - User can send chat prompts anytime

**Implementation:**
- Chat input box always active
- Send button enabled (never disabled)
- WebSocket receives prompt immediately
- Bot processes based on priority

**UI behavior:**
```
Chat input: [________________] [Send →]
                              ↑ Always enabled
```

### Can User View File Details Inline?

**YES** - Expandable file details

**Implementation:**
```
[View Files] link → Expand details

📄 14:18:30 [P1] TASK-002-002
  ┌─────────────────────────────┐
  │ Files Modified:             │
  ├─────────────────────────────┤
  │ ✏️ file1.py                 │
  │    Lines changed: 12-45     │
  │    [View] [Diff]            │
  │                             │
  │ ✏️ file2.py                 │
  │    Lines changed: 8-15      │
  │    [View] [Diff]            │
  └─────────────────────────────┘
```

**[View] button:** Open file in editor
**[Diff] button:** Show before/after comparison

### Search/Filter Capability?

**YES (Nice-to-have)**

**Filter options:**
```
[Filter by:]
  ☑️ File responses (tasks)
  ☑️ Chat responses (bot)
  ☑️ Chat input (you)

[Search box] [_______________]
              Keyword search
```

**Search results:** Highlight matching entries

---

## 4. WEBSOCKET/API NEEDS

### Endpoints Required

#### 1. GET Timeline Snapshot

```
GET /api/bot/{bot_id}/timeline
GET /api/bot/{bot_id}/timeline?limit=50&offset=0

Response:
{
    "bot_id": "BOT-002",
    "entries": [
        {
            "entry_id": "TASK-002-001",
            "timestamp": "2025-10-28T14:18:00Z",
            "source": "file",
            "task_id": "TASK-002-001",
            "priority": "P1",
            "content": "Checkin complete...",
            "success": true,
            "duration_seconds": 45
        },
        ...
    ],
    "total_entries": 7,
    "has_more": false
}
```

#### 2. WebSocket Timeline Stream

```
GET /ws/bot/{bot_id}/timeline

Message Type: timeline_snapshot (on connect)
{
    "type": "timeline_snapshot",
    "entries": [...]  // Full initial timeline
}

Message Type: entry_added (new response arrives)
{
    "type": "entry_added",
    "entry": {
        "entry_id": "TASK-002-004",
        "timestamp": "2025-10-28T14:19:00Z",
        "source": "file",
        ...
    }
}

Message Type: entry_chunk (streaming response)
{
    "type": "entry_chunk",
    "entry_id": "CHAT-001",
    "chunk": "Adding logging...\n"
}

Message Type: entry_complete (response done)
{
    "type": "entry_complete",
    "entry_id": "CHAT-001",
    "success": true,
    "duration": 8.5
}
```

#### 3. WebSocket Chat Input

```
POST /ws/bot/{bot_id}/prompt

Send:
{
    "type": "prompt",
    "message": "User's message here",
    "user": "Q33N"
}

Response: (Same format as entry_added + entry_chunk + entry_complete)
```

#### 4. Pause/Resume Bot

```
POST /api/bot/{bot_id}/pause
POST /api/bot/{bot_id}/resume

Creates/deletes `.deia/hive/controls/{bot_id}-PAUSE` file
```

#### 5. Get Bot Status

```
GET /api/bot/{bot_id}/status

Response:
{
    "bot_id": "BOT-002",
    "status": "working" | "idle" | "paused",
    "current_task": "TASK-002-001" | null,
    "queue_size": 3,
    "websocket_connected": true
}
```

### WebSocket Connection Flow

```
1. Client connects: GET /ws/bot/BOT-002/timeline
2. Server sends: timeline_snapshot with full history
3. Client displays initial timeline
4. Server monitors .deia/hive/responses/ for new files
5. New response file → Server sends entry_added
6. Streaming response → Server sends entry_chunk (multiple)
7. Response complete → Server sends entry_complete
8. Repeat from step 5
```

### Real-Time Streaming vs Polling

**RECOMMENDED: Real-Time Streaming (WebSocket)**

**Advantages:**
- No polling lag (entries appear instantly)
- Efficient (only sends when data changes)
- Bidirectional (client can send prompts)
- Real-time streaming responses

**Alternative: Polling (REST)**
- GET /api/bot/{bot_id}/timeline every 5 seconds
- Not ideal (lag, inefficient)
- But works if WebSocket unavailable

**Suggested Implementation: Hybrid**
1. Initial load: REST GET (full timeline)
2. Live updates: WebSocket stream

---

## 5. COMMANDEER UI LAYOUT

### Main Conversation View

```
┌────────────────────────────────────────────────────────┐
│ BOT-002 Conversation         [Status: Idle]   [⋮ Menu]│
├────────────────────────────────────────────────────────┤
│                                                         │
│ [Timeline entries here, scrollable]                    │
│                                                         │
│                                                         │
│                                                         │
├────────────────────────────────────────────────────────┤
│ [Chat input] [____________________] [Send →] [Pause]   │
│                                                         │
└────────────────────────────────────────────────────────┘
```

### Sidebar (Optional)

```
┌──────────────────┐
│ BOT-002          │
├──────────────────┤
│ Status: Working  │
│ Task: TASK-002-01│
│ Queue: 3         │
│ Time: 00:45      │
├──────────────────┤
│ [Pause] [Stop]   │
│ [Clear History]  │
│                  │
└──────────────────┘
```

---

## 6. IMPLEMENTATION CHECKLIST

### Frontend Tasks

- [ ] Timeline component (scrollable list)
- [ ] File entry display (📄 icon, priority, timestamp)
- [ ] Chat entry display (💬 icon, sender, message)
- [ ] Streaming animation (for real-time responses)
- [ ] Expand/collapse for file details
- [ ] Auto-scroll to latest entry
- [ ] Timestamp formatting (short/long form)
- [ ] Color-coded priority badges
- [ ] Status indicators (✅ ❌ 🔴 🟢)
- [ ] Chat input box + send button
- [ ] Pause/resume buttons

### API/WebSocket Tasks

- [ ] GET /api/bot/{bot_id}/timeline endpoint
- [ ] WebSocket /ws/bot/{bot_id}/timeline handler
- [ ] File monitoring (watch .deia/hive/responses/)
- [ ] Message streaming (entry_chunk format)
- [ ] WebSocket /ws/bot/{bot_id}/prompt handler
- [ ] Pause/resume endpoints
- [ ] Status endpoint

### Integration Tasks

- [ ] Connect Commandeer to REST API
- [ ] Connect Commandeer to WebSocket
- [ ] Test with BOT-002
- [ ] Test timeline with mixed file + chat
- [ ] Test real-time streaming
- [ ] Test pause/resume
- [ ] Performance testing (large timeline)

---

## 7. SUCCESS CRITERIA

✅ Timeline displays file and chat entries mixed
✅ Entries sorted by timestamp (oldest first)
✅ Real-time updates via WebSocket
✅ User can send chat prompts anytime
✅ User can pause/resume bot
✅ File response details expandable
✅ Success/failure indicators visible
✅ Timestamps clearly displayed
✅ Visual distinction between entry types

---

