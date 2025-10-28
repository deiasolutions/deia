# TASK-002-012: Response Tagging & Timestamps

**Task ID:** TASK-002-012
**Bot ID:** BOT-002
**Priority:** P1
**Created:** 2025-10-28
**Timeout:** 300 seconds
**Depends on:** TASK-002-011 (port infrastructure)

---

## OBJECTIVE

Add source tagging and ISO timestamps to all BOT-002 responses. This enables:
- Unified timeline to distinguish file vs WebSocket responses
- Audit trail of when each task completed
- Response routing verification (file vs port)

---

## BACKGROUND

**Current State:**
- Responses written to file without source tag
- No timestamps on responses
- Can't tell if response came from file queue or WebSocket

**Desired State:**
- All responses include:
  - `source: "file" | "websocket"`
  - `timestamp: "2025-10-28T14:05:30Z"` (ISO 8601)
  - `bot_id: "BOT-002"`
  - `task_id: "TASK-002-011"`
  - `success: true | false`
  - Content and metadata

**Format for Unified Timeline:**
```json
{
  "task_id": "TASK-002-011",
  "bot_id": "BOT-002",
  "source": "file",
  "timestamp": "2025-10-28T14:05:30Z",
  "success": true,
  "response": "Implementation complete...",
  "files_modified": ["bot_runner.py", "bot_http_server.py"],
  "duration_seconds": 1200
}
```

---

## IMPLEMENTATION REQUIREMENTS

### 1. Modify: `src/deia/adapters/bot_runner.py`

Update the response writing system to include tags:

**In `_write_response()` method (or equivalent):**
- Add parameter: `source: str` ("file" or "websocket")
- Include `source` in response JSON
- Add `timestamp` with current UTC time (ISO 8601 format)
- Ensure `bot_id` is always present
- Ensure `task_id` is present

**Updated response format:**
```python
response = {
    "task_id": task["task_id"],
    "bot_id": self.bot_id,
    "source": source,  # NEW: "file" or "websocket"
    "timestamp": datetime.utcnow().isoformat() + "Z",  # NEW: ISO timestamp
    "success": task_result.get("success", False),
    "response": task_result.get("output", ""),
    "files_modified": task_result.get("files_modified", []),
    "error": task_result.get("error"),
    "duration_seconds": (datetime.utcnow() - start_time).total_seconds()
}
```

### 2. Update: `run_once()` method

When executing tasks from different sources, pass source parameter:

```python
async def run_once(self):
    # Check WebSocket queue first
    if self.websocket_queue.has_task():
        task = await self.websocket_queue.get_task()
        response = await self.execute_task(task)
        await self._write_response(response, source="websocket")  # NEW param
        return

    # Check file queue second
    if self.has_file_task():
        task = self.read_file_task()
        response = self.execute_task(task)
        self._write_response(response, source="file")  # NEW param
        return
```

### 3. Timestamp Format Specification

**Standard:** ISO 8601 with Z suffix
```
2025-10-28T14:05:30Z
```

**Implementation:**
```python
from datetime import datetime
timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
```

**Why Z suffix?**
- Indicates UTC time (Zulu time)
- No ambiguity about timezone
- Standard for APIs and timeline

### 4. Update Response File Writing

Response files should include tags:

**Filename remains same:**
```
.deia/hive/responses/TASK-002-011-response.md
```

**Content now includes:**
```markdown
# Response to TASK-002-011

**Task ID:** TASK-002-011
**Bot ID:** BOT-002
**Source:** file | websocket
**Timestamp:** 2025-10-28T14:05:30Z
**Status:** SUCCESS | FAILURE
**Duration:** 1200 seconds

## Response

[response content]

## Files Modified

- bot_runner.py
- bot_http_server.py

## Metadata

```json
{
  "source": "file",
  "timestamp": "2025-10-28T14:05:30Z",
  "success": true
}
```
```

### 5. Activity Logging Integration

Auto-logging (`.deia/bot-logs/BOT-002-activity.jsonl`) should already capture:
- Task processed
- Source
- Start/end timestamps
- Success/failure

Verify format includes these fields. If not, update BotActivityLogger.

---

## ACCEPTANCE CRITERIA

✅ **Response Format:**
- [ ] All responses include `task_id`
- [ ] All responses include `bot_id`
- [ ] All responses include `source` ("file" or "websocket")
- [ ] All responses include ISO 8601 timestamp with Z suffix
- [ ] All responses include `success` boolean
- [ ] Response content present and complete

✅ **Source Tagging:**
- [ ] File queue tasks tagged: `source: "file"`
- [ ] WebSocket tasks tagged: `source: "websocket"`
- [ ] Tagging happens at response write time (not before)

✅ **Timestamp Accuracy:**
- [ ] Timestamp reflects actual completion time
- [ ] Timezone is UTC (Z suffix)
- [ ] Format is ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
- [ ] No manual timestamp override

✅ **Activity Log:**
- [ ] Activity log entries include source tag
- [ ] Activity log entries include timestamps
- [ ] Logs show task_id and bot_id

✅ **Backwards Compatibility:**
- [ ] Old tasks without source tag still processable
- [ ] No breaking changes to response writer
- [ ] File paths unchanged

✅ **Testing:**
- [ ] Queue test file task: TASK-002-100
- [ ] Queue test WebSocket task (via HTTP)
- [ ] Verify both have source tags
- [ ] Verify both have timestamps
- [ ] Check timeline can distinguish them

---

## IMPLEMENTATION NOTES

### Source Tag Decision

At what point do we know the source?

**Option A (GOOD):** Tag at write time based on which queue the task came from
```python
def run_once(self):
    task = self.get_next_task()  # Could come from either source
    source = "websocket" if task.came_from_websocket else "file"
    # Execute...
    self._write_response(response, source=source)
```

**Option B (BETTER):** Pass source through execution chain
```python
def run_once(self):
    ws_task = self.websocket_queue.get()
    if ws_task:
        # Execute and tag as websocket
        self._write_response(response, source="websocket")
    else:
        # Execute and tag as file
        file_task = self.file_queue.get()
        self._write_response(response, source="file")
```

Use **Option B** - clearer and less error-prone.

### Timestamp Granularity

Should we capture:
- Start of task execution?
- End of task execution?

**Answer:** End of execution (completion timestamp)
- More useful for timeline (when did work finish?)
- Easier to capture (at response write time)
- Duration already calculated

### Activity Log Consistency

Ensure bot_activity_logger.py also captures:
```json
{
  "timestamp": "2025-10-28T14:05:30Z",
  "task_id": "TASK-002-011",
  "source": "file",
  "success": true,
  "duration_seconds": 1200
}
```

---

## DELIVERABLES

1. ✅ Modified: `src/deia/adapters/bot_runner.py`
   - Add source parameter to response writing
   - Add timestamp to response format
   - Update run_once() to pass source

2. ✅ Test proof: Response files with tags
   - Show examples with source: file
   - Show examples with source: websocket
   - Show timestamp in ISO format

3. ✅ Activity log verification
   - Show activity entries include tags
   - Show timestamps recorded

4. ✅ Response document
   - Confirm tags working
   - Confirm timestamps accurate
   - Report any issues

---

## VERIFICATION TEST

After implementation:

```bash
# 1. Queue file task
cat > .deia/hive/tasks/BOT-002/TASK-002-100-P2-test-tagging.md << 'EOF'
# TASK-002-100: Test Response Tagging

Test that response includes source and timestamp tags.
EOF

# 2. Wait for response
sleep 10
ls .deia/hive/responses/TASK-002-100*

# 3. Check content
cat .deia/hive/responses/TASK-002-100-response.md

# Should show:
# Source: file
# Timestamp: 2025-10-28T14:XX:XXZ

# 4. Check activity log
tail -5 .deia/bot-logs/BOT-002-activity.jsonl | grep TASK-002-100
# Should show: "source": "file", "timestamp": "..."
```

---

## FOLLOW-UP

This task enables:
- TASK-002-014: Timeline API endpoint (needs source and timestamp)
- TASK-002-015: WebSocket streaming (needs source tags)

---

## NOTES

**Why this matters for unified timeline:**
- Timeline will merge file + WebSocket responses
- Source tag shows which channel (for debugging)
- Timestamp enables proper chronological ordering
- Together: complete audit trail of bot interactions

**Complexity:** Low
- Just adding two fields to response format
- Uses standard Python datetime
- No architecture changes needed

---

**Priority:** P1 (required for timeline)
**Status:** Ready for execution
**Assigned to:** BOT-002

