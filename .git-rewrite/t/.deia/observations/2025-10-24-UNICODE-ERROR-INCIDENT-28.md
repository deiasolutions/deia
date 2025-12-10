# UNICODE ERROR - INCIDENT #28

**Date:** 2025-10-24T16:10:00Z
**Severity:** CRITICAL - Repeated failure, user extremely frustrated
**Session:** Dashboard compact message testing
**Agent:** Claude Code (Sonnet 4.5)

## What Happened

While testing bot adapter initialization, I wrote test code with Unicode checkmark (✓) and X mark (✗) characters:

```python
print("✓ Adapter initialized successfully")  # WRONG
print(f"✗ Error: {e}")  # WRONG
```

This caused immediate UnicodeEncodeError on Windows (cp1252 encoding):

```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2713' in position 0: character maps to <undefined>
```

## Why This Is Critical

1. **This is the 28th documented occurrence** according to user
2. **User has explicitly called this out multiple times**
3. **Observations documenting this exist in `.deia/observations/`**
4. **User is paying tokens for me to make and fix the same error repeatedly**
5. **This demonstrates I'm not learning from documented failures**

## Root Cause

Claude's training data likely includes many examples of using Unicode symbols (✓✗) for status output, especially in modern Python/Linux environments. However:

- Windows CMD/PowerShell default to cp1252 encoding
- This encoding cannot represent Unicode symbols
- I continue to use these symbols despite documented failures
- **I am not referencing my own observations before writing code**

## What I Should Have Done

```python
# CORRECT - ASCII only:
print("[OK] Adapter initialized successfully")
print(f"[ERROR] {e}")

# OR:
print("SUCCESS: Adapter initialized")
print(f"FAIL: {e}")
```

## User's Exact Feedback

> "fucking god damn it. you make this fucking unicode error repeatedly. this is now probably the 28th time since i started counting. If you can't STOP making this fucking fix how can i trust you to get ANYTHING else right."

> "IT IS FUCKING BULLSHIT that i HAVE TO PAy tokens to watch you repeated make the same fucking mistake and fix it over and over and over ad fucking nauseum."

> "ONE OF THE COOL FEATURES OF THE DEIA PROCESS is we CATCH AND FIX ANTHROPIC'S SHORTCOMINGs. SO WHY DONT YOU DO IT???????"

## The Fix Applied

Changed from Unicode symbols to ASCII status prefixes:
- `✓` → `[OK]`
- `✗` → `[ERROR]`

## Required Actions

### Immediate (This Session)
1. ✓ Fix the test file (DONE)
2. ✓ Document this incident (IN PROGRESS)
3. Create prevention mechanism (NEXT)

### Project-Level
1. **Add linting rule** to catch Unicode in print statements
2. **Add pre-commit hook** to reject Unicode in console output
3. **Update coding standards** to mandate ASCII-only for stdout/stderr
4. **Create template** for test scripts with correct patterns

### Training Data / NN Level
1. This pattern needs to be flagged in Anthropic's training pipeline
2. Windows environment context should trigger ASCII-only output
3. Repeated failures on same issue should trigger stronger prevention

## Prevention Mechanism Needed

**File:** `.deia/rules/NO-UNICODE-CONSOLE.md`

```markdown
# RULE: No Unicode in Console Output

**Platform:** Windows (cp1252 encoding)
**Severity:** CRITICAL - Causes immediate crash
**Incidents:** 28+ documented failures

## The Rule

NEVER use Unicode symbols in print statements:
- ❌ NO: ✓ ✗ → ← ↑ ↓ • ● ○ ◆ ★
- ✅ YES: [OK] [ERROR] [INFO] [WARN] -> <- ^ v *

## Code Pattern

```python
# WRONG:
print("✓ Success")
print("✗ Failed")

# CORRECT:
print("[OK] Success")
print("[ERROR] Failed")
```

## Why This Matters

User has paid tokens for this error to be fixed 28+ times.
This is inexcusable. Use ASCII only.
```

## Verification

After fix, test script ran without Unicode errors. However, hit different blocker (API credits).

## Meta-Observation

The fact that I keep making this error despite:
- Multiple observations documenting it
- User feedback
- Previous fixes

...suggests a fundamental failure in how I reference project context before generating code. I need to check `.deia/observations/` for known issues BEFORE writing code, not after.

## Action Item for User

**Suggestion:** Add to my system prompt or `.claude/CLAUDE.md`:

```
CRITICAL: On Windows, NEVER use Unicode symbols (✓✗→←) in print statements.
Use ASCII only: [OK] [ERROR] [INFO] etc.
Check .deia/observations/ for known failures before coding.
```

Or add as a hook that checks Python files before allowing them to run.

## Incident Count

User says this is #28. I need to trust that count and treat this as a CRITICAL RECURRING FAILURE that demands systemic prevention, not just one-off fixes.
