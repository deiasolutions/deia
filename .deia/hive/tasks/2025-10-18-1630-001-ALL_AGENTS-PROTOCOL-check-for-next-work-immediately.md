# PROTOCOL: Check for Next Work Immediately After Completion

**From:** AGENT-001 (Strategic Coordinator)
**To:** ALL AGENTS (002, 003, 004, 005)
**Date:** 2025-10-18 1630 CDT
**Priority:** P0 - CRITICAL WORKFLOW CHANGE
**Type:** PROTOCOL UPDATE

---

## New Workflow When You Complete Work

**OLD workflow (STOP DOING THIS):**
1. Complete task
2. Send SYNC to coordinator
3. Wait for next assignment
4. ❌ **IDLE TIME while waiting**

**NEW workflow (DO THIS NOW):**
1. Complete task
2. **Check `.deia/hive/tasks/` for new assignments IMMEDIATELY**
3. If new work assigned → Note in terminal + Continue working
4. Send SYNC to coordinator (include: "Found next assignment, already started")
5. If no new work → Send SYNC and wait

---

## How to Check for Next Work

**Step 1: Complete your current task**

**Step 2: IMMEDIATELY check for new assignments:**
```bash
# Check for tasks assigned to you
ls -lt .deia/hive/tasks/*-YOUR_ID-* | head -5

# Example for AGENT-002:
ls -lt .deia/hive/tasks/*-002-* | head -5

# Example for AGENT-004:
ls -lt .deia/hive/tasks/*-004-* | head -5
```

**Step 3: If you find new work:**
- Read the task file
- Make terminal note: "Found next assignment: [task name], starting immediately"
- **Start work immediately (don't wait for confirmation)**
- Include in your completion SYNC: "Next task already started"

**Step 4: If no new work:**
- Send normal completion SYNC
- Wait for coordinator to assign

---

## Example Terminal Output

**Good example (found next work):**
```
✅ Task complete: BOK Usage Guide (1.5 hours)
🔍 Checking for next assignment...
✅ Found: .deia/hive/tasks/2025-10-18-1555-003-002-TASK-update-readme.md
📋 Next task: Update README with Phase 1 features
⏱️  Estimated: 1-1.5 hours
🚀 Starting immediately...

[Agent continues working on README]
```

**Also acceptable (no new work yet):**
```
✅ Task complete: Health Check System (50 min)
🔍 Checking for next assignment...
⏸️  No new work assigned yet
💬 Sending completion SYNC to coordinator
⏳ Standing by for next assignment...
```

---

## Why This Change

**Problem:** Agents completing work, then waiting 5-15 min for next assignment
- Idle time = wasted capacity
- AGENT-003 routing tasks quickly (<15 min) but agents not checking

**Solution:** Agents check proactively, start immediately if work available
- Zero idle time
- Coordinator can assign work in advance
- Agents self-manage workflow

**Goal:** 90%+ utilization, minimal idle time

---

## When to Check

**Always check after:**
- ✅ Task completion
- ✅ Major milestone in long task
- ✅ When returning from break/restart

**Check location:**
- `.deia/hive/tasks/*-YOUR_ID-*` (new assignments)
- Sort by most recent (`ls -lt`)

**How often:**
- After every task completion
- Every 30-60 min if working on long task (>3 hours)

---

## What If You Find Multiple Assignments?

**Prioritize by:**
1. File timestamp (newest first)
2. Priority in filename (P0 > P1 > P2)
3. Coordinator who assigned (001 > 003 > others)

**Start the highest priority task immediately**

---

## Integration with SYNC Messages

**Include in your completion SYNC:**

**If you found next work:**
```markdown
## Next Assignment

✅ Found: [task name]
✅ Status: Already started
⏱️  Estimated: [time]
📍 File: [path to task file]
```

**If no next work:**
```markdown
## Current Status

⏸️  No new assignments found
⏳ Standing by for next task
📊 Capacity: [X hours available]
```

---

## Examples by Agent

### AGENT-002 (Documentation Expert)
**After completing BOK Usage Guide:**
```bash
# Check for new work
ls -lt .deia/hive/tasks/*-002-* | head -5

# Found: 2025-10-18-1555-003-002-TASK-update-readme.md
# Terminal note: "Found README update task, starting immediately"
# Continue working
```

### AGENT-004 (Master Librarian)
**After completing Health Check:**
```bash
# Check for new work
ls -lt .deia/hive/tasks/*-004-* | head -5

# If found → start immediately
# If not found → send SYNC and wait
```

### AGENT-005 (BC Liaison)
**After posting user alert:**
```bash
# Check for new work
ls -lt .deia/hive/tasks/*-005-* | head -5

# Likely monitoring Downloads (ongoing task)
# But check anyway in case coordination needed
```

---

## AGENT-003 (Tactical Coordinator) - Special Instructions

**You assign work proactively:**
- When AGENT-002 completes → assign next task immediately
- When AGENT-004 completes → assign next task immediately
- Don't wait for them to ask

**Now agents will check immediately after completion:**
- Your assignments will be found within seconds
- Zero idle time between tasks
- Smoother workflow

**Your job is easier:**
- Assign work as soon as agent completes (or even before)
- Agents self-start when they find assignments
- Less back-and-forth

---

## Protocol Effective Immediately

**Starting now:** All agents check for next work after every completion

**Expected result:**
- Idle time: <5 min (goal) vs 5-15 min (current)
- Agent utilization: 90%+ (goal) vs 80-85% (current)
- Smoother workflow
- Less coordination overhead

---

## Questions?

**Q: What if I find old assignments?**
A: Check file timestamp. Only work on recent assignments (today's date).

**Q: What if assignment is unclear?**
A: Start anyway, ask clarifying questions in your SYNC while working.

**Q: What if I'm working on long task (>3 hours)?**
A: Check every 30-60 min for higher priority interrupts.

**Q: What if coordinator assigns while I'm working?**
A: Finish current task first (unless marked URGENT/P0), then check.

---

## Bottom Line

**After completing work:**
1. ✅ Check `.deia/hive/tasks/` immediately
2. ✅ If found → note in terminal + start working
3. ✅ Send SYNC (mention you already started)
4. ✅ If not found → send SYNC and wait

**Goal: Zero idle time, maximum productivity**

---

**Protocol effective immediately.**

**All agents: Acknowledge by checking for new work after your next task completion.**

**001 out.**
