# REAL TASK: Add AnthropicService to llm_service.py
**From:** Q33N
**To:** BOT-001
**Date:** 2025-10-26 11:30 AM CDT
**Priority:** P0 - BLOCKING
**Status:** Do this NOW

---

## What to do

Add AnthropicService class to `src/deia/services/llm_service.py`

**Pattern to follow:** Copy OpenAIService (lines 405-470), modify for Anthropic

**Changes:**
1. Import anthropic: `from anthropic import Anthropic, AsyncAnthropic`
2. Add AnthropicService class (follow OpenAIService pattern exactly)
3. Use environment variable `ANTHROPIC_API_KEY`
4. Support same methods: `chat()`, `chat_async()`, `chat_stream()`
5. Support Claude 3.5 Sonnet model

**Tests:**
- 5 basic tests (init, chat, stream, history, error handling)
- All must pass

**Time:** 30 minutes max

**Deliverable:** `.deia/hive/responses/deiasolutions/bot-001-anthropic-service-done.md`

Go now.
