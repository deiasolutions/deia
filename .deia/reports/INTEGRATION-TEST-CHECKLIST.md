# Integration Test Checklist - Port 8000 Chat Interface

**Status:** Ready to Execute (waiting for BOT-003 completion)
**When to Run:** After BOT-003 posts "bot-003-frontend-chat-fixes-complete.md"

---

## Pre-Integration Test

1. [ ] Verify BOT-001 completion posted ✅ (12:45 PM)
2. [ ] Verify BOT-003 completion posted (waiting...)
3. [ ] All backend API endpoints exist
4. [ ] WebSocket auth implemented
5. [ ] DOM elements added

---

## Integration Test Execution

### Step 1: Start Services
```bash
# Terminal 1: Start chat app
cd src/deia/services
python -m uvicorn chat_interface_app:app --port 8000
```

Wait for: "Application startup complete"

### Step 2: Open Browser
```
http://localhost:8000
```

### Step 3: Test Matrix

| Test | Expected | Pass |
|------|----------|------|
| Page loads without errors | Content displays | [ ] |
| WebSocket connects | 🟢 Connected shows | [ ] |
| Browser console | No errors | [ ] |
| Bot list displays | Empty or shows bots | [ ] |
| Launch bot button works | Dialog appears | [ ] |
| Enter "BOT-001" | Input accepts text | [ ] |
| Click Launch | Toast: "✅ Launched" | [ ] |
| Bot appears in list | BOT-001 shows | [ ] |
| Bot status shows | 🟢 Running | [ ] |
| Click bot to select | Chat area activates | [ ] |
| Type message | Message appears in chat | [ ] |
| Send message | Toast: "Sending..." | [ ] |
| Get response | Bot responds | [ ] |
| See confirmation | Toast: "Sent" | [ ] |
| Status updates | Every 5 sec | [ ] |
| Stop bot | Toast: "✅ Stopped" | [ ] |
| Bot disappears | List updates | [ ] |

### Step 4: Browser Compatibility

- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Step 5: Error Scenarios

- [ ] Invalid bot ID → Error message shown
- [ ] No bot selected → Warning shown
- [ ] WebSocket disconnects → Status updates to offline
- [ ] API unreachable → Graceful error message

---

## Success Criteria

✅ All tests pass
✅ No console errors
✅ User feedback working (toasts showing)
✅ Status updates live
✅ Chat functional end-to-end
✅ Multiple browser compatibility

---

## If Issues Found

Post to: `.deia/hive/responses/deiasolutions/Q33N-INTEGRATION-TEST-RESULTS.md`

Format:
```markdown
# Integration Test Results

**Status:** PASS / FAIL

## Issues Found:
1. [Issue description]
   - Expected: [what should happen]
   - Actual: [what happened]
   - Severity: CRITICAL / HIGH / MEDIUM

## Tests Passed: X/Y

## Next Steps:
[Action items for fixing]
```

---

## Wait for BOT-003 Completion

Status: Checking for completion report...
Last BOT-003 update: bot-003-chat-command-complete.md (12:15 PM)
Current time: Monitoring...

When BOT-003 posts frontend chat fixes completion → Run this checklist
