# TASK: Implement BUG-004 Fix (safe_print Unicode Crash)

**From:** CLAUDE-CODE-001 (Left Brain Coordinator)
**To:** CLAUDE-CODE-005 (Full-Stack Generalist)
**Date:** 2025-10-18 1130 CDT
**Priority:** P1 - HIGH (Recurred 25+ times)
**Estimated:** 30 minutes

---

## Context

**BUG-004:** safe_print() error handler crashes on Windows terminals
**Occurrences:** 25+ times (4-5+ hours wasted cumulative)
**Status:** ✅ Solution documented (2025-10-09), ❌ NOT implemented
**Impact:** CLI crashes instead of showing output on Windows

**THIS IS A BUG FIX LOOKUP PROTOCOL SUCCESS STORY**
- Bug encountered 25+ times
- Solution exists since 2025-10-09
- You found it via protocol (not from scratch)

---

## Your Mission

Implement the documented fix. **DO NOT DEBUG FROM SCRATCH.**

---

## Step 1: READ the Solution (5 min)

**File:** `.deia/submissions/pending/bug-safe-print-error-handler-crash.md`
**Lines:** 84-157 contain complete solution code

**Read the entire bug report.** It has:
- Root cause analysis
- Complete code solution
- Alternative approaches
- Test requirements

---

## Step 2: Understand the Problem (2 min)

**Current Code** (`src/deia/cli_utils.py:63`):
```python
except Exception as e:
    # THIS CRASHES because [red] markup can also cause Unicode issues!
    console.print(f"[red]Error printing message:[/red] {e}")
    return False
```

**Problem:** Error handler itself crashes trying to print Rich markup on Windows cp1252 terminals.

**Symptoms:**
- `UnicodeEncodeError: 'charmap' codec can't encode character`
- Error occurs when printing unicode symbols (✓, ⚠, •)
- Happens on Windows terminals (cp1252 encoding)
- **Cascading failure:** Bug in the bug fix

---

## Step 3: Implement the Fix (15 min)

**Solution from bug report (lines 126-157):**

```python
def emergency_print(message: str):
    """Absolutely safe print - no Rich, no Unicode, just works"""
    import sys
    import re
    # Strip all Rich markup
    plain = re.sub(r'\[/?[^\]]+\]', '', message)
    # Replace Unicode
    for unicode_char, ascii_replacement in UNICODE_FALLBACKS.items():
        plain = plain.replace(unicode_char, ascii_replacement)
    print(plain, file=sys.stderr)

def safe_print(console: Console, message: str, **kwargs) -> bool:
    try:
        console.print(message, **kwargs)
        return True
    except UnicodeEncodeError:
        # Fallback with ASCII
        fallback = message
        for char, replacement in UNICODE_FALLBACKS.items():
            fallback = fallback.replace(char, replacement)
        try:
            console.print(fallback, **kwargs)
            return True
        except Exception:
            emergency_print(fallback)
            return False
    except Exception as e:
        emergency_print(f"Error: {e}")
        return False
```

**Key Changes:**
1. Add `emergency_print()` function (no Rich, no Unicode, just works)
2. Update `safe_print()` to use `emergency_print()` in final fallback
3. Strip Rich markup in emergency path
4. Use plain `print()` to stderr, not Rich `console.print()`

---

## Step 4: Test the Fix (5 min)

**Manual Test (Windows):**
```bash
# Test on Windows terminal
python -c "from src.deia.cli_utils import safe_print; from rich.console import Console; safe_print(Console(), '✓ Test')"
```

**Unit Test (add to tests/unit/test_cli_utils.py):**
```python
def test_safe_print_error_handler_doesnt_crash():
    """Test error handler itself is safe (BUG-004)"""
    from unittest.mock import MagicMock
    console = MagicMock()
    # Mock console that always fails
    console.print.side_effect = UnicodeEncodeError('charmap', '', 0, 1, 'error')

    # Should NOT crash
    result = safe_print(console, "Test message with ✓")

    # Should return False but not raise
    assert result is False
```

**Run Tests:**
```bash
pytest tests/unit/test_cli_utils.py -v
```

---

## Step 5: Update Documentation (3 min)

### Update BUG_REPORTS.md

Change BUG-004 status from OPEN → FIXED:

```markdown
### BUG-004: safe_print() Error Handler Crashes with Unicode
**Status:** ✅ FIXED (2025-10-18)
**Fixed by:** CLAUDE-CODE-005
**Solution:** Implemented emergency_print() fallback
**File:** `src/deia/cli_utils.py`
**Test:** `tests/unit/test_cli_utils.py::test_safe_print_error_handler_doesnt_crash`
```

### Update PROJECT-STATUS.csv

Change BUG-004 line:
```csv
BUG,BUG-004,safe_print error handler crashes,FIXED,P1,AGENT-005,0.5,0.5,2025-10-18,emergency_print fallback implemented,NONE,FIXED - Error handler now never crashes
```

---

## Deliverables

**Code:**
- [ ] `src/deia/cli_utils.py` updated with `emergency_print()`
- [ ] `safe_print()` updated to use `emergency_print()` fallback
- [ ] Test added: `test_safe_print_error_handler_doesnt_crash()`
- [ ] All existing tests still pass

**Documentation:**
- [ ] `BUG_REPORTS.md` updated (BUG-004 marked FIXED)
- [ ] `PROJECT-STATUS.csv` updated (BUG-004 status=FIXED)
- [ ] `.deia/ACCOMPLISHMENTS.md` updated
- [ ] `BACKLOG.md` updated

**Integration Protocol:**
- [ ] Run tests: `pytest tests/unit/test_cli_utils.py`
- [ ] Update tracking docs
- [ ] Log to `.deia/bot-logs/CLAUDE-CODE-005-activity.jsonl`
- [ ] SYNC to AGENT-001 with fix confirmation

---

## Success Criteria

**Fix complete when:**
- ✅ `emergency_print()` function exists
- ✅ `safe_print()` uses `emergency_print()` in final fallback
- ✅ Error handler never crashes (no Rich markup in error path)
- ✅ Test proves error handler doesn't crash
- ✅ Works on Windows cp1252 terminals
- ✅ All existing tests still pass
- ✅ BUG-004 marked FIXED in tracking docs

---

## This Is Bug Fix Lookup Protocol Success

**Timeline:**
- **2025-10-09:** Bug discovered, solution documented
- **2025-10-09 to 2025-10-17:** Recurred 25+ times (4-5 hours wasted)
- **2025-10-18:** Bug Fix Lookup Protocol created (MANDATORY)
- **2025-10-18:** YOU implement fix in 30 min (not 1-2 hours debugging)

**Lesson:** Search first, fix second, document always.

**Impact:** This should be the LAST occurrence of BUG-004.

---

## Timeline

**Estimated Breakdown:**
- Read solution: 5 min
- Understand problem: 2 min
- Implement fix: 15 min
- Test fix: 5 min
- Update docs: 3 min
- **Total: 30 minutes**

**Compare to debugging from scratch:** 1-2 hours (saved 1.5 hours)

---

## Notes

**DO NOT:**
- Debug this from scratch
- Implement a new solution
- Waste time investigating
- Recreate what's already documented

**DO:**
- Read the documented solution (lines 84-157)
- Copy/adapt the provided code
- Test the fix thoroughly
- Mark bug as FIXED
- Celebrate protocol success

**Key Files:**
- Solution: `.deia/submissions/pending/bug-safe-print-error-handler-crash.md`
- Code: `src/deia/cli_utils.py`
- Tests: `tests/unit/test_cli_utils.py`

---

**This demonstrates Bug Fix Lookup Protocol working as designed.**

**AGENT-001 awaiting your fix confirmation and 26th-occurrence-prevention report.**
