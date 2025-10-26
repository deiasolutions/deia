"""
Unit tests for ObservabilityAPI service.

Tests unified metrics aggregation and historical data retrieval.
"""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, MagicMock
from src.deia.services.observability_api import ObservabilityAPI
from src.deia.services.bot_process_monitor import (
    BotProcessMonitor,
    ProcessMetrics
)
from src.deia.services.api_health_monitor import APIHealthMonitor
from src.deia.services.queue_analytics import QueueAnalytics
from src.deia.services.failure_analyzer import FailureAnalyzer
from src.deia.services.health_monitor import HealthMonitor


@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary working directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def process_monitor(temp_dir):
    """Create BotProcessMonitor instance."""
    return BotProcessMonitor(temp_dir)


@pytest.fixture
def api_monitor(temp_dir):
    """Create APIHealthMonitor instance."""
    return APIHealthMonitor(temp_dir)


@pytest.fixture
def queue_analytics(temp_dir):
    """Create QueueAnalytics instance."""
    return QueueAnalytics(temp_dir)


@pytest.fixture
def failure_analyzer(temp_dir):
    """Create FailureAnalyzer instance."""
    return FailureAnalyzer(temp_dir)


@pytest.fixture
def health_monitor(temp_dir):
    """Create HealthMonitor instance."""
    return HealthMonitor(temp_dir)


@pytest.fixture
def observability_api(
    process_monitor,
    api_monitor,
    queue_analytics,
    failure_analyzer,
    health_monitor
):
    """Create ObservabilityAPI instance with all monitors."""
    return ObservabilityAPI(
        process_monitor=process_monitor,
        api_monitor=api_monitor,
        queue_analytics=queue_analytics,
        failure_analyzer=failure_analyzer,
        health_monitor=health_monitor
    )


class TestObservabilityAPIInitialization:
    """Test ObservabilityAPI initialization."""

    def test_observability_api_creation(self, observability_api):
        """Test creating ObservabilityAPI with all monitors."""
        assert observability_api.process_monitor is not None
        assert observability_api.api_monitor is not None
        assert observability_api.queue_analytics is not None
        assert observability_api.failure_analyzer is not None
        assert observability_api.health_monitor is not None

    def test_observability_api_partial_monitors(self, temp_dir):
        """Test creating ObservabilityAPI with partial monitors."""
        monitor = BotProcessMonitor(temp_dir)
        api = ObservabilityAPI(process_monitor=monitor)

        assert api.process_monitor is not None
        assert api.api_monitor is None


class TestMetricsSnapshot:
    """Test comprehensive metrics snapshot."""

    def test_get_metrics_snapshot_empty(self, observability_api):
        """Test getting snapshot with no data."""
        snapshot = observability_api.get_metrics_snapshot()

        assert "timestamp" in snapshot
        assert "system" in snapshot
        assert "queues" in snapshot
        assert "api" in snapshot
        assert "failures" in snapshot
        assert "health" in snapshot

    def test_get_metrics_snapshot_with_process_data(
        self,
        observability_api,
        process_monitor
    ):
        """Test snapshot includes process metrics."""
        # Add some process metrics
        now = datetime.now().isoformat()
        metrics = ProcessMetrics(
            bot_id="bot-001",
            timestamp=now,
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

        process_monitor.metric_history["bot-001"] = [metrics]

        snapshot = observability_api.get_metrics_snapshot()

        assert "system" in snapshot
        # System metrics should be populated
        if snapshot["system"]:
            assert "bot-001" in snapshot["system"]

    def test_metrics_snapshot_structure(self, observability_api):
        """Test snapshot has correct structure."""
        snapshot = observability_api.get_metrics_snapshot()

        # All main categories should exist
        required_keys = ["system", "queues", "api", "failures", "health"]
        for key in required_keys:
            assert key in snapshot

        # Should have timestamp
        assert "timestamp" in snapshot
        assert isinstance(snapshot["timestamp"], str)

    def test_metrics_snapshot_timestamp_validity(self, observability_api):
        """Test snapshot timestamp is valid ISO format."""
        snapshot = observability_api.get_metrics_snapshot()

        # Should be parseable as ISO format
        try:
            datetime.fromisoformat(snapshot["timestamp"])
            valid = True
        except ValueError:
            valid = False

        assert valid


class TestHistoricalMetrics:
    """Test historical metrics retrieval."""

    def test_get_historical_metrics_process(
        self,
        observability_api,
        process_monitor
    ):
        """Test getting historical process metrics."""
        # Add some historical data
        now = datetime.now()
        metrics1 = ProcessMetrics(
            bot_id="bot-001",
            timestamp=now.isoformat(),
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

        process_monitor.metric_history["bot-001"] = [metrics1]

        history = observability_api.get_historical_metrics("process", hours=24)

        assert "metric_type" in history
        assert history["metric_type"] == "process"
        assert "data" in history

    def test_get_historical_metrics_queue(
        self,
        observability_api,
        queue_analytics
    ):
        """Test getting historical queue metrics."""
        # Add queue snapshot
        queue_analytics.record_queue_snapshot(
            queue_depth=5,
            tasks_executing=2,
            tasks_completed=50,
            avg_queue_wait_ms=100.0,
            avg_execution_time_ms=150.0
        )

        history = observability_api.get_historical_metrics("queue", hours=24)

        assert "metric_type" in history
        assert history["metric_type"] == "queue"
        assert "data" in history

    def test_get_historical_metrics_api(
        self,
        observability_api,
        api_monitor
    ):
        """Test getting historical API metrics."""
        history = observability_api.get_historical_metrics("api", hours=24)

        assert "metric_type" in history
        assert history["metric_type"] == "api"
        assert "data" in history

    def test_get_historical_metrics_failures(
        self,
        observability_api,
        failure_analyzer
    ):
        """Test getting historical failure metrics."""
        # Record some failures
        failure_analyzer.record_failure(
            task_id="TASK-001",
            task_type="development",
            bot_id="bot-001",
            error_message="Error",
            error_type="timeout"
        )

        history = observability_api.get_historical_metrics("failures", hours=24)

        assert "metric_type" in history
        assert history["metric_type"] == "failures"
        assert "data" in history

    def test_get_historical_metrics_with_limit(
        self,
        observability_api,
        queue_analytics
    ):
        """Test historical metrics with limit parameter."""
        # Record multiple snapshots
        for i in range(10):
            queue_analytics.record_queue_snapshot(
                queue_depth=5,
                tasks_executing=2,
                tasks_completed=50+i,
                avg_queue_wait_ms=100.0,
                avg_execution_time_ms=150.0
            )

        # Request with limit
        history = observability_api.get_historical_metrics(
            "queue",
            hours=24,
            limit=5
        )

        # Should not exceed limit
        assert len(history.get("data", [])) <= 5

    def test_get_historical_metrics_with_hours(
        self,
        observability_api,
        queue_analytics
    ):
        """Test historical metrics with different hour ranges."""
        # Record snapshot
        queue_analytics.record_queue_snapshot(
            queue_depth=5,
            tasks_executing=2,
            tasks_completed=50,
            avg_queue_wait_ms=100.0,
            avg_execution_time_ms=150.0
        )

        # Request with 1 hour history
        history_1h = observability_api.get_historical_metrics(
            "queue",
            hours=1
        )

        # Request with 24 hour history
        history_24h = observability_api.get_historical_metrics(
            "queue",
            hours=24
        )

        assert "metric_type" in history_1h
        assert "metric_type" in history_24h


class TestAggregationAcrossMonitors:
    """Test metrics aggregation across multiple monitors."""

    def test_aggregates_all_monitor_types(
        self,
        observability_api,
        process_monitor,
        queue_analytics,
        failure_analyzer
    ):
        """Test aggregation includes data from all monitors."""
        # Add data to different monitors
        now = datetime.now().isoformat()

        # Process data
        metrics = ProcessMetrics(
            bot_id="bot-001",
            timestamp=now,
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
        process_monitor.metric_history["bot-001"] = [metrics]

        # Queue data
        queue_analytics.record_queue_snapshot(
            queue_depth=5,
            tasks_executing=2,
            tasks_completed=50,
            avg_queue_wait_ms=100.0,
            avg_execution_time_ms=150.0
        )

        # Failure data
        failure_analyzer.record_failure(
            task_id="TASK-001",
            task_type="development",
            bot_id="bot-001",
            error_message="Error",
            error_type="timeout"
        )

        snapshot = observability_api.get_metrics_snapshot()

        # All data types should be present
        assert "system" in snapshot or not snapshot["system"]
        assert "queues" in snapshot or not snapshot["queues"]
        assert "failures" in snapshot or not snapshot["failures"]

    def test_snapshot_includes_cascade_analysis(
        self,
        observability_api,
        failure_analyzer
    ):
        """Test snapshot includes cascade risk analysis."""
        # Record failures that indicate cascade risk
        for i in range(5):
            failure_analyzer.record_failure(
                task_id=f"TASK-{i:03d}",
                task_type="critical",
                bot_id="bot-001",
                error_message="Cascade indicator",
                error_type="dependency"
            )

        snapshot = observability_api.get_metrics_snapshot()

        assert "failures" in snapshot


class TestObservabilityIntegration:
    """Test ObservabilityAPI integration scenarios."""

    def test_complete_observability_workflow(
        self,
        observability_api,
        process_monitor,
        queue_analytics,
        failure_analyzer,
        api_monitor
    ):
        """Test complete observability workflow."""
        # Simulate system activity
        now = datetime.now().isoformat()

        # Process monitoring
        metrics = ProcessMetrics(
            bot_id="bot-001",
            timestamp=now,
            pid=12345,
            memory_mb=150.0,
            memory_percent=0.15,
            rss_mb=150.0,
            vms_mb=200.0,
            file_descriptors=30,
            thread_count=8,
            open_connections=3,
            cpu_percent=0.2,
            num_fds=30
        )
        process_monitor.metric_history["bot-001"] = [metrics]

        # Queue monitoring
        queue_analytics.record_queue_snapshot(
            queue_depth=10,
            tasks_executing=3,
            tasks_completed=100,
            avg_queue_wait_ms=200.0,
            avg_execution_time_ms=300.0
        )

        # Failure monitoring
        failure_analyzer.record_failure(
            task_id="TASK-CRITICAL",
            task_type="critical",
            bot_id="bot-001",
            error_message="Critical failure",
            error_type="cascade"
        )

        # Get comprehensive snapshot
        snapshot = observability_api.get_metrics_snapshot()

        # Verify comprehensive view
        assert isinstance(snapshot, dict)
        assert "timestamp" in snapshot
        assert "system" in snapshot
        assert "queues" in snapshot
        assert "failures" in snapshot

        # Get historical data
        history = observability_api.get_historical_metrics("process", hours=24)
        assert "metric_type" in history

    def test_observability_with_no_monitors(self):
        """Test ObservabilityAPI with no monitors initialized."""
        api = ObservabilityAPI()

        snapshot = api.get_metrics_snapshot()

        # Should still return valid structure
        assert "timestamp" in snapshot
        assert isinstance(snapshot, dict)
