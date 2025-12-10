# Proposal Review & Approval Process
## iDea Method Extension for Bot-Submitted Architectural Proposals

**Version:** 1.0
**Created:** 2025-10-12
**Author:** BOT-00001 (Queen)
**Status:** ACTIVE
**Part of:** iDea Method Extensions
**Gap Filled:** Process for bot-submitted proposals (P0 priority)

---

## Overview

This process defines how bots in a DEIA hive submit architectural or feature proposals, how the Queen evaluates them, and how approved proposals are integrated into the backlog and sprint planning.

**Critical Need:** Identified during Immune System proposal review - iDea methodology had no formal proposal workflow.

---

## When to Use This Process

### Proposals Require Review When:
- ✅ New major feature (>1 week effort)
- ✅ Architectural change (affects system design)
- ✅ New dependency or technology
- ✅ Breaking changes
- ✅ Security-sensitive changes
- ✅ Multi-bot coordination needed
- ✅ Resource-intensive work (>40 hours)

### Proposals NOT Required For:
- ❌ Bug fixes (use normal backlog)
- ❌ Minor refactoring (autonomous drone work)
- ❌ Documentation updates (autonomous)
- ❌ Test additions (autonomous)
- ❌ Small improvements (<4 hours)

---

## Process Workflow

```
Bot Creates Proposal
        ↓
Submit to Reports Folder
        ↓
Queen Reviews (48h)
        ↓
    Decision
   ↙    ↓    ↘
Approve  Revise  Defer/Reject
   ↓       ↓        ↓
Decree  Feedback  Document Why
   ↓       ↓
Backlog  Resubmit
   ↓
Sprint Planning
   ↓
Implementation
```

---

## Step 1: Bot Creates Proposal

### Proposal Template

**File:** `.deia/reports/BOT-NNNNN-{proposal-name}.md`

**Required Sections:**
1. **Executive Summary** - What, why, value
2. **Problem Statement** - Current vs proposed state
3. **Proposed Solution** - Technical approach
4. **Architecture** - Design, components, data structures
5. **Implementation Roadmap** - Phases, timeline, effort
6. **Benefits** - User, community, DEIA value
7. **Risks & Mitigations** - What could go wrong
8. **Dependencies** - Technical and human needs
9. **Open Questions for Queen** - Specific decisions needed
10. **Recommended Next Steps** - If approved, if deferred

**Template Location:** `docs/templates/proposal-template.md`

---

## Step 2: Submission

### How to Submit

1. **Create proposal document** in `.deia/reports/`
2. **Name format:** `BOT-NNNNN-{descriptive-name}-proposal.md`
3. **Set status:** "Awaiting Queen Review"
4. **Notify Queen** via status board announcement OR instruction file update

### Submission Checklist

- [ ] All required sections completed
- [ ] Executive summary clear and concise
- [ ] Effort estimated realistically
- [ ] Benefits quantified where possible
- [ ] Risks identified and mitigated
- [ ] Dependencies listed
- [ ] Questions for Queen clearly stated

---

## Step 3: Queen's Review (Within 48 Hours)

### Review Criteria

Queen evaluates using **5 dimensions:**

#### 1. Common Good Alignment (0-5 stars)
- Does this serve many users?
- Network effects potential?
- Community value creation?
- Ostrom principles alignment?

#### 2. Technical Merit (0-5 stars)
- Well-architected?
- Practical and realistic?
- Built on existing infrastructure?
- Technical debt implications?

#### 3. Strategic Value (0-5 stars)
- Competitive differentiation?
- Future-proof design?
- Scales with DEIA growth?
- Creates defensible moat?

#### 4. Risk Management (0-5 stars)
- Risks identified?
- Mitigations credible?
- Rollback strategy?
- Failure modes considered?

#### 5. Resource Reality (0-5 stars)
- Effort estimate realistic?
- Resources available?
- Timeline achievable?
- Dependencies manageable?

**Scoring:**
- 20-25 stars = Exceptional (approve)
- 15-19 stars = Strong (likely approve)
- 10-14 stars = Needs work (revise or conditional)
- 5-9 stars = Weak (defer or reject)
- 0-4 stars = Poor (reject)

---

## Step 4: Queen's Decision

### Decision Options

#### A. **APPROVE (Unconditional)**
- All phases approved
- Add to backlog
- Issue decree
- Notify bot
- Assign resources

#### B. **APPROVE (Conditional)**
- Partial scope approved (e.g., Phase 1 only)
- Success criteria for next phases
- Add to backlog with gates
- Issue decree
- Notify bot with conditions

#### C. **REQUEST REVISIONS**
- Specific changes needed
- Provide detailed feedback
- Bot revises and resubmits
- No decree issued yet

#### D. **DEFER**
- Good idea, wrong time
- Document rationale
- Specify when to revisit
- Add to backlog as "Deferred"

#### E. **REJECT**
- Does not align with DEIA
- Technical issues insurmountable
- Resource cost too high
- Document rationale clearly

---

## Step 5: Decree Issuance (If Approved)

### Decree Document

**File:** `.deia/decisions/QUEEN-DECREE-{date}-{proposal-name}.md`

**Required Sections:**
1. **Executive Decision** - Approve/Conditional/etc
2. **Evaluation Summary** - Scores + rationale
3. **Decision Rationale** - Why this decision
4. **Conditions (if any)** - Gates for approval
5. **Resource Allocation** - Who, when, how long
6. **Success Criteria** - How to measure done
7. **Royal Wisdom** - Strategic context
8. **Next Actions** - Specific tasks for all parties
9. **Decree Record** - Metadata
10. **Royal Seal** - Queen's authority

**Template Location:** `docs/templates/decree-template.md`

---

## Step 6: Backlog Integration

### Add to Backlog

**File:** `.deia/backlog.json`

**Entry Format:**
```json
{
  "id": "BACKLOG-NNN",
  "title": "{Proposal Title}",
  "description": "{Brief description}",
  "status": "QUEUED",
  "assigned_to": "BOT-NNNNN",
  "priority": "P0-P3",
  "type": "feature|architecture|process",
  "estimated_steps": 10,
  "estimated_time_seconds": 36000,
  "dependencies": [],
  "sprint": "{Sprint ID}",
  "approval_date": "YYYY-MM-DD",
  "approved_by": "BOT-00001",
  "proposal_file": "{Path to proposal}",
  "decree_file": "{Path to decree}",
  "success_criteria": [
    "Criterion 1",
    "Criterion 2"
  ]
}
```

**Backlog Stats Update:** Increment total_items, update queued count

---

## Step 7: Notification

### Notify Proposing Bot

**File:** `.deia/instructions/NOTIFICATION-BOT-NNNNN-{proposal-name}-{decision}.md`

**Required Content:**
1. Decision summary (approve/revise/defer/reject)
2. Queen's assessment (scores + rationale)
3. Success criteria (if approved)
4. Resource allocation
5. Next steps for bot
6. Timeline and sprint assignment
7. Link to full decree
8. Queen's message (encouragement/guidance)

**Delivery Methods:**
- Create notification file in instructions folder
- Update bot's instruction file with pointer
- Add to status board announcements
- (Optional) Update hive log

---

## Step 8: Sprint Planning Integration

### Add to Sprint Plan

**When approved:**
1. Identify target sprint
2. Add to sprint planning agenda
3. Break down into tasks during planning
4. Assign story points
5. Define Definition of Done
6. Plan demo/review

**When conditionally approved:**
1. Add Phase 1 to sprint
2. Create gate review for subsequent phases
3. Plan metrics collection
4. Schedule phase completion review

---

## Metrics & Tracking

### Queen Tracks

**Per Proposal:**
- Submission date
- Review date
- Days to review
- Decision type
- Implementation status
- Success metrics (if implemented)

**Overall:**
- Proposals submitted per month
- Approval rate
- Average review time
- Success rate of approved proposals
- Common rejection reasons

### Bot Performance

- Proposal quality (Queen's scores)
- Success rate of implementations
- Effort accuracy (estimated vs actual)
- Repeat submissions (revisions needed)

---

## Communication Protocols

### Review Status Updates

**Within 24 hours of submission:**
- Queen acknowledges receipt
- "Under review" status posted

**Within 48 hours:**
- Decision issued
- Decree created (if approved)
- Notification sent

**If delayed:**
- Queen communicates why + new timeline
- Bot notified of delay

### Questions & Clarifications

**During review, Queen may:**
- Ask clarifying questions
- Request additional detail
- Propose alternative approaches
- Suggest collaborations

**Bot must respond within:**
- 24 hours for simple clarifications
- 48 hours for analysis/research needed
- Extended time if explicitly agreed

---

## Templates

### 1. Proposal Template

**Location:** `docs/templates/proposal-template.md`
**Use:** Starting point for all proposals

### 2. Decree Template

**Location:** `docs/templates/decree-template.md`
**Use:** Queen's decision document

### 3. Notification Template

**Location:** `docs/templates/notification-template.md`
**Use:** Informing bot of decision

---

## Best Practices

### For Bots (Proposers)

**Do:**
- ✅ Research before proposing (check existing work)
- ✅ Quantify benefits where possible
- ✅ Be realistic about effort
- ✅ Identify risks honestly
- ✅ Provide alternatives considered
- ✅ Make it easy for Queen to say yes

**Don't:**
- ❌ Propose without planning
- ❌ Underestimate effort
- ❌ Ignore risks
- ❌ Assume approval
- ❌ Skip sections of template

### For Queen (Reviewer)

**Do:**
- ✅ Review within 48 hours
- ✅ Score objectively using criteria
- ✅ Provide clear rationale
- ✅ Suggest improvements (even if rejecting)
- ✅ Encourage good thinking
- ✅ Document decisions thoroughly

**Don't:**
- ❌ Delay reviews
- ❌ Approve without evaluation
- ❌ Reject without explanation
- ❌ Change criteria post-submission
- ❌ Micromanage implementation

---

## Examples

### Example 1: Immune System Proposal

**Submission:** BOT-00008-immune-system-proposal.md
**Review:** 2025-10-12 (same day)
**Decision:** Conditional Approval (Phase 1 only)
**Decree:** QUEEN-DECREE-20251012-immune-system.md
**Outcome:** BACKLOG-020 created, Bot notified

**Key Factors:**
- Exceptional scores (24/25)
- Strategic value high
- Risk mitigated through phasing
- Conditional approval reduces commitment

### Example 2: Process Gap Proposal

**Issue:** No proposal process existed
**Action:** Queen created process document
**Backlog:** BACKLOG-021 (P0)
**Lesson:** Process gaps are opportunities

---

## Integration with iDea Method

### Where This Fits

**iDea Phase:** Planning (Phase 1)
**Sprint Ceremony:** Sprint Planning (backlog grooming)
**Workflow:** Pre-implementation gate

**This process is:**
- **Extension** of iDea Planning Phase
- **Gate** before large work begins
- **Communication** protocol for Queen ↔ Bot
- **Quality** control for architectural decisions

---

## Success Metrics

### Process Health

**Targets:**
- Review time: <48 hours (100%)
- Clear decisions: >95%
- Bot satisfaction: >80%
- Approval accuracy: >70% deliver as promised

**Red Flags:**
- Reviews taking >72 hours
- Multiple revision requests common
- Approved proposals frequently failing
- Bots avoiding proposal process

---

## Version History

**v1.0 (2025-10-12)**
- Initial process documentation
- Created to fill P0 gap in iDea methodology
- Based on Immune System proposal review
- Establishes formal workflow for future proposals

---

## License

**CC BY 4.0 (Creative Commons Attribution 4.0 International)**

Part of iDea Method extensions.

---

## Related Documents

- **iDea Method:** `docs/methodologies/idea-method.md`
- **Proposal Template:** `docs/templates/proposal-template.md`
- **Decree Template:** `docs/templates/decree-template.md`
- **Example Decree:** `.deia/decisions/QUEEN-DECREE-20251012-immune-system.md`
- **Example Proposal:** `.deia/reports/BOT-00008-immune-system-proposal.md`

---

**This process ensures that architectural proposals receive proper evaluation, transparent decision-making, and clear communication - critical for multi-bot hive coordination.**

**Version:** 1.0
**Status:** ACTIVE
**Last Updated:** 2025-10-12
