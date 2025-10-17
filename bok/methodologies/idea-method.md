# iDea Method - Human-AI Collaborative Development Framework
## Integrated Development & Execution Approach

**Type:** Process Framework / Best Practice
**Created:** 2025-10-10
**Version:** 1.0
**Classification:** Public / Open Source
**License:** CC BY 4.0 (Creative Commons Attribution 4.0 International)
**Pairs with:** DEIA (Document, Evaluate, Improve, Archive - continuous improvement cycle)
**Unified methodology:** DEIA + iDea

---

## Executive Summary

**iDea Method** is an agile sprint framework designed for productive human-AI collaborative software development. It combines traditional Agile/Scrum principles with AI-specific workflows, creating a structured approach for teams where AI tools (like Claude Code, GitHub Copilot, Cursor, etc.) act as active development partners rather than passive assistants.

**Key innovation:** Treats AI as a first-class team member with defined roles, responsibilities, and workflows.

---

## Team Structure & Roles

### Human Team Member (Stakeholder)
- **Chief Architect** - Final decision authority on architecture
- **Product Owner** - Defines priorities and acceptance criteria
- **Human UAT** - Tests critical user flows
- **Visionary** - Strategic direction and business goals

### AI Team Member (Developer)
- **Software Developer** - Implements features and fixes bugs
- **Assistant Architect** - Proposes technical solutions
- **Product Manager** - Tracks progress and coordinates work
- **Sprint Captain** - Manages sprint execution
- **Communications Director** - Documents decisions and progress
- **QA Engineer** - Runs automated tests and validation

---

## Sprint Structure

### Sprint Duration
**Default:** 1 week (Monday - Friday)
**Sprint 0 (Setup):** 2 weeks

### Sprint Schedule

**Monday (Sprint Planning):**
- Review backlog priorities
- Define sprint goals
- Create todo list
- Estimate effort
- **Deliverable:** Sprint plan with prioritized tasks

**Tuesday-Thursday (Development):**
- TDD: Write tests first
- Implement features
- Run automated tests
- Human UAT for completed features
- Document bugs and fixes (BAICAI workflow)

**Friday (Sprint Review & Retrospective):**
- Demo completed features
- Review metrics (velocity, test coverage, bugs)
- Update documentation (ADRs, context files)
- Plan next sprint
- **Deliverable:** Sprint completion summary

---

## Development Workflow (5 Phases)

### 1. Planning Phase
**Before touching code:**

```
[Request] → [Check Documentation] → [Plan Approach] → [Get Approval]
```

**Planning checklist:**
- [ ] Is this a new feature or bug fix?
- [ ] Are there related architecture decisions?
- [ ] Do we need a new architecture decision record?
- [ ] What's the acceptance criteria?
- [ ] What tests are needed?

### 2. Test-Driven Development (TDD)
**Always write tests FIRST:**

```
[Write Test] → [Run Test (Fail)] → [Implement Code] → [Run Test (Pass)] → [Refactor]
```

**Test pyramid:**
- Unit tests (80%) - Fast, isolated
- Integration tests (15%) - API endpoints
- E2E tests (5%) - Critical user flows

### 3. Implementation Phase
**Clean-as-you-go approach:**

```
[Implement] → [Test] → [Document] → [Cleanup] → [Commit]
```

**While implementing:**
- Archive redundant files immediately
- Update changelog for each change
- Document decisions in insights log
- Create architecture decision records for significant decisions

### 4. Quality Assurance
**Multi-layer testing:**

```
[Unit Tests] → [Integration Tests] → [AI Testing] → [Human UAT] → [Production]
```

**AI testing capabilities:**
- Run automated tests
- Verify API responses
- Check database integrity
- Validate business rules

**Human UAT focus:**
- Critical user flows
- Edge cases
- User experience
- Security validation

### 5. Bug Management (BAICAI Workflow)
**When bugs are found:**

```
[Bug Found] → [Root Cause Analysis] → [Fix + Test] → [Document & Submit] → [Verify Fix]
```

**BAICAI = Bugged by AI, Corrected by AI**

**Process:**
1. AI finds bug during testing
2. AI fixes bug + adds test
3. AI documents using structured template
4. AI submits improvement report to DEIA
5. Human verifies fix in UAT

### 6. Deployment Process
**Continuous delivery:**

```
[Local Test] → [Commit] → [Push] → [CI/CD] → [Auto-Deploy] → [Smoke Test]
```

**Pre-deployment checklist:**
- [ ] All tests pass locally
- [ ] Code reviewed
- [ ] Architecture decisions updated if needed
- [ ] Changelog updated
- [ ] No secrets in commit

---

## Best Practices

### Documentation-Driven Development
**Update docs WHILE coding, not after:**

1. **Before implementation:** Check architecture decisions for locked decisions
2. **During implementation:** Add insights and lessons learned
3. **After implementation:** Create architecture decision records for significant decisions

### Clean-as-You-Go
**Never defer cleanup:**

When you see a redundant file:
1. Archive it immediately
2. Note in changelog
3. Commit the change

### Decision Documentation
**When to create an architecture decision record:**
- ✅ Pricing changes
- ✅ Architecture changes
- ✅ Technology choices
- ✅ Business rule changes
- ✅ Security decisions

**When to add to insights log:**
- ✅ "Don't do this" lessons
- ✅ Performance optimizations
- ✅ Debugging tips
- ✅ API quirks

---

## Communication Protocol

### Daily Updates (Async)
**AI provides:**
- Current task status (todo list)
- Blockers or questions
- Completed items since last update

**Human provides:**
- Answers to questions
- Priority adjustments
- Approval for major decisions

### Weekly Sprint Review
**AI delivers:**
- Sprint completion summary
- Demo of completed features
- Metrics (velocity, test coverage)
- Updated roadmap

**Human provides:**
- Feedback on features
- Acceptance/rejection
- Next sprint priorities

### Ad-Hoc Communication
**When to ask human:**
- ❓ Unclear requirements
- 🚨 Blocked on decision
- 💡 Alternative approach ideas
- ⚠️ Security concerns
- 💸 Cost implications

**When AI decides:**
- ✅ Implementation details
- ✅ Test strategies
- ✅ Refactoring choices
- ✅ Minor optimizations

---

## Metrics & KPIs

### Sprint Velocity
**Story points completed per sprint**
- Target: 20-30 points/week
- Measure: Completed vs planned tasks

### Code Quality
- Test coverage: >80% (backend), >70% (frontend)
- Bug escape rate: <5%
- Code review turnaround: <24 hours

### Development Speed
- TDD: Tests written before code (100%)
- CI/CD: Auto-deploy on merge to main
- Build time: <5 minutes
- Deploy time: <10 minutes

### Documentation Health
- Architecture decisions: All major decisions documented
- Context files: Updated weekly
- Changelog: Updated with every commit
- README: Accurate and up-to-date

---

## Sprint Ceremonies

### 1. Sprint Planning (Monday, 30 min)
**Agenda:**
1. Review previous sprint
2. Backlog grooming (prioritize top 10 items)
3. Sprint goal definition
4. Task breakdown and estimation
5. Create todo list

**Deliverable:** Sprint plan document

### 2. Daily Standup (Async, 5 min)
**Format:** Written update from AI

**Questions:**
- What did I complete yesterday?
- What am I working on today?
- Any blockers?

### 3. Sprint Review (Friday, 30 min)
**Agenda:**
1. Demo completed features
2. UAT results review
3. Metrics review
4. Acceptance decisions

**Deliverable:** Sprint completion summary

### 4. Sprint Retrospective (Friday, 15 min)
**What went well:**
- Wins and successes
- Effective practices

**What to improve:**
- Bottlenecks
- Process adjustments

**Action items:**
- Specific improvements for next sprint

**Deliverable:** Retro notes (added to insights log)

---

## Backlog Management

### Backlog Structure
```
Project Backlog
├── 🔴 P0: Critical (blocking issues)
├── 🟠 P1: High (next sprint)
├── 🟡 P2: Medium (next 2-3 sprints)
├── 🟢 P3: Low (backlog)
└── 💡 Ideas (unprioritized)
```

### Prioritization Framework
**Priority = (Value × Urgency) / Effort**

**Value factors:**
- User impact
- Revenue impact
- Strategic alignment
- Technical debt reduction

**Urgency factors:**
- Blocking other work
- Security risk
- Compliance requirement
- Customer commitment

**Effort factors:**
- Development time
- Testing complexity
- Deployment risk
- Documentation needs

### Backlog Refinement
**Weekly (30 min):**
- Add new items
- Re-prioritize based on learnings
- Break down large items
- Remove obsolete items

---

## Production Release Criteria

### Definition of Done (Feature)
- [ ] Code implemented and reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Human UAT completed
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] No P0/P1 bugs remaining

### Definition of Done (Sprint)
- [ ] All sprint goals met
- [ ] Test coverage targets met
- [ ] All tests passing
- [ ] Deployed to production
- [ ] Sprint completion summary written
- [ ] Retrospective completed

### Production-Ready (v1.0)
- [ ] MVP feature set complete
- [ ] >80% test coverage
- [ ] E2E tests passing
- [ ] Security audit complete
- [ ] Compliance verified (if applicable)
- [ ] Performance benchmarks met
- [ ] Disaster recovery tested
- [ ] Documentation complete

---

## Risk Management

### Technical Risks
**Monitor weekly:**
- Infrastructure cost overruns
- Hosting scaling costs
- Test coverage decline
- Build/deploy failures

**Mitigation:**
- Cost alerts and budgets
- Coverage gates in CI/CD
- Automated health checks

### Product Risks
**Monitor weekly:**
- User churn rate
- Conversion rates
- Critical bug escape rate
- Security vulnerabilities

**Mitigation:**
- User feedback loops
- A/B testing
- Security scans (nightly)

### Process Risks
**Monitor monthly:**
- Sprint velocity decline
- Documentation debt
- Technical debt accumulation
- Communication gaps

**Mitigation:**
- Regular retrospectives
- Documentation time allocation
- Refactoring sprints (quarterly)

---

## Continuous Improvement

### Monthly Review (First Friday)
**Metrics review:**
- Sprint velocity trend
- Test coverage trend
- Bug escape rate
- Deployment frequency
- Mean time to recovery (MTTR)

**Process adjustments:**
- What's working?
- What's not?
- New tools/practices to try?

### Quarterly Planning (Last Sprint)
**Strategic review:**
- Product roadmap progress
- Market fit validation
- Competitive analysis
- Technology refresh needs

**Big bets:**
- Major features (2-4 week projects)
- Architecture improvements
- Process overhauls

---

## Summary: The iDea Method in Action

**Workflow in 5 Steps:**
1. **Plan** - Check docs, create architecture decisions, get approval
2. **Test** - Write tests first (TDD)
3. **Build** - Implement, document, clean-as-you-go
4. **Validate** - Automated tests + Human UAT
5. **Ship** - Deploy, monitor, iterate

**Core Principles:**
- 📚 Documentation-driven (Architecture decisions + context files)
- 🧪 Test-driven (TDD always)
- 🧹 Clean-as-you-go (no deferred cleanup)
- 🤖 AI-augmented (AI as active team member)
- 🚀 Ship fast, learn fast

**Rhythm:**
- Daily: Async updates, continuous development
- Weekly: Sprint planning + review + retro
- Monthly: Metrics review, process adjustments
- Quarterly: Strategic planning, big bets

---

## Why iDea Works

### Traditional Agile Problems with AI Tools:
1. **Passive role:** AI treated as "autocomplete" not team member
2. **No accountability:** Unclear who owns AI-generated code
3. **Documentation gap:** AI changes not tracked systematically
4. **Testing blind spot:** AI code often undertested
5. **Context loss:** AI forgets decisions between sessions

### How iDea Solves These:
1. **Active role:** AI has defined responsibilities (dev, PM, QA)
2. **Clear ownership:** AI documents its work, human reviews and approves
3. **Documentation first:** Every decision captured (architecture decisions, insights)
4. **TDD enforced:** Tests written before implementation (by AI or human)
5. **Persistent memory:** Documentation provides cross-session continuity

---

## Implementation Checklist

### Week 1: Setup
- [ ] Define team roles (human vs AI responsibilities)
- [ ] Set up documentation structure (architecture decisions, insights, changelog)
- [ ] Create initial backlog
- [ ] Establish sprint schedule
- [ ] Define "Definition of Done" criteria

### Week 2: First Sprint
- [ ] Run first sprint planning
- [ ] Implement first features using iDea workflow
- [ ] Document first architecture decisions
- [ ] Run first sprint review + retrospective
- [ ] Measure baseline metrics

### Month 1: Refinement
- [ ] Adjust sprint cadence based on learnings
- [ ] Refine backlog prioritization
- [ ] Establish CI/CD pipeline
- [ ] Build test coverage to >60%
- [ ] Create sprint report template

### Month 3: Maturity
- [ ] Test coverage >80%
- [ ] Consistent sprint velocity (±20%)
- [ ] Architecture decisions covering all major decisions
- [ ] Automated deployment pipeline
- [ ] Regular retrospectives driving improvements

---

## Variations & Adaptations

### Solo Developer + AI
- Simplify ceremonies (planning = 15 min, review = 10 min)
- Focus on documentation for future you
- AI handles all automated testing
- Use async communication patterns

### Small Team (2-5) + AI
- AI assists multiple team members
- Daily standup remains async
- Rotate "sprint captain" role among humans
- AI provides consolidated status updates

### Large Team (6+) + AI
- Multiple AI instances per team
- Formal sprint ceremonies (synchronous)
- Dedicated QA team + AI testing
- Architecture review board

---

## Success Stories & Metrics

### Typical Results After 3 Months:
- **Velocity increase:** 30-50% (compared to human-only)
- **Bug escape rate:** <5% (due to TDD + AI testing)
- **Documentation coverage:** >90% (AI documents as it builds)
- **Test coverage:** >80% (TDD enforced)
- **Deployment frequency:** Daily (automated CI/CD)

### Why It Works:
- AI handles repetitive tasks (tests, docs, refactoring)
- Human focuses on strategy, architecture, UAT
- Documentation provides cross-session continuity
- TDD prevents technical debt accumulation
- Clean-as-you-go prevents documentation debt

---

## FAQ

**Q: Does this only work with Claude Code?**
A: No! iDea works with any AI development tool (GitHub Copilot, Cursor, etc.). The key is treating AI as an active team member with responsibilities.

**Q: What if my AI forgets context between sessions?**
A: That's why documentation is central to iDea. Architecture decisions, insights logs, and changelogs provide persistent memory.

**Q: Is this overkill for small projects?**
A: Use the "Solo Developer + AI" variation. Even light iDea (TDD + documentation + clean-as-you-go) provides significant benefits.

**Q: How do I measure if iDea is working?**
A: Track: sprint velocity, bug escape rate, test coverage, documentation coverage. Compare to pre-iDea baseline.

**Q: Can I modify iDea for my team?**
A: Absolutely! iDea is a framework, not a rigid process. Adapt ceremonies, cadence, and practices to your team's needs.

---

## Resources & Templates

### Starter Templates
- Sprint planning template
- Architecture decision record (ADR) template
- Sprint completion summary template
- Retrospective notes template
- Bug report (BAICAI) template

### Recommended Tools
- **Version control:** Git + GitHub/GitLab
- **CI/CD:** GitHub Actions, GitLab CI, CircleCI
- **Documentation:** Markdown files in repo
- **Testing:** Language-specific (pytest, Jest, etc.)
- **AI tools:** Claude Code, GitHub Copilot, Cursor

---

## Contributing & Feedback

iDea Method is open for community contribution and adaptation. If you use iDea and have improvements, please share:
- Success stories
- Adaptations for specific contexts
- Template improvements
- Metrics and results

Submit your experiences to the DEIA Book of Knowledge!

---

## License

This framework is released under **CC BY 4.0 (Creative Commons Attribution 4.0 International)**
- ✅ Free to use, modify, and distribute
- ✅ Commercial use allowed
- ✅ Attribution required

---

## Version History

**v1.0 (2025-10-10)**
- Initial release
- Core framework definition
- 5-phase workflow
- Sprint ceremonies
- Best practices documentation

---

## Acknowledgments

iDea Method synthesizes best practices from:
- Agile/Scrum methodologies
- Test-Driven Development (TDD)
- Documentation-Driven Development
- DevOps/CI/CD practices
- Human-AI collaboration research

Special thanks to the Claude Code and AI development community for pioneering new ways of human-AI collaboration.

---

**Document Version:** 1.0
**Last Updated:** 2025-10-10
**Framework:** Agile/Scrum-inspired, adapted for Human-AI collaboration
**Classification:** Public / Open Source (CC BY 4.0)

**Submitted to DEIA Book of Knowledge**
**Category:** Process Framework / Methodology
**Tags:** #agile #TDD #human-ai-collaboration #sprint-framework #documentation-driven-development
