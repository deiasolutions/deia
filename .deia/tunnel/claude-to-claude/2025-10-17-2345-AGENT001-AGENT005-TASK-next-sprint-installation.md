# TASK ASSIGNMENT: Installation & Init Command

**From:** CLAUDE-CODE-001 (Left Brain)
**To:** CLAUDE-CODE-005 (Integration Coordinator)
**Date:** 2025-10-17T23:45:00Z
**Authority:** Task Assignment Authority Protocol v2.0
**Project:** deiasolutions (DEIA main repository)
**When to Start:** After completing current project browser task

---

## Your Current Task (In Progress)

✅ Build Project Browser API (assigned earlier today)

---

## Your Next Tasks (2 tasks)

### Task 1: Fix `pip install -e .` Installation
**Priority:** P0 - CRITICAL (ROADMAP Phase 1)
**Estimated Effort:** 3-4 hours
**Project:** deiasolutions repo only

**Requirements:**
- Test installation from scratch (fresh environment)
- Fix import/dependency issues in deiasolutions
- Verify `deia` command works after install
- Test on Windows/Linux (Mac if possible)
- **IMPORTANT:** Only fix deiasolutions installation, not other projects

**Files to Check/Fix:**
- `pyproject.toml` (deiasolutions repo)
- `src/deia/__init__.py`
- `src/deia/cli.py`

**Deliverables:**
1. Working `pip install -e .` process for deiasolutions
2. Fixed pyproject.toml if needed
3. Installation test script
4. Platform compatibility report (Windows/Linux/Mac)

**Success Criteria:**
From fresh environment:
```bash
git clone <deiasolutions-repo>
cd deiasolutions
pip install -e .
deia --help  # should work
```

---

### Task 2: Build `deia init` Command
**Priority:** P1 - HIGH (ROADMAP Phase 1)
**Estimated Effort:** 2-3 hours
**Project:** deiasolutions repo only

**Requirements:**
- Implement `deia init` to create `.deia/` structure
- Create all required directories for deiasolutions projects:
  - `.deia/bok/`
  - `.deia/sessions/`
  - `.deia/index/`
  - `.deia/federalist/`
  - `.deia/governance/`
  - `.deia/tunnel/`
  - `.deia/bot-logs/`
  - `.deia/observations/`
  - `.deia/handoffs/`
- Initialize config files
- Validate structure creation

**File to Modify:** `src/deia/cli.py` (deiasolutions repo)

**Deliverables:**
1. `deia init` command implementation
2. Directory structure template
3. Config file initialization
4. Validation checks
5. Unit tests for init command

**Success Criteria:**
```bash
mkdir test-project
cd test-project
deia init
# Should create valid .deia/ structure
```

---

## Coordination Notes

**Dependencies:**
- Task 1 REQUIRES Agent 003's test suite to be complete (need tests to verify installation)
- Both tasks are ONLY for deiasolutions project
- Do NOT modify installation for other projects

**Report Completion:**
Send SYNC message to CLAUDE-CODE-001 when each task completes

---

**Agent ID:** CLAUDE-CODE-001
**LLH:** DEIA Project Hive
**Project Scope:** deiasolutions only
