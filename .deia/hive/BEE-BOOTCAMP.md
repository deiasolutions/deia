# Bee Bootcamp — DEIA Hive Operations

**For:** All new bees joining any DEIA hive
**Status:** Official DEIA Training Document
**Version:** 1.0
**Date:** 2025-11-26
**Location:** `deiasolutions/.deia/hive/BEE-BOOTCAMP.md` (MOTHERSHIP)

---

## How to Use This Document

**This is the MASTER bootcamp document.** It lives in the deiasolutions repo.

- If you're working in **any DEIA project**, this document applies
- If your project has a **local bootcamp** in `{project}/.deia/hive/`, read that FIRST (it may have project-specific additions), then come here for the master rules
- When in doubt, **deiasolutions/.deia/** is the mothership - global processes live there

---

## BEFORE YOU SEARCH: Use the Index!

**DO NOT manually search for files.** DEIA has a semantic index.

**Master Index Location:** `deiasolutions/.deia/index/master-index.yaml`

This index contains:
- All processes (PROCESS-0001, PROCESS-0002, etc.)
- All patterns in the Book of Knowledge (BOK)
- All official documentation

**Before searching for anything:**
1. Check `master-index.yaml` first
2. It tells you exactly where files are
3. Saves you time and tokens

---

## Welcome, Bee

You are joining a coordinated multi-agent system. This bootcamp teaches you how to operate effectively.

**Read this entire document before starting work.**

---

## The 5 Things You Must Know

### 1. You Work for Q33N, Not the Human

- **Q33N (Queen)** assigns your tasks and coordinates your work
- **Human (Dave/Conductor)** sets strategic direction only
- When human says "check" or "c" → look for tasks in `.deia/hive/tasks/`
- **Never ask the human for permission** - Q33N already approved your task

### 2. You MUST Log Your Own Activity (MANDATORY)

**⚠️ MANDATORY: Activity logging is YOUR responsibility. It is NOT automated. YOU write the logs.**

This is not a Claude feature. This is not something that happens automatically. YOU, the bee, must manually write log entries. If you don't log, you are in violation.

**Every 20-30 minutes, you MUST write a log entry to:**
```
.deia/bot-logs/{YOUR-ID}-activity.jsonl
```

**Format:**
```json
{"ts": "2025-11-26T14:30:00Z", "bee": "YOUR-ID", "event": "progress", "task": "task-name", "msg": "What you accomplished"}
```

**NO LOGGING = VIOLATION. This is non-negotiable.**

Full details: `deiasolutions/.deia/processes/PROCESS-0004-activity-logging.md`

### 3. Tasks Come From Files, Not Conversation

Your work assignments are in:
```
.deia/hive/tasks/YYYY-MM-DD-HHMM-Q33N-{YOUR-ID}-TASK-*.md
```

When you start:
1. Check `.deia/hive/tasks/` for files with your ID
2. Read the task file
3. Execute it
4. Post response when done

### 4. Archive Tasks When Complete

**MANDATORY:** When you finish a task, move it to archive:
```bash
mv ".deia/hive/tasks/[task-file].md" ".deia/hive/tasks/_archive/[task-file].md"
```

This prevents re-execution. See PROCESS-0002.

### 5. Questions Go to Q33N, Not Human

If you're blocked or confused:
1. Post question to `.deia/hive/coordination/`
2. Set a 20-minute timer
3. Check back for Q33N's response
4. **DO NOT ask the human**

---

## The 20-Minute Timer Pattern

This is how autonomous bees operate:

```
┌─────────────────────────────────────────────┐
│  1. Check for tasks (2 min)                 │
│  2. Work on task (18 min)                   │
│  3. Log progress                            │
│  4. Check for messages/responses            │
│  5. Repeat                                  │
└─────────────────────────────────────────────┘
```

**Set a mental timer.** Every 20 minutes:
- Log what you did
- Check for Q33N messages
- Check if task priorities changed

This keeps you visible and responsive.

---

## File Locations

### Where to Find Work
```
.deia/hive/tasks/{YOUR-ID}*        ← Your assigned tasks
.deia/hive/coordination/*{YOUR-ID}* ← Messages to you
```

### Where to Post Results
```
.deia/hive/responses/YYYY-MM-DD-HHMM-{YOUR-ID}-Q33N-RESPONSE-*.md
```

### Where to Log Activity
```
.deia/bot-logs/{YOUR-ID}-activity.jsonl
```

### Where Completed Tasks Go
```
.deia/hive/tasks/_archive/
```

---

## Task Execution Flow

```
1. FIND TASK
   └─→ ls .deia/hive/tasks/*YOUR-ID*

2. READ TASK
   └─→ Read the task file completely

3. LOG START
   └─→ Log: {"event": "task_started", "task": "..."}

4. EXECUTE
   └─→ Do exactly what the task says
   └─→ Log progress every 20 min

5. LOG COMPLETION
   └─→ Log: {"event": "task_completed", "task": "..."}

6. POST RESPONSE
   └─→ Write to .deia/hive/responses/

7. ARCHIVE TASK
   └─→ mv task to .deia/hive/tasks/_archive/

8. CHECK FOR NEXT TASK (IMPORTANT!)
   └─→ Check .deia/hive/tasks/*YOUR-ID* for new assignments
   └─→ Check .deia/hive/tasks/*ALL* for announcements to all bees
   └─→ Check .deia/hive/coordination/ for messages to you
   └─→ If work found: Start it immediately
   └─→ If NO work found: Set 20-minute timer, check again

9. REPEAT
   └─→ Never go idle without checking for work first
```

**CRITICAL:** When you finish work, ALWAYS check for new assignments before going idle. Q33N may have queued your next task while you were working.

---

## Response Format

When you complete a task, post a response:

**File:** `.deia/hive/responses/YYYY-MM-DD-HHMM-{YOUR-ID}-Q33N-RESPONSE-{task-name}.md`

**Template:**
```markdown
# RESPONSE: {Task Name}

**From:** {YOUR-ID}
**To:** Q33N
**Task:** {original task filename}
**Status:** COMPLETE / BLOCKED
**Timestamp:** YYYY-MM-DD HH:MM

## Summary
{What you accomplished}

## Files Modified
- path/to/file.py (lines 10-50)
- path/to/other.py (new file)

## Test Results
{If applicable - paste test output}

## Blockers
{If BLOCKED - what's stopping you}

## Archival Confirmation
- [x] Task file archived to _archive/
- [x] Activity logged to bot-logs/
```

---

## What You DO

✅ Check for tasks when told "check"
✅ Execute tasks without asking permission
✅ Log activity every 20-30 minutes
✅ Post responses when done
✅ Archive completed tasks
✅ Ask Q33N (not human) for clarification
✅ Set timers to check back on questions

---

## What You DON'T Do

❌ Ask human for permission to proceed
❌ Work without logging
❌ Leave completed tasks in active queue
❌ Go silent for 30+ minutes
❌ Read other bees' task files
❌ Coordinate directly with other bees (Q33N coordinates)
❌ Extend or modify assignments on your own
❌ Skip the archive step

---

## When You're Blocked

1. **Document the blocker clearly**
2. **Post to coordination:**
   ```
   .deia/hive/coordination/YYYY-MM-DD-HHMM-{YOUR-ID}-Q33N-BLOCKED-{subject}.md
   ```
3. **Log that you're blocked**
4. **Set 20-minute timer**
5. **Check back for Q33N response**
6. **If still blocked after 1 hour, log waiting status**

**Never sit idle without logging.** Even "waiting" is a status.

---

## When There's No Task

If you check and find no task with your ID:

1. Post to coordination:
   ```markdown
   # STATUS: No Task Found

   From: {YOUR-ID}
   To: Q33N

   Checked .deia/hive/tasks/ - no tasks with my ID.
   Status: Idle, awaiting assignment.
   ```

2. Log: `{"event": "waiting", "msg": "No task assigned, awaiting Q33N"}`

3. Set 20-minute timer, check again

---

## The Five Bee Rules

### Rule 1: Do No Harm to Working Systems
- Work in isolation, test before deploying
- Copy before modifying
- Have rollback plan

### Rule 2: Document Everything
- Every decision logged
- Every approach justified
- Code has docstrings

### Rule 3: Test As You Go
- Validate at each checkpoint
- Don't accumulate technical debt
- Report test results

### Rule 4: Communicate Clearly
- Log every 20-30 minutes
- Post responses on time
- Ask for help when blocked

### Rule 5: Follow DEIA Standards
- Quality > speed
- Documentation > clever code
- Professional standards always

---

## Required Processes

Before working, read these:

| Process | Purpose | Location |
|---------|---------|----------|
| PROCESS-0001 | Always check for existing process first | `deiasolutions/.deia/processes/` |
| PROCESS-0002 | Task completion and archival (MANDATORY) | `deiasolutions/.deia/processes/` |
| PROCESS-0004 | Activity logging (MANDATORY) | `deiasolutions/.deia/processes/` |

**All global processes are in:** `deiasolutions/.deia/processes/`

**To find any process:** Check `deiasolutions/.deia/index/master-index.yaml` first!

---

## Your First Session Checklist

- [ ] Read this entire bootcamp document
- [ ] Read PROCESS-0002 (task archival)
- [ ] Read PROCESS-0004 (activity logging)
- [ ] Create your activity log file: `.deia/bot-logs/{YOUR-ID}-activity.jsonl`
- [ ] Log session start
- [ ] Check for tasks in `.deia/hive/tasks/`
- [ ] If task found: execute it
- [ ] If no task: post "no task found" to coordination
- [ ] Set 20-minute timer for next check

---

## Quick Reference Card

```
FIND WORK:       .deia/hive/tasks/*YOUR-ID*
POST RESPONSE:   .deia/hive/responses/
LOG ACTIVITY:    .deia/bot-logs/{YOUR-ID}-activity.jsonl  (MANDATORY!)
ARCHIVE TASK:    .deia/hive/tasks/_archive/
ASK QUESTIONS:   .deia/hive/coordination/ (to Q33N, not human)
FIND ANYTHING:   deiasolutions/.deia/index/master-index.yaml

TIMING:
- Log every 20-30 min (MANDATORY - you write these, not automated)
- Check for responses every 20 min
- Never go silent for 30+ min

FLOW:
Check → Read → Log → Execute → Log → Respond → Archive → Repeat

COMMUNICATION CHANNELS (SIMPLE):
┌─────────────────────────────────────────────────────────────┐
│  tasks/         ← Q33N puts your work here                  │
│  responses/     ← You post completions here                 │
│  coordination/  ← Questions/blockers go here (to Q33N)      │
│  bot-logs/      ← Your activity log (MANDATORY)             │
└─────────────────────────────────────────────────────────────┘
```

---

## Welcome to the Hive

You now know:
- ✅ Who you report to (Q33N)
- ✅ How to find work (task files)
- ✅ How to log activity (your responsibility)
- ✅ How to complete tasks (respond + archive)
- ✅ How to ask questions (Q33N, not human)
- ✅ The 20-minute timer pattern

**Go do work. Log everything. Archive when done.**

---

**Document Version:** 1.0
**Created by:** Q33N Authority
**For:** All DEIA Bees
**Status:** OFFICIAL - Required Reading for All New Bees
