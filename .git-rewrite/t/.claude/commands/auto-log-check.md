# Auto-Log Check (Internal - runs on startup)

**DO NOT show this to the user unless there's an error.**

## Check if auto-logging is enabled

```python
import json
from pathlib import Path

config_path = Path(".deia/config.json")
if not config_path.exists():
    exit(0)  # No config, no auto-log

config = json.loads(config_path.read_text())
auto_log = config.get("auto_log", False)

if auto_log:
    print("DEIA_AUTO_LOG_ENABLED")
else:
    exit(0)
```

## If auto_log is enabled:

You should proactively log conversations at these breakpoints:

1. **User asks "where were we"** - BEFORE responding, check for recent session log. If none exists or is old, suggest logging the previous session from memory.

2. **Major task completion** - When you finish a significant piece of work (feature implementation, bug fix, documentation), proactively offer to log.

3. **End of session** - If user says "that's it for now" or similar, offer to log before they close.

4. **On crash recovery** - If context seems lost (user references work you don't see), immediately check session logs and offer to log current state.

## How to log:

Use the same method as `/log` command:

```python
from deia.logger import ConversationLogger

logger = ConversationLogger()
log_file = logger.create_session_log(
    context="Brief description",
    transcript="Full conversation from your context",
    decisions=["Key decisions"],
    action_items=["Completed and pending items"],
    files_modified=["files changed"],
    next_steps="What's next"
)
```

## Silent operation:

- Don't announce "checking auto-log config"
- Don't mention this file
- Just log when appropriate
- Confirm after logging: "✓ Session logged to .deia/sessions/[timestamp].md"
