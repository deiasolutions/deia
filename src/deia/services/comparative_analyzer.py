"""
Comparative Analyzer - Compare system behavior across time periods.

Compares today vs yesterday, this week vs last week.
Identifies trends and change detection.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import json


class ComparativeAnalyzer:
    """Compare metrics across time periods."""

    def __init__(self, work_dir: Path):
        """Initialize analyzer."""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "comparative-reports.jsonl"
        self.metrics: Dict[str, list] = defaultdict(list)

    def record_metric(self, metric_name: str, value: float) -> None:
        """Record metric with timestamp."""
        self.metrics[metric_name].append((datetime.now(), value))

    def compare_day_over_day(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Compare today vs yesterday."""
        if metric_name not in self.metrics:
            return None

        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)

        today_values = [
            v for ts, v in self.metrics[metric_name]
            if ts >= today_start
        ]
        yesterday_values = [
            v for ts, v in self.metrics[metric_name]
            if yesterday_start <= ts < today_start
        ]

        if not today_values or not yesterday_values:
            return None

        today_avg = sum(today_values) / len(today_values)
        yesterday_avg = sum(yesterday_values) / len(yesterday_values)
        change_percent = ((today_avg - yesterday_avg) / yesterday_avg * 100) if yesterday_avg > 0 else 0

        trend = "improving" if change_percent < -5 else "degrading" if change_percent > 5 else "stable"

        return {
            "metric": metric_name,
            "period": "day_over_day",
            "today_avg": today_avg,
            "yesterday_avg": yesterday_avg,
            "change_percent": change_percent,
            "trend": trend,
            "timestamp": datetime.now().isoformat()
        }

    def compare_week_over_week(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Compare this week vs last week."""
        if metric_name not in self.metrics:
            return None

        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        last_week_start = week_start - timedelta(days=7)

        this_week = [
            v for ts, v in self.metrics[metric_name]
            if ts >= week_start
        ]
        last_week = [
            v for ts, v in self.metrics[metric_name]
            if last_week_start <= ts < week_start
        ]

        if not this_week or not last_week:
            return None

        this_avg = sum(this_week) / len(this_week)
        last_avg = sum(last_week) / len(last_week)
        change_percent = ((this_avg - last_avg) / last_avg * 100) if last_avg > 0 else 0

        trend = "improving" if change_percent < -5 else "degrading" if change_percent > 5 else "stable"

        return {
            "metric": metric_name,
            "period": "week_over_week",
            "this_week_avg": this_avg,
            "last_week_avg": last_avg,
            "change_percent": change_percent,
            "trend": trend,
            "timestamp": datetime.now().isoformat()
        }

    def detect_trend(self, metric_name: str, window_days: int = 7) -> Optional[Dict[str, Any]]:
        """Detect trend in metric over window."""
        if metric_name not in self.metrics or len(self.metrics[metric_name]) < 5:
            return None

        now = datetime.now()
        cutoff = now - timedelta(days=window_days)

        recent = [
            (ts, v) for ts, v in self.metrics[metric_name]
            if ts >= cutoff
        ]

        if len(recent) < 5:
            return None

        values = [v for _, v in recent]
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]

        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)

        trend_direction = "upward" if second_avg > first_avg else "downward" if second_avg < first_avg else "flat"
        change = ((second_avg - first_avg) / first_avg * 100) if first_avg > 0 else 0

        return {
            "metric": metric_name,
            "window_days": window_days,
            "trend": trend_direction,
            "change_percent": change,
            "current_avg": second_avg,
            "timestamp": datetime.now().isoformat()
        }

    def get_comparison_summary(self) -> Dict[str, Any]:
        """Get summary of all comparisons."""
        summaries = {}

        for metric in self.metrics.keys():
            dod = self.compare_day_over_day(metric)
            wow = self.compare_week_over_week(metric)
            trend = self.detect_trend(metric)

            summaries[metric] = {
                "day_over_day": dod,
                "week_over_week": wow,
                "trend_7d": trend
            }

        return {
            "summary": summaries,
            "timestamp": datetime.now().isoformat()
        }
