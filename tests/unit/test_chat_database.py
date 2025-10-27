"""
Tests for ChatDatabase module
"""

import pytest
import tempfile
from pathlib import Path
from deia.services.chat_database import ChatDatabase, ChatMessage


class TestChatMessage:
    """Test ChatMessage class"""

    def test_create_message(self):
        """Test creating a chat message"""
        msg = ChatMessage("BOT-001", "user", "Hello world")
        assert msg.bot_id == "BOT-001"
        assert msg.role == "user"
        assert msg.content == "Hello world"
        assert msg.timestamp is not None

    def test_message_to_dict(self):
        """Test converting message to dict"""
        msg = ChatMessage("BOT-001", "user", "Test content")
        msg_dict = msg.to_dict()
        assert msg_dict["role"] == "user"
        assert msg_dict["content"] == "Test content"
        assert msg_dict["timestamp"] is not None

    def test_message_with_custom_timestamp(self):
        """Test creating message with custom timestamp"""
        custom_ts = "2025-10-26T18:00:00"
        msg = ChatMessage("BOT-001", "assistant", "Response", timestamp=custom_ts)
        assert msg.timestamp == custom_ts


class TestChatDatabase:
    """Test ChatDatabase class"""

    @pytest.fixture
    def db(self):
        """Create temporary database for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_chat.db"
            database = ChatDatabase(str(db_path))
            yield database
            database.close()

    def test_database_initialization(self, db):
        """Test database initializes correctly"""
        assert db.db_path is not None
        assert db.conn is not None

    def test_add_single_message(self, db):
        """Test adding a single message"""
        db.add_message("BOT-001", "user", "Hello")
        messages = db.get_messages("BOT-001")
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "Hello"

    def test_add_multiple_messages(self, db):
        """Test adding multiple messages"""
        db.add_message("BOT-001", "user", "Hello")
        db.add_message("BOT-001", "assistant", "Hi there")
        db.add_message("BOT-001", "user", "How are you?")

        messages = db.get_messages("BOT-001")
        assert len(messages) == 3
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"
        assert messages[2]["role"] == "user"

    def test_get_messages_respects_limit(self, db):
        """Test that get_messages respects limit parameter"""
        for i in range(10):
            db.add_message("BOT-001", "user", f"Message {i}")

        messages = db.get_messages("BOT-001", limit=5)
        assert len(messages) == 5

    def test_messages_for_different_bots(self, db):
        """Test that messages are isolated by bot_id"""
        db.add_message("BOT-001", "user", "Bot 1 message")
        db.add_message("BOT-002", "user", "Bot 2 message")

        messages_001 = db.get_messages("BOT-001")
        messages_002 = db.get_messages("BOT-002")

        assert len(messages_001) == 1
        assert len(messages_002) == 1
        assert messages_001[0]["content"] == "Bot 1 message"
        assert messages_002[0]["content"] == "Bot 2 message"

    def test_get_messages_empty_bot(self, db):
        """Test getting messages for bot with no messages"""
        messages = db.get_messages("NONEXISTENT-BOT")
        assert len(messages) == 0

    def test_clear_messages(self, db):
        """Test clearing messages for a bot"""
        db.add_message("BOT-001", "user", "Message 1")
        db.add_message("BOT-001", "user", "Message 2")
        db.add_message("BOT-002", "user", "Other bot message")

        db.clear_messages("BOT-001")

        messages_001 = db.get_messages("BOT-001")
        messages_002 = db.get_messages("BOT-002")

        assert len(messages_001) == 0
        assert len(messages_002) == 1  # Other bot's messages unaffected

    def test_get_session_count(self, db):
        """Test getting session count (message count)"""
        db.add_message("BOT-001", "user", "Message 1")
        db.add_message("BOT-001", "assistant", "Message 2")
        db.add_message("BOT-001", "user", "Message 3")

        count = db.get_session_count("BOT-001")
        assert count == 3

    def test_invalid_role_raises_error(self, db):
        """Test that invalid role raises error"""
        with pytest.raises(ValueError):
            db.add_message("BOT-001", "invalid_role", "Content")

    def test_messages_ordered_by_timestamp(self, db):
        """Test that messages are returned in chronological order"""
        db.add_message("BOT-001", "user", "First")
        db.add_message("BOT-001", "assistant", "Second")
        db.add_message("BOT-001", "user", "Third")

        messages = db.get_messages("BOT-001")
        assert messages[0]["content"] == "First"
        assert messages[1]["content"] == "Second"
        assert messages[2]["content"] == "Third"

    def test_database_persistence(self):
        """Test that database persists data across connections"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "persistent_test.db"

            # Add messages in first connection
            db1 = ChatDatabase(str(db_path))
            db1.add_message("BOT-001", "user", "Persistent message")
            db1.close()

            # Verify messages exist in second connection
            db2 = ChatDatabase(str(db_path))
            messages = db2.get_messages("BOT-001")
            db2.close()

            assert len(messages) == 1
            assert messages[0]["content"] == "Persistent message"
