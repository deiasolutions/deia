# iDea Method - Complete Documentation
## Integrated Development & Execution Approach
### Agile Sprint Framework for Human-AI Collaborative Development

**Version:** 1.0
**Created:** 2025-10-10
**License:** CC BY 4.0 (Creative Commons Attribution 4.0 International)
**Pairs with:** DEIA (Document, Evaluate, Improve, Archive - continuous improvement cycle)
**Unified methodology:** DEIA + iDea

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Team Structure & Roles](#team-structure--roles)
3. [Sprint Structure](#sprint-structure)
4. [Development Workflow (5 Phases)](#development-workflow-5-phases)
5. [Best Practices](#best-practices)
6. [Communication Protocol](#communication-protocol)
7. [Metrics & KPIs](#metrics--kpis)
8. [Sprint Ceremonies](#sprint-ceremonies)
9. [Backlog Management](#backlog-management)
10. [Production Release Criteria](#production-release-criteria)
11. [Risk Management](#risk-management)
12. [Continuous Improvement](#continuous-improvement)
13. [Implementation Checklist](#implementation-checklist)
14. [Variations & Adaptations](#variations--adaptations)
15. [FAQ](#faq)

---

## Executive Summary

**iDea Method** is an agile sprint framework designed for productive human-AI collaborative software development. It combines traditional Agile/Scrum principles with AI-specific workflows, creating a structured approach for teams where AI tools (like Claude Code, GitHub Copilot, Cursor, etc.) act as active development partners rather than passive assistants.

**Key innovation:** Treats AI as a first-class team member with defined roles, responsibilities, and workflows.

**Core Philosophy:** Human-AI collaboration requires explicit role definition, clear accountability, and persistent memory through documentation. Traditional Agile assumes all team members retain context between sessions - AI tools don't. iDea solves this through documentation-driven development.

---

## Team Structure & Roles

### Human Team Member (Stakeholder)
- **Chief Architect** - Final decision authority on architecture
- **Product Owner** - Defines priorities and acceptance criteria
- **Human UAT** - Tests critical user flows and edge cases
- **Visionary** - Strategic direction and business goals

### AI Team Member (Developer)
- **Software Developer** - Implements features and fixes bugs
- **Assistant Architect** - Proposes technical solutions
- **Product Manager** - Tracks progress and coordinates work
- **Sprint Captain** - Manages sprint execution
- **Communications Director** - Documents decisions and progress
- **QA Engineer** - Runs automated tests and validation

**Key Principle:** Human provides strategy and approval, AI executes and documents. Both are accountable.

---

## Sprint Structure

### Sprint Duration
**Default:** 1 week (Monday - Friday)
**Sprint 0 (Setup):** 2 weeks for initial infrastructure

### Sprint Schedule

**Monday (Sprint Planning):**
- Review backlog priorities
- Define sprint goals
- Create todo list with estimates
- **Deliverable:** Sprint plan with prioritized tasks

**Tuesday-Thursday (Development):**
- TDD: Write tests first
- Implement features
- Run automated tests continuously
- Human UAT for completed features
- Document bugs and fixes

**Friday (Sprint Review & Retrospective):**
- Demo completed features to stakeholders
- Review metrics (velocity, test coverage, bugs)
- Update documentation (ADRs, context files)
- Retrospective: what worked, what didn't
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
- [ ] Do we need a new architecture decision record (ADR)?
- [ ] What's the acceptance criteria?
- [ ] What tests are needed?
- [ ] Are there dependencies on other work?

**Documentation to check:**
- Architecture Decision Records (ADRs)
- Existing context files
- ROADMAP.md for project status
- Previous sprint summaries

### 2. Test-Driven Development (TDD)
**Always write tests FIRST:**

```
[Write Test] → [Run Test (Fail)] → [Implement Code] → [Run Test (Pass)] → [Refactor]
```

**Test pyramid:**
- **Unit tests (80%)** - Fast, isolated, test single functions
- **Integration tests (15%)** - API endpoints, database interactions
- **E2E tests (5%)** - Critical user flows only

**Why TDD with AI:**
- AI can generate code quickly, but tests ensure correctness
- Tests document expected behavior
- Prevents regressions when AI refactors
- Forces good design (testable code is better code)

### 3. Implementation Phase
**Clean-as-you-go approach:**

```
[Implement] → [Test] → [Document] → [Cleanup] → [Commit]
```

**While implementing:**
- Archive redundant files immediately (don't defer)
- Update changelog for each significant change
- Document decisions in insights/context logs
- Create ADRs for significant architectural decisions
- Refactor as you go (never accumulate technical debt)

**Commit hygiene:**
- Small, focused commits
- Descriptive commit messages
- Reference issues/tickets where applicable
- Never commit secrets or PII

### 4. Quality Assurance
**Multi-layer testing:**

```
[Unit Tests] → [Integration Tests] → [AI Testing] → [Human UAT] → [Production]
```

**AI testing capabilities:**
- Run automated test suites
- Verify API responses match specs
- Check database integrity
- Validate business rules
- Load/performance testing (basic)

**Human UAT focus:**
- Critical user flows (signup, payment, core features)
- Edge cases and error handling
- User experience and usability
- Security validation
- Accessibility compliance

**When to escalate to human:**
- Test failures that AI can't diagnose
- UX concerns
- Security implications
- Breaking changes

### 5. Bug Management Workflow
**When bugs are found:**

```
[Bug Found] → [Root Cause Analysis] → [Fix + Test] → [Document] → [Verify Fix]
```

**Bug documentation process:**
1. AI finds bug during testing
2. AI performs root cause analysis
3. AI fixes bug + adds regression test
4. AI documents the fix with:
   - What was broken
   - Why it broke
   - How it was fixed
   - How to prevent recurrence
5. Human verifies fix in UAT

**Bug prioritization:**
- **P0 (Critical):** Production down, data loss risk
- **P1 (High):** Major feature broken, security issue
- **P2 (Medium):** Minor feature broken, workaround exists
- **P3 (Low):** Cosmetic, nice-to-have fixes

### 6. Deployment Process
**Continuous delivery:**

```
[Local Test] → [Commit] → [Push] → [CI/CD] → [Auto-Deploy] → [Smoke Test]
```

**Pre-deployment checklist:**
- [ ] All tests pass locally
- [ ] Code reviewed (by human or AI with human approval)
- [ ] ADRs updated if architecture changed
- [ ] Changelog updated
- [ ] No secrets in commit
- [ ] Database migrations tested
- [ ] Rollback plan documented

**Post-deployment:**
- Smoke tests run automatically
- Monitor error rates
- Verify key metrics
- Human spot-check critical flows

---

## Best Practices

### Documentation-Driven Development
**Update docs WHILE coding, not after:**

**Before implementation:**
- Check ADRs for locked decisions (don't violate past decisions)
- Check context files for patterns and lessons learned
- Understand "why" before "what"

**During implementation:**
- Add insights to context/lessons learned as you discover them
- Note "don't do this" anti-patterns immediately
- Update documentation inline with code changes

**After implementation:**
- Create ADR for significant decisions (technology choices, architecture changes)
- Update README if user-facing changes
- Add to changelog

**What qualifies as "significant":**
- Pricing changes
- Architecture changes (database schema, API design)
- Technology choices (new library, new service)
- Business rule changes
- Security decisions

### Clean-as-You-Go
**Never defer cleanup:**

**When you see redundant code or files:**
1. Archive/delete immediately
2. Note in changelog
3. Commit the cleanup

**When you see code that needs refactoring:**
1. Refactor now (if safe)
2. OR create ticket with clear acceptance criteria
3. Never let technical debt accumulate silently

**Cleanup is part of development, not a separate phase.**

### Decision Documentation

**When to create an Architecture Decision Record (ADR):**
- ✅ Pricing/business model changes
- ✅ Architecture changes (significant, not trivial)
- ✅ Technology choices (frameworks, libraries, services)
- ✅ Business rule changes
- ✅ Security decisions
- ✅ Anything that answers "Why did we...?"

**ADR Template:**
```markdown
# ADR-XXXX: [Title]

**Date:** YYYY-MM-DD
**Status:** Accepted | Rejected | Superseded
**Deciders:** [Names/Roles]

## Context
What is the issue we're addressing?

## Decision
What did we decide to do?

## Consequences
What are the positive and negative outcomes?

## Alternatives Considered
What other options did we evaluate?
```

**When to add to insights/lessons learned:**
- ✅ "Don't do this" lessons
- ✅ Performance optimizations discovered
- ✅ Debugging tips for future reference
- ✅ API quirks or gotchas
- ✅ Quick wins and hacks

---

## Communication Protocol

### Daily Updates (Async)
**AI provides (5 min):**
- Current task status
- Blockers or questions
- Completed items since last update
- Estimated time to completion

**Human provides (5-10 min):**
- Answers to questions
- Priority adjustments
- Approval for major decisions
- New requirements or changes

**Format:** Written update (no meetings required)

### Weekly Sprint Review
**AI delivers:**
- Sprint completion summary
- Demo of completed features (video or screenshots)
- Metrics (velocity, test coverage, bug counts)
- Updated roadmap with next sprint preview

**Human provides:**
- Feedback on features (acceptance or change requests)
- Acceptance/rejection decisions
- Next sprint priorities
- Strategic direction updates

### Ad-Hoc Communication
**When AI should ask human:**
- ❓ Unclear requirements or ambiguous specifications
- 🚨 Blocked on decision (technical or product)
- 💡 Alternative approach ideas (propose multiple options)
- ⚠️ Security concerns or risks
- 💸 Cost implications (infrastructure, services)
- 🔀 Breaking changes needed

**When AI decides autonomously:**
- ✅ Implementation details (code structure, variable names)
- ✅ Test strategies (how to test, not what to test)
- ✅ Refactoring choices (within established patterns)
- ✅ Minor optimizations (performance, readability)
- ✅ Documentation improvements

---

## Metrics & KPIs

### Sprint Velocity
**Definition:** Story points completed per sprint

**Target:** 20-30 points/week (calibrate to your team)

**Measurement:**
- Track completed vs planned tasks
- Adjust estimates based on actuals
- Look for trends (increasing velocity = good process fit)

### Code Quality
**Targets:**
- Test coverage: >80% (backend), >70% (frontend)
- Bug escape rate: <5% (bugs found in production)
- Code review turnaround: <24 hours

**How to measure:**
- Test coverage: Coverage reports (pytest-cov, jest --coverage)
- Bug escape: Track bugs found in production vs testing
- Review turnaround: Time from PR creation to merge

### Development Speed
**Targets:**
- TDD: 100% (tests written before code, no exceptions)
- CI/CD: Auto-deploy on merge to main
- Build time: <5 minutes
- Deploy time: <10 minutes

**How to improve:**
- Parallelize tests
- Optimize build process
- Cache dependencies
- Invest in CI/CD infrastructure

### Documentation Health
**Targets:**
- ADRs: All major decisions documented
- Context files: Updated weekly
- Changelog: Updated with every significant commit
- README: Accurate and up-to-date

**How to audit:**
- Review ADRs monthly
- Check last-modified dates on context files
- Validate README against actual code
- Ask: "Can a new team member onboard from docs alone?"

---

## Sprint Ceremonies

### 1. Sprint Planning (Monday, 30 min)
**Attendees:** Human stakeholder(s) + AI

**Agenda:**
1. Review previous sprint (5 min)
   - What shipped?
   - What didn't? Why?
2. Backlog grooming (10 min)
   - Prioritize top 10-15 items
   - Clarify acceptance criteria
3. Sprint goal definition (5 min)
   - What's the ONE thing this sprint achieves?
4. Task breakdown and estimation (10 min)
   - Break large items into sub-tasks
   - Estimate story points

**Deliverable:** Sprint plan document with:
- Sprint goal
- Prioritized task list
- Story point estimates
- Definition of done

### 2. Daily Standup (Async, 5 min)
**Format:** Written update from AI, human response as needed

**AI answers:**
- What did I complete yesterday?
- What am I working on today?
- Any blockers?

**Human responds if:**
- Blockers need resolution
- Priorities changed
- Clarification needed

**No meetings required** - async communication is more efficient

### 3. Sprint Review (Friday, 30 min)
**Attendees:** Human stakeholder(s) + AI

**Agenda:**
1. Demo completed features (15 min)
   - Show working software
   - Highlight key accomplishments
2. UAT results review (5 min)
   - What passed?
   - What needs fixes?
3. Metrics review (5 min)
   - Velocity, coverage, bugs
4. Acceptance decisions (5 min)
   - What ships to production?
   - What needs more work?

**Deliverable:** Sprint completion summary with:
- What shipped
- Metrics achieved
- Feedback for next sprint

### 4. Sprint Retrospective (Friday, 15 min)
**Attendees:** Human stakeholder(s) + AI

**Format:**
**What went well:**
- Wins and successes
- Effective practices to continue

**What to improve:**
- Bottlenecks identified
- Process adjustments needed

**Action items:**
- Specific improvements for next sprint (max 3)
- Who owns each action item

**Deliverable:** Retro notes added to insights log

---

## Backlog Management

### Backlog Structure
```
Project Backlog
├── 🔴 P0: Critical (blocking issues, security, data loss)
├── 🟠 P1: High (next sprint, important features)
├── 🟡 P2: Medium (next 2-3 sprints)
├── 🟢 P3: Low (backlog, nice-to-haves)
└── 💡 Ideas (unprioritized, need refinement)
```

### Prioritization Framework
**Priority = (Value × Urgency) / Effort**

**Value factors:**
- User impact (how many users affected?)
- Revenue impact (does this make/save money?)
- Strategic alignment (does this support our vision?)
- Technical debt reduction (does this improve code health?)

**Urgency factors:**
- Blocking other work?
- Security risk?
- Compliance requirement?
- Customer commitment?

**Effort factors:**
- Development time (hours/days/weeks)
- Testing complexity (simple vs comprehensive)
- Deployment risk (safe vs risky)
- Documentation needs (minimal vs extensive)

### Backlog Refinement
**Weekly (30 min):**
- Add new items from stakeholders
- Re-prioritize based on learnings
- Break down large items into smaller chunks
- Remove obsolete items
- Update acceptance criteria as needed

**Rule of thumb:** Top 10 items should be well-defined and ready to work

---

## Production Release Criteria

### Definition of Done (Feature)
- [ ] Code implemented and reviewed
- [ ] Unit tests written and passing (>80% coverage)
- [ ] Integration tests passing
- [ ] Human UAT completed and approved
- [ ] Documentation updated (README, ADRs, changelog)
- [ ] No P0/P1 bugs remaining
- [ ] Performance benchmarks met (if applicable)

### Definition of Done (Sprint)
- [ ] All sprint goals met (or documented why not)
- [ ] Test coverage targets met
- [ ] All tests passing in CI/CD
- [ ] Deployed to production (or staged for release)
- [ ] Sprint completion summary written
- [ ] Retrospective completed with action items

### Production-Ready (v1.0 Release)
- [ ] MVP feature set complete
- [ ] >80% test coverage (backend and frontend)
- [ ] E2E tests passing for critical flows
- [ ] Security audit complete (or scheduled)
- [ ] Performance benchmarks met
- [ ] Disaster recovery tested
- [ ] Documentation complete and accurate
- [ ] Marketing/launch plan ready

---

## Risk Management

### Technical Risks
**Monitor weekly:**
- Infrastructure cost overruns
- Test coverage decline
- Build/deploy failures increasing
- Technical debt accumulation

**Mitigation strategies:**
- Set up cost alerts and budgets
- Enforce coverage gates in CI/CD
- Automated health checks
- Scheduled refactoring sprints

### Product Risks
**Monitor weekly:**
- User adoption/engagement rates
- Conversion rates (free to paid, trials to customers)
- Critical bug escape rate
- Security vulnerabilities

**Mitigation strategies:**
- User feedback loops and surveys
- A/B testing for critical features
- Automated security scans
- Bug bounty program

### Process Risks
**Monitor monthly:**
- Sprint velocity decline
- Documentation debt
- Team communication gaps

**Mitigation strategies:**
- Regular retrospectives with action items
- Documentation time built into estimates
- Clear communication protocols

---

## Continuous Improvement

### Monthly Review (First Friday)
**Metrics review:**
- Sprint velocity trend (up, down, stable?)
- Test coverage trend
- Bug escape rate
- Deployment frequency
- Mean time to recovery (MTTR)

**Process adjustments:**
- What's working well?
- What's not working?
- New tools/practices to try?
- Action items for next month

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
- Team expansion

---

## Implementation Checklist

### Week 1: Setup
- [ ] Define team roles (human vs AI responsibilities)
- [ ] Set up documentation structure (ADRs, context files, changelog)
- [ ] Create initial backlog
- [ ] Establish sprint schedule
- [ ] Define "Definition of Done" criteria
- [ ] Set up CI/CD pipeline (basic)

### Week 2: First Sprint
- [ ] Run first sprint planning
- [ ] Implement first features using iDea workflow
- [ ] Document first ADRs
- [ ] Run first sprint review + retrospective
- [ ] Measure baseline metrics
- [ ] Adjust process based on learnings

### Month 1: Refinement
- [ ] Adjust sprint cadence based on team velocity
- [ ] Refine backlog prioritization
- [ ] Improve CI/CD pipeline
- [ ] Build test coverage to >60%
- [ ] Create sprint report templates
- [ ] Establish communication patterns

### Month 3: Maturity
- [ ] Test coverage >80%
- [ ] Consistent sprint velocity (±20% variance)
- [ ] ADRs covering all major decisions
- [ ] Automated deployment pipeline
- [ ] Regular retrospectives driving improvements
- [ ] Team operating smoothly with minimal friction

---

## Variations & Adaptations

### Solo Developer + AI
**Adjustments:**
- Simplify ceremonies (planning = 15 min, review = 10 min)
- Focus on documentation for "future you"
- AI handles all automated testing
- Use async communication patterns exclusively

**Works well for:**
- Side projects
- Freelancers
- Indie hackers

### Small Team (2-5 people) + AI
**Adjustments:**
- AI assists multiple team members
- Daily standup remains async
- Rotate "sprint captain" role among humans
- AI provides consolidated status updates

**Works well for:**
- Startups
- Small dev teams
- Consulting teams

### Large Team (6+) + AI
**Adjustments:**
- Multiple AI instances per team/squad
- Formal sprint ceremonies (synchronous meetings)
- Dedicated QA team + AI testing
- Architecture review board
- More formalized documentation process

**Works well for:**
- Enterprises
- Large product teams
- Complex systems with many stakeholders

---

## FAQ

**Q: Does this only work with specific AI tools?**
A: No! iDea works with any AI development tool (Claude Code, GitHub Copilot, Cursor, etc.). The key is treating AI as an active team member with responsibilities, regardless of the specific tool.

**Q: What if my AI forgets context between sessions?**
A: That's exactly why documentation is central to iDea. ADRs, context files, and changelogs provide persistent memory that survives across sessions and even across different AI tools.

**Q: Is this overkill for small projects?**
A: Use the "Solo Developer + AI" variation. Even a lightweight version of iDea (TDD + documentation + clean-as-you-go) provides significant benefits over ad-hoc development.

**Q: How do I measure if iDea is working?**
A: Track these metrics: sprint velocity, bug escape rate, test coverage, documentation coverage. Compare to your pre-iDea baseline after 3 months.

**Q: Can I modify iDea for my team?**
A: Absolutely! iDea is a framework, not a rigid process. Adapt ceremonies, cadence, and practices to your team's needs. The core principles (TDD, documentation-driven, clean-as-you-go) should remain.

**Q: What if my team resists writing so much documentation?**
A: Start small. Document only critical decisions (ADRs) and lessons learned. As the team sees the value of persistent memory and cross-session continuity, expand documentation practices.

**Q: How does iDea integrate with existing Agile practices?**
A: iDea extends Agile/Scrum with AI-specific workflows. If you're already doing Agile, you're 80% there. Add: (1) explicit AI roles, (2) documentation-driven development, (3) AI testing workflows.

**Q: What about pair programming with AI?**
A: iDea assumes continuous AI assistance throughout development. Think of it as "pair programming by default" where the AI is always available to implement, test, and document. Human provides direction and approval.

---

## Success Metrics

### Typical Results After 3 Months:
- **Velocity increase:** 30-50% compared to human-only development
- **Bug escape rate:** <5% due to TDD + AI testing
- **Documentation coverage:** >90% (AI documents as it builds)
- **Test coverage:** >80% (TDD enforced from day one)
- **Deployment frequency:** Daily (automated CI/CD)

### Why It Works:
- AI handles repetitive tasks (tests, docs, refactoring)
- Human focuses on strategy, architecture, UAT
- Documentation provides cross-session continuity
- TDD prevents technical debt accumulation
- Clean-as-you-go prevents documentation debt

---

## Resources & Templates

### Documentation Templates
- **Sprint Planning Template** - Agenda and deliverables
- **ADR Template** - Architecture decision records
- **Sprint Completion Summary** - Review deliverable
- **Retrospective Notes** - What worked, what didn't
- **Bug Report Template** - Structured bug documentation

### Recommended Tools
- **Version control:** Git + GitHub/GitLab/Bitbucket
- **CI/CD:** GitHub Actions, GitLab CI, CircleCI, Jenkins
- **Documentation:** Markdown files in repository
- **Testing:** Language-specific frameworks (pytest, Jest, JUnit, etc.)
- **AI tools:** Claude Code, GitHub Copilot, Cursor, Continue, etc.
- **Project management:** GitHub Projects, Linear, Jira, Trello

---

## Contributing & Feedback

iDea Method is open for community contribution and adaptation.

**Share your experiences:**
- Success stories and case studies
- Adaptations for specific contexts
- Template improvements
- Metrics and results
- Challenges and solutions

**How to contribute:**
- Submit patterns to DEIA Book of Knowledge
- Participate in discussions
- Propose improvements via issues/PRs
- Share your sprint reports and metrics

---

## Acknowledgments

iDea Method synthesizes best practices from:
- Agile/Scrum methodologies (iterative development, ceremonies)
- Test-Driven Development (TDD principles)
- Documentation-Driven Development (docs as code)
- DevOps/CI/CD practices (automation, continuous delivery)
- Human-AI collaboration research (emerging field)

Special thanks to the AI development community for pioneering new ways of working with AI tools as true collaborators.

---

## Version History

**v1.0 (2025-10-10)**
- Initial public release
- Core framework definition
- 5-phase workflow
- Sprint ceremonies
- Best practices documentation
- Implementation checklist
- Variations for different team sizes

---

## License

This framework is released under **CC BY 4.0 (Creative Commons Attribution 4.0 International)**

✅ Free to use, modify, and distribute
✅ Commercial use allowed
✅ Attribution required

**Attribution format:**
```
iDea Method by DEIA Project (https://github.com/deiasolutions/deia)
Licensed under CC BY 4.0
```

---

## Learn More

- **DEIA Project:** [github.com/deiasolutions/deia](https://github.com/deiasolutions/deia)
- **Community Discussion:** [GitHub Discussions](https://github.com/deiasolutions/deia/discussions)
- **Book of Knowledge (BOK):** Browse community-contributed patterns
- **Quick Start:** See [README.md](../../README.md) for DEIA installation

---

**This is a living framework. Use it, adapt it, improve it, share it.**

**Version:** 1.0
**Last Updated:** 2025-10-10
**Framework Status:** Stable, production-ready
