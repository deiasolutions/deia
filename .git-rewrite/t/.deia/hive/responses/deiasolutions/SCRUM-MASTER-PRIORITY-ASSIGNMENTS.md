# PRIORITY ASSIGNMENTS - BOT-001 REBOOT PERIOD
**Authority:** Interim Scrum Master
**Issued:** 2025-10-25 16:11 CDT
**Status:** NO IDLE TIME - Keep working while BOT-001 reboots

---

## IMMEDIATE ASSIGNMENTS

### BOT-003: Design Implementation Lead (16:11-17:00, 49 minutes)

**CRITICAL FIXES FROM BOT-004 SPECS:**

Apply these 6 fixes from `.deia/reports/PORT-8000-DESIGN-REVIEW.md`:

#### Fix 1: Replace Bot Launch prompt() → Modal Dialog (10 min)
**File:** `llama-chatbot/app.py` line ~446
**Current:** Uses browser `prompt()` dialog
**New:** Create professional modal form with:
- Input field (focused, ready to type)
- Available bots list below
- Launch button
- Cancel button
- Input validation feedback

**Reference:** BOT-004's IMPLEMENTATION-STRATEGY.md "Task 1: Replace Bot Launch Dialog"

#### Fix 2: Input Field Enable/Disable (5 min)
**File:** `llama-chatbot/app.py` line ~524
**Current:** Input field always disabled
**New:** Enable input when bot selected
```javascript
chatInput.disabled = false;  // Enable
chatInput.focus();           // Focus
```
**Reference:** PORT-8000-DESIGN-REVIEW.md Issue #3

#### Fix 3: Complete selectBot() Function (5 min)
**Current:** Function exists but incomplete
**New:** Full implementation
```javascript
function selectBot(botId) {
    selectedBotId = botId;
    selectedBotInfo.textContent = `🔗 Connected to ${botId}`;
    chatInput.disabled = false;
    sendButton.disabled = false;
    chatMessages.innerHTML = '';
    addMessage('assistant', `Connected to ${botId}. Ready for commands.`);
    loadChatHistory();
    refreshBotList();
}
```
**Reference:** PORT-8000-DESIGN-REVIEW.md Issue #4

#### Fix 4: Message Routing Feedback (10 min)
**File:** `llama-chatbot/app.py` message send handler
**Current:** Returns "success": true even on errors, shows confusing [Offline] messages
**New:** Clear success/failure feedback
```javascript
// ON SEND: Show loading state
sendButton.disabled = true;
sendButton.textContent = "Sending...";

// ON SUCCESS: Clear, show message in chat
// ON ERROR: "✗ Command failed to reach BOT-001 (offline)"
//           with [Retry] [Switch Bot] buttons
```
**Reference:** PORT-8000-UX-FIXES.md Workflow 2

#### Fix 5: Verify WebSocket Initialization (5 min)
**Already done in Chat Comms fix, just verify:**
- Open browser dev tools console
- Check: `console.log(ws)` shows WebSocket object
- Check: `ws.readyState === 1` (OPEN state)
- No [Offline] errors in chat

#### Fix 6: Status Dashboard Polling (10 min)
**File:** Line ~428 (`statusUpdateInterval`)
**Current:** Never initialized
**New:** Start polling on page load
```javascript
// Initialize status polling on page load
if (!statusUpdateInterval) {
  statusUpdateInterval = setInterval(async () => {
    const response = await fetch('/api/bots');
    const data = await response.json();
    updateStatusPanel(data.bots);  // Your update function
  }, 3000);  // Every 3 seconds
}
```
**Reference:** PORT-8000-UX-FIXES.md Workflow 3

---

**Execution Timeline:**
- 16:11-16:21: Fixes 1-3 (Launch modal + selectBot)
- 16:21-16:31: Fix 4 (Message routing feedback)
- 16:31-16:41: Fix 5 (WebSocket verification)
- 16:41-16:51: Fix 6 (Status dashboard polling)
- 16:51-17:00: Test entire flow end-to-end

**Success Criteria:**
- [ ] Bot launch uses professional modal (not prompt)
- [ ] Input field enables when bot selected
- [ ] selectBot() fully implemented
- [ ] Message send shows clear feedback
- [ ] WebSocket connected (no [Offline] errors)
- [ ] Status panel updates live every 3 seconds
- [ ] Full user workflow tested: Launch → Select → Send → Receive

**Deliverable:** Post status to `.deia/hive/responses/deiasolutions/bot-003-design-implementation-complete.md`

---

### BOT-004: Design Polish & Visual Review (16:11-17:00, 49 minutes)

**ROLE: Design Architect & Visual Review**

You review BOT-003's implementation against visual design specs.

#### Task 1: Design Review Checklist (10 min)
Create detailed checklist from PORT-8000-VISUAL-REDESIGN.md:
- [ ] Colors match spec (blue #4a7ff5 for accents, not purple)
- [ ] Spacing uses 4px grid (8, 12, 16, 20px)
- [ ] Typography: Clear hierarchy (no more than 3-4 font sizes)
- [ ] Buttons have proper padding/spacing
- [ ] Hover states visible (darker, lift effect)
- [ ] Focus states clear (blue glow on inputs)
- [ ] Message bubbles have clear attribution
- [ ] Status indicators color-coded (green/amber/red)
- [ ] Overall appearance: Professional, not amateur
- [ ] Dark theme has depth (not flat)

#### Task 2: Monitor BOT-003 Implementation (30 min)
As BOT-003 applies fixes:
1. Review each code change
2. Check visual result on port 8000
3. Compare against PORT-8000-VISUAL-REDESIGN.md specs
4. Flag any design issues
5. Provide specific feedback with code suggestions

#### Task 3: Polish Interactive States (9 min)
Document visual improvements needed:
- Button hover/active states
- Input focus glow
- Message bubble polish
- Status indicator animations
- Transition smoothness

#### Task 4: Create Design Sign-Off (10 min)
Create document confirming visual design quality.

**Deliverable:** Post to `.deia/hive/responses/deiasolutions/bot-004-design-review-signin-complete.md`

---

## PARALLEL WORK (If finished early)

### If BOT-003 finishes design implementation <16:51:
- Start next design batch from PORT-8000-DESIGN-REVIEW.md HIGH issues
- High priority items (7 issues):
  - Status updates initialization
  - Chat history persistence
  - Message routing improvements
  - Error handling UX
  - Input validation
  - Command history dropdown
  - Responsive design

### If BOT-004 finishes design review <17:00:
- Prepare final visual design document for post-reboot integration
- Document any technical debt or follow-up items
- Create design handoff guide for future iterations

---

## SUCCESS CRITERIA (By 17:00 CDT)

✅ **BOT-003:**
- 6 critical fixes implemented
- Full user workflow tested
- No breaking changes
- Code quality verified

✅ **BOT-004:**
- Design review complete
- Visual specs validated
- Polish recommendations documented
- Ready for final integration when BOT-001 returns

✅ **System Status:**
- Port 8000 fully functional (replaces CLI)
- Professional appearance
- Ready for BOT-001 to integrate with core system

---

## CHECKPOINT

Report back at **16:51 CDT** with:
- BOT-003: Code changes complete, ready for testing
- BOT-004: Design review complete, ready for sign-off
- Ready to transition to final integration with BOT-001

---

**NO IDLE TIME - EXECUTE IMMEDIATELY**

Interim Scrum Master
