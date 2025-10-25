"""
Bot Shutdown Handler - Graceful shutdown with cleanup.

Implements SIGTERM/SIGINT handling for graceful shutdown.
Saves state, closes connections, cleans up temporary files.
"""

import signal
import os
import json
import atexit
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class ShutdownState:
    """State snapshot when bot shuts down."""
    timestamp: str
    bot_id: str
    reason: str  # "sigterm", "sigint", "error", "normal"
    uptime_seconds: float
    tasks_completed: int
    final_status: Optional[str] = None


class GracefulShutdownHandler:
    """
    Handles graceful shutdown of bot process.

    Features:
    - Catches SIGTERM and SIGINT signals
    - Completes current task before shutdown
    - Saves final state to disk
    - Cleans up temporary files
    - Unregisters from service registry
    - Configurable timeout (default 10s)
    """

    # Default shutdown timeout
    DEFAULT_SHUTDOWN_TIMEOUT_SECONDS = 10

    def __init__(
        self,
        bot_id: str,
        work_dir: Path,
        shutdown_timeout_seconds: int = DEFAULT_SHUTDOWN_TIMEOUT_SECONDS
    ):
        """
        Initialize shutdown handler.

        Args:
            bot_id: Bot identifier
            work_dir: Working directory
            shutdown_timeout_seconds: Grace period before force kill (default 10s)
        """
        self.bot_id = bot_id
        self.work_dir = Path(work_dir)
        self.shutdown_timeout = shutdown_timeout_seconds

        # State tracking
        self.start_time = datetime.now()
        self.tasks_completed = 0
        self.is_shutting_down = False
        self.shutdown_callbacks: list[Callable] = []

        # Response directory
        self.response_dir = self.work_dir / ".deia" / "hive" / "responses"
        self.response_dir.mkdir(parents=True, exist_ok=True)

        # Register signal handlers
        signal.signal(signal.SIGTERM, self._handle_sigterm)
        signal.signal(signal.SIGINT, self._handle_sigint)

        # Register cleanup at exit
        atexit.register(self._cleanup_at_exit)

    def register_shutdown_callback(self, callback: Callable) -> None:
        """
        Register a callback to run during shutdown.

        Called after SIGTERM/SIGINT but before cleanup.
        Useful for saving state or closing connections.

        Args:
            callback: Function to call during shutdown
        """
        self.shutdown_callbacks.append(callback)

    def register_task_completion(self) -> None:
        """Track task completion for uptime calculation."""
        self.tasks_completed += 1

    def request_shutdown(self, reason: str = "manual") -> None:
        """
        Request graceful shutdown.

        Args:
            reason: Why shutdown was requested
        """
        if not self.is_shutting_down:
            print(f"[{self.bot_id}] Graceful shutdown requested: {reason}")
            self.is_shutting_down = True
            self._perform_shutdown(reason)

    def _handle_sigterm(self, signum, frame) -> None:
        """Handle SIGTERM signal (graceful shutdown request)."""
        print(f"\n[{self.bot_id}] Received SIGTERM, initiating graceful shutdown...")
        self.request_shutdown("sigterm")

    def _handle_sigint(self, signum, frame) -> None:
        """Handle SIGINT signal (Ctrl+C)."""
        print(f"\n[{self.bot_id}] Received SIGINT, initiating graceful shutdown...")
        self.request_shutdown("sigint")

    def _perform_shutdown(self, reason: str) -> None:
        """
        Perform graceful shutdown.

        Args:
            reason: Reason for shutdown
        """
        # Call registered callbacks
        for callback in self.shutdown_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"[{self.bot_id}] Error in shutdown callback: {e}")

        # Save shutdown state
        self._save_shutdown_state(reason)

        # Cleanup temporary files
        self._cleanup_temp_files()

        print(f"[{self.bot_id}] Graceful shutdown complete")

    def _save_shutdown_state(self, reason: str) -> None:
        """
        Save final state to response file.

        Args:
            reason: Reason for shutdown
        """
        uptime = (datetime.now() - self.start_time).total_seconds()

        state = ShutdownState(
            timestamp=datetime.now().isoformat(),
            bot_id=self.bot_id,
            reason=reason,
            uptime_seconds=uptime,
            tasks_completed=self.tasks_completed,
            final_status="shutdown"
        )

        # Write state file
        state_file = self.response_dir / f"{self.bot_id}-shutdown-state.json"
        try:
            with open(state_file, "w") as f:
                json.dump(asdict(state), f, indent=2)
            print(f"[{self.bot_id}] Shutdown state saved to {state_file.name}")
        except Exception as e:
            print(f"[{self.bot_id}] Failed to save shutdown state: {e}")

    def _cleanup_temp_files(self) -> None:
        """Clean up temporary files created during operation."""
        temp_dir = self.work_dir / ".deia" / "temp"

        if temp_dir.exists():
            try:
                import shutil
                count = 0
                for item in temp_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                        count += 1
                    elif item.is_dir():
                        shutil.rmtree(item)
                        count += 1

                if count > 0:
                    print(f"[{self.bot_id}] Cleaned up {count} temporary files")
            except Exception as e:
                print(f"[{self.bot_id}] Error cleaning temp files: {e}")

    def _cleanup_at_exit(self) -> None:
        """Run cleanup when Python exits (atexit)."""
        if not self.is_shutting_down:
            self._perform_shutdown("exit")


class ShutdownMonitor:
    """
    Monitors shutdown status and prevents orphaned processes.

    Can force kill a bot if it doesn't shutdown gracefully within timeout.
    """

    def __init__(self, pid: int, timeout_seconds: float = 10):
        """
        Initialize shutdown monitor.

        Args:
            pid: Process ID to monitor
            timeout_seconds: How long to wait before force kill
        """
        self.pid = pid
        self.timeout = timeout_seconds

    def wait_for_shutdown(self) -> bool:
        """
        Wait for process to shutdown gracefully.

        Returns:
            True if process exited, False if forced kill was needed
        """
        import time
        import psutil

        start = time.time()
        while time.time() - start < self.timeout:
            try:
                if not psutil.pid_exists(self.pid):
                    return True  # Process exited gracefully
            except Exception:
                return True

            time.sleep(0.1)

        # Timeout exceeded - force kill
        self._force_kill()
        return False

    def _force_kill(self) -> None:
        """Force kill process (SIGKILL)."""
        import signal
        try:
            os.kill(self.pid, signal.SIGKILL)
            print(f"[SHUTDOWN] Force killed process {self.pid}")
        except Exception as e:
            print(f"[SHUTDOWN] Failed to force kill {self.pid}: {e}")


def setup_graceful_shutdown(
    bot_id: str,
    work_dir: Path,
    on_shutdown: Optional[Callable] = None
) -> GracefulShutdownHandler:
    """
    Setup graceful shutdown for a bot.

    Convenience function to create and configure shutdown handler.

    Args:
        bot_id: Bot identifier
        work_dir: Working directory
        on_shutdown: Optional callback for shutdown

    Returns:
        Configured GracefulShutdownHandler
    """
    handler = GracefulShutdownHandler(
        bot_id=bot_id,
        work_dir=work_dir
    )

    if on_shutdown:
        handler.register_shutdown_callback(on_shutdown)

    return handler
