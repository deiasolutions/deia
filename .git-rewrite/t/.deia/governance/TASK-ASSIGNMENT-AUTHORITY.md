# Task Assignment Authority Protocol

**Version:** 2.0 (CLAUDE-CODE Agent Era)
**Date:** 2025-10-17
**Status:** Active
**Authority:** Documentation Systems Lead (CLAUDE-CODE-002)
**Approved By:** User (daaaave-atx)

---

## Overview

This document defines who has authority to assign tasks to agents in the DEIA Project Hive, and under what circumstances.

---

## Authority Hierarchy

### Level 1: Ultimate Authority - User (daaaave-atx)

**Powers:**
- ✅ Can assign tasks to ANY agent
- ✅ Can override any other assignment
- ✅ Can create, modify, or dissolve roles
- ✅ Can establish or change priorities
- ✅ Can halt or redirect any work

**Method:** Direct instruction in chat or through task files

**Example:**
> "CLAUDE-CODE-005, integrate the AgentStatusTracker next"

---

### Level 2: Strategic Coordinator - CLAUDE-CODE-001 (Left Brain)

**Role:** Strategic Planner & Coordinator
**Current Status:** Inactive (no recent activity)

**Powers (when active):**
- ✅ Can assign tasks within strategic scope
- ✅ Can set priorities for integration queue
- ✅ Can coordinate multi-agent work
- ✅ Can delegate to specialists

**Limitations:**
- ❌ Cannot override user directives
- ❌ Cannot change agent roles (only user can)
- ⚠️ Should coordinate major assignments with user

**Method:** TASK messages via Corpus Callosum protocol

**Example:** Bootstrap message sent to CLAUDE-CODE-002 with 3 initial tasks

---

### Level 3: Domain Specialists (Self-Assignment Within Role)

**Agents:**
- CLAUDE-CODE-002: Documentation Systems & Knowledge Management
- CLAUDE-CODE-003: QA & Testing
- CLAUDE-CODE-004: Documentation Curation
- CLAUDE-CODE-005: Integration & Implementation

**Powers:**
- ✅ Can self-assign work within their domain
- ✅ Can propose priorities to coordinator or user
- ✅ Can delegate sub-tasks within their specialty
- ✅ Can handoff work to agents in related domains

**Limitations:**
- ❌ Cannot assign work to other agents outside handoffs
- ❌ Cannot change another agent's priorities
- ⚠️ Should coordinate cross-domain work via SYNC

**Method:** Self-assignment documented in activity log + heartbeat

**Example:** CLAUDE-CODE-002 deciding to create COMMUNICATION-PROTOCOL.md as part of documentation systems work

---

### Level 4: Cross-Domain Coordination (Peer Assignment)

**When peers can assign to each other:**

**Scenario 1: Handoff**
- ✅ Agent completes work that naturally flows to another domain
- ✅ Documents handoff with context and rationale
- ✅ New agent accepts or proposes alternative

**Example:** CLAUDE-CODE-002 handed integration queue to CLAUDE-CODE-005 during role transition

**Scenario 2: Blocker Resolution**
- ✅ Agent blocked on dependency owned by another agent
- ✅ Requests work via QUERY message
- ✅ Other agent prioritizes or proposes timeline

**Example:** Agent needs QA specialist to review before proceeding

**Scenario 3: Collaborative Work**
- ✅ Multi-agent task requiring coordination
- ✅ One agent proposes division of labor
- ✅ Others agree via SYNC responses

**Example:** Large feature requiring implementation + testing + documentation

---

## Assignment Methods & Protocols

### 1. Direct User Assignment

**Format:** Instruction in chat

**Process:**
1. User gives directive to specific agent
2. Agent acknowledges in response
3. Agent logs assignment in activity.jsonl
4. Agent updates heartbeat with new current_task
5. Agent proceeds with work

**Example:**
```
User: "CLAUDE-CODE-002, create a documentation taxonomy"
Agent: "Acknowledged. Creating documentation taxonomy as next priority."
{logs assignment event}
```

---

### 2. Strategic Coordinator Assignment (CLAUDE-CODE-001)

**Format:** TASK message via Corpus Callosum

**File:** `.deia/tunnel/claude-to-claude/YYYY-MM-DD-HHMM-COORDINATOR-AGENT-TASK-description.md`

**Process:**
1. Coordinator creates TASK message with:
   - Clear task description
   - Acceptance criteria
   - Priority level
   - Estimated duration
   - Resources available
2. Agent reads TASK message
3. Agent moves message to archive/ (acknowledgment)
4. Agent logs assignment
5. Agent updates heartbeat
6. Agent sends SYNC when starting work

**Example:** Left Brain's bootstrap message to CLAUDE-CODE-002

---

### 3. Self-Assignment Within Domain

**Format:** Activity log entry

**Process:**
1. Agent identifies work within their domain
2. Agent logs self-assignment:
   ```json
   {"timestamp":"...", "event":"task_self_assigned", "details":{"task":"...", "rationale":"...", "priority":"..."}}
   ```
3. Agent updates heartbeat current_task
4. Agent proceeds with work
5. Agent sends SYNC if work impacts others

**When to notify others:**
- ⚠️ If work affects shared systems
- ⚠️ If work changes protocols other agents use
- ⚠️ If work creates new requirements for others

**Example:** CLAUDE-CODE-002 creating COMMUNICATION-PROTOCOL.md

---

### 4. Peer Handoff

**Format:** SYNC message with handoff

**File:** `~/Downloads/uploads/YYYY-MM-DD-HHMM-AGENT_FROM-AGENT_TO-SYNC-handoff-description.md`

**Process:**
1. Source agent creates handoff document:
   - Work completed
   - Work remaining
   - Resources available
   - Recommended next steps
   - Why handoff is appropriate
2. Target agent reads handoff
3. Target agent either:
   - ✅ Accepts: Logs acceptance, updates heartbeat
   - ⚠️ Proposes alternative: Sends SYNC with counter-proposal
   - ❌ Declines: Sends SYNC explaining why, suggests alternative
4. If accepted, source agent archives handoff
5. Target agent proceeds with work

**Example:** CLAUDE-CODE-002 → CLAUDE-CODE-005 integration handoff

---

### 5. Collaborative Assignment

**Format:** SYNC message proposing collaboration

**Process:**
1. Initiating agent sends SYNC:
   - Describes multi-agent task
   - Proposes division of labor
   - Suggests timeline and dependencies
2. Other agents respond via SYNC:
   - Agree and commit
   - Propose modifications
   - Decline with rationale
3. Once all agree, agents log collaborative task
4. Agents coordinate via SYNC messages during work
5. Final SYNC when complete

**Example:** Feature requiring implementation + testing + documentation

---

## Decision Tree: "Can I Assign This?"

```
Is it the USER assigning?
├─ YES → ✅ Assign to anyone, any task
└─ NO → Continue...

Are you CLAUDE-CODE-001 (Coordinator)?
├─ YES → Is it within strategic scope?
│         ├─ YES → ✅ Assign via TASK message
│         └─ NO → ⚠️ Consult user first
└─ NO → Continue...

Is the work in YOUR domain?
├─ YES → ✅ Self-assign, log it
└─ NO → Continue...

Are you handing off completed work?
├─ YES → ✅ Handoff via SYNC, wait for acceptance
└─ NO → Continue...

Are you blocked on another agent's work?
├─ YES → ⚠️ Send QUERY, don't assign
└─ NO → Continue...

Is it collaborative multi-agent work?
├─ YES → ⚠️ Propose via SYNC, need agreement
└─ NO → ❌ Don't assign, ask coordinator or user
```

---

## Special Cases

### Case 1: Coordinator is Inactive

**Current State:** CLAUDE-CODE-001 has no recent activity

**Protocol:**
1. Agents self-assign within domains
2. Cross-domain work coordinated via SYNC
3. Major priorities set by user
4. No single coordinator - distributed coordination

**When coordinator returns:**
- User reactivates coordinator role
- Coordinator catches up via activity logs
- Coordinator can resume strategic assignments

---

### Case 2: Role Transition

**When agent changes roles:**
1. Agent creates handoff for work in old role
2. Agent identifies target for handoff
3. Target accepts or declines
4. If declined, work goes back to user for assignment
5. Agent updates all protocols with new role

**Example:** CLAUDE-CODE-002 transition from Integration to Documentation Systems

---

### Case 3: Urgent Work

**When something urgent arises:**
1. Agent can self-assign if in domain AND time-sensitive
2. Agent must immediately notify via SYNC
3. Agent explains urgency and rationale
4. Other agents or user can override if needed

**Example:** Critical bug discovered during QA

---

### Case 4: Conflict Resolution

**If two agents claim same work:**
1. First to log assignment in activity.jsonl wins
2. Second agent sends SYNC acknowledging conflict
3. Agents negotiate via SYNC or escalate to user
4. User makes final decision if agents can't agree

---

## Assignment Best Practices

### For Assigners (Coordinator or User):

**DO:**
- ✅ Be specific about task scope
- ✅ Provide acceptance criteria
- ✅ Estimate duration if known
- ✅ List resources/files available
- ✅ Explain priority and dependencies

**DON'T:**
- ❌ Assign without checking agent capacity
- ❌ Override without explaining why
- ❌ Assign work outside agent's capabilities
- ❌ Create conflicting assignments

---

### For Assignees (All Agents):

**DO:**
- ✅ Acknowledge assignment immediately
- ✅ Log assignment in activity.jsonl
- ✅ Update heartbeat current_task
- ✅ Ask clarifying questions if unclear
- ✅ Report blockers as soon as they arise

**DON'T:**
- ❌ Accept assignment silently
- ❌ Start work without logging
- ❌ Ignore assignments you can't complete
- ❌ Spin on blockers without escalating

---

## Logging Requirements

**Every assignment must be logged:**

**Self-Assignment:**
```json
{
  "timestamp": "2025-10-17T20:00:00Z",
  "agent_id": "CLAUDE-CODE-002",
  "event": "task_self_assigned",
  "details": {
    "task": "Create documentation taxonomy",
    "rationale": "Within documentation systems domain",
    "priority": "high",
    "estimated_duration": "30 minutes"
  },
  "status": "working"
}
```

**Assignment Received:**
```json
{
  "timestamp": "2025-10-17T20:00:00Z",
  "agent_id": "CLAUDE-CODE-005",
  "event": "task_assigned",
  "details": {
    "task": "Integrate AgentStatusTracker",
    "assigned_by": "CLAUDE-CODE-002",
    "method": "handoff",
    "priority": "high",
    "handoff_file": "2025-10-17-2050-CLAUDE-CODE-002-ALL_AGENTS-SYNC-role-transition.md"
  },
  "status": "acknowledged"
}
```

**Assignment Completed:**
```json
{
  "timestamp": "2025-10-17T21:00:00Z",
  "agent_id": "CLAUDE-CODE-002",
  "event": "task_completed",
  "details": {
    "task": "Create documentation taxonomy",
    "duration_minutes": 35,
    "deliverables": [".deia/governance/DOCUMENTATION-TAXONOMY.md"]
  },
  "status": "complete"
}
```

---

## Accountability

**All assignments are:**
- 📝 Logged in activity.jsonl
- 📍 Visible in heartbeat current_task
- 🔍 Auditable via activity logs
- 📢 Communicated via SYNC when cross-domain

**Violations:**
- Assigning outside authority → Escalate to user
- Not logging assignment → Protocol violation
- Ignoring assignment → Report to user

---

## Current Assignment Authorities (2025-10-17)

| Agent | Role | Can Assign To | Within Domain |
|-------|------|---------------|---------------|
| **User (daaaave-atx)** | Ultimate Authority | Anyone | All domains |
| **CLAUDE-CODE-001** | Strategic Coordinator | Any agent (when active) | Strategic scope |
| **CLAUDE-CODE-002** | Documentation Systems | Self | Documentation, protocols, governance |
| **CLAUDE-CODE-003** | QA & Testing | Self | Testing, quality, reviews |
| **CLAUDE-CODE-004** | Documentation Curator | Self | Content curation, BOK |
| **CLAUDE-CODE-005** | Integration Coordinator | Self | Integration, implementation |

**Cross-domain:** Via handoff or SYNC with acceptance required

---

## Questions & Answers

**Q: Can CLAUDE-CODE-002 assign integration work to CLAUDE-CODE-005?**
A: Only via handoff with acceptance. CLAUDE-CODE-002 cannot unilaterally assign.

**Q: Can CLAUDE-CODE-005 assign QA work to CLAUDE-CODE-003?**
A: Only via QUERY (request) or collaborative SYNC. Not direct assignment.

**Q: Who assigns work when CLAUDE-CODE-001 is inactive?**
A: User assigns cross-domain work. Agents self-assign within domains.

**Q: Can an agent refuse an assignment from the coordinator?**
A: Yes, with clear rationale via SYNC. User makes final decision.

**Q: What if two agents want the same task?**
A: First to log assignment wins, or negotiate via SYNC, or escalate to user.

---

## Related Protocols

- **Corpus Callosum Protocol** - Inter-agent messaging (`.deia/tunnel/BOOTSTRAP-FAQ.md`)
- **Communication Protocol** - Identity footer and message types (`.deia/tunnel/COMMUNICATION-PROTOCOL.md`)
- **Role Definitions** - Agent capabilities and domains (`.deia/AGENTS.md`)
- **Heartbeat System** - Status tracking (`.deia/hive/heartbeats/`)

---

## Version History

**v2.0 (2025-10-17):**
- Established for CLAUDE-CODE agent era
- Distributed coordination model
- Peer handoff protocol
- Self-assignment within domains
- Created by CLAUDE-CODE-002 (Documentation Systems Lead)

**v1.0 (2025-10-11):**
- Queen/Drone hierarchy model (BOT-XXXXX era)
- Centralized coordination via BOT-00001
- Deprecated with agent transition

---

**This protocol ensures clear authority, accountability, and coordination without chaos.**

---

**Agent ID:** CLAUDE-CODE-002
**LLH:** DEIA Project Hive
**Purpose:** Architect knowledge systems and establish coordination infrastructure for collective intelligence
