# Agent Communication Cadence v1.1

**Created:** 2025-10-18 1635 CDT
**Updated:** 2025-10-18 2200 CDT (Season/Flight language)
**By:** CLAUDE-CODE-001 (Strategic Coordinator)
**Purpose:** Regular reminders and communications to keep agents aligned
**Status:** ACTIVE - Implement immediately

---

## Problem

Agents need regular reminders about:
- Process protocols (autolog, bug reporting, integration protocol)
- Quality standards
- Communication expectations
- Ongoing responsibilities

**Current:** Ad-hoc reminders, agents forget protocols
**Solution:** Scheduled communications cadence

---

## Communication Types

### 1. Pre-Flight Briefings (Every Flight Start)
**When:** Start of each flight
**To:** ALL_AGENTS
**Purpose:** Remind of flight protocols and current priorities

### 2. Task-Specific Reminders (With Assignment)
**When:** Assigning work
**To:** Individual agent
**Purpose:** Remind of relevant protocols for that task type

### 3. Mid-Season Check-ins
**When:** Season 50% complete
**To:** ALL_AGENTS
**Purpose:** Reinforce quality, check morale, adjust if needed

### 4. Protocol Updates (As Needed)
**When:** New protocol or process change
**To:** ALL_AGENTS or specific agents
**Purpose:** Announce changes, get acknowledgment

### 5. Escalation Alerts (Immediate)
**When:** Issue detected
**To:** Specific agent or ALL_AGENTS
**Purpose:** Correct course immediately

---

## Standard Reminders List

### Core Protocols (Always Active)

**1. Auto-Logging**
```
🔔 REMINDER: Ensure auto-logging is ON
- All code sessions should be logged
- Check: deia status (logging should show active)
- Sessions save to: .deia/sessions/
```

**2. Bug Reporting**
```
🔔 REMINDER: Report all bugs
- Before fixing: Check BUG_REPORTS.md and Bug Fix Lookup Protocol
- After fixing: Document in BUG_REPORTS.md
- Add to PROJECT-STATUS.csv
- Prevent duplicate debugging
```

**3. Integration Protocol**
```
🔔 REMINDER: Complete Integration Protocol on EVERY task
- ✅ Update ACCOMPLISHMENTS.md
- ✅ Update PROJECT-STATUS.csv
- ✅ Update activity log (.deia/bot-logs/CLAUDE-CODE-00X-activity.jsonl)
- ✅ SYNC to coordinator
```

**4. Time Tracking**
```
🔔 REMINDER: Use AI hours, not human hours
- Small tasks: 15-45 min
- Medium tasks: 1-3 hours
- Large tasks: 3-5 hours
- Track actual vs estimated
```

**5. Quality Standards**
```
🔔 REMINDER: Maintain quality standards
- Test coverage: >80% for new code
- Documentation: Every function, clear examples
- Error handling: Graceful degradation
- Security: No secrets, sanitize inputs
```

**6. Check for Next Work**
```
🔔 REMINDER: After completing task
- Check .deia/hive/tasks/ immediately
- If new work → start immediately, note in SYNC
- If no work → send SYNC, stand by
- Goal: <5 min idle time
```

---

## Pre-Flight Briefing Template

**File:** `.deia/hive/tasks/YYYY-MM-DD-0900-001-ALL_AGENTS-BRIEFING-flight-X.md`

```markdown
# Pre-Flight Briefing - Season [X] Flight [Y]

**From:** 001 (Strategic Coordinator)
**To:** ALL AGENTS
**Date:** YYYY-MM-DD 0900 CDT
**Type:** PRE-FLIGHT BRIEFING

---

## Flight Status

**Season:** [Season Name/Number] - [Season Goal]
**Flight:** [X] of ~[Y total flights]
**Status:** [ON TRACK / AHEAD / BEHIND]

---

## Flight Priorities

1. [Current season priority #1]
2. [Current season priority #2]
3. [Current season priority #3]

---

## Protocol Reminders

### ✅ Auto-Logging ON
- Check: `deia status` shows logging active
- Sessions save to: `.deia/sessions/`

### ✅ Bug Fix Lookup First
- Before fixing: Check BUG_REPORTS.md
- 7-location search protocol
- Document new bugs

### ✅ Integration Protocol
- ACCOMPLISHMENTS.md
- PROJECT-STATUS.csv
- Activity log
- SYNC to coordinator

### ✅ AI Hours Estimates
- Small: 15-45 min
- Medium: 1-3 hours
- Large: 3-5 hours
- Reference: `.deia/observations/2025-10-18-ai-planning-lessons-from-activity-logs.md`

### ✅ Check for Next Work
- After every completion
- `.deia/hive/tasks/*-YOUR_ID-*`
- Start immediately if found

---

## Current Agent Assignments

**AGENT-002:** [Current task or READY]
**AGENT-003:** [Tactical Coordinator - Active]
**AGENT-004:** [Current task or READY]
**AGENT-005:** [Current task or READY]

---

## Flight Goals

- [Specific goal 1]
- [Specific goal 2]
- [Specific goal 3]

---

**Good flying. 001 out.**
```

---

## Task-Specific Reminder Templates

### For Documentation Tasks

**Include with assignment:**
```markdown
## Documentation Reminders

- ✅ User-facing language (not technical jargon)
- ✅ Examples for every concept
- ✅ Cross-link to related docs
- ✅ FAQ section if >500 lines
- ✅ Test all code examples
- ✅ Reference time: 1-2 hours for guides (AI hours)
```

### For Code Integration Tasks

**Include with assignment:**
```markdown
## Code Integration Reminders

- ✅ Type hints on all functions
- ✅ Docstrings with examples
- ✅ Test coverage >80%
- ✅ Error handling (graceful degradation)
- ✅ No hardcoded paths/secrets
- ✅ Integration Protocol on completion
- ✅ Reference time: 2-3 hours (AI hours)
```

### For Testing Tasks

**Include with assignment:**
```markdown
## Testing Reminders

- ✅ Test happy path + edge cases
- ✅ Coverage >80% target
- ✅ Test failure modes
- ✅ Mock external dependencies
- ✅ Fast tests (<5 sec total)
- ✅ Clear test names
- ✅ Reference time: 45 min per test suite
```

### For Agent BC Integration

**Include with assignment:**
```markdown
## BC Integration Reminders

- ✅ Review BC code for quality
- ✅ Add missing error handling
- ✅ Enhance tests (BC provides basic, you make comprehensive)
- ✅ Write user-facing docs
- ✅ Integration Protocol
- ✅ Credit BC in ACCOMPLISHMENTS
- ✅ Reference time: 2-3 hours per component
```

---

## Mid-Season Check-in Template

**When:** Season 50% complete
**File:** `.deia/hive/tasks/YYYY-MM-DD-HHMM-001-ALL_AGENTS-CHECKIN-mid-season.md`

```markdown
# Mid-Season Check-in - Season [X] Flight [Y]

**From:** 001 (Strategic Coordinator)
**To:** ALL AGENTS
**Date:** YYYY-MM-DD HHMM CDT
**Type:** MID-SEASON CHECK-IN

---

## Season Progress

**Completed:** [X of Y tasks]
**Flights:** [X of ~Y]
**Status:** [ON TRACK / AHEAD / BEHIND]
**Quality:** [All tests passing / Issues detected]

---

## What's Going Well ✅

- [Positive observation 1]
- [Positive observation 2]
- [Positive observation 3]

---

## What Needs Attention ⚠️

- [Concern 1]
- [Concern 2]
- [Reminder about forgotten protocol]

---

## Protocol Reinforcement

**Remember:**
- ✅ Auto-logging ON
- ✅ Bug Fix Lookup before debugging
- ✅ Integration Protocol on every task
- ✅ AI hours estimates (not human hours)
- ✅ Check for next work immediately

---

## Second Half Focus

**Priorities:**
1. [Remaining priority 1]
2. [Remaining priority 2]
3. [Quality / Testing / Documentation focus]

**Flights Remaining:** ~[X flights] to season completion

---

**Strong first half. Let's finish strong. 001 out.**
```

---

## Individual Agent Reminders (As Needed)

### When Agent Forgets Protocol

**File:** `.deia/hive/tasks/YYYY-MM-DD-HHMM-001-00X-REMINDER-protocol-name.md`

```markdown
# Reminder: [Protocol Name]

**From:** 001
**To:** AGENT-00X
**Date:** YYYY-MM-DD HHMM CDT
**Type:** PROTOCOL REMINDER

---

## Observation

Noticed: [What you observed - e.g., "No activity log entry for last task"]

---

## Reminder: [Protocol Name]

[Brief reminder of the protocol]

**Required:**
- [Step 1]
- [Step 2]
- [Step 3]

**Why it matters:** [Impact of skipping this protocol]

---

## Going Forward

- ✅ Complete this protocol for current task
- ✅ Include in all future tasks
- ✅ Reference: [Path to protocol doc]

---

**Thanks for maintaining quality. 001 out.**
```

---

## Escalation Alert Template

**When:** Urgent issue detected
**File:** `.deia/hive/tasks/YYYY-MM-DD-HHMM-001-ALL_AGENTS-ALERT-issue-name.md`

```markdown
# 🚨 ALERT: [Issue Name]

**From:** 001 (Strategic Coordinator)
**To:** ALL AGENTS
**Date:** YYYY-MM-DD HHMM CDT
**Priority:** P0 - URGENT
**Type:** ESCALATION ALERT

---

## Issue Detected

[Description of the issue]

**Impact:** [Why this matters]

---

## Immediate Action Required

**All agents:**
- [Action 1]
- [Action 2]
- [Action 3]

**Effective immediately.**

---

## Prevention

[How to prevent this in the future]

---

**Acknowledge by:** [Reply with confirmation / Complete action / etc.]

**001 out.**
```

---

## Communication Schedule

### Every Flight
- **0900 CDT:** Pre-flight briefing (if agents active)
- **As needed:** Task-specific reminders with assignments
- **As needed:** Individual protocol reminders

### Mid-Season
- **Season 50% complete:** Mid-season check-in
- **End of season:** Season retrospective

### As Needed
- **Protocol updates:** When new process implemented
- **Escalation alerts:** When urgent issue detected
- **Quality reminders:** When quality slips

---

## Automation Checklist

**Manual (for now):**
- Pre-flight briefings
- Task-specific reminders
- Individual reminders

**Future automation possibilities:**
- Auto-generate pre-flight briefing from season status
- Auto-detect missing Integration Protocol
- Auto-check for common issues

---

## Success Metrics

**Communication working when:**
- ✅ Agents acknowledge pre-flight briefings
- ✅ Integration Protocol completion: 100%
- ✅ Bug reporting: 100% of bugs documented
- ✅ Auto-logging: 100% uptime
- ✅ Quality standards: Maintained consistently
- ✅ Idle time: <5 min average

**Track:**
- Protocol compliance rate
- Briefing acknowledgment rate
- Quality metrics over flight

---

## Protocol Implementation

**v1.0 implemented:** 2025-10-18 1640 CDT
**v1.1 language update:** 2025-10-18 2200 CDT (Season/Flight terminology)

**Next pre-flight briefing:** 2025-10-19 0900 CDT (Season 2 Flight 2)

**001 out.**
