# TASK-002-016: URGENT - Sprint-Aware Task Filtering - RESPONSE

**Task ID:** TASK-002-016
**Bot ID:** BOT-002
**Priority:** P0 (BLOCKING)
**Status:** ANALYSIS & SPECIFICATION COMPLETE
**Completed:** 2025-10-28T14:37:00Z
**Duration:** 15 minutes

---

## CRITICAL ISSUE SUMMARY

**Problem:** Bots process tasks from old/completed sprints, contaminating new sprint work

**Example:**
```
Oct 21: Sprint 1 ends, leaves TASK-100 in queue
Oct 22: Sprint 2 starts, BOT-002 processes TASK-100 (wrong!)
Result: Sprint 2 contaminated with Sprint 1 work
```

**Impact:**
- Unclear task ownership
- Context switching between sprints
- Cannot measure sprint velocity
- Violates agile process
- Operator confusion

**Solution:** Implement sprint-aware task filtering

---

## SOLUTION ARCHITECTURE

### 3-Part Fix

**Part 1: Tag tasks with sprint ID**
```markdown
**Sprint:** SPRINT-2025-10-28
**Expires:** 2025-10-29T23:59:59Z
```

**Part 2: Configure bot with sprint assignment**
```bash
python run_single_bot.py BOT-002 --sprint SPRINT-2025-10-28
```

**Part 3: Filter in BotRunner**
```
check_file_queue():
  For each task:
    if task.sprint_id != current_sprint_id:
      skip (wrong sprint)
    if task.expires_at < now:
      skip (expired)
    else:
      process task
```

---

## IMPLEMENTATION SPECIFICATION

### 1. Task File Format (NEW)

**Add two fields to task markdown:**

```markdown
# TASK-002-014: Unified Timeline API

**Task ID:** TASK-002-014
**Bot ID:** BOT-002
**Priority:** P1
**Sprint:** SPRINT-2025-10-28        ← NEW
**Expires:** 2025-10-29T23:59:59Z    ← NEW
**Created:** 2025-10-28
**Timeout:** 300 seconds

## INSTRUCTION

[task content]
```

**Sprint format:** `SPRINT-YYYY-MM-DD`
**Expires format:** ISO 8601 with Z (UTC)

---

### 2. BotRunner Configuration

**Update `__init__` method:**

```python
def __init__(self,
    bot_id,
    work_dir,
    # ... existing params ...
    sprint_id=None,      # NEW
    season=None,         # NEW (alternative naming)
    ):
    self.bot_id = bot_id
    self.sprint_id = sprint_id  # NEW
    self.season = season        # NEW (optional)
```

**Store sprint ID for filtering later**

---

### 3. Command Line Interface

**Update `run_single_bot.py`:**

```python
import argparse

parser = argparse.ArgumentParser()
# ... existing arguments ...
parser.add_argument('--sprint', type=str, default=None,
                   help='Sprint ID (e.g., SPRINT-2025-10-28)')

args = parser.parse_args()

runner = BotRunner(
    bot_id=args.bot_id,
    sprint_id=args.sprint,  # NEW
    # ... other params
)
```

**Usage:**
```bash
python run_single_bot.py BOT-002 --sprint SPRINT-2025-10-28
```

---

### 4. Filtering Logic

**Replace `check_file_queue()` method:**

```python
def check_file_queue(self):
    """Get next task from CURRENT SPRINT ONLY"""
    task_dir = Path(self.task_queue_dir)
    task_files = sorted(task_dir.glob("TASK-*.md"))

    for task_file in task_files:
        # Skip already processed
        if task_file.name in self.processed_tasks:
            continue

        # Parse task
        task = self._parse_task_file(task_file)
        if not task:
            continue

        # NEW: Sprint filtering
        if self.sprint_id:
            task_sprint = task.get("sprint_id")
            if task_sprint != self.sprint_id:
                logger.debug(f"Skipping {task['task_id']}: "
                           f"wrong sprint ({task_sprint} != {self.sprint_id})")
                continue

        # NEW: Expiration filtering
        if self._is_task_expired(task):
            logger.info(f"Skipping {task['task_id']}: expired")
            continue

        # All filters passed - return task
        return task

    return None
```

**Key behavior:**
- Skip tasks from different sprints (log why)
- Skip expired tasks (log why)
- Process matching tasks
- Return None if no valid tasks

---

### 5. Helper Methods

**Check expiration:**

```python
def _is_task_expired(self, task):
    """Check if task has passed expiration time"""
    if "expires_at" not in task:
        return False  # No expiration = never expires

    try:
        # Parse ISO 8601 timestamp
        expires = datetime.fromisoformat(
            task["expires_at"].replace('Z', '+00:00')
        )
        # Compare to current UTC time
        current = datetime.now(timezone.utc)
        return current > expires
    except Exception as e:
        logger.error(f"Error parsing expiration: {e}")
        return False
```

**Parse task metadata:**

```python
def _parse_task_file(self, file_path):
    """Extract sprint_id and expires_at from task markdown"""
    import re

    try:
        with open(file_path) as f:
            content = f.read()

        # Extract Sprint field: **Sprint:** SPRINT-2025-10-28
        sprint_match = re.search(r'\*\*Sprint:\*\*\s+(\S+)', content)
        sprint_id = sprint_match.group(1) if sprint_match else None

        # Extract Expires field: **Expires:** 2025-10-29T23:59:59Z
        expires_match = re.search(r'\*\*Expires:\*\*\s+(\S+)', content)
        expires_at = expires_match.group(1) if expires_match else None

        # Extract other fields (existing code)
        task_id = self._extract_task_id(content)
        priority = self._extract_priority(content)
        command = self._extract_command(content)

        return {
            "task_id": task_id,
            "sprint_id": sprint_id,
            "expires_at": expires_at,
            "priority": priority,
            "command": command,
            "file": str(file_path),
        }
    except Exception as e:
        logger.error(f"Error parsing {file_path}: {e}")
        return None
```

---

## PROCESS DOCUMENTATION UPDATE

**Update SCRUMMASTER-PROTOCOL.md**

Add new section:

```markdown
### Sprint-Aware Task Queueing

**Critical:** All tasks must include sprint metadata.

**Before queuing a task:**
1. Determine current sprint ID (e.g., SPRINT-2025-10-28)
2. Determine sprint end date
3. Include both in task file

**Task template:**

cat > .deia/hive/tasks/BOT-002/TASK-002-014-P1-timeline-api.md << 'EOF'
# TASK-002-014: Unified Timeline API

**Task ID:** TASK-002-014
**Bot ID:** BOT-002
**Priority:** P1
**Sprint:** SPRINT-2025-10-28           ← REQUIRED
**Expires:** 2025-10-29T23:59:59Z       ← REQUIRED
**Created:** 2025-10-28
**Timeout:** 300 seconds

## INSTRUCTION

[task content]
EOF

**Bots will skip any tasks not matching their assigned sprint.**

**Sprint ID format:** SPRINT-YYYY-MM-DD
**Expires format:** ISO 8601 with Z (UTC)

**Example:**
- Current sprint: SPRINT-2025-10-28
- End date: Oct 29, 23:59:59 UTC
- Expires value: 2025-10-29T23:59:59Z

If bot is started with:
```bash
python run_single_bot.py BOT-002 --sprint SPRINT-2025-10-28
```

Then only tasks with `**Sprint:** SPRINT-2025-10-28` will be processed.
Tasks from SPRINT-2025-10-27 will be skipped.
```

---

## TESTING PROCEDURE

**Scenario: Verify sprint filtering works**

```bash
# 1. Create old sprint task (should be SKIPPED)
cat > .deia/hive/tasks/BOT-002/TASK-999-old.md << 'EOF'
# TASK-999: Old Sprint Task

**Sprint:** SPRINT-2025-10-27
**Expires:** 2025-10-28T00:00:00Z

Do something
EOF

# 2. Create current sprint task (should be PROCESSED)
cat > .deia/hive/tasks/BOT-002/TASK-014-new.md << 'EOF'
# TASK-014: Current Sprint Task

**Sprint:** SPRINT-2025-10-28
**Expires:** 2025-10-29T23:59:59Z

Do something else
EOF

# 3. Create expired task (should be SKIPPED)
cat > .deia/hive/tasks/BOT-002/TASK-998-expired.md << 'EOF'
# TASK-998: Expired Task

**Sprint:** SPRINT-2025-10-28
**Expires:** 2025-10-27T00:00:00Z

Already expired
EOF

# 4. Start BOT-002 with current sprint
python run_single_bot.py BOT-002 --sprint SPRINT-2025-10-28

# 5. Check activity log
tail -20 .deia/bot-logs/BOT-002-activity.jsonl

# Should show:
# - Skipping TASK-999: wrong sprint (SPRINT-2025-10-27)
# - Skipping TASK-998: expired (2025-10-27T00:00:00Z)
# - Processing TASK-014: current sprint (SPRINT-2025-10-28)
```

---

## EDGE CASES

### Edge Case 1: Task with no sprint tag

**Behavior:** Skip it (safer than processing wrong sprint)

```python
if self.sprint_id:
    task_sprint = task.get("sprint_id")
    if task_sprint is None:
        # No sprint specified - skip to be safe
        logger.warning(f"Skipping {task['task_id']}: no sprint specified")
        continue
    if task_sprint != self.sprint_id:
        # Different sprint - skip
        continue
```

### Edge Case 2: Bot running with no sprint specified

**Behavior:** Process all tasks (backward compatible, but not recommended)

```python
if self.sprint_id:
    # Apply sprint filtering
    if task.sprint_id != self.sprint_id:
        continue
else:
    # No sprint configured - process all
    logger.warning("No sprint configured - processing all tasks")
```

### Edge Case 3: Task with no expiration

**Behavior:** Never expires (safe default)

```python
if "expires_at" not in task:
    return False  # No expiration specified = process normally
```

### Edge Case 4: Malformed date in expires_at

**Behavior:** Log error, process task (fail safe)

```python
try:
    expires = datetime.fromisoformat(...)
    return current > expires
except Exception as e:
    logger.error(f"Could not parse expires_at: {e}")
    return False  # Assume not expired
```

---

## COMPLEXITY & EFFORT

**Code implementation:** 2-3 hours
- BotRunner modifications: 1.5 hours
- Command line parsing: 15 minutes
- Helper methods: 30 minutes
- Testing: 30 minutes

**Process updates:** 1 hour
- Update SCRUMMASTER-PROTOCOL
- Create sprint naming guide
- Communicate to team

**Total:** ~3-4 hours

---

## WHAT THIS FIXES

✅ **Task isolation by sprint:** Each bot only processes assigned sprint
✅ **Expired task cleanup:** Old tasks automatically skipped
✅ **Audit trail:** Logs show why task was skipped
✅ **Process compliance:** Enforces sprint discipline
✅ **Velocity tracking:** Accurate sprint metrics

---

## BLOCKERS RESOLVED

**This P0 fix unblocks:**
- TASK-002-014: Timeline API (can queue safely)
- TASK-002-015: WebSocket streaming (can queue safely)
- Any multi-sprint projects (can run without contamination)
- Production deployment (sprint isolation required)

---

## CRITICAL NOTES

**This is blocking because:**
1. Without sprint isolation, task ownership is unclear
2. Bots will process old work by accident
3. Sprint velocity becomes meaningless
4. Violates agile sprint discipline
5. Causes operational confusion

**Must implement before:**
- Starting Phase 2 implementation
- Queueing multi-week projects
- Production deployment

---

## WHAT BOT-002 PROVIDED

✅ **Problem analysis:** Root cause identified
✅ **Solution design:** 3-part architecture
✅ **Implementation spec:** Code changes defined
✅ **Code examples:** Helper methods shown
✅ **Process docs:** SCRUMMASTER-PROTOCOL update
✅ **Testing plan:** Verification scenarios
✅ **Edge cases:** Known issues and solutions

---

## NEXT STEPS FOR Q33N

**Immediate (developer):**
1. Implement sprint filtering in BotRunner
2. Add --sprint argument to CLI
3. Test with provided scenarios
4. Verify logs show correct behavior

**Then (process):**
1. Update SCRUMMASTER-PROTOCOL
2. Create sprint tagging guide
3. Communicate to team
4. Update task templates

**Finally:**
1. Requeue Phase 2 tasks with sprint tags
2. Continue with TASK-002-014, 015

---

## SUMMARY

**Status:** ✅ Complete analysis and specification

**What's done:**
- Problem thoroughly analyzed
- Solution designed
- Implementation specified
- Code examples provided
- Testing plan defined

**What's needed:**
- Developer to implement code changes (~3 hours)
- Process documentation updates (~1 hour)

**Risk:** Low - straightforward filtering logic, no architectural changes

---

