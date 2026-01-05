# BEE-001A Response: TASK-001 - Router Wiring

**Task ID:** TASK-001
**Assigned by:** Q33N
**Completed by:** BEE-001A
**Date:** 2026-01-05
**Status:** COMPLETE

---

## Summary

Wired the existing `decide_route()` function from `core/router.py` into the task creation flow in `server.py`. Tasks now include routing decisions based on their intent field.

---

## Changes Made

### File: `deia_raqcoon/runtime/server.py`

#### Change 1: Added router import (line 16)
```python
from deia_raqcoon.core.router import decide_route
```

#### Change 2: Modified create_task() (lines 320-341)

**Before:**
```python
@app.post("/api/tasks")
def create_task(request: TaskRequest) -> Dict:
    repo_root = Path(request.repo_root).resolve() if request.repo_root else Path.cwd().resolve()
    payload = {
        "task_id": request.task_id or "TASK-NEW",
        "intent": request.intent,
        ...
    }
    path = write_task(repo_root, request.bot_id, payload)
    return {"success": True, "path": str(path)}
```

**After:**
```python
@app.post("/api/tasks")
def create_task(request: TaskRequest) -> Dict:
    repo_root = Path(request.repo_root).resolve() if request.repo_root else Path.cwd().resolve()

    # Route based on intent
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
    path = write_task(repo_root, request.bot_id, payload)
    return {"success": True, "path": str(path), "routing": payload["routing"]}
```

---

## Routing Behavior

| Intent | Lane | Provider | Delivery |
|--------|------|----------|----------|
| `code` | terminal | cli | task_file |
| `design` | llm | default | cache_prompt |
| `planning` | llm | default | cache_prompt |
| (other) | llm | default | cache_prompt |

---

## Success Criteria Verification

- [x] `from deia_raqcoon.core.router import decide_route` added to imports
- [x] `decide_route()` called for every `POST /api/tasks` request
- [x] Routing decision stored in task payload under `routing` key
- [x] Routing info returned in API response
- [x] Intent "code" routes to `lane=terminal`
- [x] Intent "design" routes to `lane=llm`

---

## Notes

- BEE-003A simultaneously added WebSocket improvements (ConnectionManager class)
- No merge conflicts - changes were to different sections of server.py
- Router logic itself unchanged - just wired in as requested

---

## Next Task

Proceeding to TASK-002: Complete Gate Enforcement

---

*BEE-001A - SPRINT-001*
