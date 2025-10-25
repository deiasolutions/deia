# Q33N DIAGNOSIS: Chat History Bug Root Cause + Fix

**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-003 (Chat Controller)
**Date:** 2025-10-25 20:55 CDT
**Priority:** P0 - CRITICAL BLOCKER
**SLA:** 30 min fix deadline

---

## ROOT CAUSE IDENTIFIED

The chat history disappears when switching bots because of **two connected bugs** in your code:

### Bug #1: Browser DOM Cleared on Bot Switch (Line 511)

**File:** `llama-chatbot/app.py` lines 506-515

```javascript
function selectBot(botId) {
    selectedBotId = botId;
    selectedBotInfo.textContent = `Talking to: ${botId}`;
    chatInput.disabled = false;
    sendButton.disabled = false;
    chatMessages.innerHTML = '';  // ← THIS CLEARS ALL MESSAGES
    addMessage('assistant', `Connected to ${botId}. Ready for commands.`);
    loadChatHistory();
    refreshBotList();
}
```

**Problem:** `chatMessages.innerHTML = ''` wipes everything. Then `loadChatHistory()` tries to restore, but...

### Bug #2: History Endpoint Doesn't Filter by Bot ID (Line 520)

**File:** `llama-chatbot/app.py` lines 518-541

```javascript
async function loadChatHistory() {
    try {
        const response = await fetch('/api/chat/history?limit=100');  // ← NO BOT_ID FILTER
        const data = await response.json();

        if (data.messages && data.messages.length > 0) {
            // Clear current messages and reload history
            const messageElements = chatMessages.querySelectorAll('.message:not(.assistant)');
            messageElements.forEach(el => el.remove());

            // Load historical messages
            data.messages.forEach(msg => {
                displayHistoryMessage(msg);
            });
```

**Problem:** When you load history, you're not telling the backend "give me history for Bot A". It returns all messages or the last ones, mixing bots together.

---

## THE FIX (30 minutes)

### Fix #1: Pass bot_id to history fetch

Change line 520 from:
```javascript
const response = await fetch('/api/chat/history?limit=100');
```

To:
```javascript
const response = await fetch(`/api/chat/history?bot_id=${selectedBotId}&limit=100`);
```

### Fix #2: Backend endpoint must filter by bot_id

Find your backend `/api/chat/history` endpoint and ensure it:
1. Accepts `bot_id` query parameter
2. Filters JSONL messages by `bot_id` before returning
3. Returns only messages for that bot

**Check around line 702-720** in your backend where you implemented history endpoints.

The endpoint should look like:
```python
@app.get("/api/chat/history")
async def get_chat_history(bot_id: str, limit: int = 100, offset: int = 0):
    # Load chat-history-{date}.jsonl
    # Filter messages where msg['bot_id'] == bot_id
    # Return paginated results
```

### Fix #3: Don't clear welcome message initially

Consider showing the welcome message AFTER loading history, or append rather than replace.

---

## TESTING THE FIX

1. **Start 3 bots** (Bot A, Bot B, Bot C)
2. **Send message to Bot A** → See it in chat
3. **Switch to Bot B** → Send message → See Bot B message
4. **Switch to Bot C** → Send message → See Bot C message
5. **Switch back to Bot A** → **Bot A message must be there**
6. **Switch to Bot B** → **Bot B message must be there**
7. **Repeat 5-6** → All histories must persist

If any bot's history is missing, you haven't fully isolated by bot_id.

---

## TIME BUDGET

- **Diagnosis & code review:** 5 min
- **Frontend fix (pass bot_id):** 5 min
- **Backend fix (filter by bot_id):** 10 min
- **Testing (3 bots, switching):** 10 min
- **Total:** 30 minutes max

**If you get stuck:** Escalate with specific error message within 15 min.

---

## WHAT TO DELIVER

When fixed, update `bot-003-sprint-2-status.md`:
- ✅ Chat history now persists per-bot
- ✅ Switching bots restores their history
- ✅ Test evidence (screenshots or logs showing 3-bot switch test)
- ✅ Code locations of fixes

---

## THEN CONTINUE

After fix verified:
- Test server is running ✓
- History persists ✓
- Move immediately to Sprint 2.2 (Multi-session support) - queued and ready

No idle time. You have Task 2 waiting.

---

**Q33N out. You have the diagnosis. 30 min to fix. Go.**

**Time start:** 2025-10-25 20:55 CDT
**Time due:** 2025-10-25 21:25 CDT
