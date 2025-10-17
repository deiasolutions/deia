# Global Commons Quick Reference

**Version:** 1.0
**Last Updated:** 2025-10-16
**Documents:** 15 (public)
**Status:** Production

---

## 🚨 By Urgency (Start Here If Crisis)

### ⚡ CRITICAL - Production Down

**DNS outage? Domain not resolving?**
- **[DNS Outage Case Study](../../docs/global-commons/case-studies/dns-outage-registrar-confusion.md)** - Check registrar FIRST
- **[Netlify DNS UI Confusion](../../bok/platforms/netlify/dns-configuration-ui-confusion.md)** - Configure at registrar, not platform

**Deployment broken after delete/recreate?**
- **[Nuclear Recovery Checklist](../../bok/processes/netlify-nuclear-option-recovery.md)** - Complete recovery steps
- **[Nuclear Recovery Case Study](../../docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md)** - What went wrong

**Privacy/LLM hallucination issue?**
- **[Name Hallucination Incident](../../docs/global-commons/case-studies/llm-name-hallucination-incident.md)** - Attribution safeguards

### ⚠️ HIGH - Deployment/Recovery Issues

**Deployment failed?**
- **[Direct-to-Production Anti-Pattern](../../bok/anti-patterns/direct-to-production-deployment.md)** - Proper workflow
- **[Hugo Version Requirement](../../bok/platforms/netlify/hugo-version-requirement.md)** - Set HUGO_VERSION env var

**LLM communication issues?**
- **[Incomplete Instructions Pattern](../../docs/global-commons/case-studies/incomplete-instructions-pattern.md)** - Prerequisites matter

---

## 🔍 By Problem Type

### Deployment Failures
- Direct-to-Production Anti-Pattern (workflow + QA)
- Nuclear Recovery Checklist (delete/recreate)
- Nuclear Recovery Case Study (60+ min outage)
- Hugo Version Requirement (Netlify builds)
- DNS Outage Case Study (DNS causes failures)

### DNS Issues
- DNS Outage Case Study (registrar confusion)
- Netlify DNS UI Confusion (where to configure)

### LLM Communication
- Incomplete Instructions Pattern (missing prerequisites)
- Name Hallucination Incident (privacy violation)

### Prevention & Quality
- Vaporware Safeguard (fact-checking)
- Emergent Behavior Protocol (capability documentation)
- BOK Context Injection (prevent repeated mistakes)

### Architecture & Learning
- The Factory Egg (organizational design)
- Egg Offline Launch (Commons-disconnected operation)

### Platform Gotchas (Windows/Python)
- Windows Python Console UTF-8 Encoding (emoji/unicode output)

---

## 🛠️ By Platform

### Netlify (5 docs)
- **[Nuclear Recovery Checklist](../../bok/processes/netlify-nuclear-option-recovery.md)** ⚡ CRITICAL
- **[Hugo Version Requirement](../../bok/platforms/netlify/hugo-version-requirement.md)** ⚠️ HIGH
- **[DNS UI Confusion](../../bok/platforms/netlify/dns-configuration-ui-confusion.md)** ⚠️ HIGH
- **[DNS Outage Case Study](../../docs/global-commons/case-studies/dns-outage-registrar-confusion.md)** ⚡ CRITICAL
- **[Nuclear Recovery Case Study](../../docs/global-commons/case-studies/nuclear-option-incomplete-recovery.md)** ⚡ CRITICAL

**Quick Tips:**
- Always set `HUGO_VERSION=0.134.3`
- Configure DNS at registrar, not Netlify UI
- Before nuclear option: read the checklist!

### Squarespace
- **[DNS Configuration](../../bok/platforms/netlify/dns-configuration-ui-confusion.md)** - Delete existing records first

### Windows (1 doc)
- **[Python Console UTF-8 Encoding](../../bok/platforms/windows/python-console-utf8-encoding.md)** 📝 MEDIUM

**Quick Tips:**
- Add UTF-8 wrapper at top of all Python CLI scripts
- Fix applies when using emoji/unicode in console output
- Prevents `UnicodeEncodeError: 'charmap' codec` errors

---

## 👥 By Audience

### DevOps / Deployment Teams (8 docs)
**Critical:** DNS Outage, Nuclear Recovery (case + checklist)
**High:** Direct-to-prod, DNS UI, Hugo version

### AI Researchers / LLM Designers (6 docs)
**Critical:** Name hallucination
**High:** Incomplete instructions
**Medium:** Emergent behavior, Vaporware safeguard, BOK injection

### Developers (6 docs)
**Critical:** Nuclear checklist
**High:** Direct-to-prod, Hugo version
**Medium:** Windows Python UTF-8 encoding

### Technical Writers (3 docs)
**High:** Incomplete instructions
**Medium:** Vaporware safeguard

### System Architects (2 docs)
**Low:** Factory Egg, Offline launch

---

## 🎯 Quick Search

**"deployment failed"** → Deployment Safety (5 docs)
**"DNS not working"** → DNS Configuration (2 docs)
**"using Netlify"** → Platform Gotchas (5 docs)
**"LLM hallucinated"** → LLM Communication (2 docs)
**"prevent mistakes"** → Process Safeguards (3 docs)
**"what is Factory Egg"** → DEIA Architecture (2 docs)
**"Windows encoding error"** → Platform Gotchas Windows (1 doc)

---

## ⚠️ Proactive Warnings

If you're about to:
- **Delete/recreate Netlify** → READ NUCLEAR CHECKLIST FIRST!
- **Configure DNS** → Ask: where is domain registered?
- **Deploy to production** → Have you tested locally?

---

## 📚 All Documents (Alphabetical)

### BOK Entries (5)
1. Direct-to-Production Deployment Anti-Pattern
2. Netlify DNS Configuration UI Confusion
3. Hugo Version Requirement for Netlify
4. Netlify Nuclear Option Recovery Process
5. Windows Python Console UTF-8 Encoding Issue

### Case Studies (4)
1. DNS Outage from Registrar Confusion
2. Incomplete Procedural Instructions Pattern
3. LLM Name Hallucination Incident
4. Nuclear Option Without Complete Recovery

### Process Documents (3)
1. BOK Context Injection Proposal
2. Emergent Behavior Observation Protocol
3. Vaporware Safeguard

### Articles & Specs (2)
1. The Factory Egg (article)
2. Egg Offline Launch Capability (spec)

---

## 📊 Statistics

**By Urgency:**
- Critical: 4 docs
- High: 5 docs
- Medium: 4 docs (added Windows Python UTF-8)
- Low: 2 docs

**By Type:**
- Case Studies: 4 (CC BY 4.0)
- BOK: 5 (patterns/gotchas)
- Process: 3 (protocols)
- Articles/Specs: 2 (architecture)

**Most Relevant To:**
- DevOps (8 docs)
- Developers (6 docs) (added Python/Windows)
- AI Researchers (6 docs)

---

## 🤖 For AI Agents

**Query examples:**
```
"DNS not working" → dns-configuration cluster
"deployment failed" → deployment-safety cluster
"nuclear option" → INJECT checklist BEFORE proceeding
"LLM hallucination" → llm-communication-quality cluster
```

**Proactive injection:**
Watch for: "delete", "netlify", "recreate" → Inject nuclear checklist
Watch for: "dns", "configure" → Ask about registrar
Watch for: "UnicodeEncodeError", "charmap codec" → Inject Windows UTF-8 fix

---

**Maintained by:** LIBRARIAN-001 (future)
**Generated from:** `.deia/index/master-index.yaml`
**Index version:** 1.0
