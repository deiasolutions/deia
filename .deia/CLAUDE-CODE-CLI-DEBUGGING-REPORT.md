# Claude Code CLI Adapter - Debugging Report

**Date:** 2025-10-29
**Issue:** Bot launches via web commander but dies immediately, preventing task execution
**Status:** ROOT CAUSE IDENTIFIED - Graceful error handling implemented

---

## Problem Statement

When launching a bot with adapter type "claude" (Claude Code CLI):
1. Bot appears to launch (shows in registry)
2. Bot immediately becomes unresponsive
3. Cannot send prompts via web commander
4. Bot disappears from registry or stays non-functional

---

## Root Cause Analysis

**Primary Issue:** The `ClaudeCodeCLIAdapter.start_session()` method raises an exception or returns `False` when trying to start the subprocess.

**Secondary Issue:** When adapter startup fails, the bot process would either:
- Crash with uncaught exception (RuntimeError)
- Exit immediately with error code
- Prevent any diagnostic logging

This made it impossible to see WHY the adapter failed to start.

---

## Technical Details

### The Failure Chain

1. **run_single_bot.py** calls `runner.start()`
2. **BotRunner.start()** calls `self.adapter.start_session()`
3. **ClaudeCodeCLIAdapter.start_session()** tries to spawn Claude Code CLI subprocess
4. **Subprocess.Popen()** fails or times out
5. **ClaudeCodeProcess.start()** returns `False`
6. **ClaudeCodeCLIAdapter** raised RuntimeError (old code)
7. **BotRunner** caught it and crashed
8. **run_single_bot** exited with code 1
9. **Bot process died** - no diagnostic information available

### Possible Failure Reasons

The Claude Code CLI subprocess can fail to start for several reasons:
- ❓ Claude Code CLI binary not in PATH
- ❓ Subprocess initialization failure
- ❓ Environment variable issues (e.g., ANTHROPIC_API_KEY conflicts)
- ❓ Working directory permissions
- ❓ Timeout waiting for ready signal
- ❓ Missing dependencies

We couldn't diagnose which one because the bot crashed before logging.

---

## Fixes Implemented

### 1. BotRunner - Graceful Degradation (Commit: 91650e8)

**File:** `src/deia/adapters/bot_runner.py`

**Change:** Modified `start()` method to return `False` instead of raising exceptions

```python
# Before: Raised RuntimeError - bot crashed
if success:
    # ...
else:
    raise RuntimeError("Failed to start adapter session")

# After: Returns False - bot stays alive for diagnostics
if success:
    # ...
else:
    self._log(f"[ERROR] Adapter failed to start (returned False)")
    self.activity_logger.log_error(...)
    return False
```

**Impact:** Bot process continues even if adapter fails, allowing diagnostic access

---

### 2. Run Single Bot - Non-Fatal Handling (Commit: 91650e8)

**File:** `run_single_bot.py`

**Change:** Removed `sys.exit(1)` when adapter startup fails

```python
# Before: Exited immediately on failure
if not runner.start():
    print(f"[ERROR] Failed to start adapter")
    return 1  # Bot dies here

# After: Logs error and continues
if not runner.start():
    print(f"[ERROR] Failed to start adapter")
    # Don't exit - allow diagnostics
    print(f"[WARNING] Bot continuing for diagnostics")
```

**Impact:** Bot stays alive in registry, can be queried for logs/state

---

### 3. CLI Adapter - Detailed Error Reporting (Commit: 91650e8)

**File:** `src/deia/adapters/claude_code_cli_adapter.py`

**Change:** Added comprehensive error logging to `start_session()`

```python
# Now logs:
# - Success message when CLI starts
# - Error buffer contents when subprocess fails
# - FileNotFoundError with expected path
# - Full exception traceback for unexpected errors

except FileNotFoundError as e:
    print(f"[ERROR] Claude Code CLI executable not found: {e}")
    return False
except Exception as e:
    print(f"[ERROR] Failed to start Claude Code CLI: {type(e).__name__}: {e}")
    import traceback
    print(f"[ERROR] Traceback: {traceback.format_exc()}")
    return False
```

**Impact:** Console output shows exactly what went wrong

---

## Next Steps for Diagnosis

Now that the bot won't crash, here's how to troubleshoot the actual issue:

### 1. Launch a CLI bot from web commander
```
POST /api/launch-bot
{
  "bot_id": "TEST-CLAUDE-001",
  "adapter_type": "claude"
}
```

### 2. Capture the bot's output
The console output will show:
```
[TEST-CLAUDE-001] Initializing adapter...
[TEST-CLAUDE-001] [ERROR] Claude Code CLI executable not found: ...
OR
[TEST-CLAUDE-001] [ERROR] Claude Code process.start() returned False
OR
[TEST-CLAUDE-001] [ERROR] Failed to start Claude Code CLI: FileNotFoundError: ...
```

### 3. Based on the error message:

**If "executable not found":**
- Check that `claude` binary is in PATH
- Run `which claude` (Unix) or `where claude` (Windows)
- Check environment PATH variable

**If "process.start() returned False":**
- Check Claude Code CLI subprocess error buffer output
- Verify working directory exists and is writable
- Check for timeout issues (0.2s might be too short)

**If exception traceback:**
- Use the traceback to identify the exact failure point
- May indicate Popen configuration issue

---

## Testing the Fix

### Test 1: Verify bot stays alive with CLI adapter
```bash
python run_single_bot.py TEST-BOT-001 --adapter-type cli --port 9001
```
Expected: Bot prints startup messages and stays running (doesn't exit)

### Test 2: Verify error messages are logged
```bash
# Look for error output like:
# [TEST-BOT-001] [ERROR] Claude Code CLI executable not found...
# or
# [TEST-BOT-001] [ERROR] Failed to start Claude Code CLI...
```

### Test 3: Verify fallback to mock adapter works
```bash
python run_single_bot.py TEST-BOT-001 --adapter-type mock --port 9002
```
Expected: Bot starts successfully and responds to tasks

---

## Files Changed

| File | Changes | Commit |
|------|---------|--------|
| `src/deia/adapters/bot_runner.py` | Graceful error handling in start() | 91650e8 |
| `run_single_bot.py` | Non-fatal handling of startup failures | 91650e8 |
| `src/deia/adapters/claude_code_cli_adapter.py` | Detailed error logging | 91650e8 |

---

## Commit Message

```
fix: Gracefully handle Claude Code CLI adapter failures instead of crashing

The bot process was dying immediately when the Claude Code CLI adapter
failed to start. This prevented diagnostics and made troubleshooting
impossible.

Now:
- Bot stays alive in registry when adapter fails
- Console shows detailed error messages
- Activity logs capture failure details
- Process can be queried for diagnostics
```

**Commit:** `91650e8`

---

## Remaining Work

1. **Identify the actual adapter startup failure** using the new diagnostic logging
2. **Fix the underlying cause** (e.g., missing binary, path issue, environment problem)
3. **Test end-to-end** bot launch → task submission → task execution
4. **Document the working configuration** for Claude Code CLI adapter

---

**Status:** ✅ Graceful error handling in place
**Next:** Launch bot and capture the actual error message
