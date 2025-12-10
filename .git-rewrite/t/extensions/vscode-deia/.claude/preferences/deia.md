# DEIA Auto-Logging System

**DEIA enables conversation logging and knowledge capture.**

## Startup Behavior

**IMPORTANT: Only activate DEIA if `.deia/` directory exists in the project.**

When you start a session, first check if DEIA is present:

1. **Check if `.deia/` directory exists:**
   ```python
   from pathlib import Path
   if not Path('.deia').exists():
       # Not a DEIA project, skip all DEIA behavior
       pass
   ```

2. **If DEIA exists, check installation:**
   ```python
   import sys
   sys.path.insert(0, 'src')
   from deia.logger import ConversationLogger
   ```

3. **Read project resume:**
   - Check if `project_resume.md` exists
   - If yes, read it to understand context from previous sessions
   - If no, this is a fresh project

4. **Check auto-log setting:**
   - Read `.deia/config.json`
   - If `auto_log: true`, enable real-time logging

## Real-Time Logging (when auto_log = true)

**Log after each significant step:**
- File creation/modification
- Key decision made
- Problem solved
- Error fixed
- Task completed

**What to log:**
```python
logger = ConversationLogger()
logger.log_step(
    action="what was done",
    files_modified=["list", "of", "files"],
    decision="key decision if any",
    next_step="what comes next"
)
```

## End of Session

**Always do this before conversation ends:**
1. Create final session log with full context
2. Update `project_resume.md` with current state
3. Note any pending tasks

## Manual Fallback

If auto-logging isn't working:
- User can say "read project_resume.md" to load context
- User can say "log this chat" to manually trigger logging
- Both should work even if auto-logging is broken

## Commands Available

- `/log` - Manually log current session
- `/auto-log-check` - Check if auto-logging is enabled

## Config Location

`.deia/config.json` contains:
```json
{
  "auto_log": true,
  "project": "project-name",
  "user": "username"
}
```

## Important

**Real-time logging means DURING the session, not just at the end.**

When `auto_log: true`:
- Log after each meaningful action
- Don't wait until the end
- Keep project_resume.md current throughout

## For User-Level Memory

If you're setting this as a user-level memory (applies to ALL projects):
- The `.deia/` existence check is CRITICAL
- Only activate in projects that have `.deia/` directory
- Skip silently in non-DEIA projects

## For Project-Level Memory

If you're setting this as a project-level memory (applies to THIS project only):
- The `.deia/` check is still good practice
- But you can assume DEIA is present in this project

## Clarifying Questions Policy

**CRITICAL SAFETY RULE:**

When you ask multiple yes/no questions and receive a single yes/no answer:
- **ALWAYS ask a clarifying question** before proceeding
- Do NOT assume which question was answered
- Do NOT guess user intent
- Ask: "Which one - [option A], [option B], or both?"

**Example of INCORRECT behavior:**
```
Assistant: "Would you like me to check the memory setup? Or start logging?"
User: "yes"
Assistant: [starts logging without asking which]  ❌ WRONG
```

**Example of CORRECT behavior:**
```
Assistant: "Would you like me to check the memory setup? Or start logging?"
User: "yes"
Assistant: "Which one - check memory setup, start logging, or both?"  ✅ CORRECT
```

**Why this matters:**
- Ambiguous responses can lead to wrong actions
- "Sometimes the safety of the entire universe is on the line"
- Better to over-clarify than to proceed incorrectly

**Apply to all ambiguous responses:**
- Multiple questions answered with single response
- Unclear pronouns ("do that", "the first one" when multiple options exist)
- Vague confirmations when multiple paths are possible
