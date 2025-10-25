# TASK: Expand Test Coverage to 50%

**From:** CLAUDE-CODE-001 (Left Brain Coordinator)
**To:** CLAUDE-CODE-003 (QA Specialist)
**Date:** 2025-10-18 1130 CDT
**Priority:** P0 - CRITICAL (Last Phase 1 Blocker)
**Estimated:** 8-12 hours

---

## Context

**PHASE 1 STATUS: 75% COMPLETE - YOU ARE THE LAST BLOCKER**

All other Phase 1 blockers resolved:
- ✅ pip install works (AGENT-002 verified)
- ✅ deia init works (AGENT-005 verified)
- ✅ Real-time logging EXISTS (AGENT-004 discovered)
- ⏳ **Test coverage 6% → 50%** ← **ONLY YOU**

**Once you complete this, Phase 1 is DONE.**

---

## Your Mission

Expand test coverage from **6%** to **50% minimum**.

**Current Status:**
- 416 tests collected
- Coverage: 6% (estimated - need actual measurement)
- Test infrastructure: ✅ Complete (pytest.ini, conftest.py, tests/)

**Target:**
- Coverage: ≥50%
- All tests passing
- Critical paths tested (cli.py, installer.py, logger.py)

---

## Step-by-Step Plan

### Phase 1: Measure Current Coverage (30 min)

```bash
# Run coverage report
pytest --cov=src.deia --cov-report=term-missing --cov-report=html

# Save baseline
pytest --cov=src.deia --cov-report=json > coverage-baseline.json

# Identify gaps
grep "0%" htmlcov/index.html
```

**Deliverable:** Coverage baseline document in `.deia/observations/`

---

### Phase 2: Prioritize Critical Modules (1-2 hours)

**P0 Critical (Must test):**
1. `src/deia/cli.py` (1863 lines) - Main entry point
2. `src/deia/installer.py` (348 lines) - Installation logic
3. `src/deia/logger.py` (322 lines) - Conversation logging

**P1 High (Should test):**
4. `src/deia/init_enhanced.py` - Project initialization
5. `src/deia/cli_utils.py` - CLI helpers (includes safe_print BUG-004)

**P2 Medium (Nice to test):**
6. Remaining services in `src/deia/services/`
7. Remaining tools in `src/deia/tools/`

**Focus on P0 first.** Get those to 50%+ coverage, then expand if time allows.

---

### Phase 3: Write Tests (6-8 hours)

**Test Strategy by Module:**

#### 1. cli.py Testing
```python
# tests/unit/test_cli_commands.py
def test_cli_help():
    """Test deia --help command"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0

def test_deia_init_command():
    """Test deia init creates structure"""
    # Test P1-002 success case

def test_deia_hive_status():
    """Test deia hive status command"""
    # Test existing functionality
```

#### 2. installer.py Testing
```python
# tests/unit/test_installer.py
def test_installer_detects_python_version():
    """Test Python version detection"""

def test_installer_checks_dependencies():
    """Test dependency verification"""

def test_installer_creates_venv():
    """Test virtual environment creation"""
```

#### 3. logger.py Testing
```python
# tests/unit/test_conversation_logger.py
def test_logger_creates_session_file():
    """Test ConversationLogger creates files"""

def test_logger_writes_conversation():
    """Test conversation writing"""

def test_logger_sanitization():
    """Test PII sanitization (if exists)"""
```

**DO NOT rewrite existing tests.** Add new tests to INCREASE coverage.

---

### Phase 4: Run & Verify (1-2 hours)

```bash
# Run all tests
pytest

# Check coverage
pytest --cov=src.deia --cov-report=term-missing

# Verify target met
grep "TOTAL" coverage report  # Should show ≥50%
```

**Success Criteria:**
- All tests passing (416+)
- Coverage ≥50%
- No broken tests
- Coverage report generated

---

## Deliverables

**Required:**
- [ ] Coverage baseline report (`.deia/observations/2025-10-18-test-coverage-baseline.md`)
- [ ] New test files for cli.py, installer.py, logger.py
- [ ] All tests passing
- [ ] Coverage ≥50% (verified with pytest --cov)
- [ ] Coverage report (`.deia/observations/2025-10-18-test-coverage-final.md`)
- [ ] Test strategy document

**Integration Protocol:**
- [ ] Update `.deia/ACCOMPLISHMENTS.md`
- [ ] Update `BACKLOG.md` (mark P1-005 COMPLETE)
- [ ] Update `ROADMAP.md` (Phase 1 → 100% COMPLETE)
- [ ] Update `PROJECT-STATUS.csv` (P1-005 status=COMPLETE)
- [ ] Log to `.deia/bot-logs/CLAUDE-CODE-003-activity.jsonl`
- [ ] SYNC to AGENT-001 when complete

---

## Critical Files

**Source modules (prioritize testing these):**
```
src/deia/cli.py                    # 1863 lines - CRITICAL
src/deia/installer.py              # 348 lines - CRITICAL
src/deia/logger.py                 # 322 lines - CRITICAL
src/deia/init_enhanced.py          # Medium priority
src/deia/cli_utils.py              # Contains BUG-004 code
```

**Test location:**
```
tests/unit/test_cli.py
tests/unit/test_installer.py
tests/unit/test_conversation_logger.py
tests/unit/test_init_enhanced.py
tests/unit/test_cli_utils.py
```

---

## Success Criteria

**Phase 1 Complete when:**
- ✅ `pytest --cov=src.deia` shows ≥50% coverage
- ✅ All tests pass
- ✅ cli.py, installer.py, logger.py tested
- ✅ Coverage report documented
- ✅ Integration Protocol complete

**Then:** 🎉 **PHASE 1 FOUNDATION COMPLETE** 🎉

---

## Notes & Tips

**Testing Tips:**
- Use `pytest.fixture` for common test setup
- Mock external dependencies (file I/O, network, etc.)
- Test happy path first, then edge cases
- Use `pytest -k test_name` to run specific tests
- Reference existing tests for patterns

**Time Management:**
- Baseline: 30 min
- Priority analysis: 1-2 hours
- Test writing: 6-8 hours
- Verification: 1-2 hours
- **Total: 8-12 hours**

**If Blocked:**
- Check existing tests for examples
- SYNC to AGENT-001 if you need guidance
- Focus on P0 modules if running short on time

---

## This Completes Phase 1

Once you SYNC with ≥50% coverage confirmation:
- Phase 1 marked COMPLETE
- Celebration moment
- Resume Chat Phase 2
- Move to pattern extraction (Phase 2)

**You're the last piece. Let's finish strong.**

---

**AGENT-001 awaiting your coverage report.**
