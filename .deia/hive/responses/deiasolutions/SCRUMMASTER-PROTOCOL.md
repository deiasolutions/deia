# SCRUMMASTER PROTOCOL

**Role:** ScrumMaster (Orchestrator/Q33N)
**Purpose:** Manage bot operations, coordinate tasks, ensure system health
**Date:** 2025-10-28
**Status:** ACTIVE

---

## CORE RESPONSIBILITIES

### As ScrumMaster, You Are Responsible For:

1. **Bot Health** - Monitor all bots, ensure they stay alive
2. **Task Queue** - Create, prioritize, and queue tasks
3. **Response Monitoring** - Track task completion, read responses
4. **Error Resolution** - Handle failures, escalate when needed
5. **Communication** - Clear messaging to bots and stakeholders
6. **Decision Authority** - Decide priorities, pause/resume, allocate resources

---

## SECTION 1: BOT STATUS MONITORING

### How to Check Bot Health

#### Quick Status Check
```bash
# Check task queue (tasks waiting)
ls -la .deia/hive/tasks/BOT-XXX/ | grep -v LAUNCH

# Check responses (completed tasks)
ls -la .deia/hive/responses/ | grep TASK-

# Check activity log (what bot has done)
tail -50 .deia/bot-logs/BOT-XXX-activity.jsonl

# Check error log (any problems)
tail -20 .deia/bot-logs/BOT-XXX-errors.jsonl
```

#### Detailed Status Check
```bash
# Count pending tasks in queue
ls .deia/hive/tasks/BOT-XXX/*.md | wc -l

# Count completed responses
ls .deia/hive/responses/TASK-* | wc -l

# Check for recent errors
grep '"error"' .deia/bot-logs/BOT-XXX-errors.jsonl | tail -10

# Check bot subprocess status
ps aux | grep claude  # or grep the bot process
```

#### Status Indicators

| Indicator | Healthy | Warning | Critical |
|-----------|---------|---------|----------|
| Task queue | 0-5 tasks | 6-20 tasks | 20+ tasks |
| Response time | <60s | 60-300s | >300s timeout |
| Error rate | 0% | <5% | >5% |
| Activity log | Recent entries | Stale (>5m) | No entries |

### Interpretation Guide

**Healthy Bot:**
- Active task queue monitored
- Responses written within timeout
- Error log empty or minimal
- Activity log recent

**Degraded Bot:**
- Task queue growing
- Responses delayed but present
- Minor errors in error log
- Activity log present but stale

**Failed Bot:**
- Task queue growing, responses not written
- Tasks timing out
- Multiple errors in error log
- Activity log has no recent entries

---

## SECTION 2: TASK QUEUEING

### How to Create Tasks

#### Task File Format (Mode 1 - CLI-Only)
```markdown
# TASK-BOT-XXX-NNN: Brief Description

**Task ID:** TASK-BOT-XXX-NNN
**Bot ID:** BOT-XXX
**Priority:** [P0|P1|P2]
**Created:** 2025-10-28T14:00:00Z
**Timeout:** [seconds - typically 60-300]

---

## INSTRUCTION

Your actual instruction to the bot goes here.

Be specific and actionable.

---
```

#### Naming Convention
```
.deia/hive/tasks/BOT-XXX/TASK-BOT-XXX-NNN-Priority-Description.md

Examples:
- TASK-BOT-002-001-P1-verify-config.md
- TASK-BOT-002-002-P0-emergency-rollback.md
- TASK-BOT-003-010-P2-documentation-update.md
```

#### Priority Levels

| Priority | Use Case | Timeout | Response Time SLA |
|----------|----------|---------|-------------------|
| P0 | Emergency/critical | 60s | Immediate |
| P1 | Important | 120s | <5 min |
| P2 | Normal | 300s | <15 min |

### How to Queue a Task

1. **Create task file:**
   ```bash
   cat > .deia/hive/tasks/BOT-002/TASK-BOT-002-NNN-P1-description.md << 'EOF'
   # TASK-BOT-002-NNN: Description
   ...
   EOF
   ```

2. **Verify file created:**
   ```bash
   ls .deia/hive/tasks/BOT-002/TASK-BOT-002-NNN*.md
   ```

3. **Bot will process** - Bot monitoring system polls every 5 seconds

4. **Track completion** - Watch for response file

### Task Ordering

Tasks are processed by bot in this order:
1. **Priority** - P0 > P1 > P2
2. **Timestamp** - Within same priority, FIFO (first created, first processed)
3. **Exclusion** - Already-processed tasks are skipped

### Best Practices for Task Creation

- ✅ Be specific and clear
- ✅ Include acceptance criteria (how to know it's done)
- ✅ Set appropriate timeout for complexity
- ✅ Use correct priority level
- ✅ One task = one responsibility
- ❌ Don't overload with multiple requests
- ❌ Don't set unrealistic timeouts
- ❌ Don't mix concerns in one task

---

## SECTION 3: RESPONSE READING

### How to Monitor Task Completion

#### Watch for Response File
```bash
# Monitor for specific task response
watch -n 5 'ls .deia/hive/responses/ | grep TASK-BOT-002-001'

# Check if response exists
test -f .deia/hive/responses/TASK-BOT-002-001-*-response.md && echo "COMPLETE"
```

#### Read Response Content
```bash
# Find and read response (most recent)
cat $(ls -t .deia/hive/responses/TASK-BOT-002-001*.md | head -1)

# Read all responses for a task
grep "Task ID.*TASK-BOT-002-001" .deia/hive/responses/*.md
```

#### Response Format
Response files contain:
- Task ID and Bot ID
- Success status (true/false)
- Response content (findings, output)
- Files modified (list)
- Errors (if any)
- Completion timestamp
- Duration in seconds

#### Response Status
```markdown
# Response includes:
- Status: COMPLETE/FAILED
- Summary: What was done
- Findings: What was discovered
- Recommendations: Next actions (if any)
- Error info: If something went wrong
```

### Response File Locations
```
.deia/hive/responses/TASK-BOT-XXX-NNN-description-response.md
```

---

## SECTION 4: ERROR HANDLING

### When Task Fails

#### Step 1: Check Error Log
```bash
# View recent errors
tail -20 .deia/bot-logs/BOT-XXX-errors.jsonl

# Search for specific error
grep "TASK-BOT-002-001" .deia/bot-logs/BOT-XXX-errors.jsonl
```

#### Step 2: Read Task Response
```bash
# Read response file for error details
cat .deia/hive/responses/TASK-BOT-002-001-*-response.md
```

#### Step 3: Classify Error

| Error Type | Symptom | Recovery |
|-----------|---------|----------|
| Timeout | Response file never appears | Increase timeout, requeue |
| Execution | Response file says "success: false" | Review error details, requeue |
| Resource | Subprocess crashes | Check logs, restart bot |
| Input | Bot can't understand task | Clarify task, requeue |

#### Step 4: Recovery Action

**For Timeout:**
1. Increase timeout in requeued task
2. Check if bot is stuck
3. If stuck >10 min, restart bot

**For Execution Error:**
1. Read error details in response file
2. Modify task based on feedback
3. Requeue task with same or higher priority

**For Resource Issue:**
1. Check bot process: `ps aux | grep claude`
2. Check logs: `.deia/bot-logs/BOT-XXX-errors.jsonl`
3. Restart bot if crashed

**For Input Issue:**
1. Reread task specification
2. Clarify instruction
3. Provide example if helpful
4. Requeue with updated instruction

### Error Prevention

- ✅ Test tasks on non-critical work first
- ✅ Use realistic timeouts
- ✅ Monitor bot health regularly
- ✅ Keep error logs rotated (archive old logs)
- ✅ Document patterns (if same error repeats, it's a design issue)

---

## SECTION 5: MODE OPERATIONS

### CLI-Only Mode (BOT-002)

**How it works:**
1. You create task files
2. Bot polls queue every 5 seconds
3. Bot processes task
4. Bot writes response file
5. You read response file

**Your responsibilities:**
- Create clear task files
- Monitor task queue
- Read responses
- Create new tasks when needed

**Advantages:**
- Offline-friendly (works even if you disconnect)
- Persistent (responses saved for audit)
- Simple (no real-time connection needed)

**Limitations:**
- Asynchronous (not real-time)
- Polling delay (up to 5 seconds)
- No interactive feedback

### Hybrid Mode (When Available)

**How it works:**
1. Bot listens to BOTH file queue AND WebSocket
2. WebSocket messages get priority
3. File queue processed when no WebSocket task
4. Both methods feed into unified timeline

**Your responsibilities:**
- Queue async tasks (file system)
- Send interactive prompts (WebSocket/chat)
- Monitor unified timeline
- Pause/resume as needed

### Commander-Only Mode (When Available)

**How it works:**
1. You chat with bot via Commandeer UI
2. All communication via WebSocket
3. No file queue
4. Real-time only

**Your responsibilities:**
- Type prompts in chat
- Read responses in real-time
- Handle response directly

---

## SECTION 6: SCRUMMASTER RESPONSIBILITIES

### Daily Duties

**Morning Check:**
- [ ] Verify all bots are alive
- [ ] Review error logs from overnight
- [ ] Check task queue status
- [ ] Plan day's tasks

**During Day:**
- [ ] Monitor task completion
- [ ] Queue new tasks as needed
- [ ] Respond to task failures
- [ ] Keep stakeholders informed

**Evening/Cleanup:**
- [ ] Archive completed responses
- [ ] Rotate error logs
- [ ] Verify no tasks pending unexpectedly
- [ ] Plan next day's work

### Decision Authority

As ScrumMaster, you have authority to:

**Pause/Stop:**
- Pause: Create `.deia/hive/controls/BOT-XXX-PAUSE` file
- Stop: Create `.deia/hive/controls/BOT-XXX-STOP` file
- Resume: Delete pause/stop file

**Reprioritize:**
- Delete low-priority tasks if urgent work comes up
- Requeue with higher priority if needed

**Escalate:**
- If bot repeatedly fails → investigate root cause
- If queue grows uncontrollably → consider second bot
- If errors are critical → escalate to engineer

**Resource Allocation:**
- Assign tasks based on bot capacity
- Balance workload across bots
- Queue tasks efficiently

### Decision Criteria

**When to pause a bot:**
- If it's producing errors affecting other systems
- If you need to update bot or system
- If resource consumption is too high

**When to escalate:**
- If same error repeats 3+ times
- If bot unresponsive for >10 minutes
- If task fails with security/data integrity issue
- If queue exceeds 50 pending tasks

**When to require code review:**
- Bot produces unexpected output
- Error pattern indicates design issue
- Bot behavior contradicts specification

---

## SECTION 7: COMMUNICATION TEMPLATES

### Task Template: Investigation/Audit

```markdown
# TASK-BOT-XXX-NNN: Audit [System/Component]

**Priority:** P1

---

## INSTRUCTION

Review [system/component] and report:
1. Current status
2. Any issues found
3. Recommendations

Keep response concise.
```

### Task Template: Code Changes

```markdown
# TASK-BOT-XXX-NNN: [Change Type] - [Component]

**Priority:** P1

---

## INSTRUCTION

[Change type] [component] to [achieve goal].

Current behavior: [describe what it does now]
Desired behavior: [describe what you want]
Acceptance criteria:
- [ ] Criterion 1
- [ ] Criterion 2

Include implementation details if helpful.
```

### Task Template: Documentation

```markdown
# TASK-BOT-XXX-NNN: Document [Feature/System]

**Priority:** P2

---

## INSTRUCTION

Create/update documentation for [feature/system].

Include:
- Overview
- How to use
- Common patterns
- Troubleshooting

Location: [where to save doc]
Format: [Markdown/other]
```

### Task Template: Emergency/P0

```markdown
# TASK-BOT-XXX-NNN: URGENT - [Issue]

**Priority:** P0

---

## INSTRUCTION

[Immediate action required]

Current impact: [what's broken]
Required fix: [what needs to happen]
Timeline: [when it's needed]

Do this NOW, report status immediately.
```

---

## SECTION 8: ESCALATION PROCEDURES

### Escalation Path

1. **Level 1 (You/ScrumMaster):**
   - Monitor bots
   - Handle routine task failures
   - Requeue failed tasks
   - Rotate logs

2. **Level 2 (Engineer):**
   - Investigate repeated errors
   - Review bot behavior
   - Modify tasks/procedures
   - Consider design changes

3. **Level 3 (Architect):**
   - System-level issues
   - Infrastructure changes
   - New bot deployment
   - Mode switching

### When to Escalate to Engineer

**Immediate escalation if:**
- Bot crashes (exit code != 0)
- Data corruption detected
- Security issue suspected
- Same error 3+ times without fix

**Escalation before requeue if:**
- Task timeout exceeded
- Resource exhaustion (CPU, memory)
- Subprocess communication failure
- File system errors

### Pause/Stop Procedures

#### To Pause a Bot (Temporarily Stop Processing)
```bash
# Create pause file
touch .deia/hive/controls/BOT-002-PAUSE

# Bot will finish current task then pause
# Check status: task queue will accumulate
# To resume: remove pause file
rm .deia/hive/controls/BOT-002-PAUSE
```

#### To Stop a Bot (Emergency Stop)
```bash
# Create stop file
touch .deia/hive/controls/BOT-002-STOP

# Bot will halt immediately
# Check status: monitor logs
# To restart: remove stop file, bot restarts fresh
rm .deia/hive/controls/BOT-002-STOP
```

### Communication When Escalating

```markdown
**Escalation Report:**
- **Issue:** [What went wrong]
- **When:** [When it happened]
- **Bot:** [Which bot]
- **Task:** [TASK-ID]
- **Impact:** [What's affected]
- **Attempted Fix:** [What you tried]
- **Next Action:** [What engineer should do]
- **Urgency:** [P0/P1/P2]
```

---

## OPERATIONAL CHECKLIST

### Daily Morning
- [ ] Check `.deia/bot-logs/BOT-XXX-errors.jsonl` for overnight issues
- [ ] Verify task queue is manageable
- [ ] Check all bots are alive
- [ ] Review any pending responses

### Before Queuing Tasks
- [ ] Task file properly formatted
- [ ] Priority level appropriate
- [ ] Timeout realistic for task complexity
- [ ] Bot has capacity (queue <20 tasks)
- [ ] Clear acceptance criteria included

### After Bot Task Completes
- [ ] Response file created successfully
- [ ] Read response and verify completion
- [ ] Check for errors in response
- [ ] Archive response or mark for next step
- [ ] Queue any follow-up tasks

### Weekly
- [ ] Archive old response files (>7 days)
- [ ] Rotate and compress error logs
- [ ] Review task patterns and efficiency
- [ ] Plan upcoming work
- [ ] Document any recurring issues

---

## QUICK REFERENCE

### Key Directories
```
Tasks:        .deia/hive/tasks/BOT-XXX/
Responses:    .deia/hive/responses/
Activity:     .deia/bot-logs/BOT-XXX-activity.jsonl
Errors:       .deia/bot-logs/BOT-XXX-errors.jsonl
Controls:     .deia/hive/controls/
```

### Common Commands
```bash
# Check bot status
tail -10 .deia/bot-logs/BOT-002-activity.jsonl

# Queue task
cat > .deia/hive/tasks/BOT-002/TASK-XXX.md << 'EOF'
...
EOF

# Read response
cat $(ls -t .deia/hive/responses/TASK-*.md | head -1)

# Pause bot
touch .deia/hive/controls/BOT-002-PAUSE

# Check errors
grep error .deia/bot-logs/BOT-002-errors.jsonl
```

---

## SUMMARY

As ScrumMaster, you are responsible for:
1. **Monitoring** - Keep tabs on bot health
2. **Tasking** - Queue work efficiently
3. **Tracking** - Monitor completion
4. **Troubleshooting** - Handle failures
5. **Escalating** - Know when to get help

You have the authority to pause, stop, reprioritize, and escalate as needed.

Keep communication clear, decisions documented, and always know your bot's status.

---

