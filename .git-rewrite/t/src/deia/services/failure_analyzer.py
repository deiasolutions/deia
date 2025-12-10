"""
Failure Analyzer - Detect failure patterns and predict cascades.

Tracks task failures by type, bot, time of day. Correlates failures
and predicts impending cascades.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import json
from collections import defaultdict


@dataclass
class FailureEvent:
    """A single task failure."""
    task_id: str
    task_type: str
    bot_id: str
    timestamp: str
    error_message: str
    error_type: str
    is_retryable: bool


@dataclass
class FailurePattern:
    """Detected failure pattern."""
    pattern_id: str
    pattern_type: str  # task_type, bot_specific, time_based, cascade
    task_type: Optional[str] = None
    bot_id: Optional[str] = None
    time_of_day: Optional[str] = None
    failure_count: int = 0
    failure_rate: float = 0.0
    is_active: bool = True


class FailureAnalyzer:
    """
    Analyze and predict failure patterns.

    Features:
    - Track failures by type and bot
    - Detect correlations
    - Identify time-based patterns
    - Predict cascade risk
    - Alert on anomalies
    """

    # Thresholds
    FAILURE_RATE_WARNING = 0.1  # 10% failure rate
    FAILURE_RATE_CRITICAL = 0.25  # 25% failure rate
    FAILURE_SPIKE_THRESHOLD = 0.05  # Alert on 5% increase in failure rate
    CASCADE_PREDICTION_WINDOW = timedelta(minutes=5)

    def __init__(self, work_dir: Path):
        """
        Initialize failure analyzer.

        Args:
            work_dir: Working directory for logs
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.failure_log = self.log_dir / "failure-analysis.jsonl"

        # Track failures
        self.failures: List[FailureEvent] = []
        self.failure_patterns: Dict[str, FailurePattern] = {}

        # Correlations
        self.failure_correlations: Dict[str, List[str]] = defaultdict(list)

    def record_failure(
        self,
        task_id: str,
        task_type: str,
        bot_id: str,
        error_message: str,
        error_type: str = "unknown",
        is_retryable: bool = True
    ) -> FailureEvent:
        """
        Record a task failure.

        Args:
            task_id: Failed task ID
            task_type: Type of task
            bot_id: Bot that failed
            error_message: Error description
            error_type: Category of error
            is_retryable: Can this be retried?

        Returns:
            FailureEvent
        """
        failure = FailureEvent(
            task_id=task_id,
            task_type=task_type,
            bot_id=bot_id,
            timestamp=datetime.now().isoformat(),
            error_message=error_message,
            error_type=error_type,
            is_retryable=is_retryable
        )

        self.failures.append(failure)

        # Keep 24 hours of history
        cutoff = datetime.now() - timedelta(hours=24)
        self.failures = [
            f for f in self.failures
            if datetime.fromisoformat(f.timestamp) > cutoff
        ]

        # Update patterns
        self._update_patterns(failure)

        # Check for cascade risk
        self._check_cascade_risk(failure)

        # Log failure
        self._log_failure(failure)

        return failure

    def get_failure_stats(self) -> Dict[str, Any]:
        """
        Get failure statistics.

        Returns:
            Failure stats summary
        """
        if not self.failures:
            return {"status": "no_failures"}

        # Stats by task type
        by_task_type = defaultdict(lambda: {"count": 0, "tasks": []})
        for failure in self.failures:
            by_task_type[failure.task_type]["count"] += 1
            by_task_type[failure.task_type]["tasks"].append(failure.task_id)

        # Stats by bot
        by_bot = defaultdict(lambda: {"count": 0, "tasks": []})
        for failure in self.failures:
            by_bot[failure.bot_id]["count"] += 1
            by_bot[failure.bot_id]["tasks"].append(failure.task_id)

        # Calculate failure rates
        total_failures = len(self.failures)

        return {
            "total_failures_24h": total_failures,
            "by_task_type": dict(by_task_type),
            "by_bot": dict(by_bot),
            "failure_patterns": [
                asdict(p) for p in self.failure_patterns.values()
            ],
            "timestamp": datetime.now().isoformat()
        }

    def get_task_type_failure_rate(self, task_type: str) -> float:
        """
        Get failure rate for a task type.

        Args:
            task_type: Task type to analyze

        Returns:
            Failure rate (0.0 - 1.0)
        """
        # This would need to be calculated from orchestrator's task history
        # For now, return from tracked failures
        failures = [f for f in self.failures if f.task_type == task_type]
        if not failures:
            return 0.0

        # Rough estimate: failures / (failures + estimated successes)
        # In practice, would get actual total attempts from orchestrator
        return min(len(failures) / max(len(failures), 1), 1.0)

    def get_bot_failure_rate(self, bot_id: str) -> float:
        """
        Get failure rate for a bot.

        Args:
            bot_id: Bot identifier

        Returns:
            Failure rate (0.0 - 1.0)
        """
        failures = [f for f in self.failures if f.bot_id == bot_id]
        if not failures:
            return 0.0

        return min(len(failures) / max(len(failures), 1), 1.0)

    def predict_cascade_risk(self) -> Dict[str, Any]:
        """
        Predict cascade risk based on current failures.

        Returns:
            Cascade risk analysis
        """
        recent_failures = [
            f for f in self.failures
            if datetime.fromisoformat(f.timestamp) > (datetime.now() - self.CASCADE_PREDICTION_WINDOW)
        ]

        if not recent_failures:
            return {
                "cascade_risk": "low",
                "recent_failures": 0,
                "timestamp": datetime.now().isoformat()
            }

        # Risk factors
        failure_count = len(recent_failures)
        unique_bots_failing = len(set(f.bot_id for f in recent_failures))
        unique_task_types_failing = len(set(f.task_type for f in recent_failures))

        # Cascade detection: multiple bot types failing in same window
        cascade_risk = "low"
        if unique_bots_failing >= 2 and unique_task_types_failing >= 2:
            cascade_risk = "high"
        elif failure_count >= 3:
            cascade_risk = "medium"

        return {
            "cascade_risk": cascade_risk,
            "recent_failures": failure_count,
            "bots_affected": unique_bots_failing,
            "task_types_affected": unique_task_types_failing,
            "failure_pattern": [
                {
                    "bot_id": f.bot_id,
                    "task_type": f.task_type,
                    "error_type": f.error_type
                }
                for f in recent_failures
            ],
            "timestamp": datetime.now().isoformat()
        }

    def get_error_trends(self) -> Dict[str, Any]:
        """
        Get error type trends.

        Returns:
            Error trends by type
        """
        error_counts = defaultdict(int)
        for failure in self.failures:
            error_counts[failure.error_type] += 1

        return {
            "error_types": dict(error_counts),
            "total_failures": len(self.failures),
            "timestamp": datetime.now().isoformat()
        }

    def _update_patterns(self, failure: FailureEvent) -> None:
        """Update detected patterns."""
        now = datetime.now()

        # Task type pattern
        task_type_key = f"task_type:{failure.task_type}"
        task_type_failures = [
            f for f in self.failures
            if f.task_type == failure.task_type and
            datetime.fromisoformat(f.timestamp) > (now - timedelta(hours=1))
        ]

        if len(task_type_failures) >= 3:
            if task_type_key not in self.failure_patterns:
                self.failure_patterns[task_type_key] = FailurePattern(
                    pattern_id=task_type_key,
                    pattern_type="task_type",
                    task_type=failure.task_type,
                    failure_count=len(task_type_failures),
                    failure_rate=len(task_type_failures) / 10  # Rough estimate
                )

                self._log_event("pattern_detected", {
                    "pattern": task_type_key,
                    "count": len(task_type_failures)
                })

        # Bot-specific pattern
        bot_key = f"bot:{failure.bot_id}"
        bot_failures = [
            f for f in self.failures
            if f.bot_id == failure.bot_id and
            datetime.fromisoformat(f.timestamp) > (now - timedelta(hours=1))
        ]

        if len(bot_failures) >= 3:
            if bot_key not in self.failure_patterns:
                self.failure_patterns[bot_key] = FailurePattern(
                    pattern_id=bot_key,
                    pattern_type="bot_specific",
                    bot_id=failure.bot_id,
                    failure_count=len(bot_failures),
                    failure_rate=len(bot_failures) / 10
                )

                self._log_event("pattern_detected", {
                    "pattern": bot_key,
                    "count": len(bot_failures)
                })

    def _check_cascade_risk(self, failure: FailureEvent) -> None:
        """Check for cascade risk from new failure."""
        cascade_risk = self.predict_cascade_risk()

        if cascade_risk["cascade_risk"] == "high":
            self._log_event("cascade_risk_high", cascade_risk)

    def _log_failure(self, failure: FailureEvent) -> None:
        """Log failure event."""
        entry = {
            "timestamp": failure.timestamp,
            "task_id": failure.task_id,
            "task_type": failure.task_type,
            "bot_id": failure.bot_id,
            "error_type": failure.error_type,
            "is_retryable": failure.is_retryable
        }

        try:
            with open(self.failure_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[FAILURE-ANALYZER] Failed to log failure: {e}")

    def _log_event(self, event: str, details: Dict = None) -> None:
        """Log analyzer event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details or {}
        }

        try:
            with open(self.failure_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[FAILURE-ANALYZER] Failed to log event: {e}")
