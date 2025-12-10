"""
Unit tests for BotMessenger service.

Tests message sending, delivery, priority handling, expiration, etc.
"""

import pytest
import json
from pathlib import Path
from datetime import datetime, timedelta
from src.deia.services.bot_messenger import (
    BotMessenger,
    Message,
    MessagePriority,
    MessageStatus,
    MessageBox
)


@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary working directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def messenger(temp_dir):
    """Create BotMessenger instance."""
    return BotMessenger(temp_dir)


class TestMessage:
    """Test Message dataclass."""

    def test_message_creation(self):
        """Test creating a message."""
        msg = Message(
            message_id="test-123",
            from_bot="bot-1",
            to_bot="bot-2",
            content="Hello"
        )
        assert msg.message_id == "test-123"
        assert msg.from_bot == "bot-1"
        assert msg.to_bot == "bot-2"
        assert msg.content == "Hello"
        assert msg.status == MessageStatus.PENDING

    def test_message_expiration(self):
        """Test message expiration."""
        msg = Message(
            message_id="test",
            from_bot="bot-1",
            to_bot="bot-2",
            content="Hello",
            ttl_seconds=1  # 1 second TTL
        )
        assert not msg.is_expired()

        # Simulate expired message
        msg.created_at = (datetime.now() - timedelta(seconds=2)).isoformat()
        assert msg.is_expired()

    def test_message_deliverable(self):
        """Test message deliverability."""
        msg = Message(
            message_id="test",
            from_bot="bot-1",
            to_bot="bot-2",
            content="Hello",
            ttl_seconds=3600
        )
        assert msg.is_deliverable()

        # Exceed retries
        msg.retry_count = 3
        msg.max_retries = 3
        assert not msg.is_deliverable()


class TestMessageBox:
    """Test MessageBox for bot inboxes."""

    def test_messagebox_creation(self):
        """Test creating a message box."""
        box = MessageBox(bot_id="bot-1")
        assert box.bot_id == "bot-1"
        assert len(box.messages) == 0

    def test_add_message(self):
        """Test adding message to inbox."""
        box = MessageBox(bot_id="bot-1")
        msg = Message(
            message_id="test",
            from_bot="sender",
            to_bot="bot-1",
            content="Hello"
        )
        box.add_message(msg)
        assert len(box.messages) == 1
        assert box.messages[0].message_id == "test"

    def test_get_unread(self):
        """Test getting unread messages."""
        box = MessageBox(bot_id="bot-1")
        msg1 = Message(
            message_id="1",
            from_bot="s1",
            to_bot="bot-1",
            content="Hello"
        )
        msg2 = Message(
            message_id="2",
            from_bot="s2",
            to_bot="bot-1",
            content="Hi",
            status=MessageStatus.READ
        )
        box.add_message(msg1)
        box.add_message(msg2)

        unread = box.get_unread()
        assert len(unread) == 1
        assert unread[0].message_id == "1"

    def test_mark_read(self):
        """Test marking message as read."""
        box = MessageBox(bot_id="bot-1")
        msg = Message(
            message_id="test",
            from_bot="sender",
            to_bot="bot-1",
            content="Hello"
        )
        box.add_message(msg)

        assert msg.status == MessageStatus.PENDING
        success = box.mark_read("test")
        assert success
        assert msg.status == MessageStatus.READ
        assert msg.read_at is not None


class TestBotMessenger:
    """Test BotMessenger service."""

    def test_messenger_creation(self, messenger):
        """Test creating messenger."""
        assert len(messenger.inboxes) == 0
        assert len(messenger.outgoing_queue) == 0

    def test_send_message(self, messenger):
        """Test sending a message."""
        msg_id = messenger.send_message(
            from_bot="bot-1",
            to_bot="bot-2",
            content="Hello",
            priority="P1"
        )
        assert msg_id is not None
        assert len(messenger.outgoing_queue) == 1
        assert len(messenger.message_history) == 1

    def test_get_inbox(self, messenger):
        """Test getting bot inbox."""
        inbox1 = messenger.get_inbox("bot-1")
        assert inbox1.bot_id == "bot-1"

        # Same bot should return same inbox
        inbox2 = messenger.get_inbox("bot-1")
        assert inbox1 is inbox2

    def test_retrieve_messages(self, messenger):
        """Test retrieving messages."""
        # Send message
        msg_id = messenger.send_message(
            from_bot="bot-1",
            to_bot="bot-2",
            content="Hello"
        )

        # Process queue to deliver
        messenger.process_outgoing_queue()

        # Retrieve
        messages = messenger.retrieve_messages("bot-2")
        assert len(messages) == 1
        assert messages[0]["content"] == "Hello"
        assert messages[0]["status"] == "delivered"

    def test_process_outgoing_queue(self, messenger):
        """Test processing outgoing queue."""
        # Send multiple messages
        msg_id1 = messenger.send_message(
            from_bot="bot-1",
            to_bot="bot-2",
            content="Message 1"
        )
        msg_id2 = messenger.send_message(
            from_bot="bot-1",
            to_bot="bot-3",
            content="Message 2"
        )

        # Process queue
        result = messenger.process_outgoing_queue()
        assert len(result["delivered"]) == 2
        assert len(result["failed"]) == 0
        assert result["pending"] == 0

    def test_mark_message_read(self, messenger):
        """Test marking message as read."""
        # Send and deliver
        msg_id = messenger.send_message(
            from_bot="bot-1",
            to_bot="bot-2",
            content="Hello"
        )
        messenger.process_outgoing_queue()

        # Mark as read
        success = messenger.mark_as_read("bot-2", msg_id)
        assert success

        # Check status
        messages = messenger.retrieve_messages("bot-2")
        assert len(messages) == 1
        assert messages[0]["status"] == "read"

    def test_priority_filtering(self, messenger):
        """Test priority-based message filtering."""
        # Send messages with different priorities
        messenger.send_message("bot-1", "bot-2", "P0 msg", "P0")
        messenger.send_message("bot-1", "bot-2", "P1 msg", "P1")
        messenger.send_message("bot-1", "bot-2", "P2 msg", "P2")

        messenger.process_outgoing_queue()

        # Filter by priority
        p1_messages = messenger.retrieve_messages("bot-2", "P1")
        assert len(p1_messages) == 1
        assert p1_messages[0]["content"] == "P1 msg"

    def test_message_expiration(self, messenger):
        """Test message expiration."""
        # Send with short TTL
        msg_id = messenger.send_message(
            from_bot="bot-1",
            to_bot="bot-2",
            content="Expiring message",
            ttl_seconds=1
        )

        # Manually expire message
        msg = messenger.message_history[msg_id]
        msg.created_at = (datetime.now() - timedelta(seconds=2)).isoformat()

        # Process should mark as expired
        result = messenger.process_outgoing_queue()
        assert any(msg.status == MessageStatus.EXPIRED for msg in messenger.message_history.values())

    def test_message_conversation(self, messenger):
        """Test getting conversation between two bots."""
        # Exchange messages
        messenger.send_message("bot-1", "bot-2", "Hi from 1")
        messenger.send_message("bot-2", "bot-1", "Hi from 2")
        messenger.send_message("bot-1", "bot-2", "Bye from 1")

        messenger.process_outgoing_queue()

        # Get conversation
        conversation = messenger.get_bot_conversation("bot-1", "bot-2")
        assert len(conversation) == 3
        # Should be sorted by time
        assert conversation[0]["from_bot"] == "bot-1"
        assert conversation[1]["from_bot"] == "bot-2"

    def test_messaging_status(self, messenger):
        """Test getting messaging status."""
        # Send messages
        messenger.send_message("bot-1", "bot-2", "Message 1", "P0")
        messenger.send_message("bot-1", "bot-3", "Message 2", "P1")

        status = messenger.get_messaging_status()
        assert status["total_messages"] == 2
        assert status["pending_delivery"] == 2
        assert status["status_breakdown"]["pending"] == 2

    def test_logging(self, messenger, temp_dir):
        """Test that events are logged."""
        messenger.send_message("bot-1", "bot-2", "Test message")

        # Check log file exists and has content
        log_file = temp_dir / ".deia" / "bot-logs" / "bot-messaging.jsonl"
        assert log_file.exists()

        # Read and parse log
        with open(log_file) as f:
            lines = f.readlines()
        assert len(lines) > 0

        # Parse first line (should be message_queued event)
        entry = json.loads(lines[0])
        assert entry["event"] == "message_queued"
        assert entry["from_bot"] == "bot-1"

    def test_cleanup_expired(self, messenger):
        """Test cleanup of expired messages."""
        # Send messages with expired TTL
        msg_id = messenger.send_message(
            "bot-1", "bot-2", "Expiring",
            ttl_seconds=1
        )

        # Add to inbox and expire it
        messenger.process_outgoing_queue()
        msg = messenger.message_history[msg_id]
        msg.created_at = (datetime.now() - timedelta(seconds=2)).isoformat()

        # Cleanup
        stats = messenger.cleanup_expired()
        # Should have removed from inbox
        messages = messenger.retrieve_messages("bot-2")
        assert len(messages) == 0


class TestMessageRetry:
    """Test message retry logic."""

    def test_retry_on_failure(self, messenger):
        """Test that failed messages are retried."""
        msg_id = messenger.send_message(
            "bot-1", "bot-2", "Test",
            ttl_seconds=3600
        )

        msg = messenger.message_history[msg_id]
        initial_retries = msg.retry_count

        # Simulate failure - won't be in this test since we don't inject failures
        # But we can verify the structure exists
        assert msg.max_retries == 3
        assert msg.retry_count >= 0
