# DEIA Health Check & Monitoring Guide

**Version:** 1.0
**Last Updated:** 2025-10-25
**Status:** Production Ready

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Health Check Endpoints](#health-check-endpoints)
3. [Monitoring Components](#monitoring-components)
4. [Alert System](#alert-system)
5. [Health Baseline](#health-baseline)
6. [Degradation Modes](#degradation-modes)
7. [Recovery Procedures](#recovery-procedures)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## Quick Start

### Check System Health

```bash
# Quick health check
curl http://localhost:8001/health

# Detailed status
curl http://localhost:8001/status

# Dashboard view (all metrics)
curl http://localhost:8001/api/dashboard/health
```

### Expected Responses

All endpoints should respond within 100ms with HTTP 200:

```json
{
  "status": "ok",
  "bot_id": "deiasolutions-CLAUDE-CODE-001",
  "timestamp": "2025-10-25T16:25:00Z"
}
```

---

## Health Check Endpoints

### 1. Basic Health Check
**Endpoint:** `GET /health`
**Response Time:** <5ms
**Frequency:** Check every 30 seconds

```bash
curl -i http://localhost:8001/health
```

**Response:**
```json
{
  "status": "ok",
  "bot_id": "deiasolutions-CLAUDE-CODE-001",
  "timestamp": "2025-10-25T16:25:00Z"
}
```

**Interpretation:**
- `status: ok` - Service responding
- Status code 200 - Service healthy

### 2. Detailed Status Check
**Endpoint:** `GET /status`
**Response Time:** <10ms
**Frequency:** Check every 30 seconds

```bash
curl -i http://localhost:8001/status
```

**Response:**
```json
{
  "bot_id": "deiasolutions-CLAUDE-CODE-001",
  "status": "working|idle|paused",
  "current_task": "task-id or null",
  "port": 8001,
  "pid": 12345,
  "timestamp": "2025-10-25T16:25:00Z"
}
```

**Status Meanings:**
- `working` - Bot actively executing a task
- `idle` - Bot waiting for tasks
- `paused` - Bot paused (interrupt requested)

### 3. Health Dashboard
**Endpoint:** `GET /api/dashboard/health`
**Response Time:** <20ms
**Frequency:** Check every 60 seconds

```bash
curl -i http://localhost:8001/api/dashboard/health
```

**Response:**
```json
{
  "timestamp": "2025-10-25T16:25:00Z",
  "system": {
    "cpu_percent": 0.45,
    "memory_percent": 0.62,
    "status": "healthy"
  },
  "bots": {
    "total": 3,
    "healthy": 3,
    "unhealthy": 0,
    "avg_load": 0.55
  },
  "queue": {
    "depth": 5,
    "avg_wait_time_ms": 2.1,
    "status": "healthy"
  },
  "services": {
    "messaging": "ok",
    "scheduling": "ok",
    "orchestration": "ok",
    "audit": "ok"
  },
  "alerts": {
    "active": 0,
    "critical": 0,
    "warnings": 0
  }
}
```

**Key Metrics:**
- `cpu_percent` - System CPU usage (0-1, warn at 0.80, critical at 0.95)
- `memory_percent` - System memory usage (0-1, warn at 0.75, critical at 0.90)
- `queue_depth` - Tasks waiting to be executed
- `bot_healthy` - Count of healthy bots
- `alerts.active` - Number of active alerts

---

## Monitoring Components

### 1. Bot Health Monitor
**Service:** `bot_health_monitor.py`
**Interval:** Every 30 seconds
**Data Logged To:** `.deia/bot-logs/BOT-{id}-health.jsonl`

**Monitors:**
- Process status (running/crashed)
- CPU usage per bot
- Memory usage per bot
- Task completion rate
- Error rate

**Alert Triggers:**
- CPU > 95%
- Memory > 90%
- Task failure rate > 30%
- No updates in 2 minutes (bot stuck)

### 2. Resource Monitor
**Service:** `bot_resource_monitor.py`
**Interval:** Every 60 seconds
**Data Logged To:** `.deia/bot-logs/BOT-{id}-resources.jsonl`

**Monitors:**
- CPU usage (per-core)
- Memory usage (RSS, VSS, shared)
- File descriptors (open files)
- Network connections
- Disk I/O

**Alert Triggers:**
- CPU spike >80%
- Memory spike >75%
- File descriptor exhaustion >900/1024
- Disk I/O high (>50% queue depth)

### 3. API Health Monitor
**Service:** `api_health_monitor.py`
**Interval:** Every 30 seconds
**Data Logged To:** `.deia/bot-logs/api-health.jsonl`

**Monitors:**
- Endpoint response times
- HTTP error rates
- Request throughput
- API availability

**Alert Triggers:**
- Endpoint response time > 1 second
- HTTP 5xx errors > 5%
- API unavailable (3 failed checks)

### 4. Process Monitor
**Service:** `bot_process_monitor.py`
**Interval:** Every 30 seconds
**Data Logged To:** `.deia/bot-logs/process-monitor.jsonl`

**Monitors:**
- Process state (running/zombie/defunct)
- File descriptor leaks
- Memory leaks (growth trend)
- Hanging processes (stuck in system call)

**Alert Triggers:**
- Process state abnormal
- Memory growth >100MB/hour (leak detected)
- Hanging process >5 minutes

### 5. Task Queue Monitor
**Monitored By:** Health Monitor aggregator
**Data Logged To:** `.deia/bot-logs/queue-monitor.jsonl`

**Monitors:**
- Queue depth
- Task wait times
- Task completion times
- Task failure rate

**Alert Triggers:**
- Queue depth > 10 tasks
- Task wait time > 5 minutes
- Task failure rate > 30%

---

## Alert System

### Alert Levels

| Level | Severity | Response Time | Action |
|-------|----------|---------------|--------|
| CRITICAL | P0 | Immediate | Page on-call engineer |
| WARNING | P1 | 15 minutes | Log and notify team |
| INFO | P2 | 1 hour | Log for review |

### Alert Examples

**CRITICAL Alert:**
```json
{
  "timestamp": "2025-10-25T16:25:00Z",
  "level": "CRITICAL",
  "source": "bot_resource_monitor",
  "message": "CPU usage critical: 95%",
  "bot_id": "bot-001",
  "current_value": 0.95,
  "threshold": 0.95
}
```

**WARNING Alert:**
```json
{
  "timestamp": "2025-10-25T16:25:00Z",
  "level": "WARNING",
  "source": "bot_resource_monitor",
  "message": "Memory usage warning: 75%",
  "bot_id": "bot-001",
  "current_value": 0.75,
  "threshold": 0.75
}
```

### Alert Configuration

Alerts are configured in `bot-config.yaml`:

```yaml
thresholds:
  cpu_warning_percent: 0.80
  cpu_critical_percent: 0.95
  memory_warning_percent: 0.75
  memory_critical_percent: 0.90
  queue_backlog_threshold: 10
  bot_failure_threshold: 0.30
  message_failure_threshold: 5
```

To modify alerts:
1. Edit `bot-config.yaml`
2. System reloads within 5 minutes
3. New thresholds take effect immediately

---

## Health Baseline

### Healthy System Metrics

**System-wide Baseline (idle):**

| Metric | Value | Status |
|--------|-------|--------|
| CPU Usage | 5-15% | ✅ OK |
| Memory Usage | 30-40% | ✅ OK |
| Queue Depth | 0-2 tasks | ✅ OK |
| Bot Count | 1-2 running | ✅ OK |
| Task Latency | 3-5ms | ✅ OK |
| Message Latency | 1-2ms | ✅ OK |
| Health Check Response | <5ms | ✅ OK |
| API Response | <20ms | ✅ OK |
| Task Success Rate | >99% | ✅ OK |
| Service Availability | 100% | ✅ OK |

**Healthy System Metrics (normal load):**

| Metric | Value | Status |
|--------|-------|--------|
| CPU Usage | 40-60% | ✅ OK |
| Memory Usage | 50-65% | ✅ OK |
| Queue Depth | 5-15 tasks | ✅ OK |
| Bot Count | 2-4 running | ✅ OK |
| Task Latency | 5-10ms | ✅ OK |
| Message Latency | 2-4ms | ✅ OK |
| Health Check Response | <5ms | ✅ OK |
| API Response | <20ms | ✅ OK |
| Task Success Rate | >95% | ✅ OK |
| Service Availability | >99.9% | ✅ OK |

**Healthy System Metrics (high load):**

| Metric | Value | Status |
|--------|-------|--------|
| CPU Usage | 70-85% | ✅ OK |
| Memory Usage | 70-80% | ✅ OK |
| Queue Depth | 20-50 tasks | ✅ OK |
| Bot Count | 5-10 running | ✅ OK |
| Task Latency | 15-30ms | ✅ OK |
| Message Latency | 5-10ms | ✅ OK |
| Health Check Response | <10ms | ✅ OK |
| API Response | <50ms | ✅ OK |
| Task Success Rate | >90% | ✅ OK |
| Service Availability | >99% | ✅ OK |

**Degraded System Metrics (should trigger alerts):**

| Metric | Value | Status |
|--------|-------|--------|
| CPU Usage | >95% | ⚠️ CRITICAL |
| Memory Usage | >90% | ⚠️ CRITICAL |
| Queue Depth | >100 tasks | ⚠️ WARNING |
| Bot Health | <50% healthy | ⚠️ CRITICAL |
| Task Success Rate | <70% | ⚠️ CRITICAL |
| Service Availability | <99% | ⚠️ WARNING |

---

## Degradation Modes

### Graceful Degradation
When system resources constrained, system degrades gracefully:

**Level 1 - High CPU (>80%)**
- Reduce scaling-up frequency (wait longer to add bots)
- Disable feature flags: `adaptive_scheduling_enabled`
- Continue: Task execution, messaging, health monitoring

**Level 2 - Critical CPU (>95%)**
- Stop accepting new tasks
- Disable: `request_validation_enabled`, `audit_logging_enabled`
- Continue: Existing task execution only

**Level 3 - Memory Pressure (>90%)**
- Clear task history cache
- Disable: `health_monitoring_enabled`
- Stop: New task acceptance
- Continue: Executing in-flight tasks only

**Level 4 - Total System Failure**
- Stop all bot execution
- Preserve state to `.deia/state/crash-dump.json`
- Enable read-only mode (no new tasks, messages, or changes)

### Recovery from Degradation

Once resources available:
1. **Level 4→3:** Restore state from crash dump, verify integrity
2. **Level 3→2:** Re-enable memory-intensive features
3. **Level 2→1:** Resume normal task acceptance
4. **Level 1→OK:** Resume adaptive scheduling, scaling adjustments

Recovery is automatic. Time to full recovery: 2-5 minutes depending on extent of degradation.

---

## Recovery Procedures

### Automatic Recovery

System automatically detects and recovers from:
- **Bot crashes:** Auto-restart within 30 seconds
- **Task failures:** Retry with exponential backoff
- **Transient network errors:** Automatic reconnect
- **Resource pressure:** Graceful degradation + recovery
- **Monitoring failures:** Fallback to basic health checks

### Manual Recovery

If automatic recovery fails:

#### 1. Restart Single Bot
```bash
# Kill a specific bot
pkill -f "python run_single_bot.py.*bot-001"

# System will auto-restart (or manually start)
python run_single_bot.py --bot-id bot-001 --port 8001
```

#### 2. Restart All Bots
```bash
# Kill all bots
pkill -f "python run_single_bot.py"

# Restart main bot
python run_single_bot.py --bot-id main-bot --port 8001
```

#### 3. Full System Restart
```bash
# Stop system
pkill -f "python run_single_bot.py"

# Check state files
ls -la .deia/state/

# Restore from backup if needed
tar -xzf .deia/backups/state-{timestamp}.tar.gz -C .deia/

# Restart
python run_single_bot.py --bot-id main-bot --port 8001
```

#### 4. Clear Stuck Tasks
If queue has stuck tasks not executing:

```bash
# View queue
ls -la .deia/bot-logs/task-queue*.jsonl

# Clear queue (DANGER - loses tasks)
rm .deia/bot-logs/task-queue*.jsonl

# Restart
python run_single_bot.py --bot-id main-bot --port 8001
```

---

## Troubleshooting

### Health Check Returns Error

**Symptom:** `curl http://localhost:8001/health` returns error or timeout

**Steps:**
1. Check if service running: `ps aux | grep "python run_single_bot"`
2. Check port in use: `lsof -i :8001`
3. Check logs: `tail -f .deia/bot-logs/system.jsonl`
4. Restart service: `python run_single_bot.py --bot-id main-bot --port 8001`

### High CPU Usage

**Symptom:** CPU usage consistently >80%

**Steps:**
1. Check which service: `ps aux | sort -k3 -rn | head -5`
2. Check task queue: `curl http://localhost:8001/api/orchestrate/status | grep queue`
3. Check configuration: Reduce `max_bots` in bot-config.yaml
4. Monitor: `top -p $(pgrep -f python | head -5)`

### High Memory Usage

**Symptom:** Memory usage >80%

**Steps:**
1. Check memory trend: `tail -f .deia/bot-logs/BOT-*-resources.jsonl | grep memory`
2. Check for leaks: Look for steady growth over time
3. Restart bot: `pkill -f "python run_single_bot.py" && python run_single_bot.py --bot-id main-bot --port 8001`
4. Monitor: `watch -n 5 'free -h'`

### Alerts Not Triggering

**Symptom:** Metrics bad but no alerts

**Steps:**
1. Verify alerts enabled: Check `alert_enabled: true` in bot-config.yaml
2. Check thresholds: `cat bot-config.yaml | grep -A 10 thresholds`
3. Check alert logs: `tail -f .deia/bot-logs/alerts.jsonl`
4. Force alert: Manually set value above threshold in test

### Tasks Not Processing

**Symptom:** Queue depth increasing, tasks not executing

**Steps:**
1. Check bot status: `curl http://localhost:8001/status`
2. Check bot health: `curl http://localhost:8001/api/dashboard/health`
3. Check queue: `ls -la .deia/bot-logs/task-queue*.jsonl | wc -l`
4. Check errors: `tail -f .deia/bot-logs/BOT-*-errors.jsonl`
5. Restart bots: `pkill -f "python run_single_bot.py" && python run_single_bot.py --bot-id main-bot --port 8001`

---

## Best Practices

1. **Monitor continuously:** Check health dashboard every hour
2. **Act on warnings:** Don't ignore WARNING level alerts
3. **Baseline regularly:** Establish normal metrics for your workload
4. **Test recovery:** Regularly test failure scenarios (kill process, restart, verify recovery)
5. **Log analysis:** Review logs weekly for patterns or issues
6. **Alerting integration:** Integrate with your alerting system (PagerDuty, Slack, etc.)
7. **Capacity planning:** Monitor trends to predict when you need more resources
8. **Keep backups:** Test backup/restore procedures monthly

---

## Success Criteria

System is healthy when:

- ✅ Health check responds <5ms
- ✅ CPU usage <80% (or <95% critical)
- ✅ Memory usage <75% (or <90% critical)
- ✅ Queue depth <10 tasks
- ✅ Task success rate >95%
- ✅ No CRITICAL alerts active
- ✅ All services responding
- ✅ No memory leaks detected (stable over time)
- ✅ Auto-recovery working (verified in logs)
- ✅ Backups created and tested

---

**Status:** ✅ PRODUCTION READY

**Last Verified:** 2025-10-25 16:25 CDT
**Verified By:** BOT-001 (Infrastructure Lead)

For more information, see TROUBLESHOOTING.md or contact the on-call engineer.
