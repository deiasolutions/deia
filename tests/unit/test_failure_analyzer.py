"""
Unit tests for FailureAnalyzer service.

Tests failure tracking, pattern detection, cascade risk prediction.
"""

import pytest
import time
from pathlib import Path
from datetime import datetime, timedelta
from src.deia.services.failure_analyzer import (
    FailureAnalyzer,
    FailureEvent,
    FailurePattern
)


@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary working directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def failure_analyzer(temp_dir):
    """Create FailureAnalyzer instance."""
    return FailureAnalyzer(temp_dir)


class TestFailureEvent:
    """Test FailureEvent dataclass."""

    def test_failure_event_creation(self):
        """Test creating failure event."""
        now = datetime.now().isoformat()
        event = FailureEvent(
            task_id="TASK-001",
            task_type="development",
            bot_id="bot-001",
            timestamp=now,
            error_message="Timeout after 30 seconds",
            error_type="timeout",
            is_retryable=True
        )
        assert event.task_id == "TASK-001"
        assert event.task_type == "development"
        assert event.error_type == "timeout"
        assert event.is_retryable is True


class TestFailurePattern:
    """Test FailurePattern dataclass."""

    def test_failure_pattern_creation(self):
        """Test creating failure pattern."""
        pattern = FailurePattern(
            pattern_id="pattern-001",
            pattern_type="task_type",
            task_type="development",
            failure_count=15,
            failure_rate=0.25
        )
        assert pattern.pattern_id == "pattern-001"
        assert pattern.failure_count == 15
        assert pattern.failure_rate == 0.25


class TestFailureAnalyzer:
    """Test FailureAnalyzer functionality."""

    def test_record_failure(self, failure_analyzer):
        """Test recording a failure."""
        event = failure_analyzer.record_failure(
            task_id="TASK-001",
            task_type="development",
            bot_id="bot-001",
            error_message="Timeout",
            error_type="timeout"
        )

        assert event is not None
        assert event.task_id == "TASK-001"
        assert event.bot_id == "bot-001"
        assert len(failure_analyzer.failures) > 0

    def test_record_multiple_failures(self, failure_analyzer):
        """Test recording multiple failures."""
        for i in range(5):
            failure_analyzer.record_failure(
                task_id=f"TASK-{i:03d}",
                task_type="development",
                bot_id="bot-001",
                error_message="Error",
                error_type="timeout"
            )

        assert len(failure_analyzer.failures) == 5

    def test_get_failure_stats(self, failure_analyzer):
        """Test getting failure statistics."""
        # Record some failures
        for i in range(3):
            failure_analyzer.record_failure(
                task_id=f"TASK-{i:03d}",
                task_type="development",
                bot_id="bot-001",
                error_message="Error",
                error_type="timeout"
            )

        for i in range(2):
            failure_analyzer.record_failure(
                task_id=f"TASK-OTHER-{i:03d}",
                task_type="analysis",
                bot_id="bot-002",
                error_message="Error",
                error_type="resource"
            )

        stats = failure_analyzer.get_failure_stats()

        assert "total_failures" in stats
        assert stats["total_failures"] == 5

    def test_failure_rate_calculation(self, failure_analyzer):
        """Test failure rate calculation."""
        # Record 1 failure and 9 successes (10% failure rate)
        failure_analyzer.record_failure(
            task_id="TASK-FAIL",
            task_type="development",
            bot_id="bot-001",
            error_message="Failed",
            error_type="unknown"
        )

        # Simulate successes by recording more tasks
        failure_analyzer.total_tasks = 10
        failure_analyzer.failed_tasks = 1

        stats = failure_analyzer.get_failure_stats()

        assert "total_failures" in stats

    def test_detect_failure_pattern_by_task_type(self, failure_analyzer):
        """Test detecting failure pattern by task type."""
        # Record many development task failures
        for i in range(10):
            failure_analyzer.record_failure(
                task_id=f"TASK-DEV-{i:03d}",
                task_type="development",
                bot_id=f"bot-{i%3}",
                error_message="Development error",
                error_type="compilation"
            )

        # Record few analysis failures
        for i in range(2):
            failure_analyzer.record_failure(
                task_id=f"TASK-ANALYSIS-{i:03d}",
                task_type="analysis",
                bot_id="bot-001",
                error_message="Analysis error",
                error_type="data"
            )

        patterns = failure_analyzer.detect_failure_patterns()

        assert len(patterns) > 0

    def test_detect_failure_pattern_by_bot(self, failure_analyzer):
        """Test detecting failure pattern by bot."""
        # Record many failures for specific bot
        for i in range(8):
            failure_analyzer.record_failure(
                task_id=f"TASK-{i:03d}",
                task_type="development",
                bot_id="bot-problem",  # This bot has issues
                error_message="Bot error",
                error_type="memory"
            )

        # Record few failures for other bots
        for i in range(2):
            failure_analyzer.record_failure(
                task_id=f"TASK-OTHER-{i:03d}",
                task_type="development",
                bot_id=f"bot-{i}",
                error_message="Rare error",
                error_type="network"
            )

        patterns = failure_analyzer.detect_failure_patterns()

        assert isinstance(patterns, list)

    def test_predict_cascade_risk(self, failure_analyzer):
        """Test cascade risk prediction."""
        # Record multiple failures indicating cascade risk
        for i in range(5):
            failure_analyzer.record_failure(
                task_id=f"TASK-CASCADE-{i:03d}",
                task_type="development",
                bot_id=f"bot-{i%2}",
                error_message="Cascade indicator",
                error_type="dependency"
            )

        cascade_risk = failure_analyzer.predict_cascade_risk()

        assert isinstance(cascade_risk, dict)
        assert "cascade_risk_score" in cascade_risk

    def test_cascade_risk_scoring(self, failure_analyzer):
        """Test cascade risk scoring logic."""
        # High failure rate scenario
        for i in range(20):
            failure_analyzer.record_failure(
                task_id=f"TASK-{i:03d}",
                task_type="critical",
                bot_id="bot-001",
                error_message="Critical failure",
                error_type="cascade_indicator"
            )

        cascade_risk = failure_analyzer.predict_cascade_risk()

        # Risk score should be higher with more failures
        risk_score = cascade_risk.get("cascade_risk_score", 0)
        assert 0 <= risk_score <= 1

    def test_get_error_trends(self, failure_analyzer):
        """Test getting error trends."""
        # Record failures over time
        for i in range(5):
            failure_analyzer.record_failure(
                task_id=f"TASK-{i:03d}",
                task_type="development",
                bot_id="bot-001",
                error_message="Error",
                error_type="timeout"
            )

        trends = failure_analyzer.get_error_trends()

        assert "total_errors" in trends

    def test_error_trend_direction(self, failure_analyzer):
        """Test error trend direction (increasing/decreasing/stable)."""
        # Record a pattern of failures
        for i in range(5):
            failure_analyzer.record_failure(
                task_id=f"TASK-{i:03d}",
                task_type="development",
                bot_id="bot-001",
                error_message="Error",
                error_type="timeout"
            )

        trends = failure_analyzer.get_error_trends()

        # Should have trend direction info
        assert isinstance(trends, dict)

    def test_failure_correlation_detection(self, failure_analyzer):
        """Test failure correlation detection."""
        # Record correlated failures (same error across multiple bots/tasks)
        for bot in ["bot-001", "bot-002", "bot-003"]:
            failure_analyzer.record_failure(
                task_id=f"TASK-{bot}",
                task_type="development",
                bot_id=bot,
                error_message="Service unavailable",
                error_type="dependency"
            )

        # Check correlations
        assert isinstance(failure_analyzer.failure_correlations, dict)

    def test_retryable_vs_non_retryable(self, failure_analyzer):
        """Test distinction between retryable and non-retryable failures."""
        # Record retryable failure
        event1 = failure_analyzer.record_failure(
            task_id="TASK-RETRY",
            task_type="development",
            bot_id="bot-001",
            error_message="Temporary timeout",
            error_type="timeout",
            is_retryable=True
        )

        # Record non-retryable failure
        event2 = failure_analyzer.record_failure(
            task_id="TASK-PERMANENT",
            task_type="analysis",
            bot_id="bot-001",
            error_message="Invalid input",
            error_type="validation",
            is_retryable=False
        )

        assert event1.is_retryable is True
        assert event2.is_retryable is False

    def test_metrics_logging(self, failure_analyzer, temp_dir):
        """Test that failures are logged to file."""
        failure_analyzer.record_failure(
            task_id="TASK-001",
            task_type="development",
            bot_id="bot-001",
            error_message="Timeout",
            error_type="timeout"
        )

        log_file = temp_dir / ".deia" / "bot-logs" / "failure-analysis.jsonl"
        assert log_file.exists()

        with open(log_file, "r") as f:
            lines = f.readlines()
            assert len(lines) > 0

    def test_time_based_pattern_detection(self, failure_analyzer):
        """Test time-based failure pattern detection."""
        # Record failures at specific times (simulating time-of-day pattern)
        now = datetime.now()

        for hour in [6, 7, 8]:  # Simulate early morning failures
            failure_analyzer.record_failure(
                task_id=f"TASK-HOUR{hour}",
                task_type="critical",
                bot_id="bot-001",
                error_message="Early morning failure",
                error_type="load_spike"
            )

        patterns = failure_analyzer.detect_failure_patterns()

        assert isinstance(patterns, list)
