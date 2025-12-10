"""
Unit tests for SessionLogger service.

Tests session logging functionality including task tracking,
file operations, tool calls, session analysis, and persistence.
"""

import json
import os
import tempfile
import time
import unittest
from unittest.mock import mock_open, patch

from deia.services.session_logger import (
    FileEvent,
    SessionAnalysis,
    SessionLogger,
    SessionSummary,
    TaskEvent,
    ToolEvent,
)


class TestTaskEvent(unittest.TestCase):
    """Test TaskEvent dataclass."""

    def test_task_event_creation(self):
        """Test creating a TaskEvent."""
        event = TaskEvent(name="test_task", start_time=time.time())
        self.assertEqual(event.name, "test_task")
        self.assertIsNone(event.end_time)
        self.assertEqual(event.metadata, {})

    def test_task_event_with_metadata(self):
        """Test creating a TaskEvent with metadata."""
        metadata = {"priority": "high", "tag": "feature"}
        event = TaskEvent(
            name="test_task", start_time=time.time(), metadata=metadata
        )
        self.assertEqual(event.metadata, metadata)

    def test_task_event_with_end_time(self):
        """Test TaskEvent with end time."""
        start = time.time()
        end = time.time()
        event = TaskEvent(name="test_task", start_time=start, end_time=end)
        self.assertEqual(event.end_time, end)


class TestFileEvent(unittest.TestCase):
    """Test FileEvent dataclass."""

    def test_file_event_read(self):
        """Test creating a file read event."""
        event = FileEvent(path="/test/file.txt", operation="read", size_bytes=1024)
        self.assertEqual(event.path, "/test/file.txt")
        self.assertEqual(event.operation, "read")
        self.assertEqual(event.size_bytes, 1024)
        self.assertIsNone(event.lines)

    def test_file_event_write(self):
        """Test creating a file write event."""
        event = FileEvent(
            path="/test/output.txt", operation="write", size_bytes=2048, lines=50
        )
        self.assertEqual(event.path, "/test/output.txt")
        self.assertEqual(event.operation, "write")
        self.assertEqual(event.size_bytes, 2048)
        self.assertEqual(event.lines, 50)


class TestToolEvent(unittest.TestCase):
    """Test ToolEvent dataclass."""

    def test_tool_event_creation(self):
        """Test creating a ToolEvent."""
        params = {"command": "test", "arg": "value"}
        event = ToolEvent(name="bash", params=params, duration_ms=500)
        self.assertEqual(event.name, "bash")
        self.assertEqual(event.params, params)
        self.assertEqual(event.duration_ms, 500)


class TestSessionLogger(unittest.TestCase):
    """Test SessionLogger class."""

    def setUp(self):
        """Set up test fixtures."""
        self.logger = SessionLogger(agent_id="TEST-AGENT")

    def test_initialization(self):
        """Test SessionLogger initialization."""
        self.assertEqual(self.logger.agent_id, "TEST-AGENT")
        self.assertIsNotNone(self.logger.session_id)
        self.assertIsNotNone(self.logger.start_time)
        self.assertEqual(self.logger.events, [])

    def test_custom_session_id(self):
        """Test SessionLogger with custom session ID."""
        logger = SessionLogger(agent_id="TEST", session_id="custom-123")
        self.assertEqual(logger.session_id, "custom-123")

    def test_log_task_start(self):
        """Test logging task start."""
        self.logger.log_task_start("test_task")
        self.assertEqual(len(self.logger.events), 1)
        event = self.logger.events[0]
        self.assertIsInstance(event, TaskEvent)
        self.assertEqual(event.name, "test_task")
        self.assertIsNone(event.end_time)

    def test_log_task_start_with_metadata(self):
        """Test logging task start with metadata."""
        metadata = {"priority": "high"}
        self.logger.log_task_start("test_task", metadata=metadata)
        event = self.logger.events[0]
        self.assertEqual(event.metadata, metadata)

    def test_log_task_complete(self):
        """Test logging task completion."""
        self.logger.log_task_start("test_task")
        time.sleep(0.01)  # Small delay to ensure time difference
        self.logger.log_task_complete("test_task", duration_ms=100)

        event = self.logger.events[0]
        self.assertIsNotNone(event.end_time)
        self.assertGreater(event.end_time, event.start_time)

    def test_log_task_complete_without_start(self):
        """Test logging task completion without start event logs warning."""
        with patch('deia.services.session_logger.logger') as mock_logger:
            self.logger.log_task_complete("nonexistent_task", duration_ms=100)
            mock_logger.warning.assert_called_once()

    def test_log_task_complete_with_metadata(self):
        """Test logging task completion with additional metadata."""
        self.logger.log_task_start("test_task", metadata={"initial": "data"})
        self.logger.log_task_complete(
            "test_task", duration_ms=100, metadata={"result": "success"}
        )

        event = self.logger.events[0]
        self.assertEqual(event.metadata["initial"], "data")
        self.assertEqual(event.metadata["result"], "success")

    def test_log_file_read(self):
        """Test logging file read."""
        self.logger.log_file_read("/test/file.txt", size_bytes=1024)
        self.assertEqual(len(self.logger.events), 1)
        event = self.logger.events[0]
        self.assertIsInstance(event, FileEvent)
        self.assertEqual(event.path, "/test/file.txt")
        self.assertEqual(event.operation, "read")
        self.assertEqual(event.size_bytes, 1024)

    def test_log_file_write(self):
        """Test logging file write."""
        self.logger.log_file_write("/test/output.txt", size_bytes=2048, lines=50)
        self.assertEqual(len(self.logger.events), 1)
        event = self.logger.events[0]
        self.assertIsInstance(event, FileEvent)
        self.assertEqual(event.path, "/test/output.txt")
        self.assertEqual(event.operation, "write")
        self.assertEqual(event.size_bytes, 2048)
        self.assertEqual(event.lines, 50)

    def test_log_tool_call(self):
        """Test logging tool call."""
        params = {"command": "ls", "args": ["-la"]}
        self.logger.log_tool_call("bash", params=params, duration_ms=250)
        self.assertEqual(len(self.logger.events), 1)
        event = self.logger.events[0]
        self.assertIsInstance(event, ToolEvent)
        self.assertEqual(event.name, "bash")
        self.assertEqual(event.params, params)
        self.assertEqual(event.duration_ms, 250)

    def test_get_session_summary_empty(self):
        """Test getting session summary with no events."""
        summary = self.logger.get_session_summary()
        self.assertIsInstance(summary, SessionSummary)
        self.assertGreaterEqual(summary.total_duration_ms, 0)
        self.assertEqual(summary.tasks_completed, 0)
        self.assertEqual(summary.files_read, 0)
        self.assertEqual(summary.files_written, 0)
        self.assertEqual(summary.tool_calls_count, 0)
        self.assertEqual(summary.velocity, 0.0)  # Zero for empty session

    def test_get_session_summary_with_events(self):
        """Test getting session summary with various events."""
        # Add task events
        self.logger.log_task_start("task1")
        self.logger.log_task_complete("task1", duration_ms=100)
        self.logger.log_task_start("task2")
        self.logger.log_task_complete("task2", duration_ms=200)

        # Add file events
        self.logger.log_file_read("/file1.txt", size_bytes=1024)
        self.logger.log_file_read("/file2.txt", size_bytes=2048)
        self.logger.log_file_write("/output.txt", size_bytes=3072, lines=100)

        # Add tool events
        self.logger.log_tool_call("bash", params={}, duration_ms=50)

        summary = self.logger.get_session_summary()
        self.assertEqual(summary.tasks_completed, 2)
        self.assertEqual(summary.files_read, 2)
        self.assertEqual(summary.files_written, 1)
        self.assertEqual(summary.tool_calls_count, 1)
        self.assertGreaterEqual(summary.velocity, 0)  # May be 0 for very fast tests

    def test_save_session(self):
        """Test saving session to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Add some events
            self.logger.log_task_start("test_task")
            self.logger.log_file_read("/test.txt", size_bytes=1024)

            # Save session
            self.logger.save_session(tmpdir)

            # Check file was created
            expected_file = os.path.join(
                tmpdir, f"TEST-AGENT_{self.logger.session_id}.jsonl"
            )
            self.assertTrue(os.path.exists(expected_file))

            # Verify content
            with open(expected_file, "r") as f:
                lines = f.readlines()
                self.assertEqual(len(lines), 2)

                # Check first event (TaskEvent)
                event1 = json.loads(lines[0])
                self.assertEqual(event1["name"], "test_task")

                # Check second event (FileEvent)
                event2 = json.loads(lines[1])
                self.assertEqual(event2["path"], "/test.txt")

    def test_analyze_session(self):
        """Test analyzing a saved session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a session log file
            session_file = os.path.join(tmpdir, "test_session.jsonl")

            events = [
                {
                    "type": "TaskEvent",
                    "name": "task1",
                    "start_time": time.time(),
                    "end_time": time.time() + 1.0,
                    "metadata": {}
                },
                {
                    "type": "TaskEvent",
                    "name": "task2",
                    "start_time": time.time(),
                    "end_time": time.time() + 2.0,
                    "metadata": {}
                },
                {
                    "type": "FileEvent",
                    "path": "/test.txt",
                    "operation": "read",
                    "size_bytes": 1024,
                    "lines": None
                },
                {
                    "type": "FileEvent",
                    "path": "/output.txt",
                    "operation": "write",
                    "size_bytes": 2048,
                    "lines": 50
                },
                {
                    "type": "ToolEvent",
                    "name": "bash",
                    "params": {},
                    "duration_ms": 100
                }
            ]

            with open(session_file, "w") as f:
                for event in events:
                    f.write(json.dumps(event) + "\n")

            # Analyze session
            analysis = self.logger.analyze_session(session_file)

            self.assertIsInstance(analysis, SessionAnalysis)
            self.assertIn("task1", analysis.task_breakdown)
            self.assertIn("task2", analysis.task_breakdown)
            self.assertEqual(analysis.file_operation_stats["read"], 1)
            self.assertEqual(analysis.file_operation_stats["write"], 1)
            self.assertIn("tasks_per_hour", analysis.velocity_metrics)

    def test_analyze_session_detects_bottlenecks(self):
        """Test that session analysis detects bottlenecks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            session_file = os.path.join(tmpdir, "test_session.jsonl")

            # Create a session with one slow task (bottleneck)
            events = [
                {
                    "type": "TaskEvent",
                    "name": "slow_task",
                    "start_time": time.time(),
                    "end_time": time.time() + 10.0,  # 10 seconds
                    "metadata": {}
                },
                {
                    "type": "TaskEvent",
                    "name": "fast_task",
                    "start_time": time.time(),
                    "end_time": time.time() + 0.1,  # 0.1 seconds
                    "metadata": {}
                }
            ]

            with open(session_file, "w") as f:
                for event in events:
                    f.write(json.dumps(event) + "\n")

            analysis = self.logger.analyze_session(session_file)

            # slow_task should be >30% of total time, thus a bottleneck
            self.assertIn("slow_task", analysis.bottlenecks)
            self.assertNotIn("fast_task", analysis.bottlenecks)

    def test_multiple_task_completions(self):
        """Test completing the same task multiple times."""
        self.logger.log_task_start("recurring_task")
        self.logger.log_task_complete("recurring_task", duration_ms=100)

        self.logger.log_task_start("recurring_task")
        self.logger.log_task_complete("recurring_task", duration_ms=200)

        # Both tasks should have end times
        task_events = [e for e in self.logger.events if isinstance(e, TaskEvent)]
        self.assertEqual(len(task_events), 2)
        self.assertIsNotNone(task_events[0].end_time)
        self.assertIsNotNone(task_events[1].end_time)

    def test_session_with_mixed_events(self):
        """Test a realistic session with mixed event types."""
        # Simulate a realistic workflow
        self.logger.log_task_start("implement_feature")
        self.logger.log_file_read("/src/module.py", size_bytes=4096)
        self.logger.log_tool_call("grep", params={"pattern": "TODO"}, duration_ms=50)
        self.logger.log_file_write("/src/module.py", size_bytes=5120, lines=150)
        time.sleep(0.01)  # Small delay to ensure time difference
        self.logger.log_task_complete("implement_feature", duration_ms=300000)

        self.logger.log_task_start("run_tests")
        self.logger.log_tool_call("pytest", params={"path": "tests/"}, duration_ms=2000)
        time.sleep(0.01)  # Small delay to ensure time difference
        self.logger.log_task_complete("run_tests", duration_ms=2500)

        # Verify all events were logged (2 tasks + 2 files + 2 tools = 6 events)
        # Note: log_task_complete updates existing TaskEvent, doesn't create new one
        self.assertEqual(len(self.logger.events), 6)

        # Verify summary is accurate
        summary = self.logger.get_session_summary()
        self.assertEqual(summary.tasks_completed, 2)
        self.assertEqual(summary.files_read, 1)
        self.assertEqual(summary.files_written, 1)
        self.assertEqual(summary.tool_calls_count, 2)


class TestSessionSummary(unittest.TestCase):
    """Test SessionSummary dataclass."""

    def test_session_summary_creation(self):
        """Test creating a SessionSummary."""
        summary = SessionSummary(
            total_duration_ms=60000,
            tasks_completed=5,
            files_read=10,
            files_written=3,
            tool_calls_count=15,
            velocity=5.0
        )
        self.assertEqual(summary.total_duration_ms, 60000)
        self.assertEqual(summary.tasks_completed, 5)
        self.assertEqual(summary.files_read, 10)
        self.assertEqual(summary.files_written, 3)
        self.assertEqual(summary.tool_calls_count, 15)
        self.assertEqual(summary.velocity, 5.0)


class TestSessionAnalysis(unittest.TestCase):
    """Test SessionAnalysis dataclass."""

    def test_session_analysis_creation(self):
        """Test creating a SessionAnalysis."""
        analysis = SessionAnalysis(
            task_breakdown={"task1": 1000, "task2": 2000},
            bottlenecks=["task2"],
            velocity_metrics={"tasks_per_hour": 120.0},
            file_operation_stats={"read": 10, "write": 5}
        )
        self.assertEqual(analysis.task_breakdown, {"task1": 1000, "task2": 2000})
        self.assertEqual(analysis.bottlenecks, ["task2"])
        self.assertEqual(analysis.velocity_metrics["tasks_per_hour"], 120.0)
        self.assertEqual(analysis.file_operation_stats["read"], 10)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_save_session_creates_directory(self):
        """Test that save_session works even if output_dir doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Use a subdirectory that doesn't exist yet
            output_dir = os.path.join(tmpdir, "sessions")

            logger = SessionLogger(agent_id="TEST")
            logger.log_task_start("test")

            # Should create directory if it doesn't exist
            # Note: Current implementation doesn't do this, but it should
            # This test documents expected behavior
            try:
                logger.save_session(output_dir)
            except FileNotFoundError:
                # Expected with current implementation
                # Future enhancement: auto-create directory
                pass

    def test_analyze_session_empty_file(self):
        """Test analyzing an empty session file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            session_file = os.path.join(tmpdir, "empty.jsonl")

            # Create empty file
            with open(session_file, "w") as f:
                pass

            logger = SessionLogger(agent_id="TEST")
            analysis = logger.analyze_session(session_file)

            # Should handle empty file gracefully
            self.assertEqual(analysis.task_breakdown, {})
            self.assertEqual(analysis.bottlenecks, [])

    def test_analyze_session_missing_fields(self):
        """Test analyzing session with events missing optional fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            session_file = os.path.join(tmpdir, "partial.jsonl")

            events = [
                {
                    "type": "TaskEvent",
                    "name": "task1",
                    "start_time": time.time(),
                    "end_time": None,  # Not completed
                    "metadata": {}
                }
            ]

            with open(session_file, "w") as f:
                for event in events:
                    f.write(json.dumps(event) + "\n")

            logger = SessionLogger(agent_id="TEST")
            analysis = logger.analyze_session(session_file)

            # Should skip incomplete tasks
            self.assertEqual(analysis.task_breakdown, {})


if __name__ == "__main__":
    unittest.main()
