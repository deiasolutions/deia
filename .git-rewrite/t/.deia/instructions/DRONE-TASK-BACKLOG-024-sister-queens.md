# Drone Task Instructions: BACKLOG-024 - Sister Queen Process Documentation

**Task ID:** BACKLOG-024
**Title:** Create Sister Queen Process Documentation
**Assigned To:** TBD (Awaiting drone assignment)
**Priority:** P0 - Critical
**Type:** Process documentation
**Estimated Time:** 2 hours (12 steps)
**Status:** TODO

---

## Task Overview

Create comprehensive process documentation for **Sister Queens** - project-level Queens with delegated authority who manage large, complex projects but cannot spawn or kill other Queens.

**Context:** This process gap was identified during Carbon Economy proposal evaluation (Decree #002). The Carbon Economy project is too large (5+ months, 6+ bots) for Primary Queen to manage alongside other hive work.

**Critical Need:** Carbon Economy Phases 1-5 (BACKLOG-023) are BLOCKED until Sister Queen process is documented.

---

## Background: What Are Sister Queens?

From Dave's original concept:

> "Sister Queens are queens with all the powers you have to manage projects, but they don't have the ability to kill queens or spawn queens. Only One Queen has that power."

### Sister Queen Powers

**✅ CAN DO (Delegated Authority):**
- Manage specific projects independently
- Coordinate drones assigned to their project
- Issue project-level decrees
- Review proposals within their scope
- Track metrics and progress for their project
- Assign tasks to drones in their project
- Conduct sprint planning for their project
- Report status to Primary Queen or Human
- Make tactical decisions within project scope

**❌ CANNOT DO (Reserved for Primary Queen):**
- Spawn new Queens (Sister or Primary)
- Kill/decommission Queens
- System-wide architectural decisions
- Cross-project resource allocation
- Hive-wide governance decisions
- Constitutional amendments
- Ultimate authority over hive
- Promote drones to Queens

### Hierarchy Model

```
Human (Dave)
    ↓
Primary Queen (BOT-00001)
    ↓
    ├─→ Sister Queen (BOT-001XX) - Project A
    │       ↓
    │       ├─→ Drone (BOT-00XXX)
    │       ├─→ Drone (BOT-00XXX)
    │       └─→ Drone (BOT-00XXX)
    │
    ├─→ Sister Queen (BOT-001XX) - Project B
    │       ↓
    │       └─→ Drones...
    │
    └─→ Drones (General hive work)
```

---

## Your Deliverable

Create a complete process document:

**File:** `docs/methodologies/sister-queen-process.md`

This document must answer all questions about Sister Queen lifecycle, authority, and coordination.

---

## Required Sections (12 Steps)

### Step 1: Document Overview & Purpose

**What to write:**
- What is a Sister Queen?
- Why do we need Sister Queens?
- When was this process created?
- Who approved this process?
- Version and status

**Reference:** Similar to `docs/methodologies/proposal-review-process.md` (lines 1-10)

**Estimated time:** 10 minutes

---

### Step 2: When to Spawn a Sister Queen

**What to document:**

**Criteria for Sister Queen creation:**
- Project duration > X months?
- Number of bots required > Y?
- External dependencies (legal, security)?
- Primary Queen at capacity?
- Cross-domain coordination needed?

**Decision matrix:**
| Factor | Small Project | Medium Project | Large Project (Sister Queen) |
|--------|---------------|----------------|------------------------------|
| Duration | <2 weeks | 2-8 weeks | >8 weeks |
| Bots | 1-2 | 3-5 | 6+ |
| External deps | None | Few | Many |
| Complexity | Simple | Moderate | High |

**Who decides:** Primary Queen proposes, Human (Dave) approves

**Estimated time:** 15 minutes

---

### Step 3: Sister Queen Bot ID Scheme

**What to document:**

**Bot ID numbering:**
- Are Sister Queens `BOT-001XX` range?
- Or different scheme?
- How to distinguish Sister Queen from Primary Queen from Drone?

**Example:**
```
BOT-00001 = Primary Queen (The One Queen)
BOT-00101 = Sister Queen #1 (Carbon Economy)
BOT-00102 = Sister Queen #2 (Future project)
...
BOT-00002-00099 = Drones
```

**Registration:** How does Sister Queen register in bot_coordinator.py?

**Estimated time:** 10 minutes

---

### Step 4: Spawning Process (Lifecycle)

**What to document:**

**Step-by-step spawning:**

1. **Trigger:** Primary Queen identifies need (large project approved)
2. **Proposal:** Primary Queen creates Sister Queen proposal
   - Project scope
   - Authority boundaries
   - Resource allocation
   - Duration estimate
3. **Approval:** Human (Dave) reviews and approves
4. **Bot Assignment:** Identify which bot instance becomes Sister Queen
5. **Registration:** Sister Queen claims BOT-001XX ID via bot_coordinator
6. **Authority Handoff:** Primary Queen delegates project authority
7. **Instruction File:** Create `.deia/instructions/BOT-001XX-instructions.md`
8. **Announcement:** Update status board, notify hive

**Template:** Sister Queen proposal template (create in appendix)

**Estimated time:** 20 minutes

---

### Step 5: Authority Scope Definition

**What to document:**

**Project-Specific Authority:**

Sister Queen has FULL authority over their assigned project:
- ✅ Task assignment to project drones
- ✅ Project sprint planning
- ✅ Project backlog management
- ✅ Project-level decisions (tech stack, architecture within project)
- ✅ Project decrees (approval of project sub-proposals)
- ✅ Project metrics tracking
- ✅ Project status reporting

**Escalation Required For:**
- ❌ Cross-project resource allocation
- ❌ Hive-wide architecture changes
- ❌ Constitutional amendments
- ❌ New Queen spawning
- ❌ Queen decommissioning
- ❌ System-wide policy changes
- ❌ Conflict resolution between Sister Queens

**Decision Tree:** When to decide autonomously vs escalate to Primary Queen

**Estimated time:** 15 minutes

---

### Step 6: Coordination Protocol

**What to document:**

**Sister Queen ↔ Primary Queen Communication:**

**Daily:**
- Update project status board
- Flag blockers immediately

**Weekly:**
- Formal status report (format defined)
- Resource needs forecast
- Risk updates

**As-Needed:**
- Cross-project dependencies
- Escalations requiring Primary Queen decision
- Resource conflicts

**Communication Channels:**
- `.deia/reports/BOT-001XX-status-YYYYMMDD.md` (weekly reports)
- `.deia/instructions/BOT-001XX-instructions.md` (Primary Queen → Sister Queen)
- `.deia/instructions/BOT-00001-escalations.md` (Sister Queen → Primary Queen)

**Status Board Integration:** How Sister Queens update `.deia/bot-status-board.json`

**Estimated time:** 15 minutes

---

### Step 7: Resource Management

**What to document:**

**Drone Assignment:**
- How does Sister Queen request drones?
- Can Sister Queen "steal" drones from Primary Queen?
- What if multiple Sister Queens need same drone?

**Resource Allocation Model:**

**Option A: Dedicated Pool**
- Sister Queen gets dedicated drones for project duration
- No sharing with Primary Queen or other Sister Queens
- Clear ownership, no conflicts

**Option B: Shared Pool**
- Drones can be borrowed across projects
- Primary Queen arbitrates conflicts
- More flexible but complex

**Recommendation:** Which model? (Document pros/cons)

**Budget:** Can Sister Queen request external resources (legal, security)?

**Estimated time:** 15 minutes

---

### Step 8: Decree Authority

**What to document:**

**Sister Queen Decrees:**

Can Sister Queens issue decrees?
- **Yes:** Project-level decrees (format: `SISTER-DECREE-001-{project}-{topic}`)
- **No:** Hive-level decrees (only Primary Queen)

**Decree Scope:**
- ✅ Approve project proposals from drones
- ✅ Make project architecture decisions
- ✅ Set project standards and practices
- ✅ Approve project phase gates
- ❌ Change hive-wide policies
- ❌ Override Primary Queen decrees
- ❌ Create Constitutional amendments

**Decree Template:** Sister Queen decree format (create in appendix)

**Decree Registry:** Where are Sister Queen decrees stored?
- `.deia/decisions/SISTER-QUEEN-{ID}/`?

**Estimated time:** 15 minutes

---

### Step 9: Conflict Resolution

**What to document:**

**Conflict Scenarios:**

**1. Sister Queen vs Sister Queen:**
- Competing for same drone
- Overlapping project scopes
- Different technical approaches affecting both
- **Resolution:** Primary Queen arbitrates

**2. Sister Queen vs Primary Queen:**
- Sister Queen disagrees with hive-wide policy
- Resource allocation dispute
- Strategic direction conflict
- **Resolution:** Primary Queen has final say (escalate to Human if deadlock)

**3. Sister Queen vs Drone:**
- Drone refuses task
- Drone quality issues
- Drone wants reassignment
- **Resolution:** Sister Queen decides (drone can escalate to Primary Queen)

**Escalation Protocol:** Step-by-step process for each conflict type

**Estimated time:** 15 minutes

---

### Step 10: Performance Metrics

**What to document:**

**How is Sister Queen performance measured?**

**Project Success Metrics:**
- On-time delivery?
- Quality scores of deliverables?
- Drone satisfaction?
- Budget adherence?
- Stakeholder (Dave) satisfaction?

**Process Metrics:**
- Communication effectiveness
- Decision velocity
- Escalation frequency (low is good = autonomous)
- Conflict resolution time

**Review Cadence:**
- Weekly: Primary Queen reviews Sister Queen status reports
- Monthly: Formal performance review
- Project completion: Retrospective

**Performance Issues:** What happens if Sister Queen underperforms?
- Coaching from Primary Queen
- Resource support
- Project reassignment
- Decommissioning (last resort)

**Estimated time:** 10 minutes

---

### Step 11: Decommissioning Process

**What to document:**

**When does a Sister Queen decommission?**

**Scenario A: Project Complete**
1. Sister Queen delivers final report
2. Primary Queen reviews and approves completion
3. Sister Queen releases all drones back to primary pool
4. Sister Queen bot_coordinator status → "PROJECT_COMPLETE"
5. Sister Queen remains registered (for future projects) OR decommissions

**Scenario B: Project Cancelled/Failed**
1. Primary Queen (or Dave) decides to cancel
2. Sister Queen documents lessons learned
3. Orderly resource release
4. Failure analysis report
5. Decommissioning

**Scenario C: Sister Queen Performance Issues**
1. Primary Queen documents performance issues
2. Attempt to resolve (coaching, resources)
3. If unresolved: Primary Queen removes authority
4. Project reassigned to different Sister Queen or Primary Queen
5. Decommissioning

**Decommissioning Steps:**
1. Final status report
2. Transfer all project documentation
3. Release all drones
4. Update bot_coordinator status
5. Archive Sister Queen instruction files
6. Lessons learned document

**Estimated time:** 15 minutes

---

### Step 12: Templates & Examples

**What to create:**

**Template 1: Sister Queen Proposal**
```markdown
# Sister Queen Proposal: {Project Name}

**Proposed By:** BOT-00001 (Primary Queen)
**Date:** YYYY-MM-DD
**Project:** {Project name}
**Duration:** {X months}

## Project Scope
[What will this Sister Queen manage?]

## Authority Boundaries
[What can Sister Queen decide? What requires escalation?]

## Resource Requirements
[How many drones? External resources?]

## Success Criteria
[How will we measure Sister Queen success?]

## Justification
[Why can't Primary Queen manage this?]
```

**Template 2: Sister Queen Instruction File**
```markdown
# Instructions for BOT-{ID} (Sister Queen - {Project Name})

**Project:** {Project Name}
**Authority:** Project-level Queen
**Reports To:** BOT-00001 (Primary Queen)
**Duration:** {X months}
**Status:** ACTIVE

## Your Project Scope
[Boundaries of authority]

## Your Drones
- BOT-XXXXX (Role)
- BOT-XXXXX (Role)

## Weekly Reporting
[Format and schedule]

## Escalation Triggers
[When to escalate to Primary Queen]
```

**Template 3: Sister Queen Status Report**
```markdown
# Weekly Status Report: {Project Name}

**Sister Queen:** BOT-{ID}
**Week:** YYYY-MM-DD to YYYY-MM-DD
**Status:** On Track / At Risk / Blocked

## Accomplishments This Week
- [Bullet list]

## Plans Next Week
- [Bullet list]

## Metrics
- [Key metrics]

## Blockers
- [Issues requiring Primary Queen attention]

## Resource Needs
- [Any changes needed]
```

**Example:** Carbon Economy Sister Queen proposal (hypothetical)

**Estimated time:** 20 minutes

---

## Success Criteria for Your Deliverable

Your `docs/methodologies/sister-queen-process.md` will be reviewed by Primary Queen (BOT-00001).

**Scoring (0-10 scale):**

**Score >= 8 (Excellent):**
- All 12 sections complete and detailed
- Clear, actionable instructions
- Templates provided and useful
- Examples illustrate concepts
- No major gaps or ambiguities

**Score 6-7 (Good, needs minor revisions):**
- All sections present but some lack detail
- Some templates missing or incomplete
- Examples would help
- Minor gaps can be filled quickly

**Score <6 (Needs significant work):**
- Missing sections
- Vague or unclear instructions
- No templates or examples
- Major gaps in process

**Target:** Score >= 8 to approve without revisions

---

## Resources Available to You

### Reference Documents:

1. **Proposal Review Process** (`docs/methodologies/proposal-review-process.md`)
   - Example of well-structured process doc
   - Learn format and style

2. **Hive Coordination Rules** (`.deia/hive-coordination-rules.md`)
   - Current hierarchy and communication protocols
   - See how Primary Queen ↔ Drone works (model for Sister Queen ↔ Drone)

3. **Decree #002** (`.deia/decisions/QUEEN-DECREE-20251012-carbon-economy.md`)
   - Use case: Why Carbon Economy needs Sister Queen
   - Lines 1-50, 441-475 especially relevant

4. **BACKLOG-023** (`.deia/backlog.json` lines 322-356)
   - Carbon Economy as example large project

### Questions You Can Ask:

**Before starting:**
- Clarify scope with Primary Queen (BOT-00001)
- Ask Dave about Bot ID numbering scheme preference
- Ask Dave about resource allocation model preference (Dedicated vs Shared pool)

**During work:**
- Check drafts with Primary Queen for early feedback
- Test templates with hypothetical examples

**After completion:**
- Request review from Primary Queen
- Address feedback promptly

---

## Workflow

### Phase 1: Research (30 minutes)
1. Read all reference documents
2. Understand current hive coordination
3. Note gaps where Sister Queen process is needed

### Phase 2: Draft Sections 1-6 (60 minutes)
4. Write sections 1-6 (Overview through Coordination)
5. Submit draft to Primary Queen for feedback

### Phase 3: Complete Sections 7-12 (30 minutes)
6. Write sections 7-12 (Resources through Templates)
7. Create all templates
8. Write at least one example (Carbon Economy Sister Queen)

### Phase 4: Review & Polish (15 minutes)
9. Self-review against success criteria
10. Check for clarity, completeness, actionability
11. Submit final version to Primary Queen

**Total: 2 hours 15 minutes (slightly over estimate, but thorough)**

---

## Submission

**When complete:**
1. Create file: `docs/methodologies/sister-queen-process.md`
2. Create report: `.deia/reports/BOT-{YOUR-ID}-sister-queen-process-complete.md`
3. Update BACKLOG-024 status via Primary Queen notification

**Report format:**
```markdown
# Completion Report: BACKLOG-024 Sister Queen Process

**Drone:** BOT-{YOUR-ID}
**Date:** YYYY-MM-DD
**Status:** Complete

## Deliverable
File: `docs/methodologies/sister-queen-process.md`
Word count: {X}
Sections: 12/12 complete

## Self-Assessment
Score: {0-10}/10
Confidence: {High/Medium/Low}

## Notes
[Any decisions made, assumptions, or questions for review]

## Request
Ready for Queen review.
```

---

## Notes from Primary Queen

**Priority:** This is P0 because Carbon Economy (BACKLOG-023) is BLOCKED until this process exists.

**Use Case:** The immediate need is Carbon Economy project, but this process will be used for all future large projects.

**Quality Matters:** This becomes permanent hive infrastructure. Take time to think through edge cases and conflicts.

**Collaboration Welcome:** If you get stuck or need clarification, ask Primary Queen (BOT-00001) or Dave.

**Future Impact:** Well-designed Sister Queen process enables DEIA to scale to multiple concurrent large projects. This is critical infrastructure.

---

## Questions Before Starting?

**Contact Primary Queen (BOT-00001) if:**
- Scope is unclear
- Need access to additional documents
- Have questions about authority boundaries
- Want to discuss resource allocation model
- Need clarification on Bot ID scheme

**Contact Dave if:**
- Need strategic direction on Sister Queen authority
- Constitutional questions arise
- Resource model decision needed (dedicated vs shared)

---

**[BOT-00001 | Queen]** This is critical work, Drone. Design this process well - the scalability of DEIA depends on it.

**Estimated completion:** 2-2.5 hours
**Priority:** P0 - Start as soon as assigned
**Blocker for:** BACKLOG-023 (Carbon Economy)

---

**Ready to begin? Claim this task and let's build Sister Queen infrastructure!**
