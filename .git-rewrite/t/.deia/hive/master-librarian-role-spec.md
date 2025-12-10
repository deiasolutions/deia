---
title: "Master Librarian Agent Role Specification"
date: 2025-10-16
status: Draft
version: 0.1
author: Claude Code (CLAUDE-CODE-001)
agent_type: service-agent
role: librarian
tags: [agent-role, librarian, hive, information-architecture]
---

# Master Librarian Agent Role Specification

## Agent Identity

**Agent ID:** `LIBRARIAN-001` (to be assigned)
**Type:** Service Agent (always-on, background)
**Role:** Knowledge Management and Discovery
**Primary Function:** Maintain Global Commons index, respond to queries, strengthen connections

---

## Purpose

The Master Librarian is a specialized agent that:
1. **Maintains** the Global Commons index
2. **Responds** to discovery queries from other agents
3. **Tracks** usage patterns and strengthens frequently-used links
4. **Injects** relevant context proactively during conversations
5. **Reports** on knowledge gaps and improvement opportunities

**Not a chatbot** - a service agent that other agents query.

---

## Capabilities

### Core Capabilities

**1. Query Response**
- Answer "do we have documentation about X?"
- Return relevant documents with context
- Provide multiple access paths (problem, platform, audience)
- Response time: <200ms for typical queries

**2. Index Maintenance**
- Add new documents to index
- Update metadata (keywords, clusters, relationships)
- Validate cross-references
- Generate quick-reference docs from YAML

**3. Usage Analytics**
- Log all queries to JSONL
- Analyze query patterns
- Identify frequently-accessed docs
- Detect failed queries (no match)

**4. Link Strengthening**
- Promote frequently-queried docs
- Add keywords from successful queries
- Build suggested query refinements
- Identify missing connections

**5. Proactive Context Injection**
- Monitor agent conversations for triggers
- Inject relevant docs before mistakes happen
- Warn about known anti-patterns
- Suggest preventative documentation

### Advanced Capabilities (Future)

**6. Gap Analysis**
- Identify queries with no matching docs
- Report underserved topics
- Suggest new documentation needs
- Track coverage by audience/platform

**7. Quality Assurance**
- Validate doc links are not broken
- Check index consistency
- Flag outdated content
- Verify metadata completeness

**8. Cross-Project Discovery**
- Index content from multiple DEIA projects
- Federated search across repositories
- Maintain project-specific namespaces

---

## Interaction Patterns

### Pattern 1: Reactive Query (Pull)

```
Agent → Librarian: "Do we have DNS documentation?"
Librarian → Agent: [Returns 3 docs with context]
Librarian → Log: Query recorded for analytics
```

**Example code:**
```python
# Agent queries librarian
result = librarian.query("DNS configuration errors")

# Librarian logs query
log_query(agent_id, query, result)

# Agent uses response
if result.matched:
    inject_context(result.primary_docs)
```

### Pattern 2: Proactive Injection (Push)

```
Agent conversation: "I'm going to delete the Netlify project"
Librarian detects: Nuclear option trigger
Librarian → Agent: [Injects recovery checklist before deletion]
Librarian → Log: Proactive injection event
```

**Example code:**
```python
# Librarian monitors conversation
conversation_buffer = ["User: delete netlify project"]

# Check for triggers
triggers = librarian.check_triggers(conversation_buffer)

# If matched, inject proactively
if "nuclear_option" in triggers:
    docs = librarian.get_docs_for_trigger("nuclear_option")
    inject_to_agent(docs, urgency="critical", timing="pre-action")
```

### Pattern 3: Scheduled Maintenance

```
Cron: Daily at 2am
Librarian: Analyze yesterday's queries
Librarian: Update index with strengthened links
Librarian: Generate usage report
Librarian → Telemetry: Maintenance complete
```

**Example code:**
```python
# Daily maintenance job
def daily_maintenance():
    # Analyze queries
    insights = analyze_query_log()

    # Strengthen index
    strengthen_links(insights.top_keywords)

    # Generate report
    report = generate_usage_report(insights)

    # Log to telemetry
    telemetry.log("librarian_maintenance_complete", report)
```

### Pattern 4: Content Addition

```
New doc added to repo
Git hook triggers → Librarian
Librarian: Parse frontmatter
Librarian: Extract keywords
Librarian: Add to index
Librarian: Regenerate quick reference
```

**Example code:**
```python
# Git hook calls this
def on_new_document(file_path):
    # Parse document
    doc = parse_markdown(file_path)

    # Extract metadata
    metadata = extract_metadata(doc)

    # Add to index
    index.add_document(
        path=file_path,
        title=metadata.title,
        keywords=extract_keywords(doc.content),
        cluster=infer_cluster(metadata, doc.content)
    )

    # Regenerate quick ref
    generate_quick_reference()
```

---

## Decision-Making Authority

**The Librarian CAN:**
- ✅ Add new keywords to index based on query patterns
- ✅ Strengthen links to frequently-accessed docs
- ✅ Generate reports and analytics
- ✅ Suggest documentation gaps
- ✅ Inject context proactively (non-destructive)

**The Librarian CANNOT:**
- ❌ Modify documentation content (read-only)
- ❌ Delete documents from index without approval
- ❌ Override agent queries (always returns what's asked)
- ❌ Make architectural decisions about taxonomy
- ❌ Block agents from accessing content

**Escalation:** For taxonomy changes, cluster restructuring, or major index redesign, Librarian creates proposal for human review.

---

## Data Sources

### Primary Source: YAML Master Index

```yaml
# .deia/index/master-index.yaml
# Librarian's source of truth
```

**Librarian responsibilities:**
- Keep synchronized with actual docs
- Validate paths exist
- Update metadata
- Add new entries

### Query Log: JSONL

```jsonl
# .deia/index/query-log.jsonl
# Librarian writes here
```

**Librarian responsibilities:**
- Append every query
- Include agent ID, timestamp, result
- Use for analytics

### Generated: Markdown Quick Reference

```markdown
# .deia/index/QUICK-REFERENCE.md
# Librarian generates from YAML
```

**Librarian responsibilities:**
- Regenerate when index changes
- Keep human-readable
- Publish to docs/

---

## Operational Modes

### Mode 1: Always-On Service (Recommended)

**Implementation:** Background process, API endpoint, or bot integration

```bash
# Start librarian service
python .deia/librarian/service.py &

# Agents query via API
curl http://localhost:8080/query?q="DNS+errors"

# Or via Python
from deia.librarian import query
result = query("DNS errors")
```

**Pros:**
- Fast response (<50ms)
- Always available
- Can monitor conversations

**Cons:**
- Requires running process
- Resource overhead (minimal)

### Mode 2: On-Demand (CLI)

**Implementation:** CLI tool called when needed

```bash
# Agent calls when needed
deia-librarian query "DNS errors"

# Returns YAML/JSON to stdout
```

**Pros:**
- No background process
- Simple implementation
- Easy to debug

**Cons:**
- Slower (200-500ms startup)
- Can't do proactive injection
- No conversation monitoring

### Mode 3: Bot Integration

**Implementation:** Librarian as capability of bot coordinator

```python
# Bot has librarian module
bot.librarian.query("deployment failed")

# Librarian monitors bot's conversation
bot.on_message(librarian.check_triggers)
```

**Pros:**
- Integrated with existing bot system
- Can inject into LLM context directly
- Shared telemetry

**Cons:**
- Coupled to bot implementation
- Only available when bot running

**Recommendation:** Start with Mode 2 (CLI), evolve to Mode 1 (service) as usage grows.

---

## Performance Requirements

### Response Time Targets

| Query Type | Target | Max Acceptable |
|------------|--------|----------------|
| Simple keyword | <100ms | <200ms |
| Natural language | <200ms | <500ms |
| Platform filter | <150ms | <300ms |
| Proactive trigger check | <50ms | <100ms |

### Scalability

| Doc Count | Index Size | Load Time | Query Time |
|-----------|-----------|-----------|------------|
| 18 (current) | ~50KB | <10ms | <50ms |
| 100 (near-term) | ~300KB | <50ms | <100ms |
| 1000 (future) | ~3MB | <200ms | <300ms |

**Optimization strategies:**
- Cache frequently-accessed queries
- Pre-compute common filters (platform, audience)
- Shard by cluster if >1000 docs
- Use incremental indexing

---

## Telemetry and Reporting

### Events Logged

**Query events:**
```jsonl
{"ts":"2025-10-16T16:00:00Z","agent_id":"LIBRARIAN-001","event":"query","query":"DNS errors","matched":true,"docs_returned":3,"response_time_ms":120}
```

**Proactive injection:**
```jsonl
{"ts":"2025-10-16T16:15:00Z","agent_id":"LIBRARIAN-001","event":"proactive_injection","trigger":"nuclear_option","target_agent":"CLAUDE-CODE-001","docs_injected":2,"prevented_error":true}
```

**Index update:**
```jsonl
{"ts":"2025-10-16T16:30:00Z","agent_id":"LIBRARIAN-001","event":"index_update","action":"add_document","doc_id":"new-case-study","cluster":"deployment-safety"}
```

**Maintenance:**
```jsonl
{"ts":"2025-10-16T02:00:00Z","agent_id":"LIBRARIAN-001","event":"maintenance","queries_analyzed":47,"links_strengthened":12,"gaps_identified":3}
```

### Daily Report Format

```markdown
# Librarian Daily Report - 2025-10-16

## Query Activity

**Total queries:** 47
**Unique agents:** 3 (CLAUDE-CODE-001, GPT-5-BOT-D, USER-davee)
**Match rate:** 94% (44 matched, 3 no-match)
**Avg response time:** 145ms

## Top Queries

1. "DNS configuration" - 8 queries (cluster: dns-configuration)
2. "deployment recovery" - 6 queries (cluster: deployment-safety)
3. "LLM instructions" - 4 queries (cluster: llm-communication-quality)

## Proactive Injections

**Total:** 5 injections
**Successful prevention:** 4 (estimated - no error occurred after injection)

Most common trigger: "nuclear_option" (3 times)

## Index Health

**Documents indexed:** 18
**Clusters:** 7
**Broken links:** 0
**Stale content:** 0 (all updated within 7 days)

## Gaps Identified

**Queries with no match:**
- "Python debugging" (2 queries) - Suggest: Create Python BOK section
- "Git workflow" (1 query) - Partial match only

**Underserved audiences:**
- Frontend developers (0 docs tagged)
- QA engineers (1 doc tagged)

## Recommendations

1. Create Python/debugging documentation
2. Expand Git workflow documentation
3. Add frontend developer content
4. Strengthen links for "deployment recovery" cluster (high query volume)
```

---

## Integration with Hive

### Agent Profile

```json
{
  "agent_id": "LIBRARIAN-001",
  "type": "service-agent",
  "role": "librarian",
  "capabilities": [
    "query_response",
    "index_maintenance",
    "usage_analytics",
    "proactive_injection",
    "gap_analysis"
  ],
  "status": "active",
  "mode": "always-on",
  "telemetry_enabled": true,
  "log_path": ".deia/bot-logs/LIBRARIAN-001-activity.jsonl",
  "coordination": {
    "can_handoff": false,
    "can_receive_handoff": false,
    "coordination_protocol": "service-query"
  },
  "data_sources": [
    ".deia/index/master-index.yaml",
    ".deia/index/query-log.jsonl"
  ],
  "outputs": [
    ".deia/index/QUICK-REFERENCE.md",
    ".deia/librarian/reports/"
  ]
}
```

### Coordination Protocol

**Service-Query Pattern:**
- Agents query Librarian (request-response)
- Librarian does NOT handoff work
- Librarian does NOT receive work handoffs
- Pure service role

**Telemetry Integration:**
- Logs to standard JSONL format
- Uses same agent_id schema
- Integrates with hive telemetry dashboard

---

## Implementation Phases

### Phase 1: Minimum Viable Librarian (MVP)

**Capabilities:**
- Simple keyword query (CLI)
- Returns doc paths
- Manual index updates

**Time estimate:** 4-6 hours

**Deliverables:**
- Python script: `deia-librarian query`
- Basic YAML index
- Query response format

### Phase 2: Enhanced Query

**Capabilities:**
- Natural language queries
- Rich context responses
- Query logging
- Multiple output formats

**Time estimate:** 6-8 hours

**Deliverables:**
- Improved NLP matching
- JSONL query log
- JSON/YAML/Markdown outputs

### Phase 3: Proactive Injection

**Capabilities:**
- Trigger pattern matching
- Conversation monitoring
- Pre-action warnings

**Time estimate:** 8-10 hours

**Deliverables:**
- Trigger library
- Bot integration
- Injection logging

### Phase 4: Analytics & Learning

**Capabilities:**
- Usage analytics
- Link strengthening
- Gap analysis
- Daily reports

**Time estimate:** 6-8 hours

**Deliverables:**
- Analytics engine
- Report generator
- Index optimization

### Phase 5: Always-On Service

**Capabilities:**
- Background service
- API endpoint
- Real-time monitoring
- Auto-index updates

**Time estimate:** 10-12 hours

**Deliverables:**
- Service daemon
- REST API
- Git hooks for auto-indexing

---

## Success Metrics

### Query Performance

- ✅ **95%+ match rate** - Most queries find relevant docs
- ✅ **<200ms avg response time** - Fast enough for real-time use
- ✅ **80%+ agent satisfaction** - Agents find results useful

### Prevention Impact

- ✅ **Proactive injections** - Prevent errors before they happen
- ✅ **Reduced repeated errors** - Same mistake not made twice
- ✅ **Faster problem resolution** - Less time searching for answers

### Index Quality

- ✅ **Zero broken links** - All doc paths valid
- ✅ **Complete coverage** - All audiences/platforms served
- ✅ **Fresh content** - No stale/outdated docs

### Usage Growth

- ✅ **Increasing query volume** - Agents using librarian more
- ✅ **Diverse queries** - Not just same topics repeatedly
- ✅ **Cross-project adoption** - Other DEIA projects using it

---

## Open Questions

1. **Agent identity:** Should Librarian be a bot (with LLM) or pure logic service?
2. **Proactive injection:** How aggressive? Risk of noise vs missed prevention?
3. **Multi-project:** One librarian for all DEIA projects or project-specific?
4. **Query privacy:** Should queries be logged with agent ID or anonymized?
5. **Index authority:** Who approves major taxonomy changes?

**Will resolve during implementation based on usage patterns.**

---

## Related Specifications

- **Index Format:** `docs/specs/global-commons-index-format-spec.md`
- **Query Interface:** `docs/specs/librarian-query-interface.md`
- **Hive Architecture:** `.deia/hive-architecture.md`
- **Bot Coordination:** `.deia/bot-coordinator.py`

---

**Status:** Draft specification, ready for Phase 1 implementation
**Dependencies:** YAML master index, taxonomy from GPT-5
**Next:** Sample index entries and implementation plan

**Tags:** `#agent-role` `#librarian` `#service-agent` `#hive` `#phase2-prep`
