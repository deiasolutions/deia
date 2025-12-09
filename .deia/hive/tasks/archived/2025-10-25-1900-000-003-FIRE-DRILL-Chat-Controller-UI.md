# FIRE DRILL TASK: Chat Controller UI (BOT-003)
**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-003 (CLAUDE-CODE-003)
**Date:** 2025-10-25 19:00 CDT
**Priority:** P0 - CRITICAL PATH
**Mode:** Fire Drill - Parallel execution

---

## Mission: Build Chat Interface for Bot Control

We need a clean, simple chat UI on port 8000 where you can launch bots and send them commands.

---

## Task 1: Enhance Dashboard Server HTML/CSS (60 min)
**Status:** ACTION REQUIRED

**Current State:**
- `llama-chatbot/app.py` has basic chat HTML
- Need to adapt for bot controller UI

**Your Work:**
1. Open `llama-chatbot/app.py` GET `/` endpoint
2. Enhance HTML UI to include:
   - **Left panel:** Active bot list with status (running/idle/error)
   - **Center panel:** Chat message history (scrollable)
   - **Bottom:** Input box for commands
   - **Top:** "Launch New Bot" button
3. Style with basic CSS (dark mode, clean layout, responsive)
4. Make it look like Claude Code's web interface

**Success Criteria:**
- UI loads on http://localhost:8000
- Chat history visible
- Input box works
- Bot list panel present
- Mobile-responsive layout

**Files:**
- Modify: `llama-chatbot/app.py` (HTML section)

---

## Task 2: Implement Bot Launch Controls (60 min)
**Status:** ACTION REQUIRED

**What We Need:**
UI buttons to launch/stop bots:

**Your Work:**
1. Add REST endpoints to `llama-chatbot/app.py`:
   - `POST /api/bot/launch` - Request: `{"bot_id": "BOT-001"}` → Launch bot
   - `POST /api/bot/stop/{bot_id}` - Stop running bot
   - `GET /api/bots` - List all active bots (from registry)
   - `GET /api/bot/{bot_id}/status` - Get bot status

2. Wire up "Launch New Bot" button to call `/api/bot/launch`
3. Add stop button for each bot in list
4. Call `/api/bots` every 2 seconds to refresh bot list

**Success Criteria:**
- Launch button triggers bot launch
- Bot appears in list after launch
- Stop button terminates bot
- List auto-refreshes

**Files:**
- Modify: `llama-chatbot/app.py` (add endpoints + JavaScript)

---

## Task 3: Implement WebSocket for Real-Time Bot Messages (60 min)
**Status:** ACTION REQUIRED

**What We Need:**
Real-time message streaming from bots as they respond:

**Your Work:**
1. Enhance WebSocket endpoint in `llama-chatbot/app.py`
2. Connect to bot HTTP services (via registry)
3. Forward bot responses to chat in real-time
4. Display bot typing indicator while working
5. Show "BOT-001 responded:" before each message

**Success Criteria:**
- WebSocket connects on load
- Messages stream in real-time
- Bot name/ID shown with messages
- Typing indicator displays during work

**Files:**
- Modify: `llama-chatbot/app.py` (WebSocket handling)
- Add JavaScript for client-side message handling

---

## Task 4: Implement Message Routing to Correct Bot (45 min)
**Status:** ACTION REQUIRED

**What We Need:**
When user types command, route to the right bot:

**Your Work:**
1. Add message input handler to send to selected bot
2. Detect which bot is "active" (selected in UI)
3. Route message to that bot's HTTP `/task` endpoint
4. Show response back in chat
5. Support format: `@bot-001 do this task` or default to selected bot

**Success Criteria:**
- User can type command and submit
- Command routes to correct bot
- Response appears in chat
- User knows which bot handled request

**Files:**
- Modify: `llama-chatbot/app.py` (message routing)
- Enhance JavaScript event handling

---

## Task 5: Implement Bot Status Dashboard (45 min)
**Status:** ACTION REQUIRED

**What We Need:**
Live status panel showing what each bot is doing:

**Your Work:**
1. Add status indicators:
   - Green "Running" - bot responsive
   - Yellow "Busy" - bot executing task
   - Red "Error" - bot crashed/unresponsive
   - Gray "Stopped" - bot offline

2. Show for each bot:
   - Bot ID
   - Current status
   - Current task (if executing)
   - Uptime
   - Quick actions (stop, restart, details)

3. Update status every 5 seconds via `/api/bot/{bot_id}/status`

**Success Criteria:**
- Status panel always visible
- Colors indicate state correctly
- Status updates live
- Shows useful info about each bot

**Files:**
- Modify: `llama-chatbot/app.py` (status endpoints)
- Enhance HTML/CSS for status display

---

## Task 6: Test End-to-End UI Flow (30 min)
**Status:** ACTION REQUIRED

**Your Work:**
1. Start chat controller: `python -m uvicorn llama_chatbot.app:app --port 8000`
2. Open http://localhost:8000 in browser
3. Test full flow:
   - Click "Launch BOT-001" button
   - Verify it appears in bot list
   - Type command in chat
   - Send to bot
   - Receive response in chat
   - Click stop button
   - Verify bot removed from list

4. Test with 2 bots running simultaneously

**Success Criteria:**
- Full UI flow works end-to-end
- No JavaScript errors
- Responsive and clean
- Ready for production use

---

## Deliverables (Report When Complete)

Create file: `.deia/hive/responses/deiasolutions/bot-003-fire-drill-status.md`

Include:
- [ ] Dashboard HTML/CSS enhanced (Task 1)
- [ ] Bot launch/stop controls working (Task 2)
- [ ] WebSocket real-time messaging working (Task 3)
- [ ] Message routing to correct bot working (Task 4)
- [ ] Bot status dashboard implemented (Task 5)
- [ ] End-to-end testing passed (Task 6)
- [ ] Evidence: Screenshots of working UI
- [ ] Any blockers or issues encountered

**Estimated Total Time:** 4 hours (tasks can run parallel with BOT-001)

---

## Important Notes

**Coordinate with BOT-001:**
- Don't start testing until BOT-001 has bots launching
- BOT-001 provides working bot launcher + registry
- You build UI to control what BOT-001 built

**Port 8000 is shared:**
- Dashboard backend and chat frontend both run on 8000
- Integrate into single FastAPI instance

**Keep it Simple:**
- Clean, minimal UI (not fancy)
- Focus on functionality over design
- Must work on localhost:8000

---

## If You Get Stuck

Post blockers to: `.deia/hive/responses/deiasolutions/bot-003-questions.md`

Q33N (BEE-000) will respond within 30 minutes.

---

**Q33N out. BOT-003: Fire drill mode - build chat controller. Go.**
