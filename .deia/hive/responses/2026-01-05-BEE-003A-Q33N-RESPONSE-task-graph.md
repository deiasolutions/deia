# Response: TASK-009 - Task Graph Builder

**Task ID:** TASK-009
**Completed by:** BEE-003A
**Date:** 2026-01-05
**Status:** COMPLETE

---

## Summary

Created `deia_raqcoon/runtime/task_graph.py` - a task graph builder that converts specs into executable task graphs with dependency resolution, topological sorting, and task file creation.

---

## File Created

| File | Lines | Description |
|------|-------|-------------|
| `deia_raqcoon/runtime/task_graph.py` | ~280 | Task graph builder module |

---

## Features Implemented

| Feature | Description | Status |
|---------|-------------|--------|
| `TaskNode` | Dataclass for task with status tracking | Done |
| `TaskGraph` | Container with nodes and execution order | Done |
| `get_ready_tasks()` | Return tasks with satisfied dependencies | Done |
| `mark_complete()` | Update status, return newly unblocked | Done |
| `mark_in_progress()` | Mark task as in progress | Done |
| `mark_blocked()` | Mark task as blocked | Done |
| `get_parallel_groups()` | Group tasks by execution depth | Done |
| `_topological_sort()` | Kahn's algorithm with cycle detection | Done |
| `build_task_graph()` | Main entry point from spec | Done |
| `create_task_files()` | Generate actual task files | Done |

---

## Test Output

```
Execution order: ['TASK-001', 'TASK-002', 'TASK-003', 'TASK-004']
Parallel groups: [['TASK-001'], ['TASK-002', 'TASK-003'], ['TASK-004']]
Ready tasks: ['TASK-001']

Marking TASK-001 complete...
Newly ready: ['TASK-002', 'TASK-003']
Ready tasks: ['TASK-002', 'TASK-003']

Testing circular dependency detection...
Correctly detected: Circular dependency detected involving: {'C', 'A', 'B'}
```

---

## Test Results

| Test | Expected | Actual | Pass |
|------|----------|--------|------|
| Execution order | `['TASK-001', 'TASK-002', 'TASK-003', 'TASK-004']` | Same | Yes |
| Parallel groups | `[['TASK-001'], ['TASK-002', 'TASK-003'], ['TASK-004']]` | Same | Yes |
| Initial ready tasks | `['TASK-001']` | Same | Yes |
| Newly ready after complete | `['TASK-002', 'TASK-003']` | Same | Yes |
| Circular detection | Raises ValueError | Raised | Yes |

---

## Success Criteria Verification

- [x] Builds graph from spec with proper node creation
- [x] Topological sort produces correct order
- [x] Detects circular dependencies with clear error
- [x] `get_ready_tasks()` returns tasks with no pending dependencies
- [x] `mark_complete()` correctly updates dependent tasks
- [x] `get_parallel_groups()` identifies parallelizable tasks
- [x] `create_task_files()` creates valid task files using existing `write_task()`
- [x] All tests pass when run directly

---

## Design Decisions

1. **Kahn's algorithm for topological sort** - Chosen for simplicity and clear cycle detection
2. **Deterministic ordering** - Queue is sorted to ensure reproducible execution order
3. **Status transitions** - Tasks start as `pending`, become `ready` when deps satisfied
4. **Parallel groups by depth** - Simple depth calculation identifies parallelizable batches
5. **Integration with existing `write_task()`** - Reuses core task file creation logic

---

## Usage Example

```python
from deia_raqcoon.runtime.task_graph import build_task_graph, create_task_files

spec = {
    "spec_id": "SPEC-001",
    "title": "My Feature",
    "tasks": [
        {"task_id": "T1", "title": "Setup", "intent": "code", "depends_on": []},
        {"task_id": "T2", "title": "Implement", "intent": "code", "depends_on": ["T1"]},
        {"task_id": "T3", "title": "Test", "intent": "test", "depends_on": ["T2"]},
    ]
}

graph = build_task_graph(spec)
print(graph.execution_order)  # ['T1', 'T2', 'T3']
print(graph.get_parallel_groups())  # [['T1'], ['T2'], ['T3']]

# Create actual task files
paths = create_task_files(graph, repo_root=Path("."), default_assignee="BEE-001A")
```

---

*BEE-003A - SPRINT-002*
