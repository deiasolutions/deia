"""
Integration tests for Claude Code CLI Adapter.

Tests both the adapter layer and bot runner with mock subprocess.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import patch

from src.deia.adapters.claude_code_cli_adapter import (
    ClaudeCodeCLIAdapter,
    MockClaudeCodeProcess,
    extract_file_paths_from_tools
)
from src.deia.adapters.bot_runner import BotRunner


class TestClaudeCodeCLIAdapter:
    """Test CLI adapter with mock subprocess."""

    @pytest.fixture(autouse=True)
    def use_mock_subprocess(self):
        """Automatically use mock subprocess for all tests."""
        with patch('src.deia.adapters.claude_code_cli_adapter.ClaudeCodeProcess', MockClaudeCodeProcess):
            yield

    def test_adapter_init(self):
        """Test adapter initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)

            adapter = ClaudeCodeCLIAdapter(
                bot_id="TEST-CLI-001",
                work_dir=work_dir,
                timeout_seconds=60
            )

            assert adapter.bot_id == "TEST-CLI-001"
            assert adapter.work_dir == work_dir
            assert adapter.session_active is False

    def test_session_start(self):
        """Test starting a CLI session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)

            adapter = ClaudeCodeCLIAdapter(
                bot_id="TEST-CLI-001",
                work_dir=work_dir
            )

            success = adapter.start_session()

            assert success is True
            assert adapter.session_active is True
            assert adapter.started_at is not None

    def test_send_task_without_session(self):
        """Test that send_task fails if session not started."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)

            adapter = ClaudeCodeCLIAdapter(
                bot_id="TEST-CLI-001",
                work_dir=work_dir
            )

            result = adapter.send_task("Test task")

            assert result["success"] is False
            assert "Session not active" in result["error"]

    def test_send_task_with_session(self):
        """Test sending a task with active session (mock)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)

            adapter = ClaudeCodeCLIAdapter(
                bot_id="TEST-CLI-001",
                work_dir=work_dir
            )

            adapter.start_session()

            result = adapter.send_task("Create a test file")

            assert result["success"] is True
            assert result["output"] != ""
            assert "files_modified" in result
            assert "tool_uses" in result
            assert result["timed_out"] is False

    def test_health_check(self):
        """Test health check."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)

            adapter = ClaudeCodeCLIAdapter(
                bot_id="TEST-CLI-001",
                work_dir=work_dir
            )

            # Health check before start
            assert adapter.check_health() is False

            # Health check after start
            adapter.start_session()
            assert adapter.check_health() is True

            # Health check after stop
            adapter.stop_session()
            assert adapter.check_health() is False

    def test_session_info(self):
        """Test session info retrieval."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)

            adapter = ClaudeCodeCLIAdapter(
                bot_id="TEST-CLI-001",
                work_dir=work_dir
            )

            info = adapter.get_session_info()

            assert info["bot_id"] == "TEST-CLI-001"
            assert info["status"] == "stopped"

            adapter.start_session()
            info = adapter.get_session_info()

            assert info["status"] == "active"
            assert info["tasks_completed"] == 0

    def test_stop_and_force_kill(self):
        """Test graceful stop vs force kill."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)

            adapter = ClaudeCodeCLIAdapter(
                bot_id="TEST-CLI-001",
                work_dir=work_dir
            )

            adapter.start_session()
            assert adapter.session_active is True

            # Test graceful stop
            adapter.stop_session()
            assert adapter.session_active is False

            # Test force kill
            adapter.start_session()
            adapter.force_kill()
            assert adapter.session_active is False


class TestFilePathExtraction:
    """Test file path extraction from tool uses."""

    def test_extract_from_write_tool(self):
        """Test extraction from Write tool."""
        tool_uses = [
            {
                "name": "Write",
                "parameters": {
                    "file_path": "test.py",
                    "content": "print('hello')"
                }
            }
        ]

        files = extract_file_paths_from_tools(tool_uses)

        assert len(files) == 1
        assert Path("test.py") in files

    def test_extract_from_edit_tool(self):
        """Test extraction from Edit tool."""
        tool_uses = [
            {
                "name": "Edit",
                "parameters": {
                    "file_path": "src/main.py",
                    "old_string": "old",
                    "new_string": "new"
                }
            }
        ]

        files = extract_file_paths_from_tools(tool_uses)

        assert len(files) == 1
        assert Path("src/main.py") in files

    def test_extract_from_multiple_tools(self):
        """Test extraction from multiple tool uses."""
        tool_uses = [
            {"name": "Write", "parameters": {"file_path": "a.py"}},
            {"name": "Edit", "parameters": {"file_path": "b.py"}},
            {"name": "Read", "parameters": {"file_path": "c.py"}},  # Not extracted
            {"name": "Write", "parameters": {"file_path": "a.py"}},  # Duplicate
        ]

        files = extract_file_paths_from_tools(tool_uses)

        assert len(files) == 2  # a.py and b.py (no duplicates, no Read)
        assert Path("a.py") in files
        assert Path("b.py") in files

    def test_extract_empty_list(self):
        """Test extraction from empty tool uses."""
        files = extract_file_paths_from_tools([])

        assert len(files) == 0


class TestBotRunner:
    """Test autonomous bot runner."""

    def test_runner_init(self):
        """Test bot runner initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)
            task_dir = work_dir / "tasks"
            response_dir = work_dir / "responses"
            task_dir.mkdir()

            runner = BotRunner(
                bot_id="TEST-BOT-001",
                work_dir=work_dir,
                task_dir=task_dir,
                response_dir=response_dir,
                adapter_type="cli"
            )

            assert runner.bot_id == "TEST-BOT-001"
            assert runner.adapter_type == "cli"
            assert runner.running is False

    def test_runner_start(self):
        """Test runner start."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)
            task_dir = work_dir / "tasks"
            response_dir = work_dir / "responses"
            task_dir.mkdir()

            runner = BotRunner(
                bot_id="TEST-BOT-001",
                work_dir=work_dir,
                task_dir=task_dir,
                response_dir=response_dir,
                adapter_type="cli"
            )

            success = runner.start()

            assert success is True
            assert runner.session_started is True

    def test_run_once_no_tasks(self):
        """Test run_once with no tasks in queue."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)
            task_dir = work_dir / "tasks"
            response_dir = work_dir / "responses"
            task_dir.mkdir()

            runner = BotRunner(
                bot_id="TEST-BOT-001",
                work_dir=work_dir,
                task_dir=task_dir,
                response_dir=response_dir,
                adapter_type="cli"
            )

            runner.start()
            result = runner.run_once()

            assert result["task_found"] is False
            assert result["task_executed"] is False

    def test_run_once_with_task(self):
        """Test run_once with task in queue."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)
            task_dir = work_dir / "tasks"
            response_dir = work_dir / "responses"
            task_dir.mkdir()

            # Create a test task file
            task_file = task_dir / "2025-10-23-1234-BEE001-TEST-BOT-001-TASK-test.md"
            task_file.write_text("""# Test Task

**To:** TEST-BOT-001
**From:** BEE-001
**Priority:** P1

## Task

Create a test file.
""")

            runner = BotRunner(
                bot_id="TEST-BOT-001",
                work_dir=work_dir,
                task_dir=task_dir,
                response_dir=response_dir,
                adapter_type="cli"
            )

            runner.start()
            result = runner.run_once()

            assert result["task_found"] is True
            assert result["task_executed"] is True

            # Check response file was created
            response_files = list(response_dir.glob("*.md"))
            assert len(response_files) == 1

    def test_get_status(self):
        """Test status retrieval."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)
            task_dir = work_dir / "tasks"
            response_dir = work_dir / "responses"
            task_dir.mkdir()

            runner = BotRunner(
                bot_id="TEST-BOT-001",
                work_dir=work_dir,
                task_dir=task_dir,
                response_dir=response_dir,
                adapter_type="cli"
            )

            status = runner.get_status()

            assert status["bot_id"] == "TEST-BOT-001"
            assert status["adapter_type"] == "cli"
            assert status["running"] is False
            assert status["session_started"] is False

    def test_stop(self):
        """Test runner stop."""
        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir)
            task_dir = work_dir / "tasks"
            response_dir = work_dir / "responses"
            task_dir.mkdir()

            runner = BotRunner(
                bot_id="TEST-BOT-001",
                work_dir=work_dir,
                task_dir=task_dir,
                response_dir=response_dir,
                adapter_type="cli"
            )

            runner.start()
            runner.stop()

            assert runner.running is False
            assert runner.session_started is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
