# DEIA Integration Guide for Claude Code

**How to make Claude Code aware of DEIA and enable auto-logging**

---

## The Two-Tier Approach

### Tier 1: # Memory (Automatic - Preferred)

Create a `# deia` memory in Claude Code that tells it about DEIA on startup.

**Already done:** `.claude/preferences/deia.md` exists in this repo.

**To use it:**
1. In Claude Code, type: `# deia`
2. Claude will remember DEIA behavior for future sessions
3. Auto-logging will work as configured

### Tier 2: Manual Fallback

If # memory isn't working, use manual commands:

**Start of session:**
```
Read project_resume.md to catch up on context
```

**End of session:**
```
Log this chat using ConversationLogger
```

---

## How Auto-Logging Works

When `auto_log: true` in `.deia/config.json`:

### Real-Time Logging (During Session)

Claude should call `logger.log_step()` after each significant action:

```python
from deia.logger import ConversationLogger
logger = ConversationLogger()

# After each meaningful step
logger.log_step(
    action="Created authentication system",
    files_modified=["src/auth.py", "src/middleware.py"],
    decision="Using JWT instead of sessions for scalability",
    next_step="Add rate limiting"
)
```

This creates:
- `.deia/sessions/YYYYMMDD-HHMMSS-realtime.md` (detailed step-by-step log)
- Updates `project_resume.md` in real-time with each step

### End-of-Session Logging

At the end of the conversation, create a comprehensive log:

```python
logger.create_session_log(
    context="Built authentication system",
    transcript="[full conversation text]",
    decisions=["JWT for auth", "Redis for sessions", "2FA required"],
    action_items=["Add rate limiting", "Write tests", "Deploy to staging"],
    files_modified=["src/auth.py", "src/middleware.py", "tests/test_auth.py"],
    next_steps="Test in staging, then add OAuth providers"
)
```

---

## File Structure

```
project/
├── .deia/
│   ├── config.json          # { "auto_log": true, "project": "name" }
│   └── sessions/
│       ├── INDEX.md
│       ├── 20251007-143022-realtime.md    # Real-time step logging
│       └── 20251007-143022-conversation.md # Full session log
├── project_resume.md        # Auto-updated, Claude reads on startup
└── .claude/
    └── preferences/
        └── deia.md          # Tells Claude about DEIA (for # memory)
```

---

## Setup Steps

### 1. Install DEIA

```bash
cd /path/to/your/project
pip install -e /path/to/deia/repo
```

### 2. Initialize Project

```bash
deia init
```

This creates:
- `.deia/config.json`
- `.deia/sessions/` directory
- `project_resume.md` (if doesn't exist)

### 3. Enable Auto-Logging

Edit `.deia/config.json`:
```json
{
  "auto_log": true,
  "project": "your-project-name",
  "user": "your-name"
}
```

### 4. Set Up # Memory

In Claude Code:
1. Type `# deia`
2. Claude will read `.claude/preferences/deia.md`
3. Future sessions will remember DEIA behavior

---

## Verification

### Check if it's working:

**Start a Claude Code session and Claude should:**
1. Mention it's checking for DEIA
2. Read `project_resume.md` automatically
3. Start logging steps as you work

**If not working:**
- Check `.deia/config.json` exists and `auto_log: true`
- Verify DEIA is installed: `pip show deia`
- Manually tell Claude: "Read .claude/preferences/deia.md"
- Fall back to manual logging

---

## Real-Time vs End-of-Session

**Real-time logging (`log_step`):**
- ✅ Captures progress as you go
- ✅ Survives crashes (partial work saved)
- ✅ Updates project_resume.md live
- ⚠️ More verbose, multiple small logs

**End-of-session logging (`create_session_log`):**
- ✅ Clean, comprehensive summary
- ✅ Full conversation transcript
- ✅ All decisions and files in one place
- ⚠️ Lost if Claude crashes before logging

**Best practice:** Use both
- Real-time logging during the session
- Comprehensive log at the end

---

## Troubleshooting

### Claude doesn't auto-log

1. Check `.deia/config.json` has `"auto_log": true`
2. Verify DEIA installed: `python -c "from deia.logger import ConversationLogger"`
3. Try # memory: Type `# deia` in Claude
4. Manual fallback: Tell Claude "log_step after each action"

### Import errors

```python
# If this fails:
from deia.logger import ConversationLogger

# Try this workaround:
import sys
sys.path.insert(0, 'src')
from deia.logger import ConversationLogger
```

Or install DEIA properly:
```bash
pip install -e /path/to/deia
```

### project_resume.md not updating

- Check file permissions
- Verify `.deia/sessions/` directory exists
- Check for errors in real-time log file

---

## Example Session

**Start of session:**
```
Claude: I see this is a DEIA-enabled project. Let me read project_resume.md...
Claude: I see we were working on the authentication system. Last session added JWT support.
```

**During session:**
```python
# Claude logs each step automatically
logger.log_step("Added rate limiting middleware", ["src/middleware.py"], "10 req/min per IP")
logger.log_step("Created tests", ["tests/test_rate_limit.py"])
```

**End of session:**
```python
# Claude creates final comprehensive log
logger.create_session_log(
    context="Added rate limiting to API",
    transcript="[full conversation]",
    decisions=["10 req/min", "Redis for state", "429 status code"],
    files_modified=["src/middleware.py", "tests/test_rate_limit.py"],
    next_steps="Deploy to staging and monitor"
)
```

**Result:**
- `.deia/sessions/20251007-143022-realtime.md` has step-by-step log
- `.deia/sessions/20251007-143022-conversation.md` has full summary
- `project_resume.md` is updated with latest state

---

## Benefits

✅ **Never lose context** - Crash recovery in seconds
✅ **Continuous documentation** - Auto-updated as you work
✅ **Knowledge capture** - Every decision logged
✅ **Team sharing** - Others can catch up from logs
✅ **Pattern extraction** - Convert logs to BOK patterns later

---

**For more help:** See [CONTRIBUTING.md](CONTRIBUTING.md) or file an issue.
