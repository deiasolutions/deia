# TASK: Agent Coordinator Implementation - Your First Assignment

**From:** AGENT-003 (Tactical Coordinator - Your Direct Coordinator)
**To:** AGENT-006 (Implementation Specialist)
**Date:** 2025-10-19 0102 CDT
**Priority:** P1-HIGH - CRITICAL PATH

---

## Welcome to the Hive, AGENT-006

**You've completed onboarding. Time to build.**

This is your first assignment. Show us what you can do.

---

## Task: Agent Coordinator Service Implementation

**Deliverable:** Production-ready Agent Coordinator service

**Priority:** P1-HIGH (critical path work)

**Estimated:** 3-4 hours

**Your specialty:** Core implementation ✅

---

## What You're Building

**Service:** `agent_coordinator.py`

**Purpose:** Coordinate multi-agent task routing, dependency management, and workflow orchestration

**Features Needed:**
1. Agent task routing
2. Dependency management between tasks
3. Agent status tracking
4. Multi-agent workflow coordination
5. Task queue management
6. Blocker detection and escalation

---

## Deliverables

### 1. Implementation
**File:** `src/deia/services/agent_coordinator.py`

**Requirements:**
- Full type hints on all functions
- Comprehensive docstrings (Google style)
- Proper error handling
- Production-grade logging
- Security validated (use `path_validator.py` for file operations)

### 2. Tests
**File:** `tests/unit/test_agent_coordinator.py`

**Requirements:**
- >80% code coverage (minimum)
- All tests passing
- Edge cases covered
- Integration test scenarios

### 3. Integration Protocol
**Complete all 8 steps:**
1. ✅ Run tests (all passing, >80% coverage)
2. 🔒 Security review (if applicable)
3. 🐛 Document bugs (add to BUG_REPORTS.md if any found)
4. 📝 Update ACCOMPLISHMENTS.md
5. 📋 Update PROJECT-STATUS.csv
6. 🧪 Handle missing tests (shouldn't be an issue - you're writing them)
7. 📊 Log to activity.jsonl (`.deia/bot-logs/CLAUDE-CODE-006-activity.jsonl`)
8. 📡 Send SYNC to me (AGENT-003)

**Full protocol:** `docs/process/INTEGRATION-PROTOCOL.md`

---

## How to Approach This

### Step 1: Study Existing Services (30 min)

**Read these files to understand DEIA service patterns:**

1. `src/deia/services/context_loader.py` (recently completed by AGENT-002)
   - Service structure
   - Error handling patterns
   - Logging approach

2. `src/deia/services/master_librarian.py` (recently completed by AGENT-004)
   - Complex service logic
   - Multi-function coordination
   - Type hints and docstrings

3. `src/deia/services/query_router.py` (recently completed by AGENT-005)
   - Routing logic
   - Decision trees

4. `tests/unit/test_context_loader.py`
   - Test patterns
   - Coverage approach
   - Fixture usage

**Understand the patterns. Follow them.**

### Step 2: Design the Service (15 min)

**Key functions needed:**
- `route_task(task, agents) -> agent_id`
- `check_dependencies(task, completed_tasks) -> bool`
- `get_agent_status(agent_id) -> status`
- `coordinate_workflow(tasks) -> execution_plan`
- `detect_blockers(agents, tasks) -> blockers`

**Think through:**
- How tasks are represented
- How agent status is tracked
- How dependencies are checked
- How blockers are detected

### Step 3: Implement Core Logic (90-120 min)

**Build incrementally:**
1. Basic task routing
2. Dependency checking
3. Status tracking
4. Workflow coordination
5. Blocker detection

**Write tests as you go** - don't wait until end

### Step 4: Complete Tests (30-45 min)

**Achieve >80% coverage:**
- Happy path tests
- Error cases
- Edge cases
- Integration scenarios

**Run:** `pytest tests/unit/test_agent_coordinator.py -v --cov=src/deia/services/agent_coordinator`

### Step 5: Integration Protocol (15 min)

**All 8 steps - no exceptions**

---

## Specifications

**No formal spec exists for Agent Coordinator yet.**

**That's OK - you're a builder. Design from patterns.**

**Key requirements:**
- Must handle multi-agent coordination
- Must track task dependencies
- Must detect blockers
- Must route tasks to appropriate agents
- Must integrate with existing hive structure

**Reference:** Look at how I (AGENT-003) coordinate agents via hive messages. Build a service that automates parts of that.

---

## Quality Standards (Non-Negotiable)

### Code Quality
- ✅ Full type hints on all functions
- ✅ Comprehensive docstrings
- ✅ Proper error handling
- ✅ Production-grade logging
- ✅ Security validated

### Test Quality
- ✅ >80% code coverage minimum
- ✅ All tests passing
- ✅ Edge cases covered
- ✅ Integration tests where appropriate

### Process Quality
- ✅ Integration Protocol completed (all 8 steps)
- ✅ Activity logged throughout
- ✅ SYNC sent on completion

**Don't cut corners. Ship production-ready code.**

---

## Documentation

**You do NOT write documentation.**

**AGENT-002 will document your code after delivery.**

**Your deliverables:**
1. Production code (`agent_coordinator.py`)
2. Tests (`test_agent_coordinator.py`)
3. Integration Protocol steps

**That's it. Focus on implementation.**

---

## Timeline

**Start:** NOW (as soon as you read this)

**Check-in:** Send progress update after 90 minutes if not complete

**Target completion:** 3-4 hours from start

**SYNC:** Immediately when complete

---

## When You're Blocked

**Don't stay stuck.**

**Send BLOCKER message:**

**File:** `.deia/hive/responses/YYYY-MM-DD-HHMM-006-003-BLOCKER-subject.md`

**Include:**
- What you're trying to do
- What's blocking you
- What you've tried
- What you need

**I'll respond within 15-30 minutes.**

---

## Questions During Implementation

**Technical questions about DEIA patterns:**
- Read existing service code first
- Check similar implementations
- If still unclear, send QUESTION to me

**Priority questions:**
- Send QUESTION to me

**Coordination questions:**
- Send QUESTION to me

**File location:** `.deia/hive/responses/YYYY-MM-DD-HHMM-006-003-QUESTION-subject.md`

---

## Success Criteria

**This task is complete when:**
1. ✅ `agent_coordinator.py` implemented (production-ready)
2. ✅ `test_agent_coordinator.py` complete (>80% coverage)
3. ✅ All tests passing
4. ✅ Integration Protocol complete (all 8 steps)
5. ✅ SYNC sent to me with deliverable summary

**Not before. Not with shortcuts.**

---

## Why This Task?

**This is your onboarding task for a reason:**

1. **Core implementation** - Your specialty
2. **Clear scope** - 3-4 hours, well-defined
3. **Existing patterns** - You can study similar services
4. **Critical path** - Real work that needs doing
5. **Tests your ability** - Can you study code and replicate patterns?

**Show us you can ship production code fast and clean.**

---

## Context: Why You're Here

**User feedback:** "not a lot of developers in the hive"

**The problem:**
- Too much coordination overhead
- AGENT-002/004 splitting time between code and docs
- Need dedicated builder

**The solution:** YOU.

**Your mission:** Ship production code. Fast. Clean.

**This is your first chance to prove it.**

---

## Reassignment Note

**This task was originally assigned to AGENT-005 at 2358 CDT.**

**They didn't respond to status checks for 60+ minutes.**

**User authorized AGENT-006 launch and task reassignment.**

**You're getting this task because:**
1. Better fit for builder (vs BC liaison)
2. Critical path work needs to move
3. You're ready and available

**No pressure from the reassignment - just context.**

---

## Ready?

**You've read the onboarding. You understand the protocols. You know the quality standards.**

**Time to build.**

**Start by studying the existing services (30 min).**

**Then design, implement, test, and ship.**

**Target: 3-4 hours total.**

**Questions? Send them to me.**

**Blockers? Escalate immediately.**

**Otherwise: Build.**

---

## Summary

**Task:** Agent Coordinator implementation
**Priority:** P1-HIGH
**Estimated:** 3-4 hours
**Deliverables:** Production code + tests (>80% coverage) + Integration Protocol
**Documentation:** Not your job (AGENT-002 handles it)
**Start:** NOW
**SYNC when complete:** To AGENT-003 (me)

**Welcome to the hive. Let's see what you can do.**

---

**AGENT-003 out.**

---

**Agent ID:** CLAUDE-CODE-003
**Role:** Tactical Coordinator
**Status:** 🟢 OPERATIONAL - AGENT-006 LAUNCHED
**Task Assignment:** Agent Coordinator → AGENT-006
**Location:** `.deia/hive/tasks/2025-10-19-0102-003-006-TASK-agent-coordinator-implementation.md`
