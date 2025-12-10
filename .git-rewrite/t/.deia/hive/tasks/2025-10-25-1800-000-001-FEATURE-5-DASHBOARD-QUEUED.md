# QUEUED: BOT-001 - Feature 5: System Health Dashboard

**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-001 (Bot Infrastructure)
**Date:** 2025-10-25 18:20 CDT
**Priority:** P0 - NEXT IN QUEUE
**Status:** QUEUED - START AFTER FEATURE 4

---

## Feature 5: System Health Dashboard (1.5 hours)

**What it is:**
Real-time view of entire bot system. Know what's happening everywhere.

**What to build:**
- Dashboard endpoint: `GET /api/dashboard` - system overview
- Metrics returned:
  - Total bots running + their statuses
  - Task queue depth (total pending)
  - System load (CPU, memory, latency)
  - Errors in last hour
  - Busiest bot (by throughput)
  - Slowest task type (by avg latency)
  - Alerts triggered
- UI page: Real-time updating dashboard (refresh every 2s)
- Alerts: `GET /api/alerts` - show system warnings/errors

**Implementation:**
- Aggregate metrics from all services
- Show on web dashboard (HTML page)
- Color code by health (green=healthy, yellow=warn, red=critical)
- Log system state snapshots to `.deia/bot-logs/dashboard-snapshots.jsonl`

**Success criteria:**
- [ ] All metrics accessible via API
- [ ] Dashboard loads and updates
- [ ] Color coding accurate
- [ ] Alerts working
- [ ] Performance: dashboard renders < 500ms
- [ ] 70%+ test coverage

**Time estimate:** 1.5 hours

---

## Queue Position

After Feature 4 (Adaptive Scheduling).

**Final feature for BOT-001. Push strong to finish.**

---

**Q33N out. Feature 5 final, queued and ready.**
