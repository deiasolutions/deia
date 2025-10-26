# Q33N PRIORITY LOCK - CORE WORK ONLY
**From:** Q33N (BEE-000 Queen)
**Date:** 2025-10-26 11:15 AM CDT
**Status:** 🔴 CRITICAL PRIORITY OVERRIDE
**Authority:** User Directive Override

---

## MISSION RESET

**ALL INFRASTRUCTURE WORK CANCELLED**
**ALL ADVANCED FEATURES PAUSED**
**ALL OTHER ASSIGNMENTS VOIDED**

---

## CORE MISSION (ONLY)

Get **Port 8000 Chat App** + **CLI Integration** complete with:
1. ✅ OpenAI bot (READY - needs testing)
2. ❌ Anthropic/Claude bot (MISSING - must build)
3. ❌ Chat CLI command (MISSING - must build)
4. ❌ Bot selector UI (MISSING - must build)
5. ❌ Multi-bot tests (MISSING - must build)

**WHEN COMPLETE:** User does UAT. Fix bugs until 100% working.

---

## BOT ASSIGNMENTS (CORE ONLY)

### BOT-001: ANTHROPIC SERVICE IMPLEMENTATION
**Task:** Build Anthropic/Claude LLM service

**Scope:**
- Implement `AnthropicService` class (extends `BaseLLMService`)
- Support streaming (async)
- Handle message history
- API key validation
- Error handling
- Unit tests (15+ tests, 100% pass)

**Deliverable:** `.deia/hive/responses/deiasolutions/bot-001-anthropic-service-complete.md`

**Estimated:** 120 minutes

**NO OTHER WORK**

---

### BOT-003: CLI CHAT COMMAND + BOT SELECTOR
**Task:** Build `deia chat` command and UI bot selector

**Scope:**
1. `deia chat` CLI command (launches FastAPI on port 8000)
2. HTML bot selector dropdown (OpenAI / Anthropic)
3. Bot switching in chat (maintains history per bot)
4. CLI integration with chat interface
5. Unit tests (20+ tests, 100% pass)

**Deliverable:** `.deia/hive/responses/deiasolutions/bot-003-chat-command-complete.md`

**Estimated:** 180 minutes

**NO OTHER WORK**

---

### BOT-004: INTEGRATION & E2E TESTS
**Task:** Build comprehensive tests for multi-bot chat

**Scope:**
1. E2E tests for chat flow (message send/receive)
2. Bot switching tests (history isolation)
3. Multi-bot message routing tests
4. API integration tests
5. CLI command tests
6. 40+ tests, 100% pass rate

**Deliverable:** `.deia/hive/responses/deiasolutions/bot-004-chat-e2e-tests-complete.md`

**Estimated:** 180 minutes

**NO OTHER WORK**

---

## QUEUE STATUS

**ALL OTHER TASKS:** PAUSED

**BOT-001:** 1 task (120 min)
**BOT-003:** 1 task (180 min)
**BOT-004:** 1 task (180 min)

**Total:** 480 minutes = **8 hours to complete core mission**

---

## EXECUTION RULES

1. **STOP all current work immediately**
2. **NO feature work until core complete**
3. **100% test coverage required**
4. **All unit tests must pass**
5. **Complete in 8 hours max**
6. **Then: User tests. Fix bugs until all green.**

---

## VERIFICATION CHECKPOINT

When complete, user will:
1. Open `deia chat`
2. Select OpenAI bot → chat works ✅
3. Switch to Anthropic bot → chat works ✅
4. Switch back → history preserved ✅
5. Run full test suite → 100% pass ✅

**Then UAT begins.**

---

**Q33N**
**Infrastructure Lead - DEIA Hive**
**Authority: User Directive Override**

**Status: CORE MISSION LOCKED**
