# Documentation Audit

**Purpose:** Systematically verify documentation accuracy and identify redundancies

**Pattern Reference:** `bok/patterns/documentation/documentation-audit.md`

---

## Instructions for Claude

When the user runs `/doc-audit`, follow this structured process:

### Phase 1: Inventory & Index (15-20 min)

1. **Find all markdown documentation:**
   ```bash
   find . -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/.deia/*" | sort
   ```

2. **Categorize files** into:
   - Core (README, QUICKSTART, main entry points)
   - Setup/Installation docs
   - Reference docs (API, configuration)
   - Governance (LICENSE, CONTRIBUTING, CONSTITUTION)
   - Internal (admin/, backlog, decisions)

3. **Check if REPO_INDEX.md exists:**
   - If yes: Verify it's accurate
   - If no: Offer to create one

**Output to user:**
```markdown
## Documentation Inventory

**Core Files (5):**
- README.md
- QUICKSTART.md
- ...

**Setup Docs (3):**
- ...

**Reference (12):**
- ...

**Total:** X markdown files

Proceeding to Phase 2: Verification...
```

---

### Phase 2: Accuracy Verification (30-45 min)

**For each core/setup doc, verify:**

#### A. Installation/Setup Instructions

1. **Extract command claims** from docs:
   ```bash
   grep -E "(npm|pip|deia|git) " QUICKSTART.md README.md
   ```

2. **Verify CLI commands exist:**
   ```bash
   # Test each command mentioned
   python -c "from src.X.cli import main; main(['--help'])" 2>&1
   ```

3. **Check file path references:**
   ```bash
   # Extract paths mentioned in docs
   grep -oE "\.\w+/[a-zA-Z0-9/_.-]+" docs/*.md
   # Verify each exists
   ```

4. **Compare claimed features to ROADMAP:**
   - Read ROADMAP.md (if exists)
   - Flag any overselling of features

**Flag issues:**
- ❌ Command doesn't exist
- ❌ File path incorrect
- ❌ Feature claimed as working but ROADMAP says beta/planned
- ❌ Import statements that fail

#### B. Cross-References

1. **Check internal links:**
   ```bash
   grep -oE "\[.*\]\([^)]+\)" docs/*.md README.md
   ```

2. **Verify referenced files exist**

3. **Test anchor links** (if critical docs)

**Flag issues:**
- ❌ Link to non-existent file
- ❌ Broken anchor links
- ⚠️ Links to deprecated docs

**Output to user:**
```markdown
## Verification Results

### Critical Issues (must fix):
- README.md:75 - References non-existent file: OLD_QUICKSTART.md
- QUICKSTART.md:45 - Claims "auto-logging works" but ROADMAP shows beta status

### Warnings:
- SETUP.md:120 - Links to deprecated installation guide

Proceeding to Phase 3: Redundancy Analysis...
```

---

### Phase 3: Redundancy Analysis (15-30 min)

1. **Identify docs on same topics:**
   - Installation/setup guides
   - Configuration docs
   - Getting started guides
   - API/reference docs

2. **For each group, compare:**
   ```bash
   # Check file lengths
   wc -l QUICKSTART.md INSTALL.md GETTING_STARTED.md

   # Quick diff
   diff QUICKSTART.md INSTALL.md | head -20
   ```

3. **Read each redundant set and assess:**
   - Same content → one should be deleted
   - Different depth → merge or add clear navigation
   - Different audience → keep both with cross-links
   - Outdated → archive

4. **Check for backup files:**
   ```bash
   find . -name "*.backup" -o -name "*.bak" -o -name "*~"
   ```

**Output to user:**
```markdown
## Redundancy Analysis

### Duplicate Content:
| Topic | Files | Recommendation |
|-------|-------|----------------|
| Installation | QUICKSTART.md, INSTALL.md, README.md | Keep QUICKSTART, reference from README, delete INSTALL |
| Memory Setup | MEMORY_SETUP.md, MEMORY_HIERARCHY.md | Merge into one (simple→advanced) |

### Backup Files:
- README.md.backup → Delete
- old_config.md~ → Delete

Proceeding to Phase 4: Recommendations...
```

---

### Phase 4: Generate Recommendations (10-15 min)

**Create structured audit report:**

```markdown
# Documentation Audit Report
**Date:** [today's date]
**Files Audited:** X
**Issues Found:** Y critical, Z warnings

---

## Executive Summary

Overall Quality: [A-F grade]

[2-3 sentence summary]

---

## Critical Issues (Fix Immediately)

1. **[Issue description]**
   - File: path/to/file.md:line
   - Problem: [description]
   - Fix: [specific action]

---

## High Priority (Fix Soon)

[Same format]

---

## Redundancy Issues

[Table from Phase 3]

---

## Execution Plan

```bash
# 1. Delete factually wrong files
git rm WRONG_FILE.md

# 2. Archive superseded docs
mkdir -p docs/archive
git mv OLD_DOC.md docs/archive/

# 3. Fix references (manual edits needed)
# README.md:75 - Change X to Y
# QUICKSTART.md:45 - Add beta caveat

# 4. Commit
git add -A
git commit -m "Documentation audit: fix inaccuracies and remove redundant files"
```

---

## Recommended File Structure (After Cleanup)

### Root Level (Keep <10 files):
- README.md
- QUICKSTART.md
- ...

### Remove/Archive:
- [list]

---

## Next Steps

1. Review this report
2. Execute plan incrementally
3. Test instructions after fixes
4. Schedule next audit: [3 months from now]
```

**Save report to:**
```bash
docs/audits/YYYY-MM-DD-audit.md
```

**Show to user:**
- Summary
- Ask if they want to proceed with execution

---

### Phase 5: Execution (Optional - User Confirms)

**Only if user says "proceed" or "execute":**

1. **Show execution plan again**

2. **Confirm each destructive action:**
   - "Delete BOK_MOVED.md? (factually incorrect)"
   - Wait for confirmation

3. **Execute confirmed actions:**
   ```bash
   git rm [file]
   mkdir -p docs/archive
   git mv [file] docs/archive/
   ```

4. **For manual edits, guide user:**
   - "Edit README.md line 75"
   - "Change [old text] to [new text]"
   - Use Edit tool if user wants help

5. **After all changes:**
   ```bash
   git status
   ```
   - Show what changed
   - Ask about committing

**DO NOT auto-commit.** Let user review and commit manually.

---

## Usage Notes

**When to use:**
- User explicitly asks for documentation audit
- Quarterly maintenance
- Before major releases
- After significant refactoring

**When NOT to use:**
- During active development (moving target)
- For single doc fixes (overkill)
- In projects <1 month old (too early)

**Estimated time:**
- Small project (<20 docs): 30-60 min
- Medium project (20-50 docs): 1-2 hours
- Large project (50+ docs): 2-4 hours

**Important:**
- Be thorough but concise in output
- Flag issues by severity (critical/high/medium/low)
- Give specific line numbers for fixes
- Don't auto-delete without confirmation
- Save audit report for future reference

---

## Example Output

```markdown
Starting documentation audit...

## Phase 1: Inventory
Found 47 markdown files
- Core: 6 files
- Setup: 4 files
- Reference: 18 files
- Governance: 3 files
- Internal: 16 files (excluded from audit)

## Phase 2: Verification
Checking installation instructions... ✓
Checking CLI commands... ❌ Found 2 issues
Checking file paths... ✓
Checking cross-references... ⚠️ Found 3 warnings

## Phase 3: Redundancy
Found 3 sets of redundant docs
Identified 2 backup files for deletion

## Phase 4: Recommendations
Generated audit report: docs/audits/2025-10-07-audit.md

**Summary:**
- Grade: B+
- 2 critical issues (broken setup instructions)
- 5 redundant files (recommend merge/delete)
- Estimated fix time: 30 minutes

**Next:** Review report and confirm execution plan?
```

---

## Edge Cases

**If no issues found:**
```markdown
✅ Documentation audit complete!

No critical issues found.
No redundant files detected.
All links valid.

**Grade: A**

Next audit recommended: [3 months from now]
```

**If project has no docs:**
```markdown
⚠️ No documentation found.

Recommend creating:
1. README.md (what/why/how)
2. QUICKSTART.md (installation)
3. CONTRIBUTING.md (how to help)

Would you like me to create starter templates?
```

**If ROADMAP missing:**
```markdown
⚠️ No ROADMAP.md found - cannot verify feature claims.

Recommend creating ROADMAP to track:
- What works now
- What's in progress
- What's planned

This prevents docs from overselling capabilities.
```

---

## Success Criteria

Audit is successful when:
- ✅ All core docs verified for accuracy
- ✅ Redundancies identified with recommendations
- ✅ Cross-references validated
- ✅ Audit report saved for reference
- ✅ Execution plan is actionable (specific file:line references)
- ✅ User understands what needs fixing and why

---

**Pattern developed from actual DEIA audit session (2025-10-07)**
