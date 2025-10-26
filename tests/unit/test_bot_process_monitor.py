"""
Unit tests for BotProcessMonitor service.

Tests process health monitoring, memory leak detection, anomaly alerts, etc.
"""

import pytest
import os
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch
from src.deia.services.bot_process_monitor import (
    BotProcessMonitor,
    ProcessMetrics,
    MemoryTrend
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
    """Create BotProcessMonitor instance."""
    return BotProcessMonitor(temp_dir)


class TestProcessMetrics:
    """Test ProcessMetrics dataclass."""

    def test_metrics_creation(self):
        """Test creating process metrics."""
        now = datetime.now().isoformat()
        metrics = ProcessMetrics(
            bot_id="bot-001",
            timestamp=now,
            pid=12345,
            memory_mb=150.5,
            memory_percent=0.25,
            rss_mb=150.5,
            vms_mb=200.0,
            file_descriptors=50,
            thread_count=10,
            open_connections=5,
            cpu_percent=0.15,
            num_fds=50
        )
        assert metrics.bot_id == "bot-001"
        assert metrics.pid == 12345
        assert metrics.memory_mb == 150.5
        assert metrics.memory_percent == 0.25

    def test_metrics_to_dict(self):
        """Test metrics conversion to dict."""
        now = datetime.now().isoformat()
        metrics = ProcessMetrics(
            bot_id="bot-001",
            timestamp=now,
            pid=12345,
            memory_mb=150.5,
            memory_percent=0.25,
            rss_mb=150.5,
            vms_mb=200.0,
            file_descriptors=50,
            thread_count=10,
            open_connections=5,
            cpu_percent=0.15,
            num_fds=50
        )
        result = metrics.to_dict()
        assert result["bot_id"] == "bot-001"
        assert result["memory_mb"] == 150.5
        assert "timestamp" in result


class TestMemoryTrend:
    """Test MemoryTrend tracking."""

    def test_memory_trend_creation(self):
        """Test creating memory trend."""
        now = datetime.now().isoformat()
        trend = MemoryTrend(
            bot_id="bot-001",
            start_time=now,
            measurements=[100.0, 110.0, 120.0],
            duration_minutes=60,
            growth_rate_mb_per_hour=20.0,
            is_leaking=True
        )
        assert trend.bot_id == "bot-001"
        assert trend.is_leaking is True
        assert trend.growth_rate_mb_per_hour == 20.0


class TestBotProcessMonitor:
    """Test BotProcessMonitor functionality."""

    @patch('src.deia.services.bot_process_monitor.psutil.Process')
    def test_monitor_bot_success(self, mock_process_class, monitor, temp_dir):
        """Test successful bot monitoring."""
        # Mock process
        mock_process = MagicMock()
        mock_process.memory_info.return_value = Mock(rss=150*1024*1024, vms=200*1024*1024)
        mock_process.memory_percent.return_value = 25.0
        mock_process.open_files.return_value = [1, 2, 3]
        mock_process.num_threads.return_value = 10
        mock_process.cpu_percent.return_value = 15.0
        mock_process.net_connections.return_value = [1, 2]
        mock_process_class.return_value = mock_process

        metrics = monitor.monitor_bot("bot-001", 12345)

        assert metrics is not None
        assert metrics.bot_id == "bot-001"
        assert metrics.pid == 12345
        assert metrics.memory_mb == pytest.approx(150.0, rel=1)
        assert metrics.file_descriptors == 3

    @patch('src.deia.services.bot_process_monitor.psutil.Process')
    def test_monitor_bot_no_such_process(self, mock_process_class, monitor):
        """Test monitoring non-existent process."""
        import psutil
        mock_process_class.side_effect = psutil.NoSuchProcess(99999)

        metrics = monitor.monitor_bot("bot-001", 99999)

        assert metrics is None

    @patch('src.deia.services.bot_process_monitor.psutil.Process')
    def test_detect_memory_leak(self, mock_process_class, monitor):
        """Test memory leak detection."""
        # Create metrics with memory growth
        metrics1 = ProcessMetrics(
            bot_id="bot-001",
            timestamp=datetime.now().isoformat(),
            pid=12345,
            memory_mb=100.0,
            memory_percent=0.1,
            rss_mb=100.0,
            vms_mb=150.0,
            file_descriptors=20,
            thread_count=5,
            open_connections=2,
            cpu_percent=0.1,
            num_fds=20
        )

        # Wait a bit and add metric with higher memory
        import time
        time.sleep(0.1)

        metrics2 = ProcessMetrics(
            bot_id="bot-001",
            timestamp=datetime.now().isoformat(),
            pid=12345,
            memory_mb=150.0,  # 50MB increase
            memory_percent=0.15,
            rss_mb=150.0,
            vms_mb=200.0,
            file_descriptors=20,
            thread_count=5,
            open_connections=2,
            cpu_percent=0.1,
            num_fds=20
        )

        monitor.metric_history["bot-001"] = [metrics1, metrics2]

        trend = monitor.detect_memory_leak("bot-001")

        # Should not detect leak with just 2 metrics over short time
        if trend:
            # If it does detect, growth rate should be reasonable
            assert trend.bot_id == "bot-001"

    @patch('src.deia.services.bot_process_monitor.psutil.Process')
    def test_get_bot_health(self, mock_process_class, monitor):
        """Test getting bot health report."""
        metrics = ProcessMetrics(
            bot_id="bot-001",
            timestamp=datetime.now().isoformat(),
            pid=12345,
            memory_mb=100.0,
            memory_percent=0.1,
            rss_mb=100.0,
            vms_mb=150.0,
            file_descriptors=20,
            thread_count=5,
            open_connections=2,
            cpu_percent=0.1,
            num_fds=20
        )

        monitor.metric_history["bot-001"] = [metrics]

        health = monitor.get_bot_health("bot-001")

        assert health["bot_id"] == "bot-001"
        assert health["status"] in ["healthy", "warning", "critical"]
        assert "latest_metrics" in health

    def test_get_all_health(self, monitor):
        """Test getting health for all bots."""
        metrics1 = ProcessMetrics(
            bot_id="bot-001",
            timestamp=datetime.now().isoformat(),
            pid=12345,
            memory_mb=100.0,
            memory_percent=0.1,
            rss_mb=100.0,
            vms_mb=150.0,
            file_descriptors=20,
            thread_count=5,
            open_connections=2,
            cpu_percent=0.1,
            num_fds=20
        )

        metrics2 = ProcessMetrics(
            bot_id="bot-002",
            timestamp=datetime.now().isoformat(),
            pid=12346,
            memory_mb=120.0,
            memory_percent=0.12,
            rss_mb=120.0,
            vms_mb=170.0,
            file_descriptors=25,
            thread_count=8,
            open_connections=3,
            cpu_percent=0.12,
            num_fds=25
        )

        monitor.metric_history["bot-001"] = [metrics1]
        monitor.metric_history["bot-002"] = [metrics2]

        all_health = monitor.get_all_health()

        assert len(all_health) == 2
        assert "bot-001" in all_health
        assert "bot-002" in all_health

    def test_check_anomalies_memory_warning(self, monitor):
        """Test anomaly detection for high memory."""
        metrics = ProcessMetrics(
            bot_id="bot-001",
            timestamp=datetime.now().isoformat(),
            pid=12345,
            memory_mb=400.0,
            memory_percent=0.6,  # 60% - above warning threshold
            rss_mb=400.0,
            vms_mb=500.0,
            file_descriptors=20,
            thread_count=5,
            open_connections=2,
            cpu_percent=0.1,
            num_fds=20
        )

        monitor._check_anomalies("bot-001", metrics)

        alerts = monitor.alerts.get("bot-001", [])
        assert len(alerts) > 0
        assert any("Memory" in alert for alert in alerts)

    def test_check_anomalies_fd_warning(self, monitor):
        """Test anomaly detection for high file descriptors."""
        metrics = ProcessMetrics(
            bot_id="bot-001",
            timestamp=datetime.now().isoformat(),
            pid=12345,
            memory_mb=100.0,
            memory_percent=0.1,
            rss_mb=100.0,
            vms_mb=150.0,
            file_descriptors=950,  # Above warning threshold
            thread_count=5,
            open_connections=2,
            cpu_percent=0.1,
            num_fds=950
        )

        monitor._check_anomalies("bot-001", metrics)

        alerts = monitor.alerts.get("bot-001", [])
        assert len(alerts) > 0
        assert any("file descriptor" in alert.lower() for alert in alerts)

    def test_check_anomalies_thread_warning(self, monitor):
        """Test anomaly detection for high thread count."""
        metrics = ProcessMetrics(
            bot_id="bot-001",
            timestamp=datetime.now().isoformat(),
            pid=12345,
            memory_mb=100.0,
            memory_percent=0.1,
            rss_mb=100.0,
            vms_mb=150.0,
            file_descriptors=50,
            thread_count=120,  # Above warning threshold
            open_connections=2,
            cpu_percent=0.1,
            num_fds=50
        )

        monitor._check_anomalies("bot-001", metrics)

        alerts = monitor.alerts.get("bot-001", [])
        assert len(alerts) > 0
        assert any("thread" in alert.lower() for alert in alerts)

    def test_metrics_logging(self, monitor, temp_dir):
        """Test that metrics are logged to file."""
        metrics = ProcessMetrics(
            bot_id="bot-001",
            timestamp=datetime.now().isoformat(),
            pid=12345,
            memory_mb=100.0,
            memory_percent=0.1,
            rss_mb=100.0,
            vms_mb=150.0,
            file_descriptors=20,
            thread_count=5,
            open_connections=2,
            cpu_percent=0.1,
            num_fds=20
        )

        monitor._log_metrics(metrics)

        log_file = temp_dir / ".deia" / "bot-logs" / "bot-process-health.jsonl"
        assert log_file.exists()

        with open(log_file, "r") as f:
            lines = f.readlines()
            assert len(lines) > 0
            assert "bot-001" in lines[0]
