# Master Librarian Service - Specification (WIP)

**Status:** Work in Progress
**Created:** 2025-10-16
**Context:** Emerged from information architecture work during Q33N deployment session
**Priority:** Medium
**Dependencies:** Query tool MVP (✅ complete), Master index YAML (✅ complete)

---

## Context: Why We Need This

During today's session (2025-10-16), we hit a critical realization:

> "we now have more info than one AI can ingest and hold in context... Maybe we consider having a research assistant role... a master librarian"

**The Problem:**
- 18+ documents in Global Commons, growing constantly
- Recurring patterns (Windows UTF-8 bug happened 20+ times, wasted 4-5 hours cumulative)
- AI agents can't hold all context at once
- No proactive injection of relevant docs before mistakes happen

**What We Built So Far:**
- ✅ `master-index.yaml` - YAML source of truth with rich metadata
- ✅ `query.py` - MVP CLI for keyword search
- ✅ Practical taxonomy with 7 content clusters
- ✅ Query patterns mapping user mental models to documents

**What's Missing:**
A service that actively monitors conversations, recognizes patterns, and injects relevant context **before** the same mistake happens for the 21st time.

---

## Vision: The Master Librarian

**Role:** Knowledge guardian and proactive assistant for DEIA ecosystem

**Core Capabilities:**
1. **Query Response** - Answer "do we have something about X?"
2. **Proactive Injection** - Detect patterns and inject docs before mistakes
3. **Usage Tracking** - Measure doc utility, identify gaps
4. **Index Maintenance** - Keep cross-links strong, metadata current
5. **Commons Curation** - Suggest new entries, flag outdated ones

**Operating Modes:**
- **Passive Mode:** Responds to explicit queries (like current `query.py`)
- **Active Mode:** Monitors conversations, triggers injections
- **Curator Mode:** Maintenance tasks (overnight batch jobs)

---

## Specification Shell

### 1. Architecture

**Service Type:** [ ]
- [ ] CLI tool (extension of `query.py`)
- [ ] Long-running daemon (monitors conversations)
- [ ] Hybrid (CLI + optional daemon)
- [ ] MCP server integration

**Deployment:**
- [ ] Installed to `~/.deia/librarian/`
- [ ] Source in `src/deia/librarian/`
- [ ] Config in `~/.deia/librarian/config.json`

**Data Sources:**
- [ ] Master index: `.deia/index/master-index.yaml`
- [ ] Usage logs: `.deia/librarian/usage.jsonl`
- [ ] Session transcripts: `.deia/sessions/*.md` (opt-in)

**Dependencies:**
- Python 3.8+
- PyYAML (already in project)
- watchdog (for file monitoring, optional)
- [ ] Other? (TBD)

---

### 2. Core Functions

#### 2.1 Query Interface

**Extend existing `query.py` with:**
- [ ] Fuzzy matching (typo tolerance)
- [ ] Multi-keyword AND/OR logic
- [ ] Filter by urgency level
- [ ] Filter by platform (Netlify, Windows, etc.)
- [ ] Filter by audience (beginner, advanced)
- [ ] Recent docs (last 7/30 days)
- [ ] Most referenced docs

**Query Patterns to Support:**

```bash
# Current (MVP)
query.py "DNS not working"
query.py --platform netlify

# Proposed extensions
query.py "deployment failed" --urgency critical
query.py "python encoding" --platform windows
query.py "coordination" --recent 7d
query.py --most-referenced
query.py "AI" AND "governance" --audience advanced
```

---

#### 2.2 Proactive Injection

**Trigger Patterns:**

Define regex/keyword patterns that, when detected in conversation transcripts, trigger document injection.

**Example triggers:**

```yaml
triggers:
  - pattern: "deployment.*failed|outage|nuclear.*option"
    docs: ["bok-direct-to-prod", "case-nuclear-option"]
    urgency: critical
    message: "⚠️ Detected deployment discussion. Relevant safety docs:"

  - pattern: "windows.*python.*encoding|charmap.*codec|unicode.*error"
    docs: ["bok-windows-python-utf8"]
    urgency: high
    message: "⚠️ Windows UTF-8 encoding issue detected (seen 20+ times). Use this fix:"

  - pattern: "DNS.*not.*resolving|nameserver.*issue"
    docs: ["case-dns-outage", "bok-dns-registrar-confusion"]
    urgency: high
    message: "🔍 DNS troubleshooting resources:"
```

**Implementation Options:**
- [ ] Real-time monitoring (daemon watches `.deia/sessions/`)
- [ ] Post-session analysis (batch job after session ends)
- [ ] Claude Code hook integration (`.claude/hooks/`)

---

#### 2.3 Usage Tracking

**Metrics to Capture:**

```jsonl
# .deia/librarian/usage.jsonl
{"ts": "2025-10-16T23:45:00Z", "query": "deployment failed", "results": 3, "clicked": "bok-direct-to-prod"}
{"ts": "2025-10-16T23:50:00Z", "injection": "auto", "trigger": "windows-utf8", "doc": "bok-windows-python-utf8", "session": "20251016-session"}
```

**Analytics to Generate:**
- Most queried topics
- Most injected docs (measure pattern recurrence)
- Zero-result queries (identify gaps)
- Docs never accessed (candidates for archive/update)

---

#### 2.4 Index Maintenance

**Automated Tasks:**
- [ ] Validate all `doc.path` entries exist
- [ ] Check for broken cross-references
- [ ] Detect new files in `docs/`, `bok/` not in index
- [ ] Flag docs not updated in 90+ days
- [ ] Suggest related docs based on keyword overlap

**Report Format:**

```bash
deia librarian audit

DEIA Librarian Audit Report
============================
Index version: 1.0
Last updated: 2025-10-16

Issues Found:
⚠️  3 documents missing from index
⚠️  1 broken path reference
⚠️  2 docs not accessed in 90+ days

Suggestions:
💡 Add cross-link: bok-direct-to-prod → case-nuclear-option (keyword overlap: 85%)
💡 Update summary: case-dns-outage (last updated 45 days ago)
```

---

#### 2.5 Commons Curation

**Suggest New Entries:**
- Monitor session logs for new incident reports
- Detect repeated patterns not yet documented
- Flag high-value findings (like GPT-5 task affinity discovery)

**Workflow:**
```bash
deia librarian suggest

DEIA Librarian - New Entry Suggestions
=======================================
Based on recent activity:

📋 Suggested Case Study:
   Title: "Filesystem Coordination Pattern for Multi-Agent Workflows"
   Source: Session 2025-10-16 (Q33N deployment)
   Reason: Novel pattern, successful execution, reusable
   Template: docs/patterns/coordination/

📋 Suggested BOK Entry:
   Title: "Windows Python UTF-8 Console Encoding Fix"
   Source: Recurred 20+ times across sessions
   Reason: High cost pattern (4-5 hours cumulative)
   Template: bok/platforms/windows/
```

---

### 3. User Interface

#### 3.1 CLI Commands

```bash
# Query
deia librarian query "DNS not working"
deia librarian search "deployment" --urgency critical

# Stats
deia librarian stats
deia librarian top-docs
deia librarian gaps  # zero-result queries

# Maintenance
deia librarian audit
deia librarian suggest
deia librarian update  # refresh index from filesystem

# Daemon (optional)
deia librarian watch start
deia librarian watch stop
deia librarian watch status
```

#### 3.2 Integration Points

**Claude Code Hooks:**
```bash
# .claude/hooks/user-prompt-submit
# Trigger librarian injection before Claude responds
deia librarian inject --session-file .deia/sessions/current.md --context last-10-lines
```

**MCP Server (Future):**
```json
{
  "mcpServers": {
    "deia-librarian": {
      "command": "deia",
      "args": ["librarian", "mcp-server"]
    }
  }
}
```

---

### 4. Configuration

**Example Config:** `~/.deia/librarian/config.json`

```json
{
  "version": "1.0",
  "index_path": ".deia/index/master-index.yaml",
  "usage_log": ".deia/librarian/usage.jsonl",
  "triggers_enabled": true,
  "triggers_file": ".deia/librarian/triggers.yaml",
  "watch_sessions": true,
  "session_dir": ".deia/sessions",
  "inject_threshold": 0.7,
  "audit_frequency": "weekly",
  "retention": {
    "usage_logs": "90d",
    "injection_logs": "30d"
  }
}
```

---

### 5. Implementation Phases

#### Phase 1: Enhanced Query Tool (Extend MVP)
**Status:** Foundation complete (current `query.py`)
**Next Steps:**
- [ ] Add fuzzy matching
- [ ] Multi-keyword AND/OR logic
- [ ] Filter by urgency/platform/audience
- [ ] Usage tracking (log queries)

**Estimated Effort:** Small (1-2 sessions)
**Deliverable:** `deia librarian query` command

---

#### Phase 2: Proactive Injection System
**Dependencies:** Phase 1 complete
**Next Steps:**
- [ ] Define trigger patterns YAML
- [ ] Implement pattern matching engine
- [ ] Session transcript monitoring (opt-in)
- [ ] Injection logging

**Estimated Effort:** Medium (2-3 sessions)
**Deliverable:** `deia librarian watch` daemon

---

#### Phase 3: Index Maintenance & Curation
**Dependencies:** Phase 1 complete
**Next Steps:**
- [ ] Audit functionality (validate paths, detect gaps)
- [ ] Suggestion engine (new entries, cross-links)
- [ ] Scheduled maintenance tasks

**Estimated Effort:** Medium (2-3 sessions)
**Deliverable:** `deia librarian audit` and `suggest` commands

---

#### Phase 4: Advanced Features
**Dependencies:** Phases 1-3 complete
**Next Steps:**
- [ ] MCP server integration
- [ ] Claude Code hook integration
- [ ] Analytics dashboard
- [ ] Multi-repo support

**Estimated Effort:** Large (4-6 sessions)
**Deliverable:** Full-featured knowledge management system

---

## Next Steps for This Spec

### Immediate (Complete the Spec)
- [ ] **Decision:** Service architecture (CLI vs daemon vs hybrid)
- [ ] **Decision:** Integration strategy (hooks vs MCP vs both)
- [ ] **Define:** Trigger patterns YAML schema
- [ ] **Define:** Usage log schema
- [ ] **Design:** Injection mechanism (how does Claude see the suggestion?)
- [ ] **Prototype:** Fuzzy matching algorithm
- [ ] **Document:** Security considerations (session transcript access)

### Short-Term (Start Phase 1)
- [ ] Extend `query.py` with filters and fuzzy matching
- [ ] Add usage logging to query tool
- [ ] Create `deia librarian` CLI entry point
- [ ] Test with real queries from today's session

### Long-Term (Full Vision)
- [ ] Build trigger pattern engine
- [ ] Implement session monitoring
- [ ] Create maintenance automation
- [ ] Integrate with Claude Code hooks

---

## Open Questions

1. **Injection Mechanism:** How does the Librarian inject context into Claude Code?
   - Option A: Pre-populate context via hooks (`.claude/hooks/user-prompt-submit`)
   - Option B: Write suggestion to stdout (relies on Claude seeing it)
   - Option C: Modify session file in-place (risky)

2. **Privacy:** Session transcripts may contain sensitive info. How to handle?
   - Option A: Opt-in only (explicit user permission)
   - Option B: Sanitized analysis (strip PII before processing)
   - Option C: Local-only, never shared

3. **Performance:** Real-time monitoring could be expensive. How to optimize?
   - Option A: Batch processing (analyze after session ends)
   - Option B: Incremental updates (monitor only new lines)
   - Option C: Sampling (check every N lines, not every line)

4. **Multi-Repo:** Should Librarian work across multiple DEIA projects?
   - Option A: Per-project index (each repo has own librarian)
   - Option B: Global index (one librarian, all projects)
   - Option C: Hybrid (local + shared Commons index)

---

## References

**Completed Work (Today's Session):**
- `.deia/index/master-index.yaml` - Source of truth index
- `.deia/index/taxonomy-practical.md` - Taxonomy decisions
- `.deia/librarian/query.py` - MVP query tool
- `bok/platforms/windows/python-console-utf8-encoding.md` - Example BOK entry
- `docs/global-commons/observations/gpt5-task-type-affinity.md` - Example observation

**Related Concepts:**
- Pheromone coordination (Federalist Papers 1, 12)
- Stigmergy (indirect coordination through environment)
- The Mycelium (knowledge substrate, Federalist Paper 11 proposed)
- Proactive context injection (preventing repeated mistakes)

---

## License & Ownership

**License:** CC BY 4.0 International
**Copyright:** © 2025 DEIA Global Commons
**Authors:** Claude (CLAUDE-CODE-001), daaaave-atx

---

**Last Updated:** 2025-10-16T19:45:00Z
**Next Review:** TBD (after backlog prioritization)
