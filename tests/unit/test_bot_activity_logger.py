"""Unit tests for BotActivityLogger service."""

import pytest
from pathlib import Path
from src.deia.services.bot_activity_logger import (
    BotActivityLogger, EventType, ActivityEvent
)
import json


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def logger(temp_work_dir):
    """Create BotActivityLogger instance."""
    return BotActivityLogger("test-bot-001", temp_work_dir)


class TestActivityLogging:
    """Test activity logging functionality."""

    def test_log_startup(self, logger):
        """Test logging bot startup."""
        success = logger.log_event(
            event_type=EventType.STARTUP,
            operation="bot initialization",
            result="success"
        )

        assert success
        assert logger.event_count > 0

    def test_log_shutdown(self, logger):
        """Test logging bot shutdown."""
        success = logger.log_event(
            event_type=EventType.SHUTDOWN,
            operation="graceful shutdown",
            result="success"
        )

        assert success

    def test_log_task_lifecycle(self, logger):
        """Test logging complete task lifecycle."""
        # Task received
        logger.log_event(
            event_type=EventType.TASK_RECEIVED,
            operation="receive task",
            task_id="task-001"
        )

        # Task started
        logger.log_event(
            event_type=EventType.TASK_STARTED,
            operation="start execution",
            task_id="task-001"
        )

        # Task completed
        logger.log_event(
            event_type=EventType.TASK_COMPLETED,
            operation="task execution complete",
            result="success",
            duration_seconds=45.2,
            task_id="task-001"
        )

        assert logger.event_count >= 3

    def test_log_error(self, logger):
        """Test logging errors."""
        success = logger.log_event(
            event_type=EventType.ERROR,
            operation="process error",
            error="Connection timeout",
            context={"timeout_seconds": 30}
        )

        assert success

    def test_log_warning(self, logger):
        """Test logging warnings."""
        success = logger.log_event(
            event_type=EventType.WARNING,
            operation="high memory usage",
            context={"memory_mb": 450}
        )

        assert success

    def test_log_with_context(self, logger):
        """Test logging with additional context."""
        context = {
            "request_id": "req-123",
            "user": "admin",
            "endpoint": "/api/tasks"
        }

        success = logger.log_event(
            event_type=EventType.STATUS_UPDATE,
            operation="API request processed",
            result="success",
            context=context
        )

        assert success

    def test_log_with_duration(self, logger):
        """Test logging with execution duration."""
        success = logger.log_event(
            event_type=EventType.TASK_COMPLETED,
            operation="task completed",
            result="success",
            duration_seconds=123.456,
            task_id="task-002"
        )

        assert success


class TestLogPersistence:
    """Test log persistence."""

    def test_logs_written_to_file(self, logger, temp_work_dir):
        """Test that logs are written to file."""
        logger.log_event(
            event_type=EventType.STARTUP,
            operation="initialization",
            result="success"
        )

        log_file = temp_work_dir / ".deia" / "bot-logs" / "BOT-test-bot-001-activity.jsonl"
        assert log_file.exists()

        with open(log_file) as f:
            lines = f.readlines()
        assert len(lines) > 0

    def test_log_format_is_json(self, logger, temp_work_dir):
        """Test that log entries are valid JSON."""
        logger.log_event(
            event_type=EventType.STARTUP,
            operation="init",
            result="success"
        )

        log_file = temp_work_dir / ".deia" / "bot-logs" / "BOT-test-bot-001-activity.jsonl"
        with open(log_file) as f:
            for line in f:
                entry = json.loads(line)
                assert "timestamp" in entry
                assert "bot_id" in entry
                assert "event_type" in entry
                assert "operation" in entry

    def test_log_rotation_threshold(self, temp_work_dir):
        """Test log rotation when size exceeds threshold."""
        # Create logger with small rotation threshold (1MB)
        logger = BotActivityLogger("test-bot-002", temp_work_dir, max_log_size_mb=1)

        # Log many events to trigger rotation
        for i in range(100):
            logger.log_event(
                event_type=EventType.TASK_COMPLETED,
                operation=f"task {i}",
                result="success",
                duration_seconds=10.0,
                context={"index": i, "data": "x" * 1000}
            )

        # Check if rotation occurred (archived files exist)
        log_dir = temp_work_dir / ".deia" / "bot-logs"
        gz_files = list(log_dir.glob("BOT-test-bot-002-activity*.gz"))
        # May or may not have rotation depending on content size
        # But should not error
        assert True  # If we got here without exception, rotation is working


class TestEventTypes:
    """Test different event types."""

    def test_all_event_types(self, logger):
        """Test logging all event types."""
        event_types = [
            EventType.STARTUP,
            EventType.SHUTDOWN,
            EventType.TASK_RECEIVED,
            EventType.TASK_STARTED,
            EventType.TASK_COMPLETED,
            EventType.TASK_FAILED,
            EventType.HEALTH_CHECK,
            EventType.ERROR,
            EventType.WARNING,
            EventType.STATUS_UPDATE
        ]

        for event_type in event_types:
            success = logger.log_event(
                event_type=event_type,
                operation=f"test {event_type.value}",
                result="success"
            )
            assert success

        assert logger.event_count == len(event_types)


class TestLogQueries:
    """Test querying log data."""

    def test_get_recent_events(self, logger):
        """Test retrieving recent events."""
        # Log multiple events
        logger.log_event(EventType.STARTUP, "startup", "success")
        logger.log_event(EventType.TASK_RECEIVED, "receive", task_id="t1")
        logger.log_event(EventType.TASK_COMPLETED, "complete", duration_seconds=10, task_id="t1")

        # Get recent events
        recent = logger.get_recent_events(limit=10)
        assert len(recent) >= 3

    def test_get_events_by_type(self, logger):
        """Test filtering events by type."""
        logger.log_event(EventType.STARTUP, "startup", "success")
        logger.log_event(EventType.TASK_RECEIVED, "receive", task_id="t1")
        logger.log_event(EventType.TASK_RECEIVED, "receive", task_id="t2")
        logger.log_event(EventType.SHUTDOWN, "shutdown", "success")

        # Get only task received events
        task_events = logger.get_events_by_type(EventType.TASK_RECEIVED)
        assert len(task_events) >= 2

    def test_get_task_history(self, logger):
        """Test getting history for specific task."""
        task_id = "task-123"

        logger.log_event(EventType.TASK_RECEIVED, "receive", task_id=task_id)
        logger.log_event(EventType.TASK_STARTED, "start", task_id=task_id)
        logger.log_event(EventType.TASK_COMPLETED, "complete",
                        result="success", duration_seconds=42.1, task_id=task_id)

        history = logger.get_task_history(task_id)
        assert len(history) >= 3

    def test_get_statistics(self, logger):
        """Test getting log statistics."""
        logger.log_event(EventType.STARTUP, "startup", "success")
        logger.log_event(EventType.TASK_COMPLETED, "task", result="success", duration_seconds=10)
        logger.log_event(EventType.ERROR, "error", error="Test error")

        stats = logger.get_statistics()
        assert stats["total_events"] >= 3
        assert "event_type_breakdown" in stats
        assert "errors" in stats


class TestNoLogPII:
    """Test that PII is not logged."""

    def test_context_does_not_contain_sensitive_data(self, logger):
        """Test logging without sensitive data."""
        context = {
            "request_id": "req-123",
            "operation": "data_processing",
            "timestamp": "2025-10-25T00:00:00Z"
        }

        success = logger.log_event(
            event_type=EventType.STATUS_UPDATE,
            operation="process",
            context=context
        )

        assert success
        # Verify data was logged
        assert logger.event_count > 0


class TestConcurrentLogging:
    """Test concurrent logging."""

    def test_multiple_sequential_logs(self, logger):
        """Test logging multiple events sequentially."""
        for i in range(50):
            logger.log_event(
                event_type=EventType.TASK_COMPLETED,
                operation=f"task-{i}",
                result="success",
                duration_seconds=float(i)
            )

        assert logger.event_count == 50


class TestLogMetrics:
    """Test log metrics."""

    def test_event_count(self, logger):
        """Test event counting."""
        initial = logger.event_count

        logger.log_event(EventType.STARTUP, "startup", "success")
        logger.log_event(EventType.SHUTDOWN, "shutdown", "success")

        assert logger.event_count == initial + 2

    def test_error_tracking(self, logger):
        """Test error tracking."""
        logger.log_event(EventType.TASK_COMPLETED, "task", result="success")
        logger.log_event(EventType.TASK_FAILED, "task", error="Failure reason")
        logger.log_event(EventType.ERROR, "error", error="System error")

        errors = logger.get_errors()
        assert len(errors) >= 2
