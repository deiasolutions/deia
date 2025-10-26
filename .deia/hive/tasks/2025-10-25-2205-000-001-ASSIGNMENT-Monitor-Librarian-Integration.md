# TASK ASSIGNMENT: Integrate Monitor with Librarian Service
**From:** Q33N (BEE-000 Queen)
**To:** BOT-001 (CLAUDE-CODE-001)
**Date:** 2025-10-25 22:05 CDT
**Priority:** P2
**Backlog ID:** BACKLOG-017
**Queue Position:** 3/5

---

## Mission

Auto-index documents when monitor routes them to Librarian service. Integrate monitor + librarian for full document lifecycle.

---

## Task Details

**What:** Make monitor auto-index documents as it routes them

**Current State:**
- Monitor routes documents to directories
- Librarian service exists but not integrated

**Your Work:**
1. Detect routing events in monitor
2. Call librarian index API on routed documents
3. Log index results
4. Handle indexing failures gracefully

**Acceptance Criteria:**
- [ ] Documents auto-indexed when routed
- [ ] Librarian API integration working
- [ ] Error handling for failed indexing
- [ ] Tests cover success and failure cases
- [ ] Performance: indexing doesn't slow routing

---

## Deliverable

Create file: `.deia/hive/responses/deiasolutions/bot-001-backlog-017-complete.md`

**Estimated Time:** 180 minutes

---

**Queue Position:** After BACKLOG-012

Go.
