# CRITICAL NOTE: Task Lifecycle & Sprint Isolation

**Date:** 2025-10-28
**Issue:** Old queued tasks being picked up by bots from previous sprints
**Severity:** HIGH
**Status:** REQUIRES PROCESS CHANGE

---

## THE PROBLEM

**Current Issue:**
When tasks are queued to BOT-002 (or any bot), there's no mechanism to prevent the bot from processing:
1. Tasks from old/completed sprints
2. Stale tasks that should have been expired
3. Tasks from cancelled work
4. Tasks that were meant for previous seasons

**Example Scenario:**
```
Sprint 1 (Oct 20):  Queue TASK-001-100 to BOT-002 (incomplete at sprint end)
Sprint 2 (Oct 27):  BOT-002 still processes TASK-001-100 from Sprint 1
                    Should only process Sprint 2 tasks!
Sprint 3 (Oct 28):  Still picking up old work from Sprint 1 & 2
```

**Impact:**
- Bot resources wasted on old work
- Context switching between old/new sprints
- Unclear which sprint owns which task
- Difficult to track sprint velocity
- Process violations

---

## ROOT CAUSE

**Missing Components:**

1. **Sprint/Season Tags on Tasks**
   - Tasks don't include sprint_id or season
   - No way to know which work period they belong to
   - Bot has no way to filter

2. **Task Lifecycle Policy**
   - No expiration mechanism
   - No "archive old tasks" process
   - Old tasks pile up indefinitely
   - Sorting doesn't account for sprint

3. **Bot Configuration**
   - BotRunner doesn't know which sprint to process
   - File queue has no filtering
   - No context about current season

4. **Queueing Discipline**
   - No validation that tasks belong to current sprint
   - No cleanup of old sprint tasks
   - No sprint-aware task sorting

---

## PROPOSED SOLUTION

### 1. Task Tagging with Sprint/Season

**Update task file format:**

```markdown
# TASK-002-011: Bot HTTP Server

**Task ID:** TASK-002-011
**Bot ID:** BOT-002
**Priority:** P1
**Sprint:** SPRINT-2025-10-28  // NEW
**Season:** 2025-Q4-W44         // NEW
**Created:** 2025-10-28
**Expires:** 2025-10-29T23:59:59Z  // NEW
```

**Or in JSON:**
```json
{
  "task_id": "TASK-002-011",
  "bot_id": "BOT-002",
  "priority": "P1",
  "sprint_id": "SPRINT-2025-10-28",  // NEW
  "season": "2025-Q4-W44",           // NEW
  "created_at": "2025-10-28T14:00:00Z",
  "expires_at": "2025-10-29T23:59:59Z"  // NEW
}
```

---

### 2. Bot Configuration with Sprint Assignment

**Update BotRunner initialization:**

```python
runner = BotRunner(
    bot_id="BOT-002",
    sprint_id="SPRINT-2025-10-28",  # NEW: Only process this sprint
    season="2025-Q4-W44",           # NEW: Or use season
    # ... other params
)
```

**Add to run_single_bot.py:**
```bash
python run_single_bot.py BOT-002 --sprint SPRINT-2025-10-28
# or
python run_single_bot.py BOT-002 --season 2025-Q4-W44
```

---

### 3. Bot Task Filtering

**In BotRunner.check_file_queue():**

```python
def check_file_queue(self):
    """Get next task from current sprint only"""
    task_dir = Path(self.task_queue_dir)
    task_files = sorted(task_dir.glob("TASK-*.md"))

    for task_file in task_files:
        task = self._parse_task_file(task_file)

        # NEW: Skip if not for current sprint
        if task.get("sprint_id") != self.sprint_id:
            logger.debug(f"Skipping task {task['task_id']} - wrong sprint")
            continue

        # NEW: Skip if expired
        if self._is_task_expired(task):
            logger.info(f"Task {task['task_id']} expired, archiving")
            self._archive_task(task_file)
            continue

        # Process this task
        if task_file.name not in self.processed_tasks:
            return task

    return None
```

---

### 4. Cleanup Process

**Archive old sprint tasks:**

```bash
# At end of sprint:
mv .deia/hive/tasks/BOT-002/TASK-2025-10-27-*.md \
   .deia/hive/archive/SPRINT-2025-10-27/

# Keep completed tasks in responses
# Move OLD, UNPROCESSED tasks to archive
```

**New directory structure:**
```
.deia/hive/
├── tasks/
│   ├── BOT-002/           # Current sprint only
│   │   ├── TASK-002-011-P1-...md
│   │   └── TASK-002-012-P1-...md
│   └── BOT-003/
├── archive/               # OLD tasks
│   ├── SPRINT-2025-10-27/
│   │   ├── TASK-002-050-OLD.md
│   │   └── TASK-003-075-OLD.md
│   └── SPRINT-2025-10-26/
└── responses/             # All completed responses (keep)
```

---

### 5. ScrumMaster Protocol Update

**Add to SCRUMMASTER-PROTOCOL.md:**

**Sprint Task Queueing:**
```
Before creating task file, verify:
- [ ] Current sprint_id known
- [ ] Task tagged with current sprint
- [ ] Expiration date set (usually sprint_end_date)
- [ ] No duplicate task from previous sprint

Command:
cat > .deia/hive/tasks/BOT-002/TASK-002-NNN-P1-description.md << 'EOF'
# TASK-002-NNN: Description

**Sprint:** SPRINT-2025-10-28
**Expires:** 2025-10-29T23:59:59Z

[task content]
EOF
```

---

### 6. Sprint Lifecycle Process

**When sprint starts:**
1. ✅ Define sprint_id (e.g., SPRINT-2025-10-28)
2. ✅ Define end date (e.g., 2025-10-29 23:59:59)
3. ✅ Assign bots to sprint: `python run_single_bot.py BOT-002 --sprint SPRINT-2025-10-28`
4. ✅ Start queueing tasks with sprint tag

**During sprint:**
1. ✅ All tasks tagged with current sprint_id
2. ✅ Bots only process current sprint tasks
3. ✅ Monitor task queue for old tasks (alert if found)

**When sprint ends:**
1. ✅ Stop accepting new tasks for this sprint
2. ✅ Let bots finish any in-progress tasks
3. ✅ Archive unprocessed tasks to .deia/hive/archive/
4. ✅ Start new sprint with fresh queue

---

## IMMEDIATE ACTION ITEMS

### Task 1: Add Sprint Validation to BotRunner
**Priority:** P0 (BLOCKING)
**Effort:** 1-2 hours
**Owner:** Developer

Changes needed:
- Add `sprint_id` parameter to BotRunner.__init__
- Add `_is_same_sprint(task)` check in check_file_queue()
- Add `_is_task_expired(task)` check
- Add logging for skipped tasks

### Task 2: Create Sprint Configuration
**Priority:** P1
**Effort:** 30 minutes
**Owner:** Q33N

Create: `.deia/config/SPRINT-2025-10-28.json`
```json
{
  "sprint_id": "SPRINT-2025-10-28",
  "season": "2025-Q4-W44",
  "start_date": "2025-10-28",
  "end_date": "2025-10-29",
  "bots": ["BOT-002", "BOT-003"],
  "status": "active"
}
```

### Task 3: Update SCRUMMASTER-PROTOCOL
**Priority:** P2
**Effort:** 1 hour
**Owner:** BOT-002

Add section on sprint-aware task queueing with examples

### Task 4: Create Sprint Archive Process
**Priority:** P2
**Effort:** 1 hour
**Owner:** Q33N

Create script to archive old sprint tasks:
```bash
.deia/scripts/archive-sprint.sh
```

---

## BACKLOG ITEM

**Create new task:** `TASK-???-???-P0-sprint-task-filtering`

```markdown
# TASK-???-???: Sprint-Aware Task Filtering

Implement sprint isolation for bot task queues.

Prevent bots from processing tasks from old sprints.
Add sprint_id and expiration to task format.
Filter queue by current sprint.
Archive old sprint tasks.

See: Q33N-CRITICAL-NOTE-TASK-LIFECYCLE-MANAGEMENT.md
```

---

## RECOMMENDED TIMELINE

**Immediate (Next run):**
- Implement sprint validation in BotRunner (blocks current work)

**This sprint:**
- Create sprint configuration files
- Update SCRUMMASTER protocol
- Document sprint lifecycle

**Next sprint:**
- Implement archive process
- Test sprint isolation
- Refine based on experience

---

## NOTES FOR Q33N

This is a **process issue**, not a code issue. The fix requires:

1. **Discipline:** Always tag tasks with sprint_id
2. **Configuration:** Define sprints with dates
3. **Filtering:** BotRunner checks sprint before processing
4. **Cleanup:** Archive old sprint tasks regularly

Without this, sprint-based work planning is impossible.

---

## RELATED ITEMS

- ScrumMaster Protocol (needs update)
- BotRunner (needs sprint filtering)
- Bot launch config (needs sprint parameter)
- Backlog management (needs sprint isolation)

---

**Created:** 2025-10-28
**Status:** PROPOSAL - PENDING APPROVAL
**Owner:** Q33N
**Next step:** Decide on sprint naming convention + implement

