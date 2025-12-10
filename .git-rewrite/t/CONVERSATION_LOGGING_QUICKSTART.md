# Conversation Logging - Quick Start

**Problem solved:** Never lose Claude Code conversations to crashes again.

---

## How to Use (3 Ways)

### 1. Slash Command (Easiest)

During your conversation with Claude Code:

```
/log-conversation
```

Claude will save everything.

### 2. Python One-Liner (For Right Now)

```bash
python -c "from src.deia.logger import quick_log; quick_log('Your context here', 'Your transcript here')"
```

### 3. CLI Command (After install)

```bash
deia log conversation
```

Prompts you for:
- Context (what you worked on)
- Decisions made
- Files modified
- Next steps

---

## Where Logs Are Saved

```
.deia/sessions/
├── INDEX.md                        # Quick index of all conversations
└── 20251006-111339-conversation.md # Your conversation (timestamped)
```

**Already gitignored** - won't accidentally commit.

---

## Usage Pattern

**Before ending session:**
```
/log-conversation
```

**If computer crashes:**
```bash
cat .deia/sessions/INDEX.md              # Find latest session
cat .deia/sessions/20251006-*.md         # Read the log
# Resume exactly where you left off
```

---

## What Gets Logged

✅ Full conversation transcript
✅ Context (what you were working on)
✅ Key decisions made
✅ Action items completed/pending
✅ Files created/modified
✅ Next steps for resume

---

## Test It Now

```bash
python -c "from src.deia.logger import ConversationLogger; logger = ConversationLogger(); log = logger.create_session_log(context='Testing conversation logging', transcript='This is a test', decisions=['Test the logger'], action_items=['Run this command'], files_modified=['None'], next_steps='Use it for real conversations'); print(f'Created: {log}')"
```

Then check:
```bash
cat .deia/sessions/INDEX.md
```

---

## Full Docs

See `docs/conversation-logging.md` for complete documentation.

---

**You're now insured against crashes. Get back to building.**
