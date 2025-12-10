"""
Observability API - Unified interface for all monitoring data.

Aggregates metrics from all monitors and exposes via REST endpoints.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path


class ObservabilityAPI:
    """
    Unified API for system observability.

    Aggregates data from:
    - BotProcessMonitor
    - APIHealthMonitor
    - QueueAnalytics
    - FailureAnalyzer
    """

    def __init__(
        self,
        process_monitor=None,
        api_monitor=None,
        queue_analytics=None,
        failure_analyzer=None,
        health_monitor=None
    ):
        """
        Initialize observability API.

        Args:
            process_monitor: BotProcessMonitor instance
            api_monitor: APIHealthMonitor instance
            queue_analytics: QueueAnalytics instance
            failure_analyzer: FailureAnalyzer instance
            health_monitor: HealthMonitor instance (from Features 3-5)
        """
        self.process_monitor = process_monitor
        self.api_monitor = api_monitor
        self.queue_analytics = queue_analytics
        self.failure_analyzer = failure_analyzer
        self.health_monitor = health_monitor

    def get_metrics_snapshot(self) -> Dict[str, Any]:
        """
        Get comprehensive metrics snapshot.

        Returns all current metrics from all monitors.

        Returns:
            {
                "system": {...},
                "queues": {...},
                "api": {...},
                "failures": {...},
                "health": {...}
            }
        """
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "system": {},
            "queues": {},
            "api": {},
            "failures": {},
            "health": {}
        }

        # Process metrics
        if self.process_monitor:
            snapshot["system"] = self.process_monitor.get_all_health()

        # Queue metrics
        if self.queue_analytics:
            snapshot["queues"] = self.queue_analytics.get_queue_status()
            snapshot["queues"]["bottlenecks"] = (
                self.queue_analytics.identify_bottlenecks()
            )

        # API health
        if self.api_monitor:
            snapshot["api"] = self.api_monitor.get_api_status()

        # Failure analysis
        if self.failure_analyzer:
            snapshot["failures"] = self.failure_analyzer.get_failure_stats()
            snapshot["failures"]["cascade_risk"] = (
                self.failure_analyzer.predict_cascade_risk()
            )
            snapshot["failures"]["error_trends"] = (
                self.failure_analyzer.get_error_trends()
            )

        # Health dashboard
        if self.health_monitor:
            snapshot["health"] = self.health_monitor.get_dashboard()

        return snapshot

    def get_historical_metrics(
        self,
        metric_type: str,
        hours: int = 24,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get historical metrics over time.

        Args:
            metric_type: "process", "queue", "api", "failures", "health"
            hours: Hours of history to return
            limit: Max number of data points

        Returns:
            Time-series data
        """
        result = {
            "metric_type": metric_type,
            "hours": hours,
            "data": [],
            "timestamp": datetime.now().isoformat()
        }

        if metric_type == "queue" and self.queue_analytics:
            # Return queue history
            result["data"] = [
                {
                    "timestamp": s.timestamp,
                    "queue_depth": s.queue_depth,
                    "throughput": s.throughput_tasks_per_minute
                }
                for s in self.queue_analytics.queue_history[-limit:]
            ]

        elif metric_type == "process" and self.process_monitor:
            # Return process metrics history
            all_metrics = []
            for bot_id, history in self.process_monitor.metric_history.items():
                all_metrics.extend(history)

            # Sort by timestamp and limit
            all_metrics.sort(key=lambda m: m.timestamp)
            result["data"] = [
                {
                    "timestamp": m.timestamp,
                    "bot_id": m.bot_id,
                    "memory_mb": m.memory_mb,
                    "cpu_percent": m.cpu_percent
                }
                for m in all_metrics[-limit:]
            ]

        elif metric_type == "failures" and self.failure_analyzer:
            # Return failure history
            result["data"] = [
                {
                    "timestamp": f.timestamp,
                    "bot_id": f.bot_id,
                    "task_type": f.task_type,
                    "error_type": f.error_type
                }
                for f in self.failure_analyzer.failures[-limit:]
            ]

        return result

    def get_alerts(self) -> Dict[str, Any]:
        """
        Get all current alerts from all monitors.

        Returns:
            Aggregated alerts
        """
        alerts = {
            "timestamp": datetime.now().isoformat(),
            "total_alerts": 0,
            "by_severity": {"critical": [], "warning": [], "info": []},
            "sources": {}
        }

        # Process alerts
        if self.process_monitor:
            process_alerts = []
            for bot_id, alert_list in self.process_monitor.alerts.items():
                for alert in alert_list:
                    if "CRITICAL" in alert:
                        alerts["by_severity"]["critical"].append({
                            "source": "process_monitor",
                            "bot_id": bot_id,
                            "message": alert
                        })
                    else:
                        alerts["by_severity"]["warning"].append({
                            "source": "process_monitor",
                            "bot_id": bot_id,
                            "message": alert
                        })
            alerts["sources"]["process_monitor"] = len(process_alerts)

        # Failure alerts
        if self.failure_analyzer:
            cascade_risk = self.failure_analyzer.predict_cascade_risk()
            if cascade_risk["cascade_risk"] == "high":
                alerts["by_severity"]["critical"].append({
                    "source": "failure_analyzer",
                    "message": "Cascade risk detected",
                    "details": cascade_risk
                })
            elif cascade_risk["cascade_risk"] == "medium":
                alerts["by_severity"]["warning"].append({
                    "source": "failure_analyzer",
                    "message": "Elevated failure rate",
                    "details": cascade_risk
                })

        # API alerts
        if self.api_monitor:
            cascade_risk = self.api_monitor.cascade_risk
            if cascade_risk:
                alerts["by_severity"]["warning"].append({
                    "source": "api_monitor",
                    "message": f"API cascade risk: {', '.join(cascade_risk)}"
                })

        # Health alerts
        if self.health_monitor:
            dashboard = self.health_monitor.get_dashboard()
            for alert in dashboard.get("active_alerts", []):
                severity = alert.get("level", "info")
                alerts["by_severity"][severity].append({
                    "source": "health_monitor",
                    "message": alert.get("title"),
                    "details": alert
                })

        alerts["total_alerts"] = (
            len(alerts["by_severity"]["critical"]) +
            len(alerts["by_severity"]["warning"]) +
            len(alerts["by_severity"]["info"])
        )

        return alerts

    def get_system_status(self) -> Dict[str, Any]:
        """
        Get overall system status (health check).

        Returns:
            System status summary
        """
        alerts = self.get_alerts()
        critical_alerts = len(alerts["by_severity"]["critical"])
        warning_alerts = len(alerts["by_severity"]["warning"])

        if critical_alerts > 0:
            overall_status = "critical"
        elif warning_alerts > 0:
            overall_status = "warning"
        else:
            overall_status = "healthy"

        return {
            "overall_status": overall_status,
            "critical_alerts": critical_alerts,
            "warning_alerts": warning_alerts,
            "info_alerts": len(alerts["by_severity"]["info"]),
            "services": {
                "process_monitor": self.process_monitor is not None,
                "api_monitor": self.api_monitor is not None,
                "queue_analytics": self.queue_analytics is not None,
                "failure_analyzer": self.failure_analyzer is not None,
                "health_monitor": self.health_monitor is not None
            },
            "timestamp": datetime.now().isoformat()
        }

    def get_recommendations(self) -> Dict[str, Any]:
        """
        Get system recommendations based on current state.

        Returns:
            List of recommendations
        """
        recommendations = []

        # Queue recommendations
        if self.queue_analytics:
            queue_status = self.queue_analytics.get_queue_status()
            if queue_status.get("queue_depth", 0) > 10:
                recommendations.append({
                    "category": "scaling",
                    "priority": "high",
                    "message": "Consider scaling up - queue depth is high",
                    "metric": queue_status.get("queue_depth")
                })

            bottlenecks = self.queue_analytics.identify_bottlenecks()
            for bottleneck in bottlenecks.get("bottlenecks", []):
                recommendations.append({
                    "category": "bottleneck",
                    "priority": "medium",
                    "message": f"Bottleneck in {bottleneck.get('task_type')}",
                    "details": bottleneck
                })

        # Process recommendations
        if self.process_monitor:
            for bot_id, health in self.process_monitor.get_all_health().items():
                if health.get("status") == "warning":
                    recommendations.append({
                        "category": "process",
                        "priority": "medium",
                        "message": f"Bot {bot_id} has high resource usage",
                        "bot_id": bot_id
                    })

        # Failure recommendations
        if self.failure_analyzer:
            cascade_risk = self.failure_analyzer.predict_cascade_risk()
            if cascade_risk.get("cascade_risk") == "high":
                recommendations.append({
                    "category": "failure",
                    "priority": "critical",
                    "message": "Cascade failure risk detected - investigate immediately",
                    "details": cascade_risk
                })

        return {
            "recommendations": recommendations,
            "count": len(recommendations),
            "critical_count": sum(1 for r in recommendations if r.get("priority") == "critical"),
            "timestamp": datetime.now().isoformat()
        }
