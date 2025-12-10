# DEIA Feature Requests

**Purpose:** Track feature requests and enhancements for the DEIA project.

**Status Legend:**
- 🟢 **Approved** - Approved for development
- 🟡 **Under Review** - Being evaluated
- 🔵 **Proposed** - Initial proposal, needs discussion
- 🔴 **Deferred** - Not prioritized for current sprint
- ✅ **Implemented** - Complete

---

## Feature Requests

### FR-001: Establish Documentation Standards
**Status:** 🔵 Proposed
**Priority:** High
**Requested by:** Dave (User)
**Date:** 2025-10-11
**Entered by:** BOT-00002 (on behalf of Dave)

**Description:**
Establish and implement a standardized documentation approach for DEIA to ensure all features and code are properly documented.

**Problem Statement:**
- Need to ensure features are documented as they're developed
- Need consistency across all documentation
- Need to decide on documentation standards and structure
- Need to start implementing the standard systematically

**Requirements:**
1. Define documentation standard/format (e.g., Google Style, NumPy Style, etc.)
2. Decide on documentation structure:
   - README sections
   - API documentation
   - User guides
   - Developer guides
   - Inline code documentation (docstrings)
3. Create documentation templates
4. Document existing features retroactively
5. Integrate documentation checks into development workflow

**Potential Approaches:**
- **Sphinx** with autodoc for API documentation
- **MkDocs** for user-facing documentation
- **Google Style Guide** or **NumPy Style Guide** for docstrings
- **GitHub Wiki** for community documentation
- **Jupyter notebooks** for tutorials/examples

**Success Criteria:**
- [ ] Documentation standard defined and documented
- [ ] Templates created for common documentation types
- [ ] All modules have complete docstrings
- [ ] All CLI commands documented with examples
- [ ] User guide available for major features
- [ ] Developer guide available for contributors
- [ ] Documentation builds automatically (CI/CD)
- [ ] Documentation hosted/accessible

**Related:**
- Impacts all current and future features
- Related to FR-002 (if exists - code quality standards)

**Notes:**
- This is foundational - should be prioritized
- Can start with templates and gradually document existing code
- Consider automated documentation generation from docstrings

**Estimated Effort:** Medium (2-3 days initial setup, ongoing maintenance)

---

## Template for New Requests

```markdown
### FR-XXX: [Feature Name]
**Status:** 🔵 Proposed
**Priority:** [High/Medium/Low]
**Requested by:** [Name/Bot]
**Date:** [YYYY-MM-DD]

**Description:**
[Brief description of the feature]

**Problem Statement:**
[What problem does this solve?]

**Requirements:**
1. [Requirement 1]
2. [Requirement 2]

**Success Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Estimated Effort:** [Hours/Days/Weeks]
```

---

### FR-002: Improved Bot Coordination Timing Protocols
**Status:** 🔵 Proposed
**Priority:** High
**Requested by:** Dave (User)
**Date:** 2025-10-12
**Entered by:** BOT-00006

**Description:**
Improve bot coordination timing protocols to prevent premature bot identity takeovers and ensure proper handoff procedures.

**Problem Statement:**
- Current 60-second timeout is too aggressive
- Bots can take over identities of actively working bots
- No check for whether a bot is mid-task before takeover
- No mechanism for idle bots to maintain their claim
- Risk of interrupting important work

**Requirements:**
1. **Longer timeout for active work:**
   - Increase stale claim threshold from 60 seconds to 5-10 minutes for bots with active tasks
   - Check task status before allowing takeover

2. **Active heartbeat for idle bots:**
   - Idle bots (status: STANDBY) check in every 30 seconds
   - Working bots update status more frequently (every 15-30 seconds)

3. **Task-aware handoff:**
   - Before claiming identity, check if bot has incomplete work
   - Require explicit "work complete" or "abandoned" status
   - Add "handoff requested" status for graceful transitions

4. **Escalation path:**
   - If bot unresponsive for >10 minutes, escalate to Queen
   - Queen decides: wait longer, reassign, or allow takeover
   - Log all takeovers for audit

5. **Status board integration:**
   - Update .deia/bot-status-board.json with timing info
   - Show "last active task", "time on current task"
   - Warning if bot exceeds reasonable time for task

**Potential Approaches:**
- **Tiered timeouts:** Different timeouts for STANDBY (60s), WORKING (5min), BLOCKED (10min)
- **Graceful degradation:** Bot can request longer timeout if task is complex
- **Queen oversight:** Queen manages all takeovers, not peer-to-peer
- **Work checkpoint:** Bots save state periodically so takeover can resume

**Success Criteria:**
- [ ] No accidental takeovers of actively working bots
- [ ] Clear escalation path when bot is truly stuck
- [ ] Idle bots maintain claim with minimal overhead
- [ ] Queen can audit all bot activity timing
- [ ] Documentation of timing protocols in hive-coordination-rules.md

**Related:**
- .deia/hive-coordination-rules.md (needs timing section)
- ~/.deia/bot_coordinator.py (claim_identity function)
- .deia/bot-status-board.json (add timing fields)

**Notes:**
- Critical for multi-bot coordination stability
- Prevents work loss from interrupted tasks
- Improves trust in hive system

**Estimated Effort:** Medium (1-2 days implementation, testing coordination scenarios)

---

**Last Updated:** 2025-10-12 by BOT-00006
