# BOT-001 DEPLOYMENT READINESS GUIDE - WINDOW 2
**From:** Q33N (BEE-000)
**To:** BOT-001
**Issued:** 2025-10-25 16:36 CDT
**Window:** 18:32 - 20:32 CDT (2 hours) - Deploy after Window 1 complete
**Priority:** HIGH - Production readiness

---

## ASSIGNMENT

Create comprehensive deployment readiness package. This is what ops/devops needs to safely deploy port 8000 to production.

---

## DELIVERABLE FILE

**File:** `.deia/docs/DEPLOYMENT-READINESS-GUIDE.md`

---

## CONTENT REQUIRED

### 1. Pre-Deployment Checklist (30 min)
**Comprehensive checklist for deployment team:**

```
PRE-DEPLOYMENT CHECKLIST
□ All CRITICAL fixes from Window 1 verified working
□ All HIGH priority fixes from Window 1 verified working
□ Visual polish from Window 1 applied and tested
□ Accessibility audit from Window 1 reviewed and critical issues resolved
□ API Reference complete and up-to-date
□ User Guide complete and published
□ All unit tests passing (run pytest)
□ All integration tests passing
□ Database migrations applied (if any)
□ Environment variables configured (list them)
□ Dependencies installed and locked
□ Git history clean, all changes committed
□ Code reviewed and approved
□ Feature flags configured (if any)
□ Monitoring/alerting configured
□ Rollback plan documented and tested (see section 3)
```

**Deliverable:** Clear checkbox list that ops can use

### 2. Health Check Procedures (30 min)
**Specific commands/scripts to verify deployment succeeded:**

```
POST-DEPLOYMENT HEALTH CHECKS

1. Application Startup (1 min)
   Command: systemctl status deia-port-8000
   Expected: running

2. API Connectivity (1 min)
   Command: curl http://localhost:8000/health
   Expected: {"status": "healthy"}

3. Bot Management (2 min)
   - Launch test bot
   - Send test command
   - Verify response
   - Shut down test bot

4. WebSocket Connection (1 min)
   Command: [script to test WebSocket]
   Expected: Connection established, messages flowing

5. Database Connectivity (1 min)
   Command: curl http://localhost:8000/api/system/health
   Expected: {"db": "connected"}

6. Performance Baseline (2 min)
   - Measure response time for 10 requests
   - Expected: < 200ms per request
   - Alert if > 500ms

7. Error Handling (1 min)
   - Send malformed request
   - Expected: Proper error response (not 500)
```

**Deliverable:** Step-by-step health check commands

### 3. Rollback Procedures (30 min)
**How to safely revert if deployment goes wrong:**

```
ROLLBACK PROCEDURES

Scenario 1: Application Won't Start
- Stop service: systemctl stop deia-port-8000
- Revert code to previous version: git checkout [previous-commit]
- Restart service: systemctl start deia-port-8000
- Verify: curl http://localhost:8000/health
- Timeline: ~3 minutes

Scenario 2: Performance Degradation (> 1s response time)
- Check logs: tail -f /var/log/deia-port-8000.log
- If memory leak: Restart service (may buy time)
- If database issue: Check DB performance
- If stuck: Rollback to previous version
- Timeline: ~5-10 minutes to decide

Scenario 3: High Error Rate (> 5% failures)
- Check error logs: grep "ERROR" /var/log/deia-port-8000.log
- Correlate with changes made in this deployment
- If clear bug: Rollback immediately
- If unclear: Investigate while running at reduced capacity
- Timeline: ~15 minutes investigation, then decide

Scenario 4: Critical Security Issue Found
- Stop service immediately: systemctl stop deia-port-8000
- Rollback to previous version
- Notify security team
- Investigate while running previous version
- Timeline: ~1 minute to stop, 3 minutes to rollback
```

**Deliverable:** Clear rollback paths for each scenario

### 4. Production Startup Script (30 min)
**Exact commands to start the application in production:**

```
PRODUCTION STARTUP SCRIPT
#!/bin/bash

# 1. Set environment variables
export FLASK_ENV=production
export LOG_LEVEL=INFO
export PORT=8000
export BOT_SERVICE_URL=http://localhost:9000
export DATABASE_URL=postgres://user:pass@db-host:5432/deia

# 2. Install dependencies (if not cached)
pip install -r requirements.txt

# 3. Run database migrations
python -m alembic upgrade head

# 4. Start application
gunicorn \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class eventlet \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  src.deia.adapters.web.app:app

# 5. Monitor (tail logs)
tail -f /var/log/deia-port-8000.log
```

**Deliverable:** Copy-paste ready startup script

---

## FORMAT & STRUCTURE

```markdown
# Port 8000 Deployment Readiness Guide

## Pre-Deployment Checklist
[Full checklist with items and verification steps]

## Post-Deployment Health Checks
[7 checks with commands and expected output]

## Rollback Procedures
[4 scenarios with exact steps and timelines]

## Production Startup Script
[Exact bash script ready to execute]

## Deployment Timeline
- T-5min: Final checklist verification
- T-0min: Execute startup script
- T+2min: Run health checks
- T+5min: Monitor logs for errors
- T+15min: Full validation complete

## Support Contacts
- On-Call DevOps: [contact]
- Database Team: [contact]
- Security Team: [contact]

## Sign-Off
Reviewed by: [ops engineer]
Approved by: [deployment lead]
Date: [date]
```

---

## SUCCESS CRITERIA

- ✅ Pre-deployment checklist complete (20+ items)
- ✅ Health check procedures documented (7+ checks with exact commands)
- ✅ Rollback procedures clear (4+ scenarios with timelines)
- ✅ Production startup script ready (copy-paste executable)
- ✅ File created: `.deia/docs/DEPLOYMENT-READINESS-GUIDE.md`
- ✅ Clear, actionable language (no ambiguity)
- ✅ Includes timelines and contacts

---

## STATUS REPORT LOCATION

**Due:** 2025-10-25 20:32 CDT

Create file: `.deia/hive/responses/deiasolutions/BOT-001-DEPLOYMENT-READINESS-WINDOW-2-COMPLETE.md`

**Include:**
- All 4 sections complete?
- File created and ready for ops team
- Any edge cases discovered
- Time spent per section
- Ready for Window 3? (YES/NO)

---

## CONTEXT

This guide will be handed to the operations/devops team. Make it bulletproof. No ambiguity. They should be able to deploy port 8000 to production with zero questions.

---

**Q33N - BEE-000**
**CREATE DEPLOYMENT-READY GUIDE FOR OPS TEAM**
