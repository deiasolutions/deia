"""
API Health Monitor - Monitor bot service endpoints for health and performance.

Tracks response times, error rates, timeouts, latency patterns.
Detects degraded services and cascading failures.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import json
import time
import requests


@dataclass
class EndpointMetrics:
    """Health metrics for a single API endpoint."""
    endpoint_url: str
    bot_id: str
    timestamp: str
    response_time_ms: float
    status_code: int
    is_healthy: bool
    error_message: Optional[str] = None
    timeout: bool = False
    request_count: int = 0
    error_count: int = 0
    error_rate: float = 0.0
    avg_response_time_ms: float = 0.0


@dataclass
class ServiceHealth:
    """Overall health of a bot's service."""
    bot_id: str
    service_url: str
    overall_status: str  # healthy, degraded, critical
    endpoints_healthy: int = 0
    endpoints_total: int = 0
    error_rate: float = 0.0
    avg_response_time_ms: float = 0.0
    last_check: str = ""
    consecutive_failures: int = 0


class APIHealthMonitor:
    """
    Monitor bot service endpoint health.

    Features:
    - Track response times and error rates per endpoint
    - Detect service degradation
    - Detect cascading failures
    - Health status aggregation
    - Performance trend analysis
    """

    # Response time thresholds
    RESPONSE_TIME_NORMAL_MS = 100
    RESPONSE_TIME_SLOW_MS = 500
    RESPONSE_TIME_CRITICAL_MS = 2000

    # Error thresholds
    ERROR_RATE_WARNING = 0.1  # 10% error rate
    ERROR_RATE_CRITICAL = 0.25  # 25% error rate

    # Failure tracking
    CONSECUTIVE_FAILURES_ALERT = 3

    # Request timeout
    REQUEST_TIMEOUT_SECONDS = 5

    def __init__(self, work_dir: Path):
        """
        Initialize API health monitor.

        Args:
            work_dir: Working directory for logs
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.health_log = self.log_dir / "api-health.jsonl"

        # Track metrics per endpoint
        self.endpoint_metrics: Dict[str, List[EndpointMetrics]] = {}
        self.service_health: Dict[str, ServiceHealth] = {}
        self.cascade_risk: List[str] = []  # Endpoints at risk of cascade

    def check_endpoint(self, bot_id: str, endpoint_url: str) -> EndpointMetrics:
        """
        Check single endpoint health.

        Args:
            bot_id: Bot identifier
            endpoint_url: Full URL to check (e.g., http://localhost:8001/health)

        Returns:
            EndpointMetrics snapshot
        """
        start_time = time.time()
        status_code = 0
        is_healthy = False
        error_message = None
        timeout = False

        try:
            response = requests.get(
                endpoint_url,
                timeout=self.REQUEST_TIMEOUT_SECONDS
            )
            status_code = response.status_code
            is_healthy = status_code == 200

        except requests.exceptions.Timeout:
            timeout = True
            error_message = "Request timeout"
            status_code = 0
        except requests.exceptions.ConnectionError:
            error_message = "Connection refused"
            status_code = 0
        except Exception as e:
            error_message = str(e)
            status_code = 0

        response_time_ms = (time.time() - start_time) * 1000

        # Track metrics
        key = f"{bot_id}:{endpoint_url}"
        if key not in self.endpoint_metrics:
            self.endpoint_metrics[key] = []

        # Calculate running stats
        history = self.endpoint_metrics[key]
        request_count = len(history) + 1
        error_count = sum(1 for m in history if not m.is_healthy) + (0 if is_healthy else 1)
        error_rate = error_count / request_count if request_count > 0 else 0

        avg_response_time = (
            sum(m.response_time_ms for m in history) + response_time_ms
        ) / request_count if request_count > 0 else response_time_ms

        metrics = EndpointMetrics(
            endpoint_url=endpoint_url,
            bot_id=bot_id,
            timestamp=datetime.now().isoformat(),
            response_time_ms=response_time_ms,
            status_code=status_code,
            is_healthy=is_healthy,
            error_message=error_message,
            timeout=timeout,
            request_count=request_count,
            error_count=error_count,
            error_rate=error_rate,
            avg_response_time_ms=avg_response_time
        )

        self.endpoint_metrics[key].append(metrics)

        # Keep recent history (24 hours)
        cutoff = datetime.now() - timedelta(hours=24)
        self.endpoint_metrics[key] = [
            m for m in self.endpoint_metrics[key]
            if datetime.fromisoformat(m.timestamp) > cutoff
        ]

        # Check for anomalies
        self._check_endpoint_anomalies(bot_id, metrics)

        # Log metrics
        self._log_metrics(metrics)

        return metrics

    def check_bot_service(self, bot_id: str, service_url: str) -> ServiceHealth:
        """
        Check overall health of a bot's service.

        Args:
            bot_id: Bot identifier
            service_url: Base URL of bot service (e.g., http://localhost:8001)

        Returns:
            ServiceHealth summary
        """
        # Standard endpoints to check
        endpoints = [
            f"{service_url}/health",
            f"{service_url}/status",
            f"{service_url}/api/orchestrate/status",
        ]

        results = []
        for endpoint in endpoints:
            metrics = self.check_endpoint(bot_id, endpoint)
            if metrics:
                results.append(metrics)

        # Calculate overall health
        if not results:
            overall_status = "unknown"
            endpoints_healthy = 0
            endpoints_total = 0
            error_rate = 0.0
            avg_response_time = 0.0
        else:
            endpoints_healthy = sum(1 for m in results if m.is_healthy)
            endpoints_total = len(results)
            error_rate = sum(m.error_rate for m in results) / len(results)
            avg_response_time = sum(m.avg_response_time_ms for m in results) / len(results)

            if endpoints_healthy == endpoints_total:
                overall_status = "healthy"
            elif endpoints_healthy >= endpoints_total * 0.5:
                overall_status = "degraded"
            else:
                overall_status = "critical"

        # Track consecutive failures
        key = bot_id
        if key not in self.service_health:
            self.service_health[key] = ServiceHealth(
                bot_id=bot_id,
                service_url=service_url,
                overall_status=overall_status
            )

        prev_health = self.service_health[key]
        consecutive_failures = (
            prev_health.consecutive_failures + 1
            if overall_status != "healthy" else 0
        )

        health = ServiceHealth(
            bot_id=bot_id,
            service_url=service_url,
            overall_status=overall_status,
            endpoints_healthy=endpoints_healthy,
            endpoints_total=endpoints_total,
            error_rate=error_rate,
            avg_response_time_ms=avg_response_time,
            last_check=datetime.now().isoformat(),
            consecutive_failures=consecutive_failures
        )

        self.service_health[key] = health

        # Check for cascade risk
        self._check_cascade_risk(bot_id, health)

        return health

    def get_api_status(self, bot_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get API health status.

        Args:
            bot_id: Optional - specific bot, or None for all

        Returns:
            API health summary
        """
        if bot_id and bot_id in self.service_health:
            health = self.service_health[bot_id]
            return {
                "bot_id": bot_id,
                "status": health.overall_status,
                "endpoints_healthy": health.endpoints_healthy,
                "endpoints_total": health.endpoints_total,
                "error_rate": health.error_rate,
                "avg_response_time_ms": health.avg_response_time_ms,
                "consecutive_failures": health.consecutive_failures,
                "timestamp": datetime.now().isoformat()
            }

        # Return all
        return {
            "services": [
                {
                    "bot_id": bot_id,
                    "status": health.overall_status,
                    "endpoints_healthy": health.endpoints_healthy,
                    "endpoints_total": health.endpoints_total,
                    "error_rate": health.error_rate,
                    "avg_response_time_ms": health.avg_response_time_ms
                }
                for bot_id, health in self.service_health.items()
            ],
            "cascade_risk": self.cascade_risk,
            "timestamp": datetime.now().isoformat()
        }

    def _check_endpoint_anomalies(self, bot_id: str, metrics: EndpointMetrics) -> None:
        """Check for endpoint anomalies."""
        # Response time anomalies
        if metrics.response_time_ms > self.RESPONSE_TIME_CRITICAL_MS and not metrics.timeout:
            self._log_event("response_time_critical", bot_id, {
                "endpoint": metrics.endpoint_url,
                "response_time_ms": metrics.response_time_ms
            })

        if metrics.timeout:
            self._log_event("endpoint_timeout", bot_id, {
                "endpoint": metrics.endpoint_url
            })

        if not metrics.is_healthy:
            self._log_event("endpoint_unhealthy", bot_id, {
                "endpoint": metrics.endpoint_url,
                "status_code": metrics.status_code,
                "error": metrics.error_message
            })

    def _check_cascade_risk(self, bot_id: str, health: ServiceHealth) -> None:
        """Check for cascading failure risk."""
        if health.consecutive_failures >= self.CONSECUTIVE_FAILURES_ALERT:
            cascade_key = f"{bot_id}:cascade_risk"
            if cascade_key not in self.cascade_risk:
                self.cascade_risk.append(cascade_key)
                self._log_event("cascade_risk_detected", bot_id, {
                    "consecutive_failures": health.consecutive_failures,
                    "service_url": health.service_url
                })

    def _log_metrics(self, metrics: EndpointMetrics) -> None:
        """Log API metrics."""
        entry = {
            "timestamp": metrics.timestamp,
            "bot_id": metrics.bot_id,
            "endpoint": metrics.endpoint_url,
            "response_time_ms": metrics.response_time_ms,
            "status_code": metrics.status_code,
            "is_healthy": metrics.is_healthy,
            "error_rate": metrics.error_rate
        }

        try:
            with open(self.health_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[API-HEALTH-MONITOR] Failed to log metrics: {e}")

    def _log_event(self, event: str, bot_id: str, details: Dict = None) -> None:
        """Log API health event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "bot_id": bot_id,
            "details": details or {}
        }

        try:
            with open(self.health_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[API-HEALTH-MONITOR] Failed to log event: {e}")
