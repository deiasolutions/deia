# Log This Conversation

**Trigger:** When user wants to save the current conversation as a session log.

## Instructions for Claude:

You have access to this entire conversation in your context. When the user runs `/log`, you should:

1. **Read the DEIA config** to confirm logging is enabled:
   ```python
   import json
   from pathlib import Path

   config_path = Path(".deia/config.json")
   if config_path.exists():
       config = json.loads(config_path.read_text())
       if not config.get("auto_log", False):
           print("Auto-logging is disabled. Enable with: deia config set auto_log true")
           exit(0)
   ```

2. **Extract key information from the conversation:**
   - What was the context? (What were we working on?)
   - What decisions were made?
   - What action items were completed/pending?
   - What files were created or modified?
   - What should happen next?

3. **Call the logger** with the full conversation transcript:
   ```python
   from deia.logger import ConversationLogger

   logger = ConversationLogger()
   log_file = logger.create_session_log(
       context="Brief description of what we worked on",
       transcript="Full conversation text from your context",
       decisions=["Key decision 1", "Key decision 2"],
       action_items=["Completed item", "Pending item"],
       files_modified=["path/to/file1.py", "path/to/file2.md"],
       next_steps="What should happen in the next session"
   )
   print(f"✓ Logged to: {log_file}")
   ```

4. **Confirm** the log was saved successfully.

## What This Does

- Saves the full conversation (prompts + responses) to `.deia/sessions/YYYYMMDD-HHMMSS-conversation.md`
- Updates `.deia/sessions/INDEX.md` with session metadata
- Updates `project_resume.md` with reference to this session
- Provides crash recovery - if Claude Code crashes, the log persists

## Cost Note

This uses your API tokens (Claude writes the log), but ensures you never lose context from crashes.
