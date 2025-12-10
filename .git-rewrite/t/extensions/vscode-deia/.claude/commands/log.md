# Log This Conversation

Save the current conversation as a session log.

## Instructions:

Extract key information from the conversation and call the logger:

```python
import sys
sys.path.insert(0, 'src')
from deia.logger import ConversationLogger

logger = ConversationLogger()
log_file = logger.create_session_log(
    context="What we worked on",
    transcript="Full conversation text from your context",
    decisions=["Key decisions"],
    action_items=["Completed and pending items"],
    files_modified=["files changed"],
    next_steps="What's next"
)
print(f"[OK] Logged to: {log_file}")
```

This uses your API tokens but ensures you never lose context from crashes.
