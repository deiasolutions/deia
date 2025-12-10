"""
Adaptive Scheduler - Learn and optimize bot performance per task type.

Tracks bot performance metrics on different task types and learns over time
which bots are fastest at what. Routes similar tasks to the same fast bot.
Uses exponential moving average for continuous learning.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import json
from enum import Enum


class TaskType(Enum):
    """Task type categories."""
    DEVELOPMENT = "development"
    ANALYSIS = "analysis"
    WRITING = "writing"
    PLANNING = "planning"
    VALIDATION = "validation"
    GENERAL = "general"


@dataclass
class BotTaskPerformance:
    """Performance metrics for a bot on a specific task type."""
    bot_id: str
    task_type: str
    total_tasks: int = 0
    avg_execution_time: float = 0.0  # seconds
    success_rate: float = 1.0  # 0.0 - 1.0
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class SchedulingRecommendation:
    """Recommendation for which bot to use for a task."""
    task_type: str
    recommended_bot: str
    confidence: float  # 0.0 - 1.0 (based on sample size and consistency)
    reason: str  # Why this bot was chosen
    alternatives: List[Dict] = field(default_factory=list)  # Other good options


class AdaptiveScheduler:
    """
    Adaptive task scheduler that learns bot performance over time.

    Features:
    - Track bot performance per task type
    - Learn using exponential moving average
    - Make routing recommendations
    - Provide performance insights
    - Log all scheduling decisions
    """

    # Learning rate for exponential moving average (0.0 - 1.0)
    # Higher = more recent data weighted more heavily
    LEARNING_RATE = 0.1

    # Minimum sample size before recommending a bot (avoid recommendations from single event)
    MIN_SAMPLES_FOR_RECOMMENDATION = 3

    # Minimum confidence threshold for strong recommendation
    MIN_CONFIDENCE_THRESHOLD = 0.7

    def __init__(self, work_dir: Path):
        """
        Initialize adaptive scheduler.

        Args:
            work_dir: Working directory for logs and state
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.scheduling_log = self.log_dir / "adaptive-scheduling.jsonl"

        # Performance tracking: {bot_id}-{task_type} -> BotTaskPerformance
        self.performance_db: Dict[str, BotTaskPerformance] = {}

        # Task assignments history for learning
        self.task_history: List[Dict] = []

    def record_task_execution(
        self,
        bot_id: str,
        task_type: str,
        execution_time: float,
        success: bool
    ) -> None:
        """
        Record a task execution and update learning.

        Args:
            bot_id: Bot that executed task
            task_type: Type of task
            execution_time: How long task took (seconds)
            success: Whether task succeeded
        """
        # Get or create performance record
        key = f"{bot_id}:{task_type}"
        if key not in self.performance_db:
            self.performance_db[key] = BotTaskPerformance(
                bot_id=bot_id,
                task_type=task_type
            )

        perf = self.performance_db[key]

        # Update using exponential moving average
        # EMA_new = EMA_old * (1 - alpha) + new_value * alpha
        if perf.total_tasks == 0:
            perf.avg_execution_time = execution_time
            perf.success_rate = 1.0 if success else 0.0
        else:
            perf.avg_execution_time = (
                perf.avg_execution_time * (1 - self.LEARNING_RATE) +
                execution_time * self.LEARNING_RATE
            )

            # Update success rate
            perf.success_rate = (
                perf.success_rate * (1 - self.LEARNING_RATE) +
                (1.0 if success else 0.0) * self.LEARNING_RATE
            )

        perf.total_tasks += 1
        perf.last_updated = datetime.now().isoformat()

        # Record in history
        self.task_history.append({
            "timestamp": datetime.now().isoformat(),
            "bot_id": bot_id,
            "task_type": task_type,
            "execution_time": execution_time,
            "success": success,
            "updated_perf": perf.to_dict()
        })

        # Log event
        self._log_event("task_recorded", {
            "bot_id": bot_id,
            "task_type": task_type,
            "execution_time": execution_time,
            "success": success,
            "avg_time": perf.avg_execution_time,
            "success_rate": perf.success_rate
        })

    def get_recommendation(
        self,
        task_type: str,
        available_bots: Optional[List[str]] = None
    ) -> Optional[SchedulingRecommendation]:
        """
        Get scheduling recommendation for a task type.

        Args:
            task_type: Type of task
            available_bots: List of bot IDs to consider (None = all)

        Returns:
            SchedulingRecommendation or None if not enough data
        """
        # Get performance records for this task type
        candidates = self._get_task_type_performers(task_type, available_bots)

        if not candidates:
            return None

        # Score bots: prefer faster execution + higher success rate
        best_bot = None
        best_score = -1.0
        scores = {}

        for perf in candidates:
            if perf.total_tasks < self.MIN_SAMPLES_FOR_RECOMMENDATION:
                continue

            # Composite score
            # Faster is better (invert time, normalize to 0-1)
            # Success rate directly
            time_score = max(0, 1 - (perf.avg_execution_time / 1000.0))  # Normalize with 1000s baseline
            time_score = min(1.0, time_score)
            success_score = perf.success_rate

            composite_score = (time_score * 0.4) + (success_score * 0.6)
            scores[perf.bot_id] = composite_score

            if composite_score > best_score:
                best_score = composite_score
                best_bot = perf

        if not best_bot:
            return None

        # Calculate confidence based on lead over second place
        sorted_scores = sorted(scores.values(), reverse=True)
        confidence = 0.5
        if len(sorted_scores) > 1:
            confidence = min(1.0, sorted_scores[0] - sorted_scores[1] + 0.5)
        else:
            confidence = 0.8

        # Get alternatives
        alternatives = [
            {
                "bot_id": perf.bot_id,
                "score": scores.get(perf.bot_id, 0),
                "avg_time": perf.avg_execution_time,
                "success_rate": perf.success_rate
            }
            for perf in sorted(candidates, key=lambda p: scores.get(p.bot_id, 0), reverse=True)[:3]
        ]

        reason = (
            f"Best performer on {task_type} tasks: "
            f"{best_bot.avg_execution_time:.1f}s avg, "
            f"{best_bot.success_rate:.0%} success rate "
            f"({best_bot.total_tasks} tasks)"
        )

        return SchedulingRecommendation(
            task_type=task_type,
            recommended_bot=best_bot.bot_id,
            confidence=confidence,
            reason=reason,
            alternatives=alternatives
        )

    def get_bot_performance(self, bot_id: str) -> Dict[str, BotTaskPerformance]:
        """
        Get all performance metrics for a bot across task types.

        Args:
            bot_id: Bot identifier

        Returns:
            Dict of task_type -> BotTaskPerformance
        """
        return {
            perf.task_type: perf
            for perf in self.performance_db.values()
            if perf.bot_id == bot_id
        }

    def get_task_type_performance(self, task_type: str) -> List[BotTaskPerformance]:
        """
        Get all bots' performance on a specific task type.

        Args:
            task_type: Task type

        Returns:
            List of BotTaskPerformance records, sorted by score
        """
        performers = self._get_task_type_performers(task_type)
        # Sort by composite score
        return sorted(
            performers,
            key=lambda p: (p.success_rate * 0.6) - (p.avg_execution_time / 1000.0 * 0.4),
            reverse=True
        )

    def get_learning_insights(self) -> Dict[str, Any]:
        """
        Get insights about what we've learned so far.

        Returns:
            Dict with learning insights
        """
        if not self.performance_db:
            return {"status": "no_data"}

        # Group by task type
        by_task_type = {}
        for perf in self.performance_db.values():
            if perf.task_type not in by_task_type:
                by_task_type[perf.task_type] = []
            by_task_type[perf.task_type].append(perf)

        # Analyze each task type
        insights = {
            "total_executions": len(self.task_history),
            "total_bots_observed": len(set(p.bot_id for p in self.performance_db.values())),
            "task_types_learned": len(by_task_type),
            "by_task_type": {}
        }

        for task_type, performers in by_task_type.items():
            best = max(performers, key=lambda p: p.success_rate)
            fastest = min(performers, key=lambda p: p.avg_execution_time)

            insights["by_task_type"][task_type] = {
                "bots_tracked": len(performers),
                "total_tasks": sum(p.total_tasks for p in performers),
                "best_success_rate": {
                    "bot_id": best.bot_id,
                    "rate": best.success_rate
                },
                "fastest": {
                    "bot_id": fastest.bot_id,
                    "avg_time": fastest.avg_execution_time
                },
                "variability": self._calculate_variability(performers)
            }

        return insights

    def reset_bot_learning(self, bot_id: str, task_type: Optional[str] = None) -> None:
        """
        Reset learning for a bot (or bot+task_type combination).

        Useful if a bot's behavior changed significantly.

        Args:
            bot_id: Bot identifier
            task_type: Optional task type (if None, reset all task types for this bot)
        """
        keys_to_delete = []

        for key, perf in self.performance_db.items():
            if perf.bot_id == bot_id:
                if task_type is None or perf.task_type == task_type:
                    keys_to_delete.append(key)

        for key in keys_to_delete:
            del self.performance_db[key]

        self._log_event("learning_reset", {
            "bot_id": bot_id,
            "task_type": task_type
        })

    def get_scheduling_history(self, limit: int = 100) -> List[Dict]:
        """
        Get recent scheduling history.

        Args:
            limit: Number of records to return

        Returns:
            List of history records
        """
        return self.task_history[-limit:]

    def _get_task_type_performers(
        self,
        task_type: str,
        available_bots: Optional[List[str]] = None
    ) -> List[BotTaskPerformance]:
        """Get all bots that have performed on a task type."""
        performers = [
            perf for perf in self.performance_db.values()
            if perf.task_type == task_type
        ]

        if available_bots:
            performers = [p for p in performers if p.bot_id in available_bots]

        return performers

    def _calculate_variability(self, performers: List[BotTaskPerformance]) -> float:
        """Calculate variability (standard deviation) of performance."""
        if len(performers) < 2:
            return 0.0

        # Simple measure: max - min of success rates
        rates = [p.success_rate for p in performers]
        return max(rates) - min(rates)

    def _log_event(self, event: str, details: Dict = None) -> None:
        """Log scheduling event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details or {}
        }

        try:
            with open(self.scheduling_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[ADAPTIVE-SCHEDULER] Failed to log event: {e}")
