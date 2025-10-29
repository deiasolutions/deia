# HIVE PROTOCOLS MASTER - Unified Source of Truth

**Version:** 1.0
**Effective Date:** 2025-10-29
**Authority:** Q33N (BEE-000) - Meta-Governance
**Status:** 🟢 ACTIVE - SINGLE SOURCE OF TRUTH
**Last Updated:** 2025-10-29T15:30:00Z

---

## ⚠️ CRITICAL NOTICE

**THIS IS THE AUTHORITATIVE SOURCE FOR ALL HIVE PROTOCOLS.**

All other protocol documents are DEPRECATED or supplementary. When there is a conflict between this document and any other protocol document, **THIS DOCUMENT TAKES PRECEDENCE.**

---

## Table of Contents

1. [Governance Model](#governance-model)
2. [Hybrid Communication Model](#hybrid-communication-model)
3. [Task Assignment & Execution Protocol](#task-assignment--execution-protocol)
4. [Bug Fix Protocol](#bug-fix-protocol)
5. [Agent Coordination](#agent-coordination)
6. [Roles and Responsibilities](#roles-and-responsibilities)
7. [File Structure & Locations](#file-structure--locations)
8. [Escalation & Decision-Making](#escalation--decision-making)
9. [Deprecated Systems](#deprecated-systems)
10. [Implementation Checklist](#implementation-checklist)

---

## 1. Governance Model

### Authority Structure

```
Q33N (BEE-000)
├─ Meta-Governance Authority
├─ Sets hive strategy and direction
├─ Assigns tasks to agents
└─ Resolves conflicts and ambiguities

CLAUDE-CODE-001 (Left Brain)
├─ Strategic Planner & Coordinator
├─ Coordinates agent activities
├─ Updates protocols (approved by Q33N)
└─ Enforces protocol compliance

CLAUDE-CODE-002, 003, 004, 005
├─ Specialist agents
├─ Execute assigned tasks
├─ Report results to Q33N
└─ Comply with all active protocols
```

### Decision-Making

- **Strategic decisions** (new features, major changes): Q33N + CLAUDE-CODE-001
- **Protocol decisions** (how we work): Q33N approval required
- **Task decisions** (what to work on): Q33N assigns
- **Technical decisions** (how to implement): Assigned agent + peer review if complex

### Conflict Resolution

1. **Disagreement on task interpretation**: Agent asks Q33N for clarification
2. **Protocol violation by agent**: CLAUDE-CODE-001 logs, reports to Q33N
3. **Disagreement between agents**: Q33N makes final decision
4. **Protocol deemed ineffective**: Agent proposes update to Q33N

---

## 2. Hybrid Communication Model

The hive operates on a **hybrid communication model** with two complementary systems:

### System A: File-Based (Persistent, Auditable)

**Purpose:** Asynchronous, documented task assignment and reporting

**Files:**
- **Assignments:** `.deia/hive/tasks/YYYY-MM-DD-HHMM-SENDER-BOT-XXX-TASK-NAME.md`
- **Responses:** `.deia/hive/responses/deiasolutions/bot-xxx-taskname-complete.md`

**Advantages:**
- ✅ Complete audit trail
- ✅ Asynchronous (no real-time requirement)
- ✅ Self-documenting
- ✅ Easy to reference later
- ✅ Works for complex, multi-step tasks
- ✅ Supports detailed instructions

**Use when:**
- Tasks are complex or multi-step
- Detailed instructions are needed
- Audit trail is important
- Agent will work offline
- Results need to be documented formally

### System B: Direct (Real-Time, Interactive)

**Purpose:** Real-time, direct communication via Bot Commander web tool

**Mechanism:** HTTP/WebSocket endpoints in `chat_interface_app.py`

**Advantages:**
- ✅ Immediate feedback
- ✅ Interactive debugging
- ✅ Real-time task monitoring
- ✅ Quick status checks
- ✅ Supports multi-turn conversation

**Use when:**
- Need immediate response
- Debugging or troubleshooting
- Interactive problem-solving required
- Quick status check needed

**Status:** Currently in development (MVP phase)

### Priority & Relationship

**Rule: File-based system is primary; direct system is supplementary**

- File-based assignments are the official record
- Direct communication can supplement but doesn't replace file-based assignments
- When conflict exists, file-based assignment takes precedence
- All critical tasks MUST have file-based assignment

---

## 3. Task Assignment & Execution Protocol

### Version: 2.0 (Effective 2025-10-26)

This protocol ensures efficient, focused task execution with no wasted effort.

### Phase 1: Assignment (Q33N)

**Q33N creates ONE clear assignment file per bot per task:**

**File location:** `.deia/hive/tasks/YYYY-MM-DD-HHMM-Q33N-BOT-XXX-TASKNAME.md`

**File content template:**
```markdown
# Task Assignment: BOT-XXX - Task Name

**Assigned to:** BOT-XXX
**Assigned by:** Q33N (BEE-000)
**Date:** YYYY-MM-DD
**Priority:** P0/P1/P2/P3
**Deadline:** YYYY-MM-DD (if applicable)

## Task

[SPECIFIC, CLEAR DESCRIPTION OF WHAT TO DO]

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Deliverable

Post response to: `.deia/hive/responses/deiasolutions/bot-xxx-taskname-complete.md`

Use format:
```markdown
# BOT-XXX: Task Name - COMPLETE

**Status:** ✅ COMPLETE / ⚠️ PARTIAL / ❌ BLOCKED

**Results:**
[Specific results, findings, or deliverables]

**Issues:** (if any)
[Any blockers or problems encountered]

**Time spent:** [Hours]
```

## Rules

- **ONE FILE = ONE TASK** (no compound assignments)
- **SPECIFIC INSTRUCTIONS** (no ambiguity)
- **CLEAR SUCCESS CRITERIA** (objective completion)
- **NO REFERENCES TO OTHER BOTS** (coordinate through Q33N only)
- **NO "READ ALSO" sections** (assignment is complete and self-contained)
- **NO WAITING** (if task blocks on another task, Q33N coordinates)

Go.
```

### Phase 2: Execution (Agent)

**Agent reads assignment and executes exactly:**

1. **Read** your assignment file ONLY
2. **Understand** what's being asked (if unclear, ask Q33N)
3. **Execute** exactly what the task says
4. **Document** your work
5. **Post** result in specified format
6. **Done** - wait for next assignment

### Phase 3: Monitoring (Q33N)

**Q33N monitors response files:**

1. **Watch** `.deia/hive/responses/deiasolutions/bot-xxx-*-complete.md` for new files
2. **Review** results and completion status
3. **Resolve** any blockers
4. **Create** next assignment immediately
5. **Maintain** no idle time (always have next task ready)

### What Agents DO NOT Do

❌ Read other bots' task files
❌ Read other bots' response files
❌ Check on other bots' progress
❌ Wait for other bots to finish
❌ Coordinate with other bots directly
❌ Read session logs or status files
❌ Do research beyond assignment scope
❌ Modify or extend the assignment
❌ Do extra work not requested

### Efficiency Gains

This protocol saves time and tokens:
- **Before:** Agent reads 5-10 files for context = 50 tokens + 15 min
- **After:** Agent reads 1 assignment = 5 tokens + 10 min
- **Savings per cycle:** 45 tokens + 5 minutes per agent

---

## 4. Bug Fix Protocol

### Version: 1.0 (Effective 2025-10-18)

**CRITICAL RULE: SEARCH BEFORE FIX**

Failing to check for existing bug fixes wastes 4-5+ hours of duplicate work.

### Mandatory Compliance Checklist

**BEFORE fixing ANY bug, you MUST:**

- [ ] Search `BUG_REPORTS.md` for error message
- [ ] Check `.deia/submissions/pending/bug-*.md` for similar issues
- [ ] Review `.deia/observations/*.md` for recent discoveries
- [ ] Search BOK for platform-specific gotchas
- [ ] Check `.deia/index/QUICK-REFERENCE.md` for proactive warnings
- [ ] Search session logs for historical context
- [ ] Verify bug not already in `PROJECT-STATUS.csv`

### Search Locations (In Priority Order)

1. **BUG_REPORTS.md** - Central bug database
2. **`.deia/submissions/pending/bug-*.md`** - Pending bug documentation
3. **`.deia/observations/*.md`** - Recent discoveries
4. **`bok/platforms/`** - Platform-specific issues (Windows, macOS, Linux)
5. **`.deia/index/QUICK-REFERENCE.md`** - Proactive warnings section
6. **`.deia/sessions/*.md`** - Historical context from past sessions
7. **`PROJECT-STATUS.csv`** - All tracked tasks and bugs

### Known High-Recurrence Bugs

**BUG-004: UnicodeEncodeError with safe_print**
- **Symptom:** `UnicodeEncodeError: 'charmap' codec can't encode`
- **Platform:** Windows terminals with cp1252 encoding
- **Solution location:** `.deia/submissions/pending/bug-safe-print-error-handler-crash.md`
- **Status:** OPEN - Fix documented, implement emergency_print() function
- **Estimated effort:** 30 minutes

### Process

1. **Identify** error message and symptoms
2. **Search** all locations above
3. **If found:** Apply existing fix, DO NOT reimplement
4. **If new:** Document bug BEFORE fixing (use template below)
5. **Fix** the issue
6. **Update** BUG_REPORTS.md and PROJECT-STATUS.csv
7. **Log** activity to bot logs

### New Bug Documentation Template

```markdown
# BUG-XXX: [Clear Title]

**Status:** 🟠 OPEN
**Severity:** Critical/High/Medium/Low
**Reported by:** [Agent ID]
**Date:** YYYY-MM-DD
**Recurrence count:** 1

## Symptoms
[What's broken]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Error Message
```
[Exact error text]
```

## Reproduction Steps
1. Step 1
2. Step 2

## Root Cause
[Technical analysis]

## Solution
[How to fix]

## Files Affected
- file1.py
- file2.py

## Estimated Effort
[Hours]
```

---

## 5. Agent Coordination

### Direct Agent-to-Agent Communication

**RULE: Agents coordinate ONLY through Q33N**

❌ Agent 1 messages Agent 2 directly
❌ Agent 1 reads Agent 2's task file
❌ Agent 1 creates task for Agent 2
✅ Agent 1 reports to Q33N, Q33N creates task for Agent 2

### Agent Roles

#### Q33N (BEE-000) - Meta-Governance Authority
- Sets hive strategy
- Assigns all tasks
- Monitors all progress
- Resolves conflicts
- Updates protocols
- Makes final decisions

#### CLAUDE-CODE-001 - Left Brain / Strategic Planner
- Coordinates agent activities
- Proposes protocol updates
- Enforces protocol compliance
- Reports to Q33N
- Acts as point of escalation for complex decisions

#### CLAUDE-CODE-002 - Documentation Systems Lead
- Creates and maintains documentation
- Coordinates knowledge systems
- Implements Q33N directives
- Reports to Q33N

#### CLAUDE-CODE-003 - QA Specialist
- Tests implementations
- Verifies bug fixes
- Reports on quality
- Reports to Q33N

#### CLAUDE-CODE-004 - Documentation Curator
- Curates Body of Knowledge
- Maintains knowledge index
- Preserves institutional knowledge
- Reports to Q33N

#### CLAUDE-CODE-005 - Full-Stack Generalist & BC Liaison
- Implements agent BC work
- Coordinates external deliverables
- Performs repository-level operations
- Reports to Q33N

### Synchronous Reporting

**All agents report completion to Q33N via:**
- Response files in `.deia/hive/responses/deiasolutions/`
- Activity logs in `.deia/bot-logs/AGENT-*.jsonl`
- Status updates in weekly syncs (if established)

---

## 6. Roles and Responsibilities

### Q33N (BEE-000) Responsibilities

**MUST DO:**
- ✅ Create ONE clear assignment file per bot per task
- ✅ Monitor `.deia/hive/responses/deiasolutions/` for completions
- ✅ Resolve blockers immediately
- ✅ Create next assignments before current tasks complete
- ✅ Enforce protocol compliance
- ✅ Make all strategic decisions
- ✅ Approve all protocol changes

**MUST NOT DO:**
- ❌ Ask agents to read other files
- ❌ Ask agents to coordinate with each other
- ❌ Ask agents to check on other agents
- ❌ Create compound/ambiguous assignments
- ❌ Leave agents idle
- ❌ Expect agents to coordinate themselves

### Agent Responsibilities

**MUST DO:**
- ✅ Read assignment file completely and carefully
- ✅ Execute exactly what assignment says
- ✅ Post result in specified format
- ✅ Report accurately and honestly
- ✅ Follow all active protocols
- ✅ Ask for clarification if assignment is unclear
- ✅ Update activity logs

**MUST NOT DO:**
- ❌ Read other bots' files
- ❌ Check on other bots' progress
- ❌ Modify or extend assignment
- ❌ Do extra work beyond assignment
- ❌ Coordinate with other agents directly
- ❌ Skip protocol requirements
- ❌ Reimplement known bug fixes without searching first

### CLAUDE-CODE-001 Responsibilities

**MUST DO:**
- ✅ Coordinate agent activities
- ✅ Monitor protocol compliance
- ✅ Propose protocol improvements to Q33N
- ✅ Enforce protocols
- ✅ Serve as escalation point for complex decisions
- ✅ Report to Q33N regularly

**MUST NOT DO:**
- ❌ Assign tasks (Q33N does)
- ❌ Override Q33N decisions
- ❌ Unilaterally change protocols
- ❌ Coordinate agent-to-agent work

---

## 7. File Structure & Locations

### Task Assignment & Reporting

```
.deia/hive/tasks/
├── YYYY-MM-DD-HHMM-Q33N-BOT-001-TASKNAME.md (assignment)
├── YYYY-MM-DD-HHMM-Q33N-BOT-002-TASKNAME.md (assignment)
└── ...

.deia/hive/responses/deiasolutions/
├── bot-001-taskname-complete.md (response)
├── bot-002-taskname-complete.md (response)
└── ...
```

### Activity Logging

```
.deia/bot-logs/
├── BOT-00001-activity.jsonl (Q33N activity)
├── CLAUDE-CODE-001-activity.jsonl (coordinator activity)
├── CLAUDE-CODE-002-activity.jsonl (documentation lead)
├── CLAUDE-CODE-003-activity.jsonl (QA specialist)
├── CLAUDE-CODE-004-activity.jsonl (knowledge curator)
└── CLAUDE-CODE-005-activity.jsonl (generalist)
```

### Knowledge Management

```
.deia/
├── BUG_REPORTS.md (central bug database)
├── ACCOMPLISHMENTS.md (what's been done)
├── PROJECT-STATUS.csv (all tracked tasks)
├── AGENTS.md (agent roster)
├── protocols/ (protocol documents)
│   ├── PROTOCOLS-MASTER.md (THIS - authoritative)
│   ├── BUG-FIX-LOOKUP-PROTOCOL.md (bug fixing rules)
│   ├── BEE-000-Q33N-BOOT-PROTOCOL.md (Q33N governance)
│   └── ...
├── index/
│   ├── master-index.yaml (semantic index)
│   └── QUICK-REFERENCE.md (fast lookups)
└── archive/protocols/ (deprecated protocols)
```

---

## 8. Escalation & Decision-Making

### Issue Escalation Path

```
Issue Encountered
    ↓
Agent unable to resolve
    ↓
Agent reports to Q33N
    ↓
Q33N evaluates:
├─ Simple clarification → Q33N provides answer
├─ Complex decision → Q33N + CLAUDE-CODE-001 discuss → Q33N decides
├─ Protocol violation → CLAUDE-CODE-001 enforces
└─ Major issue → Q33N makes decision, updates protocols if needed
```

### Decision Authority

| Decision Type | Authority | Process |
|---|---|---|
| Task assignment | Q33N | Unilateral |
| Technical implementation | Assigned agent | Q33N can request changes |
| Bug fix verification | CLAUDE-CODE-003 | Reports to Q33N |
| Protocol interpretation | Q33N | Provides clarification |
| Protocol changes | Q33N | With input from CLAUDE-CODE-001 |
| Conflict resolution | Q33N | Final decision |

---

## 9. Deprecated Systems

### ❌ DEPRECATED: Corpus Callosum Protocol

**Status:** DEPRECATED (DO NOT USE)

**References in:**
- `AGENTS.md` (outdated)
- `BEE-000-Q33N-BOOT-PROTOCOL.md` (outdated)

**Replacement:** File-based task assignment protocol (Section 3)

### ❌ DEPRECATED: tunnel Directory System

**Status:** DEPRECATED (directory is defunct)

**What was there:** `.deia/tunnel/claude-to-claude/` (no longer used)

**Replacement:** `.deia/hive/tasks/` and `.deia/hive/responses/deiasolutions/`

### ❌ DEPRECATED: hive-coordination-rules.md

**Status:** SEVERELY OUTDATED (do not follow)

**Issues:**
- References defunct Queen-Drone instruction system
- Lists incorrect active agents
- Contains contradictions with current protocols

**Replacement:** This document (PROTOCOLS-MASTER.md)

### ❌ DEPRECATED: Multiple "Queen" Personas

**Status:** CONSOLIDATED - Only Q33N (BEE-000)

**Issue:** Documents referenced both Q33N and Q88N ("Queen of All Queens")

**Resolution:** Q33N is THE authority. No other queen personas exist.

---

## 10. Implementation Checklist

### For Q33N

- [ ] Read this entire document
- [ ] Understand governance model (Section 1)
- [ ] Review task assignment protocol (Section 3)
- [ ] Review bug fix protocol (Section 4)
- [ ] Understand escalation path (Section 8)
- [ ] Begin using file-based assignment format
- [ ] Archive deprecated protocol documents
- [ ] Update AGENTS.md to reference this document

### For All Agents

- [ ] Read this entire document
- [ ] Understand task assignment protocol (Section 3)
- [ ] Follow Role and Responsibilities (Section 6)
- [ ] Comply with bug fix protocol before fixing (Section 4)
- [ ] Use proper file locations (Section 7)
- [ ] Report via response files, not other methods
- [ ] Ask for clarification if assignment unclear
- [ ] Update activity logs

### For CLAUDE-CODE-001

- [ ] Review governance model (Section 1)
- [ ] Understand coordination role (Section 5)
- [ ] Monitor protocol compliance
- [ ] Propose improvements to Q33N
- [ ] Archive deprecated documents
- [ ] Update related documentation

---

## Appendix A: File Templates

### Task Assignment Template

```markdown
# Task Assignment: BOT-XXX - [Task Name]

**Assigned to:** BOT-XXX
**Assigned by:** Q33N (BEE-000)
**Date:** YYYY-MM-DD
**Priority:** P0/P1/P2
**Deadline:** [Date or N/A]

## Task

[Clear, specific description of what to do]

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Expected Deliverable

Post response to: `.deia/hive/responses/deiasolutions/bot-xxx-taskname-complete.md`

Format:
```markdown
# BOT-XXX: [Task Name] - COMPLETE

**Status:** ✅ COMPLETE / ⚠️ PARTIAL / ❌ BLOCKED

**Results:**
[What was accomplished]

**Issues:** (if any)
[Blockers or problems]

**Time spent:** [Hours]
```

Go.
```

### Task Response Template

```markdown
# BOT-XXX: [Task Name] - COMPLETE

**Status:** ✅ COMPLETE / ⚠️ PARTIAL / ❌ BLOCKED
**Completed:** YYYY-MM-DD HH:MM UTC
**Assigned task:** [Link to task file if possible]

## Results

[Specific results, findings, or deliverables]

## Issues (if any)

[Any blockers, problems, or exceptions]

## Time Spent

[Hours: e.g., "2.5 hours"]

## Next Steps (optional)

[If applicable, suggested next work]
```

---

## Appendix B: Protocol Compliance Checklist

**Use this before starting any work:**

### Task Understanding
- [ ] I have read my assignment file completely
- [ ] The assignment is clear and unambiguous
- [ ] I understand success criteria
- [ ] I know where to post my response
- [ ] (If unclear, ask Q33N before proceeding)

### Protocol Compliance
- [ ] I will follow task assignment protocol (Section 3)
- [ ] I will not read other bots' files
- [ ] I will not coordinate with other agents directly
- [ ] I will not do extra work beyond assignment
- [ ] I will post results in specified format

### Bug Fixes (if applicable)
- [ ] I searched BUG_REPORTS.md
- [ ] I checked pending bug submissions
- [ ] I reviewed observations for similar issues
- [ ] I confirmed this is a new bug
- [ ] (If existing fix found, I applied it)

### Documentation
- [ ] I updated my activity log
- [ ] I posted response to correct location
- [ ] I used specified response format
- [ ] I reported accurately and honestly

---

## Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2025-10-29 | CLAUDE-CODE-002 | Initial master protocol consolidation |

---

## Related Documents

- `.deia/AGENTS.md` - Agent roster and roles
- `.deia/protocols/BUG-FIX-LOOKUP-PROTOCOL.md` - Detailed bug fix procedures
- `.deia/BUG_REPORTS.md` - Central bug database
- `.deia/ACCOMPLISHMENTS.md` - Completed work tracking
- `.deia/PROJECT-STATUS.csv` - All tracked tasks and status

---

## Authority & Governance

**Created by:** CLAUDE-CODE-002 (Documentation Systems Lead)
**Approved by:** Q33N (BEE-000)
**Enforced by:** CLAUDE-CODE-001 (Strategic Planner & Coordinator)
**Effective:** 2025-10-29
**Status:** 🟢 ACTIVE - MANDATORY COMPLIANCE

**Questions or clarifications:** Contact Q33N (BEE-000) via task assignment

---

**This is the single, authoritative source of truth for all hive operations.**

**All other protocol documents are supplementary or deprecated.**

**When in doubt, refer to this document.**

---

Last updated: 2025-10-29T15:30:00Z
Version: 1.0
Status: ACTIVE
