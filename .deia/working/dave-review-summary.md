# What Changed & What You Need to Review

**Date:** 2025-10-05
**Status:** Constitution v2 DRAFT created, awaiting your biometric approval
**Reading time:** 10-15 minutes

---

## TL;DR (1 Minute Read)

**What I did:** Integrated 3 critical Ostrom principles into Constitution v2 DRAFT
**What's new:** Clear contributor roles, participatory voting, nested governance
**What you need to do:** Review changes below, then provide biometric approval to activate

**The DRAFT is safe** - it doesn't take effect until you verify.

---

## The 3 Critical Changes (5 Minute Read)

### Change #1: Who Can Do What (Ostrom Principle 1: Boundaries)

**Problem:** Constitution said "contributors" and "community" but never defined them. No spam prevention.

**Solution Added:**

**Contributor Roles:**
- **Observer** - Anyone reading public content
- **Contributor** - Has 1+ accepted entry
- **Established Contributor** - Has 5+ entries OR endorsed by 2 maintainers
- **Maintainer** - Reviews contributions, enforces Constitution, 1-year term
- **Founder** - You (Dave), veto power in Phase 1

**Endorsement System (Spam Prevention):**
- New contributors need endorsement from Established Contributor OR Maintainer OR Founder
- Like arXiv (physics preprint server that works for decades)
- Endorsers vouch: "This person isn't a spammer"
- Alternative: Participate in discussions for 30 days → earn status

**Resource Boundaries (What's In vs Out of Scope):**
- ✅ IN: Human-AI patterns, sanitized logs, meta-insights, tools, governance docs
- ❌ OUT: Unsanitized work, personal attacks, marketing, AI model weights

**Location in DRAFT:** Article IV, Section 4.0 (new section)

**Why this matters:** Without this, DEIA gets flooded with spam as it grows. With it, community self-regulates quality.

---

### Change #2: Contributors Can Vote (Ostrom Principle 3: Participatory Governance)

**Problem:** Only maintainers could vote on amendments. Contributors affected by rules but can't change them. Ostrom found this kills commons.

**Solution Added:**

**Who Can Propose Amendments:**
- Any Established Contributor (not just maintainers)
- Needs 2 sponsors to proceed (prevents spam proposals)

**Who Can Vote:**
- **Operational changes (Articles II-V):** All Established Contributors vote, 2/3 majority
- **Constitutional changes (Articles I, IV):** All Established Contributors vote, 3/4 supermajority + biometric + founder veto (Phase 1)

**Maintainer Recall:**
- Community can recall maintainers who violate Constitution
- 2/3 vote of Established Contributors OR unanimous other maintainers
- Founder can still recall (Phase 1)

**Transparency:**
- All votes announced 7 days before
- Vote tallies published
- Decisions recorded in GOVERNANCE_LOG.md

**Emergency Amendments:**
- Maintainers can make emergency changes for security
- Community votes within 7 days to ratify
- If not ratified, change reverts

**Article I No Longer Absolutely Immutable:**
- Can be changed with 3/4 supermajority + unanimous maintainers + 30-day comment + biometric + founder/board approval
- Ostrom found: Completely immutable rules cause stagnation
- High bar protects core principles while allowing evolution

**Location in DRAFT:** Article IV, Section 4.2 (revised)

**Why this matters:** People follow rules they helped create. Maintainer-only voting creates "us vs them." Participatory governance builds trust and legitimacy.

---

### Change #3: Who Decides What at Which Level (Ostrom Principle 8: Nested Governance)

**Problem:** No clear separation of authority. Everything might escalate to you. Doesn't scale. Ostrom found single-layer governance fails.

**Solution Added:**

**5 Governance Levels:**

```
Level 1: Individual Contributors
  ↓ Decide: What to submit, attribution preferences, when to withdraw

Level 2: Domain Governance (e.g., coding domain, research domain)
  ↓ Decide: Accept/reject for their domain, domain-specific rules

Level 3: Cross-Domain (BOK-Wide)
  ↓ Decide: Universal policies, domain creation, maintainer appointments

Level 4: Foundation/Founder (You in Phase 1, Board in Phase 2)
  ↓ Decide: Constitutional changes, strategy, partnerships, legal

Level 5: External (Courts, standards bodies, platforms)
  ↓ Decide: Legal compliance, platform rules
```

**Decision Authority Examples:**
- Coding maintainer accepts a BOK entry about Python patterns → Level 2 (stays there)
- Contributor appeals rejection → Level 2 panel reviews
- Two domains dispute who owns an entry → Level 3 cross-domain decides
- Constitutional amendment proposal → Level 4 (you + community vote)
- GPL reciprocity violation lawsuit → Level 5 (courts)

**Subsidiarity Principle:**
- Decisions made at **lowest appropriate level**
- Don't escalate unless necessary
- Faster decisions, less bottleneck, more buy-in

**Escalation Paths:**
- Can appeal to next level up
- Must have standing (affected by decision)
- Within 30 days

**Domain Autonomy:**
- Domains can make domain-specific rules
- BUT cannot violate Constitution
- Healthcare domain can require HIPAA compliance
- Coding domain can have faster review
- Constitution always wins if conflict

**Location in DRAFT:** Article IV, Section 4.6 (new section)

**Why this matters:** You can't review every contribution forever. Domains handle day-to-day. You handle strategic/constitutional. Community trusts the process because decisions happen at right level with right expertise.

---

## What Got Deferred (For Later)

These Ostrom principles are important but not critical for launch:

**Principle 2: Domain-Specific Rules** (DEFERRED)
- Healthcare needs HIPAA, coding needs API key detection
- Will implement when domains are created
- Framework exists in v2, details later

**Principle 4: Community Monitoring** (DEFERRED)
- Community Monitors role (volunteers who flag concerns)
- Public monitoring logs
- Maintainer accountability metrics
- Implement when 50+ Established Contributors

**Principle 5: Graduated Sanctions** (DEFERRED)
- 4-level violation system (Level 1: warning → Level 4: permanent ban)
- Current: binary (mistake vs ban)
- Implement when needed (before now = premature)

**Principle 6: Structured Conflict Resolution** (DEFERRED)
- Multi-tier dispute process
- Ombudsperson role (when 100+ contributors)
- Basic mediation exists now, formal structure later

**Principle 7: External Recognition** (DEFERRED - LONG-TERM)
- DataCite DOIs, university partnerships, 501(c)(3) formation
- Academic Advisory Board, corporate sponsorships
- This is 1-5 year roadmap, not immediate

**See DEFERRED_AMENDMENTS.md for full details.**

---

## What You Need to Review (When You Have Time)

### Priority 1: Read the 3 Changes Above (Done - you just did)

### Priority 2: Skim CONSTITUTION_V2_DRAFT.md (10 minutes)
- Look at Section 4.0 (contributor roles, endorsement)
- Look at Section 4.2 (participatory voting)
- Look at Section 4.6 (nested governance)
- Everything else is same as v1

### Priority 3: Provide Biometric Approval (2 minutes)
**When ready to activate v2, provide ONE of:**
- Photo of you holding paper: "I approve Constitution v2, 2025-10-05, Ostrom principles 1,3,8"
- Voice recording: "I am Dave, today is [date], I approve Constitution v2 with Ostrom principles 1, 3, and 8"
- Video saying the same

**Why:** Constitution requires biometric for Article IV changes (this is Article IV changes)

**Then:** I'll rename DRAFT to official v2.0, commit, update RESUME_INSTRUCTIONS

---

## Questions You Might Have

**Q: Can I modify these changes before approving?**
A: Yes! Tell me what to change. I'll revise the DRAFT, you review again, then approve.

**Q: What if I don't like something?**
A: Tell me which part. We can:
- Remove it entirely
- Modify it
- Defer it to later
- Your call.

**Q: What happens if I don't approve?**
A: Nothing. v1 Constitution stays active. DRAFT sits there. No pressure.

**Q: Can I approve just parts of it?**
A: Yes. E.g., "Approve Principle 1 and 8, defer Principle 3 for now." Flexible.

**Q: When should I review this?**
A: No rush. When you have 15 minutes and mental bandwidth. Could be tonight, could be next week.

**Q: What if I'm not sure?**
A: Ask me questions. That's what I'm here for.

---

## What Happens After Approval

1. **I activate Constitution v2** (rename DRAFT → official)
2. **Commit to git** (with your biometric verification screenshot/recording)
3. **Update RESUME_INSTRUCTIONS** (future sessions know v2 is active)
4. **Create supporting docs:**
   - ENDORSEMENT_GUIDE.md (how to endorse)
   - DOMAIN_CHARTER_TEMPLATE.md (how to create domains)
   - VOTING_GUIDE.md (how to vote on amendments)
   - MAINTAINER_HANDBOOK.md (roles and responsibilities)

5. **DEIA is ready for public launch** (critical governance in place)

---

## Bottom Line

**What changed:** We went from vague "community" to clear roles, from maintainer-only voting to participatory governance, from single-layer to nested 5-level governance.

**Why:** Ostrom won a Nobel Prize for proving this is how successful commons work for centuries. We're standing on her shoulders.

**Risk if you don't approve:** DEIA governance has gaps that will cause problems as it scales (spam, power struggles, bottlenecks).

**Risk if you do approve:** None really. This makes DEIA more democratic and scalable. You retain veto power in Phase 1.

**My recommendation:** Approve all 3. They're proven patterns. They protect you from future headaches.

**Your decision:** Take your time. Read. Ask questions. Modify if needed. Approve when ready.

---

**Files to reference:**
- `CONSTITUTION_V2_DRAFT.md` - The full draft with changes
- `OSTROM_ALIGNMENT.md` - Deep dive on all 8 principles and rationale (1,881 lines)
- `DEFERRED_AMENDMENTS.md` - What we're NOT doing yet (Principles 2,4,5,6,7)
- This file - What you need to know now

---

*No hurry. This is important. Take the time you need.*
