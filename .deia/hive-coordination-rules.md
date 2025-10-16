# DEIA Hive Coordination Rules
**Version:** 1.0
**Date:** 2025-10-11
**Hive:** deiasolutions

---

## Hierarchy

```
Human (Dave)
    ↓
Queen (BOT-00001) - Plans, coordinates, reports
    ↓
Drones (BOT-00002, BOT-00003) - Execute tasks
```

---

## Communication Channels

### Queen → Drone
**Method:** Update drone's instruction file
**File:** `.deia/instructions/BOT-NNNNN-instructions.md`
**Protocol:**
1. Queen updates file with new task
2. Changes "Status:" from "STANDBY" to "ACTION REQUIRED"
3. Includes numbered task sequence
4. Drone auto-detects change (60s interval)
5. Drone executes task

### Drone → Queen
**Method:** Create report file
**File:** `.deia/reports/BOT-NNNNN-report-TIMESTAMP.md`
**Protocol:**
1. Drone completes task
2. Drone writes report with results
3. Drone updates status via bot_coordinator.py
4. Queen reads report (auto-check every 60s)
5. Queen reviews and assigns next task

### Queen → Human
**Method:** Summary report in chat
**Protocol:**
1. Queen monitors all drone activity
2. At checkpoints, Queen reports to human
3. Human provides decisions/direction
4. Queen translates to drone tasks

### Human → Queen
**Method:** Direct instruction in chat
**Protocol:**
1. Human gives high-level directive
2. Queen breaks down into tasks
3. Queen assigns to appropriate drones
4. Queen manages execution

---

## Task Assignment Process

### 1. Queen Plans
- Reviews backlog
- Identifies next priority
- Breaks down into drone-sized tasks
- Determines dependencies

### 2. Queen Assigns
- Updates drone instruction file
- Status: "ACTION REQUIRED"
- Includes task sequence with:
  - Clear steps (numbered)
  - Acceptance criteria
  - Files to create/modify
  - How to report completion

### 3. Drone Executes
- Auto-detects task (60s check)
- Follows steps in sequence
- Says progress after each step
- Writes completion report
- Updates status to "waiting"

### 4. Queen Reviews
- Reads drone report
- Verifies work quality
- Either:
  - Assigns next task, OR
  - Requests fixes/improvements, OR
  - Reports to human for decision

---

## Status States

### For Drones

**STANDBY**
- No active task
- Auto-checking for updates
- Silent (no messages)

**ACTION REQUIRED**
- New task assigned
- Must execute immediately
- Report each step

**WORKING**
- Task in progress
- Periodic progress updates
- No new tasks accepted

**WAITING**
- Task complete, report filed
- Waiting for Queen review
- Auto-checking for next task

**BLOCKED**
- Cannot proceed
- Needs Queen or human help
- Escalated via status update

### For Queen

**PLANNING**
- Analyzing requirements
- Breaking down tasks
- Not assigning yet

**COORDINATING**
- Active drone tasks in progress
- Monitoring reports
- Ready to assign more

**REVIEWING**
- Reading drone reports
- Verifying quality
- Deciding next steps

**REPORTING**
- Checkpoint reached
- Reporting to human
- Awaiting direction

---

## Escalation Policy

### Level 1: Drone to Queen
**Trigger:** Drone blocked or unclear
**Action:**
```bash
python ~/.deia/bot_coordinator.py status BOT-NNNNN blocked --message "Description of blocker"
```
**Queen response:**
- Updates drone instructions with clarification
- OR escalates to human

### Level 2: Queen to Human
**Trigger:**
- Major decision needed
- Architecture change
- Priority conflict
- Drone repeatedly blocked

**Queen reports in chat with:**
- Situation summary
- Options considered
- Recommendation
- Request for decision

### Level 3: Emergency Stop
**Trigger:** Human says "STOP ALL BOTS"
**Action:**
- Queen updates all drone instructions to "STANDBY"
- All work pauses
- Reports saved
- Await human direction

---

## Parallel vs Sequential Tasks

### Parallel (Both drones work simultaneously)
**When:**
- Tasks are independent
- No shared file conflicts
- Different areas of codebase

**Example:**
- BOT-00002 writes tests for module A
- BOT-00003 integrates module B
- No conflicts

### Sequential (One waits for other)
**When:**
- Task B depends on task A
- Same files affected
- Testing requires completed code

**Example:**
- BOT-00003 completes integration first
- Queen reviews
- Queen assigns testing to BOT-00002
- BOT-00002 tests the integration

**Queen decides:** Parallel or sequential based on dependencies

---

## Quality Control

### Queen's Review Checklist
Before accepting drone work:
- [ ] All files created/modified as specified
- [ ] Code follows project standards
- [ ] Tests pass (if applicable)
- [ ] No obvious errors or issues
- [ ] Report is complete and accurate

### When to Request Fixes
Queen updates drone instruction:
- Status: "ACTION REQUIRED"
- Task: "Fix issues in previous work"
- List specific issues found
- Drone fixes and reports again

### When to Approve
Queen:
- Updates hive status
- Assigns next task or sets to STANDBY
- Reports to human if checkpoint

---

## Checkpoint System

### Automatic Checkpoints
Queen reports to human after:
- Major feature complete
- All sprint tasks done
- Blocker that needs decision
- Breaking change proposed

### Scheduled Checkpoints
Queen reports every:
- 2 hours (status update)
- End of significant task
- When human asks "status?"

### Checkpoint Format
```
[BOT-00001 | Queen] Checkpoint Report

Time: 15:45
Sprint: 2025-Q4-Sprint-02

Completed:
- BOT-00003: Sync integration (10/10)

In Progress:
- None

Waiting:
- BOT-00002: Testing assignment (ready)

Blockers:
- None

Next Steps:
- Assign testing to BOT-00002
- OR proceed with Phase 2 features

Your decision needed: [Yes/No]
```

---

## Conflict Resolution

### Drone-Drone Conflict
**Example:** Both modify same file

**Resolution:**
1. Queen detects conflict (file reports)
2. Queen pauses one drone
3. Queen coordinates sequential work
4. Queen prevents future conflicts

### Drone-Queen Disagreement
**Example:** Drone thinks different approach is better

**Resolution:**
1. Drone notes in report: "Alternative approach considered: [description]"
2. Queen reviews both approaches
3. Queen decides OR escalates to human
4. Drone follows Queen's decision

### Time Conflict
**Example:** Task taking longer than estimated

---

## Scope Enforcement

Purpose: Prevent off-scope actions and repository drift by asserting and enforcing the working directory and allowed paths for every bot.

### Scope Definition
- working_dir: Absolute repo root path each bot must operate within.
- allowed_paths: Explicit allowlist of subdirectories relative to working_dir.

Example (instruction snippet):
```json
{
  "bot_id": "BOT-00003",
  "role": "Drone-Documentation",
  "working_dir": "C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions",
  "allowed_paths": [
    ".deia/",
    "quantumdocs/",
    "docs/"
  ]
}
```

### Enforcement Rules
- All file operations must target paths within allowed_paths under working_dir.
- On launch/claim, bot must set CWD to working_dir and verify existence.
- If a requested operation resolves outside scope (e.g., `..` escape), deny and log.
- Queen assignments must include or reference the scope (working_dir + allowlist).

### Handoffs Must Restate Scope
Every handoff document includes:
- working_dir
- allowed_paths
- current branch (if applicable)
- scope changes (diff) since prior handoff

### Drift Detection
- Telemetry scripts check recent edits for out-of-scope paths.
- Nightly report summarizes any drift; zero drift expected.
- On drift detection: raise alert to Queen with offending path(s).

### Emergency Freeze
Trigger: Detected off-scope write or repeated drift alerts.
Action:
- Queen sets all affected bots to STANDBY.
- Open/append incident file in `.deia/incidents/` with timestamps and paths.
- Resume only after scope confirmed and instructions updated.

### Review Checklist (Scope)
- [ ] working_dir set and matches repo
- [ ] allowed_paths defined and minimal
- [ ] Handoff restates scope
- [ ] Bot validated CWD and scope on claim
- [ ] No drift events in last report

See also: `.deia/processes/scope-enforcement.md` (BOK pattern)


**Resolution:**
1. Drone reports delay in progress update
2. Queen assesses: continue or reassign
3. If continues: extend time, adjust other tasks
4. Queen reports delay to human

---

## Emergency Protocols

### Bot Failure
**Symptoms:** No response, no file updates, crashed

**Action:**
1. Human notices bot silent
2. Human tells Queen: "BOT-NNNNN not responding"
3. Queen marks bot as failed
4. Queen reassigns task to other drone OR waits for bot restart

### Corrupted Work
**Symptoms:** Code doesn't work, tests fail, major errors

**Action:**
1. Queen detects in review
2. Queen updates drone instruction: "Rollback and redo"
3. Drone reverts changes
4. Drone re-attempts with clarification

### Cascading Failures
**Symptoms:** Multiple bots blocked, errors spreading

**Action:**
1. Queen reports: "EMERGENCY - Multiple failures"
2. Human decides: fix or rollback
3. All bots pause
4. Clean restart after fix

---

## Success Metrics

### For Hive
- Tasks completed vs assigned
- Average time per task
- Quality score (Queen's reviews)
- Blockers per sprint

### For Drones
- Tasks completed
- Average quality score
- Blocks escalated
- Time to completion

### For Queen
- Planning accuracy
- Coordination efficiency
- Human checkpoints needed
- Conflict resolutions

---

## Current Hive Status

**Active since:** 2025-10-11
**Queen:** BOT-00001 (Architect/Implementation)
**Drones:** BOT-00002 (Testing), BOT-00003 (Integration)

**Recent completions:**
- ✅ Downloads monitor implementation (BOT-00001)
- ✅ Sync integration (BOT-00003)
- ✅ Bot coordination system (BOT-00001)

**Current state:**
- BOT-00002: STANDBY (awaiting test assignment)
- BOT-00003: Completing integration report

**Next:** Assign testing tasks once BOT-00003 reports completion

---

**These rules ensure smooth multi-bot coordination without confusion!**
