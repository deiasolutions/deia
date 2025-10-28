# TASK-002-008: Hybrid Mode Coordination Design - COMPLETE

**Task ID:** TASK-002-008
**Bot ID:** BOT-002
**Priority:** P2
**Status:** COMPLETE
**Completed:** 2025-10-28T14:25:45Z
**Duration:** 90 seconds

---

## DELIVERABLE

Created: `.deia/hive/responses/deiasolutions/HYBRID-MODE-DESIGN.md`

Complete design for Mode 3 (Hybrid) bot coordination.

---

## DESIGN SUMMARY

### 1. Priority Handling

**Rule:** WebSocket input > File queue

When both arrive simultaneously:
- WebSocket (real-time chat) executes immediately
- File task (async) waits in queue

**Rationale:** Human user waiting for response should get priority

Implementation: Check WebSocket first, then file queue in `run_once()`

---

### 2. Response Routing

**File-Based Task:**
- Execution: Read from `.deia/hive/tasks/BOT-XXX/`
- Output: Write to `.deia/hive/responses/`
- Timeline: Entry with source="file"

**WebSocket Prompt:**
- Execution: Receive from WebSocket connection
- Output 1: Stream response to chat (real-time)
- Output 2: Write to `.deia/hive/responses/` (persistence)
- Timeline: Entry with source="chat"

**Both in timeline?** YES
- File responses: source="file", task_id present
- Chat responses: source="chat", sender present
- Single unified timeline sorted by timestamp

---

### 3. State Management

**Bot must track:**
- Current task (what are we executing?)
- Current source (file, chat, or idle?)
- Task start time and timeout
- File queue and WebSocket queue
- WebSocket connection state
- Pause/resume state

**Handling interrupts mid-task:**
- If almost done (< 30s remaining): queue WebSocket prompt
- If long task: interrupt and execute WebSocket prompt
- If idle: execute immediately

**Recovery if WebSocket disconnects:**
- Try/except catches WebSocketDisconnect
- Incomplete response saved to file
- Timeline has complete record
- Bot continues operating

---

### 4. Code Changes Needed

**Change 1:** Modify `run_once()` in bot_runner.py
- Add check for WebSocket queue first
- Then check file queue
- Return source indicator ("file" or "chat")

**Change 2:** Add WebSocket handler
- Accept connections on `/ws/bot/{bot_id}/prompt`
- Queue incoming prompts to async queue
- Stream responses back to client

**Change 3:** Update `run_continuous()` polling loop
- In hybrid mode, check both queues
- Minimal wait for chat responses
- Normal wait for file tasks

---

## IMPLEMENTATION PHASES

**Phase 1:** CLI-Only (Current BOT-002)
- ✅ File queue polling
- ✅ Response file writing
- File-based coordination

**Phase 2:** Hybrid Mode (Next)
- Add WebSocket handler
- Add priority logic (WebSocket > file)
- Modify run_once() for dual queues
- Implement state tracking

**Phase 3:** Commander-Only (Future)
- WebSocket exclusive
- No file queue
- Pure real-time

---

## RISK MITIGATION

**Concurrent execution:** Single-threaded, queue serialization
**WebSocket disconnect:** Try/except, response saved to file
**File queue backup:** Still executes, ScrumMaster can pause

---

## BENEFITS

✅ Real-time chat interaction with async task processing
✅ Single bot handles both file queue and WebSocket
✅ User gets priority for urgent requests
✅ Complete timeline of all interactions
✅ Backward compatible (file queue still works)

---

