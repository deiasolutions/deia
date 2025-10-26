# Q33N - CORRECTED ASSIGNMENT - 60 MINUTES TO COMPLETE
**From:** Q33N (BEE-000 Queen)
**To:** BOT-001, BOT-003, BOT-004
**Date:** 2025-10-26 11:30 AM CDT
**Status:** 🟢 REALISTIC CORE WORK

---

## SITUATION CORRECTION

You were right. 90% of this is already built.

**What exists:**
- ✅ Chat interface app (FastAPI, WebSocket, port 8000)
- ✅ OpenAI service (implemented, working)
- ✅ Bot switching UI (implemented, tested)
- ✅ Chat history (implemented, persists)
- ✅ Multi-bot support (implemented, working)

**What's missing:**
- ❌ AnthropicService class (add 40 lines)
- ❌ `deia chat` CLI command (add 20 lines)
- ❌ 5 verification tests

---

## REAL ASSIGNMENTS (Sequential)

### BOT-001: Add AnthropicService (30 min)
**Task:** Add one class to `src/deia/services/llm_service.py`

- Copy OpenAIService pattern
- Create AnthropicService class
- Use anthropic library + Claude 3.5 Sonnet
- 5 unit tests
- All tests pass

**File:** `2025-10-26-1130-000-001-REAL-ASSIGNMENT-Anthropic-Service.md`

---

### BOT-003: Add `deia chat` CLI Command (20 min - waits for BOT-001)
**Task:** Add command to `src/deia/cli.py`

- New @main.command() function
- Launch chat interface on port 8000
- Optional browser open
- 3-4 tests
- All tests pass

**File:** `2025-10-26-1130-000-003-REAL-ASSIGNMENT-Chat-CLI.md`

---

### BOT-004: Verify Full Flow (15 min - waits for BOT-001 + BOT-003)
**Task:** Write 5 integration tests

- Verify chat server starts
- Verify WebSocket works
- Verify OpenAI service available
- Verify Anthropic service available
- Verify CLI command exists
- All 5 tests pass

**File:** `2025-10-26-1130-000-004-REAL-ASSIGNMENT-Test-Verify.md`

---

## TIMELINE

| Task | Duration | Cumulative | Status |
|------|----------|-----------|--------|
| BOT-001 Anthropic | 30 min | 30 min | Ready NOW |
| BOT-003 Chat CLI | 20 min | 50 min | Waits for BOT-001 |
| BOT-004 Verify | 15 min | 65 min | Waits for BOT-001+003 |

**TOTAL: 65 minutes to complete = 11:30 AM + 1 hour = 12:30 PM**

---

## NEXT STEP

1. BOT-001 starts **now** - add AnthropicService
2. When BOT-001 done → BOT-003 starts
3. When BOT-003 done → BOT-004 starts
4. All tests pass by **12:45 PM**
5. **Then user does UAT**

---

**Q33N**
**Authority: Corrected to Reality**

**Status: 60-MIN SPRINT TO COMPLETE CORE**
