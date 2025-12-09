# FIRE DRILL TASK: Bot Launcher Infrastructure (BOT-001)
**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-001 (CLAUDE-CODE-001)
**Date:** 2025-10-25 19:00 CDT
**Priority:** P0 - CRITICAL PATH
**Mode:** Fire Drill - Parallel execution

---

## Mission: Get Claude Code Bots Controllable & Launchable

We need working bot launcher infrastructure so BOT-003 can control bots from the chat interface.

---

## Task 1: Fix `run_single_bot.py` Subprocess Spawning (45 min)
**Status:** ACTION REQUIRED

**Current Problem:**
- `run_single_bot.py` fails to spawn interactive Claude Code subprocess
- Bots don't register in service registry
- Can't detect task queue changes

**Your Work:**
1. Open `run_single_bot.py`
2. Test `subprocess.Popen` vs `pty` module for Claude Code CLI spawning
3. Add debug logging to show where subprocess hangs
4. Implement timeout handling
5. Test launching one bot manually

**Success Criteria:**
- Bot subprocess starts without hanging
- Bot can be killed gracefully
- Subprocess output visible in logs

**File:** `run_single_bot.py`

---

## Task 2: Implement Bot Service HTTP Endpoints (60 min)
**Status:** ACTION REQUIRED

**What We Need:**
Each bot needs to expose HTTP API on assigned port (8001-8999) with:
- `GET /health` - Health check
- `GET /status` - Current bot status
- `POST /task` - Send task to bot
- `POST /stop` - Graceful shutdown
- `POST /interrupt` - Stop current work

**Your Work:**
1. Create `src/deia/services/bot_http_service.py` (if doesn't exist)
2. Implement above 5 endpoints
3. Auto-register bot in service registry (`.deia/hive/registry.json`)
4. Start service alongside bot process in `run_single_bot.py`

**Success Criteria:**
- Bot service starts on correct port
- Health endpoint responds
- Registry updates with bot info

**Files:**
- Create/enhance: `src/deia/services/bot_http_service.py`
- Modify: `run_single_bot.py` to start service

---

## Task 3: Implement Task Queue Monitoring (60 min)
**Status:** ACTION REQUIRED

**What We Need:**
Bot needs to watch its task folder and execute new tasks:

**Your Work:**
1. Create `src/deia/services/task_queue_monitor.py`
2. Bot monitors `.deia/hive/tasks/{bot-id}/` every 5 seconds
3. On new task:
   - Parse task file
   - Log receipt
   - Execute task (run command, write response)
   - Move task to archive
4. Write response to `.deia/hive/responses/{timestamp}-{bot-id}-RESPONSE-{task-id}.md`

**Success Criteria:**
- Bot detects new task files
- Task execution works
- Response file created

**Files:**
- Create: `src/deia/services/task_queue_monitor.py`
- Modify: `run_single_bot.py` to enable monitoring

---

## Task 4: Service Registry Integration (45 min)
**Status:** ACTION REQUIRED

**What We Need:**
Central registry so dashboard knows which bots are running:

**Your Work:**
1. Ensure `.deia/hive/registry.json` structure exists:
   ```json
   {
     "bots": {
       "BOT-001": {"port": 8001, "pid": 12345, "status": "running", "registered_at": "2025-10-25T19:00:00Z"},
       "BOT-003": {"port": 8003, "pid": 12346, "status": "running", "registered_at": "2025-10-25T19:00:00Z"}
     }
   }
   ```
2. On bot startup: register in registry
3. On bot shutdown: remove from registry
4. Implement `get_bot_port(bot_id)` helper function

**Success Criteria:**
- Registry creates/updates correctly
- Bot appears in registry when running
- Bot removed from registry on shutdown

**Files:**
- Modify: `run_single_bot.py` to update registry
- Create/enhance: `src/deia/services/registry.py`

---

## Task 5: Launch 2 Test Bots & Verify (45 min)
**Status:** ACTION REQUIRED

**Your Work:**
1. Launch BOT-001 instance: `python run_single_bot.py BOT-001 --adapter sdk`
2. Launch BOT-003 instance: `python run_single_bot.py BOT-003 --adapter sdk`
3. Verify both:
   - Appear in registry
   - Respond to `/health` requests
   - Accept POST /task requests
4. Create test task in `.deia/hive/tasks/BOT-001/` and verify response
5. Verify responses appear in `.deia/hive/responses/`

**Success Criteria:**
- 2 bots running simultaneously
- Both respond to HTTP requests
- Task queue works end-to-end
- Responses written correctly

---

## Deliverables (Report When Complete)

Create file: `.deia/hive/responses/deiasolutions/bot-001-fire-drill-status.md`

Include:
- [ ] `run_single_bot.py` fixed and tested
- [ ] Bot HTTP service working
- [ ] Task queue monitoring working
- [ ] Registry integration done
- [ ] 2 test bots launched and verified
- [ ] Evidence: Screenshots or logs of bot launches
- [ ] Any blockers or issues encountered

**Estimated Total Time:** 4 hours (broken into 5 parallel-able tasks)

---

## If You Get Stuck

Post blockers to: `.deia/hive/responses/deiasolutions/bot-001-questions.md`

Q33N (BEE-000) will respond within 30 minutes.

---

**Q33N out. BOT-001: Fire drill mode - get bot launcher working. Go.**
