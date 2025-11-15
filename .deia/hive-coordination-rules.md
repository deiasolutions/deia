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

### Unified Communication System (Standard Naming Convention)
**Format:** `YYYY-MM-DD-HHMM-FROM-TO-TYPE-subject.md`

Components:
- `YYYY-MM-DD-HHMM` = Date and time (ISO format + 24-hour time)
- `FROM` = Who created it (Q33N, BOT-00001, BOT-00002, etc.)
- `TO` = Who it's for (BOT-00002, Q33N, ALL, etc.)
- `TYPE` = Message type (TASK, RESPONSE, SYNC, ALERT, DECISION)
- `subject` = kebab-case description

**Location Rules (One Location Per Message Type):**
- **Tasks** → `.deia/hive/tasks/` ONLY
- **Responses** → `.deia/hive/responses/` ONLY
- **Coordination** → `.deia/hive/coordination/` ONLY
- **Status** → `.deia/hive/heartbeats/` ONLY

### Queen → Drone (Task Assignment)
**Method:** Create timestamped task file
**Location:** `.deia/hive/tasks/YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-subject.md`
**Protocol:**
1. Queen creates task file with timestamp
2. File goes in `.deia/hive/tasks/` directory
3. Includes numbered task sequence
4. Drone polls/discovers file
5. Drone executes task

**Example:** `2025-11-14-1600-Q33N-BOT-00002-TASK-season-008-tests.md`

### Drone → Queen (Task Completion)
**Method:** Create timestamped response file
**Location:** `.deia/hive/responses/YYYY-MM-DD-HHMM-BOT-NNNNN-Q33N-RESPONSE-subject.md`
**Protocol:**
1. Drone completes task
2. Creates response file with timestamp in `.deia/hive/responses/`
3. Includes completion status and results
4. Queen polls/reads response
5. Queen reviews and assigns next task

**Example:** `2025-11-14-1700-BOT-00002-Q33N-RESPONSE-season-008-complete.md`

### Queen ↔ Drone (Real-time Coordination)
**Method:** Create coordination messages
**Location:** `.deia/hive/coordination/YYYY-MM-DD-HHMM-FROM-TO-TYPE-subject.md`
**Protocol:**
1. Used for syncs, alerts, decisions between agents
2. Timestamped for chronological ordering
3. FROM/TO clearly identifies sender/recipient
4. TYPE indicates message class (SYNC, ALERT, DECISION, etc.)

**Examples:**
```
2025-11-14-1610-Q33N-BOT-00002-SYNC-task-clarification.md
2025-11-14-1850-Q33N-BOT-00002-ALERT-production-issue.md
2025-11-14-1920-BOT-00002-Q33N-DECISION-escalation-needed.md
```

### Status Tracking
**Method:** Heartbeat files
**Location:** `.deia/hive/heartbeats/BOT-NNNNN.yaml`
**Protocol:**
1. One file per active drone
2. Updated regularly with status, progress, blockers
3. YAML format for structured data
4. Queen reads for health checks

**Example:** `.deia/hive/heartbeats/BOT-00002.yaml`

### Queen → Human
**Method:** Summary report in chat
**Protocol:**
1. Queen monitors all drone activity via hive directories
2. At checkpoints, Queen reports to human
3. Human provides decisions/direction
4. Queen translates to task files or coordination messages

### Human → Queen
**Method:** Direct instruction in chat
**Protocol:**
1. Human gives high-level directive
2. Queen breaks down into tasks
3. Queen creates task files in `.deia/hive/tasks/`
4. Queen manages execution via coordination messages

---

## Task Assignment Process

### 1. Queen Plans
- Reviews backlog
- Identifies next priority
- Breaks down into drone-sized tasks
- Determines dependencies

### 2. Queen Assigns (Creates Task File)
**File location:** `.deia/hive/tasks/YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-subject.md`

**Contents include:**
- Clear numbered steps
- Acceptance criteria
- Files to create/modify
- How to report completion (location and format)

**Example task creation:**
```bash
# Create task file with standard naming
.deia/hive/tasks/2025-11-14-1600-Q33N-BOT-00002-TASK-season-008-tests.md
```

### 3. Drone Executes
- Discovers task file in `.deia/hive/tasks/`
- Follows steps in sequence
- Reports progress during execution
- Completes work per acceptance criteria

### 4. Drone Completes & Archives (REQUIRED - PROCESS-0002)
**MANDATORY - DO NOT SKIP:**

1. **Create completion response file:**
   - Location: `.deia/hive/responses/YYYY-MM-DD-HHMM-BOT-NNNNN-Q33N-RESPONSE-subject.md`
   - Status: `COMPLETE` or `BLOCKED`
   - Document: Summary, files modified, test results, issues, time spent

2. **ARCHIVE the original task file:**
   - Move (not copy) from `.deia/hive/tasks/` → `.deia/hive/tasks/_archive/`
   - Prevents re-execution of completed tasks
   - Keeps active task directory clean
   - Non-negotiable per PROCESS-0002

3. **Example archival:**
   ```bash
   # Original task file is moved to archive
   mv ".deia/hive/tasks/2025-11-14-1600-Q33N-BOT-00002-TASK-season-008-tests.md" \
      ".deia/hive/tasks/_archive/2025-11-14-1600-Q33N-BOT-00002-TASK-season-008-tests.md"
   ```

**Completion Report Format (REQUIRED):**
```markdown
# Task Completion Report

**Task:** YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-subject
**Assigned to:** BOT-NNNNN
**Completed by:** BOT-NNNNN
**Status:** COMPLETE / BLOCKED
**Completion Timestamp:** YYYY-MM-DD HH:MM CDT

## Summary
[Brief summary of what was accomplished]

## Files Modified
[List of all files modified with line numbers]

## Test Results
[Test output showing pass/fail]

## Issues Encountered
[Any blockers or problems solved]

## Time Spent
[X hours Y minutes]

## Archival Confirmation
- [x] Original task file moved to `.deia/hive/tasks/_archive/`
- [x] Original filename: 2025-11-14-1600-Q33N-BOT-00002-TASK-season-008-tests.md
- [x] Response file created in `.deia/hive/responses/`
- [x] Completion status locked in this report
```

### 5. Queen Reviews
- Reads drone response from `.deia/hive/responses/`
- Verifies work quality
- **Confirms task file IS archived** (not still in active `.deia/hive/tasks/`)
- Either:
  - Creates next task file (Assigns next task), OR
  - Creates coordination message requesting fixes (if BLOCKED), OR
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
- [ ] **Original task file has been ARCHIVED** (moved to `.deia/hive/tasks/archived/`)
- [ ] Completion report matches archival filename
- [ ] No duplicate task execution risk

### When to Request Fixes
Queen updates drone instruction:
- Status: "ACTION REQUIRED"
- Task: "Fix issues in previous work"
- List specific issues found
- Drone fixes and reports again
- **Note:** If task file was archived, do NOT re-archive. Update the existing archived file status.

### When to Approve
Queen:
- Verifies task file is archived
- Updates hive status
- Assigns next task or sets to STANDBY
- Reports to human if checkpoint
- **Confirm:** No task files remain in active `.deia/hive/tasks/` for completed work

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
