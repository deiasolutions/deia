"""
Bot Auto Scaler - Dynamically spawn and terminate bots based on system load.

Monitors system load, automatically scales bot count up/down.
Resource-aware to prevent system exhaustion.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum
import json
import subprocess
import psutil


class ScalingAction(Enum):
    """Scaling actions."""
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    NO_CHANGE = "no_change"


@dataclass
class ScalingMetrics:
    """Metrics used for scaling decisions."""
    timestamp: str
    current_bot_count: int
    system_load_avg: float  # 0-1
    total_queue_size: int
    avg_bot_load: float
    system_memory_percent: float
    system_cpu_percent: float
    scaling_action: ScalingAction = ScalingAction.NO_CHANGE


class BotAutoScaler:
    """
    Automatically scales bot count based on system load and queue depth.

    Policies:
    - Scale UP when: queue depth high + low bot load OR system load increasing
    - Scale DOWN when: queue empty + bots idle for duration
    - Respect resource limits: don't exceed system capacity
    - Gradual scaling: add/remove 1-2 bots at a time
    """

    # Configuration
    MIN_BOTS = 1
    MAX_BOTS = 10
    QUEUE_THRESHOLD_FOR_SCALE_UP = 5  # Queue 5+ items = scale up
    IDLE_TIME_FOR_SCALE_DOWN_SECONDS = 300  # 5 minutes idle = scale down
    SYSTEM_MEMORY_THRESHOLD = 0.85  # Don't scale if 85%+ memory used
    SYSTEM_CPU_THRESHOLD = 0.90  # Don't scale if 90%+ CPU used
    SCALE_UP_COOLDOWN_SECONDS = 30  # Wait 30s between scale-up operations
    SCALE_DOWN_COOLDOWN_SECONDS = 60  # Wait 60s between scale-down operations

    def __init__(self, work_dir: Path, bot_launcher_script: Optional[Path] = None):
        """
        Initialize auto scaler.

        Args:
            work_dir: Working directory
            bot_launcher_script: Path to script that launches bots (e.g., run_single_bot.py)
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.scaling_log = self.log_dir / "auto-scaling.jsonl"
        self.metrics_log = self.log_dir / "scaling-metrics.jsonl"
        self.bot_launcher = bot_launcher_script

        # Scaling state
        self.current_bot_count = 0
        self.active_bots: Dict[str, Dict] = {}  # bot_id -> {pid, launched_at, status}
        self.last_scale_up_time: Optional[datetime] = None
        self.last_scale_down_time: Optional[datetime] = None
        self.idle_start_time: Optional[datetime] = None

    def should_scale_up(
        self,
        current_load: float,
        queue_size: int,
        avg_bot_load: float
    ) -> bool:
        """
        Determine if system should scale up.

        Args:
            current_load: Average system load (0.0-1.0)
            queue_size: Number of queued tasks
            avg_bot_load: Average load across bots (0.0-1.0)

        Returns:
            True if should add more bots
        """
        # Don't scale if already at max
        if self.current_bot_count >= self.MAX_BOTS:
            return False

        # Don't scale if system resources exhausted
        if not self._check_system_resources():
            return False

        # Check cooldown
        if self.last_scale_up_time:
            elapsed = (datetime.now() - self.last_scale_up_time).total_seconds()
            if elapsed < self.SCALE_UP_COOLDOWN_SECONDS:
                return False

        # Scale up if: queue backlog OR increasing load
        if queue_size >= self.QUEUE_THRESHOLD_FOR_SCALE_UP:
            return True

        if current_load > 0.7 and avg_bot_load > 0.6:
            return True

        return False

    def should_scale_down(
        self,
        queue_size: int,
        avg_bot_load: float
    ) -> bool:
        """
        Determine if system should scale down.

        Args:
            queue_size: Number of queued tasks
            avg_bot_load: Average load across bots (0.0-1.0)

        Returns:
            True if should remove bots
        """
        # Don't scale down below minimum
        if self.current_bot_count <= self.MIN_BOTS:
            return False

        # Don't scale down if queue has work
        if queue_size > 0:
            return False

        # Don't scale down if bots are busy
        if avg_bot_load > 0.3:
            return False

        # Check idle duration
        if not self.idle_start_time:
            self.idle_start_time = datetime.now()
            return False

        idle_duration = (datetime.now() - self.idle_start_time).total_seconds()

        # Scale down only after idle for threshold duration
        if idle_duration >= self.IDLE_TIME_FOR_SCALE_DOWN_SECONDS:
            # Check cooldown
            if self.last_scale_down_time:
                elapsed = (datetime.now() - self.last_scale_down_time).total_seconds()
                if elapsed < self.SCALE_DOWN_COOLDOWN_SECONDS:
                    return False

            return True

        return False

    def scale_up(self, count: int = 1) -> Tuple[bool, List[str]]:
        """
        Add bots to the system.

        Args:
            count: Number of bots to add (default 1)

        Returns:
            Tuple of (success, list of new bot IDs)
        """
        if not self._check_system_resources():
            self._log_event("scale_up_blocked", "insufficient_resources")
            return False, []

        if self.current_bot_count + count > self.MAX_BOTS:
            count = self.MAX_BOTS - self.current_bot_count

        if count <= 0:
            return False, []

        new_bots = []

        for i in range(count):
            bot_id = self._generate_bot_id()

            try:
                # Launch bot (actual implementation depends on bot_launcher script)
                pid = self._launch_bot(bot_id)

                if pid:
                    self.active_bots[bot_id] = {
                        "pid": pid,
                        "launched_at": datetime.now().isoformat(),
                        "status": "starting"
                    }
                    self.current_bot_count += 1
                    new_bots.append(bot_id)

                    self._log_event("bot_launched", bot_id, {"pid": pid})

            except Exception as e:
                self._log_event("launch_failed", bot_id, {"error": str(e)})

        if new_bots:
            self.last_scale_up_time = datetime.now()
            self.idle_start_time = None  # Reset idle timer

            self._log_event("scaled_up", None, {
                "added": len(new_bots),
                "new_total": self.current_bot_count,
                "bot_ids": new_bots
            })

        return len(new_bots) > 0, new_bots

    def scale_down(self, count: int = 1) -> Tuple[bool, List[str]]:
        """
        Remove bots from the system.

        Args:
            count: Number of bots to remove (default 1)

        Returns:
            Tuple of (success, list of removed bot IDs)
        """
        if self.current_bot_count - count < self.MIN_BOTS:
            count = self.current_bot_count - self.MIN_BOTS

        if count <= 0:
            return False, []

        removed_bots = []

        # Remove least-recently-launched bots
        bots_by_age = sorted(
            self.active_bots.items(),
            key=lambda x: x[1]["launched_at"]
        )

        for bot_id, info in bots_by_age[:count]:
            try:
                self._terminate_bot(bot_id, info["pid"])
                del self.active_bots[bot_id]
                self.current_bot_count -= 1
                removed_bots.append(bot_id)

                self._log_event("bot_terminated", bot_id, {"pid": info["pid"]})

            except Exception as e:
                self._log_event("termination_failed", bot_id, {"error": str(e)})

        if removed_bots:
            self.last_scale_down_time = datetime.now()

            self._log_event("scaled_down", None, {
                "removed": len(removed_bots),
                "new_total": self.current_bot_count,
                "bot_ids": removed_bots
            })

        return len(removed_bots) > 0, removed_bots

    def evaluate_and_scale(
        self,
        current_load: float,
        queue_size: int,
        avg_bot_load: float
    ) -> Optional[ScalingAction]:
        """
        Evaluate system state and take scaling action if needed.

        Args:
            current_load: System load (0.0-1.0)
            queue_size: Queued tasks
            avg_bot_load: Average bot load (0.0-1.0)

        Returns:
            Scaling action taken, or None if no change
        """
        system_memory = psutil.virtual_memory().percent / 100.0
        system_cpu = psutil.cpu_percent(interval=0.1) / 100.0

        metrics = ScalingMetrics(
            timestamp=datetime.now().isoformat(),
            current_bot_count=self.current_bot_count,
            system_load_avg=current_load,
            total_queue_size=queue_size,
            avg_bot_load=avg_bot_load,
            system_memory_percent=system_memory,
            system_cpu_percent=system_cpu
        )

        # Determine action
        if self.should_scale_up(current_load, queue_size, avg_bot_load):
            success, new_bots = self.scale_up()
            metrics.scaling_action = ScalingAction.SCALE_UP if success else ScalingAction.NO_CHANGE

        elif self.should_scale_down(queue_size, avg_bot_load):
            success, removed_bots = self.scale_down()
            metrics.scaling_action = ScalingAction.SCALE_DOWN if success else ScalingAction.NO_CHANGE

        # Log metrics
        self._log_metrics(metrics)

        return metrics.scaling_action if metrics.scaling_action != ScalingAction.NO_CHANGE else None

    def get_scaling_status(self) -> Dict:
        """Get current scaling status."""
        return {
            "timestamp": datetime.now().isoformat(),
            "current_bot_count": self.current_bot_count,
            "min_bots": self.MIN_BOTS,
            "max_bots": self.MAX_BOTS,
            "active_bots": list(self.active_bots.keys()),
            "scaling_enabled": True,
            "last_scale_up": self.last_scale_up_time.isoformat() if self.last_scale_up_time else None,
            "last_scale_down": self.last_scale_down_time.isoformat() if self.last_scale_down_time else None
        }

    def _check_system_resources(self) -> bool:
        """Check if system has resources available for more bots."""
        try:
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=0.1)

            memory_available = (memory.percent / 100.0) < self.SYSTEM_MEMORY_THRESHOLD
            cpu_available = (cpu / 100.0) < self.SYSTEM_CPU_THRESHOLD

            return memory_available and cpu_available

        except Exception:
            return True  # Default to allowing if can't check

    def _launch_bot(self, bot_id: str) -> Optional[int]:
        """
        Launch a bot process.

        Args:
            bot_id: Bot identifier

        Returns:
            PID of launched bot, or None if failed
        """
        if not self.bot_launcher:
            return None

        try:
            # Launch bot asynchronously
            process = subprocess.Popen(
                ["python", str(self.bot_launcher), bot_id],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True  # Detach from parent
            )

            return process.pid

        except Exception as e:
            print(f"[AUTO-SCALER] Failed to launch {bot_id}: {e}")
            return None

    def _terminate_bot(self, bot_id: str, pid: int) -> None:
        """
        Gracefully terminate a bot.

        Args:
            bot_id: Bot identifier
            pid: Process ID
        """
        try:
            import signal
            os.kill(pid, signal.SIGTERM)
        except Exception:
            pass

    def _generate_bot_id(self) -> str:
        """Generate unique bot ID."""
        timestamp = int(datetime.now().timestamp() * 1000)
        return f"BOT-SCALED-{timestamp}"

    def _log_event(self, event: str, bot_id: Optional[str], details: Dict = None) -> None:
        """Log scaling event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "bot_id": bot_id,
            "details": details or {}
        }

        try:
            with open(self.scaling_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[AUTO-SCALER] Failed to log event: {e}")

    def _log_metrics(self, metrics: ScalingMetrics) -> None:
        """Log scaling metrics."""
        try:
            with open(self.metrics_log, "a") as f:
                f.write(json.dumps({
                    "timestamp": metrics.timestamp,
                    "current_bot_count": metrics.current_bot_count,
                    "system_load_avg": metrics.system_load_avg,
                    "total_queue_size": metrics.total_queue_size,
                    "avg_bot_load": metrics.avg_bot_load,
                    "system_memory_percent": metrics.system_memory_percent,
                    "system_cpu_percent": metrics.system_cpu_percent,
                    "scaling_action": metrics.scaling_action.value
                }) + "\n")
        except Exception as e:
            print(f"[AUTO-SCALER] Failed to log metrics: {e}")
