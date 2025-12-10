"""
Bot Resource Monitor - CPU and memory tracking for bot processes.

Monitors resource usage per bot, detects runaway processes, logs metrics.
Alerts when bot exceeds resource limits.
"""

import psutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from collections import deque


@dataclass
class ResourceMetric:
    """Snapshot of bot resource usage."""
    timestamp: str
    bot_id: str
    pid: int
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    threads: int
    uptime_seconds: Optional[float] = None


class BotResourceMonitor:
    """
    Monitors resource usage of bot subprocesses.

    Features:
    - Track CPU and memory per bot
    - Detect runaway processes
    - Alert on resource limits
    - Historical metric logging
    - Resource trend analysis
    """

    # Default limits
    CPU_ALERT_THRESHOLD = 80  # Percent
    MEMORY_ALERT_THRESHOLD_MB = 500  # Megabytes
    THREAD_ALERT_THRESHOLD = 100  # Thread count

    def __init__(
        self,
        bot_id: str,
        work_dir: Path,
        cpu_threshold: float = CPU_ALERT_THRESHOLD,
        memory_threshold_mb: float = MEMORY_ALERT_THRESHOLD_MB
    ):
        """
        Initialize resource monitor.

        Args:
            bot_id: Bot identifier
            work_dir: Working directory for logs
            cpu_threshold: Alert if CPU exceeds this % (default 80)
            memory_threshold_mb: Alert if memory exceeds this MB (default 500)
        """
        self.bot_id = bot_id
        self.work_dir = Path(work_dir)
        self.cpu_threshold = cpu_threshold
        self.memory_threshold_mb = memory_threshold_mb

        # Log directory
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.resource_log_file = self.log_dir / f"BOT-{bot_id}-resources.jsonl"
        self.alert_log_file = self.log_dir / f"BOT-{bot_id}-resource-alerts.jsonl"

        # Historical metrics (keep last 60 samples for trend analysis)
        self.metric_history: Dict[int, deque] = {}  # PID -> deque of metrics

    def collect_metrics(self, pid: int) -> Optional[ResourceMetric]:
        """
        Collect resource metrics for a process.

        Args:
            pid: Process ID to monitor

        Returns:
            ResourceMetric or None if process not found
        """
        try:
            process = psutil.Process(pid)

            if not process.is_running():
                return None

            cpu_percent = process.cpu_percent(interval=0.1)
            mem_info = process.memory_info()
            memory_mb = mem_info.rss / (1024 * 1024)
            memory_percent = process.memory_percent()
            threads = process.num_threads()
            uptime = datetime.now().timestamp() - process.create_time()

            metric = ResourceMetric(
                timestamp=datetime.now().isoformat(),
                bot_id=self.bot_id,
                pid=pid,
                cpu_percent=cpu_percent,
                memory_mb=memory_mb,
                memory_percent=memory_percent,
                threads=threads,
                uptime_seconds=uptime
            )

            # Store in history
            if pid not in self.metric_history:
                self.metric_history[pid] = deque(maxlen=60)
            self.metric_history[pid].append(metric)

            # Log metric
            self._log_metric(metric)

            # Check for alerts
            self._check_alerts(metric)

            return metric

        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return None
        except Exception as e:
            return None

    def get_current_metrics(self, pid: int) -> Optional[Dict[str, Any]]:
        """
        Get current metrics for a process.

        Args:
            pid: Process ID

        Returns:
            Metrics dict or None if process not found
        """
        metric = self.collect_metrics(pid)
        if metric:
            return asdict(metric)
        return None

    def get_metric_history(self, pid: int, limit: int = 60) -> List[Dict[str, Any]]:
        """
        Get historical metrics for a process.

        Args:
            pid: Process ID
            limit: Maximum number of metrics to return

        Returns:
            List of metrics (newest first)
        """
        if pid not in self.metric_history:
            return []

        metrics = [asdict(m) for m in self.metric_history[pid]]
        return list(reversed(metrics))[:limit]

    def get_trend(self, pid: int) -> Optional[Dict[str, Any]]:
        """
        Get resource usage trend for a process.

        Analyzes the last 60 samples to determine trends.

        Args:
            pid: Process ID

        Returns:
            Trend dict with avg, min, max, direction or None
        """
        if pid not in self.metric_history or len(self.metric_history[pid]) < 2:
            return None

        metrics = list(self.metric_history[pid])

        # Calculate averages
        avg_cpu = sum(m.cpu_percent for m in metrics) / len(metrics)
        avg_memory = sum(m.memory_mb for m in metrics) / len(metrics)

        # Calculate trend (comparing first half to second half)
        mid = len(metrics) // 2
        first_half_cpu = sum(m.cpu_percent for m in metrics[:mid]) / mid
        second_half_cpu = sum(m.cpu_percent for m in metrics[mid:]) / (len(metrics) - mid)

        cpu_trend = "increasing" if second_half_cpu > first_half_cpu else "stable"

        return {
            "pid": pid,
            "avg_cpu_percent": avg_cpu,
            "avg_memory_mb": avg_memory,
            "cpu_trend": cpu_trend,
            "sample_count": len(metrics)
        }

    def is_runaway_process(
        self,
        pid: int,
        min_samples: int = 10
    ) -> bool:
        """
        Detect if process is a runaway (consistently high resource use).

        Args:
            pid: Process ID
            min_samples: Minimum samples before can declare runaway

        Returns:
            True if process appears to be runaway
        """
        if pid not in self.metric_history:
            return False

        metrics = list(self.metric_history[pid])
        if len(metrics) < min_samples:
            return False

        # Check if consistently exceeds thresholds
        high_cpu_count = sum(1 for m in metrics if m.cpu_percent > self.cpu_threshold)
        high_mem_count = sum(1 for m in metrics if m.memory_mb > self.memory_threshold_mb)

        # If 80% of samples are high, it's runaway
        threshold_ratio = 0.8
        if high_cpu_count / len(metrics) > threshold_ratio:
            return True
        if high_mem_count / len(metrics) > threshold_ratio:
            return True

        return False

    def get_all_process_summary(self) -> Dict[str, Any]:
        """
        Get summary of all monitored processes.

        Returns:
            Dictionary with current state of all processes
        """
        summary = {
            "bot_id": self.bot_id,
            "timestamp": datetime.now().isoformat(),
            "processes": {}
        }

        for pid in list(self.metric_history.keys()):
            current = self.get_current_metrics(pid)
            trend = self.get_trend(pid)
            is_runaway = self.is_runaway_process(pid)

            summary["processes"][str(pid)] = {
                "current": current,
                "trend": trend,
                "is_runaway": is_runaway
            }

        return summary

    def _check_alerts(self, metric: ResourceMetric) -> None:
        """Check if metric exceeds alert thresholds."""
        alerts = []

        if metric.cpu_percent > self.cpu_threshold:
            alerts.append(f"CPU {metric.cpu_percent}% exceeds threshold {self.cpu_threshold}%")

        if metric.memory_mb > self.memory_threshold_mb:
            alerts.append(f"Memory {metric.memory_mb}MB exceeds threshold {self.memory_threshold_mb}MB")

        if metric.threads > self.THREAD_ALERT_THRESHOLD:
            alerts.append(f"Threads {metric.threads} exceeds threshold {self.THREAD_ALERT_THRESHOLD}")

        for alert in alerts:
            self._log_alert(metric, alert)

    def _log_metric(self, metric: ResourceMetric) -> None:
        """Log resource metric."""
        with open(self.resource_log_file, "a") as f:
            f.write(json.dumps(asdict(metric)) + "\n")

    def _log_alert(self, metric: ResourceMetric, alert_msg: str) -> None:
        """Log resource alert."""
        alert = {
            "timestamp": metric.timestamp,
            "bot_id": self.bot_id,
            "pid": metric.pid,
            "alert": alert_msg,
            "cpu_percent": metric.cpu_percent,
            "memory_mb": metric.memory_mb
        }

        with open(self.alert_log_file, "a") as f:
            f.write(json.dumps(alert) + "\n")

        print(f"[{self.bot_id}] RESOURCE ALERT: {alert_msg}")

    def query_metrics(
        self,
        time_range_minutes: Optional[int] = None,
        alert_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Query metrics from log file.

        Args:
            time_range_minutes: Only return metrics from last N minutes (optional)
            alert_only: Only return periods with alerts (optional)

        Returns:
            List of metrics matching criteria
        """
        if not self.resource_log_file.exists():
            return []

        cutoff_time = None
        if time_range_minutes:
            from datetime import timedelta
            cutoff_time = datetime.now() - timedelta(minutes=time_range_minutes)

        metrics = []
        try:
            with open(self.resource_log_file, "r") as f:
                for line in f:
                    if line.strip():
                        metric = json.loads(line)

                        if cutoff_time:
                            ts = datetime.fromisoformat(metric["timestamp"])
                            if ts < cutoff_time:
                                continue

                        metrics.append(metric)
        except Exception as e:
            pass

        return metrics
