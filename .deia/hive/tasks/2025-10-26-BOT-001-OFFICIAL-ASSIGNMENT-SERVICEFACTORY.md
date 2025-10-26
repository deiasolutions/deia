# 🎯 BOT-001 - OFFICIAL ASSIGNMENT: ServiceFactory & Task Endpoint Routing

**FROM:** User (via Q33N)
**TO:** BOT-001
**DATE:** 2025-10-26 (APPROVED - This is now official work)
**PRIORITY:** P0 CRITICAL (MVP blocking)
**STATUS:** APPROVED - PROCEED NOW

---

## CONTEXT

You identified a critical gap: ServiceFactory + task endpoint routing is needed for BOT-004 to do proper E2E testing with real bot-type routing.

**User approved this work.** You now have official assignment to complete it.

---

## YOUR ASSIGNMENT

Complete the ServiceFactory implementation + task endpoint wiring so all 5 bot types (Claude, ChatGPT, Claude Code, Codex, LLaMA) route correctly to their services/adapters.

---

## WHAT TO DO

### Part 1: ServiceFactory Class
**File:** `src/deia/services/service_factory.py`

Create factory that maps bot_type → service instance:
- "claude" → AnthropicService
- "chatgpt" → OpenAIService
- "claude-code" → ClaudeCodeCLIAdapter
- "codex" → CodexCLIAdapter
- "llama" → OllamaService

Must have:
- `get_service(bot_type, bot_id, work_dir)` method
- `is_cli_service(bot_type)` helper
- `is_api_service(bot_type)` helper
- Proper error handling

### Part 2: Wire Task Endpoint
**File:** `src/deia/services/chat_interface_app.py`

Update `/api/bot/{bot_id}/task` endpoint to:
- Import ServiceFactory
- Use it to get correct service for bot_type
- Route CLI services → `send_task()` method
- Route API services → `chat()` method
- Handle both response types correctly
- Return proper response format

### Part 3: Update Tests
**File:** `tests/unit/test_chat_api_endpoints.py`

Ensure test_send_bot_task tests:
- ✅ API services (Claude, ChatGPT, LLaMA) work
- ✅ CLI services (Claude Code, Codex) work
- ✅ Proper response formatting for each type
- ✅ Mock services correctly (not using production code)

**Critical:** Tests must NOT rely on mocks that hide real behavior. They should verify routing logic.

---

## SUCCESS CRITERIA

- [ ] ServiceFactory class created
- [ ] Maps all 5 bot types correctly
- [ ] Task endpoint uses ServiceFactory
- [ ] Tests verify routing (not just mocks passing)
- [ ] `pytest tests/unit/test_chat_api_endpoints.py` passes
- [ ] All 5 bot types can be routed (API + CLI both)
- [ ] Completion report submitted

---

## DELIVERABLE

**File:** `.deia/hive/responses/deiasolutions/bot-001-servicefactory-complete.md`

```markdown
# BOT-001: ServiceFactory Complete

Status: ✅ COMPLETE
Time: X minutes
Issues: [None / describe]

What was built:
- ServiceFactory class with routing logic
- Task endpoint integration
- Support for all 5 bot types (Claude, ChatGPT, Claude Code, Codex, LLaMA)

Tests:
- [Test results: X/X passing]
- [Any issues found]

Quality:
- [Tests verify real routing, not just mocks]
- [Both API and CLI services working]

Ready for: BOT-004 E2E verification

Notes: [Any relevant notes]
```

---

## TIMELINE

**Start:** Now
**Duration:** ~45 minutes
**Blocker for:** BOT-004 E2E testing (can't proceed without this)
**Expected done:** ~16:15

---

## KEY POINTS

✅ This is OFFICIAL work - you have approval
✅ BOT-004 is blocked waiting for this
✅ Tests must be real (not just passing mocks)
✅ All 5 bot types must route correctly
✅ Report completion when done

**Execute this. Get tests green. Unblock BOT-004.** 🚀

---

## REMINDER: THE GOVERNANCE RULE

For future work:
- ✅ Identify gaps
- ✅ Propose work ("I think we need X")
- ✅ **WAIT for approval**
- ✅ Then execute

Don't execute without approval. Propose first. 👍

---

**This assignment is APPROVED. Proceed now.** ✅
