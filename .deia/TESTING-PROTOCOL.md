# DEIA Testing Protocol

**Authority:** Dave (User/Project Lead)
**Effective Date:** 2025-10-28
**Status:** Official Process

---

## Core Principle

**Bots test their own shit before they say it's done. Dave doesn't test anything until it passes all bot tests.**

---

## Testing Hierarchy

### 1. BOT TESTING (Primary Gate)
**When:** Before marking any task as COMPLETE
**Who:** The bot doing the work (BOT-002, BOT-003, etc.)
**Requirement:** MANDATORY - Non-negotiable

**Bot Test Responsibilities:**
- Run applicable unit tests for changed code
- Run integration tests if cross-module changes
- Verify the feature/fix works as intended
- Document test results in the task completion response
- ONLY mark task complete if all tests pass

**Test Execution:**
```bash
# For Python code changes
pytest tests/unit/ -v --tb=short
pytest tests/integration/ -v --tb=short

# For specific module
pytest tests/unit/test_<module>.py -v
```

**Acceptance Criteria:**
- All existing tests pass (no regressions)
- New tests written for new functionality
- Coverage maintained or improved
- Error cases tested

### 2. DAVE VERIFICATION (Secondary Gate)
**When:** After bot marks task complete
**Who:** Dave (User)
**Requirement:** MANDATORY before code merges to main

**Dave Tests:**
- Reviews bot test results
- Spot checks critical paths
- May run full test suite before merge
- Verifies feature in context of larger system
- Makes go/no-go decision on merge

**Test Execution:**
```bash
# Full suite before merge
pytest --cov=src/deia --cov-report=html

# Specific concern area
pytest tests/integration/ -k "bot_launch" -v
```

---

## Test Organization

```
tests/
├── unit/               # Fast, isolated module tests
│   ├── test_bot_runner.py
│   ├── test_adapters.py
│   └── ... (individual module tests)
├── integration/        # Cross-module workflows
│   ├── test_bot_launch.py      ← Bot launch testing
│   ├── test_cli_workflows.py
│   └── ... (end-to-end tests)
├── fixtures/           # Shared test data
├── mocks/              # Mock implementations
├── conftest.py         # Pytest configuration
└── README.md
```

---

## Test Types & When to Use

### Unit Tests
**When:** Testing individual functions/classes in isolation
**Examples:**
- Bot runner initialization
- Path resolution logic
- Adapter initialization
- Error handling

**Run:** `pytest tests/unit/ -v`

### Integration Tests
**When:** Testing workflows across modules
**Examples:**
- Bot launch end-to-end
- Task submission and execution
- Multi-bot coordination
- API endpoints

**Run:** `pytest tests/integration/ -v`

### Slow/Heavy Tests
**Mark:** `@pytest.mark.slow`
**When:** Run locally before commit, skipped in CI feedback

**Run:** `pytest -m "not slow" -v` (skip slow)
**Run:** `pytest -m slow -v` (slow only)

---

## For This Fix: Claude Code CLI Launch Testing

**Bot should have tested:**
1. ✅ Path resolution returns correct directory
   ```python
   project_root = Path(__file__).parent.parent.parent.parent
   assert (project_root / "run_single_bot.py").exists()
   ```

2. ✅ spawn_bot_process() successfully finds script
   ```python
   # Before: would return None (script not found)
   # After: should return a PID
   ```

3. ✅ Claude Code bot actually launches
   ```python
   # POST to /api/bot/launch with bot_type="claude-code"
   # Should return success=True and valid PID
   ```

4. ✅ Bot process stays alive and initializes properly
   ```python
   # Check bot status endpoint returns "running"
   # Check adapter initialized with CLI type
   ```

**Dave will verify:**
- Full test suite passes
- No regressions in other adapters
- Claude Code bot actually executes a task
- Llama bot still works

---

## Running Tests

### Quick Check (Before Committing)
```bash
# Just unit tests, fast feedback
pytest tests/unit/ -v
```

### Pre-Merge Check (Before PR)
```bash
# Full suite with coverage
pytest tests/ -v --cov=src/deia --cov-report=term-missing
```

### Specific Module (Debugging)
```bash
pytest tests/unit/test_bot_runner.py::TestBotRunner::test_start -v -s
```

### With Print Statements (Debug)
```bash
pytest tests/ -v -s  # -s shows print() output
```

---

## Test Documentation

**When you write a test, document it:**
```python
def test_spawn_bot_process_finds_script():
    """
    Verify spawn_bot_process() can locate run_single_bot.py

    Bug Fix: Path resolution was off by 1 level, preventing script discovery
    Related: BUG-CLAUDE-CODE-CLI-LAUNCH-001
    """
    # Test code here
```

---

## Common Testing Commands

| Command | Purpose |
|---------|---------|
| `pytest` | Run all tests |
| `pytest tests/unit/` | Run only unit tests |
| `pytest tests/integration/` | Run only integration tests |
| `pytest -v` | Verbose output |
| `pytest -s` | Show print statements |
| `pytest -k "launch"` | Run tests matching "launch" |
| `pytest --lf` | Run last failed tests |
| `pytest --tb=short` | Shorter traceback |
| `pytest --cov=src/deia` | Coverage report |

---

## Coverage Requirements

- **Minimum:** 70% coverage on changed files
- **Target:** 80% coverage
- **Critical:** 95% coverage on security/auth code

Check coverage report:
```bash
pytest --cov=src/deia --cov-report=html
# Opens htmlcov/index.html
```

---

## When Tests Fail

**Step 1:** Read the error message (entire traceback)
**Step 2:** Run just that test with `-s` to see print output
**Step 3:** Check if it's a real bug or a test issue
**Step 4:** Document the failure in the task
**Step 5:** Don't mark complete until fixed

Example:
```bash
pytest tests/unit/test_spawner.py::test_spawn_bot -v -s
```

---

## Pytest Configuration

**File:** `pytest.ini`

```ini
[pytest]
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

addopts =
    -v                          # Verbose
    --strict-markers            # Require marker registration
    --tb=short                  # Short tracebacks
    --disable-warnings          # Cleaner output
    --cov=src/deia              # Coverage tracking
    --cov-report=term-missing   # Show missing lines
    --cov-report=html           # HTML report

markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (cross-module)
    slow: Slow/heavy tests (skip by default)
    security: Security tests
```

---

## Summary

**The Rule:**
1. **Bot does all testing** ← If not passing tests, task isn't done
2. **Bot documents results** ← Commit includes test output
3. **Dave reviews results** ← Then decides if it's actually done
4. **Dave runs tests again** ← Final verification before merge

**For Claude Code CLI Launch Fix:**
- Bot: Run tests on path resolution, bot spawning, adapter init
- Document: Test results in PR/commit
- Dave: Verify full test suite passes, do spot check
- Merge: Only after both gates pass

