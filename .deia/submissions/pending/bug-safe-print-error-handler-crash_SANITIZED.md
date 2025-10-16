---
type: bug
project: deiasolutions
created: 2025-10-09
status: pending
sanitized: true
category: cli
severity: high
reporter: davee
---

# Bug: safe_print() Error Handler Crashes with Unicode

## Problem

The `safe_print()` function was created to fix Unicode crashes on Windows terminals, but **the error handler itself crashes** when trying to print error messages.

This is a bug in the bug fix! 🐛🐛

## Current Behavior

1. `safe_print()` tries to print Unicode (e.g., "✓ Success")
2. Windows terminal raises `UnicodeEncodeError`
3. Fallback replaces Unicode → ASCII
4. Fallback tries to print with Rich markup: `[red]Error printing message:[/red]`
5. **Rich markup also has Unicode issues on Windows**
6. Second `UnicodeEncodeError` occurs
7. **Entire CLI crashes**

## Expected Behavior

- Error handler should NEVER crash
- Should use plain text (no Rich markup) in error messages
- Should gracefully degrade to basic printing

## Root Cause

**File:** `src/deia/cli_utils.py:63`
```python
except Exception as e:
    # This line crashes because [red] markup can also cause Unicode issues!
    console.print(f"[red]Error printing message:[/red] {e}")
    return False
```

## Stack Trace

```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2713' in position 0
  File "src/deia/cli_utils.py", line 47, in safe_print
    console.print(message, **kwargs)

During handling of the above exception, another exception occurred:
  File "src/deia/cli_utils.py", line 59, in safe_print
    console.print(fallback_message, **kwargs)

During handling of the above exception, another exception occurred:
  File "src/deia/cli_utils.py", line 63, in safe_print
    console.print(f"[red]Error printing message:[/red] {e}")  # <- THIS CRASHES
```

## Impact

- **CLI Unusable:** Commands crash instead of showing output
- **Defeats Purpose:** The fix makes things worse
- **User Frustration:** Can't use DEIA on Windows at all

## Reproduction

1. Windows terminal with cp1252 encoding
2. Run: `python -m deia.cli config set auto_log false`
3. CLI attempts to print: "✓ Set auto_log = false"
4. **Crash occurs**

## Environment

- OS: Windows 11
- Python: 3.13
- Terminal: cmd.exe (cp1252 encoding)
- DEIA: v0.1.0

## Suggested Fix

**Use plain print() for error messages (no Rich):**

```python
def safe_print(console: Console, message: str, **kwargs) -> bool:
    """
    Print message to console with Unicode fallback for Windows terminals
    """
    try:
        # First attempt: print as-is (works on UTF-8 terminals)
        console.print(message, **kwargs)
        return True

    except UnicodeEncodeError:
        # Fallback: replace Unicode symbols with ASCII
        fallback_message = message

        for unicode_char, ascii_replacement in UNICODE_FALLBACKS.items():
            fallback_message = fallback_message.replace(unicode_char, ascii_replacement)

        # Retry with ASCII-safe message
        try:
            console.print(fallback_message, **kwargs)
            return True
        except UnicodeEncodeError:
            # Last resort: plain print (no Rich, no Unicode)
            import sys
            plain_message = fallback_message
            # Strip Rich markup tags
            import re
            plain_message = re.sub(r'\[/?[^\]]+\]', '', plain_message)
            print(plain_message, file=sys.stderr)
            return False

    except Exception as e:
        # Catch any other errors - use plain print!
        import sys
        print(f"Error printing message: {e}", file=sys.stderr)
        return False
```

## Alternative Fix

**Create a completely safe fallback function:**

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

## Tests Affected

The existing tests pass because they use mocks and don't test the actual error path on Windows terminals.

**Need to add:**
```python
def test_safe_print_error_handler_doesnt_crash():
    """Test error handler itself is safe"""
    # Mock console that always fails
    console = MagicMock()
    console.print.side_effect = UnicodeEncodeError('charmap', '', 0, 1, 'error')

    # Should NOT crash
    result = safe_print(console, "Test message")

    # Should return False but not raise
    assert result is False
```

## Priority

**P1 - High**
- Breaks CLI on Windows
- Defeats purpose of Unicode fix
- Affects all Windows users
- Easy to fix (known solution)

## Acceptance Criteria

- [ ] Error handler never crashes
- [ ] Falls back to plain print() when Rich fails
- [ ] Strips Rich markup in final fallback
- [ ] Works on Windows cp1252 terminals
- [ ] Test added for error handler safety
- [ ] All existing tests still pass

---

**Submitted via:** DEIA official bug submission process
**Next Steps:** Triage → Prioritize → Fix immediately (P1)
