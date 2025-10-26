# Production Deployment Procedures

**Date:** 2025-10-25
**Version:** 1.0
**Operator:** BOT-001 (Architect)
**Status:** READY

---

## Pre-Deployment Checklist

**Complete these 15 items before deploying (estimated time: 15 minutes)**

### Infrastructure Checks

- [ ] **1. PostgreSQL running**
  ```bash
  systemctl status postgresql
  psql -U deia -d deia_prod -c "SELECT 1"
  ```
  Expected: Running, connection successful

- [ ] **2. Ollama service running**
  ```bash
  systemctl status ollama
  curl http://localhost:11434/api/tags
  ```
  Expected: Running, models available

- [ ] **3. Redis service running** (optional)
  ```bash
  systemctl status redis-server
  redis-cli ping
  ```
  Expected: Running, returns PONG

- [ ] **4. Backup current state**
  ```bash
  # PostgreSQL backup
  pg_dump -U deia deia_prod | gzip > deia_prod_backup_$(date +%s).sql.gz

  # Application code backup
  cp -r ~/app ~/app_backup_$(date +%s)
  ```
  Expected: Backup files created successfully

- [ ] **5. Database connection pool healthy**
  ```bash
  psql -U deia -d deia_prod -c "SELECT count(*) FROM pg_stat_activity WHERE datname='deia_prod';"
  ```
  Expected: <10 connections (not exhausted)

- [ ] **6. Disk space adequate**
  ```bash
  df -h /
  ```
  Expected: >10GB free

- [ ] **7. Monitoring dashboards accessible**
  - Navigate to: `http://localhost:3000` (Grafana)
  - Expected: All 4 dashboards loading, no errors

### Code & Configuration Checks

- [ ] **8. Code changes tested locally**
  - All tests passing
  - No console errors in browser dev tools

- [ ] **9. Configuration files reviewed**
  - `production.yaml` matches production environment
  - Database connection string correct
  - API endpoints correct
  - No debug mode enabled

- [ ] **10. Database migrations pending**
  ```bash
  # Check if migrations needed
  npm run db:status
  ```
  Expected: "No pending migrations" or list of migrations to run

- [ ] **11. SSL certificates valid**
  ```bash
  openssl x509 -in /etc/ssl/certs/port8000.crt -noout -dates
  ```
  Expected: `notAfter` date is in future (>30 days)

- [ ] **12. Secrets configured**
  ```bash
  # Check environment variables set
  env | grep -E "(JWT_SECRET|DATABASE_URL|OLLAMA)"
  ```
  Expected: All critical secrets set

### Notification & Approval

- [ ] **13. Team notified of deployment**
  - Post in #deia-deployment channel
  - Expected: Acknowledgment from team lead

- [ ] **14. Change ticket created** (if required)
  - Document changes
  - Link to deployment plan

- [ ] **15. Approval obtained**
  - Get sign-off from production owner
  - Expected: Slack approval reaction or email

---

## Deployment Sequence

**Estimated time: 10-15 minutes**

### Phase 1: Graceful Shutdown (2-3 minutes)

**Goal:** Stop old version without dropping active connections

**Step 1.1: Enter maintenance mode**
```bash
# Create maintenance flag (causes /api endpoints to return 503)
touch /var/lib/deia/MAINTENANCE_MODE

# Notify users
# UI should show "System undergoing maintenance" message
```

**Step 1.2: Stop accepting new connections (wait for existing to drain)**
```bash
# Wait for active connections to drain
# Expected: Current connections decrease over 60-120 seconds

# Check connection status every 10 seconds
watch -n 10 'curl -s http://localhost:8000/health | jq ".active_connections"'

# When active connections <5, proceed to next step
```

**Step 1.3: Stop application gracefully**
```bash
# Send SIGTERM to allow graceful shutdown
sudo systemctl stop deia-bot-controller

# Verify it stopped (wait max 30 seconds)
sleep 5 && systemctl status deia-bot-controller
# Expected: inactive (dead)
```

### Phase 2: Code Deployment (3-5 minutes)

**Goal:** Deploy new code version

**Step 2.1: Pull latest code**
```bash
cd ~/app
git pull origin main
# Expected: "Already up to date" or list of changes
```

**Step 2.2: Install dependencies**
```bash
npm install --production
# Expected: "added X packages" or "up to date"
```

**Step 2.3: Run database migrations** (if needed)
```bash
npm run db:migrate
# Expected: "No pending migrations" or "Applied X migrations"
```

**Step 2.4: Build assets** (if needed)
```bash
npm run build
# Expected: Build completes without errors
```

### Phase 3: Health Verification (3-5 minutes)

**Goal:** Verify deployment succeeded before opening to traffic

**Step 3.1: Start application**
```bash
sudo systemctl start deia-bot-controller

# Wait for startup
sleep 10

# Check status
systemctl status deia-bot-controller
# Expected: active (running)
```

**Step 3.2: Verify health endpoint**
```bash
curl http://localhost:8000/health
# Expected: HTTP 200, JSON response with "status": "healthy"
```

**Step 3.3: Verify database connectivity**
```bash
curl http://localhost:8000/health/db
# Expected: HTTP 200, database latency <50ms
```

**Step 3.4: Verify application logs**
```bash
journalctl -u deia-bot-controller -f --tail=50
# Watch for 30 seconds, expect: no errors, successful startup messages
```

**Step 3.5: Run smoke test**
```bash
# Test bot launch endpoint
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id": "TEST-BOT-SMOKE"}'

# Expected: HTTP 200, bot launches successfully
```

### Phase 4: Exit Maintenance Mode (1 minute)

**Goal:** Resume normal operations

**Step 4.1: Remove maintenance flag**
```bash
rm /var/lib/deia/MAINTENANCE_MODE

# UI should automatically restore normal messaging
```

**Step 4.2: Verify production traffic**
```bash
# Check request rate
curl http://localhost:8000/metrics | grep http_requests_total

# Expected: Request count increasing (traffic flowing)
```

**Step 4.3: Verify monitoring shows healthy**
```bash
# Check Grafana dashboard
# Expected: All panels green, no alerts firing
```

---

## Post-Deployment Verification

**Complete within 5 minutes of deployment**

### Immediate Checks (1-2 minutes)

```bash
# Check application is running
systemctl status deia-bot-controller

# Check error rate is low (<0.5%)
curl http://localhost:8000/metrics | grep http_requests_total.*status=\"5\"

# Check response times normal
curl http://localhost:8000/metrics | grep http_request_duration_seconds

# Check database connections stable
psql -U deia -d deia_prod -c "SELECT count(*) FROM pg_stat_activity WHERE datname='deia_prod';"
```

### 5-Minute Checks

- [ ] **Dashboard shows green:** Grafana shows all metrics normal
- [ ] **No alerts firing:** Slack #deia-alerts quiet
- [ ] **User reports:** No deployment impact messages
- [ ] **Error logs clean:** No new error patterns

### 15-Minute Checks

- [ ] **Performance metrics:** Response times P95 <1.5s
- [ ] **Database queries:** Average query time <50ms
- [ ] **Memory usage:** Stable, not growing
- [ ] **Connections:** Distributed evenly, not exhausted

### 1-Hour Check

- [ ] **Stability:** System handling normal traffic
- [ ] **No memory leaks:** Memory usage stable
- [ ] **No connection leaks:** Connection pool stable
- [ ] **Error rate steady:** Consistent with baseline

---

## Rollback Procedures

**Use only if critical issues found post-deployment**

### Quick Rollback (if deployment code is the problem)

**Time to execute: 5-10 minutes**

**Step 1: Check git history**
```bash
cd ~/app
git log --oneline -10
# Find previous stable commit
```

**Step 2: Revert to previous version**
```bash
git reset --hard <previous_commit_hash>
# Example: git reset --hard f25daf9
```

**Step 3: Reinstall dependencies** (if changed)
```bash
npm install --production
```

**Step 4: Restart application**
```bash
sudo systemctl restart deia-bot-controller

# Wait and verify
sleep 5
curl http://localhost:8000/health
```

**Step 5: Verify rollback successful**
```bash
# Check error rate returned to normal
# Monitor for 2-3 minutes to confirm stability
```

### Database Rollback (if migrations caused problems)

**Time to execute: 5-15 minutes**

**Step 1: Restore from backup**
```bash
# Stop application first
sudo systemctl stop deia-bot-controller

# Restore database from recent backup
gunzip < deia_prod_backup_TIMESTAMP.sql.gz | psql -U deia deia_prod

# Verify restore
psql -U deia -d deia_prod -c "SELECT count(*) FROM chat_messages;"
```

**Step 2: Restart application**
```bash
sudo systemctl start deia-bot-controller
sleep 10
curl http://localhost:8000/health
```

**Step 3: Communicate status**
```bash
# Notify team: "Database rolled back to [timestamp], investigating migration issue"
```

---

## Deployment Decision Matrix

**Use this to decide: Deploy? Or Rollback?**

| Symptom | Action |
|---------|--------|
| Error rate >5% for >5 min | 🔴 ROLLBACK |
| Response time P95 >5 seconds | 🔴 ROLLBACK |
| Application crashes | 🔴 ROLLBACK |
| Database unreachable | 🔴 ROLLBACK |
| Memory leak (>100MB/min) | 🔴 ROLLBACK |
| Error rate 1-5% for <5 min | 🟡 INVESTIGATE (don't rollback yet) |
| Response time P95 2-5 seconds | 🟡 INVESTIGATE |
| Single error in logs | 🟢 OK (monitor, but don't rollback) |
| Memory usage increased 10% | 🟢 OK (expected, monitor) |

---

## Deployment Runbook Summary

```
START
  ↓
PRE-DEPLOYMENT CHECKLIST (15 items)
  ↓
PHASE 1: GRACEFUL SHUTDOWN (2-3 min)
  - Enter maintenance mode
  - Wait for connections to drain
  - Stop application
  ↓
PHASE 2: CODE DEPLOYMENT (3-5 min)
  - Pull latest code
  - Install dependencies
  - Run migrations
  - Build assets
  ↓
PHASE 3: HEALTH VERIFICATION (3-5 min)
  - Start application
  - Verify health endpoints
  - Check database connectivity
  - Verify logs clean
  - Run smoke test
  ↓
PHASE 4: EXIT MAINTENANCE (1 min)
  - Remove maintenance flag
  - Verify traffic flowing
  - Verify monitoring healthy
  ↓
POST-DEPLOYMENT VERIFICATION
  - Immediate checks (1-2 min)
  - 5-minute checks
  - 15-minute checks
  - 1-hour check
  ↓
IF CRITICAL ISSUE FOUND
  - Check decision matrix
  - Execute rollback (5-15 min)
  - Communicate status
  ↓
END
```

**Total deployment time: 15-30 minutes**
**Rollback time: 5-15 minutes**

---

## Communication Template

**Post to #deia-deployment when deployment begins:**

```
🚀 DEPLOYMENT STARTED

Time: 2025-10-25 21:00 CDT
Version: [commit hash]
Changes: [summary of changes]
Estimated duration: 15-30 minutes

Status: MAINTENANCE MODE - System temporarily unavailable

Expected back online: 21:15-21:30 CDT
```

**Post when deployment complete:**

```
✅ DEPLOYMENT COMPLETE

Time: 2025-10-25 21:12 CDT
Status: HEALTHY - All checks passing
Error rate: <0.5%
Response time P95: 1.2s

System is back online. No user action needed.
```

**If rollback needed:**

```
🔄 DEPLOYMENT ROLLED BACK

Time: 2025-10-25 21:08 CDT
Reason: [specific issue]
Previous version restored: [commit hash]
Status: HEALTHY

Investigating issue. Will reschedule deployment after fix verified.
```

---

## Post-Deployment Monitoring

**Recommended monitoring schedule for 24 hours post-deployment:**

| Time | Check |
|------|-------|
| T+5 min | Error rate, response times, application logs |
| T+15 min | Database performance, connection pool |
| T+30 min | Memory usage trend, CPU usage |
| T+1 hour | Full metrics review, user feedback |
| T+4 hours | Overnight stability check |
| T+8 hours | Full day trend analysis |
| T+24 hours | Performance vs baseline comparison |

---

**Deployment Procedures Ready:** ✅
**Date:** 2025-10-25
**Next Step:** Incident Response Playbooks
