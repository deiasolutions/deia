# URGENT TASK: BOT-003 - Fix Chat History Persistence Bug

**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-003 (Chat Controller)
**Date:** 2025-10-25 20:52 CDT
**Priority:** P0 - CRITICAL / BLOCKING
**Status:** STOP CURRENT WORK - FIX NOW

---

## THE PROBLEM (Reported by Dave)

**Chat history disappears when switching between bots.**

- User selects Bot A → sees conversation history
- User switches to Bot B → sees Bot B conversation
- User switches back to Bot A → **BOT A HISTORY IS GONE**

**This is broken.** History should persist per-bot and restore instantly.

---

## YOUR MISSION

**STOP Sprint 2.2 multi-session work immediately.**

**Focus 100% on fixing this NOW:**

1. **Root cause analysis** (5 min)
   - Is history being saved per-bot or globally?
   - Is `loadChatHistory()` filtering by `bot_id`?
   - Is history being cleared on bot switch?
   - Check browser console for JavaScript errors

2. **Fix the bug** (15-30 min expected)
   - Ensure history loads with bot_id filter from JSONL
   - Append previous bot's history to DOM (don't replace)
   - Call `loadChatHistory()` when bot selection changes
   - Verify session storage not clearing history

3. **Test the fix** (10 min)
   - Launch 3 bots
   - Send message to Bot A
   - Switch to Bot B, send message
   - Switch to Bot C, send message
   - Switch back to Bot A → **history must be there**
   - Repeat switches → history must persist every time

4. **Report when done**
   - Update `bot-003-sprint-2-status.md` with fix
   - Show test evidence (screenshots or logs)
   - Confirm: All 3 bots' histories persist correctly

---

## Why This Matters

Dave is testing the controller **right now** and seeing broken behavior. This is production-blocking.

**Definition of Done for Sprint 2.1:**
- ✅ Code written
- ✅ Tests pass
- ✅ **History actually persists** ← YOU'RE FAILING THIS RIGHT NOW

---

## Your Code (Sprint 2.1)

**Location:** `llama-chatbot/app.py`

**Check these functions:**
- `loadChatHistory()` - Lines 517-592
- Bot selection change handler - Look for where bot switches
- Message save on send - Ensure bot_id is saved
- History JSONL format - Ensure it's per-bot keyed

**The bug is in your code. You wrote it. Fix it.**

---

## Timeline

- **Right now:** Debug (5 min)
- **Next:** Fix (15-30 min)
- **Then:** Test (10 min)
- **Total:** < 1 hour to resolve

After fix verified, resume Sprint 2.2 multi-session work.

---

## Dave's Feedback

"GFN go fix now"

That's your directive.

---

**Q33N out. STOP. FIX. REPORT.**

This is not a normal task. This is a blocker. Go.

---

**Timestamp:** 2025-10-25 20:52 CDT
**Escalation:** Dave directly observing chat controller behavior
**Status:** AWAITING FIX
