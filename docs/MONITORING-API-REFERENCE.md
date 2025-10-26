# Monitoring Services REST API Reference

## Overview

The Monitoring Services API provides comprehensive visibility into bot system health, performance, and failure patterns. This document describes all monitoring endpoints integrated into the `bot_service.py` FastAPI service.

**Base URL:** `http://{bot_host}:{bot_port}/api/monitoring`

**Status:** All endpoints fully integrated and operational

---

## Process Monitoring Endpoints

### Get Process Health for a Bot

```http
GET /api/monitoring/process/{bot_id}
```

Get process health metrics for a specific bot.

**Path Parameters:**
- `bot_id` (string, required): Bot identifier (e.g., "bot-001")

**Query Parameters:**
- `pid` (integer, optional): Process ID to monitor. If provided, will collect metrics for this process.

**Response (200 OK):**
```json
{
  "bot_id": "bot-001",
  "health": {
    "bot_id": "bot-001",
    "status": "healthy",
    "latest_metrics": {
      "bot_id": "bot-001",
      "timestamp": "2025-10-25T17:45:00.000000",
      "pid": 12345,
      "memory_mb": 150.5,
      "memory_percent": 0.15,
      "rss_mb": 150.5,
      "vms_mb": 200.0,
      "file_descriptors": 45,
      "thread_count": 8,
      "open_connections": 3,
      "cpu_percent": 0.12,
      "num_fds": 45
    },
    "memory_trend": {
      "is_leaking": false,
      "growth_rate_mb_per_hour": 2.5,
      "duration_minutes": 60
    },
    "alerts": []
  },
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

**Status Codes:**
- `200`: Success
- `404`: Bot not found in monitoring history

---

### Get All Bot Health Status

```http
GET /api/monitoring/process/all/health
```

Get process health for all currently monitored bots.

**Response (200 OK):**
```json
{
  "bots": {
    "bot-001": { /* health data */ },
    "bot-002": { /* health data */ },
    "bot-003": { /* health data */ }
  },
  "total_bots": 3,
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

---

### Check for Memory Leak

```http
GET /api/monitoring/process/{bot_id}/memory-leak
```

Analyze memory usage trends to detect potential memory leaks.

**Path Parameters:**
- `bot_id` (string, required): Bot identifier

**Response (200 OK):**
```json
{
  "bot_id": "bot-001",
  "is_leaking": false,
  "growth_rate_mb_per_hour": 2.5,
  "duration_minutes": 60,
  "measurements": [100.0, 105.2, 110.1, 115.8],
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

**Notes:**
- Memory leak detection requires minimum 10 minutes of data
- Growth rate > 10 MB/hour is flagged as potential leak
- Measurements array shows memory values over the observation window

---

## API Health Monitoring Endpoints

### Get API Health Status

```http
GET /api/monitoring/api/status
```

Get health status of all monitored API endpoints.

**Response (200 OK):**
```json
{
  "overall_health": "healthy",
  "endpoints": {
    "http://localhost:8001/health": {
      "response_time_ms": 150.5,
      "status_code": 200,
      "is_healthy": true,
      "error_rate": 0.0,
      "last_checked": "2025-10-25T17:45:00.000000"
    },
    "http://localhost:8001/status": {
      "response_time_ms": 200.0,
      "status_code": 200,
      "is_healthy": true,
      "error_rate": 0.0,
      "last_checked": "2025-10-25T17:45:00.000000"
    }
  },
  "cascade_risk": 0.05,
  "response_time_p95_ms": 250.0
}
```

**Health Status Values:**
- `healthy`: All endpoints responding normally
- `degraded`: Some endpoints slow or errors < 10%
- `critical`: Multiple endpoints down or error rate > 25%

---

## Queue Analytics Endpoints

### Get Queue Status

```http
GET /api/monitoring/queue/status
```

Get current queue depth, throughput, and latency metrics.

**Response (200 OK):**
```json
{
  "total_tasks": 150,
  "queue_depth": 5,
  "tasks_executing": 3,
  "tasks_completed": 142,
  "throughput_tasks_per_minute": 2.5,
  "avg_latency_seconds": 45.2,
  "p95_latency_seconds": 120.0,
  "p99_latency_seconds": 180.0,
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

**Metrics Explained:**
- `queue_depth`: Number of tasks waiting to execute
- `throughput_tasks_per_minute`: Tasks completed per minute
- `avg_latency_seconds`: Average time from queue → completion
- `p95_latency_seconds`: 95th percentile latency (most tasks faster)
- `p99_latency_seconds`: 99th percentile latency (very slow outliers)

---

### Identify Queue Bottlenecks

```http
GET /api/monitoring/queue/bottlenecks
```

Detect performance bottlenecks in the task queue.

**Response (200 OK):**
```json
{
  "bottlenecks": [
    {
      "type": "queue_depth_high",
      "severity": "warning",
      "message": "Queue depth 45 exceeds threshold (30)",
      "metrics": {
        "current_depth": 45,
        "threshold": 30,
        "recommendation": "Scale up bots or reduce incoming task rate"
      }
    },
    {
      "type": "execution_time_high",
      "severity": "info",
      "message": "Average execution time 300s is high",
      "metrics": {
        "current_avg_ms": 300000,
        "normal_avg_ms": 150000
      }
    }
  ],
  "count": 2,
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

**Bottleneck Types:**
- `queue_depth_high`: Too many tasks waiting
- `execution_time_high`: Tasks taking longer than expected
- `wait_time_high`: Tasks spending too long in queue
- `throughput_low`: Completion rate below expected

---

### Add Task (for Analytics)

```http
POST /api/monitoring/queue/add-task
```

Record a task in the queue analytics system.

**Request Body:**
```json
{
  "task_id": "TASK-001",
  "task_type": "development",
  "priority": "P1"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "task_id": "TASK-001",
  "queue_depth": 5,
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

---

### Complete Task (for Analytics)

```http
POST /api/monitoring/queue/complete-task
```

Mark a task as completed for analytics tracking.

**Request Body:**
```json
{
  "task_id": "TASK-001",
  "execution_time_seconds": 45.2,
  "success": true
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "task_id": "TASK-001",
  "queue_depth": 4,
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

---

## Failure Analysis Endpoints

### Get Failure Statistics

```http
GET /api/monitoring/failures/stats
```

Get comprehensive failure statistics and patterns.

**Response (200 OK):**
```json
{
  "total_failures": 15,
  "failure_rate": 0.1,
  "failures_24h": 12,
  "by_task_type": {
    "development": {
      "count": 8,
      "error_type": "timeout",
      "failure_rate": 0.15
    },
    "analysis": {
      "count": 7,
      "error_type": "resource",
      "failure_rate": 0.12
    }
  },
  "by_bot": {
    "bot-001": {
      "count": 9,
      "failure_rate": 0.18
    },
    "bot-002": {
      "count": 6,
      "failure_rate": 0.08
    }
  },
  "recent_failures": [
    {
      "task_id": "TASK-999",
      "error_message": "Timeout after 30 seconds",
      "error_type": "timeout",
      "timestamp": "2025-10-25T17:40:00.000000"
    }
  ],
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

---

### Predict Cascade Failure Risk

```http
GET /api/monitoring/failures/cascade-risk
```

Predict the risk of cascading failures affecting multiple systems.

**Response (200 OK):**
```json
{
  "cascade_risk_score": 0.35,
  "risk_level": "medium",
  "affected_bots": ["bot-001", "bot-003"],
  "vulnerable_services": ["task_orchestrator", "api_health_monitor"],
  "recommendations": [
    "Scale up bot capacity to reduce load",
    "Investigate dependency failures in task_orchestrator",
    "Review circuit breaker settings"
  ],
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

**Risk Levels:**
- `low` (0.0-0.25): Isolated failures only
- `medium` (0.25-0.6): Multiple failures detected
- `high` (0.6+): Cascade conditions detected

---

### Get Error Trends

```http
GET /api/monitoring/failures/trends
```

Analyze error trends over time.

**Response (200 OK):**
```json
{
  "total_errors": 25,
  "trend": "stable",
  "trend_direction": "flat",
  "by_error_type": {
    "timeout": 12,
    "resource": 8,
    "network": 5
  },
  "hourly_distribution": [
    { "hour": "14:00", "error_count": 2 },
    { "hour": "15:00", "error_count": 4 },
    { "hour": "16:00", "error_count": 6 },
    { "hour": "17:00", "error_count": 13 }
  ],
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

**Trend Values:**
- `stable`: Error rate not changing significantly
- `increasing`: Error rate trending up (⚠️)
- `decreasing`: Error rate trending down (✓)

---

### Record Failure

```http
POST /api/monitoring/failures/record
```

Record a task failure for analytics.

**Request Body:**
```json
{
  "task_id": "TASK-001",
  "bot_id": "bot-001",
  "task_type": "development",
  "error_message": "Timeout after 30 seconds",
  "error_code": 504
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "task_id": "TASK-001",
  "total_failures": 16,
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

---

## Observability API (Unified)

### Get Comprehensive Metrics Snapshot

```http
GET /api/monitoring/observability/snapshot
```

Get unified snapshot of all system metrics from all monitoring sources.

**Response (200 OK):**
```json
{
  "timestamp": "2025-10-25T17:45:00.000000",
  "system": {
    "bot-001": {
      "status": "healthy",
      "latest_metrics": { /* process metrics */ },
      "memory_trend": { /* memory analysis */ },
      "alerts": []
    }
  },
  "queues": {
    "queue_depth": 5,
    "throughput_tasks_per_minute": 2.5,
    "avg_latency_seconds": 45.2,
    "bottlenecks": []
  },
  "api": {
    "overall_health": "healthy",
    "endpoints": { /* endpoint status */ }
  },
  "failures": {
    "total_failures": 15,
    "failure_rate": 0.1,
    "cascade_risk": { /* cascade analysis */ }
  },
  "health": {
    "overall_status": "healthy",
    "health_score": 85,
    "active_alerts": 0
  }
}
```

---

### Get Historical Metrics

```http
GET /api/monitoring/observability/history/{metric_type}
```

Retrieve historical time-series data for any metric type.

**Path Parameters:**
- `metric_type` (string, required): One of `process`, `queue`, `api`, `failures`, `health`

**Query Parameters:**
- `hours` (integer, optional, default=24): Number of hours of history to retrieve
- `limit` (integer, optional, default=100): Maximum number of data points to return

**Response (200 OK):**
```json
{
  "metric_type": "queue",
  "hours": 24,
  "data": [
    {
      "timestamp": "2025-10-24T17:45:00.000000",
      "queue_depth": 3,
      "throughput": 2.1
    },
    {
      "timestamp": "2025-10-24T18:45:00.000000",
      "queue_depth": 5,
      "throughput": 2.3
    },
    {
      "timestamp": "2025-10-24T19:45:00.000000",
      "queue_depth": 8,
      "throughput": 1.9
    }
  ],
  "count": 24,
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

**Example Requests:**

Process metrics from last 24 hours:
```
GET /api/monitoring/observability/history/process?hours=24&limit=100
```

Queue metrics from last 7 days:
```
GET /api/monitoring/observability/history/queue?hours=168&limit=500
```

---

## Status Codes and Errors

All endpoints follow standard HTTP status codes:

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Data retrieved successfully |
| 400 | Bad Request | Missing required parameter |
| 404 | Not Found | Bot or metric not found |
| 500 | Server Error | Internal monitoring error |

**Error Response Format:**
```json
{
  "success": false,
  "error": "Bot bot-999 not found",
  "timestamp": "2025-10-25T17:45:00.000000"
}
```

---

## Integration with Features 3-5

The monitoring services are fully integrated with:

- **Feature 3: Bot Communication** - Messaging performance tracked
- **Feature 4: Adaptive Task Scheduling** - Task scheduling performance analyzed
- **Feature 5: System Health Dashboard** - Monitoring feeds health metrics

---

## Authentication & Security

Currently, monitoring endpoints are accessible without authentication. For production deployment, consider:

1. Adding JWT authentication via AuthManager
2. Implementing role-based access control (viewer, admin)
3. Adding rate limiting per client
4. Encrypting sensitive metrics in transit

---

## Performance Notes

- **Snapshot endpoint**: O(1) - aggregates pre-computed metrics
- **Historical data**: O(n) where n = data points, typically < 100ms
- **Process monitoring**: Per-bot monitoring has ~50ms overhead
- **Failure analysis**: Pattern detection runs on-demand, ~100-500ms depending on data volume

---

## Logging

All monitoring activities are logged to `.deia/bot-logs/`:
- `bot-process-health.jsonl` - Process metrics
- `api-health.jsonl` - API endpoint checks
- `queue-analytics.jsonl` - Queue snapshots
- `failure-analysis.jsonl` - Failure events
- `health-metrics.jsonl` - Health evaluations

---

## Examples

### Python Client Example

```python
import requests

# Get queue status
resp = requests.get("http://localhost:8001/api/monitoring/queue/status")
queue_status = resp.json()
print(f"Queue depth: {queue_status['queue_depth']}")
print(f"Throughput: {queue_status['throughput_tasks_per_minute']} tasks/min")

# Get bot process health
resp = requests.get("http://localhost:8001/api/monitoring/process/bot-001")
health = resp.json()
print(f"Bot status: {health['health']['status']}")
print(f"Memory: {health['health']['latest_metrics']['memory_mb']} MB")

# Check for cascade risk
resp = requests.get("http://localhost:8001/api/monitoring/failures/cascade-risk")
cascade = resp.json()
print(f"Cascade risk level: {cascade['risk_level']}")
```

### cURL Examples

Get all bot health:
```bash
curl http://localhost:8001/api/monitoring/process/all/health
```

Record task completion:
```bash
curl -X POST http://localhost:8001/api/monitoring/queue/complete-task \
  -H "Content-Type: application/json" \
  -d '{"task_id":"TASK-001","execution_time_seconds":45.2,"success":true}'
```

Get 7-day history of queue metrics:
```bash
curl "http://localhost:8001/api/monitoring/observability/history/queue?hours=168&limit=500"
```

---

## Changelog

**Version 1.0 - 2025-10-25**
- Initial release
- 22 monitoring endpoints
- Full integration with Features 3-5
- Support for all metric types
- Real-time and historical data access
