---
title: "Master Librarian Query Interface Specification"
date: 2025-10-16
status: Draft
version: 0.1
author: Claude Code (CLAUDE-CODE-001)
purpose: Define how AI agents query the Global Commons index
tags: [query-interface, librarian, api-design, phase2]
---

# Master Librarian Query Interface Specification

## Purpose

Define how AI agents interact with the Master Librarian to discover relevant Global Commons documentation.

**Design Goals:**
1. **Natural language queries** - Agents ask in plain English
2. **Fast responses** - <200ms for typical queries
3. **Rich context** - Not just file paths, but why/how to use them
4. **Learning system** - Gets better over time through usage tracking
5. **Multiple modalities** - Support different query styles

---

## Query Methods

### Method 1: Natural Language Question

**Use case:** Agent facing a problem, asks for help

**Format:**
```python
query = "I'm seeing DNS configuration errors"
# or
query = "How do I recover from a failed deployment?"
# or
query = "LLM is hallucinating names"
```

**Librarian Response:**
```yaml
query: "I'm seeing DNS configuration errors"
matched: true
confidence: high
primary_cluster: dns-configuration
urgency: critical

documents:
  primary:
    - id: bok-dns-ui-confusion
      path: bok/platforms/netlify/dns-configuration-ui-confusion.md
      title: "Netlify DNS Configuration UI Confusion"
      summary: "Netlify doesn't show DNS records after domain add"
      why_relevant: "Explains common DNS configuration confusion"
      action: "Check if you're configuring DNS at registrar vs platform"

    - id: case-dns-outage
      path: docs/global-commons/case-studies/dns-outage-registrar-confusion.md
      title: "DNS Outage from Registrar Confusion"
      summary: "Production outage from deleting wrong DNS records"
      why_relevant: "Shows critical mistake to avoid"
      action: "Verify where domain is registered before deleting DNS"

  secondary:
    - id: bok-nuclear-checklist
      path: bok/processes/netlify-nuclear-option-recovery.md
      title: "Netlify Nuclear Option Recovery"
      summary: "Complete recovery checklist if you deleted DNS"
      why_relevant: "Recovery path if DNS is already broken"

keywords_matched: [dns, configuration, errors]
suggested_next:
  - "Check domain registrar location"
  - "Review Netlify DNS UI limitations"
  - "Have you already deleted DNS records? Check recovery checklist"

related_queries:
  - "Domain not resolving"
  - "Netlify DNS issues"
  - "Production outage from DNS"
```

---

### Method 2: Keyword Search

**Use case:** Agent knows what they're looking for

**Format:**
```python
keywords = ["deployment", "nuclear", "recovery"]
```

**Librarian Response:**
```yaml
query_type: keyword_search
keywords: [deployment, nuclear, recovery]
matched_documents: 3

results:
  - id: bok-nuclear-checklist
    relevance: 100%
    keywords_matched: [nuclear, recovery, deployment]
    path: bok/processes/netlify-nuclear-option-recovery.md

  - id: case-nuclear-recovery
    relevance: 95%
    keywords_matched: [nuclear, recovery, deployment]
    path: docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md

  - id: bok-direct-to-prod
    relevance: 60%
    keywords_matched: [deployment]
    path: bok/anti-patterns/direct-to-production-deployment.md

clusters_found: [deployment-safety, platform-gotchas]
```

---

### Method 3: Context-Aware Proactive Injection

**Use case:** Librarian monitoring conversation, injects relevant docs

**Trigger:**
```
Agent conversation contains:
- "I'm going to delete the Netlify project and recreate it"
```

**Librarian Action:**
```yaml
event: proactive_injection
trigger: "conversation pattern matched 'nuclear option'"
confidence: high
urgency: critical

injection:
  type: warning_with_docs
  message: "⚠️ Detected 'nuclear option' (delete/recreate) - I have a complete recovery checklist for this."

  documents:
    - id: bok-nuclear-checklist
      path: bok/processes/netlify-nuclear-option-recovery.md
      inject_mode: full_context
      reason: "Prevents incomplete recovery (60+ min outage pattern)"

    - id: case-nuclear-recovery
      path: docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md
      inject_mode: summary_only
      reason: "Case study showing what happens without checklist"

  action_required: "Review checklist BEFORE deleting project"
  timing: pre-action (before user executes nuclear option)
```

**Benefits:**
- Prevents mistakes before they happen
- Applies BOK knowledge proactively
- Reduces repeated failures

---

### Method 4: Platform-Filtered Query

**Use case:** Agent working on specific platform

**Format:**
```python
query = "show me all Netlify documentation"
# or
platform_filter = "netlify"
```

**Librarian Response:**
```yaml
query_type: platform_filter
platform: netlify
documents_found: 4

by_urgency:
  critical:
    - bok-nuclear-checklist
    - case-dns-outage
    - case-nuclear-recovery

  high:
    - bok-dns-ui-confusion
    - bok-hugo-version

by_category:
  gotchas:
    - bok-dns-ui-confusion (UI doesn't show DNS records)
    - bok-hugo-version (Must set env var)

  processes:
    - bok-nuclear-checklist (Delete/recreate recovery)

  case_studies:
    - case-dns-outage (Registrar confusion)
    - case-nuclear-recovery (Incomplete recovery)

quick_tips:
  - "Always set HUGO_VERSION environment variable"
  - "Configure DNS at registrar, not in Netlify UI"
  - "After nuclear option: verify build settings, env vars, domains, DNS"
```

---

### Method 5: Audience-Specific View

**Use case:** Show me what's relevant for my role

**Format:**
```python
audience = "devops"
# or
query = "what should DevOps engineers know?"
```

**Librarian Response:**
```yaml
query_type: audience_view
audience: devops
documents_found: 8

high_priority:
  - case-dns-outage (Critical: Production outage pattern)
  - case-nuclear-recovery (Critical: Incomplete recovery)
  - bok-nuclear-checklist (Critical: Recovery checklist)
  - bok-direct-to-prod (High: Deployment anti-pattern)

medium_priority:
  - bok-dns-ui-confusion (Platform gotcha)
  - bok-hugo-version (Platform requirement)

by_urgency:
  when_production_down:
    - DNS outage case study + recovery docs
    - Nuclear recovery case study + checklist

  for_prevention:
    - Direct-to-production anti-pattern
    - All platform gotchas

learning_path:
  1: Read anti-patterns first (prevention)
  2: Familiarize with platform gotchas
  3: Know where recovery checklists are
  4: Review case studies for context
```

---

## Query Interface Implementations

### Option A: Python Function Call

```python
from deia.librarian import query_commons

# Simple query
result = query_commons("DNS not working")

# With filters
result = query_commons(
    query="deployment failed",
    platform="netlify",
    urgency="critical"
)

# Keyword search
result = query_commons(
    keywords=["nuclear", "recovery"],
    return_format="paths_only"
)

# Response
print(result.primary_docs)  # List of Document objects
print(result.summary)       # Human-readable summary
```

### Option B: CLI Command

```bash
# Simple query
deia search "DNS configuration errors"

# Platform filter
deia search --platform netlify

# Audience view
deia search --audience devops --urgency critical

# Output formats
deia search "deployment" --format json
deia search "deployment" --format markdown
deia search "deployment" --format paths
```

### Option C: Bot Integration (Pheromone Pattern)

```python
# Bot monitoring conversation
conversation = ["User: I'm going to delete the Netlify project"]

# Librarian checks for triggers
triggers = librarian.check_triggers(conversation)

if triggers:
    # Inject relevant docs
    context = librarian.get_context(triggers)
    bot.inject_to_llm_context(context)
```

### Option D: LLM Tool Call

```xml
<tool_use>
  <tool_name>query_global_commons</tool_name>
  <parameters>
    <query>How do I recover from failed deployment?</query>
    <urgency>critical</urgency>
  </parameters>
</tool_use>

<tool_result>
  <primary_docs>
    <doc path="bok/processes/netlify-nuclear-option-recovery.md">
      Complete recovery checklist for delete/recreate workflow
    </doc>
    <doc path="docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md">
      Case study: What happens without complete verification
    </doc>
  </primary_docs>
  <action>Review checklist before proceeding with recovery</action>
</tool_result>
```

---

## Response Formats

### Minimal (Paths Only)

```
bok/processes/netlify-nuclear-option-recovery.md
docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md
bok/anti-patterns/direct-to-production-deployment.md
```

**Use case:** Agent just needs to know what exists

### Summary

```markdown
## Found 3 documents about "deployment recovery"

**Primary:**
- Netlify Nuclear Option Recovery (bok/processes) - Complete checklist
- Nuclear Recovery Case Study (case-studies) - Learn from 60+ min outage

**Action:** Review checklist before delete/recreate
```

**Use case:** Human-readable quick reference

### Full Context (For LLM Injection)

```markdown
# Relevant Documentation: Deployment Recovery

## Critical: Netlify Nuclear Option Recovery Checklist

**Source:** bok/processes/netlify-nuclear-option-recovery.md

When doing delete/recreate ("nuclear option"), you MUST reconfigure:

1. **Build Configuration**
   - Build command: `cd website && hugo`
   - Publish directory: `website/public`
   - ⚠️ Base directory: LEAVE BLANK

2. **Environment Variables** (OFTEN FORGOTTEN)
   - HUGO_VERSION: 0.134.3
   - Verify scope: Production

3. **Verification Steps** (DO NOT SKIP)
   - [ ] Check deploy log shows build ran
   - [ ] Check deploy log shows pages built (not "0 pages")
   - [ ] Test site at netlify.app URL
   - [ ] Test all custom domains

**Why this matters:** Previous incident resulted in 60+ minutes broken production
because build settings were marked "complete" without verification.

---

## Related Case Study

[Full case study content embedded here...]
```

**Use case:** LLM needs full context to provide good advice

---

## Query Matching Logic

### Keyword Extraction

```python
# From natural language query
query = "I'm seeing DNS configuration errors"

# Extract keywords
keywords = extract_keywords(query)
# → ["dns", "configuration", "errors"]

# Match against index
matches = index.search(keywords)

# Rank by relevance
ranked = rank_by_relevance(matches, query)
```

### Fuzzy Matching

```python
query_keywords = ["deploi", "failur"]  # Typos

# Fuzzy match
matched = fuzzy_search(query_keywords, index)
# → ["deployment", "failure"]

# Return corrected results
```

### Semantic Matching (Future)

```python
query = "my site won't load"

# Semantic understanding
concepts = extract_concepts(query)
# → ["dns", "deployment", "outage", "broken"]

# Match to clusters
clusters = semantic_match(concepts)
# → [dns-configuration, deployment-safety]
```

---

## Usage Tracking

**Log every query:**

```jsonl
{"ts":"2025-10-16T16:00:00Z","agent":"CLAUDE-CODE-001","query":"deployment failed","matched":true,"cluster":"deployment-safety","docs":["bok-nuclear-checklist","case-nuclear-recovery"],"response_time_ms":180}
```

**Analyze patterns:**
- Most queried topics
- Failed queries (no match)
- Query → resolution success rate
- Time to find answer

**Strengthen index:**
- Add keywords from successful queries
- Promote frequently-needed docs
- Identify gaps (queries with no matches)
- Build suggested query refinements

---

## Error Handling

### No Match Found

```yaml
query: "quantum entanglement debugging"
matched: false
reason: no_documents_match

suggestions:
  - "Try broader keywords: 'debugging' alone"
  - "Available topics: deployment, DNS, LLM communication, processes"
  - "Browse by platform: netlify"
  - "Browse by audience: devops, ai-researchers"

similar_queries:
  - "deployment debugging" (3 docs)
  - "process debugging" (1 doc)
```

### Ambiguous Query

```yaml
query: "errors"
matched: partial
reason: query_too_broad

refinement_needed: true

suggestions:
  - "Be more specific: 'DNS errors', 'deployment errors', 'build errors'?"
  - "What platform: netlify?"
  - "What urgency: critical (production down) or learning?"

available_clusters:
  - deployment-safety (deployment errors, recovery)
  - dns-configuration (DNS resolution errors)
  - llm-communication-quality (instruction errors)
```

---

## Performance Targets

**Query response time:**
- Simple keyword search: <100ms
- Natural language query: <200ms
- Context-aware injection: <50ms (pre-indexed triggers)

**Scalability:**
- Current (18 docs): Instant
- Expected (100 docs): <200ms
- Future (1000 docs): <500ms (may need optimization)

---

## Integration Points

### With Bot Coordinator

```python
# Bot detects user intent
if user_intent == "need_help_with_deployment":
    # Query librarian
    docs = librarian.query("deployment help")

    # Inject into LLM context
    bot.add_context(docs.full_context)
```

### With Claude Code CLI

```python
# User working on DNS issue
# Claude Code proactively checks

if task_involves("dns"):
    relevant_docs = librarian.query(
        platform=current_platform,
        topic="dns",
        urgency="high"
    )

    # Offer to user
    print(f"💡 I found {len(relevant_docs)} relevant docs about DNS.")
    print("Would you like me to review them before proceeding?")
```

### With Telemetry System

```python
# Log query for analytics
telemetry.log_event(
    agent_id="CLAUDE-CODE-001",
    event="librarian_query",
    query=query,
    matched=result.matched,
    docs_returned=len(result.documents),
    response_time_ms=response_time
)
```

---

## Next Steps

1. **Implement basic query function** in Python
2. **Build trigger pattern matcher** for proactive injection
3. **Create query log analyzer** for usage insights
4. **Test with real agent queries**
5. **Iterate based on usage patterns**

---

**Status:** Draft specification, ready for implementation
**Dependencies:** Master index format (YAML), Master Librarian role spec
**Next:** Master Librarian full role specification

**Tags:** `#query-interface` `#librarian` `#api-design` `#phase2-prep`
