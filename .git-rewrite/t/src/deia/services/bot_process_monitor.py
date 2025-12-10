"""
Bot Process Monitor - Deep visibility into bot subprocess health.

Tracks system resource usage (memory, file descriptors, threads, GC),
detects memory leaks and handle exhaustion, alerts on anomalies.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import json
import psutil


@dataclass
class ProcessMetrics:
    """Process metrics snapshot for a bot."""
    bot_id: str
    timestamp: str
    pid: int
    memory_mb: float
    memory_percent: float
    rss_mb: float  # Resident set size
    vms_mb: float  # Virtual memory size
    file_descriptors: int
    thread_count: int
    open_connections: int
    cpu_percent: float
    num_fds: int  # Number of open file descriptors

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class MemoryTrend:
    """Track memory usage over time for leak detection."""
    bot_id: str
    start_time: str
    measurements: List[float] = None  # Memory values over time
    duration_minutes: int = 0
    growth_rate_mb_per_hour: float = 0.0
    is_leaking: bool = False


class BotProcessMonitor:
    """
    Monitor bot subprocess health and resource usage.

    Features:
    - Track memory, file descriptors, threads, CPU
    - Detect memory leaks via trend analysis
    - Detect handle/file descriptor exhaustion
    - Anomaly detection on unusual patterns
    - Comprehensive logging
    """

    # Thresholds for anomalies
    MEMORY_GROWTH_THRESHOLD_MB_PER_HOUR = 10.0  # Alert if growing >10 MB/hour
    MEMORY_PERCENT_WARNING = 0.5  # Alert if >50% system memory
    MEMORY_PERCENT_CRITICAL = 0.8  # Alert if >80% system memory
    FILE_DESCRIPTORS_WARNING = 900  # Alert if >900 FDs (typical limit ~1024)
    FILE_DESCRIPTORS_CRITICAL = 950  # Alert if >950 FDs
    THREADS_WARNING = 100  # Alert if >100 threads
    CPU_PERCENT_WARNING = 0.8  # Alert if >80% CPU
    TREND_WINDOW_MINUTES = 60  # Track over 1 hour for leak detection

    def __init__(self, work_dir: Path):
        """
        Initialize process monitor.

        Args:
            work_dir: Working directory for logs
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.health_log = self.log_dir / "bot-process-health.jsonl"

        # Track metrics over time for trend analysis
        self.metric_history: Dict[str, List[ProcessMetrics]] = {}
        self.memory_trends: Dict[str, MemoryTrend] = {}
        self.alerts: Dict[str, List[str]] = {}

    def monitor_bot(self, bot_id: str, pid: int) -> ProcessMetrics:
        """
        Monitor a single bot process.

        Args:
            bot_id: Bot identifier
            pid: Process ID to monitor

        Returns:
            ProcessMetrics snapshot
        """
        try:
            process = psutil.Process(pid)

            # Collect metrics
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()
            fd_count = len(process.open_files())
            thread_count = process.num_threads()
            cpu_percent = process.cpu_percent(interval=0.1)
            open_conns = len(process.net_connections())

            metrics = ProcessMetrics(
                bot_id=bot_id,
                timestamp=datetime.now().isoformat(),
                pid=pid,
                memory_mb=memory_info.rss / (1024 * 1024),
                memory_percent=memory_percent / 100.0,
                rss_mb=memory_info.rss / (1024 * 1024),
                vms_mb=memory_info.vms / (1024 * 1024),
                file_descriptors=fd_count,
                thread_count=thread_count,
                open_connections=open_conns,
                cpu_percent=cpu_percent / 100.0,
                num_fds=fd_count
            )

            # Track history
            if bot_id not in self.metric_history:
                self.metric_history[bot_id] = []
            self.metric_history[bot_id].append(metrics)

            # Keep only recent history (1 hour window)
            cutoff = datetime.now() - timedelta(minutes=self.TREND_WINDOW_MINUTES)
            self.metric_history[bot_id] = [
                m for m in self.metric_history[bot_id]
                if datetime.fromisoformat(m.timestamp) > cutoff
            ]

            # Check for anomalies
            self._check_anomalies(bot_id, metrics)

            # Log metrics
            self._log_metrics(metrics)

            return metrics

        except psutil.NoSuchProcess:
            self._log_event("process_not_found", bot_id, {"pid": pid})
            return None
        except Exception as e:
            self._log_event("monitoring_error", bot_id, {"error": str(e), "pid": pid})
            return None

    def detect_memory_leak(self, bot_id: str) -> Optional[MemoryTrend]:
        """
        Analyze memory trend to detect potential leaks.

        Memory leak detection: if memory grows >10 MB/hour over 1 hour window.

        Args:
            bot_id: Bot identifier

        Returns:
            MemoryTrend if leak detected, None otherwise
        """
        if bot_id not in self.metric_history or len(self.metric_history[bot_id]) < 2:
            return None

        history = self.metric_history[bot_id]
        if len(history) < 3:  # Need at least 3 points for trend
            return None

        # Calculate memory growth
        first_metric = history[0]
        last_metric = history[-1]

        first_time = datetime.fromisoformat(first_metric.timestamp)
        last_time = datetime.fromisoformat(last_metric.timestamp)
        duration_minutes = (last_time - first_time).total_seconds() / 60

        if duration_minutes < 10:  # Need at least 10 minutes of data
            return None

        memory_growth_mb = last_metric.memory_mb - first_metric.memory_mb
        growth_rate_mb_per_hour = (memory_growth_mb / duration_minutes) * 60

        is_leaking = growth_rate_mb_per_hour > self.MEMORY_GROWTH_THRESHOLD_MB_PER_HOUR

        trend = MemoryTrend(
            bot_id=bot_id,
            start_time=first_metric.timestamp,
            measurements=[m.memory_mb for m in history],
            duration_minutes=int(duration_minutes),
            growth_rate_mb_per_hour=growth_rate_mb_per_hour,
            is_leaking=is_leaking
        )

        self.memory_trends[bot_id] = trend

        if is_leaking:
            self._log_event("memory_leak_detected", bot_id, {
                "growth_rate": growth_rate_mb_per_hour,
                "duration_minutes": int(duration_minutes),
                "memory_growth_mb": memory_growth_mb
            })

        return trend

    def get_bot_health(self, bot_id: str) -> Dict[str, Any]:
        """
        Get comprehensive health report for a bot.

        Args:
            bot_id: Bot identifier

        Returns:
            Health summary
        """
        if bot_id not in self.metric_history or not self.metric_history[bot_id]:
            return {"status": "no_data"}

        latest = self.metric_history[bot_id][-1]
        trend = self.memory_trends.get(bot_id)
        alerts = self.alerts.get(bot_id, [])

        status = "healthy"
        if alerts:
            status = "warning"

        return {
            "bot_id": bot_id,
            "status": status,
            "latest_metrics": latest.to_dict(),
            "memory_trend": {
                "is_leaking": trend.is_leaking if trend else False,
                "growth_rate_mb_per_hour": trend.growth_rate_mb_per_hour if trend else 0,
                "duration_minutes": trend.duration_minutes if trend else 0
            } if trend else None,
            "alerts": alerts,
            "timestamp": datetime.now().isoformat()
        }

    def get_all_health(self) -> Dict[str, Dict]:
        """
        Get health for all monitored bots.

        Returns:
            Dict of bot_id -> health summary
        """
        return {
            bot_id: self.get_bot_health(bot_id)
            for bot_id in self.metric_history.keys()
        }

    def _check_anomalies(self, bot_id: str, metrics: ProcessMetrics) -> None:
        """Check for anomalies and generate alerts."""
        if bot_id not in self.alerts:
            self.alerts[bot_id] = []

        alerts = []

        # Memory checks
        if metrics.memory_percent > self.MEMORY_PERCENT_CRITICAL:
            alerts.append(f"CRITICAL: Memory usage {metrics.memory_percent*100:.1f}%")
        elif metrics.memory_percent > self.MEMORY_PERCENT_WARNING:
            alerts.append(f"WARNING: Memory usage {metrics.memory_percent*100:.1f}%")

        # File descriptor checks
        if metrics.file_descriptors > self.FILE_DESCRIPTORS_CRITICAL:
            alerts.append(f"CRITICAL: {metrics.file_descriptors} file descriptors (limit ~1024)")
        elif metrics.file_descriptors > self.FILE_DESCRIPTORS_WARNING:
            alerts.append(f"WARNING: {metrics.file_descriptors} file descriptors")

        # Thread checks
        if metrics.thread_count > self.THREADS_WARNING:
            alerts.append(f"WARNING: {metrics.thread_count} threads (high)")

        # CPU checks
        if metrics.cpu_percent > self.CPU_PERCENT_WARNING:
            alerts.append(f"WARNING: CPU {metrics.cpu_percent*100:.1f}%")

        # Memory leak check
        trend = self.detect_memory_leak(bot_id)
        if trend and trend.is_leaking:
            alerts.append(f"WARNING: Possible memory leak ({trend.growth_rate_mb_per_hour:.1f} MB/hour)")

        self.alerts[bot_id] = alerts

        if alerts:
            for alert in alerts:
                self._log_event("anomaly_detected", bot_id, {"alert": alert})

    def _log_metrics(self, metrics: ProcessMetrics) -> None:
        """Log process metrics."""
        entry = {
            "timestamp": metrics.timestamp,
            "bot_id": metrics.bot_id,
            "pid": metrics.pid,
            "memory_mb": metrics.memory_mb,
            "memory_percent": metrics.memory_percent,
            "file_descriptors": metrics.file_descriptors,
            "thread_count": metrics.thread_count,
            "cpu_percent": metrics.cpu_percent
        }

        try:
            with open(self.health_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[PROCESS-MONITOR] Failed to log metrics: {e}")

    def _log_event(self, event: str, bot_id: str, details: Dict = None) -> None:
        """Log process monitor event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "bot_id": bot_id,
            "details": details or {}
        }

        try:
            with open(self.health_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[PROCESS-MONITOR] Failed to log event: {e}")
