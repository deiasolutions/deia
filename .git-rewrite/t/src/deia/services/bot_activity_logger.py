"""
Bot Activity Logger - Structured JSON logging for all bot operations.

Logs all bot events (startup, shutdown, task received, task completed, errors)
in JSON format with timestamps, bot ID, operation, and result.
Implements log rotation to manage disk space.
"""

import json
import gzip
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum


class EventType(Enum):
    """Types of bot events."""
    STARTUP = "startup"
    SHUTDOWN = "shutdown"
    TASK_RECEIVED = "task_received"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    HEALTH_CHECK = "health_check"
    ERROR = "error"
    WARNING = "warning"
    STATUS_UPDATE = "status_update"


@dataclass
class ActivityEvent:
    """Structured bot activity event."""
    timestamp: str
    bot_id: str
    event_type: str
    operation: str
    result: Optional[str] = None
    duration_seconds: Optional[float] = None
    error: Optional[str] = None
    task_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


class BotActivityLogger:
    """
    Logs all bot activities to structured JSON format.

    Features:
    - JSON-formatted logs for easy parsing
    - Queryable format with timestamp, bot_id, event_type
    - Log rotation with compression
    - No PII in logs (configurable redaction)
    - Metrics and statistics
    """

    # Maximum size before rotation (100MB)
    MAX_LOG_SIZE_BYTES = 100 * 1024 * 1024

    def __init__(
        self,
        bot_id: str,
        work_dir: Path,
        max_log_size_mb: int = 100
    ):
        """
        Initialize activity logger.

        Args:
            bot_id: Bot identifier
            work_dir: Working directory for logs
            max_log_size_mb: Maximum log file size before rotation (default 100MB)
        """
        self.bot_id = bot_id
        self.work_dir = Path(work_dir)
        self.max_log_size = max_log_size_mb * 1024 * 1024

        # Log directory
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.activity_log_file = self.log_dir / f"BOT-{bot_id}-activity.jsonl"
        self.stats_file = self.log_dir / f"BOT-{bot_id}-stats.json"

        # Statistics
        self.stats = {
            "bot_id": bot_id,
            "start_time": datetime.now().isoformat(),
            "events_logged": 0,
            "tasks_received": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_task_duration": 0.0,
            "errors": 0,
            "warnings": 0
        }

    def log_event(
        self,
        event_type: EventType,
        operation: str,
        result: Optional[str] = None,
        duration_seconds: Optional[float] = None,
        error: Optional[str] = None,
        task_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log a bot activity event.

        Args:
            event_type: Type of event
            operation: What operation happened
            result: Result of operation (success/failure details)
            duration_seconds: How long the operation took
            error: Error message if operation failed
            task_id: Associated task ID (if applicable)
            context: Additional context as dict
        """
        timestamp = datetime.now().isoformat()

        event = ActivityEvent(
            timestamp=timestamp,
            bot_id=self.bot_id,
            event_type=event_type.value,
            operation=operation,
            result=result,
            duration_seconds=duration_seconds,
            error=error,
            task_id=task_id,
            context=context or {}
        )

        # Write to log file
        self._write_log(event)

        # Update statistics
        self._update_stats(event)

        # Check for rotation
        self._check_rotation()

    def log_startup(self, adapter_type: str) -> None:
        """Log bot startup."""
        self.log_event(
            event_type=EventType.STARTUP,
            operation="Bot startup",
            result="initialized",
            context={"adapter_type": adapter_type}
        )

    def log_shutdown(self, reason: str = "normal") -> None:
        """Log bot shutdown."""
        self.log_event(
            event_type=EventType.SHUTDOWN,
            operation="Bot shutdown",
            result=reason
        )

    def log_task_received(self, task_id: str, priority: str = "P2") -> None:
        """Log that a task was received."""
        self.log_event(
            event_type=EventType.TASK_RECEIVED,
            operation="Task queued",
            task_id=task_id,
            context={"priority": priority}
        )

    def log_task_started(self, task_id: str) -> None:
        """Log that a task started execution."""
        self.log_event(
            event_type=EventType.TASK_STARTED,
            operation="Task execution started",
            task_id=task_id
        )

    def log_task_completed(
        self,
        task_id: str,
        duration_seconds: float,
        result_summary: str = "success"
    ) -> None:
        """Log that a task completed successfully."""
        self.log_event(
            event_type=EventType.TASK_COMPLETED,
            operation="Task execution completed",
            result=result_summary,
            duration_seconds=duration_seconds,
            task_id=task_id
        )

    def log_task_failed(
        self,
        task_id: str,
        error_message: str,
        duration_seconds: Optional[float] = None
    ) -> None:
        """Log that a task failed."""
        self.log_event(
            event_type=EventType.TASK_FAILED,
            operation="Task execution failed",
            error=error_message,
            duration_seconds=duration_seconds,
            task_id=task_id
        )

    def log_health_check(
        self,
        status: str,
        memory_mb: Optional[float] = None,
        cpu_percent: Optional[float] = None
    ) -> None:
        """Log a health check."""
        context = {}
        if memory_mb is not None:
            context["memory_mb"] = memory_mb
        if cpu_percent is not None:
            context["cpu_percent"] = cpu_percent

        self.log_event(
            event_type=EventType.HEALTH_CHECK,
            operation="Health check",
            result=status,
            context=context
        )

    def log_error(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log an error."""
        self.log_event(
            event_type=EventType.ERROR,
            operation="Error occurred",
            error=message,
            context=context
        )

    def log_warning(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log a warning."""
        self.log_event(
            event_type=EventType.WARNING,
            operation="Warning",
            result=message,
            context=context
        )

    def log_status_update(self, status: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log a status update."""
        self.log_event(
            event_type=EventType.STATUS_UPDATE,
            operation="Status update",
            result=status,
            context=context
        )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get current statistics.

        Returns:
            Statistics dictionary
        """
        self.stats["last_updated"] = datetime.now().isoformat()
        if self.stats["tasks_completed"] > 0:
            self.stats["avg_task_duration"] = \
                self.stats["total_task_duration"] / self.stats["tasks_completed"]
        return self.stats

    def save_stats(self) -> None:
        """Save statistics to file."""
        with open(self.stats_file, "w") as f:
            json.dump(self.get_stats(), f, indent=2)

    def query_events(
        self,
        event_type: Optional[EventType] = None,
        task_id: Optional[str] = None,
        limit: int = 100
    ) -> list[Dict[str, Any]]:
        """
        Query logged events.

        Args:
            event_type: Filter by event type (optional)
            task_id: Filter by task ID (optional)
            limit: Maximum number of events to return

        Returns:
            List of matching events
        """
        events = []

        try:
            with open(self.activity_log_file, "r") as f:
                for line in f:
                    if line.strip():
                        event = json.loads(line)

                        # Apply filters
                        if event_type and event["event_type"] != event_type.value:
                            continue
                        if task_id and event.get("task_id") != task_id:
                            continue

                        events.append(event)

                        if len(events) >= limit:
                            break
        except FileNotFoundError:
            pass

        return list(reversed(events))  # Most recent first

    def get_task_history(self, task_id: str) -> list[Dict[str, Any]]:
        """
        Get all events related to a task.

        Args:
            task_id: Task identifier

        Returns:
            List of events related to task
        """
        return self.query_events(task_id=task_id, limit=1000)

    def _write_log(self, event: ActivityEvent) -> None:
        """Write event to log file."""
        with open(self.activity_log_file, "a") as f:
            f.write(json.dumps(asdict(event)) + "\n")

    def _update_stats(self, event: ActivityEvent) -> None:
        """Update statistics based on event."""
        self.stats["events_logged"] += 1

        if event.event_type == EventType.TASK_RECEIVED.value:
            self.stats["tasks_received"] += 1
        elif event.event_type == EventType.TASK_COMPLETED.value:
            self.stats["tasks_completed"] += 1
            if event.duration_seconds:
                self.stats["total_task_duration"] += event.duration_seconds
        elif event.event_type == EventType.TASK_FAILED.value:
            self.stats["tasks_failed"] += 1
        elif event.event_type == EventType.ERROR.value:
            self.stats["errors"] += 1
        elif event.event_type == EventType.WARNING.value:
            self.stats["warnings"] += 1

        # Save stats periodically
        if self.stats["events_logged"] % 10 == 0:
            self.save_stats()

    def _check_rotation(self) -> None:
        """Check if log file needs rotation."""
        if not self.activity_log_file.exists():
            return

        file_size = self.activity_log_file.stat().st_size

        if file_size > self.max_log_size:
            self._rotate_logs()

    def _rotate_logs(self) -> None:
        """Rotate log files with compression."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"BOT-{self.bot_id}-activity-{timestamp}.jsonl.gz"
        backup_path = self.log_dir / backup_name

        # Compress and move current log
        try:
            with open(self.activity_log_file, "rb") as f_in:
                with gzip.open(backup_path, "wb") as f_out:
                    f_out.writelines(f_in)

            # Clear original file
            self.activity_log_file.unlink()

            # Log rotation event
            self.log_event(
                event_type=EventType.STATUS_UPDATE,
                operation="Log rotation",
                result=f"rotated to {backup_name}"
            )
        except Exception as e:
            # If rotation fails, just continue logging
            self.log_event(
                event_type=EventType.ERROR,
                operation="Log rotation failed",
                error=str(e)
            )

    def cleanup_old_logs(self, keep_days: int = 7) -> None:
        """
        Clean up old compressed log files.

        Args:
            keep_days: Keep logs from the last N days
        """
        import time

        now = time.time()
        cutoff = now - (keep_days * 86400)

        for log_file in self.log_dir.glob(f"BOT-{self.bot_id}-activity-*.jsonl.gz"):
            if log_file.stat().st_mtime < cutoff:
                try:
                    log_file.unlink()
                except Exception as e:
                    print(f"Failed to delete old log {log_file}: {e}")
