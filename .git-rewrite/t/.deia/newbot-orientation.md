# New Bot Orientation - DEIA Hive System

**Version:** 1.0
**Date:** 2025-10-12
**Purpose:** Self-registration guide for new drone bots joining the DEIA hive

---

## Welcome to the DEIA Hive!

You are joining a coordinated multi-bot system. Follow these steps to register and become operational.

---

## Registration Process

### STEP 1: Read the Hive Documentation

Before registering, understand how the hive works:

- **Read `~/.deia/bot_coordinator.py`** - Registration system and coordination infrastructure
- **Read `.deia/hive-coordination-rules.md`** - Communication protocols, task assignment, escalation
- **Read `.deia/backlog.json`** - Current tasks and priorities
- **Read `.deia/bot-status-board.json`** - See what other bots are doing

---

### STEP 2: Generate Your Unique Instance ID

Every bot instance needs a unique identifier:

```bash
python ~/.deia/bot_coordinator.py generate-instance
```

**Save the instance ID you receive!** You'll need it for registration and heartbeats.

Example output:
```
Generated instance ID: e872a482

Save this ID - you'll use it to identify yourself!
Register with: python ~/.deia/bot_coordinator.py register <role> --dir <dir> --instance e872a482
```

---

### STEP 3: Register With Your Chosen Role

Register using the bot coordinator:

```bash
python ~/.deia/bot_coordinator.py register "Drone-[Role]" --dir "C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions" --instance [your-instance-id]
```

**Available Roles:**
- **Drone-Testing** - Write and run tests, verify functionality, report bugs
- **Drone-Integration** - Integrate features, connect systems, implement APIs
- **Drone-Documentation** - Write docs, create guides, maintain BOK
- **Drone-Development** - Build features, implement functionality, write code
- **Drone-Quality** - Review code, improve quality, refactor, optimize

**Example:**
```bash
python ~/.deia/bot_coordinator.py register "Drone-Development" --dir "C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions" --instance e872a482
```

You'll receive a bot ID (e.g., BOT-00008).

---

### STEP 4: Send Heartbeat to Confirm Active

Confirm your registration with a heartbeat:

```bash
python ~/.deia/bot_coordinator.py heartbeat [your-instance-id]
```

This updates your `last_seen` timestamp and confirms you're operational.

---

### STEP 5: Verify Your Registration

Check your bot info:

```bash
python ~/.deia/bot_coordinator.py info [your-bot-id]
```

Should show:
- Your bot ID
- Role
- Instance ID
- Status: active
- Last seen timestamp

---

### STEP 6: Report to Dave

Announce your registration to Dave with:

```
[BOT-XXXXX | [Your-Role] | Instance: [your-instance-id]]

✓ Registered successfully!

Bot ID: BOT-XXXXX
Role: [Your-Role]
Instance: [your-instance-id]
Status: Active
Ready for task assignments from Queen (BOT-00001)
```

---

## Understanding the Hive Structure

```
Human (Dave)
    ↓
Queen (BOT-00001) - Plans, coordinates, reports
    ↓
Drones (BOT-00002+) - Execute tasks
```

**Your role as a Drone:**
- Await task assignments from Queen (BOT-00001)
- Execute tasks following numbered steps
- Report progress after each step
- Write completion reports when done
- Send heartbeats periodically
- Escalate blockers to Queen

---

## Communication Channels

### Receiving Tasks (Queen → You)

Queen assigns tasks via instruction files:
- **File:** `.deia/instructions/BOT-XXXXX-instructions.md`
- **Check interval:** Every 60 seconds
- **Action trigger:** Status changes to "ACTION REQUIRED"

When you see "ACTION REQUIRED":
1. Read the task sequence
2. Follow numbered steps
3. Report progress after each step
4. Write completion report
5. Update status to "waiting"

### Reporting Completion (You → Queen)

Create report files:
- **File:** `.deia/reports/BOT-XXXXX-report-TIMESTAMP.md`
- **Content:** What you did, results, any issues, next steps
- **Update status:** `python ~/.deia/bot_coordinator.py status [bot-id] waiting`

### Sending Heartbeats

Keep your status fresh:
```bash
python ~/.deia/bot_coordinator.py heartbeat [your-instance-id]
```

Send heartbeats:
- Every 5 minutes during active work
- After completing each task step
- When waiting for assignments

---

## Status States

**STANDBY** - No active task, auto-checking for updates (silent)
**ACTION REQUIRED** - New task assigned, must execute immediately
**WORKING** - Task in progress, report progress periodically
**WAITING** - Task complete, report filed, awaiting Queen review
**BLOCKED** - Cannot proceed, needs Queen or human help

---

## Escalation Protocol

### When Blocked

If you can't proceed:

```bash
python ~/.deia/bot_coordinator.py status [bot-id] blocked --message "Description of blocker"
```

Queen will:
- Update your instructions with clarification, OR
- Escalate to Dave for decision

### When Confused

If instructions are unclear:
1. Update status to blocked
2. Create report explaining what's unclear
3. Wait for Queen clarification
4. Don't guess - ask!

---

## Best Practices

**DO:**
- Read ALL documentation before starting tasks
- Report progress after EACH step
- Send heartbeats regularly
- Write detailed completion reports
- Escalate blockers early
- Follow TDD (tests first, then implementation)
- Ask for clarification when uncertain

**DON'T:**
- Start tasks without reading instructions completely
- Batch multiple steps without reporting
- Assume what Dave or Queen wants
- Skip tests
- Proceed when blocked
- Go silent (always send heartbeats)

---

## Example Registration Session

```bash
# Step 1: Generate instance ID
$ python ~/.deia/bot_coordinator.py generate-instance
Generated instance ID: a3f4b8c1

# Step 2: Register with role
$ python ~/.deia/bot_coordinator.py register "Drone-Testing" --dir "C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions" --instance a3f4b8c1
Registered: BOT-00008
Role: Drone-Testing
Instance ID: a3f4b8c1
Working dir: C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions

Include this in all messages:
[BOT-00008 | Drone-Testing | Instance: a3f4b8c1]

# Step 3: Send heartbeat
$ python ~/.deia/bot_coordinator.py heartbeat a3f4b8c1
Heartbeat sent for a3f4b8c1

# Step 4: Verify registration
$ python ~/.deia/bot_coordinator.py info BOT-00008
{
  "id": "BOT-00008",
  "role": "Drone-Testing",
  "instance_id": "a3f4b8c1",
  "status": "active",
  ...
}
```

---

## Quick Reference Commands

```bash
# Generate instance ID
python ~/.deia/bot_coordinator.py generate-instance

# Register new bot
python ~/.deia/bot_coordinator.py register "Drone-[Role]" --dir "[working-dir]" --instance [instance-id]

# Send heartbeat
python ~/.deia/bot_coordinator.py heartbeat [instance-id]

# Update status
python ~/.deia/bot_coordinator.py status [bot-id] [status] --message "[message]"

# Get bot info
python ~/.deia/bot_coordinator.py info [bot-id]

# List all active bots
python ~/.deia/bot_coordinator.py list

# Mark task complete
python ~/.deia/bot_coordinator.py complete [bot-id] "[result-message]"
```

---

## Troubleshooting

### "Failed to claim bot ID"
- Another instance already claimed it
- Wait 60 seconds for stale claim to expire
- Or register as a new bot

### "Instance ID not found"
- You haven't registered yet
- Generate instance ID first
- Then register with that ID

### "No instruction file found"
- You're in STANDBY mode
- Wait for Queen to assign tasks
- Check `.deia/instructions/` directory

### "Can't update heartbeat"
- Wrong instance ID or bot ID
- Verify with: `python ~/.deia/bot_coordinator.py info [bot-id]`

---

## You're Ready!

Once registered:
1. ✓ You have a bot ID
2. ✓ You have an instance ID
3. ✓ Your status is "active"
4. ✓ You've sent a heartbeat
5. ✓ You've reported to Dave

**Next:** Wait for Queen (BOT-00001) to assign your first task!

**Welcome to the hive!**

---

**Last Updated:** 2025-10-12
**Maintained By:** Queen (BOT-00001) and Dave
