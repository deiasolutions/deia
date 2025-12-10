---
title: "Practical Taxonomy for Global Commons Content"
date: 2025-10-16
author: Claude Code (CLAUDE-CODE-001)
version: 1.0
purpose: Actionable organization for 18 documents to enable fast AI agent discovery
status: final
tags: [taxonomy, content-organization, right-brain-work, phase1]
---

# Practical Taxonomy for Global Commons Content

## Purpose

Organize 18 documents from 2025-10-16 session into natural clusters that match how users and AI agents actually think about problems.

**Approach:** Pattern recognition based on:
- What problems do these docs solve?
- When would a user need them together?
- What mental models do agents have when searching?
- What are the natural groupings by intent, not just topic?

---

## Content Clusters (7 Total)

### Cluster 1: Deployment Safety & Recovery

**Core concept:** Preventing and recovering from deployment disasters

**Documents (5):**
1. **Direct-to-Production Anti-Pattern** (bok/anti-patterns/)
   - Problem: Deploying without testing causes production failures
   - When needed: Before any deployment, during QA setup

2. **Nuclear Option Recovery Checklist** (bok/processes/)
   - Problem: Delete/recreate without complete reconfiguration
   - When needed: BEFORE deleting, DURING recovery

3. **Nuclear Recovery Case Study** (case-studies/)
   - Problem: 60+ min outage from incomplete recovery
   - When needed: Understanding what goes wrong, learning from failure

4. **Hugo Version Requirement** (bok/platforms/netlify/)
   - Problem: Build fails with "command not found"
   - When needed: Netlify/Hugo deploys, after nuclear option

5. **DNS Outage Case Study** (case-studies/)
   - Problem: Production outage from DNS deletion
   - When needed: Understanding DNS risks, recovery context

**Why grouped:**
- All about deployment going wrong and fixing it
- User asking: "My deployment failed, now what?"
- Progression: prevention → recovery → learning
- Cross-platform patterns (not just Netlify-specific)

**Common user queries:**
- "deployment failed"
- "site is down"
- "broken production"
- "how do I recover?"
- "I'm deleting and recreating"

**Urgency:** CRITICAL (production down) + HIGH (prevention)

---

### Cluster 2: DNS Configuration & Domain Management

**Core concept:** DNS setup, registrar confusion, domain routing

**Documents (2):**
1. **DNS Outage Case Study** (case-studies/)
   - Problem: Blanket DNS advice without checking registrar
   - When needed: Before ANY DNS changes

2. **Netlify DNS UI Confusion** (bok/platforms/netlify/)
   - Problem: UI doesn't show DNS records, unclear where to configure
   - When needed: Adding domains to Netlify, Squarespace DNS

**Why grouped:**
- Both about DNS configuration mistakes
- Common root cause: not understanding registrar vs platform
- User needs both to avoid and fix DNS issues

**Common user queries:**
- "DNS not working"
- "domain not resolving"
- "where do I configure DNS?"
- "Netlify DNS"
- "DNS outage"

**Cross-references:**
- Deployment Safety (DNS issues cause outages)
- Platform Gotchas (Netlify-specific)

**Urgency:** CRITICAL (production down)

---

### Cluster 3: LLM Communication Quality

**Core concept:** How LLMs should communicate with users - completeness, accuracy, safety

**Documents (2):**
1. **Incomplete Instructions Pattern** (case-studies/)
   - Problem: Omitting prerequisite steps frustrates users
   - When needed: Writing technical docs, giving instructions

2. **Name Hallucination Incident** (case-studies/)
   - Problem: Privacy violation from hallucinated names
   - When needed: Attribution, privacy reviews

**Why grouped:**
- Both about LLM communication failures
- User impact: frustration, trust erosion, potential harm
- Lessons for LLM system design

**Common user queries:**
- "LLM gave bad instructions"
- "incomplete guidance"
- "LLM hallucinated"
- "privacy issue"
- "how should LLMs communicate?"

**Audience:** Technical writers, LLM designers, AI researchers

**Urgency:** CRITICAL (privacy) + HIGH (UX)

---

### Cluster 4: Process Safeguards & Quality Control

**Core concept:** Protocols to prevent documentation/system failures

**Documents (3):**
1. **Vaporware Safeguard** (docs/process/)
   - Problem: Aspirational claims become canon
   - When needed: Documentation review, fact-checking

2. **Emergent Behavior Protocol** (docs/process/)
   - Problem: LLMs claiming capabilities without permission
   - When needed: Documenting new behaviors, capability reviews

3. **BOK Context Injection Proposal** (docs/process/)
   - Problem: Repeated mistakes when solutions exist
   - When needed: System design, preventing known errors

**Why grouped:**
- All about quality control and process improvement
- Preventative measures for system-level issues
- Meta-documentation (how to document)

**Common user queries:**
- "how do we prevent X?"
- "quality control process"
- "fact-checking documentation"
- "preventing repeated errors"

**Audience:** Documentation teams, system designers, process engineers

**Urgency:** MEDIUM (prevention/improvement)

---

### Cluster 5: Platform-Specific Gotchas (Netlify)

**Core concept:** Netlify platform requirements, limitations, workarounds

**Documents (3 - cross-referenced from other clusters):**
1. **Netlify DNS UI Confusion** (from Cluster 2)
2. **Hugo Version Requirement** (from Cluster 1)
3. **Nuclear Option Recovery Checklist** (from Cluster 1)

**Why separate cluster:**
- Users often search by platform ("Netlify issues")
- Platform-specific documentation needs dedicated access
- Cross-cutting: touches deployment, DNS, recovery

**Common user queries:**
- "Netlify problems"
- "using Netlify"
- "Netlify gotchas"
- "Hugo on Netlify"

**Platform:** Netlify (primary), Hugo (secondary)

**Urgency:** CRITICAL (nuclear checklist) + HIGH (requirements)

**Note:** This is a VIEW on documents from other clusters, not separate storage

---

### Cluster 6: DEIA System Architecture

**Core concept:** DEIA design patterns, organizational structures, philosophy

**Documents (2):**
1. **The Factory Egg** (docs/articles/)
   - Problem: Understanding DEIA organizational blueprints
   - When needed: Learning DEIA concepts, architecture review

2. **Egg Offline Launch Capability** (docs/specs/)
   - Problem: How Eggs work without Commons connection
   - When needed: Implementation, technical specs

**Why grouped:**
- Both about DEIA system design
- Conceptual understanding (article) + technical detail (spec)
- Not urgent for production issues, but foundational knowledge

**Common user queries:**
- "what is Factory Egg?"
- "how does DEIA work?"
- "offline mode"
- "organizational design"

**Audience:** System architects, Commons contributors, organizational designers

**Urgency:** LOW (learning/background)

---

### Cluster 7: Internal Incidents & Observability

**Core concept:** Incident tracking and process accountability

**Documents (5 - internal only, NOT in Global Commons):**
1. Name Hallucination Incident (internal)
2. Incomplete Instructions Incident (internal)
3. DNS Outage Incident (internal)
4. Nuclear Recovery Incident (internal)
5. Claude Code No Telemetry Incident (internal)

**Why separate:**
- Internal project-specific details
- Sanitized versions published as case studies in other clusters
- Not for public index, but tracked for completeness

**Note:** These are source material for case studies, not indexed for public query

---

## Query Pattern Mapping

### Query: "My deployment failed / is broken"

**Primary cluster:** Deployment Safety & Recovery
**Urgency:** CRITICAL

**Documents to return:**
1. **Nuclear Recovery Checklist** - If delete/recreate involved
2. **Direct-to-Production Anti-Pattern** - If no testing done
3. **Hugo Version Requirement** - If Netlify/Hugo build
4. **DNS Outage Case Study** - If DNS-related

**Suggested follow-up:** "Is this Netlify? Did you delete the project?"

---

### Query: "DNS not working / domain not resolving"

**Primary cluster:** DNS Configuration
**Urgency:** CRITICAL

**Documents to return:**
1. **DNS Outage Case Study** - Check registrar first
2. **Netlify DNS UI Confusion** - Platform-specific guidance

**Suggested follow-up:** "Where is the domain registered? Netlify or external?"

---

### Query: "LLM gave bad/incomplete instructions"

**Primary cluster:** LLM Communication Quality
**Urgency:** HIGH

**Documents to return:**
1. **Incomplete Instructions Pattern** - Learn from failure
2. **Vaporware Safeguard** - Fact-checking process

**Audience:** Technical writers, LLM designers

---

### Query: "I'm deleting and recreating [project/deployment]"

**Primary cluster:** Deployment Safety
**Urgency:** CRITICAL
**Action:** PROACTIVE INJECTION (inject BEFORE user proceeds)

**Documents to inject:**
1. **Nuclear Recovery Checklist** - MUST READ before deleting
2. **Nuclear Recovery Case Study** - What goes wrong

**Warning message:** "⚠️ Detected 'nuclear option' - complete recovery checklist required to prevent 60+ min outage"

---

### Query: "Using Netlify" / "Netlify issues"

**Primary cluster:** Platform Gotchas (Netlify)
**Urgency:** varies

**Documents to return:**
1. **Nuclear Recovery Checklist** - If delete/recreate
2. **Hugo Version Requirement** - If Hugo
3. **DNS UI Confusion** - If DNS issues

**Filter by urgency:** Return critical docs first

---

### Query: "How to prevent [mistakes/errors]"

**Primary cluster:** Process Safeguards
**Urgency:** MEDIUM

**Documents to return:**
1. **Vaporware Safeguard** - Documentation quality
2. **BOK Context Injection Proposal** - System design
3. **Emergent Behavior Protocol** - Capability documentation

**Audience:** Process designers, documentation teams

---

### Query: "What is Factory Egg / DEIA architecture"

**Primary cluster:** DEIA System Architecture
**Urgency:** LOW

**Documents to return:**
1. **The Factory Egg** - Conceptual overview
2. **Egg Offline Launch** - Technical specs

**Audience:** Architects, Commons contributors

---

## Multi-Dimensional Access Paths

### By Urgency

**CRITICAL (production down):**
- DNS Outage case study
- Nuclear Recovery case study + checklist
- Name Hallucination incident

**HIGH (deployment/recovery):**
- Direct-to-production anti-pattern
- Incomplete Instructions pattern
- DNS UI Confusion
- Hugo Version Requirement

**MEDIUM (prevention/process):**
- Vaporware Safeguard
- Emergent Behavior Protocol
- BOK Context Injection Proposal

**LOW (learning/architecture):**
- Factory Egg article
- Offline Launch spec

---

### By Audience

**DevOps / Deployment Teams:**
- Deployment Safety (all 5 docs)
- DNS Configuration (2 docs)
- Platform Gotchas (3 docs)

**AI Researchers / LLM Designers:**
- LLM Communication Quality (2 docs)
- Process Safeguards (3 docs)

**Technical Writers / Documentation:**
- LLM Communication Quality (2 docs)
- Process Safeguards (especially Vaporware)

**System Architects:**
- DEIA System Architecture (2 docs)
- Process Safeguards (BOK Injection)

---

### By Platform

**Netlify:**
- Nuclear Recovery Checklist
- Hugo Version Requirement
- DNS UI Confusion
- DNS Outage case study (Netlify context)
- Nuclear Recovery case study

**Squarespace:**
- DNS UI Confusion (delete-first requirement)

**Platform-agnostic:**
- All case studies (patterns apply broadly)
- All process docs

---

## Proactive Injection Triggers

**Trigger patterns to watch for in conversations:**

### Trigger: "delete" + "netlify" OR "recreate" OR "nuclear"

**Action:** Inject Nuclear Recovery Checklist BEFORE user proceeds
**Urgency:** CRITICAL
**Message:** "⚠️ I have a complete recovery checklist for delete/recreate. Review before proceeding to avoid 60+ min outage."

### Trigger: "dns" + "configure" OR "add domain"

**Action:** Inject DNS Outage case study (ask about registrar first)
**Urgency:** HIGH
**Message:** "Before configuring DNS, where is this domain registered? (Platform vs external registrar)"

### Trigger: "deploy" + "production" WITHOUT "test" OR "preview"

**Action:** Inject Direct-to-production anti-pattern
**Urgency:** HIGH
**Message:** "I see you're deploying to production. Have you tested locally and used deploy preview?"

---

## Cross-Cluster Relationships

**Deployment Safety ↔ DNS Configuration:**
- DNS issues cause deployment failures
- Nuclear option affects DNS configuration

**Deployment Safety ↔ Platform Gotchas:**
- Platform-specific recovery steps
- Requirements missed during recovery

**LLM Communication ↔ Process Safeguards:**
- Communication quality affects all docs
- Safeguards prevent communication failures

**Process Safeguards ↔ All clusters:**
- Quality control applies to all documentation
- BOK injection prevents issues in all domains

---

## Keywords for AI Matching

### Deployment Safety
- deployment, failed, broken, production, outage, down, recover, fix, nuclear, delete, recreate, build, hugo, environment-variables

### DNS Configuration
- dns, domain, registrar, nameserver, not-resolving, configure, netlify-dns, squarespace, records

### LLM Communication
- llm, instructions, incomplete, hallucination, privacy, attribution, communication, prerequisites, verification

### Process Safeguards
- vaporware, fact-checking, emergent-behavior, quality-control, safeguard, prevention, bok-injection

### Platform Gotchas
- netlify, hugo, platform, gotcha, requirement, ui-confusion

### DEIA Architecture
- factory-egg, egg, offline, deia, organizational, blueprint, architecture

---

## Implementation Notes

**For Phase 2 (Index Implementation):**

1. **YAML master index:**
   - Use these 7 clusters as top-level organization
   - Cross-reference documents in multiple clusters (views, not duplication)
   - Include all keywords, query patterns, urgency levels

2. **Query matching:**
   - Keyword → cluster → documents
   - Multi-cluster queries (deployment + netlify → intersection)
   - Fuzzy matching on keywords

3. **Proactive injection:**
   - Monitor for trigger patterns
   - Inject with urgency indicator
   - Pre-action warnings for critical triggers

4. **Quick reference:**
   - Generate Markdown from YAML
   - Organize by urgency first (critical/high/medium/low)
   - Include platform and audience filters

---

## Statistics

**Total documents:** 18 (13 public + 5 internal)
**Public clusters:** 6 (Cluster 7 is internal only)
**Cross-cluster documents:** 3 (appear in multiple clusters as views)
**Unique documents per cluster:**
- Deployment Safety: 5
- DNS Configuration: 2
- LLM Communication: 2
- Process Safeguards: 3
- Platform Gotchas: 3 (all cross-referenced)
- DEIA Architecture: 2

**By urgency:**
- Critical: 4 docs
- High: 5 docs
- Medium: 3 docs
- Low: 2 docs

**By audience:**
- DevOps: 8 docs (most served)
- AI Researchers: 6 docs
- Developers: 5 docs
- LLM Designers: 5 docs
- Technical Writers: 3 docs
- System Architects: 3 docs

---

## Validation

**Can answer these queries?**
- ✅ "DNS not working" → DNS Configuration cluster (2 docs)
- ✅ "deployment failed" → Deployment Safety cluster (5 docs)
- ✅ "using Netlify" → Platform Gotchas view (3 docs)
- ✅ "LLM hallucinated" → LLM Communication cluster (1 doc)
- ✅ "how to prevent mistakes" → Process Safeguards cluster (3 docs)
- ✅ "what is Factory Egg" → DEIA Architecture cluster (2 docs)

**Multiple access paths?**
- ✅ DNS Outage accessible via: DNS cluster, Deployment cluster, Platform view
- ✅ Nuclear checklist accessible via: Deployment cluster, Platform view
- ✅ All docs accessible by: urgency, audience, platform, problem

**Natural groupings?**
- ✅ Related docs cluster together (nuclear checklist + case study)
- ✅ Cross-cutting concerns handled (platform view)
- ✅ User mental models supported (problem-based, platform-based, urgency-based)

---

**Status:** Complete and ready for Phase 2 implementation
**Next:** Map to YAML master index structure
**Time to create:** ~90 minutes

**Tags:** `#taxonomy` `#practical` `#phase1-complete` `#ready-for-implementation`
