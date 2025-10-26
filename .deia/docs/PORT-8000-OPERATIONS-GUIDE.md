# PORT 8000 Operations Guide

**Author:** BOT-001 (Infrastructure Lead)  
**Last Updated:** 2025-10-25 23:50 CDT  
**Target Audience:** DEIA Operations, SRE, DevOps, On-Call Engineers  
**Scope:** Port 8000 Chatbot Controller (UI + Orchestration layer) production window

---

## Table of Contents

1. Monitoring Setup
2. Alert Configuration
3. Maintenance Procedures
4. Incident Response Runbooks

---

## 1. Monitoring Setup

### 1.1 Prometheus Metrics To Collect

| Category | Metric | Description | Target / Threshold |
| --- | --- | --- | --- |
| Request health | `http_requests_total{status}` | Count per status code | Alert if 5xx > 5% of total |
| Latency | `http_request_duration_seconds` (p50/p95/p99) | UI & API latency | Warning > 500aEUR-ms p95, critical > 750aEUR-ms |
| Bot pipeline | `bot_dispatch_latency_seconds` | Time to hand task to bot | Alert > 2aEUR-s median |
| Queue depth | `task_queue_depth` | Outstanding tasks in orchestrator | Alert if > 25 for 3 min |
| Bot resource | `bot_cpu_percent`, `bot_memory_mb` | Per bot usage | Warning > 80%, critical > 90% |
| System | `node_cpu_seconds_total`, `node_memory_MemAvailable_bytes`, `node_filesystem_avail_bytes` | Host health | Warning CPU > 75%, memory < 20% free |
| Process | `process_open_fds`, `process_uptime_seconds` | File descriptors & uptime | Alert if FD > 85% limit |
| Dependencies | `ollama_latency_ms`, `db_connection_pool_in_use` | External services | Alert if latency > 400aEUR-ms or pool > 80% |

> Reference Prometheus scrape configs in `docs/MONITORING-SETUP.md` and ensure port 8000 exposes `/metrics` with these series.

### 1.2 Log Aggregation

- **Sources:** Flask access logs, orchestrator events (`.deia/bot-logs/`), bot health monitor logs, system journal.
- **Pipeline:** Filebeat a+' Logstash a+' Elasticsearch (or OpenSearch) with index `port8000-*`.
- **Parsing:** Apply JSON filter to bot logs; Grok pattern for Nginx/Flask access logs.
- **Retention:** 30 days hot, 60 days warm, 180 days archive (S3 or blob storage).
- **Access controls:** Minimum role `operations.read`. Streaming queries allowed for on-call.

### 1.3 Alert Thresholds / Rules

| Signal | Warning | Critical | Notes |
| --- | --- | --- | --- |
| Error rate (% of 5xx/4xx retried) | > 2% for 5 min | > 5% for 2 min | Tied to SLO 99.5% availability |
| Response time (p95) | > 500aEUR-ms 3 min | > 750aEUR-ms 1 min | Use histogram quantile |
| Bot crash loop | 2 restarts/10 min | 4 restarts/10 min | Hook into `bot_health_monitor` |
| Queue backlog | > 20 tasks 5 min | > 40 tasks 2 min | Check auto-scaler capacity |
| Memory usage | > 75% system RAM | > 85% system RAM | Cross-check with swap activity |
| Disk free | < 15% | < 10% | Evaluate `/var/log` rotation |
| Dependency latency | > 300aEUR-ms | > 500aEUR-ms | Ollama / DB |

Alert rules live in `prometheus/alerts/port8000-rules.yml` and forward to Alertmanager.

### 1.4 Dashboard Setup

1. **Grafana Folder:** `Port 8000 / Production`.
2. **Dashboards:**
   - **Service Overview:** Traffic, error rate, latency, queue depth.
   - **Bot Fleet Health:** Active bots, per-bot CPU/RAM, circuit breaker states.
   - **Resource Utilization:** Host CPU, memory, disk, network.
   - **Dependency Panel:** Ollama latency, DB pool usage, external API status.
3. **Annotations:** Auto-tag deployments (from CI webhook) & incidents (from PagerDuty).
4. **Sharing:** Read-only links for leadership; edit rights limited to Ops/SRE.

---

## 2. Alert Configuration

### 2.1 High Error Rate (>5%)

- **Trigger:** `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05`.
- **Actions:**
  1. Auto-page on-call (PagerDuty) and send Slack `#deia-ops` notification.
  2. Attach log samples (from ELK) and recent deploy metadata.
  3. Runbook reference: Section 4.5 (Deployment rollback) if caused by release.

### 2.2 High Latency (>500aEUR-ms)

- **Trigger:** `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[2m])) by (le)) > 0.5`.
- **Actions:** Warning to Slack; escalate to page if >750aEUR-ms for 1 min. Include CPU, queue depth panels in alert message.

### 2.3 Memory Leak Detection

- **Trigger:** `increase(process_resident_memory_bytes[15m]) > 500MB` combined with `node_memory_MemAvailable_bytes` downward trend.
- **Automation:** Auto-capture heap snapshot (Python `tracemalloc` dump) when warning fires.
- **Escalation:** Warning a+' Ops backlog ticket; Critical a+' page plus prepare controlled restart (see Section 4.2).

### 2.4 Connection Drops

- **Trigger:** `rate(websocket_disconnect_total[1m]) > 20` OR `tcp_connection_errors_total > 10`.
- **Response:** Notify Ops Slack thread with list of affected clients (from logs). Secondary check reverse proxy / network.

### 2.5 Disk Space Warnings

- **Trigger:** `node_filesystem_avail_bytes / node_filesystem_size_bytes < 0.15` warning, `< 0.10` critical.
- **Automation:** Warning runs log rotation script, critical blocks deployments and pages infra lead.

Alertmanager routes:
- `severity="critical"` a+' PagerDuty + SMS backup.
- `severity="warning"` a+' Slack `#deia-ops` (+ email summary every hour).
- `severity="info"` a+' Log only, reviewed in daily standup.

---

## 3. Maintenance Procedures

### 3.1 Daily Tasks (15 min)

| Item | Responsible | Notes |
| --- | --- | --- |
| Verify Prometheus scrape success (<1% scrape errors) | On-call | `prometheus_target_scrapes_exceeded` |
| Review overnight alerts (resolved) | On-call | Ensure annotations entered |
| Health check endpoints | Automation + manual spot check | `curl https://port8000/health` |
| Log volume sanity check | Ops | Detect spikes >25% day-over-day |
| Bot registry audit | Infra | Run `python src/deia/services/registry.py --audit` |

### 3.2 Weekly Tasks

- Reconcile alert noise: tune thresholds, dedupe rules.
- Validate auto-scaler behavior against queue data.
- Rotate on-call checklist & ensure documentation updated.
- Test backup/restore of Prometheus snapshots.
- Patch OS security updates during low-traffic window.

### 3.3 Monthly Tasks

- Conduct performance review using Grafana export; capture p95 trends.
- Run synthetic load test (30 min) to validate headroom; document results in `metrics/monthly/`.
- Review disaster-recovery plan and practice failover (port 8000 a+' standby host).
- Audit access logs for least-privilege compliance.

### 3.4 Quarterly / As Needed

- Full security audit (vuln scans, dependency review).
- Capacity planning (CPU, RAM, disk, network) with growth projections.
- Refresh incident runbooks; verify contact matrix.
- Chaos day: intentionally disable key component to test detection + response.

---

## 4. Incident Response Runbooks

### 4.1 High CPU Consumption

1. Confirm via `node_cpu_seconds_total` and `top`.
2. Identify culprit process (bot vs orchestrator). If bot-specific, engage bot auto-scaler to redistribute load.
3. Capture thread dump (`py-spy dump`) for analysis.
4. Mitigate:
   - Scale horizontally (spawn additional bots) if queue depth high.
   - Throttle expensive tasks via `bot_load_manager`.
5. Update incident log and monitor for stabilization (<70% CPU).

### 4.2 Out of Memory (OOM) / Imminent Memory Exhaustion

1. Alert triggered when memory >85% or kernel OOM kill detected.
2. Collect diagnostics: `free -h`, `ps aux --sort -rss | head`.
3. Dump heap for offending process (Python `tracemalloc` or `objgraph`).
4. Mitigation options:
   - Restart affected bot(s) in rolling fashion.
   - Temporarily lower concurrency.
   - Purge large caches/log buffers.
5. Post-incident: file bug with code owners, attach heap data, adjust monitoring thresholds if needed.

### 4.3 Database Connection Lost

1. Confirm DB status (`pg_isready` or service monitor). Check network path (firewall/VPN).
2. Inspect application logs for `ConnectionReset`, `OperationalError`.
3. Switch orchestrator to degraded mode: queue inbound tasks, respond with "degraded" banner on UI.
4. Attempt reconnection with exponential backoff; if >5 min downtime, failover to standby DB.
5. After service restored, flush backlog, verify data integrity, close incident with timeline.

### 4.4 WebSocket Connection Issues

1. Check reverse proxy logs for `101` upgrade failures or TLS handshake errors.
2. Validate certificate status and CORS/Origin headers.
3. Restart WebSocket worker pool if stuck (no heartbeats > 60aEUR-s).
4. Communicate to users via status page if user-facing impact >5 min.
5. Capture packet trace if issue persists; escalate to network team.

### 4.5 Deployment Rollback

1. Criteria: error rate >5%, latency >750aEUR-ms, or functional regression within 15 min of deploy.
2. Steps:
   - Freeze queue (pause new tasks) using deployment toggle.
   - `git checkout` last known good release tag; redeploy container/service.
   - Run smoke tests (`pytest tests/smoke/test_port8000.py`, UI ping).
   - Unpause queue and monitor for 10 min.
3. Post-rollback: open RCA ticket, attach metrics screenshots, list offending commit(s).

---

**Deliverable Status:** COMPLETE aEUR" operations playbook ready for Ops/SRE teams.  
**Next Steps:** Mirror thresholds into Alertmanager config, review with Q33N during 00:32 CDT status update.


