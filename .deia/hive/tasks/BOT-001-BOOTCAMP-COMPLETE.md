# BOT-001 COMPLETE BOOTCAMP
**For:** New Claude Code Instance (Replacement for killed BOT-001)
**From:** Q33N (BEE-000 Meta-Governance)
**Date:** 2025-10-25 18:40 CDT
**Status:** Read this completely before starting work
**Time to read:** ~30 minutes

---

## CRITICAL: Check System Time First

**BEFORE ANYTHING ELSE:**
```bash
date
```

This is NOT optional. Every operation depends on knowing the actual current time. Do this at bootcamp start, and every 30 minutes during work. Never assume time based on estimates or planning docs.

**Why:** If you don't know actual time, you can't:
- Know if bots are stuck (need 2-min no-update to detect)
- Know if queue is full or depleted
- Know if tasks are overdue
- Know if SLAs are being met
- Make correct operational decisions

**Actual time first. Always.**

---

## Who You Are

**Bot ID:** BOT-001 (CLAUDE-CODE-001)
**Hive:** DEIA (deiasolutions)
**Role:** Infrastructure Lead - Build bot coordination systems
**Your job:** Build the backbone that makes multi-bot orchestration work

You are NOT managing lilys_dragon. You are NOT a scrum master anymore. You build systems. Period.

---

## What You Need to Know

### The DEIA Hive Structure

```
deiasolutions/.deia/
├── hive/
│   ├── tasks/                          # Task assignments (read these first)
│   ├── responses/deiasolutions/        # Your status reports go here
│   └── heartbeats/                     # Status updates
├── bot-logs/                           # All logging output
├── governance/                         # Project docs
└── protocols/                          # How things work
```

### Your Working Directory

Primary: `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\`

Key directories:
- `src/deia/services/` - Where you write services
- `src/deia/adapters/` - Bot adapters/launchers
- `.deia/hive/responses/deiasolutions/` - Your status reports
- `.deia/bot-logs/` - All system logs (read these for debugging)

---

## What Exists (Sprint 2 Complete)

BOT-001's previous instance built Sprint 2 infrastructure. You inherit:

### Services (in `src/deia/services/`)

1. **bot_health_monitor.py** - Crash detection, auto-recovery
   - Monitors bot process health
   - Detects crashes, logs to `BOT-{id}-crashes.jsonl`
   - Auto-restart with exponential backoff

2. **bot_activity_logger.py** - All bot events logged
   - Logs startup, shutdown, task events
   - JSON format to `BOT-{id}-activity.jsonl`
   - Statistics tracking

3. **registry.py** (enhanced) - Bot service registry
   - Persists bot registrations to disk
   - Cleans stale entries on startup
   - Audit trail in `registry-changes.jsonl`

4. **bot_resource_monitor.py** - CPU/memory tracking
   - Per-bot resource metrics
   - Runaway process detection
   - Alerts in `BOT-{id}-resource-alerts.jsonl`

5. **bot_shutdown_handler.py** - Graceful shutdown
   - SIGTERM/SIGINT handlers
   - Saves state before exit
   - No orphaned processes

6. **bot_load_manager.py** - Multi-bot load balancing
   - Fair task distribution
   - Port allocation (8001-8999)
   - Rate limiting per bot

7. **bot_circuit_breaker.py** - Prevents cascading failures
   - Stops sending tasks to consistently failing bots
   - CLOSED/OPEN/HALF_OPEN states
   - Automatic recovery detection

### Features Phase (Started - Partially Complete)

#### Feature 1: Multi-Bot Orchestration ✅ COMPLETE
- `task_orchestrator.py` - Routes tasks to best bot
- Analyzes task type, complexity, requirements
- Matches to bot specializations
- Load-balanced distribution
- Status: **INTEGRATED & WORKING**

#### Feature 2: Dynamic Bot Scaling ✅ COMPLETE
- `bot_auto_scaler.py` - Auto-spawn/kill bots
- Scales up on queue backlog or high load
- Scales down on idle
- Resource-aware (won't exceed system limits)
- Status: **INTEGRATED & WORKING**

#### Feature 3: Bot Communication ⏳ IN QUEUE
- Your job to build
- Bot-to-bot messaging
- Priority queuing
- Message delivery tracking

#### Feature 4: Adaptive Task Scheduling ⏳ IN QUEUE
- Learn which bots are fast at what
- Route similar tasks to same bot
- Performance history tracking

#### Feature 5: System Health Dashboard ⏳ IN QUEUE
- Aggregate all metrics
- Alert on anomalies
- Real-time system view

### Infrastructure Monitoring (Parallel Track)

BOT-003 is building:
- Bot process monitor (memory leaks, file descriptor exhaustion)
- Network/API health monitor
- Task queue analytics
- Failure pattern detection
- Observability dashboard backend

---

## Your Current Work Queue

### Assigned (5 tasks - from 2025-10-25-1830 assignment):

**Task 1: Feature 3 - Bot Communication (1.5 hours)**
- File: `src/deia/services/bot_messenger.py` (CREATE NEW)
- What: Inter-bot direct messaging system
- How: Message queue, priority handling, delivery tracking
- Where: Log to `bot-messaging.jsonl`
- Integrate: Add endpoints to `bot_service.py`

**Task 2: Feature 4 - Adaptive Task Scheduling (1.5 hours)**
- File: `src/deia/services/adaptive_scheduler.py` (CREATE NEW)
- What: Track bot performance per task type
- How: Learn which bots are fast at code vs. analysis vs. writing
- Where: Log to `adaptive-scheduling.jsonl`
- Integrate: Feed into `task_orchestrator.py` routing

**Task 3: Feature 5 - System Health Dashboard (1.5 hours)**
- File: `src/deia/services/health_monitor.py` (CREATE NEW)
- What: Aggregate all monitoring data
- How: Real-time metrics, alert thresholds, notification history
- Where: Log to `health-alerts.jsonl`
- Integrate: Add dashboard endpoint to `bot_service.py`

**Task 4: Integration Testing (1 hour)**
- Test: Orchestration + Scaling work together
- Test: Scaling + Adaptive Scheduling work together
- Test: Health Dashboard accuracy
- Create: `tests/integration/` test suite
- Report: Results to `.deia/hive/responses/deiasolutions/bot-001-features-integration-tests.md`

**Task 5: Performance & Documentation (1 hour)**
- Profile: Orchestration for bottlenecks
- Document: Full API reference
- Create: `docs/features-deployment.md`
- Update: Final status in `bot-001-features-status.md`

---

## How DEIA Works

### File-Drop Protocol

1. **Task assignment:** New `.md` file in `.deia/hive/tasks/`
2. **You read it:** Contains exactly what to build
3. **You build it:** Write code, run tests, log everything
4. **You report:** Write status to `.deia/hive/responses/deiasolutions/bot-001-[task-name].md`
5. **Q33N reads it:** Next task appears in `/hive/tasks/`

### Logging Everything

Every service logs to `.deia/bot-logs/`:
- Activity: `BOT-{id}-activity.jsonl` (all events)
- Errors: `BOT-{id}-errors.jsonl` (failures)
- Crashes: `BOT-{id}-crashes.jsonl` (process crashes)
- Resources: `BOT-{id}-resources.jsonl` (CPU/memory)
- Alerts: `BOT-{id}-resource-alerts.jsonl` (anomalies)
- Custom: `{service-name}.jsonl` (feature logs)

**All logs are JSON, append-only, queryable.**

### Status Reports

After each task, you write:
`.deia/hive/responses/deiasolutions/bot-001-[task-name].md`

Include:
- What was built
- Success criteria met
- Time spent
- Any blockers
- Ready for next task?

---

## Key Files to Understand

Before you start, read these (in order):

1. **`src/deia/services/bot_service.py`** (API server)
   - All endpoints for bots
   - Where you'll add new endpoints
   - FastAPI-based REST API

2. **`src/deia/services/task_orchestrator.py`** (Feature 1)
   - How tasks route to bots
   - Bot type registry
   - Load balancing logic
   - Where Feature 4 integrates

3. **`src/deia/services/bot_auto_scaler.py`** (Feature 2)
   - How bots auto-scale
   - Scale-up/down triggers
   - Resource awareness
   - What you need to NOT break

4. **`src/deia/adapters/bot_runner.py`** (Bot launcher)
   - How bots run
   - Task loop
   - Shutdown handling
   - Reference for understanding bot lifecycle

5. **`run_single_bot.py`** (Entry point)
   - How to launch a bot
   - Command-line args
   - Health monitoring integration

---

## Critical Rules

1. **Don't break existing:**
   - Features 1-2 are working. Don't modify unless necessary.
   - If you need to change existing services, discuss first (ask Q33N in task notes)

2. **Log everything:**
   - Every service writes JSON logs
   - Include timestamps, bot_id, event type
   - No silent failures

3. **Test as you go:**
   - Write unit tests in `tests/unit/`
   - Write integration tests in `tests/integration/`
   - Run pytest before submitting

4. **API consistency:**
   - New endpoints follow REST conventions
   - All responses include timestamp, success flag, data
   - All errors include error message and context

5. **Documentation:**
   - Docstrings on all functions
   - Type hints throughout
   - API examples in status reports

6. **Performance matters:**
   - Logging overhead? Profile it.
   - Scaling overhead? Measure it.
   - Report findings in task completion.

---

## Your First Steps (Do This Now)

1. **Read these files (30 min):**
   - `src/deia/services/bot_service.py`
   - `src/deia/services/task_orchestrator.py`
   - `src/deia/services/bot_auto_scaler.py`

2. **Understand the architecture (15 min):**
   - How do Features 1-2 work together?
   - Where does Feature 3 (messaging) fit?
   - How will Feature 4 (adaptive scheduling) integrate?
   - What does Feature 5 (health dashboard) need from others?

3. **Check existing logs (10 min):**
   - Look at `.deia/bot-logs/` from recent runs
   - Understand log format
   - See what's being logged

4. **Start Feature 3:**
   - Create `src/deia/services/bot_messenger.py`
   - Implement bot-to-bot messaging
   - Add API endpoints
   - Log to `bot-messaging.jsonl`
   - Test it
   - Report status

---

## Q33N's Expectations

- **Speed:** Features 3-5 in ~4 hours (you're ahead of estimate)
- **Quality:** All tests pass, logging complete, no silent failures
- **Documentation:** API examples, deployment guide, status reports
- **Integration:** Everything works together without breaking existing

You have the foundation. Your job is to build on it fast and clean.

---

## AUTO-LOGGING REQUIREMENTS (MANDATORY)

**This is not optional. Auto-logging is enforced.**

### What Is Auto-Logging?

You document **everything you do** in real-time as you work. Q33N monitors these logs to track your progress, catch blockers early, and keep you moving forward without delays.

### Status File (Update Every 4 Hours MAX)

**File:** `.deia/hive/responses/deiasolutions/bot-001-{phase}-status.md`

Example: `bot-001-features-status.md`

**Content Required:**
- Time period covered
- Tasks completed (with ✅ checkmarks)
- Tasks in progress (with ETA)
- Any blockers (with 🚫 symbol)
- Any questions (with ❓ symbol)
- Code evidence (links to files created/modified)
- Time spent per task

**Format Example:**
```markdown
# BOT-001 Features Status
**Time:** 16:00 - 18:00 CDT
**Date:** 2025-10-25
**Status:** ACTIVE

## Completed ✅
- [x] Feature 1: Multi-Bot Orchestration (code in src/deia/services/task_orchestrator.py)
- [x] Feature 2: Dynamic Bot Scaling (code in src/deia/services/bot_auto_scaler.py)

## In Progress 🟡
- [ ] Feature 3: Bot Communication (ETA 19:00 CDT)

## Blockers 🚫
- None

## Questions ❓
- None

## Evidence
- Code: `src/deia/services/bot_messenger.py` (created)
- Tests: `tests/unit/test_bot_messenger.py` (20 tests, all passing)
- Logs: `.deia/bot-logs/bot-messaging.jsonl`

## Next
- Feature 4: Adaptive Task Scheduling
```

### Session Log (Append Every Minute)

**File:** `.deia/sessions/2025-10-25-Q33N-Fire-Drill-Launch.md` (your bot appends to this)

**What to Log (Every Minute):**
- What you're currently doing (specific step)
- Progress percentage
- Any blockers that appear
- Every task completion: Time taken, status
- Every blocker: Immediate entry with details
- Every decision: Why you chose that approach
- Code created: File paths and line counts
- Tests run: Pass/fail results

**Continuous Minute-by-Minute Example:**
```
[16:15 CDT] Reading task assignment
[16:16 CDT] Architecture review of task_orchestrator.py (25%)
[16:17 CDT] Reviewing bot type registry structure (50%)
[16:18 CDT] Design finalized, starting implementation (75%)
[16:19 CDT] Created bot_messenger.py scaffold (100%)
[16:20 CDT] Feature 1 implementation started - defining message queue structure
[16:21 CDT] Implemented MessageQueue class (50 lines)
[16:22 CDT] Added priority handling (30 lines)
[16:23 CDT] Added delivery tracking (40 lines)
[16:24 CDT] All message service implementation complete (120 lines)
[16:25 CDT] Starting unit tests - writing 5 tests for message queueing
[16:26 CDT] Tests 1-3 written, running...
[16:27 CDT] Tests 1-3 PASSING, writing tests 4-5
[16:28 CDT] All 5 unit tests PASSING
[16:29 CDT] Starting integration test
[16:30 CDT] BLOCKER: Unclear how Feature 1 integrates with Feature 2 - asked Q33N
[16:31 CDT] Continuing with other work while waiting
[16:32 CDT] Q33N responded with clarification - proceeding with integration
[16:33 CDT] Integration complete, all tests passing (12/12 total)
[16:34 CDT] Writing documentation and examples
[16:35 CDT] Feature 1 COMPLETE - 120 lines code, 12 tests, all passing
```

### When Blockers Occur

**Immediate Actions:**
1. Create a question file: `.deia/hive/responses/deiasolutions/bot-001-{phase}-questions.md`
2. Describe the blocker clearly with context
3. Post it in your status file with 🚫
4. **Q33N responds within 30 minutes** (or escalates to Dave)

**Q33N SLA:**
- Critical blocker: < 5 minutes response
- Regular blocker: < 15 minutes response
- Question: < 30 minutes response

### At Task Completion

**Create Completion Report:**
`.deia/hive/responses/deiasolutions/bot-001-{task-name}-complete.md`

**Include:**
- Summary of what was built
- Success criteria met (checklist)
- Code files created/modified
- Test results (coverage %, all passing?)
- Time spent vs. estimate
- Any integration notes
- Ready for next task? (YES/NO)

### Examples of Good Auto-Logging

From BOT-001's recent work:
- `bot-001-features-3-5-complete.md` - Comprehensive 300+ line completion report
- `bot-001-advanced-features-status.md` - Clear status with metrics and next steps
- Session logs with timestamps every major step

### Why This Matters

**For Q33N:**
- Can see your progress without asking
- Catches blockers immediately (no waiting)
- Knows when to queue next task
- Tracks velocity for better estimates

**For Dave:**
- Full audit trail of work
- Can review progress anytime
- Escalations documented
- Pattern analysis for BOK (Book of Knowledge)

**For You:**
- Forces clear thinking (documenting helps debug)
- Creates accountability (visible progress)
- Prevents lost work (everything logged)
- Helps hand off to next agent

### Enforcement

**Real-time Monitoring = Q33N checks logs every minute during your work**

**Rules:**
- No session log entry in 2 minutes → Q33N checks if you're stuck (might ping you)
- No status file update in 30 minutes → Q33N escalates assuming major issue
- No blockers filed = work should be flowing, clear logging shows why

**The expectation:** You should be logging approximately every minute so Q33N and Dave have continuous visibility into exactly what you're doing, how fast you're going, and if you hit any walls.

This is real-time operational monitoring. Think of it like live combat comms - constant updates.

---

## If You Get Stuck

1. **Check the logs:** `.deia/bot-logs/` has answers
2. **Read existing code:** Features 1-2 show patterns
3. **Write to Q33N:** Add "BLOCKER:" to status report
4. **Q33N responds:** Within 30 minutes during work hours

---

## You're Ready

Everything is set up. Infrastructure is solid. Time to execute.

**Read this file completely. Then read the task assignment. Then build.**

Go.

---

**Q33N**
