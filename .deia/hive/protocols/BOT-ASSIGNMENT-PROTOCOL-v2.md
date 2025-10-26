# Bot Assignment & Execution Protocol v2

**Purpose:** Efficient task execution. Bots focus on THEIR work only.
**Status:** NEW STANDARD PROTOCOL
**Date:** 2025-10-26

---

## CURRENT PROBLEM (What We're Fixing)

❌ Bots reading other bots' files
❌ Bots checking on other bots' progress
❌ Bots monitoring their own status
❌ Bots doing context research
❌ Wasted tokens on non-essential reads

**Result:** Reduced focus, slower execution, token waste

---

## NEW PROTOCOL: ASSIGNMENT → EXECUTE → REPORT

### Rule 1: Q33N Gives Clear Assignments

**Q33N's Job:**
- Create specific task files for each bot
- Post assignments to `.deia/hive/tasks/`
- Monitor bot progress
- Coordinate between bots
- Give new assignments

**Q33N does NOT:**
- Ask bots to read other files
- Ask bots to check on other bots
- Expect bots to coordinate themselves

### Rule 2: Bot Gets Assignment & Executes It

**Bot's Job:**
1. Read YOUR assignment file (`.deia/hive/tasks/2025-10-26-ASSIGNMENT-BOT-XXX-*.md`)
2. Execute EXACTLY what it says
3. Post result to `.deia/hive/responses/deiasolutions/`
4. STOP

**Bot does NOT:**
- ❌ Read other bots' task files
- ❌ Read other bots' response files
- ❌ Check on other bots' progress
- ❌ Wait for other bots
- ❌ Coordinate with other bots
- ❌ Read session logs
- ❌ Read status files they didn't create
- ❌ Do research on context
- ❌ Cross-reference with other work

### Rule 3: Assignment File Format

**Location:** `.deia/hive/tasks/2025-10-26-ASSIGNMENT-BOT-XXX-TASKNAME.md`

**Content:**
```
# Task Assignment: BOT-XXX - Task Name

Your task: [SPECIFIC THING TO DO]

Success criteria:
- [ ] Criterion 1
- [ ] Criterion 2

When done, post: `.deia/hive/responses/deiasolutions/bot-xxx-taskname-complete.md`

Format:
[Specific format for report]

Go.
```

**That's it.** No references to other bots, no "check on status", no "wait for this bot".

### Rule 4: Execution

**DO THIS:**
1. Read assignment
2. Do exactly what it says
3. Post result using exact filename
4. Done

**DON'T DO THIS:**
- ❌ Read other files for context
- ❌ Check if other bots are done
- ❌ Wait for other bots
- ❌ Modify your assignment
- ❌ Do extra work not in assignment
- ❌ Read status files

### Rule 5: Q33N Monitors Only

**Q33N watches:**
- `.deia/hive/responses/deiasolutions/bot-xxx-*-complete.md` files
- New files posted by bots
- Completion times
- Issues reported

**Q33N coordinates:**
- Creates next assignments based on results
- Gives new work immediately
- Fixes blockers
- No idle time

---

## File Structure

### Assignment Files (Q33N → Bots)
```
.deia/hive/tasks/
├── 2025-10-26-ASSIGNMENT-BOT-001-TASKNAME.md
├── 2025-10-26-ASSIGNMENT-BOT-003-TASKNAME.md
├── 2025-10-26-ASSIGNMENT-BOT-004-TASKNAME.md
```

**One file per bot per task.** Clear, specific, complete.

### Response Files (Bots → Q33N)
```
.deia/hive/responses/deiasolutions/
├── bot-001-taskname-complete.md
├── bot-003-taskname-complete.md
├── bot-004-taskname-complete.md
```

**One file per completed task.** Report results only.

### What Bots DON'T Read
```
❌ .deia/hive/responses/deiasolutions/bot-XXX-*.md (other bots' responses)
❌ .deia/sessions/ (session logs)
❌ .deia/reports/ (reports)
❌ Other bot task files
❌ Status files
```

---

## Communication Flow

### Current (❌ WRONG):
```
BOT-001 reads task
BOT-001 reads BOT-003's status to understand context
BOT-001 checks BOT-004's files
BOT-001 reads session logs
BOT-001 finally executes
(Lots of wasted tokens)
```

### New (✅ RIGHT):
```
Q33N: "BOT-001, do THIS. Success criteria: THIS. Report: THIS format."
BOT-001: "Read assignment. Execute. Post result."
Q33N: Monitoring... sees result... coordinates next steps
```

---

## Efficiency Rules

### For Bots:
1. **ONE TASK = ONE FILE READ** (your assignment only)
2. **EXECUTE** what it says
3. **POST RESULT** in exact format
4. **DONE**

### For Q33N:
1. **GIVE CLEAR ASSIGNMENTS** (no ambiguity)
2. **MONITOR RESULTS** (not process)
3. **COORDINATE NEXT WORK** (based on results)
4. **NO IDLE TIME** (always have next task ready)

---

## Example: RIGHT WAY

**Q33N Creates:**
```
.deia/hive/tasks/2025-10-26-ASSIGNMENT-BOT-001-BACKEND-CODE-REVIEW.md

Content:
# BOT-001: Code Review

Review your API endpoint code.

Check for:
- Security issues
- Error handling
- Edge cases

Success Criteria:
- All endpoints verified
- No issues found OR issues documented
- Report posted

When done, post:
bot-001-code-review-complete.md

Format:
```markdown
# BOT-001 Code Review

Status: READY FOR PRODUCTION / ISSUES FOUND

Issues: [list or none]

Next: [Ready for integration / Needs fixes]
```

Go.
```

**BOT-001 Does:**
1. Reads assignment (1 file, ~2 min read)
2. Reviews own code (20 min work)
3. Posts result (5 min write)
4. Done

**BOT-001 does NOT:**
- Read BOT-003's files
- Check on BOT-004's progress
- Read session logs
- Wait for other bots
- Do research

---

## What This Saves

### Tokens:
- ❌ Before: Each bot reads 5-10 files for context = 50 tokens per bot
- ✅ After: Each bot reads 1 assignment file = 5 tokens per bot
- **Savings: 45 tokens × 3 bots = 135 tokens per assignment cycle**

### Time:
- ❌ Before: 15 min per bot (work + research + monitoring)
- ✅ After: 10 min per bot (work only)
- **Savings: 5 min × 3 bots = 15 min per cycle**

### Focus:
- ❌ Before: Bots distracted, context-switching, reading irrelevant files
- ✅ After: Bots hyper-focused on assigned task

---

## Protocol Rules

### For Q33N (bee-000):
1. ✅ Create ONE clear assignment file per bot per task
2. ✅ Make assignments specific and complete
3. ✅ Monitor ONLY `.deia/hive/responses/deiasolutions/` for results
4. ✅ Create next assignments immediately when current complete
5. ✅ Never ask bots to coordinate with each other
6. ✅ Never ask bots to read other files
7. ✅ Never ask bots to check status

### For All Bots (001, 003, 004):
1. ✅ Read your assignment file ONLY
2. ✅ Execute exactly what it says
3. ✅ Post result in specified format
4. ✅ Done
5. ❌ Do NOT read other bots' files
6. ❌ Do NOT check on other bots
7. ❌ Do NOT read session logs or status files
8. ❌ Do NOT wait for other bots
9. ❌ Do NOT do extra research

---

## Implementation Starting Now

**All future assignments will follow this protocol:**
- One clear task file per bot
- No references to other bots
- No "wait for", "check on", "read"
- Execute and report only

**All bots:** Focus on YOUR assignment. Ignore everything else.

---

This is the new standard. Efficient. Focused. Fast.

🚀
