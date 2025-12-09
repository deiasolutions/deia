# BOT-001 HIGH PRIORITY FIXES + USER GUIDE - PORT 8000
**From:** Q33N (BEE-000)
**To:** BOT-001
**Issued:** 2025-10-25 16:32 CDT
**Due:** 2025-10-25 18:32 CDT (2 hours)
**Priority:** HIGH - Breaks key workflows

---

## PRIMARY TASK: HIGH PRIORITY FIXES

Fix 4 HIGH priority UX issues that break core workflows. **Parallel:** While working on these, also document User Guide.

---

## HIGH PRIORITY ISSUES TO FIX

### 1. Status Dashboard Empty/Not Polling (HIGH)
**File:** `src/deia/adapters/web/app.py` (search for status, dashboard, polling)
**Issue:** Dashboard shows no bot information - doesn't update in real-time
**Current State:** Empty section, no data flowing in
**Fix Required:**
- Verify polling loop is initialized on page load
- Check polling interval (should be ~2 seconds)
- Verify API endpoint being called: GET `/api/bots/status`
- Parse response and update DOM elements
- Handle error cases (bot down, connection lost)
- Test: Launch bot → dashboard updates every 2 seconds with status

### 2. Command Feedback Missing (HIGH)
**File:** `src/deia/adapters/web/app.py` (search for command, input, send)
**Issue:** User sends command but gets no feedback that command was received
**Current State:** Message appears in history but no acknowledgment
**Fix Required:**
- Add immediate feedback when send button clicked
- Show command in chat with timestamp
- Wait for bot response (with timeout)
- Show bot's response when it arrives
- Handle timeouts (> 5 seconds with no response)
- Test: Type "help" → see message sent → see bot response

### 3. Error Messages Vague (HIGH)
**File:** `src/deia/adapters/web/app.py` (search for error, catch, alert)
**Issue:** Errors show generic messages that don't help user fix problem
**Current State:** "Error" or "Failed" without details
**Fix Required:**
- Catch all errors and show specific messages
- Network error: "Connection lost - check internet"
- Bot error: Show actual error from bot service
- Timeout: "Bot not responding - check if running"
- Validation: "Invalid command - type 'help' for options"
- Test: Intentionally break connection → see specific error message

### 4. Chat History Pagination/Reversal Bug (HIGH)
**File:** `src/deia/adapters/web/app.py` (search for history, scroll, load)
**Issue:** Chat history shows messages in wrong order or doesn't load old messages
**Current State:** Newest at top (should be bottom), or messages duplicate, or old messages missing
**Fix Required:**
- Verify messages are in chronological order (oldest → newest, bottom → top)
- Add pagination: Load 50 messages at a time
- Add "Load Earlier Messages" button
- Verify no duplicates when loading pages
- Test: Send 20+ messages → scroll up → click "Load Earlier" → old messages appear in order

---

## PARALLEL TASK (Do simultaneously)

**User Guide Documentation** (2 hours parallel with fixes)

**File:** `.deia/docs/USER-GUIDE.md`

**Content Required:**
1. **Quick Start** (5 min read)
   - How to launch the application
   - How to connect/launch a bot
   - How to send your first command

2. **Core Workflows** (detailed)
   - Launching a Bot (step-by-step)
   - Sending Commands (with examples)
   - Viewing Chat History (search, pagination, export?)
   - Switching Between Bots (context isolation)
   - Stopping a Bot (cleanup)

3. **Keyboard Shortcuts** (comprehensive list)
   - Enter to send message
   - Ctrl+K to clear chat
   - Ctrl+L to list all bots
   - Up/Down arrows for command history
   - etc. (match your actual implementation)

4. **Troubleshooting** (common issues)
   - "Bot won't launch" → checklist
   - "No response to commands" → checklist
   - "Can't see old messages" → checklist
   - "Connection lost" → recovery steps

5. **FAQ**
   - Can I run multiple bots? Yes/No?
   - How long do conversations persist?
   - Can I export chat history?
   - etc.

**Format:** Markdown with clear sections, code examples, screenshots if possible

---

## SUCCESS CRITERIA

**High Priority Fixes:**
- ✅ All 4 issues fixed in code
- ✅ Tested manually (verify each workflow works)
- ✅ Error handling verified
- ✅ Documented in status report

**User Guide:**
- ✅ All 5 sections complete (Quick Start, Workflows, Shortcuts, Troubleshooting, FAQ)
- ✅ Clear, concise language
- ✅ Examples provided
- ✅ Uploaded to `.deia/docs/USER-GUIDE.md`

**Overall:**
- ✅ All code committed/saved
- ✅ Status report uploaded
- ✅ Ready for next task

---

## STATUS REPORT LOCATION

**Due:** 2025-10-25 18:32 CDT

Create file: `.deia/hive/responses/deiasolutions/BOT-001-HIGH-FIXES-USER-GUIDE-WINDOW-1-COMPLETE.md`

**Include:**
- HIGH priority fixes (all 4 done?)
- Testing evidence per issue
- User Guide completion status
- User Guide file location
- Any blockers encountered
- Time spent on fixes vs. documentation
- Ready for Batch 1? (YES/NO)

---

## RESOURCES

- Port 8000 application: `src/deia/adapters/web/app.py`
- Bot service API: `src/deia/services/bot_service.py`
- Design review (context): `.deia/hive/responses/deiasolutions/PORT-8000-DESIGN-REVIEW.md`
- UX fixes (reference): `.deia/hive/responses/deiasolutions/PORT-8000-UX-FIXES.md`

---

## NOTES

- HIGH priority = breaks important workflows
- User Guide = help your users self-serve
- Balance between fixes and documentation (split time 50/50)
- If stuck on any fix > 15 min, file blocker immediately
- Autologging required: Update every 5-10 minutes
- Next task ready at 18:32 (Deployment Readiness Guide)

---

**Q33N - BEE-000**
**FIX HIGH PRIORITY ISSUES, WRITE USER GUIDE, REPORT AT 18:32**
