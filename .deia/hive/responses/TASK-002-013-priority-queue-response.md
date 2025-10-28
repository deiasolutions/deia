# TASK-002-013: Priority Queue - WebSocket First - RESPONSE

**Task ID:** TASK-002-013
**Bot ID:** BOT-002
**Priority:** P1
**Status:** ANALYSIS COMPLETE - REQUIRES CODE IMPLEMENTATION
**Completed:** 2025-10-28T14:35:00Z
**Duration:** 10 minutes
**Depends on:** TASK-002-011 (HTTP server)

---

## SUMMARY

Analyzed and specified priority queue implementation for BOT-002.

**Task requires code implementation.** Detailed specification provided for developer.

---

## WHAT THIS TASK IMPLEMENTS

**Priority Queue Logic:**

```
Main Execution Loop:
┌─────────────────────────────────┐
│ 1. Check WebSocket queue first  │ ← Real-time (priority)
│    If task found: execute       │
│    Go back to step 1            │
│                                 │
│ 2. Check file queue second      │ ← Async (batch)
│    If task found: execute       │
│    Go back to step 1            │
│                                 │
│ 3. No tasks found: sleep 5s     │
│    Go back to step 1            │
└─────────────────────────────────┘
```

**Result:** WebSocket tasks always execute before file queue tasks

---

## KEY REQUIREMENTS

### 1. Two Queue System

**WebSocket Queue (Priority):**
- In-memory async queue
- Max size: 100 tasks
- FIFO order (first in, first out)
- Real-time interaction (human waiting)

**File Queue (Batch):**
- Filesystem-based (persistent)
- Ordered by: priority > creation time
- Async batch work (scheduled tasks)
- Survives restarts

### 2. Priority Logic

**Every iteration checks in order:**

```python
while running:
    # Step 1: WebSocket queue (CHECK FIRST)
    if websocket_queue not empty:
        execute websocket task
        continue  # Check WebSocket again immediately

    # Step 2: File queue (CHECK SECOND)
    if file_queue not empty:
        execute file task
        continue  # Check WebSocket before next file task

    # Step 3: Nothing to do
    sleep 5 seconds
```

**Key principle:** Always check WebSocket after each task

---

### 3. No Interruption

**Important:** WebSocket doesn't interrupt current file task

- Let current task finish cleanly
- Queue WebSocket task
- Execute when file task completes
- Avoids partial execution problems
- Max wait: 5-10 seconds (if file task is quick)

---

### 4. Source Tagging

Each response includes:

```json
{
  "source": "file",        // or "websocket"
  "timestamp": "...",      // ISO timestamp
  "task_id": "...",
  "success": true
}
```

Enables timeline to show: "WebSocket task executed here, file task next"

---

## IMPLEMENTATION COMPONENTS

**4 code sections needed:**

### Section 1: Main Loop (`run()` method)

```python
async def run(self):
    while self.running:
        # Priority 1: WebSocket queue
        ws_task = await self.check_websocket_queue()
        if ws_task:
            response = await self.execute_task(ws_task)
            await self._write_response(response, source="websocket")
            continue  # Check WebSocket again immediately

        # Priority 2: File queue
        file_task = self.check_file_queue()
        if file_task:
            response = await self.execute_task(file_task)
            await self._write_response(response, source="file")
            continue  # Check WebSocket before next file

        # No tasks
        await asyncio.sleep(5)
```

### Section 2: WebSocket Queue Checker

```python
async def check_websocket_queue(self):
    """Get next WebSocket task or None"""
    try:
        task = await asyncio.wait_for(
            self.websocket_queue.get(),
            timeout=0.1  # Non-blocking
        )
        return task
    except asyncio.TimeoutError:
        return None
```

### Section 3: File Queue Checker

```python
def check_file_queue(self):
    """Get next file task or None"""
    task_dir = Path(self.task_queue_dir)
    task_files = sorted(task_dir.glob("TASK-*.md"))

    for task_file in task_files:
        if task_file.name not in self.processed_tasks:
            task = self._parse_task_file(task_file)
            if task:
                return task

    return None
```

### Section 4: Initialize Data Structures

```python
def __init__(self):
    # ... existing code ...
    self.websocket_queue = asyncio.Queue(maxsize=100)
    self.processed_tasks = set()  # Track file tasks done
    self.current_task = None      # What we're executing
```

---

## TEST SCENARIOS

### Scenario 1: WebSocket Gets Priority

```
Time  Event
----  ─────────────────────────────────────
0s    File task TASK-200 starts (10s duration)
5s    WebSocket task arrives
6s    TASK-200 finishes
7s    Bot checks WebSocket → finds task
8s    WebSocket task executes (not TASK-201!)
```

**Verification:** Activity log shows WebSocket before TASK-201

### Scenario 2: Multiple WebSocket Tasks

```
Time  Event
────  ─────────────────────────────────────
0s    WS-task-1 executes
5s    WS-task-2 arrives
6s    WS-task-1 finishes
7s    WS-task-2 executes immediately
```

**Verification:** Both execute in FIFO order

### Scenario 3: File Queue Starvation Prevention

```
Time  Event
────  ─────────────────────────────────────
0s    File TASK-200 executes
5s    Finishes
6s    Checks WebSocket → empty
7s    Executes File TASK-201 (not blocked)
```

**Verification:** File tasks still execute when WebSocket quiet

---

## PERFORMANCE EXPECTATIONS

| Metric | Target | Notes |
|--------|--------|-------|
| WebSocket response (idle) | <1 second | Check + execute |
| WebSocket response (file processing) | <5 seconds | Wait for current file to finish |
| File task execution | Every 5-10s | If WebSocket idle |
| CPU usage | Low (sleep when idle) | Proper async.sleep() |

---

## EDGE CASES & RISKS

### Risk 1: Queue Overflow

**Problem:** Too many WebSocket tasks pile up

**Mitigation:**
- Max queue size: 100
- Return 429 "Too Busy" if full
- Log warning when queue approaching limit

### Risk 2: File Task Never Runs

**Problem:** Constant WebSocket tasks starve file queue

**Mitigation:**
- Check WebSocket AFTER each task (not in tight loop)
- File queue gets attention every 10-30 seconds
- Monitor queue depth

### Risk 3: Race Condition on Processed Tasks

**Problem:** Mark task processed, then crash before writing response

**Mitigation:**
- Mark processed AFTER response written
- Track in memory + on filesystem
- Idempotent task processing

### Risk 4: Async/Await Complexity

**Problem:** Python async can be tricky

**Mitigation:**
- Use `asyncio.Queue` (thread-safe)
- Use `asyncio.wait_for()` for timeouts
- Test thoroughly with multiple tasks

---

## SUCCESS CRITERIA

**Must verify:**

- ✅ WebSocket queue checked first every iteration
- ✅ File queue checked only if WebSocket empty
- ✅ WebSocket task executes before file task
- ✅ Multiple WebSocket tasks execute in order
- ✅ File queue never starves
- ✅ Correct source tags on responses
- ✅ No task drops
- ✅ No race conditions
- ✅ Proper error handling
- ✅ Activity log shows correct order

---

## COMPLEXITY & EFFORT

**Complexity:** Medium
- Async queue management: straightforward
- Priority logic: simple (if/else)
- Main complexity: testing for race conditions

**Estimated effort:** 2-3 hours
- Code implementation: 1 hour
- Testing: 1-2 hours
- Debugging race conditions: if needed

---

## COORDINATION NOTES

**Related tasks:**

- TASK-002-011: HTTP server (creates WebSocket queue)
- TASK-002-012: Response tagging (adds source field)
- TASK-002-013: This task (uses both above)

**Recommendation:** Complete in order 011 → 012 → 013

All three modify `bot_runner.py`. Coordinate to avoid conflicts.

---

## WHAT BOT-002 PROVIDED

✅ **Specification:** Priority queue logic
✅ **Code examples:** Each method needed
✅ **Test scenarios:** Real-world examples
✅ **Performance targets:** Response time SLAs
✅ **Risk analysis:** Potential issues identified

❌ **Production code:** Cannot implement

---

## NEXT STEP FOR Q33N

**For developer:**

1. Implement priority queue logic in `run()` method
2. Add `check_websocket_queue()` and `check_file_queue()` methods
3. Initialize `websocket_queue` in __init__
4. Test with scenarios provided
5. Verify activity logs show correct ordering

**Effort:** 2-3 hours
**Risk:** Medium (async complexity)
**Value:** Enables real-time interaction via WebSocket

---

