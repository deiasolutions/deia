# Auto-Logging Definitions

**Source:** Dave, 2025-10-10 session
**Purpose:** Clear terminology for logging behavior types

---

## Full Auto

**Definition:** Claude Code knows to start logging from initial startup (without any user prompt or file reading trigger)

**Behavior:**
- Logging begins immediately when Claude Code session starts
- No user action required
- No file reading trigger needed

**Status:** Not implemented (as of 2025-10-10)

---

## Semi-Auto

**Definition:** Claude Code knows to start logging once it reads `project_resume.md`

**Behavior:**
- Logging begins after reading startup files
- Triggered by reading `project_resume.md` (which happens at session start per instructions)
- Claude proactively logs throughout session at breakpoints
- No explicit "/log" command needed from user

**Lesser version of semi-auto:** User has to explicitly tell Claude Code to start logging (e.g., "start logging")

**Status:** This is what DEIA currently implements via `.claude/INSTRUCTIONS.md`

---

## Current Implementation (Semi-Auto)

**How it works:**

1. `project_resume.md` tells Claude to read startup files
2. `.claude/STARTUP_CHECKLIST.md` includes reading `.claude/INSTRUCTIONS.md`
3. `.claude/INSTRUCTIONS.md` tells Claude:
   - Check if `auto_log: true` in `.deia/config.json`
   - If enabled, proactively log at breakpoints:
     - After major task completion
     - When user ends session
     - On crash recovery
     - When user asks "where were we?"

4. Claude captures conversation from context and calls:
   ```python
   from deia.logger import ConversationLogger
   logger = ConversationLogger()
   logger.create_session_log(...)
   ```

**Key distinction:** This is NOT real-time streaming to a file. This is Claude periodically capturing the conversation from its context window and writing it to a log file.

---

## What We Don't Have

**Real-time streaming:** Conversation logged line-by-line as it happens (this would require OS-level hooks or Claude Code API integration)

**ROADMAP.md status:** Lines 41-45 say "Actual conversation capture mechanism" is not complete, meaning the semi-auto behavior may not be consistently executed.

---

## Improvement Needed

Based on this session, the issue is:

✅ Semi-auto logging mechanism EXISTS
❌ Claude doesn't consistently execute it

**Root cause:** Instructions say to do it, but Claude may not follow instructions reliably without explicit prompting.

**Possible solutions:**
1. Strengthen instructions in `.claude/INSTRUCTIONS.md`
2. Add explicit reminder in `project_resume.md`
3. Create a startup hook that confirms "Logging active"
4. Build actual real-time capture (move to full-auto)

---

**Last Updated:** 2025-10-10
