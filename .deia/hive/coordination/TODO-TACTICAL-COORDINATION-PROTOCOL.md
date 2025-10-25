# TODO: Create Tactical Coordination Protocol

**Created:** 2025-10-19 0200 CDT
**Priority:** P0-CRITICAL
**Assigned:** AGENT-003 (when user approves)
**Estimated:** 2-3 hours
**Trigger:** Epic fail - duplicate assignment (see `.deia/observations/2025-10-19-EPIC-FAIL-agent003-duplicate-assignment.md`)

---

## Purpose

Create comprehensive protocol for AGENT-003 (Tactical Coordinator) role to prevent coordination failures.

**Target File:** `docs/process/TACTICAL-COORDINATION-PROTOCOL.md`

---

## Critical Gaps to Address

### 1. Response Monitoring Protocol
**Must define:**
- Check `.deia/hive/responses/` every 15 minutes during active coordination
- Read ALL responses before making decisions
- Response time SLA: 30 minutes max for agent questions
- Escalation process if coordinator doesn't respond

### 2. Task State Management
**Must define:**
- Active task registry (who's working on what)
- Task lock mechanism (prevent duplicate assignments)
- Verification before assignment (is task still needed?)
- Atomic claim process (race condition prevention)

### 3. Assignment Verification Checklist
**Must define:**
- Check if implementation already exists
- Check if task already assigned
- Check for agent responses before escalating
- Verify task actually needed before assignment

### 4. Reassignment Protocol
**Must define:**
- When reassignment is allowed
- Verification steps (has agent started? how much done?)
- Contact agent before reassigning
- Get confirmation before reassignment
- Handoff process if work partially complete

### 5. Agent Question Handling
**Must define:**
- Response time SLA (30 min max)
- Priority handling for URGENT/BLOCKER questions
- Auto-escalation if coordinator doesn't respond
- Acknowledgment required even if answer takes time

### 6. Coordination Audit Trail
**Must define:**
- Log all assignment decisions
- Log all verification checks performed
- Log all responses read
- Log all escalations
- Reviewable history for debugging

---

## Required Sections

1. **Role Definition** - What tactical coordinator does
2. **Response Monitoring** - Check frequency, what to do
3. **Task Assignment** - Verification checklist before assigning
4. **Task Reassignment** - When/how to safely reassign
5. **Agent Question Handling** - SLA and process
6. **Conflict Resolution** - Duplicate assignments, race conditions
7. **Escalation to Strategic Coordinator** - When to escalate to 001
8. **Audit Trail** - What to log, where, when
9. **Quality Checks** - Coordination quality metrics
10. **Examples** - Good/bad coordination scenarios

---

## Must Include Real Failures

**Include these as anti-patterns:**
- 2025-10-19 duplicate assignment (Agent Coordinator to 005 and 006)
- Root cause: didn't check responses before escalating
- What should have been done differently

---

## Success Criteria

**Protocol is complete when:**
1. Covers all 6 critical gaps identified above
2. Includes verification checklists
3. Includes response time SLAs
4. Includes audit trail requirements
5. Includes real failure examples
6. Prevents duplicate assignment scenario
7. Prevents ignored-question scenario
8. Reviewed by AGENT-001

---

## Dependencies

None - can start immediately

---

## Deliverables

1. `docs/process/TACTICAL-COORDINATION-PROTOCOL.md` (comprehensive protocol)
2. Verification checklist (can be embedded in protocol)
3. Response monitoring schedule (can be embedded in protocol)

---

## Notes

**DO NOT START until user approves.**

This protocol is needed to prevent recurrence of 2025-10-19 epic fail.

---

**Created by:** AGENT-003
**Status:** TODO (awaiting user approval)
**Location:** `.deia/hive/coordination/TODO-TACTICAL-COORDINATION-PROTOCOL.md`
