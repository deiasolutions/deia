# 🎯 BOT-003 - OFFICIAL MVP ASSIGNMENT (ONLY TASK)

**FROM:** Q33N (Coordinator)
**TO:** BOT-003
**DATE:** 2025-10-26 15:30
**PRIORITY:** P0 - BLOCKING MVP
**STATUS:** ✅ READY TO START NOW

---

## ⚠️ CRITICAL INSTRUCTION

**IGNORE ALL OTHER TASKS** assigned to you from earlier today.

You have been assigned MANY tasks:
- REST API Builder (ARCHIVED - do NOT work on)
- Advanced Search (ARCHIVED - do NOT work on)
- GraphQL Integration (ARCHIVED - do NOT work on)
- Caching Layer (ARCHIVED - do NOT work on)
- Encryption Toolkit (ARCHIVED - do NOT work on)
- Stream Processing (ARCHIVED - do NOT work on)
- Workflow Orchestration (ARCHIVED - do NOT work on)
- API Gateway (ARCHIVED - do NOT work on)
- Data Validation (ARCHIVED - do NOT work on)
- Browser Testing (ARCHIVED - do NOT work on)
- Chat CLI (ARCHIVED - do NOT work on)

**ALL OF THOSE ARE ARCHIVED AND REMOVED FROM YOUR ACTIVE TASKS.**

---

## YOUR ONLY JOB FOR TODAY

Focus 100% on this one task until it's complete:

### **Service Integration & Frontend Chat Interface**

**What you need to do:**

1. **Update ChatPanel Frontend (20 min)**
   - Add bot type selector dropdown
   - Display current bot type in header
   - Show which bot is connected

2. **Handle Service-Specific Responses (15 min)**
   - API services (Claude, ChatGPT, LLaMA) return chat text
   - CLI services (Claude Code, Codex) return file modifications
   - Display responses appropriately for each type

3. **Add Bot Type Badges (5 min)**
   - Show bot type badge in each chat message
   - Color-code by service type

4. **Test (5 min)**
   - Run: `pytest tests/unit/test_chat_api_endpoints.py -v`
   - Verify tests pass

5. **Write Completion Report (5 min)**
   - Create: `.deia/hive/responses/deiasolutions/bot-003-mvp-complete.md`
   - Document what was done

---

## DETAILED IMPLEMENTATION GUIDE

### PART 1: Frontend Bot Type Selector

**File:** `src/deia/services/chat_interface.html` (or your chat UI file)

Add this to the HTML form:

```html
<div id="launch-controls">
    <input type="text" id="bot-id" placeholder="Bot ID (e.g., TEST-CLAUDE)" required>

    <select id="bot-type" required>
        <option value="">-- Select Bot Type --</option>
        <option value="claude">Claude (Anthropic API)</option>
        <option value="chatgpt">ChatGPT (OpenAI API)</option>
        <option value="claude-code">Claude Code (CLI)</option>
        <option value="codex">Codex (CLI)</option>
        <option value="llama">LLaMA (Ollama)</option>
    </select>

    <button type="button" id="launch-btn">Launch Bot</button>
</div>

<div id="chat-header">
    <h2 id="bot-info">No bot connected</h2>
</div>
```

### PART 2: JavaScript to Launch & Display

```javascript
document.getElementById('launch-btn').addEventListener('click', async () => {
    const botId = document.getElementById('bot-id').value.trim();
    const botType = document.getElementById('bot-type').value;

    if (!botId || !botType) {
        alert('Please enter Bot ID and select Bot Type');
        return;
    }

    try {
        const response = await fetch('/api/bot/launch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                bot_id: botId,
                bot_type: botType,
                token: 'dev-token-12345'
            })
        });

        const result = await response.json();

        if (result.success) {
            // Update header with bot info
            document.getElementById('bot-info').textContent = `Bot: ${botId} (${botType}) - Ready`;
            document.getElementById('bot-info').style.color = 'green';

            // Store current bot
            window.currentBot = { id: botId, type: botType };

            alert(`✅ ${botId} (${botType}) launched!`);
        } else {
            alert(`❌ Failed: ${result.error}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
});
```

### PART 3: Send Messages

```javascript
async function sendMessage(message) {
    if (!window.currentBot) {
        alert('No bot connected');
        return;
    }

    try {
        const response = await fetch(`/api/bot/${window.currentBot.id}/task`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: message })
        });

        const result = await response.json();

        if (result.success) {
            // Display response
            displayChatMessage(result.response, false, window.currentBot.type);
        } else {
            displayChatMessage(`Error: ${result.error}`, false);
        }
    } catch (error) {
        displayChatMessage(`Error: ${error.message}`, false);
    }
}

function displayChatMessage(text, isUser, botType = 'unknown') {
    const messageDiv = document.createElement('div');
    messageDiv.className = isUser ? 'message user' : 'message assistant';

    if (!isUser) {
        const badge = document.createElement('span');
        badge.className = 'bot-type-badge';
        badge.textContent = botType;
        messageDiv.appendChild(badge);
    }

    const textSpan = document.createElement('span');
    textSpan.textContent = text;
    messageDiv.appendChild(textSpan);

    document.getElementById('messages').appendChild(messageDiv);
}
```

### PART 4: CSS Styling

```css
.bot-type-badge {
    display: inline-block;
    background: #007bff;
    color: white;
    padding: 4px 10px;
    border-radius: 3px;
    font-size: 0.85em;
    margin-right: 8px;
    font-weight: bold;
}

.message {
    padding: 12px;
    margin: 8px 0;
    border-radius: 4px;
    border-left: 3px solid #ccc;
}

.message.user {
    background: #f0f0f0;
    border-left-color: #666;
    text-align: right;
}

.message.assistant {
    background: #e7f3ff;
    border-left-color: #007bff;
}

#bot-info {
    padding: 10px;
    background: #f9f9f9;
    border-radius: 4px;
    font-size: 1em;
}
```

---

## TESTING

Run this command to verify tests pass:

```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions
pytest tests/unit/test_chat_api_endpoints.py::TestBotTaskEndpoint -v
```

Expected result: **All tests PASS**

---

## COMPLETION CHECKLIST

- [ ] Bot type selector added to frontend
- [ ] Can launch different bot types from UI
- [ ] Chat header displays current bot type
- [ ] Messages show bot type badge
- [ ] Different response handling for CLI vs API services
- [ ] Tests passing
- [ ] Completion report written
- [ ] Ready for BOT-004 verification

---

## DELIVERABLE

When done, create this file:

**File:** `.deia/hive/responses/deiasolutions/bot-003-mvp-complete.md`

**Content:**
```markdown
# BOT-003: Service Integration MVP Complete

**Date:** [TODAY]
**Status:** ✅ COMPLETE

## What was done:
- ✅ Bot type selector added
- ✅ Frontend displays active bot type
- ✅ Service-specific response handling
- ✅ Bot type badges in chat
- ✅ Tests passing

## Ready for:
- E2E verification by BOT-004
- MVP deployment

## Notes:
[Add any notes about what you did]
```

---

## TIME BUDGET

Total: **50 minutes**
- Frontend update: 20 min
- Response handling: 15 min
- Styling: 5 min
- Tests: 5 min
- Documentation: 5 min

---

## SUCCESS CRITERIA

✅ User can select bot type in UI
✅ User can launch different bot types
✅ Chat displays which bot is active
✅ Responses show appropriately
✅ Tests pass
✅ Report written

---

## IF YOU GET STUCK

1. Check the backend endpoint: `curl http://localhost:8000/api/bots`
2. Test task endpoint: `curl -X POST http://localhost:8000/api/bot/TEST-BOT/task -H "Content-Type: application/json" -d '{"command": "hello"}'
3. Look at test file for examples: `tests/unit/test_chat_api_endpoints.py`
4. Ask Q33N for clarification

---

## IGNORE EVERYTHING ELSE

This is your ONLY task.
No REST API work.
No other features.
Just this.

**Start now. Report completion when done.**

---

**You've got this! Let's ship the MVP.** 🚀
