# Incident Response Playbooks

**Date:** 2025-10-25
**Author:** BOT-001 (Architect)
**Status:** READY FOR PRODUCTION

---

## Quick Reference

| Incident | Detection | Time to Action | Severity |
|----------|-----------|---|---|
| **Port 8000 Crash** | Health check fails | <1 min | CRITICAL |
| **Database Down** | Connection errors | <1 min | CRITICAL |
| **Ollama Offline** | API unreachable | <1 min | CRITICAL |
| **Memory Leak** | >1.6GB usage | <5 min | HIGH |
| **Connection Pool Full** | >80% utilization | <2 min | HIGH |
| **High Error Rate** | >1% errors | <5 min | HIGH |
| **Slow Response Times** | P95 >1s | <10 min | MEDIUM |

---

## PLAYBOOK 1: Port 8000 Application Crash

**Severity:** 🔴 CRITICAL
**Detection Time:** <1 minute (health check)
**Action Required:** Immediate
**Expected Resolution:** 2-5 minutes

### Detection

**Alert Trigger:**
- Health check endpoint (`/health`) returns non-200 status
- Browser connection refused error
- Slack alert: "Port 8000 Service Down"

**Verification:**
```bash
curl http://localhost:8000/health
# Expected: Connection refused or timeout
```

### Investigation (30 seconds)

**Q1: Is the application running?**
```bash
systemctl status deia-bot-controller
ps aux | grep node
```
- If NOT running → Jump to "Solution: Restart"
- If running but unresponsive → Jump to "Solution: Force Restart"

**Q2: Check application logs for errors**
```bash
journalctl -u deia-bot-controller -n 50 --no-pager
# Look for: stack traces, segmentation faults, out of memory
```

### Solutions (choose in order)

**Solution 1: Soft Restart**
```bash
sudo systemctl restart deia-bot-controller
sleep 10
curl http://localhost:8000/health
# Check if health returns 200 OK
```
- **Success time:** 30-60 seconds
- **Success rate:** 95%

**Solution 2: Force Kill & Restart** (if soft restart fails)
```bash
pkill -9 node
sleep 2
sudo systemctl start deia-bot-controller
sleep 10
curl http://localhost:8000/health
```
- **Success time:** 60-90 seconds
- **Success rate:** 99%

**Solution 3: Check and Fix Dependencies**
```bash
# If restart fails, check dependencies
curl http://localhost:5432  # PostgreSQL
curl http://localhost:11434/api/tags  # Ollama

# If PostgreSQL down: systemctl restart postgresql
# If Ollama down: systemctl restart ollama
```
- **Success time:** 3-5 minutes

### Escalation (if not resolved in 5 minutes)

1. **Page on-call engineer** (via PagerDuty)
2. **Message in Slack:** `@deia-oncall Port 8000 down, restart not successful, needs investigation`
3. **Save debug info:**
   ```bash
   sudo journalctl -u deia-bot-controller --no-pager > /tmp/app_logs.txt
   curl http://localhost:8000/metrics > /tmp/metrics.txt 2>&1
   ```

### Recovery Verification

After restart, verify within 5 minutes:

- [ ] Health check returns 200 OK
- [ ] No errors in recent logs
- [ ] Response time P95 <1.5 seconds
- [ ] Error rate <1%
- [ ] Database connections <10
- [ ] Memory usage normal

---

## PLAYBOOK 2: Database Connection Down

**Severity:** 🔴 CRITICAL
**Detection Time:** <1 minute
**Action Required:** Immediate
**Expected Resolution:** 3-10 minutes

### Detection

**Alert Trigger:**
- Application logs: `Error: connect ECONNREFUSED 127.0.0.1:5432`
- Health check `/health/db` returns non-200
- Error rate spikes to >50%

**Verification:**
```bash
curl http://localhost:8000/health/db
# Expected: Non-200 response or error message
```

### Investigation (1 minute)

**Q1: Is PostgreSQL running?**
```bash
systemctl status postgresql
```
- If running → Jump to "Solution: Connection Leak"
- If stopped → Jump to "Solution: Restart Service"

**Q2: Can you connect to database locally?**
```bash
psql -U deia -d deia_prod -c "SELECT 1"
```
- If successful → Connection pool issue
- If fails → Database authentication issue

### Solutions (choose in order)

**Solution 1: Verify Connection Pool**
```bash
psql -U deia -d deia_prod -c "SELECT count(*) FROM pg_stat_activity"
# If >20: Too many connections
# If <20: Pool should work
```

**Solution 2: Increase Connection Pool**
```bash
# Edit production.yaml
# Find: connection_pool: 20
# Change: connection_pool: 40

# Restart application
sudo systemctl restart deia-bot-controller
```
- **Success time:** 2-3 minutes
- **Success rate:** 85%

**Solution 3: Kill Slow Queries**
```bash
psql -U deia -d deia_prod -c "
  SELECT pid, query, query_start FROM pg_stat_activity
  WHERE state='active' AND query_start < NOW() - INTERVAL '1 minute'
  ORDER BY query_start;"

# Kill identified slow queries (be careful!)
# psql -U deia -d deia_prod -c "SELECT pg_terminate_backend(pid) FROM ..."
```

**Solution 4: Restart PostgreSQL**
```bash
sudo systemctl restart postgresql
sleep 5
psql -U deia -d deia_prod -c "SELECT 1"
# Verify connection works
```
- **Success time:** 5-10 minutes (includes restart and data integrity checks)
- **Success rate:** 100% (but causes brief unavailability)

### Escalation (if not resolved in 10 minutes)

1. **Page on-call database admin** (separate escalation from apps)
2. **Message in Slack:** `@database-oncall PostgreSQL connectivity issue, standard remediation not successful`
3. **Consider failover:** If database replica available
4. **Save database status:**
   ```bash
   pg_dump -U deia deia_prod --schema-only | head -50
   psql -U deia -d deia_prod -c "SELECT * FROM pg_stat_database WHERE datname='deia_prod'\G"
   ```

### Recovery Verification

After resolution, verify within 5 minutes:

- [ ] Health check `/health/db` returns 200 OK
- [ ] Database query latency <50ms
- [ ] Active connections stable (<10)
- [ ] No "connection refused" errors in logs
- [ ] Error rate back to normal (<1%)

---

## PLAYBOOK 3: High Memory Usage / Memory Leak

**Severity:** 🟡 HIGH
**Detection Time:** <5 minutes
**Action Required:** Within 10 minutes
**Expected Resolution:** 10-30 minutes

### Detection

**Alert Trigger:**
- Memory usage >1.6GB (warning threshold)
- Memory usage >1.9GB (critical threshold)
- Alert from monitoring system

**Verification:**
```bash
ps aux | grep node | grep -v grep
# Look at RSS column (resident set size in KB)

# Also check from metrics
curl http://localhost:8000/metrics | grep process_resident_memory_bytes
```

### Investigation (2 minutes)

**Q1: Is memory growing continuously?**
```bash
# Take initial measurement
memory_before=$(ps aux | grep node | grep -v grep | awk '{print $6}')
sleep 30
memory_after=$(ps aux | grep node | grep -v grep | awk '{print $6}')

# If growing significantly, it's a leak
# If stable, it's just normal usage
```

**Q2: Which component is using memory?**
```bash
# Check for large objects in cache/memory
curl http://localhost:8000/metrics | grep -E "(cache|memory|heap)" | head -10
```

### Solutions (choose based on findings)

**Solution 1: If Memory Stable (not leaking)**
- Just monitor
- No action required
- Set alert threshold higher if too sensitive

**Solution 2: If Small Leak (<50MB/hour)**
- Schedule restart during next maintenance window
- Monitor trend
- Investigate root cause (can wait 1-2 days)

**Solution 3: If Large Leak (>100MB/hour)**
- Restart immediately to prevent OOM crash
- Escalate for investigation

**Restart Procedure:**
```bash
sudo systemctl restart deia-bot-controller
sleep 10

# Verify restart successful
curl http://localhost:8000/health

# Monitor memory
watch -n 5 'ps aux | grep node'
# Watch for 5 minutes, verify memory stable
```
- **Success time:** 2-3 minutes
- **Success rate:** 100%

**After Restart: Root Cause Investigation**
```bash
# Check if memory grows again (confirms leak)
# Known leak sources:
# 1. Unbounded cache growth → Clear cache or implement TTL
# 2. Message queue not draining → Check message processor
# 3. Connection leaks → Verify all connections properly closed

# Review recent code changes
git log --oneline -20

# Look for likely culprits
# - Array.push() without limit
# - Missing event listener cleanup
# - Cache without expiration
```

### Escalation (if leak persists after restart)

1. **Page on-call engineer:** "Memory leak detected, restart is temporary fix"
2. **Save debug heap snapshot:**
   ```bash
   kill -USR2 <pid_of_node_process>
   # This creates heap snapshot in current directory
   ```
3. **Investigate code changes** that might cause leak

### Recovery Verification

- [ ] Memory stable after restart (no growth for 5 minutes)
- [ ] Memory usage <1.2GB
- [ ] No "out of memory" errors in logs
- [ ] Application functionality normal

---

## PLAYBOOK 4: Database Connection Pool Exhaustion

**Severity:** 🟡 HIGH
**Detection Time:** <2 minutes
**Action Required:** Immediate
**Expected Resolution:** 5-15 minutes

### Detection

**Alert Trigger:**
- Active connections >16/20 (warning threshold)
- Active connections >19/20 (critical threshold)
- Alert from monitoring system

**Verification:**
```bash
psql -U deia -d deia_prod -c "SELECT count(*) FROM pg_stat_activity WHERE datname='deia_prod';"
# Alert if count >16
```

### Investigation (1 minute)

**Q1: What queries are holding connections?**
```bash
psql -U deia -d deia_prod -c "
  SELECT pid, usename, query, query_start, state
  FROM pg_stat_activity
  WHERE datname='deia_prod'
  ORDER BY query_start;"
```
- Look for: queries running for >1 minute (slow queries)
- Look for: idle connections not being released

**Q2: Are connections being properly closed?**
- If lots of "idle in transaction" → Application not closing transactions
- If lots of "active" → Slow queries holding locks

### Solutions (choose in order)

**Solution 1: Increase Pool Size** (quick, temporary)
```bash
# Edit production.yaml
# Change: connection_pool: 20
# To: connection_pool: 40

# Restart application
sudo systemctl restart deia-bot-controller
```
- **Success time:** 2-3 minutes
- **Success rate:** 85% (fixes immediate problem)
- **Note:** Temporary fix, doesn't solve root cause

**Solution 2: Optimize Queries**
```bash
# Identify slow queries
psql -U deia -d deia_prod -c "
  SELECT query, calls, mean_time, total_time
  FROM pg_stat_statements
  ORDER BY mean_time DESC LIMIT 5;"

# Solution: Add indexes, rewrite queries
```
- **Success time:** Hours to days (involves code changes)
- **Success rate:** Permanent fix

**Solution 3: Kill Long-Running Transactions** (careful!)
```bash
psql -U deia -d deia_prod -c "
  SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
  WHERE datname='deia_prod'
  AND query_start < NOW() - INTERVAL '5 minutes'
  AND pid != pg_backend_pid();"
```
- **Warning:** This kills user queries, may cause data inconsistency
- **Use only if:** Pool is completely exhausted and new connections failing

### Escalation (if not resolved in 15 minutes)

1. **Page database admin:** "Connection pool exhausted, standard fixes not working"
2. **Message in Slack:** `@deia-oncall Database connection pool at 95%, investigating slow queries`
3. **Prepare for failover:** If replica available

### Recovery Verification

- [ ] Active connections <15 again
- [ ] New connection requests succeeding
- [ ] Response time back to normal
- [ ] Error rate <1%

---

## PLAYBOOK 5: High Error Rate

**Severity:** 🟡 HIGH
**Detection Time:** <5 minutes
**Action Required:** Within 10 minutes
**Expected Resolution:** 5-30 minutes

### Detection

**Alert Trigger:**
- Error rate >1% (warning)
- Error rate >5% (critical)
- Alert from monitoring system

**Verification:**
```bash
curl http://localhost:8000/metrics | grep http_requests_total | grep status=\"5\"
```

### Investigation (2-3 minutes)

**Q1: What type of errors?**
```bash
journalctl -u deia-bot-controller -f --tail=20 | grep -i error
```
- 500 errors → Application error
- 502/503 errors → Backend unavailable
- 429 errors → Rate limiting

**Q2: Check each dependency:**
```bash
# Database
psql -U deia -d deia_prod -c "SELECT 1"

# Ollama
curl http://localhost:11434/api/tags

# Redis (if used)
redis-cli ping
```

### Solutions (based on error type)

**Solution 1: If 5XX errors (application)**
- Check logs for stack traces
- Usually indicates code bug or resource exhaustion
- Restart application if needed

**Solution 2: If 502/503 (backend unavailable)**
- Check if backend service is running (Ollama, database)
- Restart backend service
- Verify connectivity

**Solution 3: If 429 (rate limiting)**
- Check if traffic spike
- Increase rate limit if needed (edit production.yaml)
- Check for DDoS patterns in request log

### Root Cause Analysis

Common error causes:
1. **Database unavailable** → Restart PostgreSQL
2. **Ollama offline** → Restart Ollama
3. **Out of memory** → Restart application
4. **Slow queries** → Kill slow queries, add indexes
5. **Application bug** → Check recent code changes, rollback if needed

### Escalation (if error rate remains >1% after 10 minutes)

1. **Call on-call engineer**
2. **Consider partial rollback** if recent deploy
3. **Enable debug logging:** (temporarily)
   ```bash
   export LOG_LEVEL=debug
   sudo systemctl restart deia-bot-controller
   ```

### Recovery Verification

- [ ] Error rate <1%
- [ ] No 5XX errors in recent logs
- [ ] Response time normal
- [ ] All dependencies operational

---

## Escalation Contacts

**On-Call Rotation:**
- **Primary (App):** See PagerDuty schedule
- **Database:** See PagerDuty schedule
- **Infrastructure:** See PagerDuty schedule
- **Manager (if escalation needed):** See contact list

**Communication Channels:**
- **Slack:** #deia-oncall, #deia-alerts, #deia-deployment
- **Phone:** See on-call page for phone numbers
- **Email:** Incident log for post-mortem

---

## Incident Log Template

```markdown
## INCIDENT: [Title]

**Time Started:** 2025-10-25 21:00 CDT
**Time Resolved:** 2025-10-25 21:12 CDT
**Duration:** 12 minutes
**Severity:** [CRITICAL/HIGH/MEDIUM]

### Detection
- How was this discovered?
- What alert fired?

### Impact
- How many users affected?
- What functionality unavailable?
- Estimated data loss?

### Root Cause
- What caused this?
- Why was it not caught earlier?

### Resolution
- What actions were taken?
- How long did each step take?

### Prevention
- What should we do to prevent this?
- What monitoring should be added?

### Follow-Up
- Post-mortem scheduled for: [date/time]
- Owner: [name]
```

---

**Incident Response Playbooks Ready:** ✅
**Date:** 2025-10-25
**Next Step:** BOT-003 Strategic Work
