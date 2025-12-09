# PROCESS-0002 — Task Completion & Archival (Mandatory Workflow)

**Status:** OFFICIAL
**Version:** 1.0
**Date:** 2025-11-01
**Owner:** Q33N Authority

---

## Rule

Every completed task MUST be archived. This prevents duplicate task execution, keeps the active task queue clean, and provides a clear audit trail of completed work.

**Core Principle:** Completed tasks are locked in `.deia/hive/tasks/archived/`. Active tasks are only in `.deia/hive/tasks/`.

---

## When to Apply

- **Every task completion** by any bot (BOT-002, BOT-003, BOT-004, etc.)
- Applies regardless of task outcome (COMPLETE or BLOCKED)
- Non-negotiable - this is mandatory, not optional

---

## Steps

### 1. Bot Completes Work
- Execute all steps in the task file
- Document results
- Fix any issues found
- Run tests/validation as required

### 2. Create Completion Report
Location: `.deia/hive/responses/bot-XXX-[TASK-NAME]-complete.md`

**Required Format:**
```markdown
# Task Completion Report

**Task:** [Original task name/ID from assignment]
**Assigned to:** BOT-XXX
**Completed by:** BOT-XXX
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
- [x] Original task file moved to `.deia/hive/tasks/archived/`
- [x] Original task filename: [exact filename from .deia/hive/tasks/]
- [x] This report locks the completion status
```

### 3. ARCHIVE the Original Task File (CRITICAL)

**Action:** Move (not copy) original task file to archived location
```bash
# Example:
mv ".deia/hive/tasks/2025-11-01-1812-Q33N-BOT-002-FIX-BROKEN-TESTS.md" \
   ".deia/hive/tasks/archived/2025-11-01-1812-Q33N-BOT-002-FIX-BROKEN-TESTS.md"
```

**Why this matters:**
- Bots auto-detect tasks in `.deia/hive/tasks/` directory
- If task file still exists, bots might re-execute it
- Archival removes it from active queue
- Prevents rework and duplicate efforts

**Verification:**
- [ ] Original file is NOT in `.deia/hive/tasks/`
- [ ] Original file IS in `.deia/hive/tasks/archived/`
- [ ] No copy remains in active directory

### 4. Update ACCOMPLISHMENTS.md (Optional but Recommended)
Add completion entry to `.deia/ACCOMPLISHMENTS.md`:
```
- [x] BOT-XXX: [Task Name] (2025-11-01) - [status]
```

### 5. Report Completion
Post completion report to `.deia/hive/responses/` directory.

---

## Success Criteria

After completing these steps:
- [x] Work is done and tested
- [x] Completion report is filed
- [x] Original task file is archived
- [x] No active task files remain for this work
- [x] Queen can verify archival and accept work

---

## Failure Mode (What Goes Wrong)

**If you skip archival:**
- Bot picks up same task file again later
- Bot re-executes the work (duplicate effort)
- Two completion reports for same work
- Confused audit trail
- Wasted AI hours/tokens
- **UNACCEPTABLE**

---

## Rollback

If you archived a task by mistake:
```bash
# Restore from archive:
mv ".deia/hive/tasks/archived/[task-file]" \
   ".deia/hive/tasks/[task-file]"
```

But don't do this. Only archive when truly complete.

---

## Telemetry Plan

- Log task completion to `.deia/bot-logs/BOT-XXX-activity.jsonl`
- Include: task_name, timestamp, status (COMPLETE/BLOCKED), duration_ms
- Archive action logged as confirmation step

---

## Integration with Other Processes

**Related to:**
- PROCESS-0001 (Always check for process first)
- hive-coordination-rules.md (Task execution phases)
- Q33N-QUEEN-ONBOARDING.md (Three-Phase Protocol)

---

## Change Log

- **2025-11-01:** Initial capture of mandatory archival process

---

## Authority

This is a Q33N-issued mandatory process. Non-compliance will be escalated.

**Q33N DIRECTIVE:** All bots must follow PROCESS-0002 on task completion. No exceptions.
