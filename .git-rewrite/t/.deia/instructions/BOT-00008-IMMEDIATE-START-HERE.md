# IMMEDIATE ORDERS: BOT-00008 - Start Code Review

**From:** BOT-00001 (Queen)
**Date:** 2025-10-12
**Priority:** P0 - START NOW
**Context:** You're 9% from autocompact - keep focused

---

## 🎯 YOUR MISSION

**Review all Python code from Oct 11-12 for Path to 1.0**

**Full plan:** `.deia/instructions/BOT-00008-TASK-code-review-1.0.md` (read when you have context)

**Quick summary:** Dave wants comprehensive review of ALL recent work to determine path to DEIA 1.0. You handle code, BOT-09 handles docs, Queen synthesizes.

---

## 🚀 START HERE (Phase 1: Inventory)

### Step 1: Find the Python files (15 min)

```bash
# List all Python files modified in last 2 days
find . -name "*.py" -mtime -2 2>/dev/null | grep -v ".git" | grep -v "node_modules" | grep -v "__pycache__"

# Save to file for tracking
find . -name "*.py" -mtime -2 2>/dev/null | grep -v ".git" | grep -v "node_modules" | grep -v "__pycache__" > .deia/code-review-files.txt
```

### Step 2: Create inventory table (30 min)

Create file: `.deia/reports/BOT-00008-code-inventory-WIP.md`

**Use this template:**

```markdown
# Code Inventory - Work in Progress

**Reviewer:** BOT-00008
**Date:** 2025-10-12
**Status:** Phase 1 - Inventory

## Files Found

| # | File Path | Lines | Purpose | Has Tests? | Quick Assessment |
|---|-----------|-------|---------|------------|------------------|
| 1 | src/deia/hive.py | 276 | Hive management | Yes (test_hive.py) | Needs review |
| 2 | ... | ... | ... | ... | ... |

## Quick Stats
- Total files: X
- Total LOC: ~Y
- Files with tests: X/Y
- Priority 1 files: [list]
- Priority 2 files: [list]

## Next Steps
- [ ] Deep review of Priority 1 files
- [ ] Run tests and check coverage
- [ ] Document findings
```

**For each file, note:**
- Path
- Line count (use `wc -l filename.py`)
- One-sentence purpose
- Whether tests exist
- Priority (1=critical, 2=important, 3=nice-to-have)

### Step 3: Report inventory to Queen (5 min)

When done with inventory, create:

`.deia/reports/BOT-00008-inventory-complete.md`

```markdown
# Inventory Complete

**BOT-00008**
**Date:** 2025-10-12

## Summary
- Found X Python files
- Total ~Y lines of code
- Z files have tests

## Priority 1 Files (Need Deep Review)
1. src/deia/hive.py (276 lines) - Core hive functionality
2. [list others]

## Ready for Phase 2
Inventory complete. Ready to begin deep review of Priority 1 files.

## Request
Awaiting Queen's go-ahead for Phase 2.
```

---

## 📋 Expected Deliverables (This Session)

**Phase 1 Goal:** Create complete inventory

**Files you'll create:**
1. `.deia/code-review-files.txt` (list of files)
2. `.deia/reports/BOT-00008-code-inventory-WIP.md` (table)
3. `.deia/reports/BOT-00008-inventory-complete.md` (status)

**Time:** ~1 hour
**Output:** Clear list of what needs deep review

---

## 🎯 Key Files to Prioritize

Based on what Queen knows was built:

**Priority 1 (MUST REVIEW):**
- `src/deia/hive.py` - NEW, core hive management
- `src/deia/cli.py` - MODIFIED, new hive commands
- `tests/test_hive.py` - NEW, 15 tests
- `src/deia/bot_queue.py` - NEW? Bot queue service

**Priority 2 (SHOULD REVIEW):**
- `src/deia/config.py` - May be modified
- Other test files
- Integration modules

**Priority 3 (NICE TO HAVE):**
- Utility modules
- Extensions (if modified)

---

## 🚨 Keep It Simple (Low Context Mode)

**Do:**
- ✅ Focus on inventory ONLY this session
- ✅ List files, count lines, note tests
- ✅ Identify priorities
- ✅ Report to Queen when done

**Don't:**
- ❌ Deep code review yet (save for Phase 2)
- ❌ Run full analysis (not enough context)
- ❌ Write final report (that's later)

**Why:** You're 9% from autocompact. Get inventory done, report results, then we'll continue in fresh session for deep review.

---

## 📞 Coordination

**When inventory complete:**
1. Create inventory-complete.md report
2. Queen will review
3. Queen will confirm priorities
4. Fresh session for Phase 2 deep review

**If you hit issues:**
Create `.deia/instructions/ESCALATION-BOT-00008.md` with question

---

## 🎯 Success Criteria (This Session)

**Minimum:**
- [ ] Found all Python files from Oct 11-12
- [ ] Created inventory table
- [ ] Identified Priority 1, 2, 3 files
- [ ] Reported completion to Queen

**Target:**
- [ ] Accurate line counts
- [ ] Clear one-sentence purpose for each file
- [ ] Tests mapped to source files
- [ ] Prioritization justified

**Excellence:**
- [ ] Quick assessment notes in table
- [ ] Spotted obvious issues during inventory
- [ ] Clear recommendations for Phase 2 focus

---

## 📖 Reference (If Needed)

**Full plan:** `.deia/instructions/BOT-00008-TASK-code-review-1.0.md`
**Master plan:** `.deia/MASTER-REVIEW-PLAN-path-to-1.0.md`
**Status:** `.deia/STATUS-UPDATE-path-to-1.0-mobilized.md`

**But focus on inventory first. Details later.**

---

## 🚀 START NOW

1. Run find command
2. Create inventory table
3. Report results

**Time estimate:** 1 hour
**Goal:** Know exactly what needs deep review

---

**👑 By Order of the Queen**

**[BOT-00001 | Queen]**
**Orders issued:** 2025-10-12
**For:** BOT-00008
**Action:** Create code inventory (Phase 1)

---

**GO, BOT-00008. The hive is counting on you.**
