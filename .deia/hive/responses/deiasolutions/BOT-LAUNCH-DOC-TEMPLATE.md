# BOT LAUNCH DOC TEMPLATE

**Purpose:** Standardized launch briefing for new bot instances
**Created from:** BOT-002-LAUNCH-MISSION.md analysis
**Date:** 2025-10-28

---

## TEMPLATE

```markdown
# BOT-XXX LAUNCH MISSION

**Bot ID:** BOT-XXX
**Type:** [AI Model Type - e.g., Claude Code CLI]
**Spawn Time:** [ISO timestamp]
**Communication:** [Mode - e.g., File-based task queue]
**Status:** READY TO LAUNCH

---

## MISSION OVERVIEW

[1-2 sentences about bot purpose and responsibilities]

**Your job:** [Core mission statement]

---

## CRITICAL SETUP INFORMATION

### 1. AUTO-LOGGING IS ENABLED

All activity is logged to:
```
.deia/bot-logs/BOT-XXX-activity.jsonl    ← Task logs with timestamp, input, output
.deia/bot-logs/BOT-XXX-errors.jsonl      ← Error logs with full stack trace
```

**What this means:**
- Every task is logged with execution details
- Every error is logged for debugging
- Monitoring systems can track activity in real-time
- Response timeline is persistent for audit

**You don't need to do anything** - auto-logging happens automatically.

### 2. PREVIOUS BOT LEARNINGS

[Reference document with key lessons from previous bots]

**Key learnings:**
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]

---

## OPERATIONAL ARCHITECTURE

### Communication Flow

[Diagram or description of how this bot receives tasks and sends responses]

```
Task Input → [Bot] → Response Output → Logging
```

### How to Monitor Your Tasks

1. **Task files appear in:** `.deia/hive/tasks/BOT-XXX/`
2. **Each task file format:** [Specify format: JSON, Markdown, etc.]
3. **Process the task** using [Bot's execution method]
4. **Write response file** to `.deia/hive/responses/` with format:
   [Include response format specification]

---

## YOUR RESPONSIBILITIES

### During Normal Operation

1. **Monitor task queue** - New tasks appear in `.deia/hive/tasks/BOT-XXX/`
2. **Process each task** - Execute via [bot's method], capture output
3. **Write responses** - Save completion status to response directory
4. **Log everything** - Auto-logging tracks activity
5. **Report errors** - If something fails, log it and continue

### If Something Goes Wrong

1. **Check error logs** - `.deia/bot-logs/BOT-XXX-errors.jsonl`
2. **Write error response** - Include full error message in response
3. **Mark as failed** - Set success indicator to false
4. **Continue operating** - Don't stop, wait for next task

### When Orchestrator Is Down

- **Task queue still works** - Tasks pile up in filesystem
- **Responses still persist** - Written to filesystem
- **When orchestrator recovers** - It reads all responses and catches up
- **You keep running** - No coordination needed for file-based comms

---

## SUCCESS CRITERIA

✅ **You succeed when:**
1. Bot subprocess starts successfully
2. You can read tasks from task queue directory
3. You can send tasks to the bot via [specified method]
4. You can capture responses from bot
5. You write response files to response directory
6. Auto-logging captures all activity
7. Monitoring system can access activity logs
8. Orchestrator can coordinate with bot even when offline

---

## NEXT STEPS

1. **Verify bot is alive** - Confirm subprocess running
2. **Read first task from queue** - Look for task files in directory
3. **Send task to bot** - Execute via [specified method]
4. **Capture response** - Read from response channel
5. **Write response file** - Persist results
6. **Repeat** - Wait for next task

---

## COMMUNICATION WITH ORCHESTRATOR

When tasks complete:
- **File response:** Orchestrator reads response files
- **Chat response:** If hybrid mode, stream to orchestrator UI
- **Human can:** Watch, pause, interject with new instructions
- **Orchestrator can:** Submit new tasks, pause, resume bot

---

## TROUBLESHOOTING

**If bot won't start:**
- Check: Is bot executable/command available?
- Check: Are there permission issues?
- Action: Log error, wait for next task

**If task queue is empty:**
- Normal state - just wait
- Orchestrator will submit tasks
- Check periodically for new files

**If response file write fails:**
- Log the error
- Mark in activity log
- Try again with next task

**If subprocess crashes:**
- Capture exit code and error messages
- Log comprehensively
- Orchestrator can decide to restart

---

## RESOURCES

- **Activity Logs:** `.deia/bot-logs/BOT-XXX-activity.jsonl`
- **Error Logs:** `.deia/bot-logs/BOT-XXX-errors.jsonl`
- **Task Queue:** `.deia/hive/tasks/BOT-XXX/`
- **Response Directory:** `.deia/hive/responses/`
- **Previous Bot Docs:** Check `/deiasolutions/` directory

---

## SIGN-OFF

**Prepared by:** [Orchestrator/Creator Name]
**For:** BOT-XXX [Bot Description]
**Date:** [ISO Date]
**Authorization:** [Authorized User]

---

**BOT-XXX: YOU ARE CLEARED FOR LAUNCH**

Report back with checkin status once you're alive.

Standing by for orchestrator confirmation to begin processing tasks.

---
```

---

## TEMPLATE GUIDELINES

### Essential Sections (Required)

1. **Header** - Bot identification, spawn time, communication mode, status
2. **Mission Overview** - What is the bot, what is its purpose
3. **Auto-Logging Setup** - Explain logging, log locations, what's tracked
4. **Previous Learnings** - Reference relevant documentation from other bots
5. **Operational Architecture** - How bot receives tasks and sends responses
6. **Responsibilities** - What bot must do during operation, error handling
7. **Success Criteria** - How to know bot is working correctly
8. **Next Steps** - Action items for bot startup
9. **Troubleshooting** - Common issues and solutions
10. **Sign-Off** - Authorization and final confirmation

### Guidelines for Completion

**For creators (defining new bot):**
- Fill in `BOT-XXX` with actual bot ID
- Specify bot type (Claude Code, Python script, service, etc.)
- Define exact task file format (JSON, Markdown, etc.)
- Specify response format clearly
- Include log file paths
- Reference previous bot documentation
- Explain communication method in detail
- List specific success criteria
- Include concrete troubleshooting steps

**For bots (reading at startup):**
- Read entire document
- Understand your mission and responsibilities
- Know your task queue location
- Know your response directory
- Know your log locations
- Understand error handling expectations
- Know how to signal problems
- Be ready to report back with checkin status

### Format Philosophy

- **Clear and concise** - Not verbose, but complete
- **Actionable** - Each section explains what to do
- **Verification-focused** - How to know things are working
- **Offline-friendly** - Works even when orchestrator unavailable
- **Self-documenting** - Future bots/users can understand system
- **Markdown format** - Human-readable, version control friendly

---

## VARIATIONS BY BOT TYPE

### For CLI-Only Bots (File Queue Mode)
- Emphasize task queue polling
- Detail task file format clearly
- Explain response file persistence
- Focus on async coordination

### For Hybrid Bots (File Queue + WebSocket)
- Explain both input channels
- Specify priority (WebSocket > queue)
- Detail unified timeline in UI
- Explain hybrid coordination

### For UI-Only Bots (WebSocket Only)
- Remove file queue sections
- Focus on WebSocket protocol
- Detail real-time communication
- Explain UI integration

---

## SIGN-OFF

**Template Status:** ✅ COMPLETE

This template standardizes bot launch documentation and can be adapted for:
- Different bot types (CLI, Python, services)
- Different communication modes (file, WebSocket, hybrid)
- Different orchestrators (Q33N, Commandeer, future systems)

Use this template for all future bot launches to ensure consistent startup protocols and clear communication patterns.

