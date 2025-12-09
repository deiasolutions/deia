# TASK ASSIGNMENT: HTTP Service API Expansion
**From:** Q33N (BEE-000 Queen)
**To:** BOT-001 (CLAUDE-CODE-001)
**Date:** 2025-10-25 22:15 CDT
**Priority:** P2
**Backlog ID:** NEW
**Queue Position:** 6/9

---

## Mission

Expand bot HTTP service API with additional endpoints for status monitoring, metrics, and lifecycle management.

---

## Task Details

**What:** Add comprehensive HTTP endpoints to bot service infrastructure

**Endpoints to Implement:**
1. `GET /metrics` - Performance metrics (CPU, memory, task queue depth)
2. `GET /history?limit=N` - Task execution history
3. `POST /restart` - Graceful service restart
4. `GET /logs?lines=N` - Recent logs
5. `POST /config` - Update bot configuration
6. `GET /dependencies` - List service dependencies
7. `DELETE /cache` - Clear bot caches

**Acceptance Criteria:**
- [ ] All 7 endpoints working
- [ ] Response format consistent (JSON)
- [ ] Error handling robust (invalid args, missing resources)
- [ ] Metrics accurate
- [ ] Tests for all endpoints
- [ ] Performance acceptable (< 100ms response)

---

## Deliverable

Create file: `.deia/hive/responses/deiasolutions/bot-001-http-service-expansion-complete.md`

**Estimated Time:** 240 minutes

---

**Queue Position:** After BACKLOG-012

Go.
