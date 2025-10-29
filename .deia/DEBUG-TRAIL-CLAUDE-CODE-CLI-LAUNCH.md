# DEBUG TRAIL: Claude Code CLI Bot Launch Failure

**Session Date:** 2025-10-28
**Session Time:** 19:55 - 20:20 UTC
**Investigator:** Claude Code (Haiku 4.5)
**Status:** IN PROGRESS - One fix applied, needs end-to-end testing

---

## INVESTIGATION SUMMARY

**User Report:** "Commander can't launch Claude Code, but can launch Llama. Focus on Claude Code CLI. It's only half broken."

**Investigation Duration:** ~25 minutes
**Findings:** 1 critical bug identified and fixed
**Remaining:** End-to-end testing needed

---

## FINDINGS LOG

### Finding #1: Path Resolution Bug in Web Commander [FIXED]

**Severity:** P1 Blocker
**Discovered:** 2025-10-28 20:05 UTC
**File:** `src/deia/services/chat_interface_app.py`
**Line:** 132
**Function:** `spawn_bot_process(bot_id: str, adapter_type: str = "api") -> Optional[int]`

#### The Problem

When web commander tries to launch Claude Code CLI bots, it fails to find `run_single_bot.py`:

```
logger.error(f"run_single_bot.py not found at {script_path}")
return None
```

#### Root Cause Analysis

Path traversal calculation was off by one level:

```python
# BEFORE (WRONG - Line 132)
project_root = Path(__file__).parent.parent.parent  # Only 3 levels up
# Result: Points to src/ instead of deiasolutions/
# Script path: src/run_single_bot.py ❌ (does not exist)

# AFTER (CORRECT - Line 132)
project_root = Path(__file__).parent.parent.parent.parent  # 4 levels up
# Result: Points to deiasolutions/ (project root)
# Script path: deiasolutions/run_single_bot.py ✅ (exists)
```

**Path Breakdown:**
- `chat_interface_app.py` location: `deiasolutions/src/deia/services/chat_interface_app.py`
- Level 1 (`.parent`): `deiasolutions/src/deia/services/`
- Level 2 (`.parent.parent`): `deiasolutions/src/deia/`
- Level 3 (`.parent.parent.parent`): `deiasolutions/src/` ← **STOPPED HERE (WRONG)**
- Level 4 (`.parent.parent.parent.parent`): `deiasolutions/` ← **CORRECT**

#### Verification

**Before fix:**
```python
from pathlib import Path
services_file = Path('C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions/src/deia/services/chat_interface_app.py')
project_root = services_file.parent.parent.parent
script_path = project_root / 'run_single_bot.py'
print(script_path)  # C:\Users\davee\...\deiasolutions\src\run_single_bot.py
print(script_path.exists())  # False ❌
```

**After fix:**
```python
from pathlib import Path
services_file = Path('C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions/src/deia/services/chat_interface_app.py')
project_root = services_file.parent.parent.parent.parent
script_path = project_root / 'run_single_bot.py'
print(script_path)  # C:\Users\davee\...\deiasolutions\run_single_bot.py
print(script_path.exists())  # True ✅
```

#### Fix Applied

**Date:** 2025-10-28 20:15 UTC
**Command:** `sed` replacement in bash
**Change:** Line 132, added one `.parent`

```bash
sed -i 's/project_root = Path(__file__).parent.parent.parent  # From src\/deia\/services\/ to root/project_root = Path(__file__).parent.parent.parent.parent  # From src\/deia\/services\/ to project root/' src/deia/services/chat_interface_app.py
```

**Verification after fix:**
```
132:        project_root = Path(__file__).parent.parent.parent.parent  # From src/deia/services/ to project root
```
✅ Confirmed

---

## NEXT INVESTIGATION STEPS

### Still Need to Verify

1. **Is there a second bug?** After fixing the path, does Claude Code actually launch?
   - Need to: Test bot spawn, check process creation, verify adapter initialization
   - Likely issues: Claude CLI might not be in PATH, adapter startup might fail, etc.

2. **Why didn't anyone catch this?**
   - The error logging goes to `.deia/bot-logs/` - need to check those files
   - Llama adapter might use different code path that doesn't have this bug

3. **Are there similar path bugs elsewhere?**
   - Search for other `.parent.parent.parent` patterns in codebase
   - Check other bot launchers for similar issues

### Test Plan

```bash
# 1. Start web commander (if not running)
python -m uvicorn src.deia.services.chat_interface_app:app --port 8000

# 2. Test Claude Code launch
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id": "TEST-CLAUDE-CODE-001", "bot_type": "claude-code"}'

# 3. Check bot health
curl http://localhost:8000/api/bot/TEST-CLAUDE-CODE-001/status

# 4. Review error logs if still failing
tail -50 .deia/bot-logs/TEST-CLAUDE-CODE-001-errors.jsonl
```

---

## CODE CONTEXT

### Why This Bug Existed

The adapter mapping is correct:
```python
# Line 749-756 in chat_interface_app.py
adapter_type_map = {
    "claude": "mock",
    "chatgpt": "mock",
    "claude-code": "cli",      # ✅ Correct
    "codex": "cli",            # ✅ Correct
    "llama": "api"             # ✅ Correct
}
```

The spawn function receives the right adapter type:
```python
# Line 768
adapter_type = adapter_type_map.get(bot_type, "mock")
pid = spawn_bot_process(bot_id, adapter_type)  # ✅ Passes "cli" for claude-code
```

But it fails to find the script to run:
```python
# Line 132 (BEFORE FIX)
project_root = Path(__file__).parent.parent.parent  # ❌ Off by one
```

### Why Llama Works

Llama uses `adapter_type="api"` which might:
- Use a different code path
- Have different initialization
- Or possibly has its own path resolution that's correct

Need to verify: Does Llama actually work or is it just not being tested?

---

## COOKIE TRAIL FOR NEXT SESSION

**If Claude Code still doesn't launch after this fix:**

1. Check `run_single_bot.py` execution:
   ```bash
   python run_single_bot.py TEST-001 --adapter-type cli
   ```
   - Does it start without errors?
   - Can it find ClaudeCodeCLIAdapter?

2. Check Claude CLI availability:
   ```bash
   which claude
   claude --version
   ```
   - Is Claude CLI installed?
   - Is it in PATH?

3. Check adapter initialization:
   - File: `src/deia/adapters/claude_code_cli_adapter.py`
   - Check `ClaudeCodeProcess.start()` method
   - Verify subprocess creation works

4. Check error logs in this order:
   - `.deia/bot-logs/TEST-CLAUDE-CODE-001-errors.jsonl`
   - `.deia/bot-logs/TEST-CLAUDE-CODE-001-activity.jsonl`
   - Check for "Claude CLI process exited immediately after spawn"

---

## FILES MODIFIED

| File | Line | Change |
|------|------|--------|
| `src/deia/services/chat_interface_app.py` | 132 | Added `.parent` to path traversal (3→4 levels) |

**Git Status After Fix:**
```
M src/deia/services/chat_interface_app.py
```

---

## QUICK REFERENCE

**Problem:** Web commander can't launch Claude Code CLI bots
**Cause:** Path resolution off by 1 level
**Fix:** `Path(__file__).parent.parent.parent` → `Path(__file__).parent.parent.parent.parent`
**File:** `src/deia/services/chat_interface_app.py:132`
**Status:** Fixed, pending end-to-end test

