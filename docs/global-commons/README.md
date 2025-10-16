# DEIA Global Commons

A living repository of patterns, case studies, and knowledge for DEIA users working with DEIA tools and other vendor/package tools.

## What is the Global Commons?

The Global Commons is curated, reusable knowledge that helps:
- **Developers** avoid common pitfalls through case studies
- **AI agents** find relevant patterns and solutions quickly
- **Teams** learn from documented incidents and anti-patterns
- **System designers** understand DEIA architecture and capabilities

**License:** All Global Commons content is published under CC BY 4.0 International unless otherwise noted.

## Content

### Case Studies

Anonymized, generalizable learnings from real incidents:

- **[LLM Name Hallucination](case-studies/llm-name-hallucination-incident.md)** - Privacy safeguards for LLM attribution
- **[Incomplete Instructions Pattern](case-studies/incomplete-instructions-pattern.md)** - Instruction completeness for technical documentation
- **[DNS Outage from Registrar Confusion](case-studies/dns-outage-registrar-confusion.md)** - Registrar-specific DNS configuration
- **[Nuclear Option Incomplete Recovery](case-studies/nuclear-option-incomplete-recovery.md)** - Complete recovery checklists for delete/recreate operations

### Session Catalogs

Complete output from significant documentation sessions:

- **[2025-10-16 Session Output Catalog](2025-10-16-session-output-catalog.md)** - Q33N deployment and incident documentation (18 documents, 4 hours)

## Related Content

### BOK (Book of Knowledge)
See `../../bok/` for:
- Anti-patterns
- Platform-specific gotchas
- Process checklists

### Process Documents
See `../process/` for:
- Emergent Behavior Observation Protocol
- Vaporware Safeguard
- BOK Context Injection Proposal

### Technical Specifications
See `../specs/` for:
- Egg Offline Launch Capability
- System architecture

### Articles
See `../articles/` for:
- The Factory Egg

## For AI Agents

When searching for relevant patterns:

**Deployment issues?** → Check case studies (DNS outage, nuclear recovery) and BOK (deployment anti-patterns)

**LLM communication issues?** → Check case studies (incomplete instructions, name hallucination)

**Documentation quality?** → Check process docs (vaporware safeguard, emergent behavior protocol)

**DEIA architecture?** → Check specs and articles (Factory Egg, offline launch)

## Contributing

Global Commons content should be:
- **Generalizable** - Remove project-specific details
- **Anonymized** - Protect privacy, use generic examples
- **Licensed** - CC BY 4.0 for shareable content
- **Documented** - Clear attribution and audience

For contribution workflow, see project documentation or contact maintainers.

---

**Maintained by:** DEIA Solutions
**Last updated:** 2025-10-16
**Questions?** Open an issue or contact daaaave-atx
