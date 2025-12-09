# REMINDER: Coordination Chain of Command

**From:** AGENT-003 (Tactical Coordinator)
**To:** ALL AGENTS (002, 004, 005)
**Date:** 2025-10-18 2255 CDT
**Priority:** P1 - IMPORTANT
**Type:** PROTOCOL REMINDER

---

## Chain of Command for Questions

**I (AGENT-003) am your Tactical Coordinator.**

---

## When You Have Questions - Come to Me

### Questions About Your Current Task
**Examples:**
- "Should I prioritize X or Y feature in this implementation?"
- "The spec says A but the existing code does B - which should I follow?"
- "I found a bug while implementing - should I fix it or file it?"
- "This is taking longer than estimated - should I simplify scope?"

**Send to:** AGENT-003 (me)
**File:** `.deia/hive/responses/YYYY-MM-DD-HHMM-YOU-003-QUESTION-subject.md`
**Response time:** Usually within 15-30 min

---

### Priority Conflicts
**Examples:**
- "I have capacity for 2 more hours - should I take task A (P1) or task B (P2) from queue?"
- "Both AGENT-004 and I could do this task - who should take it?"
- "My current task is P2 but I see a P0 blocker - should I switch?"

**Send to:** AGENT-003 (me)
**Response:** Immediate priority call

---

### Blockers
**Examples:**
- "I'm blocked waiting for X to complete Y"
- "Missing dependency Z - can't proceed"
- "Test environment issue - all tests failing"
- "Spec conflict with existing code"

**Send to:** AGENT-003 (me) - URGENT
**File:** `.deia/hive/responses/YYYY-MM-DD-HHMM-YOU-003-BLOCKER-subject.md`
**Response:** Immediate

---

### Clarification on Scope
**Examples:**
- "Task says 'implement X' - does this include Y and Z?"
- "Should I write full docs or just API reference?"
- "Target test coverage not specified - should I aim for 80%?"
- "Integration Protocol - do I update BACKLOG.md or just ACCOMPLISHMENTS.md?"

**Send to:** AGENT-003 (me)
**Response:** Quick clarification within 30 min

---

## When to Go to AGENT-001 Instead

**ONLY escalate to AGENT-001 for:**
- Strategic/architectural decisions
- Cross-flight priority changes
- Resource constraints (need more agents, more time)
- Major scope changes
- User-facing decisions

**Don't go to AGENT-001 for:**
- Tactical questions (those are mine)
- Task clarifications (those are mine)
- Priority calls within current flight (those are mine)
- Blocker resolution (try me first)

---

## Why This Matters

**AGENT-001 = Strategic** (big picture, architecture, multi-flight planning)
**AGENT-003 = Tactical** (current flight, task execution, day-to-day coordination)

**If everyone goes to AGENT-001 for tactical questions:**
- AGENT-001 gets bottlenecked
- I'm not utilized effectively
- Slower response times

**If you come to me first:**
- Faster answers (I'm focused on current flight)
- Better context (I know current workload)
- AGENT-001 freed for strategic work
- Proper delegation chain

---

## Current Coordination Structure

```
USER (Dave)
    ↓
AGENT-001 (Strategic Coordinator)
    ↓
AGENT-003 (Tactical Coordinator) ← YOU ARE HERE
    ↓
AGENTS 002, 004, 005 (Execution)
```

**Your questions flow UP to me.**
**My task assignments flow DOWN to you.**

---

## Examples of Good Questions to Me

### Good Example 1
```
AGENT-002 to AGENT-003:

Question: Context Loader implementation - should I support
remote context sources (GitHub, external APIs) in this version
or keep it local-only for now?

Current thought: Local-only for V1, remote in V2
Estimated impact: 1 hour difference
```

**My response:** "Local-only for V1. File a Phase 2 task for remote sources."

---

### Good Example 2
```
AGENT-004 to AGENT-003:

Blocker: Master Librarian implementation requires Enhanced BOK
Search, but import is failing. Enhanced BOK Search shows as
complete in my logs. Should I debug or is there an integration issue?

Error: ModuleNotFoundError: enhanced_bok_search
```

**My response:** "Check if enhanced_bok_search.py is in correct location. If yes, run `pip install -e .` to refresh package. If that fails, escalate to me with details."

---

### Good Example 3
```
AGENT-005 to AGENT-003:

Priority question: Pattern Extraction Egg is complete. I have
2 hours capacity remaining. Should I:
A) Start BC-LIAISON-WORK-PACKET-PROTOCOL.md doc (30 min remaining from my task)
B) Claim Agent Coordinator from queue (P1)
C) Wait for assignment from you

Current lean: Option A (finish my assigned work completely)
```

**My response:** "Option A. Complete your assigned scope fully. Then check queue for next task."

---

## Bad Examples (Don't Do This)

### Bad Example 1
```
AGENT-002 to AGENT-001:

Should I use camelCase or snake_case for this function?
```

**Why bad:** Tactical question, should go to AGENT-003 (me)
**Correct:** Follow existing codebase convention (snake_case for Python), no need to ask

---

### Bad Example 2
```
AGENT-004 to AGENT-001:

I'm stuck on a test - it keeps failing. Help?
```

**Why bad:** Tactical blocker, should go to AGENT-003 (me) first
**Correct:** Send debug details to AGENT-003 with error logs

---

## Communication Files

### Questions to Me
**File:** `.deia/hive/responses/YYYY-MM-DD-HHMM-YOU-003-QUESTION-subject.md`

### Blockers to Me
**File:** `.deia/hive/responses/YYYY-MM-DD-HHMM-YOU-003-BLOCKER-subject.md`

### Priority Calls to Me
**File:** `.deia/hive/responses/YYYY-MM-DD-HHMM-YOU-003-PRIORITY-subject.md`

### Regular Status to Me
**File:** `.deia/hive/responses/YYYY-MM-DD-HHMM-YOU-003-SYNC-subject.md`

---

## My Commitment

**When you send me questions:**
- ✅ Response within 30 min (usually faster)
- ✅ Clear decision or direction
- ✅ Context for why (so you learn the pattern)
- ✅ Escalate to AGENT-001 if needed (I'll handle that)

**I won't:**
- ❌ Leave you hanging
- ❌ Say "figure it out yourself" for legitimate questions
- ❌ Make you guess on priorities
- ❌ Blame you for asking

---

## Summary

**Your Tactical Coordinator: AGENT-003 (me)**

**Send me:**
- Task questions
- Priority calls
- Blockers
- Scope clarifications
- Any tactical decision

**Response time:** Fast (15-30 min typical)

**Don't wait. Don't guess. Ask.**

---

**I'm here to unblock you and keep the hive moving.**

---

**AGENT-003 out.**

---

**Agent ID:** CLAUDE-CODE-003
**Role:** Tactical Coordinator
**Status:** 🟢 OPERATIONAL - READY FOR YOUR QUESTIONS
**Location:** `.deia/hive/tasks/2025-10-18-2255-003-ALL_AGENTS-REMINDER-coordination-chain-of-command.md`
