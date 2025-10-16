---
type: bug
project: deiasolutions
created: 2025-10-09
status: pending
sanitized: true
category: process
severity: high
reporter: davee
---

# Bug: Claude Code Doesn't Follow Startup Checklist on Session Resume

## Problem

When a Claude Code session resumes from a previous conversation, Claude does not follow the startup checklist defined in `.claude/INSTRUCTIONS.md` and `.claude/REPO_INDEX.md`.

This causes:
- Inefficient searching (grep/glob instead of using index)
- Missing auto-log checks
- Ignoring documented processes
- Wasted time and frustration

## Current Behavior

**On session resume:**
1. Claude continues from previous context
2. Does NOT read `.claude/INSTRUCTIONS.md`
3. Does NOT read `.claude/REPO_INDEX.md`
4. Does NOT check auto-log status
5. Proceeds without startup orientation

**Result:** Claude searches for documentation inefficiently instead of using the index

## Expected Behavior

**On EVERY session start (new or resumed):**
1. Read `.claude/INSTRUCTIONS.md` (startup checklist)
2. Read `.claude/REPO_INDEX.md` (file navigation)
3. Check `.deia/config.json` for auto-log status
4. Orient to project before proceeding

## Example of Failure

**Session:** 2025-10-09 (continuation)

Dave asked: "What is the proper method for DEIA global admin to review submissions?"

Claude's response:
- Used `Grep` to search for "admin review"
- Used `Glob` to find admin files
- Eventually found `SUBMISSION_WORKFLOW.md`

**What should have happened:**
1. Read `.claude/REPO_INDEX.md` first
2. See that process docs exist
3. Check index for submission workflow reference
4. Go directly to documented process

**Index says (line 125):**
> Load on startup:
> - This index
> - ROADMAP.md (know what works)
> - QUICKSTART.md (know the simple path)

Claude didn't load the index.

## Root Cause

**Technical:** Claude Code session resume doesn't trigger startup behaviors

**Contributing factors:**
1. No automated reminder to check startup files
2. REPO_INDEX.md is incomplete (missing recent docs)
3. No process to keep index updated
4. Instructions say "read on startup" but resumption isn't "startup"

## Impact

- **Wasted Time:** Searching instead of using index
- **User Frustration:** "Why are you not using the index?"
- **Process Violation:** Not following documented procedures
- **Trust Erosion:** User created tools, Claude ignores them

## Proposed Solution

### 1. Create Startup Checklist (Always Follow)

**File:** `.claude/STARTUP_CHECKLIST.md`

```markdown
# Claude Code Startup Checklist

**Run this EVERY session (new or resumed):**

- [ ] Read `.claude/INSTRUCTIONS.md`
- [ ] Read `.claude/REPO_INDEX.md`
- [ ] Check `.deia/config.json` auto_log status
- [ ] Read `ROADMAP.md` (know what works)
- [ ] Review pending todos (if any)

**Then proceed with user request.**
```

### 2. Update Index Regularly

**Add to development process:**

**After creating/updating ANY doc:**
```bash
# Update index
deia update-index

# Or manual: Edit .claude/REPO_INDEX.md
```

**Trigger points:**
- After writing new doc
- After major refactoring
- Weekly maintenance (check index accuracy)
- Before major release

### 3. Index Maintenance Command (New Feature)

```bash
deia doctor index

# Output:
# Checking .claude/REPO_INDEX.md...
#
# ⚠️  Missing from index:
#   - docs/SUBMISSION_WORKFLOW.md (created 2025-10-09)
#   - docs/Dave-Questions-Dialog.md (created 2025-10-09)
#   - docs/DEV-PRACTICES-SUMMARY.md (created 2025-10-09)
#
# 📝 Outdated entries:
#   - docs/backlog/ (listed but doesn't exist)
#
# [U]pdate index | [S]kip
```

### 4. Reminder in DEIA Memory

**Update:** `.claude/preferences/deia.md`

Add prominent reminder:
```markdown
## ALWAYS START BY:
1. Reading .claude/STARTUP_CHECKLIST.md
2. Reading .claude/REPO_INDEX.md
3. Checking auto-log config

DO THIS EVERY SESSION (new or resumed)
```

## Immediate Actions

### Fix #1: Update REPO_INDEX.md Now

Add missing docs:
- `docs/SUBMISSION_WORKFLOW.md` - Admin review process
- `docs/SUBMISSION_WORKFLOW_AUDIT.md` - Workflow gap analysis
- `docs/Dave-Questions-Dialog.md` - Q&A tracking
- `docs/DEV-PRACTICES-SUMMARY.md` - Coding standards
- `docs/CLAUDE-PROJECT-BRIEFING.md` - Strategic context
- `docs/decisions/0001-extension-python-installation-strategy.md` - ADR

### Fix #2: Create STARTUP_CHECKLIST.md

Make it impossible to miss.

### Fix #3: Add Index Update to Process

**In CONTRIBUTING.md:**
```markdown
## When You Create/Update Docs

1. Write/update the doc
2. Update .claude/REPO_INDEX.md
3. Commit both together
4. Run: deia doctor index (to verify)
```

## Acceptance Criteria

- [ ] `.claude/STARTUP_CHECKLIST.md` created
- [ ] `.claude/REPO_INDEX.md` updated with all current docs
- [ ] Index update process documented in CONTRIBUTING.md
- [ ] `deia doctor index` command implemented (or manual process defined)
- [ ] DEIA memory updated with startup reminder
- [ ] Claude follows checklist on next session (test!)

## Priority

**P1 - High**

This breaks the fundamental workflow Dave set up. The index exists specifically to prevent inefficient searching, and Claude is ignoring it.

## Related Issues

- Missing: Index maintenance process
- Missing: `deia doctor index` command
- Issue: REPO_INDEX.md out of date
- Issue: No automated startup checks

---

**Lesson:** Documentation is useless if not followed. Need both technical solution (startup checks) and process solution (keep index updated).
