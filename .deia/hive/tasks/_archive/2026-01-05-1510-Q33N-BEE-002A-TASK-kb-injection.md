# Task Assignment: TASK-003 - Implement KB Injection into Tasks

**Task ID:** TASK-003
**Assigned to:** BEE-002A
**Assigned by:** Q33N
**Priority:** P0 - Critical
**Sprint:** SPRINT-001 (Integration Wiring)
**Status:** QUEUED - Start after BEE-001A completes TASK-001
**Depends On:** TASK-001 (to avoid merge conflicts in create_task())

---

## Task

Implement actual KB content injection into task payloads. Currently, `create_task()` stores KB entity IDs but never retrieves or injects the actual content. The `preview_injection()` function exists but is never called during task creation.

---

## Current State

```python
# server.py - create_task()
payload = {
    "kb_entities": request.kb_entities,  # Just stores IDs - content never retrieved!
    # ...
}
```

The `preview_injection` function is already imported but unused in task creation:
```python
from deia_raqcoon.kb.store import list_entities, preview_injection, upsert_entity
```

---

## Required Changes

### 1. Modify create_task() to inject KB content

After building the base payload (and after routing is added by TASK-001), add KB injection:

```python
@app.post("/api/tasks")
def create_task(request: TaskRequest) -> Dict:
    repo_root = Path(request.repo_root).resolve() if request.repo_root else Path.cwd().resolve()

    # Route based on intent (added by TASK-001)
    routing = decide_route({"intent": request.intent})

    payload = {
        "task_id": request.task_id or "TASK-NEW",
        "intent": request.intent,
        "title": request.title,
        "summary": request.summary,
        "kb_entities": request.kb_entities,
        "delivery": {"mode": request.delivery_mode},
        "routing": {
            "lane": routing.lane,
            "provider": routing.provider,
            "delivery": routing.delivery,
        },
    }

    # KB Injection - retrieve actual content for entity IDs
    if request.kb_entities:
        kb_content = preview_injection(request.kb_entities)
        if request.delivery_mode == "cache_prompt":
            payload["cache_prompt_content"] = kb_content
        elif request.delivery_mode == "task_file":
            payload["kb_injection"] = kb_content
        elif request.delivery_mode == "both":
            payload["cache_prompt_content"] = kb_content
            payload["kb_injection"] = kb_content

    path = write_task(repo_root, request.bot_id, payload)
    return {"success": True, "path": str(path), "routing": payload["routing"]}
```

### 2. Update task_files.py to include kb_injection in written file

Check if `write_task()` in `core/task_files.py` includes `kb_injection` in the written file. If not, ensure it's included in the task file output.

---

## Files to Modify

| File | Action |
|------|--------|
| `deia_raqcoon/runtime/server.py` | Add KB injection logic to `create_task()` |
| `deia_raqcoon/core/task_files.py` | Ensure `kb_injection` field is written to task file (if needed) |

---

## Success Criteria

- [ ] `preview_injection()` called when `kb_entities` list is non-empty
- [ ] KB content included in task payload (not just IDs)
- [ ] `delivery_mode` respected:
  - `cache_prompt` -> content in `cache_prompt_content` field
  - `task_file` -> content in `kb_injection` field
  - `both` -> content in both fields
- [ ] Empty `kb_entities` list handled gracefully (no error, no injection)
- [ ] Task file on disk contains the injected KB content

---

## Test Commands

```bash
# Step 1: Create a KB entity first
curl -X POST http://127.0.0.1:8010/api/kb/entities \
  -H "Content-Type: application/json" \
  -d '{"id":"RULE-TEST","type":"RULE","title":"Test Rule","summary":"Never do X under any circumstances","tags":["test"],"delivery_mode":"task_file","load_mode":"always"}'

# Step 2: Create task with that entity
curl -X POST http://127.0.0.1:8010/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"bot_id":"TEST-001","intent":"code","title":"Test KB Injection","summary":"Test that KB content is injected","kb_entities":["RULE-TEST"],"delivery_mode":"task_file"}'

# Step 3: Read the created task file and verify it contains "Never do X" (the rule content), not just "RULE-TEST" (the ID)
```

---

## Rules

1. Only modify the files listed above
2. Do not change the KB store logic itself - just call existing functions
3. Preserve all existing functionality including routing (from TASK-001)
4. Handle edge cases: empty list, non-existent entity IDs
5. Follow existing code style

---

## Deliverable

**On Completion:**
1. Create response file: `.deia/hive/responses/2026-01-05-BEE-002A-Q33N-RESPONSE-kb-injection.md`
2. Include:
   - Summary of changes made
   - Exact lines modified
   - Test output showing KB content in task file
   - Any issues encountered
3. Archive this task file to `.deia/hive/tasks/_archive/`

---

## Working Directory

```
working_dir: C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions
allowed_paths:
  - deia_raqcoon/
  - .deia/hive/
```

---

*Q33N Assignment - SPRINT-001*
