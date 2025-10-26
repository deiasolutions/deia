# BOT-004 Code Fix Priority Sequence

**Date:** 2025-10-25
**Target:** Production-ready chat in minimum time
**Strategy:** Dependency-based execution

---

## Execution Sequence (Optimal Order)

### PHASE 1: ENABLE BASIC CHAT (30-45 minutes)

**Goal:** Users can launch bot, select it, type, and see it works

#### Task 1: Fix Input Field Enable/Disable (15 min)
**Why first:** Unblocks testing of other fixes
**File:** `llama-chatbot/static/js/components/BotLauncher.js` (Line 398)

**Current:**
```javascript
<input type="text" id="chatInput" class="chat-input"
       placeholder="..." disabled>  // ← ALWAYS DISABLED
```

**Fix:**
```javascript
// In BotLauncher.js, add:
function enableInput() {
  document.getElementById('chatInput').disabled = false;
  document.getElementById('chatInput').focus();
}

function disableInput() {
  document.getElementById('chatInput').disabled = true;
}

// Call enableInput() when bot is selected
// Call disableInput() when no bot selected
```

**Status:** ✅ CRITICAL - unblocks testing
**Est time:** 15 minutes

---

#### Task 2: Implement selectBot() Function (15 min)
**Why second:** Lets users actually select a bot to chat with
**File:** Same file (BotLauncher.js)

**Current:**
```javascript
// Line 496: Called but never defined
// <button onclick="selectBot('${botId}')">Select</button>
```

**Fix:**
```javascript
function selectBot(botId) {
  // Store selected bot
  window.selectedBotId = botId;

  // Update UI to show selection
  document.querySelectorAll('.bot-item').forEach(item => {
    item.classList.remove('selected');
  });
  document.querySelector(`[data-bot-id="${botId}"]`).classList.add('selected');

  // Enable input field for this bot
  enableInput();

  // Update status display
  updateBotStatus(botId);
}

// Add to HTML: data-bot-id attribute to bot items
```

**Status:** ✅ CRITICAL - enables core workflow
**Est time:** 15 minutes

---

#### Task 3: Replace prompt() with Proper Input (15 min)
**Why third:** Better UX for bot launch
**File:** BotLauncher.js (Line 431-454)

**Current:**
```javascript
async function launchBot() {
    const botId = prompt('Enter Bot ID (e.g., BOT-001):');
    // ← Janky browser dialog
}
```

**Fix:**
```javascript
// Add HTML input field to page:
<div class="bot-launch-form">
  <input type="text" id="botIdInput" placeholder="Enter Bot ID (e.g., BOT-001)">
  <button onclick="launchBotWithInput()">Launch</button>
</div>

// Replace launchBot():
async function launchBotWithInput() {
  const botId = document.getElementById('botIdInput').value.trim();

  if (!botId) {
    showError('Bot ID required');
    return;
  }

  if (!/^[A-Z0-9\-]+$/.test(botId)) {
    showError('Invalid Bot ID format');
    return;
  }

  try {
    const response = await fetch('/api/bot/launch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bot_id: botId })
    });

    if (!response.ok) throw new Error('Launch failed');
    const data = await response.json();

    refreshBotList();
    showSuccess(`Bot ${botId} launched on port ${data.port}`);
  } catch(e) {
    showError(`Failed to launch bot: ${e.message}`);
  }
}
```

**Status:** ✅ CRITICAL - improves UX
**Est time:** 15 minutes

---

### PHASE 2: ENABLE REAL-TIME CHAT (45-60 minutes)

**Goal:** Messages send and receive in real-time via WebSocket

#### Task 4: Initialize WebSocket Connection (20 min)
**Why fourth:** Enables real-time messaging
**File:** BotLauncher.js (Line 1064, currently just `let ws = null`)

**Current:**
```javascript
let ws = null;  // ← Created but never initialized
```

**Fix:**
```javascript
function initWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws`;

  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log('WebSocket connected');
    document.getElementById('connectionStatus').textContent = 'Connected';
    document.getElementById('connectionStatus').className = 'status-online';
  };

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    handleWebSocketMessage(message);
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
    document.getElementById('connectionStatus').textContent = 'Disconnected';
    document.getElementById('connectionStatus').className = 'status-offline';
  };

  ws.onclose = () => {
    console.log('WebSocket closed');
    document.getElementById('connectionStatus').textContent = 'Disconnected';
    document.getElementById('connectionStatus').className = 'status-offline';
  };
}

// Call on page load
document.addEventListener('DOMContentLoaded', () => {
  initWebSocket();
});
```

**Status:** ✅ CRITICAL - enables real-time
**Est time:** 20 minutes

---

#### Task 5: Handle WebSocket Messages (15 min)
**Why after websocket init:** Processes incoming messages
**File:** BotLauncher.js (add new function)

**Fix:**
```javascript
function handleWebSocketMessage(message) {
  const { type, bot_id, content, success } = message;

  if (type === 'response') {
    // Bot sent a response
    addMessage({
      sender: bot_id,
      content: content,
      timestamp: new Date(),
      isBot: true
    });
    hideTypingIndicator();
  } else if (type === 'typing') {
    // Bot is typing
    showTypingIndicator(`${bot_id} is typing...`);
  } else if (type === 'error') {
    // Error occurred
    addMessage({
      sender: 'System',
      content: `Error: ${content}`,
      timestamp: new Date(),
      isBot: false
    });
    hideTypingIndicator();
  }
}
```

**Status:** ✅ CRITICAL - makes WebSocket useful
**Est time:** 15 minutes

---

#### Task 6: Send Messages via WebSocket (15 min)
**Why after websocket init:** Users can actually send messages
**File:** BotLauncher.js (replace REST API call)

**Current:**
```javascript
// Currently uses REST API
const response = await session.post(...)
```

**Fix:**
```javascript
async function sendMessage() {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();

  if (!message) return;
  if (!window.selectedBotId) {
    showError('No bot selected');
    return;
  }

  // Show user's message immediately
  addMessage({
    sender: 'You',
    content: message,
    timestamp: new Date(),
    isBot: false
  });

  input.value = '';

  // Send via WebSocket
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      type: 'command',
      bot_id: window.selectedBotId,
      command: message
    }));

    showTypingIndicator(`${window.selectedBotId} is processing...`);
  } else {
    // Fallback to REST API if WebSocket unavailable
    sendMessageViaREST(message);
  }
}

// Listen for Enter key
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('chatInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });
});
```

**Status:** ✅ CRITICAL - core chat functionality
**Est time:** 15 minutes

---

### PHASE 3: MESSAGE FEEDBACK (20-30 minutes)

**Goal:** Users see clear success/failure indication

#### Task 7: Fix Message Routing Feedback (10 min)
**Why after WebSocket:** Improves message reliability indication
**File:** Python backend `app.py` message routing

**Current:**
```python
return {
    "success": True,  # ← ALWAYS TRUE EVEN ON ERRORS
    "response": response_text,
    "bot_id": bot_id
}
```

**Fix:**
```python
async def send_command(request):
    bot_id = request.json.get('bot_id')
    command = request.json.get('command')

    if not bot_id or not command:
        return JSONResponse({
            "success": False,
            "error": "bot_id and command required",
            "bot_id": bot_id
        }, status_code=400)

    # Check if bot exists and is running
    bot_port = get_bot_port(bot_id)
    if not bot_port:
        return JSONResponse({
            "success": False,
            "error": f"Bot {bot_id} not running",
            "bot_id": bot_id
        }, status_code=404)

    try:
        response = await send_to_bot(bot_port, command, timeout=30)
        return {
            "success": True,
            "response": response,
            "bot_id": bot_id,
            "timestamp": datetime.now().isoformat()
        }
    except asyncio.TimeoutError:
        return JSONResponse({
            "success": False,
            "error": "Bot timeout (>30s)",
            "bot_id": bot_id
        }, status_code=504)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e),
            "bot_id": bot_id
        }, status_code=500)
```

**Status:** ✅ HIGH - critical for reliability
**Est time:** 10 minutes

---

#### Task 8: Update Frontend to Handle Failures (10 min)
**Why after routing fix:** Displays error feedback to users
**File:** BotLauncher.js (update handleWebSocketMessage)

**Fix:**
```javascript
function handleWebSocketMessage(message) {
  const { type, bot_id, content, success, error, timestamp } = message;

  if (success === false) {
    // Handle error
    addMessage({
      sender: 'System',
      content: `❌ Error sending to ${bot_id}: ${error}`,
      timestamp: new Date(timestamp),
      isBot: false,
      isError: true
    });
    hideTypingIndicator();
    return;
  }

  if (type === 'response') {
    addMessage({
      sender: bot_id,
      content: content,
      timestamp: new Date(timestamp),
      isBot: true,
      isSuccess: true
    });
    hideTypingIndicator();
  }
}

// Update addMessage to show errors differently
function addMessage(msg) {
  const messageEl = document.createElement('div');
  messageEl.className = `message ${msg.isBot ? 'bot' : 'user'}`;
  if (msg.isError) messageEl.classList.add('error');
  if (msg.isSuccess) messageEl.classList.add('success');

  messageEl.innerHTML = `
    <span class="sender">${msg.sender}</span>
    <span class="time">${msg.timestamp.toLocaleTimeString()}</span>
    <p>${msg.content}</p>
  `;

  document.getElementById('chatMessages').appendChild(messageEl);
  document.getElementById('chatMessages').scrollTop =
    document.getElementById('chatMessages').scrollHeight;
}
```

**Status:** ✅ HIGH - user feedback
**Est time:** 10 minutes

---

### PHASE 4: STATUS VISIBILITY (15-20 minutes)

**Goal:** Users see bot health and activity

#### Task 9: Initialize Status Polling (10 min)
**Why: After core chat works:** Adds visibility
**File:** BotLauncher.js (Line 428, currently null)

**Current:**
```javascript
let statusUpdateInterval = null;  // ← Never started
```

**Fix:**
```javascript
function startStatusPolling() {
  // Poll every 5 seconds
  statusUpdateInterval = setInterval(async () => {
    try {
      const response = await fetch('/api/bots/status');
      const bots = await response.json();

      updateStatusDashboard(bots);
    } catch(e) {
      console.error('Status poll error:', e);
    }
  }, 5000);
}

function updateStatusDashboard(bots) {
  const statusPanel = document.getElementById('statusPanel');
  statusPanel.innerHTML = '';

  bots.forEach(bot => {
    const botStatus = document.createElement('div');
    botStatus.className = `bot-status ${bot.running ? 'online' : 'offline'}`;
    botStatus.innerHTML = `
      <div class="bot-id">${bot.id}</div>
      <div class="status-indicator">
        ${bot.running ? '🟢 Running' : '🔴 Offline'}
      </div>
      <div class="bot-info">
        <span>Port: ${bot.port || 'N/A'}</span>
        <span>Memory: ${bot.memory_mb || '?'}MB</span>
        <span>PID: ${bot.pid || 'N/A'}</span>
      </div>
    `;
    statusPanel.appendChild(botStatus);
  });
}

// Start on page load
document.addEventListener('DOMContentLoaded', () => {
  initWebSocket();
  startStatusPolling();
});
```

**Status:** ✅ HIGH - visibility
**Est time:** 10 minutes

---

### PHASE 5: RELIABILITY (15-20 minutes)

**Goal:** Chat history works, no crashes

#### Task 10: Fix Chat History Persistence (15 min)
**Why last:** Once core chat works, fix persistence
**File:** Python backend `app.py`

**Current:**
```python
# Loads entire file into memory - CRASHES AT SCALE
all_messages = [json.loads(line) for line in f if line.strip()]
```

**Fix:**
```python
async def get_chat_history(request):
    bot_id = request.query_params.get('bot_id')
    offset = int(request.query_params.get('offset', 0))
    limit = int(request.query_params.get('limit', 100))

    # Use database query instead of loading entire file
    try:
        query = "SELECT * FROM chat_messages WHERE bot_id = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3"
        messages = await db.fetch(query, bot_id, limit, offset)

        # Reverse to chronological order
        messages = list(reversed(messages))

        return {
            "success": True,
            "messages": [dict(msg) for msg in messages],
            "count": len(messages),
            "offset": offset
        }
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

async def save_message(request):
    data = request.json

    try:
        query = """
        INSERT INTO chat_messages (bot_id, sender, content, created_at)
        VALUES ($1, $2, $3, $4)
        RETURNING id
        """
        result = await db.fetchval(
            query,
            data['bot_id'],
            data['sender'],
            data['content'],
            datetime.now(timezone.utc)
        )

        return {
            "success": True,
            "message_id": result
        }
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)
```

**Status:** ✅ CRITICAL - prevents crashes
**Est time:** 15 minutes

---

## Execution Timeline

```
PHASE 1 (30-45 min): Enable Basic Chat
  ✅ Fix input field
  ✅ Implement selectBot()
  ✅ Replace prompt() dialog
  → Result: Users can launch bot, select it, type

PHASE 2 (45-60 min): Real-Time Messaging
  ✅ Initialize WebSocket
  ✅ Handle WebSocket messages
  ✅ Send messages via WebSocket
  → Result: Real-time chat works

PHASE 3 (20-30 min): Message Feedback
  ✅ Fix routing feedback (backend)
  ✅ Update frontend error handling
  → Result: Users see success/failure clearly

PHASE 4 (15-20 min): Status Visibility
  ✅ Initialize status polling
  → Result: Users see bot health

PHASE 5 (15-20 min): Reliability
  ✅ Fix chat history (use database)
  → Result: No crashes at scale

TOTAL: 2-3.5 hours → PRODUCTION-READY CHAT
```

---

## PARALLEL WORK POSSIBLE

**While BOT-004 does PHASE 1-2 (2 hours):**
- BOT-001 can complete integration validation
- BOT-003 can complete GO/NO-GO summary
- Both can be done in parallel ✅

**Then reconverge when all code ready for testing**

---

## Success Criteria (Each Phase)

**PHASE 1 ✅**
- [ ] Input field enables/disables properly
- [ ] selectBot() works - bot gets highlighted
- [ ] Bot launch uses proper input instead of prompt()

**PHASE 2 ✅**
- [ ] WebSocket connects on page load
- [ ] Can send message and receive response in real-time
- [ ] Typing indicator shows while processing

**PHASE 3 ✅**
- [ ] Failed message sends show error clearly
- [ ] Success shows checkmark or confirmation
- [ ] Users know definitively if command worked

**PHASE 4 ✅**
- [ ] Status dashboard shows running bots
- [ ] Green/red indicators for online/offline
- [ ] Refreshes every 5 seconds

**PHASE 5 ✅**
- [ ] Chat history loads without crashing
- [ ] Scrolling up loads older messages
- [ ] Works with 1000+ messages

---

**Ready for BOT-004 to start PHASE 1?**
