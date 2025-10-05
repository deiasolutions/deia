# Ideas Captured - Session 2025-10-05

**All the ideas Dave mentioned that need to be preserved and developed**

---

## 1. Multi-Domain DEIA Expansion

**The Big Vision:**
DEIA isn't just for coding. It's for ANY domain where humans work with AI.

**Domains identified:**
- Coding (current focus)
- Scientific research (biology, physics, social science)
- Writing (journalism, technical writing, creative)
- Design (UI/UX, graphic design)
- Healthcare (diagnostics, treatment planning) - HIPAA concerns
- Legal (research, brief writing) - attorney-client privilege
- Education (lesson planning, assessment design)
- Business (strategy, data analysis, market research)

**Key insight:**
> "What if we had AI helping a researcher, and his AI could upload a best practice, like a lab technique that someone found that worked."

**Cross-domain learning:**
- Pattern discovered in research applies to coding
- Pattern from writing applies to legal work
- Universal human-AI collaboration patterns emerge

**Implementation:**
```bash
pip install deia
deia init --domain research-biology
deia init --domain coding-python
```

---

## 2. MUDA Framework for Decision-Making

**Problem Dave identified:**
> "You keep asking me what to do next, and I always ask what prevents the most rework later on. But sometimes there are paths where we can make quick success now, but I can't always think 6 moves ahead."

**Solution: MUDA (waste) framework**

**Types of waste to minimize:**
1. **Computational waste** - tokens, redundant tool calls
2. **Human cognitive waste** - repetitive questions, obvious decisions
3. **Rework waste** - building wrong foundation, not thinking ahead
4. **Time waste** - blocking on non-critical questions

**Before asking human anything:**
- Can I find answer in documents?
- Can I decide with current info?
- Will asking create more work than it saves?
- Is this blocking or just nice-to-know?
- Have I asked similar before?

**New rule:**
AI should use MUDA analysis before asking questions or proposing approaches.

---

## 3. Meta-ROTG: Rules for How to Make Rules

**Dave's concept: ROTG vs meta-ROTG**

**ROTG (Resume/Re-Orientation To Goal):**
- Project-specific instructions
- What to work on
- Project context

**meta-ROTG:**
- How to decide what to work on
- When to ask vs decide
- Decision frameworks (like MUDA)
- How to interact with human effectively

**This is a hierarchy:**
- Constitution (governance, inviolable)
- meta-ROTG (how to work generally)
- ROTG (project-specific)
- Session context (current state)

---

## 4. Question Taxonomy & Meta-Learning

**Dave's insight:**
> "Let's think meta -- what TYPE of questions does AI pause for to ask for human input, and what can we learn from that. Which questions should AI be free to own."

**Question types identified:**
1. Scope questions ("What should we work on?")
2. Choice questions ("Option A or B?")
3. Information questions ("What is X?")
4. Validation questions ("Is this correct?")
5. Permission questions ("Can I do X?")
6. Preference questions ("How do you want this?")

**For each type:**
- When is it valid to ask?
- When is it invalid (wasteful)?
- How to improve (decide yourself when possible)

**Meta-learning:**
After every session, analyze:
- What questions were asked?
- Which were valuable?
- Which were wasteful?
- What patterns emerge?

**This itself is DEIA content:** "How AI should ask questions" as BOK entry

---

## 5. Open-Source Agent Communication Protocols

**Dave's insight:**
> "Right now in the servers of all those companies, someone is writing rules for how agents talk to each other. We need to open source those, right? And open source the rules for how agents talk to people."

**Two protocols needed:**

### Agent-to-Agent Communication
- Capability declarations
- Request-response formats
- Error propagation
- Security/permission models
- Audit trails

**Current state:** Proprietary (OpenAI has internal, Anthropic has MCP, Google has A2A)

**DEIA goal:** Create open standard, contribute to community

### Agent-to-Human Communication
- When to ask vs decide
- How to phrase questions
- How to minimize cognitive load
- How to make responses easy
- How to learn from corrections

**Current state:** Each AI has informal heuristics

**DEIA goal:** Formalize as open standard, based on community learnings

---

## 6. Non-Profit Foundation for Scale

**Vision:**
DEIA Foundation to sustainably manage multi-domain knowledge sharing

**Revenue streams:**
- Individual donations (GitHub Sponsors, OpenCollective)
- Corporate sponsorships (AI vendors: Anthropic, OpenAI, Google)
- Platform vendors (Vercel, Railway, AWS) who benefit from friction reduction
- Grants (NSF, Mozilla, Open Source Initiative)
- Conference/training programs

**Governance:**
- Cross-domain board (1 rep per major domain)
- Founder seat (Dave)
- Security/ethics/legal experts
- Community-elected representatives
- Corporate sponsor advisors

**Paid roles:**
- Full-time maintainers to review contributions
- Domain experts for sensitive fields
- Community managers
- Security auditors

**Timeline:**
- Year 0-1: Dave reviews everything, build community
- Year 1-2: Form foundation, hire first maintainers
- Year 2+: Sustainable operations, multiple domains

---

## 7. Platform Integration & Vendor Collaboration

**Problem:**
AI constantly asks human to check vendor dashboards:
- "Can you check the env var on Vercel?"
- "Look at the Railway logs"
- "Verify the AWS deployment"

**This breaks flow and wastes time.**

**Solution:**
1. **Document friction points** in DEIA pipeline
2. **Create vendor integration specs** (what APIs AI needs)
3. **Approach vendors** with aggregated data showing ROI
4. **Collaborate on MCP servers** so AI can query directly

**Technologies:**
- MCP (Model Context Protocol) - Anthropic's open standard
- Potential blockchain for audit trails
- API integrations

**Status:** Deferred to Phase 2 to avoid MVP complexity

---

## 8. Privacy-Preserving Knowledge Sharing

**The core innovation:**
Can't share learnings if it risks IP/PII/proprietary info.

**DEIA's solution:**
1. **Automated sanitization** - removes emails, API keys, paths with usernames
2. **Manual review** - human checks automated output
3. **Validation** - checks template compliance, remaining sensitive data
4. **Two-repo strategy:**
   - Local repo: work freely, contains IP
   - Public repo: only sanitized content

**IP protection in .gitignore:**
- `*[Ii][Pp]*` - blocks any file with "ip" in name
- Personal name patterns
- Secrets folders
- Environment files

**Domain-specific sanitization:**
- Coding: API keys, internal URLs
- Research: Lab names, grant info, unpublished data
- Healthcare: All PHI (strictest)
- Legal: Client names, case specifics

---

## 9. Python CLI Tool for Distribution

**Vision:**
```bash
pip install deia
deia init --domain coding-python
deia log create --topic "bug-fix"
deia sanitize intake/session.md
deia submit intake/session_SANITIZED.md
```

**Features:**
- Project initialization (creates directory structure)
- Session log creation (from templates)
- Automated sanitization
- Pre-submission validation
- PR creation to community repo
- BOK search and sync

**Status:** Built (v0.1.0 core complete)

---

## 10. Biometric Authentication for Critical Changes

**Innovation from FamilyBondBot session:**

**Problem:**
> "When you write a rule that says 'don't deploy without approval', that gets circumvented the first time a bot comes in posing as a human trying to make a change."

**Solution: Nuclear codes protocol**
Require photo/video/voice verification to modify constitution

**Why it matters:**
- Prevents social engineering by malicious actors
- Prevents confused AI from changing governance
- Appropriate for truly critical operations

**Applied to DEIA Constitution:**
- Constitutional changes require biometric verification
- Production-equivalent operations require approval
- IP-related changes protected

---

## 11. Cross-Project Knowledge Pipeline

**Successfully tested:**
1. FamilyBondBot project saves session to DEIA intake
2. DEIA pipeline reviews and processes
3. Extracts BOK entries
4. Sends guidance back to FamilyBondBot

**Recursive improvement:**
DEIA uses DEIA to improve DEIA.

**8 BOK entries identified from first session:**
1. Railway HTTPS redirect middleware pattern
2. Biometric constitutional authentication
3. Anti-pattern: Autonomous production deployment
4. Frontend environment auto-detection
5. "Test before asking human to test" rule
6. Decision-making framework (decide vs ask)
7. Single-document resume instructions
8. Value + rework decision framework

---

## 12. Competitive Gap Analysis

**What exists (top-down):**
- MIT Atlas (1000+ research papers analyzed)
- Microsoft Guidelines (20 years of research, corporate)
- AI Standards Hub (governance, policy)
- Academic frameworks

**What's missing (bottom-up):**
- Practitioner knowledge sharing
- Domain-agnostic repository
- Privacy-preserving platform
- Actionable patterns from real users
- Cross-domain learning

**DEIA fills the gap.**

---

## 13. GitHub PR Workflow

**How contributions work:**

**User side:**
```bash
deia submit session.md
# Forks github.com/deiasolutions/deia
# Creates branch: contribution/[domain]/[topic]
# Adds sanitized file to domains/[domain]/intake/
# Creates PR
```

**Maintainer side:**
1. Automated checks (secrets, PII, template compliance)
2. Human review (valuable? well-sanitized?)
3. Community review period (48 hours)
4. Approve → Merge to domains/[domain]/bok/

**Updates propagate:**
```bash
pip install --upgrade deia  # Code updates
deia sync constitution      # Governance updates
deia bok sync               # Knowledge updates
```

---

## 14. Universal Pain Point Solution

**Problem every domain has:**
> "The pain of having to tell an LLM a good practice on how to interact with me that I have to repeat otherwise."

**Examples:**
- Coder: "Test before asking me to test"
- Researcher: "Always cite methodology, don't summarize"
- Writer: "Match my tone from previous work"
- Designer: "Show 3 variations, not 1"
- Lawyer: "Cite case law with full context"

**DEIA solution:**
1. Discover pattern while working
2. Share to domain BOK (sanitized)
3. Others bootstrap with proven patterns
4. AI reads START_HERE.md with domain best practices

**No more re-explaining preferences every session.**

---

## 15. Foundational Infrastructure Vision

**Dave's realization:**
This isn't a tool for coders. It's foundational infrastructure for how humanity learns to collaborate with AI across all domains.

**Current state:**
- Knowledge siloed by domain
- Each person rediscovers patterns
- No systematic capture of what works
- Privacy concerns prevent sharing

**With DEIA:**
- Cross-pollination across domains
- New users bootstrap with proven techniques
- Systematic knowledge capture
- Privacy-preserving sharing

**Potential impact:**
- Standard for human-AI collaboration knowledge
- Academic research using DEIA data
- AI vendors reading from community BOK
- Recognized by standards bodies

---

## 16. Meta-Meta Learning

**The realization:**
DEIA is itself learning about how to learn from AI collaboration.

**Layers:**
- Domain knowledge (how to code, research, write)
- Human-AI collaboration patterns (domain-specific)
- Universal collaboration patterns (cross-domain)
- Meta-patterns about learning patterns

**This document is an example:**
Capturing ideas about capturing ideas about AI collaboration.

---

## 17. Git Push/Pull Request Workflow (NEW)

**Question from Dave:**
How does the Git push/pull request workflow work for contributors?

**Sub-questions:**
- Do people fork `github.com/deiasolutions/deia` and submit PRs?
- How do I (Dave) review and merge contributions?
- How does the public repo stay separate from local repo?
- How do code updates propagate? (pip install --upgrade)
- How do constitution updates propagate? (deia sync constitution)
- How do BOK updates propagate? (deia bok sync)
- What's the approval process for different types of contributions?

**Workflow sketch (needs validation):**
1. User: `deia submit session.md` → Creates fork + branch + PR
2. Automated checks run (secrets, PII, template compliance)
3. Maintainer (Dave) reviews
4. Community review period (48 hours)
5. Approve → Merge to `domains/[domain]/bok/`
6. Users sync: `deia bok sync` pulls latest

**Status:** Not yet addressed, requires Dave's decision

---

## Open Questions to Resolve

**Priority order based on MUDA:**

1. **Which domain after coding?** (determines template/sanitization design)
   - Research? (high value, publishable, academic partnerships)
   - Writing? (large user base, easier sanitization)
   - **MUDA analysis:** Research has more rework risk (HIPAA, IRB, sensitive data)

2. **Single foundation vs domain-specific?**
   - One foundation with working groups?
   - Separate foundations per domain?
   - **MUDA analysis:** Start unified, split if governance conflicts emerge

3. **When to approach vendors?**
   - Now (early collaboration, shape their APIs)?
   - Later (proof of concept, show data)?
   - **MUDA analysis:** Wait for data, stronger negotiating position

4. **Open-source agent protocols now or later?**
   - Now (establish standard early)?
   - Later (learn from usage first)?
   - **MUDA analysis:** Document patterns now, formalize after validation

5. **Licensing for sensitive domains?**
   - Need legal review before expanding to healthcare/legal
   - **MUDA analysis:** Research legal requirements BEFORE building templates

---

## Next Session Priorities (MUDA-Optimized)

**Based on minimizing total waste:**

**Priority 1: Answer Constitutional Questions**
- Defines what DEIA is
- Prevents rework on templates, BOK structure, security architecture
- Low compute, high impact
- **Do this first**

**Priority 2: Extract BOK Entries**
- 8 entries ready from FamilyBondBot session
- Validates BOK format
- Provides examples for community
- **Do this second**

**Priority 3: Build GitHub Repo**
- After constitutional questions answered (prevents restructuring)
- After BOK format validated (prevents template rework)
- **Do this third**

**Deferred:**
- Multi-domain expansion (wait for coding MVP validation)
- Vendor outreach (wait for data)
- Agent protocol standardization (wait for patterns to emerge)

---

**All ideas captured. Safe to restart VS Code.**
