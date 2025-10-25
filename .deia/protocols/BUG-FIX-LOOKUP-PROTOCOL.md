# Bug Fix Lookup Protocol

**Version:** 1.0
**Effective:** 2025-10-18
**Applies to:** ALL AGENTS (Claude Code, GPT, ChatGPT, all LLMs)
**Authority:** CRITICAL PROCESS - MANDATORY COMPLIANCE

---

## ⚠️ THE PROBLEM

**Bug encountered 25+ times:** Windows Unicode encoding error (safe_print crash)
**Cumulative waste:** 4-5+ hours of duplicate debugging
**Root cause:** Agents not checking for existing fixes before implementing

**THIS ENDS NOW.**

---

## 🔴 MANDATORY PROTOCOL

### BEFORE fixing ANY bug, you MUST:

1. **STOP** - Do not immediately implement a fix
2. **SEARCH** - Check all bug documentation locations
3. **READ** - Review existing fixes and solutions
4. **REUSE** - Apply documented fix if exists
5. **DOCUMENT** - If new bug, document before fixing

**Violation:** Implementing a fix for a known bug without checking = process failure

---

## 📋 Required Search Locations (IN ORDER)

### 1. Bug Reports Database
**File:** `BUG_REPORTS.md`
**Search for:**
- Exact error message
- Error type (UnicodeEncodeError, ImportError, etc.)
- Component name (cli_utils, logger, installer)
- Symptom description

**Command:**
```bash
grep -i "error_message" BUG_REPORTS.md
grep -i "component_name" BUG_REPORTS.md
```

### 2. Pending Bug Submissions
**Location:** `.deia/submissions/pending/bug-*.md`
**Search for:**
- Error patterns
- File names
- Function names

**Command:**
```bash
find .deia/submissions/pending -name "bug-*.md" -exec grep -l "error_pattern" {} \;
```

### 3. Observations (Recent Discoveries)
**Location:** `.deia/observations/*.md`
**Search for:**
- Recent bug discoveries
- Pattern documentation
- Lessons learned

**Command:**
```bash
find .deia/observations -name "*.md" -exec grep -l "bug\|error\|fix" {} \;
```

### 4. Body of Knowledge (BOK)
**Location:** `.deia/index/master-index.yaml` + `bok/platforms/`
**Search for:**
- Platform-specific gotchas (Windows, macOS, Linux)
- Common patterns
- Known workarounds

**Command:**
```bash
grep -i "error_type\|platform" .deia/index/master-index.yaml
find bok/platforms -name "*.md" -exec grep -l "error_pattern" {} \;
```

### 5. Quick Reference Guide
**File:** `.deia/index/QUICK-REFERENCE.md`
**Check:**
- Proactive warnings section
- Platform gotchas
- Common issues

**Command:**
```bash
grep -i "error_pattern\|symptom" .deia/index/QUICK-REFERENCE.md
```

### 6. Session Logs (Historical Context)
**Location:** `.deia/sessions/*.md`
**Search for:**
- Similar errors in past sessions
- Previous solutions
- Conversation context

**Command:**
```bash
find .deia/sessions -name "*.md" -exec grep -l "error_message" {} \; | head -10
```

### 7. Project Status CSV
**File:** `.deia/PROJECT-STATUS.csv`
**Check:**
- Known bugs (BUG-* entries)
- Status (OPEN, FIXED, IN_PROGRESS)
- Assigned owner

**Command:**
```bash
grep -i "BUG.*error_pattern" .deia/PROJECT-STATUS.csv
```

---

## 🎯 Specific Known Bugs (MUST CHECK FIRST)

### BUG-004: safe_print Unicode Error ⚠️ CRITICAL

**Symptoms:**
- `UnicodeEncodeError: 'charmap' codec can't encode character`
- Error occurs when printing unicode symbols (✓, ⚠, •)
- Happens on Windows terminals (cp1252 encoding)
- Error in error handler (safe_print itself crashes)

**Solution Location:**
`.deia/submissions/pending/bug-safe-print-error-handler-crash.md`

**Status:** OPEN - Fix documented but NOT implemented
**Priority:** P1 - High (recurs 25+ times)
**Estimated fix time:** 30 minutes

**DO NOT:**
- Debug this from scratch
- Implement a new solution
- Waste time investigating

**DO:**
1. Read the bug report (lines 84-157 contain complete solution)
2. Implement the `emergency_print()` function
3. Update `safe_print()` in `src/deia/cli_utils.py`
4. Test on Windows terminal
5. Mark bug as FIXED in BUG_REPORTS.md
6. Update PROJECT-STATUS.csv

---

### BUG-005: PathValidator .ssh Regex ✅ FIXED

**Symptom:** .ssh directory not blocked by PathValidator
**Solution:** `.deia/observations/2025-10-17-pathvalidator-regex-bug.md`
**Status:** FIXED (2025-10-18)
**Pattern:** `\.ssh/` → `\.ssh($|/|\\)`

**If you encounter:** This is already fixed. Do NOT re-implement.

---

### BUG-003: Test Suite Bugs ✅ FIXED

**Symptoms:**
- Directory/file name collision
- Exception message mismatch

**Solution:** `BUG_REPORTS.md` lines 197-302
**Status:** FIXED (2025-10-17)

**If you encounter:** Already fixed in test_project_browser.py

---

## 📊 Search Command Reference

### Quick search across all bug docs:
```bash
# Search all bug locations at once
grep -r "error_pattern" BUG_REPORTS.md .deia/submissions/pending/ .deia/observations/ bok/platforms/
```

### Search master index for known patterns:
```bash
# Check taxonomy
grep -i "unicode\|encoding\|windows\|safe_print" .deia/index/master-index.yaml
```

### Check if bug already tracked in CSV:
```bash
# Search project status
grep -i "BUG.*unicode\|safe_print\|UnicodeEncodeError" .deia/PROJECT-STATUS.csv
```

---

## ✅ Compliance Checklist

Before implementing ANY bug fix:

- [ ] Searched BUG_REPORTS.md for error message
- [ ] Checked .deia/submissions/pending/bug-*.md
- [ ] Reviewed .deia/observations/ for recent discoveries
- [ ] Searched BOK (master-index.yaml + bok/platforms/)
- [ ] Checked QUICK-REFERENCE.md proactive warnings
- [ ] Searched session logs for historical context
- [ ] Verified bug not in PROJECT-STATUS.csv
- [ ] **If found:** Applied existing fix, did NOT reimplement
- [ ] **If new:** Documented bug BEFORE fixing
- [ ] Updated bug status after fix
- [ ] Logged activity to .deia/bot-logs/AGENT-*.jsonl

---

## 🚨 Known High-Recurrence Bugs

### Priority 1 - Check These FIRST:

| Bug ID | Symptom | Status | Location |
|--------|---------|--------|----------|
| BUG-004 | UnicodeEncodeError / safe_print crash | OPEN | .deia/submissions/pending/bug-safe-print-error-handler-crash.md |
| BUG-005 | .ssh directory not blocked | FIXED | .deia/observations/2025-10-17-pathvalidator-regex-bug.md |
| BOK-WINDOWS-UTF8 | Python console encoding | DOCUMENTED | bok/platforms/windows/python-console-utf8-encoding.md |

---

## 📝 New Bug Documentation Template

If you determine this IS a new bug:

```markdown
### BUG-XXX: [Clear Bug Title]
**Status:** 🟠 OPEN
**Severity:** [Critical/High/Medium/Low]
**Reported by:** [Agent ID]
**Date:** [YYYY-MM-DD]
**Recurrence:** 1 (first occurrence)

**Description:**
[What's broken]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Error Message:**
```
[Exact error text]
```

**Reproduction Steps:**
1. Step 1
2. Step 2

**Root Cause:**
[Technical analysis]

**Proposed Solution:**
[How to fix]

**Files Affected:**
- file1.py
- file2.py

**Estimated Effort:** [Hours]

**Related:**
- [Links to similar bugs or BOK entries]
```

**Then:**
1. Add to BUG_REPORTS.md
2. Add to PROJECT-STATUS.csv
3. Create detailed bug file in .deia/submissions/pending/
4. Update master-index.yaml if pattern-worthy
5. Log to activity.jsonl

---

## 🔍 Semantic Search Patterns

### Windows Python Unicode Issues:
**Search terms:** `unicode, encoding, charmap, cp1252, safe_print, UnicodeEncodeError`
**Locations:** BOK Windows platform, bug reports, observations
**Known fix:** BOK entry `python-console-utf8-encoding.md`

### Path Security Issues:
**Search terms:** `path, directory traversal, .ssh, .env, security, validator`
**Locations:** Observations, bug reports
**Known fix:** PathValidator class in `src/deia/services/path_validator.py`

### Import/Dependency Issues:
**Search terms:** `import, ModuleNotFoundError, dependency, pip, install`
**Locations:** Bug reports, observations, INSTALLATION.md
**Known fix:** Dependency list in `pyproject.toml` + INSTALLATION.md guide

### Test Failures:
**Search terms:** `pytest, test failure, assertion, mock, fixture`
**Locations:** Bug reports, observations
**Known fixes:** Various test files in `tests/unit/`

---

## 🎓 Learning from Failures

**Case Study: Unicode Bug Recurrence**

**Timeline:**
- First occurrence: 2025-10-09
- Bug documented: 2025-10-09
- Solution provided: 2025-10-09
- **Recurrences:** 25+ times (including 2025-10-17)
- **Total waste:** 4-5+ hours

**Why it keeps happening:**
1. Agents don't check bug reports before fixing
2. No mandatory search protocol
3. Knowledge exists but not accessed
4. Each agent treats as new bug

**Solution (THIS PROTOCOL):**
- MANDATORY search before fix
- Clear documentation locations
- Compliance checklist
- Proactive injection in Quick Reference

**Prevention:**
- Follow this protocol ALWAYS
- Update master index after every fix
- Keep PROJECT-STATUS.csv current
- Document patterns in BOK

---

## 🤖 For AI Agents

### Proactive Pattern Matching

If you see these error patterns, CHECK THESE FIRST:

**Error pattern:** `UnicodeEncodeError` + `charmap` + `codec`
→ **Check:** BUG-004, BOK Windows UTF-8 pattern

**Error pattern:** `.ssh` + `not blocked` + `security`
→ **Check:** BUG-005 (already fixed)

**Error pattern:** `ModuleNotFoundError` + `deia`
→ **Check:** INSTALLATION.md, pyproject.toml dependencies

**Error pattern:** `pytest` + `failed` + specific test name
→ **Check:** BUG-003, BUG_REPORTS.md test section

**Error pattern:** `Permission denied` + file operation
→ **Check:** PathValidator security docs, observations

### Integration with Query Tool

Future enhancement:
```bash
# Semantic search for bug fixes
deia librarian query "UnicodeEncodeError windows" --category bug-reports
```

---

## 📈 Success Metrics

**Protocol is working when:**
- Zero duplicate bug fixes in 30-day period
- <5 minutes from bug encounter to fix discovery
- 100% of agents check documentation first
- Bug recurrence rate = 0

**Monitor:**
- Activity logs for protocol compliance
- Bug report update frequency
- Time from error to resolution
- Duplicate work incidents

---

## ⚖️ Governance

**Authority:** CLAUDE-CODE-001 (Left Brain Coordinator)
**Enforcement:** All agents must comply
**Updates:** Coordinator updates protocol as needed
**Review:** Monthly review of compliance and effectiveness

**Violations:**
- First: Warning + re-training
- Second: Task reassignment
- Repeated: Process review and protocol update

---

## 📚 Related Documents

- `BUG_REPORTS.md` - Central bug database
- `.deia/PROJECT-STATUS.csv` - All tasks including bugs
- `.deia/index/master-index.yaml` - Semantic taxonomy
- `.deia/index/QUICK-REFERENCE.md` - Fast lookups
- `docs/process/INTEGRATION-PROTOCOL.md` - Task completion checklist
- `.deia/AGENTS.md` - Agent roles and coordination

---

**Remember:** 5 minutes searching saves 5 hours debugging.

**SEARCH FIRST. FIX SECOND. DOCUMENT ALWAYS.**

---

**Last Updated:** 2025-10-18
**Version:** 1.0
**Status:** ACTIVE - MANDATORY COMPLIANCE
**Coordinator:** CLAUDE-CODE-001
