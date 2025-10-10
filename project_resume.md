# DEIA Project Resume

**⚠️ CRITICAL: Claude Code MUST read this file at the start of EVERY session.**

**⚠️ DO NOT SKIM. Follow ALL instructions below. They exist because you fail without them.**

---

## Step 1: Read These Files (IN ORDER, COMPLETELY)

Execute these reads **before doing anything else:**

1. **`.claude/STARTUP.md`** - **EXECUTE STARTUP ACTIONS** (auto-log status notification)
2. **`.claude/STARTUP_CHECKLIST.md`** - Follow every step in the checklist
3. **`.claude/REPO_INDEX.md`** - Navigation guide (where to find things)
4. **`.claude/INSTRUCTIONS.md`** - Auto-logging behavior and breakpoints
5. **`~/.deia/dave/preferences.md`** - Dave's preferences (TDD, communication, etc.)
6. **`ROADMAP.md`** - What actually works vs what's infrastructure-only

**These are NOT optional. Read them completely. Don't skim.**

---

## Step 2: Check Configuration

```bash
cat .deia/config.json
```

**If `auto_log: true`:** Start logging at breakpoints (see INSTRUCTIONS.md for when)

**If `auto_log: false`:** Something is wrong - it should be `true` in DEIA projects

---

## Step 3: Review Latest Session

**Last Updated:** 2025-10-10T10:30:17.036720
### [2025-10-10 10:30] 20251010-103017-conversation
**Context:** Building automated conversation logging system

**Key decisions:**
- Create real-time logging
- Use Python + slash command approach

**Files modified:**
- src/deia/logger.py
- .claude/commands/log-conversation.md

**Full log:** `.deia/sessions/20251010-103017-conversation.md`

---

