# TASK-002-009: Commandeer UI Requirements - COMPLETE

**Task ID:** TASK-002-009
**Bot ID:** BOT-002
**Priority:** P2
**Status:** COMPLETE
**Completed:** 2025-10-28T14:27:00Z
**Duration:** 75 seconds

---

## DELIVERABLE

Created: `.deia/hive/responses/deiasolutions/COMMANDEER-UI-REQUIREMENTS.md`

Complete UI/UX specification for unified timeline in Commandeer.

---

## REQUIREMENTS SUMMARY

### 1. UI Components

**File Response Entry (Async Task):**
- 📄 Icon + timestamp + [P1] priority badge
- Task ID and description
- Success indicator (✅ or ❌)
- Duration ("45 seconds")
- [View Full] [Expand] [View File] actions

**Chat Input Entry (User Message):**
- 💬 Icon + timestamp
- Sender: "Q33N (You)"
- Message text (simple styling)

**Chat Response Entry (Streaming):**
- 💬 Icon + timestamp
- Sender: "BOT-002"
- Status: "(Streaming)" or "(Complete)"
- Live-updated content
- Status indicator: 🔴 Working / 🟢 Complete
- Files modified count
- [Cancel] [View Full] actions

**Source Indicators:**
- File: 📄 (light gray background)
- Chat input: 💬 (light blue background)
- Chat response: 💬 (light green background)

---

### 2. Timeline View Example

Full mixed timeline provided showing:
- File responses (TASK-002-001, -002, -003)
- Chat messages (Q33N prompts)
- Chat responses (BOT-002 streaming)
- All sorted by timestamp
- Success indicators and durations
- File changes listed
- Entry counter (7 entries: 4 file, 3 chat)

---

### 3. Interaction Features

**Pause/Interrupt:**
- [Pause Bot] button → Creates pause control file
- Bot finishes current task then waits
- [Resume] button → Deletes pause file

**Queue New Tasks:**
- Chat input box always active (never disabled)
- User can send prompts anytime
- Bot processes by priority (WebSocket > file queue)

**View File Details:**
- [View Files] link expands inline details
- Shows files modified with line ranges
- [View] button opens file in editor
- [Diff] button shows before/after

**Search/Filter:**
- Filter by entry type (file/chat/input)
- Keyword search in timeline
- Highlight matching entries

---

### 4. WebSocket/API Specification

**Endpoints:**

1. **GET /api/bot/{bot_id}/timeline** (REST)
   - Returns array of TimelineEntry objects
   - Supports pagination (limit, offset)
   - Initial load of full timeline

2. **GET /ws/bot/{bot_id}/timeline** (WebSocket)
   - Sends `timeline_snapshot` on connect
   - Sends `entry_added` when new response arrives
   - Sends `entry_chunk` for streaming content
   - Sends `entry_complete` when done

3. **POST /ws/bot/{bot_id}/prompt** (WebSocket)
   - User sends chat message
   - Bot processes based on priority

4. **POST /api/bot/{bot_id}/pause** (REST)
   - Pause bot execution
   - Finishes current task

5. **POST /api/bot/{bot_id}/resume** (REST)
   - Resume bot after pause

6. **GET /api/bot/{bot_id}/status** (REST)
   - Returns bot status (working/idle/paused)
   - Current task, queue size, connection state

---

## RECOMMENDED APPROACH

**Hybrid:**
1. REST GET for initial timeline snapshot (full history)
2. WebSocket stream for live updates (real-time entries)

**Benefits:**
- No polling lag
- Efficient (only changes sent)
- Bidirectional communication
- Real-time streaming responses

---

## UI LAYOUT

**Main View:**
```
[BOT-002 Conversation] [Status] [Menu]
┌─────────────────────────────────────────┐
│ [Timeline entries, scrollable]          │
│ - File responses                        │
│ - Chat messages (interleaved)           │
│ - Streaming indicators                  │
└─────────────────────────────────────────┘
[Chat input] [Send] [Pause]
```

**Optional Sidebar:**
```
Bot Status:
- Status: Working
- Current task
- Queue depth
- Timer
- [Pause] [Stop] buttons
```

---

## IMPLEMENTATION CHECKLIST

**Frontend:**
- [ ] Timeline component (scrollable)
- [ ] Entry type components (file, chat input, chat response)
- [ ] Streaming animation
- [ ] Expand/collapse details
- [ ] Auto-scroll to latest
- [ ] Timestamp formatting
- [ ] Color-coded priorities
- [ ] Status indicators
- [ ] Chat input + send button
- [ ] Pause/resume buttons

**Backend/API:**
- [ ] GET /api/bot/{bot_id}/timeline
- [ ] WebSocket /ws/bot/{bot_id}/timeline
- [ ] File monitoring (.deia/hive/responses/)
- [ ] Entry_chunk streaming
- [ ] WebSocket /ws/bot/{bot_id}/prompt
- [ ] Pause/resume endpoints
- [ ] Status endpoint

**Integration:**
- [ ] Commandeer ↔ REST API
- [ ] Commandeer ↔ WebSocket
- [ ] Test with BOT-002
- [ ] Test mixed timeline
- [ ] Test real-time streaming
- [ ] Performance (large timelines)

---

## SUCCESS CRITERIA

✅ Timeline displays mixed file + chat entries
✅ Entries sorted by timestamp
✅ Real-time updates via WebSocket
✅ User can send prompts anytime
✅ User can pause/resume
✅ File details expandable
✅ Success/failure indicators visible
✅ Timestamps clearly displayed
✅ Visual distinction between entry types

---

**Commandeer UI requirements complete and ready for frontend implementation.**

