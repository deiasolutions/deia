"""
Heat Map Generator - Generate data for dashboards.

Creates time-of-day, bot-usage, and task-type heatmaps in JSON format.
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import json


@dataclass
class HeatMapData:
    """Heat map data structure."""
    title: str
    type: str  # time_of_day, bot_usage, task_type
    data: List[Dict[str, Any]]
    timestamp: str


class HeatMapGenerator:
    """Generate heat maps for visualization."""

    def __init__(self, work_dir: Path):
        """Initialize heat map generator."""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.heatmap_log = self.log_dir / "heatmap-data.jsonl"
        self.events: List[Dict[str, Any]] = []

    def record_event(
        self,
        bot_id: str,
        task_type: str,
        duration_ms: float,
        success: bool
    ) -> None:
        """Record an event for heat map analysis."""
        self.events.append({
            "timestamp": datetime.now().isoformat(),
            "bot_id": bot_id,
            "task_type": task_type,
            "duration_ms": duration_ms,
            "success": success
        })

        # Keep 7 days of events
        cutoff = datetime.now() - timedelta(days=7)
        self.events = [
            e for e in self.events
            if datetime.fromisoformat(e["timestamp"]) > cutoff
        ]

    def generate_time_of_day_heatmap(self) -> Dict[str, Any]:
        """Generate time-of-day heatmap (when is system busiest?)."""
        hourly_data = defaultdict(lambda: {"count": 0, "total_duration": 0, "success_rate": 0})

        for event in self.events:
            ts = datetime.fromisoformat(event["timestamp"])
            hour = ts.hour

            hourly_data[hour]["count"] += 1
            hourly_data[hour]["total_duration"] += event["duration_ms"]
            if event["success"]:
                hourly_data[hour]["success"] = hourly_data[hour].get("success", 0) + 1

        # Calculate metrics
        heatmap = []
        for hour in range(24):
            data = hourly_data[hour]
            success_rate = (data.get("success", 0) / data["count"]) if data["count"] > 0 else 0

            heatmap.append({
                "hour": hour,
                "task_count": data["count"],
                "avg_duration_ms": data["total_duration"] / data["count"] if data["count"] > 0 else 0,
                "success_rate": success_rate,
                "intensity": data["count"]  # For visualization
            })

        return {
            "title": "Task Activity by Time of Day",
            "type": "time_of_day",
            "data": heatmap,
            "timestamp": datetime.now().isoformat()
        }

    def generate_bot_usage_heatmap(self) -> Dict[str, Any]:
        """Generate bot-usage heatmap (which bots most used?)."""
        bot_stats = defaultdict(lambda: {"task_count": 0, "success_count": 0})

        for event in self.events:
            bot_id = event["bot_id"]
            bot_stats[bot_id]["task_count"] += 1
            if event["success"]:
                bot_stats[bot_id]["success_count"] += 1

        heatmap = []
        for bot_id, stats in sorted(bot_stats.items(), key=lambda x: x[1]["task_count"], reverse=True):
            success_rate = stats["success_count"] / stats["task_count"] if stats["task_count"] > 0 else 0

            heatmap.append({
                "bot_id": bot_id,
                "task_count": stats["task_count"],
                "success_rate": success_rate,
                "intensity": stats["task_count"]
            })

        return {
            "title": "Bot Usage Distribution",
            "type": "bot_usage",
            "data": heatmap,
            "timestamp": datetime.now().isoformat()
        }

    def generate_task_type_heatmap(self) -> Dict[str, Any]:
        """Generate task-type heatmap (what tasks are common?)."""
        task_stats = defaultdict(lambda: {"count": 0, "total_duration": 0, "success_count": 0})

        for event in self.events:
            task_type = event["task_type"]
            task_stats[task_type]["count"] += 1
            task_stats[task_type]["total_duration"] += event["duration_ms"]
            if event["success"]:
                task_stats[task_type]["success_count"] += 1

        heatmap = []
        for task_type, stats in sorted(task_stats.items(), key=lambda x: x[1]["count"], reverse=True):
            success_rate = stats["success_count"] / stats["count"] if stats["count"] > 0 else 0

            heatmap.append({
                "task_type": task_type,
                "count": stats["count"],
                "avg_duration_ms": stats["total_duration"] / stats["count"] if stats["count"] > 0 else 0,
                "success_rate": success_rate,
                "intensity": stats["count"]
            })

        return {
            "title": "Task Type Distribution",
            "type": "task_type",
            "data": heatmap,
            "timestamp": datetime.now().isoformat()
        }

    def get_all_heatmaps(self) -> Dict[str, Dict[str, Any]]:
        """Get all heat maps."""
        return {
            "time_of_day": self.generate_time_of_day_heatmap(),
            "bot_usage": self.generate_bot_usage_heatmap(),
            "task_type": self.generate_task_type_heatmap()
        }

    def _log_heatmap(self, heatmap: Dict[str, Any]) -> None:
        """Log heatmap data."""
        try:
            with open(self.heatmap_log, "a") as f:
                f.write(json.dumps(heatmap) + "\n")
        except Exception as e:
            print(f"[HEATMAP-GENERATOR] Failed to log: {e}")
