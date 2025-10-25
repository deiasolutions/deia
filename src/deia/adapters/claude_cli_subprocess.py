"""
claude_cli_subprocess.py

Core subprocess management for Claude Code CLI integration.
Handles process spawning, stream capture, task submission, and termination.

This module provides low-level process control for spawning and managing
'claude code' CLI processes. It captures output streams in background threads,
submits tasks via stdin, parses XML tool invocations, and enforces timeouts.
"""

from typing import Optional, List, Dict, Any, Set
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import subprocess
import threading
import time
import re
import sys
import os


class ProcessState(Enum):
    """Claude Code process states."""
    NOT_STARTED = "not_started"
    STARTING = "starting"
    READY = "ready"
    PROCESSING = "processing"
    ERROR = "error"
    TERMINATED = "terminated"


@dataclass
class ProcessResult:
    """Result from Claude Code process execution."""
    success: bool
    output: str
    stderr: str
    tool_uses: List[Dict[str, Any]]
    duration: float
    exit_code: Optional[int]
    timed_out: bool


class ClaudeCodeProcess:
    """
    Claude Code CLI subprocess manager.

    Handles:
    - Process spawning and termination
    - Stream capture with background threads
    - Task submission via stdin
    - XML tool use parsing
    - Timeout enforcement

    Example:
        process = ClaudeCodeProcess(work_dir=Path("/project"))
        if process.start():
            result = process.send_task("Create test.py")
            process.terminate()
    """

    def __init__(
        self,
        work_dir: Path,
        claude_cli_path: str = "claude",
        timeout_seconds: int = 300
    ):
        """
        Initialize process manager.

        Args:
            work_dir: Working directory for claude code process
            claude_cli_path: Path to claude CLI (default: "claude" in PATH)
            timeout_seconds: Default timeout for tasks (default: 300)
        """
        self.work_dir = Path(work_dir).resolve()
        self.claude_cli_path = claude_cli_path
        self.timeout_seconds = timeout_seconds

        self.process: Optional[subprocess.Popen] = None
        self.state = ProcessState.NOT_STARTED

        self.output_buffer: List[str] = []
        self.error_buffer: List[str] = []

        self._stop_event: Optional[threading.Event] = None
        self._stdout_thread: Optional[threading.Thread] = None
        self._stderr_thread: Optional[threading.Thread] = None
        self._buffer_lock = threading.Lock()

    def start(self) -> bool:
        """
        Start claude code subprocess.

        Returns:
            True if started successfully, False otherwise

        Process:
            1. Verify work_dir exists
            2. Spawn subprocess with pipes
            3. Start background capture threads
            4. Wait for ready signal (10 second timeout)
            5. Return success status
        """
        if self.state not in [ProcessState.NOT_STARTED, ProcessState.TERMINATED]:
            return False

        try:
            self.state = ProcessState.STARTING

            # Verify working directory exists
            if not self.work_dir.exists():
                try:
                    self.work_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    self._append_error(f"Failed to create work_dir: {e}")
                    self.state = ProcessState.ERROR
                    return False

            # Create isolated environment for Claude Code CLI
            # CRITICAL: Remove ANTHROPIC_API_KEY to prevent auth conflict with claude.ai login
            env = os.environ.copy()
            if 'ANTHROPIC_API_KEY' in env:
                del env['ANTHROPIC_API_KEY']
                self._append_error("[INFO] Removed ANTHROPIC_API_KEY from environment for CLI bot")

            # Add Claude Code to PATH if not present (for subprocess execution)
            claude_npm_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "npm")
            if os.path.exists(claude_npm_dir):
                if 'PATH' in env:
                    if claude_npm_dir not in env['PATH']:
                        env['PATH'] = f"{env['PATH']};{claude_npm_dir}"
                else:
                    env['PATH'] = claude_npm_dir

            # Resolve claude executable path
            claude_cmd = self.claude_cli_path
            if claude_cmd == "claude":
                # Try to find claude.cmd in npm directory
                claude_cmd_path = os.path.join(claude_npm_dir, "claude.cmd")
                if os.path.exists(claude_cmd_path):
                    claude_cmd = claude_cmd_path

            # Spawn claude code process with isolated environment
            self.process = subprocess.Popen(
                [claude_cmd],  # Use resolved path
                cwd=str(self.work_dir),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                env=env  # Use isolated environment
            )

            # Start background threads for stream capture
            self._start_capture_threads()

            # Wait for ready signal (10 second timeout)
            ready = self._wait_for_ready(timeout=10)

            if ready:
                self.state = ProcessState.READY
                return True
            else:
                self._append_error("Process did not reach ready state")
                self.terminate(force=True)
                self.state = ProcessState.ERROR
                return False

        except FileNotFoundError:
            self._append_error(f"Claude CLI not found at: {self.claude_cli_path}")
            self.state = ProcessState.ERROR
            return False
        except Exception as e:
            self._append_error(f"Failed to start process: {e}")
            self.state = ProcessState.ERROR
            return False

    def send_task(
        self,
        task_content: str,
        timeout: Optional[int] = None
    ) -> ProcessResult:
        """
        Send task to Claude Code and wait for completion.

        Args:
            task_content: Task description/prompt
            timeout: Override default timeout for this task

        Returns:
            ProcessResult with execution details

        Process:
            1. Verify process is ready
            2. Write task to stdin
            3. Wait for completion or timeout
            4. Parse tool uses from output
            5. Return structured result
        """
        if self.state != ProcessState.READY:
            return ProcessResult(
                success=False,
                output="",
                stderr=f"Process not ready (state: {self.state.value})",
                tool_uses=[],
                duration=0.0,
                exit_code=None,
                timed_out=False
            )

        timeout_value = timeout if timeout is not None else self.timeout_seconds
        start_time = time.time()

        try:
            self.state = ProcessState.PROCESSING

            # Clear buffers for new task
            with self._buffer_lock:
                self.output_buffer.clear()
                self.error_buffer.clear()

            # Send task via stdin
            try:
                self.process.stdin.write(task_content + "\n")
                self.process.stdin.flush()
            except Exception as e:
                duration = time.time() - start_time
                self.state = ProcessState.ERROR
                return ProcessResult(
                    success=False,
                    output="",
                    stderr=f"Failed to write task to stdin: {e}",
                    tool_uses=[],
                    duration=duration,
                    exit_code=None,
                    timed_out=False
                )

            # Wait for completion or timeout
            completed = self._wait_for_completion(timeout_value)
            duration = time.time() - start_time

            # Get current buffer state
            with self._buffer_lock:
                output = "\n".join(self.output_buffer)
                stderr = "\n".join(self.error_buffer)

            if not completed:
                # Timeout occurred
                self.terminate(force=True)
                return ProcessResult(
                    success=False,
                    output=output,
                    stderr=f"Task timed out after {timeout_value}s",
                    tool_uses=[],
                    duration=duration,
                    exit_code=None,
                    timed_out=True
                )

            # Parse tool uses from output
            tool_uses = self._parse_tool_uses(self.output_buffer)

            # Determine success based on output content
            success = self._check_success(output, stderr)

            # Get exit code if process terminated
            exit_code = self.process.poll()

            # Set state back to ready if process still alive
            if exit_code is None:
                self.state = ProcessState.READY
            else:
                self.state = ProcessState.TERMINATED

            return ProcessResult(
                success=success,
                output=output,
                stderr=stderr,
                tool_uses=tool_uses,
                duration=duration,
                exit_code=exit_code,
                timed_out=False
            )

        except Exception as e:
            duration = time.time() - start_time
            self.state = ProcessState.ERROR
            return ProcessResult(
                success=False,
                output="\n".join(self.output_buffer),
                stderr=f"Task execution error: {e}",
                tool_uses=[],
                duration=duration,
                exit_code=None,
                timed_out=False
            )

    def interrupt(self) -> bool:
        """
        Send interrupt signal to running process (Ctrl+C).

        This is gentler than terminate() - it interrupts the current operation
        but keeps the process alive for recovery.

        Returns:
            True if interrupt sent successfully

        Use cases:
            - Bot is churning on unwanted task
            - ScrumMaster needs to stop current operation
            - Human intervention via dashboard
        """
        if self.process is None or self.process.poll() is not None:
            return False

        try:
            if sys.platform == "win32":
                # Windows: Send Ctrl+C event
                import signal
                os.kill(self.process.pid, signal.CTRL_C_EVENT)
            else:
                # Unix: Send SIGINT
                self.process.send_signal(subprocess.signal.SIGINT)

            self.state = ProcessState.READY
            return True

        except Exception as e:
            print(f"Failed to interrupt process: {e}")
            return False

    def terminate(self, force: bool = False) -> None:
        """
        Terminate subprocess.

        Args:
            force: If True, use SIGKILL immediately. If False, try SIGTERM first.

        Process:
            1. Signal background threads to stop
            2. Try graceful termination (SIGTERM) if force=False
            3. Use SIGKILL if needed or if force=True
            4. Wait for threads to finish
            5. Update state
        """
        if self.process is None:
            return

        try:
            # Signal threads to stop
            if self._stop_event:
                self._stop_event.set()

            if force:
                # Force kill immediately
                self.process.kill()
                try:
                    self.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    pass  # Process should be dead after kill()
            else:
                # Try graceful termination first
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Process didn't terminate gracefully, force kill
                    self.process.kill()
                    try:
                        self.process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        pass  # Best effort

            # Wait for threads to finish
            if self._stdout_thread and self._stdout_thread.is_alive():
                self._stdout_thread.join(timeout=2)
            if self._stderr_thread and self._stderr_thread.is_alive():
                self._stderr_thread.join(timeout=2)

        except Exception as e:
            self._append_error(f"Error during termination: {e}")
        finally:
            self.process = None
            self.state = ProcessState.TERMINATED

    def is_alive(self) -> bool:
        """
        Check if subprocess is still running.

        Returns:
            True if process alive, False otherwise
        """
        if self.process is None:
            return False
        return self.process.poll() is None

    def get_output_buffer(self) -> List[str]:
        """
        Get captured stdout lines.

        Returns:
            Copy of output buffer
        """
        with self._buffer_lock:
            return self.output_buffer.copy()

    def get_error_buffer(self) -> List[str]:
        """
        Get captured stderr lines.

        Returns:
            Copy of error buffer
        """
        with self._buffer_lock:
            return self.error_buffer.copy()

    # Private methods

    def _start_capture_threads(self) -> None:
        """
        Start background threads for stdout/stderr capture.

        Creates daemon threads that continuously read from process streams
        and append lines to buffers. Uses stop_event for clean shutdown.
        """
        self._stop_event = threading.Event()

        self._stdout_thread = threading.Thread(
            target=self._capture_stream,
            args=(self.process.stdout, self.output_buffer, self._stop_event),
            daemon=True
        )
        self._stdout_thread.start()

        self._stderr_thread = threading.Thread(
            target=self._capture_stream,
            args=(self.process.stderr, self.error_buffer, self._stop_event),
            daemon=True
        )
        self._stderr_thread.start()

    def _capture_stream(
        self,
        stream,
        buffer: List[str],
        stop_event: threading.Event
    ) -> None:
        """
        Capture stream to buffer (runs in background thread).

        Args:
            stream: subprocess stdout or stderr
            buffer: List to append lines to
            stop_event: Event to signal stop

        Continuously reads lines from stream and appends to buffer.
        Stops when stop_event is set or stream closes.
        """
        try:
            while not stop_event.is_set():
                line = stream.readline()
                if not line:
                    break

                with self._buffer_lock:
                    buffer.append(line.rstrip())

        except Exception as e:
            with self._buffer_lock:
                buffer.append(f"[Stream capture error: {e}]")

    def _wait_for_ready(self, timeout: int) -> bool:
        """
        Wait for Claude Code to signal ready.

        Args:
            timeout: Maximum seconds to wait

        Returns:
            True if ready signal found, False if timeout

        Monitors output buffer for ready indicators like "ready",
        "waiting for input", or similar signals.
        """
        start = time.time()

        while time.time() - start < timeout:
            # Check if process died
            if self.process.poll() is not None:
                return False

            # Check last 5 lines of output for ready signals
            with self._buffer_lock:
                recent = self.output_buffer[-5:] if len(self.output_buffer) >= 5 else self.output_buffer

            for line in recent:
                line_lower = line.lower()
                if any(signal in line_lower for signal in
                       ["ready", "waiting for input", "listening", "initialized"]):
                    return True

            time.sleep(0.1)

        return False

    def _wait_for_completion(self, timeout: int) -> bool:
        """
        Wait for task completion signal.

        Args:
            timeout: Maximum seconds to wait

        Returns:
            True if completion found, False if timeout

        Monitors output for completion indicators like "task completed",
        "done", "finished", or error messages indicating task end.
        """
        start = time.time()

        while time.time() - start < timeout:
            # Check if process exited
            if self.process.poll() is not None:
                return True

            # Check recent output for completion signals
            with self._buffer_lock:
                recent = "\n".join(self.output_buffer[-10:]) if self.output_buffer else ""

            recent_lower = recent.lower()
            if any(signal in recent_lower for signal in
                   ["task completed", "done", "finished", "error:", "failed",
                    "exception", "traceback"]):
                return True

            time.sleep(0.1)

        return False

    def _parse_tool_uses(self, output_lines: List[str]) -> List[Dict[str, Any]]:
        """
        Parse XML tool invocations from output.

        Args:
            output_lines: Lines of stdout

        Returns:
            List of tool use dicts: {"name": str, "parameters": dict}

        Extracts <invoke> blocks with tool names and parameters.
        Handles nested XML structure for parameter extraction.
        """
        output_text = "\n".join(output_lines)

        # Pattern: <invoke name="ToolName">...</invoke>
        invoke_pattern = r'<invoke name="([^"]+)">(.*?)</invoke>'

        tool_uses = []
        for match in re.finditer(invoke_pattern, output_text, re.DOTALL):
            tool_name = match.group(1)
            tool_content = match.group(2)

            # Extract parameters
            params = {}
            param_pattern = r'<parameter name="([^"]+)">(.*?)</parameter>'
            for param_match in re.finditer(param_pattern, tool_content, re.DOTALL):
                param_name = param_match.group(1)
                param_value = param_match.group(2).strip()
                params[param_name] = param_value

            tool_uses.append({
                "name": tool_name,
                "parameters": params
            })

        return tool_uses

    def _check_success(self, output: str, stderr: str) -> bool:
        """
        Determine if task completed successfully.

        Args:
            output: stdout content
            stderr: stderr content

        Returns:
            True if success indicators found, False for errors
        """
        output_lower = output.lower()
        stderr_lower = stderr.lower()

        # Check for success indicators
        success_indicators = ["successfully", "completed", "done", "finished"]
        if any(indicator in output_lower for indicator in success_indicators):
            return True

        # Check for failure indicators
        failure_indicators = ["error:", "failed", "exception", "traceback",
                            "fatal", "critical"]
        if any(indicator in stderr_lower or indicator in output_lower
               for indicator in failure_indicators):
            return False

        # Default to success if no clear failure
        return True

    def _append_error(self, message: str) -> None:
        """
        Append error message to error buffer (thread-safe).

        Args:
            message: Error message to append
        """
        with self._buffer_lock:
            self.error_buffer.append(message)


def extract_file_paths_from_tools(tool_uses: List[Dict[str, Any]]) -> Set[Path]:
    """
    Extract file paths from Write/Edit tool uses.

    Args:
        tool_uses: List of tool use dicts

    Returns:
        Set of Path objects for modified files

    Searches tool parameters for file_path or path keys that indicate
    file modifications from Write, Edit, str_replace, or create_file tools.
    """
    files = set()

    for tool in tool_uses:
        tool_name = tool.get("name", "")
        params = tool.get("parameters", {})

        # Check for file modification tools
        if tool_name in ["Write", "Edit", "str_replace", "create_file", "file_create"]:
            # Try common parameter names for file paths
            if "file_path" in params:
                files.add(Path(params["file_path"]))
            elif "path" in params:
                files.add(Path(params["path"]))
            elif "file" in params:
                files.add(Path(params["file"]))

    return files
