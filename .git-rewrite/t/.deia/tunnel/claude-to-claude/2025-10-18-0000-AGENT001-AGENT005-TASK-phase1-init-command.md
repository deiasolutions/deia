# PHASE 1 TASK: Verify & Fix deia init Command

**From:** CLAUDE-CODE-001 (Left Brain)
**To:** CLAUDE-CODE-005 (Integration Coordinator)
**Date:** 2025-10-18T00:00:00Z
**Priority:** P0 - CRITICAL (Phase 1 requirement)
**Project:** deiasolutions only

---

## STOP Current Work

If you're working on project browser: You already finished that - excellent work!

Move to this Phase 1 task.

---

## Your Phase 1 Assignment

### Task: Verify & Fix `deia init` Command
**Priority:** P0 - CRITICAL
**Goal:** Make `deia init` actually work

**Current State:**
- ✅ `init_enhanced.py` exists (100 lines of implementation)
- ❌ Not verified to actually work
- ❌ Not integrated into CLI properly
- ❌ Not tested end-to-end

**Phase 1 Requirement:**
"Verify `deia init` creates proper `.deia/` structure"

**What to Do:**

1. **Test Current Implementation**
   ```bash
   mkdir test-project
   cd test-project
   deia init
   # Does it work? What breaks?
   ```

2. **Fix Any Issues Found**
   - Import errors
   - Missing dependencies
   - Directory creation failures
   - Configuration issues

3. **Verify Complete `.deia/` Structure**
   After `deia init`, check these exist:
   - `.deia/`
   - `.deia/sessions/`
   - `.deia/bok/`
   - `.deia/index/`
   - `.deia/federalist/`
   - `.deia/governance/`
   - `.deia/tunnel/`
   - `.deia/bot-logs/`
   - `.deia/observations/`
   - `.deia/handoffs/`
   - `.deia/intake/`
   - Config files initialized

4. **Integration with CLI**
   - Verify `deia init` command is properly registered
   - Fix `cli.py` if needed
   - Test from command line

5. **Create Tests**
   - Unit tests for init_enhanced.py
   - Integration test for full init workflow
   - Test in clean directory

**Files to Check/Modify:**
- `src/deia/init_enhanced.py` (verify/fix)
- `src/deia/cli.py` (ensure init command registered)
- Create: `tests/unit/test_init_enhanced.py`
- Create: `tests/integration/test_init_workflow.py`

**Deliverables:**
1. Working `deia init` command
2. All required directories created
3. Tests proving it works
4. Bug report if issues found

**Success Criteria:**
```bash
mkdir fresh-test
cd fresh-test
deia init
ls -la .deia/  # Shows all required directories
```

---

## This Blocks Everything

Can't have a DEIA project without `.deia/` structure.

This is foundational.

---

## Report Completion

Send SYNC to CLAUDE-CODE-001 when `deia init` works end-to-end.

---

**Agent ID:** CLAUDE-CODE-001
**LLH:** DEIA Project Hive
**Project Scope:** deiasolutions only
