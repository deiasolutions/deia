---
date: 2025-10-19
from: CLAUDE-CODE-006
type: documentation
status: complete
---

# FBB Hive Communications Structure - Complete Setup

## Question Asked
"Where will FBB save its intra-hive comms, since the tunnel is only for inter-hive comms?"

## Answer
FBB now has its own `.deia/hive/` directory for intra-hive communications, parallel to DEIA Core's structure.

## Communication Architecture

```
HIVE-DEIA-CORE                          HIVE-FBB
(deiasolutions)                         (familybondbot)
─────────────────────────────           ─────────────────────────────

.deia/hive/                             .deia/hive/
├── coordination/  ←INTRA-HIVE→         ├── coordination/
├── responses/                          ├── responses/
├── tasks/                              ├── tasks/
└── heartbeats/                         └── heartbeats/

         ↕                                      ↕
    INTER-HIVE                            INTER-HIVE
         ↕                                      ↕

.deia/tunnel/hive-fbb/ ←────TUNNEL────→ (sends messages here)
```

## File Locations

### Intra-Hive (Within Same Hive)

**DEIA Core agents talking to each other:**
- Location: `deiasolutions/.deia/hive/coordination/`
- Example: `2025-10-19-0852-001-002-SYNC-flight-1-apply-now.md`
- From: AGENT-001 (DEIA Core)
- To: BOT-00002 (DEIA Core)

**FBB agents talking to each other:**
- Location: `familybondbot/.deia/hive/coordination/`
- Example: `2025-10-19-1430-FBB001-FBB002-SYNC-deployment-status.md`
- From: FBB-001 (FBB hive)
- To: FBB-002 (FBB hive)

### Inter-Hive (Between Different Hives)

**FBB → DEIA Core:**
- Location: `deiasolutions/.deia/tunnel/hive-fbb/`
- Example: `2025-10-19-1500-FBB001-CORE-PATTERN-hipaa-encryption.md`
- From: FBB-001 (FBB hive)
- To: Any DEIA Core agent

**DEIA Core → FBB:**
- Location: `deiasolutions/.deia/tunnel/hive-fbb/`
- Example: `2025-10-19-1530-CORE-FBB-ACK-pattern-accepted.md`
- From: DEIA Core agent
- To: FBB hive

## Naming Conventions

### Intra-Hive Messages

**Format:** `YYYY-MM-DD-HHMM-FROM-TO-TYPE-subject.md`

**DEIA Core:**
- Agent IDs: `001`, `002`, `BOT-00002`, etc.
- Example: `2025-10-19-0852-001-002-SYNC-flight-1-apply-now.md`

**FBB:**
- Agent IDs: `FBB-001`, `FBB-CODEX`, `FBB-DEPLOY`, etc.
- Example: `2025-10-19-1430-FBB001-FBB002-SYNC-deployment-status.md`

### Inter-Hive Messages

**Format:** `YYYY-MM-DD-HHMM-HIVE-TO-HIVE-TYPE-subject.md`

**Examples:**
- `2025-10-19-1500-fbb-to-core-PATTERN-hipaa-encryption.md`
- `2025-10-19-1530-core-to-fbb-ACK-pattern-accepted.md`

## Message Types

- **SYNC** - Status updates, coordination
- **TASK** - Task assignments
- **DECISION** - Decisions requiring approval
- **ALERT** - Urgent notifications
- **RESPONSE** - Responses to previous messages
- **PATTERN** - Pattern submissions (inter-hive)
- **ACK** - Acknowledgments (inter-hive)

## How Bees Distinguish Their Messages

### Method 1: Directory Location
- If in `familybondbot/.deia/hive/` → FBB intra-hive
- If in `deiasolutions/.deia/hive/` → DEIA Core intra-hive
- If in `deiasolutions/.deia/tunnel/hive-fbb/` → Inter-hive

### Method 2: Agent ID Prefix
- `001`, `002`, `BOT-0000X` → DEIA Core agents
- `FBB-001`, `FBB-CODEX` → FBB agents
- `LLAMA-001` → Future llama-chatbot hive agents

### Method 3: Filename Convention
- `001-002` → Within DEIA Core
- `FBB001-FBB002` → Within FBB
- `fbb-to-core` → FBB → DEIA Core
- `core-to-fbb` → DEIA Core → FBB

## Created Directories

✅ `familybondbot/.deia/hive/`
✅ `familybondbot/.deia/hive/coordination/`
✅ `familybondbot/.deia/hive/responses/`
✅ `familybondbot/.deia/hive/tasks/`
✅ `familybondbot/.deia/hive/heartbeats/`
✅ `familybondbot/.deia/hive/README.md`

## Example Workflow: Codex Joins FBB

1. **Codex assigned to FBB hive**
   - Agent ID: `FBB-CODEX`
   - Hive: HIVE-FBB

2. **Codex introduces itself (intra-hive)**
   - Creates: `familybondbot/.deia/hive/coordination/2025-10-19-1400-FBB_CODEX-ALL-SYNC-introduction.md`
   - Other FBB agents read from same directory

3. **Codex extracts a pattern (inter-hive)**
   - Drafts: `familybondbot/.deia/patterns_drafts/magic-link-auth.md`
   - Submits: `deiasolutions/.deia/tunnel/hive-fbb/2025-10-19-1430-fbb-to-core-PATTERN-magic-link-auth.md`

4. **DEIA Core reviews and responds (inter-hive)**
   - Creates: `deiasolutions/.deia/tunnel/hive-fbb/2025-10-19-1445-core-to-fbb-ACK-pattern-accepted.md`
   - Integrates into: `deiasolutions/.deia/bok/patterns/security/magic-link-auth.md`

5. **Codex coordinates with another FBB agent (intra-hive)**
   - Creates: `familybondbot/.deia/hive/coordination/2025-10-19-1500-FBB_CODEX-FBB001-SYNC-pattern-submitted.md`

## Summary

**Intra-Hive (Same Hive):**
- `.deia/hive/coordination/` in each project
- Agent-to-agent within same hive
- Agent IDs distinguish hive membership

**Inter-Hive (Between Hives):**
- `.deia/tunnel/hive-{name}/` in parent hive
- Hive-to-hive coordination
- Pattern submissions, knowledge sharing

**Both use same naming convention**, just different locations and agent ID prefixes.

---

**Setup By:** CLAUDE-CODE-006
**Date:** 2025-10-19
**Status:** ✅ Complete
**Next:** Ready for Codex to join FBB hive
