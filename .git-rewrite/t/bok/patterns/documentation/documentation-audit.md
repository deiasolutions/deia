# Documentation Audit Pattern

**Category:** Project Maintenance
**Difficulty:** Intermediate
**Time Required:** 1-3 hours
**Frequency:** Quarterly or after major releases

---

## Problem

Documentation drift is inevitable:
- Files become outdated as features evolve
- Redundant guides accumulate over time
- Cross-references break when files move
- Claims about capabilities become inaccurate
- New contributors get confused by contradictions

**Symptoms:**
- Users report "this doc says X but Y is actually true"
- Multiple docs explain the same thing differently
- README references non-existent files
- Setup instructions don't work
- Navigation is confusing (too many entry points)

---

## Solution

**Documentation Audit: Systematic verification and rationalization of project docs**

A structured process that:
1. Verifies claims against actual code/capabilities
2. Identifies redundant or contradictory documentation
3. Validates cross-references and file paths
4. Recommends consolidation and cleanup
5. Creates actionable remediation plan

---

## When to Use

**Triggers:**
- New major release approaching
- Multiple doc-related bug reports
- Onboarding feedback mentions confusion
- Quarterly maintenance cycle
- After significant refactoring
- Before going public/open-sourcing

**Don't use for:**
- Active development (wait for stability)
- Single doc updates (overkill)
- Brand new projects (<3 months old)

---

## Process

### Phase 1: Inventory & Index (30-60 min)

**Objective:** Understand what documentation exists

**Steps:**
1. List all documentation files
   ```bash
   find . -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" | sort
   ```

2. Categorize by purpose:
   - **User-facing:** README, QUICKSTART, tutorials
   - **Developer:** CONTRIBUTING, architecture docs
   - **Reference:** API docs, configuration guides
   - **Governance:** LICENSE, CODE_OF_CONDUCT, CONSTITUTION
   - **Internal:** Project notes, decisions, backlog

3. Create/update repository index (`.claude/REPO_INDEX.md`)
   - List core files (load first)
   - List reference files (load when needed)
   - List archive/deprecated files
   - Add decision rules (when to use which doc)

**Output:** Complete inventory categorized by purpose and priority

---

### Phase 2: Accuracy Verification (60-90 min)

**Objective:** Check if documentation matches reality

**For each user-facing doc, verify:**

#### A. Installation/Setup Instructions
- [ ] Commands actually exist (`deia init` → check CLI code)
- [ ] File paths are correct (`.deia/config.json` → verify structure)
- [ ] Prerequisites are accurate (Python version, dependencies)
- [ ] Steps work in stated order
- [ ] Success criteria are measurable

**Method:**
```bash
# Verify CLI commands exist
python -c "from src.deia.cli import main; main(['--help'])"

# Check file paths referenced in docs
grep -r "\.deia/" docs/ | # Extract paths, verify existence
```

#### B. Feature Claims
Compare docs to ROADMAP/changelog:
- [ ] "Auto-logging works" → Check ROADMAP phase status
- [ ] "Supports X platforms" → Verify in code
- [ ] "Integrates with Y tool" → Test or find evidence

**Method:**
- Read ROADMAP.md for "What works" vs "What doesn't"
- Cross-reference feature claims in README/QUICKSTART
- Flag overselling (claiming beta features as production-ready)

#### C. Code Examples
- [ ] Import statements work (`from deia.logger import X`)
- [ ] API usage matches actual signatures
- [ ] Examples run without errors
- [ ] Output matches what's shown

**Method:**
```bash
# Extract code blocks from docs, test them
python test_doc_examples.py docs/tutorial.md
```

#### D. Cross-References
- [ ] Internal links point to existing files
- [ ] Anchor links work (`#section-name`)
- [ ] External URLs are not 404

**Method:**
```bash
# Check all markdown links
markdown-link-check docs/**/*.md
```

**Output:** List of inaccuracies with severity (critical/minor) and line numbers

---

### Phase 3: Redundancy Analysis (30-45 min)

**Objective:** Identify overlapping/duplicate documentation

**For common topics, compare:**

| Topic | Doc 1 | Doc 2 | Doc 3 | Recommendation |
|-------|-------|-------|-------|----------------|
| Installation | README.md | QUICKSTART.md | INSTALL.md | Keep QUICKSTART, reference from README |
| Memory Setup | SETUP.md | HIERARCHY.md | INTEGRATION.md | Merge into one (simple→advanced) |

**Analysis criteria:**
- **Same topic, same depth** → Delete duplicate, keep better one
- **Same topic, different depth** → Merge (simple path first, advanced at end)
- **Same topic, different audience** → Keep both, add clear navigation
- **Outdated version** → Archive or delete

**Method:**
```bash
# Compare file lengths
wc -l QUICKSTART.md INSTALL.md

# Compare content similarity (manual review)
diff QUICKSTART.md INSTALL.md
```

**Output:**
- Table of redundant docs
- Recommended actions (delete/archive/merge)
- Priority order

---

### Phase 4: Recommendations (15-30 min)

**Objective:** Create actionable cleanup plan

**Deliverable: Audit Report with:**

1. **Summary** (2-3 sentences)
   - Overall quality assessment (A-F grade)
   - Major issues found
   - Estimated remediation time

2. **Issues Found** (categorized)
   - Critical: Broken instructions, factual errors
   - High: Misleading claims, dead links
   - Medium: Redundancy, outdated examples
   - Low: Typos, formatting inconsistencies

3. **Rationalization Plan** (specific actions)
   - Files to delete (with justification)
   - Files to archive (with location)
   - Files to merge (with strategy)
   - References to fix (with line numbers)

4. **Execution Plan** (ordered bash commands)
   ```bash
   # 1. Delete obviously wrong files
   git rm WRONG_FILE.md

   # 2. Archive superseded docs
   mkdir -p docs/archive
   git mv OLD_DOC.md docs/archive/

   # 3. Fix references (manual)
   # Edit README.md line 42: Change X to Y

   # 4. Commit
   git commit -m "Documentation audit: cleanup redundant files"
   ```

**Output:** Complete audit report (can be saved as `docs/audits/YYYY-MM-DD-audit.md`)

---

### Phase 5: Execution (varies)

**Objective:** Apply the remediation plan

**Steps:**
1. Review plan with team/maintainer
2. Execute in order (delete → archive → fix → merge)
3. Test instructions after fixes
4. Commit with clear message
5. Update CHANGELOG

**Verification:**
- [ ] All referenced files exist
- [ ] Setup instructions work end-to-end
- [ ] No broken links
- [ ] Navigation is clear

---

## Example: DEIA Project Audit (2025-10-07)

**Context:** After documentation sprint before crash, needed to verify accuracy

**Phase 1: Inventory**
- Found 50+ markdown files
- Created `.claude/REPO_INDEX.md` with categorization
- Identified 5 core files, 15 reference, 8 archive candidates

**Phase 2: Verification**
- ✅ CLI commands all exist and match docs
- ❌ QUICKSTART.md oversells auto-logging (still beta per ROADMAP)
- ❌ BOK_MOVED.md claims BOK moved to separate repo (incorrect - still in `bok/`)
- ✅ Memory hierarchy docs accurate

**Phase 3: Redundancy**
- Found 3 overlapping quickstart guides
- Found 2 overlapping memory setup guides
- Recommended deletion/merge

**Phase 4: Recommendations**
```markdown
## Immediate Actions
1. Delete BOK_MOVED.md (factually wrong)
2. Delete CONVERSATION_LOGGING_QUICKSTART.md (superseded)
3. Update README.md reference (line 75)
4. Add caveat to QUICKSTART.md (beta status)

## Medium Priority
5. Merge memory docs into one
6. Archive old how-to guides
```

**Phase 5: Execution**
- Deleted 3 files
- Archived 2 files
- Fixed 5 references
- Reduced root-level docs from 12 to 6

**Result:** A- grade, clear navigation, accurate claims

---

## Success Criteria

**A successful audit produces:**

✅ **Accurate documentation**
- Setup instructions work
- Feature claims match reality
- Code examples run
- Links are valid

✅ **Clear navigation**
- One obvious entry point (README → QUICKSTART)
- Clear "simple vs advanced" paths
- No contradictions

✅ **Minimal redundancy**
- Each topic covered once (or with clear differentiation)
- Root directory has <10 docs
- Archive exists for old versions

✅ **Actionable output**
- Specific line numbers for fixes
- Ordered execution plan
- Testable verification steps

---

## Tools & Automation

### Manual Tools (Human judgment required)
- Read docs vs read code
- Compare redundant docs
- Assess writing quality
- Decide merge strategy

### Automated Tools (Can be scripted)
```bash
# Check links
markdown-link-check docs/**/*.md

# Find dead file references
grep -r "path/to/file" docs/ | while read ref; do
  # Extract path, test existence
done

# Compare similarity
diff -u doc1.md doc2.md

# Verify CLI commands
python -c "from cli import main; main(['--help'])" 2>&1
```

### DEIA Integration
```bash
# Run automated checks
deia doctor docs

# Run full audit (with AI assistance)
/doc-audit
```

---

## Antipatterns

❌ **Don't:**
- Delete docs without reading them first
- Fix everything at once (test incrementally)
- Assume older = worse (sometimes newer docs are rushed)
- Skip verification (automated checks miss context)
- Audit during active development (moving target)

✅ **Do:**
- Keep audit report for reference
- Date archived files (`docs/archive/YYYY-MM-DD-old-setup.md`)
- Test instructions after every change
- Get second opinion on deletion decisions
- Schedule regular audits (quarterly)

---

## Variations

### Quick Audit (30 min)
- Skip Phase 3 (redundancy analysis)
- Focus on critical issues only
- Good for: Pre-release sanity check

### Deep Audit (1 week)
- Include API documentation
- Test all code examples
- Check translations/localizations
- User testing of instructions
- Good for: Major version releases

### Continuous Audit (Ongoing)
- Pre-commit hook checks links
- CI tests code examples
- Bot flags outdated version references
- Good for: Active projects

---

## Related Patterns

- **Documentation-First Development** - Prevent drift by updating docs before code
- **Living Documentation** - Generate docs from code/tests
- **Docs as Tests** - Code examples are also integration tests
- **README-Driven Development** - Write README first, implement to match

---

## Metadata

**Pattern ID:** `bok-pattern-doc-audit-001`
**Version:** 1.0
**Author:** DEIA Community
**Date:** 2025-10-07
**Status:** Stable
**Tested:** Yes (DEIA project)

**License:** CC BY-SA 4.0

---

## Discussion

**Q: How often should we audit?**
A: Quarterly for active projects, or after major milestones. Small projects: annually.

**Q: What if team disagrees on what's redundant?**
A: Keep both, add navigation. Example: "For quick start, see X. For detailed explanation, see Y."

**Q: Should we delete or archive?**
A: Archive if historical value (shows evolution). Delete if factually wrong or misleading.

**Q: Can this be fully automated?**
A: No. Automated tools catch links/commands, but human judgment needed for accuracy, redundancy, quality.

---

## Contributions

Improvements to this pattern? Submit to: https://github.com/deiasolutions/deia/issues

**Areas for expansion:**
- Automated link checking integration
- Example scripts for common checks
- Integration with documentation generators
- Multi-language documentation audits
