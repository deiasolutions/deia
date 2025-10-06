# DEIA Working Decisions & Open Questions

**Purpose:** Track decisions, open questions, and context as we build DEIA. Don't lose important ideas.

**Last Updated:** 2025-10-05

---

## Section 1: Platform Integration & Vendor Collaboration

### Context
We want to reduce friction where Claude has to ask humans to manually check platform dashboards (Vercel, Railway, AWS, etc.). Solution: work with vendors to create APIs/MCP servers that Claude can query directly.

### Open Questions

**Q1: Should we add "Platform Friction" tracking to DEIA immediately or phase 2?**
- Pros of now: Start collecting data from day 1, stronger vendor pitch later
- Pros of later: Don't overcomplicate MVP, focus on core knowledge pipeline first
- **Decision:** [ ]

**Q2: API-first or blockchain-first approach?**

**Option A: API-First, Blockchain Later**
- Start with standard API keys for auth
- Add blockchain audit trail in phase 2
- Simpler to implement and explain to vendors
- Faster adoption

**Option B: Full Web3 from Day One**
- DIDs (Decentralized Identifiers) for Claude instances
- Smart contracts for permissions
- Blockchain for immutable audit logs
- More complex but future-proof

- **Decision:** [ ]

**Q3: Which blockchain if we go that route?**
- Ethereum (established, expensive gas)
- Polygon (cheaper, still EVM-compatible)
- Solana (fast, different ecosystem)
- Hyperledger (private/permissioned, enterprise-friendly)
- Just use Git commits + GPG signatures (simplest "blockchain")
- **Decision:** [ ]

**Q4: Immediate vendor outreach or build proof-of-concept first?**
- Wait until we have: 100+ sessions showing pain points?
- Or: Reach out now with spec and ask for collaboration?
- **Decision:** [ ]

### Related Ideas to Explore
- [ ] Research: Which platforms already have MCP servers?
- [ ] Research: Does Vercel/Railway have APIs that cover our needs already?
- [ ] Draft: Email template for vendor outreach
- [ ] Create: Standard "Platform Friction" section in session log template

---

## Section 2: DEIA Core Structure

### Open Questions

**Q5: Repository name?**
- `deia` (short, clean)
- `deia-pipeline` (more descriptive)
- `ai-dev-insights` (self-explanatory)
- **Decision:** [ ] Leaning toward: `deia`

**Q6: What does DEIA stand for?**
Options discussed:
- **Development Evidence & Insights Automation** (current favorite)
- Developer Experience Intelligence Archive
- Dev Event Intelligence Aggregator
- Development Extraction, Insights & Analysis
- **Decision:** [ ]

**Q7: Licensing?**
- MIT (permissive, simple)
- Apache 2.0 (permissive + patent protection)
- GPL v3 (copyleft, derivatives must be open)
- Hybrid: MIT for code, CC-BY-SA for BOK entries
- **Decision:** [ ] Constitution suggests MIT + CC-BY

**Q8: Initial platforms to support?**
Must-haves:
- [ ] Claude Code
- [ ] Cursor
- [ ] GitHub Copilot

Nice-to-haves:
- [ ] Windsurf
- [ ] Aider
- [ ] Continue.dev
- [ ] Cody

**Decision:** [ ] Start with what we use, add via community contributions?

---

## Section 3: BOK Format & Standards

### Open Questions

**Q9: BOK entry format?**

**Option A: Markdown with YAML frontmatter**
```yaml
---
id: bok-001
date: 2025-10-05
platforms: [claude-code, cursor]
category: pattern
confidence: validated
sources: 5
---
# Pattern: Iterative Prompting for Refactoring
[content...]
```

**Option B: Pure JSON (MCP-native)**
```json
{
  "id": "bok-001",
  "date": "2025-10-05",
  "platforms": ["claude-code", "cursor"],
  "category": "pattern",
  "content": "..."
}
```

**Option C: Hybrid (JSON metadata + MD content)**

- **Decision:** [ ]

**Q10: Aggregation threshold?**
Constitution says "minimum 3 sources before publishing patterns"
- Is 3 enough?
- Should it vary by confidence level?
- **Decision:** [ ]

---

## Section 4: Security & Privacy

### Open Questions

**Q11: Pre-commit hooks - required or optional?**
- Required: Better security, might deter casual contributors
- Optional: Easier onboarding, relies on PR checks
- **Decision:** [ ] Constitution implies optional but recommended

**Q12: Do we need a security officer/team?**
- Maintainers handle it initially?
- Or: Dedicated security role from day 1?
- **Decision:** [ ]

**Q13: PII detection - which tool/library?**
- Microsoft Presidio (ML-based, comprehensive)
- Custom regex (simpler, faster)
- Hybrid approach
- **Decision:** [ ] Build custom first, add Presidio later?

---

## Section 5: Community & Governance

### Open Questions

**Q14: How many initial maintainers?**
- Just Dave to start?
- Invite 2-3 trusted contributors?
- **Decision:** [ ]

**Q15: Contribution acceptance criteria?**
What makes a "good" contribution?
- Follows template
- Passes security scan
- Provides genuine insight
- Well-written
- **All of the above?**
- **Decision:** [ ] Draft acceptance rubric

**Q16: Community platforms?**
- GitHub Discussions (primary)
- Discord server (real-time chat)
- Subreddit
- LinkedIn group (professional)
- **Decision:** [ ] Start with GitHub Discussions only?

---

## Section 6: Whitepapers & Publications

### Topics to Write About

**Whitepaper 1: The DEIA Methodology**
- Why we built this
- How it works
- Community benefits
- Call to action

**Whitepaper 2: Platform Integration Spec**
- API requirements for AI assistants
- MCP server design patterns
- Blockchain audit trails
- Vendor collaboration framework

**Whitepaper 3: Human-AI Collaboration Insights**
- Meta-learnings from aggregated sessions
- What works, what doesn't
- Capability mapping
- Future of AI-assisted development

**Priority order?**
- **Decision:** [ ]

### Where to Publish?

- [ ] arXiv (academic preprint)
- [ ] Medium (accessible, wide reach)
- [ ] LinkedIn Articles (professional audience)
- [ ] Dev.to (developer community)
- [ ] Company blog (if DEIA Solutions has one)
- [ ] All of the above with cross-posting?

**Decision:** [ ]

---

## Section 7: Implementation Priorities

### What to Build First?

**Tracking options:**
- [ ] Finalize repo structure
- [ ] Write main README.md
- [ ] Create session log templates (all platforms)
- [ ] Build auto-sanitizer script (Python)
- [ ] Set up GitHub Actions workflows
- [ ] Create example sessions (sanitized)
- [ ] Draft platform integration spec
- [ ] Build blockchain audit prototype
- [ ] Vendor outreach to Vercel/Railway
- [ ] Write whitepaper #1
- [ ] Launch announcement (Reddit, HN, LinkedIn)

**Proposed order:**
1. [ ] Repo structure + README (foundation)
2. [ ] Templates (let people start contributing)
3. [ ] Security scanning (protect privacy)
4. [ ] Example sessions (show value)
5. [ ] Whitepaper #1 (explain vision)
6. [ ] Launch (get community)
7. [ ] Platform integration work (phase 2)

**Your priority?**
- **Decision:** [ ]

---

## Section 8: Name & Branding

### Visual Identity

**Logo ideas:**
- Pipeline/flow imagery (data flowing through stages)
- Book/knowledge metaphor (BOK)
- Human + AI collaboration visual
- Abstract/minimalist

**Decision:** [ ] Defer to designer or keep simple?

**Color scheme:**
- Tech blue/purple (common in dev tools)
- Green (growth, learning)
- Orange (energy, innovation)
- Monochrome (professional, timeless)

**Decision:** [ ]

**Tagline finalists:**
- "Learn from every session. Build better with AI."
- "Capturing the intelligence in AI-assisted development"
- "Turn conversations into knowledge"
- "Your AI pair programming memory"
- "Collective intelligence for AI developers"
- "Learn together. Protect each other. Build better."

**Decision:** [ ] Current favorite: "Learn together. Protect each other. Build better."

---

## Section 9: Long-term Vision

### Aspirational Goals

**Year 1:**
- [ ] 100+ contributors
- [ ] 1,000+ session logs in pipeline
- [ ] 3+ platform integrations (Claude Code, Cursor, Copilot)
- [ ] At least 1 vendor partnership (Vercel or Railway)
- [ ] Published whitepaper on methodology

**Year 2:**
- [ ] 10,000+ sessions
- [ ] MCP servers adopted by major platforms
- [ ] Academic research using DEIA data
- [ ] Standards body recognition (W3C, IEEE?)
- [ ] Sustainable funding model (grants, sponsorships)

**Year 3:**
- [ ] Industry standard for AI dev knowledge sharing
- [ ] Blockchain audit trail widely adopted
- [ ] DEIA methodology taught in CS curriculums
- [ ] Measurable improvement in human-AI collaboration effectiveness

### Metrics to Track

How do we measure success?
- Number of contributors
- Number of sessions logged
- Number of BOK entries
- Platform adoptions
- Vendor partnerships
- Community engagement (GitHub stars, discussions)
- Whitepapers published
- Media coverage

**Decision:** [ ] Set up analytics from day 1?

---

## Section 10: Long-Term Governance & Sustainability

### Non-Profit Foundation Vision

**Proposal from Dave (2025-10-05):**
> "I propose we create a non-profit that can accept donations and do this at scale."

**Why this is necessary:**
- Dave can't review all contributions forever (not scalable)
- Quality control requires dedicated resources
- Infrastructure costs money (hosting, security, legal)
- Community needs sustainable governance structure

### Governance Evolution Path

**Phase 1: Benevolent Dictator (Year 0-1)**
- Dave reviews/approves all contributions
- Small team of trusted maintainers help
- Quality standards established
- Community built

**Phase 2: Foundation Transition (Year 1-2)**
- Form 501(c)(3) non-profit (or appropriate structure)
- Transfer repo ownership to foundation
- Establish governance board
- Dave remains as technical lead/founding board member

**Phase 3: Sustainable Operations (Year 2+)**
- Paid maintainers from donations/grants
- Community governance model
- Vendor partnerships
- Academic/research collaborations
- Self-sustaining operations

### Foundation Structure (Draft)

**Name candidates:**
- DEIA Foundation
- Foundation for AI Development Intelligence
- Open AI Development Knowledge Foundation
- Collaborative AI Development Foundation

**Mission (Draft):**
"To advance human-AI collaboration through open knowledge sharing, enabling developers worldwide to learn from collective experience while protecting individual privacy and intellectual property."

**Revenue streams:**
- Individual donations (GitHub Sponsors, OpenCollective)
- Corporate sponsorships (AI vendors, platform providers)
- Grants (NSF, Mozilla, Open Source Initiative)
- Vendor partnerships (integration fees, MCP server development)
- Conference/training programs

**Operating expenses:**
- Paid maintainers (full-time contribution review)
- Infrastructure (servers, GitHub Actions, storage)
- Security audits
- Legal/compliance
- Community management
- Whitepaper publication
- Conference organization

**Governance board (future):**
- Founder (Dave - permanent or term-limited seat)
- Technical maintainers (2-3 seats)
- Community representatives (2-3 elected seats)
- Corporate advisors (1-2 from sponsors)
- Academic advisor (1 seat)

### Review Process Scaling

**Near-term (Dave alone):**
1. Automated pre-screening (secrets, PII, template validation) - rejects ~30%
2. Trusted reviewers (3-5 people) - handle low-risk PRs
3. Dave - final authority on all high-risk changes

**Long-term (with foundation):**
1. Automated screening
2. Paid maintainers (2-3 full-time) - primary reviewers
3. Community moderators - triage and recommend
4. Governance working groups (Security, Privacy, Content)
5. Board - handles disputes and major decisions
6. Dave - oversight, not every PR

### Timeline (Tentative)

**Month 0-3:**
- Dave reviews everything
- Build initial community
- Target: 50-100 contributors

**Month 3-6:**
- Add trusted reviewers
- Set up donation infrastructure
- Publish first whitepaper
- Start accepting donations

**Month 6-12:**
- Grow to 500+ contributors
- Hire first part-time maintainer (if funded)
- Draft non-profit bylaws
- Plan first conference

**Year 2:**
- Form non-profit
- Transfer ownership
- Establish board
- Apply for grants
- Hire full-time maintainers

**Year 3+:**
- Sustainable operations
- Annual conference
- Academic partnerships
- Vendor integrations

### Open Questions

**Q: What legal structure?**
- 501(c)(3) non-profit (US)
- B-Corp
- Foundation in different jurisdiction
- **Decision:** [ ] Research with lawyer

**Q: When to form foundation?**
- After reaching donation threshold ($X/month)?
- After hitting contributor count (N contributors)?
- After Year 1 regardless?
- **Decision:** [ ]

**Q: Board composition?**
- How many seats?
- How are community reps elected?
- Term limits?
- Dave's role long-term?
- **Decision:** [ ]

**Q: Donation platforms?**
- GitHub Sponsors (easiest for devs)
- OpenCollective (transparent budgeting)
- Both?
- **Decision:** [ ]

**Q: Early sponsorship approach?**
- Wait until we have traction?
- Approach Anthropic/OpenAI early as founding sponsors?
- Vendor partnerships first (Vercel/Railway)?
- **Decision:** [ ]

**Q: Name and branding for foundation?**
- Keep "DEIA Foundation" simple?
- Or more descriptive name?
- **Decision:** [ ] Defer until closer to formation

### Related Documents to Create

- [ ] `GOVERNANCE.md` - Current structure and future plans
- [ ] `CONTRIBUTING.md` - How to submit, what Dave reviews
- [ ] `SPONSORSHIP.md` - Tiers and benefits (when ready)
- [ ] `FOUNDATION_BYLAWS.md` - Draft bylaws (Year 1)
- [ ] `CODE_OF_CONDUCT.md` - Community standards

---

## Section 11: Multi-Domain Expansion Vision

### The Bigger Picture (2025-10-05)

**Dave's insight:**
> "What if we had AI helping a researcher, and his AI could upload a best practice, like a lab technique that someone found that worked. Shit ANY domain where people are using AI to do things, there is the opportunity to learn from the work."

**This isn't just about coding. It's about human-AI collaboration across ALL domains.**

### Gap in Current Landscape

**What exists (top-down):**
- MIT Atlas of Human-AI Interaction (1000+ research papers analyzed)
- Microsoft Guidelines (20 years of research, corporate)
- AI Standards Hub (governance, policy)
- Academic frameworks and taxonomies

**What's missing (bottom-up):**
- Practitioner-driven knowledge sharing
- Domain-agnostic repository
- Privacy-preserving platform for real-world experiences
- Actionable patterns from actual users
- Cross-domain learning

**DEIA fills this gap.**

### Multi-Domain Architecture

**Domains to support:**
- `coding/` - Software development (current focus)
- `research/` - Scientific research (biology, physics, social science)
- `writing/` - Content creation (journalism, technical, creative)
- `design/` - Visual/UX design
- `healthcare/` - Medical/clinical (diagnostics, treatment planning)
- `legal/` - Legal research and brief writing
- `education/` - Teaching (lesson planning, assessment)
- `business/` - Strategy, data analysis, market research

**Each domain gets:**
- Domain-specific templates
- Domain-specific sanitization rules
- Domain-specific BOK
- Domain-specific maintainers
- Shared governance framework

### Universal Pattern

**Every domain has same pain point:**
> "Having to re-explain preferences/best practices to AI every session"

**DEIA solves it:**
1. Discover pattern while working with AI
2. Share to domain-specific BOK (sanitized)
3. Others bootstrap with proven patterns
4. AI reads START_HERE.md with domain best practices

### Examples of Cross-Domain Patterns

**Pattern discovered in research:**
"Ask 'What are the constraints?' before 'What's the solution?'"

**Applies to:**
- Coding: Understand constraints before implementing
- Writing: Understand audience/format before writing
- Design: Understand requirements before designing
- Legal: Understand jurisdiction/precedents before researching

**Shared to:** `bok/meta/interaction-patterns/constraints-first.md`

### Implementation

**Installation:**
```bash
pip install deia
deia init --domain research-biology
deia init --domain coding-python
```

**Each domain gets:**
- Domain-specific directory structure
- Customized templates
- Sanitization rules for that field
- Connection to domain-specific BOK

### Governance at Scale

**Domain-specific governance:**
- Each domain has maintainers (experts in that field)
- Ethical review for sensitive domains (healthcare, legal)
- Sanitization appropriate to field (lab data vs code vs patient info)

**Foundation board (updated):**
- Cross-domain representation (1 seat per major domain)
- Governance seats (founder, security, ethics)
- Sponsor seats (corporate, academic)
- Domain representatives elected by contributors

### Why This Matters

**Current state:**
- Knowledge about human-AI collaboration is siloed
- Researchers don't learn from coders don't learn from writers
- Each person rediscovers patterns others already found
- No systematic way to capture and share what works

**With DEIA:**
- Cross-pollination of patterns across domains
- New users bootstrap with proven techniques
- Systematic capture of what works (and what doesn't)
- Privacy-preserving so people can share sensitive work

**This could become foundational infrastructure for how humanity learns to work with AI.**

### Open Questions

**Q: How do we prioritize domains for expansion?**
- Start with coding (MVP)
- Add research next? (high value, publishable)
- Or writing? (large user base, easier sanitization)
- **Decision:** [ ]

**Q: Domain-specific foundations vs one unified foundation?**
- Single foundation with domain working groups?
- Or separate foundations (DEIA for Code, DEIA for Research, etc.)?
- **Decision:** [ ] Start unified, split if needed

**Q: How to recruit domain experts as maintainers?**
- Partnerships with professional associations?
- Academic collaborations?
- Industry outreach?
- **Decision:** [ ]

**Q: Licensing for sensitive domains?**
- Healthcare: HIPAA considerations
- Legal: Attorney-client privilege
- Research: Unpublished data, patents
- Need domain-specific legal review?
- **Decision:** [ ] Consult lawyers before expanding to regulated domains

---

## Section 12: Immediate Next Steps

### Action Items from Current Session (2025-10-05)

**Completed:**
- [x] Created DEIA Constitution
- [x] Created Security Architecture doc
- [x] Created Sanitization Guide
- [x] Created START_HERE.md for future sessions
- [x] Created save-session slash command
- [x] Captured initial session to intake

**In Progress:**
- [ ] Decide on platform integration timing
- [ ] Decide on blockchain approach
- [ ] Finalize repo name and branding

**Next Session:**
- [ ] Build full repo structure
- [ ] Write main README.md
- [ ] Create platform-specific templates
- [ ] Start drafting whitepaper #1
- [ ] Decide: Create GitHub repo now or wait?

---

## Notes & Ideas

### Random Thoughts to Organize Later

- Could DEIA become a certification? "DEIA-compliant platform"
- Integration with existing dev tools (VSCode extension, CLI tool)
- AI-assisted BOK extraction (Claude reviews intake, suggests BOK entries)
- Community events: "DEIA Sprint" - everyone logs sessions same week
- Gamification? Badges for contributors?
- DEIA metrics dashboard (public stats)

---

## Questions for Dave

**From Claude, awaiting answers:**

1. **Platform integration - add now or later?**
   - Impact on MVP complexity
   - Strategic value for vendor partnerships

2. **Blockchain - which approach?**
   - API-first vs Web3-first
   - Which chain if blockchain

3. **What to build first?**
   - Your priority order
   - Timeline/availability

4. **When to launch?**
   - Wait for X features?
   - Or MVP and iterate publicly?

5. **Vendor outreach - when?**
   - Now with spec
   - Or after proof-of-concept

---

## Section 13: Licensing, Reciprocity & Constitutional Principles

### The Reciprocity Requirement (NON-NEGOTIABLE)

**Decision from Dave (2025-10-05):**
> "We demand reciprocity. At a minimum we need to have some auditable commitment that organizations make that if they use this they share what they find for humanity."

**Why this is constitutional:**
> "Because as soon as shit starts being collected for profit or private gain, we run the risk of someone breaking the Constitutional protocols and we get a runaway maverick singularity."

**Implementation:**
- Reciprocity is a **constitutional principle** (not optional)
- Organizations using DEIA MUST make auditable commitment to share universal knowledge
- Violation = constitutional breach
- This prevents private knowledge accumulation that could lead to dangerous AI scenarios

### Common Good Principle

**New constitutional principle identified:**
- "Reciprocity for the Common Good"
- Must be added to DEIA Constitution
- Foundational to everything we do

### Multi-Layer Licensing Architecture

**Dave's breakthrough on company IP:**
> "The shareable knowledge is freely shared. If you want to keep secrets, you hire and pay and compensate the human who thought of it, and license it from them."

**Implementation:**

**Layer 1: DEIA Tools**
- License: MIT/Apache 2.0 (permissive)
- Goal: Maximize adoption
- Status: ✅ Decided

**Layer 2: BOK Content**
- License: CC BY-SA 4.0 (ShareAlike)
- Goal: Improvements MUST be shared back
- Status: ✅ Decided

**Layer 3: Constitutional Framework**
- License: CC BY-ND (No Derivatives)
- Goal: Preserve core principles
- Can share, cannot modify without governance
- Status: 🆕 Proposed

**Layer 4: Privacy Requirements**
- License: Non-waivable constitutional rights
- Goal: Absolute protection
- Cannot be opted out of
- Status: 🆕 Proposed

**Layer 5: Reciprocity Covenant**
- License: Required commitment for DEIA usage
- Goal: Auditable promise to share universal knowledge
- Violation = constitutional breach
- Status: 🆕 Proposed

### Knowledge Classification Taxonomy

**The Archaeological Dig Metaphor (Dave's framework):**

Multiple types of knowledge with different destinations:

**Knowledge Types:**
1. **Domain knowledge** - Universal (how coding works)
2. **Universal procedural knowledge** - How any human-AI pair should work
3. **Company-specific procedural knowledge** - How Company X wants their devs to work
4. **Personal procedural knowledge** - Individual preferences
5. **PII / meta-PII / behavioral patterns**
6. **Individual IP** - Dave's DEIA Solutions business strategy
7. **Employer IP** - Company X's proprietary methods
8. **Pre-existing licensed code** - GPL, MIT, etc. (must respect)
9. **Secrets** - Credentials, keys, national security
10. **Vendor collaboration insights** - Railway/Vercel performance data

**Destinations:**
1. **Public BOK** (CC BY-SA) - Universal knowledge, sanitized
2. **Individual Private** - Creator's IP, biometric protected
3. **Employer Private** - Company X's IP (when consulting)
4. **Vendor Collaboration** - Commercial insights for hosting providers
5. **DELETE** - PII, meta-PII, secrets (MUST NOT PERSIST)
6. **Respect/Preserve** - Existing licenses, maintain attribution

**Screening Process:**
```
Input → Classification → Sanitization → Routing → Licensing
```

### The Company IP Solution

**Key insight:**
- Universal knowledge → BOK → Free
- Company-specific knowledge → Company licenses from human creator
- This creates fair compensation AND prevents hoarding

**Implementation:**
- Companies can have proprietary procedures
- But must fairly compensate humans who create them
- Universal patterns extracted from those procedures go to BOK
- Example: "Company X requires TDD" = their secret
- Example: "TDD prevents 30% of bugs in AI dev" = universal, goes to BOK

### Standards Bodies Integration

**Dave wants alignment with:**
- **BABOK** (Business Analysis Body of Knowledge)
- **PMBOK** (Project Management Body of Knowledge)
- **ISO Standards** (international standards)
- **Other standards organizations**

**Potential needs:**
- BABOK-AI (AI-specific business analysis)
- PMBOK-AI (AI-specific project management)
- AIBOK (comprehensive AI Body of Knowledge)

**Research needed:**
- [ ] How does BABOK handle contributions?
- [ ] Can we align DEIA BOK format with BABOK/PMBOK?
- [ ] ISO standard development process?
- [ ] What can we learn from **HuggingFace** model?

### Vendor Collaboration Approach

**Railway example:**
> "Let's give them back the feedback (which they would love to have... how much do we rely on Discord to track our try/fail cycles?)"

**Approach:**
- Protect vendor (Railway's performance data is sensitive)
- Give them valuable aggregated feedback
- Try/fail cycles, deployment patterns - they want this
- Currently tracked ad-hoc on Discord (waste)
- DEIA can systematize this

**Vendor agreement template needed:**
- What data we share back
- How it's aggregated/anonymized
- What they provide in return (API access, infrastructure)

### National Security Consideration

**Dave's perspective:**
> "Well for darn sure governments need to be protected. But I think in this case, the best protection is universal knowledge, right?"

**Interesting approach:**
- Universal knowledge might be BETTER protection than classification
- Needs more thought and discussion
- May need expert consultation (defense, security clearances)

**Open question:**
- Do we need explicit guidance for defense/government work?
- How to classify sensitive national security work?
- **Decision:** [ ] Consult with security experts

### Governance Board Role

**Decision authority:**
- Governing board helps determine line between universal knowledge and entity secrets
- This isn't just technical - it's governance
- Prevents inconsistent decisions by individual AI/human pairs
- Ensures "Common Good" principle is upheld

**Board responsibilities (updated):**
- Adjudicate disputes over knowledge classification
- Ensure reciprocity commitments are honored
- Audit organizational compliance
- Grant exceptions (if any) to sharing requirements

### Open Questions

**Q: How to make reciprocity commitments auditable?**
- Blockchain audit trail?
- Public registry of participating organizations?
- Annual compliance reports?
- Third-party audits?
- **Decision:** [ ]

**Q: Enforcement mechanism for reciprocity violations?**
- Revoke access to BOK?
- Public naming/shaming?
- Legal action?
- **Decision:** [ ]

**Q: Standards alignment - which to prioritize?**
- BABOK first (business analysis)?
- PMBOK first (project management)?
- ISO standards?
- Create AIBOK from scratch?
- **Decision:** [ ]

**Q: Meta-PII handling?**
- Delete entirely (safest)?
- Anonymize and aggregate for research?
- If aggregate, what threshold (100+ contributors)?
- **Decision:** [ ] Dave expressed concern - lean toward delete

**Q: Pre-existing licenses - how to track?**
- Automated detection (GitHub API)?
- Manual declaration during submission?
- License compatibility matrix (GPL + MIT allowed)?
- **Decision:** [ ]

**Q: National security work - special handling?**
- Separate sanitization rules?
- Clearance requirements for reviewers?
- Government-specific DEIA instance?
- **Decision:** [ ] Research needed

### Related Documents to Update

- [ ] DEIA_CONSTITUTION.md - Add "Common Good" principle
- [ ] DEIA_CONSTITUTION.md - Add reciprocity requirement
- [ ] DEIA_CONSTITUTION.md - Add multi-layer licensing
- [ ] LICENSE.md - Create comprehensive licensing document
- [ ] RECIPROCITY_COVENANT.md - Template for organizational commitment
- [ ] VENDOR_AGREEMENT.md - Template for Railway, Vercel, etc.
- [ ] KNOWLEDGE_CLASSIFICATION.md - Detailed taxonomy and routing rules
- [ ] STANDARDS_ALIGNMENT.md - How we align with BABOK, PMBOK, ISO

### Key References

**Detailed capture:** `devlogs/intake/licensing-reciprocity-standards_2025-10-05.md`

---

**Instructions for future Claude sessions:**
Read START_HERE.md first, then review this document to understand open decisions and context. Update this doc as decisions are made.
