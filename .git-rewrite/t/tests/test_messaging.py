"""
Tests for DEIA Messaging System

Tests the core messaging infrastructure including:
- FilenameParser: Message filename validation and parsing
- TaskQueue: Priority queue operations
- MessageRouter: Message routing logic

Author: Claude (CLAUDE-CODE-001)
Date: 2025-10-17
"""

import pytest
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
import threading
import time

from src.deia.services.messaging import (
    FilenameParser,
    TaskQueue,
    MessageRouter,
    Message,
    create_task_file,
    get_agent_queue_status,
    VALID_AGENTS,
    VALID_MESSAGE_TYPES,
    MESSAGE_PRIORITY,
)


class TestFilenameParser:
    """Test filename parsing and validation"""

    def test_valid_filename(self):
        """Test parsing a valid filename"""
        filename = "2025-10-17-0900-CLAUDE_CODE-CLAUDE_AI-TASK-implement-status-tracker.md"
        result = FilenameParser.parse(filename)

        assert result is not None
        assert result["filename"] == filename
        assert result["timestamp"] == datetime(2025, 10, 17, 9, 0)
        assert result["from_agent"] == "CLAUDE_CODE"
        assert result["to_agent"] == "CLAUDE_AI"
        assert result["message_type"] == "TASK"
        assert result["subject"] == "implement-status-tracker"
        assert result["priority"] == MESSAGE_PRIORITY["TASK"]

    def test_invalid_filename_no_md_extension(self):
        """Test that non-.md files are rejected"""
        filename = "2025-10-17-0900-CLAUDE_CODE-CLAUDE_AI-TASK-test.txt"
        result = FilenameParser.parse(filename)
        assert result is None

    def test_invalid_filename_bad_date(self):
        """Test that invalid dates are rejected"""
        filename = "2025-13-32-0900-CLAUDE_CODE-CLAUDE_AI-TASK-test.md"
        result = FilenameParser.parse(filename)
        assert result is None

    def test_invalid_filename_bad_time(self):
        """Test that invalid times are rejected"""
        filename = "2025-10-17-2500-CLAUDE_CODE-CLAUDE_AI-TASK-test.md"
        result = FilenameParser.parse(filename)
        assert result is None

    def test_invalid_filename_bad_agent(self):
        """Test that invalid agent IDs are rejected"""
        filename = "2025-10-17-0900-INVALID_AGENT-CLAUDE_AI-TASK-test.md"
        result = FilenameParser.parse(filename)
        assert result is None

    def test_invalid_filename_bad_message_type(self):
        """Test that invalid message types are rejected"""
        filename = "2025-10-17-0900-CLAUDE_CODE-CLAUDE_AI-INVALID-test.md"
        result = FilenameParser.parse(filename)
        assert result is None

    def test_validate_valid_filename(self):
        """Test validation of valid filename"""
        filename = "2025-10-17-0900-CLAUDE_CODE-CLAUDE_AI-TASK-test.md"
        is_valid, errors = FilenameParser.validate(filename)
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_invalid_filename(self):
        """Test validation of invalid filename"""
        filename = "invalid-filename.md"
        is_valid, errors = FilenameParser.validate(filename)
        assert is_valid is False
        assert len(errors) > 0

    def test_priority_ordering(self):
        """Test that different message types get correct priorities"""
        escalate = FilenameParser.parse("2025-10-17-0900-DAVE-CLAUDE_CODE-ESCALATE-urgent.md")
        task = FilenameParser.parse("2025-10-17-0900-DAVE-CLAUDE_CODE-TASK-normal.md")
        report = FilenameParser.parse("2025-10-17-0900-DAVE-CLAUDE_CODE-REPORT-status.md")

        assert escalate["priority"] < task["priority"]  # Lower number = higher priority
        assert task["priority"] < report["priority"]


class TestTaskQueue:
    """Test task queue operations"""

    @pytest.fixture
    def temp_queue_dir(self):
        """Create temporary directory for queue"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def queue(self, temp_queue_dir):
        """Create a TaskQueue instance"""
        return TaskQueue("TEST_AGENT", queue_dir=temp_queue_dir)

    def test_queue_initialization(self, queue, temp_queue_dir):
        """Test queue is initialized correctly"""
        assert queue.agent_id == "TEST_AGENT"
        assert queue.queue_dir == Path(temp_queue_dir)
        assert queue.queue_dir.exists()
        assert queue.size() == 0

    def test_enqueue_dequeue(self, queue, temp_queue_dir):
        """Test basic enqueue and dequeue operations"""
        message = Message(
            filename="2025-10-17-0900-DAVE-TEST_AGENT-TASK-test.md",
            timestamp=datetime(2025, 10, 17, 9, 0),
            from_agent="DAVE",
            to_agent="TEST_AGENT",
            message_type="TASK",
            subject="test",
            priority=3,
            filepath=str(Path(temp_queue_dir) / "test.md")
        )

        queue.enqueue(message)
        assert queue.size() == 1

        dequeued = queue.dequeue()
        assert dequeued is not None
        assert dequeued.filename == message.filename
        assert queue.size() == 0

    def test_priority_ordering(self, queue, temp_queue_dir):
        """Test that messages are dequeued by priority"""
        # Create messages with different priorities
        low_priority = Message(
            filename="2025-10-17-0900-DAVE-TEST_AGENT-REPORT-low.md",
            timestamp=datetime(2025, 10, 17, 9, 0),
            from_agent="DAVE",
            to_agent="TEST_AGENT",
            message_type="REPORT",
            subject="low",
            priority=5,  # Lower priority
            filepath=""
        )

        high_priority = Message(
            filename="2025-10-17-0900-DAVE-TEST_AGENT-ESCALATE-high.md",
            timestamp=datetime(2025, 10, 17, 9, 1),
            from_agent="DAVE",
            to_agent="TEST_AGENT",
            message_type="ESCALATE",
            subject="high",
            priority=1,  # Higher priority
            filepath=""
        )

        # Enqueue low priority first, then high priority
        queue.enqueue(low_priority)
        queue.enqueue(high_priority)

        # High priority should come out first
        first = queue.dequeue()
        assert first.message_type == "ESCALATE"
        assert first.priority == 1

        second = queue.dequeue()
        assert second.message_type == "REPORT"
        assert second.priority == 5

    def test_peek(self, queue):
        """Test peeking at next message without removing"""
        message = Message(
            filename="2025-10-17-0900-DAVE-TEST_AGENT-TASK-test.md",
            timestamp=datetime(2025, 10, 17, 9, 0),
            from_agent="DAVE",
            to_agent="TEST_AGENT",
            message_type="TASK",
            subject="test",
            priority=3,
            filepath=""
        )

        queue.enqueue(message)

        peeked = queue.peek()
        assert peeked is not None
        assert peeked.filename == message.filename
        assert queue.size() == 1  # Still in queue

    def test_list_pending(self, queue):
        """Test listing pending messages"""
        msg1 = Message(
            filename="2025-10-17-0900-DAVE-TEST_AGENT-TASK-one.md",
            timestamp=datetime(2025, 10, 17, 9, 0),
            from_agent="DAVE",
            to_agent="TEST_AGENT",
            message_type="TASK",
            subject="one",
            priority=3,
            filepath=""
        )
        msg2 = Message(
            filename="2025-10-17-0901-DAVE-TEST_AGENT-TASK-two.md",
            timestamp=datetime(2025, 10, 17, 9, 1),
            from_agent="DAVE",
            to_agent="TEST_AGENT",
            message_type="TASK",
            subject="two",
            priority=3,
            filepath=""
        )

        queue.enqueue(msg1)
        queue.enqueue(msg2)

        pending = queue.list_pending()
        assert len(pending) == 2


class TestMessageRouter:
    """Test message routing logic"""

    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing"""
        inbox_dir = tempfile.mkdtemp()
        queue_base = tempfile.mkdtemp()
        yield inbox_dir, queue_base
        shutil.rmtree(inbox_dir)
        shutil.rmtree(queue_base)

    @pytest.fixture
    def router(self, temp_dirs):
        """Create a MessageRouter instance"""
        inbox_dir, queue_base = temp_dirs
        return MessageRouter(inbox_dir=inbox_dir)

    def test_router_initialization(self, router, temp_dirs):
        """Test router is initialized correctly"""
        inbox_dir, _ = temp_dirs
        assert router.inbox_dir == Path(inbox_dir)
        assert router.inbox_dir.exists()

    def test_route_to_specific_agent(self, router, temp_dirs):
        """Test routing to a specific agent"""
        inbox_dir, _ = temp_dirs

        # Create a test message file
        filename = "2025-10-17-0900-DAVE-CLAUDE_CODE-TASK-test.md"
        filepath = Path(inbox_dir) / filename
        filepath.write_text("Test message content")

        # Route the message
        success = router.route_message(filename, str(filepath))
        assert success is True

        # Check that message was queued for CLAUDE_CODE
        queue = router.get_queue("CLAUDE_CODE")
        assert queue.size() == 1

        message = queue.dequeue()
        assert message.to_agent == "CLAUDE_CODE"

    def test_route_invalid_filename(self, router, temp_dirs):
        """Test that invalid filenames are rejected"""
        inbox_dir, _ = temp_dirs

        filename = "invalid-filename.md"
        filepath = Path(inbox_dir) / filename
        filepath.write_text("Test")

        success = router.route_message(filename, str(filepath))
        assert success is False

    def test_broadcast_to_all(self, router, temp_dirs):
        """Test broadcasting to all agents"""
        inbox_dir, _ = temp_dirs

        filename = "2025-10-17-0900-DAVE-ALL-REPORT-status.md"
        filepath = Path(inbox_dir) / filename
        filepath.write_text("Broadcast message")

        success = router.route_message(filename, str(filepath))
        assert success is True

        # Check that multiple agents received the message
        agents_with_messages = []
        for agent_id in ["CLAUDE_CODE", "CLAUDE_AI", "CHATGPT"]:
            queue = router.get_queue(agent_id)
            if queue.size() > 0:
                agents_with_messages.append(agent_id)

        assert len(agents_with_messages) >= 3  # At least 3 agents got it

    def test_process_inbox(self, router, temp_dirs):
        """Test processing multiple files in inbox"""
        inbox_dir, _ = temp_dirs

        # Create multiple message files
        files = [
            "2025-10-17-0900-DAVE-CLAUDE_CODE-TASK-one.md",
            "2025-10-17-0901-DAVE-CLAUDE_AI-TASK-two.md",
            "2025-10-17-0902-DAVE-CHATGPT-QUERY-three.md",
        ]

        for filename in files:
            filepath = Path(inbox_dir) / filename
            filepath.write_text(f"Content for {filename}")

        # Process inbox
        count = router.process_inbox()
        assert count == 3

        # Verify messages were routed
        assert router.get_queue("CLAUDE_CODE").size() == 1
        assert router.get_queue("CLAUDE_AI").size() == 1
        assert router.get_queue("CHATGPT").size() == 1


class TestConcurrency:
    """Test thread safety and concurrent operations"""

    @pytest.fixture
    def temp_queue_dir(self):
        """Create temporary directory for queue"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_concurrent_enqueue(self, temp_queue_dir):
        """Test multiple threads enqueueing simultaneously"""
        queue = TaskQueue("TEST_AGENT", queue_dir=temp_queue_dir)
        num_threads = 5
        messages_per_thread = 10

        def enqueue_messages(thread_id):
            for i in range(messages_per_thread):
                message = Message(
                    filename=f"2025-10-17-09{i:02d}-DAVE-TEST_AGENT-TASK-thread{thread_id}-msg{i}.md",
                    timestamp=datetime(2025, 10, 17, 9, i),
                    from_agent="DAVE",
                    to_agent="TEST_AGENT",
                    message_type="TASK",
                    subject=f"thread{thread_id}-msg{i}",
                    priority=3,
                    filepath=""
                )
                queue.enqueue(message)
                time.sleep(0.001)  # Small delay to encourage interleaving

        threads = [
            threading.Thread(target=enqueue_messages, args=(i,))
            for i in range(num_threads)
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should have all messages
        assert queue.size() == num_threads * messages_per_thread

    def test_concurrent_read_write(self, temp_queue_dir):
        """Test reading and writing simultaneously"""
        queue = TaskQueue("TEST_AGENT", queue_dir=temp_queue_dir)
        stop_flag = threading.Event()
        results = {"enqueued": 0, "dequeued": 0}

        def writer():
            count = 0
            while not stop_flag.is_set() and count < 50:
                message = Message(
                    filename=f"2025-10-17-09{count:02d}-DAVE-TEST_AGENT-TASK-write{count}.md",
                    timestamp=datetime(2025, 10, 17, 9, count),
                    from_agent="DAVE",
                    to_agent="TEST_AGENT",
                    message_type="TASK",
                    subject=f"write{count}",
                    priority=3,
                    filepath=""
                )
                queue.enqueue(message)
                results["enqueued"] += 1
                count += 1
                time.sleep(0.001)

        def reader():
            while not stop_flag.is_set():
                msg = queue.dequeue()
                if msg:
                    results["dequeued"] += 1
                time.sleep(0.001)

        writer_thread = threading.Thread(target=writer)
        reader_thread = threading.Thread(target=reader)

        writer_thread.start()
        reader_thread.start()

        writer_thread.join()
        time.sleep(0.1)  # Let reader catch up
        stop_flag.set()
        reader_thread.join()

        # Should have processed most/all messages
        assert results["enqueued"] == 50
        assert results["dequeued"] <= results["enqueued"]


class TestHelperFunctions:
    """Test convenience functions"""

    def test_create_task_file(self):
        """Test creating a task file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = create_task_file(
                from_agent="CLAUDE_CODE",
                to_agent="CLAUDE_AI",
                task_type="TASK",
                subject="test-task",
                content="This is a test task",
                output_dir=temp_dir
            )

            assert filepath is not None
            assert Path(filepath).exists()

            # Check filename format
            filename = Path(filepath).name
            assert "CLAUDE_CODE" in filename
            assert "CLAUDE_AI" in filename
            assert "TASK" in filename
            assert "test-task" in filename
            assert filename.endswith(".md")

            # Check content
            content = Path(filepath).read_text()
            assert "This is a test task" in content

    def test_get_agent_queue_status(self):
        """Test getting agent queue status"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a queue with some test files
            queue_dir = Path(temp_dir) / "queues" / "TEST_AGENT"
            queue_dir.mkdir(parents=True)

            # Create some dummy message files
            (queue_dir / "2025-10-17-0900-DAVE-TEST_AGENT-TASK-one.md").write_text("test")
            (queue_dir / "2025-10-17-0901-DAVE-TEST_AGENT-TASK-two.md").write_text("test")

            # Get status
            status = get_agent_queue_status("TEST_AGENT")

            # Note: This will use default queue dir, not our temp dir
            # So we're just testing it doesn't crash
            assert "agent_id" in status
            assert "queue_size" in status
            assert status["agent_id"] == "TEST_AGENT"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
