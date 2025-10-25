"""
Claude Code CLI Adapter - True subprocess-based Claude Code integration

Wraps the ClaudeCodeProcess subprocess controller with bot coordination layer.
This adapter works with actual `claude code` CLI sessions.
"""

from typing import Dict, Any, Optional, List, Set
from pathlib import Path
from datetime import datetime
import time

# Import real subprocess controller from BC
from .claude_cli_subprocess import ClaudeCodeProcess, extract_file_paths_from_tools

# Keep mock for backwards compatibility in tests
class MockClaudeCodeProcess:
    """Mock subprocess for development until BC delivers real implementation."""

    def __init__(self, work_dir: Path, claude_cli_path: str = "claude", timeout_seconds: int = 300):
        self.work_dir = work_dir
        self.claude_cli_path = claude_cli_path
        self.timeout_seconds = timeout_seconds
        self._alive = False
        self._output_buffer = []
        self._error_buffer = []

    def start(self) -> bool:
        """Mock start - returns True."""
        self._alive = True
        self._output_buffer = ["Claude Code CLI ready."]
        return True

    def send_task(self, task_content: str, timeout: Optional[int] = None) -> 'MockProcessResult':
        """Mock task execution."""
        from dataclasses import dataclass

        @dataclass
        class MockProcessResult:
            success: bool
            output: str
            stderr: str
            tool_uses: List[Dict[str, Any]]
            duration: float
            exit_code: Optional[int]
            timed_out: bool

        # Simulate task execution
        time.sleep(0.1)

        output = f"[MOCK] Executed task:\n{task_content[:100]}..."

        # Mock some tool uses
        tool_uses = [
            {"name": "Write", "parameters": {"file_path": "mock_test.py", "content": "# mock"}},
        ]

        return MockProcessResult(
            success=True,
            output=output,
            stderr="",
            tool_uses=tool_uses,
            duration=0.1,
            exit_code=None,
            timed_out=False
        )

    def terminate(self, force: bool = False) -> None:
        """Mock termination."""
        self._alive = False

    def is_alive(self) -> bool:
        """Mock health check."""
        return self._alive

    def get_output_buffer(self) -> List[str]:
        """Mock output buffer."""
        return self._output_buffer

    def get_error_buffer(self) -> List[str]:
        """Mock error buffer."""
        return self._error_buffer


# extract_file_paths_from_tools is now imported from claude_cli_subprocess


class ClaudeCodeCLIAdapter:
    """
    Claude Code CLI subprocess controller with bot coordination.

    Spawns actual `claude code` CLI processes for full tool access:
    - Read, Write, Edit files
    - Execute Bash commands
    - Multi-step autonomous workflows

    This wraps the low-level subprocess controller (from BC) with:
    - Bot coordination layer
    - File tracking
    - Response formatting
    - Health monitoring
    """

    def __init__(
        self,
        bot_id: str,
        work_dir: Path,
        claude_cli_path: str = "claude",
        timeout_seconds: int = 300
    ):
        """
        Initialize CLI adapter.

        Args:
            bot_id: Unique bot identifier (e.g., "CLAUDE-CODE-001")
            work_dir: Working directory for Claude Code session
            claude_cli_path: Path to claude CLI binary (default: "claude" in PATH)
            timeout_seconds: Default timeout for tasks

        Raises:
            ValueError: If bot_id is empty or work_dir doesn't exist
        """
        if not bot_id:
            raise ValueError("bot_id cannot be empty")

        if not work_dir.exists():
            raise ValueError(f"work_dir does not exist: {work_dir}")

        self.bot_id = bot_id
        self.work_dir = Path(work_dir)
        self.claude_cli_path = claude_cli_path
        self.timeout_seconds = timeout_seconds

        # Session state
        self.session_active = False
        self.started_at = None
        self.tasks_completed = 0
        self.total_files_modified = set()

        # Use real subprocess controller from BC
        self.process = ClaudeCodeProcess(
            work_dir=work_dir,
            claude_cli_path=claude_cli_path,
            timeout_seconds=timeout_seconds
        )

    def start_session(self) -> bool:
        """
        Start Claude Code CLI subprocess.

        Returns:
            True if session started successfully

        Raises:
            RuntimeError: If subprocess fails to start
        """
        if self.session_active:
            return True

        try:
            success = self.process.start()

            if success:
                self.session_active = True
                self.started_at = datetime.now().isoformat()
                return True
            else:
                raise RuntimeError("Claude Code process failed to start (returned False)")

        except Exception as e:
            raise RuntimeError(f"Failed to start Claude Code CLI: {str(e)}")

    def send_task(self, task_content: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Send task to Claude Code CLI and get response.

        Args:
            task_content: Full task specification
            timeout: Override default timeout for this task

        Returns:
            dict: {
                "success": bool,
                "output": str,
                "files_modified": List[str],
                "tool_uses": List[dict],
                "error": Optional[str],
                "duration_seconds": float,
                "timed_out": bool
            }
        """
        if not self.session_active:
            return {
                "success": False,
                "output": "",
                "files_modified": [],
                "tool_uses": [],
                "error": "Session not active. Call start_session() first.",
                "duration_seconds": 0.0,
                "timed_out": False
            }

        start_time = time.time()

        try:
            result = self.process.send_task(task_content, timeout=timeout)

            # Extract file paths from tool uses
            modified_files = extract_file_paths_from_tools(result.tool_uses)
            self.total_files_modified.update(modified_files)

            # Convert to strings for response
            files_modified_list = [str(f) for f in modified_files]

            duration = time.time() - start_time

            if result.success and not result.timed_out:
                self.tasks_completed += 1

            return {
                "success": result.success,
                "output": result.output,
                "files_modified": files_modified_list,
                "tool_uses": result.tool_uses,
                "error": result.stderr if result.stderr else None,
                "duration_seconds": round(duration, 1),
                "timed_out": result.timed_out
            }

        except Exception as e:
            duration = time.time() - start_time
            return {
                "success": False,
                "output": "",
                "files_modified": [],
                "tool_uses": [],
                "error": f"Exception during task execution: {str(e)}",
                "duration_seconds": round(duration, 1),
                "timed_out": False
            }

    def check_health(self) -> bool:
        """
        Check if Claude Code subprocess is alive.

        Returns:
            True if process is alive and responding
        """
        if not self.session_active:
            return False

        return self.process.is_alive()

    def interrupt(self) -> bool:
        """
        Send interrupt signal (Ctrl+C) to Claude Code subprocess.

        This interrupts the current operation but keeps the process alive.
        Use when bot is churning on an unwanted task.

        Returns:
            True if interrupt sent successfully

        Use cases:
            - Bot is stuck in a loop
            - ScrumMaster needs to stop current task
            - Human clicks "Stop" in dashboard
        """
        if not self.session_active:
            return False

        success = self.process.interrupt()

        if success:
            print(f"[{self.bot_id}] Interrupted current operation")

        return success

    def stop_session(self) -> None:
        """
        Terminate Claude Code subprocess gracefully.
        """
        if self.session_active:
            self.process.terminate(force=False)
            self.session_active = False

    def force_kill(self) -> None:
        """
        Force-kill Claude Code subprocess immediately.

        Use this for runaway processes or emergency shutdown.
        """
        if self.session_active:
            self.process.terminate(force=True)
            self.session_active = False

    def get_session_info(self) -> Dict[str, Any]:
        """
        Get current session metadata.

        Returns:
            dict: {
                "bot_id": str,
                "started_at": str,
                "tasks_completed": int,
                "total_files_modified": int,
                "status": str,
                "alive": bool
            }
        """
        status = "active" if self.session_active else "stopped"
        alive = self.process.is_alive() if self.session_active else False

        return {
            "bot_id": self.bot_id,
            "started_at": self.started_at or "not started",
            "tasks_completed": self.tasks_completed,
            "total_files_modified": len(self.total_files_modified),
            "status": status,
            "alive": alive,
            "work_dir": str(self.work_dir)
        }

    def get_output_logs(self) -> List[str]:
        """
        Get captured stdout logs from subprocess.

        Returns:
            List of output lines
        """
        return self.process.get_output_buffer()

    def get_error_logs(self) -> List[str]:
        """
        Get captured stderr logs from subprocess.

        Returns:
            List of error lines
        """
        return self.process.get_error_buffer()
