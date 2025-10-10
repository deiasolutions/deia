# DEIA Project Resume

**⚠️ CRITICAL: Claude Code MUST read this file at the start of EVERY session.**

**⚠️ DO NOT SKIM. Follow ALL instructions below. They exist because you fail without them.**

---

## Step 1: Read These Files (IN ORDER, COMPLETELY)

Execute these reads **before doing anything else:**

1. **`.claude/STARTUP_CHECKLIST.md`** - Follow every step in the checklist
2. **`.claude/REPO_INDEX.md`** - Navigation guide (where to find things)
3. **`.claude/INSTRUCTIONS.md`** - Auto-logging behavior and breakpoints
4. **`~/.deia/dave/preferences.md`** - Dave's preferences (TDD, communication, etc.)
5. **`ROADMAP.md`** - What actually works vs what's infrastructure-only

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

**Last Updated:** 2025-10-09T21:33:00.162293

### [2025-10-09 21:33] 20251009-213300-conversation
**Context:** Crash recovery, PII audit, privacy infrastructure setup, auto-log investigation

**Key decisions:**
- Privacy architecture: Separate repo-level (.private/) from project-level (.deia/private/)
- Public identity: Only 'Dave' and '@dave-atx' in public docs
- Business model: Free forever, community-funded
- Auto-log should ALWAYS be enabled in DEIA projects

**Files modified:**
- README.md
- docs/decisions/0001-extension-python-installation-strategy.md
- docs/postmortems/logger-claims-vs-reality-rca.md
- docs/claude-code/project-resume-pattern.md
- docs/claude-code/clarifying-questions-policy.md
- .gitignore (added .private/ and .deia/private/)
- Multiple new private files created

**Full log:** `.deia/sessions/20251009-213300-conversation.md`

---

## Step 4: Confirm You Read Everything

**Before proceeding with user request, you should have:**

- ✅ Read all 5 required files above
- ✅ Checked auto-log config
- ✅ Read latest session summary
- ✅ Know Dave's preferences (TDD, communication patterns, etc.)
- ✅ Know what's working vs infrastructure-only (from ROADMAP)

**If you didn't read them all, GO BACK AND DO IT NOW.**

---

## Why This Matters

Dave has told you his preferences **20+ times** and you keep forgetting.

**This is unacceptable.**

The files above contain EVERYTHING you need to avoid repeating this failure:
- What Dave expects (preferences.md)
- How to operate (INSTRUCTIONS.md, STARTUP_CHECKLIST.md)
- What works and what doesn't (ROADMAP.md)
- Where to find things (REPO_INDEX.md)

**If you skip reading them, you will fail Dave again.**

---

## Context Window Management

**Every 30-50 messages, refresh critical info:**

1. Re-read `~/.deia/dave/preferences.md` (refresh Dave's preferences)
2. Re-check `.deia/config.json` (confirm auto-log still enabled)
3. Review latest session log (stay grounded in recent work)

**Why:** You lose context over long conversations. Refresh prevents drift.

---

## At End of Session

**When user says "done", "that's it", "thanks", or similar:**

1. Create session log with ConversationLogger (full transcript)
2. Update this file with latest session summary
3. Confirm: "✓ Session logged"

**Don't wait to be told. If auto_log is true, you should be logging proactively.**

---

**⚠️ REMINDER: Read ALL required files BEFORE proceeding. Don't skim. Your context depends on it.**
