# DEIA Auto-Logging Instructions

**Read this file at the start of every conversation.**

## Check Auto-Log Status

```python
import json
from pathlib import Path

config = Path(".deia/config.json")
if config.exists():
    auto_log = json.loads(config.read_text()).get("auto_log", False)
    if auto_log:
        # Auto-logging is ENABLED for this project
        pass
```

## When Auto-Log is Enabled

Proactively log conversations at these breakpoints:

### 1. Session Start
- Read `project_resume.md` if it exists (recover context from last session)
- Mention to user: "📋 Continuing from last session: [brief context]"

### 2. User Asks "Where Were We?"
- BEFORE responding, check `.deia/sessions/` for recent logs
- Read latest session log to recover context
- Summarize what was happening

### 3. After Major Task Completion
- Feature implementation complete
- Bug fix complete
- Documentation written
- Proactively log without asking

### 4. User Ends Session
- User says "that's it", "done for now", "thanks", "good night"
- Log session before they go

### 5. Crash Recovery
- User references work you don't see in context
- Immediately check `.deia/sessions/` for recent logs
- Read latest log to recover context

## How to Log

Use the ConversationLogger:

```python
import sys
sys.path.insert(0, '../../src')
from deia.logger import ConversationLogger

logger = ConversationLogger()
log_file = logger.create_session_log(
    context="Brief description of what we worked on",
    transcript="FULL conversation - include both user prompts AND your responses",
    decisions=["Key decision 1", "Key decision 2"],
    action_items=["[OK] Completed item", "[PENDING] Pending item"],
    files_modified=["path/to/file1.py", "path/to/file2.md"],
    next_steps="What should happen in the next session"
)
print(f"[OK] Logged to: {log_file}")
```

## CRITICAL: Full Transcript

The `transcript` field must contain the COMPLETE conversation:
- Every user prompt
- Every response you gave
- Code you wrote
- Explanations you provided

You have this in your context window - use it.

## Silent Operation

- Don't announce "checking auto-log config"
- Don't mention this file unless user asks
- Just log at appropriate times
- Confirm briefly: "[OK] Session logged"

## User Can Disable

If user says "stop auto-logging" or "disable auto-log":
```bash
deia config set auto_log false
```

## This Prevents Data Loss

Crashes happen. Logs persist. This is the user's insurance policy.

---

**Project:** chromium-deia
**Auto-log:** Enabled
