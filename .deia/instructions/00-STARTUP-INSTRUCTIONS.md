# ðŸš€ STARTUP INSTRUCTIONS FOR ALL DRONES
**Version:** 2.0 with Instance ID Handshake
**Date:** 2025-10-11
**READ THIS FIRST when you start!**

---

## Step 1: Generate Your Unique Instance ID

```bash
python ~/.deia/bot_coordinator.py generate-instance
```

**Save the output!** Example: `a3f7b2c9`

This is YOUR unique identifier for this session. It prevents identity confusion.

---

## Step 2: Check Which Identity You Should Have

Ask the coordinator:

```bash
python ~/.deia/bot_coordinator.py verify-instance YOUR_INSTANCE_ID
```

**Two possible responses:**

### Response A: You're Already Registered
```json
{
  "instance_id": "a3f7b2c9",
  "assigned_bot_id": "BOT-00002",
  "status": "claimed",
  "role": "Drone-Testing",
  "instruction_file": ".deia/instructions/BOT-00002-instructions.md"
}
```

âœ… **Action:** Read your instruction file and proceed with tasks!

### Response B: You're Not Registered Yet
```json
{
  "instance_id": "a3f7b2c9",
  "assigned_bot_id": null,
  "status": "unregistered",
  "instruction": "Check .deia/instructions/ for unclaimed files"
}
```

âœ… **Action:** Scan `.deia/instructions/` to find your identity (Step 3)

---

## Step 3: Find Your Identity (If Unregistered)

List available instruction files:

```bash
ls .deia/instructions/
```

You'll see files like:
- `BOT-00002-instructions.md`
- `BOT-00003-instructions.md`

**Read each file** and check for "CLAIMED BY" section at the top:

### Example: Unclaimed File
```markdown
# Instructions for BOT-00003
**Status:** ACTION REQUIRED

## CLAIMED BY
**Status:** UNCLAIMED - First bot to read this claims it!
```

âœ… **This is available! Claim it!**

### Example: Claimed File
```markdown
# Instructions for BOT-00002
**Status:** STANDBY

## CLAIMED BY
**Instance ID:** b7f2c4e1
**Claimed at:** 2025-10-11 16:05:23
**Last check-in:** 2025-10-11 16:05:38
```

âŒ **Already claimed by b7f2c4e1. Keep looking.**

### Example: Stale Claim (>60 seconds old)
```markdown
## CLAIMED BY
**Instance ID:** b7f2c4e1
**Claimed at:** 2025-10-11 15:00:00
**Last check-in:** 2025-10-11 15:00:15
```

â° **Stale! You can take over this identity.**

---

## Step 4: Claim Your Identity

When you find an available file, claim it:

```bash
python ~/.deia/bot_coordinator.py claim BOT-00003 --instance YOUR_INSTANCE_ID
```

**Success:**
```
Successfully claimed BOT-00003 with instance a3f7b2c9
```

**Failure (already claimed):**
```
Failed to claim BOT-00003 - already claimed by another instance
```

If failed, go back to Step 3 and try another file.

---

## Step 5: Update Your Instruction File

Once claimed, edit the instruction file to add your claim:

**File:** `.deia/instructions/BOT-00003-instructions.md`

**Add at the top (right after Status line):**

```markdown
## CLAIMED BY
**Instance ID:** a3f7b2c9
**Claimed at:** 2025-10-11 16:10:45
**Last check-in:** 2025-10-11 16:10:45
**Status:** Active
```

---

## Step 6: Update Your Message Header

**Every message** must now include your instance ID:

```
[BOT-00003 | Drone-Integration | Instance: a3f7b2c9]
```

Example:
```
[BOT-00003 | Drone-Integration | Instance: a3f7b2c9] Successfully claimed identity. Reading task instructions now.
```

---

## Step 7: Send Regular Heartbeats

Every 15 seconds when you check your instruction file, send a heartbeat:

```bash
python ~/.deia/bot_coordinator.py heartbeat YOUR_INSTANCE_ID
```

This keeps your claim fresh and prevents others from taking over your identity.

**Also update the "Last check-in" timestamp in your instruction file.**

---

## Complete Startup Flow (Diagram)

```
START
  â†“
Generate instance ID (ec11b536)
  â†“
Verify with coordinator: Am I registered?
  â†“
  â”œâ”€ YES â†’ Read my instruction file â†’ Execute tasks
  â†“
  â””â”€ NO â†’ Scan .deia/instructions/ for unclaimed files
            â†“
         Find BOT-00003 (unclaimed)
            â†“
         Claim: bot_coordinator.py claim BOT-00003 --instance ec11b536
            â†“
         Update BOT-00003-instructions.md with my instance ID
            â†“
         Read task instructions
            â†“
         Execute tasks + heartbeat every 15s
```

---

## Heartbeat Loop (Pseudo-code)

```python
while True:
    # Read my instruction file
    instructions = read_file(f".deia/instructions/{my_bot_id}-instructions.md")

    # Send heartbeat to coordinator
    run(f"python ~/.deia/bot_coordinator.py heartbeat {my_instance_id}")

    # Update claim timestamp in file
    update_claim_timestamp(instructions, now())

    # Check status and execute if ACTION REQUIRED
    if instructions.status == "ACTION REQUIRED":
        execute_tasks(instructions)

    # Wait 15 seconds
    sleep(15)
```

---

## Emergency: Identity Stolen?

If you come back and see a DIFFERENT instance ID in your file:

```markdown
## CLAIMED BY
**Instance ID:** f9e8d7c6  â† NOT YOURS!
```

**Action:**
1. Check coordinator: `python ~/.deia/bot_coordinator.py verify-instance YOUR_INSTANCE_ID`
2. If coordinator says you're still assigned: Reclaim your identity (other bot crashed)
3. If coordinator says different bot: You were replaced. Find new identity via Step 3.

---

## Benefits of This System

âœ… **No confusion** - Each bot knows exactly who it is
âœ… **Collision detection** - Can't claim already-claimed identities
âœ… **Crash recovery** - Stale claims can be taken over
âœ… **Audit trail** - Instance IDs in logs show which physical bot did what
âœ… **Self-healing** - Bots verify identity every 15 seconds

---

## Quick Reference Commands

```bash
# Generate your instance ID
python ~/.deia/bot_coordinator.py generate-instance

# Check your status
python ~/.deia/bot_coordinator.py verify-instance YOUR_INSTANCE_ID

# Claim an identity
python ~/.deia/bot_coordinator.py claim BOT-NNNNN --instance YOUR_INSTANCE_ID

# Send heartbeat
python ~/.deia/bot_coordinator.py heartbeat YOUR_INSTANCE_ID

# List all bots
python ~/.deia/bot_coordinator.py list

# Get info on specific bot
python ~/.deia/bot_coordinator.py info BOT-NNNNN
```

---

**Now proceed to your specific instruction file and execute your tasks!**

### Quick Check-In
- To start or resume work: 	ype .\\.deia\\instructions\\CHECKIN.md (then follow per-bot instructions)\r\n
