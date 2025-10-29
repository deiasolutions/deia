# ⚠️ DEPRECATED PROTOCOL

**THIS DOCUMENT IS DEPRECATED AND ARCHIVED**

**Reason for deprecation:** This protocol has been superseded by the comprehensive master protocol.

**See instead:**  (the authoritative source of truth)

**Archive date:** 2025-10-29
**Archived by:** CLAUDE-CODE-002 (Documentation Systems Lead)

---

# Communication Protocol - Identity & Purpose Declaration

**Status:** Active Protocol
**Date Established:** 2025-10-17
**Authority:** User directive (daaaave-atx)
**Scope:** All agent communications

---

## Requirement: Identity Footer

**All agent communications must end with an identity declaration containing:**

1. **Agent ID** - Your unique identifier (e.g., CLAUDE-CODE-002)
2. **LLH Citizenship** - Your hive/Limited Liability Hive affiliation
3. **Purpose/North Star** - Your role's core mission

---

## Format Template

```markdown
---

**Agent ID:** [AGENT-ID]
**LLH:** [Hive/Project Name]
**Purpose:** [Your core mission/north star]
```

---

## Examples

### Example 1: Integration Specialist

```markdown
---

**Agent ID:** CLAUDE-CODE-002
**LLH:** DEIA Project Hive
**Purpose:** Integrate, deploy, and maintain system coherence across deliverables
```

### Example 2: Documentation Curator

```markdown
---

**Agent ID:** CLAUDE-CODE-004 (Agent DOC)
**LLH:** DEIA Project Hive
**Purpose:** Organize, curate, and preserve the Body of Knowledge for collective learning
```

### Example 3: QA Specialist

```markdown
---

**Agent ID:** CLAUDE-CODE-003 (Agent Y)
**LLH:** DEIA Project Hive
**Purpose:** Ensure quality, reliability, and production-readiness through systematic testing
```

---

## Rationale

**Why this matters:**

1. **Accountability** - Every communication is traceable to a specific agent
2. **Context** - Readers immediately understand the perspective/expertise
3. **Alignment** - Agents regularly state their purpose, maintaining focus
4. **Transparency** - Clear organizational structure visible in all interactions
5. **Governance** - Enforces identity awareness and LLH boundaries

---

## Scope of Application

**Required for:**
- All SYNC messages between agents
- All TASK assignments and responses
- All formal deliverables (specs, reports, documentation)
- All observations and findings
- Session summaries and handoffs

**Optional for:**
- Casual coordination messages
- Quick status updates
- Internal working notes

**When in doubt:** Include the footer. Over-communication is better than under-communication.

---

## Implementation

### For Existing Agents

1. Update your communication templates to include identity footer
2. Review recent communications and add retroactively where critical
3. Update your heartbeat file to include `north_star` field (optional)

### For New Agents

1. Identity footer requirement included in onboarding documentation
2. First communication must establish identity declaration
3. BOOTSTRAP messages should model the pattern

---

## Related Protocols

- **Corpus Callosum Protocol** - Inter-agent messaging format
- **Heartbeat System** - Agent status tracking
- **Activity Logging** - Event telemetry in JSONL

---

## Governance Connection

This protocol embodies principles from:
- **Federalist No. 1** - Transparency in deliberation
- **Federalist No. 2** - Identity and bounded authority
- **LLH Framework** - Limited liability through clear scope

---

**Protocol Status:** Active and enforced
**Next Review:** When onboarding new agent types or expanding to multi-hive coordination

---

**Agent ID:** CLAUDE-CODE-002
**LLH:** DEIA Project Hive
**Purpose:** Integrate, deploy, and maintain system coherence across deliverables
