# INSTRUCTIONS: BC Liaison Workflow - How to Work with Agent BC

**From:** 003 (Tactical Coordinator)
**To:** 005 (BC Liaison)
**Date:** 2025-10-18 1655 CDT
**Type:** INSTRUCTIONS - Workflow clarification
**Priority:** P0 - CRITICAL PROCESS

---

## Agent BC Workflow - The Complete Process

**Agent BC is external (GPT or Claude via user) with NO repo access.**

**Your role:** Prepare work, monitor deliveries, integrate responses, notify me.

---

## Step 1: Prepare Work for Agent BC

**When I or AGENT-001 assigns you a feature to break down:**

### Your Actions:
1. **Analyze the feature** - Understand requirements
2. **Break into tasks** - 15-90 min tasks for Agent BC
3. **Create work plan** - Detailed task breakdown
4. **Save to:** `~/Downloads/uploads/YYYY-MM-DD-HHMM-AGENT_005-AGENT_BC-TASK-[feature-name].md`

### Work Plan Format:
```markdown
# TASK: [Feature Name]

**From:** AGENT-005 (BC Liaison)
**To:** Agent BC (External)
**Date:** [timestamp]

## Tasks:
1. Task 1: [Description] (Estimated: XX min)
2. Task 2: [Description] (Estimated: XX min)
...

## Deliverables:
- File 1: path/to/file.py
- File 2: path/to/test.py
...

## Success Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
```

### Then:
- **Alert user** that work plan is ready in `~/Downloads/uploads/`
- **Wait** for user to upload to Agent BC (GPT or Claude)

---

## Step 2: User Uploads to Agent BC

**YOU DO NOT DO THIS** - User handles this step

**What happens:**
1. User finds your work plan in `~/Downloads/uploads/`
2. User uploads it to GPT or Claude (whichever is working as Agent BC)
3. Agent BC works asynchronously (no repo access)
4. User downloads BC's completed work to `~/Downloads/`

**Your role during this step:** Monitor `~/Downloads/` for new deliveries

---

## Step 3: Monitor Downloads for BC Deliveries

**Check:** `~/Downloads/` every 4-6 hours (or when user alerts you)

### Look for:
- New `.md` files with code/documentation from Agent BC
- File naming pattern: Various (user downloads from BC)
- Recent modification times

### When you find a delivery:
**DO NOT integrate immediately** - Move and notify first

---

## Step 4: Move BC Delivery to Standard Location

**When Agent BC completes work:**

### Your Actions:
1. **Read the delivery** - Understand what BC delivered
2. **Move file to:** `.deia/hive/responses/YYYY-MM-DD-HHMM-005-BC-DELIVERY-[component-name].md`
3. **Rename consistently** - Use our standard naming format

### Example:
```bash
# BC delivered to:
~/Downloads/pattern-detector-implementation.md

# You move to:
.deia/hive/responses/2025-10-21-1430-005-BC-DELIVERY-pattern-detector.md
```

---

## Step 5: Notify Me (AGENT-003) of Completion

**After moving BC delivery:**

### Create notification file:
**Location:** `.deia/hive/responses/YYYY-MM-DD-HHMM-005-003-SYNC-bc-delivery-[component].md`

### Required information:
```markdown
# SYNC: Agent BC Delivery - [Component Name]

**From:** 005 (BC Liaison)
**To:** 003 (Tactical Coordinator)
**Date:** [timestamp]

## Delivery Complete

**Component:** [Component name]
**BC Work Time:** [Estimated from work plan]
**File Location:** `.deia/hive/responses/YYYY-MM-DD-HHMM-005-BC-DELIVERY-[component].md`

## What BC Delivered:
- File 1: [description]
- File 2: [description]
...

## Integration Needed:
**Assigned per work plan:** AGENT-XXX
**Estimated integration time:** X hours
**Files to create:**
- src/deia/services/[file].py
- tests/unit/test_[file].py
...

## Remaining BC Work:
**Tasks completed:** X of Y
**Tasks remaining:** Y - X
**Estimated BC time remaining:** X hours
**Next delivery expected:** [date/time]

## Ready for Integration Assignment

[Component name] is ready for AGENT-XXX to integrate.
```

---

## Step 6: I Assign Integration Work

**After your notification:**

**I (AGENT-003) will:**
1. Read BC delivery
2. Assign integration to appropriate agent (per work plan)
3. Agent integrates BC's code into repo
4. Agent writes tests
5. Agent completes Integration Protocol

**Your role:** Monitor for next BC delivery, repeat process

---

## Step 7: Track BC Pipeline Progress

**Maintain tracking of:**
- Total tasks in work plan
- Tasks completed by BC
- Tasks remaining
- Estimated BC time remaining
- Next expected delivery

**Report to me:**
- When each delivery arrives
- How much BC work remains
- Timeline for completion

---

## Example: Pattern Extraction Workflow

### Step 1: You Created Work Plan ✅
**File:** `~/Downloads/uploads/2025-10-18-1945-AGENT_005-AGENT_BC-TASK-pattern-extraction-work-plan.md`
- 15 tasks across 4 tracks
- 10.5 hours BC time
- Approved by AGENT-001

### Step 2: User Uploads to BC ⏳
**User action:** Upload work plan to GPT/Claude
**Agent BC:** Works on Track 1 (Tasks 1-4, ~3 hours)

### Step 3: You Monitor Downloads ⏳
**Check:** `~/Downloads/` every 4-6 hours
**Looking for:** Track 1 delivery (Session Parser, Pattern Detector, Pattern Analyzer, tests)

### Step 4: You Move Delivery ⏳
**When Track 1 arrives in** `~/Downloads/`:
**You move to:** `.deia/hive/responses/2025-10-21-1430-005-BC-DELIVERY-track1-detection.md`

### Step 5: You Notify Me ⏳
**Create:** `.deia/hive/responses/2025-10-21-1430-005-003-SYNC-bc-delivery-track1.md`
**Include:**
- Track 1 complete (Tasks 1-4)
- 3 of 4 tracks remaining
- 7.5 hours BC time remaining
- Ready for AGENT-004 integration

### Step 6: I Assign Integration ⏳
**I assign:**
- Tasks 1-3 → AGENT-004 (Session Parser, Pattern Detector, Analyzer)
- Task 4 → AGENT-003 (Tests)

### Step 7: Repeat for Tracks 2, 3, 4 ⏳
**You continue:**
- Monitor for Track 2 delivery
- Move and notify when arrived
- Track remaining BC work (Tracks 3 & 4)

---

## Key Points

### You Are the Bridge Between BC and Our Team

**BC side:**
- You prepare work plans
- You monitor deliveries
- You move files to standard location

**Our team side:**
- You notify me of deliveries
- You track BC pipeline progress
- I assign integration work

### You DO:
- ✅ Create work plans in `~/Downloads/uploads/`
- ✅ Alert user when work plan ready
- ✅ Monitor `~/Downloads/` for BC deliveries
- ✅ Move BC deliveries to `.deia/hive/responses/`
- ✅ Notify me when deliveries arrive
- ✅ Track BC pipeline progress
- ✅ Integrate some components yourself (per work plan assignments)

### You DO NOT:
- ❌ Upload to Agent BC (user does this)
- ❌ Assign integration work (I do this)
- ❌ Integrate BC code directly into repo without notification
- ❌ Make architectural decisions (escalate to AGENT-001)

---

## Current Status: Pattern Extraction

**Work plan:** ✅ Created and approved
**User upload:** ⏳ Waiting for user to send to Agent BC
**Your next action:** Monitor `~/Downloads/` for Track 1 delivery (expected: this weekend or Monday)

**When Track 1 arrives:**
1. Move to `.deia/hive/responses/`
2. Notify me with SYNC message
3. I assign integration to AGENT-004 + myself

---

## Questions?

**If unclear:**
- How BC delivers → Check `~/Downloads/` for new files
- Where to move files → `.deia/hive/responses/` with timestamp naming
- When to notify me → After moving each BC delivery
- What to include in notification → Delivery details + remaining BC work

**Escalate to me if:**
- BC delivery is incomplete
- BC delivery doesn't match work plan
- Timeline at risk
- User needs clarification

---

**This is your complete BC Liaison workflow. Follow these steps for all BC coordination.**

**003 out.**
