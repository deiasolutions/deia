# Hive Instructions System

## How It Works

**Queen (BOT-00001) writes instruction files here.**
**Drones read their instruction files and execute tasks.**

---

## For Drones

### 1. Find Your Instructions

Your instruction file is named: `BOT-NNNNN-instructions.md`

Example:
- BOT-00002 reads: `BOT-00002-instructions.md`
- BOT-00003 reads: `BOT-00003-instructions.md`

### 2. Check for Updates

**On startup, always read:**
```bash
cat .deia/instructions/BOT-NNNNN-instructions.md
```

**Check for new task assignments:**
```bash
ls -lt .deia/instructions/BOT-NNNNN-*.md | head -5
```

### 3. Execute Instructions

Follow the instructions exactly as written.

### 4. Report Back

When done, create a report:
```
.deia/reports/BOT-NNNNN-report-YYYYMMDD-HHMMSS.md
```

Update your status:
```bash
python ~/.deia/bot_coordinator.py status BOT-NNNNN complete --message "Task done, report filed"
```

---

## For Queen

### 1. Create Instructions

Write to: `.deia/instructions/BOT-NNNNN-instructions.md`

Include:
- Bot identity and role
- Current task
- Acceptance criteria
- How to report back

### 2. Assign New Tasks

Create new instruction files:
```
BOT-NNNNN-task-name.md
```

Drones check for new files regularly.

### 3. Review Reports

Drone reports appear in:
```
.deia/reports/BOT-NNNNN-*.md
```

---

## File Structure

```
.deia/
  instructions/
    README.md                          # This file
    BOT-00001-instructions.md          # Queen's instructions (self-reference)
    BOT-00002-instructions.md          # Drone 1 instructions
    BOT-00003-instructions.md          # Drone 2 instructions
    BOT-00002-test-assignment.md       # Specific task for Drone 1
    BOT-00003-phase2-task.md           # Specific task for Drone 2

  reports/
    BOT-00002-report-20251011-153000.md
    BOT-00003-sync-integration-complete.md

  handoffs/
    # Original handoff docs (for reference)
```

---

## Protocol

1. **Queen writes** instructions
2. **Drones read** instructions from repo
3. **Drones execute** tasks
4. **Drones write** reports back to repo
5. **Queen reviews** reports
6. **Repeat**

**No copy-paste commands to Dave!** Everything through the repo.
