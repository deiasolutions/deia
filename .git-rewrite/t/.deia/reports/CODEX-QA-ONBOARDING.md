# CODEX QA ONBOARDING - QUICK START
**Prepared by:** Q33N (BEE-000)
**For:** CODEX (QA Agent)
**Date:** 2025-10-25
**ETA Arrival:** 20:30 CDT

---

## QUICK FACTS

**What you're testing:** Multi-bot orchestration platform with web-based chat interface
**Platform:** Python FastAPI backend + Vanilla JS frontend
**Status:** Production-ready (as of 17:30 CDT)
**Entry point:** http://localhost:8000

---

## 1. SYSTEM ARCHITECTURE (5 minutes)

### Three Main Components:

**Backend (Python):**
- `src/deia/services/` - 56 service modules
- `llama-chatbot/app.py` - FastAPI server + HTML/CSS/JS
- Port: 8000 (chat UI) + dynamic ports (bot services)

**Key Services:**
- `task_orchestrator.py` - Distributes work to bots
- `bot_auto_scaler.py` - Scales bots on demand
- `bot_messenger.py` - Inter-bot communication
- `config_manager.py` - Runtime configuration
- `disaster_recovery.py` - Crash recovery & backups
- `audit_logger.py` - Complete action logging

**Frontend:**
- Single-page app in FastAPI response
- Real-time WebSocket for status updates
- 3-panel layout (bot list, chat, status)
- Dark theme, responsive design

---

## 2. START TESTING (DO THIS FIRST)

### Pre-flight Checklist:
- [ ] Verify port 8000 is accessible
- [ ] Open http://localhost:8000 in browser
- [ ] WebSocket connects (no console errors)
- [ ] Status dashboard shows live updates
- [ ] Input field is enabled after bot selection

### Critical Path Test (15 minutes):

1. **Launch a bot:**
   - Click "+ Launch Bot"
   - Enter bot ID: "TEST-BOT-001"
   - Verify it appears in left panel ✓

2. **Select the bot:**
   - Click "Select" button next to bot
   - Verify input field becomes enabled ✓

3. **Send a command:**
   - Type: "Hello, what is 2+2?"
   - Click Send
   - Verify message appears in chat ✓

4. **Receive response:**
   - Wait for bot response in chat
   - Verify response attribution (shows bot ID) ✓
   - Verify timestamp ✓

5. **Check status:**
   - Right panel shows bot status
   - See uptime, PID, port ✓
   - Status updates in real-time ✓

6. **Review history:**
   - Switch to different bot
   - Switch back
   - Previous messages still there ✓

### If ANYTHING fails:
- Check browser console for JavaScript errors
- Check server logs: `.deia/bot-logs/`
- Check `.deia/reports/PORT-8000-DESIGN-REVIEW.md` for known issues
- Escalate to Q33N immediately

---

## 3. TEST CATEGORIES

### CRITICAL (Must Pass)
- [ ] Chat Comms: Launch, select, send, receive, history
- [ ] Error Handling: Offline bot, timeout, invalid command
- [ ] Real-time Updates: WebSocket connected, status updates live
- [ ] Data Isolation: Multiple bots don't share chat history

### HIGH (Important)
- [ ] Status Dashboard: Shows live bot metrics
- [ ] Command Feedback: User knows if command executed
- [ ] Message Formatting: Code blocks, JSON rendering
- [ ] Session Persistence: History survives refresh

### MEDIUM (Polish)
- [ ] Visual Design: Matches Claude Code quality
- [ ] Keyboard Navigation: Tab, Enter, Escape work
- [ ] Mobile Responsive: Layouts adapt properly
- [ ] Animations: Smooth transitions, no jank

### LOW (Nice-to-have)
- [ ] Autocomplete: Command suggestions work
- [ ] Command History: Previous commands recalled
- [ ] Settings: Theme and preference changes
- [ ] Export: Save chat to JSON/PDF

---

## 4. TEST SCENARIOS

### Scenario 1: Single Bot Workflow
1. Launch BOT-001
2. Select it
3. Send 5 different commands
4. Verify all responses appear
5. Refresh page, verify history persists

### Scenario 2: Multiple Bot Isolation
1. Launch BOT-001
2. Send command: "Hello from Bot 1"
3. Launch BOT-002
4. Send command: "Hello from Bot 2"
5. Switch back to BOT-001
6. Verify message says "Hello from Bot 1" (not Bot 2)

### Scenario 3: Error Recovery
1. Launch BOT-001
2. Send command
3. Kill the bot (simulate crash)
4. Verify UI shows bot offline
5. Try sending command
6. Verify error message appears
7. Restart bot
8. Verify bot comes back online

### Scenario 4: Performance Under Load
1. Open 3 browser tabs
2. Launch 5 bots simultaneously
3. Send 50 commands (10 per bot)
4. Measure response time per command
5. No crashes or lost messages
6. UI remains responsive

---

## 5. KNOWN ISSUES (From Design Review)

**CRITICAL (Recently Fixed):**
- ❌ WebSocket initialization → ✅ FIXED by BOT-003
- ❌ Input field disabled → ✅ FIXED by BOT-003
- ❌ selectBot() missing → ✅ FIXED by BOT-003
- ❌ Status polling never starts → ✅ FIXED by BOT-003

**HIGH (Should be Fixed):**
- ❌ Message routing no feedback → ✅ Being fixed by BOT-003
- ❌ Chat history buggy → ✅ Being fixed by BOT-003

**MEDIUM (Polish):**
- ⚠️ Button hover states inconsistent
- ⚠️ Mobile layout cramped on small screens
- ⚠️ No keyboard shortcuts

See `.deia/reports/PORT-8000-DESIGN-REVIEW.md` for full list of 17 issues

---

## 6. PERFORMANCE BASELINES

**Expected Metrics (from design phase):**
- Message latency: < 1 second
- Status update frequency: Every 3 seconds
- Support 10+ concurrent users
- Chat history: 1000+ messages paginated efficiently

**Measurement Tools:**
- Browser DevTools Network tab (latency)
- Browser DevTools Performance tab (UI responsiveness)
- Server logs `.deia/bot-logs/` (backend metrics)

---

## 7. TESTING REPORTS

Create reports in `.deia/reports/CODEX-QA/`:
- `CODEX-critical-tests-result.md` - Critical path results
- `CODEX-scenario-tests-result.md` - Scenario testing results
- `CODEX-performance-result.md` - Performance metrics
- `CODEX-issues-found.md` - Any bugs discovered

---

## 8. ESCALATION

**If you find:**
- ❌ Critical failure (can't use system) → Ping Q33N immediately
- ❌ High-priority bug (feature broken) → Create issue file, report
- ⚠️ Medium issue (polish) → Document, can wait
- ✅ Test passed → Log result in report

---

## 9. SUCCESS CRITERIA

By end of QA (22:00 CDT):
- ✅ All CRITICAL tests passing
- ✅ All HIGH tests passing or documented
- ✅ Performance metrics captured
- ✅ No blocking issues
- ✅ System ready for production

---

## 10. RESOURCES

**Key Files to Know:**
- `llama-chatbot/app.py` - Source code (2586 lines)
- `.deia/reports/PORT-8000-*.md` - Design/UX specs (4 docs)
- `tests/integration/test_chat_comms_integration.py` - Test suite
- `.deia/bot-logs/` - Live system logs

**Documentation:**
- Architecture: `.deia/reports/` (multiple docs)
- API Reference: Swagger at http://localhost:8000/docs
- Troubleshooting: `.deia/reports/PORT-8000-*-ISSUES.md`

---

## READY TO TEST

System is production-hardened and design-improved as of 17:30 CDT.

Go test it. Find the bugs. Make it bulletproof.

**Q33N is standing by for your reports.**

