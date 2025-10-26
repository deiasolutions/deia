# CORE MISSION TASK: Anthropic/Claude LLM Service
**From:** Q33N (BEE-000 Queen)
**To:** BOT-001 (CLAUDE-CODE-001)
**Date:** 2025-10-26 11:15 AM CDT
**Priority:** P0 - CORE MISSION
**Status:** BLOCKING - Do not start other work

---

## MISSION CRITICAL

Build Anthropic/Claude LLM service to enable bot selection in chat app.

**This is the blocker for UAT.** Chat app needs two working bots (OpenAI ✅ + Anthropic ❌).

---

## Task Requirements

**Create:** `AnthropicService` class in `src/deia/services/llm_service.py`

**Must support:**
1. Anthropic API client initialization
2. Chat messages (sync + async)
3. Streaming responses (async generator)
4. Conversation history management
5. Error handling (invalid keys, rate limits, timeouts)
6. Message validation

**Requirements:**
- Extends `BaseLLMService` (already exists, follow OpenAIService pattern)
- Supports Claude 3.5 Sonnet (latest Anthropic model)
- API key from environment: `ANTHROPIC_API_KEY`
- Graceful degradation if API key missing
- Proper error messages

**Tests required:**
- ✅ Service initialization
- ✅ Chat (sync) message handling
- ✅ Streaming response
- ✅ Conversation history
- ✅ Invalid API key handling
- ✅ Token limit enforcement
- ✅ Error recovery
- ✅+ 8 more (15 total, 100% pass)

---

## Acceptance Criteria

- [ ] AnthropicService class created and functional
- [ ] Extends BaseLLMService correctly
- [ ] Chat (sync) method works
- [ ] Chat stream (async) method works
- [ ] Conversation history tracked
- [ ] Error handling comprehensive
- [ ] 15+ unit tests, 100% passing
- [ ] No breaking changes to existing OpenAI/Ollama services
- [ ] Code review ready

---

## Deliverable

`.deia/hive/responses/deiasolutions/bot-001-anthropic-service-complete.md`

**Estimated Time:** 120 minutes

---

## CRITICAL NOTES

1. **Do NOT** start other work until this is complete
2. **Use existing OpenAI service as reference** - pattern should match
3. **All tests must pass** before completion
4. **Follow existing code style** in llm_service.py
5. **No optional features** - core only

---

**GO. BLOCKING WORK - CORE MISSION.**
