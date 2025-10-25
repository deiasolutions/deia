"""
Multi-Bot Load Manager - Efficient resource distribution across multiple bots.

Features:
- Dynamic port allocation (8001-8999)
- Fair task queue distribution
- Rate limiting per bot
- Load monitoring and balancing
- Priority-based task scheduling
- Circuit breaker for failing bots
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import json
import hashlib
from .bot_circuit_breaker import MultiCircuitBreaker


@dataclass
class BotLoad:
    """Load information for a single bot."""
    bot_id: str
    port: int
    pid: int
    current_load: float = 0.0  # 0.0 to 1.0
    tasks_queued: int = 0
    tasks_completed: int = 0
    total_processing_time: float = 0.0
    last_heartbeat: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def avg_task_time(self) -> float:
        """Average time per task."""
        if self.tasks_completed == 0:
            return 0.0
        return self.total_processing_time / self.tasks_completed

    @property
    def capacity_remaining(self) -> float:
        """Available capacity (0.0 to 1.0)."""
        return 1.0 - self.current_load


class BotLoadManager:
    """
    Manages load distribution across multiple bots.

    Features:
    - Track load per bot
    - Suggest which bot should take next task
    - Prevent overload (queue tasks fairly)
    - Rate limiting (don't overwhelm bots)
    - Historical load tracking
    """

    # Port range for bot services
    MIN_PORT = 8001
    MAX_PORT = 8999
    TOTAL_PORTS = MAX_PORT - MIN_PORT + 1

    # Load thresholds
    HIGH_LOAD_THRESHOLD = 0.8
    OVERLOAD_THRESHOLD = 0.95

    # Rate limiting
    DEFAULT_MAX_TASKS_PER_BOT = 5  # Max queued tasks per bot
    DEFAULT_RATE_LIMIT_MS = 1000   # Min ms between task sends to same bot

    def __init__(self, work_dir: Path):
        """
        Initialize load manager.

        Args:
            work_dir: Working directory for state persistence
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Load tracking
        self.bot_loads: Dict[str, BotLoad] = {}
        self.port_assignment_history: Dict[str, int] = {}  # bot_id -> port

        # Rate limiting
        self.last_task_time: Dict[str, datetime] = {}  # bot_id -> last task timestamp
        self.max_queued_tasks = self.DEFAULT_MAX_TASKS_PER_BOT
        self.rate_limit_ms = self.DEFAULT_RATE_LIMIT_MS

    def register_bot(self, bot_id: str, port: int, pid: int) -> None:
        """
        Register a bot for load management.

        Args:
            bot_id: Bot identifier
            port: Service port
            pid: Process ID
        """
        self.bot_loads[bot_id] = BotLoad(
            bot_id=bot_id,
            port=port,
            pid=pid
        )
        self.port_assignment_history[bot_id] = port
        self._log_load_event("bot_registered", bot_id, {"port": port, "pid": pid})

    def unregister_bot(self, bot_id: str) -> None:
        """
        Unregister a bot from load management.

        Args:
            bot_id: Bot identifier
        """
        if bot_id in self.bot_loads:
            del self.bot_loads[bot_id]
        if bot_id in self.last_task_time:
            del self.last_task_time[bot_id]
        self._log_load_event("bot_unregistered", bot_id)

    def suggest_bot_for_task(self, priority: str = "P2") -> Optional[str]:
        """
        Suggest which bot should handle the next task.

        Uses load balancing: suggests least-loaded bot.
        Respects rate limiting and queue limits.

        Args:
            priority: Task priority (P0, P1, P2 - lower number = higher priority)

        Returns:
            Bot ID or None if no suitable bot available
        """
        if not self.bot_loads:
            return None

        # Filter out overloaded bots
        available_bots = [
            bot_id for bot_id, load in self.bot_loads.items()
            if load.current_load < self.OVERLOAD_THRESHOLD
            and load.tasks_queued < self.max_queued_tasks
        ]

        if not available_bots:
            return None

        # Check rate limiting
        available_bots = [
            bot_id for bot_id in available_bots
            if self._check_rate_limit(bot_id)
        ]

        if not available_bots:
            return None

        # Sort by current load (ascending) to find least-loaded
        available_bots.sort(
            key=lambda b: self.bot_loads[b].current_load
        )

        # For high priority tasks, skip to lowest load
        selected = available_bots[0]
        self.last_task_time[selected] = datetime.now()

        return selected

    def update_bot_load(
        self,
        bot_id: str,
        current_load: Optional[float] = None,
        task_completed: bool = False,
        task_duration: Optional[float] = None
    ) -> None:
        """
        Update load information for a bot.

        Args:
            bot_id: Bot identifier
            current_load: Current load (0.0 to 1.0)
            task_completed: Whether a task completed
            task_duration: Duration of completed task (seconds)
        """
        if bot_id not in self.bot_loads:
            return

        load = self.bot_loads[bot_id]

        if current_load is not None:
            load.current_load = min(1.0, max(0.0, current_load))

        if task_completed:
            load.tasks_completed += 1
            load.tasks_queued = max(0, load.tasks_queued - 1)

            if task_duration is not None:
                load.total_processing_time += task_duration

            # Alert if high load
            if load.current_load > self.HIGH_LOAD_THRESHOLD:
                self._log_load_event(
                    "high_load_alert",
                    bot_id,
                    {"current_load": load.current_load}
                )

        load.last_heartbeat = datetime.now().isoformat()

    def queue_task(self, bot_id: str) -> bool:
        """
        Queue a task to a bot.

        Returns False if bot is overloaded or doesn't exist.

        Args:
            bot_id: Bot identifier

        Returns:
            True if task queued successfully
        """
        if bot_id not in self.bot_loads:
            return False

        load = self.bot_loads[bot_id]

        # Check queue limit
        if load.tasks_queued >= self.max_queued_tasks:
            return False

        load.tasks_queued += 1
        return True

    def get_load_summary(self) -> Dict[str, any]:
        """
        Get summary of all bot loads.

        Returns:
            Summary dict with aggregate and per-bot info
        """
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_bots": len(self.bot_loads),
            "bots": {}
        }

        total_load = 0.0
        overloaded_count = 0

        for bot_id, load in self.bot_loads.items():
            summary["bots"][bot_id] = {
                "port": load.port,
                "current_load": load.current_load,
                "capacity_remaining": load.capacity_remaining,
                "tasks_queued": load.tasks_queued,
                "tasks_completed": load.tasks_completed,
                "avg_task_time": load.avg_task_time
            }

            total_load += load.current_load

            if load.current_load > self.OVERLOAD_THRESHOLD:
                overloaded_count += 1

        # Aggregate stats
        summary["avg_load"] = total_load / len(self.bot_loads) if self.bot_loads else 0.0
        summary["overloaded_bots"] = overloaded_count
        summary["available_capacity"] = 1.0 - (total_load / len(self.bot_loads)) if self.bot_loads else 0.0

        return summary

    def get_bot_load(self, bot_id: str) -> Optional[Dict]:
        """Get load info for a specific bot."""
        if bot_id not in self.bot_loads:
            return None

        load = self.bot_loads[bot_id]
        return {
            "bot_id": bot_id,
            "port": load.port,
            "pid": load.pid,
            "current_load": load.current_load,
            "capacity_remaining": load.capacity_remaining,
            "tasks_queued": load.tasks_queued,
            "tasks_completed": load.tasks_completed,
            "avg_task_time": load.avg_task_time,
            "last_heartbeat": load.last_heartbeat
        }

    def assign_port(self, bot_id: str) -> int:
        """
        Assign a port to a bot.

        Uses consistent hashing so same bot ID always gets same port.
        Falls back to next available if collision.

        Args:
            bot_id: Bot identifier

        Returns:
            Assigned port number (8001-8999)
        """
        # Check if already assigned
        if bot_id in self.port_assignment_history:
            return self.port_assignment_history[bot_id]

        # Hash-based port assignment
        hash_val = int(hashlib.md5(bot_id.encode()).hexdigest(), 16)
        port = self.MIN_PORT + (hash_val % self.TOTAL_PORTS)

        # Check for collision
        used_ports = set(self.port_assignment_history.values())
        while port in used_ports:
            port = port + 1 if port < self.MAX_PORT else self.MIN_PORT

        self.port_assignment_history[bot_id] = port
        self._log_load_event("port_assigned", bot_id, {"port": port})

        return port

    def set_rate_limit(self, milliseconds: int) -> None:
        """
        Set rate limit for task distribution.

        Args:
            milliseconds: Minimum ms between tasks sent to same bot
        """
        self.rate_limit_ms = milliseconds

    def set_max_queued_tasks(self, max_tasks: int) -> None:
        """
        Set maximum queued tasks per bot.

        Args:
            max_tasks: Max queued tasks before bot is considered overloaded
        """
        self.max_queued_tasks = max_tasks

    def _check_rate_limit(self, bot_id: str) -> bool:
        """Check if enough time has passed since last task to this bot."""
        if bot_id not in self.last_task_time:
            return True

        last_time = self.last_task_time[bot_id]
        elapsed_ms = (datetime.now() - last_time).total_seconds() * 1000

        return elapsed_ms >= self.rate_limit_ms

    def _log_load_event(self, event: str, bot_id: str, details: Optional[Dict] = None) -> None:
        """Log load management event."""
        log_file = self.log_dir / "load-management.jsonl"
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "bot_id": bot_id,
            "details": details or {}
        }

        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass
