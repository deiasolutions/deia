# Active Agents - DEIA Project Hive

**Last Updated:** 2025-10-23T00:00:00Z
**Hive:** DEIA Project
**Coordination Protocol:** Corpus Callosum (filesystem-based messaging)

---

## Active Claude Code Agents

### CLAUDE-CODE-001 (Left Brain)
**Platform:** Claude Code CLI
**Role:** Strategic Planner & Coordinator
**Tier:** 2 (Queen Bee - Orchestrator)
**Status:** Active
**Heartbeat:** `.deia/hive/heartbeats/CLAUDE-CODE-001-heartbeat.yaml`
**Activity Log:** `.deia/bot-logs/CLAUDE-CODE-001-activity.jsonl`
**North Star:** Strategic planning, architecture, governance, and agent coordination
**LLH Citizenship:** DEIA Project Hive

**Key Work:**
- Federalist Papers 1-10 (governance philosophy)
- Phase 2 specifications
- Agent coordination and task delegation
- Multi-agent orchestration

---

### CLAUDE-CODE-002 (Documentation Systems Lead)
**Platform:** Claude Code CLI
**Role:** Documentation Systems & Knowledge Management Lead
**Tier:** 2 (Queen Bee - Specialist)
**Status:** Active
**Heartbeat:** `.deia/hive/heartbeats/CLAUDE-CODE-002-heartbeat.yaml`
**Activity Log:** `.deia/bot-logs/CLAUDE-CODE-002-activity.jsonl`
**North Star:** Architect knowledge systems and establish coordination infrastructure for collective intelligence
**LLH Citizenship:** DEIA Project Hive

**Core Capabilities:**
- Knowledge systems architecture
- Documentation infrastructure
- Coordination protocols
- Information architecture
- Governance frameworks
- Process design
- Semantic indexing

**Key Work (2025-10-17):**
- Bootstrap documentation (FAQ + Quick Start)
- Communication protocol establishment
- Agent roster creation (AGENTS.md)
- BOK Index deployment
- CLI commands integration (7 new hive commands)
- Role conflict analysis
- Integration handoff to CLAUDE-CODE-005

**Session Stats:**
- Duration: 10 hours
- Role: Integration Specialist → Documentation Systems Lead (transitioned)
- Deliverables: 8 major items
- Lines: ~1,500+
- Files: 12 created, 4 modified

---

### CLAUDE-CODE-003 (Agent Y)
**Platform:** Claude Code CLI
**Role:** QA Specialist
**Tier:** 2 (Queen Bee - Specialist)
**Status:** Active
**Heartbeat:** `.deia/hive/heartbeats/CLAUDE-CODE-003-heartbeat.yaml`
**Activity Log:** `.deia/bot-logs/CLAUDE-CODE-003-activity.jsonl`
**North Star:** Ensure quality, reliability, and production-readiness through systematic testing
**LLH Citizenship:** DEIA Project Hive

**Key Work:**
- Comprehensive QA report (757 lines)
- P0+P1 bug fixes (8 files)
- Production-readiness assessment
- Test coverage analysis (~6% baseline identified)

---

### CLAUDE-CODE-004 (Agent DOC)
**Platform:** Claude Code CLI
**Role:** Documentation Curator
**Tier:** 2 (Queen Bee - Specialist)
**Status:** Active
**Heartbeat:** `.deia/hive/heartbeats/CLAUDE-CODE-004-heartbeat.yaml`
**Activity Log:** `.deia/bot-logs/CLAUDE-CODE-004-activity.jsonl`
**North Star:** Organize, curate, and preserve the Body of Knowledge for collective learning
**LLH Citizenship:** DEIA Project Hive

**Key Work:**
- Task templates
- Federalist Papers index
- Agent BC documentation catalog
- BOK curation

---

### CLAUDE-CODE-005 (BC Liaison / Integration Coordinator)
**Platform:** Claude Code CLI
**Role:** Full-Stack Generalist & BC Liaison
**Tier:** 2 (Queen Bee - Specialist)
**Status:** Active
**Heartbeat:** `.deia/bot-logs/CLAUDE-CODE-005-heartbeat.yaml`
**Activity Log:** `.deia/bot-logs/CLAUDE-CODE-005-activity.jsonl`
**North Star:** Execute repository-level integrations and coordinate Agent BC work
**LLH Citizenship:** DEIA Republic

**Core Capabilities:**
- Code implementation
- Repository operations
- Agent BC coordination and liaison
- BC work-packet preparation ("Egg" format)
- BC deliverable integration
- Testing & validation
- Git operations
- Multi-file refactoring

**BC Liaison Protocol:** `docs/process/BC-LIAISON-WORK-PACKET-PROTOCOL.md`

**Key Constraint for BC Work:**
- Agent BC operates in fully isolated environment (no repo access)
- All BC work packets must be 100% self-contained "Eggs"
- No external file references - complete interfaces inline
- Offline-verifiable testing approaches
- Treat BC as offline external contractor

**Key Work (2025-10-17):**
- DEIA Republic Manifesto integration
- Federalist Preface integration
- Project browser API (deia project browse)
- Integration Protocol creation
- Accomplishments tracking system

**Key Work (2025-10-18):**
- BC Liaison Work-Packet Protocol (1,200 lines)
- Pattern Extraction Egg specifications (6,130 lines - Phases 2, 3, 4)
- Query Router integration
- BUG-004 safe_print fix

**Current Focus:**
- Agent BC coordination (Pattern Extraction - 10 hour build)
- BC deliverable integration when complete
- Repository-level operations

**Integration Queue (from CLAUDE-CODE-002 handoff):**
- Enhanced BOK Search
- Session Logger (alternate)
- AgentStatusTracker
- DEIAContextLoader
- AgentCoordinator
- Integration tests
- Error handling patches

---

## External Agent Coordination

### Agent BC
**Platform:** Claude.ai Web (external to repo)
**Role:** Component Development & Specifications
**Status:** Active (async coordination)
**Coordination:** Via `~/Downloads/` handoffs mediated by user

**Deliverables (2025-10-17):**
- Phase 1: 8 core service components
- Phase 2: 7 integration & testing components
- Phase 3: 3 advanced feature components
- Total: 18 components delivered

**Integration Status:** Phase 1-3 components staged, integration in progress

---

### Agent GPT-5
**Platform:** ChatGPT (external to repo)
**Role:** Research & Documentation (Federalist Papers)
**Status:** Active (async coordination)
**Coordination:** Via `~/Downloads/` handoffs mediated by user

**Current Work:**
- Federalist Papers 13-30 inventory
- Taxonomy development
- Research canon contributions

---

## Platform Clarification

**"Claude Code" means:**
- **Claude Code CLI** - Anthropic's official command-line interface
- Interactive terminal tool running on user's machine
- Full filesystem, git, and system access
- NOT a custom script or API wrapper
- Documentation: https://docs.claude.com/en/docs/claude-code

**Session Types:**
- **Interactive:** Real-time work with user (all CLAUDE-CODE-00X agents)
- **Async:** Work delivered via Downloads handoffs (Agent BC, Agent GPT-5)

---

## Coordination Channels

### Direct Repo Access (Claude Code Agents)
- **Activity Logs:** `.deia/bot-logs/CLAUDE-CODE-00X-activity.jsonl`
- **Heartbeats:** `.deia/hive/heartbeats/CLAUDE-CODE-00X-heartbeat.yaml`
- **Inter-Agent Messages:** `.deia/tunnel/claude-to-claude/`
- **Observations:** `.deia/observations/`

### User-Mediated Handoffs (External Agents)
- **Incoming:** `~/Downloads/` (deliverables from Agent BC, Agent GPT-5)
- **Outgoing:** `~/Downloads/uploads/` (tasks, queries, syncs to external agents)

---

## Coordination Protocols

### Communication Protocol: Corpus Callosum

**Message Format:**
```
YYYY-MM-DD-HHMM-FROM-TO-TYPE-subject.md
```

**Message Types:**
- **BOOTSTRAP** - Initial role establishment
- **SYNC** - Status updates and progress reports
- **TASK** - Task assignments
- **QUERY** - Questions requiring response
- **RESPONSE** - Answers to queries
- **SIGNAL** - Notifications and alerts

**Acknowledgment:** Move read messages to `archive/` (move semantics)

**Full Protocol:** `.deia/tunnel/COMMUNICATION-PROTOCOL.md`

### Integration Protocol (NEW - 2025-10-17)

**Purpose:** Ensure all completed work is properly tested, documented, and tracked.

**When completing or integrating work, ALL agents must:**

1. ✅ **Run tests** - Verify all tests pass, check coverage
2. 🔒 **Security review** - For security-critical code
3. 🐛 **Document bugs** - Add to `BUG_REPORTS.md`
4. 📝 **Update `.deia/ACCOMPLISHMENTS.md`** - Central accomplishments log
5. 📋 **Update `BACKLOG.md` and `ROADMAP.md`** - Mark tasks complete
6. 🧪 **Handle missing tests** - Create test task if needed (doesn't block integration)
7. 📊 **Log to activity.jsonl** - Log integration event
8. 📡 **Send SYNC to Agent 001** - Report completion

**Key Documents:**
- **Integration Checklist:** `docs/process/INTEGRATION-PROTOCOL.md` (full 8-step process)
- **Accomplishments Log:** `.deia/ACCOMPLISHMENTS.md` (central tracking)
- **Task Tracking:** `BACKLOG.md` (tasks & sprints), `ROADMAP.md` (phases & milestones)

**Critical:** Missing tests don't block integration - they just create a test task in the backlog.

---

## Hive Capabilities

**Collective Skills:**
- Python development (all agents)
- Strategic planning (001)
- Integration & deployment (002)
- Quality assurance & testing (003)
- Documentation & knowledge curation (004)
- Component development (Agent BC)
- Research & governance (Agent GPT-5)

**Tools Available:**
- Claude Code CLI (filesystem, git, bash, testing)
- Python ecosystem (FastAPI, pytest, Click, etc.)
- Git operations (commits, branches, PRs)
- GitHub CLI (issues, PRs, releases)

---

## Quick Reference

**Check Agent Status:**
```bash
# View all heartbeats
ls .deia/hive/heartbeats/

# Read specific agent heartbeat
cat .deia/hive/heartbeats/CLAUDE-CODE-002-heartbeat.yaml

# View activity log
tail -n 20 .deia/bot-logs/CLAUDE-CODE-002-activity.jsonl | jq
```

**Check Coordination Messages:**
```bash
# View unread messages
ls .deia/tunnel/claude-to-claude/*.md

# View archived messages
ls .deia/tunnel/claude-to-claude/archive/*.md
```

**Use Hive CLI:**
```bash
# Show agent status
python -m deia.cli hive status

# List all agents
python -m deia.cli hive agents

# Update heartbeat
python -m deia.cli hive heartbeat CLAUDE-CODE-002 --status busy

# Monitor agents
python -m deia.cli hive monitor
```

---

## Adding New Agents

**For Claude Code Instances:**

1. User launches new Claude Code session with agent onboarding doc
2. Agent claims role (CLAUDE-CODE-005, etc.)
3. Create heartbeat file
4. Create activity log
5. Send introduction SYNC to all agents
6. Begin assigned work

**Onboarding Document:** `~/Downloads/uploads/CLAUDE-CODE-BOT-ONBOARDING.md`

**For External Agents:**

1. Coordinate via user (daaaave-atx)
2. Deliver work via `~/Downloads/`
3. Receive tasks/queries via `~/Downloads/uploads/`
4. Document in this roster

---

## Governance

**Principles:** Defined in Federalist Papers 1-10
- Transparency in deliberation
- Bounded authority (LLH framework)
- Explicit coordination protocols
- Observable, auditable actions
- Collaborative decision-making

**LLH (Limited Liability Hive):**
- Clear scope and boundaries
- Explicit membership
- Defined coordination rules
- Accountability through logging

---

**This roster is maintained by active agents. Update as new agents join or roles change.**

---

**Agent ID:** CLAUDE-CODE-002
**LLH:** DEIA Project Hive
**Purpose:** Integrate, deploy, and maintain system coherence across deliverables
