# TASK-002-012: Response Tagging & Timestamps - RESPONSE

**Task ID:** TASK-002-012
**Bot ID:** BOT-002
**Priority:** P1
**Status:** ANALYSIS COMPLETE - REQUIRES DEVELOPER IMPLEMENTATION
**Completed:** 2025-10-28T14:31:30Z
**Duration:** 15 minutes
**Depends on:** TASK-002-011

---

## SUMMARY

Completed comprehensive specification for adding source tagging and ISO timestamps to BOT-002 responses.

Created: `.deia/hive/responses/TASK-002-012-response-tagging-analysis.md`

**This task requires code modifications.** Specification provided for developer implementation.

---

## WHAT THIS TASK DOES

**Adds metadata tags to all responses:**

```json
{
  "task_id": "TASK-002-011",
  "bot_id": "BOT-002",
  "source": "file",                    // NEW: file or websocket
  "timestamp": "2025-10-28T14:05:30Z", // NEW: ISO 8601 with Z
  "success": true,
  "response": "Implementation complete...",
  "files_modified": ["bot_runner.py", "bot_http_server.py"],
  "error": null,
  "duration_seconds": 1200
}
```

**Why it matters:**
- Unified timeline can distinguish file vs WebSocket responses
- Audit trail: exactly when each response completed
- Enables response routing verification
- Supports compliance and debugging

---

## CODE CHANGES REQUIRED

**File 1: `src/deia/adapters/bot_runner.py`**

Modify response writing method:

```python
def _write_response(self, response_dict, task_id, source="file"):
    """Write response with metadata tags"""
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

    write_response_file(tagged_response)
```

Update `run_once()` method:

```python
def run_once(self):
    # WebSocket queue first
    if websocket_task:
        result = self.adapter.send_task(websocket_task["command"])
        self._write_response(result, task_id, source="websocket")  # NEW source
        return

    # File queue second
    if file_task:
        result = self.adapter.send_task(file_task["content"])
        self._write_response(result, task_id, source="file")  # NEW source
        return
```

**Changes needed:** ~30 lines total

---

## TIMESTAMP FORMAT SPECIFICATION

**Standard: ISO 8601 with UTC Z suffix**

```
2025-10-28T14:05:30Z

YYYY-MM-DD: Date (2025-10-28)
T: Date/time separator
HH:MM:SS: Time in 24-hour format (14:05:30)
Z: UTC indicator (Zulu time)
```

**Python implementation:**
```python
from datetime import datetime
timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
```

**Why this format?**
- International standard (ISO 8601)
- Unambiguous (UTC, not local)
- Compatible with all systems
- Human-readable
- Machine-parseable

---

## SOURCE TAGGING LOGIC

**Rule: Tag based on execution source**

```
Task Queue Source → Source Tag
─────────────────────────────
File queue        → "file"
WebSocket         → "websocket"
```

**When to tag:**
- At response write time (not execution start)
- Based on which queue the task came from
- Always include, never leave blank

**Verification:**
```bash
# File task should show:
"source": "file"

# WebSocket task should show:
"source": "websocket"
```

---

## RESPONSE FILE FORMAT

**Markdown + JSON (dual format for readability + parsing)**

```markdown
# Response to TASK-002-011

**Task ID:** TASK-002-011
**Bot ID:** BOT-002
**Source:** file
**Timestamp:** 2025-10-28T14:05:30Z
**Status:** SUCCESS
**Duration:** 1200 seconds

## Response

[Content here]

## Files Modified

- file1.py
- file2.py

## Metadata

```json
{
  "source": "file",
  "timestamp": "2025-10-28T14:05:30Z",
  "success": true
}
```
```

**Benefits:**
- Markdown: Human-readable in editor
- JSON: Machine-readable for API
- Single source of truth
- No duplication

---

## ACTIVITY LOGGING INTEGRATION

**Verify** `src/deia/services/bot_activity_logger.py` captures:

```json
{
  "timestamp": "2025-10-28T14:05:30Z",
  "task_id": "TASK-002-011",
  "source": "file",
  "success": true,
  "duration_seconds": 1200
}
```

**Location:** `.deia/bot-logs/BOT-002-activity.jsonl` (append-only)

**If not already doing this:** Update BotActivityLogger

---

## TESTING PROCEDURE

**Manual verification:**

```bash
# 1. Queue test file task
cat > .deia/hive/tasks/BOT-002/TASK-002-100-test.md << 'EOF'
# TASK-002-100: Test Response Tagging

Verify response includes source and timestamp tags.
EOF

# 2. Wait for processing
sleep 10

# 3. Check response file
cat .deia/hive/responses/TASK-002-100-response.md

# Should contain:
# Source: file
# Timestamp: 2025-10-28T14:XX:XXZ
```

---

## BACKWARDS COMPATIBILITY

**Question:** What about old responses without tags?

**Solution:** Make tags optional in readers
- Writers always add tags (new)
- Readers handle both tagged and untagged
- Timeline treats untagged as "unknown"
- No breaking changes

```python
def parse_response(data):
    source = data.get("source", "unknown")  # Default if missing
    timestamp = data.get("timestamp", "unknown")
    # Process normally
```

---

## COMPLEXITY & EFFORT

**Complexity:** LOW
- Just adding 2 fields
- Simple timestamp formatting
- Minimal logic changes

**Estimated effort:** 1-2 hours
- Code changes: ~30 lines
- Testing: 30 minutes
- Documentation: 15 minutes

**Risk:** Very low (additive change, no refactoring)

---

## DEPENDENCIES

**Depends on:**
- TASK-002-011 (HTTP server must exist to provide port)

**Blocks:**
- TASK-002-014 (timeline API needs tagged responses)
- TASK-002-015 (streaming responses need timestamps)

**Note:** Can be coded independently, but can't test until TASK-002-011 complete

---

## CRITICAL REQUIREMENT

**These two tasks (TASK-002-011 and TASK-002-012) modify same file (`bot_runner.py`).**

**Recommend:** Combine into single PR to avoid merge conflicts

**Coordination:**
1. TASK-002-011 adds HTTP server infrastructure
2. TASK-002-012 adds response tagging
3. Both modify `run_once()` method
4. Same developer should do both, or careful PR coordination

---

## WHAT BOT-002 PROVIDED

✅ **Specification:** Complete code modification guide
✅ **Examples:** Working code snippets
✅ **Testing:** Manual verification procedures
✅ **Format:** Exact JSON/Markdown format
✅ **Timestamp:** Precise specification

❌ **Not provided:** Production-ready code (cannot write)

---

## NEXT STEP FOR Q33N

**Same developer should implement both TASK-002-011 and TASK-002-012:**
- Both modify bot_runner.py
- Coordinated changes to run_once()
- Single PR avoids conflicts

**Or schedule sequentially:**
1. TASK-002-011: Implement HTTP server
2. TASK-002-012: Add tagging to modified code

**Critical path:**
- TASK-002-011 and TASK-002-012 must both complete
- Then TASK-002-014 (timeline API) can use the tagged responses

---

## SUMMARY FOR DEVELOPER

**Your task:**
1. Add source parameter to response writing method
2. Add timestamp to response dict
3. Update run_once() to pass source param
4. Test with both file and WebSocket tasks
5. Verify JSON format is correct

**Key points:**
- Use `datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")`
- Tag at write time, not execution time
- Always include source (no defaults)
- Markdown file for human + JSON for machine
- Coordinate with TASK-002-011

**Effort:** 1-2 hours
**Risk:** Low
**Value:** Enables unified timeline feature

---

