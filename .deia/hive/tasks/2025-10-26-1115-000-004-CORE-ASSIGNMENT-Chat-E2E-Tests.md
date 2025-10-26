# CORE MISSION TASK: Chat E2E Tests & Verification
**From:** Q33N (BEE-000 Queen)
**To:** BOT-004 (CLAUDE-CODE-004)
**Date:** 2025-10-26 11:15 AM CDT
**Priority:** P0 - CORE MISSION
**Status:** BLOCKING - Waits for BOT-001 + BOT-003

---

## MISSION CRITICAL

Build comprehensive E2E test suite for complete chat workflow with multi-bot support.

**This validates the entire system is ready for user UAT.**

---

## Task Requirements

**Create comprehensive test suite** in `tests/e2e/test_chat_e2e.py`

### Test Categories

#### 1. Chat Flow Tests (8 tests)
- ✅ User connects to chat
- ✅ Send message to OpenAI bot
- ✅ Receive response from OpenAI
- ✅ Message appears in history
- ✅ Send message to Anthropic bot
- ✅ Receive response from Anthropic
- ✅ Bot selector renders correctly
- ✅ Switch between bots works

#### 2. Bot Switching Tests (8 tests)
- ✅ Select OpenAI → history empty
- ✅ Send message, history populated
- ✅ Switch to Anthropic → new history
- ✅ Back to OpenAI → original history preserved
- ✅ Switch multiple times → histories isolated
- ✅ Context maintained per bot
- ✅ Timestamps correct per switch
- ✅ No crosstalk between histories

#### 3. API Integration Tests (8 tests)
- ✅ OpenAI service called correctly
- ✅ Anthropic service called correctly
- ✅ Message payloads correct
- ✅ Response parsing works
- ✅ Streaming responses handled
- ✅ Error responses handled
- ✅ API timeouts handled
- ✅ Missing API keys handled gracefully

#### 4. CLI Integration Tests (8 tests)
- ✅ `deia chat` command launches
- ✅ Server listens on correct port
- ✅ Browser opens (when requested)
- ✅ Shutdown graceful
- ✅ Port conflict detected
- ✅ Custom port works
- ✅ --no-open-browser flag respected
- ✅ Connection persists across refreshes

#### 5. Data Integrity Tests (8 tests)
- ✅ No message loss
- ✅ History survives bot switch
- ✅ Timestamps accurate
- ✅ User role correct
- ✅ Assistant role correct
- ✅ System prompts not leaked
- ✅ API keys not in logs/responses
- ✅ Concurrent users isolated

---

## Acceptance Criteria

- [ ] 40+ unit/integration tests created
- [ ] 100% pass rate
- [ ] All categories covered (chat, switching, API, CLI, integrity)
- [ ] Tests use fixtures for bot setup
- [ ] Mocked external APIs (OpenAI, Anthropic)
- [ ] Clear test names and documentation
- [ ] Coverage report 90%+
- [ ] No flaky tests
- [ ] Ready for CI/CD

---

## Testing Approach

**Fixtures (required):**
- Chat app instance (FastAPI TestClient)
- OpenAI service mock
- Anthropic service mock
- Test WebSocket client
- Pre-populated histories

**Tools:**
- pytest (existing)
- pytest-asyncio (for async tests)
- unittest.mock (for API mocking)
- FastAPI TestClient

**Test structure:**
```python
tests/
  e2e/
    test_chat_e2e.py
    conftest.py  # Fixtures
```

---

## Deliverable

`.deia/hive/responses/deiasolutions/bot-004-chat-e2e-tests-complete.md`

**Must include:**
- Test results (40+ passing)
- Coverage report
- Test execution time
- Any known limitations

**Estimated Time:** 180 minutes

---

## DEPENDENCIES

- **Waits for:** BOT-001 (Anthropic service) + BOT-003 (CLI command)
- **Then:** Start this task
- **Sequential execution:** BOT-001 → BOT-003 → BOT-004

---

## CRITICAL NOTES

1. **Do NOT** start until BOT-001 AND BOT-003 complete
2. **Use mocks for external APIs** - don't call real OpenAI/Anthropic
3. **All tests MUST pass** before marking complete
4. **40+ tests minimum** for comprehensive coverage
5. **Verify user flow works end-to-end**

---

**WAIT for BOT-001 + BOT-003, then GO. FINAL CORE TASK.**

---

After this completes: **USER DOES UAT. Fix bugs until 100% working.**
