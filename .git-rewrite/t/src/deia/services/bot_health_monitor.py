"""
Bot Health Monitor - Crash detection, auto-recovery, error handling.

Monitors bot subprocess health, detects crashes, auto-restarts with exponential backoff.
Logs all errors to structured JSON format for debugging.
"""

import psutil
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict


@dataclass
class HealthCheckResult:
    """Result of a health check operation."""
    timestamp: str
    bot_id: str
    is_healthy: bool
    pid: Optional[int] = None
    memory_mb: Optional[float] = None
    cpu_percent: Optional[float] = None
    uptime_seconds: Optional[float] = None
    error: Optional[str] = None


@dataclass
class CrashRecord:
    """Record of a bot crash event."""
    timestamp: str
    bot_id: str
    pid: int
    reason: str  # "segfault", "killed", "exited", "unresponsive"
    last_heartbeat: Optional[str] = None
    restart_attempt: int = 1
    restart_timestamp: Optional[str] = None


class BotHealthMonitor:
    """
    Monitors bot subprocess health and implements auto-recovery.

    Features:
    - Health checks every N seconds (configurable)
    - Crash detection and logging
    - Auto-restart with exponential backoff
    - Memory/CPU monitoring
    - Stale process cleanup
    """

    def __init__(
        self,
        bot_id: str,
        work_dir: Path,
        check_interval_seconds: int = 30,
        health_check_timeout_seconds: int = 10
    ):
        """
        Initialize health monitor.

        Args:
            bot_id: Bot identifier
            work_dir: Working directory for logs
            check_interval_seconds: How often to check health (default 30s)
            health_check_timeout_seconds: Timeout for health response (default 10s)
        """
        self.bot_id = bot_id
        self.work_dir = Path(work_dir)
        self.check_interval = check_interval_seconds
        self.health_check_timeout = health_check_timeout_seconds

        # Log directory
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.error_log_file = self.log_dir / f"BOT-{bot_id}-errors.jsonl"
        self.crash_log_file = self.log_dir / f"BOT-{bot_id}-crashes.jsonl"

        # Health tracking
        self.processes: Dict[int, Dict[str, Any]] = {}  # PID -> process info
        self.crash_count = 0
        self.restart_backoff = 1  # Start with 1s backoff, exponential
        self.max_backoff = 60  # Cap at 60s
        self.max_restart_attempts = 5

    def register_process(self, pid: int, start_time: datetime) -> None:
        """
        Register a bot process for monitoring.

        Args:
            pid: Process ID
            start_time: When the process started
        """
        self.processes[pid] = {
            "pid": pid,
            "start_time": start_time,
            "last_check": datetime.now(),
            "consecutive_failures": 0,
            "restart_count": 0
        }
        self._log(f"Registered process {pid} for health monitoring")

    def check_health(self, pid: int) -> HealthCheckResult:
        """
        Check if a process is healthy.

        Args:
            pid: Process ID to check

        Returns:
            HealthCheckResult with current status
        """
        timestamp = datetime.now().isoformat()

        # Verify process exists
        try:
            process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            return HealthCheckResult(
                timestamp=timestamp,
                bot_id=self.bot_id,
                is_healthy=False,
                pid=pid,
                error="Process not found (crashed)"
            )

        # Check if process is still running
        if not process.is_running():
            return HealthCheckResult(
                timestamp=timestamp,
                bot_id=self.bot_id,
                is_healthy=False,
                pid=pid,
                error="Process is not running"
            )

        # Get resource usage
        try:
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)
            cpu_percent = process.cpu_percent(interval=1)
            uptime = time.time() - process.create_time()

            # Check for resource exhaustion
            if memory_mb > 500:  # Alert at 500MB
                return HealthCheckResult(
                    timestamp=timestamp,
                    bot_id=self.bot_id,
                    is_healthy=False,
                    pid=pid,
                    memory_mb=memory_mb,
                    cpu_percent=cpu_percent,
                    uptime_seconds=uptime,
                    error=f"Memory limit exceeded: {memory_mb}MB"
                )

            if cpu_percent > 80:  # Alert at 80% CPU
                return HealthCheckResult(
                    timestamp=timestamp,
                    bot_id=self.bot_id,
                    is_healthy=False,
                    pid=pid,
                    memory_mb=memory_mb,
                    cpu_percent=cpu_percent,
                    uptime_seconds=uptime,
                    error=f"CPU limit exceeded: {cpu_percent}%"
                )

            # Process is healthy
            return HealthCheckResult(
                timestamp=timestamp,
                bot_id=self.bot_id,
                is_healthy=True,
                pid=pid,
                memory_mb=memory_mb,
                cpu_percent=cpu_percent,
                uptime_seconds=uptime
            )

        except Exception as e:
            return HealthCheckResult(
                timestamp=timestamp,
                bot_id=self.bot_id,
                is_healthy=False,
                pid=pid,
                error=f"Health check failed: {str(e)}"
            )

    def handle_crash(
        self,
        pid: int,
        reason: str,
        restart_callback=None
    ) -> bool:
        """
        Handle a bot crash with auto-restart.

        Args:
            pid: Process ID that crashed
            reason: Reason for crash ("segfault", "killed", "exited", "unresponsive")
            restart_callback: Function to call to restart (returns new PID or None)

        Returns:
            True if restart was successful, False otherwise
        """
        timestamp = datetime.now().isoformat()

        # Log the crash
        crash_record = CrashRecord(
            timestamp=timestamp,
            bot_id=self.bot_id,
            pid=pid,
            reason=reason,
            restart_attempt=self.crash_count + 1
        )

        self._log_crash(crash_record)
        self.crash_count += 1

        # Check if we should retry
        if self.crash_count > self.max_restart_attempts:
            self._log(f"Max restart attempts ({self.max_restart_attempts}) exceeded. Giving up.")
            return False

        # Wait with exponential backoff before restart
        wait_time = min(self.restart_backoff, self.max_backoff)
        self._log(f"Waiting {wait_time}s before restart (attempt {self.crash_count}/{self.max_restart_attempts})")
        time.sleep(wait_time)
        self.restart_backoff = min(wait_time * 2, self.max_backoff)

        # Attempt restart
        if restart_callback:
            try:
                new_pid = restart_callback()
                if new_pid:
                    self.register_process(new_pid, datetime.now())
                    crash_record.restart_timestamp = datetime.now().isoformat()
                    self._log(f"Auto-restart successful. New PID: {new_pid}")
                    return True
            except Exception as e:
                self._log(f"Auto-restart failed: {str(e)}")

        return False

    def cleanup_stale_processes(self) -> List[int]:
        """
        Clean up stale process entries (processes that have exited).

        Returns:
            List of removed PIDs
        """
        removed = []

        for pid in list(self.processes.keys()):
            try:
                if not psutil.pid_exists(pid):
                    removed.append(pid)
                    del self.processes[pid]
            except Exception:
                removed.append(pid)
                del self.processes[pid]

        if removed:
            self._log(f"Cleaned up {len(removed)} stale processes: {removed}")

        return removed

    def get_health_summary(self) -> Dict[str, Any]:
        """
        Get summary of all monitored processes.

        Returns:
            Dictionary with health information
        """
        results = []

        for pid in list(self.processes.keys()):
            result = self.check_health(pid)
            results.append(asdict(result))

        return {
            "bot_id": self.bot_id,
            "timestamp": datetime.now().isoformat(),
            "process_count": len(self.processes),
            "crash_count": self.crash_count,
            "processes": results
        }

    def _log(self, message: str) -> None:
        """Log message to error log."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "bot_id": self.bot_id,
            "level": "INFO",
            "message": message
        }

        with open(self.error_log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        print(f"[{timestamp}] [{self.bot_id}] {message}")

    def _log_crash(self, crash_record: CrashRecord) -> None:
        """Log crash event to structured log."""
        with open(self.crash_log_file, "a") as f:
            f.write(json.dumps(asdict(crash_record)) + "\n")

        self._log(f"CRASH DETECTED: {crash_record.reason} (PID {crash_record.pid}, attempt {crash_record.restart_attempt})")

    def log_error(self, error: str, context: Dict[str, Any] = None) -> None:
        """
        Log an error event.

        Args:
            error: Error message
            context: Additional context (optional)
        """
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "bot_id": self.bot_id,
            "level": "ERROR",
            "message": error,
            "context": context or {}
        }

        with open(self.error_log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")


class ProcessCrashDetector:
    """
    Detects subprocess crashes by monitoring exit codes and signals.

    Wraps subprocess.Popen to detect when process exits unexpectedly.
    """

    @staticmethod
    def is_crashed(process: subprocess.Popen) -> tuple[bool, str]:
        """
        Check if process has crashed.

        Args:
            process: subprocess.Popen instance

        Returns:
            Tuple of (crashed: bool, reason: str)
        """
        if process.poll() is None:
            # Process still running
            return False, ""

        exit_code = process.returncode

        if exit_code == 0:
            return False, "normal exit"
        elif exit_code < 0:
            # Killed by signal
            signal_num = -exit_code
            return True, f"killed by signal {signal_num}"
        else:
            # Abnormal exit
            return True, f"exited with code {exit_code}"

    @staticmethod
    def is_unresponsive(process: subprocess.Popen, timeout_seconds: float = 10) -> bool:
        """
        Check if process is unresponsive to communication.

        Args:
            process: subprocess.Popen instance
            timeout_seconds: How long to wait for response

        Returns:
            True if process is unresponsive
        """
        try:
            # Try to communicate (with timeout)
            process.communicate(timeout=timeout_seconds)
            return False
        except subprocess.TimeoutExpired:
            return True
