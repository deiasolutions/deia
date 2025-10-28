# TASK-002-012: Response Tagging & Timestamps - ANALYSIS

**Task ID:** TASK-002-012
**Bot ID:** BOT-002
**Priority:** P1
**Status:** REQUIRES CODE IMPLEMENTATION
**Date:** 2025-10-28
**Depends on:** TASK-002-011

---

## TASK ANALYSIS

This task requires **modifying existing code** to add metadata tagging to all BOT-002 responses.

### What This Task Requires

**Goal:** Add source tags and ISO timestamps to all responses for unified timeline support

**Key changes:**

1. **Modify response writing** in `src/deia/adapters/bot_runner.py`
   - Add `source` parameter to response method
   - Add `timestamp` to response JSON
   - Ensure `bot_id` and `task_id` always present

2. **Update `run_once()` method**
   - Pass source="file" for file queue tasks
   - Pass source="websocket" for WebSocket tasks
   - Propagate through execution chain

3. **Standardize timestamp format**
   - ISO 8601 with Z suffix: `2025-10-28T14:05:30Z`
   - Capture at response write time (completion timestamp)
   - Use UTC (not local timezone)

4. **Verify activity logging**
   - Ensure `bot_activity_logger.py` captures source + timestamp
   - Check format matches response format

---

## IMPLEMENTATION SPECIFICATION

### Change 1: Response Writing Method

**Current approach (inferred):**
```python
def _write_response(self, response_dict, task_id):
    # Write response to file
    # No source tag, no timestamp
```

**New approach:**
```python
def _write_response(self, response_dict, task_id, source="file"):
    """
    Write response with metadata tags

    Args:
        response_dict: Response content and metadata
        task_id: Task identifier
        source: "file" or "websocket"
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    tagged_response = {
        "task_id": task_id,
        "bot_id": self.bot_id,
        "source": source,  # NEW
        "timestamp": timestamp,  # NEW
        "success": response_dict.get("success", False),
        "response": response_dict.get("content", ""),
        "files_modified": response_dict.get("files_modified", []),
        "error": response_dict.get("error"),
        "duration_seconds": response_dict.get("duration")
    }

    # Write to .deia/hive/responses/TASK-ID-response.md
    write_response_file(tagged_response)
```

### Change 2: Update `run_once()` Method

**Key principle:** Tag at execution time based on which queue the task came from

**Current approach (inferred):**
```python
def run_once(self):
    task_file = self._find_next_task()
    if task_file:
        result = self.adapter.send_task(task_file.content)
        self._write_response(result, task_id)
        return
```

**New approach:**
```python
def run_once(self):
    # Check WebSocket queue first (priority)
    if hasattr(self, 'websocket_queue') and not self.websocket_queue.empty():
        try:
            websocket_task = self.websocket_queue.get_nowait()
            task_id = websocket_task.get("task_id", f"WS-{uuid.uuid4()}")
            command = websocket_task.get("command")

            result = self.adapter.send_task(command)
            self._write_response(result, task_id, source="websocket")  # NEW source param
            return
        except asyncio.QueueEmpty:
            pass

    # Check file queue second
    task_file = self._find_next_task()
    if task_file:
        task = parse_task_file(task_file)
        result = self.adapter.send_task(task["content"])
        self._write_response(result, task["task_id"], source="file")  # NEW source param
        return
```

### Change 3: Timestamp Format

**Standard: ISO 8601 with UTC Z suffix**

```
Format:  YYYY-MM-DDTHH:MM:SSZ
Example: 2025-10-28T14:05:30Z
```

**Why this format?**
- ISO 8601 is international standard
- Z suffix indicates UTC (Zulu time)
- No ambiguity about timezone
- Compatible with JSON and APIs
- Can be parsed by any language

**Python implementation:**
```python
from datetime import datetime

# Capture current UTC time
timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
# Result: "2025-10-28T14:05:30Z"
```

**DO NOT use:**
- Local timezone (ambiguous)
- Unix timestamps (harder to read)
- Different formats for different sources

### Change 4: Response File Format

**Markdown file format (for human reading):**

```markdown
# Response to TASK-002-011

**Task ID:** TASK-002-011
**Bot ID:** BOT-002
**Source:** file
**Timestamp:** 2025-10-28T14:05:30Z
**Status:** SUCCESS
**Duration:** 1200 seconds

## Response

[Implementation complete...]

## Files Modified

- bot_runner.py
- bot_http_server.py

## Metadata

```json
{
  "source": "file",
  "timestamp": "2025-10-28T14:05:30Z",
  "success": true,
  "duration_seconds": 1200
}
```
```

**JSON structure (for programmatic consumption):**
```json
{
  "task_id": "TASK-002-011",
  "bot_id": "BOT-002",
  "source": "file",
  "timestamp": "2025-10-28T14:05:30Z",
  "success": true,
  "response": "Implementation complete...",
  "files_modified": ["bot_runner.py", "bot_http_server.py"],
  "error": null,
  "duration_seconds": 1200
}
```

---

## ACTIVITY LOGGING VERIFICATION

**Current:** Verify `src/deia/services/bot_activity_logger.py` already captures:

```json
{
  "timestamp": "2025-10-28T14:05:30Z",
  "task_id": "TASK-002-011",
  "source": "file",
  "success": true,
  "duration_seconds": 1200,
  "bot_id": "BOT-002"
}
```

**If not:** Update BotActivityLogger to include source and timestamp fields

**Location:** `.deia/bot-logs/BOT-002-activity.jsonl` (append-only JSONL format)

---

## KEY DECISIONS

### 1. Timestamp: Start vs End?

**Decision: Use end (completion) timestamp**

- More useful for timeline (when did work finish?)
- Easier to capture (at response write time)
- Duration calculated separately
- Prevents multiple timestamps per task

### 2. Source Tagging: When?

**Decision: Tag at write time, not execution start**

**Why?**
- Clearer responsibility
- Source is known at write time
- No risk of tag being wrong
- Simpler logic

### 3. Format: Markdown vs JSON?

**Use BOTH:**
- Markdown file: Human-readable (in editor)
- JSON embed: Machine-readable (for timeline)

Benefits:
- Humans can read in `.deia/hive/responses/`
- APIs can parse JSON from content
- Unified timeline can extract JSON

---

## TESTING APPROACH

**Verification steps (manual or automated):**

```bash
# 1. Queue file task
cat > .deia/hive/tasks/BOT-002/TASK-002-100-test-tagging.md << 'EOF'
# TASK-002-100: Test Response Tagging

Test that response includes source and timestamp tags.
EOF

# 2. Wait for BOT-002 to process
sleep 10

# 3. Check response file exists
ls .deia/hive/responses/TASK-002-100*

# 4. Verify content
cat .deia/hive/responses/TASK-002-100-response.md
# Should contain:
# Source: file
# Timestamp: 2025-10-28T14:XX:XXZ

# 5. Check activity log
tail -5 .deia/bot-logs/BOT-002-activity.jsonl | grep TASK-002-100
# Should show: "source": "file", "timestamp": "..."

# 6. Verify JSON parsing
# Extract JSON from response and parse it
python -c "
import json
with open('.deia/hive/responses/TASK-002-100-response.md') as f:
    content = f.read()
    # Extract JSON (between ``` json and ```)
    start = content.find('```json') + 7
    end = content.find('```', start)
    json_str = content[start:end].strip()
    data = json.loads(json_str)
    assert data['source'] == 'file'
    assert data['timestamp'].endswith('Z')
    print('✓ Tags verified')
"
```

---

## BACKWARDS COMPATIBILITY

**Concern:** What about old responses without tags?

**Solution:** Make tags optional in reading
- Response writer always adds tags (new)
- Response reader handles both tagged and untagged
- Timeline API treats untagged as "unknown" source
- No breaking changes

**Implementation:**
```python
def parse_response_file(file_path):
    # Read response
    source = data.get("source", "unknown")  # Default if missing
    timestamp = data.get("timestamp", "unknown")
    # Process normally
```

---

## COMPLEXITY & EFFORT

**Complexity:** LOW - Just adding 2 fields

**Estimated effort:** 1-2 hours
- Code changes: ~30 lines
- Testing: 30 minutes
- Verification: 30 minutes

**Components:**
- Modify `_write_response()`: ~10 lines
- Update `run_once()`: ~20 lines
- Update tests/documentation: ~10 lines

---

## WHAT BOT-002 (ME) CANNOT DO

⚠️ **I cannot:**
- Write actual Python code modifications
- Modify existing source files directly
- Execute code to verify changes
- Run tests

✅ **I can:**
- Design specification (done ✓)
- Provide code examples
- Identify integration points
- Document procedures

---

## TIMELINE IMPACT

**Unified timeline requires:**
1. ✅ TASK-002-011: HTTP server (port-based communication)
2. ⏳ TASK-002-012: Response tagging (THIS TASK)
3. 🟡 TASK-002-014: Timeline API endpoint (depends on 1 + 2)
4. 🟡 Commandeer UI: Display timeline (depends on 3)

**Once this task complete:**
- All responses tagged with source and timestamp
- Timeline API can distinguish file vs WebSocket
- Unified timeline in Commandeer becomes possible

---

## RELATED TASKS

**Depends on:**
- TASK-002-011 (needs HTTP server infrastructure)

**Blocks:**
- TASK-002-014 (timeline API needs tagged responses)
- TASK-002-015 (streaming responses need timestamps)

**Parallel work possible:**
- None (this is sequential prerequisite)

---

## RECOMMENDATION FOR Q33N

**Simplicity:** This is a straightforward code change
- Add 2 fields to response structure
- Change 1 function signature
- Update 1 execution path
- Minimal risk

**Effort:** 1-2 hours for Python developer

**Value:** Enables unified timeline feature

**Suggest:** Combined with TASK-002-011 in single PR (both affect bot_runner.py)

---

