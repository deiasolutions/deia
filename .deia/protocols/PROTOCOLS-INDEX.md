# DEIA Protocols Index

**Master index of all operational protocols** governing DEIA hive behavior.

Reference this document when:
- Starting work in DEIA
- Looking for governance guidance
- Questions about how something should be done
- Uncertainty about procedure

---

## Active Protocols

### Core Governance

| Protocol | Purpose | Version | Updated |
|----------|---------|---------|---------|
| **BEE-000-Q33N-BOOT-PROTOCOL.md** | Q33N (meta-governance authority) boot and role definition | v1.0 | 2025-10-23 |
| **AGENT-COMMUNICATION-CADENCE-v1.0.md** | How agents communicate, report status, and coordinate | v1.0 | 2025-10-17 |

### Operational Procedures

| Protocol | Purpose | Version | Updated |
|----------|---------|---------|---------|
| **CLAUDE-CODE-SETTINGS-PROTOCOL.md** | Configure Claude Code permissions for autonomous bot operation | v1.0 | 2025-10-31 |
| **TIMESTAMP-PROTOCOL.md** | Standard timestamp format and logging conventions | v1.0 | 2025-10-18 |
| **BUG-FIX-LOOKUP-PROTOCOL.md** | How to discover, report, and track bugs | v1.0 | 2025-10-17 |
| **PROTOCOL-agent-instruction-consistency.md** | How agents handle instruction conflicts and deviations from guides | v1.0 | 2025-10-25 |

---

## Protocol Hierarchy

```
BEE-000-Q33N-BOOT-PROTOCOL
├── AGENT-COMMUNICATION-CADENCE (how to operate)
├── PROTOCOL-agent-instruction-consistency (when to ask questions)
├── TIMESTAMP-PROTOCOL (formatting standards)
└── BUG-FIX-LOOKUP-PROTOCOL (handling issues)
```

---

## When to Consult Each Protocol

### Setting Up a New Hive
1. Read **CLAUDE-CODE-SETTINGS-PROTOCOL.md** - Configure Claude Code permissions
2. Create `.claude/settings.local.json` with recommended configuration
3. Commit to git and notify team

### Starting Work in a Hive
1. Read **BEE-000-Q33N-BOOT-PROTOCOL.md** - Understand Q33N authority and DEIA structure
2. Read **AGENT-COMMUNICATION-CADENCE-v1.0.md** - Learn how to operate and report

### Receiving Instructions
1. Check your **bootcamp guide** (BOT-001-BOOTCAMP-COMPLETE.md, etc.)
2. If instructions differ from bootcamp, follow **PROTOCOL-agent-instruction-consistency.md**
3. Ask clarifying questions using the escalation pattern

### Finding a Bug
1. Follow **BUG-FIX-LOOKUP-PROTOCOL.md** for reporting

### Logging and Formatting
1. Follow **TIMESTAMP-PROTOCOL.md** for all timestamps
2. Follow **AGENT-COMMUNICATION-CADENCE-v1.0.md** for status reports

### Claude Code Not Prompting (Or Over-Prompting)
1. Check **CLAUDE-CODE-SETTINGS-PROTOCOL.md** - Diagnose settings issues
2. Verify `.claude/settings.local.json` exists and is readable
3. Review allow/deny/ask lists for your operations

---

## Key Principles (Across All Protocols)

- **Guides are source of truth** - Follow bootcamp guides as the primary reference
- **Questions are encouraged** - Raising inconsistencies protects the system
- **Consistency matters** - Deviations from established procedures should be intentional and documented
- **Transparency** - Log decisions, changes, and reasoning
- **Federalism** - Each agent has autonomy within established protocols

---

## Adding New Protocols

When creating a new protocol:

1. **File it in `.deia/protocols/`** with `PROTOCOL-` prefix or specific name
2. **Add to this index** with purpose, version, and date
3. **Link from relevant documents** (bootcamp guides, task assignments)
4. **Reference existing protocols** it builds on or relates to
5. **Notify Q33N** of new protocol in status report

---

## Protocol Change History

| Date | Protocol | Change | Authority |
|------|----------|--------|-----------|
| 2025-10-31 | CLAUDE-CODE-SETTINGS-PROTOCOL.md | Created - new recommended practice for hive setup | Q33N |
| 2025-10-25 | PROTOCOL-agent-instruction-consistency.md | Created | BOT-001 suggestion, Q33N approval |

---

## Discovery & Linking

**Current Issue:** Protocols are indexed here but not linked from bootcamp guides.

**Recommended Fix:** Update bootcamp guides to reference `.deia/protocols/PROTOCOLS-INDEX.md` in the "Critical Principles" section or link PROTOCOL-agent-instruction-consistency.md from the "If You Get Stuck" section.

**Example Addition to Bootcamp:**
```
If instructions conflict with this guide:
- See .deia/protocols/PROTOCOL-agent-instruction-consistency.md
- Ask Q33N for clarification
- This is correct behavior, not an error
```

## Questions?

- Q33N approves protocol updates
- Contact Q33N if you believe a protocol is outdated
- See PROTOCOL-agent-instruction-consistency.md for instruction conflict resolution
- All protocols discoverable via this index

---

**Last Updated:** 2025-10-31
**Maintained By:** Q33N (BEE-000)
**Suggestion:** Link to `.deia/protocols/PROTOCOLS-INDEX.md` from all bootcamp guides
