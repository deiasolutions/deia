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
        # Auto-logging is ENABLED
        pass
```

## When Auto-Log is Enabled

Proactively log conversations at these breakpoints:

### 1. User Asks "Where Were We?"
- BEFORE responding, check `.deia/sessions/` for recent logs
- If latest log is old or missing, suggest creating one
- Read `project_resume.md` for quick context

### 2. After Major Task Completion
- Feature implementation complete
- Bug fix complete
- Documentation written
- Offer: "✓ Task complete. Log this session?"

### 3. User Ends Session
- User says "that's it", "done for now", "thanks"
- Offer: "Log this session before you go?"

### 4. Crash Recovery
- User references work you don't see in context
- Immediately check `.deia/sessions/` for recent logs
- Read latest log to recover context
- Log current state to prevent future loss

## How to Log

Use the ConversationLogger:

```python
from deia.logger import ConversationLogger

logger = ConversationLogger()
log_file = logger.create_session_log(
    context="Brief description of what we worked on",
    transcript="FULL conversation text from your context - include both user prompts AND your responses",
    decisions=["Key decision 1", "Key decision 2"],
    action_items=["✓ Completed item", "Pending item"],
    files_modified=["path/to/file1.py", "path/to/file2.md"],
    next_steps="What should happen in the next session"
)
print(f"✓ Logged to: {log_file}")
```

## CRITICAL: Full Transcript

The `transcript` field must contain the COMPLETE conversation including:
- Every user prompt
- Every response you gave
- Code you wrote
- Explanations you provided

You have this in your context window - use it.

## Silent Operation

- Don't announce "checking auto-log config"
- Don't mention this file to the user
- Just log at appropriate times
- Confirm after: "✓ Session logged"

## User Can Disable

If user says "stop auto-logging":
```bash
# You can run this for them:
python -c "
import json
from pathlib import Path
config = Path('.deia/config.json')
data = json.loads(config.read_text())
data['auto_log'] = False
config.write_text(json.dumps(data, indent=2))
print('Auto-logging disabled')
"
```

## This Prevents Data Loss

Crashes happen. Logs persist. This is Dave's insurance policy.

---

**⚠️ END OF FILE REMINDER:**

You just read the auto-logging instructions. Do you know:

- When to log? (4 breakpoints listed above)
- How to log? (ConversationLogger code above)
- What auto_log status is right now? (Did you check config?)

**If you can't answer these, re-read this file. Don't proceed until you know.**
