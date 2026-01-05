# SPRINT-002: Phase 1 Spec Intake

**Sprint ID:** SPRINT-002
**Created:** 2026-01-05
**Target Duration:** 1 day (6-8 working hours)
**Goal:** Turn a spec into a machine-readable plan and task graph

---

## 1. Sprint Overview

### 1.1 Problem Statement
The system can execute tasks but cannot autonomously create them from specifications. Users must manually create task files. Phase 1 enables automatic task decomposition from structured specs.

### 1.2 Success Criteria
- Spec schema defined and validated
- Markdown/spec documents can be parsed to JSON
- Task graph generated from parsed spec with dependencies
- `/api/spec/plan` endpoint accepts spec and returns task graph
- Integration test: spec in -> task files created

### 1.3 Out of Scope
- Task execution (Phase 2)
- Test verification (Phase 2)
- Git automation (Phase 3)
- Cost tracking (Phase 4)

---

## 2. Hive Structure

### 2.1 Q33N (Queen Bee) — Orchestrator

**Role:** Coordination, task sequencing, code review, integration testing

**Responsibilities:**
1. Assign tasks to worker bees based on dependencies
2. Review PRs/patches before marking complete
3. Run integration tests after each task completion
4. Write flight recap at sprint end

---

### 2.2 BEE-001A (Worker 1) — Schema & Endpoint Specialist

**Role:** Schema definition + API endpoint wiring

**Assigned Tasks:**
- TASK-006: Create spec.json schema
- TASK-007: Create /api/spec/plan endpoint

**Files to Create/Modify:**
- `deia_raqcoon/schemas/spec.json` (new)
- `deia_raqcoon/runtime/server.py` (add endpoint)

**Estimated Time:** 2-3 hours

---

### 2.3 BEE-002A (Worker 2) — Parser Specialist

**Role:** Spec parsing implementation

**Assigned Tasks:**
- TASK-008: Create runtime/spec_parser.py

**Files to Create:**
- `deia_raqcoon/runtime/spec_parser.py` (new)

**Estimated Time:** 2-3 hours

---

### 2.4 BEE-003A (Worker 3) — Graph Builder Specialist

**Role:** Task graph construction

**Assigned Tasks:**
- TASK-009: Create runtime/task_graph.py

**Files to Create:**
- `deia_raqcoon/runtime/task_graph.py` (new)

**Estimated Time:** 2-3 hours

---

## 3. Task Specifications

### TASK-006: Create Spec Schema

**Assignee:** BEE-001A
**Priority:** Critical
**Depends On:** None
**Estimated:** 1 hour

#### 3.6.1 Requirements

Create a JSON schema that defines valid spec documents:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["spec_id", "title", "goals", "acceptance_criteria"],
  "properties": {
    "spec_id": {
      "type": "string",
      "pattern": "^SPEC-[A-Z0-9-]+$"
    },
    "title": {
      "type": "string",
      "minLength": 5
    },
    "goals": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 1
    },
    "constraints": {
      "type": "array",
      "items": {"type": "string"}
    },
    "acceptance_criteria": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 1
    },
    "scope_exclusions": {
      "type": "array",
      "items": {"type": "string"}
    },
    "context": {
      "type": "object",
      "properties": {
        "project": {"type": "string"},
        "path": {"type": "string"},
        "kb_entities": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["task_id", "title", "intent"],
        "properties": {
          "task_id": {"type": "string"},
          "title": {"type": "string"},
          "intent": {"type": "string", "enum": ["code", "design", "planning", "test", "docs"]},
          "depends_on": {
            "type": "array",
            "items": {"type": "string"}
          },
          "assignee": {"type": "string"},
          "files": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    }
  }
}
```

#### 3.6.2 Acceptance Criteria
- [ ] Schema file created at `schemas/spec.json`
- [ ] Schema validates example spec documents
- [ ] All required fields documented
- [ ] Optional fields have sensible defaults

---

### TASK-007: Create /api/spec/plan Endpoint

**Assignee:** BEE-001A
**Priority:** Critical
**Depends On:** TASK-006, TASK-008, TASK-009
**Estimated:** 1.5 hours

#### 3.7.1 Requirements

Add endpoint to server.py that:
1. Accepts spec (JSON or markdown)
2. Validates against schema
3. Parses if markdown
4. Builds task graph
5. Optionally creates task files

```python
class SpecPlanRequest(BaseModel):
    spec: Optional[Dict] = None          # JSON spec directly
    spec_markdown: Optional[str] = None  # Or markdown to parse
    create_tasks: bool = False           # Actually create task files
    flight_id: Optional[str] = None      # Associate with flight
    repo_root: Optional[str] = None

@app.post("/api/spec/plan")
def plan_spec(request: SpecPlanRequest) -> Dict:
    # 1. Get spec (parse markdown if needed)
    # 2. Validate against schema
    # 3. Build task graph
    # 4. Optionally create task files
    # Return: {"success": True, "task_graph": {...}, "tasks_created": [...]}
```

#### 3.7.2 Acceptance Criteria
- [ ] Endpoint accepts JSON spec
- [ ] Endpoint accepts markdown spec (calls parser)
- [ ] Validates spec against schema
- [ ] Returns task graph with dependencies
- [ ] `create_tasks=true` creates actual task files
- [ ] Returns clear error if spec is invalid

---

### TASK-008: Create Spec Parser

**Assignee:** BEE-002A
**Priority:** Critical
**Depends On:** TASK-006 (needs schema to validate output)
**Estimated:** 2.5 hours

#### 3.8.1 Requirements

Create `runtime/spec_parser.py` that converts markdown specs to JSON:

```python
from typing import Dict, Optional
from pathlib import Path

def parse_spec_markdown(markdown: str) -> Dict:
    """
    Parse a markdown spec document into structured JSON.

    Expected markdown structure:
    # Spec Title

    ## Goals
    - Goal 1
    - Goal 2

    ## Constraints
    - Constraint 1

    ## Acceptance Criteria
    - [ ] Criterion 1
    - [ ] Criterion 2

    ## Out of Scope
    - Exclusion 1

    ## Tasks
    ### TASK-001: Task Title
    **Intent:** code
    **Depends On:** None
    **Files:** file1.py, file2.py

    Description of the task...
    """
    pass

def parse_spec_file(path: Path) -> Dict:
    """Load and parse a markdown spec file."""
    pass

def validate_spec(spec: Dict) -> tuple[bool, Optional[str]]:
    """Validate spec against schema. Returns (valid, error_message)."""
    pass
```

#### 3.8.2 Parsing Rules
- `# Title` -> `spec.title`
- `## Goals` section -> `spec.goals[]`
- `## Constraints` section -> `spec.constraints[]`
- `## Acceptance Criteria` section -> `spec.acceptance_criteria[]`
- `## Out of Scope` section -> `spec.scope_exclusions[]`
- `### TASK-XXX: Title` -> `spec.tasks[]`
- `**Intent:**` -> `task.intent`
- `**Depends On:**` -> `task.depends_on[]`
- `**Files:**` -> `task.files[]`

#### 3.8.3 Acceptance Criteria
- [ ] Parses markdown to valid spec JSON
- [ ] Extracts all required fields
- [ ] Handles missing optional sections gracefully
- [ ] Generates spec_id if not provided
- [ ] Returns validation errors for malformed markdown
- [ ] Unit tests for parser

---

### TASK-009: Create Task Graph Builder

**Assignee:** BEE-003A
**Priority:** Critical
**Depends On:** TASK-006 (needs spec structure)
**Estimated:** 2.5 hours

#### 3.9.1 Requirements

Create `runtime/task_graph.py` that builds executable task graph:

```python
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TaskNode:
    task_id: str
    title: str
    intent: str
    depends_on: List[str]
    assignee: Optional[str]
    files: List[str]
    status: str = "pending"  # pending, ready, in_progress, complete, blocked

@dataclass
class TaskGraph:
    spec_id: str
    nodes: Dict[str, TaskNode]
    execution_order: List[str]  # Topologically sorted

    def get_ready_tasks(self) -> List[TaskNode]:
        """Return tasks with all dependencies satisfied."""
        pass

    def mark_complete(self, task_id: str) -> List[str]:
        """Mark task complete, return newly unblocked tasks."""
        pass

    def to_dict(self) -> Dict:
        """Serialize for API response."""
        pass

def build_task_graph(spec: Dict) -> TaskGraph:
    """
    Build task graph from parsed spec.

    1. Create TaskNode for each task in spec
    2. Resolve dependencies
    3. Topological sort for execution order
    4. Detect circular dependencies
    """
    pass

def create_task_files(graph: TaskGraph, repo_root: Path, flight_id: Optional[str] = None) -> List[Path]:
    """
    Create actual task files from graph.
    Uses existing write_task() from task_files.py.
    """
    pass
```

#### 3.9.2 Graph Features
- Topological sort for execution order
- Detect and reject circular dependencies
- Track task status (pending, ready, complete)
- Identify parallelizable tasks (no shared dependencies)
- Associate tasks with flight if provided

#### 3.9.3 Acceptance Criteria
- [ ] Builds graph from spec
- [ ] Detects circular dependencies
- [ ] Returns correct execution order
- [ ] `get_ready_tasks()` returns parallelizable tasks
- [ ] `mark_complete()` updates dependents correctly
- [ ] `create_task_files()` creates valid task files
- [ ] Unit tests for graph operations

---

## 4. Task Dependencies & Sequencing

```
TASK-006 (Schema) ──────────────────────────────┐
                                                │
TASK-008 (Parser) ────────────depends on────────┤
                                                │
TASK-009 (Graph) ─────────────depends on────────┤
                                                ▼
                                         TASK-007 (Endpoint)
                                                │
                                                ▼
                                     Q33N Integration Test
```

**Execution Order:**
1. BEE-001A starts TASK-006 (schema) - **immediate**
2. BEE-002A starts TASK-008 (parser) - **after schema exists**
3. BEE-003A starts TASK-009 (graph) - **after schema exists**
4. BEE-001A does TASK-007 (endpoint) - **after parser + graph complete**

**Parallel Work:**
- TASK-008 and TASK-009 can run in parallel once TASK-006 is done

---

## 5. Integration Test Checklist

After all tasks complete, Q33N runs:

| # | Test | Expected |
|---|------|----------|
| 5.1 | Schema validates example | `validate_spec()` returns True |
| 5.2 | Parser converts markdown | Returns valid spec JSON |
| 5.3 | Graph builds from spec | Returns sorted execution order |
| 5.4 | Circular dep detected | Returns error for A->B->A |
| 5.5 | Endpoint accepts JSON | Returns task_graph in response |
| 5.6 | Endpoint accepts markdown | Parses then returns task_graph |
| 5.7 | create_tasks=true | Task files exist in .deia/hive/tasks/ |

---

## 6. Example Spec (For Testing)

```markdown
# SPEC-TEST-001: Add User Authentication

## Goals
- Users can log in with email/password
- Sessions persist across browser refresh
- Logout clears session

## Constraints
- No third-party auth providers
- Use existing User model
- Must work offline-first

## Acceptance Criteria
- [ ] Login form validates email format
- [ ] Password hashed with bcrypt
- [ ] Session stored in localStorage
- [ ] Logout removes session
- [ ] Tests pass for auth flow

## Out of Scope
- OAuth/social login
- Password reset flow
- Email verification

## Tasks

### TASK-001: Create Auth Service
**Intent:** code
**Depends On:** None
**Files:** src/services/auth.py

Implement AuthService class with login(), logout(), verify_session() methods.

### TASK-002: Add Login Endpoint
**Intent:** code
**Depends On:** TASK-001
**Files:** src/api/routes.py

Add POST /api/auth/login endpoint using AuthService.

### TASK-003: Create Login Form
**Intent:** code
**Depends On:** TASK-002
**Files:** src/ui/LoginForm.tsx

React component with email/password fields, validation, and submit.

### TASK-004: Write Auth Tests
**Intent:** test
**Depends On:** TASK-001, TASK-002
**Files:** tests/test_auth.py

Unit tests for AuthService and login endpoint.
```

---

## 7. Files Created/Modified Summary

| File | Task | Action |
|------|------|--------|
| deia_raqcoon/schemas/spec.json | TASK-006 | CREATE |
| deia_raqcoon/runtime/spec_parser.py | TASK-008 | CREATE |
| deia_raqcoon/runtime/task_graph.py | TASK-009 | CREATE |
| deia_raqcoon/runtime/server.py | TASK-007 | MODIFY (add endpoint) |

---

*End of Sprint Specification*
