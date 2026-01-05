# Task Assignment: TASK-007 - Create /api/spec/plan Endpoint

**Task ID:** TASK-007
**Assigned to:** BEE-001A
**Assigned by:** Q33N
**Priority:** P0 - Critical
**Sprint:** SPRINT-002 (Spec Intake)
**Status:** QUEUED - Start after TASK-006, TASK-008, TASK-009 complete
**Depends On:** TASK-006 (schema), TASK-008 (parser), TASK-009 (graph)

---

## Task

Create the `/api/spec/plan` endpoint in server.py that accepts a spec (JSON or markdown), validates it, builds a task graph, and optionally creates task files.

---

## Requirements

### 1. Add Imports

```python
from deia_raqcoon.runtime.spec_parser import parse_spec_markdown, validate_spec
from deia_raqcoon.runtime.task_graph import build_task_graph, create_task_files
```

### 2. Add Request Model

```python
class SpecPlanRequest(BaseModel):
    spec: Optional[Dict] = None          # JSON spec directly
    spec_markdown: Optional[str] = None  # Or markdown to parse
    create_tasks: bool = False           # Actually create task files
    flight_id: Optional[str] = None      # Associate with flight
    bot_id: Optional[str] = None         # Default assignee for tasks
    repo_root: Optional[str] = None
```

### 3. Add Endpoint

```python
@app.post("/api/spec/plan")
def plan_spec(request: SpecPlanRequest) -> Dict:
    """
    Convert a spec into a task graph, optionally creating task files.

    Accepts either:
    - spec: JSON spec object
    - spec_markdown: Markdown text to parse

    Returns:
    - task_graph: Dependency-ordered list of tasks
    - execution_order: Topologically sorted task IDs
    - tasks_created: List of created task file paths (if create_tasks=True)
    """
    repo_root = Path(request.repo_root).resolve() if request.repo_root else Path.cwd().resolve()

    # 1. Get spec (parse markdown if needed)
    if request.spec:
        spec = request.spec
    elif request.spec_markdown:
        spec = parse_spec_markdown(request.spec_markdown)
    else:
        return {"success": False, "error": "Must provide spec or spec_markdown"}

    # 2. Validate against schema
    valid, error = validate_spec(spec)
    if not valid:
        return {"success": False, "error": f"Invalid spec: {error}"}

    # 3. Build task graph
    try:
        graph = build_task_graph(spec)
    except ValueError as e:
        return {"success": False, "error": str(e)}

    # 4. Optionally create task files
    tasks_created = []
    if request.create_tasks:
        tasks_created = create_task_files(
            graph,
            repo_root,
            flight_id=request.flight_id,
            default_assignee=request.bot_id
        )
        tasks_created = [str(p) for p in tasks_created]

    return {
        "success": True,
        "spec_id": spec.get("spec_id"),
        "task_graph": graph.to_dict(),
        "execution_order": graph.execution_order,
        "ready_tasks": [t.task_id for t in graph.get_ready_tasks()],
        "tasks_created": tasks_created,
    }
```

---

## Files to Modify

| File | Action |
|------|--------|
| `deia_raqcoon/runtime/server.py` | ADD imports, request model, endpoint |

---

## Success Criteria

- [ ] Endpoint accepts JSON spec directly
- [ ] Endpoint accepts markdown and parses it
- [ ] Returns error if neither spec nor spec_markdown provided
- [ ] Validates spec against schema before processing
- [ ] Returns validation errors with clear messages
- [ ] Returns task graph with execution order
- [ ] Returns list of ready tasks (no dependencies)
- [ ] `create_tasks=True` creates actual task files
- [ ] Created tasks appear in `.deia/hive/tasks/{bot_id}/`

---

## Test Commands

```bash
# Test 1: JSON spec
curl -X POST http://127.0.0.1:8010/api/spec/plan \
  -H "Content-Type: application/json" \
  -d '{
    "spec": {
      "spec_id": "SPEC-TEST-001",
      "title": "Test Spec",
      "goals": ["Test goal"],
      "acceptance_criteria": ["Test criterion"],
      "tasks": [
        {"task_id": "TASK-001", "title": "First task", "intent": "code"},
        {"task_id": "TASK-002", "title": "Second task", "intent": "code", "depends_on": ["TASK-001"]}
      ]
    }
  }'
# Expected: execution_order = ["TASK-001", "TASK-002"]

# Test 2: Markdown spec
curl -X POST http://127.0.0.1:8010/api/spec/plan \
  -H "Content-Type: application/json" \
  -d '{
    "spec_markdown": "# SPEC-MD-001: Test\n\n## Goals\n- Goal 1\n\n## Acceptance Criteria\n- Criterion 1\n\n## Tasks\n\n### TASK-001: First\n**Intent:** code\n"
  }'
# Expected: Parsed and returns task graph

# Test 3: Create tasks
curl -X POST http://127.0.0.1:8010/api/spec/plan \
  -H "Content-Type: application/json" \
  -d '{
    "spec": {
      "spec_id": "SPEC-CREATE-001",
      "title": "Create Tasks Test",
      "goals": ["Test creation"],
      "acceptance_criteria": ["Tasks created"],
      "tasks": [
        {"task_id": "TASK-001", "title": "Task to create", "intent": "code"}
      ]
    },
    "create_tasks": true,
    "bot_id": "TEST-BOT"
  }'
# Expected: tasks_created contains file path

# Test 4: Invalid spec
curl -X POST http://127.0.0.1:8010/api/spec/plan \
  -H "Content-Type: application/json" \
  -d '{"spec": {"title": "Missing required fields"}}'
# Expected: success=false, error describes missing fields
```

---

## Rules

1. Only modify server.py
2. Import from spec_parser.py and task_graph.py (they should exist)
3. Handle all error cases gracefully
4. Return clear error messages
5. Follow existing code patterns in server.py

---

## Deliverable

**On Completion:**
1. Create response file: `.deia/hive/responses/2026-01-05-BEE-001A-Q33N-RESPONSE-spec-endpoint.md`
2. Include:
   - Summary of changes
   - All test outputs
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

*Q33N Assignment - SPRINT-002*
