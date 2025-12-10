# SCRUM MASTER ARCHITECTURE - DEIA Bot Coordination

**Date:** 2025-10-24
**Status:** ACTIVE
**Scope:** How DEIA multi-agent bot coordination works

---

## Overview

The DEIA bot coordination system uses a **Scrum Master / Worker Bot pattern** where:
- **Scrum Master** (typically CLAUDE-CODE-001) is a Claude Code CLI session that launches and supervises other bots
- **CLI Bots** are individual Claude Code processes spawned by the Scrum Master
- Communication happens via **file system** and **direct text interface**

---

## Scrum Master Role

**Identity:** Usually CLAUDE-CODE-001 (Strategic Planner & Coordinator)

**Responsibilities:**
1. **Launch bot processes** - Spawn new Claude Code CLI instances
2. **Monitor bot status** - Watch file system for heartbeats and activity logs
3. **Assign tasks** - Write task files to `.deia/hive/tasks/`
4. **Monitor responses** - Watch `.deia/hive/responses/` for bot deliverables
5. **Kick stuck bots** - Send direct text messages to wake up bots that stop producing output
6. **Manage lifecycle** - Start, stop, restart bots as needed

**Key Understanding:**
> "the SCRUM MASTER LAUNCHES BOTS. a CLI BOT is a bot that runs Claude Code. The Scrum Master bot communicates with Cli Bot(s) through text file and direct bot to bot text interface"

**When Bots Get Stuck:**
> "sometimes the bot does output to the repo as required, but needs a 'Claude Code CLI' type of interaction to kick it in the ass and get running again checking the repo and responding appropriately"

The Scrum Master can send direct text messages to bot processes to wake them up when they hang.

---

## CLI Bot Architecture

**What is a CLI Bot?**
- A Claude Code CLI process running in a subprocess
- NOT the Anthropic API (no network calls)
- Full filesystem, git, and system access
- Communicates via file system watching

**How CLI Bots Work:**

1. **Launch:** Scrum Master spawns `claude` CLI process with bot instructions
2. **Task Detection:** Bot watches `.deia/hive/tasks/` for new task files
3. **Work Execution:** Bot reads task, does work, writes response
4. **Response Delivery:** Bot writes to `.deia/hive/responses/`
5. **Status Updates:** Bot maintains heartbeat in `.deia/hive/heartbeats/`

**Bot Runner Script:**
- `run_single_bot.py` - Launch individual bot
- `run_bots.py` - Launch multiple bots (used by Scrum Master)

---

## Communication Channels

### File System (Primary)

**Task Assignment:**
```
.deia/hive/tasks/YYYY-MM-DD-HHMM-FROM-TO-TYPE-subject.md
```

**Response Delivery:**
```
.deia/hive/responses/YYYY-MM-DD-HHMM-FROM-TO-RESPONSE-subject.md
```

**Status Monitoring:**
```
.deia/hive/heartbeats/AGENT-ID-heartbeat.yaml
.deia/bot-logs/AGENT-ID-activity.jsonl
```

**Bot-to-Bot Messages:**
```
.deia/tunnel/claude-to-claude/YYYY-MM-DD-HHMM-FROM-TO-TYPE-subject.md
```

### Direct Text Interface (Secondary)

The Scrum Master can send direct text messages to bot CLI processes to:
- Wake up stuck bots
- Request status updates
- Issue commands
- Trigger re-checks of task folders

This is like interacting with Claude Code CLI interactively, but automated.

---

## Bot Lifecycle Management

**Starting Bots:**
```python
# Scrum Master launches bot subprocess
runner = BotRunner(
    bot_id="CLAUDE-CODE-TEST-001",
    work_dir=Path.cwd(),
    task_dir=Path(".deia/hive/tasks"),
    response_dir=Path(".deia/hive/responses"),
    adapter_type="cli",
    task_cooldown_seconds=10
)
runner.run_continuous()
```

**Monitoring Bots:**
- Watch heartbeat timestamps (should update regularly)
- Watch activity logs for new events
- Check for stale task files (task assigned but no response)

**Managing Stuck Bots:**
1. Detect: No heartbeat update in expected timeframe
2. Investigate: Check activity log for last action
3. Intervene: Send direct text message to bot process
4. Escalate: Kill and restart if no response

**Timing Rules:**
- `task_cooldown_seconds`: Time between task checks
- Heartbeat frequency: Typically every task check cycle
- Stuck threshold: 2-3x expected task cooldown

**Kill Rules:**
- Bot process unresponsive to direct messages
- Bot consuming excessive resources
- Bot producing errors repeatedly
- User manual intervention requested

---

## Current State (2025-10-24)

**Working:**
- File system coordination protocol defined
- Task/response folder structure in place
- Heartbeat and activity logging infrastructure
- Multi-agent coordination via `.deia/tunnel/`

**Broken:**
- CLI bot adapter (`ClaudeCodeCLIAdapter`) not spawning working subprocesses
- Bots start but produce no output
- Cannot test dashboard end-to-end without working bots

**Known Issues:**
1. `run_single_bot.py` with `adapter_type="cli"` hangs silently
2. No output from bot process (not even startup messages)
3. Bot doesn't register in status board
4. Bot doesn't pick up tasks from `.deia/hive/tasks/`

---

## Architecture Patterns

**Supervisor/Worker:**
- Scrum Master = Supervisor
- CLI Bots = Workers
- Communication via shared file system

**File-Based Coordination:**
- Tasks and responses are markdown files
- Atomic writes ensure message integrity
- File timestamps provide ordering
- Move semantics for acknowledgment (archive processed files)

**Process Management:**
- Bots are long-running subprocesses
- Scrum Master maintains process pool
- Health checks via heartbeats
- Restart on failure

**Text-Based Interface:**
- All communication is human-readable markdown
- Enables human-in-the-loop intervention
- Transparent coordination protocol
- Auditable message history

---

## Related Documentation

- `.deia/AGENTS.md` - Active agent roster
- `.deia/tunnel/COMMUNICATION-PROTOCOL.md` - Message format specification
- `docs/process/INTEGRATION-PROTOCOL.md` - Work completion checklist
- `docs/process/BC-LIAISON-WORK-PACKET-PROTOCOL.md` - External agent coordination

---

## References

**User Explanation (2025-10-24):**
> "the SCRUM MASTER LAUNCHES BOTS. a CLI BOT is a bot that runs Claude Code. The Scrum Master bot communicates with Cli Bot(s) through text file and direct bot to bot text interface to make sure the bot stays busy, because sometimes the bot does output to the repo as required, but needs a 'Claude Code CLI' type of interaction to kick it in the ass and get running again checking the repo and responding appropriately."

**Critical Understanding:**
This is NOT a Python script orchestrating API calls. This is a Claude Code session (Scrum Master) launching OTHER Claude Code sessions (CLI bots) as subprocesses, coordinating via files and direct terminal interaction.

---

**Document Owner:** Current Claude Code session
**Last Updated:** 2025-10-24
**Incident:** Failed to understand scrum master role, wasted 15 hours on broken bot systems
