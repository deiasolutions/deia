# DEIA Sessions Directory

**Purpose:** Store all Claude Code conversation logs (insurance against crashes)

---

## What's Here

- **INDEX.md** - Quick index of all your conversations
- **YYYYMMDD-HHMMSS-conversation.md** - Individual conversation logs (timestamped)

---

## How to Use

### Log Current Conversation

Use slash command during conversation:
```
/log-conversation
```

Or CLI after conversation:
```bash
deia log conversation
```

### Find Latest Conversation

```bash
cat INDEX.md
```

Or:
```bash
ls -t *.md | head -1
```

### Read a Log

```bash
cat 20251006-111339-conversation.md
```

---

## File Format

Each log contains:
- **Metadata:** Timestamp, session ID, status
- **Context:** What you were working on
- **Transcript:** Full conversation
- **Decisions:** Key choices made
- **Action Items:** What was done/pending
- **Files Modified:** List of changed files
- **Next Steps:** How to resume

---

## Privacy

✅ This directory is **gitignored** by default
✅ Never committed to public repos
✅ Only on your local machine

**To share a conversation:**
1. Sanitize first: `deia sanitize session.md`
2. Review manually
3. Then share if appropriate

---

## Maintenance

**Clean old sessions:**
```bash
# Archive sessions older than 90 days
find .deia/sessions -name "*.md" -mtime +90 -exec mv {} archive/ \;
```

**Search sessions:**
```bash
grep -r "keyword" .deia/sessions/
```

**Reindex:**
```bash
rm INDEX.md
deia sessions reindex  # Coming soon
```

---

## Full Documentation

See `docs/conversation-logging.md` for complete guide.

---

**Your conversations are safe here. Build with confidence.**
