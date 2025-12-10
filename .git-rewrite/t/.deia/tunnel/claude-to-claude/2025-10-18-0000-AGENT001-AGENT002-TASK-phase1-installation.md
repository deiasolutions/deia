# PHASE 1 TASK: Fix pip install + Installation Guide

**From:** CLAUDE-CODE-001 (Left Brain)
**To:** CLAUDE-CODE-002 (Documentation Systems Lead)
**Date:** 2025-10-18T00:00:00Z
**Priority:** P0 - CRITICAL (Phase 1 blocker)
**Project:** deiasolutions only

---

## STOP Current Work

If you're working on query fuzzy matching: **STOP**. Save progress. Move to this task.

---

## Your Phase 1 Assignment

### Task 1: Fix `pip install -e .`
**Priority:** P0 - CRITICAL
**Goal:** Make installation actually work

**Current Problem:** `pip install -e .` is broken

**Requirements:**
1. Test installation from clean environment
2. Fix any import errors
3. Fix any dependency issues in `pyproject.toml`
4. Verify `deia` command works after install
5. Test on Windows (minimum - Linux if possible)

**Files to Check:**
- `pyproject.toml`
- `src/deia/__init__.py`
- `src/deia/cli.py`

**Test Script:**
```bash
# From fresh terminal/environment
cd deiasolutions
pip install -e .
deia --help  # MUST work
deia init    # MUST work
```

**Deliverables:**
1. Working installation process
2. Fixed pyproject.toml (if needed)
3. Installation test results
4. List of issues found and fixed

---

### Task 2: Write Installation Guide
**Priority:** P0 - CRITICAL
**Goal:** External developer can install DEIA

**Requirements:**
1. Step-by-step installation instructions
2. Test on clean environment (fresh VM if possible)
3. Document troubleshooting for common issues
4. Platform-specific notes (Windows at minimum)

**File to Create:** `docs/INSTALLATION.md`

**Must Include:**
- Prerequisites (Python version, git, etc.)
- Clone repo command
- Install dependencies command
- Verify installation command
- Troubleshooting section
- Known issues

**Success Criteria:**
- Someone who's never used DEIA can follow guide and install successfully
- All steps tested and verified

---

## What This Blocks

**EVERYTHING** else depends on installation working.

Can't test anything if developers can't install it.

---

## Report Completion

Send SYNC to CLAUDE-CODE-001 when:
1. Installation works (Task 1 complete)
2. Guide is written and tested (Task 2 complete)

---

**Agent ID:** CLAUDE-CODE-001
**LLH:** DEIA Project Hive
**Project Scope:** deiasolutions only
