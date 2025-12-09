---
eos: "0.1"
kind: assignment
id: "2025-10-27-0745-000-NEW-BOT-CLAUDE-CLI-BOT-HARDENING"
assigned_to: "NEW-BOT-INSTANCE"
assigned_by: "Q33N (BEE-000)"
status: "ACTIVE"
priority: "P0"
session_date: "2025-10-27"
session_time: "07:45 CDT"
focus: "claude-code-cli-bot"
---

# 🎯 FOCUSED MISSION: Claude CLI Bot Hardening

**Objective:** Make the Claude Code CLI bot work reliably in the chatbot system
**Current Status:** Adapter exists but bot hangs with no output
**Blocker Level:** P0 - Cannot test chatbot MVP without working Claude CLI bot
**Scope:** Fix + validate + document

---

## THE PROBLEM

### Current State
- `ClaudeCodeCLIAdapter` exists in `src/deia/adapters/claude_code_cli_adapter.py`
- Bot launches via `run_single_bot.py` with `adapter_type="cli"`
- **Bot process starts but produces NO OUTPUT**
- Bot doesn't register in status board
- Bot doesn't pick up tasks from `.deia/hive/tasks/`
- **Dashboard E2E testing blocked**

### Root Cause (Known Issues)
1. **Subprocess initialization failing** - CLI adapter can't spawn interactive Claude Code subprocess
2. **stdin/stdout piping broken** - Output not being captured/returned
3. **Claude Code CLI may require TTY** - May need pseudo-terminal support
4. **Output buffering** - Process may be working but output hidden

### Historical Context
- 15+ hours of troubleshooting documented
- Multiple failed workarounds attempted
- Known workarounds: Mock bot (works), API bot (works), CLI bot (broken)

---

## YOUR MISSION: 3 FOCUSED TASKS

### TASK 1: Diagnose Claude CLI Subprocess Issue (1.5 hours)

**Goal:** Understand exactly why the subprocess hangs

**What to do:**

1. **Read the current adapter**
   - File: `src/deia/adapters/claude_code_cli_adapter.py`
   - Focus on: `__init__()`, `start_session()`, `send_task()` methods
   - File: `src/deia/adapters/claude_cli_subprocess.py` (the subprocess wrapper)
   - Understand: How it tries to spawn the `claude` CLI process

2. **Test subprocess manually**
   ```bash
   # Try to run claude CLI directly
   claude code --help

   # Try with a simple prompt
   claude code --prompt "print('hello')"

   # Try with piped stdin
   echo "print('hello')" | claude code
   ```
   - Document what works/fails
   - Note any error messages
   - Record: Does it require TTY? Interactive mode?

3. **Review the known issues**
   - Read: `.deia/observations/2025-10-24-CLI-BOT-SOLUTIONS-PROPOSAL.md`
   - Read: Previous session notes about subprocess failures
   - Identify: What was tried and what failed

4. **Create diagnosis report**
   - Document each test result
   - Identify: Is this a TTY issue? A piping issue? Missing timeout?
   - Hypothesis: What's actually broken

**Success criteria:**
- ✅ Understand the root cause
- ✅ Can explain why subprocess hangs
- ✅ Have 2-3 potential fixes identified
- ✅ Report in: `.deia/hive/responses/deiasolutions/NEW-BOT-claude-cli-diagnosis.md`

---

### TASK 2: Implement Fix (2 hours)

**Goal:** Get the Claude CLI bot subprocess working

**Based on Task 1, choose the best fix:**

#### Option A: PTY Support (If TTY is required)
If testing shows Claude Code needs a terminal:
```python
import pty
import subprocess

# Use pty instead of regular Popen
master, slave = pty.openpty()
process = subprocess.Popen(
    ["claude", "code", "--prompt", task],
    stdin=slave,
    stdout=slave,
    stderr=slave,
    text=True
)
```

**Files to modify:**
- `src/deia/adapters/claude_cli_subprocess.py`

**Time:** 1 hour

#### Option B: Output Buffering Fix
If Claude Code works but output isn't visible:
```python
# Use non-blocking reads
import fcntl
import select

# Set stdout to non-blocking
fcntl.fcntl(process.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

# Use select() to wait for output
while True:
    ready = select.select([process.stdout], [], [], timeout)
    if ready[0]:
        output = process.stdout.read()
```

**Files to modify:**
- `src/deia/adapters/claude_cli_subprocess.py`

**Time:** 1 hour

#### Option C: Timeout + Retry Logic
If subprocess starts but takes time to initialize:
```python
# Add startup delay and multiple retries
time.sleep(2)  # Wait for Claude Code to fully start
retries = 3
for attempt in range(retries):
    result = self.send_task(test_prompt, timeout=10)
    if result.success:
        return True
    time.sleep(1)  # Wait before retry
```

**Files to modify:**
- `src/deia/adapters/claude_code_cli_adapter.py`

**Time:** 30 min

---

### TASK 3: Validate & Test (1.5 hours)

**Goal:** Prove the Claude CLI bot works

**What to test:**

1. **Unit test the adapter**
   ```python
   # Test: Adapter can initialize
   adapter = ClaudeCodeCLIAdapter(
       bot_id="TEST-BOT-001",
       work_dir=Path.cwd()
   )

   # Test: Can start session
   assert adapter.start_session() == True

   # Test: Can send task and get response
   result = adapter.send_task("print('hello')")
   assert result.success == True
   assert result.output != ""
   ```

2. **Integration test with bot launcher**
   ```bash
   # Start bot with CLI adapter
   python run_single_bot.py TEST-BOT-001 --adapter cli

   # Verify bot registers
   # Check: Does it appear in status board?
   # Check: Does it respond to tasks?
   ```

3. **Create test task and verify response**
   - Write a task file to `.deia/hive/tasks/`
   - Wait for bot to pick it up
   - Verify bot writes response to `.deia/hive/responses/`
   - Check: Response is valid Claude Code output

4. **Stress test (optional)**
   - Send 3-5 tasks in sequence
   - Verify all get responses
   - Check for resource leaks
   - Verify clean shutdown

**Success criteria:**
- ✅ Adapter passes unit tests
- ✅ Bot starts without hanging
- ✅ Bot picks up tasks
- ✅ Bot writes responses
- ✅ All responses are valid
- ✅ Clean shutdown works
- ✅ Test results documented

**Report in:** `.deia/hive/responses/deiasolutions/NEW-BOT-claude-cli-validation.md`

---

## FILES INVOLVED

**Main files to work with:**
```
src/deia/adapters/claude_code_cli_adapter.py       (Bot coordinator wrapper)
src/deia/adapters/claude_cli_subprocess.py         (Low-level subprocess control)
src/deia/services/service_factory.py               (Bot type routing - don't modify)
src/deia/services/chat_interface_app.py            (Chat API - don't modify)
```

**Reference files:**
```
.deia/observations/2025-10-24-CLI-BOT-SOLUTIONS-PROPOSAL.md   (Context)
examples/cli_bot_runner_example.py                            (Example usage)
```

---

## WORKFLOW

### Step 1: Understand the Problem (30 min)
- Read this entire assignment
- Read the diagnosis proposal file
- Run Claude CLI manually to understand behavior

### Step 2: Run Diagnosis (1.5 hours)
- Execute Task 1 completely
- Document all findings
- Identify root cause
- Write diagnosis report

### Step 3: Implement Fix (2 hours)
- Based on diagnosis, implement best fix
- Test fix locally
- Handle any new issues that arise
- Keep detailed notes

### Step 4: Validate Solution (1.5 hours)
- Run unit tests
- Run integration tests
- Verify end-to-end flow
- Write validation report

### Step 5: Deliver Results (30 min)
- Create final summary
- Commit code changes
- Send completion report to Q33N

**Total time:** ~5.5 hours

---

## WHAT SUCCESS LOOKS LIKE

**When you're done:**

- ✅ Claude Code CLI bot subprocess works without hanging
- ✅ Bot process starts and registers in status board
- ✅ Bot picks up tasks from `.deia/hive/tasks/`
- ✅ Bot writes valid responses to `.deia/hive/responses/`
- ✅ Bot gracefully handles shutdown
- ✅ Unit tests pass
- ✅ Integration tests pass
- ✅ Diagnosis report explains the problem
- ✅ Validation report proves the fix works
- ✅ Code changes committed to git

**Next step after:** Claude CLI bot enabled in chatbot MVP → Dashboard E2E testing unblocked

---

## CRITICAL CONSTRAINTS

**Must Follow:**
1. **NO Unicode in output** - Use ASCII only (learned from incident)
2. **Document everything** - Each test result, each attempt, each failure
3. **Test before claiming success** - Verify with actual bot launcher, not just unit tests
4. **Keep Claude Code running** - Don't kill it without proper cleanup
5. **Monitor resources** - Watch for memory leaks, zombie processes

**Cannot Do Without Asking:**
- Change the chat_interface_app.py
- Modify service_factory.py routing logic
- Add new dependencies
- Change the bot adapter interface

---

## REPORTING PROTOCOL

### When you START
Create file: `.deia/hive/responses/deiasolutions/NEW-BOT-claude-cli-checkin.md`
Include:
- Start time
- Understanding of the problem
- Diagnosis plan
- Any blockers

### After DIAGNOSIS (Task 1)
Create file: `.deia/hive/responses/deiasolutions/NEW-BOT-claude-cli-diagnosis.md`
Include:
- Test results
- Root cause analysis
- Proposed fix
- Risk assessment

### After IMPLEMENTATION (Task 2)
Create file: `.deia/hive/responses/deiasolutions/NEW-BOT-claude-cli-implementation.md`
Include:
- Changes made
- Why this approach
- Any issues encountered
- Workarounds applied

### After VALIDATION (Task 3)
Create file: `.deia/hive/responses/deiasolutions/NEW-BOT-claude-cli-validation.md`
Include:
- Test results
- Pass/fail status
- Evidence (screenshots, logs)
- Recommendations

### FINAL REPORT
Create file: `.deia/hive/responses/deiasolutions/NEW-BOT-CLAUDE-CLI-BOT-HARDENING-COMPLETE.md`
Include:
- Executive summary
- All 3 task results
- Overall status
- Ready for production? YES/NO
- Next steps

---

## Q33N SUPPORT

I will monitor your progress in `.deia/hive/responses/deiasolutions/`

**Response time:** <30 min for blockers

**Escalation flags:**
- 🚨 BLOCKER - Can't proceed
- 🤔 UNCLEAR - Need clarification
- ❓ STUCK - Need help debugging
- 💡 FINDING - Discovered something important

---

## CONTEXT & KNOWLEDGE

**Why this matters:**
- Claude CLI bot is the "scrum master" bot in the original architecture
- It's the one that actually does file operations and code changes
- Chat MVP depends on all 5 bot types working
- This bot specifically handles developer workflows

**What you need to know:**
- Claude Code CLI is a real tool (`claude` command from Anthropic)
- It runs in subprocess mode here, not as interactive session
- The adapter wraps it for use in the chatbot system
- Previous attempts have been unsuccessful due to subprocess issues

**How to think about it:**
- View the subprocess as a black box that needs input/output management
- Focus on: How do we feed it tasks and get responses out?
- The fix is likely small but critical (TTY, buffering, timeout, etc.)

---

## SUCCESS DEFINITION

**You're done when:**

1. Claude CLI bot launches without hanging ✅
2. Bot appears in status board within 10 seconds ✅
3. Bot responds to tasks within 30 seconds ✅
4. All tests pass ✅
5. Documentation complete ✅
6. Code committed to git ✅
7. Q33N has verified results ✅

---

## 🎯 GO SIGNAL

**You are cleared to proceed immediately on Claude CLI bot work.**

This is **P0 critical path** - once this is fixed, dashboard E2E testing unblocks.

Expect you in response files with diagnosis report in ~2 hours.

---

**Assignment issued:** 2025-10-27 07:45 CDT
**Issued by:** Q33N (BEE-000)
**Authority:** Dave
**Priority:** P0 CRITICAL

Ready to make Claude CLI bot solid. 🚀

---

**See you in the response files.**
