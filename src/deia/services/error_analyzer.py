"""
Error Analyzer - Track, aggregate, and analyze errors in the system.

Features:
- Aggregate errors by type
- Error rate tracking and alerts
- Root cause analysis automation
- Trend detection (errors increasing/decreasing)
- Error correlation detection
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import json
import statistics


@dataclass
class ErrorEvent:
    """Single error event."""
    timestamp: str
    error_type: str  # timeout, network, validation, database, etc.
    error_message: str
    affected_component: str  # user, bot, api, database, etc.
    error_code: int
    context: Dict[str, Any]


@dataclass
class ErrorStats:
    """Statistics for an error type."""
    error_type: str
    total_count: int
    occurrences_24h: int
    occurrence_rate_per_hour: float
    first_occurrence: str
    last_occurrence: str
    affected_components: List[str]
    severity: str  # low, medium, high, critical


class ErrorAnalyzer:
    """
    Analyze errors in the system to detect patterns and trends.

    Tracks:
    - Error frequencies by type
    - Error trends (increasing/stable/decreasing)
    - Root causes and correlations
    - Component-specific error rates
    """

    # Thresholds for alerts
    ERROR_RATE_WARNING = 0.05  # 5% errors
    ERROR_RATE_CRITICAL = 0.1  # 10% errors
    SPIKE_THRESHOLD = 0.5  # 50% increase in errors

    def __init__(self, work_dir: Path):
        """
        Initialize error analyzer.

        Args:
            work_dir: Working directory for logs
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.error_log = self.log_dir / "error-analysis.jsonl"

        # Track errors
        self.errors: List[ErrorEvent] = []
        self.error_by_type: Dict[str, List[ErrorEvent]] = defaultdict(list)
        self.error_by_component: Dict[str, List[ErrorEvent]] = defaultdict(list)
        self.error_trends: Dict[str, List[float]] = defaultdict(list)

    def record_error(
        self,
        error_type: str,
        error_message: str,
        affected_component: str,
        error_code: int,
        context: Optional[Dict[str, Any]] = None
    ) -> ErrorEvent:
        """
        Record an error event.

        Args:
            error_type: Type of error (timeout, network, validation, database)
            error_message: Error message/description
            affected_component: Component that had the error
            error_code: HTTP or application error code
            context: Additional context data

        Returns:
            ErrorEvent that was recorded
        """
        event = ErrorEvent(
            timestamp=datetime.now().isoformat(),
            error_type=error_type,
            error_message=error_message,
            affected_component=affected_component,
            error_code=error_code,
            context=context or {}
        )

        self.errors.append(event)
        self.error_by_type[error_type].append(event)
        self.error_by_component[affected_component].append(event)

        # Log to file
        self._log_event(event)

        return event

    def get_error_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive error statistics.

        Returns:
            Error statistics by type, component, and trends
        """
        now = datetime.now()
        cutoff_24h = now - timedelta(hours=24)

        stats = {
            "total_errors": len(self.errors),
            "errors_24h": sum(
                1 for e in self.errors
                if datetime.fromisoformat(e.timestamp) >= cutoff_24h
            ),
            "by_type": {},
            "by_component": {},
            "error_rate": self._calculate_error_rate(),
            "trends": self._analyze_trends()
        }

        # Stats by error type
        for error_type, events in self.error_by_type.items():
            count_24h = sum(
                1 for e in events
                if datetime.fromisoformat(e.timestamp) >= cutoff_24h
            )

            components = list(set(e.affected_component for e in events))

            stats["by_type"][error_type] = {
                "total": len(events),
                "in_24h": count_24h,
                "rate_per_hour": count_24h / 24.0,
                "affected_components": components,
                "severity": self._assess_severity(error_type, len(events), count_24h)
            }

        # Stats by component
        for component, events in self.error_by_component.items():
            count_24h = sum(
                1 for e in events
                if datetime.fromisoformat(e.timestamp) >= cutoff_24h
            )

            stats["by_component"][component] = {
                "total": len(events),
                "in_24h": count_24h,
                "error_types": list(set(e.error_type for e in events))
            }

        return stats

    def detect_error_spikes(self) -> List[Dict[str, Any]]:
        """
        Detect error spikes (sudden increases).

        Returns:
            List of detected spikes with details
        """
        spikes = []
        now = datetime.now()

        for error_type, events in self.error_by_type.items():
            if len(events) < 10:
                continue  # Need enough data

            # Compare last hour vs. previous hour
            one_hour_ago = now - timedelta(hours=1)
            two_hours_ago = now - timedelta(hours=2)

            recent = sum(
                1 for e in events
                if datetime.fromisoformat(e.timestamp) >= one_hour_ago
            )
            previous = sum(
                1 for e in events
                if two_hours_ago <= datetime.fromisoformat(e.timestamp) < one_hour_ago
            )

            if previous == 0:
                if recent > 0:
                    spikes.append({
                        "error_type": error_type,
                        "severity": "high",
                        "message": f"First occurrence of {error_type} in recent hour",
                        "current_rate": recent
                    })
            else:
                ratio = recent / previous
                if ratio >= (1 + self.SPIKE_THRESHOLD):
                    spikes.append({
                        "error_type": error_type,
                        "severity": "medium",
                        "message": f"{error_type} increased {ratio:.1f}x in last hour",
                        "previous_hour": previous,
                        "current_hour": recent
                    })

        return spikes

    def detect_error_patterns(self) -> List[Dict[str, Any]]:
        """
        Detect patterns and correlations in errors.

        Returns:
            List of detected patterns
        """
        patterns = []

        # Pattern 1: Multiple error types affecting same component
        for component, events in self.error_by_component.items():
            error_types = set(e.error_type for e in events)

            if len(error_types) > 2:
                patterns.append({
                    "type": "multiple_error_types_same_component",
                    "component": component,
                    "error_types": list(error_types),
                    "count": len(events),
                    "message": f"Component {component} experiencing {len(error_types)} different error types"
                })

        # Pattern 2: High error rate for specific component
        total_errors = len(self.errors)
        if total_errors > 0:
            for component, events in self.error_by_component.items():
                rate = len(events) / total_errors
                if rate > 0.3:
                    patterns.append({
                        "type": "high_error_component",
                        "component": component,
                        "error_rate": rate,
                        "count": len(events),
                        "message": f"Component {component} accounts for {rate*100:.1f}% of errors"
                    })

        return patterns

    def get_error_trends(self, hours: int = 24) -> Dict[str, Any]:
        """
        Get error trends over time.

        Args:
            hours: Number of hours to analyze

        Returns:
            Trend data
        """
        now = datetime.now()
        cutoff = now - timedelta(hours=hours)

        # Count errors per hour
        hourly_counts = defaultdict(int)
        for error in self.errors:
            error_time = datetime.fromisoformat(error.timestamp)
            if error_time >= cutoff:
                hour_key = error_time.strftime("%Y-%m-%d %H:00")
                hourly_counts[hour_key] += 1

        if not hourly_counts:
            return {
                "trend": "no_data",
                "hourly": {},
                "summary": "No error data in period"
            }

        # Calculate trend
        counts = list(hourly_counts.values())
        if len(counts) >= 2:
            first_half = statistics.mean(counts[:len(counts)//2])
            second_half = statistics.mean(counts[len(counts)//2:])

            if second_half > first_half * 1.2:
                trend = "increasing"
            elif second_half < first_half * 0.8:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return {
            "trend": trend,
            "hourly": dict(sorted(hourly_counts.items())),
            "total_errors": sum(counts),
            "avg_per_hour": statistics.mean(counts),
            "max_per_hour": max(counts),
            "min_per_hour": min(counts)
        }

    def _calculate_error_rate(self) -> float:
        """Calculate overall error rate."""
        if not self.errors:
            return 0.0

        now = datetime.now()
        cutoff = now - timedelta(hours=24)

        recent_errors = sum(
            1 for e in self.errors
            if datetime.fromisoformat(e.timestamp) >= cutoff
        )

        # Assume ~100 operations per hour per day = 2400 operations
        # This is a rough estimate; in production, would track actual operations
        estimated_operations = 2400

        return recent_errors / estimated_operations if estimated_operations > 0 else 0.0

    def _assess_severity(self, error_type: str, total: int, count_24h: int) -> str:
        """Assess error severity based on frequency and type."""
        rate = count_24h / 24.0

        critical_types = {"database", "authentication", "security"}
        if error_type in critical_types and rate > 1:
            return "critical"

        if count_24h > 20:
            return "high"
        elif count_24h > 5:
            return "medium"
        else:
            return "low"

    def _analyze_trends(self) -> Dict[str, Any]:
        """Analyze error trends across types."""
        trends = {}

        for error_type, events in self.error_by_type.items():
            if len(events) < 5:
                continue

            now = datetime.now()
            last_day = now - timedelta(hours=24)

            recent = [
                e for e in events
                if datetime.fromisoformat(e.timestamp) >= last_day
            ]

            if recent:
                trends[error_type] = {
                    "total": len(events),
                    "last_24h": len(recent),
                    "status": "active" if recent else "inactive"
                }

        return trends

    def _log_event(self, event: ErrorEvent) -> None:
        """Log error event to file."""
        try:
            with open(self.error_log, "a") as f:
                f.write(json.dumps(asdict(event)) + "\n")
        except Exception as e:
            print(f"[ERROR-ANALYZER] Failed to log event: {e}")

    def generate_report(self) -> str:
        """
        Generate comprehensive error analysis report.

        Returns:
            Markdown formatted report
        """
        stats = self.get_error_stats()
        spikes = self.detect_error_spikes()
        patterns = self.detect_error_patterns()
        trends = self.get_error_trends(24)

        report = f"""# Error Analysis Report
**Generated:** {datetime.now().isoformat()}

## Summary
- **Total Errors:** {stats['total_errors']}
- **24h Errors:** {stats['errors_24h']}
- **Error Rate:** {stats['error_rate']*100:.2f}%

## Top Error Types
"""
        for error_type, data in sorted(
            stats['by_type'].items(),
            key=lambda x: x[1]['in_24h'],
            reverse=True
        )[:5]:
            report += f"""
### {error_type.upper()}
- Count (24h): {data['in_24h']}
- Rate/hour: {data['rate_per_hour']:.2f}
- Severity: {data['severity']}
- Affected: {', '.join(data['affected_components'][:3])}
"""

        if spikes:
            report += "\n## Error Spikes Detected\n"
            for spike in spikes:
                report += f"- **{spike['error_type']}**: {spike['message']}\n"

        if patterns:
            report += "\n## Patterns Detected\n"
            for pattern in patterns[:5]:
                report += f"- {pattern['message']}\n"

        report += f"\n## Trend Analysis (24h)\n"
        report += f"- **Direction:** {trends['trend']}\n"
        report += f"- **Avg/hour:** {trends['avg_per_hour']:.1f}\n"

        return report
