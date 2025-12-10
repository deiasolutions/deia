"""
Tests for the CLI log command
"""

import pytest
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock, call
from deia.cli_log import log


class TestLogCommand:
    """Test deia log command"""

    def test_log_with_auto_flag(self):
        """Test log command with --auto flag shows coming soon message"""
        runner = CliRunner()
        result = runner.invoke(log, ['--auto'])

        assert result.exit_code == 0
        assert "Auto-logging feature coming soon" in result.output

    def test_log_with_context_and_transcript_file(self, tmp_path):
        """Test log command with context and transcript file"""
        # Create a transcript file
        transcript_file = tmp_path / "transcript.txt"
        transcript_file.write_text("User: Hello\nAssistant: Hi there!")

        runner = CliRunner()

        with patch('deia.cli_log.ConversationLogger') as mock_logger:
            mock_instance = MagicMock()
            mock_logger.return_value = mock_instance
            mock_instance.create_session_log.return_value = Path(".deia/sessions/test.md")
            mock_instance.index_file = Path(".deia/sessions/INDEX.md")

            # Mock all the prompts to return empty strings
            with patch('deia.cli_log.Prompt.ask', side_effect=["", "", "", "Continue"]):
                result = runner.invoke(log, [
                    '--context', 'Testing feature X',
                    '--transcript', str(transcript_file)
                ])

                assert result.exit_code == 0
                assert mock_instance.create_session_log.called

                # Verify the logger was called with correct arguments
                call_args = mock_instance.create_session_log.call_args
                assert call_args[1]['context'] == 'Testing feature X'
                assert call_args[1]['transcript'] == "User: Hello\nAssistant: Hi there!"
                assert call_args[1]['status'] == 'Completed'

    def test_log_with_nonexistent_transcript_file(self):
        """Test log command with nonexistent transcript file"""
        runner = CliRunner()

        result = runner.invoke(log, [
            '--context', 'Testing',
            '--transcript', '/nonexistent/file.txt'
        ])

        assert result.exit_code == 0
        assert "Transcript file not found" in result.output

    def test_log_prompts_for_context_when_not_provided(self):
        """Test that log command prompts for context if not provided"""
        runner = CliRunner()

        with patch('deia.cli_log.ConversationLogger') as mock_logger:
            mock_instance = MagicMock()
            mock_logger.return_value = mock_instance
            mock_instance.create_session_log.return_value = Path(".deia/sessions/test.md")
            mock_instance.index_file = Path(".deia/sessions/INDEX.md")

            with patch('deia.cli_log.Prompt.ask', side_effect=[
                "Working on feature Y",  # context
                "",  # decisions
                "",  # action_items
                "",  # files
                "Continue from here"  # next_steps
            ]):
                result = runner.invoke(log, [])

                assert result.exit_code == 0
                assert mock_instance.create_session_log.called

    def test_log_without_transcript_shows_note(self):
        """Test log command without transcript shows note message"""
        runner = CliRunner()

        with patch('deia.cli_log.ConversationLogger') as mock_logger:
            mock_instance = MagicMock()
            mock_logger.return_value = mock_instance
            mock_instance.create_session_log.return_value = Path(".deia/sessions/test.md")
            mock_instance.index_file = Path(".deia/sessions/INDEX.md")

            with patch('deia.cli_log.Prompt.ask', side_effect=[
                "Test context",
                "",  # decisions
                "",  # action_items
                "",  # files
                "Next steps"
            ]):
                result = runner.invoke(log, ['--context', 'Test'])

                assert result.exit_code == 0
                assert "No transcript provided" in result.output

    def test_log_with_all_optional_details(self):
        """Test log command with all optional details provided"""
        runner = CliRunner()

        with patch('deia.cli_log.ConversationLogger') as mock_logger:
            mock_instance = MagicMock()
            mock_logger.return_value = mock_instance
            mock_instance.create_session_log.return_value = Path(".deia/sessions/test.md")
            mock_instance.index_file = Path(".deia/sessions/INDEX.md")

            with patch('deia.cli_log.Prompt.ask', side_effect=[
                "Decision A, Decision B",  # decisions
                "Task 1, Task 2",  # action_items
                "file1.py, file2.md",  # files_modified
                "Continue work"  # next_steps
            ]):
                result = runner.invoke(log, ['--context', 'Full details test'])

                assert result.exit_code == 0
                call_args = mock_instance.create_session_log.call_args
                assert call_args[1]['decisions'] == ["Decision A", "Decision B"]
                assert call_args[1]['action_items'] == ["Task 1", "Task 2"]
                assert call_args[1]['files_modified'] == ["file1.py", "file2.md"]

    def test_log_creates_logger_instance(self):
        """Test that log command creates ConversationLogger instance"""
        runner = CliRunner()

        with patch('deia.cli_log.ConversationLogger') as mock_logger:
            mock_instance = MagicMock()
            mock_logger.return_value = mock_instance
            mock_instance.create_session_log.return_value = Path(".deia/sessions/test.md")
            mock_instance.index_file = Path(".deia/sessions/INDEX.md")

            with patch('deia.cli_log.Prompt.ask', side_effect=[
                "Context",
                "",  # decisions
                "",  # action_items
                "",  # files
                "Next"
            ]):
                result = runner.invoke(log, ['--context', 'Test'])

                assert result.exit_code == 0
                assert mock_logger.called

    def test_log_shows_success_message(self):
        """Test that log command shows success message"""
        runner = CliRunner()

        with patch('deia.cli_log.ConversationLogger') as mock_logger:
            mock_instance = MagicMock()
            mock_logger.return_value = mock_instance
            mock_instance.create_session_log.return_value = Path(".deia/sessions/20251006-test.md")
            mock_instance.index_file = Path(".deia/sessions/INDEX.md")

            with patch('deia.cli_log.Prompt.ask', side_effect=[
                "Test",
                "",  # decisions
                "",  # action_items
                "",  # files
                "Next"
            ]):
                result = runner.invoke(log, ['--context', 'Test'])

                assert result.exit_code == 0
                assert "Conversation logged successfully" in result.output
                assert "20251006-test" in result.output
