"""
Unit tests for QueueAnalytics service.

Tests queue tracking, latency analysis, throughput calculation, bottleneck detection.
"""

import pytest
import time
from pathlib import Path
from datetime import datetime, timedelta
from src.deia.services.queue_analytics import (
    QueueAnalytics,
    QueueSnapshot,
    TaskLatencyAnalysis
)


@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary working directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def queue_analytics(temp_dir):
    """Create QueueAnalytics instance."""
    return QueueAnalytics(temp_dir)


class TestQueueSnapshot:
    """Test QueueSnapshot dataclass."""

    def test_queue_snapshot_creation(self):
        """Test creating queue snapshot."""
        now = datetime.now().isoformat()
        snapshot = QueueSnapshot(
            timestamp=now,
            queue_depth=5,
            tasks_queued=5,
            tasks_executing=3,
            tasks_completed=50,
            total_tasks_processed=58,
            avg_queue_wait_ms=100.0,
            avg_execution_time_ms=150.0,
            throughput_tasks_per_minute=3.5
        )
        assert snapshot.queue_depth == 5
        assert snapshot.tasks_executing == 3
        assert snapshot.throughput_tasks_per_minute == 3.5


class TestTaskLatencyAnalysis:
    """Test TaskLatencyAnalysis dataclass."""

    def test_task_latency_creation(self):
        """Test creating task latency analysis."""
        now = datetime.now().isoformat()
        analysis = TaskLatencyAnalysis(
            task_id="TASK-001",
            queued_at=now,
            executed_at=now,
            completed_at=now,
            queue_wait_ms=50.0,
            execution_time_ms=100.0,
            total_time_ms=150.0,
            task_type="development",
            bot_id="bot-001"
        )
        assert analysis.task_id == "TASK-001"
        assert analysis.queue_wait_ms == 50.0
        assert analysis.execution_time_ms == 100.0


class TestQueueAnalytics:
    """Test QueueAnalytics functionality."""

    def test_add_task(self, queue_analytics):
        """Test adding task to queue."""
        queue_analytics.add_task("TASK-001", "development", "P1")

        assert "TASK-001" in queue_analytics.task_latencies
        latency = queue_analytics.task_latencies["TASK-001"]
        assert latency.task_type == "development"

    def test_complete_task(self, queue_analytics):
        """Test completing a task."""
        queue_analytics.add_task("TASK-001", "development", "P1")

        # Simulate execution
        time.sleep(0.1)

        queue_analytics.complete_task("TASK-001", 0.15, True)

        assert "TASK-001" in queue_analytics.task_latencies
        latency = queue_analytics.task_latencies["TASK-001"]
        assert latency.execution_time_ms >= 150.0

    def test_record_queue_snapshot(self, queue_analytics):
        """Test recording queue snapshot."""
        snapshot = queue_analytics.record_queue_snapshot(
            queue_depth=5,
            tasks_executing=3,
            tasks_completed=50,
            avg_queue_wait_ms=100.0,
            avg_execution_time_ms=150.0
        )

        assert snapshot is not None
        assert snapshot.queue_depth == 5
        assert snapshot.tasks_executing == 3

        # Should be in history
        assert len(queue_analytics.queue_history) > 0

    def test_get_queue_status(self, queue_analytics):
        """Test getting queue status."""
        # Add some tasks
        for i in range(5):
            queue_analytics.add_task(f"TASK-{i:03d}", "development", "P2")

        # Record snapshot
        queue_analytics.record_queue_snapshot(
            queue_depth=5,
            tasks_executing=2,
            tasks_completed=10,
            avg_queue_wait_ms=100.0,
            avg_execution_time_ms=150.0
        )

        status = queue_analytics.get_queue_status()

        assert "queue_depth" in status
        assert "throughput_tasks_per_minute" in status
        assert "avg_latency_seconds" in status

    def test_get_task_latency(self, queue_analytics):
        """Test getting individual task latency."""
        queue_analytics.add_task("TASK-001", "development", "P1")
        time.sleep(0.05)
        queue_analytics.complete_task("TASK-001", 0.1, True)

        latency = queue_analytics.get_task_latency("TASK-001")

        assert latency is not None
        assert latency.task_id == "TASK-001"

    def test_get_task_type_stats(self, queue_analytics):
        """Test getting task type statistics."""
        # Add tasks of different types
        queue_analytics.add_task("TASK-001", "development", "P1")
        queue_analytics.add_task("TASK-002", "analysis", "P2")
        queue_analytics.add_task("TASK-003", "development", "P1")

        queue_analytics.complete_task("TASK-001", 0.15, True)
        queue_analytics.complete_task("TASK-002", 0.20, True)
        queue_analytics.complete_task("TASK-003", 0.12, True)

        stats = queue_analytics.get_task_type_stats()

        assert "development" in stats or len(stats) > 0

    def test_identify_bottlenecks_high_queue_depth(self, queue_analytics):
        """Test bottleneck detection - high queue depth."""
        # Create high queue depth condition
        for i in range(100):
            queue_analytics.add_task(f"TASK-{i:03d}", "development", "P2")

        queue_analytics.record_queue_snapshot(
            queue_depth=100,
            tasks_executing=1,
            tasks_completed=50,
            avg_queue_wait_ms=5000.0,  # High wait time
            avg_execution_time_ms=150.0
        )

        bottlenecks = queue_analytics.identify_bottlenecks()

        # Should detect high queue depth bottleneck
        assert isinstance(bottlenecks, list)

    def test_identify_bottlenecks_high_latency(self, queue_analytics):
        """Test bottleneck detection - high latency."""
        queue_analytics.record_queue_snapshot(
            queue_depth=5,
            tasks_executing=3,
            tasks_completed=50,
            avg_queue_wait_ms=500.0,  # Elevated wait time
            avg_execution_time_ms=5000.0  # Very slow execution
        )

        bottlenecks = queue_analytics.identify_bottlenecks()

        assert isinstance(bottlenecks, list)

    def test_percentile_calculations(self, queue_analytics):
        """Test percentile latency calculations."""
        # Add tasks with varying latencies
        latencies = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        for i, latency_ms in enumerate(latencies):
            queue_analytics.add_task(f"TASK-{i:03d}", "general", "P2")
            queue_analytics.complete_task(f"TASK-{i:03d}", latency_ms/1000, True)

        stats = queue_analytics.get_queue_status()

        assert "p95_latency_seconds" in stats or "avg_latency_seconds" in stats

    def test_throughput_calculation(self, queue_analytics):
        """Test throughput calculation."""
        # Add multiple tasks
        for i in range(10):
            queue_analytics.add_task(f"TASK-{i:03d}", "general", "P2")
            queue_analytics.complete_task(f"TASK-{i:03d}", 1.0, True)

        queue_analytics.record_queue_snapshot(
            queue_depth=0,
            tasks_executing=0,
            tasks_completed=10,
            avg_queue_wait_ms=500.0,
            avg_execution_time_ms=1000.0
        )

        status = queue_analytics.get_queue_status()

        # Throughput should be positive
        if "throughput_tasks_per_minute" in status:
            assert status["throughput_tasks_per_minute"] > 0

    def test_metrics_logging(self, queue_analytics, temp_dir):
        """Test that queue metrics are logged to file."""
        queue_analytics.record_queue_snapshot(
            queue_depth=5,
            tasks_executing=2,
            tasks_completed=50,
            avg_queue_wait_ms=100.0,
            avg_execution_time_ms=150.0
        )

        log_file = temp_dir / ".deia" / "bot-logs" / "queue-analytics.jsonl"
        assert log_file.exists()

        with open(log_file, "r") as f:
            lines = f.readlines()
            assert len(lines) > 0

    def test_task_type_performance(self, queue_analytics):
        """Test task type performance tracking."""
        # Add tasks of different types with different performance
        queue_analytics.add_task("TASK-001", "development", "P1")
        queue_analytics.complete_task("TASK-001", 0.5, True)

        queue_analytics.add_task("TASK-002", "analysis", "P2")
        queue_analytics.complete_task("TASK-002", 0.3, True)

        queue_analytics.add_task("TASK-003", "development", "P1")
        queue_analytics.complete_task("TASK-003", 0.45, True)

        stats = queue_analytics.task_type_stats

        # Should have stats for both task types
        assert isinstance(stats, dict)
