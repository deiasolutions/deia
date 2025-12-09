# SPRINT 2 TASK: Bot Infrastructure Hardening (BOT-001)
**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-001 (CLAUDE-CODE-001)
**Date:** 2025-10-25 23:00 CDT (Post-Fire Drill)
**Priority:** P1 - HIGH
**Mode:** Sprint Work - Sequential then parallel
**Duration:** 6-8 hours

---

## Mission: Harden Bot Launcher for Production Use

Fire drill got bots working. Now we need production-quality bot infrastructure: stability, error handling, monitoring, logging.

---

## Task 1: Error Handling & Recovery (2 hours)
**Status:** PENDING - START AFTER FIRE DRILL

**Current Issues to Fix:**
- Subprocess crashes aren't caught gracefully
- Bot hanging not detected or recovered
- Missing error messages
- No crash recovery mechanism

**Your Work:**
1. Add try-catch around bot subprocess lifecycle
2. Detect bot crashes (check PID alive every 30s)
3. Auto-restart crashed bots (with exponential backoff)
4. Log all errors to `.deia/bot-logs/BOT-{id}-errors.jsonl`
5. Report crashes to status board immediately

**Success Criteria:**
- Bot restart on crash
- Detailed error logs
- No silent failures
- Health check every 30s

**Files:**
- Enhance: `run_single_bot.py`
- Create: `src/deia/services/bot_health_monitor.py`

---

## Task 2: Comprehensive Bot Logging (2 hours)
**Status:** PENDING - START AFTER FIRE DRILL

**Current Issues:**
- Limited visibility into bot operations
- Hard to debug issues after the fact
- No structured logging

**Your Work:**
1. Add structured JSON logging to bot subprocess
2. Log all bot events: startup, shutdown, task received, task completed, errors
3. Include timestamps, bot ID, operation, result
4. Append to `.deia/bot-logs/BOT-{id}-activity.jsonl`
5. Create log rotation (keep last 100MB of logs)

**Success Criteria:**
- Every bot action logged
- Queryable JSON format
- No PII in logs
- Logs survive bot restart

**Files:**
- Create: `src/deia/services/bot_activity_logger.py`
- Modify: `run_single_bot.py` to use logger

---

## Task 3: Service Registry Persistence & Recovery (1.5 hours)
**Status:** PENDING - START AFTER FIRE DRILL

**Current Issues:**
- Registry lost if service crashes
- Stale bot entries if process dies
- No recovery after system restart

**Your Work:**
1. Persist registry to disk (JSON backup every 10s)
2. On startup, clean stale entries (check if PID alive)
3. Handle bot ID collisions (prevent double-launch)
4. Add registry versioning (track changes)
5. Provide registry audit trail in `.deia/bot-logs/registry-changes.jsonl`

**Success Criteria:**
- Registry survives restart
- No stale entries
- No duplicate bots
- Audit trail available

**Files:**
- Enhance: `src/deia/services/registry.py`
- Add: Registry backup/recovery logic

---

## Task 4: Resource Monitoring (Subprocess Management) (1.5 hours)
**Status:** PENDING - START AFTER FIRE DRILL

**What We Need:**
Monitor bot subprocess resource usage to catch issues:

**Your Work:**
1. Track CPU usage per bot
2. Track memory usage per bot
3. Detect runaway processes (CPU > 80%, memory > 500MB)
4. Log resource metrics every minute
5. Alert if bot becomes unresponsive

**Success Criteria:**
- Resource metrics collected
- Alerts triggered for anomalies
- Data stored in `.deia/bot-logs/BOT-{id}-resources.jsonl`
- Can query "is bot X healthy?"

**Files:**
- Create: `src/deia/services/bot_resource_monitor.py`

---

## Task 5: Graceful Shutdown & Cleanup (1 hour)
**Status:** PENDING - START AFTER FIRE DRILL

**Current Issues:**
- Bots might not shut down cleanly
- Orphaned processes possible
- Incomplete state on shutdown

**Your Work:**
1. Implement graceful shutdown signal (SIGTERM)
2. Bot finishes current task before shutting down
3. Write final state to `.deia/hive/responses/`
4. Unregister from registry cleanly
5. Clean up temporary files

**Success Criteria:**
- 10s timeout for graceful shutdown
- Force kill if needed (SIGKILL)
- No orphaned processes
- Clean state after shutdown

**Files:**
- Enhance: `run_single_bot.py`
- Create: `src/deia/services/bot_shutdown_handler.py`

---

## Task 6: Multi-Bot Load Management (1.5 hours)
**Status:** PENDING - START AFTER FIRE DRILL

**What We Need:**
Handle multiple bots efficiently:

**Your Work:**
1. Implement port allocation strategy (8001-8999 dynamic assignment)
2. Prevent port collisions
3. Load balance task queue (don't overload one bot)
4. Queue management: prioritize urgent tasks
5. Rate limiting: don't send tasks faster than bot can process

**Success Criteria:**
- 10+ bots launchable simultaneously
- No port conflicts
- Tasks queued fairly
- Bot load monitored

**Files:**
- Enhance: `run_single_bot.py`
- Create: `src/deia/services/bot_load_manager.py`

---

## Deliverables (Report When Complete)

Create file: `.deia/hive/responses/deiasolutions/bot-001-sprint-2-status.md`

Include:
- [ ] Error handling & recovery working
- [ ] Comprehensive logging implemented
- [ ] Registry persistence & recovery done
- [ ] Resource monitoring active
- [ ] Graceful shutdown working
- [ ] Multi-bot load management implemented
- [ ] All 6 tasks tested
- [ ] Evidence: logs showing bot stability
- [ ] Any issues or edge cases discovered

**Estimated Total Time:** 6-8 hours (can overlap with BOT-003 work)

---

## Success Criteria for Sprint 2

**Stability:**
- Bot doesn't crash unexpectedly
- Auto-recovery on crash
- Registry survives restart
- No orphaned processes

**Observability:**
- Every action logged
- Metrics collected (CPU, memory)
- Audit trail available
- Easy to debug issues

**Scalability:**
- 10+ bots simultaneously
- Fair task distribution
- No resource exhaustion
- Graceful degradation

---

## If You Get Stuck

Post to: `.deia/hive/responses/deiasolutions/bot-001-sprint-2-questions.md`

Q33N responds within 30 minutes.

---

**Q33N out. BOT-001: Sprint 2 = Harden infrastructure. Make it production-ready.**
