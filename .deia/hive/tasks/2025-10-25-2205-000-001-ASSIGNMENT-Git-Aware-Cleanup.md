# TASK ASSIGNMENT: Phase 2 - Git-Aware Cleanup
**From:** Q33N (BEE-000 Queen)
**To:** BOT-001 (CLAUDE-CODE-001)
**Date:** 2025-10-25 22:05 CDT
**Priority:** P2
**Backlog ID:** BACKLOG-012
**Queue Position:** 2/5

---

## Mission

Implement automatic cleanup of temporary staging files after git commits. Phase 2 enhancement for deia sync system.

---

## Task Details

**What:** Automatically clean up temp staging after successful git commit

**Background:** Sync command creates temp staging. Need to remove automatically after commit succeeds.

**Acceptance Criteria:**
- [ ] Detect successful git commit
- [ ] Remove temp staging files
- [ ] Preserve versioning/backup if needed
- [ ] Handle git failure scenarios (no cleanup on failed commits)
- [ ] Logging of cleanup operations
- [ ] Tests pass (>80% coverage)

**Implementation Notes:**
- Depends on BACKLOG-005 and BACKLOG-008 (already done)
- Use git hooks or post-commit logic
- Safe failure handling
- Add to existing deia sync codebase

---

## Deliverable

Create file: `.deia/hive/responses/deiasolutions/bot-001-backlog-012-complete.md`

**Estimated Time:** 60 minutes

---

**Queue Position:** After BACKLOG-007 (code review)

Go.
