"""
Unit tests for ConversationLogger
"""
import pytest
from pathlib import Path
import json
import sys

# Add src to path for imports
sys.path.insert(0, 'src')

from deia.logger import ConversationLogger


@pytest.mark.unit
class TestConversationLogger:
    """Test ConversationLogger class"""

    def test_logger_init(self, mock_deia_project, monkeypatch):
        """Test logger initialization"""
        monkeypatch.chdir(mock_deia_project)

        logger = ConversationLogger()
        assert logger.sessions_dir.exists()
        assert logger.index_file.exists()

    def test_create_session_log(self, mock_deia_project, monkeypatch):
        """Test creating a session log"""
        monkeypatch.chdir(mock_deia_project)

        logger = ConversationLogger()

        log_file = logger.create_session_log(
            context="Test session",
            transcript="User: Hello\nAssistant: Hi there!",
            decisions=["Use pytest", "Write tests"],
            action_items=["Create tests", "Run tests"],
            files_modified=["tests/test_logger.py"],
            next_steps="Add more tests"
        )

        # Check file was created
        assert log_file.exists()
        assert log_file.suffix == '.md'

        # Check content
        content = log_file.read_text(encoding='utf-8')
        assert 'Test session' in content
        assert 'Hello' in content
        assert 'pytest' in content

    def test_session_log_updates_index(self, mock_deia_project, monkeypatch):
        """Test that session logs update the index"""
        monkeypatch.chdir(mock_deia_project)

        logger = ConversationLogger()

        logger.create_session_log(
            context="First session",
            transcript="Test transcript",
            decisions=[],
            action_items=[],
            files_modified=[],
            next_steps="Continue"
        )

        # Check index was updated
        index_content = logger.index_file.read_text(encoding='utf-8')
        assert 'First session' in index_content

    def test_multiple_sessions(self, mock_deia_project, monkeypatch):
        """Test creating multiple session logs"""
        monkeypatch.chdir(mock_deia_project)

        logger = ConversationLogger()

        log1 = logger.create_session_log(
            context="Session 1",
            transcript="First",
            decisions=[],
            action_items=[],
            files_modified=[],
            next_steps="Next"
        )

        log2 = logger.create_session_log(
            context="Session 2",
            transcript="Second",
            decisions=[],
            action_items=[],
            files_modified=[],
            next_steps="Done"
        )

        assert log1 != log2
        assert log1.exists()
        assert log2.exists()

        # Both should be in index
        index_content = logger.index_file.read_text(encoding='utf-8')
        assert 'Session 1' in index_content
        assert 'Session 2' in index_content


@pytest.mark.unit
class TestLoggerEdgeCases:
    """Test edge cases and error handling"""

    def test_logger_without_deia_dir(self, temp_dir, monkeypatch):
        """Test logger behavior when .deia doesn't exist"""
        monkeypatch.chdir(temp_dir)

        # Should create .deia structure if missing
        logger = ConversationLogger()

        # Check it created the directories
        assert (temp_dir / '.deia').exists()
        assert (temp_dir / '.deia' / 'sessions').exists()

    def test_empty_transcript(self, mock_deia_project, monkeypatch):
        """Test creating log with empty transcript"""
        monkeypatch.chdir(mock_deia_project)

        logger = ConversationLogger()

        log_file = logger.create_session_log(
            context="Empty test",
            transcript="",
            decisions=[],
            action_items=[],
            files_modified=[],
            next_steps=""
        )

        assert log_file.exists()

    def test_long_transcript(self, mock_deia_project, monkeypatch):
        """Test creating log with very long transcript"""
        monkeypatch.chdir(mock_deia_project)

        logger = ConversationLogger()

        long_transcript = "User: Hello\n" * 1000

        log_file = logger.create_session_log(
            context="Long session",
            transcript=long_transcript,
            decisions=[],
            action_items=[],
            files_modified=[],
            next_steps=""
        )

        assert log_file.exists()
        content = log_file.read_text(encoding='utf-8')
        assert 'Hello' in content
