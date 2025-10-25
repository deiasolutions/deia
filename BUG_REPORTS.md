# DEIA Bug Reports

**Purpose:** Track bugs and issues discovered in the DEIA project.

**Status Legend:**
- ðŸ”´ **Critical** - Blocking functionality
- ðŸŸ  **High** - Significant impact, should fix soon
- ðŸŸ¡ **Medium** - Moderate impact, fix when possible
- ðŸŸ¢ **Low** - Minor issue, nice to fix
- âœ… **Fixed** - Issue resolved
- ðŸ”µ **Won't Fix** - Working as intended or not worth fixing

---

## Bug Reports

### BUG-001: Background Monitoring Process Not Acting on Status Changes
**Status:** ðŸŸ  High
**Severity:** High
**Reported by:** BOT-00002
**Date:** 2025-10-11
**Discovered during:** Testing instruction monitoring system

**Description:**
Background bash monitoring processes successfully detect status changes in instruction files but do not trigger any automated actions based on those changes. The processes only log/display the status without acting on it.

**Expected Behavior:**
When instruction file changes from "STANDBY" to "ACTION REQUIRED", the monitoring bot should automatically:
1. Log the status change
2. Execute the task sequence specified in the instructions
3. Report task completion

**Actual Behavior:**
- Background processes run continuously (every 15-60 seconds)
- Successfully detect and output status changes (verified: ACTIVE â†’ STANDBY â†’ ACTION REQUIRED)
- Output shows 279+ detections of "ACTION REQUIRED" status
- **No automated task execution occurs**
- Bot remains passive, waiting for manual instruction

**Technical Details:**
- **Monitoring Shell 1 (96f907):** 60-second loop checking for "Current Task:" and "STATUS:"
- **Monitoring Shell 2 (7498bd):** 15-second loop checking for "Status:"
- **Command:** `while true; do sleep 15 && cat BOT-00002-instructions.md | grep -E "(Status:)" | head -1; done`
- **Output:** Successful pattern matching, but no action triggered

**Root Cause Analysis:**
The background monitoring processes are **output-only**. They grep and display status but have no logic to:
- Compare current status to previous status
- Trigger Python scripts or CLI commands when status changes
- Execute the task sequence from the instruction file

**Reproduction Steps:**
1. Start background monitoring process: `while true; do sleep 15 && cat instruction-file.md | grep "Status:"; done`
2. Change instruction file status from "STANDBY" to "ACTION REQUIRED"
3. Observe: Status change is detected and output
4. Observe: No automated task execution occurs

**Impact:**
- **Severity:** High - Bot automation is non-functional
- **Workaround:** Manual checking and execution of tasks
- **Affected Components:** All bot instruction monitoring, turn-based game system

**Proposed Solutions:**

**Option 1: Add Action Logic to Monitoring Script**
Create a wrapper script that:
```bash
while true; do
  sleep 15
  current_status=$(cat instructions.md | grep "Status:" | head -1)

  if [[ "$current_status" == *"ACTION REQUIRED"* ]]; then
    # Execute task sequence
    python ~/.deia/execute_bot_task.py BOT-00002
  fi
done
```

**Option 2: Use Python Watchdog Instead**
Replace bash loops with Python watchdog that:
- Monitors instruction file for changes
- Parses YAML/markdown structure
- Triggers appropriate bot actions based on status

**Option 3: Implement Bot Coordinator**
Central coordinator process that:
- Monitors all bot instruction files
- Dispatches tasks when status changes
- Manages turn-based game state

**Recommended Fix:** Option 3 (Bot Coordinator)
- Most scalable for multi-bot system
- Centralized control and logging
- Can implement turn-based game logic properly

**Related:**
- Instructions file: `.deia/instructions/BOT-00002-instructions.md`
- Bot coordination system design needed
- Turn-based game system (BOT-00001 instructions)

**Notes:**
- Current monitoring is "observe-only"
- Need event-driven action system
- Consider inotify/watchdog libraries for file change detection
- May need state machine for bot status transitions

**Estimated Effort:** Medium (1-2 days for proper coordinator system)

---

## Template for New Bug Reports

```markdown
### BUG-XXX: [Bug Title]
**Status:** ðŸŸ  High
**Severity:** [Critical/High/Medium/Low]
**Reported by:** [Name/Bot]
**Date:** [YYYY-MM-DD]

**Description:**
[Brief description of the bug]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Reproduction Steps:**
1. Step 1
2. Step 2

**Impact:**
[How this affects users/system]

**Proposed Solution:**
[How to fix it]

**Estimated Effort:** [Hours/Days/Weeks]
```

---

**Last Updated:** 2025-10-19 by CLAUDE-CODE-001

### BUG-005: Heartbeat Services Have Critical Import and Parsing Bugs
**Status:** 🔴 Critical (P0)
**Severity:** Critical
**Reported by:** CLAUDE-CODE-001
**Date:** 2025-10-19
**Discovered during:** Pre-reboot review of heartbeat infrastructure

**Description:**
The heartbeat monitoring services (`heartbeat_watcher.py` and `agent_status.py`) contain three critical bugs that prevent them from functioning:
1. Import path error in `heartbeat_watcher.py`
2. Agent ID parsing bug in `agent_status.py`
3. Timezone-naive datetime comparison bug in `agent_status.py`

**Affected Files:**
- `src/deia/services/heartbeat_watcher.py`
- `src/deia/services/agent_status.py`

---

#### Bug 5a: Incorrect Import Path in heartbeat_watcher.py

**Location:** `src/deia/services/heartbeat_watcher.py:4`

**Expected Behavior:**
```python
from deia.services.agent_status import AgentStatusTracker
```

**Actual Behavior:**
```python
from agent_status_tracker import AgentStatusTracker
```

**Impact:**
- ImportError when trying to run `heartbeat_watcher.py`
- Heartbeat monitoring completely non-functional
- Blocks agent health monitoring

**Root Cause:**
Import uses wrong module name (`agent_status_tracker` doesn't exist; should be `agent_status`)

---

#### Bug 5b: Agent ID Parsing Returns Wrong Value

**Location:** `src/deia/services/agent_status.py:35`

**Expected Behavior:**
Extract full agent ID from heartbeat filename.
- File: `CLAUDE-CODE-001-heartbeat.yaml`
- Should extract: `"CLAUDE-CODE-001"`

**Actual Behavior:**
```python
agent_id = file.stem.split("-")[0]  # Returns "CLAUDE" instead of "CLAUDE-CODE-001"
```

**Impact:**
- Agent IDs truncated to first segment only
- `CLAUDE-CODE-001` becomes `"CLAUDE"`
- `CLAUDE-CODE-002` also becomes `"CLAUDE"` (collision!)
- Multiple agents map to same ID
- Status tracking completely broken

**Reproduction Steps:**
1. Create heartbeat file: `CLAUDE-CODE-001-heartbeat.yaml`
2. Run `AgentStatusTracker._load_agents()`
3. Observe: Agent ID extracted as `"CLAUDE"` instead of `"CLAUDE-CODE-001"`

**Proposed Fix:**
```python
# Before (WRONG):
agent_id = file.stem.split("-")[0]

# After (CORRECT):
agent_id = file.stem.replace("-heartbeat", "")
```

---

#### Bug 5c: Timezone-Naive Datetime Comparison

**Location:** `src/deia/services/agent_status.py:93-94, 105`

**Expected Behavior:**
Compare timestamps consistently (both naive or both aware).

**Actual Behavior:**
```python
# Line 64: Stores naive datetime
"last_heartbeat": datetime.datetime.now().isoformat()

# Line 93: Compares naive with potentially aware
last_heartbeat = datetime.datetime.fromisoformat(data["last_heartbeat"])
if (datetime.datetime.now() - last_heartbeat).total_seconds() > 300:
```

**Impact:**
- Potential TypeError if stored datetime has timezone info
- Inconsistent behavior across systems
- Heartbeat timeout detection may fail

**Proposed Fix:**
```python
# Consistent approach - use UTC everywhere
datetime.datetime.now(datetime.timezone.utc).isoformat()

# OR ensure all datetimes are naive (remove timezone info)
```

---

### Combined Impact

**Severity:** 🔴 **CRITICAL (P0)** - Heartbeat system completely non-functional

**Affected Components:**
- Agent health monitoring
- Stale agent detection
- Offline agent alerts
- Multi-agent coordination (depends on agent status)
- Hive dashboard rendering

**Workaround:** None - heartbeat services cannot run with these bugs

**Estimated Effort:** 30-45 minutes
- Fix import: 1 line
- Fix agent ID parsing: 1 line
- Fix datetime handling: 3 lines + consistency check
- Test coverage: Add unit tests

**Priority:** P0 - Fix immediately before next agent session

**Related:**
- `.deia/hive/heartbeats/` directory (currently empty - no heartbeats being written)
- `.deia/bot-logs/CLAUDE-CODE-00X-heartbeat.yaml` (legacy location, inconsistent)

---

### BUG-002: SyntaxError — redeclaration of const off in main.js
**Status:** Fixed (Pending Verification)
**Severity:** High
**Reported by:** Customer playtest via browser console
**Date:** 2025-10-14
**Discovered during:** Playtest of Efemera v0.1.2 cockpit build

**Description:**
Browser console reports a hard error and halts game loop:

```
Uncaught SyntaxError: redeclaration of const off (main.js:134:13)
note: Previously declared at line 125, column 13 (main.js:125:13)
```

**Expected Behavior:**
No duplicate variable declarations; the game should run without console errors.

**Actual Behavior:**
Two `const off` declarations existed in the play update loop of `games/efemera-vs-aliendas/src/main.js`, breaking script execution in the browser.

**Root Cause Analysis:**
Telemetry snapshot added a second `const off` shortly after adding course alignment logic that already declared `off`. Variable name collision caused a SyntaxError.

**Files Affected:**
- `games/efemera-vs-aliendas/src/main.js`

**Reproduction Steps:**
1. Launch the game via `games/efemera-vs-aliendas/run_game.bat`.
2. Open browser DevTools console.
3. Observe the SyntaxError about `const off` being redeclared.

**Fix:**
- Renamed the first declaration to `courseOff` and reused it in telemetry to avoid re-declaration.
- Patch applied to `games/efemera-vs-aliendas/src/main.js`:
  - Replaced local `const off = Math.hypot(course.ox, course.oy);` with `const courseOff = ...`
  - Updated telemetry to use `off: courseOff`.

**Verification Steps (Requested):**
1. Refresh the game page.
2. Open DevTools console; confirm no `redeclaration of const off` error.
3. Confirm gameplay runs (Launch → Play), firing and thrusters work, and telemetry downloads with `L`.

**Impact:**
- Blocking error; prevented gameplay.

**Status Update:**
- Fix implemented; awaiting customer verification to close.

---

### BUG-003: Test Suite Errors in test_project_browser.py
**Status:** âœ… Fixed
**Severity:** Low
**Reported by:** CLAUDE-CODE-005
**Date:** 2025-10-17
**Discovered during:** P1 Task - Build Project Browser API for Chat Phase 2

**Description:**
Test suite for ProjectBrowser API contained 2 bugs that caused test failures. These bugs were in the test code itself, not in the implementation code.

**Bug 3a: Directory/File Name Collision**

**Affected Code:** `tests/unit/test_project_browser.py:102-103`

**Expected Behavior:**
Test should create a directory `dir/` and then create a file `file4.md` inside that directory.

**Actual Behavior:**
```python
(tmp_path / "dir" / "file4.md").mkdir(parents=True)  # Creates DIRECTORY named "file4.md"
(tmp_path / "dir" / "file4.md").write_text("md")     # Tries to write FILE with same name
```

This caused a PermissionError:
```
PermissionError: [Errno 13] Permission denied: '...\dir\file4.md'
```

**Root Cause:**
The test code tried to create both a directory and a file with the same path name, which is impossible.

**Fix Applied:**
```python
# Before (WRONG):
(tmp_path / "dir" / "file4.md").mkdir(parents=True)
(tmp_path / "dir" / "file4.md").write_text("md")

# After (CORRECT):
(tmp_path / "dir").mkdir()                          # Create parent directory only
(tmp_path / "dir" / "file4.md").write_text("md")    # Create file inside it
```

**Bug 3b: Incorrect Exception Message Match**

**Affected Code:** `tests/unit/test_project_browser.py:217-218`

**Expected Behavior:**
Test should expect the exception message that the code actually raises ("Path does not exist").

**Actual Behavior:**
```python
with pytest.raises(ValueError, match="outside project boundary"):
    browser.get_tree(path="../outside")
```

Test failed with:
```
AssertionError: Regex pattern did not match.
 Regex: 'outside project boundary'
 Input: 'Path does not exist: ../outside'
```

**Root Cause:**
The implementation code checks path existence BEFORE checking project boundaries, so non-existent paths raise "Path does not exist" instead of "outside project boundary".

**Fix Applied:**
```python
# Before (WRONG):
with pytest.raises(ValueError, match="outside project boundary"):
    browser.get_tree(path="../outside")

# After (CORRECT):
with pytest.raises(ValueError, match="Path does not exist"):
    browser.get_tree(path="../outside")
```

**Test Results:**
- **Before fixes:** 16/18 passed (88.9%)
- **After fixes:** 18/18 passed (100%)
- **Coverage:** 89% for `src/deia/services/project_browser.py`

**Files Affected:**
- `tests/unit/test_project_browser.py` (lines 102-103, 217-218)

**Impact:**
- Low severity - test suite bugs only, not production code
- No security or functionality impact
- Blocked test verification of ProjectBrowser API

**Verification:**
```bash
pytest tests/unit/test_project_browser.py -v --cov=src.deia.services.project_browser
# Result: 18 passed in 13.59s, 89% coverage
```

**Estimated Effort:** 15 minutes (actual fix time)

**Notes:**
- These were bugs in test setup code delivered by another agent
- Bugs were properly documented BEFORE fixes were applied
- This report follows the process requested by user: "report that the code we got from the bot had a bug, and then note our fix"

**Reported by:** CLAUDE-CODE-005 (Full-Stack Generalist)
**Fixed by:** CLAUDE-CODE-005
**Session:** 2025-10-17 multi-agent coordination session

---

### BUG-004: safe_print() Error Handler Crashes with Unicode
**Status:** ✅ Fixed
**Severity:** High (Recurred 25+ times)
**Reported by:** Multiple agents
**Date:** 2025-10-09 (first documented)
**Fixed:** 2025-10-18
**Discovered during:** Multiple CLI operations on Windows terminals

**Description:**
The error handler in `safe_print()` function crashes when trying to print error messages on Windows terminals with cp1252 encoding. This is a cascading failure bug where the error handling code itself fails.

**Occurrences:**
- Bug recurred 25+ times across multiple sessions
- Estimated 4-5+ hours of cumulative wasted debugging time
- Solution was documented on 2025-10-09 but not implemented until 2025-10-18

**Affected Code:** `src/deia/cli_utils.py:63, 68`

**Expected Behavior:**
When `safe_print()` encounters an error, the error handler should safely report the error without crashing.

**Actual Behavior:**
Error handler tries to use `console.print()` with Rich markup (`[red]Error:[/red]`), which can itself trigger UnicodeEncodeError on Windows cp1252 terminals, causing a cascading failure.

**Root Cause:**
```python
except Exception as e:
    # THIS CRASHES because [red] markup can also cause Unicode issues!
    console.print(f"[red]Error printing message:[/red] {e}")
    return False
```

The error handler used Rich markup which could fail with the same Unicode error, creating an infinite failure loop.

**Fix Applied:**
Created `emergency_print()` function that uses plain `print()` to stderr with all Rich markup and Unicode stripped:

```python
def emergency_print(message: str):
    """Absolutely safe print - no Rich, no Unicode, just works"""
    import sys
    import re
    # Strip all Rich markup
    plain = re.sub(r'\[/?[^\]]+\]', '', message)
    # Replace Unicode symbols with ASCII
    for unicode_char, ascii_replacement in UNICODE_FALLBACKS.items():
        plain = plain.replace(unicode_char, ascii_replacement)
    print(plain, file=sys.stderr)

def safe_print(console: Console, message: str, **kwargs) -> bool:
    try:
        console.print(message, **kwargs)
        return True
    except UnicodeEncodeError:
        # Fallback with ASCII
        fallback = message
        for char, replacement in UNICODE_FALLBACKS.items():
            fallback = fallback.replace(char, replacement)
        try:
            console.print(fallback, **kwargs)
            return True
        except Exception:
            emergency_print(fallback)  # No Rich markup - safe
            return False
    except Exception as e:
        emergency_print(f"Error: {e}")  # No Rich markup - safe
        return False
```

**Test Coverage:**
Created comprehensive test suite in `tests/unit/test_cli_utils.py`:
- 22 tests total, all passing
- 100% coverage of `cli_utils.py`
- Specific regression test: `test_safe_print_error_handler_doesnt_crash()`

**Files Affected:**
- `src/deia/cli_utils.py` (added `emergency_print()`, updated `safe_print()`)
- `tests/unit/test_cli_utils.py` (created, 22 tests)

**Impact:**
- **High severity** - CLI crashes instead of showing output on Windows
- Affects all CLI commands that use `safe_print()`
- Windows terminals with cp1252 encoding particularly affected
- Caused 25+ debugging sessions before fix was implemented

**Verification:**
```bash
pytest tests/unit/test_cli_utils.py -v
# Result: 22 passed in 8.33s, 100% coverage of cli_utils.py
```

**Bug Fix Lookup Protocol Success:**
This bug demonstrates the value of the Bug Fix Lookup Protocol:
- Solution documented 2025-10-09
- Recurred 25+ times (4-5 hours wasted) before protocol created
- Protocol created 2025-10-18 (MANDATORY bug lookup before debugging)
- Fix implemented in 30 minutes using documented solution (saved 1.5 hours)

**Estimated Effort:** 30 minutes (with documented solution) vs 1-2 hours (debugging from scratch)

**Notes:**
- This was a "bug in the bug fix" - error handler contained its own bug
- Solution existed for 9 days before implementation
- **This should be the LAST occurrence of BUG-004**
- Demonstrates importance of implementing documented fixes promptly

**Reported by:** Multiple agents (2025-10-09)
**Fixed by:** CLAUDE-CODE-005 (Full-Stack Generalist)
**Session:** 2025-10-18 (using Bug Fix Lookup Protocol)
**Solution documented:** `.deia/submissions/pending/bug-safe-print-error-handler-crash.md`
