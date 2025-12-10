# Integration Protocol

**Version:** 1.0
**Status:** Active
**Last Updated:** 2025-10-17

---

## Purpose

Define the standard process for integrating completed work into the DEIA project, ensuring:
- All tracking documents stay current
- Tests are run and documented
- Security is reviewed
- Team visibility is maintained

---

## Roles

**Developer Agent:** Completes the work (writes code, tests)
**Integration Agent:** Reviews, tests, and integrates the work (updates tracking)
**Coordinator Agent (001):** Assigns work, reviews integration reports

---

## Integration Checklist

When integrating new code or completed work, the **Integration Agent** must:

### 1. Test Validation ✅

- [ ] **Run all tests** for the component
  ```bash
  pytest tests/unit/test_<component>.py -v --cov=src.deia.<module> --cov-report=term-missing
  ```
- [ ] **Verify coverage** meets minimum:
  - New code: 80% minimum
  - Security code: 90% minimum
  - Existing code: Don't decrease coverage
- [ ] **Check test results:**
  - If **all tests pass** → Continue to step 2
  - If **tests fail** → Document failures, return to developer or fix
  - If **no tests exist** → Add to testing backlog (see step 6)

### 2. Security Review 🔒

- [ ] **For security-critical code** (auth, file access, path validation):
  - Review for common vulnerabilities
  - Check input validation
  - Verify error handling doesn't leak info
  - Test boundary conditions
- [ ] **For all code:**
  - Check for hardcoded secrets (.env, API keys)
  - Verify no PII in logs or outputs
  - Check file permissions are appropriate

### 3. Bug Documentation 🐛

- [ ] **Check for known bugs:**
  - Read developer's notes
  - Review activity logs
  - Check BUG_REPORTS.md for references
- [ ] **Document new bugs found:**
  - Add to BUG_REPORTS.md (see template in that file)
  - Link to component in accomplishments log
  - Note if blocking or non-blocking

### 4. Update Accomplishments Log 📝

- [ ] **Add entry to `.deia/ACCOMPLISHMENTS.md`:**
  - Use template from that file
  - Include all deliverables (code, tests, docs)
  - Note test status and coverage
  - Note security review status
  - Document bugs found/fixed
  - Mark integration status

### 5. Update Tracking Documents 📋

- [ ] **Update BACKLOG.md:**
  - Mark task as complete with checkmark in "In Progress" section
  - Add detailed entry to "Done" section
  - Include actual time vs estimated
  - Note test results and coverage

- [ ] **Update ROADMAP.md:**
  - Mark corresponding phase task as complete
  - Update phase completion percentage if applicable
  - Note if milestone achieved

### 6. Handle Missing Tests 🧪

**If tests don't exist or are incomplete:**

- [ ] **Create test task in BACKLOG.md:**
  ```markdown
  ### Tests for [Component Name]
  **Status:** TODO
  **Priority:** [P0 if security, P1 if core, P2 otherwise]
  **Estimated Effort:** [hours]
  **Dependencies:** Component implementation complete

  **Goal:** Achieve [80/90]% coverage for [component]

  **Tasks:**
  - [ ] Unit tests for core functionality
  - [ ] Edge case tests
  - [ ] Error handling tests
  - [ ] Integration tests (if applicable)
  ```

- [ ] **Mark component as "Needs Tests" in ACCOMPLISHMENTS.md**

- [ ] **Assign test task** or leave unassigned for next available agent

### 7. Activity Logging 📊

- [ ] **Log integration event** to your activity.jsonl:
  ```json
  {
    "ts": "2025-10-17T...",
    "agent_id": "CLAUDE-CODE-XXX",
    "role": "...",
    "event": "integration_complete",
    "message": "Integrated [Component] - [status summary]",
    "meta": {
      "component": "component_name",
      "developer": "CLAUDE-CODE-YYY",
      "files_integrated": ["file1.py", "file2.py"],
      "test_results": "18/18 passed",
      "coverage": "89%",
      "security_review": "passed",
      "bugs_found": 2,
      "bugs_fixed": 2,
      "tracking_updated": ["BACKLOG.md", "ROADMAP.md", "ACCOMPLISHMENTS.md"]
    }
  }
  ```

### 8. Coordination Communication 📡

- [ ] **Send SYNC to Agent 001** (Left Brain Coordinator):
  - Create file: `~/Downloads/uploads/YYYY-MM-DD-HHMM-AGENT_XXX-AGENT_001-SYNC-integration-complete-[component].md`
  - Include:
    - Component integrated
    - Test results
    - Security review status
    - Bugs found/fixed
    - Tracking documents updated
    - Any blockers or concerns
    - Ready for next assignment

---

## Integration Status Levels

Use these in ACCOMPLISHMENTS.md:

- **✅ Complete** - All tests passing, security reviewed, fully integrated
- **⚠️ Needs Tests** - Code complete but no tests or low coverage
- **⚠️ Needs Review** - Tests exist but need security/code review
- **❌ Blocked** - Cannot integrate due to failures, conflicts, or dependencies
- **🚧 In Progress** - Integration underway
- **⏸️ Paused** - Integration stopped, waiting for dependency or decision

---

## Example Integration Flow

### Scenario: Agent 005 completes ProjectBrowser API

1. **Agent 005 (Developer):**
   - Writes `src/deia/services/project_browser.py`
   - Writes `tests/unit/test_project_browser.py`
   - Runs tests locally (18/18 pass, 89% coverage)
   - Documents 2 bugs found in `BUG_REPORTS.md`
   - Sends SYNC to Agent 001: "Task complete, ready for integration"

2. **Agent 005 (Self-Integration, in this case):**
   - Re-runs tests to verify (✅ pass)
   - Reviews security (✅ path validation present)
   - Adds entry to `.deia/ACCOMPLISHMENTS.md`
   - Updates `BACKLOG.md` (mark complete, add to Done)
   - Updates `ROADMAP.md` (mark Phase 2 task complete)
   - Logs integration event to activity.jsonl
   - Sends SYNC to Agent 001: "Integration complete"

3. **Agent 001 (Coordinator):**
   - Reviews integration SYNC
   - Notes completion in session notes
   - Assigns next task to Agent 005

---

## Special Cases

### Self-Integration
- Developer can integrate their own work IF they follow full checklist
- Must still send SYNC to Agent 001 for visibility

### Integration by Different Agent
- Preferred for critical security components
- Second pair of eyes on code review
- Must credit both developer and integrator

### Work Without Tests
- Still document in ACCOMPLISHMENTS.md
- Mark as "⚠️ Needs Tests"
- Create test task in BACKLOG.md
- Don't block integration if code is needed

### Failed Integration
- Document failure reason in activity log
- Return to developer with specific feedback
- Don't update BACKLOG.md as complete
- Create SYNC to Agent 001 with blocker status

---

## Success Metrics

Track these over time:

- **Integration Time:** Time from "work complete" to "integration complete"
- **Test Coverage:** Average coverage of integrated components
- **Bugs per Integration:** Average bugs found during integration
- **Tracking Accuracy:** % of work that's in ACCOMPLISHMENTS.md
- **Rework Rate:** % of integrations that need fixes

---

## Related Documents

- `.deia/ACCOMPLISHMENTS.md` - Central accomplishments log
- `BACKLOG.md` - Task tracking and sprint planning
- `ROADMAP.md` - Phase and milestone tracking
- `BUG_REPORTS.md` - Bug documentation
- `.deia/bot-logs/*.jsonl` - Activity logs
- `docs/process/TASK-ASSIGNMENT-PROTOCOL.md` - How work gets assigned

---

**Maintained By:** All integration agents
**Review Cycle:** After every 10 integrations or monthly
**Change Process:** Propose changes via SYNC to Agent 001
