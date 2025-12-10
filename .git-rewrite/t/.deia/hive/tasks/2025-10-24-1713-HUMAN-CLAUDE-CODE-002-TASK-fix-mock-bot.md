# TASK: Fix Mock Bot Implementation

**To:** CLAUDE-CODE-002
**From:** HUMAN-DAVE
**Priority:** P0
**Created:** 2025-10-24T17:13:00Z

## Context

CLAUDE-CODE-001 attempted to implement mock bot for dashboard testing but failed:
- Created `src/deia/adapters/mock_bot_adapter.py` (ASCII only, no Unicode errors)
- Updated `src/deia/adapters/bot_runner.py` to support "mock" adapter type
- Updated `run_single_bot.py` to add --adapter-type flag and call runner.start()
- Bot process starts but produces NO output (same issue as CLI bots)

**Time Estimate Given:** 1-2 hours
**Actual Time Spent:** ~45 minutes before failure

## The Problem

When running:
```bash
python run_single_bot.py CLAUDE-CODE-TEST-001 --adapter-type mock --cooldown 5
```

Expected: Bot prints startup messages and begins monitoring task folder
Actual: Process runs but produces zero output (silent hang)

## CRITICAL DISCOVERY - AUTH CONFLICT RESOLVED

**Root Cause Found:** Lines 77 and 83 in `.claude/settings.local.json` had ANTHROPIC_API_KEY hardcoded in bash permission entries. This polluted the environment for all new Claude Code sessions.

**Fix Applied:** Removed those lines from settings.local.json.

**Remaining Work:** Update ClaudeCodeCLIAdapter to isolate environment per bot type:
- CLI bots: Remove ANTHROPIC_API_KEY from subprocess environment
- API bots: Add ANTHROPIC_API_KEY to subprocess environment
- This allows both types to run simultaneously without conflict

**CRITICAL PROCESS FAILURE:** CLAUDE-CODE-001 didn't monitor subprocess stdout/stderr to see the auth error message.

## Your Task

### Option A: Fix Auth Conflict in CLI Adapter (RECOMMENDED)

1. **Update ClaudeCodeCLIAdapter** to:
   - Read subprocess stdout/stderr
   - Detect auth conflict message
   - Automatically resolve: unset ANTHROPIC_API_KEY before spawning subprocess
   - Log all subprocess output for debugging
   - Respond to interactive prompts if needed

2. **Test with real CLI bot**:
   - Run with proper auth (no conflict)
   - Verify subprocess output is captured and logged
   - Verify bot actually works

### Option B: Standalone Mock (If A Blocked)

1. **Create simple standalone test script** that:
   - Watches `.deia/hive/tasks/` for task files
   - Reads task markdown
   - Writes mock response to `.deia/hive/responses/`
   - Prints clear status messages (ASCII only)
   - Does NOT use BotRunner class

2. **Test the script works** by:
   - Running it in foreground with visible output
   - Creating a test task file manually
   - Verifying it picks up task and writes response
   - Verifying response file appears in dashboard

### CRITICAL PROCESS REQUIREMENT

**Monitor subprocess output and interpret it!** That's the entire point of CLI interface:
- Read stdout/stderr from subprocess
- Log it for debugging
- Interpret messages (errors, prompts, status)
- Take appropriate action or ask user if unclear

## Success Criteria

- [  ] Standalone script runs with visible output
- [  ] Script picks up task files from `.deia/hive/tasks/`
- [  ] Script writes response files to `.deia/hive/responses/`
- [  ] Response files appear in dashboard at http://localhost:8000
- [  ] Documentation of findings in `.deia/observations/`

## Files to Reference

- `.deia/rules/NO-UNICODE-CONSOLE-ENFORCEMENT.md` - CRITICAL: ASCII only
- `.deia/rules/SCRUM-MASTER-ARCHITECTURE.md` - Bot coordination docs
- `src/deia/adapters/mock_bot_adapter.py` - Previous attempt (reference only)
- `.deia/hive/tasks/` - Task folder to watch
- `.deia/hive/responses/` - Response folder to write

## Constraints

- **NO Unicode symbols** in print statements (see enforcement doc)
- Use simple Python with minimal dependencies
- Print status messages so we can see it's working
- Test thoroughly before claiming success
- Do NOT modify BotRunner or existing adapters

## Deliverables

1. Working standalone test script: `test_mock_coordination.py`
2. Observation document: `.deia/observations/2025-10-24-002-mock-bot-fix.md`
3. Response in `.deia/hive/responses/` confirming completion

---

**Note:** CLAUDE-CODE-001 failed at design/execution. Focus on simple, testable solution first.
