# 🎯 TASK ASSIGNMENT: BOT-004 - Full Integration Test Suite

**From:** Q33N (bee-000)
**To:** BOT-004 - QA & Testing Specialist
**Priority:** CRITICAL - Verify everything works
**Date:** 2025-10-26 12:15 PM
**ETA:** 30 minutes
**Status:** EXECUTE IMMEDIATELY

---

## THE MISSION

Run comprehensive integration tests to verify frontend + backend working together.

**Goal:** Fully functional chat interface end-to-end verified.

---

## YOUR TASK

### Test Suite to Execute

1. **Server Start Test**
   - Start FastAPI server: `python -m uvicorn src.deia.services.chat_interface_app:app --port 8000 --reload`
   - Verify: Server starts without errors
   - Verify: All 6 API endpoints respond
   - Report: Server status

2. **API Endpoint Tests**
   - [ ] GET /api/bots - Returns bot list (empty is OK)
   - [ ] POST /api/bot/launch - Launch test bot
   - [ ] GET /api/bots - Verify bot appears
   - [ ] POST /api/bot/stop/{botId} - Stop test bot
   - [ ] GET /api/bots/status - Status endpoint works
   - [ ] GET /api/chat/history - History endpoint works
   - [ ] POST /api/bot/{botId}/task - Task endpoint works

   All endpoints must:
   - ✅ Return proper HTTP status
   - ✅ Return valid JSON
   - ✅ Have no server errors
   - ✅ Have proper error messages

3. **Frontend Browser Test**
   - Open: http://localhost:8000
   - Check:
     - [ ] Page loads without JavaScript errors
     - [ ] No console errors (F12 → Console)
     - [ ] WebSocket shows "🟢 Connected"
     - [ ] Bot list loads (or shows "No bots")
     - [ ] Launch button appears and works
     - [ ] Toast notifications appear when expected
     - [ ] All UI elements load properly

4. **End-to-End Workflow Test**
   - [ ] Click Launch Bot
   - [ ] Enter bot name
   - [ ] Verify "Launching..." toast shows
   - [ ] Verify "✅ Launched" toast shows
   - [ ] Verify bot appears in list
   - [ ] Click bot in list
   - [ ] Verify chat area activates
   - [ ] Type a message
   - [ ] Verify "Sending..." toast shows
   - [ ] Verify message appears in chat
   - [ ] Stop bot
   - [ ] Verify "✅ Stopped" toast shows
   - [ ] Verify bot disappears from list

5. **Browser Compatibility Test**
   - [ ] Chrome - All tests pass
   - [ ] Firefox - All tests pass
   - [ ] (Safari if available - All tests pass)

6. **Error Scenario Test**
   - [ ] Invalid bot ID → Error message shown
   - [ ] No bot selected → Warning message shown
   - [ ] WebSocket disconnects → Status updates properly
   - [ ] API error → Error toast shown with message

---

## SUCCESS CRITERIA

All of these must be true:
- ✅ Server starts cleanly
- ✅ All 6 API endpoints respond correctly
- ✅ Frontend loads without JavaScript errors
- ✅ WebSocket connects successfully
- ✅ Bot launch/stop workflows complete
- ✅ Chat messaging works end-to-end
- ✅ Toast notifications appear correctly
- ✅ Status updates display live
- ✅ Error handling works properly
- ✅ Works in Chrome + Firefox (minimum)
- ✅ No console errors or warnings

---

## REPORT WHAT YOU FIND

Create file: `.deia/hive/responses/deiasolutions/bot-004-integration-test-complete.md`

Format:
```markdown
# BOT-004: Integration Test Results

**Status:** PASS / FAIL
**Date:** [timestamp]
**Duration:** [X minutes]
**Tests:** [X/Y passing]

## Test Results Summary:
[List what passed/failed]

## Issues Found:
[Any problems found]

## Recommendations:
[Fix needed or system ready]

## Next Steps:
[Ready for production / Needs fixes / Blocked on]
```

---

## If You Find Issues

### CRITICAL Issues (Blocks functionality):
- Server won't start → Post immediately, Q33N will help
- API endpoints returning errors → Post immediately
- JavaScript errors in console → Post immediately
- Chat not working end-to-end → Post immediately

### HIGH Issues (Needs fixing):
- Toast not showing → Post to Q33N
- WebSocket not connecting → Post to Q33N
- Status not updating → Post to Q33N

### MEDIUM Issues (Polish):
- Minor UI issues → Document in report
- Browser compatibility issues → Document in report

---

## Tools You'll Need

```bash
# Start server
cd /path/to/deiasolutions
python -m uvicorn src.deia.services.chat_interface_app:app --port 8000 --reload

# Test API endpoints (use curl or Postman)
curl http://localhost:8000/api/bots
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id": "TEST-001"}'

# Browser testing
Open: http://localhost:8000
F12 to open console
Check for errors
```

---

## Timeline

- **12:15 PM:** You start
- **12:20 PM:** Server tests complete
- **12:25 PM:** API endpoint tests complete
- **12:30 PM:** Frontend browser tests complete
- **12:40 PM:** E2E workflow tests complete
- **12:45 PM:** Browser compatibility verified
- **12:50 PM:** Error scenarios tested
- **12:50 PM:** Report posted

---

## GO

You know what to do. Execute the tests. Report what you find.

If anything breaks, post immediately - don't wait.

When complete, post your results.

🚀 **Let's verify this thing works!**
