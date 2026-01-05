# TASK: Gap Analyst & Bug Hunter

**Task ID**: BEE3-GAP-ANALYST
**Assigned To**: Claude Instance 3
**Priority**: High
**Status**: Pending

---

## Objective

Cross-reference spec against implementation to find gaps, missing pieces, and bugs. This is a READ-ONLY research task - no code changes.

---

## Approach

### Phase A: Direct Comparison (Start Immediately)
Compare these directly without waiting for Bee 1/2:
- `deia_raqcoon/docs/mvp-checklist.md` vs `deia_raqcoon/runtime/server.py`
- `deia_raqcoon/docs/2026-01-04-DEIA-RAQCOON-SPEC-IN-TO-CODE-OUT.md` vs actual files

### Phase B: Deep Analysis
After reviewing the code, check for logic bugs and wiring issues.

---

## Files to Review

**Spec files:**
- `deia_raqcoon/docs/mvp-checklist.md`
- `deia_raqcoon/docs/2026-01-04-DEIA-RAQCOON-SPEC-IN-TO-CODE-OUT.md`
- `deia_raqcoon/docs/architecture.md`

**Implementation files:**
- `deia_raqcoon/runtime/server.py` (primary)
- `deia_raqcoon/core/router.py`
- `deia_raqcoon/core/task_files.py`
- `deia_raqcoon/runtime/minder.py`
- `deia_raqcoon/kb/store.py`
- `deia_raqcoon/adapters/*.py`

---

## Deliverable

Create file: `.deia/hive/responses/2026-01-05-BEE3-GAP-ANALYSIS.md`

### Required Sections

```markdown
# BEE3: Gap Analysis & Bug Report

## 1. Missing Endpoints
Endpoints in spec but NOT in server.py:
| Endpoint | Method | Spec Source | Priority |
|----------|--------|-------------|----------|
| /api/spec/plan | POST | spec-in-to-code-out.md Phase 1 | High |
| /api/tasks/run | POST | spec-in-to-code-out.md Phase 2 | High |
| ... | ... | ... | ... |

## 2. Missing Files
Files mentioned in spec that don't exist:
| File Path | Purpose | Spec Source |
|-----------|---------|-------------|
| runtime/executor.py | Task execution loop | Phase 2 |
| runtime/verifier.py | Test runner | Phase 2 |
| ... | ... | ... |

## 3. Unconnected Code
Functions/classes that exist but aren't wired up:
| Item | File | Issue |
|------|------|-------|
| decide_route() | router.py | Defined but never called from server.py |
| ... | ... | ... |

## 4. Incomplete Implementations
Code exists but is a stub/placeholder:
| Item | File | What's Missing |
|------|------|----------------|
| WebSocket /api/ws | server.py | Only echoes, no real functionality |
| ... | ... | ... |

## 5. Logic Bugs
Code that won't work as written:
| Bug | File:Line | Issue | Severity |
|-----|-----------|-------|----------|
| ... | ... | ... | Critical/High/Medium/Low |

### Bug Hunting Checklist Results

- [ ] **Router unused**: Does `decide_route()` get called?
  - Finding: ...

- [ ] **Minder not scheduled**: Does `minder.py` have scheduled execution?
  - Finding: ...

- [ ] **PTY cleanup**: Are sessions cleaned up on disconnect?
  - Finding: ...

- [ ] **WebSocket functionality**: Is `/api/ws` doing anything useful?
  - Finding: ...

- [ ] **Git gate check**: Does commit check `allow_flight_commits`?
  - Finding: ...

- [ ] **Task archival**: Is `complete_task` working correctly?
  - Finding: ...

- [ ] **KB injection**: Is it actually used when creating tasks?
  - Finding: ...

## 6. MVP Checklist Status
For each MVP item, current status:
| Category | Item | Status | Notes |
|----------|------|--------|-------|
| Runtime | FastAPI app | DONE | server.py exists |
| Runtime | WebSocket /api/ws | PARTIAL | Exists but echo-only |
| ... | ... | ... | ... |

## 7. Priority Ranking
What to fix/build first for MVP:

### Critical (Blocks MVP)
1. ...

### High (Core functionality)
1. ...

### Medium (Important but not blocking)
1. ...

### Low (Nice to have)
1. ...

## 8. Recommended Next Steps
Ordered list of what to tackle:
1. ...
2. ...
3. ...
```

---

## Success Criteria

- [ ] All missing endpoints identified
- [ ] All missing files identified
- [ ] Unconnected code found
- [ ] Bug checklist completed
- [ ] MVP status table complete
- [ ] Priority ranking done
- [ ] Report created at correct path

---

## Notes

- You can start Phase A immediately in parallel with Bee 1 and Bee 2
- If Bee 1/Bee 2 reports become available, incorporate their findings
- Focus on actionable findings - what needs to be fixed/built
- Be specific about line numbers for bugs
