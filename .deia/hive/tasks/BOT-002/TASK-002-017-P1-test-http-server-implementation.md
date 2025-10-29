# TASK-002-017: Test HTTP Server Implementation

**Task ID:** TASK-002-017
**Bot ID:** BOT-002
**Priority:** P1
**Created:** 2025-10-28
**Timeout:** 600 seconds

---

## OBJECTIVE

Validate and test the HTTP server implementation that was just coded (TASK-002-011, 012, 013).

BOT-002 should:
1. Review the implemented code
2. Test all endpoints
3. Verify priority queue logic
4. Verify response tagging
5. Report any bugs or issues found
6. Provide recommendations for fixes

---

## BACKGROUND

The developer just implemented:
- `src/deia/adapters/bot_http_server.py` - FastAPI HTTP/WebSocket server
- Modified `src/deia/adapters/bot_runner.py` - Added HTTP integration, priority queue, response tagging
- Modified `run_single_bot.py` - Added --port flag

Code was committed in git commit: `bb53152`

**What was implemented:**

### HTTP Server (bot_http_server.py)
- FastAPI app with three endpoints:
  - GET `/status` - Returns bot health/status
  - POST `/api/task` - HTTP task submission
  - WebSocket `/ws` - Real-time WebSocket interaction
- asyncio.Queue for task queueing (max 100)
- Proper error handling and logging

### BotRunner Integration (bot_runner.py)
- Added `port` parameter to __init__
- WebSocket queue check FIRST (priority over file queue)
- Response tagging with:
  - `source` field ("file" or "websocket")
  - `timestamp` field (ISO 8601 with Z)
- `_start_http_server()` method to start server in background
- HTTP server cleanup in `stop()` method

### Command-line Support (run_single_bot.py)
- Added `--port` argument (optional, int)
- Passed port to BotRunner
- Logging when port specified

---

## TESTING REQUIREMENTS

### Code Review:
- [ ] Read bot_http_server.py - verify all endpoints implemented
- [ ] Read bot_runner.py changes - verify priority logic correct
- [ ] Check run_single_bot.py - verify --port flag works
- [ ] Verify imports are correct (asyncio, threading, uvicorn, FastAPI)
- [ ] Check for obvious bugs or issues

### Functional Testing (if possible):
- [ ] Attempt to start BOT-002 with --port flag
  ```bash
  python run_single_bot.py BOT-002 --port 8002
  ```
- [ ] Test /status endpoint
  ```bash
  curl http://localhost:8002/status
  ```
- [ ] Test /api/task endpoint (if running)
- [ ] Verify HTTP server starts without crashing

### Quality Checks:
- [ ] No syntax errors
- [ ] All required imports present
- [ ] No obvious logic errors
- [ ] Error handling looks adequate
- [ ] Comments are clear

---

## EXPECTED ISSUES TO LOOK FOR

1. **Async/await issues:**
   - `get_next_websocket_task()` might not work in sync context
   - asyncio.Queue operations in non-async code

2. **Event loop issues:**
   - Running asyncio in separate thread might need event loop setup
   - uvicorn server startup in thread might cause issues

3. **Queue handling:**
   - WebSocket queue might not be properly accessed
   - Non-blocking get might fail

4. **Response tagging:**
   - Source and timestamp might not be included in responses
   - ISO timestamp format might be wrong

5. **Priority logic:**
   - WebSocket task check might skip file tasks
   - Priority might not be properly enforced

---

## TESTING PROCEDURE

### Step 1: Code Review
Review the three files:
1. `src/deia/adapters/bot_http_server.py` - Full review
2. `src/deia/adapters/bot_runner.py` - Focus on modified sections
3. `run_single_bot.py` - Check --port additions

### Step 2: Static Analysis
- Check for Python syntax errors
- Verify all imports
- Look for obvious logic errors
- Check error handling

### Step 3: Runtime Testing (if possible)
- Try to start bot with --port
- Monitor for crashes or errors
- Try to hit endpoints
- Check logs for errors

### Step 4: Report Findings
Document:
- Any bugs found
- Any issues with implementation
- Any missing pieces
- Recommendations for fixes
- Overall assessment (working/not working)

---

## DELIVERABLES

1. **Code Review Report**
   - Summary of what was implemented
   - Any issues found
   - Quality assessment

2. **Test Results**
   - Did server start?
   - Did endpoints work?
   - Any errors?

3. **Bug Report (if needed)**
   - Description of each bug
   - Where it is (file:line)
   - How to reproduce
   - Suggested fix

4. **Recommendations**
   - What needs to be fixed
   - What needs improvement
   - Priority of fixes

---

## ACCEPTANCE CRITERIA

✅ **Code Review Complete:**
- [ ] All three files reviewed
- [ ] No obvious syntax errors found
- [ ] Imports verified
- [ ] Logic reviewed

✅ **Issues Documented:**
- [ ] Any bugs clearly described
- [ ] Location of bugs specified
- [ ] Reproduction steps provided

✅ **Recommendations Clear:**
- [ ] Fix priorities established
- [ ] Implementation guidance provided
- [ ] Timeline estimate given

---

## NOTES

- This is a CODE REVIEW and TESTING task for BOT-002
- BOT-002 should act as a QA engineer reviewing the developer's work
- Be thorough but constructive
- Focus on finding real issues, not nitpicks
- Provide actionable feedback

---

**Status:** Ready for execution by BOT-002
**Assigned to:** BOT-002
**Priority:** P1

