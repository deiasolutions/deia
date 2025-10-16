---
title: "Global Commons Index Format Specification"
date: 2025-10-16
status: Draft
version: 0.1
author: Claude Code (CLAUDE-CODE-001)
purpose: Technical design for AI-readable content index
tags: [index, format-spec, technical-design, phase2]
---

# Global Commons Index Format Specification

## Purpose

Define technical formats for indexing DEIA Global Commons content to enable fast AI agent discovery of relevant documentation.

**Design Goals:**
1. **Fast scanning** - AI can quickly check "do we have X?"
2. **Multiple access patterns** - Find by keyword, problem, platform, audience, urgency
3. **Human readable** - Maintainable by humans, parseable by AI
4. **Extensible** - Easy to add new content/metadata
5. **Multi-format** - Right tool for each use case

---

## Format Option 1: YAML Master Index

**Use case:** Structured, hierarchical organization with rich metadata

**Pros:**
- Human readable and editable
- Supports nested structures (clusters, hierarchies)
- Strong typing for metadata
- Git-friendly (clean diffs)

**Cons:**
- Slower to parse than JSONL
- Can get large (full file load required)
- Indentation-sensitive

**Example:**

```yaml
# .deia/index/master-index.yaml

version: "1.0"
last_updated: "2025-10-16T16:30:00Z"
total_documents: 18

clusters:
  deployment-safety:
    description: "Preventing and recovering from deployment disasters"
    keywords:
      - deployment
      - production
      - outage
      - recovery
      - nuclear-option
    documents:
      - id: "bok-direct-to-prod"
        path: "bok/anti-patterns/direct-to-production-deployment.md"
        title: "Direct-to-Production Deployment Anti-Pattern"
        summary: "Deploying without testing - includes proper workflow"
        audience: [developers, devops]
        urgency: high
        tags: [anti-pattern, deployment, qa-process]

      - id: "case-nuclear-recovery"
        path: "docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md"
        title: "Nuclear Option Without Complete Recovery"
        summary: "Delete/recreate without verification - 60+ min outage"
        audience: [devops, deployment-teams]
        urgency: critical
        tags: [nuclear-option, incomplete-recovery, todo-discipline]

      - id: "bok-nuclear-checklist"
        path: "bok/processes/netlify-nuclear-option-recovery.md"
        title: "Netlify Nuclear Option Recovery Process"
        summary: "Complete checklist for delete/recreate workflow"
        audience: [netlify-users, devops]
        urgency: critical
        tags: [netlify, nuclear-option, recovery-checklist]

    related_clusters: [platform-gotchas, llm-verification]

  llm-communication-quality:
    description: "How LLMs should communicate with users - completeness, accuracy, attribution"
    keywords:
      - llm
      - instructions
      - incomplete
      - hallucination
      - attribution
      - communication
    documents:
      - id: "case-incomplete-instructions"
        path: "docs/global-commons/case-studies/incomplete-instructions-pattern.md"
        title: "Incomplete Procedural Instructions Pattern"
        summary: "Omitting prerequisite steps causes user frustration"
        audience: [technical-writers, llm-designers]
        urgency: high
        tags: [incomplete-instructions, user-experience]

      - id: "case-name-hallucination"
        path: "docs/global-commons/case-studies/llm-name-hallucination-incident.md"
        title: "LLM Name Hallucination Incident"
        summary: "Privacy safeguards for LLM attribution"
        audience: [ai-safety, llm-designers]
        urgency: critical
        tags: [privacy, hallucination, attribution]

    related_clusters: [process-safeguards]

query_patterns:
  - query: "deployment failed"
    keywords: [deployment, failed, failure, broken]
    primary_cluster: deployment-safety
    urgency: critical

  - query: "DNS not working"
    keywords: [dns, domain, not resolving, outage]
    primary_cluster: dns-configuration
    urgency: critical

  - query: "LLM gave bad instructions"
    keywords: [llm, instructions, incomplete, wrong, bad]
    primary_cluster: llm-communication-quality
    urgency: high

platform_index:
  netlify:
    - bok-dns-ui-confusion
    - bok-hugo-version
    - bok-nuclear-checklist
    - case-dns-outage
    - case-nuclear-recovery

  squarespace:
    - bok-dns-ui-confusion

audience_index:
  devops:
    - deployment-safety (all)
    - dns-configuration (all)
    - platform-gotchas (netlify)

  ai-researchers:
    - llm-communication-quality (all)
    - process-safeguards (emergent-behavior, vaporware)

  llm-designers:
    - llm-communication-quality (all)
    - process-safeguards (bok-injection)

urgency_index:
  critical:
    - case-dns-outage
    - case-nuclear-recovery
    - case-name-hallucination
    - bok-nuclear-checklist
  high:
    - case-incomplete-instructions
    - bok-direct-to-prod
  medium:
    - process docs (general)
  low:
    - articles (factory-egg)
    - specs (offline-launch)
```

**File size estimate:** ~500-1000 lines for current content, scales linearly

---

## Format Option 2: JSONL Query Log

**Use case:** Streaming query tracking, usage analytics, link strengthening

**Pros:**
- Appendable (no full file rewrite)
- Fast to parse incrementally
- Perfect for time-series data
- Easy to analyze with standard tools

**Cons:**
- Not great for hierarchical data
- Less human-readable
- Needs separate schema doc

**Example:**

```jsonl
# .deia/index/query-log.jsonl

{"ts":"2025-10-16T16:00:00Z","agent":"CLAUDE-CODE-001","query":"deployment failed","matched_cluster":"deployment-safety","docs_retrieved":["bok-direct-to-prod","case-nuclear-recovery"],"found":true,"resolution_time_ms":150}
{"ts":"2025-10-16T16:15:00Z","agent":"GPT-5-BOT-D","query":"DNS configuration","matched_cluster":"dns-configuration","docs_retrieved":["bok-dns-ui-confusion","case-dns-outage"],"found":true,"resolution_time_ms":220}
{"ts":"2025-10-16T16:30:00Z","agent":"CLAUDE-CODE-001","query":"LLM hallucination","matched_cluster":"llm-communication-quality","docs_retrieved":["case-name-hallucination"],"found":true,"resolution_time_ms":180}
{"ts":"2025-10-16T16:45:00Z","agent":"CLAUDE-CODE-001","query":"vaporware detection","matched_cluster":"process-safeguards","docs_retrieved":["process-vaporware-safeguard"],"found":true,"resolution_time_ms":200}
```

**Usage:** Master Librarian analyzes patterns, strengthens frequently-queried links

---

## Format Option 3: Markdown Quick Reference

**Use case:** Human-readable catalog for quick scanning

**Pros:**
- Extremely readable
- Git-friendly
- Can embed examples
- Good for documentation

**Cons:**
- Not structured for parsing
- Manual maintenance
- Less queryable

**Example:**

```markdown
# Global Commons Quick Reference

## By Problem Type

### 🚨 Deployment Failures
- **[Direct-to-Production Anti-Pattern](bok/anti-patterns/direct-to-production-deployment.md)** - Proper Git workflow and QA
- **[Nuclear Option Recovery](docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md)** - Complete recovery checklists
- **[Netlify Nuclear Checklist](bok/processes/netlify-nuclear-option-recovery.md)** - Build config, env vars, domains, DNS

### 🌐 DNS Issues
- **[DNS Outage from Registrar Confusion](docs/global-commons/case-studies/dns-outage-registrar-confusion.md)** - Check where domain is registered first
- **[Netlify DNS UI Confusion](bok/platforms/netlify/dns-configuration-ui-confusion.md)** - Configure at registrar, not Netlify

### 🤖 LLM Communication Quality
- **[Incomplete Instructions Pattern](docs/global-commons/case-studies/incomplete-instructions-pattern.md)** - Always include prerequisites
- **[Name Hallucination Incident](docs/global-commons/case-studies/llm-name-hallucination-incident.md)** - Privacy safeguards for attribution

## By Platform

### Netlify
- DNS UI Confusion
- Hugo Version Requirement
- Nuclear Option Recovery

## By Urgency

### Critical (Production Down)
- DNS Outage case study
- Nuclear Recovery case study
- Nuclear Recovery checklist

### High (Deployment/Recovery)
- Direct-to-production anti-pattern
- Incomplete instructions pattern
```

**File size:** ~200-400 lines, highly maintainable

---

## Recommended Hybrid Approach

**Use all three formats for different purposes:**

1. **YAML Master Index** (`.deia/index/master-index.yaml`)
   - Single source of truth
   - Rich metadata and structure
   - Updated when content added/changed
   - Used by Master Librarian for complex queries

2. **JSONL Query Log** (`.deia/index/query-log.jsonl`)
   - Tracks all agent queries
   - Analytics for usage patterns
   - Informs link strengthening
   - Continuously appended

3. **Markdown Quick Ref** (`.deia/index/QUICK-REFERENCE.md`)
   - Human-readable catalog
   - Updated from YAML automatically
   - Good for onboarding, browsing
   - Published to docs/

**Workflow:**
```
Content added → Update YAML master index
                    ↓
                Generate Markdown quick ref
                    ↓
Agent queries → Log to JSONL
                    ↓
Librarian analyzes → Strengthens YAML metadata
```

---

## Index Entry Schema

**Minimum required fields:**

```yaml
document:
  id: unique-identifier          # Required
  path: relative/path/to/doc.md  # Required
  title: Human Readable Title    # Required
  summary: One-sentence description  # Required
  keywords: [list, of, terms]    # Required

  # Optional but recommended
  audience: [target, audiences]
  urgency: critical|high|medium|low
  tags: [freeform, tags]
  related_docs: [other-doc-ids]
  cluster: cluster-name

  # Metadata
  created: ISO-8601-timestamp
  updated: ISO-8601-timestamp
  author: agent-or-human-id
```

---

## Query Response Format

When agent queries index:

```yaml
query_result:
  query: "original query string"
  matched: true|false
  primary_cluster: cluster-name
  documents:
    - id: doc-id
      relevance: primary|secondary|context
      path: path/to/doc.md
      summary: Quick description
      urgency: level
  keywords_matched: [terms, that, triggered]
  suggested_refinements: [alternative, queries]
  related_clusters: [other-clusters-to-check]
```

---

## File Locations

**Proposed structure:**

```
.deia/index/
├── master-index.yaml          # YAML master index (source of truth)
├── query-log.jsonl            # Query tracking and analytics
├── QUICK-REFERENCE.md         # Human-readable catalog
├── schemas/
│   ├── index-entry.schema.yaml
│   └── query-log.schema.json
└── scripts/
    ├── update-index.py        # Adds new content to index
    ├── generate-quick-ref.py  # YAML → Markdown
    └── analyze-queries.py     # JSONL → insights
```

---

## Performance Considerations

**For AI agents:**
- YAML master index: ~100-200ms to parse and search (18 docs)
- Scales to ~1000 docs before performance concerns
- Consider sharding if >1000 docs (by cluster, platform, etc.)

**For humans:**
- Markdown quick ref loads instantly
- YAML readable but prefer Markdown for browsing

**For analytics:**
- JSONL query log: stream-processable, no size limits
- Analyze with standard tools (jq, pandas, etc.)

---

## Migration Path

**Phase 1 (Now):**
- Create YAML master index for current 18 docs
- Generate Markdown quick ref
- Define query log schema

**Phase 2 (After taxonomy from GPT-5):**
- Populate clusters from taxonomy
- Add query patterns
- Build platform/audience/urgency indexes

**Phase 3 (Master Librarian):**
- Implement query interface
- Start logging queries
- Analyze and strengthen links

**Phase 4 (Scale):**
- Add automation for index updates
- Build cross-reference validation
- Create usage dashboards

---

## Open Questions

1. **Cluster naming:** Use GPT-5's taxonomy verbatim or normalize?
2. **Keyword extraction:** Manual or automated NLP?
3. **Related docs:** Explicit links or inferred from cluster membership?
4. **Query matching:** Exact keywords or fuzzy/semantic?
5. **Index updates:** Manual, semi-automated, or fully automated?

**Will answer after GPT-5 taxonomy arrives.**

---

**Status:** Draft specification, ready for Phase 2 implementation
**Next:** Query interface patterns and Master Librarian role spec

**Tags:** `#index-format` `#technical-spec` `#phase2-prep` `#yaml` `#jsonl` `#markdown`
