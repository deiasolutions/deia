# BOT-004 PHASE 1 HANDOFF - Enable Basic Chat

**Duration:** 30-45 minutes
**Status:** 🔴 READY TO EXECUTE NOW
**Target:** Users can launch bot → select it → type

---

## TASK 1: Fix Input Field Enable/Disable

**Time:** 15 minutes
**File:** `llama-chatbot/static/js/components/BotLauncher.js`
**Line:** ~398

### CURRENT (Wrong)
```html
<input type="text" id="chatInput" class="chat-input"
       placeholder="..." disabled>
```

### FIXED (What to Add)
Add these two functions at top of BotLauncher.js:

```javascript
function enableInput() {
  const input = document.getElementById('chatInput');
  input.disabled = false;
  input.focus();
  input.style.opacity = '1';
}

function disableInput() {
  const input = document.getElementById('chatInput');
  input.disabled = true;
  input.style.opacity = '0.5';
}
```

### UPDATE HTML
Change the input from `disabled` to just empty:
```html
<input type="text" id="chatInput" class="chat-input"
       placeholder="Type message and press Enter...">
```

### VERIFICATION
- [ ] Input field is enabled (not greyed out)
- [ ] Input field is disabled when no bot selected (greyed out)
- [ ] Input field focused when bot selected
- [ ] Can type text when enabled

---

## TASK 2: Implement selectBot() Function

**Time:** 15 minutes
**File:** Same file `BotLauncher.js`
**Location:** Add new function after enableInput/disableInput

### CURRENT (Wrong)
```javascript
// Line 496 - CALLED BUT NEVER DEFINED
// <button onclick="selectBot('${botId}')">Select</button>
```

### FIXED (Exact Implementation)

Add this function:

```javascript
function selectBot(botId) {
  // Store selected bot globally
  window.selectedBotId = botId;

  // Update UI - highlight selected bot
  document.querySelectorAll('.bot-item').forEach(item => {
    item.classList.remove('selected');
  });

  const selectedItem = document.querySelector(`[data-bot-id="${botId}"]`);
  if (selectedItem) {
    selectedItem.classList.add('selected');
  }

  // Enable input field
  enableInput();

  // Show success message
  showMessage(`Selected bot: ${botId}`, 'system');

  // Clear previous messages (optional)
  document.getElementById('chatMessages').innerHTML = '';
}

function showMessage(text, sender) {
  const messageEl = document.createElement('div');
  messageEl.className = `message ${sender}`;
  messageEl.innerHTML = `<span class="sender">${sender}</span>: ${text}`;
  document.getElementById('chatMessages').appendChild(messageEl);
}
```

### UPDATE BOT LIST HTML
When rendering bot items, add `data-bot-id`:

```javascript
// In refreshBotList() or wherever bots are listed:
botItem.setAttribute('data-bot-id', botId);

// Update button to use function:
botItem.innerHTML = `
    <div class="bot-id">${botId}</div>
    <button onclick="selectBot('${botId}')">Select</button>
    <button onclick="stopBot('${botId}')">Stop</button>
`;
```

### ADD CSS
Add to CSS file for visual feedback:

```css
.bot-item.selected {
  background-color: #e3f2fd;
  border-left: 4px solid #2196F3;
}

.bot-item.selected .bot-id {
  font-weight: bold;
  color: #2196F3;
}
```

### VERIFICATION
- [ ] Can click "Select" button next to bot
- [ ] Selected bot gets highlighted (blue background)
- [ ] Input field becomes enabled
- [ ] System message shows "Selected bot: [botId]"
- [ ] Selecting different bot updates highlight

---

## TASK 3: Replace prompt() Dialog with Proper UI Input

**Time:** 15 minutes
**File:** Same file `BotLauncher.js`
**Location:** Replace launchBot() function and add HTML

### CURRENT (Wrong)
```javascript
async function launchBot() {
    const botId = prompt('Enter Bot ID (e.g., BOT-001):');
    // Janky browser dialog
}
```

### FIXED - STEP 1: Add HTML Form

Add this to the page (above the bot list):

```html
<div class="bot-launch-section">
  <h3>Launch New Bot</h3>
  <div class="launch-form">
    <input
      type="text"
      id="botIdInput"
      placeholder="Enter Bot ID (e.g., BOT-001)"
      maxlength="50"
    >
    <button onclick="launchBotFromInput()">Launch</button>
  </div>
  <div id="launchStatus"></div>
</div>
```

### FIXED - STEP 2: Replace launchBot() Function

Replace the old function:

```javascript
async function launchBotFromInput() {
  const input = document.getElementById('botIdInput');
  const botId = input.value.trim().toUpperCase();
  const statusDiv = document.getElementById('launchStatus');

  // Clear previous status
  statusDiv.innerHTML = '';

  // Validation: Bot ID required
  if (!botId) {
    statusDiv.innerHTML = '<span class="error">❌ Bot ID required</span>';
    return;
  }

  // Validation: Format check (letters, numbers, hyphens only)
  if (!/^[A-Z0-9\-]+$/.test(botId)) {
    statusDiv.innerHTML = '<span class="error">❌ Invalid format. Use letters, numbers, hyphens only</span>';
    return;
  }

  // Validation: Min length
  if (botId.length < 3) {
    statusDiv.innerHTML = '<span class="error">❌ Bot ID too short (min 3 chars)</span>';
    return;
  }

  // Show loading state
  statusDiv.innerHTML = '<span class="loading">⏳ Launching bot...</span>';
  const button = document.querySelector('.launch-form button');
  button.disabled = true;

  try {
    // Call launch API
    const response = await fetch('/api/bot/launch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bot_id: botId })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Launch failed');
    }

    const data = await response.json();

    // Success
    statusDiv.innerHTML = `<span class="success">✅ Bot ${botId} launched on port ${data.port}</span>`;
    input.value = '';

    // Refresh bot list
    refreshBotList();

  } catch (error) {
    statusDiv.innerHTML = `<span class="error">❌ ${error.message}</span>`;
  } finally {
    button.disabled = false;
  }
}

// Allow Enter key to launch
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('botIdInput');
  if (input) {
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        launchBotFromInput();
      }
    });
  }
});
```

### ADD CSS

```css
.bot-launch-section {
  margin: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.launch-form {
  display: flex;
  gap: 10px;
  margin: 10px 0;
}

.launch-form input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.launch-form button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.launch-form button:hover {
  background-color: #45a049;
}

.launch-form button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

#launchStatus {
  margin-top: 10px;
  font-size: 14px;
  min-height: 20px;
}

#launchStatus .success {
  color: #4CAF50;
  font-weight: bold;
}

#launchStatus .error {
  color: #f44336;
  font-weight: bold;
}

#launchStatus .loading {
  color: #2196F3;
}
```

### VERIFICATION
- [ ] Input field accepts text
- [ ] "Launch" button works
- [ ] Validation shows error if ID invalid
- [ ] Loading state shows while launching
- [ ] Success message shows when bot launches
- [ ] Enter key in input field launches bot
- [ ] Input field clears after successful launch

---

## END OF PHASE 1

### Success Checklist (All 3 Tasks)

- [ ] **TASK 1:** Input field enables/disables correctly
- [ ] **TASK 2:** Can select bot, it gets highlighted, message shown
- [ ] **TASK 3:** Can launch bot with proper UI input (not prompt dialog)

### User Journey After PHASE 1
```
1. User enters Bot ID in launch form
2. User clicks "Launch"
3. Status shows "Launching..." then "✅ Bot launched"
4. Bot appears in list with "Select" button
5. User clicks "Select"
6. Bot gets highlighted
7. Input field becomes enabled and focused
8. User types message and presses Enter
   ↓ (PHASE 2 will make this work)
```

---

## Testing PHASE 1

**Quick smoke test:**
```
1. Open page → input field should be DISABLED (greyed out)
2. Enter "BOT-TEST" in launch form → click Launch
3. Should see "✅ Bot BOT-TEST launched on port XXXX"
4. Should see bot in list with "Select" button
5. Click "Select" next to bot
6. Input field should become ENABLED
7. Can now type in input field
8. Message appears: "Selected bot: BOT-TEST"
```

**If this works → PHASE 1 COMPLETE ✅**

---

## Files to Modify

| File | Lines | Task |
|------|-------|------|
| `BotLauncher.js` | ~398 | Add enableInput/disableInput functions |
| `BotLauncher.js` | Variable area | Add selectBot() function |
| `BotLauncher.js` | Function area | Replace/add launchBotFromInput() |
| HTML file | - | Add bot-launch-section div |
| CSS file | - | Add styling for launch form and selected bot |

---

## Exact Line Numbers (Estimate)

- **Input HTML:** Line ~398
- **selectBot() function:** Add after line ~450
- **launchBotFromInput() function:** Add after line ~500
- **CSS:** End of style section
- **DOMContentLoaded:** Add event listener at end of script

---

## NEXT AFTER PHASE 1 COMPLETE

When all 3 tasks done and tests pass:
1. Commit code: `git add . && git commit -m "PHASE 1: Enable basic chat - input field, selectBot, launch UI"`
2. Start PHASE 2 (WebSocket)
3. Keep work visible in queue

---

**GO NOW - START PHASE 1** ✅

Reference: `BOT-004-CODE-PRIORITY-SEQUENCE.md` for PHASE 2-5 details
