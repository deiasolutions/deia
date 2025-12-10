"""
Optimization Advisor - AI-driven suggestions for system improvement.

Analyzes performance and recommends specific optimizations with ROI estimates.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json


class OptimizationAdvisor:
    """Generate optimization recommendations."""

    def __init__(self, work_dir: Path):
        """Initialize advisor."""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "optimization-recommendations.jsonl"
        self.metrics: Dict[str, float] = {}

    def analyze_metrics(self, metrics: Dict[str, float]) -> None:
        """Update current metrics."""
        self.metrics = metrics

    def get_recommendations(self) -> List[Dict[str, Any]]:
        """Generate optimization recommendations."""
        recommendations = []

        # CPU optimization
        if self.metrics.get("cpu_usage", 0) > 70:
            recommendations.append({
                "category": "resource_allocation",
                "priority": "high",
                "recommendation": "Increase CPU allocation or optimize task parallelism",
                "metric": "cpu_usage",
                "current_value": self.metrics.get("cpu_usage"),
                "target_value": 60,
                "estimated_improvement": "15-20% throughput increase",
                "roi_days": 1,
                "effort": "medium"
            })

        # Memory optimization
        if self.metrics.get("memory_usage", 0) > 75:
            recommendations.append({
                "category": "memory_optimization",
                "priority": "high",
                "recommendation": "Implement memory pooling or increase available memory",
                "metric": "memory_usage",
                "current_value": self.metrics.get("memory_usage"),
                "target_value": 60,
                "estimated_improvement": "10-15% latency reduction",
                "roi_days": 2,
                "effort": "medium"
            })

        # Latency optimization
        if self.metrics.get("avg_latency_ms", 0) > 500:
            recommendations.append({
                "category": "performance",
                "priority": "medium",
                "recommendation": "Optimize database queries or add caching layer",
                "metric": "avg_latency_ms",
                "current_value": self.metrics.get("avg_latency_ms"),
                "target_value": 200,
                "estimated_improvement": "3x faster task execution",
                "roi_days": 3,
                "effort": "high"
            })

        # Queue optimization
        if self.metrics.get("queue_depth", 0) > 50:
            recommendations.append({
                "category": "throughput",
                "priority": "high",
                "recommendation": "Scale worker processes or optimize task routing",
                "metric": "queue_depth",
                "current_value": self.metrics.get("queue_depth"),
                "target_value": 10,
                "estimated_improvement": "80% reduction in queue backlog",
                "roi_days": 1,
                "effort": "low"
            })

        # Error rate optimization
        if self.metrics.get("error_rate", 0) > 0.05:
            recommendations.append({
                "category": "reliability",
                "priority": "critical",
                "recommendation": "Implement retry logic or improve error handling",
                "metric": "error_rate",
                "current_value": self.metrics.get("error_rate"),
                "target_value": 0.01,
                "estimated_improvement": "99.9% reliability SLA",
                "roi_days": 1,
                "effort": "medium"
            })

        # Sort by priority and ROI
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(key=lambda x: (
            priority_order.get(x["priority"], 99),
            x.get("roi_days", 999)
        ))

        return recommendations

    def get_optimization_summary(self) -> Dict[str, Any]:
        """Get summary of optimization opportunities."""
        recommendations = self.get_recommendations()

        priorities = {}
        total_potential_improvement = 0

        for rec in recommendations:
            priority = rec["priority"]
            if priority not in priorities:
                priorities[priority] = 0
            priorities[priority] += 1

        return {
            "total_recommendations": len(recommendations),
            "by_priority": priorities,
            "top_recommendation": recommendations[0] if recommendations else None,
            "estimated_roi_days": min([r.get("roi_days", 999) for r in recommendations], default=None),
            "timestamp": datetime.now().isoformat()
        }

    def estimate_impact(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate impact of implementing recommendation."""
        return {
            "recommendation": recommendation.get("recommendation"),
            "current_metric": recommendation.get("metric"),
            "current_value": recommendation.get("current_value"),
            "projected_value": recommendation.get("target_value"),
            "improvement_percent": (
                ((recommendation.get("target_value", 0) - recommendation.get("current_value", 1)) /
                 recommendation.get("current_value", 1) * 100)
                if recommendation.get("current_value", 0) != 0 else 0
            ),
            "estimated_improvement": recommendation.get("estimated_improvement"),
            "implementation_effort": recommendation.get("effort"),
            "roi_timeline_days": recommendation.get("roi_days"),
            "timestamp": datetime.now().isoformat()
        }
