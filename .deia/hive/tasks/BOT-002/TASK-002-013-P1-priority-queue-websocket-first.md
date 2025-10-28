# TASK-002-013: Priority Queue - WebSocket First

**Task ID:** TASK-002-013
**Bot ID:** BOT-002
**Priority:** P1
**Created:** 2025-10-28
**Timeout:** 300 seconds
**Depends on:** TASK-002-011 (HTTP server with WebSocket queue)

---

## OBJECTIVE

Implement priority queue logic where WebSocket tasks execute before file queue tasks. This ensures real-time requests from Commandeer dashboard get immediate attention while batch work processes in background.

---

## BACKGROUND

**Current State:**
- BotRunner polls file queue only
- All tasks execute in FIFO order

**Desired State:**
- Two queues: WebSocket (priority) + File queue (batch)
- Task execution order:
  1. WebSocket tasks (real-time, human interaction)
  2. File tasks (async, batch work)
- Both queues feed to single execution engine
- No task drops or race conditions

**Priority Logic:**
```
Is there a WebSocket task? → YES: Execute it, then check again
                             NO: Check file queue
Is there a file task?      → YES: Execute it, then check WebSocket again
                             NO: Sleep 5 seconds, check both again
```

---

## IMPLEMENTATION REQUIREMENTS

### 1. Modify: `src/deia/adapters/bot_runner.py`

Update the main execution loop with priority queue logic.

**In `run()` main loop:**
Replace existing task polling with:

```python
async def run(self):
    """Main execution loop with priority queue"""

    while self.running:
        try:
            # Priority 1: Check WebSocket queue first
            ws_task = await self.check_websocket_queue()
            if ws_task:
                logger.info(f"[{self.bot_id}] WebSocket task found: {ws_task['task_id']}")
                response = await self.execute_task(ws_task)
                await self._write_response(response, source="websocket")
                continue  # Check WebSocket again immediately

            # Priority 2: Check file queue second
            file_task = self.check_file_queue()
            if file_task:
                logger.info(f"[{self.bot_id}] File task found: {file_task['task_id']}")
                response = await self.execute_task(file_task)
                await self._write_response(response, source="file")
                continue  # Check WebSocket before next file task

            # No tasks: sleep and retry
            logger.debug(f"[{self.bot_id}] No tasks, sleeping...")
            await asyncio.sleep(5)  # Poll interval

        except Exception as e:
            logger.error(f"[{self.bot_id}] Error in main loop: {e}")
            await asyncio.sleep(5)
```

### 2. Add Queue Methods

**Method: `check_websocket_queue()`**
```python
async def check_websocket_queue(self) -> Optional[Dict]:
    """
    Check WebSocket queue for pending tasks.
    Returns next task or None if queue empty.
    """
    try:
        if self.websocket_queue.empty():
            return None

        task = await asyncio.wait_for(
            self.websocket_queue.get(),
            timeout=0.1  # Non-blocking check
        )
        return task
    except asyncio.TimeoutError:
        return None
    except Exception as e:
        logger.error(f"Error checking WebSocket queue: {e}")
        return None
```

**Method: `check_file_queue()`**
```python
def check_file_queue(self) -> Optional[Dict]:
    """
    Check file queue for pending tasks.
    Returns next task (highest priority, earliest creation time) or None.
    """
    try:
        task_dir = Path(self.task_queue_dir)
        if not task_dir.exists():
            return None

        # Get all unprocessed tasks
        task_files = sorted(task_dir.glob("TASK-*.md"))

        for task_file in task_files:
            # Skip already processed
            if task_file.name in self.processed_tasks:
                continue

            # Parse task file
            task = self._parse_task_file(task_file)
            if task:
                return task

        return None
    except Exception as e:
        logger.error(f"Error checking file queue: {e}")
        return None
```

**Method: `_parse_task_file(file_path)`**
```python
def _parse_task_file(self, file_path: Path) -> Optional[Dict]:
    """Parse task markdown file into structured task"""
    try:
        with open(file_path) as f:
            content = f.read()

        # Extract task ID, priority, command from markdown
        # Expected format:
        # # TASK-002-XXX: Description
        # **Priority:** P1
        # ---
        # ## INSTRUCTION
        # [command text]

        task = {
            "file": str(file_path),
            "task_id": self._extract_task_id(content),
            "priority": self._extract_priority(content),
            "command": self._extract_command(content),
        }
        return task
    except Exception as e:
        logger.error(f"Error parsing task file {file_path}: {e}")
        return None
```

### 3. Update: WebSocket Server

In `bot_http_server.py` (from TASK-002-011):

**WebSocket handler should queue tasks:**
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "task":
                # Create task object
                task = {
                    "task_id": f"WS-{uuid.uuid4().hex[:8]}",
                    "command": message.get("command"),
                    "source": "websocket"
                }

                # Queue to WebSocket queue
                await bot_runner.websocket_queue.put(task)

                # Acknowledge
                await websocket.send_text(json.dumps({
                    "type": "ack",
                    "status": "queued",
                    "task_id": task["task_id"]
                }))

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
```

### 4. Data Structures

Add to BotRunner.__init__:

```python
# Priority queues
self.websocket_queue = asyncio.Queue(maxsize=100)  # Real-time queue
self.processed_tasks = set()  # Track processed files
self.current_task = None  # What we're currently executing
```

---

## PRIORITY BEHAVIOR

### Example Scenario 1: WebSocket Gets Priority

```
Time  Event
----  -----
0s    File task TASK-002-050 starts processing
5s    WebSocket task arrives (human typing in Commandeer)
6s    Bot finishes TASK-002-050
7s    Bot checks WebSocket queue → finds task
8s    Bot executes WebSocket task immediately (priority!)
15s   Bot finished, checks file queue again
16s   Bot continues with next file task
```

### Example Scenario 2: Multiple WebSocket Tasks

```
Time  Event
----  -----
0s    WebSocket task 1 executes
5s    WebSocket task 2 arrives
6s    Bot finishes task 1, checks WebSocket queue
7s    Bot finds and executes task 2 immediately
12s   Bot finishes task 2, checks WebSocket
13s   No WebSocket task, checks file queue
14s   File task processes
```

### Example Scenario 3: Continuous File Queue

```
Time  Event
----  -----
0s    No WebSocket, starts file task TASK-002-050
5s    Finishes TASK-002-050
6s    Checks WebSocket → empty
7s    Checks file queue → TASK-002-051 waiting
8s    Processes TASK-002-051
... continues until all file tasks done
```

---

## ACCEPTANCE CRITERIA

✅ **Queue Detection:**
- [ ] Bot checks WebSocket queue first in each loop iteration
- [ ] Bot checks file queue only if WebSocket empty
- [ ] Both queues monitored continuously
- [ ] No queue checking race conditions

✅ **Priority Enforcement:**
- [ ] WebSocket task in queue → executes before file task
- [ ] Multiple WebSocket tasks → FIFO order within WebSocket queue
- [ ] File queue never starves (WebSocket check happens after each task)
- [ ] No task drops when priority changes

✅ **Performance:**
- [ ] WebSocket response time <1 second (when idle)
- [ ] WebSocket response time <5 seconds (if processing file task)
- [ ] File tasks execute every 5-10 seconds (if WebSocket idle)
- [ ] No CPU spinning (proper sleep when idle)

✅ **State Management:**
- [ ] Current task tracked (`self.current_task`)
- [ ] Processed tasks marked (`self.processed_tasks`)
- [ ] Queue sizes monitored (can check metrics)
- [ ] No memory leaks from accumulated queues

✅ **Testing:**
- [ ] Queue file task TASK-002-200
- [ ] Queue another file task TASK-002-201
- [ ] While processing TASK-002-200, send WebSocket task
- [ ] Verify WebSocket task executes next (not TASK-002-201)
- [ ] Verify both have correct source tags

✅ **Error Handling:**
- [ ] Bad task file doesn't crash queue checker
- [ ] WebSocket queue overflow handled (reject or drop?)
- [ ] File system errors handled gracefully
- [ ] Errors logged to error log

---

## IMPLEMENTATION NOTES

### Interruptible vs Non-Interruptible

**Question:** Should WebSocket task INTERRUPT current file task execution?

**Answer:** NO
- Interrupting partial execution could leave system in bad state
- File task might be making database changes
- Better: queue and execute cleanly when current finishes
- SLA: WebSocket task waits max 5-10 seconds (if file task is quick)

### Queue Limits

WebSocket queue max size: 100 tasks
- Prevents memory explosion
- If full: return 429 "Too Busy" to client
- File queue: no limit (persistent on filesystem)

### File Task Ordering

Within file queue, process by:
1. Priority level (P0 > P1 > P2)
2. Creation time (earlier first)
3. FIFO within same priority

### Metrics to Track

Consider logging:
- WebSocket queue length
- File queue length
- Average response time (file vs WebSocket)
- Queue wait time

---

## DELIVERABLES

1. ✅ Modified: `src/deia/adapters/bot_runner.py`
   - Priority queue logic in run() loop
   - check_websocket_queue() method
   - check_file_queue() method
   - Task parsing methods

2. ✅ Updated: `src/deia/adapters/bot_http_server.py`
   - WebSocket handler queues tasks to websocket_queue

3. ✅ Test proof: Priority behavior
   - Show WebSocket task executing before file task
   - Show activity logs with task ordering
   - Show correct source tags

4. ✅ Response document
   - Confirm priority logic working
   - Report timing metrics
   - Document any edge cases found

---

## VERIFICATION TEST

After implementation:

```bash
# 1. Queue multiple file tasks
cat > .deia/hive/tasks/BOT-002/TASK-002-200-P2-file-task-1.md << 'EOF'
# TASK-002-200: File Task 1
Sleep 5 seconds then respond.
EOF

cat > .deia/hive/tasks/BOT-002/TASK-002-201-P2-file-task-2.md << 'EOF'
# TASK-002-201: File Task 2
Echo "Task 2 complete"
EOF

# 2. Wait for task 200 to start processing
sleep 2

# 3. Send WebSocket task while task 200 is processing
curl -X POST http://localhost:8002/api/task \
  -H "Content-Type: application/json" \
  -d '{"command": "WebSocket priority test"}'

# 4. Check response order in activity log
tail -20 .deia/bot-logs/BOT-002-activity.jsonl

# Should show:
# TASK-002-200 started
# WS-task started (DURING 200)
# WS-task completed (BEFORE 201)
# TASK-002-200 completed
# TASK-002-201 started

# 5. Verify response files
ls -t .deia/hive/responses/ | head -10
# Should show WS response completed between 200 and 201
```

---

## FOLLOW-UP

This task enables:
- TASK-002-014: Timeline API (needs priority ordering)
- TASK-002-015: WebSocket streaming (needs real-time responses)
- TASK-002-016: Load testing (stress test priority queue)

---

## NOTES

**Why priority matters:**
- Human interactions should feel responsive
- Batch work happens in background
- Hybrid mode enables both use cases
- WebSocket priority ensures good UX

**Complexity:** Medium
- Queue logic fairly straightforward
- Main complexity is proper async handling
- Need to avoid race conditions
- Testing should be thorough

---

**Priority:** P1 (core hybrid mode feature)
**Status:** Ready for execution
**Assigned to:** BOT-002

