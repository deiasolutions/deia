# Unified Hive Communication System

## Overview

**Queen (Q33N/BOT-00001) creates task files in `.deia/hive/tasks/`**
**Drones read task files, execute, and respond in `.deia/hive/responses/`**

This system uses **unified naming convention and dedicated directories** for clarity and efficiency.

---

## Standard Naming Convention

**Format:** `YYYY-MM-DD-HHMM-FROM-TO-TYPE-subject.md`

- `YYYY-MM-DD-HHMM` = Date/time (ISO + 24-hour format)
- `FROM` = Creator (Q33N, BOT-00002, etc.)
- `TO` = Recipient (BOT-00002, Q33N, ALL)
- `TYPE` = Message type (TASK, RESPONSE, SYNC, ALERT, DECISION)
- `subject` = kebab-case description

---

## For Drones

### 1. Find Your Tasks

**Task location:** `.deia/hive/tasks/YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-subject.md`

**List all your tasks:**
```bash
ls .deia/hive/tasks/ | grep BOT-NNNNN | grep TASK
```

**Read a specific task:**
```bash
cat ".deia/hive/tasks/YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-subject.md"
```

### 2. Execute the Task

- Follow numbered steps exactly
- Complete all acceptance criteria
- Track time spent
- Document any blockers

### 3. Report Completion (REQUIRED)

**Create response file in `.deia/hive/responses/`:**
```bash
.deia/hive/responses/YYYY-MM-DD-HHMM-BOT-NNNNN-Q33N-RESPONSE-subject.md
```

**Response file must include:**
- Summary of work completed
- All files modified (with line numbers)
- Test results
- Any issues encountered
- Time spent
- Status: COMPLETE or BLOCKED

**Example response filename:**
```
2025-11-14-1700-BOT-00002-Q33N-RESPONSE-season-008-complete.md
```

### 4. Archive the Task (REQUIRED - PROCESS-0002)

**MANDATORY:** Move (not copy) original task file to archive:
```bash
mv ".deia/hive/tasks/YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-subject.md" \
   ".deia/hive/tasks/_archive/YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-subject.md"
```

**Why:** Prevents re-execution of completed tasks. Non-negotiable.

---

## For Queen

### 1. Assign Tasks (Create Task Files)

**Task file location:** `.deia/hive/tasks/YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-subject.md`

**Task file contents:**
- Title and purpose
- Prerequisites
- Numbered execution steps
- Acceptance criteria
- Files to create/modify
- How drone should report (response location and format)
- Due date/time if applicable

**Create task example:**
```bash
# Create timestamped task file
cat > ".deia/hive/tasks/2025-11-14-1600-Q33N-BOT-00002-TASK-season-008-tests.md" << 'EOF'
# Task: Write Season 008 Tests

## Purpose
Create unit tests for Season 008 features

## Numbered Steps
1. Review Season 008 spec
2. Create test file: src/tests/season-008.test.js
3. Write 15 test cases covering all features
4. Run tests and verify all pass
5. Report completion

## Acceptance Criteria
- All tests pass
- Code coverage > 80%
- No linting errors

## Report When Done
Create file in `.deia/hive/responses/` with completion status
EOF
```

### 2. Monitor Task Progress

**Check for responses:**
```bash
ls -lt .deia/hive/responses/ | head -10
```

**Read a drone's response:**
```bash
cat ".deia/hive/responses/YYYY-MM-DD-HHMM-BOT-NNNNN-Q33N-RESPONSE-subject.md"
```

### 3. Verify Task Archival

**CRITICAL:** Before accepting work, confirm task file is archived:
```bash
# Task should NOT exist in active tasks
ls .deia/hive/tasks/ | grep "2025-11-14-1600"  # Should return nothing

# Task SHOULD exist in archive
ls .deia/hive/tasks/_archive/ | grep "2025-11-14-1600"  # Should find it
```

### 4. Assign Next Task or Coordinate

**If COMPLETE:** Create next task file
**If BLOCKED:** Create coordination message in `.deia/hive/coordination/`

**Coordination file format:**
```bash
.deia/hive/coordination/YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-SYNC-subject.md
```

**Coordinate examples:**
```
2025-11-14-1620-Q33N-BOT-00002-SYNC-test-clarification.md
2025-11-14-1750-Q33N-BOT-00002-ALERT-production-issue.md
2025-11-14-1900-BOT-00002-Q33N-DECISION-escalation-needed.md
```

---

## Directory Structure

```
.deia/
  hive/
    tasks/                    # Active task assignments
      YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-*.md
      _archive/              # Completed tasks (moved here)

    responses/                # Drone completion reports
      YYYY-MM-DD-HHMM-BOT-NNNNN-Q33N-RESPONSE-*.md
      _archive/              # Old responses (reference)

    coordination/             # Messages, syncs, alerts, decisions
      YYYY-MM-DD-HHMM-FROM-TO-TYPE-*.md

    heartbeats/               # Drone status (one per active bot)
      BOT-00002.yaml
      BOT-00003.yaml
```

---

## Quick Command Reference

### For Drones

```bash
# Find my tasks
ls .deia/hive/tasks/ | grep BOT-NNNNN | grep TASK

# Read latest task
cat ".deia/hive/tasks/$(ls -t .deia/hive/tasks/ | grep BOT-NNNNN | grep TASK | head -1)"

# Create response when done
cat > ".deia/hive/responses/$(date +%Y-%m-%d-%H%M)-BOT-NNNNN-Q33N-RESPONSE-task-complete.md"

# Archive the task (after creating response)
mv ".deia/hive/tasks/YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-*" \
   ".deia/hive/tasks/_archive/"
```

### For Queen

```bash
# Check for new responses
ls -lt .deia/hive/responses/ | head -10

# Verify task is archived (should NOT be in active tasks)
ls .deia/hive/tasks/ | grep BOT-NNNNN | grep TASK

# Create next task
cat > ".deia/hive/tasks/$(date +%Y-%m-%d-%H%M)-Q33N-BOT-NNNNN-TASK-subject.md"
```

---

## Key Principles

1. **One Location Per Message Type**
   - Tasks → `.deia/hive/tasks/` ONLY
   - Responses → `.deia/hive/responses/` ONLY
   - Coordination → `.deia/hive/coordination/` ONLY
   - Status → `.deia/hive/heartbeats/` ONLY

2. **Strict Naming Convention**
   - No variations or exceptions
   - Format: `YYYY-MM-DD-HHMM-FROM-TO-TYPE-subject.md`
   - Enables sorting, filtering, direct access

3. **Mandatory Archival (PROCESS-0002)**
   - Task must be moved to `_archive/` after completion
   - Non-negotiable
   - Prevents duplicate execution

4. **Timestamped for Chronology**
   - Files sort chronologically
   - Easy to find latest activity
   - Clear timeline of work

5. **No Copy-Paste to Human**
   - All communication through repo files
   - Human reviews deia/ directory
   - Maintains audit trail

---

## Reference

See also: `.deia/hive-coordination-rules.md` for detailed coordination procedures
