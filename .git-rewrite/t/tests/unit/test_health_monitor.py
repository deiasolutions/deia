"""
Unit tests for HealthMonitor service.

Tests alert generation, health evaluation, dashboard data, etc.
"""

import pytest
import json
from pathlib import Path
from src.deia.services.health_monitor import (
    HealthMonitor,
    Alert,
    AlertLevel,
    AlertType,
    SystemHealthMetrics
)


@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary working directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def monitor(temp_dir):
    """Create HealthMonitor instance."""
    return HealthMonitor(temp_dir)


class TestAlert:
    """Test Alert dataclass."""

    def test_alert_creation(self):
        """Test creating an alert."""
        alert = Alert(
            alert_id="test-1",
            alert_type=AlertType.CPU_HIGH,
            level=AlertLevel.WARNING,
            title="High CPU",
            message="CPU at 80%"
        )
        assert alert.alert_id == "test-1"
        assert alert.level == AlertLevel.WARNING
        assert not alert.resolved

    def test_alert_resolution(self):
        """Test resolving an alert."""
        alert = Alert(
            alert_id="test-1",
            alert_type=AlertType.CPU_HIGH,
            level=AlertLevel.WARNING,
            title="High CPU",
            message="CPU at 80%"
        )
        assert not alert.resolved

        alert.resolved = True
        assert alert.resolved


class TestSystemHealthMetrics:
    """Test SystemHealthMetrics dataclass."""

    def test_metrics_creation(self):
        """Test creating metrics."""
        metrics = SystemHealthMetrics(
            timestamp="2025-10-25T12:00:00",
            total_bots=5,
            active_bots=4,
            queued_tasks=2,
            avg_bot_load=0.65,
            system_cpu_percent=0.45,
            system_memory_percent=0.60,
            message_queue_size=1,
            pending_message_failures=0,
            avg_success_rate=0.95
        )
        assert metrics.total_bots == 5
        assert metrics.active_bots == 4


class TestHealthMonitor:
    """Test HealthMonitor service."""

    def test_monitor_creation(self, monitor):
        """Test creating monitor."""
        assert len(monitor.alerts) == 0
        assert len(monitor.alert_history) == 0

    def test_evaluate_health_healthy(self, monitor):
        """Test evaluating healthy system."""
        metrics = monitor.evaluate_health(
            total_bots=5,
            active_bots=5,
            queued_tasks=0,
            avg_bot_load=0.3,
            system_cpu_percent=0.4,
            system_memory_percent=0.5,
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.99
        )

        assert metrics.total_bots == 5
        # Should have no critical alerts
        critical = [a for a in monitor.alerts.values() if not a.resolved and a.level == AlertLevel.CRITICAL]
        assert len(critical) == 0

    def test_cpu_critical_alert(self, monitor):
        """Test CPU critical alert generation."""
        metrics = monitor.evaluate_health(
            total_bots=5,
            active_bots=5,
            queued_tasks=0,
            avg_bot_load=0.3,
            system_cpu_percent=0.96,  # Critical
            system_memory_percent=0.5,
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.99
        )

        # Should have CPU alert
        cpu_alert = [a for a in monitor.alerts.values() if a.alert_type == AlertType.CPU_HIGH]
        assert len(cpu_alert) > 0
        assert cpu_alert[0].level == AlertLevel.CRITICAL

    def test_cpu_warning_alert(self, monitor):
        """Test CPU warning alert."""
        metrics = monitor.evaluate_health(
            total_bots=5,
            active_bots=5,
            queued_tasks=0,
            avg_bot_load=0.3,
            system_cpu_percent=0.85,  # Warning threshold
            system_memory_percent=0.5,
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.99
        )

        cpu_alert = [a for a in monitor.alerts.values() if a.alert_type == AlertType.CPU_HIGH]
        assert len(cpu_alert) > 0
        assert cpu_alert[0].level == AlertLevel.WARNING

    def test_memory_critical_alert(self, monitor):
        """Test memory critical alert."""
        metrics = monitor.evaluate_health(
            total_bots=5,
            active_bots=5,
            queued_tasks=0,
            avg_bot_load=0.3,
            system_cpu_percent=0.4,
            system_memory_percent=0.91,  # Critical
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.99
        )

        mem_alert = [a for a in monitor.alerts.values() if a.alert_type == AlertType.MEMORY_HIGH]
        assert len(mem_alert) > 0
        assert mem_alert[0].level == AlertLevel.CRITICAL

    def test_queue_backlog_alert(self, monitor):
        """Test queue backlog alert."""
        metrics = monitor.evaluate_health(
            total_bots=5,
            active_bots=5,
            queued_tasks=15,  # Over threshold
            avg_bot_load=0.3,
            system_cpu_percent=0.4,
            system_memory_percent=0.5,
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.99
        )

        queue_alert = [a for a in monitor.alerts.values() if a.alert_type == AlertType.QUEUE_BACKLOG]
        assert len(queue_alert) > 0
        assert queue_alert[0].level == AlertLevel.WARNING

    def test_bot_offline_alert(self, monitor):
        """Test bot offline alert."""
        metrics = monitor.evaluate_health(
            total_bots=5,
            active_bots=2,  # 3 offline
            queued_tasks=0,
            avg_bot_load=0.3,
            system_cpu_percent=0.4,
            system_memory_percent=0.5,
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.99
        )

        bot_alert = [a for a in monitor.alerts.values() if a.alert_type == AlertType.BOT_FAILURE]
        assert len(bot_alert) > 0
        assert bot_alert[0].level == AlertLevel.WARNING

    def test_low_success_rate_alert(self, monitor):
        """Test low success rate alert."""
        metrics = monitor.evaluate_health(
            total_bots=5,
            active_bots=5,
            queued_tasks=0,
            avg_bot_load=0.3,
            system_cpu_percent=0.4,
            system_memory_percent=0.5,
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.25  # Low
        )

        rate_alert = [a for a in monitor.alerts.values() if a.alert_type == AlertType.LOW_SUCCESS_RATE]
        assert len(rate_alert) > 0
        assert rate_alert[0].level == AlertLevel.WARNING

    def test_message_delivery_alert(self, monitor):
        """Test message delivery failure alert."""
        metrics = monitor.evaluate_health(
            total_bots=5,
            active_bots=5,
            queued_tasks=0,
            avg_bot_load=0.3,
            system_cpu_percent=0.4,
            system_memory_percent=0.5,
            message_queue_size=0,
            pending_message_failures=6,  # Over threshold
            avg_success_rate=0.99
        )

        msg_alert = [a for a in monitor.alerts.values() if a.alert_type == AlertType.MESSAGE_DELIVERY_FAILED]
        assert len(msg_alert) > 0

    def test_resource_exhausted_alert(self, monitor):
        """Test resource exhausted alert."""
        metrics = monitor.evaluate_health(
            total_bots=5,
            active_bots=5,
            queued_tasks=0,
            avg_bot_load=0.3,
            system_cpu_percent=0.92,  # Both high
            system_memory_percent=0.86,
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.99
        )

        exhaust_alert = [a for a in monitor.alerts.values() if a.alert_type == AlertType.RESOURCE_EXHAUSTED]
        assert len(exhaust_alert) > 0
        assert exhaust_alert[0].level == AlertLevel.CRITICAL

    def test_resolve_alert(self, monitor):
        """Test resolving an alert."""
        # Generate alert
        metrics = monitor.evaluate_health(
            total_bots=5, active_bots=5, queued_tasks=15, avg_bot_load=0.3,
            system_cpu_percent=0.4, system_memory_percent=0.5,
            message_queue_size=0, pending_message_failures=0, avg_success_rate=0.99
        )

        queue_alert_id = [a for a in monitor.alerts.values() if a.alert_type == AlertType.QUEUE_BACKLOG][0].alert_id

        # Resolve it
        success = monitor.resolve_alert(queue_alert_id)
        assert success

        # Check it's resolved
        alert = monitor.alerts[queue_alert_id]
        assert alert.resolved

    def test_get_dashboard(self, monitor):
        """Test getting dashboard data."""
        metrics = monitor.evaluate_health(
            total_bots=5, active_bots=5, queued_tasks=2, avg_bot_load=0.5,
            system_cpu_percent=0.4, system_memory_percent=0.5,
            message_queue_size=1, pending_message_failures=0, avg_success_rate=0.95
        )

        dashboard = monitor.get_dashboard()

        assert "overall_status" in dashboard
        assert "health_score" in dashboard
        assert "metrics" in dashboard
        assert "active_alerts" in dashboard
        assert "bot_health" in dashboard
        assert "system_resources" in dashboard

    def test_health_score_calculation(self, monitor):
        """Test health score calculation."""
        # Healthy system
        monitor.evaluate_health(
            total_bots=5, active_bots=5, queued_tasks=0, avg_bot_load=0.3,
            system_cpu_percent=0.3, system_memory_percent=0.4,
            message_queue_size=0, pending_message_failures=0, avg_success_rate=0.99
        )

        dashboard = monitor.get_dashboard()
        healthy_score = dashboard["health_score"]

        # System with issues
        monitor2 = HealthMonitor(monitor.work_dir)
        monitor2.evaluate_health(
            total_bots=5, active_bots=2, queued_tasks=20, avg_bot_load=0.8,
            system_cpu_percent=0.95, system_memory_percent=0.92,
            message_queue_size=5, pending_message_failures=10, avg_success_rate=0.5
        )

        dashboard2 = monitor2.get_dashboard()
        unhealthy_score = dashboard2["health_score"]

        # Healthy score should be higher
        assert healthy_score > unhealthy_score

    def test_get_alerts_filtered(self, monitor):
        """Test getting filtered alerts."""
        metrics = monitor.evaluate_health(
            total_bots=5, active_bots=5, queued_tasks=15, avg_bot_load=0.3,
            system_cpu_percent=0.96, system_memory_percent=0.91,
            message_queue_size=0, pending_message_failures=0, avg_success_rate=0.99
        )

        # Get critical alerts
        critical = monitor.get_alerts(level="critical")
        assert len(critical) > 0
        assert all(a["level"] == "critical" for a in critical)

        # Get warning alerts
        warnings = monitor.get_alerts(level="warning")
        assert len(warnings) > 0

    def test_logging(self, monitor, temp_dir):
        """Test that events are logged."""
        metrics = monitor.evaluate_health(
            total_bots=5, active_bots=5, queued_tasks=15, avg_bot_load=0.3,
            system_cpu_percent=0.4, system_memory_percent=0.5,
            message_queue_size=0, pending_message_failures=0, avg_success_rate=0.99
        )

        # Check alert log
        log_file = temp_dir / ".deia" / "bot-logs" / "health-alerts.jsonl"
        assert log_file.exists()

        # Check metrics log
        metrics_log = temp_dir / ".deia" / "bot-logs" / "health-metrics.jsonl"
        assert metrics_log.exists()

    def test_alert_persistence_across_evaluations(self, monitor):
        """Test that alerts persist across evaluations."""
        # First evaluation generates queue alert
        metrics1 = monitor.evaluate_health(
            total_bots=5, active_bots=5, queued_tasks=15, avg_bot_load=0.3,
            system_cpu_percent=0.4, system_memory_percent=0.5,
            message_queue_size=0, pending_message_failures=0, avg_success_rate=0.99
        )

        alerts_after_first = len([a for a in monitor.alerts.values() if not a.resolved])

        # Second evaluation with same issue
        metrics2 = monitor.evaluate_health(
            total_bots=5, active_bots=5, queued_tasks=16, avg_bot_load=0.3,
            system_cpu_percent=0.4, system_memory_percent=0.5,
            message_queue_size=0, pending_message_failures=0, avg_success_rate=0.99
        )

        alerts_after_second = len([a for a in monitor.alerts.values() if not a.resolved])

        # Should be same or similar (not doubled)
        assert alerts_after_second <= alerts_after_first + 1

    def test_alert_resolution_on_improvement(self, monitor):
        """Test that alerts are resolved when issue is fixed."""
        # First evaluation with high CPU
        metrics1 = monitor.evaluate_health(
            total_bots=5, active_bots=5, queued_tasks=0, avg_bot_load=0.3,
            system_cpu_percent=0.96, system_memory_percent=0.5,
            message_queue_size=0, pending_message_failures=0, avg_success_rate=0.99
        )

        cpu_alerts = [a for a in monitor.alerts.values() if a.alert_type == AlertType.CPU_HIGH and not a.resolved]
        assert len(cpu_alerts) > 0

        # Second evaluation with normal CPU
        metrics2 = monitor.evaluate_health(
            total_bots=5, active_bots=5, queued_tasks=0, avg_bot_load=0.3,
            system_cpu_percent=0.5, system_memory_percent=0.5,
            message_queue_size=0, pending_message_failures=0, avg_success_rate=0.99
        )

        # CPU alert should be resolved
        cpu_alerts_resolved = [a for a in monitor.alerts.values() if a.alert_type == AlertType.CPU_HIGH and not a.resolved]
        assert len(cpu_alerts_resolved) == 0
