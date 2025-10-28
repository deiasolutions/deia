# RESPONSE SOURCE TAGGING IMPLEMENTATION

**Task ID:** TASK-002-006
**Status:** COMPLETE
**Date:** 2025-10-28
**Purpose:** Enable Commandeer to distinguish between file-based and WebSocket responses

---

## OVERVIEW

Response source tagging allows Commandeer UI to build a unified timeline showing:
- Which responses came from file-based task queue
- Which responses came from WebSocket/chat
- When each response was generated
- Which bot generated it

This enables a single conversation view mixing both async (file) and real-time (chat) interactions.

---

## IMPLEMENTATION CHANGES

### File Location
`src/deia/adapters/bot_runner.py` - `run_once()` method (lines 165-318)

### Change #1: Modify write_response_file() Call

**Current code (lines 271-278):**
```python
response_file = write_response_file(
    response_dir=self.response_dir,
    from_bot=self.bot_id,
    to_bot=task["from"],
    task_id=task_id,
    result=result
)
```

**Modified code:**
```python
response_file = write_response_file(
    response_dir=self.response_dir,
    from_bot=self.bot_id,
    to_bot=task["from"],
    task_id=task_id,
    result=result,
    source="file",  # NEW: Tag this as file-based response
    timestamp=datetime.now().isoformat()  # NEW: ISO timestamp
)
```

---

### Change #2: Add source and timestamp to response object

**Location:** Before `write_response_file()` call (after line 266)

**Add this code:**
```python
# Tag response with source and timestamp
result["source"] = "file"
result["bot_id"] = self.bot_id
result["timestamp"] = datetime.now().isoformat()
```

---

### Change #3: Update write_response_file() signature

**File:** `src/deia/adapters/claude_code_adapter.py`

**Current function signature:**
```python
def write_response_file(
    response_dir: Path,
    from_bot: str,
    to_bot: str,
    task_id: str,
    result: Dict[str, Any]
) -> Path:
```

**Updated signature:**
```python
def write_response_file(
    response_dir: Path,
    from_bot: str,
    to_bot: str,
    task_id: str,
    result: Dict[str, Any],
    source: str = "file",  # NEW parameter
    timestamp: Optional[str] = None  # NEW parameter
) -> Path:
```

---

### Change #4: Include tags in response file content

**Inside write_response_file(), when building response JSON:**

**Add to response JSON:**
```python
response_data = {
    "task_id": task_id,
    "from_bot": from_bot,
    "to_bot": to_bot,
    "source": source,  # NEW: "file" or "chat"
    "timestamp": timestamp or datetime.now().isoformat(),  # NEW: ISO timestamp
    "bot_id": result.get("bot_id"),  # NEW: Which bot generated response
    # ... existing fields
    "success": result.get("success"),
    "response": result.get("response"),
    "files_modified": result.get("files_modified", []),
    "errors": result.get("error"),
    "completed_at": result.get("completed_at"),
    "duration_seconds": result.get("duration_seconds")
}
```

---

## COMMANDEER INTEGRATION

### How Commandeer Uses Tags

**Building Unified Timeline:**
```javascript
// Pseudocode - in Commandeer UI timeline builder
const timeline = [];

// Read all response files
for each response_file in responses_dir:
    const response = JSON.parse(response_file);

    if (response.source === "file") {
        // Display as: "[BOT-002] Completed TASK-002-001"
        timeline.push({
            type: "bot_response",
            source: "file",
            bot_id: response.bot_id,
            task_id: response.task_id,
            timestamp: response.timestamp,
            content: response.response
        });
    } else if (response.source === "chat") {
        // Display as: "[BOT-002 Chat] <response>"
        timeline.push({
            type: "chat_response",
            source: "chat",
            bot_id: response.bot_id,
            timestamp: response.timestamp,
            content: response.response
        });
    }

// Sort by timestamp, display mixed
timeline.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
```

---

## FUTURE: WebSocket/Chat Mode Support

When Hybrid or Commander-Only modes are implemented, the bot runner will also tag WebSocket responses:

```python
# In future websocket_handler() method
response_data = {
    "source": "chat",  # Instead of "file"
    "timestamp": datetime.now().isoformat(),
    "bot_id": self.bot_id,
    # ... response content
}

# Send via WebSocket to Commandeer
await websocket.send(json.dumps(response_data))
```

---

## RESPONSE FILE FORMAT (AFTER IMPLEMENTATION)

**Example response file with tags:**

```json
{
    "task_id": "TASK-002-001",
    "from_bot": "BOT-002",
    "to_bot": "Q33N",
    "source": "file",
    "timestamp": "2025-10-28T14:18:30Z",
    "bot_id": "BOT-002",
    "success": true,
    "response": "Checkin report: BOT-002 is alive and ready",
    "files_modified": [],
    "errors": null,
    "completed_at": "2025-10-28T14:18:30Z",
    "duration_seconds": 45
}
```

---

## COMMANDEER TIMELINE EXAMPLE

**Unified timeline view (mixed file + chat):**

```
[14:18:00] BOT-002 → File response (TASK-002-001)
          "Checkin: BOT-002 operational"

[14:18:15] Q33N → Chat message
          "Great! Now review the framework"

[14:18:30] BOT-002 → File response (TASK-002-002)
          "Framework verified: 3 modes correctly defined"

[14:18:45] BOT-002 → Chat response (live streaming)
          "Adding documentation to framework..."
          [Bot is working in real-time]

[14:19:00] BOT-002 → File response (TASK-002-003)
          "Bot inventory audit complete"

[14:19:15] Q33N → Chat message
          "Excellent. Update the ScrumMaster protocol next."
```

---

## IMPLEMENTATION PRIORITY

**Critical (blocks timeline feature):**
1. Add `source` and `timestamp` to response JSON
2. Update `write_response_file()` to accept source parameter
3. Ensure all file-based responses tagged with "file"

**Important (enables Commandeer integration):**
4. Add `bot_id` to response JSON
5. Document response format for Commandeer

**Future (for WebSocket modes):**
6. WebSocket response handler using same tags
7. Commandeer timeline builder consuming tags

---

## TESTING CHECKLIST

- [ ] Response file contains `"source": "file"`
- [ ] Response file contains valid ISO `timestamp`
- [ ] Response file contains `bot_id`
- [ ] Response format is valid JSON
- [ ] Existing responses still work (backward compatible)
- [ ] Commandeer can parse tagged responses
- [ ] Timeline displays both file and chat responses

---

## BENEFITS

✅ **Unified Timeline:** Single view of all bot interactions
✅ **Source Clarity:** Know where each response came from
✅ **Timestamp Tracking:** Exact timing of responses
✅ **Future-Ready:** Same format for WebSocket responses
✅ **Audit Trail:** Persistent record with metadata
✅ **Extensible:** Easy to add more tags/metadata

---

## NEXT STEPS FOR COMMANDEER

1. Parse response files and extract source/timestamp
2. Build unified timeline sorted by timestamp
3. Display file-based responses with task ID
4. Display WebSocket responses with chat indicator
5. Handle mixed async + real-time interactions
6. Support timeline filtering by source (file, chat, all)

---

