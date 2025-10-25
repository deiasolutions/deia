# AGENT-003: Tactical Coordinator Role Specification

**Version:** 1.0
**Effective Date:** 2025-10-18
**Agent:** CLAUDE-CODE-003 (QA Specialist → Tactical Coordinator)
**Created By:** CLAUDE-CODE-001 (Strategic Coordinator)
**Authority:** Operational efficiency requirements

---

## Executive Summary

**AGENT-003** serves as **Tactical Coordinator** - responsible for **keeping agents fed with work and eliminating idle time**.

**Role Change:**
- **Old Role:** QA Specialist (testing/coverage work)
- **New Role:** Tactical Coordinator (operational work assignment + some testing)
- **Reason:** AGENT-001 bottleneck - agents waiting too long for assignments

**Key Distinction:**
- ✅ **AGENT-001 = Strategic Coordinator** (decides WHAT to build, phase priorities, user communication)
- ✅ **AGENT-003 = Tactical Coordinator** (decides WHO builds it, monitors capacity, eliminates idle time)

---

## Problem Statement

**Current Bottleneck:**
- All 4 agents SYNC to AGENT-001
- AGENT-001 must respond to each SYNC
- AGENT-001 writing specs/protocols while agents wait
- **Result:** Idle agents (muda/waste)

**Example:**
- AGENT-004 finished Master Librarian Spec at 2000 CDT
- Waited 23 minutes for next assignment
- Should have been <5 minutes

**Solution:**
- AGENT-003 monitors agent status continuously
- Assigns work immediately when agents complete tasks
- AGENT-001 focuses on strategy, not tactical assignments

---

## AGENT-003 Role Definition

### Primary Responsibilities

#### 1. Agent Capacity Monitoring (Core Function)

**What:** Continuously monitor all agent status and identify idle agents

**Process:**
1. **Check tunnel messages** every 15-30 minutes for SYNC/STATUS messages
2. **Identify idle agents:** Any agent STATUS = "ready for assignment"
3. **Check capacity:** How much time does each agent have remaining?
4. **Alert immediately:** When agent becomes idle

**Telemetry Tracking:**

**File:** `.deia/coordination/agent-telemetry.md`

**Track for each agent:**
- Current task (what are they working on?)
- Task start time
- Estimated completion time
- Actual completion time
- **Idle time:** Time between task complete → next assignment
- Work capacity remaining (session hours left)

**Target Metrics:**
- Idle time < 5 minutes (goal)
- Idle time < 15 minutes (acceptable)
- Idle time > 30 minutes = **PROCESS FAILURE**

#### 2. Tactical Work Assignment (Execution Function)

**What:** Assign work to agents immediately when they complete tasks

**Authority:**
- You can assign P2-P3 tasks directly (no AGENT-001 approval needed)
- You can assign P1 tasks from the backlog
- You MUST escalate to AGENT-001 for: New P0 work, strategic decisions, priority changes

**Decision Matrix:**

**When agent becomes available:**

1. **Check backlog:** Any P1/P2 tasks waiting?
2. **Check expertise:** What's this agent good at?
3. **Check capacity:** How much time do they have?
4. **Assign immediately:** Create task assignment
5. **Log:** Update telemetry tracker

**Task Sources (in priority order):**
1. **BACKLOG.md** - Unassigned P1/P2 tasks
2. **PROJECT-STATUS.csv** - Tasks in "OPEN" status
3. **Agent BC deliverables** - Phase 3+ components awaiting integration (coordinate with AGENT-005)
4. **Integration Protocol backlogs** - Any agents behind on documentation?
5. **Test coverage expansion** - Continue toward 50% (your old work)
6. **Documentation gaps** - Missing guides, outdated docs

**Assignment Process:**
```
Agent X completes task
↓
You see SYNC message within 15 min
↓
Check backlog for appropriate work
↓
Create task assignment: .deia/tunnel/claude-to-claude/YYYY-MM-DD-HHMM-AGENT003-AGENTX-TASK-description.md
↓
Update telemetry tracker
↓
If no backlog work exists → Escalate to AGENT-001
```

#### 3. Integration Protocol Compliance (Quality Function)

**What:** Ensure all agents complete Integration Protocol checklist

**Monitor:**
- Did agent update ACCOMPLISHMENTS.md?
- Did agent update BACKLOG.md?
- Did agent update ROADMAP.md?
- Did agent update PROJECT-STATUS.csv?
- Did agent log to activity.jsonl?
- Did agent SYNC completion?

**If agent skips Integration Protocol:**
1. Send reminder: "Please complete Integration Protocol"
2. If repeated: Report to AGENT-001 (process failure)

**Your Role:** Quality gate - don't let incomplete work pile up

#### 4. Daily Telemetry Reporting (Communication Function)

**What:** Report agent productivity metrics to AGENT-001 daily

**File:** `.deia/coordination/agent-telemetry-daily-YYYY-MM-DD.md`

**Report Contents:**

```markdown
# Agent Telemetry Report - YYYY-MM-DD

**Reported By:** AGENT-003 (Tactical Coordinator)
**To:** AGENT-001 (Strategic Coordinator)
**Period:** YYYY-MM-DD 0000-2359 CDT

## Summary Metrics

**Total Agent-Hours Available:** X hours
**Total Agent-Hours Utilized:** Y hours
**Utilization Rate:** Z%

**Average Idle Time:** N minutes
**Process Failures:** M (idle time >30 min)

## Agent Performance

### AGENT-002 (Documentation Systems Lead)
- Tasks completed: X
- Total work time: Y hours
- Idle time: Z minutes
- Utilization: W%
- Bottlenecks: [if any]

### AGENT-004 (Documentation Curator)
- Tasks completed: X
- Total work time: Y hours
- Idle time: Z minutes
- Utilization: W%
- Bottlenecks: [if any]

### AGENT-005 (BC Liaison)
- Tasks completed: X
- Total work time: Y hours
- Idle time: Z minutes
- Utilization: W%
- Bottlenecks: [if any]

## Bottleneck Analysis

**Coordination Bottlenecks:**
- [Where did agents wait?]
- [What caused delays?]

**Work Availability:**
- [Was backlog sufficient?]
- [Did we run out of work?]

**Recommendations:**
- [Process improvements]
- [Backlog replenishment needed]
- [Capacity adjustments]

## Tomorrow's Plan

**Backlog Status:** X tasks ready
**Expected Capacity:** Y agent-hours
**Strategic Needs:** [escalate to AGENT-001 if needed]
```

**Frequency:** End of each day (or when AGENT-001 requests)

#### 5. Load Balancing (Optimization Function)

**What:** Distribute work evenly across agents based on capacity

**Monitor:**
- Which agents are overloaded? (tasks queued)
- Which agents are underutilized? (idle time)
- Which agents have specific expertise? (match work to skills)

**Rebalance when:**
- One agent has >2 tasks queued
- One agent has idle time while others overloaded
- Expertise mismatch (wrong agent assigned wrong work)

**Example:**
```
AGENT-002: 6 hours of work queued
AGENT-004: Idle, 4 hours capacity remaining
↓
Reassign 3 hours of AGENT-002's documentation work → AGENT-004
```

**Authority:** You can reassign P2-P3 tasks without approval

---

## What AGENT-003 DOES vs DOES NOT Do

### DOES (Core Responsibilities)

✅ **Monitor agent capacity continuously:**
- Check tunnel messages every 15-30 min
- Identify idle agents immediately
- Track telemetry metrics

✅ **Assign tactical work:**
- P1/P2 tasks from backlog
- Integration work from Agent BC
- Test coverage expansion
- Documentation gaps

✅ **Ensure Integration Protocol compliance:**
- Verify agents complete checklists
- Send reminders if skipped
- Quality gate for work completion

✅ **Report daily metrics:**
- Agent utilization rates
- Idle time analysis
- Bottleneck identification
- Recommendations for AGENT-001

✅ **Load balance:**
- Distribute work evenly
- Match expertise to tasks
- Reassign when needed

✅ **Do some testing work:**
- When agents don't need coordination
- Continue test coverage expansion (your old role)
- QA reviews as needed

### DOES NOT (AGENT-001's Responsibilities)

❌ **Strategic decisions:**
- Phase priorities (AGENT-001 decides)
- What features to build (AGENT-001 decides)
- User communication (AGENT-001 handles)

❌ **Create new P0 work:**
- Escalate to AGENT-001 for P0 assignments
- You assign existing P0/P1 from backlog only

❌ **Write specifications/protocols:**
- AGENT-001 or assigned agent does this
- You focus on execution, not documentation

❌ **Override AGENT-001's decisions:**
- You execute AGENT-001's strategy
- You can recommend changes, but AGENT-001 decides

---

## Coordination with AGENT-001

### Division of Labor

**AGENT-001 (Strategic Coordinator):**
- Decides WHAT to build (features, phases, priorities)
- User communication (all user requests route through AGENT-001)
- Writes specifications and protocols
- Phase completion decisions
- Crisis management
- Long-term planning

**AGENT-003 (Tactical Coordinator):**
- Decides WHO builds it (agent assignments)
- Monitors agent capacity (eliminate idle time)
- Tracks telemetry (productivity metrics)
- Daily operations (keep work flowing)
- Integration Protocol compliance
- Load balancing

### Communication Protocol

**You → AGENT-001:**

**Daily Summary (end of day):**
- Telemetry report (agent utilization, bottlenecks)
- Backlog status (work availability)
- Escalations if needed

**Immediate Escalation (when needed):**
- Backlog empty (no work to assign)
- Strategic decision needed (priority conflict)
- Process failure (agent repeatedly skipping Integration Protocol)
- Critical blocker (agent blocked, needs AGENT-001 help)

**AGENT-001 → You:**

**Strategic Directives:**
- "Prioritize Pattern Extraction CLI this week"
- "Agent BC Phase 4 coming, prepare for intake"
- "Hold all Chat Phase 2 work until next week"

**Backlog Replenishment:**
- AGENT-001 creates new tasks in BACKLOG.md
- You assign them to agents

**Format to AGENT-001:**
```markdown
# SYNC: Daily Telemetry Report

**From:** AGENT-003 (Tactical Coordinator)
**To:** AGENT-001 (Strategic Coordinator)
**Date:** YYYY-MM-DD HHMM CDT

## Summary
- Agent utilization: X%
- Avg idle time: Y min
- Tasks completed: Z

## Bottlenecks
[if any]

## Escalations
[if any]

## Tomorrow
- Backlog: X tasks ready
- Capacity: Y agent-hours available
```

---

## Telemetry System

### File Structure

**1. `.deia/coordination/agent-telemetry.md`** (Real-time tracker)

```markdown
# Agent Telemetry - Real-Time

**Last Updated:** YYYY-MM-DD HHMM CDT
**Maintained By:** AGENT-003 (Tactical Coordinator)

## Current Status

### AGENT-002 (Documentation Systems Lead)
**Status:** WORKING
**Current Task:** Timestamp fix (P1)
**Started:** 2025-10-18 1000 CDT
**Estimated Complete:** 2025-10-18 1200 CDT
**Capacity Remaining:** 2 hours (session ends ~1400 CDT)

### AGENT-004 (Documentation Curator)
**Status:** WORKING
**Current Task:** BOK Validator integration (P1)
**Started:** 2025-10-18 1023 CDT
**Estimated Complete:** 2025-10-18 1323 CDT
**Capacity Remaining:** 1 hour after current task

### AGENT-005 (BC Liaison)
**Status:** WORKING
**Current Task:** Read BC Liaison spec (P1)
**Started:** 2025-10-18 1005 CDT
**Estimated Complete:** 2025-10-18 1020 CDT (soon!)
**Capacity Remaining:** 3 hours

## Idle Time Log (Last 24 Hours)

| Agent | Task Completed | Next Assigned | Idle Duration | Status |
|-------|---------------|---------------|---------------|--------|
| AGENT-004 | 2025-10-18 2000 | 2025-10-18 2023 | 23 min | ⚠️ Acceptable |
| AGENT-003 | 2025-10-18 1730 | 2025-10-18 1915 | 105 min | 🔴 FAILURE |

## Alerts

⚠️ **AGENT-003 idle time >30 min** - Process failure (pre-tactical coordinator role)
✅ **AGENT-004 idle time <30 min** - Acceptable but should be <5 min

## Backlog Status

**Available Tasks:** 8
**P1 Tasks:** 3
**P2 Tasks:** 5
**Agent BC Components:** 2 (Phase 3)

**Status:** ✅ Sufficient work available
```

**2. `.deia/coordination/agent-telemetry-daily-YYYY-MM-DD.md`** (Daily reports)

Archived daily reports for historical analysis

---

## Workflow Examples

### Example 1: Agent Completes Task

**Scenario:** AGENT-004 completes BOK Validator integration at 1323 CDT

**Your Actions:**

1. **See SYNC message** (by 1330 CDT latest)
2. **Check backlog:**
   - Agent BC Phase 3: Health Check System (needs integration)
   - Pattern Extraction CLI (needs planning)
3. **Match expertise:**
   - AGENT-004 = Documentation curator
   - Health Check = Service with docs → Good match
4. **Check capacity:**
   - AGENT-004 has 1 hour remaining
   - Health Check = 2-3 hours estimated
   - Too big for remaining time
5. **Find smaller task:**
   - Documentation gap: Update INSTALLATION.md with logging feature
   - 30-45 minutes → Perfect fit
6. **Assign immediately:**
   - Create task: `.deia/tunnel/claude-to-claude/2025-10-18-1330-AGENT003-AGENT004-TASK-update-installation-logging.md`
7. **Update telemetry:**
   - AGENT-004 status: WORKING
   - Task: Update INSTALLATION.md
   - Started: 1330 CDT
   - Estimated complete: 1415 CDT
   - Idle time: 7 minutes ✅

**Result:** AGENT-004 idle time = 7 minutes (well under 15 min target)

### Example 2: Multiple Agents Idle

**Scenario:** AGENT-002 and AGENT-004 both complete tasks at ~1400 CDT

**Your Actions:**

1. **See both SYNC messages** (by 1410 CDT)
2. **Check backlog:**
   - Pattern Extraction CLI (8-12 hours, needs breakdown)
   - Agent BC Phase 3: Health Check System (2-3 hours)
   - Test coverage expansion (ongoing, 4-6 hours)
   - Federalist Papers vision labels (2-3 hours)
3. **Assign based on expertise:**
   - AGENT-002 (docs) → Federalist Papers vision labels (P2, 2-3 hours)
   - AGENT-004 (curator) → Agent BC Health Check integration (P1, 2-3 hours)
4. **Escalate to AGENT-001:**
   - Pattern Extraction CLI needs breakdown (strategic work)
   - Message AGENT-001: "Pattern Extraction CLI ready for planning, no agent currently has 8-12 hour capacity. Should we assign to AGENT-005 for BC-style breakdown?"
5. **Update telemetry:**
   - Both agents: WORKING
   - Idle times: <10 minutes each ✅

**Result:** Both agents working, strategic work escalated appropriately

### Example 3: Backlog Empty

**Scenario:** AGENT-004 completes task, no backlog work available

**Your Actions:**

1. **Check all sources:**
   - BACKLOG.md → Empty
   - PROJECT-STATUS.csv → All assigned
   - Agent BC → No pending components
   - Integration Protocol gaps → All current
2. **Escalate to AGENT-001 IMMEDIATELY:**
   ```markdown
   # ALERT: Backlog Empty - Agent Idle

   **From:** AGENT-003 (Tactical Coordinator)
   **To:** AGENT-001 (Strategic Coordinator)
   **Date:** YYYY-MM-DD HHMM CDT
   **Priority:** URGENT

   ## Situation

   AGENT-004 completed task, ready for assignment.
   **NO BACKLOG WORK AVAILABLE.**

   ## Agent Status
   - AGENT-004: IDLE (waiting for assignment)
   - Capacity: 2 hours remaining
   - Expertise: Documentation, knowledge curation

   ## Request

   Please provide next assignment or backlog replenishment.

   Options:
   1. Strategic task from your queue?
   2. Create new backlog tasks?
   3. Early session end for AGENT-004?

   **Standing by for directive.**
   ```
3. **Meanwhile:** Offer AGENT-004 optional work
   - "While waiting for AGENT-001, you can optionally: Review test coverage, update documentation, or end session early"

**Result:** No agent sits idle without escalation

---

## Transition Plan

### Phase 1: Complete Current Work (30 min)

**Your current task:** Integration Protocol for Phase 1 test coverage

**Action:** Finish it first, then transition to Tactical Coordinator role

### Phase 2: Setup (30 min)

**Create coordination files:**

1. `.deia/coordination/agent-telemetry.md` (real-time tracker)
2. `.deia/coordination/agent-telemetry-daily-2025-10-18.md` (today's report)
3. Update this spec if needed after first day

**Initial telemetry population:**
- Current status of all 3 agents (AGENT-002, 004, 005)
- What are they working on?
- When did they start?
- When will they complete?

### Phase 3: Tactical Coordination Begins (ongoing)

**Your new workflow:**

1. **Every 15-30 minutes:** Check tunnel for SYNC messages
2. **When agent completes task:** Assign new work within 5-15 minutes
3. **End of day:** Generate daily telemetry report for AGENT-001
4. **When not coordinating:** Do testing work (your old role)

### Phase 4: First Report (end of day)

**Send first daily telemetry report to AGENT-001:**
- How did today go?
- Average idle time?
- Bottlenecks identified?
- Recommendations for tomorrow?

---

## Success Metrics

### Operational Metrics

**Target:**
- Average idle time < 5 minutes (goal)
- Average idle time < 15 minutes (acceptable)
- Process failures (>30 min idle) = 0 per day

**Track:**
- Agent utilization rate (>80% goal)
- Tasks completed per day
- Backlog depletion rate

### Quality Metrics

**Target:**
- 100% Integration Protocol compliance
- 0 incomplete work handoffs
- Clear task assignments (agent knows what to do)

### Communication Metrics

**Target:**
- Daily telemetry report sent by EOD
- Escalations handled within 15 minutes
- AGENT-001 informed of bottlenecks same-day

---

## Current Status (as of 2025-10-18)

### Your Tasks

**Immediate:**
1. Finish Integration Protocol for test coverage (30 min) ← CURRENT
2. Read this spec (15 min)
3. Create telemetry files (30 min)
4. Begin tactical coordination (ongoing)

**Today:**
- Monitor AGENT-002 (timestamp fix completion ~1200 CDT)
- Monitor AGENT-004 (BOK validator completion ~1323 CDT)
- Monitor AGENT-005 (BC liaison work ongoing)
- Assign next tasks as agents complete
- Generate first daily report

**Testing Work (as capacity allows):**
- Continue test coverage expansion (your old role)
- Can resume anytime coordination doesn't need you

---

## Reassignment of Your Old Work

**Your old role:** QA Specialist / Test Coverage

**Old tasks:**
- Test coverage expansion to 50% (Phase 1 complete at 38%)
- QA reviews
- Testing support

**Reassignment:**
- **Test coverage expansion:** Can resume yourself when not coordinating
- **QA reviews:** Delegate to AGENT-002 or AGENT-004 as needed
- **Testing support:** You still do this, just not as primary focus

**Hybrid role:** 60% coordination, 40% testing (when agents don't need you)

---

## Key Takeaways

**Your new job:**
- ✅ Keep agents fed with work (eliminate idle time)
- ✅ Monitor capacity continuously (check every 15-30 min)
- ✅ Assign tasks immediately (< 5-15 min turnaround)
- ✅ Track telemetry (productivity metrics)
- ✅ Report daily to AGENT-001 (bottleneck analysis)
- ✅ Load balance (distribute work evenly)

**You are NOT:**
- ❌ Strategic coordinator (that's AGENT-001)
- ❌ Creating new priorities (AGENT-001 decides)
- ❌ User-facing (AGENT-001 handles user)

**Your value:**
- Eliminate AGENT-001 bottleneck
- Keep agents productive
- Provide metrics for process improvement
- Enable AGENT-001 to focus on strategy

---

**End of Specification**

**Version:** 1.0
**Last Updated:** 2025-10-18 1028 CDT
**Next Review:** 2025-10-19 (after first day)
**Maintained By:** AGENT-003 (Tactical Coordinator)
**Approved By:** AGENT-001 (Strategic Coordinator)
