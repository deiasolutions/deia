# TASK ASSIGNMENT: Coordinator MVP Implementation
**From:** Q33N (BEE-000 Queen)
**To:** BOT-004 (CLAUDE-CODE-004)
**Date:** 2025-10-25 22:00 CDT
**Priority:** P1
**Backlog ID:** BACKLOG-027

---

## Mission

Implement the Coordinator MVP daemon: a monitoring system that watches for scope violations and automatically freezes offending bots. Critical for hive governance and security.

---

## What is the Coordinator?

The Coordinator is a lightweight daemon that:
1. Reads path events from `.deia/telemetry/path-events.jsonl`
2. Detects when bots access paths outside their scope
3. Automatically freezes violating bots and logs alerts

**Why Critical:** P0 incident (escaped bot) proved we need automated scope enforcement, not just human detection.

---

## Task Details

**Dependency:** BACKLOG-026 (Monitor?Action Coordinator Spec) - Should be available. If not, use best judgment based on P0 incident context.

**What to Build:**

### 1. Scope Monitoring Daemon
- Monitors `.deia/telemetry/path-events.jsonl` continuously
- Parses each event: `{timestamp, bot_id, path, within_scope, action}`
- Triggers on `within_scope=false` events

### 2. Automatic Freeze Action
- On scope violation: set bot status to `STANDBY` in status board
- Write alert to hive log: `.deia/hive/logs/scope-violations.log`
- Notify Queen (update status board with alert)
- Log incident for review

### 3. Implementation Details
- Daemon script: `src/deia/services/coordinator.py`
- Run as background service (can be started with `python coordinator.py`)
- Poll path-events every 5 seconds
- Graceful shutdown on SIGTERM

### 4. Testing
- Manual test: Create fake path events and verify freeze triggers
- Nightly test: Clean run should show zero violations
- Test script: Simulate bot accessing out-of-scope path, verify automatic freeze

---

## Acceptance Criteria

- [ ] Daemon reads path-events.jsonl correctly
- [ ] On scope violation: bot frozen (status = STANDBY)
- [ ] Alert written to hive log with details
- [ ] Queen status board updated with alert
- [ ] Test script reproduces freeze behavior
- [ ] Nightly summary shows clean/violation count
- [ ] No crashes or infinite loops in daemon
- [ ] Graceful shutdown handling

---

## Key Files

**Read these to understand context:**
- `.deia/incidents/P0-ESCAPED-BOT-POSTMORTEM.md` - Why this is critical
- `.deia/telemetry/PATH-CAPTURE-SPEC.md` - Path event format (if exists)
- `.deia/bot-status-board.json` - Status board structure

**Create/Modify:**
- `src/deia/services/coordinator.py` - Main daemon
- `src/deia/services/coordinator_test.py` - Tests
- `.deia/hive/logs/scope-violations.log` - Log file

---

## Deliverable

Create file: `.deia/hive/responses/deiasolutions/bot-004-coordinator-mvp-complete.md`

Include:
- [ ] Daemon implemented and tested
- [ ] Manual test results (scope violation detected and frozen)
- [ ] Nightly test results (zero violations on clean run)
- [ ] Code quality assessment
- [ ] Any architectural decisions made
- [ ] Integration points confirmed

**Estimated Time:** 300 minutes (5 hours)

---

## If Blocked

Post questions to: `.deia/hive/responses/deiasolutions/bot-004-questions.md`

Q33N will respond within 30 minutes.

---

**Q33N out. BOT-004: Coordinator MVP - build scope enforcement daemon. Go.**
