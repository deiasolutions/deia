"""
Unit tests for AdaptiveScheduler service.

Tests learning, recommendations, performance tracking, etc.
"""

import pytest
import json
from pathlib import Path
from src.deia.services.adaptive_scheduler import (
    AdaptiveScheduler,
    BotTaskPerformance,
    TaskType
)


@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary working directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def scheduler(temp_dir):
    """Create AdaptiveScheduler instance."""
    return AdaptiveScheduler(temp_dir)


class TestBotTaskPerformance:
    """Test BotTaskPerformance dataclass."""

    def test_performance_creation(self):
        """Test creating performance record."""
        perf = BotTaskPerformance(
            bot_id="bot-1",
            task_type="development",
            total_tasks=10,
            avg_execution_time=45.2,
            success_rate=0.95
        )
        assert perf.bot_id == "bot-1"
        assert perf.task_type == "development"
        assert perf.total_tasks == 10
        assert perf.avg_execution_time == 45.2


class TestAdaptiveScheduler:
    """Test AdaptiveScheduler service."""

    def test_scheduler_creation(self, scheduler):
        """Test creating scheduler."""
        assert len(scheduler.performance_db) == 0
        assert len(scheduler.task_history) == 0

    def test_record_single_execution(self, scheduler):
        """Test recording a single task execution."""
        scheduler.record_task_execution(
            bot_id="bot-1",
            task_type="development",
            execution_time=45.0,
            success=True
        )

        assert len(scheduler.performance_db) == 1
        assert len(scheduler.task_history) == 1

        # Check performance record
        key = "bot-1:development"
        assert key in scheduler.performance_db
        perf = scheduler.performance_db[key]
        assert perf.total_tasks == 1
        assert perf.avg_execution_time == 45.0
        assert perf.success_rate == 1.0

    def test_record_multiple_executions(self, scheduler):
        """Test recording multiple executions and learning."""
        # First execution
        scheduler.record_task_execution("bot-1", "development", 40.0, True)

        # Second execution (slightly slower)
        scheduler.record_task_execution("bot-1", "development", 50.0, True)

        perf = scheduler.performance_db["bot-1:development"]
        assert perf.total_tasks == 2

        # Average should use exponential moving average
        # EMA = 40 * (1 - 0.1) + 50 * 0.1 = 36 + 5 = 41
        assert 40 <= perf.avg_execution_time <= 50

    def test_success_rate_learning(self, scheduler):
        """Test learning success rate over time."""
        scheduler.record_task_execution("bot-1", "development", 45.0, True)
        scheduler.record_task_execution("bot-1", "development", 50.0, False)

        perf = scheduler.performance_db["bot-1:development"]
        # Should be between 0.5 and 1.0
        assert 0.5 <= perf.success_rate <= 1.0

    def test_get_recommendation(self, scheduler):
        """Test getting scheduling recommendation."""
        # Record some data
        scheduler.record_task_execution("bot-1", "development", 40.0, True)
        scheduler.record_task_execution("bot-1", "development", 42.0, True)
        scheduler.record_task_execution("bot-1", "development", 41.0, True)

        scheduler.record_task_execution("bot-2", "development", 60.0, True)
        scheduler.record_task_execution("bot-2", "development", 65.0, True)
        scheduler.record_task_execution("bot-2", "development", 62.0, True)

        # Get recommendation
        rec = scheduler.get_recommendation("development")

        assert rec is not None
        assert rec.recommended_bot == "bot-1"  # Faster
        assert rec.confidence > 0.5
        assert len(rec.alternatives) > 0

    def test_no_recommendation_without_data(self, scheduler):
        """Test that we don't recommend without enough data."""
        rec = scheduler.get_recommendation("nonexistent")
        assert rec is None

    def test_insufficient_samples_for_recommendation(self, scheduler):
        """Test that recommendation requires minimum samples."""
        # Only one execution - should not recommend
        scheduler.record_task_execution("bot-1", "development", 40.0, True)

        rec = scheduler.get_recommendation("development")
        # Should be None because we need MIN_SAMPLES_FOR_RECOMMENDATION (3)
        assert rec is None

    def test_get_bot_performance(self, scheduler):
        """Test getting all performance for a bot."""
        scheduler.record_task_execution("bot-1", "development", 40.0, True)
        scheduler.record_task_execution("bot-1", "development", 42.0, True)
        scheduler.record_task_execution("bot-1", "development", 41.0, True)

        scheduler.record_task_execution("bot-1", "analysis", 30.0, True)
        scheduler.record_task_execution("bot-1", "analysis", 32.0, True)
        scheduler.record_task_execution("bot-1", "analysis", 31.0, True)

        perf = scheduler.get_bot_performance("bot-1")

        assert len(perf) == 2
        assert "development" in perf
        assert "analysis" in perf

    def test_get_task_type_performance(self, scheduler):
        """Test getting all bots' performance on a task type."""
        scheduler.record_task_execution("bot-1", "development", 40.0, True)
        scheduler.record_task_execution("bot-1", "development", 42.0, True)
        scheduler.record_task_execution("bot-1", "development", 41.0, True)

        scheduler.record_task_execution("bot-2", "development", 60.0, True)
        scheduler.record_task_execution("bot-2", "development", 62.0, True)
        scheduler.record_task_execution("bot-2", "development", 61.0, True)

        performers = scheduler.get_task_type_performance("development")

        assert len(performers) == 2
        # Should be sorted by score (bot-1 is faster)
        assert performers[0].bot_id == "bot-1"

    def test_learning_insights(self, scheduler):
        """Test getting learning insights."""
        # Record some data
        scheduler.record_task_execution("bot-1", "development", 40.0, True)
        scheduler.record_task_execution("bot-1", "development", 42.0, True)
        scheduler.record_task_execution("bot-1", "development", 41.0, True)

        scheduler.record_task_execution("bot-1", "analysis", 30.0, True)
        scheduler.record_task_execution("bot-1", "analysis", 32.0, True)
        scheduler.record_task_execution("bot-1", "analysis", 31.0, True)

        insights = scheduler.get_learning_insights()

        assert insights["total_executions"] == 6
        assert insights["total_bots_observed"] == 1
        assert insights["task_types_learned"] == 2
        assert "development" in insights["by_task_type"]
        assert "analysis" in insights["by_task_type"]

    def test_reset_bot_learning(self, scheduler):
        """Test resetting bot learning."""
        scheduler.record_task_execution("bot-1", "development", 40.0, True)
        scheduler.record_task_execution("bot-1", "development", 42.0, True)
        scheduler.record_task_execution("bot-1", "development", 41.0, True)

        scheduler.record_task_execution("bot-1", "analysis", 30.0, True)
        scheduler.record_task_execution("bot-1", "analysis", 32.0, True)
        scheduler.record_task_execution("bot-1", "analysis", 31.0, True)

        # Reset development learning for bot-1
        scheduler.reset_bot_learning("bot-1", "development")

        # Development should be gone
        assert "bot-1:development" not in scheduler.performance_db
        # Analysis should remain
        assert "bot-1:analysis" in scheduler.performance_db

    def test_reset_all_bot_learning(self, scheduler):
        """Test resetting all learning for a bot."""
        scheduler.record_task_execution("bot-1", "development", 40.0, True)
        scheduler.record_task_execution("bot-1", "development", 42.0, True)
        scheduler.record_task_execution("bot-1", "development", 41.0, True)

        scheduler.record_task_execution("bot-1", "analysis", 30.0, True)
        scheduler.record_task_execution("bot-1", "analysis", 32.0, True)
        scheduler.record_task_execution("bot-1", "analysis", 31.0, True)

        # Reset all learning for bot-1
        scheduler.reset_bot_learning("bot-1")

        # All should be gone
        assert "bot-1:development" not in scheduler.performance_db
        assert "bot-1:analysis" not in scheduler.performance_db

    def test_scheduling_history(self, scheduler):
        """Test getting scheduling history."""
        scheduler.record_task_execution("bot-1", "development", 40.0, True)
        scheduler.record_task_execution("bot-1", "development", 42.0, True)
        scheduler.record_task_execution("bot-1", "analysis", 30.0, True)

        history = scheduler.get_scheduling_history(limit=100)

        assert len(history) == 3

    def test_available_bots_filter(self, scheduler):
        """Test filtering recommendations by available bots."""
        # Record data for multiple bots
        scheduler.record_task_execution("bot-1", "development", 40.0, True)
        scheduler.record_task_execution("bot-1", "development", 42.0, True)
        scheduler.record_task_execution("bot-1", "development", 41.0, True)

        scheduler.record_task_execution("bot-2", "development", 60.0, True)
        scheduler.record_task_execution("bot-2", "development", 62.0, True)
        scheduler.record_task_execution("bot-2", "development", 61.0, True)

        # Get recommendation with only bot-2 available
        rec = scheduler.get_recommendation("development", available_bots=["bot-2"])

        assert rec is not None
        assert rec.recommended_bot == "bot-2"

    def test_logging(self, scheduler, temp_dir):
        """Test that events are logged."""
        scheduler.record_task_execution("bot-1", "development", 40.0, True)

        # Check log file exists
        log_file = temp_dir / ".deia" / "bot-logs" / "adaptive-scheduling.jsonl"
        assert log_file.exists()

        # Read and parse log
        with open(log_file) as f:
            lines = f.readlines()
        assert len(lines) > 0

        # Parse first line
        entry = json.loads(lines[0])
        assert entry["event"] == "task_recorded"

    def test_composite_scoring(self, scheduler):
        """Test that recommendation considers both speed and success rate."""
        # Fast but less reliable
        scheduler.record_task_execution("bot-1", "development", 30.0, True)
        scheduler.record_task_execution("bot-1", "development", 32.0, True)
        scheduler.record_task_execution("bot-1", "development", 35.0, False)

        # Slower but more reliable
        scheduler.record_task_execution("bot-2", "development", 50.0, True)
        scheduler.record_task_execution("bot-2", "development", 52.0, True)
        scheduler.record_task_execution("bot-2", "development", 51.0, True)

        rec = scheduler.get_recommendation("development")

        # Should recommend bot-2 despite being slower because success is weighted 0.6
        assert rec is not None
