# Global Commons Quick Reference - SAMPLE

**Status:** Draft / Awaiting GPT-5 taxonomy for finalization
**Last Updated:** 2025-10-16
**Documents Indexed:** 18

---

## 🚨 By Problem Type (Critical/High Priority)

### Production Down - DNS Issues

**DNS outage? Domain not resolving?**
- **[DNS Outage from Registrar Confusion](../../docs/global-commons/case-studies/dns-outage-registrar-confusion.md)** ⚡ CRITICAL
  - Check where domain is registered first (platform vs external)
  - Never delete DNS records without knowing registrar
- **[Netlify DNS UI Confusion](../../bok/platforms/netlify/dns-configuration-ui-confusion.md)** ⚠️ HIGH
  - Configure DNS at registrar, not in Netlify UI
  - Squarespace: delete existing records first

### Deployment Broken - Recovery Needed

**Deployment failed? Site broken after changes?**
- **[Nuclear Option Recovery Checklist](../../bok/processes/netlify-nuclear-option-recovery.md)** ⚡ CRITICAL
  - Complete checklist for delete/recreate (build config, env vars, DNS, verification)
  - Don't mark "complete" without verification
- **[Nuclear Recovery Case Study](../../docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md)** ⚡ CRITICAL
  - What happens when recovery is incomplete (60+ min outage)
- **[Direct-to-Production Anti-Pattern](../../bok/anti-patterns/direct-to-production-deployment.md)** ⚠️ HIGH
  - Proper Git workflow and QA process

### LLM Communication Issues

**LLM giving bad advice? Privacy concerns?**
- **[Name Hallucination Incident](../../docs/global-commons/case-studies/llm-name-hallucination-incident.md)** ⚡ CRITICAL
  - Never infer real names, always use provided handles
  - Privacy safeguards for attribution
- **[Incomplete Instructions Pattern](../../docs/global-commons/case-studies/incomplete-instructions-pattern.md)** ⚠️ HIGH
  - Always include prerequisite steps
  - Don't assume user remembers previous instructions

---

## 🛠️ By Platform

### Netlify

**All Netlify-specific documentation:**
- **[Nuclear Option Recovery](../../bok/processes/netlify-nuclear-option-recovery.md)** ⚡ Complete delete/recreate checklist
- **[Hugo Version Requirement](../../bok/platforms/netlify/hugo-version-requirement.md)** ⚠️ Must set HUGO_VERSION env var
- **[DNS UI Confusion](../../bok/platforms/netlify/dns-configuration-ui-confusion.md)** ⚠️ Where to configure DNS
- **[DNS Outage Case Study](../../docs/global-commons/case-studies/dns-outage-registrar-confusion.md)** ⚡ Registrar confusion
- **[Nuclear Recovery Case Study](../../docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md)** ⚡ Incomplete recovery

**Quick Tips:**
- Always set `HUGO_VERSION=0.134.3` in environment variables
- Configure DNS at registrar, not Netlify UI
- After nuclear option: verify build settings, env vars, domains, DNS

### Squarespace

- **[DNS Configuration](../../bok/platforms/netlify/dns-configuration-ui-confusion.md)** - Delete existing records before adding new ones

---

## 👥 By Audience

### DevOps / Deployment Teams

**Critical:**
- DNS Outage case study
- Nuclear Recovery case study + checklist

**High:**
- Direct-to-production anti-pattern
- DNS UI confusion
- Hugo version requirement

### AI Researchers / LLM System Designers

**Critical:**
- Name Hallucination incident

**High:**
- Incomplete Instructions pattern

**Learning:**
- Emergent Behavior Observation Protocol
- Vaporware Safeguard
- BOK Context Injection Proposal

### Developers

**High:**
- Direct-to-production anti-pattern
- Hugo version requirement (if using Hugo)
- Nuclear recovery checklist

### Technical Writers / Documentation Teams

**High:**
- Incomplete Instructions pattern

**Process:**
- Vaporware Safeguard
- Emergent Behavior Protocol

### System Architects

**Architecture:**
- The Factory Egg article
- Egg Offline Launch Capability spec

---

## 📚 By Content Type

### Case Studies (Learning from Real Incidents)

All published under CC BY 4.0, anonymized for public sharing

1. **[LLM Name Hallucination](../../docs/global-commons/case-studies/llm-name-hallucination-incident.md)** ⚡
   - Privacy violation risk from hallucinated names
2. **[Incomplete Instructions Pattern](../../docs/global-commons/case-studies/incomplete-instructions-pattern.md)** ⚠️
   - Omitted prerequisite steps cause user frustration
3. **[DNS Outage from Registrar Confusion](../../docs/global-commons/case-studies/dns-outage-registrar-confusion.md)** ⚡
   - 3 domains down from not checking registrar
4. **[Nuclear Option Without Complete Recovery](../../docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md)** ⚡
   - 60+ min outage from incomplete verification

### BOK Entries (Patterns & Platform Knowledge)

Anti-patterns, gotchas, and process checklists

1. **[Direct-to-Production Deployment](../../bok/anti-patterns/direct-to-production-deployment.md)** ⚠️
   - Anti-pattern: Proper Git workflow and QA
2. **[Netlify DNS UI Confusion](../../bok/platforms/netlify/dns-configuration-ui-confusion.md)** ⚠️
   - Platform gotcha: Where to configure DNS
3. **[Hugo Version Requirement](../../bok/platforms/netlify/hugo-version-requirement.md)** ⚠️
   - Platform requirement: Must set env var
4. **[Netlify Nuclear Option Recovery](../../bok/processes/netlify-nuclear-option-recovery.md)** ⚡
   - Process checklist: Complete recovery steps

### Process Documents (Protocols & Safeguards)

Quality controls and system improvements

1. **[Emergent Behavior Observation Protocol](../../docs/process/emergent-behavior-observation-protocol.md)**
   - How to document unexpected LLM behaviors
2. **[Vaporware Safeguard](../../docs/process/vaporware-safeguard.md)**
   - Prevent aspirational claims from becoming canon
3. **[BOK Context Injection Proposal](../../docs/process/bok-context-injection-proposal.md)**
   - Auto-inject relevant BOK based on keywords

### Articles & Specs (Architecture & Vision)

1. **[The Factory Egg](../../docs/articles/the-factory-egg.md)**
   - Self-describing organizational blueprints
2. **[Egg Offline Launch Capability](../../docs/specs/egg-offline-launch-capability.md)**
   - How Eggs work Commons-disconnected

---

## 🔍 Quick Search Patterns

**"I'm seeing..."**
- Deployment failures → Deployment Safety cluster
- DNS errors → DNS Configuration cluster
- Incomplete LLM instructions → LLM Communication Quality cluster

**"I'm using..."**
- Netlify → Platform Gotchas cluster (3 critical, 2 high priority docs)
- Squarespace → DNS Configuration (delete-first requirement)

**"I need to..."**
- Delete and recreate deployment → Nuclear Recovery Checklist (CRITICAL - read before proceeding!)
- Prevent deployment mistakes → Direct-to-production anti-pattern
- Document an incident → Case studies for format examples
- Understand Factory Egg → Articles cluster

**"How do I avoid..."**
- DNS outages → DNS Configuration cluster (2 docs)
- Deployment disasters → Deployment Safety cluster (3 docs)
- LLM communication problems → LLM Communication Quality cluster (2 docs)

---

## ⚡ Urgency Guide

**CRITICAL (Production Down):**
- DNS Outage case study
- Nuclear Recovery case study + checklist
- Name Hallucination incident

**HIGH (Deployment/Recovery):**
- Direct-to-production anti-pattern
- Incomplete Instructions pattern
- DNS UI confusion
- Hugo version requirement

**MEDIUM (Prevention/Process):**
- Emergent Behavior Protocol
- Vaporware Safeguard
- BOK Injection Proposal

**LOW (Learning/Architecture):**
- Factory Egg article
- Offline Launch spec

---

## 📊 Statistics

**Content:**
- 4 Case Studies (anonymized, CC BY 4.0)
- 4 BOK Entries (anti-patterns, gotchas, processes)
- 3 Process Documents (protocols, safeguards)
- 1 Article (Factory Egg)
- 1 Specification (Offline Launch)

**By Urgency:**
- Critical: 4 docs
- High: 5 docs
- Medium: 3 docs
- Low: 2 docs

**By Audience:**
- DevOps: 8 docs
- AI Researchers: 6 docs
- Developers: 5 docs
- LLM System Designers: 5 docs
- Technical Writers: 3 docs
- System Architects: 3 docs

---

## 🤖 For AI Agents

**Query Examples:**
```
"DNS not working" → dns-configuration cluster (2 docs)
"deployment failed" → deployment-safety cluster (3 docs)
"nuclear option" → PROACTIVE INJECT nuclear checklist
"LLM hallucination" → llm-communication-quality cluster
```

**Proactive Injection Triggers:**
- "delete netlify project" → Inject nuclear checklist BEFORE proceeding
- "recreate deployment" → Inject nuclear checklist + case study
- "configure dns" → Inject registrar confusion warning

---

**Note:** This is a SAMPLE quick reference. Final version will incorporate taxonomy from GPT-5 (Bot D).

**Maintained by:** LIBRARIAN-001 (future)
**Generated from:** `.deia/index/master-index.yaml`
**Format:** Human-readable Markdown for quick scanning
