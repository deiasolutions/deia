# ISSUE LOG: Chat History Not Persisting Between Bot Switches

**Reported By:** Dave (daaaave-atx)
**Reported At:** 2025-10-25 20:52 CDT
**Severity:** HIGH (affects user experience, data loss)
**Status:** LOGGED - AWAITING INVESTIGATION

---

## Issue Description

When switching between bots in the chat controller:
- Bot A has conversation history visible
- Switch to Bot B
- Switch back to Bot A
- **Chat history for Bot A is gone**

**Expected behavior:** Chat history should persist per-bot and restore when switching back

**Actual behavior:** History drops/clears when switching bots

---

## Impact

- Messages disappear between bot switches
- No historical context restoration
- User loses conversation thread when multitasking between bots
- Violates Sprint 2.1 requirement: "Messages survive page refresh, history loads fast"

---

## Investigation Needed

**Questions for BOT-003:**
1. Is chat history being saved per-bot or globally?
2. When switching bots, is the previous bot's history being restored from storage?
3. Is the history endpoint (`GET /api/chat/history`) being called on bot switch?
4. Are there JavaScript console errors on bot switch?

**Technical areas to check:**
- `loadChatHistory()` function - is it filtering by bot_id?
- Session storage - is it being cleared on bot switch?
- Message display - is previous history being appended to DOM or replaced?
- Storage format - is history keyed by bot_id in JSONL?

---

## Next Steps

1. **BOT-003 investigation:** Debug chat history restoration on bot switch
2. **Root cause:** Likely history loading not filtering by active bot
3. **Fix:** Ensure history loads with bot_id filter, appends to existing chat
4. **Verification:** Test switching between 3 bots, confirm history persists for each

---

## Queue Impact

This may require:
- Sprint 2.1 revisit (chat history fix)
- OR: Task 2 (multi-session) implementation handles this

**Note:** Sprint 2.1 was code-complete but testing was blocked by port issue. This issue may have existed in code but not yet tested.

---

**Logged in Q33N session for escalation if needed.**

**Assigned to:** BOT-003 investigation
**SLA:** Identify root cause within 1 hour
