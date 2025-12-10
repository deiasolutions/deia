# DEIA Bot Controller - Operations & Monitoring Guide

**Version:** 1.0
**Last Updated:** 2025-10-25
**Target Audience:** Operations, SRE, DevOps Engineers
**Operational Level:** Production, 24/7 Support

---

## Table of Contents

1. Operations Overview
2. Monitoring Setup (Prometheus & Grafana)
3. Alert Configuration
4. Incident Response Runbooks
5. Maintenance Procedures
6. Performance Tuning
7. Capacity Planning
8. Troubleshooting Guide

---

## Operations Overview

### Operational Model

```
24/7 Operational Support
├── Primary On-Call (8 hours)
├── Secondary On-Call (8 hours)
├── DevOps Lead (4 hours overlap)
└── After-Hours Escalation (manager, principal engineer)

Escalation Timeline:
1. On-Call (5-15 min response)
2. Secondary On-Call (10-20 min response)
3. DevOps Lead (15-30 min response)
4. Management Escalation (30+ min response)
```

### Key Metrics Dashboard

**Primary Metrics to Monitor:**
```
1. Service Availability       (Target: 99.5%)
2. API Response Time          (Target: <200ms p95)
3. Bot Startup Time           (Target: <5 seconds)
4. Message Processing Latency (Target: <500ms p95)
5. Error Rate                 (Target: <0.5%)
6. Database Connections       (Threshold: >80 trigger warning)
7. Memory Usage               (Threshold: >85% trigger warning)
8. Disk Space                 (Threshold: <20% free trigger critical)
```

---

## Monitoring Setup

### Prometheus Configuration

**File:** `/etc/prometheus/prometheus.yml`

```yaml
# Prometheus global configuration
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    environment: 'production'
    service: 'deia-bot-controller'

# Alerting configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']

# Scrape configurations
scrape_configs:
  # Bot Controller Application
  - job_name: 'deia-bot-controller'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'
    scrape_interval: 10s
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance

  # PostgreSQL Database
  - job_name: 'postgresql'
    static_configs:
      - targets: ['localhost:5432']
    scrape_interval: 30s
    scrape_timeout: 10s

  # Redis Cache
  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:6379']
    scrape_interval: 30s

  # Node Exporter (System Metrics)
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
    scrape_interval: 30s

  # Nginx (if used as reverse proxy)
  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']
    scrape_interval: 30s
```

**Installation:**

```bash
# Install Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar -xzf prometheus-2.40.0.linux-amd64.tar.gz
sudo mv prometheus-2.40.0.linux-amd64 /opt/prometheus

# Create systemd service
sudo tee /etc/systemd/system/prometheus.service > /dev/null <<EOF
[Unit]
Description=Prometheus
After=network.target

[Service]
Type=simple
User=prometheus
WorkingDirectory=/opt/prometheus
ExecStart=/opt/prometheus/prometheus --config.file=/etc/prometheus/prometheus.yml
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl enable prometheus
sudo systemctl start prometheus
```

### Grafana Setup

**Installation:**

```bash
# Install Grafana
apt-get install -y software-properties-common
add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
apt-get update
apt-get install grafana-server

# Enable and start
systemctl enable grafana-server
systemctl start grafana-server
```

**Access:** http://localhost:3000 (default: admin/admin)

**Initial Setup:**

1. Login with default credentials
2. Add Prometheus data source: http://localhost:9090
3. Create dashboard boards (see below)
4. Configure alert notification channels (Slack, email, PagerDuty)

### Grafana Dashboards

**Dashboard 1: System Overview**

```
┌─────────────────────────────────────────────────────┐
│ DEIA Bot Controller - System Overview              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Uptime            Response Time       Error Rate  │
│  [99.7%]           [145ms]             [0.23%]    │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Request Rate                    Request Duration  │
│  [Graph: 150 req/sec]            [Graph: p50-p99]  │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Bot Instances     Memory Usage      CPU Usage     │
│  [5/10]            [1.2GB/2GB]        [45%]       │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Database Connections             Cache Hit Rate   │
│  [8/50]                            [92%]           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Key Metrics on System Overview Dashboard:**
- Uptime (green if >99.5%)
- Response time p95 (green if <200ms)
- Error rate (green if <0.5%)
- Request rate (requests per second)
- Bot instance count (current/max)
- Memory and CPU utilization
- Database connections
- Cache hit ratio

**Dashboard 2: Bot Performance**

```
Metrics:
├── Bot Startup Time (Distribution)
├── Message Processing Latency (p50, p95, p99)
├── Bot Status Distribution (Running/Stopped/Error)
├── Bot Activity Timeline (Messages per minute)
├── Error Rate by Bot ID
└── Resource Usage per Bot Instance
```

**Dashboard 3: Database Health**

```
Metrics:
├── Database Connection Pool Status
├── Query Execution Time (slow queries)
├── Transaction Rate
├── Replication Lag (if replicated)
├── Disk Space Usage
├── Index Statistics
└── Backup Status (last backup timestamp)
```

**Dashboard 4: Cache Performance**

```
Metrics:
├── Cache Hit/Miss Rate
├── Cache Eviction Rate
├── Cache Memory Usage
├── Key Count by Type
├── Command Latency
└── Connected Clients
```

---

## Alert Configuration

### Alert Rules

**File:** `/etc/prometheus/rules/alerts.yml`

```yaml
groups:
  - name: deia_alerts
    interval: 30s
    rules:

      # CRITICAL ALERTS
      - alert: ServiceDown
        expr: up{job="deia-bot-controller"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "DEIA Bot Controller Service is DOWN"
          description: "Service at {{ $labels.instance }} has been down for 1+ minute"
          runbook: "https://wiki.internal/runbook/service-down"

      - alert: DatabaseConnectionLost
        expr: db_connection_pool_active > db_connection_pool_max
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool exhausted"
          description: "Active connections ({{ $value }}) exceed max limit"

      - alert: DiskSpaceNearFull
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes) < 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk space critical (< 5% free)"
          description: "Free disk space: {{ humanize $value }}%"

      # WARNING ALERTS
      - alert: HighCPUUsage
        expr: rate(process_cpu_seconds_total[5m]) > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage has been >80% for 5 minutes"

      - alert: HighMemoryUsage
        expr: (process_resident_memory_bytes / 1024 / 1024) > 1500
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage: {{ humanize $value }}MB"

      - alert: HighErrorRate
        expr: (rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Error rate exceeds 1%"
          description: "Error rate: {{ humanize $value }}%"

      - alert: SlowAPIResponse
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "API response time is slow (p95 > 2s)"
          description: "p95 response time: {{ humanize $value }}ms"

      - alert: BotCrashDetected
        expr: increase(bot_start_errors_total[5m]) > 0
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Bot startup errors detected"
          description: "{{ $value }} bot startup failures in last 5 minutes"

      # INFO ALERTS (Low priority, for situational awareness)
      - alert: CacheHitRateLow
        expr: cache_hit_ratio < 0.7
        for: 30m
        labels:
          severity: info
        annotations:
          summary: "Cache hit rate below 70%"
          description: "Cache efficiency may be suboptimal"
```

### Alert Notification Setup

**Alertmanager Configuration**

**File:** `/etc/alertmanager/alertmanager.yml`

```yaml
global:
  slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
  pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'
  smtp_from: 'alerts@deia.example.com'
  smtp_smarthost: 'smtp.example.com:587'
  smtp_auth_username: 'alerts@deia.example.com'
  smtp_auth_password: 'PASSWORD'

route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  routes:
    # CRITICAL: PagerDuty + Slack
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      group_wait: 0s
      repeat_interval: 1h
      continue: true

    # WARNING: Slack + Email
    - match:
        severity: warning
      receiver: 'slack-warnings'
      group_wait: 30s
      repeat_interval: 4h

    # INFO: Slack only
    - match:
        severity: info
      receiver: 'slack-info'
      group_wait: 1m
      repeat_interval: 24h

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#deia-alerts'
        title: 'Alert: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: 'YOUR-PAGERDUTY-KEY'
        description: '{{ .GroupLabels.alertname }}'
    slack_configs:
      - channel: '#deia-critical'
        title: 'CRITICAL: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        color: 'danger'

  - name: 'slack-warnings'
    slack_configs:
      - channel: '#deia-warnings'
        title: 'WARNING: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        color: 'warning'

  - name: 'slack-info'
    slack_configs:
      - channel: '#deia-info'
        title: 'INFO: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        color: 'good'
```

---

## Incident Response Runbooks

### Runbook 1: Service Outage (Complete Down)

**Trigger:** `up{job="deia-bot-controller"} == 0` for 1+ minute

**Response Timeline:**

**Minute 0-1: Verification**
```bash
# Verify service is actually down
curl -v http://localhost:8000/health
# Expected: Connection refused or timeout

# Check service status
systemctl status deia-bot-controller

# Check logs for crash reasons
journalctl -u deia-bot-controller -n 50 | tail -20

# Check if port is in use
netstat -tlnp | grep 8000
```

**Minute 1-5: Quick Recovery**

```bash
# Option 1: Service crash (restart)
systemctl restart deia-bot-controller
sleep 3
curl http://localhost:8000/health

# Option 2: Port in use by stray process
lsof -i :8000
kill -9 <PID>
systemctl start deia-bot-controller

# Option 3: Out of memory
free -h
# If <100MB free: Restart service after freeing memory
ps aux | sort -k3,3nr | head -5  # Check top memory users
```

**Minute 5-10: If Still Down**

```bash
# Check if database is accessible
psql -U deia -d deia_prod -c "SELECT 1;"

# Check Ollama is running
curl http://localhost:11434/api/tags

# Check systemd journal for errors
journalctl -u deia-bot-controller -n 100 | grep -i error

# Check if dependencies are available
npm list
```

**Minute 10+: If Still Critical**

```bash
# Escalate to DevOps lead
# Prepare for container restart or rollback
# Execute rollback procedure (see deployment guide)
```

**Recovery Verification:**
```bash
# Health check
curl -v http://localhost:8000/health

# API connectivity
curl -X GET http://localhost:8000/api/bots

# Database connectivity
curl -v http://localhost:8000/health/db

# Check error logs
journalctl -u deia-bot-controller -f | grep -i error
# Should be empty or only minor issues
```

---

### Runbook 2: High Memory Usage

**Trigger:** Memory > 85% of available

**Response Timeline:**

**Minute 0-5: Diagnosis**

```bash
# Get current memory status
free -h
# Identify available memory and usage percentage

# Get memory by process
ps aux --sort=-%mem | head -10

# Check for memory leaks in bot processes
ps aux | grep "port 800[1-9]" | awk '{print $2}' | xargs -I {} \
  sh -c 'echo "PID {} Memory:" && pmap -x {} | tail -1'

# Check cache memory
redis-cli INFO memory
# Look for: used_memory_human and max_memory
```

**Minute 5-15: Recovery**

**Option 1: Cache is too large**
```bash
# Clear cache (WARNING: temporary performance impact)
redis-cli FLUSHDB
# Restart Redis
systemctl restart redis-server
```

**Option 2: Memory leak in application**
```bash
# Check for specific memory-consuming operations
journalctl -u deia-bot-controller --since "10 min ago" | \
  grep -i "memory\|allocation\|leak"

# Restart service to clear memory
systemctl restart deia-bot-controller

# Monitor memory trend
while true; do free -h | grep Mem; sleep 10; done
```

**Option 3: Too many bot instances**
```bash
# List running bots
curl http://localhost:8000/api/bots

# Stop least-used bots
curl -X POST http://localhost:8000/api/bot/BOT-ID/stop

# Verify memory drops
free -h
```

**Prevention for Future:**
```bash
# Set memory alert earlier (80% instead of 85%)
# Configure max_memory in Redis
redis-cli CONFIG SET maxmemory 256mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru

# Enable memory monitoring
redis-cli INFO memory | grep -E "used_memory|max_memory"
```

---

### Runbook 3: Database Connection Issues

**Trigger:** Connection errors, slow queries, connection pool exhaustion

**Response Timeline:**

**Minute 0-2: Diagnosis**

```bash
# Check database is running
systemctl status postgresql

# Check connection count
psql -U postgres -d postgres -c \
  "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"

# Check connection limits
psql -U postgres -d postgres -c \
  "SHOW max_connections;"

# Check for long-running queries
psql -U deia -d deia_prod -c \
  "SELECT query, now() - pg_stat_statements.query_start \
   FROM pg_stat_statements \
   WHERE query NOT LIKE '%pg_stat%' \
   ORDER BY query_start DESC LIMIT 10;"
```

**Minute 2-10: Recovery**

**Option 1: Connection pool exhausted**
```bash
# Kill idle connections
psql -U postgres -d postgres -c \
  "SELECT pg_terminate_backend(pid) FROM pg_stat_activity \
   WHERE datname = 'deia_prod' AND state = 'idle' \
   AND query_start < now() - interval '30 minutes';"

# Verify connections drop
psql -U postgres -d postgres -c \
  "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"
```

**Option 2: Slow query is blocking**
```bash
# Find slow query (>10 second)
psql -U deia -d deia_prod -c \
  "SELECT query, query_start FROM pg_stat_activity \
   WHERE query_start < now() - interval '10 seconds' \
   AND state = 'active';"

# Cancel slow query
psql -U postgres -d postgres -c \
  "SELECT pg_terminate_backend(pid) FROM pg_stat_activity \
   WHERE pid = <slow_query_pid>;"
```

**Option 3: Database is unresponsive**
```bash
# Restart PostgreSQL
systemctl restart postgresql
sleep 5

# Verify it's back up
psql -U deia -d deia_prod -c "SELECT 1;"

# Check for startup issues
journalctl -u postgresql -n 20
```

**Recovery Verification:**
```bash
# Health check
curl http://localhost:8000/health/db

# Verify connections are normal
psql -U postgres -d postgres -c \
  "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"

# Verify performance
time curl http://localhost:8000/api/bots
# Should be <200ms
```

---

### Runbook 4: High Error Rate

**Trigger:** Error rate > 1% for 5+ minutes

**Response Timeline:**

**Minute 0-5: Diagnosis**

```bash
# Check error patterns
curl -s http://localhost:9090/api/v1/query?query=\
'increase(http_requests_total{status=~"5.."}[5m])'

# Tail application logs for errors
journalctl -u deia-bot-controller -f | grep -i error

# Check specific error types
journalctl -u deia-bot-controller --since "10 min ago" | \
  grep -E "ERROR|Exception|Failed" | head -20

# Check database errors
psql -U deia -d deia_prod -c \
  "SELECT * FROM audit_logs WHERE action LIKE '%error%' \
   ORDER BY created_at DESC LIMIT 20;"
```

**Minute 5-10: Root Cause Analysis**

**Option 1: Database errors**
```bash
# Check database connectivity
psql -U deia -d deia_prod -c "SELECT 1;"

# Check database health
psql -U deia -d deia_prod -c "
  SELECT schemaname, tablename FROM pg_tables
  WHERE schemaname = 'public';" | wc -l
# Should list all tables (no errors)
```

**Option 2: OOM or resource exhaustion**
```bash
# Check memory
free -h

# Check disk space
df -h

# Check CPU
top -b -n 1 | head -20
```

**Option 3: Ollama service failing**
```bash
# Check Ollama
curl -v http://localhost:11434/api/tags

# Check if Ollama is handling load
ps aux | grep ollama
```

**Immediate Actions:**

```bash
# Increase error alert threshold temporarily (prevent alert fatigue)
# Contact Ollama team if inference is failing
# Stop accepting new bot launches if system is overloaded

# Gracefully degrade: Disable new bot launches
# (Update in app config: MAX_BOTS=0)

# Restart service if cascade is detected
systemctl restart deia-bot-controller
```

**Recovery Verification:**
```bash
# Monitor error rate
watch -n 5 'curl -s http://localhost:9090/api/v1/query?query=\
rate(http_requests_total{status=~"5.."}[5m]) | jq .data.result[0]'

# Should drop to <0.5% within 10 minutes
```

---

## Maintenance Procedures

### Daily Maintenance (5 min)

**Each Morning:**
```bash
# Check service health
systemctl status deia-bot-controller

# Check disk space
df -h /var

# Verify backups completed
ls -lh /var/backups/deia/db_*.sql.gz | head -1

# Check for error spikes
journalctl -u deia-bot-controller --since "24 hours ago" | \
  grep -i error | wc -l
# Should be <10 errors in 24 hours
```

### Weekly Maintenance (30 min)

**Every Monday Morning:**

```bash
# Database maintenance
psql -U deia -d deia_prod <<EOF
-- Vacuum and analyze
VACUUM ANALYZE;

-- Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index usage
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename;
EOF

# Redis memory optimization
redis-cli BGSAVE
redis-cli INFO memory

# Review alert patterns
# Check Grafana for trends in last week
# Export weekly metrics report
```

### Monthly Maintenance (2 hours)

**First Friday of Month:**

```bash
# Full backup verification
# Restore database from backup to test server
cd /tmp
pg_restore --data-only -d deia_test_restore \
  /var/backups/deia/db_latest.dump

# Verify all data is intact
psql -U deia -d deia_test_restore -c \
  "SELECT COUNT(*) as message_count FROM chat_messages;"

# Analyze performance metrics
# Generate monthly report
# Review and update runbooks
# Plan for next month capacity needs

# Clean up old logs (older than 30 days)
find /var/log/deia -name "*.log.*" -mtime +30 -delete

# Rotate old database backups
find /var/backups/deia -name "db_*.sql.gz" -mtime +30 -delete
```

---

## Performance Tuning

### Application Tuning

**Node.js Optimization:**
```bash
# Increase file descriptor limit
ulimit -n 65536

# Set environment variables for performance
export NODE_ENV=production
export NODE_OPTIONS="--max-old-space-size=2048"
# Add to systemd service ExecStart

# Enable compression
# (Add to Express: app.use(compression()))
```

**Express Configuration Tuning:**
```javascript
// app.js optimizations
const compression = require('compression');
const helmet = require('helmet');

app.use(compression());              // Gzip responses
app.use(helmet());                   // Security headers
app.set('trust proxy', 1);           // Trust X-Forwarded headers
app.set('x-powered-by', false);      // Don't advertise Express

// Connection pooling
const pool = new Pool({
  max: 20,                           // Max connections
  idleTimeoutMillis: 30000,          // Close idle after 30s
  connectionTimeoutMillis: 2000,     // Timeout for new connection
});
```

### Database Tuning

**PostgreSQL Configuration:**

```bash
# Edit postgresql.conf
sudo vi /etc/postgresql/12/main/postgresql.conf

# Key tuning parameters:
shared_buffers = 256MB              # 25% of RAM
effective_cache_size = 1GB          # 50-75% of RAM
maintenance_work_mem = 64MB         # Vacuum/analyze memory
work_mem = 16MB                     # Per-operation memory
random_page_cost = 1.1              # SSD-friendly
effective_io_concurrency = 200      # SSD capability

# Checkpoint tuning
checkpoint_completion_target = 0.9
wal_buffers = 16MB
max_wal_size = 4GB

# Apply changes
sudo systemctl restart postgresql
```

### Cache Tuning

**Redis Configuration:**

```bash
# Edit redis.conf
sudo vi /etc/redis/redis.conf

# Memory management
maxmemory 256mb
maxmemory-policy allkeys-lru        # Evict LRU when full

# Persistence (tune based on durability needs)
save ""                             # Disable RDB if not needed
appendonly yes                      # Enable AOF
appendfsync everysec                # Fsync every second (balance)

# Client handling
tcp-backlog 511
timeout 0
tcp-keepalive 300

# Apply changes
sudo systemctl restart redis-server
```

---

## Capacity Planning

### Current Capacity

```
Single Server Limits:
├── Concurrent Bots: 10 max
├── Total Request Rate: ~500 req/sec
├── Message Processing: ~200 messages/sec
├── Storage (6 months): ~50GB
├── Memory: 4GB (2GB available for app)
└── CPU: 4 cores (can handle 60% sustained)
```

### Growth Projection

**6 Months:**
```
Messages per day: 10,000 → 50,000
Active users: 5 → 20
Concurrent bots: 3 → 8
Storage needed: 25GB → 50GB
```

**Scaling Triggers:**

```
SCALE WHEN:
├── Concurrent bots > 8
├── Message rate > 300 msg/sec
├── CPU sustained > 70%
├── Memory usage > 3.5GB
└── Disk usage > 80%

SCALING OPTIONS:
├── Vertical: Upgrade to 8GB RAM, 8 cores
├── Horizontal: Add second server + load balancer
└── Hybrid: Both for high availability
```

---

## Troubleshooting Guide

### Common Issues & Solutions

**Issue: "Connection refused" on port 8000**

Diagnosis:
```bash
netstat -tlnp | grep 8000
# No output = service not running

lsof -i :8000
# Output = different process using port
```

Fix:
```bash
# Restart service
systemctl restart deia-bot-controller

# If port in use by different process
kill -9 <PID>
systemctl start deia-bot-controller
```

---

**Issue: "Database connection timeout"**

Diagnosis:
```bash
psql -U deia -d deia_prod -c "SELECT 1;" -v ON_ERROR_STOP=on
# Should return "1"

netstat -an | grep 5432
# Check if database port is open
```

Fix:
```bash
# Restart database
systemctl restart postgresql

# Check database is accepting connections
sudo -u postgres psql -c "SELECT version();"
```

---

**Issue: "Slow API responses (>1 second)"**

Diagnosis:
```bash
# Check slow log
journalctl -u deia-bot-controller -f | grep "took.*ms"

# Check database slow query log
tail -f /var/log/postgresql/postgresql.log | grep "duration:"
```

Fix:
```bash
# Add indexes if needed
psql -U deia -d deia_prod <<EOF
CREATE INDEX idx_bot_created ON chat_messages(bot_id, created_at DESC);
VACUUM ANALYZE;
EOF

# Clear cache and restart
redis-cli FLUSHDB
systemctl restart deia-bot-controller
```

---

## 24/7 Operations Checklist

### Daily (9 AM)
- [ ] Check service health (curl /health)
- [ ] Verify disk space (df -h)
- [ ] Check backup status
- [ ] Review error logs (last 24h)

### On-Call Shift (Every 4 hours)
- [ ] Verify all systems running
- [ ] Check alert status in Grafana
- [ ] Review recent deployments
- [ ] Check database connection count

### Weekly (Monday)
- [ ] Database maintenance (VACUUM, ANALYZE)
- [ ] Review performance trends
- [ ] Update runbooks if needed
- [ ] Capacity planning review

### Monthly (First Friday)
- [ ] Test backup restore
- [ ] Performance analysis
- [ ] Security review
- [ ] Plan next month

---

**Last Updated:** 2025-10-25
**Operations Status:** ✅ Production-Ready
