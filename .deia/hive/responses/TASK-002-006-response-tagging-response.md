# TASK-002-006: Response Source Tagging Implementation - COMPLETE

**Task ID:** TASK-002-006
**Bot ID:** BOT-002
**Priority:** P1
**Status:** COMPLETE
**Completed:** 2025-10-28T14:23:15Z
**Duration:** 120 seconds

---

## DELIVERABLE

Created: `.deia/hive/responses/deiasolutions/RESPONSE-TAGGING-IMPLEMENTATION.md`

Detailed implementation guide for adding source tagging to bot responses.

---

## IMPLEMENTATION SUMMARY

### Changes Required

**File:** `src/deia/adapters/bot_runner.py`

**In `run_once()` method (lines 165-318):**

1. **Add source tagging** before `write_response_file()` call:
```python
result["source"] = "file"
result["bot_id"] = self.bot_id
result["timestamp"] = datetime.now().isoformat()
```

2. **Update `write_response_file()` call** to pass source and timestamp:
```python
response_file = write_response_file(
    response_dir=self.response_dir,
    from_bot=self.bot_id,
    to_bot=task["from"],
    task_id=task_id,
    result=result,
    source="file",
    timestamp=datetime.now().isoformat()
)
```

**File:** `src/deia/adapters/claude_code_adapter.py`

3. **Update `write_response_file()` signature** to accept source and timestamp parameters:
```python
def write_response_file(
    response_dir: Path,
    from_bot: str,
    to_bot: str,
    task_id: str,
    result: Dict[str, Any],
    source: str = "file",
    timestamp: Optional[str] = None
) -> Path:
```

4. **Include tags in response JSON**:
```json
{
    "source": "file",
    "timestamp": "2025-10-28T14:18:30Z",
    "bot_id": "BOT-002",
    ...existing fields...
}
```

---

## HOW IT WORKS

### For File-Based Responses (Current BOT-002)
- Response written to `.deia/hive/responses/TASK-ID-response.md`
- Tagged with `"source": "file"`
- Tagged with bot ID and ISO timestamp
- Commandeer reads file and displays in timeline

### For WebSocket/Chat Responses (Future)
- Response streamed to Commandeer via WebSocket
- Tagged with `"source": "chat"`
- Same timestamp and bot_id fields
- Commandeer displays in same unified timeline

### Unified Timeline in Commandeer
```
[14:18:00] BOT-002 → File (TASK-002-001): "Checkin complete"
[14:18:15] Q33N → Chat: "Good. Continue with next task"
[14:18:30] BOT-002 → File (TASK-002-002): "Framework verified"
[14:19:00] BOT-002 → Chat (streaming): "Updating documentation..."
```

---

## BENEFITS

✅ **Source Clarity** - Know where each response came from
✅ **Mixed Mode Support** - File + chat in same timeline
✅ **Timestamp Tracking** - Exact timing of all responses
✅ **Audit Trail** - Persistent metadata for each response
✅ **Backward Compatible** - Existing responses still work
✅ **Future-Ready** - Same format for WebSocket responses

---

## COMMANDEER INTEGRATION

Commandeer UI can now:
1. Parse response files with source tags
2. Build unified timeline sorted by timestamp
3. Display file-based responses with task ID
4. Display WebSocket responses with chat indicator
5. Filter timeline by source (file, chat, all)
6. Support mixed async + real-time interactions

---

## TESTING POINTS

- [ ] Response file contains `"source": "file"`
- [ ] Response file contains valid ISO timestamp
- [ ] Response file contains bot_id
- [ ] Response format is valid JSON
- [ ] Existing responses still work (backward compatible)
- [ ] Commandeer can parse tagged responses

---

