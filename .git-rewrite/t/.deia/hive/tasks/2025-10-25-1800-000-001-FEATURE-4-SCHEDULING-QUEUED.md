# QUEUED: BOT-001 - Feature 4: Adaptive Task Scheduling

**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-001 (Bot Infrastructure)
**Date:** 2025-10-25 18:20 CDT
**Priority:** P0 - NEXT IN QUEUE
**Status:** QUEUED - START AFTER FEATURE 3

---

## Feature 4: Adaptive Task Scheduling (1.5 hours)

**What it is:**
Learn which bots are fast at what, schedule tasks to them intelligently.

**What to build:**
- Performance tracking: Record time to complete by bot + task type
- Scheduling logic: Route tasks to fastest bot type
- Learning: Update performance scores as bots complete tasks
- Endpoint: `POST /api/schedule` - submit task, system routes optimally
- Analytics: `GET /api/schedule/analytics` - show performance data
- Logging: Scheduling decisions to `.deia/bot-logs/scheduling.jsonl`

**Example:**
- BOT-001 (infrastructure) completes infra tasks in 10 min avg
- BOT-003 (chat) completes chat tasks in 5 min avg
- New infra task comes in → route to BOT-001
- New chat task comes in → route to BOT-003
- System learns and improves routing over time

**Implementation:**
- Track performance per (bot, task_type) pair
- Update scores as tasks complete
- Use scores when routing new tasks
- Fall back to orchestrator if no historical data

**Success criteria:**
- [ ] Performance tracked per bot type
- [ ] Routing improves response time
- [ ] Scheduling decisions logged
- [ ] Analytics endpoint working
- [ ] Learns from past performance
- [ ] 70%+ test coverage

**Time estimate:** 1.5 hours

---

## Queue Position

After Feature 3 (Bot Communication).

**No idle time. Start immediately when Feature 3 complete.**

---

**Q33N out. Feature 4 queued and ready.**
