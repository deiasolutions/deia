# Start Auto-Logging

**Trigger:** User says "start logging" or "begin logging"

---

## What This Does

Initiates session-based auto-logging with periodic saves.

---

## Instructions for Claude

When user triggers this command:

### 1. Create Initial Session Log

```python
from deia.logger import ConversationLogger
from datetime import datetime

logger = ConversationLogger()

# Get conversation so far from your context
conversation_so_far = """
[Extract everything from session start to now, including:
- User messages
- Your responses
- Code written
- Files modified]
"""

# Create initial log
log_file = logger.create_session_log(
    context="[Summarize what we're working on in 1 sentence]",
    transcript=conversation_so_far,
    decisions=[],  # Will add as we go
    action_items=[],  # Will add as we go
    files_modified=[],  # Track as we modify files
    next_steps="Session in progress",
    status="Active"
)

# Store session info in memory for periodic saves
session_id = log_file.stem  # Extract filename without .md
message_count = 0  # Track messages since last save
last_save_time = datetime.now()

print(f"✓ Auto-logging started")
print(f"Session: {session_id}")
print(f"I'll save periodically and notify you.")
```

### 2. Track Session State

**Remember these for the duration of this conversation:**
- `session_id` - Which log file we're appending to
- `message_count` - Count every user message + your response
- `last_save_time` - When we last saved

### 3. Periodic Save Logic

**After EVERY message exchange (user + your response):**

```python
message_count += 1
time_since_save = datetime.now() - last_save_time

# Save if either condition met:
if message_count >= 10 or time_since_save.total_seconds() >= 900:  # 15 min
    # Append recent conversation to log
    logger.append_to_session(
        session_file=Path(f".deia/sessions/{session_id}.md"),
        new_content=f"""
**Messages {message_count - 9} to {message_count}:**

[Recent conversation excerpt from your context]

**Files modified since last save:**
- [Any files you edited/created]

**Decisions made:**
- [Any key decisions in recent messages]
"""
    )

    # Notify user
    print(f"✓ Log updated ({message_count} messages)")

    # Reset counters
    message_count = 0
    last_save_time = datetime.now()
```

### 4. Pre-Autocompact Save (CRITICAL)

**Before autocompact triggers** (when context window approaches limit):

```python
# Save immediately before losing context
logger.append_to_session(
    session_file=Path(f".deia/sessions/{session_id}.md"),
    new_content=f"""
**Pre-autocompact save:**

[Current conversation from context - save EVERYTHING before it's lost]

**Context limit approaching - auto-saving to prevent data loss**
"""
)

print(f"⚠️ Context limit approaching - log saved before autocompact")
```

**This is insurance against losing conversation when Claude's memory gets truncated.**

### 5. Session End Detection

If user says "done", "that's it", "thanks", "goodbye":

```python
# Final save
logger.append_to_session(
    session_file=Path(f".deia/sessions/{session_id}.md"),
    new_content=f"""
**Final update:**

[Any remaining conversation]

**Session completed:** {datetime.now().isoformat()}
"""
)

# Mark complete
logger.mark_session_complete(Path(f".deia/sessions/{session_id}.md"))

print(f"✓ Session logged to `.deia/sessions/{session_id}.md`")
```

---

## User Experience

**User:** "start logging"

**Claude:**
```
✓ Auto-logging started
Session: 20251010-083000-conversation
I'll save periodically and notify you.
```

**[... 10 messages later ...]**

**Claude:** *(while responding to user's question)*
```
[Answer to question]

✓ Log updated (10 messages)
```

**User:** "that's it for now"

**Claude:**
```
✓ Session logged to `.deia/sessions/20251010-083000-conversation.md`
```

---

## Important Notes

- **Message count:** User message + your response = 1 exchange
- **Time-based save:** Even if quiet, save after 15 minutes
- **Don't interrupt:** Append save notification at END of your response
- **Context extraction:** Use your conversation context to get full transcript
- **Session continuity:** Keep tracking same session_id until user ends

---

## Fallback

If you can't maintain session state (Claude's memory limitations):
- Still create initial log when triggered
- User can use `/log` manually at any time
- At minimum, log exists when session ends
