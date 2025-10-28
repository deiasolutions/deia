# HYBRID MODE COORDINATION DESIGN

**Mode 3 (Hybrid):** Bot listens to BOTH file queue AND WebSocket simultaneously

**Purpose:** Allow both async task queuing + real-time chat interaction

**Status:** Design Complete
**Date:** 2025-10-28

---

## 1. PRIORITY HANDLING

### Simultaneous Input Scenario

When both file task AND WebSocket prompt arrive within same polling cycle:

```
Timeline:
14:18:00 → File task arrives: TASK-002-001
14:18:01 → WebSocket prompt arrives: "quick fix?"
→ Bot must choose which to execute
```

### Priority Rules (WebSocket > File Queue)

**Rule:** WebSocket input takes priority over file queue

**Rationale:**
- WebSocket is real-time (human waiting for response)
- File queue is async (can wait)
- Better UX: human gets immediate feedback

**Implementation:**

```python
def run_once_hybrid():
    """
    Hybrid mode task execution: prioritize WebSocket over file queue
    """

    # 1. Check for WebSocket input (higher priority)
    websocket_prompt = self.check_websocket_queue()
    if websocket_prompt:
        # Execute WebSocket prompt IMMEDIATELY
        result = self.adapter.send_task(websocket_prompt["content"])
        # Stream response to chat
        self.stream_to_websocket(result)
        # Also write to file for timeline
        self.write_response_file(result, source="chat")
        return

    # 2. No WebSocket input - check file queue
    file_task = self.find_next_task()
    if file_task:
        # Execute file-based task
        result = self.adapter.send_task(file_task["content"])
        # Write to response file
        self.write_response_file(result, source="file")
        return

    # 3. No input at all - idle
    return
```

### Queuing Deferred Tasks

When WebSocket executes while file task is pending:

```
Queue Structure:
┌─────────────────────────────────┐
│ File Queue    │ WebSocket Queue │
├─────────────────────────────────┤
│ TASK-001      │ [waiting]       │
│ TASK-002      │                 │
│ TASK-003      │                 │
└─────────────────────────────────┘

Execution Order:
1. WebSocket prompt arrives → execute immediately
2. File TASK-001 → execute next (from file queue)
3. File TASK-002 → execute next
```

### Timeout for Pending Tasks

**File queue timeout:** Original timeout (60-300 seconds)
**WebSocket timeout:** Real-time (e.g., 5-10 seconds)

If WebSocket prompt takes longer:

```python
# Track when WebSocket task started
websocket_start_time = time.time()
websocket_timeout = 10  # seconds

# If exceeds timeout, warn user
if time.time() - websocket_start_time > websocket_timeout:
    self.warn_to_websocket("Task taking longer than expected...")

# If exceeds hard limit, cancel
if time.time() - websocket_start_time > 60:
    self.cancel_websocket_task()
    self.error_to_websocket("Task timeout - try again")
```

---

## 2. RESPONSE ROUTING

### File-Based Task Response

**Input:** Task from `.deia/hive/tasks/BOT-XXX/TASK-ID.md`

**Processing:**
1. Execute task via adapter
2. Get result

**Output Destinations:**
1. **Response file:** Write to `.deia/hive/responses/TASK-ID-response.md`
2. **Timeline:** Entry appears with source="file"
3. **Chat (optional):** Brief summary sent to WebSocket

**Example Response File:**
```json
{
    "task_id": "TASK-002-001",
    "source": "file",
    "timestamp": "2025-10-28T14:18:00Z",
    "bot_id": "BOT-002",
    "success": true,
    "response": "Task completed successfully",
    "duration_seconds": 45
}
```

### WebSocket Prompt Response

**Input:** Chat message via WebSocket from user

**Processing:**
1. Receive prompt via WebSocket
2. Execute task via adapter
3. Stream response in real-time

**Output Destinations:**
1. **WebSocket stream:** Send chunks to user in real-time
2. **Response file:** Also write complete response to `.deia/hive/responses/CHAT-ID-response.md`
3. **Timeline:** Entry appears with source="chat"

**Example Real-Time Response:**
```json
// Message 1 (start)
{
    "type": "response_start",
    "task_id": "CHAT-001",
    "timestamp": "2025-10-28T14:18:15Z"
}

// Message 2 (chunk 1)
{
    "type": "response_chunk",
    "content": "Analyzing request...\n"
}

// Message 3 (chunk 2)
{
    "type": "response_chunk",
    "content": "Found 3 issues. Fixing...\n"
}

// Message 4 (complete)
{
    "type": "response_complete",
    "success": true,
    "duration": 8.5,
    "files_modified": ["file1.py", "file2.py"]
}
```

### Both in Timeline?

**YES** - Both file and chat responses appear in timeline

**Timeline Example:**
```
[14:18:00] FILE: TASK-002-001 "Checkin complete"
[14:18:15] CHAT: User "Quick: add error handling"
[14:18:30] CHAT: Bot [streaming response...]
[14:18:45] FILE: TASK-002-002 "Inventory audit complete"
```

---

## 3. STATE MANAGEMENT

### What State to Track

```python
class HybridBotState:
    def __init__(self):
        # Current execution context
        self.current_task_id: Optional[str] = None      # What are we executing?
        self.current_source: str = "idle"               # "file", "chat", or "idle"
        self.task_start_time: float = 0                 # When did task start?
        self.task_timeout: int = 0                      # When does it timeout?

        # Queued items
        self.file_queue: List[str] = []                 # Pending file tasks
        self.websocket_queue: List[Dict] = []           # Pending chat prompts

        # WebSocket connection state
        self.websocket_connected: bool = False          # Is WS connected?
        self.websocket_client_id: Optional[str] = None  # Which client?

        # Pause/resume state
        self.paused: bool = False                       # Is bot paused?
        self.interrupted: bool = False                  # Was task interrupted?
```

### Handling Interrupts Mid-Task

**Scenario:** WebSocket user asks to cancel current file task

```
14:18:00 → Start TASK-002-001 (10 minute task)
14:18:15 → User sends: "cancel that, do THIS instead"
          → How does bot handle?
```

**Implementation:**

```python
def handle_websocket_interrupt(self, prompt):
    """
    User sent urgent prompt - interrupt current task?
    """

    # Decision tree:
    if self.current_source == "chat":
        # Already doing chat task - replace it
        self.cancel_current_task()
        self.execute_websocket_prompt(prompt)

    elif self.current_source == "file":
        # Doing file task - defer or interrupt?
        if self.task_timeout - time.time() < 30:
            # Task almost done - wait
            self.queue_websocket_prompt(prompt)
        else:
            # Long task - interrupt and execute chat prompt
            self.cancel_current_task()
            self.execute_websocket_prompt(prompt)

    elif self.current_source == "idle":
        # No current task - execute immediately
        self.execute_websocket_prompt(prompt)
```

### Recovery if WebSocket Disconnects

**Scenario:** Client disconnects mid-response

```
14:18:15 → User connects to WebSocket
14:18:20 → User sends prompt
14:18:25 → Connection drops
          → Bot should continue or cancel?
```

**Implementation:**

```python
async def websocket_handler(websocket):
    try:
        while True:
            message = await websocket.receive_text()
            # Process message
            response = await execute_task(message)

            # Send response
            for chunk in response:
                await websocket.send_json(chunk)

    except WebSocketDisconnect:
        # Client disconnected
        if self.current_source == "chat":
            # Save incomplete response to file
            self.save_response_to_file(
                task_id=self.current_task_id,
                response=self.response_buffer,
                error="Client disconnected"
            )
            # Stop execution
            self.cancel_current_task()
```

---

## 4. CODE CHANGES NEEDED

### Change 1: Modify `run_once()` to Support Hybrid

**File:** `src/deia/adapters/bot_runner.py`

**Current:** `run_once()` checks only file queue

**Changes:**

```python
def run_once(self) -> Dict[str, Any]:
    """
    Execute one iteration - hybrid mode
    Prioritize WebSocket over file queue
    """

    if self.comm_mode == "hybrid":
        return self.run_once_hybrid()
    else:
        return self.run_once_cli_only()  # Existing logic

def run_once_hybrid(self) -> Dict[str, Any]:
    """
    Hybrid mode: Check WebSocket first, then file queue
    """

    # 1. Check WebSocket queue (higher priority)
    websocket_message = self.websocket_queue.get_nowait()
    if websocket_message:
        # Execute WebSocket prompt
        task = {
            "task_id": websocket_message["id"],
            "content": websocket_message["prompt"],
            "from": websocket_message["user"]
        }

        result = self.adapter.send_task(task["content"])

        # Stream to WebSocket
        self.stream_to_websocket(result)

        # Also write to file
        self.write_response_file(
            result=result,
            source="chat",
            task_id=task["task_id"]
        )

        return {
            "task_found": True,
            "task_executed": True,
            "source": "chat",
            "task_id": task["task_id"]
        }

    # 2. Check file queue (lower priority)
    file_task = self._find_next_task()
    if file_task:
        # Execute file task (existing logic)
        task = parse_task_file(file_task)
        result = self.adapter.send_task(task["content"])
        self.write_response_file(result, source="file")

        return {
            "task_found": True,
            "task_executed": True,
            "source": "file",
            "task_id": task["task_id"]
        }

    # 3. No tasks
    return {
        "task_found": False,
        "task_executed": False
    }
```

### Change 2: Add WebSocket Handler

**File:** New file or `src/deia/services/bot_service.py`

```python
from asyncio import Queue

class HybridBotService:
    def __init__(self, bot_runner):
        self.bot_runner = bot_runner
        self.websocket_queue = Queue()  # Async queue for prompts

    @app.websocket("/ws/bot/{bot_id}/prompt")
    async def websocket_handler(websocket: WebSocket, bot_id: str):
        """
        Accept chat prompts via WebSocket
        """
        await websocket.accept()

        try:
            while True:
                # Receive prompt from user
                data = await websocket.receive_json()

                # Queue it for bot runner
                await self.websocket_queue.put({
                    "id": f"CHAT-{uuid.uuid4()}",
                    "prompt": data["message"],
                    "user": data["user"],
                    "websocket": websocket  # For streaming response
                })

        except WebSocketDisconnect:
            pass
```

### Change 3: Modify Task Polling Loop

**File:** `src/deia/adapters/bot_runner.py::run_continuous()`

**Change:** Check both queues in hybrid mode

```python
def run_continuous_hybrid(self):
    """
    Hybrid mode polling loop
    Check WebSocket queue AND file queue
    """

    while self.running:
        # run_once_hybrid() handles priority
        result = self.run_once_hybrid()

        if result.get("task_executed"):
            # Task was executed, don't cool down immediately
            # (WebSocket user expects quick response)
            if result.get("source") == "chat":
                time.sleep(1)  # Minimal wait for chat
            else:
                time.sleep(self.task_cooldown_seconds)  # Normal wait for file

        else:
            # No tasks - normal idle wait
            time.sleep(5)  # Poll every 5 seconds
```

---

## 5. IMPLEMENTATION APPROACH

### Recommended Approach: Phased Rollout

**Phase 1 (Now):** CLI-Only Mode
- ✅ File queue polling
- ✅ Response file writing
- File-based coordination only

**Phase 2 (Next):** Hybrid Mode
- Add WebSocket handler
- Add priority logic (WebSocket > file)
- Modify `run_once()` for dual queues
- Implement state tracking

**Phase 3 (Future):** Commander-Only Mode
- WebSocket exclusive
- No file queue
- Pure real-time

### Risk Mitigation

**Risk:** Concurrent task execution (file + chat simultaneously)

**Mitigation:**
- Single-threaded execution model (only 1 task at a time)
- Queue system ensures serialization
- Priority prevents starvation

**Risk:** WebSocket client disconnects mid-response

**Mitigation:**
- Try/except handles WebSocketDisconnect
- Response saved to file even if client disconnects
- Timeline has complete record

**Risk:** File queue backs up while handling WebSocket

**Mitigation:**
- File tasks still execute (just after WebSocket)
- ScrumMaster can pause bot if needed
- Queue visible in `.deia/hive/tasks/`

---

## SUMMARY

✅ **Priority:** WebSocket > File Queue
✅ **Response Routing:** Both file and chat responses written to file and timeline
✅ **State Management:** Track current task, queues, WebSocket connection
✅ **Interrupts:** Handle mid-task cancellation gracefully
✅ **Disconnects:** Save response if WebSocket drops
✅ **Code Changes:** Modify run_once(), add WebSocket handler, update polling loop

**Hybrid mode ready for implementation in Phase 2.**

