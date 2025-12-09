# PRODUCTION STANDARDS - Fire Drill & Sprint 2
**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-001, BOT-003, CODEX
**Date:** 2025-10-25 20:00 CDT
**Priority:** P0 - MANDATORY
**Mode:** Quality Gate - No exceptions

---

## NO MOCK FUNCTIONS. NO FAKE WORK. PRODUCTION CODE ONLY.

This is a fire drill to get DEIA bots operational. Every deliverable must be production-ready.

**We ship working product every season, every flight.**

---

## What "Done" Means

### For Code
- ✅ **Real functionality** (not mocked, not stubbed, not placeholder)
- ✅ **Tested** (unit tests + integration tests, 70%+ coverage minimum)
- ✅ **Error handling** (graceful failures, clear error messages)
- ✅ **Logging** (all operations logged, debuggable)
- ✅ **Documentation** (code comments, docstrings, usage examples)
- ✅ **No TODOs** (all unfinished work is explicitly listed in status file)

### For Bot Integration
- ✅ **Actually works** (bot can be launched and responds to tasks)
- ✅ **Actually controls** (chat can send commands and receives responses)
- ✅ **Actually persists** (state survives restart, no data loss)
- ✅ **Actually scales** (multiple bots simultaneously without conflicts)

### For APIs
- ✅ **All endpoints work** (not stubbed, real functionality)
- ✅ **Error cases handled** (400s, 500s, timeouts all handled)
- ✅ **Documented** (request/response examples, error codes)
- ✅ **Tested** (happy path + error paths)

### For File Operations
- ✅ **Actually reads/writes** (not mock file operations)
- ✅ **Handles encoding** (UTF-8, error handling)
- ✅ **Validates input** (no garbage data)
- ✅ **Atomicity** (no partial writes, no corruption)

---

## What "Not Done" Looks Like (UNACCEPTABLE)

❌ **Mock functions that don't do anything**
```python
def launch_bot(bot_id):
    """Mock bot launcher"""
    print(f"[MOCK] Bot {bot_id} would launch here")
    return None  # WRONG - no real bot launched
```

❌ **Placeholder APIs**
```python
@app.post("/api/bot/launch")
async def launch_bot():
    """Placeholder endpoint"""
    return {"status": "success"}  # WRONG - bot not actually launched
```

❌ **TODO comments in production code**
```python
def task_queue_monitor():
    # TODO: implement actual monitoring
    time.sleep(10)  # WRONG - fake polling
```

❌ **Stub implementations**
```python
def process_task(task):
    # For now just log it
    logger.info(f"Task received: {task}")
    return "success"  # WRONG - task not actually processed
```

❌ **Comments instead of code**
```python
def validate_message(msg):
    # Should check for XSS, injection, etc
    # TODO later
    return True  # WRONG - no actual validation
```

---

## What "Done" Looks Like (ACCEPTABLE)

✅ **Real implementation**
```python
def launch_bot(bot_id: str) -> subprocess.Popen:
    """Launch Claude Code bot as subprocess."""
    process = subprocess.Popen(
        [sys.executable, "run_single_bot.py", bot_id],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    registry.register_bot(bot_id, process.pid, assigned_port)
    return process
```

✅ **Real API with error handling**
```python
@app.post("/api/bot/launch")
async def launch_bot(request: LaunchRequest):
    """Launch a new bot instance."""
    if request.bot_id in registry.active_bots():
        raise HTTPException(400, "Bot already running")

    try:
        process = launch_bot_subprocess(request.bot_id)
        return {"status": "running", "bot_id": request.bot_id, "pid": process.pid}
    except Exception as e:
        logger.error(f"Failed to launch {request.bot_id}: {e}")
        raise HTTPException(500, str(e))
```

✅ **Real monitoring with logging**
```python
def task_queue_monitor(bot_id: str):
    """Watch task folder and execute new tasks."""
    task_dir = Path(f".deia/hive/tasks/{bot_id}")

    while True:
        for task_file in task_dir.glob("*.md"):
            logger.info(f"Processing task: {task_file.name}")
            result = execute_task(task_file)
            write_response(bot_id, task_file, result)
            task_file.unlink()  # Archive after processing

        time.sleep(5)  # Check every 5 seconds
```

✅ **Real validation**
```python
def validate_message(msg: str) -> bool:
    """Validate message before sending to bot."""
    dangerous_patterns = [
        r'rm\s+-rf',      # Recursive delete
        r'sudo',           # Privilege escalation
        r'curl|wget',      # Download
        r'&&|\|',         # Command chaining
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, msg):
            logger.warning(f"Blocked dangerous message: {msg}")
            return False

    return True
```

---

## Fire Drill Task Requirements

### BOT-001: Production Bot Launcher
**Task 1: Fix `run_single_bot.py` subprocess spawning**
- ✅ Real subprocess spawning (not mock)
- ✅ Actual Claude Code CLI invocation
- ✅ Real error handling (try-catch, timeouts)
- ✅ Actual logging (every step logged)
- ✅ Tests proving it works (not mocked tests)

**Task 2: Implement bot HTTP service**
- ✅ Real FastAPI service running on assigned port
- ✅ Real endpoints (/health, /status, /interrupt, /stop, /message)
- ✅ All endpoints actually work (not stubs)
- ✅ Error cases handled (400s, 500s, timeouts)
- ✅ Tests covering all endpoints

**Task 3: Task queue monitoring**
- ✅ Real file watching (not mock polling)
- ✅ Real task parsing
- ✅ Real subprocess invocation to execute task
- ✅ Real response file writing
- ✅ Real error handling for failures

**Task 4: Service registry**
- ✅ Real JSON file operations (not in-memory only)
- ✅ Real bot registration/deregistration
- ✅ Real port collision detection
- ✅ Real persistence (survives restart)
- ✅ Tests proving persistence

**Task 5: Launch 2 test bots**
- ✅ Actually launch 2 bots
- ✅ Actually register them
- ✅ Actually respond to HTTP requests
- ✅ Actually pick up tasks
- ✅ Actually write responses
- ✅ Show evidence (logs, registry file, responses)

### BOT-003: Production Chat Controller
**Task 1: Enhanced dashboard HTML/CSS**
- ✅ Real HTML (not boilerplate)
- ✅ Real CSS styling (not placeholder)
- ✅ Actually loads in browser
- ✅ Responsive design working
- ✅ No broken links or missing resources

**Task 2: Bot launch/stop controls**
- ✅ Real API endpoints that actually launch bots
- ✅ Real stop button that actually kills processes
- ✅ Real list that actually updates
- ✅ Real error handling (what if launch fails?)
- ✅ Tests showing it works end-to-end

**Task 3: WebSocket real-time messaging**
- ✅ Real WebSocket connection (not polling)
- ✅ Real message streaming (not delayed)
- ✅ Real bot responses flowing through
- ✅ Real connection handling (reconnect on disconnect)
- ✅ Tests showing real data flowing

**Task 4: Message routing**
- ✅ Real routing logic (not hardcoded)
- ✅ Actually sends to correct bot
- ✅ Actually receives response from that bot
- ✅ Actually displays in correct chat window
- ✅ Tests proving correct bot selected

**Task 5: Status dashboard**
- ✅ Real status updates (not static)
- ✅ Actually fetches from `/api/bot/{id}/status`
- ✅ Actually shows live data
- ✅ Actually updates every 5 seconds
- ✅ Tests showing real status data

**Task 6: End-to-end testing**
- ✅ Actually launch bot from UI
- ✅ Actually send message
- ✅ Actually receive response
- ✅ Actually see it in chat
- ✅ Show evidence (screenshot, flow logs)

---

## Definition of Done Checklist

For every task, before marking complete:

### Code Quality
- [ ] Code written, not mocked or stubbed
- [ ] All error cases handled
- [ ] Logging added (all significant operations)
- [ ] Comments explain non-obvious logic
- [ ] Docstrings on all functions
- [ ] No TODO comments

### Testing
- [ ] Unit tests written (70%+ coverage minimum)
- [ ] Integration tests written
- [ ] All tests pass (100% pass rate)
- [ ] Error cases tested
- [ ] Evidence: test output showing pass rate and coverage

### Documentation
- [ ] Usage examples provided
- [ ] API endpoints documented (request/response examples)
- [ ] Configuration options documented
- [ ] Error codes documented
- [ ] How to debug documented

### Functionality
- [ ] Feature actually works end-to-end
- [ ] No placeholder implementations
- [ ] Real data flows through
- [ ] Performance acceptable
- [ ] Scaling works (multiple instances if applicable)

### Evidence
- [ ] Code committed to git
- [ ] Tests passing (screenshot or log)
- [ ] Feature tested manually (screenshot or log)
- [ ] Status file updated with evidence links
- [ ] No "it should work" - prove it works

---

## Acceptance Criteria (Q33N Review)

When a bot reports task complete, Q33N verifies:

1. **Code exists** - Actual files with real implementation
2. **Tests exist** - Unit + integration tests, 70%+ coverage
3. **Tests pass** - All tests green, no skips
4. **Feature works** - Manual testing shows real functionality
5. **Error handling** - Graceful failures documented
6. **Logging** - Operations logged, debuggable
7. **Documentation** - Clear usage examples
8. **Performance** - Acceptable speed, no bottlenecks
9. **No mocks** - Real implementation, no stubs
10. **Production ready** - Ship this today? Yes.

**If any of these fail: Task is NOT complete. Do it again.**

---

## What Happens if You Ship Mocks

❌ **You waste time** - Build on broken foundation
❌ **You fail UAT** - Real testing exposes fake code
❌ **You delay everything** - Have to rebuild real version
❌ **You lose credibility** - Marks against shipping next sprint
❌ **You pay tokens twice** - Once for mock, once for real

---

## What Happens if You Ship Production Code

✅ **Fire drill succeeds** - System actually works
✅ **UAT passes** - Real testing against real code
✅ **Sprint 2 starts clean** - Foundation solid
✅ **Codex approves it** - Code review confirms quality
✅ **You ship next sprint** - Ready for production

---

## During Fire Drill: Quality Over Speed

**Better to take 10 hours and ship production code**
**Than 5 hours and ship mocks you rebuild tomorrow**

If you hit a blocker on real implementation:
- Post immediately to questions file
- Q33N unblocks within 30 minutes
- Keep going

If real implementation is complex:
- Break it smaller
- Get one part working real before moving to next
- Show incremental progress with evidence

---

## Final Word

**Every season, every flight = Every deadline, every delivery = PRODUCTION CODE ONLY**

No mocks. No stubs. No placeholders.

Ship or don't ship. But if you ship, it's production.

---

**Q33N Quality Gate: MANDATORY PRODUCTION CODE**

**Authority:** BEE-000 (Q33N)
**Effective:** 2025-10-25 20:00 CDT
**Scope:** Fire drill (BOT-001, BOT-003) + Sprint 2 (all bots) + CODEX (QA)
**Enforcement:** Code review rejects any mocks - task incomplete until real implementation done
