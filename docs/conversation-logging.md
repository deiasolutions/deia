# Conversation Logging - Never Lose Context Again

**Problem:** Computer crashes, browser crashes, or Claude Code session resets lose your entire conversation history.

**Solution:** Real-time conversation logging to `.deia/sessions/`

---

## Quick Start

### Option 1: Slash Command (Recommended)

Use the `/log-conversation` slash command at any point during your conversation:

```
/log-conversation
```

Claude will save the current conversation with context, decisions, and action items.

### Option 2: CLI Command

After your conversation ends (or during):

```bash
deia log conversation
```

You'll be prompted for:
- What you were working on (context)
- Key decisions made
- Action items completed
- Files modified
- Next steps

### Option 3: Python API

For programmatic logging:

```python
from deia.logger import ConversationLogger

logger = ConversationLogger()
log_file = logger.create_session_log(
    context="Building conversation logging system",
    transcript="[Your full conversation here]",
    decisions=["Use Python + slash command", "Store in .deia/sessions/"],
    action_items=["Built logger.py", "Created CLI command"],
    files_modified=["src/deia/logger.py", "src/deia/cli.py"],
    next_steps="Test and document the system"
)

print(f"Logged to: {log_file}")
```

---

## What Gets Logged

Each conversation log includes:

1. **Metadata**
   - Timestamp (ISO format)
   - Session ID (unique identifier)
   - Status (Active/Completed)

2. **Context**
   - What you were working on
   - Why it matters

3. **Full Transcript**
   - Complete conversation text
   - All tool calls and responses

4. **Key Decisions**
   - Major choices made during session
   - Rationale where applicable

5. **Action Items**
   - What was completed
   - What's still pending

6. **Files Modified**
   - All files created/edited
   - Brief description of changes

7. **Next Steps**
   - How to resume
   - What to do next session

---

## Storage Structure

```
.deia/sessions/
├── INDEX.md                           # Master index of all conversations
├── 20251006-143022-conversation.md    # Individual conversation logs
├── 20251006-160845-conversation.md
└── 20251007-091234-conversation.md
```

**INDEX.md format:**
```markdown
# DEIA Session Index

## Sessions

### 20251006-143022-conversation
- **Date:** 2025-10-06 14:30:22
- **Status:** Completed
- **Context:** Building automated conversation logging
- **File:** `.deia/sessions/20251006-143022-conversation.md`
```

---

## Use Cases

### 1. Insurance Against Crashes
**Before:** Computer crashes → lose entire conversation → waste hours reconstructing context

**After:** Computer crashes → read latest log in `.deia/sessions/` → resume exactly where you left off

### 2. Session Handoffs
**Before:** Need to context-switch projects → forget details → waste time re-reading code

**After:** Log conversation → come back days later → read log → immediate context

### 3. Knowledge Extraction
**Before:** Great insights discussed but forgotten

**After:** Review logs → extract patterns → add to BOK

### 4. Accountability
**Before:** "Wait, did we decide to use X or Y?"

**After:** Check decisions section of log → clear answer

---

## Best Practices

### When to Log

✅ **Always log:**
- Before ending a session
- After major decisions
- When about to switch contexts
- After solving complex problems
- When computer feels unstable

❌ **Don't log:**
- Trivial conversations (simple questions)
- Sessions with zero decisions or work done

### What to Include

**Good context:**
> "Building automated conversation logging to prevent data loss from crashes. Implementing Python logger + CLI + slash command."

**Bad context:**
> "Working on stuff"

**Good decisions:**
- "Store logs in `.deia/sessions/` (gitignored for privacy)"
- "Use timestamp-based filenames for chronological ordering"
- "Create INDEX.md for quick session lookup"

**Bad decisions:**
- "Made some choices"

### Log Hygiene

1. **Review before closing session**
   - Did you capture key decisions?
   - Are file paths correct?
   - Is context clear for future you?

2. **Update if conversation continues**
   ```python
   logger.append_to_session(log_file, "Additional work: Fixed bug in X")
   ```

3. **Mark complete when done**
   ```python
   logger.mark_session_complete(log_file)
   ```

---

## Advanced Usage

### Append to Existing Log

If conversation continues after logging:

```python
from pathlib import Path
from deia.logger import ConversationLogger

logger = ConversationLogger()
latest_log = logger.get_latest_session()

logger.append_to_session(
    latest_log,
    "Additional work: Implemented GitHub Actions workflow"
)
```

### Query Logs

Find conversations about specific topics:

```bash
grep -r "conversation logging" .deia/sessions/
```

Or use DEIA's search (coming soon):

```bash
deia sessions search "logging"
```

### Export for Review

Convert logs to different formats:

```bash
# Coming soon
deia sessions export --format=pdf --session=20251006-143022
```

---

## Privacy & Security

**What's logged:**
- Your conversation with Claude
- Decisions and context
- Files modified (paths only, not content)

**What's NOT logged:**
- File contents (unless you paste them in transcript)
- Secrets or credentials (sanitize first!)
- PII (your responsibility to remove)

**Storage:**
- Logs stored in `.deia/sessions/` (gitignored by default)
- Never committed to git unless you explicitly add them
- Never shared unless you sanitize and submit

**Sanitization:**
Before sharing logs:

```bash
deia sanitize .deia/sessions/20251006-143022-conversation.md
```

---

## Troubleshooting

### Log file not created

**Check:**
1. Is `.deia/` directory initialized? Run `deia init`
2. Do you have write permissions?
3. Is disk full?

### Can't find latest log

```python
from deia.logger import ConversationLogger

logger = ConversationLogger()
latest = logger.get_latest_session()
print(f"Latest log: {latest}")
```

### INDEX.md corrupted

Delete and regenerate:

```bash
rm .deia/sessions/INDEX.md
deia sessions reindex  # Coming soon
```

Or manually:
```python
from deia.logger import ConversationLogger
from pathlib import Path

logger = ConversationLogger()
# Re-index all sessions
for session_file in sorted(Path(".deia/sessions").glob("*-conversation.md")):
    # Parse and re-add to index
    pass
```

---

## Integration with DEIA Pipeline

**Workflow:**

1. **Have conversation** with Claude Code
2. **Log conversation** (manual or automatic)
3. **Review log** for extractable patterns
4. **Extract to BOK** if universally valuable
5. **Sanitize BOK entry** before submission
6. **Submit to community**

**Example:**

```bash
# During conversation
/log-conversation

# Review logs
cat .deia/sessions/INDEX.md

# Found pattern worth sharing
deia bok extract .deia/sessions/20251006-143022-conversation.md

# Sanitize
deia sanitize bok/patterns/conversation-logging.md

# Submit
deia submit bok/patterns/conversation-logging.md
```

---

## Roadmap

**v1.0 (Current):**
- ✅ Manual conversation logging
- ✅ CLI command
- ✅ Slash command integration
- ✅ Session INDEX

**v1.1 (Soon):**
- 🔄 Automatic logging (no manual trigger needed)
- 🔄 Real-time append (log updates as you chat)
- 🔄 Session search
- 🔄 Export to PDF/HTML

**v2.0 (Future):**
- 📅 AI-assisted BOK extraction from logs
- 📅 Pattern detection across sessions
- 📅 Session analytics dashboard
- 📅 Cloud backup option

---

## FAQ

**Q: Is this like the "export conversation" feature in ChatGPT?**

A: Similar, but better:
- Structured format (not just plain text)
- Includes decisions, action items, next steps
- Integrates with DEIA pipeline
- Designed for recovery, not just archival

**Q: Can Claude automatically log without me asking?**

A: Not yet. v1.1 will have automatic real-time logging. For now, use the slash command.

**Q: Do logs include file contents?**

A: No, just file paths. If you need content, paste it manually or use `deia log create` for session logs (different format).

**Q: Can I log conversations from other tools (Cursor, Copilot)?**

A: Yes! Use the CLI:
```bash
deia log conversation --context "Your context" --transcript conversation.txt
```

**Q: How much disk space do logs use?**

A: ~10-50KB per conversation. 1000 conversations ≈ 10-50MB.

**Q: Should I commit logs to git?**

A: No (gitignored by default). Only commit sanitized BOK entries.

---

## Credits

**Inspired by:** Dave's frustration with Anthropic not preserving conversations

**Design principle:** "FUCK MY COMPUTER CRASHED" should never mean lost work

**Constitutional principle:** "Never lose context"

---

**Your conversation is now safe. Get back to building.**
