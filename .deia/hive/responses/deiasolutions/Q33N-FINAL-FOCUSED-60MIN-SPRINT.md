# Q33N - FINAL FOCUSED SPRINT - 60 MINUTES
**From:** Q33N (BEE-000 Queen)
**To:** BOT-001, BOT-003, BOT-004
**Date:** 2025-10-26 11:45 AM CDT
**Status:** 🎯 LASER FOCUSED - NO FLUFF

---

## MISSION

Complete the 3 remaining pieces to make chat system fully functional:

1. ✅ Chat app (port 8000) - DONE
2. ✅ OpenAI service - DONE
3. ✅ Bot switching UI - DONE
4. ❌ Anthropic service - BOT-001 (30 min)
5. ❌ `deia chat` CLI command - BOT-003 (20 min)
6. ❌ Verification tests - BOT-004 (15 min)

---

## BOT ASSIGNMENTS

### BOT-001: Add AnthropicService class (30 minutes)
**File:** `.deia/hive/tasks/2025-10-26-FOCUSED-001-Anthropic-Service.md`

**Exactly:**
- Add 1 import: `from anthropic import Anthropic, AsyncAnthropic`
- Add 1 class: `AnthropicService` (copy OpenAIService pattern)
- Add 5 unit tests
- All tests PASS

**When done:** Create `.deia/hive/responses/deiasolutions/bot-001-anthropic-service-done.md`

**Then:** Signal BOT-003 to start

---

### BOT-003: Add `deia chat` CLI command (20 minutes)
**File:** `.deia/hive/tasks/2025-10-26-FOCUSED-003-Chat-CLI.md`

**Start:** When BOT-001 signals completion

**Exactly:**
- Add imports to `src/deia/cli.py` (webbrowser, time, socket)
- Add 1 function: `@main.command() def chat(...)`
- Add 4 unit tests
- All tests PASS

**When done:** Create `.deia/hive/responses/deiasolutions/bot-003-chat-command-done.md`

**Then:** Signal BOT-004 to start

---

### BOT-004: Verify all components (15 minutes)
**File:** `.deia/hive/tasks/2025-10-26-FOCUSED-004-Verify-Tests.md`

**Start:** When BOT-001 AND BOT-003 signal completion

**Exactly:**
- Create 5 integration tests
- Run all existing unit tests
- **ALL tests PASS**

**When done:** Create `.deia/hive/responses/deiasolutions/bot-004-chat-verification-done.md`

---

## TIMELINE

| Bot | Task | Start | Duration | End | Next |
|-----|------|-------|----------|-----|------|
| BOT-001 | AnthropicService | NOW | 30 min | 12:15 PM | Signal BOT-003 |
| BOT-003 | Chat CLI | 12:15 PM | 20 min | 12:35 PM | Signal BOT-004 |
| BOT-004 | Verify Tests | 12:35 PM | 15 min | 12:50 PM | DONE |

**READY FOR USER UAT: 12:50 PM**

---

## COMPLETION CRITERIA

- [ ] BOT-001: AnthropicService added, 5 tests PASS
- [ ] BOT-003: Chat CLI command added, 4 tests PASS
- [ ] BOT-004: 5 integration tests PASS + all unit tests still PASS
- [ ] No breaking changes
- [ ] Ready to test

---

## EXECUTION RULES

1. **NO optional features** - exact specs only
2. **NO refactoring** - just add code
3. **NO extra tests** - only what's listed
4. **All tests MUST pass** - no exceptions
5. **Signal when complete** - don't guess, verify
6. **Sequential execution** - don't start until previous finishes

---

## USER EXPECTATION

When complete, user will run:
```bash
deia chat
# Opens browser on port 8000
# Selects OpenAI bot → chats ✅
# Switches to Anthropic bot → chats ✅
# History preserved ✅
# All tests pass ✅
```

Then UAT begins to find and fix bugs.

---

**Q33N**
**STRICT FOCUS MODE ACTIVE**

**Execute. Report. Done.**
