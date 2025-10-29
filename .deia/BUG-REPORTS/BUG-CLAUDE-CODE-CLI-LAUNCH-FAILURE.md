# BUG: Claude Code CLI Bot Launch Failure in Web Commander

**Bug ID:** BUG-CLAUDE-CODE-CLI-LAUNCH-001
**Severity:** P1 - Blocker
**Status:** OPEN
**Discovered:** 2025-10-28 19:55 UTC
**Component:** Web Commander / Bot Launcher
**Related:** Chat Interface App (`src/deia/services/chat_interface_app.py`)

## Problem Statement

The web commander can successfully launch Llama bots but fails to launch Claude Code CLI bots. The adapter mapping is correct (`claude-code` → `adapter_type="cli"`), but the bot process fails to start.

## Root Cause

**PATH RESOLUTION ERROR in `spawn_bot_process()` function**

**File:** `src/deia/services/chat_interface_app.py` (line ~133)

```python
project_root = Path(__file__).parent.parent.parent
script_path = project_root / "run_single_bot.py"
```

**Issue:** The path calculation is incorrect.

- `chat_interface_app.py` location: `src/deia/services/chat_interface_app.py`
- `.parent` = `src/deia/services/`
- `.parent.parent` = `src/deia/`
- `.parent.parent.parent` = `src/`  ← **WRONG - stops here**
- Should be: `src/deia/services/` → `deia/` → `src/` → **`deiasolutions/` (project root)**

**Current behavior:** Looking for `src/run_single_bot.py` (does not exist)
**Expected behavior:** Should look for `deiasolutions/run_single_bot.py` (correct location)

**Verification:**
```python
python3 -c "
from pathlib import Path
services_file = Path('/c/Users/davee/OneDrive/Documents/GitHub/deiasolutions/src/deia/services/chat_interface_app.py')
project_root = services_file.parent.parent.parent
script_path = project_root / 'run_single_bot.py'
print(f'Script path: {script_path}')
print(f'Script exists: {script_path.exists()}')  # Returns False
"
```

## Impact

- Web commander cannot launch Claude Code CLI bots via `/api/bot/launch` endpoint
- Llama bots work fine (different code path)
- Blocks integration of Claude Code CLI with web-based bot management

## Fix Required

Change line 133 in `chat_interface_app.py`:

**Current:**
```python
project_root = Path(__file__).parent.parent.parent
```

**Should be:**
```python
project_root = Path(__file__).parent.parent.parent.parent
```

Or more robustly, find `run_single_bot.py` by searching upward or using:
```python
project_root = Path(__file__).parents[3]  # Go up 4 levels from services/
```

## Testing Steps After Fix

1. Start web commander
2. POST to `/api/bot/launch` with `{"bot_id": "TEST-CC-001", "bot_type": "claude-code"}`
3. Verify bot spawns successfully (check process PID returned)
4. Verify `run_single_bot.py` is executed with correct arguments: `python run_single_bot.py TEST-CC-001 --adapter-type cli`

## Related Code

- **Adapter mapping (correct):** Line 749-756 in `chat_interface_app.py`
  - Maps `"claude-code"` → `adapter_type="cli"` ✅

- **spawn_bot_process() function:** Lines 128-195 in `chat_interface_app.py`
  - Receives correct `adapter_type="cli"` ✅
  - But fails to locate `run_single_bot.py` ❌

- **launch_bot() endpoint:** Lines 694-793 in `chat_interface_app.py`
  - Calls `spawn_bot_process()` correctly ✅
  - Returns success/failure appropriately ✅

## Notes

- Llama bots work because they may use a different initialization path or skip the script execution
- Mock adapter may also bypass this path issue
- This is a simple fix - just need to adjust the parent path count

