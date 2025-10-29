# Project Resume - 2025-10-29 Session

**Session Status:** IN PROGRESS - Claude Code CLI adapter debugging
**Time:** 07:52 UTC - 13:25 UTC
**Main Focus:** Bot communication system - fixing CLI adapter subprocess issue

---

## What Has Been Fixed Today ✅

### 1. Bot Heartbeat Mechanism (FIXED)
- **Problem:** Bots were disappearing from registry 5 minutes after launch
- **Root Cause:** No heartbeat being sent to ServiceRegistry, triggering stale entry cleanup
- **Solution:** Added heartbeat every 10 seconds in `BotRunner.run_continuous()`
- **File:** `src/deia/adapters/bot_runner.py:397-404`
- **Commit:** `4d78e3a`

### 2. Bot Port Assignment (FIXED)
- **Problem:** Web commander assigned port but didn't tell bot which port to listen on
- **Root Cause:** `spawn_bot_process()` wasn't passing `--port` parameter
- **Solution:** Added `--port` parameter to bot spawn command
- **Files:** `src/deia/services/chat_interface_app.py:119-147, 783`
- **Commit:** `25d54a8`

### 3. Bot Task Endpoint URL (FIXED)
- **Problem:** Web commander calling wrong endpoint (`/api/bot/{bot_id}/task`)
- **Root Cause:** Endpoint mismatch - bot HTTP server exposes `/api/task`
- **Solution:** Fixed URL in `call_bot_task()` function
- **File:** `src/deia/services/chat_interface_app.py:245-250`
- **Commit:** `c412b83`

### 4. Git Cleanup (FIXED)
- **Removed:** Temporary Excel lock file from simulations
- **Commit:** `108063c`

---

## What Works Now ✅

**Mock Bot Type (bot_type: "claude"):**
- ✅ Web commander launches bot successfully
- ✅ Bot registers in service registry with heartbeat
- ✅ Port assignment and HTTP server startup works
- ✅ Task submission to `/api/task` endpoint works
- ✅ Task execution completes successfully
- ✅ Full communication flow: launch → register → task → response

**Tested Successfully:**
```bash
POST /api/bot/launch
{"bot_id": "BOT-999", "bot_type": "claude"}
→ Returns: success, port 8118, PID 31408

POST http://localhost:8118/api/task
{"command": "Hello", "task_id": "test-1"}
→ Returns: status "queued", task accepted

Bot logs show:
- task_received ✅
- task_started ✅
- task_completed ✅ (5.7ms execution time)
```

---

## What's Not Working - Claude Code CLI ❌

**Claude Code CLI Bot Type (bot_type: "claude-code"):**
- ❌ Bot subprocess fails to start properly
- ❌ ClaudeCodeProcess.start() returns False
- ❌ Adapter crashes when trying to execute tasks

**Symptoms:**
- Bot logs show: "Claude Code process failed to start (returned False)"
- When user sends prompt: task times out after 300 seconds
- Error: `'NoneType' object has no attribute 'name'` in bot runner

**Root Issue Being Investigated:**
- Claude Code CLI is interactive shell-based, not pipe-friendly
- `ClaudeCodeProcess` tries to spawn `claude` as subprocess with stdin/stdout pipes
- Process may be exiting immediately or not accepting piped input properly
- Need to debug subprocess initialization in `claude_cli_subprocess.py:93-182`

---

## Current System State

**Web Commanders Running:**
- Port 8890: ACTIVE (running with all fixes)
- Base URL: `http://127.0.0.1:8890/`

**Service Registry State:**
- BOT-222: port 8251, status active, heartbeat 08:11:31
- BOT-445: port 8026, status active, heartbeat 08:11:26
(Both from earlier test runs, still have heartbeats = fixes work!)

**Git Status:**
```
Branch: master
Commits made today: 4
Latest: c412b83 (fix: Correct bot task endpoint URL)
Working directory: CLEAN
```

**Commits This Session:**
1. `108063c` - cleanup: Remove temporary Excel lock file
2. `4d78e3a` - fix: Send service registry heartbeat from bot runner
3. `25d54a8` - fix: Pass assigned port to bot process for HTTP server
4. `c412b83` - fix: Correct bot task endpoint URL in call_bot_task()

---

## What Needs To Happen Next

### Priority 1: Fix Claude Code CLI Subprocess (CRITICAL)
The MVP needs claude-code bot type working. Current blocker is subprocess startup.

**Investigation needed:**
1. Why does `ClaudeCodeProcess.start()` return False?
2. Is Claude CLI actually being found/invoked?
3. Does Claude CLI support non-interactive stdin mode?
4. Should we use `claude code` (with "code" argument) instead of just `claude`?

**Next steps:**
- Debug subprocess spawn in `claude_cli_subprocess.py`
- Add verbose logging to understand why process.start() fails
- Test if `claude code` command exists and accepts stdin
- Verify environment setup (PATH, API keys) is correct

### Priority 2: Test Full Flow
Once CLI adapter works, test complete flow:
- Launch CLI bot via web commander
- Send prompt via web UI
- Verify bot processes task
- Verify response returns to UI

### Priority 3: Documentation
- Update handoff document with final fixes
- Document what works (mock bots) vs what's broken (CLI adapter)
- Create debugging guide for future sessions

---

## Key Discoveries

1. **Architecture is Sound:** The 3-part communication fix works perfectly - heartbeats keep bots alive, port passing works, endpoint routing works. Proven by mock bot succeeding completely.

2. **Subprocess Issue is Isolated:** Only ClaudeCodeCLIAdapter is broken. All other components (web commander, registry, HTTP server, task queuing) work perfectly.

3. **Mock Bot Proves the System:** BOT-999 (mock type) completed task in 5.7 milliseconds with full logging. This proves the entire stack works.

---

## Testing Recommendations

Before giving to user again:
1. ✅ Mock bot end-to-end (DONE - works perfectly)
2. ❌ Claude Code CLI subprocess debugging (IN PROGRESS)
3. ❌ CLI bot end-to-end test
4. ❌ Multi-bot testing (launch multiple bots, send prompts to different bots)
5. ❌ Bot failure recovery (kill bot, verify registry cleanup)

---

## Resume Instructions for Next Session

1. Web commander is running on port 8890 - reuse it
2. Test mock bot first if you need quick validation (type: "claude" works perfectly)
3. Focus on debugging `claude_cli_subprocess.py:93-182` for CLI adapter fix
4. Check if Claude CLI needs special flags (like `claude code` vs `claude`)
5. Review error logs in `.deia/bot-logs/BOT-BOT-*-errors.jsonl` for subprocess details

---

**Session paused at:** 2025-10-29 13:25 UTC
**Ready for reboot and continuation**

Q33N 🤖
