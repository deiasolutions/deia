"""
Analytics Collector - Track usage patterns, performance trends, and engagement metrics.

Collects and aggregates:
- Message volume per hour/day
- User engagement metrics
- Bot utilization patterns
- Error rate trends
- Performance metrics over time

All data persisted to analytics.jsonl for historical analysis.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import json
import statistics


@dataclass
class MessageVolume:
    """Message volume metrics for a time period."""
    timestamp: str
    hour: int
    day: str
    messages_sent: int
    messages_received: int
    unique_users: int
    unique_bots: int
    total_characters: int


@dataclass
class UserEngagement:
    """User engagement metrics."""
    user_id: str
    first_message: str
    last_message: str
    total_messages: int
    total_sessions: int
    avg_session_length_seconds: float
    commands_used: List[str]
    bots_interacted: List[str]


@dataclass
class BotUtilization:
    """Bot utilization metrics."""
    bot_id: str
    messages_processed: int
    avg_response_time_ms: float
    error_rate: float
    peak_usage_hour: int
    utilization_percentage: float


@dataclass
class PerformanceMetric:
    """Performance metric snapshot."""
    timestamp: str
    avg_message_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    throughput_msg_per_second: float
    system_cpu_percent: float
    system_memory_percent: float


class AnalyticsCollector:
    """
    Collect and aggregate analytics data for the chat system.

    Tracks usage patterns, performance trends, and engagement metrics.
    Stores data to analytics.jsonl for historical analysis.
    """

    def __init__(self, work_dir: Path):
        """
        Initialize analytics collector.

        Args:
            work_dir: Working directory for logs and data
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.analytics_file = self.log_dir / "analytics.jsonl"

        # Track data
        self.message_history: List[Dict[str, Any]] = []
        self.volume_per_hour: Dict[str, int] = defaultdict(int)
        self.user_engagement: Dict[str, UserEngagement] = {}
        self.bot_utilization: Dict[str, BotUtilization] = {}
        self.performance_metrics: List[PerformanceMetric] = []

        # Load existing data
        self._load_from_file()

    def record_message(
        self,
        user_id: str,
        bot_id: str,
        content: str,
        direction: str,  # "sent" or "received"
        latency_ms: float = 0.0
    ) -> None:
        """
        Record a message event.

        Args:
            user_id: User who sent/received
            bot_id: Bot involved
            content: Message content
            direction: "sent" or "received"
            latency_ms: Message latency in milliseconds
        """
        now = datetime.now()
        hour_key = f"{now.date()}-{now.hour:02d}"

        event = {
            "timestamp": now.isoformat(),
            "user_id": user_id,
            "bot_id": bot_id,
            "content_length": len(content),
            "direction": direction,
            "latency_ms": latency_ms
        }

        self.message_history.append(event)
        self.volume_per_hour[hour_key] += 1

        # Update user engagement
        if user_id not in self.user_engagement:
            self.user_engagement[user_id] = UserEngagement(
                user_id=user_id,
                first_message=now.isoformat(),
                last_message=now.isoformat(),
                total_messages=0,
                total_sessions=1,
                avg_session_length_seconds=0.0,
                commands_used=[],
                bots_interacted=[]
            )

        engagement = self.user_engagement[user_id]
        engagement.last_message = now.isoformat()
        engagement.total_messages += 1

        if bot_id not in engagement.bots_interacted:
            engagement.bots_interacted.append(bot_id)

        # Update bot utilization
        if bot_id not in self.bot_utilization:
            self.bot_utilization[bot_id] = BotUtilization(
                bot_id=bot_id,
                messages_processed=0,
                avg_response_time_ms=0.0,
                error_rate=0.0,
                peak_usage_hour=now.hour,
                utilization_percentage=0.0
            )

        bot_util = self.bot_utilization[bot_id]
        bot_util.messages_processed += 1

        if direction == "received":
            # Update response time tracking
            if bot_util.avg_response_time_ms == 0:
                bot_util.avg_response_time_ms = latency_ms
            else:
                bot_util.avg_response_time_ms = (
                    (bot_util.avg_response_time_ms + latency_ms) / 2
                )

        # Log to file
        self._log_event(event)

    def record_performance(
        self,
        latencies_ms: List[float],
        throughput_msg_per_sec: float,
        cpu_percent: float,
        memory_percent: float
    ) -> None:
        """
        Record system performance metrics.

        Args:
            latencies_ms: List of message latencies
            throughput_msg_per_sec: Messages per second
            cpu_percent: CPU utilization (0-1)
            memory_percent: Memory utilization (0-1)
        """
        if not latencies_ms:
            return

        metric = PerformanceMetric(
            timestamp=datetime.now().isoformat(),
            avg_message_latency_ms=statistics.mean(latencies_ms),
            p95_latency_ms=self._percentile(latencies_ms, 0.95),
            p99_latency_ms=self._percentile(latencies_ms, 0.99),
            throughput_msg_per_second=throughput_msg_per_sec,
            system_cpu_percent=cpu_percent,
            system_memory_percent=memory_percent
        )

        self.performance_metrics.append(metric)
        self._log_event(asdict(metric))

    def get_message_volume(self, hours: int = 24) -> Dict[str, int]:
        """
        Get message volume per hour for last N hours.

        Args:
            hours: Number of hours to look back

        Returns:
            Dict mapping hour key to message count
        """
        cutoff = datetime.now() - timedelta(hours=hours)
        result = {}

        for hour_key, count in self.volume_per_hour.items():
            try:
                hour_time = datetime.fromisoformat(hour_key.split("-")[0] + " " + hour_key.split("-")[1])
                if hour_time >= cutoff:
                    result[hour_key] = count
            except (ValueError, IndexError):
                pass

        return dict(sorted(result.items()))

    def get_user_engagement(self) -> Dict[str, Dict[str, Any]]:
        """
        Get user engagement metrics.

        Returns:
            Dict of user_id -> engagement data
        """
        return {
            user_id: {
                "total_messages": eng.total_messages,
                "total_sessions": eng.total_sessions,
                "bots_interacted": len(eng.bots_interacted),
                "first_message": eng.first_message,
                "last_message": eng.last_message
            }
            for user_id, eng in self.user_engagement.items()
        }

    def get_bot_utilization(self) -> Dict[str, Dict[str, Any]]:
        """
        Get bot utilization metrics.

        Returns:
            Dict of bot_id -> utilization data
        """
        return {
            bot_id: {
                "messages_processed": util.messages_processed,
                "avg_response_time_ms": util.avg_response_time_ms,
                "error_rate": util.error_rate,
                "utilization_percentage": util.utilization_percentage
            }
            for bot_id, util in self.bot_utilization.items()
        }

    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """
        Get performance summary for last N hours.

        Args:
            hours: Number of hours to analyze

        Returns:
            Performance summary statistics
        """
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [
            m for m in self.performance_metrics
            if datetime.fromisoformat(m.timestamp) >= cutoff
        ]

        if not recent:
            return {
                "avg_latency_ms": 0,
                "p95_latency_ms": 0,
                "p99_latency_ms": 0,
                "avg_throughput_msg_sec": 0,
                "avg_cpu_percent": 0,
                "avg_memory_percent": 0
            }

        return {
            "avg_latency_ms": statistics.mean([m.avg_message_latency_ms for m in recent]),
            "p95_latency_ms": statistics.mean([m.p95_latency_ms for m in recent]),
            "p99_latency_ms": statistics.mean([m.p99_latency_ms for m in recent]),
            "avg_throughput_msg_sec": statistics.mean([m.throughput_msg_per_second for m in recent]),
            "avg_cpu_percent": statistics.mean([m.system_cpu_percent for m in recent]),
            "avg_memory_percent": statistics.mean([m.system_memory_percent for m in recent]),
            "samples": len(recent),
            "hours": hours
        }

    def get_peak_usage_hour(self) -> Dict[str, Any]:
        """
        Identify peak usage hour.

        Returns:
            Info about peak usage time
        """
        if not self.volume_per_hour:
            return {"peak_hour": None, "message_count": 0}

        peak_hour = max(self.volume_per_hour.items(), key=lambda x: x[1])

        return {
            "peak_hour": peak_hour[0],
            "message_count": peak_hour[1]
        }

    def get_active_users_count(self) -> int:
        """Get count of active users."""
        return len(self.user_engagement)

    def get_active_bots_count(self) -> int:
        """Get count of active bots."""
        return len(self.bot_utilization)

    def _percentile(self, values: List[float], percentile: float) -> float:
        """Calculate percentile of values."""
        if not values:
            return 0.0

        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile)
        return sorted_values[min(index, len(sorted_values) - 1)]

    def _log_event(self, event: Dict[str, Any]) -> None:
        """Log event to analytics file."""
        try:
            with open(self.analytics_file, "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            print(f"[ANALYTICS] Failed to log event: {e}")

    def _load_from_file(self) -> None:
        """Load existing analytics from file."""
        if not self.analytics_file.exists():
            return

        try:
            with open(self.analytics_file, "r") as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        if "direction" in event:
                            # Message event
                            hour_key = event["timestamp"][:13].replace("T", "-")
                            self.volume_per_hour[hour_key] += 1
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            print(f"[ANALYTICS] Failed to load from file: {e}")

    def export_summary(self) -> Dict[str, Any]:
        """
        Export comprehensive analytics summary.

        Returns:
            Complete analytics snapshot
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "total_messages": len(self.message_history),
            "active_users": self.get_active_users_count(),
            "active_bots": self.get_active_bots_count(),
            "peak_usage": self.get_peak_usage_hour(),
            "performance_24h": self.get_performance_summary(24),
            "user_engagement": self.get_user_engagement(),
            "bot_utilization": self.get_bot_utilization()
        }
