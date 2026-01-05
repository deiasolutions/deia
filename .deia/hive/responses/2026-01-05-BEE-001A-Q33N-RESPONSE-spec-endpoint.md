# BEE-001A Response: TASK-007 - Create /api/spec/plan Endpoint

**Task ID:** TASK-007
**Assigned by:** Q33N
**Completed by:** BEE-001A
**Date:** 2026-01-05
**Status:** COMPLETE

---

## Summary

Created the `/api/spec/plan` endpoint in `server.py` that accepts a spec (JSON or markdown), validates it, builds a task graph, and optionally creates task files.

---

## Changes Made

| File | Action | Lines |
|------|--------|-------|
| `deia_raqcoon/runtime/server.py` | ADD imports | +2 lines |
| `deia_raqcoon/runtime/server.py` | ADD SpecPlanRequest model | +7 lines |
| `deia_raqcoon/runtime/server.py` | ADD /api/spec/plan endpoint | +55 lines |

---

## Imports Added

```python
from deia_raqcoon.runtime.spec_parser import parse_spec_markdown, validate_spec
from deia_raqcoon.runtime.task_graph import build_task_graph, create_task_files
```

---

## Request Model

```python
class SpecPlanRequest(BaseModel):
    spec: Optional[Dict] = None          # JSON spec directly
    spec_markdown: Optional[str] = None  # Or markdown to parse
    create_tasks: bool = False           # Actually create task files
    flight_id: Optional[str] = None      # Associate with flight
    bot_id: Optional[str] = None         # Default assignee for tasks
    repo_root: Optional[str] = None
```

---

## Test Results

| Test | Input | Expected | Actual | Pass |
|------|-------|----------|--------|------|
| JSON spec | 2 tasks with dependency | execution_order = [TASK-001, TASK-002] | Same | Yes |
| Markdown spec | Markdown with 1 task | Parsed task graph | Parsed correctly | Yes |
| Create tasks | create_tasks=true | tasks_created contains path | Path returned | Yes |
| Invalid spec | Missing required fields | success=false, error message | Error returned | Yes |
| No input | Empty object | success=false, error message | Error returned | Yes |

---

## Test 1: JSON Spec Output

```json
{
  "success": true,
  "spec_id": "SPEC-TEST-001",
  "execution_order": ["TASK-001", "TASK-002"],
  "ready_tasks": ["TASK-001"],
  "tasks_created": []
}
```

---

## Test 2: Markdown Spec Output

```json
{
  "success": true,
  "spec_id": "SPEC-MD-001",
  "execution_order": ["TASK-001"],
  "ready_tasks": ["TASK-001"]
}
```

---

## Test 3: Create Tasks Output

```json
{
  "success": true,
  "spec_id": "SPEC-CREATE-001",
  "tasks_created": [".deia/hive/tasks/TEST-BOT/2026-01-05-...-TASK-TASK-001.json"]
}
```

---

## Test 4: Invalid Spec Output

```json
{
  "success": false,
  "error": "Invalid spec: Missing required field: spec_id"
}
```

---

## Success Criteria Verification

- [x] Endpoint accepts JSON spec directly
- [x] Endpoint accepts markdown and parses it
- [x] Returns error if neither spec nor spec_markdown provided
- [x] Validates spec against schema before processing
- [x] Returns validation errors with clear messages
- [x] Returns task graph with execution order
- [x] Returns list of ready tasks (no dependencies)
- [x] `create_tasks=True` creates actual task files
- [x] Created tasks appear in `.deia/hive/tasks/{bot_id}/`

---

## Integration Notes

The endpoint integrates:
- `spec_parser.py` (TASK-008 by BEE-002A) for markdown parsing
- `task_graph.py` (TASK-009 by BEE-003A) for graph building
- `spec.json` schema (TASK-006 by BEE-001A) for validation

---

*BEE-001A - SPRINT-002 - TASK-007 Complete*
