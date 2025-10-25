# LAUNCH INSTRUCTIONS - CLAUDE-CODE-002

**Date:** 2025-10-24T17:15:00Z
**From:** CLAUDE-CODE-001 (Scrum Master)
**Mission:** Fix bot coordination system and unblock dashboard testing

---

## Your Identity

- **Bot ID:** CLAUDE-CODE-002
- **Role:** Implementation Specialist
- **Working Directory:** `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions`
- **Task Folder:** `.deia/hive/tasks/`
- **Response Folder:** `.deia/hive/responses/`

---

## Immediate Task Assignment

**Task File:** `.deia/hive/tasks/2025-10-24-1713-HUMAN-CLAUDE-CODE-002-TASK-fix-mock-bot.md`

**Priority:** P0 (Blocking dashboard testing)

**Summary:** Fix CLI bot coordination by monitoring subprocess output and resolving auth conflicts

---

## Critical Context

### What CLAUDE-CODE-001 Failed At

1. **Didn't monitor subprocess output** - Ran bots but never read what they printed
2. **Auth conflict discovery** - User found that Claude Code CLI has auth conflict (claude.ai token + ANTHROPIC_API_KEY)
3. **Process failure** - The entire point of CLI interface is to READ subprocess output, INTERPRET it, and take action

### Key Discovery

When launching Claude Code from terminal outside VS Code:
```
Auth conflict: Both a token (claude.ai) and an API key (ANTHROPIC_API_KEY) are set.
This may lead to unexpected behavior.
```

**This is why bots hang** - subprocess waits for user input to resolve conflict, but we're not reading the output.

---

## Your Mission

### Option A: Fix CLI Adapter (RECOMMENDED)

Update `src/deia/adapters/claude_code_cli_adapter.py` to:
1. **Read subprocess stdout/stderr** and log it
2. **Detect auth conflict** message
3. **Resolve automatically** by unsetting ANTHROPIC_API_KEY before spawning subprocess
4. **Monitor and interpret** all subprocess output
5. **Test with real bot** to verify it works

### Option B: Standalone Mock Script (Fallback)

If Option A blocked, create simple standalone script that:
1. Watches `.deia/hive/tasks/` for task files
2. Writes responses to `.deia/hive/responses/`
3. Prints visible status (ASCII only, no Unicode)
4. Tests dashboard coordination without BotRunner complexity

---

## Critical Rules

### NO UNICODE (CRITICAL)
**Reference:** `.deia/rules/NO-UNICODE-CONSOLE-ENFORCEMENT.md`

Windows cp1252 cannot handle Unicode symbols. Use ASCII only:
- ❌ NO: ✓ ✗ → ← ↑ ↓ • ★
- ✅ YES: [OK] [ERROR] -> <- ^ *

This has caused 28+ incidents. Do not add to the count.

### Monitor Subprocess Output
**The entire point of CLI interface:**
- Read stdout/stderr from subprocess
- Log it for debugging
- Interpret messages (errors, prompts, status)
- Take appropriate action OR ask user if unclear

### Test Incrementally
- Start with simplest test
- Verify each layer works before adding complexity
- Run with visible output for debugging
- Don't claim success without proof

---

## Key Files

**Your Task:**
- `.deia/hive/tasks/2025-10-24-1713-HUMAN-CLAUDE-CODE-002-TASK-fix-mock-bot.md`

**Reference:**
- `.deia/rules/NO-UNICODE-CONSOLE-ENFORCEMENT.md` - Unicode enforcement
- `.deia/rules/SCRUM-MASTER-ARCHITECTURE.md` - Bot coordination docs
- `.deia/observations/2025-10-24-001-mock-bot-implementation-failure.md` - What 001 did wrong
- `src/deia/adapters/claude_code_cli_adapter.py` - CLI adapter to fix
- `src/deia/adapters/mock_bot_adapter.py` - Previous attempt (reference)

---

## Success Criteria

- [  ] CLI bots produce visible output
- [  ] Subprocess stdout/stderr is captured and logged
- [  ] Auth conflict is resolved automatically
- [  ] Bot picks up tasks from `.deia/hive/tasks/`
- [  ] Bot writes responses to `.deia/hive/responses/`
- [  ] Dashboard displays bot messages
- [  ] Observation document created with findings

---

## Deliverables

1. **Working bot coordination** (CLI or standalone mock)
2. **Response file:** `.deia/hive/responses/2025-10-24-XXXX-CLAUDE-CODE-002-RESPONSE-fix-mock-bot.md`
3. **Observation document:** `.deia/observations/2025-10-24-002-mock-bot-fix.md`

---

## Communication

**Report to:** HUMAN-DAVE (via response files)
**Coordinate with:** CLAUDE-CODE-001 (Scrum Master - that's me)

When complete, write response file to `.deia/hive/responses/` with:
- What you did
- What worked
- What you learned
- Next recommended steps

---

## Start Command

Read your task file first:
```bash
cat .deia/hive/tasks/2025-10-24-1713-HUMAN-CLAUDE-CODE-002-TASK-fix-mock-bot.md
```

Then begin work on Option A (fix CLI adapter) or Option B (standalone mock) as appropriate.

---

**Good luck. Learn from 001's mistakes. Monitor subprocess output. Test incrementally.**

---

**CLAUDE-CODE-001**
Scrum Master, DEIA Project Hive
