"""
Codex CLI Adapter - Subprocess-based Codex integration

Wraps the codex CLI subprocess controller with bot coordination layer.
This adapter works with actual `codex` CLI sessions.
"""

from typing import Dict, Any, Optional, List, Set
from pathlib import Path
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)


class CodexCliSubprocess:
    """
    Low-level Codex subprocess controller.

    Manages spawning and communicating with `codex` CLI process.
    Captures stdout/stderr, pipes input, handles process lifecycle.
    """

    def __init__(self, work_dir: Path, codex_cli_path: str = "codex", timeout_seconds: int = 300):
        """
        Initialize Codex subprocess controller.

        Args:
            work_dir: Working directory for Codex session
            codex_cli_path: Path to codex CLI executable (default: "codex" in PATH)
            timeout_seconds: Default timeout for operations
        """
        self.work_dir = Path(work_dir)
        self.codex_cli_path = codex_cli_path
        self.timeout_seconds = timeout_seconds
        self._process = None
        self._alive = False
        self._output_buffer = []
        self._error_buffer = []

    def start(self) -> bool:
        """Start Codex subprocess."""
        try:
            import subprocess

            # Start codex CLI in interactive mode
            self._process = subprocess.Popen(
                [self.codex_cli_path, "code"],
                cwd=str(self.work_dir),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            self._alive = True
            logger.info(f"Started Codex subprocess (PID: {self._process.pid})")
            return True

        except Exception as e:
            logger.error(f"Failed to start Codex subprocess: {e}")
            self._alive = False
            return False

    def send_task(self, task_content: str, timeout: Optional[int] = None) -> 'CodexProcessResult':
        """Send task to Codex and get response."""
        if not self._alive or not self._process:
            return CodexProcessResult(
                success=False,
                output="",
                stderr="Codex process not running",
                tool_uses=[],
                duration=0,
                exit_code=None,
                timed_out=False
            )

        timeout = timeout or self.timeout_seconds
        start_time = time.time()

        try:
            # Send task to subprocess
            self._process.stdin.write(task_content + "\n")
            self._process.stdin.flush()

            # Read response with timeout
            import signal

            def timeout_handler(signum, frame):
                raise TimeoutError("Codex operation timed out")

            # Set timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)

            output = ""
            try:
                while True:
                    line = self._process.stdout.readline()
                    if not line:
                        break
                    output += line
                    self._output_buffer.append(line)
            finally:
                signal.alarm(0)  # Cancel timeout

            duration = time.time() - start_time

            return CodexProcessResult(
                success=True,
                output=output,
                stderr="",
                tool_uses=[],  # Would parse tool uses from output
                duration=duration,
                exit_code=None,
                timed_out=False
            )

        except TimeoutError:
            duration = time.time() - start_time
            return CodexProcessResult(
                success=False,
                output="",
                stderr="Operation timed out",
                tool_uses=[],
                duration=duration,
                exit_code=None,
                timed_out=True
            )
        except Exception as e:
            logger.error(f"Error sending task to Codex: {e}")
            return CodexProcessResult(
                success=False,
                output="",
                stderr=str(e),
                tool_uses=[],
                duration=time.time() - start_time,
                exit_code=None,
                timed_out=False
            )

    def terminate(self, force: bool = False) -> None:
        """Terminate Codex subprocess."""
        if not self._process:
            return

        try:
            if force:
                self._process.kill()
                logger.info("Force killed Codex subprocess")
            else:
                self._process.terminate()
                self._process.wait(timeout=5)
                logger.info("Terminated Codex subprocess gracefully")
        except Exception as e:
            logger.error(f"Error terminating Codex: {e}")
        finally:
            self._alive = False

    def is_alive(self) -> bool:
        """Check if subprocess is running."""
        if not self._process:
            return False
        return self._process.poll() is None

    def get_output_buffer(self) -> List[str]:
        """Get accumulated output."""
        return self._output_buffer

    def get_error_buffer(self) -> List[str]:
        """Get accumulated errors."""
        return self._error_buffer


class CodexProcessResult:
    """Result from Codex subprocess operation."""

    def __init__(self,
                 success: bool,
                 output: str,
                 stderr: str,
                 tool_uses: List[Dict],
                 duration: float,
                 exit_code: Optional[int],
                 timed_out: bool):
        self.success = success
        self.output = output
        self.stderr = stderr
        self.tool_uses = tool_uses
        self.duration = duration
        self.exit_code = exit_code
        self.timed_out = timed_out


class CodexCLIAdapter:
    """
    Codex CLI subprocess controller with bot coordination.

    Spawns actual `codex` CLI processes for full code editing capabilities:
    - Read, Write, Edit files
    - Execute Bash commands
    - Multi-step autonomous workflows

    This wraps the low-level subprocess controller with:
    - Bot coordination layer
    - File tracking
    - Response formatting
    - Health monitoring
    """

    def __init__(self,
                 bot_id: str,
                 work_dir: Path,
                 codex_cli_path: str = "codex",
                 timeout_seconds: int = 300):
        """
        Initialize Codex CLI adapter.

        Args:
            bot_id: Unique bot identifier (e.g., "CODEX-001")
            work_dir: Working directory for Codex session
            codex_cli_path: Path to codex CLI binary (default: "codex" in PATH)
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
        self.codex_cli_path = codex_cli_path
        self.timeout_seconds = timeout_seconds

        # Session state
        self.session_active = False
        self.started_at = None
        self.tasks_completed = 0
        self.total_files_modified = set()

        # Use subprocess controller
        self.process = CodexCliSubprocess(
            work_dir=work_dir,
            codex_cli_path=codex_cli_path,
            timeout_seconds=timeout_seconds
        )

        logger.info(f"Initialized CodexCLIAdapter: {bot_id} in {work_dir}")

    def start_session(self) -> bool:
        """
        Start Codex CLI subprocess.

        Returns:
            bool: True if session started successfully
        """
        if self.session_active:
            logger.info(f"Session already active for {self.bot_id}")
            return True

        try:
            if self.process.start():
                self.session_active = True
                self.started_at = datetime.now()
                logger.info(f"Started Codex session for {self.bot_id}")
                return True
            else:
                logger.error(f"Failed to start Codex subprocess for {self.bot_id}")
                return False

        except Exception as e:
            logger.error(f"Error starting Codex session: {e}")
            return False

    def send_task(self, task_content: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Send task to Codex and get response.

        Args:
            task_content: Task description/code
            timeout: Optional timeout override

        Returns:
            Dict: Task result with success, output, modified files
        """
        if not self.session_active:
            return {
                "success": False,
                "error": "Session not active",
                "output": "",
                "files_modified": []
            }

        try:
            result = self.process.send_task(task_content, timeout)
            self.tasks_completed += 1

            return {
                "success": result.success,
                "output": result.output,
                "error": result.stderr if result.stderr else None,
                "duration": result.duration,
                "tool_uses": result.tool_uses,
                "files_modified": [tu.get("filepath") for tu in result.tool_uses if "filepath" in tu],
                "timed_out": result.timed_out
            }

        except Exception as e:
            logger.error(f"Error sending task to Codex: {e}")
            return {
                "success": False,
                "error": str(e),
                "output": ""
            }

    def check_health(self) -> Dict[str, Any]:
        """Check session health."""
        return {
            "bot_id": self.bot_id,
            "session_active": self.session_active,
            "process_alive": self.process.is_alive(),
            "tasks_completed": self.tasks_completed,
            "uptime_seconds": (datetime.now() - self.started_at).total_seconds() if self.started_at else 0
        }

    def stop_session(self) -> bool:
        """Stop Codex session gracefully."""
        try:
            self.process.terminate(force=False)
            self.session_active = False
            logger.info(f"Stopped Codex session for {self.bot_id}")
            return True
        except Exception as e:
            logger.error(f"Error stopping session: {e}")
            return False

    def force_kill(self) -> bool:
        """Force kill Codex process."""
        try:
            self.process.terminate(force=True)
            self.session_active = False
            logger.info(f"Force killed Codex session for {self.bot_id}")
            return True
        except Exception as e:
            logger.error(f"Error force killing process: {e}")
            return False

    def get_session_info(self) -> Dict[str, Any]:
        """Get detailed session information."""
        return {
            "bot_id": self.bot_id,
            "work_dir": str(self.work_dir),
            "session_active": self.session_active,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "tasks_completed": self.tasks_completed,
            "files_modified_count": len(self.total_files_modified),
            "files_modified": list(self.total_files_modified)
        }
