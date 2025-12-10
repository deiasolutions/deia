"""
Capacity Planner - Predict system behavior and recommend scaling.

Forecasts when system will hit max capacity based on historical trends.
Recommends when to scale, when to optimize.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import json
import statistics


@dataclass
class CapacityForecast:
    """A capacity forecast."""
    metric_name: str
    current_value: float
    max_capacity: float
    forecast_values: List[float]  # 7-day forecast
    days_to_capacity: Optional[int]  # Days until max reached
    trend: str  # stable, increasing, decreasing
    recommendation: str
    confidence: float


class CapacityPlanner:
    """Plan for capacity needs based on trends."""

    def __init__(self, work_dir: Path, max_queue_depth: int = 100, max_cpu: float = 95.0, max_memory: float = 90.0):
        """Initialize capacity planner."""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.forecast_log = self.log_dir / "capacity-forecast.jsonl"

        # Configuration
        self.capacity_limits = {
            "queue_depth": max_queue_depth,
            "cpu_usage": max_cpu,
            "memory_usage": max_memory,
            "response_time": 2000.0  # ms
        }

        # Historical data
        self.metrics: Dict[str, List[Tuple[datetime, float]]] = defaultdict(list)
        self.forecasts: List[CapacityForecast] = []

    def record_metric(self, metric_name: str, value: float) -> None:
        """Record metric with timestamp."""
        now = datetime.now()
        self.metrics[metric_name].append((now, value))

        # Keep 30 days of history
        cutoff = now - timedelta(days=30)
        self.metrics[metric_name] = [
            (ts, v) for ts, v in self.metrics[metric_name]
            if ts > cutoff
        ]

    def forecast_metric(self, metric_name: str, days: int = 7) -> Optional[CapacityForecast]:
        """Forecast metric values for next N days."""
        if metric_name not in self.metrics or len(self.metrics[metric_name]) < 5:
            return None

        history = self.metrics[metric_name]
        values = [v for _, v in history]
        current = values[-1]
        max_cap = self.capacity_limits.get(metric_name, 100.0)

        # Calculate trend (simple linear regression)
        if len(values) >= 7:
            recent_7d = values[-7:]
            older_7d = values[-14:-7] if len(values) >= 14 else values[:7]

            recent_avg = statistics.mean(recent_7d)
            older_avg = statistics.mean(older_7d) if len(older_7d) > 0 else recent_avg

            daily_change = (recent_avg - older_avg) / 7 if len(older_7d) > 0 else 0
        else:
            daily_change = 0

        # Generate forecast
        forecast_values = []
        days_to_capacity = None

        for day in range(days):
            forecast_val = current + (daily_change * (day + 1))
            forecast_values.append(forecast_val)

            # Check if we hit capacity
            if forecast_val >= max_cap and days_to_capacity is None:
                days_to_capacity = day + 1

        # Determine trend
        if daily_change > 0.1:
            trend = "increasing"
        elif daily_change < -0.1:
            trend = "decreasing"
        else:
            trend = "stable"

        # Generate recommendation
        if days_to_capacity and days_to_capacity <= 3:
            recommendation = f"URGENT: System will hit {metric_name} capacity in {days_to_capacity} days. Scale immediately."
        elif days_to_capacity and days_to_capacity <= 7:
            recommendation = f"WARNING: System approaching {metric_name} capacity in {days_to_capacity} days. Plan scaling."
        elif trend == "increasing":
            recommendation = f"Monitor: {metric_name} trending upward. Optimize or scale within 2 weeks."
        else:
            recommendation = f"{metric_name} stable. Current usage optimal."

        # Confidence based on data points
        confidence = min(len(values) / 30.0, 0.95)

        forecast = CapacityForecast(
            metric_name=metric_name,
            current_value=current,
            max_capacity=max_cap,
            forecast_values=forecast_values,
            days_to_capacity=days_to_capacity,
            trend=trend,
            recommendation=recommendation,
            confidence=confidence
        )

        self._log_forecast(forecast)
        self.forecasts.append(forecast)

        return forecast

    def get_all_forecasts(self) -> Dict[str, Optional[CapacityForecast]]:
        """Get forecasts for all known metrics."""
        forecasts = {}

        for metric in self.metrics.keys():
            forecasts[metric] = self.forecast_metric(metric)

        return forecasts

    def get_capacity_summary(self) -> Dict[str, Any]:
        """Get summary of capacity status."""
        forecasts = self.get_all_forecasts()

        urgent = []
        warning = []
        healthy = []

        for metric, forecast in forecasts.items():
            if forecast is None:
                continue

            if forecast.days_to_capacity and forecast.days_to_capacity <= 3:
                urgent.append(forecast)
            elif forecast.days_to_capacity and forecast.days_to_capacity <= 7:
                warning.append(forecast)
            else:
                healthy.append(forecast)

        return {
            "timestamp": datetime.now().isoformat(),
            "urgent_alerts": len(urgent),
            "warnings": len(warning),
            "healthy_metrics": len(healthy),
            "urgent_details": [
                {
                    "metric": f.metric_name,
                    "current": f.current_value,
                    "max": f.max_capacity,
                    "days_to_capacity": f.days_to_capacity,
                    "recommendation": f.recommendation
                }
                for f in urgent
            ],
            "trend_analysis": {
                "increasing": len([f for f in forecasts.values() if f and f.trend == "increasing"]),
                "stable": len([f for f in forecasts.values() if f and f.trend == "stable"]),
                "decreasing": len([f for f in forecasts.values() if f and f.trend == "decreasing"])
            }
        }

    def _log_forecast(self, forecast: CapacityForecast) -> None:
        """Log forecast to file."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "metric_name": forecast.metric_name,
            "current_value": forecast.current_value,
            "max_capacity": forecast.max_capacity,
            "forecast_values": forecast.forecast_values,
            "days_to_capacity": forecast.days_to_capacity,
            "trend": forecast.trend,
            "recommendation": forecast.recommendation,
            "confidence": forecast.confidence
        }

        try:
            with open(self.forecast_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[CAPACITY-PLANNER] Failed to log forecast: {e}")
