# DEBUG TRAIL: Bot Communication Failures

**Session Date:** 2025-10-28
**Session Time:** 22:42 UTC
**Status:** INVESTIGATION - Bot launches but communication endpoints fail

---

## INCIDENT SUMMARY

**What Happened:**
1. Bot launched successfully via web commander on port 8888
2. Bot process spawned successfully (subprocess running)
3. Chat prompt sent from web UI → **No response from bot**
4. Halt bot command attempted → **Failed to stop bot**

**Impact:** Bot launches but cannot be communicated with or controlled via web commander

---

## WHAT WORKS ✅

- Web commander starts on port 8888
- Bot launch API endpoint accepts requests
- Bot subprocess spawns (process running on assigned port)
- Bot listening on its assigned port (verified with netstat)

---

## WHAT FAILS ❌

### Failure 1: Chat Prompt Gets No Response
**Symptom:** Send prompt from web UI chat → silence
**Expected:** Bot responds with output
**What actually happens:** Request times out or returns no data

**Likely causes:**
- Bot HTTP server not properly initialized
- WebSocket connection not established
- Bot task endpoint (`/api/bot/{bot_id}/task`) not responding
- Task submission to subprocess failing

**Files to check:**
- `src/deia/adapters/bot_http_server.py` - HTTP server initialization
- `src/deia/services/chat_interface_app.py` - `call_bot_task()` function
- Bot process logs (`.deia/bot-logs/BOT-{id}-activity.jsonl`)

### Failure 2: Halt Bot Command Fails
**Symptom:** Click "stop bot" in UI → error
**Expected:** Bot process terminates
**What actually happens:** Command fails silently

**Likely causes:**
- Stop endpoint not implemented
- Process termination not working
- Bot process reference lost
- Signal not reaching subprocess

**Files to check:**
- `src/deia/services/chat_interface_app.py` - Bot stop endpoint
- `src/deia/adapters/bot_runner.py` - `stop()` method
- Process manager not tracking running bots

---

## ROOT CAUSE ANALYSIS (HYPOTHESIS)

The bot launches successfully (we improved `spawn_bot_process()`), but there's a **communication gap**:

1. **Bot spawned** ✅ - `run_single_bot.py` starts
2. **Bot initializes adapter** ✅ - BotRunner creates ClaudeCodeCLIAdapter
3. **Bot HTTP server starts** ? - bot_http_server might be failing silently
4. **Web commander tracks bot** ? - Service registry might not be updated
5. **Chat sends prompt to bot** ❌ - HTTP call to bot's task endpoint fails

**Most likely:** Bot's HTTP server not starting, or web commander doesn't know which port bot is on.

---

## NEXT INVESTIGATION STEPS

### Immediate (Priority P1)

1. **Check bot process logs:**
   ```bash
   tail -100 .deia/bot-logs/BOT-001-activity.jsonl
   tail -100 .deia/bot-logs/BOT-001-errors.jsonl
   ```
   Look for: HTTP server initialization, adapter errors, task processing

2. **Check if bot HTTP server is listening:**
   ```bash
   netstat -an | grep -E "8025|8026|8027"  # Common bot ports
   ```
   Should show bot listening on assigned port

3. **Manually test bot endpoint:**
   ```bash
   curl -X POST http://localhost:8025/api/bot/BOT-001/task \
     -H "Content-Type: application/json" \
     -d '{"command": "echo hello"}'
   ```
   Should return response or timeout

4. **Check web commander logs:**
   ```bash
   tail -100 /tmp/commander_8888.log
   ```
   Look for: Bot port assignment, HTTP errors, task forwarding

### Phase 2: Service Registry

5. **Verify bot is registered:**
   Check `.deia/hive/registry.json` - should show bot with assigned port

6. **Verify web commander knows bot port:**
   In `call_bot_task()` - does it correctly retrieve bot port from registry?

### Phase 3: Communication Flow

7. **Trace chat message flow:**
   - User sends prompt in chat UI
   - WebSocket message received by commander
   - `call_bot_task()` called
   - HTTP request sent to bot endpoint
   - Where does it fail?

---

## CODE PATHS TO REVIEW

**Bot Startup:**
- `run_single_bot.py` → creates BotRunner
- `src/deia/adapters/bot_runner.py:__init__()` → initializes adapter
- `src/deia/adapters/bot_runner.py:start()` → starts HTTP server
- `src/deia/adapters/bot_http_server.py` → creates FastAPI server

**Chat Message Flow:**
- WebSocket message in `chat_interface_app.py`
- Calls `call_bot_task(bot_id, command)`
- Looks up bot port in service registry
- Makes HTTP POST to `http://localhost:{port}/api/bot/{bot_id}/task`

**Bot Control:**
- Stop endpoint (if exists) in `chat_interface_app.py`
- Calls bot stop mechanism
- Needs to track process PID or use service registry

---

## KNOWN ISSUES

**Issue: Missing bot port assignment**
- Web commander spawns bot but might not register it in service registry
- `call_bot_task()` won't know which port bot is on
- Result: Cannot send prompts to bot

**Issue: HTTP server initialization**
- Bot HTTP server might be failing silently in background
- Check `bot_http_server.py` for errors
- Might need logging improvements

**Issue: Process control**
- No way to stop bot from web commander
- Need process tracking mechanism
- Service registry should store PID and port

---

## TESTING CHECKLIST

When resuming:
- [ ] Check bot process logs for startup errors
- [ ] Verify bot HTTP server is listening
- [ ] Manually test bot task endpoint
- [ ] Check service registry has bot entry
- [ ] Verify web commander can reach bot port
- [ ] Test chat prompt end-to-end with logging
- [ ] Test bot stop/halt functionality
- [ ] Check for race conditions in bot initialization

---

## FOR NEXT SESSION

**Priority:** Fix bot communication endpoints
- Time estimate: 2-4 hours
- Impact: Web chat will work with launched bots
- Blockers: Need to understand service registry, HTTP server initialization

**Deliverables:**
- [ ] Bot launch + task submission working
- [ ] Bot responses flowing back to chat UI
- [ ] Bot stop/control working
- [ ] Activity logs showing successful communication

---

**Investigation paused at:** 2025-10-28 22:42 UTC
**Resuming at:** Next session
**Status:** Ready for continuation - clear next steps documented
