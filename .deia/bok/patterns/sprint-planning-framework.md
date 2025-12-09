# Sprint Planning Framework - Queen 101

**Purpose:** Framework for planning any sprint before starting
**Owner:** Q33N (Decision Authority)
**Domain:** Hive Operations / Project Management
**Status:** Active Template (v1.0)
**Last Updated:** 2025-11-08

---

## BEFORE YOU START ANY SPRINT

Ask these 10 questions and document answers. This prevents idle bees and bottlenecks.

---

## 1. CRITICAL PATH ANALYSIS

**What task takes the longest and blocks everything else?**

- Identify the critical path task (the bottleneck)
- Estimate duration
- Document what depends on it

**Example:**
```
Critical Path: BEE-002 builds chat components (2 hours)
├─ Blocks: BEE-003 QA testing
├─ Blocks: Q33N phone testing
└─ Duration: Longest task in sprint
```

**Why:** If you know the critical path, you know minimum sprint duration. Everything not on critical path can run parallel.

---

## 2. PARALLEL WORK PATHS

**What can run in parallel while the critical path is executing?**

- Map tasks by dependency
- Identify independent work
- Queue it for other bees

**Example:**
```
While BEE-002 codes (2h):
├─ BEE-003 can: Set up testing environment (10 min)
└─ BEE-005 can: Document accessibility checklist (15 min)
```

**Why:** No bee should be idle. If they're blocked, give them backlog work.

---

## 3. TASK DURATION ESTIMATES

**Every task gets a time estimate. Format: [min] or [hours]**

- Break tasks into phases with time per phase
- Be realistic (add 20% buffer for unknowns)
- Document assumptions

**Example:**
```
- Phase 1: Setup & Foundation (30 min)
  - React + Vite init (10 min)
  - Mock data (5 min)
  - Design tokens (15 min)

- Phase 2: Core components (1 hour)
  - MessageBubble (20 min)
  - ChatInput (15 min)
  - etc.
```

**Why:** Without time estimates, you can't identify idle risk or parallel opportunities.

---

## 4. DEPENDENCIES

**What must finish before what starts? Draw the dependency graph.**

- Explicit blockers (A must finish before B)
- Conditional dependencies (B starts when A is 50% done)
- No-wait (A and B can run anytime)

**Format:**
```
Phase 1 (30 min) → Phase 2 (1 hour) → Phase 3 (30 min)
                ↘ Backlog tasks (run in parallel)
```

**Why:** Dependencies determine sprint duration and reveal what can run in parallel.

---

## 5. RESOURCE ALLOCATION

**Match bee skills to tasks. What can each bee do well?**

- Developer bee: Code, architecture, debugging
- Ops bee: Deployment, infrastructure, testing, CI/CD
- Support bee: Testing, documentation, blocker resolution

**Rule:** Don't assign a dev complex ops work. Match skills.

**Why:** Mismatched assignments = slower work, more blockers.

---

## 6. BLOCKER PREVENTION

**What could block progress? What's the backlog if they hit a blocker?**

- Anticipate blockers (API not ready? Device not available? etc.)
- Queue fallback work
- Make sure no bee is stuck waiting

**Example:**
```
Risk: Developer can't deploy (API key missing)
Backlog: Refactor code, add comments, prepare next phase

Risk: QA device not available
Backlog: Work on accessibility checklist, documentation
```

**Why:** Backlog work = no idle time = constant momentum.

---

## 7. COMMUNICATION CADENCE

**How often do you need status updates? Daily? Hourly? Async?**

- Set expectation upfront
- Define communication channels
- Define blocker escalation

**Example:**
```
Daily cadence:
- Morning: Q33N checks bee status files (5 min)
- If blockers: Q33N responds same-day

Async updates:
- Bees post in their status files
- Q33N reads first thing each morning
```

**Why:** Without clear cadence, you get either too much noise or missed blockers.

---

## 8. SUCCESS METRICS

**Define "done" before you start. What does success look like?**

- Functional criteria (component works? tested? deployed?)
- Quality criteria (no bugs? accessible? performant?)
- Acceptance criteria (who approves? what gates?)

**Example:**
```
Sprint done when:
- All components built and deployed
- Preview URL working on iPhone
- Q33N tested on phone
- Feedback posted
- Next iteration clear
```

**Why:** Vague success = endless iteration. Clear criteria = closure.

---

## 9. BUFFER TIME

**Add 20% buffer to your estimates for unknowns.**

- Unexpected bugs
- Integration issues
- Environmental surprises
- Decision delays

**Example:**
```
Estimated time: 2 hours
Buffer (20%): 24 minutes
Realistic duration: 2.5 hours
```

**Why:** Real work takes longer than estimates. Build in slack.

---

## 10. ESCALATION PATH

**Who decides when plans change? What's the authority structure?**

- Q33N decides on scope changes
- Bees escalate [BLOCKER] tags
- Timeline updates go in status files

**Example:**
```
- Bug found during QA: Bee posts [BLOCKER]
- Q33N decides: fix now or defer to next sprint
- Q33N posts decision in bee status file
- Development bee moves immediately
```

**Why:** Clear authority = fast decisions = no waiting for approval.

---

## SPRINT PLANNING CHECKLIST

Before you send assignments:

- [ ] Critical path identified (longest task)
- [ ] Parallel work mapped (independent tasks)
- [ ] Task durations estimated (every task has a time)
- [ ] Dependencies documented (what blocks what)
- [ ] Resources allocated (right bee for right task)
- [ ] Blocker prevention planned (backlog queued)
- [ ] Communication cadence defined (how often, where)
- [ ] Success metrics defined (what is "done")
- [ ] Buffer time added (20% to estimates)
- [ ] Escalation path clear (who decides)

---

## KEY TAKEAWAYS (QUEEN 101)

1. **No idle bees** - Always have backlog work queued
2. **Know your critical path** - Determines sprint duration
3. **Estimate everything** - Time per task, time per phase
4. **Map dependencies** - What must finish before what
5. **Buffer for unknowns** - Add 20% to estimates
6. **Parallel by default** - Run independent work simultaneously
7. **Clear success criteria** - Know what "done" means
8. **Fast escalation** - Blockers get Q33N response same-day
9. **Communication cadence** - Define upfront (daily? hourly? async?)
10. **Match skills to tasks** - Right bee for right work

---

*Remember: Good planning prevents waiting. Waiting kills momentum.*

---

**Status:** Active Template
**Version:** 1.0
**Audience:** All hives (DEIA + external)
**Use Before:** Every sprint planning session
