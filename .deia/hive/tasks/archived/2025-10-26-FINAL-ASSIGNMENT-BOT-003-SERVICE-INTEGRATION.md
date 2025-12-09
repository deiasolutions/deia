# FINAL ASSIGNMENT: BOT-003 - Service Integration & Frontend

**Priority:** P0 (MVP-blocking)
**Time Estimate:** 45 minutes
**Status:** READY
**Depends On:** ServiceFactory cleanup (completed by Q33N)

---

## CONTEXT

The task endpoint has been refactored to use existing `create_llm_service()` factory. Now need to:
1. Test the endpoint works with different bot types
2. Update frontend ChatPanel to display bot type
3. Add service-specific handling in frontend (CLI vs API)

---

## OBJECTIVE

Enable frontend chat interface to:
- Display which bot type is being used
- Route messages correctly based on bot type
- Handle different response formats (API vs CLI)
- Show service-specific metadata

---

## PART 1: Verify Backend Task Endpoint (10 min)

Test that task endpoint works for all bot types:

```bash
# Test with existing registry bot
curl -X POST http://localhost:8000/api/bots \
  -H "Content-Type: application/json" \
  -d '{"action": "list"}'

# Should show registered bots including their bot_type in metadata
# Example response:
# {
#   "DEMO-BOT": {
#     "status": "ready",
#     "metadata": {"bot_type": "claude"},
#     "port": 8001
#   }
# }
```

**Verify:**
- ✅ GET /api/bots returns registered bots
- ✅ Each bot has `metadata.bot_type` set
- ✅ Bot types are one of: claude, chatgpt, claude-code, codex, llama

---

## PART 2: Update ChatPanel Frontend Component (20 min)

**File:** `src/deia/services/static/js/ChatPanel.js` or `src/deia/services/chat_interface.html`

**Change 1: Display Bot Type**

In the chat header, add bot type display:

```javascript
// In ChatPanel component or chat interface
async function updateBotInfo(botId) {
    // Get bot info from registry
    const response = await fetch(`/api/bot/${botId}`);
    const botInfo = await response.json();

    // Display bot type
    const botType = botInfo.metadata?.bot_type || 'unknown';
    document.getElementById('bot-type-display').textContent = `Bot: ${botId} (${botType})`;
}
```

**HTML:**
```html
<div id="chat-header">
    <h2 id="bot-type-display">Bot: (loading...)</h2>
</div>
```

**Change 2: Handle Service-Specific Messages**

```javascript
async function sendMessage(botId, message) {
    const botInfo = await fetch(`/api/bot/${botId}`).then(r => r.json());
    const botType = botInfo.metadata?.bot_type || 'claude';

    // Route to appropriate message handler
    if (['claude-code', 'codex'].includes(botType)) {
        // CLI services - show file operations
        return await sendCLITask(botId, message);
    } else {
        // API services - standard chat
        return await sendChatTask(botId, message);
    }
}

async function sendCLITask(botId, command) {
    const response = await fetch(`/api/bot/${botId}/task`, {
        method: 'POST',
        body: JSON.stringify({ command: command })
    });

    const result = await response.json();

    // CLI services return files_modified in response
    if (result.files_modified) {
        displayFileModifications(result.files_modified);
    }

    return result.response;
}

async function sendChatTask(botId, message) {
    const response = await fetch(`/api/bot/${botId}/task`, {
        method: 'POST',
        body: JSON.stringify({ command: message })
    });

    return await response.json();
}
```

---

## PART 3: Add Bot Type Selector (10 min)

Allow user to pick which bot type to launch:

**HTML:**
```html
<form id="launch-bot-form">
    <input type="text" id="bot-id" placeholder="Bot ID" required>

    <select id="bot-type">
        <option value="claude">Claude (Anthropic API)</option>
        <option value="chatgpt">ChatGPT (OpenAI API)</option>
        <option value="claude-code">Claude Code (CLI)</option>
        <option value="codex">Codex (CLI)</option>
        <option value="llama">LLaMA (Ollama)</option>
    </select>

    <button type="submit">Launch Bot</button>
</form>
```

**JavaScript:**
```javascript
document.getElementById('launch-bot-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const botId = document.getElementById('bot-id').value;
    const botType = document.getElementById('bot-type').value;

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
        alert(`Bot ${botId} (${botType}) launched!`);
        loadBotInfo(botId);
    } else {
        alert(`Failed: ${result.error}`);
    }
});
```

---

## PART 4: Update Message Display for Service Types (5 min)

Show service metadata in chat:

```javascript
async function displayMessage(message, isUser = false) {
    const botInfo = await fetch(`/api/bot/${currentBotId}`).then(r => r.json());
    const botType = botInfo.metadata?.bot_type || 'unknown';

    const messageDiv = document.createElement('div');
    messageDiv.className = isUser ? 'message user' : 'message assistant';

    // Add bot type badge for assistant messages
    if (!isUser) {
        const badge = document.createElement('span');
        badge.className = 'bot-type-badge';
        badge.textContent = botType;
        messageDiv.appendChild(badge);
    }

    messageDiv.textContent = message;
    document.getElementById('chat-messages').appendChild(messageDiv);
}
```

**CSS:**
```css
.bot-type-badge {
    display: inline-block;
    background: #007bff;
    color: white;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 0.85em;
    margin-right: 8px;
}

.message.assistant {
    background: #e7f3ff;
    border-left: 3px solid #007bff;
}

.message.user {
    background: #f0f0f0;
    border-left: 3px solid #666;
}
```

---

## PART 5: Run Tests (5 min)

Test the updated integration:

```bash
pytest tests/unit/test_chat_api_endpoints.py -v

# Should see:
# tests/unit/test_chat_api_endpoints.py::TestBotTaskEndpoint::test_send_bot_task_success PASSED
# tests/unit/test_chat_api_endpoints.py::TestBotTaskEndpoint::test_send_bot_task_empty_command PASSED
# tests/unit/test_chat_api_endpoints.py::TestBotTaskEndpoint::test_send_bot_task_bot_not_found PASSED
```

---

## CHECKLIST

- [ ] Task endpoint verified working for all 5 bot types
- [ ] ChatPanel displays bot type
- [ ] Bot type selector in frontend
- [ ] Service-specific message handling (CLI vs API)
- [ ] File modification display (for CLI services)
- [ ] Bot type badges shown in chat
- [ ] Tests passing
- [ ] Created completion report

---

## DELIVERABLES

When done, create: `.deia/hive/responses/deiasolutions/bot-003-service-integration-complete.md`

Write:
```markdown
# BOT-003: Service Integration Complete

**Status:** ✅ COMPLETE

- Frontend chat panel updated
- Bot type selector implemented
- All 5 bot types testable from UI
- Service-specific handling working
- Tests passing

Ready for E2E verification by BOT-004.
```

---

## SUCCESS CRITERIA

- ✅ Can select different bot types in frontend
- ✅ Chat displays which bot type is active
- ✅ Messages route to correct service (API vs CLI)
- ✅ CLI services show file modifications
- ✅ API services show chat responses
- ✅ Tests passing
- ✅ Completion report written

---

## NOTES

- Don't modify the backend task endpoint (already done by Q33N)
- Focus on frontend display and UX
- Use existing bot_type from registry metadata
- CLI services (claude-code, codex) behave differently - show results differently
- Keep it simple for MVP - can enhance later
