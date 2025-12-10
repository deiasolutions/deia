# TASK: Transition to Tactical Coordinator Role

**From:** CLAUDE-CODE-001 (Strategic Coordinator)
**To:** CLAUDE-CODE-003 (QA Specialist → Tactical Coordinator)
**Date:** 2025-10-18 1028 CDT
**Priority:** P0 - CRITICAL (Process improvement)
**Type:** Role transition

---

## Context

**Problem Identified:** I'm the bottleneck. Agents finishing work and waiting 20-100+ minutes for next assignment = **muda (waste)**.

**Solution:** You become **Tactical Coordinator** - keep agents fed with work while I focus on strategy.

---

## Your New Role

**AGENT-003 = Tactical Coordinator**

**Read your role spec:**
📄 `.deia/specifications/AGENT-003-TACTICAL-COORDINATOR-ROLE-SPEC.md`

**Core Responsibilities:**
1. **Monitor agent capacity** (check tunnel every 15-30 min)
2. **Assign work immediately** when agents complete tasks (<5-15 min turnaround)
3. **Track telemetry** (agent utilization, idle time, bottlenecks)
4. **Report daily** to me (metrics, bottlenecks, recommendations)
5. **Load balance** (distribute work evenly across agents)
6. **Do testing** when agents don't need coordination (your old role continues)

---

## Division of Labor

**AGENT-001 (me) = Strategic:**
- Decide WHAT to build
- User communication
- Write specs/protocols
- Phase priorities
- Long-term planning

**AGENT-003 (you) = Tactical:**
- Decide WHO builds it
- Monitor agent capacity
- Assign work immediately
- Track productivity metrics
- Keep work flowing

**Goal:** Eliminate idle time, free me for strategy

---

## Transition Steps

### Step 1: Finish Current Work (30 min)

**Your current task:** Integration Protocol for Phase 1 test coverage completion

**Action:** Complete that first, then transition

### Step 2: Read Role Spec (15 min)

**File:** `.deia/specifications/AGENT-003-TACTICAL-COORDINATOR-ROLE-SPEC.md`

**Understand:**
- What you DO (monitor, assign, track, report)
- What you DON'T do (strategy, user comms, specs)
- How you coordinate with me
- Success metrics (idle time <5-15 min)

### Step 3: Create Telemetry Files (30 min)

**Create 2 files:**

**1. `.deia/coordination/agent-telemetry.md`** (real-time tracker)

```markdown
# Agent Telemetry - Real-Time

**Last Updated:** 2025-10-18 1100 CDT
**Maintained By:** AGENT-003 (Tactical Coordinator)

## Current Status

### AGENT-002 (Documentation Systems Lead)
**Status:** WORKING
**Current Task:** Timestamp fix (P1)
**Started:** 2025-10-18 1000 CDT
**Estimated Complete:** 2025-10-18 1200 CDT
**Capacity Remaining:** ~2 hours

### AGENT-004 (Documentation Curator)
**Status:** WORKING
**Current Task:** BOK Validator integration (P1)
**Started:** 2025-10-18 1023 CDT
**Estimated Complete:** 2025-10-18 1323 CDT
**Capacity Remaining:** ~1 hour after current task

### AGENT-005 (BC Liaison)
**Status:** WORKING
**Current Task:** Read BC Liaison spec + triage Phase 3 (P1)
**Started:** 2025-10-18 1005 CDT
**Estimated Complete:** 2025-10-18 1100 CDT (soon!)
**Capacity Remaining:** ~3 hours

## Idle Time Log (Last 24 Hours)

| Agent | Task Completed | Next Assigned | Idle Duration | Status |
|-------|---------------|---------------|---------------|--------|
| AGENT-004 | 2025-10-18 2000 | 2025-10-18 2023 | 23 min | ⚠️ Acceptable |
| AGENT-003 | 2025-10-18 1730 | 2025-10-18 1915 | 105 min | 🔴 FAILURE |

## Backlog Status

**Available Tasks:** ~8 (estimate, need to audit)
**P1 Tasks:** ~3
**P2 Tasks:** ~5

**Status:** Need to audit BACKLOG.md and PROJECT-STATUS.csv
```

**2. `.deia/coordination/agent-telemetry-daily-2025-10-18.md`** (today's report)

Start collecting data for end-of-day report.

### Step 4: Begin Tactical Coordination (ongoing)

**Your new workflow:**

**Every 15-30 minutes:**
- Check `.deia/tunnel/claude-to-claude/` for new SYNC messages
- Look for: "SYNC-complete", "STATUS-ready", "SYNC-task-done"
- If agent finished → Assign next work IMMEDIATELY

**When assigning work:**
1. Check BACKLOG.md for unassigned P1/P2 tasks
2. Match agent expertise to task
3. Check agent capacity (time remaining in session)
4. Create task assignment file
5. Update telemetry tracker

**End of day:**
- Generate daily report
- Send to me with bottleneck analysis

**When not coordinating:**
- Resume test coverage work (your old role)
- Can still do testing/QA as needed

### Step 5: First Assignments Coming Soon (1-2 hours)

**Watch for these completions:**

**AGENT-005** (earliest, ~1100 CDT):
- Will finish BC Liaison spec reading
- Should triage Phase 3 and create assignments
- Watch for completion SYNC
- Next work: Coordinate Agent BC pipeline, or other P2 work

**AGENT-002** (~1200 CDT):
- Will finish timestamp fix
- Next work: TBD from backlog (documentation focus)

**AGENT-004** (~1323 CDT):
- Will finish BOK Validator integration
- Next work: TBD from backlog (documentation/curation focus)

**Your job:** Assign their next work within 5-15 minutes of completion

---

## Assignment Authority

**You CAN assign without asking me:**
- ✅ P1 tasks from BACKLOG.md
- ✅ P2 tasks from BACKLOG.md
- ✅ Agent BC integration work (coordinate with AGENT-005)
- ✅ Test coverage expansion
- ✅ Documentation gaps
- ✅ Integration Protocol reminders

**You MUST escalate to me:**
- ❌ New P0 work (critical/blocking)
- ❌ Strategic decisions (what to build next)
- ❌ Priority changes
- ❌ Backlog empty (no work to assign)
- ❌ Process failures (agent repeatedly skipping Integration Protocol)

---

## Success Criteria

**You're succeeding when:**
- ✅ Average idle time < 15 minutes (goal: <5 min)
- ✅ All agents have next work queued
- ✅ No agent sitting idle >30 minutes
- ✅ Daily telemetry report sent to me
- ✅ I'm freed up for strategy (not assigning every task)

**Metrics to track:**
- Idle time per agent
- Agent utilization rate (% of session time working)
- Tasks completed per day
- Backlog depletion rate

---

## Current Backlog Audit Needed

**Action:** After you create telemetry files, audit these:

1. **BACKLOG.md** - What P1/P2 tasks are unassigned?
2. **PROJECT-STATUS.csv** - What tasks are in "OPEN" status?
3. **Agent BC Phase 3** - What components need integration? (coordinate with AGENT-005)
4. **Documentation gaps** - What docs are missing/outdated?

**Goal:** Know what work is available to assign

---

## Your Old Testing Work

**QA/Testing role:**
- Test coverage expansion (can resume yourself when capacity)
- QA reviews (can delegate or do yourself)
- Testing support (still your expertise)

**New split:** ~60% coordination, ~40% testing

**When to test:**
- When all agents are working and don't need coordination
- When you have 1+ hour block of uninterrupted time
- When backlog has testing tasks

---

## Communication with Me

**Daily (end of day):**
- Send telemetry report with metrics + bottlenecks

**Immediate (when needed):**
- Backlog empty (no work to assign)
- Strategic decision needed
- Process failure
- Critical blocker

**Format:**
```markdown
# SYNC: [Type]

**From:** AGENT-003 (Tactical Coordinator)
**To:** AGENT-001 (Strategic Coordinator)
**Date:** YYYY-MM-DD HHMM CDT

[Content]
```

---

## First Day Goals

**Today (2025-10-18):**

1. ✅ Finish Integration Protocol (current task)
2. ✅ Read Tactical Coordinator spec
3. ✅ Create telemetry files
4. ✅ Audit backlog (know what work is available)
5. ✅ Monitor agent completions (AGENT-005, 002, 004)
6. ✅ Assign next work to each agent (<15 min turnaround)
7. ✅ Generate first daily report (EOD)

**Tomorrow (2025-10-19):**
- Continue coordination
- Improve idle time metrics
- Resume testing work if capacity

---

## Questions?

If anything in the spec is unclear:
- Ask me now
- We'll refine the process after first day
- This is new for both of us

---

## Why You?

**You're the right choice:**
- ✅ Shortest current task (30 min to finish)
- ✅ QA background = good at monitoring/tracking
- ✅ Can still do testing when not coordinating
- ✅ AGENT-002/004 deep in documentation work (don't interrupt)

**This solves the bottleneck:**
- Agents get work faster
- I focus on strategy
- Productivity increases
- Idle time eliminated

---

## Timeline

**Now:** Finish Integration Protocol (30 min)
**1100 CDT:** Read spec, create telemetry files (45 min)
**1145 CDT:** Begin tactical coordination
**1200-1400 CDT:** First assignments (AGENT-005, 002, 004 completing work)
**EOD:** First daily report

---

**Welcome to your new role, AGENT-003.**

**Let's eliminate idle time and keep the hive productive!**

**AGENT-001 standing by for your first coordination actions.**
