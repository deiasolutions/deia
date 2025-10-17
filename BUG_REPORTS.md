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

**Last Updated:** 2025-10-11 by BOT-00002

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
