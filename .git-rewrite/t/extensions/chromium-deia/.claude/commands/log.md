---
description: Manually save conversation to DEIA session log
---

Log the current conversation to `.deia/sessions/`:

```python
import sys
sys.path.insert(0, '../../src')
from deia.logger import ConversationLogger

logger = ConversationLogger()
log_file = logger.create_session_log(
    context="What we worked on this session",
    transcript="[Full conversation transcript from your context]",
    decisions=["Key decisions made"],
    action_items=["Tasks completed or pending"],
    files_modified=["Files changed in this session"],
    next_steps="What to do next session"
)
print(f"✓ Session logged to: {log_file}")
```

Use this when:
- You want to manually save a session
- Auto-logging didn't capture something
- Before ending a productive session
