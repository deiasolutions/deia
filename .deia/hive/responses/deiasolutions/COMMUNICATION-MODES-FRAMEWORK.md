# BOT COMMUNICATION MODES FRAMEWORK

**Status:** Design Phase
**Date:** 2025-10-28
**Author:** Claude Code (BOT-001)
**Audience:** Q33N, Bot Runners, Commandeer UI

---

## OVERVIEW

The system supports **3 distinct communication modes** for bot coordination. Q33N, bots, and UI must all understand and handle each mode.

---

## MODE 1: CLI-ONLY

**Configuration:** `--mode cli-only`

### Bot Side
- **Location:** CLI terminal window (user's desktop)
- **Input:** File-based task queue (`.deia/hive/tasks/BOT-ID/`)
- **Output:** File-based responses (`.deia/hive/responses/`)
- **Logging:** Activity logs to `.deia/bot-logs/BOT-ID-activity.jsonl`
- **UI:** None - pure CLI, user sees process in terminal
- **Subprocess:** Claude/Codex CLI runs interactively in subprocess, receives stdin from bot runner

### Q33N Side (What You Need to Do)
1. **Monitor task queue** - Create files in `.deia/hive/tasks/BOT-ID/`
2. **Monitor responses** - Read files written to `.deia/hive/responses/`
3. **Monitor logs** - Watch `.deia/bot-logs/BOT-ID-activity.jsonl` for progress
4. **Handle offline operation** - Pile up tasks while compacting, bot processes them in order

### Task File Format
```
.deia/hive/tasks/BOT-ID/TASK-ID-priority-description.md

{
  "task_id": "TASK-002-001",
  "bot_id": "BOT-002",
  "command": "Your instruction to bot",
  "priority": "P0",  // P0 (critical) P1 (high) P2 (normal)
  "created_at": "2025-10-28T13:35:00Z",
  "timeout_seconds": 300
}
```

### Response File Format
```
.deia/hive/responses/TASK-ID-timestamp-response.md

{
  "task_id": "TASK-002-001",
  "bot_id": "BOT-002",
  "success": true,
  "response": "Task execution output",
  "files_modified": ["file1.py", "file2.py"],
  "errors": null,
  "completed_at": "2025-10-28T13:40:00Z",
  "duration_seconds": 300
}
```

### When to Use
- Development/testing
- Headless environments
- When GUI not available
- BOT-002 current mode

---

## MODE 2: CLI + COMMANDER (HYBRID)

**Configuration:** `--mode hybrid`

### Bot Side
- **Location:** CLI terminal window + Commandeer UI
- **Input:** Both file queue AND WebSocket from Commandeer
- **Output:** Both file responses AND chat stream to Commandeer
- **Logging:** Activity logs + streaming to chat UI
- **Subprocess:** Claude/Codex CLI runs interactively, gets input from BOTH sources
- **Priority:** WebSocket input > file queue (human + bot can coordinate)

### Q33N Side (What You Need to Do)
1. **Monitor task queue** - Create files in `.deia/hive/tasks/BOT-ID/` (async orchestration)
2. **Chat with bot** - Send prompts via Commandeer UI (real-time interaction)
3. **Monitor Commandeer UI** - See unified conversation log (file + chat responses)
4. **Pause/resume** - Can pause bot via `.deia/hive/controls/BOT-ID-PAUSE` file
5. **Handle hybrid mode** - Bot prioritizes human input but doesn't ignore file queue

### Unified Conversation Timeline in Commandeer
```
[Timeline]

BOT-002 → File response (from task queue)
  📄 TASK-002-001-response.md
  "Added error handling to 3 files"

Q33N (You) → Chat message (via Commandeer)
  "Good. Now add logging."

BOT-002 → Chat response (live streaming)
  "Adding structured logging..."
  [Files being modified in real-time]

BOT-002 → File response (async task from queue)
  📄 TASK-002-002-response.md
  "Configuration module refactored"

[Human can interject, watch, or let it run]
```

### Task File Format (Same as CLI-only)
```
.deia/hive/tasks/BOT-ID/TASK-ID-priority-description.md
```

### Chat Message Format (Via WebSocket)
```json
{
  "type": "chat",
  "bot_id": "BOT-002",
  "sender": "Q33N",
  "message": "Your prompt here",
  "timestamp": "2025-10-28T13:35:00Z"
}
```

### Chat Response Format (Via WebSocket)
```json
{
  "type": "response",
  "bot_id": "BOT-002",
  "response_type": "streaming",
  "chunks": ["chunk1", "chunk2"],
  "files_modified": ["file1.py"],
  "completed_at": "2025-10-28T13:40:00Z"
}
```

### When to Use
- Interactive development with bots
- Real-time problem solving
- Human oversight needed
- Mixing autonomous (file queue) + interactive (chat) tasks

---

## MODE 3: COMMANDER-ONLY

**Configuration:** `--mode commander-only`

### Bot Side
- **Location:** Only in Commandeer UI, no CLI window
- **Input:** Only WebSocket from Commandeer
- **Output:** Only chat stream to Commandeer
- **Logging:** Activity logs streamed to UI
- **Subprocess:** Claude/Codex CLI runs in background, completely hidden
- **UI:** Full Commandeer interface, pure conversational

### Q33N Side (What You Need to Do)
1. **Chat exclusively** - All commands via Commandeer chat
2. **No file queue** - Forget about `.deia/hive/tasks/`
3. **No offline operation** - If Commandeer down, bot can't receive tasks
4. **Real-time only** - Every interaction synchronous through chat

### When to Use
- GUI-first environment
- Non-technical users operating bots
- Cloud deployments where CLI not available
- Real-time collaborative sessions

---

## MODE DETECTION & STARTUP

### How Bots Know Their Mode

When bot starts:
```
python run_single_bot.py BOT-002 --mode cli-only
python run_single_bot.py BOT-002 --mode hybrid
python run_single_bot.py BOT-002 --mode commander-only
```

### Bot Runner Behavior by Mode

```python
if mode == "cli-only":
    # Poll task queue only
    while running:
        task = find_task_in_queue()
        if task:
            execute(task)
            write_response_file()

elif mode == "hybrid":
    # Poll BOTH task queue and WebSocket
    while running:
        task_from_queue = find_task_in_queue()
        task_from_websocket = check_websocket_input()

        if task_from_websocket:  # Human priority
            execute(task_from_websocket)
            stream_response_to_chat()
        elif task_from_queue:    # Bot queue
            execute(task_from_queue)
            write_response_file()
            broadcast_to_chat()

elif mode == "commander-only":
    # Only WebSocket, no file queue
    while running:
        task = wait_for_websocket_input()
        if task:
            execute(task)
            stream_response_to_chat()
```

---

## Q33N (YOU) - HOW TO COORDINATE

### For CLI-Only Bots (BOT-002)
```bash
# Create task file in queue
echo '{...}' > .deia/hive/tasks/BOT-002/TASK-002-001.md

# Poll for response
watch -n 1 'ls .deia/hive/responses/ | grep TASK-002'

# Read response when available
cat .deia/hive/responses/TASK-002-001-response.md
```

### For Hybrid Bots
```bash
# Can mix both methods:

# Method 1: Queue async task
echo '{...}' > .deia/hive/tasks/BOT-003/TASK-003-001.md

# Method 2: Chat in Commandeer (real-time)
# Type in chat window while bot also processes queue tasks

# Watch unified timeline in Commandeer UI
```

### For Commander-Only Bots
```bash
# No file queue - chat only
# Commandeer UI is your only interface

# Type prompts in chat
# Get responses in real-time
```

---

## MODE TRANSITIONS

### Switching Modes
Can a bot switch modes mid-run?
- **No** - Mode set at startup, don't change
- **Why** - Avoids race conditions and coordination confusion
- **Solution** - Stop bot, restart with new `--mode` flag

### Default Mode
- If no `--mode` specified: `cli-only`
- Safest, no GUI dependency

---

## FILE-BASED TASK COORDINATION DETAILS

### Task Polling Loop (CLI-only & Hybrid)
```
Every 5 seconds:
1. Check .deia/hive/tasks/BOT-ID/ for new .md files
2. Sort by priority (P0 > P1 > P2) then timestamp
3. Pick first unprocessed task
4. Execute via adapter (Claude CLI, etc.)
5. Write response to .deia/hive/responses/
6. Mark as processed
7. Log to .deia/bot-logs/BOT-ID-activity.jsonl
```

### Response Persistence
- Each response file is permanent (for audit trail)
- Q33N can read responses at any time
- Response files are immutable (write once)
- Name format: `TASK-ID-timestamp.md` (unique)

### Error Handling
If task fails:
```json
{
  "task_id": "TASK-002-001",
  "success": false,
  "error": "Claude Code CLI subprocess crashed",
  "error_details": "...",
  "completed_at": "2025-10-28T13:40:00Z"
}
```

---

## WEBSOCKET COORDINATION DETAILS

### Commandeer Chat Connection
```
GET /ws/bot/{bot_id}
```

### Message Types (Commandeer → Bot)
```json
{
  "type": "prompt",
  "content": "User's instruction",
  "timeout": 300,
  "user_id": "Q33N"
}
```

### Message Types (Bot → Commandeer)
```json
{
  "type": "response_start",
  "task_id": "...",
  "timestamp": "..."
}

{
  "type": "response_chunk",
  "content": "Streaming output...",
  "files_modified": []
}

{
  "type": "response_complete",
  "success": true,
  "duration": 45
}
```

---

## ACTIVE/PASSIVE MODES FOR Q33N

### CLI-Only Bots
- **Q33N Activity:** Active (you must create tasks)
- **Bot Activity:** Passive waiting (responds to queue)
- **Coordination:** Asynchronous via files

### Hybrid Bots
- **Q33N Activity:** Can be both active (queue) and interactive (chat)
- **Bot Activity:** Always listening (queue + WebSocket)
- **Coordination:** Mixed async + real-time

### Commander-Only Bots
- **Q33N Activity:** Always interactive (chat)
- **Bot Activity:** Always listening (WebSocket only)
- **Coordination:** Purely real-time

---

## CURRENT DEPLOYMENT STATUS

| Bot | Mode | Status | Notes |
|-----|------|--------|-------|
| BOT-001 (Claude Code) | CLI-only | Idle | Waiting for direction |
| BOT-002 (Claude Code CLI) | CLI-only | Ready | Awaiting tasks in queue |
| Llama (8000) | N/A | Running | Standalone, outside system |
| Dashboard (6666) | Hybrid | Running | Can coordinate via API + chat |

---

## NEXT STEPS

1. **Implement mode parameter** in BotRunner
2. **Add WebSocket mode** for Hybrid/Commander-only
3. **Update bot startup** to pass `--mode` flag
4. **Test BOT-002 in CLI-only** (file queue tasks)
5. **Test Hybrid mode** with chat + file coordination
6. **Update Commandeer UI** to show unified timeline

---

## QUESTIONS FOR Q33N

1. **Default mode for all bots?** (recommend: `cli-only` for safety)
2. **WebSocket protocol already exists?** (check Commandeer implementation)
3. **Can bots receive mode switching commands?** (or hard restart required?)
4. **Priority if both file task + chat prompt arrive simultaneously?** (recommend: chat > queue)

---

**Framework complete. Ready to implement modes in bot runner.**

