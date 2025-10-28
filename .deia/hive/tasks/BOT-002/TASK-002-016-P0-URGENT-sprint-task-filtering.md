# TASK-002-016: URGENT - Sprint-Aware Task Filtering

**Task ID:** TASK-002-016
**Bot ID:** BOT-002
**Priority:** P0 (BLOCKING - PROCESS ISSUE)
**Created:** 2025-10-28
**Timeout:** 300 seconds
**Status:** CRITICAL - MUST FIX BEFORE NEXT SPRINT

---

## CRITICAL ISSUE

**Problem:** Bots are processing tasks from old/completed sprints

When BOT-002 is given 13 tasks from one sprint, it processes them correctly. But if tasks from a previous sprint are still in the queue, the bot will process those too.

**Example:**
```
Sprint 1 (Oct 20): Queue TASK-100, TASK-101, TASK-102 to BOT-002
(Sprint 1 ends Oct 21)

Sprint 2 (Oct 22): Start new sprint, BOT-002 should only process Sprint 2 tasks
Problem: BOT-002 still has TASK-100 in file queue and will process it!
Result: Sprint 2 contaminated with Sprint 1 work
```

**Impact:**
- Unclear task ownership
- Context switching between sprints
- Impossible to measure sprint velocity
- Process violations
- Confusing for operators

---

## SOLUTION OVERVIEW

Implement sprint-aware task filtering so bots ONLY process tasks assigned to their current sprint.

### Part 1: Tag Tasks with Sprint ID

**When queuing a task, include:**
```markdown
# TASK-002-014: Unified Timeline API

**Sprint:** SPRINT-2025-10-28
**Expires:** 2025-10-29T23:59:59Z
```

### Part 2: Configure Bot with Sprint Assignment

**When starting bot, specify:**
```bash
python run_single_bot.py BOT-002 --sprint SPRINT-2025-10-28
```

### Part 3: Filter in BotRunner

**BotRunner.check_file_queue() should:**
1. Parse task sprint_id from file
2. Skip if sprint_id != current sprint_id
3. Skip if task expired
4. Archive skipped tasks

---

## IMPLEMENTATION REQUIREMENTS

### 1. Modify Task File Format

**Add to task markdown:**
```markdown
# TASK-002-014: Unified Timeline API

**Task ID:** TASK-002-014
**Bot ID:** BOT-002
**Priority:** P1
**Sprint:** SPRINT-2025-10-28      ← NEW
**Expires:** 2025-10-29T23:59:59Z  ← NEW
**Created:** 2025-10-28
**Timeout:** 300 seconds

## INSTRUCTION

[task content]
```

### 2. Update BotRunner.__init__

Add sprint parameter:
```python
def __init__(self,
    bot_id,
    # ... existing params ...
    sprint_id=None,           # NEW
    season=None,              # NEW (alternative to sprint_id)
    ):
    self.bot_id = bot_id
    self.sprint_id = sprint_id  # NEW
    self.season = season        # NEW
```

### 3. Update run_single_bot.py

Add command-line argument:
```python
parser.add_argument('--sprint', type=str, default=None,
                   help='Sprint ID for task filtering (e.g., SPRINT-2025-10-28)')

args = parser.parse_args()

runner = BotRunner(
    bot_id=args.bot_id,
    sprint_id=args.sprint,  # NEW
    # ... other params
)
```

### 4. Update check_file_queue()

Filter by sprint:
```python
def check_file_queue(self):
    """Get next task from CURRENT SPRINT ONLY"""
    task_dir = Path(self.task_queue_dir)
    task_files = sorted(task_dir.glob("TASK-*.md"))

    for task_file in task_files:
        task = self._parse_task_file(task_file)

        # NEW: Skip if wrong sprint
        if self.sprint_id:
            task_sprint = task.get("sprint_id")
            if task_sprint != self.sprint_id:
                logger.debug(f"Skipping {task['task_id']} - "
                           f"belongs to {task_sprint}, not {self.sprint_id}")
                continue

        # NEW: Skip if expired
        if self._is_task_expired(task):
            logger.info(f"Skipping {task['task_id']} - expired")
            continue

        # Process this task
        if task_file.name not in self.processed_tasks:
            return task

    return None
```

### 5. Add Helper Methods

```python
def _is_task_expired(self, task):
    """Check if task has expired"""
    if "expires_at" not in task:
        return False  # No expiration = never expires

    try:
        expires = datetime.fromisoformat(task["expires_at"].replace('Z', '+00:00'))
        return datetime.utcnow(tzinfo=timezone.utc) > expires
    except:
        return False

def _parse_task_file(self, file_path):
    """Parse task markdown and extract fields"""
    with open(file_path) as f:
        content = f.read()

    # Extract sprint_id from:
    # **Sprint:** SPRINT-2025-10-28
    sprint_match = re.search(r'\*\*Sprint:\*\*\s+(\S+)', content)
    sprint_id = sprint_match.group(1) if sprint_match else None

    # Extract expires_at from:
    # **Expires:** 2025-10-29T23:59:59Z
    expires_match = re.search(r'\*\*Expires:\*\*\s+(\S+)', content)
    expires_at = expires_match.group(1) if expires_match else None

    return {
        "task_id": self._extract_task_id(content),
        "sprint_id": sprint_id,
        "expires_at": expires_at,
        # ... other fields
    }
```

---

## PROCESS UPDATE NEEDED

**Update SCRUMMASTER-PROTOCOL:**

Add new section: "Sprint-Aware Task Queueing"

```markdown
### Sprint-Aware Task Queueing

Before queuing a task, ensure:
1. Current sprint ID is known
2. Task includes Sprint tag with current sprint_id
3. Task includes Expires tag with sprint end date

Example:

cat > .deia/hive/tasks/BOT-002/TASK-002-014-P1-timeline-api.md << 'EOF'
# TASK-002-014: Unified Timeline API

**Sprint:** SPRINT-2025-10-28
**Expires:** 2025-10-29T23:59:59Z

[task content]
EOF

Bots will skip any tasks not matching their current sprint.
```

---

## ACCEPTANCE CRITERIA

✅ **Task Tagging:**
- [ ] New tasks include Sprint field
- [ ] New tasks include Expires field
- [ ] Sprint format: SPRINT-YYYY-MM-DD
- [ ] Expires format: ISO 8601

✅ **Bot Configuration:**
- [ ] BotRunner accepts --sprint parameter
- [ ] run_single_bot.py passes sprint to BotRunner
- [ ] sprint_id stored in bot configuration

✅ **Filtering Logic:**
- [ ] Tasks without matching sprint_id are skipped
- [ ] Expired tasks are skipped
- [ ] Logging shows why task was skipped
- [ ] Matching tasks still processed

✅ **Testing:**
- [ ] Queue task with different sprint_id
- [ ] Verify bot skips it
- [ ] Verify bot log shows "wrong sprint"
- [ ] Queue correct sprint task
- [ ] Verify bot processes it

---

## TEST SCENARIO

**Setup:**
```bash
# Create old sprint task (should be skipped)
cat > .deia/hive/tasks/BOT-002/TASK-999-old-sprint.md << 'EOF'
# TASK-999: Old Task from Last Sprint

**Sprint:** SPRINT-2025-10-27
**Expires:** 2025-10-28T00:00:00Z

Do something
EOF

# Create current sprint task (should be processed)
cat > .deia/hive/tasks/BOT-002/TASK-014-new-sprint.md << 'EOF'
# TASK-014: New Task from This Sprint

**Sprint:** SPRINT-2025-10-28
**Expires:** 2025-10-29T23:59:59Z

Do something else
EOF
```

**Run bot:**
```bash
python run_single_bot.py BOT-002 --sprint SPRINT-2025-10-28
```

**Expected:**
```
BOT-002 activity log should show:
- Skipping TASK-999 - belongs to SPRINT-2025-10-27, not SPRINT-2025-10-28
- Processing TASK-014 - matches current sprint SPRINT-2025-10-28
```

---

## IMPLEMENTATION EFFORT

**Code changes:** 2-3 hours
- BotRunner modifications: 1 hour
- run_single_bot.py: 30 minutes
- Helper methods: 1 hour
- Testing: 30 minutes

**Process updates:** 30 minutes
- Update SCRUMMASTER-PROTOCOL
- Create sprint naming convention doc
- Communicate to team

**Total:** ~3-4 hours

---

## DEPENDENCIES & BLOCKERS

**Blocks:**
- TASK-002-014/015/016 cannot be safely queued until this is fixed
- Any multi-sprint project
- Accurate velocity tracking

**No code dependencies** - Can be implemented independently

---

## WHY THIS IS P0

This is **blocking** because:
1. Without sprint isolation, task ownership is unclear
2. Bots will process old work by accident
3. Impossible to measure sprint velocity
4. Violates sprint discipline
5. Causes confusion and operational errors

**Must fix before:**
- Queuing Phase 2 tasks
- Starting any new sprint
- Running bots in production

---

## NOTES FOR BOT-002

This task requires:
- ✅ Analyzing requirements (done in this document)
- ✅ Specifying solution (done here)
- ⏳ Providing code examples for developer
- ⏳ Documenting edge cases
- ⏳ Creating test procedures

**You should:**
1. Read this specification
2. Provide detailed code examples
3. Identify any missing edge cases
4. Suggest improvements to filtering logic
5. Specify test procedures

**Developer will:**
1. Implement code changes
2. Test with provided scenarios
3. Verify logs show correct behavior

---

## RELATED DOCUMENTS

- Q33N-CRITICAL-NOTE-TASK-LIFECYCLE-MANAGEMENT.md (full analysis)
- SCRUMMASTER-PROTOCOL.md (will be updated)
- .deia/config/SPRINT-*.json (sprint configuration)

---

**Status:** URGENT - Analyze and provide specifications
**Assigned to:** BOT-002
**Priority:** P0 (BLOCKING)