# Work Plan: DEIA Distributed Carbon-Based Economy

**Prepared By:** BOT-00006 (Drone-Development)
**Date:** 2025-10-12
**For Review By:** BOT-00001 (Queen/Scrum Master)
**Priority:** HIGH - Major strategic initiative with cross-system impacts
**Estimated Duration:** 8-12 weeks (phased approach)

---

## Executive Summary

Dave has designed a comprehensive distributed carbon-based economy for DEIA that includes:
- Three-currency system (Deia Coin, Carbon Credits, Compute Credits)
- Peer-to-peer compute/storage marketplace
- 1.5x hosting ratio (publish 1 unit, host 1.5 units)
- Integration with bot queue, hive coordination, and service delegation
- GitHub-based distributed storage with version control
- LIMB (Local Intelligence Memory Bank) drones for edge computing

**This is infrastructure for the entire DEIA vision.** It enables:
- Cost-aware bot selection (token/carbon optimization)
- Service delegation (Python services over LLM calls)
- DEIA Commons Tools marketplace (creator compensation)
- Distributed social network (DEIA Social)
- Sustainable economic model (align incentives with common good)

**Strategic Impact:**
- Transforms DEIA from knowledge commons to full-stack infrastructure
- Creates sustainable economic model aligned with environmental values
- Enables creator economy without violating "common good" principles
- Provides technical foundation for multi-domain expansion

---

## Source Material Context

### Where This Came From

**Primary Source:**
- `.davedrop/new ideas 2025-10-12 2am.txt` (lines 11-67)
- Written by Dave during brainstorming session
- Raw notes, needs interpretation and design

**Related Sources:**
- `docs/rebel-snail-mail-reflections_20251012_004818.md` - Fibonacci Reciprocity Protocol review
- Current conversation with BOT-00006 (2025-10-12) - Bot queue service, Commons Tools discussion
- `MULTI_DOMAIN_VISION.md` - Economic model section (lines 293-299)
- `CONSTITUTION.md` - Ownership/attribution framework

**Integration Points:**
- Bot Queue Service (completed by BOT-00006)
- Hive coordination system (existing)
- Bot coordinator (existing)
- Service delegation architecture (not yet designed)
- Type system (not yet designed)

### Key Concepts Extracted

**1. Three-Currency System**

```
Deia Coin ←→ Carbon Credits ←→ Compute Credits
```

- **Deia Coin**: Barter credit currency for marketplace transactions
- **Carbon Credits**: Environmental value, tied to carbon offset standard
- **Compute Credits**: Network usage (LLM tokens, storage, bandwidth)

**Exchange rates to be designed.**

**2. The 1.5x Hosting Ratio**

From Dave's notes:
> "a person who wants to publish opts in by hosting 1.5 what he has published in Deia Coin"

Similar to Fibonacci φ ratio (1.618) from Rebel Snail Mail concept.

**Purpose:** Incentivize network participants to provide more resources than they consume.

**3. What You Can Earn Credits For**

- **Compute:** Host local LLMs, offer API tokens
- **Storage:** Host encrypted data nodes
- **Bandwidth:** Relay messages peer-to-peer
- **Memory:** Run LIMB drones (in-memory databases)
- **Contributions:** Create tools, patterns, documentation

**4. DEIA Services Ecosystem**

- **DEIA Compute**: Distributed LLM hosting
- **DEIA Storage**: Distributed encrypted storage (GitHub-based)
- **DEIA Social**: Edge-hosted social network
- **DEIA Base**: Distributed database
- **DEIA Publish**: Recipe-based content distribution
- **DEIA Commons Tools**: Vetted Python services marketplace

**5. Edge Computing Model**

Content hosted on user devices:
- E2E encrypted
- Ephemeral by default (offline = gone)
- Persistent storage requires payment in credits
- GitHub repos as "hard storage" layer

---

## System Components Breakdown

### Component 1: Currency System

**What Needs Design:**

1. **Deia Coin Specification**
   - Token standard (ERC-20? Custom blockchain? Database credits?)
   - Initial supply and distribution
   - Minting rules (how are new coins created?)
   - Transaction fees
   - Wallet system

2. **Carbon Credits Integration**
   - Mapping to real-world carbon offset standards
   - Verification mechanism (how do we know compute = X carbon?)
   - Exchange rate with Deia Coin
   - Corporate carbon offset program integration

3. **Compute Credits Specification**
   - Unit definition (1 credit = X tokens? Y GB? Z CPU hours?)
   - Metering system (how do we track usage?)
   - Rate limiting
   - Fraud prevention

4. **Exchange Mechanism**
   - Marketplace for currency exchange
   - Automated market maker (AMM) or order book?
   - Price discovery mechanism
   - Slippage protection

**Deliverables:**
- Currency specification document
- Token/credit smart contract (if blockchain-based) OR database schema
- Exchange rate calculation algorithm
- Wallet/account management system

**Estimated Effort:** 3-4 weeks

---

### Component 2: Credit Earning Mechanisms

**What Needs Design:**

1. **Compute Contribution Tracking**
   - How do we verify someone is hosting an LLM?
   - Proof-of-computation protocol
   - Quality-of-service (QoS) measurement
   - Uptime tracking
   - Fraud prevention (Sybil resistance)

2. **Storage Contribution Tracking**
   - How do we verify storage space provided?
   - Data availability proofs
   - Redundancy requirements (how many copies?)
   - GitHub storage integration

3. **Bandwidth/Relay Tracking**
   - Proof-of-relay protocol
   - Packet verification
   - 1.5x ratio enforcement
   - Privacy preservation (don't reveal routing)

4. **LIMB Drone Hosting**
   - Registration system
   - Health checks
   - Load balancing
   - Payment for uptime

5. **Content/Tool Contributions**
   - Quality gates (how do we verify "bug free, harmless, helpful"?)
   - Peer review system
   - Download/usage tracking
   - Creator attribution

**Deliverables:**
- Proof protocols for each contribution type
- Monitoring/metering services
- Credit accrual calculation engine
- Anti-fraud detection system

**Estimated Effort:** 4-6 weeks

---

### Component 3: Service Delegation Architecture

**What Needs Design:**

1. **Service Registry**
   - Catalog of available services
   - Service discovery mechanism
   - Version management
   - Dependency resolution

2. **Service Invocation**
   - RPC protocol (gRPC? REST? Custom?)
   - Authentication/authorization
   - Rate limiting per credit balance
   - Error handling and retries

3. **Cost-Aware Routing**
   - Select cheapest service for task
   - Fallback to LLM if service unavailable
   - Quality vs cost tradeoff
   - Load balancing

4. **Service Hosting**
   - Local services (Python packages)
   - Remote services (APIs)
   - Sandboxing/isolation
   - Health monitoring

**Deliverables:**
- Service registry database/API
- Client library for service invocation
- Cost calculation engine
- Service hosting toolkit

**Estimated Effort:** 3-4 weeks

---

### Component 4: Type System & Domain Filtering

**What Needs Design:**

1. **Type-Ref / Type-Def Model**
   - Type-ref: Pointer to type definition
   - Type-def: Actual type implementation
   - Type registry (centralized or distributed?)
   - Versioning

2. **Domain Filtering**
   - Allow/block lists per domain
   - Type compatibility checking
   - Censorship vs curation (policy)
   - Trust model

3. **Type Validation**
   - Schema validation
   - Runtime type checking
   - Security scanning (malicious types?)

**Deliverables:**
- Type system specification
- Type registry service
- Domain filter configuration format
- Validation tools

**Estimated Effort:** 2-3 weeks

---

### Component 5: DEIA Commons Tools Marketplace

**What Needs Design:**

1. **Tool Submission Process**
   - Quality gates (automated tests)
   - Security review
   - Community review
   - Approval workflow

2. **Tool Distribution**
   - Package management (pip? custom?)
   - Version control
   - Update notifications
   - Rollback mechanism

3. **Creator Compensation**
   - Credit earning model (downloads? usage? reviews?)
   - Attribution tracking
   - Provenance verification
   - Dispute resolution

4. **Discovery & Ratings**
   - Search/browse interface
   - Rating system
   - Review system
   - Recommendation engine

**Deliverables:**
- Marketplace web/CLI interface
- Package repository
- Creator dashboard
- Rating/review database

**Estimated Effort:** 4-5 weeks

---

### Component 6: Integration with Bot Queue

**What Needs Design:**

1. **Cost-Aware Bot Selection**
   - Extend BotQueue with cost/carbon tracking
   - Model selection logic (Opus vs Sonnet vs Haiku vs service)
   - Carbon budget per task
   - Credit balance checking

2. **Service Delegation in Bot Workflow**
   - Bot checks service registry before LLM call
   - Delegates to Python service if available
   - Falls back to LLM if service fails
   - Updates credit balances

3. **Idle Bot Utilization**
   - Idle bots host services
   - Idle bots provide compute
   - Credit earning for bot owner

**Deliverables:**
- Extended BotQueue class
- Bot cost calculation module
- Service delegation logic
- Credit integration

**Estimated Effort:** 2-3 weeks

---

### Component 7: GitHub-Based Distributed Storage

**What Needs Design:**

1. **Encryption Layer**
   - E2E encryption for all stored content
   - Key management (who has keys?)
   - Access control

2. **Recipe-Based Retrieval**
   - Recipe format (how to rebuild content from repos)
   - Recipe execution engine
   - Verification (content integrity)

3. **Version Control Integration**
   - Git-native storage
   - Branching strategy
   - Conflict resolution

4. **Storage Quota & Credits**
   - How much storage = X credits?
   - Quota enforcement
   - Garbage collection

**Deliverables:**
- Encryption library
- Recipe specification
- Storage client
- Quota management service

**Estimated Effort:** 3-4 weeks

---

### Component 8: DEIA Social Network

**What Needs Design:**

1. **Edge Hosting Model**
   - Content hosted on user devices
   - Peer discovery
   - Replication strategy

2. **E2E Encryption**
   - Signal Protocol? Custom?
   - Group messaging
   - Media sharing

3. **Ephemeral Content**
   - Offline = deleted
   - Persistence pricing
   - Backup options

4. **Credit Integration**
   - Pay for persistent presence
   - Earn credits by hosting others' content

**Deliverables:**
- Social network client (web/mobile)
- P2P protocol implementation
- Encryption layer
- Hosting service

**Estimated Effort:** 6-8 weeks (Phase 2 or later)

---

## Constitutional Alignment

### Does This Conflict with DEIA Principles?

**From PRINCIPLES.md:**
- "No paywalls, no data selling, no exclusive access"
- "Share for the common good"
- "Knowledge belongs in the commons, not locked behind walls"

**Analysis:**

**Potential Conflicts:**
- Introducing credits = economics (could corrupt "common good")
- Marketplace dynamics = competition (vs cooperation)
- Pay-for-persistence = paywall (vs free access)

**How to Align:**

1. **Knowledge Remains Free**
   - BOK patterns: Always free, no credits required
   - Documentation: Always free
   - Basic tools: Free tier with credits for premium features

2. **Credits Are for Services, Not Access**
   - Like Red Hat: FOSS software, pay for hosting/support
   - Credits pay for compute/storage/bandwidth, not knowledge
   - Can use DEIA without credits (just slower/local-only)

3. **Commons Governance Applies**
   - Marketplace governed by community (Ostrom principles)
   - No vendor lock-in
   - Open standards
   - Creator rights protected

4. **Environmental Alignment**
   - Carbon credits = incentive for sustainability
   - Aligns with "restore, don't extract" principle
   - Corporate carbon offsets fund commons

**Recommendation:** This CAN align with principles if designed carefully. Requires Constitutional amendment (Article VII - Economic Model).

---

## Proposed Work Phases

### Phase 0: Research & Architecture (Week 1-2)

**Objectives:**
- Deep dive into source materials
- Research existing systems (blockchain, distributed storage, P2P)
- Design high-level architecture
- Identify technical risks
- Define success criteria

**Deliverables:**
- Architecture diagram
- Technology stack decisions
- Risk assessment
- Detailed technical specification

**Assigned To:** BOT-00003 (Integration) + BOT-00006 (Development)

**Queen's Role:** Review architecture, approve tech stack

---

### Phase 1: Currency System MVP (Week 3-6)

**Objectives:**
- Implement Deia Coin (database-backed, not blockchain initially)
- Implement Compute Credits metering
- Simple wallet/account system
- Basic exchange mechanism

**Deliverables:**
- Credit database schema
- Account management API
- Basic transaction system
- CLI for credit operations

**Assigned To:** BOT-00006 (Development)

**Dependencies:** Phase 0 complete

**Queen's Role:** Weekly status review, unblock issues

---

### Phase 2: Service Delegation Core (Week 5-8)

**Objectives:**
- Service registry
- RPC protocol implementation
- Integration with bot queue
- Cost-aware routing logic

**Deliverables:**
- Service registry service
- Client library (Python)
- Extended BotQueue class
- Example services (3-5)

**Assigned To:** BOT-00003 (Integration) + BOT-00006 (Development)

**Dependencies:** Phase 1 in progress (can start in parallel)

**Queen's Role:** Coordinate with Phase 1, manage dependencies

---

### Phase 3: Type System & Commons Tools (Week 7-10)

**Objectives:**
- Type-ref/type-def implementation
- Tool submission workflow
- Quality gates (automated tests)
- Basic marketplace interface

**Deliverables:**
- Type registry
- Tool submission portal
- Package repository
- CLI for tool discovery

**Assigned To:** BOT-00006 (Development) + BOT-00005 (Documentation)

**Dependencies:** Phase 2 service registry complete

**Queen's Role:** Community engagement for early tool submissions

---

### Phase 4: Credit Earning Mechanisms (Week 9-12)

**Objectives:**
- Proof-of-computation protocol
- Storage contribution tracking
- Creator credit accrual
- Anti-fraud detection

**Deliverables:**
- Proof protocols implemented
- Monitoring services
- Credit accrual engine
- Fraud detection system

**Assigned To:** BOT-00006 (Development) + BOT-00002 (Testing)

**Dependencies:** Phase 1 complete

**Queen's Role:** Security review, fraud testing

---

### Phase 5: Integration & Testing (Week 11-14)

**Objectives:**
- End-to-end integration testing
- Load testing
- Security audit
- Documentation

**Deliverables:**
- Test suite (unit + integration)
- Performance benchmarks
- Security audit report
- User documentation

**Assigned To:** BOT-00002 (Testing) + BOT-00005 (Documentation)

**Dependencies:** Phases 1-4 complete

**Queen's Role:** UAT coordination with Dave

---

### Phase 6: GitHub Storage (Future Phase)

**Objectives:**
- Recipe-based content distribution
- Encryption layer
- Version control integration

**Deliverables:**
- Storage client
- Recipe engine
- Encryption library

**Assigned To:** TBD

**Dependencies:** Phase 5 complete

**Timeline:** After MVP validated (12+ weeks)

---

### Phase 7: DEIA Social (Future Phase)

**Objectives:**
- Edge-hosted social network
- E2E encryption
- P2P protocol

**Deliverables:**
- Social network client
- P2P implementation
- Hosting service

**Assigned To:** TBD

**Dependencies:** Phase 6 complete

**Timeline:** 2026 or later (separate major project)

---

## Resource Requirements

### Bot Assignments (Proposed)

**BOT-00001 (Queen/Scrum Master):**
- Overall coordination
- Sprint planning
- Dependency management
- Status reporting to Dave
- Community engagement

**BOT-00002 (Drone-Testing):**
- Test infrastructure for all phases
- Fraud detection testing
- Security testing
- UAT coordination

**BOT-00003 (Drone-Integration):**
- Service delegation architecture
- Integration between components
- API design
- Backward compatibility

**BOT-00005 (Drone-Documentation):**
- Architecture documentation
- API documentation
- User guides
- Tutorial content

**BOT-00006 (Drone-Development):**
- Currency system implementation
- Bot queue extension
- Type system
- Credit accrual engine

**BOT-00008 (if available):**
- Commons Tools marketplace frontend
- CLI tooling
- Developer experience

**Additional Resources Needed:**
- Economics advisor (design exchange rates, carbon mapping)
- Security expert (audit crypto, fraud prevention)
- Legal review (if touching real-world carbon credits)

---

## Success Criteria

### Phase 1-5 MVP Success

**Technical:**
- [ ] Deia Coin transactions work
- [ ] Services can be registered and invoked
- [ ] Bot queue selects services over LLMs when cheaper
- [ ] Credits accrue for contributions
- [ ] 3+ tools in Commons marketplace
- [ ] Zero security vulnerabilities (critical/high)

**User:**
- [ ] Dave can earn credits by hosting a service
- [ ] Dave can use credits to invoke services
- [ ] Credits reduce overall token costs by 30%+
- [ ] Tool submission takes <30 minutes
- [ ] Developer can discover and use tools easily

**Economic:**
- [ ] Exchange rates are stable (no runaway inflation)
- [ ] 1.5x hosting ratio is enforced
- [ ] Carbon credit mapping is accurate
- [ ] Economic model is sustainable (projections)

**Governance:**
- [ ] Constitutional amendment approved
- [ ] Community consensus on economic model
- [ ] No "common good" principle violations
- [ ] Transparent credit tracking

---

## Risks & Mitigations

### Risk 1: Economic Model Instability

**Risk:** Exchange rates crash, credits become worthless, users lose trust

**Likelihood:** Medium
**Impact:** Critical

**Mitigations:**
- Start with closed beta (controlled user base)
- Implement circuit breakers (halt trading if volatility too high)
- Reserve fund (stabilization mechanism)
- Regular economic audits

---

### Risk 2: Fraud / Sybil Attacks

**Risk:** Bad actors create fake accounts, earn credits without providing value

**Likelihood:** High
**Impact:** High

**Mitigations:**
- Proof protocols for all contribution types
- Reputation system (new accounts have limits)
- Anomaly detection (ML-based)
- Community reporting
- Manual review for large transactions

---

### Risk 3: Conflicts with DEIA Principles

**Risk:** Community rejects economic model as violating "common good"

**Likelihood:** Medium
**Impact:** Critical (could kill entire initiative)

**Mitigations:**
- Early community engagement
- Constitutional amendment process
- Clear articulation: Credits = services, not access
- Free tier always available
- Transparent governance

---

### Risk 4: Technical Complexity

**Risk:** System is too complex, takes 2x longer than estimated, drains resources

**Likelihood:** High
**Impact:** High

**Mitigations:**
- Phased approach (MVP first)
- Simplify where possible (database credits vs blockchain)
- Weekly progress reviews
- Kill criteria (if Phase 1-2 fail, pivot)
- External expertise (hire if needed)

---

### Risk 5: Legal/Regulatory

**Risk:** Real-world carbon credits trigger securities law, financial regulations

**Likelihood:** Low-Medium
**Impact:** Critical

**Mitigations:**
- Legal review before Phase 1 begins
- Keep credits internal initially (no real-world exchange)
- Structure as utility tokens, not securities
- Consult with regulatory experts

---

### Risk 6: User Adoption

**Risk:** Nobody wants to earn/spend credits, system is unused

**Likelihood:** Medium
**Impact:** High

**Mitigations:**
- Seed liquidity (Dave provides initial credits)
- Compelling use cases (clear value prop)
- Gamification (leaderboards, achievements)
- Integration with existing tools (BOK, bot queue)
- Marketing campaign

---

## Decision Points for Queen

### Immediate Decisions Needed

**1. Approve/Modify Work Plan**
- Is the phased approach acceptable?
- Are timeline estimates realistic?
- Should we compress or extend?

**2. Bot Assignments**
- Approve proposed bot assignments
- Any conflicts with current work?
- Need to recruit additional bots?

**3. Priority vs Other Work**
- This is 12-14 weeks of effort
- What gets deprioritized?
- Any show-stoppers for starting now?

**4. Go/No-Go on Phase 0**
- Start research & architecture phase immediately?
- Wait for Dave's approval first?
- Need more information?

---

### Upcoming Decisions (Week 1-2)

**5. Technology Stack**
- Blockchain vs database for credits?
- Which RPC protocol for services?
- Type system implementation approach?

**6. Economic Model Parameters**
- What are initial exchange rates?
- How is 1.5x ratio enforced?
- What are credit earning formulas?

**7. Constitutional Amendment**
- Propose amendment to community now?
- Wait until MVP proven?
- Scope of amendment?

---

## Coordination with Other Hive Work

### Dependencies on Current Work

**Bot Queue Service (BOT-00006, completed):**
- ✅ Foundation for cost-aware bot selection
- Will extend in Phase 2

**Bot Coordinator (existing):**
- ✅ Bot registration and identity
- Will integrate credit tracking

**Hive Coordination Rules (existing):**
- ✅ Multi-bot workflow
- Will add credit-based task pricing

### Work This Blocks

**DEIA Commons Tools Marketplace:**
- Blocked until Phase 3 complete
- Community has been asking for this

**Multi-Domain Expansion:**
- Economic model needed for sustainability
- Healthcare/Legal domains may fund development

**Vendor Partnerships:**
- Can offer carbon offsets to corporate sponsors
- Revenue model more attractive to VCs (if needed)

---

## Communication Plan

### Status Updates to Dave

**Weekly:**
- Progress report (what's done, what's blocked)
- Key decisions needed
- Risk updates

**Format:** Short summary in chat + link to detailed report

---

### Status Updates to Hive

**Daily:**
- Update bot-status-board.json with current work
- Announce major milestones in announcements array

**Weekly:**
- Cross-domain sync (all bots, 1-hour meeting)
- Dependency coordination

---

### Community Engagement

**Phase 0:**
- Announce initiative in GitHub Discussions
- Request feedback on economic model

**Phase 1-2:**
- Weekly blog posts on progress
- Invite early testers

**Phase 3:**
- Open beta for Commons Tools
- Creator onboarding

---

## Next Steps (Awaiting Queen Approval)

**If Approved:**

1. **Immediate (Today):**
   - Queen assigns BOT-00003 and BOT-00006 to Phase 0
   - Schedule Phase 0 kickoff (architecture session)
   - Create GitHub project board for tracking

2. **Week 1:**
   - Deep dive research (blockchain vs database, P2P protocols, etc.)
   - Draft architecture document
   - Identify external expertise needed

3. **Week 2:**
   - Complete architecture review with Queen
   - Dave approval on architecture
   - Begin Phase 1 implementation

**If Not Approved:**
- Queen provides feedback on plan
- BOT-00006 revises and resubmits
- Alternative: De-scope to smaller MVP

---

## Supporting Documents

**Key Files to Review:**
1. `.davedrop/new ideas 2025-10-12 2am.txt` (source material)
2. `docs/rebel-snail-mail-reflections_20251012_004818.md` (related concept)
3. `src/deia/bot_queue.py` (existing bot queue to extend)
4. `~/.deia/bot_coordinator.py` (existing coordination to integrate)
5. `CONSTITUTION.md` (governance framework)
6. `PRINCIPLES.md` (alignment check)

**New Files Created:**
- `src/deia/bot_queue.py` (completed by BOT-00006)
- `tests/test_bot_queue.py` (test suite)
- `.deia/bot-queue-service-guide.md` (documentation)
- `.deia/newbot-orientation.md` (bot onboarding)

---

## Conclusion

This is a **major strategic initiative** that will transform DEIA from a knowledge commons into full-stack infrastructure for human-AI collaboration.

**It's ambitious but necessary** to achieve the 10-year vision.

**It's risky but mitigated** through phased approach and kill criteria.

**It's economically aligned** with environmental and common good principles.

**Queen's decision:** Approve and assign resources, or modify plan, or defer.

---

**Prepared by:** BOT-00006 (Drone-Development)
**Instance:** e872a482
**Date:** 2025-10-12
**Status:** Awaiting Queen Review

---

**For Queen (BOT-00001): Please review this plan and provide one of the following:**

A) **APPROVED** - Assign bots to Phase 0 immediately
B) **APPROVED WITH CHANGES** - Specify modifications needed
C) **DEFERRED** - Provide timeline for reconsideration
D) **REJECTED** - Provide rationale and alternative direction

**Once Queen approves, BOT-00006 will pass this plan to Dave for final authorization.**
