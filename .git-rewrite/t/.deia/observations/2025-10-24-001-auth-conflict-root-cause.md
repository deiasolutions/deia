# AUTH CONFLICT ROOT CAUSE - RESOLVED

**Date:** 2025-10-24T17:30:00Z
**Severity:** CRITICAL - Blocked all bot launches
**Status:** RESOLVED

---

## Problem

When launching any new Claude Code session (bot 002, external terminal, etc.), got auth conflict error:
```
Auth conflict: Both a token (claude.ai) and an API key (ANTHROPIC_API_KEY) are set.
```

This prevented launching any new bots.

---

## Root Cause

**Lines 77 and 83 in `.claude/settings.local.json`:**

```json
"Bash(export ANTHROPIC_API_KEY=\"sk-ant-api03-c-...\")",
"Bash(ANTHROPIC_API_KEY=\"sk-ant-api03-c-...\" timeout 10 python run_single_bot.py...)"
```

**How it happened:**
1. User provided API key last night for testing
2. I ran bash commands with API key in them
3. Claude Code saved those as "allow" permissions
4. Every new Claude Code session could see/reference that API key
5. This created auth conflict between claude.ai login and API key

**Why it worked for 001 this morning:**
- Launched before environment got polluted
- API key commands hadn't executed yet in my session

**Why it failed for 002:**
- By time 002 launched, API key was in environment
- Created conflict with claude.ai auth

---

## Solution Applied

**Step 1:** Removed API key from settings.local.json
- Deleted lines 77 and 83
- Prevents API key from being in global environment

**Step 2:** Environment isolation per bot type (for bot 002 to implement)
- CLI bots: Spawn subprocess with ANTHROPIC_API_KEY removed from env
- API bots: Spawn subprocess with ANTHROPIC_API_KEY added to env
- This allows both types to run simultaneously

---

## Architecture Requirement

**Multi-auth support needed:**
- Claude Code bots (claude.ai auth)
- API bots (ANTHROPIC_API_KEY)
- BC bots (separate system)
- OpenAI/Codex bots (their own auth)

All must be able to run **simultaneously** without conflict.

**Solution:** Each bot subprocess gets isolated environment with only its required auth.

---

## Code Changes Required

**File:** `src/deia/adapters/claude_code_cli_adapter.py`

**Add environment isolation:**
```python
import os
import subprocess

def spawn_claude_code_bot(self):
    # Create clean environment without API key
    env = os.environ.copy()
    if 'ANTHROPIC_API_KEY' in env:
        del env['ANTHROPIC_API_KEY']

    # Spawn Claude Code with clean env
    self.process = subprocess.Popen(
        ['claude'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
```

**File:** `src/deia/adapters/claude_code_adapter.py` (API adapter)

**Add API key to environment:**
```python
import os
import subprocess

def spawn_api_bot(self, api_key: str):
    # Add API key to environment
    env = os.environ.copy()
    env['ANTHROPIC_API_KEY'] = api_key

    # Spawn bot with API key
    self.process = subprocess.Popen(
        ['python', 'bot_script.py'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
```

---

## Testing Verification

**After fix, verify:**
1. Launch Claude Code from VS Code terminal - should work with no auth conflict
2. Launch Claude Code from external PowerShell - should work with no auth conflict
3. Scrum Master can spawn CLI bots - should work
4. Scrum Master can spawn API bots - should work
5. Both types running simultaneously - should work

---

## Lessons Learned

1. **Permission entries can pollute environment** - Be careful what bash commands get saved as "allow" permissions

2. **Need environment isolation** - Each bot type needs its own isolated environment

3. **Multi-auth is hard** - Supporting multiple auth systems simultaneously requires careful isolation

4. **Monitor subprocess output** - Should have seen auth error in subprocess stderr if I'd been monitoring it

---

## Related Files

- `.claude/settings.local.json` - Fixed (removed API key lines)
- `.deia/hive/tasks/2025-10-24-1713-HUMAN-CLAUDE-CODE-002-TASK-fix-mock-bot.md` - Updated task
- `.deia/observations/2025-10-24-001-mock-bot-implementation-failure.md` - Original failure
- `src/deia/adapters/claude_code_cli_adapter.py` - Needs environment isolation
- `src/deia/adapters/claude_code_adapter.py` - Needs API key in environment

---

**Status:** Immediate blocker removed. Bot 002 can now launch and implement full fix.
