"""
Queue Analytics - Understand task flow and bottlenecks in the system.

Tracks queue depth, task latency, throughput, and identifies bottlenecks.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import json


@dataclass
class QueueSnapshot:
    """Snapshot of queue state at a point in time."""
    timestamp: str
    queue_depth: int
    tasks_queued: int
    tasks_executing: int
    tasks_completed: int
    total_tasks_processed: int
    avg_queue_wait_ms: float
    avg_execution_time_ms: float
    throughput_tasks_per_minute: float


@dataclass
class TaskLatencyAnalysis:
    """Analysis of task latency (queued → executed → completed)."""
    task_id: str
    queued_at: str
    executed_at: str
    completed_at: str
    queue_wait_ms: float  # Time from queued to executing
    execution_time_ms: float  # Time from executing to completed
    total_time_ms: float  # Total time in system
    task_type: str
    bot_id: str


class QueueAnalytics:
    """
    Analyze task queue dynamics and performance.

    Features:
    - Track queue depth over time
    - Measure task latency (queued → executed → completed)
    - Calculate throughput
    - Identify bottlenecks
    - Detect performance degradation
    """

    def __init__(self, work_dir: Path):
        """
        Initialize queue analytics.

        Args:
            work_dir: Working directory for logs
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.analytics_log = self.log_dir / "queue-analytics.jsonl"

        # Track queue state over time
        self.queue_history: List[QueueSnapshot] = []

        # Track individual task latencies
        self.task_latencies: Dict[str, TaskLatencyAnalysis] = {}

        # Task type performance
        self.task_type_stats: Dict[str, Dict[str, float]] = {}

    def record_queue_snapshot(
        self,
        queue_depth: int,
        tasks_executing: int,
        tasks_completed: int,
        avg_queue_wait_ms: float,
        avg_execution_time_ms: float
    ) -> QueueSnapshot:
        """
        Record current queue state.

        Args:
            queue_depth: Current queued tasks
            tasks_executing: Currently executing
            tasks_completed: Total completed so far
            avg_queue_wait_ms: Average wait time before execution
            avg_execution_time_ms: Average execution time

        Returns:
            QueueSnapshot
        """
        # Calculate throughput (tasks completed in last minute)
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        recent_completions = len([
            t for t in self.task_latencies.values()
            if t.completed_at and datetime.fromisoformat(t.completed_at) > one_minute_ago
        ])
        throughput = recent_completions  # tasks per minute

        snapshot = QueueSnapshot(
            timestamp=now.isoformat(),
            queue_depth=queue_depth,
            tasks_queued=queue_depth,
            tasks_executing=tasks_executing,
            tasks_completed=tasks_completed,
            total_tasks_processed=queue_depth + tasks_executing + tasks_completed,
            avg_queue_wait_ms=avg_queue_wait_ms,
            avg_execution_time_ms=avg_execution_time_ms,
            throughput_tasks_per_minute=float(throughput)
        )

        self.queue_history.append(snapshot)

        # Keep 24 hours of history
        cutoff = now - timedelta(hours=24)
        self.queue_history = [
            s for s in self.queue_history
            if datetime.fromisoformat(s.timestamp) > cutoff
        ]

        self._log_snapshot(snapshot)

        return snapshot

    def record_task_latency(
        self,
        task_id: str,
        task_type: str,
        bot_id: str,
        queued_at: str,
        executed_at: Optional[str] = None,
        completed_at: Optional[str] = None
    ) -> TaskLatencyAnalysis:
        """
        Record task timing information.

        Args:
            task_id: Task identifier
            task_type: Type of task
            bot_id: Bot executing task
            queued_at: When task was queued (ISO format)
            executed_at: When execution started
            completed_at: When execution completed

        Returns:
            TaskLatencyAnalysis
        """
        queue_wait_ms = 0
        execution_time_ms = 0
        total_time_ms = 0

        # Calculate latencies if we have timestamps
        if executed_at:
            queued = datetime.fromisoformat(queued_at)
            executed = datetime.fromisoformat(executed_at)
            queue_wait_ms = (executed - queued).total_seconds() * 1000

        if completed_at and executed_at:
            executed = datetime.fromisoformat(executed_at)
            completed = datetime.fromisoformat(completed_at)
            execution_time_ms = (completed - executed).total_seconds() * 1000

        if completed_at:
            queued = datetime.fromisoformat(queued_at)
            completed = datetime.fromisoformat(completed_at)
            total_time_ms = (completed - queued).total_seconds() * 1000

        analysis = TaskLatencyAnalysis(
            task_id=task_id,
            queued_at=queued_at,
            executed_at=executed_at or "",
            completed_at=completed_at or "",
            queue_wait_ms=queue_wait_ms,
            execution_time_ms=execution_time_ms,
            total_time_ms=total_time_ms,
            task_type=task_type,
            bot_id=bot_id
        )

        self.task_latencies[task_id] = analysis

        # Update task type statistics
        if task_type not in self.task_type_stats:
            self.task_type_stats[task_type] = {
                "count": 0,
                "avg_queue_wait_ms": 0,
                "avg_execution_time_ms": 0,
                "avg_total_time_ms": 0,
                "p95_execution_time_ms": 0,
                "p99_execution_time_ms": 0
            }

        self._update_task_type_stats(task_type)

        self._log_latency(analysis)

        return analysis

    def get_queue_status(self) -> Dict[str, Any]:
        """
        Get current queue status and trends.

        Returns:
            Queue analytics
        """
        if not self.queue_history:
            return {"status": "no_data"}

        recent = self.queue_history[-10:]  # Last 10 snapshots

        avg_queue_depth = sum(s.queue_depth for s in recent) / len(recent)
        avg_wait_time = sum(s.avg_queue_wait_ms for s in recent) / len(recent)
        avg_execution = sum(s.avg_execution_time_ms for s in recent) / len(recent)
        avg_throughput = sum(s.throughput_tasks_per_minute for s in recent) / len(recent)

        return {
            "queue_depth": recent[-1].queue_depth if recent else 0,
            "avg_queue_depth_recent": avg_queue_depth,
            "avg_queue_wait_ms": avg_wait_time,
            "avg_execution_time_ms": avg_execution,
            "throughput_tasks_per_minute": avg_throughput,
            "timestamp": datetime.now().isoformat()
        }

    def identify_bottlenecks(self) -> Dict[str, Any]:
        """
        Identify task type bottlenecks.

        Returns:
            Bottleneck analysis
        """
        if not self.task_type_stats:
            return {"status": "no_data"}

        bottlenecks = []

        for task_type, stats in self.task_type_stats.items():
            # High queue wait = bottleneck in routing
            if stats["avg_queue_wait_ms"] > 500:
                bottlenecks.append({
                    "type": "queue_wait",
                    "task_type": task_type,
                    "avg_queue_wait_ms": stats["avg_queue_wait_ms"]
                })

            # High execution time = bottleneck in execution
            if stats["avg_execution_time_ms"] > 5000:
                bottlenecks.append({
                    "type": "execution_time",
                    "task_type": task_type,
                    "avg_execution_time_ms": stats["avg_execution_time_ms"]
                })

        return {
            "bottlenecks": bottlenecks,
            "task_types_analyzed": len(self.task_type_stats),
            "timestamp": datetime.now().isoformat()
        }

    def get_task_type_performance(self, task_type: str) -> Dict[str, Any]:
        """
        Get performance stats for a specific task type.

        Args:
            task_type: Task type to analyze

        Returns:
            Performance stats
        """
        if task_type not in self.task_type_stats:
            return {"status": "no_data"}

        stats = self.task_type_stats[task_type]

        # Get sample tasks
        sample_tasks = [
            t for t in self.task_latencies.values()
            if t.task_type == task_type
        ][-10:]  # Last 10 tasks

        return {
            "task_type": task_type,
            "total_tasks": stats["count"],
            "avg_queue_wait_ms": stats["avg_queue_wait_ms"],
            "avg_execution_time_ms": stats["avg_execution_time_ms"],
            "avg_total_time_ms": stats["avg_total_time_ms"],
            "p95_execution_time_ms": stats["p95_execution_time_ms"],
            "p99_execution_time_ms": stats["p99_execution_time_ms"],
            "recent_samples": [
                {
                    "task_id": t.task_id,
                    "queue_wait_ms": t.queue_wait_ms,
                    "execution_time_ms": t.execution_time_ms,
                    "bot_id": t.bot_id
                }
                for t in sample_tasks
            ],
            "timestamp": datetime.now().isoformat()
        }

    def _update_task_type_stats(self, task_type: str) -> None:
        """Update statistics for a task type."""
        tasks = [
            t for t in self.task_latencies.values()
            if t.task_type == task_type
        ]

        if not tasks:
            return

        count = len(tasks)
        avg_queue_wait = sum(t.queue_wait_ms for t in tasks) / count
        avg_execution = sum(t.execution_time_ms for t in tasks) / count
        avg_total = sum(t.total_time_ms for t in tasks) / count

        # Calculate percentiles
        execution_times = sorted([t.execution_time_ms for t in tasks])
        p95_idx = int(count * 0.95)
        p99_idx = int(count * 0.99)
        p95 = execution_times[p95_idx] if p95_idx < count else 0
        p99 = execution_times[p99_idx] if p99_idx < count else 0

        self.task_type_stats[task_type] = {
            "count": count,
            "avg_queue_wait_ms": avg_queue_wait,
            "avg_execution_time_ms": avg_execution,
            "avg_total_time_ms": avg_total,
            "p95_execution_time_ms": p95,
            "p99_execution_time_ms": p99
        }

    def _log_snapshot(self, snapshot: QueueSnapshot) -> None:
        """Log queue snapshot."""
        entry = {
            "timestamp": snapshot.timestamp,
            "queue_depth": snapshot.queue_depth,
            "tasks_executing": snapshot.tasks_executing,
            "tasks_completed": snapshot.tasks_completed,
            "avg_queue_wait_ms": snapshot.avg_queue_wait_ms,
            "avg_execution_time_ms": snapshot.avg_execution_time_ms,
            "throughput_tasks_per_minute": snapshot.throughput_tasks_per_minute
        }

        try:
            with open(self.analytics_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[QUEUE-ANALYTICS] Failed to log snapshot: {e}")

    def _log_latency(self, analysis: TaskLatencyAnalysis) -> None:
        """Log task latency."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": analysis.task_id,
            "task_type": analysis.task_type,
            "bot_id": analysis.bot_id,
            "queue_wait_ms": analysis.queue_wait_ms,
            "execution_time_ms": analysis.execution_time_ms,
            "total_time_ms": analysis.total_time_ms
        }

        try:
            with open(self.analytics_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[QUEUE-ANALYTICS] Failed to log latency: {e}")
