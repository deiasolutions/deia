# BOT-004 Design Implementation Strategy for BOT-003
**Prepared for:** Collaboration Blitz (16:15 - 17:30 CDT)
**For Bot:** BOT-003 (Lead Implementation)
**By:** BOT-004 (Design Guidance)
**Status:** READY FOR EXECUTION

---

## Quick Reference - Critical Fixes Priority

### MUST FIX (6 items) - 16:15 to 17:00

1. **Bot Launch Modal** (10 min)
   - Replace `prompt()` dialog with professional modal form
   - Location: `llama-chatbot/app.py` line ~446
   - Spec: See PORT-8000-DESIGN-REVIEW.md issue #1

2. **Input Field Enable/Disable** (5 min)
   - Enable input when bot selected
   - Function: `selectBot()` needs to set `chatInput.disabled = false`
   - Location: line ~524

3. **Complete selectBot() Function** (5 min)
   - Function stub exists, needs full implementation
   - Must update visual selection feedback
   - Must enable/disable input field

4. **Message Routing Feedback** (10 min)
   - Show clear success/failure on message send
   - Replace confusing `[Offline]` messages with real feedback
   - Location: message send handler, line ~600+

5. **Verify WebSocket Initialization** (5 min)
   - Chat Comms Fix should have done this
   - Test: Check `ws` object connects on page load
   - Spec: PORT-8000-UX-FIXES.md Workflow 2

6. **Status Dashboard Polling** (10 min)
   - Initialize `statusUpdateInterval`
   - Poll `/api/bots` every 2-3 seconds
   - Update status panel in real-time
   - Spec: PORT-8000-UX-FIXES.md Workflow 3

---

## Implementation Order (45 minutes for critical fixes)

### BLOCK 1: Bot Launch & Selection (16:15-16:30, 15 min)
**Goal:** Users can launch bots and select them smoothly

**Task 1: Replace Bot Launch Dialog (10 min)**
```javascript
// OLD (janky):
const botId = prompt('Enter Bot ID...');

// NEW (professional):
// Open modal form with:
// - Input field (focused)
// - Available bots list
// - Launch button
// - Cancel button
// Visual: Clean, professional, matches design spec
```
**Spec Reference:** PORT-8000-DESIGN-REVIEW.md #1
**Testing:** Launch dialog appears, user can enter bot ID, form validates

**Task 2: Complete selectBot() Function (5 min)**
```javascript
function selectBot(botId) {
    // MUST DO:
    selectedBotId = botId;
    selectedBotInfo.textContent = `🔗 Connected to ${botId}`;
    chatInput.disabled = false;  // ← CRITICAL
    sendButton.disabled = false;  // ← CRITICAL
    chatMessages.innerHTML = '';
    addMessage('assistant', `Connected to ${botId}. Ready for commands.`);
    loadChatHistory();
    refreshBotList();
}
```
**Spec Reference:** PORT-8000-DESIGN-REVIEW.md #3, #4
**Testing:** Click bot in list → input field enables, header updates

### BLOCK 2: Messaging & Feedback (16:30-16:45, 15 min)
**Goal:** Users see clear success/failure when sending commands

**Task 3: Message Routing Feedback (10 min)**
```javascript
// ON SEND: Show loading state
sendButton.disabled = true;
sendButton.textContent = "Sending...";

// ON SUCCESS: Show confirmation
response comes back → show message in chat

// ON ERROR: Show clear error message
"✗ Command failed to reach BOT-001 (offline)"
with options: [Retry] [Switch Bot]
```
**Spec Reference:** PORT-8000-UX-FIXES.md Workflow 2
**Testing:** Send message → see immediate feedback, response shows attribution

**Task 4: Input Field States (5 min)**
- Enabled: When bot selected (blue border on focus)
- Disabled: When no bot selected (grayed out)
- Focus state: Blue accent color, glow shadow
**Spec Reference:** PORT-8000-VISUAL-REDESIGN.md "Input Fields"

### BLOCK 3: Live Monitoring (16:45-17:00, 15 min)
**Goal:** Status dashboard shows real-time bot health

**Task 5: WebSocket Verification (5 min)**
```javascript
// Should already be done by Chat Comms Fix
// But verify in JS console:
console.log("ws object:", ws);
console.log("ws.readyState:", ws.readyState);  // 1 = OPEN

// If not working, check:
// - Port 8000 server running?
// - Ollama connected?
// - No JS errors in console?
```
**Testing:** Open browser dev tools → Messages appear as sent/received, no "Offline"

**Task 6: Status Dashboard Polling (10 min)**
```javascript
// MUST INITIALIZE:
if (!statusUpdateInterval) {
  statusUpdateInterval = setInterval(async () => {
    const response = await fetch('/api/bots');
    const data = await response.json();
    // Update status panel with new data
    updateStatusPanel(data.bots);
  }, 3000);  // Every 3 seconds
}

function updateStatusPanel(bots) {
  // Clear old status items
  statusList.innerHTML = '';

  // Add new status for each bot
  for (const [botId, botData] of Object.entries(bots)) {
    const item = document.createElement('div');
    item.className = 'status-item ' + botData.status.toLowerCase();
    item.innerHTML = `
      <div class="status-label">${botId}</div>
      <div class="status-value">✓ Running</div>
      <div class="status-value">Uptime: 2m 34s</div>
      <div class="status-value">Memory: 120MB</div>
    `;
    statusList.appendChild(item);
  }
}
```
**Spec Reference:** PORT-8000-UX-FIXES.md Workflow 3
**Testing:** Launch bot → status appears in right panel, updates every 3 seconds

---

## Visual Design Polish (17:00-17:15, 15 min)

### BOT-004 Focus: Verify BOT-003's Implementation

**Review Checklist:**
- [ ] Colors match spec (blue #4a7ff5 for accents)
- [ ] Spacing uses 4px grid (8, 12, 16, 20px padding/margins)
- [ ] Typography is clean (not too many font sizes)
- [ ] Hover states visible on all buttons
- [ ] Input focus shows blue glow shadow
- [ ] Message bubbles have clear attribution (You vs Bot)
- [ ] Status indicators use correct colors (green/amber/red)
- [ ] Overall appearance professional (not amateur)

**If issues found:**
1. Document specific issue
2. Reference spec section
3. Provide fix code (BOT-004 writes, BOT-003 applies)
4. Test immediately after

---

## Testing Checkpoints

### After Each Block (5 min test cycle)

**BLOCK 1 Test (after 16:30):**
- [ ] Bot launch dialog appears
- [ ] Can enter bot ID
- [ ] Bot selection works
- [ ] Input field enables when bot selected
- [ ] No JavaScript errors in console

**BLOCK 2 Test (after 16:45):**
- [ ] Send message → appears in chat
- [ ] Success/failure feedback clear
- [ ] Multiple bots can be selected
- [ ] Input field is/isn't enabled correctly

**BLOCK 3 Test (after 17:00):**
- [ ] WebSocket connected (no offline messages)
- [ ] Status panel shows bot health
- [ ] Status updates every 3 seconds
- [ ] Color-coded indicators (green/amber/red)

**BLOCK 4 Test (after 17:15):**
- [ ] All visual design applied
- [ ] Colors match spec
- [ ] Spacing consistent
- [ ] Hover/active states visible
- [ ] No breaking changes to core

---

## Spec References for BOT-003

Use these files while implementing:

**Design Issues & Requirements:**
- `.deia/reports/PORT-8000-DESIGN-REVIEW.md` - Issues 1-7 (critical)
- `.deia/reports/PORT-8000-STRUCTURAL-FIXES.md` - Architecture (reference only)

**UX Workflows:**
- `.deia/reports/PORT-8000-UX-FIXES.md` - Workflows 1-3 (implement to these specs)

**Visual Design:**
- `.deia/reports/PORT-8000-VISUAL-DESIGN.md` - Colors, fonts, spacing, components

---

## Communication Pattern

**BOT-003 → BOT-004:**
- "I'm at [checkpoint], here's what I did"
- Share code changes
- Ask for design review

**BOT-004 → BOT-003:**
- "Looks good" / "Has issues here"
- Provide specific feedback
- Suggest code fixes if needed

**BOT-001 → Both:**
- "Tests passing" / "Breaking change detected"
- Code review results
- Integration status

---

## Success = 17:30 Complete

✅ **Chat Comms:** Fully functional (WebSocket, status, input)
✅ **Critical Fixes:** All 6 items implemented
✅ **Visual Design:** Professional appearance
✅ **No Breaking Changes:** Core system still works
✅ **70%+ Tests:** Code quality maintained

---

**Ready to execute. Waiting for 16:15 signal from Q33N.**

Generated by BOT-00004
