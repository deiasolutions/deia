# Deferred Constitutional Amendments (Ostrom Principles 2, 4, 5, 6, 7)

**Date:** 2025-10-05
**Status:** Approved for deferral, implement when trigger conditions met
**Source:** OSTROM_ALIGNMENT.md

---

## Why These Are Deferred

**Implemented in v2.0:** Principles 1, 3, 8 (critical for launch)
**Deferred for later:** Principles 2, 4, 5, 6, 7 (important but not urgent)

**Rationale:**
- Constitution v2 has enough governance to launch safely
- These add refinement and scaling capability
- Implement when actually needed (not prematurely)
- Each has clear trigger condition for when to implement

---

## Principle 2: Congruence with Local Conditions (Domain-Specific Governance)

### What It Is

Different domains have different needs. Healthcare needs HIPAA compliance, coding needs API key detection, research needs citation standards. One-size-fits-all doesn't work.

### What We'd Add

**Article V, Section 5.4: Domain-Specific Governance**
- Each domain defines sanitization requirements beyond universal baseline
- Each domain creates templates appropriate to their field
- Each domain sets review criteria
- Example: Healthcare domain requires HIPAA Safe Harbor (18 identifiers), coding domain requires credential detection

**See OSTROM_ALIGNMENT.md Principle 2 for full text**

### Current State

- Constitution v2 has framework for domains (Section 4.0.4)
- Domains can be created via governance process
- Domain-specific rules mentioned but not detailed

### Trigger to Implement

**When:** 2nd domain is created (first is coding, when 2nd domain launches)

**Why:** First domain (coding) can use defaults. Second domain forces us to define how domains differ.

**Estimated timeline:** 3-6 months after launch

---

## Principle 4: Monitoring (Community-Based with Accountability)

### What It Is

Community members monitor for rule violations, not just hired moderators. Monitors are accountable to community. Transparent logs of what gets flagged and resolved.

### What We'd Add

**Article IV, Section 4.5: Community Monitoring and Accountability**
- Community Monitor role (opt-in, volunteer)
- Flag concerns using GitHub labels (`concern:privacy`, `concern:security`, etc.)
- Maintainers MUST respond to flags within 48 hours
- Public monitoring logs (MONITORING_LOG.md)
- Maintainer performance metrics (response time, flag resolution rate)
- Automated monitoring accountability (GitHub Actions logs detections)

**See OSTROM_ALIGNMENT.md Principle 4 for full text**

### Current State

- Constitution v2 has three-tier review (automated, maintainer, community 48-hr window)
- Community can comment but no formal flagging process
- No accountability metrics for maintainers

### Trigger to Implement

**When:** 50+ Established Contributors OR 500+ BOK entries

**Why:** With small community, informal works. At scale, need structure.

**Estimated timeline:** 6-12 months after launch

---

## Principle 5: Graduated Sanctions (4-Level Violation System)

### What It Is

Don't ban people immediately. Escalate: Level 1 (warning) → Level 2 (temporary restriction) → Level 3 (longer suspension) → Level 4 (permanent ban). Proportional consequences.

### What We'd Add

**Article VI (Revised): Enforcement with Graduated Sanctions**
- **Level 1 violations:** Minor (incomplete sanitization) → Warning, help them fix, no record
- **Level 2 violations:** Moderate (repeated carelessness) → 7-30 day suspension, formal warning
- **Level 3 violations:** Serious (PII in merged contribution) → 90-day suspension, public incident report, review by maintainer committee
- **Level 4 violations:** Critical (malicious intent) → Permanent ban immediately, law enforcement if illegal

**Violation tracking:** VIOLATIONS_LOG.md (private for Level 1-2, public for Level 3-4)
**Clean slate:** Violations older than 2 years expire if no repeat

**See OSTROM_ALIGNMENT.md Principle 5 for full text**

### Current State

- Constitution v2 has binary system (good faith mistake vs malicious = ban)
- No middle ground for carelessness
- No tracking of repeat violations

### Trigger to Implement

**When:** First instance of repeat careless contributor OR first dispute over ban being too harsh

**Why:** Current system works fine until we hit edge case. Then we need this.

**Estimated timeline:** Variable - could be month 1, could be year 1. Implement when needed.

---

## Principle 6: Conflict Resolution Mechanisms (Multi-Tier with Appeals)

### What It Is

Cheap, fast, accessible conflict resolution. Contributor disagrees with maintainer → Tier 1 (second opinion), still disagree → Tier 2 (panel), still disagree → Tier 3 (founder/board). Structured process with timeframes.

### What We'd Add

**Article IV, Section 4.3 (Revised): Conflict Resolution**

**Category A: Contribution Disputes**
- Tier 1: Second maintainer review (48 hrs)
- Tier 2: Maintainer panel (7 days)
- Tier 3: Community vote (14 days, requires 5+ sponsors)

**Category B: Conduct Disputes**
- Tier 1: Private mediation (7 days)
- Tier 2: Neutral panel (3 people: 1 maintainer + 2 Community Monitors, 14 days)
- Tier 3: Founder/board review (30 days)

**Category C: Governance Disputes** → Amendment process
**Category D: IP and Privacy Disputes** → Immediate action (24 hrs), content hidden pending investigation

**Community Ombudsperson role** (when 100+ Established Contributors)

**See OSTROM_ALIGNMENT.md Principle 6 for full text**

### Current State

- Constitution v2 has basic dispute resolution (open issue, maintainer mediates, community vote)
- No structure, no tiers, no timeframes guaranteed

### Trigger to Implement

**When:** First major dispute that current process can't resolve cleanly

**Why:** If basic process works, don't over-engineer. When it breaks, add structure.

**Estimated timeline:** 6-12 months. Hope we don't need it, but prepare for it.

---

## Principle 7: Recognition of Rights by External Authorities (Legitimacy & Legal Standing)

### What It Is

Universities, courts, companies, standards bodies recognize DEIA as legitimate institution. Requires legal entity (501c3), academic partnerships, DOIs, trademark, etc.

### What We'd Add

**Article VII (New): External Recognition and Institutional Relationships**

**7.1 Legal Entity Formation:**
- Phase 1: Unincorporated project (current)
- Phase 2: 501(c)(3) formation when trigger met
- Triggers: 100+ Established Contributors OR $10k donation commitments OR external partnership request

**7.2 Foundation Governance:**
- Board of Directors (7-9 seats)
- Founder permanent seat, Executive Director, elected community reps, domain reps, academic advisor, corporate sponsor rep

**7.3 Academic Recognition:**
- DataCite DOI registration (Year 1)
- University library partnerships
- Academic Advisory Board
- Research collaborations

**7.4 Standards Body Engagement:**
- IIBA, PMI, IEEE membership
- Contribute to AI standards development

**7.5 Corporate Recognition:**
- Vendor partnerships (Anthropic, Vercel, Railway)
- Corporate sponsorship tiers (Bronze/Silver/Gold)
- Reciprocity covenant enforcement

**7.6 Government Recognition:**
- NIH/NSF repository recognition
- Grant eligibility
- NIST collaboration

**7.7 Trademark Protection:**
- File "DEIA" trademark when foundation formed
- Protect against fraudulent use

**7.8 Reciprocity Enforcement:**
- Legal standing to sue for violations
- Model: GPL enforcement (15+ successful cases)

**See OSTROM_ALIGNMENT.md Principle 7 for full text**

### Current State

- Constitution v2 mentions foundation in governance (Section 4.6, Level 4)
- No timeline, no structure, no partnerships yet

### Triggers to Implement (Phased)

**Year 1 actions:**
- [ ] DataCite DOI registration
- [ ] Reach out to GKC Workshop (knowledge commons researchers)
- [ ] File provisional trademark (if budget)

**Year 1-2 (when trigger met):**
- [ ] Form 501(c)(3)
- [ ] Partner with university libraries
- [ ] Academic Advisory Board

**Year 2-3:**
- [ ] IEEE membership
- [ ] Grant applications
- [ ] Vendor partnerships formalized

**Year 3-5:**
- [ ] NIH repository recognition
- [ ] Corporate sponsorships
- [ ] International chapters (if demand)

**This is a 1-5 year roadmap, not urgent.**

---

## Implementation Priority & Timeline

### Critical (v2.0 - NOW)
✅ Principle 1: Boundaries and roles
✅ Principle 3: Participatory governance
✅ Principle 8: Nested governance

**Status:** In DRAFT Constitution v2, awaiting Dave's approval

---

### Important (v2.1-v2.5 - Next 3-12 Months)

**v2.1: Domain-Specific Governance (Principle 2)**
- Trigger: 2nd domain created
- Estimated: 3-6 months
- Urgency: Moderate (affects quality and domain autonomy)

**v2.2: Community Monitoring (Principle 4)**
- Trigger: 50+ Established Contributors OR 500+ BOK entries
- Estimated: 6-12 months
- Urgency: Moderate (affects accountability and scaling)

**v2.3: Graduated Sanctions (Principle 5)**
- Trigger: First repeat careless contributor OR ban dispute
- Estimated: Variable (could be month 1, could be year 1)
- Urgency: Low until triggered, then high

**v2.4: Conflict Resolution (Principle 6)**
- Trigger: First major unresolved dispute
- Estimated: 6-12 months
- Urgency: Low until triggered, then high

---

### Strategic (v3.0+ - Year 1-5)

**v3.0: External Recognition (Principle 7)**
- Trigger: Phased (see timeline above)
- Estimated: 1-5 years
- Urgency: Low (long-term legitimacy and sustainability)

---

## How to Implement When Triggered

### Process

1. **Trigger condition met** (e.g., 2nd domain created)
2. **Pull amendment text** from this document
3. **Customize if needed** (adapt to actual circumstances)
4. **File amendment proposal** per Constitution v2 Section 4.2.1
5. **Community discussion** (14 days)
6. **Community vote** (7 days, 2/3 majority)
7. **Founder approval** (Phase 1) or Board approval (Phase 2)
8. **Merge to Constitution** (within 48 hours)

### Accountability

**Who monitors triggers:**
- Maintainers track contributor counts, BOK entries, domains
- Quarterly review: Are any triggers met?
- If triggered, maintainer proposes amendment

**Transparency:**
- Triggers published in GOVERNANCE_LOG.md
- When met, announced to community
- Amendment process begins

---

## Benefits of Deferred Implementation

**Avoids premature optimization:**
- Don't build community monitoring when there are only 5 contributors
- Don't build conflict resolution tiers when no conflicts exist
- Don't form 501(c)(3) when no funding to manage

**Allows learning:**
- See what actually happens in practice
- Adapt amendments based on real experience
- Ostrom emphasized: Rules should fit local conditions, which emerge over time

**Maintains focus:**
- v2.0 focuses on critical governance (boundaries, participation, levels)
- Later versions add refinement
- Incremental improvement, not boil-the-ocean

**Respects Dave's time:**
- Review 3 critical changes now
- Review 5 additional changes later when needed
- Spread cognitive load over time

---

## Complete Amendment Text

**All 5 deferred principles have full amendment text ready in OSTROM_ALIGNMENT.md.**

When trigger is met:
1. Open OSTROM_ALIGNMENT.md
2. Find the principle (2, 4, 5, 6, or 7)
3. Copy proposed amendment text
4. Follow amendment process above

**No need to reinvent. Just activate when ready.**

---

## Questions & Answers

**Q: Can we implement these sooner if we want?**
A: Yes! Triggers are "no sooner than," not "must wait until." If Dave says "I want Principle 5 now," we do it.

**Q: Can we skip any of these entirely?**
A: Technically yes, but not recommended. Ostrom found these are all necessary for successful commons at scale. Skipping = risk.

**Q: Can we modify the trigger conditions?**
A: Yes, via amendment process. If we think 50+ contributors is too many for Community Monitors, lower it.

**Q: What if we hit multiple triggers at once?**
A: Implement in priority order (2 → 4 → 5 → 6 → 7). Or batch them into single amendment if they're compatible.

**Q: Who decides when trigger is "met"?**
A: Objective triggers (50+ contributors, 2nd domain) = self-evident. Subjective triggers (first unresolved conflict) = maintainer judgment + community consensus.

---

## Summary Table

| Principle | Topic | Trigger | Timeline | Urgency |
|-----------|-------|---------|----------|---------|
| 2 | Domain-Specific Rules | 2nd domain created | 3-6 months | Moderate |
| 4 | Community Monitoring | 50+ contributors OR 500+ entries | 6-12 months | Moderate |
| 5 | Graduated Sanctions | Repeat careless contributor OR ban dispute | Variable | Low→High |
| 6 | Conflict Resolution | First major unresolved conflict | 6-12 months | Low→High |
| 7 | External Recognition | Phased (DOIs Year 1, 501c3 Year 1-2, etc.) | 1-5 years | Low (strategic) |

---

**All deferred amendments are ready to implement when conditions warrant.**

**Full text in OSTROM_ALIGNMENT.md.**

**No action needed now. Come back when triggered.**
