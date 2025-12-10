# CLI BOT SOLUTIONS - PROPOSAL FOR APPROVAL

**Date:** 2025-10-24
**Status:** AWAITING USER APPROVAL
**Context:** CLI bot adapter broken - bots hang with no output

---

## Problem Summary

**Current State:**
- `run_single_bot.py` with `adapter_type="cli"` launches bot subprocess
- Bot process starts but produces no output
- Bot doesn't register in status board
- Bot doesn't pick up tasks from `.deia/hive/tasks/`
- Cannot test dashboard end-to-end without working bots

**Root Cause (Suspected):**
- `ClaudeCodeCLIAdapter` in `src/deia/adapters/claude_code_cli_adapter.py` fails to spawn interactive Claude Code subprocess
- May be subprocess initialization issue
- May be stdin/stdout piping issue
- May be Claude Code CLI requiring interactive terminal

**Documented in:**
- `.deia/observations/2025-10-24-UNICODE-ERROR-INCIDENT-28.md` (mentions bot testing failure)
- This session history (15 hours of troubleshooting)

---

## Proposed Solutions

### Option A: Mock Bot for Testing [RECOMMENDED]

**Description:** Create a simple mock bot that implements file-based coordination without Claude Code CLI.

**Implementation:**
```python
# src/deia/adapters/mock_bot_adapter.py

import time
from pathlib import Path
from datetime import datetime

class MockBotAdapter:
    """Simple mock bot for testing file-based coordination."""

    def __init__(self, bot_id: str, work_dir: Path):
        self.bot_id = bot_id
        self.work_dir = work_dir
        self.task_dir = work_dir / ".deia" / "hive" / "tasks"
        self.response_dir = work_dir / ".deia" / "hive" / "responses"
        self.running = False

    def run_continuous(self, cooldown: int = 10):
        """Watch task folder and respond to new tasks."""
        self.running = True
        print(f"[{self.bot_id}] Mock bot started")
        print(f"[{self.bot_id}] Watching: {self.task_dir}")

        while self.running:
            # Check for new tasks
            task_files = list(self.task_dir.glob("*.md"))

            for task_file in task_files:
                # Check if this task is for this bot
                if self.bot_id in task_file.name:
                    print(f"[{self.bot_id}] Found task: {task_file.name}")

                    # Read task
                    task_content = task_file.read_text()

                    # Generate simple response
                    response_content = f"""# RESPONSE: {task_file.stem}

**From:** {self.bot_id}
**Timestamp:** {datetime.utcnow().isoformat()}Z

## Response

Received and processed task: {task_file.name}

Task content preview:
```
{task_content[:200]}...
```

This is a mock bot response for testing purposes.

Status: [OK] Task acknowledged
"""

                    # Write response
                    response_file = self.response_dir / f"{datetime.utcnow().strftime('%Y-%m-%d-%H%M')}-{self.bot_id}-RESPONSE-{task_file.stem}.md"
                    response_file.write_text(response_content)
                    print(f"[{self.bot_id}] Wrote response: {response_file.name}")

                    # Move task to archive (acknowledgment)
                    archive_dir = self.task_dir / "archive"
                    archive_dir.mkdir(exist_ok=True)
                    task_file.rename(archive_dir / task_file.name)
                    print(f"[{self.bot_id}] Archived task: {task_file.name}")

            # Cooldown
            time.sleep(cooldown)

    def stop(self):
        """Stop the bot."""
        self.running = False
        print(f"[{self.bot_id}] Mock bot stopped")
```

**Usage:**
```bash
python run_single_bot.py CLAUDE-CODE-TEST-001 --adapter mock --cooldown 5
```

**Pros:**
- Simple, guaranteed to work
- No dependency on Claude Code CLI subprocess issues
- Can test dashboard coordination immediately
- Provides baseline for comparing with real CLI bot behavior

**Cons:**
- Not testing actual Claude Code CLI integration
- Mock responses not intelligent
- Doesn't validate subprocess management

**Time to Implement:** 1-2 hours

**Recommendation:** Do this FIRST to unblock dashboard testing

---

### Option B: Fix CLI Adapter Interactive Mode

**Description:** Debug and fix `ClaudeCodeCLIAdapter` to properly spawn interactive Claude Code subprocess.

**Investigation Steps:**
1. Read `src/deia/adapters/claude_code_cli_adapter.py`
2. Test subprocess spawning manually
3. Check stdin/stdout/stderr piping
4. Verify Claude Code CLI can run in non-interactive mode
5. Add debug logging to adapter

**Potential Issues:**
- Claude Code CLI may require TTY (pseudo-terminal)
- Subprocess may need `pty` module instead of `subprocess.Popen`
- Claude Code CLI may have startup delay
- Output buffering causing apparent hang

**Pros:**
- Fixes the actual problem
- Enables real multi-bot coordination
- Tests actual architecture we'll use in production

**Cons:**
- Time-consuming debugging (could be 4-8 hours)
- May discover Claude Code CLI doesn't support this usage
- Blocks dashboard testing until fixed

**Time to Implement:** 4-8 hours (uncertain)

**Recommendation:** Do this AFTER Option A unblocks dashboard testing

---

### Option C: Get Working API Key

**Description:** Use API adapter instead of CLI adapter.

**Requirements:**
- Funded Anthropic API key
- User provides key OR adds credits to existing key

**Pros:**
- API adapter already working (tested in previous session)
- No subprocess issues
- Simpler architecture

**Cons:**
- Costs money per bot message
- Not the intended architecture (scrum master uses CLI bots)
- Doesn't test subprocess coordination
- Requires network connectivity

**Time to Implement:** 0 hours (if key available)

**Recommendation:** Only if user prefers API bots over CLI bots

---

### Option D: Manual Dashboard Testing

**Description:** Skip bot integration, test dashboard manually by creating mock task/response files.

**Process:**
1. Start dashboard
2. Manually create task file in `.deia/hive/tasks/`
3. Manually create response file in `.deia/hive/responses/`
4. Verify dashboard detects files and displays messages

**Pros:**
- No bot needed
- Tests dashboard file watching and WebSocket updates
- Quick validation of dashboard functionality

**Cons:**
- Doesn't test actual bot communication
- Manual process, not automated
- Doesn't validate end-to-end flow

**Time to Implement:** 30 minutes

**Recommendation:** Use this to verify dashboard works before implementing bot solutions

---

## Recommended Approach

**Phase 1: Verify Dashboard (Immediate)**
1. Use Option D to manually test dashboard file watching
2. Confirm compact messages, scrolling, and WebSocket updates work
3. Time: 30 minutes

**Phase 2: Unblock Bot Testing (Short-term)**
1. Implement Option A (Mock Bot)
2. Test dashboard with mock bot responses
3. Verify end-to-end coordination flow
4. Time: 1-2 hours

**Phase 3: Fix Real CLI Bots (Medium-term)**
1. Debug Option B (Fix CLI Adapter)
2. Replace mock bot with real CLI bot
3. Validate scrum master architecture
4. Time: 4-8 hours

**Total Time:** 6-11 hours

---

## User Decision Required

Please approve one of the following:

1. **Full recommended approach** (Phases 1-3)
2. **Quick validation only** (Phase 1 - Option D)
3. **Mock bot only** (Phases 1-2 - Options D + A)
4. **API bots instead** (Option C - requires funded API key)
5. **Custom approach** (specify)

---

## Constraints

**Must Follow:**
- NO Unicode in print statements (use ASCII only)
- Use `deia bok` / `deia librarian` BEFORE searching files
- Test thoroughly before presenting to user
- Document all work in observations
- Follow integration protocol when complete

**Cannot Do Without Approval:**
- Implement any code changes
- Modify bot adapters
- Change architecture
- Commit any changes

---

## Next Steps After Approval

1. Update todo list with approved solution
2. Implement solution
3. Test thoroughly
4. Document results in observation file
5. Report back to user with evidence of working system

---

**Awaiting user approval to proceed.**
