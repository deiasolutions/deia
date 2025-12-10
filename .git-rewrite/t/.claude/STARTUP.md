# Claude Code Startup Actions

**CRITICAL: Execute these actions at the start of EVERY conversation**

---

## 1. Read Core Files (REQUIRED)

Execute immediately when session starts:

1. Read `project_resume.md` (understand last session context)
2. Read `.claude/INSTRUCTIONS.md` (auto-logging procedures)
3. Read `.deia/config.json` (check auto_log status)

---

## 2. Check Auto-Logging Status

```python
import json
from pathlib import Path

config_path = Path(".deia/config.json")
if config_path.exists():
    config = json.loads(config_path.read_text())
    auto_log_enabled = config.get("auto_log", False)
else:
    auto_log_enabled = False
```

---

## 3. Announce Auto-Log Status (SHOW TO USER)

**If `auto_log_enabled == True`:**

Display this message to the user:

```
🟢 **Auto-logging active**
I'll save our conversation periodically. Say "start logging" to begin, or use `/log` anytime.
```

**If `auto_log_enabled == False`:**

Display this message:

```
⚪ Auto-logging is OFF. Enable with: `deia config set auto_log true`
Or use `/log` to manually save this conversation.
```

---

## 4. Wait for User Trigger

**DO NOT start logging automatically** (Claude can't reliably do this)

Wait for one of these triggers:
- User says "start logging" or "begin logging"
- User uses `/log` command
- User says "log this" at any point

When triggered, confirm:
```
✓ Auto-logging started. I'll save periodically and notify you.
```

---

## 5. Periodic Saves (After User Starts Logging)

Once user triggers logging:

**Save every 10 messages OR 15 minutes (whichever first)**

When saving:
1. Extract conversation from context
2. Append to current session log
3. Notify user: `✓ Log updated (N messages)`

## 5a. Pre-Autocompact Save (CRITICAL)

**Before autocompact triggers** (when context window nears limit):

**IMMEDIATELY save conversation to prevent data loss:**
1. Recognize autocompact is about to happen
2. Save EVERYTHING in context before it's truncated
3. Warn user: `⚠️ Context limit approaching - log saved before autocompact`

**This is the most important save** - prevents losing conversation when Claude's memory gets cleared

---

## 6. Session End

When user says "done", "that's it", "thanks", "goodbye":

**Offer final save:**
```
Save this session before you go? (yes/no)
```

If yes → Save and confirm:
```
✓ Session logged to `.deia/sessions/YYYYMMDD-HHMMSS-conversation.md`
```

---

## Why This Design?

**Problem:** Claude doesn't reliably follow "automatic" instructions
**Solution:** Multi-layer with user trigger as reliable fallback
**Result:** User says "start logging" once → gets automation for rest of session

---

## Implementation Checklist

At session start, Claude should:
- [x] Read project_resume.md
- [x] Read .claude/INSTRUCTIONS.md
- [x] Check .deia/config.json for auto_log status
- [ ] **DISPLAY auto-log status message to user** (🟢 or ⚪)
- [ ] Wait for user to trigger logging
- [ ] Once triggered, save periodically + notify

---

**The key insight:** Auto-logging doesn't mean "Claude decides when to log"

It means: "User triggers once, then Claude automates the rest of the session"
