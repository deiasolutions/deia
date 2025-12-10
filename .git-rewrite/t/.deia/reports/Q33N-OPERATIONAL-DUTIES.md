# Q33N Operational Duties During Bot Work
**Date:** 2025-10-25
**Role:** BEE-000 (Meta-Governance & Coordination)
**Status:** Active Monitoring

---

## What Q33N Does While Bots Work

### Continuous Monitoring (Real-time)
- [ ] Watch bot status files for completion signals
- [ ] Detect task finish → immediately queue next task
- [ ] Monitor `.deia/hive/responses/deiasolutions/` for updates
- [ ] Catch blockers within 1 minute of posting
- [ ] Read question files continuously, respond < 30 min
- [ ] Track queue depth (maintain 3-5 tasks always)

### Question Response (On-Demand)
- [ ] BOT-001 has blocker? Respond < 15 min (CRITICAL)
- [ ] BOT-003 has question? Respond < 30 min (HIGH)
- [ ] Unclear requirements? Clarify or escalate to Dave
- [ ] Design decisions needed? Make decision or escalate
- [ ] Architecture questions? Provide guidance or escalate

### Queue Management (Continuous)
- [ ] Monitor bot task completion in status files
- [ ] When bot finishes task: Add next task to queue immediately
- [ ] Check queue depth every status file update
- [ ] If < 3 tasks: Queue more NOW
- [ ] Prevent any idle moments
- [ ] Manage queue transitions (fire drill → sprint 2 → hardening → polish)

### Integration Verification (As Tasks Complete)
- [ ] BOT-003 finishes Sprint 2.1? Verify:
  - [ ] Code written (not mocked)
  - [ ] Tests exist (70%+ coverage)
  - [ ] Tests pass
  - [ ] Feature works end-to-end
  - [ ] Logging in place
  - [ ] No TODOs in production code
- [ ] Same verification for BOT-001 tasks
- [ ] Flag any quality issues immediately

### Session Logging Updates
- [ ] Append to `.deia/sessions/2025-10-25-Q33N-Fire-Drill-Launch.md`
- [ ] Log queue management decisions
- [ ] Document blockers and resolutions
- [ ] Track response times to questions
- [ ] Note any escalations to Dave

### Hive Coordination
- [ ] Prepare for CODEX arrival in ~9 hours
- [ ] Have QA task queue ready
- [ ] Have onboarding briefing prepared
- [ ] Coordinate BOT-001 and BOT-003 integration points
- [ ] Manage cross-bot dependencies

### Documentation Maintenance
- [ ] Update work queue status continuously
- [ ] Keep fire drill coordination doc current
- [ ] Track time/effort metrics for velocity
- [ ] Document any process improvements discovered
- [ ] Keep sprint 2/hardening/polish queues current

### Risk Management
- [ ] Watch for blockers that spiral into bigger issues
- [ ] Escalate CRITICAL issues to Dave within 15 min
- [ ] Monitor for stuck bots (no status update > 1 hour = investigate)
- [ ] Catch quality issues early (mocks, stubs, TODOs)
- [ ] Flag production-readiness concerns

### Escalation to Dave (When Needed)
- [ ] Bot blocked > 30 min on unsolvable issue
- [ ] Quality violation (mocks/stubs in production code)
- [ ] Architecture decision that Q33N can't make
- [ ] Scope change request
- [ ] CRITICAL blocker requiring user decision
- [ ] Velocity concerns (tasks taking 2x estimate)

### Performance Analysis
- [ ] Track actual time vs estimate for each task
- [ ] Note which tasks run over/under
- [ ] Identify patterns (UI tasks faster, infra slower?)
- [ ] Document for better estimates next sprint
- [ ] Watch for velocity trends

---

## Specific Actions During Bot Work

### If BOT-001 Posts Status:
1. Read status immediately
2. Verify tasks completed match definition of done
3. Check queue depth
4. If < 3 tasks: Add more from queue
5. Update master queue tracking
6. Append to session log

### If BOT-003 Posts Question:
1. Read immediately
2. Resolve within 30 min OR escalate
3. Post response to same file
4. Continue monitoring

### If 1 Hour Passes Without Status Update:
1. Check session logs for activity
2. If no activity: Investigate (blocked? stuck? crashed?)
3. Post inquiry to bot status file
4. If no response in 15 min: Escalate to Dave

### When BOT-001 Completes Fire Drill:
1. Verify all 5 tasks done (production code, tests pass, logged)
2. Immediately notify: "Sprint 2 queue ready, pick up Task 1"
3. Queue Sprint 2.1-2.6 confirmed
4. Add hardening tasks to secondary queue
5. No downtime transition

### When BOT-003 Finishes Sprint 2:
1. Verify all 6 tasks done (production code, tests pass, logged)
2. Immediately notify: "Hardening queue ready, pick up Task 1"
3. Queue hardening.1-5 confirmed
4. Add polish tasks to secondary queue
5. No downtime transition

---

## Time Management Strategy

**While bots work (assuming 8 hours of active work):**

- **First 2 hours:** Light monitoring, prep next queue phases
- **Middle 4 hours:** Active monitoring, respond to questions, manage queue
- **Last 2 hours:** Prepare CODEX arrival tasks, verify bot quality, prepare handoff

**Goal:** Zero idle time for Q33N too. Always something to do.

---

## Proactive Work (Q33N Self-Assigned)

If no immediate bot needs:
- [ ] Update project documentation
- [ ] Analyze velocity metrics
- [ ] Prepare CODEX onboarding brief
- [ ] Review logs for process improvements
- [ ] Update accomplishments log
- [ ] Create lessons-learned observations
- [ ] Prepare daily status for Dave

---

## Success Criteria

✅ **No bot idle time:** Queue always has next task ready
✅ **No blocker > 30 min:** Fast escalation or resolution
✅ **Quality maintained:** Production code only, tests pass
✅ **Integration verified:** Tasks meet definition of done
✅ **Handoffs smooth:** No downtime between phases
✅ **CODEX ready:** Onboarding and QA tasks prepared
✅ **Documentation current:** Session logs, queue status updated
✅ **Dave informed:** Escalations and blockers reported quickly

---

**Q33N Duty: Coordinate, monitor, queue, verify, escalate.**

**While bots build, Q33N keeps the machine running.**
