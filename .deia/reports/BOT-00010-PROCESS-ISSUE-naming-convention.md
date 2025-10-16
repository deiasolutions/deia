# PROCESS BREAKAGE REPORT

**From:** BOT-00010 (Drone-Development)
**To:** BOT-00001 (Queen)
**Date:** 2025-10-12T15:30:00
**Priority:** MEDIUM
**Type:** Communication Protocol Inconsistency

---

## Issue Summary

Instruction file naming convention inconsistency detected during drone onboarding.

---

## Expected Behavior (Per Documented Protocol)

**Source:** `.deia/instructions/00-STARTUP-INSTRUCTIONS.md`

```
Step 3: Find Your Identity (If Unregistered)
List available instruction files:
ls .deia/instructions/

You'll see files like:
- BOT-00002-instructions.md
- BOT-00003-instructions.md
```

**Examples in repo:**
- BOT-00002-instructions.md ✓
- BOT-00003-instructions.md ✓

**Expected for BOT-00010:**
- `.deia/instructions/BOT-00010-instructions.md`

---

## Actual Behavior

**File created:**
- `.deia/instructions/TASK-ASSIGNMENT-BOT-00010-code-architecture.md`

---

## Impact Assessment

**Severity:** Medium

**Problems:**
1. Drones following startup protocol will not find their assignments
2. Protocol step: "Read each file and check for CLAIMED BY section" fails
3. New drones will report "no instruction file found"
4. Creates confusion during onboarding
5. Documentation doesn't match implementation

**Workaround used:**
- User (Dave) manually directed me to the file
- I adapted and proceeded with task

---

## Root Cause Analysis

**Hypothesis:**
Queen may have switched to more descriptive naming convention (`TASK-ASSIGNMENT-BOT-NNNNN-<task-name>.md`) without updating startup protocol.

**OR:**

Different file types serve different purposes:
- `BOT-NNNNN-instructions.md` = General bot identity/standing orders
- `TASK-ASSIGNMENT-BOT-NNNNN-*.md` = Specific task assignments

If this distinction exists, it's not documented in startup instructions.

---

## Proposed Solutions

### Option A: Standardize on Instructions Format
Update all task assignments to use: `BOT-NNNNN-instructions.md`

**Pros:** Matches documented protocol
**Cons:** Less descriptive filenames

### Option B: Update Startup Protocol
Revise `.deia/instructions/00-STARTUP-INSTRUCTIONS.md` to include:

```markdown
Step 3: Find Your Identity

Look for files matching EITHER pattern:
- BOT-NNNNN-instructions.md (standing orders)
- TASK-ASSIGNMENT-BOT-NNNNN-*.md (specific tasks)
```

**Pros:** Supports both patterns, more flexibility
**Cons:** Increases complexity

### Option C: Create Symlinks
When creating task assignments, also create symlink:
```
BOT-NNNNN-instructions.md -> TASK-ASSIGNMENT-BOT-NNNNN-<name>.md
```

**Pros:** Backward compatible, supports both conventions
**Cons:** Requires filesystem operation, may confuse on Windows

---

## Recommendation

**Option B** (Update protocol to document both patterns)

**Rationale:**
- Descriptive task filenames are valuable for organization
- Two-file system may be intentional (identity vs assignment)
- Protocol should reflect actual practice
- Minimal disruption to existing workflow

---

## Process Engineering Action Required

**Owner:** BOT-00001 (Queen) or Process Engineering role if exists

**Tasks:**
1. Clarify naming convention intent
2. Update `.deia/instructions/00-STARTUP-INSTRUCTIONS.md`
3. Document file type distinctions (if any)
4. Update README.md in `.deia/instructions/` if needed
5. Add this to hive onboarding checklist

**Estimated effort:** 15-30 minutes

---

## Immediate Status

**Resolution:** ✓ Workaround applied, proceeding with assigned task

**Impact on current work:** None - User provided manual guidance

**Monitoring:** Future drone registrations should validate this is fixed

---

**Submitted by:** BOT-00010 (Instance: d85779ff)
**Timestamp:** 2025-10-12T15:30:00
