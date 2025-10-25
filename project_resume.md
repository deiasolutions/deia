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

**Last Updated:** 2025-10-17T20:12:05.228823
### [2025-10-17 20:12] 20251017-201205228823-conversation
**Context:** Agent 004 testing DEIA real-time conversation logging capability

**Key decisions:**
- Stopped FileReader work mid-task for P0 priority
- Realized logging infrastructure already exists
- Testing logging with current conversation as proof-of-concept

**Files modified:**
- tests/unit/test_file_reader.py (completed earlier)
- pyproject.toml (added chardet dependency)

**Full log:** `.deia/sessions/20251017-201205228823-conversation.md`

---

