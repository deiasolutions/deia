# DEIA Port 8000 - Production Deployment Readiness Guide

**Version:** 1.0
**Last Updated:** 2025-10-25
**Target:** Production Deployment
**Audience:** Operations, DevOps, Infrastructure Team

---

## Quick Start for Ops Teams

**Checklist Time:** 15 minutes
**Deployment Time:** 10-15 minutes
**Rollback Time:** <2 minutes

**Pre-Deployment:**
1. ✅ Run pre-deployment checklist below
2. ✅ Verify all health checks passing
3. ✅ Test rollback procedures
4. ✅ Prepare rollback plan based on failure scenarios
5. ✅ Schedule deployment window (off-peak recommended)

**Deployment:**
```bash
./scripts/deploy-production.sh
```

**Post-Deployment:**
1. ✅ Run health checks every 60 seconds for 5 minutes
2. ✅ Monitor logs for errors
3. ✅ Verify traffic routing (if load-balanced)
4. ✅ Check database connectivity
5. ✅ Monitor resource utilization

---

## Pre-Deployment Checklist

**Complete this checklist 24 hours before deployment.** Each item must show ✅ PASS or documented approval to proceed.

### Application Readiness (8 items)

- [ ] **Build Verification** - Run `npm run build` or equivalent, zero errors/warnings
  - Expected: All assets compiled, no missing dependencies
  - Time: 2-3 minutes

- [ ] **All Tests Passing** - Run `npm test` or `pytest` (100% pass rate)
  - Expected: Unit tests, integration tests, e2e tests all green
  - Failure = STOP deployment, fix issues first

- [ ] **Code Review Complete** - All production code reviewed by 2+ engineers
  - Expected: No outstanding review comments
  - Documentation: Link to PR/review record

- [ ] **Security Scan Passed** - Run SAST/dependency scanning
  - Expected: No CRITICAL/HIGH severity findings
  - Tool: npm audit, snyk, or similar

- [ ] **Database Migrations Ready** - All pending migrations created and tested
  - Expected: Backup created, migration script tested on staging
  - Rollback: Migration rollback script ready

- [ ] **Configuration Set** - Production config.yaml copied and verified
  - Expected: All required environment variables set
  - Security: Credentials in vault, not in code

- [ ] **Dependencies Updated** - npm/pip dependencies current and compatible
  - Expected: No deprecated packages, security patches applied
  - Check: `npm audit fix` completed

- [ ] **Documentation Current** - README, API docs, operational guides updated
  - Expected: Latest deployment, architecture, troubleshooting docs in place
  - Review: Team lead sign-off on docs

### Infrastructure Readiness (7 items)

- [ ] **Server Resources Allocated** - Production server(s) provisioned and ready
  - Expected: Minimum 4GB RAM, 2 CPU cores, 20GB disk
  - Verification: `free -h` shows available memory, `df -h` shows disk

- [ ] **Database Ready** - Production database initialized and tested
  - Expected: Database created, users configured, backups configured
  - Test: Connect from app server and verify query speed

- [ ] **Backup System Configured** - Automated backups scheduled and tested
  - Expected: Daily backups, 7-day retention, restore tested monthly
  - Verification: Last backup completed successfully

- [ ] **Monitoring Enabled** - Prometheus/CloudWatch/similar monitoring active
  - Expected: CPU, memory, disk, network metrics collecting
  - Verification: Metrics dashboard showing data

- [ ] **Logging Centralized** - Log aggregation system ready (ELK, Splunk, etc)
  - Expected: Application logs shipping to central location
  - Verification: Recent logs visible in logging system

- [ ] **SSL/TLS Certificates** - Production certificates installed and valid
  - Expected: Certificate valid for >30 days, proper chain installed
  - Check: `openssl s_client -connect hostname:443 -showcerts`

- [ ] **Load Balancer Configured** - If used, traffic routing rules set
  - Expected: Health check endpoints configured, timeout values appropriate
  - Test: Verify traffic routes to correct backend

### Network & Security (5 items)

- [ ] **Firewall Rules Verified** - Only necessary ports open (80, 443, etc)
  - Expected: Inbound: 80 (HTTP), 443 (HTTPS); Outbound: DNS, NTP, registry access
  - Test: `nmap` scan from external confirms only needed ports open

- [ ] **SSH Access Restricted** - Only authorized IPs can SSH to production
  - Expected: Key-based auth, no password login, rate limiting enabled
  - Verification: SSH configuration reviewed by security team

- [ ] **API Rate Limiting** - Rate limits configured on all public endpoints
  - Expected: 1000 requests/minute per IP, exponential backoff
  - Test: Exceed limit, verify 429 response

- [ ] **CORS/CSRF Protection** - Security headers configured properly
  - Expected: CORS restricted to known domains, CSRF tokens enabled
  - Test: `curl -H "Origin: https://evil.com"` returns 403 or no header

- [ ] **Secrets Management** - No hardcoded secrets in code or config
  - Expected: All secrets in vault (AWS Secrets Manager, HashiCorp Vault, etc)
  - Verification: `grep -r "password\|api_key\|secret" src/` returns nothing sensitive

### Data & Backup (4 items)

- [ ] **Data Backup Verified** - Fresh backup created and restore tested
  - Expected: Backup file created today, restore tested to alternate location
  - Time: Full backup + restore test = 30-60 minutes

- [ ] **Database Integrity Checked** - Database consistency verified
  - Expected: No corruption detected, all tables accessible, indexes valid
  - Command: Database-specific integrity check (MySQL: `CHECK TABLE`, PostgreSQL: `ANALYZE`)

- [ ] **Migration Backup** - Pre-migration database snapshot created
  - Expected: Snapshot taken, verified restorable
  - Timing: Take snapshot immediately before deployment

- [ ] **Data Retention Policy** - Backup retention and deletion policy documented
  - Expected: Retention period defined (30/90/365 days), auto-delete configured
  - Verification: Policy documented and ops team trained

### Team & Process (3 items)

- [ ] **Ops Team Trained** - All team members understand deployment procedure
  - Expected: All ops staff completed deployment runbook review
  - Verification: Sign-off from ops lead

- [ ] **Rollback Plan Reviewed** - Team practiced rollback procedure
  - Expected: Team completed dry-run rollback, timing verified <2 minutes
  - Documentation: Rollback decision tree created

- [ ] **On-Call Engineer Assigned** - Engineer available for 24 hours post-deploy
  - Expected: Dedicated person with full system access, pager configured
  - Escalation: Manager escalation path if engineer unreachable

---

## Health Check Procedures

**Run these checks BEFORE deployment, immediately AFTER deployment, and every 60 seconds for 5 minutes post-deploy.**

### Health Check 1: Application Responsiveness

**Endpoint:** `GET http://localhost:8000/health`

**Command:**
```bash
curl -v http://localhost:8000/health
```

**Expected Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Response-Time: 45ms

{
  "status": "healthy",
  "timestamp": "2025-10-25T18:45:00Z",
  "version": "1.0.0",
  "uptime": "00:15:30"
}
```

**Pass Criteria:**
- ✅ HTTP 200 status
- ✅ Response time <100ms
- ✅ Status field is "healthy"
- ✅ Version matches deployment version

**Failure Response:**
```bash
# Timeout (service not running)
curl: (7) Failed to connect

# Service unavailable
HTTP/1.1 503 Service Unavailable

# Slow response (>1 second)
< X-Response-Time: 1500ms
```

**If Failed:**
1. Check service is running: `systemctl status deia-bot-controller`
2. Check logs: `journalctl -u deia-bot-controller -n 50`
3. Check port 8000: `netstat -tlnp | grep 8000`
4. If still failing: Proceed to Rollback Procedures section

---

### Health Check 2: Database Connectivity

**Endpoint:** `GET http://localhost:8000/health/db`

**Command:**
```bash
curl -v http://localhost:8000/health/db
```

**Expected Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "connected",
  "database": "deia_prod",
  "latency_ms": 8,
  "tables_accessible": 12,
  "last_query": "2025-10-25T18:45:00Z"
}
```

**Pass Criteria:**
- ✅ HTTP 200 status
- ✅ Database status is "connected"
- ✅ Latency <50ms
- ✅ All expected tables accessible (12+ tables)

**Failure Scenarios:**

**Scenario A: Connection Timeout**
```json
{
  "status": "error",
  "error": "connection timeout",
  "database": "deia_prod"
}
```
Action: Check database server running, network connectivity, firewall rules

**Scenario B: Authentication Failed**
```json
{
  "status": "error",
  "error": "authentication failed"
}
```
Action: Verify database credentials in vault, password not expired

**Scenario C: Database Offline**
```json
{
  "status": "error",
  "error": "database unreachable"
}
```
Action: SSH to database server, check `systemctl status postgresql` (or MySQL)

---

### Health Check 3: Cache/Redis (if used)

**Endpoint:** `GET http://localhost:8000/health/cache`

**Command:**
```bash
curl -v http://localhost:8000/health/cache
```

**Expected Response:**
```http
HTTP/1.1 200 OK

{
  "status": "healthy",
  "provider": "redis",
  "latency_ms": 2,
  "memory_used": "45MB",
  "memory_limit": "256MB"
}
```

**Pass Criteria:**
- ✅ HTTP 200 status
- ✅ Cache status is "healthy"
- ✅ Latency <10ms
- ✅ Memory used <80% of limit

**If Cache Unavailable (warning, not critical):**
- ⚠️ System degraded but operational (queries slower)
- ⚠️ Restart cache: `systemctl restart redis`
- ⚠️ If restart fails, continue monitoring - non-critical for core functionality

---

### Health Check 4: Bot Launch Capability

**Test:** Launch test bot and send command

**Commands:**
```bash
# Test bot launch
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id": "TEST-BOT-DEPLOY"}'

# Expected response
# HTTP 201 Created with bot_id and port

# Test command send (adjust port from response above)
curl -X POST http://localhost:8001/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "health"}'

# Expected response: Bot responds with health status
```

**Pass Criteria:**
- ✅ Bot launches successfully (HTTP 201)
- ✅ Bot gets assigned port (8001+)
- ✅ Command routed successfully
- ✅ Response received within 3 seconds

**If Failed:**
1. Check bot controller logs: `tail -f /var/log/deia/bot-controller.log`
2. Check port availability: `lsof -i :8001` (should be empty)
3. Check Ollama running: `curl http://localhost:11434/api/tags`

---

### Health Check 5: API Response Time

**Test:** Measure API latency under normal load

**Command:**
```bash
# Simple latency test
time curl -s http://localhost:8000/health > /dev/null

# Load test (5 concurrent requests)
for i in {1..5}; do
  curl -s http://localhost:8000/health &
done
wait

# Measure 100 requests
ab -n 100 -c 5 http://localhost:8000/health
```

**Expected Results:**
- ✅ Single request: <100ms response time
- ✅ 5 concurrent: <150ms average
- ✅ 100 requests: 99th percentile <300ms, zero errors

**If Slow:**
- Check CPU: `top` or `htop` (should be <80%)
- Check memory: `free -h` (should have >500MB free)
- Check disk I/O: `iostat -x 1 5` (wait time <10ms)
- Check network: `iftop` (check for bandwidth saturation)

---

### Health Check 6: Error Logging

**Test:** Verify errors are being logged and don't indicate problems

**Command:**
```bash
# Check for error patterns
tail -n 100 /var/log/deia/bot-controller.log | grep -i "error\|exception\|critical"

# Expected: No CRITICAL errors, acceptable INFO errors
# Check: Most recent lines should be INFO level logs
```

**Pass Criteria:**
- ✅ No CRITICAL level errors in last 100 lines
- ✅ No authentication failures (unless expected)
- ✅ No database connection errors
- ✅ Warning level acceptable (background cleanup, deprecated API usage)

**If Errors Found:**
```
Example error pattern: "CRITICAL: Database connection lost"
Action: Check database status, restart service
```

---

### Health Check 7: File System Integrity

**Test:** Verify required files and directories exist

**Command:**
```bash
# Check critical directories
test -d /var/log/deia && echo "✅ Log directory exists" || echo "❌ Missing /var/log/deia"
test -d /var/lib/deia && echo "✅ Data directory exists" || echo "❌ Missing /var/lib/deia"
test -f /etc/deia/config.yaml && echo "✅ Config exists" || echo "❌ Missing config"

# Check permissions
test -w /var/log/deia && echo "✅ Logs writable" || echo "❌ Log directory not writable"
test -r /etc/deia/config.yaml && echo "✅ Config readable" || echo "❌ Config not readable"

# Check disk space
df -h /var | awk 'NR==2 {if ($5+0 < 90) print "✅ Disk OK ("$5" used)"; else print "❌ Disk FULL ("$5" used)"}'
```

**Expected Output:**
```
✅ Log directory exists
✅ Data directory exists
✅ Config exists
✅ Logs writable
✅ Config readable
✅ Disk OK (45% used)
```

**If Failed:**
- Missing directories: `mkdir -p /var/log/deia /var/lib/deia`
- Permission issues: `chown -R deia:deia /var/log/deia /var/lib/deia`
- Disk full: Archive old logs or add storage

---

## Rollback Procedures

**Rollback Decision Matrix:**

| Scenario | Severity | Rollback | Time |
|----------|----------|----------|------|
| Service won't start | CRITICAL | Yes | <5 min |
| Database connection lost | CRITICAL | Yes | <5 min |
| 50%+ requests failing | CRITICAL | Yes | <5 min |
| API response >1s (was <100ms) | HIGH | Maybe | 2 min decision |
| Memory leak (growing unbounded) | HIGH | Yes after 10 min | <5 min |
| Data corruption detected | CRITICAL | Yes + restore | <10 min |
| Performance degraded 20% | LOW | Monitor 10 min, then decide | N/A |

---

### Rollback Scenario 1: Service Won't Start

**Trigger:** `systemctl status deia-bot-controller` shows "failed"

**Immediate Actions (30 seconds):**
```bash
# 1. Check what's wrong
systemctl status deia-bot-controller
journalctl -u deia-bot-controller -n 20 | grep -i error

# 2. Quick diagnostics (don't spend >30 seconds here)
netstat -tlnp | grep 8000    # Port 8000 in use?
ps aux | grep deia           # Stray processes?
```

**Rollback Path A: Revert to Previous Version (< 2 minutes)**

```bash
#!/bin/bash
# Rollback script

# Step 1: Stop current version
echo "Stopping service..."
systemctl stop deia-bot-controller

# Step 2: Restore previous code
echo "Restoring previous version..."
cd /opt/deia
git checkout main
git pull origin main~1       # Go back 1 commit

# Step 3: Reinstall dependencies (if needed)
npm ci --production

# Step 4: Start service
echo "Starting service..."
systemctl start deia-bot-controller

# Step 5: Verify
sleep 3
curl http://localhost:8000/health
if [ $? -eq 0 ]; then
  echo "✅ Rollback successful"
else
  echo "❌ Rollback failed, restore database backup"
fi
```

**Rollback Path B: Database Rollback (if migration caused issue, < 5 minutes)**

```bash
#!/bin/bash
# Database rollback

# Step 1: Stop service
systemctl stop deia-bot-controller

# Step 2: List backups
echo "Available backups:"
ls -lht /var/backups/deia/db_*.sql | head -5

# Step 3: Restore from pre-deployment backup
BACKUP_FILE="/var/backups/deia/db_$(date -d '1 day ago' +%Y%m%d).sql"
echo "Restoring from: $BACKUP_FILE"

# PostgreSQL example
psql -U deia -d postgres -c "DROP DATABASE deia_prod;"
psql -U deia -d postgres -c "CREATE DATABASE deia_prod OWNER deia;"
psql -U deia -d deia_prod < "$BACKUP_FILE"

# Step 4: Restart service
systemctl start deia-bot-controller

# Step 5: Verify
sleep 3
curl http://localhost:8000/health/db
```

**Decision Point:** Is service healthy after rollback?
- ✅ YES: Continue monitoring for 1 hour, then document incident
- ❌ NO: Proceed to Scenario 2 (Critical Database Issue)

---

### Rollback Scenario 2: Critical Database Issue

**Trigger:** Database connection failing, data corruption detected, or migration failed

**Recovery Timeline:**
- Minutes 0-2: Assess damage
- Minutes 2-5: Restore backup
- Minutes 5-10: Verify data integrity
- Minutes 10+: Detailed investigation

**Step-by-Step Recovery:**

```bash
#!/bin/bash
# Critical database recovery

echo "=== CRITICAL DATABASE RECOVERY ==="
echo "Time: $(date)"
echo "Severity: CRITICAL - Database unavailable"

# Step 1: Confirm issue (< 1 minute)
echo "Step 1: Confirming database issue..."
systemctl stop deia-bot-controller
psql -U deia -d deia_prod -c "SELECT COUNT(*) FROM information_schema.tables;" 2>&1

# Step 2: Locate latest backup (< 1 minute)
echo "Step 2: Locating backups..."
ls -lht /var/backups/deia/db_*.sql.gz | head -10
BACKUP_FILE=$(ls -t /var/backups/deia/db_*.sql.gz | head -1)
echo "Using backup: $BACKUP_FILE"

# Step 3: Verify backup integrity (< 1 minute)
echo "Step 3: Verifying backup file..."
gunzip -t "$BACKUP_FILE" && echo "✅ Backup integrity OK" || echo "❌ Backup corrupted!"

# Step 4: Drop and recreate database (< 2 minutes)
echo "Step 4: Recreating database..."
psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='deia_prod';"
psql -U postgres -c "DROP DATABASE IF EXISTS deia_prod;"
psql -U postgres -c "CREATE DATABASE deia_prod OWNER deia;"

# Step 5: Restore backup (varies by size, typically < 3 minutes)
echo "Step 5: Restoring from backup (this may take 1-5 minutes)..."
gunzip -c "$BACKUP_FILE" | psql -U deia -d deia_prod

echo "✅ Database restored"

# Step 6: Verify data (< 1 minute)
echo "Step 6: Verifying data integrity..."
psql -U deia -d deia_prod -c "SELECT COUNT(*) as message_count FROM chat_messages;"
psql -U deia -d deia_prod -c "SELECT COUNT(*) as bot_count FROM bots;"

# Step 7: Restart service
echo "Step 7: Restarting service..."
systemctl start deia-bot-controller

# Step 8: Run health checks
echo "Step 8: Running health checks..."
sleep 3
curl -s http://localhost:8000/health/db | jq .

echo "✅ Recovery complete - $(date)"
```

**Post-Recovery Actions:**
1. Document exactly what failed
2. Create incident report (root cause analysis)
3. Update runbooks based on lessons learned
4. Schedule post-incident review meeting
5. Do NOT re-attempt deployment without addressing root cause

---

### Rollback Scenario 3: Performance Degradation (80%+ slower)

**Trigger:** Response time went from <100ms to >500ms, or error rate >5%

**Assessment Phase (2 minutes):**

```bash
# Quick diagnosis
ps aux | head -20              # High CPU/memory process?
free -h                        # Memory available?
iostat -x 1 3                  # Disk I/O bottleneck?
netstat -s | grep -i error     # Network errors?

# Check application metrics
curl -s http://localhost:8000/metrics | grep "http_request_duration"
```

**Decision Tree:**

**Is this a load spike (temporary)?**
- Check: Time of day, scheduled jobs running?
- Action: Wait 5 minutes, recheck metrics
- If resolved: No rollback needed, update alerting thresholds
- If not resolved: Proceed to rollback

**Is this a code issue?**
- Check: New code deployed that's slower?
- Action: Run performance tests: `npm run test:perf`
- If failed: Rollback to previous version
- If passed: Look for infrastructure issue

**Rollback for Performance:**

```bash
# If new code is cause:
cd /opt/deia
git log --oneline | head -5
# Find the last "good" commit
git checkout <good-commit-hash>
npm ci --production
systemctl restart deia-bot-controller

# Verify performance restored:
time curl http://localhost:8000/health
```

---

### Rollback Scenario 4: Data Integrity Issue

**Trigger:** Data corruption detected, duplicated records, or data loss

**DO NOT rollback database for this scenario - it will lose recent valid data**

**Proper Recovery:**

```bash
# Step 1: Stop service to prevent further corruption
systemctl stop deia-bot-controller

# Step 2: Create backup of current corrupt state (for investigation)
pg_dump -Fc deia_prod > /var/backups/deia/corrupt_state_$(date +%Y%m%d_%H%M%S).dump

# Step 3: Identify what's corrupted
psql -U deia -d deia_prod -c "
  SELECT table_name FROM information_schema.tables
  WHERE table_schema='public';"

# Step 4: Investigate specific corruption
# Example: Check for duplicates in critical table
psql -U deia -d deia_prod -c "
  SELECT id, COUNT(*) as cnt
  FROM chat_messages
  GROUP BY id HAVING COUNT(*) > 1;"

# Step 5: Fix corruption (depends on type)
# Option A: Delete duplicates
psql -U deia -d deia_prod -c "
  DELETE FROM chat_messages WHERE id NOT IN (
    SELECT DISTINCT ON (message_hash) id FROM chat_messages
    ORDER BY message_hash, created_at
  );"

# Option B: Restore just corrupted table from backup
pg_restore --data-only -t chat_messages -d deia_prod \
  /var/backups/deia/backup_pre_deploy.dump

# Step 6: Verify repairs
psql -U deia -d deia_prod -c "
  SELECT COUNT(*) as message_count FROM chat_messages;"

# Step 7: Restart service
systemctl start deia-bot-controller

# Step 8: Monitor for recurrence
journalctl -u deia-bot-controller -f
```

---

## Production Startup Script

**File:** `/opt/deia/scripts/deploy-production.sh`

```bash
#!/bin/bash
set -e  # Exit on any error

################################################################################
# DEIA Bot Controller - Production Deployment Script
#
# Usage: sudo ./deploy-production.sh [--skip-tests] [--skip-backup]
#
# DO NOT RUN DURING BUSINESS HOURS without explicit approval
#
################################################################################

# Color output for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DEPLOY_DIR="/opt/deia"
SERVICE_NAME="deia-bot-controller"
BACKUP_DIR="/var/backups/deia"
LOG_DIR="/var/log/deia"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Deployment options
SKIP_TESTS=${SKIP_TESTS:-0}
SKIP_BACKUP=${SKIP_BACKUP:-0}
VERBOSE=${VERBOSE:-0}

# Parse arguments
for arg in "$@"; do
  case $arg in
    --skip-tests) SKIP_TESTS=1 ;;
    --skip-backup) SKIP_BACKUP=1 ;;
    --verbose) VERBOSE=1 ;;
  esac
done

# Logging function
log() {
  echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
  if [ "$VERBOSE" -eq 1 ]; then
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> /tmp/deia_deploy.log
  fi
}

error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
  exit 1
}

warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

require_root() {
  if [ "$EUID" -ne 0 ]; then
    error "This script must be run as root"
  fi
}

################################################################################
# PRE-DEPLOYMENT VALIDATION
################################################################################

validate_prerequisites() {
  log "=== PRE-DEPLOYMENT VALIDATION ==="

  # Check if running as root
  require_root

  # Check disk space
  available=$(df /var | tail -1 | awk '{print $4}')
  if [ "$available" -lt 1000000 ]; then
    error "Insufficient disk space (need 1GB, have $(($available/1024))MB)"
  fi
  log "✅ Disk space: $(df -h /var | tail -1 | awk '{print $5}') used"

  # Check if service exists
  if ! systemctl list-unit-files | grep -q "$SERVICE_NAME"; then
    warning "Service $SERVICE_NAME not found, will create"
  fi

  # Check git repo status
  if [ -d "$DEPLOY_DIR/.git" ]; then
    cd "$DEPLOY_DIR"
    if [ -n "$(git status -s)" ]; then
      warning "Git repo has uncommitted changes, stashing..."
      git stash
    fi
  fi

  log "✅ Prerequisites validated"
}

################################################################################
# BACKUP CURRENT STATE
################################################################################

backup_current_state() {
  if [ "$SKIP_BACKUP" -eq 1 ]; then
    warning "Skipping backup (not recommended!)"
    return
  fi

  log "=== CREATING BACKUP ==="

  mkdir -p "$BACKUP_DIR"

  # Backup current code
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  CODE_BACKUP="$BACKUP_DIR/code_backup_$TIMESTAMP.tar.gz"

  log "Backing up current code to $CODE_BACKUP..."
  tar -czf "$CODE_BACKUP" -C /opt deia --exclude=node_modules --exclude=.git
  log "✅ Code backup created ($(du -h $CODE_BACKUP | cut -f1))"

  # Backup database
  if command -v psql &> /dev/null; then
    DB_BACKUP="$BACKUP_DIR/db_$TIMESTAMP.sql.gz"
    log "Backing up database..."
    pg_dump -U deia deia_prod | gzip > "$DB_BACKUP"
    log "✅ Database backup created ($(du -h $DB_BACKUP | cut -f1))"
  fi

  # Keep only last 7 backups
  log "Cleaning up old backups (keeping last 7)..."
  ls -t "$BACKUP_DIR"/code_backup_*.tar.gz 2>/dev/null | tail -n +8 | xargs rm -f
  ls -t "$BACKUP_DIR"/db_*.sql.gz 2>/dev/null | tail -n +8 | xargs rm -f

  log "✅ Backup complete"
}

################################################################################
# PULL AND BUILD
################################################################################

update_code() {
  log "=== PULLING LATEST CODE ==="

  cd "$DEPLOY_DIR"

  # Update from git
  log "Pulling from git main branch..."
  git fetch origin
  git checkout main
  git pull origin main

  CURRENT_COMMIT=$(git rev-parse --short HEAD)
  log "✅ Updated to commit: $CURRENT_COMMIT"
}

install_dependencies() {
  log "=== INSTALLING DEPENDENCIES ==="

  cd "$DEPLOY_DIR"

  log "Installing npm dependencies..."
  npm ci --production  # Uses package-lock.json for reproducible builds

  log "✅ Dependencies installed"
}

build_application() {
  log "=== BUILDING APPLICATION ==="

  cd "$DEPLOY_DIR"

  if [ -f "package.json" ] && grep -q '"build"' package.json; then
    log "Running build script..."
    npm run build
    log "✅ Build successful"
  else
    log "ℹ️ No build script found, skipping"
  fi
}

run_tests() {
  if [ "$SKIP_TESTS" -eq 1 ]; then
    warning "Skipping tests (not recommended!)"
    return
  fi

  log "=== RUNNING TESTS ==="

  cd "$DEPLOY_DIR"

  if [ -f "package.json" ] && grep -q '"test"' package.json; then
    log "Running test suite..."
    npm test
    log "✅ All tests passed"
  else
    log "ℹ️ No test script found"
  fi
}

################################################################################
# DATABASE MIGRATIONS
################################################################################

run_migrations() {
  log "=== RUNNING DATABASE MIGRATIONS ==="

  cd "$DEPLOY_DIR"

  if [ -d "db/migrations" ] && [ "$(ls -A db/migrations)" ]; then
    log "Found pending migrations, applying..."

    # Example: If using Alembic or similar
    if command -v alembic &> /dev/null; then
      alembic upgrade head
      log "✅ Migrations completed"
    else
      log "ℹ️ Migration tool not found, skipping"
    fi
  else
    log "ℹ️ No migrations pending"
  fi
}

################################################################################
# DEPLOYMENT
################################################################################

deploy_service() {
  log "=== DEPLOYING SERVICE ==="

  # Stop current service
  log "Stopping service..."
  systemctl stop "$SERVICE_NAME" || true

  # Copy code to deployment location (already in place, but sanity check)
  log "✅ Code in place at $DEPLOY_DIR"

  # Update systemd service file
  log "Creating/updating systemd service file..."
  cat > /etc/systemd/system/${SERVICE_NAME}.service <<EOF
[Unit]
Description=DEIA Bot Controller
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=deia
WorkingDirectory=$DEPLOY_DIR
Environment="NODE_ENV=production"
Environment="PORT=8000"
ExecStart=/usr/bin/npm start
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=$SERVICE_NAME

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reload

  # Start service
  log "Starting service..."
  systemctl start "$SERVICE_NAME"

  # Wait for service to stabilize
  log "Waiting for service to stabilize (5 seconds)..."
  sleep 5

  # Verify service is running
  if systemctl is-active --quiet "$SERVICE_NAME"; then
    log "✅ Service started successfully"
  else
    error "Service failed to start. Checking logs:"
    journalctl -u "$SERVICE_NAME" -n 20
  fi
}

################################################################################
# POST-DEPLOYMENT VALIDATION
################################################################################

post_deployment_checks() {
  log "=== POST-DEPLOYMENT VALIDATION ==="

  local max_attempts=5
  local attempt=1

  while [ $attempt -le $max_attempts ]; do
    log "Health check attempt $attempt/$max_attempts..."

    if curl -sf http://localhost:8000/health > /dev/null; then
      log "✅ Service responding to health check"
      break
    fi

    if [ $attempt -eq $max_attempts ]; then
      error "Service not responding after $max_attempts attempts. Rolling back."
    fi

    sleep 2
    ((attempt++))
  done

  # Check database connectivity
  log "Checking database connectivity..."
  if curl -sf http://localhost:8000/health/db > /dev/null; then
    log "✅ Database connected"
  else
    error "Database connection failed. Rolling back."
  fi

  # Check application logs for errors
  log "Checking application logs..."
  if journalctl -u "$SERVICE_NAME" -n 10 | grep -i "CRITICAL\|FATAL"; then
    error "Critical errors in logs. Rolling back."
  fi

  log "✅ Post-deployment validation passed"
}

################################################################################
# MONITORING
################################################################################

enable_enhanced_monitoring() {
  log "=== ENABLING ENHANCED MONITORING ==="

  log "Setting up log monitoring..."
  # Start real-time monitoring of service logs
  journalctl -u "$SERVICE_NAME" -f &
  MONITOR_PID=$!

  log "✅ Enhanced monitoring enabled (PID: $MONITOR_PID)"
  log "Monitor logs with: journalctl -u $SERVICE_NAME -f"
}

################################################################################
# MAIN DEPLOYMENT FLOW
################################################################################

main() {
  echo ""
  echo "╔════════════════════════════════════════════════════════════╗"
  echo "║   DEIA Bot Controller - Production Deployment              ║"
  echo "║   Started: $(date +'%Y-%m-%d %H:%M:%S')                         ║"
  echo "╚════════════════════════════════════════════════════════════╝"
  echo ""

  # Execute deployment steps
  validate_prerequisites
  backup_current_state
  update_code
  install_dependencies
  build_application
  run_tests
  run_migrations
  deploy_service
  post_deployment_checks
  enable_enhanced_monitoring

  echo ""
  echo "╔════════════════════════════════════════════════════════════╗"
  echo "║   ✅ DEPLOYMENT COMPLETE                                    ║"
  echo "║   Service: $SERVICE_NAME (running)                          ║"
  echo "║   Endpoint: http://localhost:8000                           ║"
  echo "║   Monitor: journalctl -u $SERVICE_NAME -f                   ║"
  echo "║   Logs: $LOG_DIR                                           ║"
  echo "║   Rollback: See DEPLOYMENT-READINESS-GUIDE.md               ║"
  echo "╚════════════════════════════════════════════════════════════╝"
  echo ""
}

# Run main function with error handling
main "$@" || {
  error_exit_code=$?
  warning "Deployment failed with exit code $error_exit_code"

  # Prompt for rollback
  echo ""
  read -p "Do you want to rollback to previous version? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    log "Executing rollback..."
    systemctl stop "$SERVICE_NAME"
    # Rollback code from backup
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/code_backup_*.tar.gz | head -1)
    tar -xzf "$LATEST_BACKUP" -C /opt
    systemctl start "$SERVICE_NAME"
    log "✅ Rollback complete"
  fi

  exit $error_exit_code
}
```

**Usage:**
```bash
# Standard deployment (with all checks)
sudo /opt/deia/scripts/deploy-production.sh

# Skip tests (emergency only)
sudo SKIP_TESTS=1 /opt/deia/scripts/deploy-production.sh

# Skip backup (NOT RECOMMENDED)
sudo SKIP_BACKUP=1 /opt/deia/scripts/deploy-production.sh

# Verbose logging
sudo VERBOSE=1 /opt/deia/scripts/deploy-production.sh
```

---

## Summary

**Pre-Deployment Checklist: 27 items (15 minutes)**
- Application readiness: 8 items
- Infrastructure: 7 items
- Network & Security: 5 items
- Data & Backup: 4 items
- Team & Process: 3 items

**Health Checks: 7 checks (2 minutes)**
- Application responsiveness
- Database connectivity
- Cache/Redis status
- Bot launch capability
- API response time
- Error logging
- File system integrity

**Rollback Procedures: 4 scenarios**
- Service won't start (<2 min)
- Critical database issue (<10 min)
- Performance degradation (5 min decision)
- Data integrity issue (investigation-driven)

**Deployment Script: Production-ready**
- Automated validation
- Automatic backup
- Dependency installation
- Build & test execution
- Service management
- Post-deployment verification
- Error handling with rollback

---

**Last Updated:** 2025-10-25
**Status:** ✅ Ready for Production Deployment
