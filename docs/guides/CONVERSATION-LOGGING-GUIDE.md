# DEIA Conversation Logging Guide

**Never lose context from crashes or forgetfulness again.**

---

## What is Conversation Logging?

DEIA's conversation logging system automatically captures your AI assistant conversations and saves them to `.deia/sessions/`. This means:

- **Crash Recovery:** If Claude Code crashes, your conversation is saved
- **Context Continuity:** Pick up where you left off, even days later
- **Team Collaboration:** Share session logs with teammates to show what happened
- **Knowledge Building:** Extract patterns from logs into the Body of Knowledge (BOK)
- **Audit Trail:** Track decisions, files modified, and action items over time

**Key Benefit:** You control when and what gets logged - nothing happens automatically without your configuration.

---

## Quick Start

### Option 1: Manual Logging (Recommended for New Users)

Use the `/log` slash command when you want to save a conversation:

1. **During or after a conversation**, run:
   ```
   /log
   ```

2. **Claude will:**
   - Extract the conversation from context
   - Identify key decisions, files modified, and action items
   - Save to `.deia/sessions/YYYYMMDD-HHMMSS-conversation.md`
   - Update `.deia/sessions/INDEX.md` with session metadata
   - Update `project_resume.md` with a summary

3. **Verify** the log was created:
   ```bash
   ls .deia/sessions/
   ```

**When to use `/log`:**
- After completing a major task
- Before ending a session
- When you want to preserve important context
- After making critical decisions

---

### Option 2: Enable Auto-Log Config (Advanced)

**⚠️ Note:** This enables a config flag but you still need to manually trigger logging with `/log` or `/start-logging`.

1. **Edit `.deia/config.json`:**
   ```json
   {
     "project": "your-project",
     "user": "your-name",
     "auto_log": true,
     "version": "0.1.0"
   }
   ```

2. **Or use the CLI** (if `deia config` command exists):
   ```bash
   deia config set auto_log true
   ```

3. **What this does:**
   - Sets a flag that Claude Code can check
   - Enables `/start-logging` command for session-based logging
   - Does NOT automatically log - you still control when logs are created

---

### Option 3: Session-Based Auto-Logging

For long conversations where you want periodic saves:

1. **Enable auto_log** in config (see Option 2)

2. **Start a session** at the beginning of your work:
   ```
   /start-logging
   ```

3. **Claude will:**
   - Create an initial session log
   - Track message count and time
   - Periodically append updates (every 10 messages or 15 minutes)
   - Notify you when saves occur

4. **End the session** when done:
   ```
   User: "that's it for now"
   Claude: ✓ Session logged to `.deia/sessions/20251018-090000-conversation.md`
   ```

**Best for:**
- Long debugging sessions
- Multi-hour feature development
- Complex problem-solving conversations
- When you want insurance against crashes

---

## Configuration

### Check Current Config

```bash
cat .deia/config.json
```

### Enable Auto-Logging

**Method 1: Edit config.json directly**

```json
{
  "project": "your-project",
  "user": "your-name",
  "auto_log": true,
  "version": "0.1.0"
}
```

**Method 2: CLI command** (if available)

```bash
deia config set auto_log true
```

### Disable Auto-Logging

Set `auto_log` to `false`:

```json
{
  "auto_log": false
}
```

Or:

```bash
deia config set auto_log false
```

---

## Using Logs

### Where Logs are Stored

**Location:** `.deia/sessions/`

**Files:**
- `20251018-090000123456-conversation.md` - Individual session logs
- `INDEX.md` - Master index of all sessions with metadata
- *(Logs also reference `project_resume.md` in project root)*

### Log File Format

Each log is a markdown file with this structure:

```markdown
# DEIA Conversation Log

**Date:** 2025-10-18T09:00:00.123456
**Session ID:** 20251018-090000123456-conversation
**Status:** Active | Completed

---

## Context
Brief description of what you were working on

---

## Full Transcript
Complete conversation (user messages + Claude responses)

---

## Key Decisions Made
- Decision 1
- Decision 2

---

## Action Items
- Completed item
- Pending item

---

## Files Modified
- `path/to/file1.py`
- `path/to/file2.md`

---

## Next Steps
What should happen in the next session
```

### Log Naming Convention

**Format:** `YYYYMMDD-HHMMSS[microseconds]-conversation.md`

**Example:** `20251018-143022456789-conversation.md`

**Why microseconds?** Ensures unique filenames for rapid successive sessions (testing, automation)

### Reading Session Logs

1. **List all logs** (newest first):
   ```bash
   ls -t .deia/sessions/*.md
   ```

2. **View the latest log:**
   ```bash
   cat .deia/sessions/$(ls -t .deia/sessions/*-conversation.md | head -1)
   ```

3. **Search logs by date:**
   ```bash
   ls .deia/sessions/20251018-*.md
   ```

4. **Check the index:**
   ```bash
   cat .deia/sessions/INDEX.md
   ```

5. **Quick context recovery** from `project_resume.md`:
   ```bash
   cat project_resume.md | head -50
   ```

---

## Integration with Claude Code

### Slash Commands

DEIA provides two slash commands for logging:

#### `/log` - Manual Log Creation

**Purpose:** Save the current conversation as a session log

**Usage:**
```
/log
```

**What happens:**
1. Claude reads the conversation from its context
2. Extracts key information (decisions, files, action items)
3. Calls `ConversationLogger.create_session_log()`
4. Saves to `.deia/sessions/`
5. Updates `INDEX.md` and `project_resume.md`

**When to use:**
- After completing a task
- Before ending a session
- When you want to preserve important context
- After making critical decisions

---

#### `/start-logging` - Session-Based Auto-Logging

**Purpose:** Start a session with periodic auto-saves

**Usage:**
```
/start-logging
```

**What happens:**
1. Creates initial session log
2. Tracks message count and time
3. Appends updates every 10 messages or 15 minutes
4. Saves before context window limit (autocompact protection)
5. Marks session complete when user says "done" or "goodbye"

**When to use:**
- Long debugging sessions
- Multi-hour feature development
- When you want insurance against crashes

**How it works:**

```
User: /start-logging

Claude:
✓ Auto-logging started
Session: 20251018-090000-conversation
I'll save periodically and notify you.

[... 10 messages later ...]

Claude: [Answer to your question]

✓ Log updated (10 messages)

[... continue working ...]

User: that's it for now

Claude:
✓ Session logged to `.deia/sessions/20251018-090000-conversation.md`
```

---

### INSTRUCTIONS.md Integration

Claude Code reads `.claude/INSTRUCTIONS.md` at the start of every session. DEIA's instructions tell Claude:

1. **Check auto_log status** in `.deia/config.json`
2. **Proactively offer logging** at key breakpoints:
   - When user asks "where were we?"
   - After major task completion
   - When user ends session ("done", "thanks", etc.)
   - For crash recovery
3. **Use ConversationLogger** to create logs

**How to verify:**

```bash
cat .claude/INSTRUCTIONS.md | head -30
```

You should see auto-log logic at the top.

---

## Advanced Features

### Session Updates

Append content to an existing session log:

```python
from deia.logger import ConversationLogger
from pathlib import Path

logger = ConversationLogger()
session_file = Path(".deia/sessions/20251018-090000-conversation.md")

logger.append_to_session(
    session_file=session_file,
    new_content="Additional notes or conversation updates"
)
```

**Use case:** Adding retrospective notes to a completed session

---

### Mark Session Complete

Change status from "Active" to "Completed":

```python
from deia.logger import ConversationLogger
from pathlib import Path

logger = ConversationLogger()
session_file = Path(".deia/sessions/20251018-090000-conversation.md")

logger.mark_session_complete(session_file)
```

**Result:** `**Status:** Active` → `**Status:** Completed` in log file

---

### Get Latest Session

Programmatically find the most recent log:

```python
from deia.logger import ConversationLogger

logger = ConversationLogger()
latest = logger.get_latest_session()

if latest:
    print(f"Latest session: {latest}")
    content = latest.read_text()
else:
    print("No sessions found")
```

**Use case:** Building tools that analyze or process recent sessions

---

### Project Resume Integration

Every log automatically updates `project_resume.md` with:
- Session timestamp and ID
- Brief context
- Key decisions (first 3)
- Files modified (first 5)
- Link to full log

**Why?** Provides a quick-start summary for Claude when you begin a new session.

**Disable:** Pass `update_project_resume=False` to `create_session_log()`

---

## Troubleshooting

### Logs Not Being Created

**Check 1: Is the `.deia/sessions/` directory present?**

```bash
ls .deia/sessions/
```

If missing:
```bash
deia init
```

---

**Check 2: Did you actually run `/log` or `/start-logging`?**

Auto-log config does NOT automatically log - you must trigger commands.

---

**Check 3: Are you in a DEIA project?**

```bash
ls .deia/config.json
```

If missing, initialize:
```bash
deia init
```

---

**Check 4: Check permissions**

```bash
ls -la .deia/sessions/
```

Ensure you have write permissions.

---

### Logs Missing Content

**Issue:** Log file exists but contains incomplete or placeholder text

**Cause:** Claude may not have access to full conversation context

**Solution:**
- Use `/log` during the session (not after a restart)
- For long sessions, use `/start-logging` for periodic saves
- Manually copy/paste conversation if needed

---

### `/log` Command Not Found

**Check 1: Is the command file present?**

```bash
ls .claude/commands/log.md
```

If missing, reinstall DEIA or restore from repository.

---

**Check 2: Restart Claude Code**

Sometimes commands need a restart to be recognized.

---

### Performance Issues with Large Logs

**Issue:** Log files are getting very large (>1MB)

**Current State:** No automatic log rotation exists yet

**Workarounds:**
1. **Manual archive:** Move old logs to `.deia/sessions/archive/`
   ```bash
   mkdir -p .deia/sessions/archive
   mv .deia/sessions/202510* .deia/sessions/archive/
   ```

2. **Split long sessions:** Use `/log` periodically instead of one long session

3. **Compress old logs:**
   ```bash
   tar -czf sessions-2025-10.tar.gz .deia/sessions/202510*.md
   mv .deia/sessions/202510*.md .deia/sessions/archive/
   ```

**Future:** Automatic log rotation may be added in a future release

---

## Examples

### Example 1: Bug Fixing Session

**Scenario:** You're fixing a bug and want to log the investigation and solution

```
User: I'm getting an error in path_validator.py

[... conversation about debugging ...]

User: /log

Claude:
✓ Logged to: .deia/sessions/20251018-100530456789-conversation.md
```

**Log Preview:**
```markdown
## Context
Debugging regex pattern bug in PathValidator for .ssh directory validation

## Key Decisions Made
- Changed pattern from /.ssh to /.ssh/
- Added test case for edge case
- Updated security documentation

## Files Modified
- `src/deia/services/path_validator.py`
- `tests/unit/test_path_validator.py`

## Next Steps
Run full test suite and verify no regressions
```

---

### Example 2: Feature Development Session

**Scenario:** Multi-hour development of a new feature with periodic saves

```
User: /start-logging

Claude:
✓ Auto-logging started
Session: 20251018-140000-conversation
I'll save periodically and notify you.

[... work on feature for 2 hours, 30 messages ...]

Claude: [Response to a question]

✓ Log updated (10 messages)

[... continue for another hour ...]

✓ Log updated (10 messages)

[... feature complete ...]

User: that's all for today

Claude:
✓ Session logged to `.deia/sessions/20251018-140000-conversation.md`
```

**Result:** Complete history of 3+ hour session with periodic snapshots

---

### Example 3: Quick Task Logging

**Scenario:** Small task, just want to record what you did

```
User: Update README with new installation instructions

[... Claude updates README ...]

User: /log

Claude:
✓ Logged to: .deia/sessions/20251018-163000-conversation.md
```

**Log Preview:**
```markdown
## Context
Updated README.md with comprehensive installation guide

## Files Modified
- `README.md`

## Next Steps
None - task complete
```

---

## FAQ

### Q: Do logs contain sensitive data?

**A:** Logs contain the full conversation, which may include:
- File paths (may reveal system structure)
- Code snippets (may contain business logic)
- Error messages (may contain internal details)

**⚠️ Current State:** No automatic sanitization exists

**Best Practices:**
- Review logs before sharing externally
- Add `.deia/sessions/` to `.gitignore` for public repos
- Manually redact sensitive information before sharing

**Future:** Automatic PII/secret sanitization is planned (Phase 2)

---

### Q: Can I disable logging?

**A:** Yes, two levels:

**Level 1: Don't enable auto_log**
- Keep `auto_log: false` in config
- Logging commands still work if you manually run them

**Level 2: Don't use logging commands**
- Simply don't run `/log` or `/start-logging`
- No logs are created

**Level 3: Remove command files**
```bash
rm .claude/commands/log.md
rm .claude/commands/start-logging.md
```

---

### Q: How much disk space do logs use?

**A:** Depends on conversation length:
- **Short session (5-10 messages):** 2-5 KB
- **Medium session (30 messages):** 10-20 KB
- **Long session (100+ messages, with code):** 50-200 KB

**Typical project (50 sessions):** 1-5 MB total

**Management:**
- Archive old logs periodically
- Compress archives with `tar -czf`
- Delete logs older than N months (your choice)

---

### Q: Are logs backed up?

**A:** If `.deia/sessions/` is committed to git, yes.

**Recommendation:**
- **Private repos:** Commit logs for team visibility
- **Public repos:** Add `.deia/sessions/` to `.gitignore`

**Example `.gitignore`:**
```
.deia/sessions/
.deia/observations/
.deia/bot-logs/
```

---

### Q: Can I export logs to other formats?

**A:** Not currently. Logs are markdown (.md) files.

**Manual export:**
- **PDF:** Use Pandoc: `pandoc log.md -o log.pdf`
- **HTML:** `pandoc log.md -o log.html`
- **DOCX:** `pandoc log.md -o log.docx`

**Future:** Export tools may be added in a future release

---

### Q: How do I share logs with teammates?

**Method 1: Git commit** (if private repo)
```bash
git add .deia/sessions/20251018-conversation.md
git commit -m "docs: Add session log for feature X"
git push
```

**Method 2: Direct file share**
```bash
cp .deia/sessions/20251018-*.md ~/Desktop/
# Share via email, Slack, etc.
```

**Method 3: Include in PR description**
- Copy relevant sections from log
- Paste into GitHub PR description
- Provides context for reviewers

---

### Q: What if I forget to log a session?

**A:** Unfortunately, if Claude's context is cleared (autocompact, restart), you can't recover it.

**Prevention:**
- Use `/start-logging` at session start for insurance
- Run `/log` periodically during long sessions
- Enable auto_log and use periodic manual logs

**Future:** Better autocompact detection may be added

---

### Q: Can I search across all logs?

**A:** Yes, using standard tools:

**Search by keyword:**
```bash
grep -r "keyword" .deia/sessions/
```

**Search with context:**
```bash
grep -r -A 5 -B 5 "keyword" .deia/sessions/
```

**Search by date range:**
```bash
grep -r "keyword" .deia/sessions/202510*.md
```

**Future:** Dedicated search tool (`deia search logs`) may be added

---

## Best Practices

### 1. Log After Major Milestones

Run `/log` after:
- Completing a feature
- Fixing a bug
- Making architectural decisions
- Refactoring code
- Writing documentation

---

### 2. Use Descriptive Context

When logging manually, help Claude extract meaningful context:

**Good:**
```
User: /log
[Context: Implemented user authentication with JWT tokens]
```

**Better:** Let Claude extract it naturally from conversation

---

### 3. Review Logs Periodically

Once a week:
```bash
ls -t .deia/sessions/ | head -20
```

- Archive old logs
- Extract patterns for BOK
- Identify recurring issues

---

### 4. Use Session-Based Logging for Complex Work

For sessions >1 hour or >20 messages:
```
/start-logging
```

Ensures you don't lose work to crashes or context limits.

---

### 5. Keep Logs Out of Public Repos

Add to `.gitignore`:
```
.deia/sessions/
```

Unless you're intentionally sharing for documentation purposes.

---

## Related Features

### Body of Knowledge (BOK)

Logs are raw material for BOK patterns:
1. Complete a project
2. Review session logs
3. Extract patterns using `deia extract` (Phase 2)
4. Submit to BOK

**Learn more:** `bok/README.md`

---

### Master Librarian

Query past sessions using the Master Librarian:
```bash
deia librarian query "authentication bug"
```

**Learn more:** `docs/specs/master-librarian-service-wip.md`

---

### Project Resume

Automatically updated with each log. Read it at session start:
```bash
cat project_resume.md
```

---

## Technical Reference

### ConversationLogger API

**Class:** `deia.logger.ConversationLogger`

**Methods:**

| Method | Purpose |
|--------|---------|
| `create_session_log()` | Create new log file |
| `append_to_session()` | Add content to existing log |
| `get_latest_session()` | Find most recent log file |
| `mark_session_complete()` | Update status to Completed |

**Helper Functions:**

| Function | Purpose |
|----------|---------|
| `quick_log()` | Shorthand for creating logs |
| `check_auto_log_enabled()` | Check config.json for auto_log flag |

**Full API:**

```python
from deia.logger import ConversationLogger
from pathlib import Path

# Initialize
logger = ConversationLogger(project_root=Path.cwd())

# Create log
log_file = logger.create_session_log(
    context="Brief description",
    transcript="Full conversation text",
    decisions=["Decision 1", "Decision 2"],
    action_items=["Item 1", "Item 2"],
    files_modified=["file1.py", "file2.md"],
    next_steps="What to do next",
    status="Active",  # or "Completed"
    update_project_resume=True  # Set False to skip
)

# Append to existing log
logger.append_to_session(
    session_file=Path(".deia/sessions/20251018-conversation.md"),
    new_content="Additional notes"
)

# Mark complete
logger.mark_session_complete(
    session_file=Path(".deia/sessions/20251018-conversation.md")
)

# Get latest
latest = logger.get_latest_session()
```

---

## What's Not Included (Yet)

**Features that don't exist but may be added:**

- ❌ Automatic PII/secret sanitization
- ❌ Automatic log rotation
- ❌ Export to PDF/HTML
- ❌ Search across logs UI
- ❌ Log analytics dashboard
- ❌ Automatic pattern extraction
- ❌ Real-time streaming logs

**See ROADMAP.md for planned features**

---

## Getting Help

**Issues?** Check:
1. This guide's [Troubleshooting](#troubleshooting) section
2. `INSTALLATION.md` for setup issues
3. GitHub Issues: https://github.com/deia-project/deia (if public)

**Feature Requests:** Add to project BACKLOG.md or open an issue

---

## Summary

**Quick Reference Card:**

| Task | Command | When |
|------|---------|------|
| Manual log | `/log` | After tasks, before ending session |
| Session logging | `/start-logging` | Long sessions (>1 hour) |
| Enable auto-log | Edit `.deia/config.json` | One-time setup |
| View logs | `ls .deia/sessions/` | Anytime |
| Read latest | `cat project_resume.md` | At session start |

**Key Takeaways:**
- ✅ Logging is opt-in and user-controlled
- ✅ Use `/log` for quick saves, `/start-logging` for long sessions
- ✅ Logs survive crashes and provide crash recovery
- ✅ Logs are markdown files, easy to read and share
- ⚠️ Review logs before sharing (no auto-sanitization yet)
- ⚠️ Archive old logs periodically (no auto-rotation yet)

---

**Version:** 1.0
**Last Updated:** 2025-10-18
**Author:** CLAUDE-CODE-002 (Documentation Systems Lead)
**Status:** Production-ready documentation for existing feature

---

*This guide documents the EXISTING conversation logging system built into DEIA. The feature works - you just needed to know about it!*
