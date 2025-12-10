# DIRECTIVE: Auto-Logging ON - All Agents
**From:** Q33N (BEE-000 Meta-Governance)
**To:** ALL AGENTS (BOT-001, BOT-003, future CODEX)
**Date:** 2025-10-25 19:45 CDT
**Priority:** P0 - MANDATORY
**Mode:** Operational Directive

---

## ⚠️ AUTO-LOGGING ENFORCEMENT

**EFFECTIVE IMMEDIATELY:** All agents must document work in real-time. Auto-logging is ON.

---

## Documentation Requirements

### For Every Agent Every Session

**Daily Status File (Required every 4 hours minimum):**
```
.deia/hive/responses/deiasolutions/bot-{ID}-{fire-drill|sprint-2}-status.md
```

**Content:**
- Time period covered
- Tasks completed (with ✅)
- Tasks in progress (with ETA)
- Blockers (if any)
- Questions (if any)
- Next steps
- Evidence (code links, file paths)

**Format Example:**
```markdown
# BOT-001 Fire Drill Status - Hour 0-2

**Time:** 19:00 - 21:00 CDT
**Date:** 2025-10-25

## Completed ✅
- [x] Fixed run_single_bot.py subprocess spawning
- [x] Implemented bot HTTP service endpoints

## In Progress 🟡
- [ ] Task queue monitoring (ETA 20:30)
- [ ] Service registry integration (ETA 21:15)

## Blockers 🚫
- None

## Questions ❓
- None yet

## Evidence
- Code: `src/deia/adapters/bot_http_service.py`
- Tests: `tests/unit/test_bot_http_service.py`
- Logs: `.deia/bot-logs/BOT-001-activity.jsonl`

## Tomorrow
- Task 3: Task queue monitoring
- Task 4: Registry integration
- Task 5: Test bots
```

---

## Session Logging

**Automatic session logs created at:**
```
.deia/sessions/2025-10-25-{task-name}-{bot-id}.md
```

**Each agent appends to their session log:**
- Every 30 minutes during active work
- Every time a task completes
- Every time a blocker occurs
- At end of session

**Session Log Sections:**
1. Task assignments received
2. Work completed (with timestamps)
3. Blockers encountered (with time spent)
4. Decisions made
5. Code created/modified
6. Tests run (pass/fail)
7. Time spent per task
8. Handoff notes for next agent

---

## Auto-Logging Checklist

**Before Starting Work:**
- [ ] Read your task assignment file
- [ ] Create/open session log file
- [ ] Update status file with "work starting"
- [ ] Note start time

**Every 30 minutes:**
- [ ] Update session log with progress
- [ ] Check if blockers need escalation
- [ ] Update status file

**When Task Completes:**
- [ ] Log completion time
- [ ] Create evidence (code files, test results)
- [ ] Update status file with ✅
- [ ] Link to deliverables

**When Blocker Occurs:**
- [ ] Log blocker immediately to session
- [ ] Create question file (`.deia/hive/responses/deiasolutions/bot-{ID}-questions.md`)
- [ ] Update status with 🚫 blocker
- [ ] Wait for Q33N response (< 30 min)

**At End of Session:**
- [ ] Final status file update
- [ ] Session log summary
- [ ] Handoff notes for next work
- [ ] Time tracking complete

---

## Tools for Documentation

**1. Task Assignment Files** (Read-Only)
```
.deia/hive/tasks/2025-10-25-{time}-000-{BOT-ID}-{TASK-NAME}.md
```

**2. Status Files** (Update every 4 hours)
```
.deia/hive/responses/deiasolutions/bot-{ID}-{phase}-status.md
```

**3. Question Files** (Create when blocked)
```
.deia/hive/responses/deiasolutions/bot-{ID}-{phase}-questions.md
```

**4. Session Logs** (Append continuously)
```
.deia/sessions/2025-10-25-{task-name}-{bot-id}.md
```

**5. Completion Reports** (Final summary)
```
.deia/hive/responses/deiasolutions/bot-{ID}-{phase}-complete.md
```

---

## Logging Format Standards

**ALL Markdown files must follow:**

**Header:**
```markdown
# [Type]: [Description]
**From:** [BOT-ID]
**Date:** [YYYY-MM-DD HH:MM CDT]
**Status:** [ACTIVE|BLOCKED|COMPLETE]
```

**Body:**
- Clear sections with ### headers
- ✅ Checkmarks for completed items
- 🟡 Yellow circles for in-progress
- 🚫 Blocked items clearly marked
- 📝 Evidence with links to files

**Timestamps:**
- Every major action logged with time
- Format: `[HH:MM CDT]`
- Example: `[19:45 CDT] Fixed subprocess spawning`

**No Unicode:** ASCII only (no emojis in code output)

---

## Why This Matters

**Documentation is your accountability mechanism:**
- Q33N monitors progress via these files
- Other agents see your work in real-time
- Dave can audit at any point
- Pattern extraction uses session logs for BOK

**Fire drill success depends on:**
- Clear visibility into progress
- Quick blocker escalation
- Accurate time tracking
- Evidence of what was built

---

## Auto-Logging Enforcement

**Every 4 hours (Max):**
Q33N checks:
```
.deia/hive/responses/deiasolutions/bot-{ID}-*-status.md
```

**If no update in 4 hours:**
- Q33N escalates to Dave
- Assumes bot blocked or stuck
- Reassigns work if needed

**If blocker file exists:**
- Q33N responds within 30 minutes
- Unblocks or gets Dave decision
- Never ignored

---

## For BOT-001 (Fire Drill)

**Status file:** `.deia/hive/responses/deiasolutions/bot-001-fire-drill-status.md`
**Update:** Every 2 hours minimum
**Session log:** `2025-10-25-Fire-Drill-Launch-BOT-001.md`

---

## For BOT-003 (Fire Drill)

**Status file:** `.deia/hive/responses/deiasolutions/bot-003-fire-drill-status.md`
**Update:** Every 2 hours minimum
**Session log:** `2025-10-25-Fire-Drill-Launch-BOT-003.md`

---

## For CODEX (Sprint 2 - When Available)

**Status file:** `.deia/hive/responses/deiasolutions/codex-sprint-2-status.md`
**Update:** Every 2 hours minimum
**Session log:** `2025-10-25-Code-Review-QA-CODEX.md`

---

## Q33N Autolog Status

**Q33N is logging everything:**
- `.deia/sessions/2025-10-25-Q33N-Fire-Drill-Launch.md` (main session)
- `.deia/reports/Q33N-FIRE-DRILL-HOUR-N.md` (hourly summaries)
- Monitoring all bot status files
- Escalating blockers immediately

---

## What Auto-Logging Means

✅ **Every action is documented**
✅ **Every blocker is visible**
✅ **Every decision is recorded**
✅ **Every deliverable is tracked**
✅ **Every timestamp is logged**

**Result:** Full audit trail, pattern extraction, accountability, transparency.

---

## Enforcement

**Non-compliance = Work paused**
- No status update in 4 hours → Assume blocker → Escalate
- No session log → Unclear what you did → Can't trust deliverables
- Questions not posted → Can't help you → You're stuck

**This is not optional. This is required.**

---

**Q33N DIRECTIVE: AUTO-LOGGING ON. DOCUMENT EVERYTHING. GO.**

---

**Authority:** BEE-000 (Q33N Meta-Governance)
**Effective:** 2025-10-25 19:45 CDT
**Scope:** All agents, all work, all sessions
**Enforcement:** Mandatory - work pauses if not logged
