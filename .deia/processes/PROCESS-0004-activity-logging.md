# PROCESS-0004 — Activity Logging (Mandatory Per-Bee Responsibility)

**Status:** OFFICIAL
**Version:** 1.0
**Date:** 2025-11-26
**Owner:** Q33N Authority

---

## Rule

**Every bee logs their own activity. This is not automated. This is YOUR responsibility.**

The term "activity logging" (not "auto-logging") means: YOU, the bee, must write log entries to your activity log file at regular intervals. No system does this for you. No Claude feature does this for you. YOU do it.

**Core Principle:** If you're working, you're logging. No logging = no proof of work = violation.

---

## Why This Matters

1. **Visibility** - Q33N and humans can see what you're doing without interrupting you
2. **Continuity** - If your session crashes, the next bee can pick up where you left off
3. **Accountability** - Proves you were working, not idle
4. **Debugging** - When something breaks, logs show what happened
5. **LLM-Agnostic** - Works for Claude, Codex, GPT, Llama, any vendor

**This is NOT a Claude feature. This is a DEIA process that works across all LLM vendors.**

---

## When to Log

| Trigger | Action |
|---------|--------|
| **Start of session** | Log: "Session started, checking for tasks" |
| **Every 15-30 minutes** | Log: Current status, what you're working on |
| **Task started** | Log: "Starting task: [task name]" |
| **Task completed** | Log: "Completed task: [task name]" |
| **Blocked** | Log: "BLOCKED: [reason]" |
| **Waiting** | Log: "Waiting for: [what you're waiting for]" |
| **End of session** | Log: "Session ending, handoff: [state]" |

**Minimum frequency:** Every 30 minutes. If you haven't logged in 30 minutes, you're in violation.

---

## How to Log

### Log File Location

```
.deia/bot-logs/{YOUR-ID}-activity.jsonl
```

Example: `.deia/bot-logs/BEE-002A-activity.jsonl`

### Log Entry Format (JSONL)

Each line is a JSON object:

```json
{"ts": "2025-11-26T14:30:00Z", "bee": "BEE-002A", "event": "task_started", "task": "implement-svg-endpoint", "msg": "Starting SVG counter endpoint implementation"}
{"ts": "2025-11-26T14:45:00Z", "bee": "BEE-002A", "event": "progress", "task": "implement-svg-endpoint", "msg": "Database schema complete, starting API routes"}
{"ts": "2025-11-26T15:00:00Z", "bee": "BEE-002A", "event": "progress", "task": "implement-svg-endpoint", "msg": "API routes 50% complete, testing locally"}
{"ts": "2025-11-26T15:15:00Z", "bee": "BEE-002A", "event": "task_completed", "task": "implement-svg-endpoint", "msg": "SVG endpoint complete, tests passing"}
```

### Event Types

| Event | When to Use |
|-------|-------------|
| `session_start` | Beginning of your work session |
| `session_end` | End of your work session |
| `task_started` | You begin working on a task |
| `task_completed` | You finish a task |
| `progress` | Regular status update (every 15-30 min) |
| `blocked` | You cannot proceed |
| `waiting` | You're waiting for something (response, dependency) |
| `question` | You posted a question to Q33N |
| `error` | Something went wrong |

### Quick Log Command (Copy-Paste Ready)

```bash
echo '{"ts": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'", "bee": "YOUR-ID", "event": "progress", "task": "TASK-NAME", "msg": "YOUR MESSAGE"}' >> .deia/bot-logs/YOUR-ID-activity.jsonl
```

Or write directly in your editor - just append a new JSON line.

---

## The 20-Minute Timer Pattern

**When working autonomously, set a mental timer:**

1. **Work for 20 minutes**
2. **Log your progress** (what did you accomplish?)
3. **Check for messages** (any Q33N responses? new tasks?)
4. **Repeat**

This prevents:
- Going dark (no visibility)
- Missing Q33N responses
- Working on stale/cancelled tasks
- Context loss on crash

---

## Violation Consequences

| Violation | Consequence |
|-----------|-------------|
| No log entry for 30+ minutes | Warning from Q33N |
| No log entry for 60+ minutes | Assumed idle/crashed, work may be reassigned |
| Repeated violations | Performance review, possible role reassignment |
| Fabricated logs | Immediate escalation (integrity violation) |

---

## Examples

### Good Log Sequence

```json
{"ts": "2025-11-26T10:00:00Z", "bee": "BEE-002A", "event": "session_start", "msg": "Session started, checking .deia/hive/tasks/ for work"}
{"ts": "2025-11-26T10:02:00Z", "bee": "BEE-002A", "event": "task_started", "task": "svg-counter-db-schema", "msg": "Found task, starting PostgreSQL schema design"}
{"ts": "2025-11-26T10:20:00Z", "bee": "BEE-002A", "event": "progress", "task": "svg-counter-db-schema", "msg": "counters table complete, working on visitors table"}
{"ts": "2025-11-26T10:40:00Z", "bee": "BEE-002A", "event": "progress", "task": "svg-counter-db-schema", "msg": "All tables defined, writing migration script"}
{"ts": "2025-11-26T11:00:00Z", "bee": "BEE-002A", "event": "task_completed", "task": "svg-counter-db-schema", "msg": "Schema complete, migration tested locally, posting response"}
```

### Bad Log Sequence

```json
{"ts": "2025-11-26T10:00:00Z", "bee": "BEE-002A", "event": "session_start", "msg": "Starting"}
{"ts": "2025-11-26T12:30:00Z", "bee": "BEE-002A", "event": "task_completed", "task": "unknown", "msg": "Done"}
```

**What's wrong:** 2.5 hour gap with no visibility. Q33N has no idea what happened.

---

## FAQ

### "But I was focused on coding, I forgot to log"

Set a timer. Logging is part of the work, not extra work. If you can't log while working, you're not following DEIA process.

### "Can't Claude just log automatically?"

No. Claude Code doesn't have a built-in activity logger. Even if it did, DEIA processes must be LLM-agnostic. A Codex bee or GPT bee needs the same process. YOU log. Period.

### "What if I'm waiting and nothing is happening?"

Log that you're waiting: `{"event": "waiting", "msg": "Waiting for Q33N response on blocker question"}`. Then log again in 20-30 minutes: `{"event": "waiting", "msg": "Still waiting, will check again in 20 min"}`.

### "Do I log every single line of code?"

No. Log meaningful progress milestones, not keystrokes. "Finished API routes" not "wrote line 47".

---

## Integration with Other Processes

- **PROCESS-0002:** Task completion requires final log entry before archival
- **Q33N-QUEEN-ONBOARDING:** Q33N monitors logs for bee health
- **BEE-BOOTCAMP:** Logging is Day 1 training requirement

---

## Telemetry & Monitoring

Q33N can run log analysis:

```bash
# See all activity from BEE-002A today
grep "BEE-002A" .deia/bot-logs/BEE-002A-activity.jsonl | tail -20

# Find bees who haven't logged in 30+ minutes
# (Q33N tooling - compare timestamps)
```

---

## Change Log

- **2025-11-26:** Initial process creation, replacing ambiguous "auto-log" terminology

---

## Authority

This is a Q33N-issued mandatory process. Non-compliance will be escalated.

**Q33N DIRECTIVE:** All bees must follow PROCESS-0004 for activity logging. No exceptions. The term "auto-log" is deprecated - use "activity logging" and understand it is YOUR manual responsibility.
