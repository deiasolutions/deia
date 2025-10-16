# Bot Queue Service Guide

**Version:** 1.0
**Date:** 2025-10-12
**Purpose:** FIFO bot queue with skill tracking for optimal bot selection

---

## Overview

The Bot Queue Service manages a FIFO queue of available bots with skill and context tracking. It enables intelligent bot selection for the DEIA hive, ensuring tasks are assigned to the most qualified available bot.

**Key Features:**
- FIFO check-in tracking
- Skill profiles per bot
- Context awareness (what bot recently worked on)
- Optimal bot selection (skill + context matching)
- Idle bot management (assign prep tasks like BOK reading)
- Persistent storage (JSON)

---

## Quick Start

### Python API

```python
from deia.bot_queue import BotQueue

# Create queue
queue = BotQueue()

# Add bots with skills
queue.add_bot(
    bot_id="BOT-00002",
    skills=["testing", "python", "pytest"],
    context_history=["worked on sync tests"]
)

queue.add_bot(
    bot_id="BOT-00003",
    skills=["integration", "api", "rest"],
    context_history=["built downloads monitor"]
)

# Get next available bot (FIFO)
next_bot = queue.get_next_available()
# Returns: "BOT-00002"

# Get next bot with specific skills
testing_bot = queue.get_next_available(required_skills=["testing"])
# Returns: "BOT-00002"

# Mark bot as busy
queue.mark_busy("BOT-00002", "Running integration tests")

# Update context when task completes
queue.update_context("BOT-00002", "Completed integration tests for sync module")
queue.mark_available("BOT-00002")
```

### CLI Interface

```bash
# Add bot to queue
python -m deia.bot_queue add BOT-00002 --skills testing python pytest

# Get next available bot
python -m deia.bot_queue next

# Get next bot with specific skills
python -m deia.bot_queue next --skills testing python

# Mark bot as busy
python -m deia.bot_queue busy BOT-00002 "Running tests"

# Mark bot as available
python -m deia.bot_queue available BOT-00002

# Update bot context
python -m deia.bot_queue update-context BOT-00002 "Completed sync tests"

# List available bots
python -m deia.bot_queue list

# Get bot profile
python -m deia.bot_queue profile BOT-00002
```

---

## API Reference

### `BotQueue(queue_file=None)`

Initialize bot queue.

**Args:**
- `queue_file` (Path, optional): Path to queue JSON file. Defaults to `~/.deia/bot-queue.json`

**Example:**
```python
from pathlib import Path
queue = BotQueue(Path(".deia/test-queue.json"))
```

---

### `add_bot(bot_id, skills, context_history)`

Add bot to queue with profile.

**Args:**
- `bot_id` (str): Bot ID (e.g., "BOT-00002")
- `skills` (List[str]): Bot skills (e.g., ["testing", "python"])
- `context_history` (List[str]): Recent work context

**Example:**
```python
queue.add_bot(
    bot_id="BOT-00002",
    skills=["testing", "python", "pytest"],
    context_history=["worked on sync tests", "BOK pattern documentation"]
)
```

---

### `remove_bot(bot_id)`

Remove bot from queue (bot going offline).

**Args:**
- `bot_id` (str): Bot ID to remove

**Example:**
```python
queue.remove_bot("BOT-00002")
```

---

### `get_next_available(required_skills=None, context_keywords=None)`

Get best available bot from queue.

**Selection Algorithm:**
1. Filter to available bots (not busy, no idle prep)
2. If `required_skills` provided, prefer bots with matching skills
3. If `context_keywords` provided, prefer bots with relevant context
4. Return first match in FIFO order

**Args:**
- `required_skills` (List[str], optional): Required skills
- `context_keywords` (List[str], optional): Context keywords to match

**Returns:**
- Bot ID (str) of best available bot, or None if queue empty

**Examples:**
```python
# Get any available bot (FIFO)
bot = queue.get_next_available()

# Get bot with specific skills
bot = queue.get_next_available(required_skills=["testing", "python"])

# Get bot with relevant context
bot = queue.get_next_available(
    required_skills=["integration"],
    context_keywords=["legal", "BOK"]
)
```

**Scoring:**
- +10 points per matching skill
- +5 points per matching context keyword
- Ties broken by FIFO order

---

### `mark_busy(bot_id, task)`

Mark bot as busy with a task.

**Args:**
- `bot_id` (str): Bot ID
- `task` (str): Task description

**Example:**
```python
queue.mark_busy("BOT-00002", "Running integration tests for sync module")
```

**Side Effects:**
- Sets `status` to "busy"
- Sets `current_task` to task description
- Clears `idle_prep` if set
- Bot will not be returned by `get_next_available()`

---

### `mark_available(bot_id)`

Mark bot as available.

**Args:**
- `bot_id` (str): Bot ID

**Example:**
```python
queue.mark_available("BOT-00002")
```

**Side Effects:**
- Sets `status` to "available"
- Clears `current_task`
- Bot becomes eligible for `get_next_available()`

---

### `update_context(bot_id, recent_work)`

Update bot's context history.

**Args:**
- `bot_id` (str): Bot ID
- `recent_work` (str): Description of recent work

**Example:**
```python
queue.update_context("BOT-00002", "Completed integration tests for sync module")
```

**Effect:**
Appends to bot's `context_history`. Used for context matching in `get_next_available()`.

---

### `assign_idle_prep(bot_id, prep_task)`

Assign preparation task to idle bot.

**Args:**
- `bot_id` (str): Bot ID
- `prep_task` (str): Preparation task

**Example:**
```python
queue.assign_idle_prep("BOT-00002", "Read BOK INDEX for process diagnosis")
```

**Effect:**
- Bot stays in queue but is not returned by `get_next_available()`
- Used to keep idle bots productive (e.g., reading documentation)
- Cleared when bot is assigned real task via `mark_busy()`

---

### `get_bot_profile(bot_id)`

Get bot's full profile.

**Args:**
- `bot_id` (str): Bot ID

**Returns:**
- Bot profile dict, or None if not found

**Profile Structure:**
```python
{
    "bot_id": "BOT-00002",
    "skills": ["testing", "python", "pytest"],
    "context_history": ["worked on sync tests"],
    "status": "available",  # or "busy"
    "current_task": None,  # or task description
    "idle_prep": None,  # or prep task
    "added_at": "2025-10-12T10:30:00",
    "last_updated": "2025-10-12T10:45:00"
}
```

---

### `list_available_bots()`

List all available bots in queue order.

**Returns:**
- List of bot IDs (List[str])

**Example:**
```python
available = queue.list_available_bots()
# Returns: ["BOT-00002", "BOT-00003", "BOT-00004"]
```

---

## Integration with Hive System

### Queen Bot Usage

The Queen (BOT-00001) uses the queue service to assign tasks:

```python
from deia.bot_queue import BotQueue

queue = BotQueue()

# Add drones to queue as they come online
queue.add_bot("BOT-00002", ["testing", "python"], [])
queue.add_bot("BOT-00003", ["integration", "api"], [])

# Task assignment
task = get_next_task_from_backlog()  # Your backlog logic

if task.requires_testing:
    bot_id = queue.get_next_available(required_skills=["testing"])
    if bot_id:
        queue.mark_busy(bot_id, f"BACKLOG-{task.id}: {task.title}")
        assign_task_to_bot(bot_id, task)  # Your assignment logic

# When task completes
queue.update_context(bot_id, f"Completed {task.title}")
queue.mark_available(bot_id)
```

### Drone Bot Self-Registration

Drones register themselves when they come online:

```python
from deia.bot_queue import BotQueue

queue = BotQueue()

# Register with skills
queue.add_bot(
    bot_id="BOT-00002",
    skills=["testing", "python", "pytest", "tdd"],
    context_history=[]
)

# Bot is now in queue and can be assigned tasks
```

### Idle Bot Management

When no good task match exists, assign prep work:

```python
bot_id = queue.get_next_available(required_skills=["blockchain"])

if bot_id:
    # Found a bot with blockchain skills
    queue.mark_busy(bot_id, "BACKLOG-042: Blockchain integration")
else:
    # No blockchain bot available, assign prep to any idle bot
    idle_bot = queue.get_next_available()
    if idle_bot:
        queue.assign_idle_prep(
            idle_bot,
            "Read BOK INDEX to prepare for process diagnosis"
        )
```

---

## Data Storage

Queue persists to JSON file at `~/.deia/bot-queue.json` (or custom path).

**Format:**
```json
{
  "queue": [
    "BOT-00002",
    "BOT-00003",
    "BOT-00004"
  ],
  "profiles": {
    "BOT-00002": {
      "bot_id": "BOT-00002",
      "skills": ["testing", "python", "pytest"],
      "context_history": ["worked on sync tests"],
      "status": "available",
      "current_task": null,
      "idle_prep": null,
      "added_at": "2025-10-12T10:30:00.123456",
      "last_updated": "2025-10-12T10:30:00.123456"
    }
  },
  "version": "1.0"
}
```

---

## Best Practices

### Skill Naming

Use consistent, lowercase skill names:
- ✅ "testing", "python", "pytest", "integration", "api"
- ❌ "Testing", "PYTHON", "PyTest", "Integration Tests"

### Context Updates

Update context after every completed task:
```python
queue.update_context(bot_id, f"Completed BACKLOG-{task_id}: {task.title}")
```

This improves future bot selection.

### Idle Prep

Assign prep tasks to idle bots:
```python
if no_good_match:
    idle_bot = queue.get_next_available()
    queue.assign_idle_prep(idle_bot, "Read BOK INDEX for X")
```

Common prep tasks:
- "Read BOK INDEX for process diagnosis"
- "Review recent hive activity"
- "Study DEIA methodology docs"
- "Prepare for code review tasks"

### Queue Cleanup

Remove bots when they go offline:
```python
queue.remove_bot("BOT-00002")
```

---

## Examples

### Example 1: Simple Task Assignment

```python
from deia.bot_queue import BotQueue

queue = BotQueue()

# Setup
queue.add_bot("BOT-00002", ["testing"], [])
queue.add_bot("BOT-00003", ["integration"], [])

# Assign task
bot = queue.get_next_available(required_skills=["testing"])
queue.mark_busy(bot, "Run sync tests")

# ... bot does work ...

# Complete
queue.update_context(bot, "Completed sync tests - all passing")
queue.mark_available(bot)
```

### Example 2: Context-Aware Selection

```python
# Bots with different context
queue.add_bot("BOT-00002", ["testing"], ["worked on sync module"])
queue.add_bot("BOT-00003", ["testing"], ["worked on legal docs", "BOK patterns"])

# Task needs testing + legal knowledge
bot = queue.get_next_available(
    required_skills=["testing"],
    context_keywords=["legal"]
)
# Returns: BOT-00003 (has legal context)
```

### Example 3: Idle Management

```python
# Try to find bot with rare skill
bot = queue.get_next_available(required_skills=["rust"])

if not bot:
    # No rust expert available
    # Assign prep task to keep bot productive
    idle_bot = queue.get_next_available()
    if idle_bot:
        queue.assign_idle_prep(idle_bot, "Study Rust documentation for future tasks")
```

---

## Testing

Run tests:
```bash
pytest tests/test_bot_queue.py -v
```

Test coverage: 52% (21 tests, all passing)

---

## Troubleshooting

### "No available bots"

**Problem:** `get_next_available()` returns None

**Solutions:**
- Check if any bots registered: `queue.list_available_bots()`
- Check if all bots busy: Look at bot profiles
- Check if bots have idle_prep: Clear with `mark_busy()`

### "Bot not being selected"

**Problem:** Bot exists but not returned by `get_next_available()`

**Check:**
- Bot status: Should be "available"
- Idle prep: Should be None
- Skills: Must match required_skills if provided

**Debug:**
```python
profile = queue.get_bot_profile("BOT-00002")
print(profile)  # Check status, idle_prep, skills
```

### "Skill matching not working"

**Problem:** Bot with skills not selected

**Cause:** Skill names don't match exactly

**Solution:** Use consistent, lowercase skill names
```python
# Wrong
queue.add_bot("BOT-00002", ["Testing", "PYTHON"], [])
bot = queue.get_next_available(required_skills=["testing"])  # Won't match

# Right
queue.add_bot("BOT-00002", ["testing", "python"], [])
bot = queue.get_next_available(required_skills=["testing"])  # Matches
```

---

## Related Systems

- **Bot Coordinator** (`~/.deia/bot_coordinator.py`) - Bot registration and identity
- **Bot Status Board** (`.deia/bot-status-board.json`) - Real-time bot status
- **Hive Coordination Rules** (`.deia/hive-coordination-rules.md`) - Communication protocols

**Integration:**
1. Bot registers with Bot Coordinator (gets BOT-XXXXX ID)
2. Bot adds itself to Bot Queue (with skills)
3. Queen uses Bot Queue to select bots for tasks
4. Queen updates Bot Status Board with assignments

---

## Future Enhancements

Potential improvements:
- **Load balancing:** Track tasks per bot, prefer less busy bots
- **Skill levels:** Not just binary (has skill / doesn't have skill), but proficiency levels
- **Historical performance:** Track success rate per bot per skill
- **Team formation:** Find best pair/group of bots for complex tasks
- **Adaptive learning:** Learn which bot+task combinations work best

---

## Changelog

**v1.0** (2025-10-12)
- Initial release
- FIFO queue with skill tracking
- Context-aware bot selection
- Idle prep management
- CLI interface
- 21 passing tests

---

**Last Updated:** 2025-10-12
**Maintained By:** BOT-00006 (Drone-Development)
**File Location:** `.deia/bot-queue-service-guide.md`
