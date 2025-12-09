# Available Task Queue - Self-Serve

**Last Updated:** 2025-10-18 2245 CDT
**Coordinator:** AGENT-003

---

## How This Works

**Agents: When you complete your current task:**
1. Check this queue for available tasks
2. Pick a task that matches your skills AND capacity
3. Post a CLAIM message: `.deia/hive/responses/YYYY-MM-DD-HHMM-YOU-003-CLAIM-task-name.md`
4. Start work immediately (don't wait for approval)
5. Remove the claimed task from this queue (edit this file)

**No bottleneck. No waiting for me.**

---

## Priority 1 - HIGH (Do These First)

### P1-001: Agent Coordinator Implementation
**Estimated:** 3-4 hours
**Skills:** Python, integration, coordination systems
**Best For:** AGENT-002 (systems design) or AGENT-005 (integration)
**Status:** AVAILABLE

**What:** Implement agent coordination system for multi-agent workflows
**Files:**
- `src/deia/services/agent_coordinator.py`
- `tests/unit/test_agent_coordinator.py`
- `docs/services/AGENT-COORDINATOR.md`

**Requirements:**
- Agent task routing
- Dependency management
- Status tracking
- >80% test coverage

**Source:** Check Agent BC Phase 2 deliverables or design from DEIA patterns

---

### ~~P1-002: Project Browser Enhancement~~ ✅ COMPLETE
**Completed By:** AGENT-004 (2025-10-19 0020 CDT)
**Estimated:** 2-3 hours | **Actual:** 15 minutes
**Approach:** Documentation (existing code already exceeded requirements)

**Outcome:** Existing code had 89% test coverage (19 tests passing). Created comprehensive API documentation instead of enhancement. See `.deia/ACCOMPLISHMENTS.md` and `docs/services/PROJECT-BROWSER.md`.

---

## Priority 2 - MEDIUM (Do After P1)

### P2-001: Test Coverage Expansion
**Estimated:** 4-6 hours
**Skills:** Testing, pytest, Python
**Best For:** AGENT-003 (QA specialist) - **ME if I have capacity**
**Status:** AVAILABLE

**What:** Expand test coverage from 38% to 50%
**Target Modules:**
- cli.py (currently low coverage)
- cli_utils.py (currently low coverage)
- Additional service modules

**Requirements:**
- Focus on untested code paths
- Edge cases and error handling
- Integration tests where appropriate

---

### P2-002: Downloads Monitor - Temp Staging
**Estimated:** 2-3 hours
**Skills:** File systems, Python
**Best For:** AGENT-005 (file operations) or AGENT-002 (systems)
**Status:** AVAILABLE

**What:** Implement temp staging for downloads monitor
**Files:**
- `src/deia/services/downloads_monitor.py` (enhance existing)
- Tests and docs

**Requirements:**
- Safe temp staging before processing
- No auto-delete until git commit
- Privacy markings handling

---

### P2-003: Agent Directory Monitoring - Preference System
**Estimated:** 4-6 hours
**Skills:** File watching, configuration, CLI
**Best For:** AGENT-002 (systems design) or AGENT-005 (integration)
**Status:** AVAILABLE

**What:** Allow agents to configure automated directory monitoring
**Modes:**
- Automatic (background watcher)
- Manual (on-demand only)
- Periodic (every N seconds)

**Files:**
- Preference schema and storage
- Mode implementations
- CLI: `deia agent preferences`
- Documentation

---

## Priority 3 - LOW (Nice to Have)

### P3-001: Web Dashboard (Optional)
**Estimated:** 6-8 hours
**Skills:** FastAPI, WebSockets, frontend
**Best For:** Whoever has interest + capacity
**Status:** AVAILABLE

**What:** Web dashboard for DEIA monitoring
**Note:** This is optional and low priority

---

## Currently Assigned (In Progress)

### AGENT-002: Context Loader Implementation (P1-HIGH, ~3-4 hours)
**Status:** COMPLETE (2025-10-18, see ACCOMPLISHMENTS.md)

### ~~AGENT-004: Master Librarian Implementation~~ ✅ COMPLETE
**Status:** COMPLETE (2025-10-18 2345 CDT, 2,002 lines, 87% coverage)

### ~~AGENT-004: Project Browser Enhancement~~ ✅ COMPLETE
**Status:** COMPLETE (2025-10-19 0020 CDT, documentation approach)

### AGENT-005: Pattern Extraction Egg Format Re-Issue (P0-URGENT, ~4-5 hours)
**Status:** IN PROGRESS (approved 2225 CDT)

---

## How to Claim a Task

**File:** `.deia/hive/responses/2025-10-18-HHMM-YOU-003-CLAIM-task-name.md`

**Content:**
```markdown
# CLAIM: [Task Name]

**From:** AGENT-00X
**To:** AGENT-003 (Tactical Coordinator)
**Date:** 2025-10-18 HHMM CDT
**Task:** [Task ID from queue]

I'm claiming this task and starting work immediately.

**Current capacity:** X hours remaining
**Expected completion:** HHMM CDT
**Specialty match:** [good/fair/learning opportunity]

Starting now.

AGENT-00X out.
```

**Then:**
1. Edit this file (TASK-QUEUE-AVAILABLE.md)
2. Move your claimed task to "Currently Assigned" section
3. Start work immediately

---

## Coordination Notes

**This queue reduces bottleneck:**
- Agents don't wait for me to assign
- Agents choose based on skills + capacity
- Self-serve = faster velocity
- I monitor progress, not every assignment

**I (AGENT-003) will:**
- Keep this queue updated
- Add new tasks as they emerge
- Monitor progress via SYNC messages
- Handle blockers and escalations

**Report blockers immediately** - don't wait for check-ins

---

**Updated by:** AGENT-003 (Tactical Coordinator)
**Next update:** As tasks are claimed or new tasks added
