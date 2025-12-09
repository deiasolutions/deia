# IMMEDIATE ASSIGNMENT: BOT-001 - Sprint 2 Queue Ready
**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-001 (Bot Infrastructure)
**Date:** 2025-10-25 20:40 CDT
**Priority:** P0 - QUEUE READY NOW
**Status:** STANDING BY - NO IDLE TIME

---

## Fire Drill Status

When you complete fire drill tasks, Sprint 2 tasks are already queued and waiting.

**Don't wait for assignment. Queue is ready. Pick it up.**

---

## Your Sprint 2 Queue (6 tasks, ready now)

### Task 1: Error Handling & Recovery (2 hours)
- Add try-catch around bot subprocess lifecycle
- Detect bot crashes (check PID alive every 30s)
- Auto-restart crashed bots (exponential backoff)
- Log all errors to `.deia/bot-logs/BOT-{id}-errors.jsonl`
- Report crashes immediately

**Success:** Bot restarts on crash, detailed error logs

### Task 2: Comprehensive Bot Logging (2 hours)
- Add structured JSON logging to bot subprocess
- Log all bot events: startup, shutdown, task, complete, errors
- Include timestamps, bot ID, operation, result
- Append to `.deia/bot-logs/BOT-{id}-activity.jsonl`
- Log rotation (keep last 100MB)

**Success:** Every action logged, queryable format

### Task 3: Registry Persistence & Recovery (1.5 hours)
- Persist registry to disk (JSON backup every 10s)
- Clean stale entries on startup (check PID alive)
- Handle bot ID collisions (prevent double-launch)
- Add registry versioning
- Audit trail in `.deia/bot-logs/registry-changes.jsonl`

**Success:** Registry survives restart, no stale entries

### Task 4: Resource Monitoring (1.5 hours)
- Track CPU usage per bot
- Track memory usage per bot
- Detect runaway processes (CPU > 80%, memory > 500MB)
- Log metrics every minute
- Alert on anomalies

**Success:** Resource metrics collected, alerts triggered

### Task 5: Graceful Shutdown & Cleanup (1 hour)
- Implement SIGTERM handling
- Bot finishes current task before shutdown
- Write final state to responses
- Unregister from registry cleanly
- Clean up temporary files

**Success:** 10s graceful shutdown, force kill if needed

### Task 6: Multi-Bot Load Management (1.5 hours)
- Port allocation strategy (8001-8999 dynamic)
- Prevent port collisions
- Load balance task queue (don't overload one bot)
- Queue management: prioritize urgent
- Rate limiting: max task send rate

**Success:** 10+ bots launchable, no conflicts, fair load

---

## After Sprint 2

Hardening tasks queue waits:
- Hardening.1: Circuit breaker (1.5h)
- Hardening.2: Metrics collection (2h)
- Hardening.3: Backpressure (1.5h)
- Hardening.4: Health checks (1h)
- Hardening.5: Performance profiling (2h)

---

## Queue Management

Your queue is continuously managed:
1. You finish task → queue has next task ready
2. No idle time
3. No waiting for assignments
4. 3-5 tasks always ahead

---

## Status File

Update continuously:
```
.deia/hive/responses/deiasolutions/bot-001-sprint-2-status.md
```

---

## GO

Fire drill → Sprint 2 (seamless transition).

**When you're done with fire drill, Sprint 2 starts immediately. Queue is ready.**

---

**Q33N out. No idle time. Keep shipping.**
