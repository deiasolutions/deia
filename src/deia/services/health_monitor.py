"""
Health Monitor - Aggregate system health metrics and alert on anomalies.

Monitors all bot infrastructure (orchestration, scaling, messaging, scheduling)
and provides real-time health dashboard with alerts for anomalies.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
import json


class AlertLevel(Enum):
    """Alert severity levels."""
    CRITICAL = "critical"  # Immediate action required
    WARNING = "warning"    # Should be addressed soon
    INFO = "info"          # Informational


class AlertType(Enum):
    """Types of alerts."""
    CPU_HIGH = "cpu_high"
    MEMORY_HIGH = "memory_high"
    QUEUE_BACKLOG = "queue_backlog"
    BOT_FAILURE = "bot_failure"
    LOW_SUCCESS_RATE = "low_success_rate"
    MESSAGE_DELIVERY_FAILED = "message_delivery_failed"
    SCALING_ISSUE = "scaling_issue"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    COMMUNICATION_TIMEOUT = "communication_timeout"


@dataclass
class Alert:
    """System alert."""
    alert_id: str
    alert_type: AlertType
    level: AlertLevel
    title: str
    message: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    resolved: bool = False
    resolved_at: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            **asdict(self),
            "alert_type": self.alert_type.value,
            "level": self.level.value
        }


@dataclass
class SystemHealthMetrics:
    """Current system health metrics."""
    timestamp: str
    total_bots: int
    active_bots: int
    queued_tasks: int
    avg_bot_load: float
    system_cpu_percent: float
    system_memory_percent: float
    message_queue_size: int
    pending_message_failures: int
    avg_success_rate: float
    alert_count: int = 0
    critical_alerts: int = 0

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class HealthMonitor:
    """
    System health monitoring and alerting.

    Features:
    - Real-time metrics aggregation
    - Alert generation on anomalies
    - Alert history and resolution tracking
    - Health status summary
    - Dashboard data
    """

    # Alert thresholds
    CPU_CRITICAL_THRESHOLD = 0.95
    CPU_WARNING_THRESHOLD = 0.80
    MEMORY_CRITICAL_THRESHOLD = 0.90
    MEMORY_WARNING_THRESHOLD = 0.75
    QUEUE_BACKLOG_THRESHOLD = 10
    BOT_FAILURE_THRESHOLD = 0.3  # Success rate < 30%
    MESSAGE_FAILURE_THRESHOLD = 5  # More than 5 failed messages

    # Alert retention (keep for 24 hours)
    ALERT_RETENTION_HOURS = 24

    def __init__(self, work_dir: Path):
        """
        Initialize health monitor.

        Args:
            work_dir: Working directory for logs
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.alerts_log = self.log_dir / "health-alerts.jsonl"

        # Alert tracking
        self.alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []

        # Last known metrics
        self.last_metrics: Optional[SystemHealthMetrics] = None

    def evaluate_health(
        self,
        total_bots: int,
        active_bots: int,
        queued_tasks: int,
        avg_bot_load: float,
        system_cpu_percent: float,
        system_memory_percent: float,
        message_queue_size: int,
        pending_message_failures: int,
        avg_success_rate: float
    ) -> SystemHealthMetrics:
        """
        Evaluate system health and generate alerts.

        Args:
            total_bots: Total bots in system
            active_bots: Currently active bots
            queued_tasks: Tasks in queue
            avg_bot_load: Average bot load (0-1)
            system_cpu_percent: System CPU usage (0-1)
            system_memory_percent: System memory usage (0-1)
            message_queue_size: Pending messages
            pending_message_failures: Failed messages
            avg_success_rate: Average success rate (0-1)

        Returns:
            SystemHealthMetrics with current state
        """
        metrics = SystemHealthMetrics(
            timestamp=datetime.now().isoformat(),
            total_bots=total_bots,
            active_bots=active_bots,
            queued_tasks=queued_tasks,
            avg_bot_load=avg_bot_load,
            system_cpu_percent=system_cpu_percent,
            system_memory_percent=system_memory_percent,
            message_queue_size=message_queue_size,
            pending_message_failures=pending_message_failures,
            avg_success_rate=avg_success_rate
        )

        # Check for anomalies and generate alerts
        self._check_cpu_health(system_cpu_percent)
        self._check_memory_health(system_memory_percent)
        self._check_queue_health(queued_tasks)
        self._check_bot_health(active_bots, total_bots, avg_success_rate)
        self._check_messaging_health(message_queue_size, pending_message_failures)
        self._check_resource_health(system_cpu_percent, system_memory_percent)

        # Update metrics
        metrics.alert_count = len([a for a in self.alerts.values() if not a.resolved])
        metrics.critical_alerts = len([
            a for a in self.alerts.values()
            if not a.resolved and a.level == AlertLevel.CRITICAL
        ])

        self.last_metrics = metrics

        # Log metrics
        self._log_metrics(metrics)

        return metrics

    def get_dashboard(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard data.

        Returns:
            Dashboard dict with all health information
        """
        if not self.last_metrics:
            return {
                "status": "no_data",
                "message": "No metrics available yet"
            }

        # Get active alerts
        active_alerts = [
            a.to_dict() for a in self.alerts.values()
            if not a.resolved
        ]

        # Get recent history (last 100 alerts)
        recent_alerts = [
            a.to_dict() for a in self.alert_history[-100:]
        ]

        # Calculate health score (0-100)
        health_score = self._calculate_health_score()

        # System status
        if len([a for a in self.alerts.values() if not a.resolved and a.level == AlertLevel.CRITICAL]) > 0:
            overall_status = "critical"
        elif len([a for a in self.alerts.values() if not a.resolved and a.level == AlertLevel.WARNING]) > 0:
            overall_status = "warning"
        else:
            overall_status = "healthy"

        return {
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "health_score": health_score,
            "metrics": self.last_metrics.to_dict(),
            "active_alerts": active_alerts,
            "recent_alerts": recent_alerts,
            "alert_summary": {
                "total_active": len(active_alerts),
                "critical": len([a for a in active_alerts if a["level"] == "critical"]),
                "warning": len([a for a in active_alerts if a["level"] == "warning"]),
                "info": len([a for a in active_alerts if a["level"] == "info"])
            },
            "bot_health": {
                "total": self.last_metrics.total_bots,
                "active": self.last_metrics.active_bots,
                "inactive": self.last_metrics.total_bots - self.last_metrics.active_bots,
                "avg_load": self.last_metrics.avg_bot_load,
                "avg_success_rate": self.last_metrics.avg_success_rate
            },
            "system_resources": {
                "cpu_percent": self.last_metrics.system_cpu_percent,
                "memory_percent": self.last_metrics.system_memory_percent
            },
            "queue_status": {
                "queued_tasks": self.last_metrics.queued_tasks,
                "pending_messages": self.last_metrics.message_queue_size,
                "failed_messages": self.last_metrics.pending_message_failures
            }
        }

    def resolve_alert(self, alert_id: str) -> bool:
        """
        Mark an alert as resolved.

        Args:
            alert_id: Alert identifier

        Returns:
            True if resolved
        """
        if alert_id not in self.alerts:
            return False

        alert = self.alerts[alert_id]
        alert.resolved = True
        alert.resolved_at = datetime.now().isoformat()

        self._log_event("alert_resolved", {
            "alert_id": alert_id,
            "alert_type": alert.alert_type.value
        })

        return True

    def get_alerts(self, level: Optional[str] = None, resolved: bool = False) -> List[Dict]:
        """
        Get alerts, optionally filtered.

        Args:
            level: Filter by level (critical|warning|info)
            resolved: Include resolved alerts

        Returns:
            List of alert dicts
        """
        alerts = [
            a for a in self.alerts.values()
            if (resolved or not a.resolved) and (level is None or a.level.value == level)
        ]

        return [a.to_dict() for a in alerts]

    def get_health_timeline(self, hours: int = 24) -> List[Dict]:
        """
        Get health metrics timeline.

        Args:
            hours: Hours to look back

        Returns:
            List of metrics snapshots
        """
        # This would be retrieved from metrics log
        # For now, return empty (would be extended with actual time-series data)
        return []

    def _check_cpu_health(self, cpu_percent: float) -> None:
        """Check CPU health and generate alerts."""
        alert_id = "cpu_health"

        if cpu_percent >= self.CPU_CRITICAL_THRESHOLD:
            self._generate_alert(
                alert_id=alert_id,
                alert_type=AlertType.CPU_HIGH,
                level=AlertLevel.CRITICAL,
                title="Critical CPU Usage",
                message=f"System CPU at {cpu_percent*100:.1f}%",
                metrics={"cpu_percent": cpu_percent}
            )
        elif cpu_percent >= self.CPU_WARNING_THRESHOLD:
            self._generate_alert(
                alert_id=alert_id,
                alert_type=AlertType.CPU_HIGH,
                level=AlertLevel.WARNING,
                title="High CPU Usage",
                message=f"System CPU at {cpu_percent*100:.1f}%",
                metrics={"cpu_percent": cpu_percent}
            )
        else:
            # Resolve if below threshold
            if alert_id in self.alerts:
                self.resolve_alert(alert_id)

    def _check_memory_health(self, memory_percent: float) -> None:
        """Check memory health and generate alerts."""
        alert_id = "memory_health"

        if memory_percent >= self.MEMORY_CRITICAL_THRESHOLD:
            self._generate_alert(
                alert_id=alert_id,
                alert_type=AlertType.MEMORY_HIGH,
                level=AlertLevel.CRITICAL,
                title="Critical Memory Usage",
                message=f"System memory at {memory_percent*100:.1f}%",
                metrics={"memory_percent": memory_percent}
            )
        elif memory_percent >= self.MEMORY_WARNING_THRESHOLD:
            self._generate_alert(
                alert_id=alert_id,
                alert_type=AlertType.MEMORY_HIGH,
                level=AlertLevel.WARNING,
                title="High Memory Usage",
                message=f"System memory at {memory_percent*100:.1f}%",
                metrics={"memory_percent": memory_percent}
            )
        else:
            if alert_id in self.alerts:
                self.resolve_alert(alert_id)

    def _check_queue_health(self, queue_size: int) -> None:
        """Check queue health."""
        alert_id = "queue_health"

        if queue_size >= self.QUEUE_BACKLOG_THRESHOLD:
            self._generate_alert(
                alert_id=alert_id,
                alert_type=AlertType.QUEUE_BACKLOG,
                level=AlertLevel.WARNING,
                title="Task Queue Backlog",
                message=f"{queue_size} tasks queued",
                metrics={"queue_size": queue_size}
            )
        else:
            if alert_id in self.alerts:
                self.resolve_alert(alert_id)

    def _check_bot_health(self, active_bots: int, total_bots: int, success_rate: float) -> None:
        """Check bot health."""
        # Check for inactive bots
        if active_bots < total_bots:
            alert_id = "bot_availability"
            inactive = total_bots - active_bots
            self._generate_alert(
                alert_id=alert_id,
                alert_type=AlertType.BOT_FAILURE,
                level=AlertLevel.WARNING,
                title="Bots Offline",
                message=f"{inactive}/{total_bots} bots inactive",
                metrics={"active": active_bots, "total": total_bots}
            )
        else:
            if "bot_availability" in self.alerts:
                self.resolve_alert("bot_availability")

        # Check success rate
        alert_id = "success_rate"
        if success_rate < self.BOT_FAILURE_THRESHOLD:
            self._generate_alert(
                alert_id=alert_id,
                alert_type=AlertType.LOW_SUCCESS_RATE,
                level=AlertLevel.WARNING,
                title="Low Success Rate",
                message=f"Average success rate: {success_rate*100:.1f}%",
                metrics={"success_rate": success_rate}
            )
        else:
            if alert_id in self.alerts:
                self.resolve_alert(alert_id)

    def _check_messaging_health(self, queue_size: int, failures: int) -> None:
        """Check messaging health."""
        alert_id = "messaging_health"

        if failures >= self.MESSAGE_FAILURE_THRESHOLD:
            self._generate_alert(
                alert_id=alert_id,
                alert_type=AlertType.MESSAGE_DELIVERY_FAILED,
                level=AlertLevel.WARNING,
                title="Message Delivery Failures",
                message=f"{failures} failed message deliveries",
                metrics={"failures": failures}
            )
        else:
            if alert_id in self.alerts:
                self.resolve_alert(alert_id)

    def _check_resource_health(self, cpu_percent: float, memory_percent: float) -> None:
        """Check overall resource exhaustion."""
        alert_id = "resource_exhausted"

        if cpu_percent >= 0.9 and memory_percent >= 0.85:
            self._generate_alert(
                alert_id=alert_id,
                alert_type=AlertType.RESOURCE_EXHAUSTED,
                level=AlertLevel.CRITICAL,
                title="System Resources Exhausted",
                message="CPU and memory both critically high",
                metrics={"cpu": cpu_percent, "memory": memory_percent}
            )
        else:
            if alert_id in self.alerts:
                self.resolve_alert(alert_id)

    def _generate_alert(
        self,
        alert_id: str,
        alert_type: AlertType,
        level: AlertLevel,
        title: str,
        message: str,
        metrics: Dict = None
    ) -> None:
        """Generate an alert if not already present."""
        if alert_id in self.alerts and not self.alerts[alert_id].resolved:
            # Alert already exists, just update metrics
            self.alerts[alert_id].metrics = metrics or {}
            return

        alert = Alert(
            alert_id=alert_id,
            alert_type=alert_type,
            level=level,
            title=title,
            message=message,
            metrics=metrics or {}
        )

        self.alerts[alert_id] = alert
        self.alert_history.append(alert)

        # Clean old alerts
        cutoff = datetime.now() - timedelta(hours=self.ALERT_RETENTION_HOURS)
        self.alert_history = [
            a for a in self.alert_history
            if datetime.fromisoformat(a.timestamp) > cutoff
        ]

        self._log_event("alert_generated", {
            "alert_id": alert_id,
            "alert_type": alert_type.value,
            "level": level.value,
            "title": title
        })

    def _calculate_health_score(self) -> float:
        """Calculate overall health score (0-100)."""
        if not self.last_metrics:
            return 0.0

        score = 100.0

        # Deduct points for issues
        active_alerts = [a for a in self.alerts.values() if not a.resolved]

        for alert in active_alerts:
            if alert.level == AlertLevel.CRITICAL:
                score -= 20
            elif alert.level == AlertLevel.WARNING:
                score -= 10
            else:
                score -= 2

        # Deduct for high resource usage
        if self.last_metrics.system_cpu_percent > 0.8:
            score -= 5
        if self.last_metrics.system_memory_percent > 0.8:
            score -= 5

        # Deduct for low success rate
        if self.last_metrics.avg_success_rate < 0.9:
            score -= 10

        return max(0.0, min(100.0, score))

    def _log_metrics(self, metrics: SystemHealthMetrics) -> None:
        """Log health metrics."""
        entry = {
            "timestamp": metrics.timestamp,
            "metrics": metrics.to_dict()
        }

        try:
            # Keep a separate metrics log
            with open(self.log_dir / "health-metrics.jsonl", "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[HEALTH-MONITOR] Failed to log metrics: {e}")

    def _log_event(self, event: str, details: Dict = None) -> None:
        """Log health monitor event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details or {}
        }

        try:
            with open(self.alerts_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[HEALTH-MONITOR] Failed to log event: {e}")
