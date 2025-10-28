# TASK-002-007: Unified Timeline Architecture Design - COMPLETE

**Task ID:** TASK-002-007
**Bot ID:** BOT-002
**Priority:** P1
**Status:** COMPLETE
**Completed:** 2025-10-28T14:24:30Z
**Duration:** 75 seconds

---

## DELIVERABLE

Created: `.deia/hive/responses/deiasolutions/UNIFIED-TIMELINE-DESIGN.md`

Comprehensive architecture for Commandeer unified timeline.

---

## DESIGN SUMMARY

### 1. Data Model

**TimelineEntry Schema:**
- Identity: entry_id, timestamp (ISO 8601)
- Source: "file" (task responses) or "chat" (WebSocket messages)
- Bot: bot_id
- Content: The actual message/response
- Status: success, duration, errors

**Distinguishing file vs chat:**
- File: has task_id, priority, duration
- Chat: has sender, sender_type (user/bot)

---

### 2. Retrieval Architecture

**Option A: REST Polling**
- GET `/api/bot/{bot_id}/timeline`
- Simple, synchronous
- Polling lag

**Option B: WebSocket Streaming (Recommended)**
- `GET /ws/bot/{bot_id}/timeline`
- Real-time, efficient
- Handles streaming entries as they arrive

**Recommended Approach: Hybrid**
1. REST GET to fetch existing timeline
2. WebSocket stream for new entries (live)

---

### 3. Display Order

**File responses appear in timeline?** YES

Rationale:
- Users need to see task completions
- Provides context for chat
- Complete conversation history
- Audit trail

**Async vs Real-Time:**
- Both sorted by timestamp
- Single unified view
- File entries appear as they complete (async)
- Chat entries appear immediately (real-time)

**Example Timeline (Mixed):**
```
14:18:00 FILE: TASK-002-001 "Checkin complete" ✅
14:18:15 CHAT: Q33N "Good, verify framework"
14:18:30 FILE: TASK-002-002 "Framework verified" ✅
14:18:45 CHAT: BOT-002 "Check complete, ready..."
14:19:00 FILE: TASK-002-003 "Audit complete" ✅
14:19:15 CHAT: Q33N "Update ScrumMaster protocol"
```

---

### 4. Implementation Steps

**Phase 1: Data Preparation** ✅ COMPLETE (TASK-002-006)
- Tag responses with source, timestamp, bot_id
- Response JSON ready for API

**Phase 2: API Endpoint** PENDING
- Add GET `/api/bot/{bot_id}/timeline`
- Parse response files
- Return TimelineEntry array sorted by timestamp
- Location: `src/deia/services/bot_service.py`

**Phase 3: WebSocket Handler** PENDING
- Add `GET /ws/bot/{bot_id}/timeline`
- Send initial snapshot
- Monitor `.deia/hive/responses/` for new files
- Stream new entries to connected clients

**Phase 4: Commandeer UI** PENDING
- Load initial timeline via REST
- Connect to WebSocket for live updates
- Render mixed file + chat entries
- Display with source indicators (📄 vs 💬)

---

## CODE LOCATIONS

| Component | File | Method | Status |
|-----------|------|--------|--------|
| Data prep | bot_runner.py | run_once() | ✅ Done |
| REST API | bot_service.py | GET /api/bot/{bot_id}/timeline | 📋 Ready |
| WebSocket | bot_service.py | /ws/bot/{bot_id}/timeline | 📋 Ready |
| UI | Commandeer | displayTimeline() | 📋 Ready |

---

## BENEFITS

✅ Single conversation view mixing async tasks + real-time chat
✅ Complete history of all interactions
✅ Source clarity (know where each entry came from)
✅ Timestamp-based ordering
✅ Audit trail for accountability
✅ Enables hybrid mode coordination

---

## NEXT STEPS

1. Implement REST API endpoint in BotService
2. Implement WebSocket handler in BotService
3. Add file monitoring for new response files
4. Implement Commandeer UI timeline component
5. Connect to REST API or WebSocket
6. Test mixed file + chat display

---

