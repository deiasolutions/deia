"""
Anomaly Detection Engine - Spot unusual patterns before they become problems.

Detects anomalies in:
- Task latency patterns
- Queue depth trends
- Bot behavior changes
- Resource utilization spikes

Methods:
- Statistical baseline + deviation detection
- Trend analysis
- Probabilistic alerting (80% confidence threshold)
- Root cause suggestions
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import json
import statistics
from collections import defaultdict


@dataclass
class AnomalyEvent:
    """A detected anomaly."""
    anomaly_id: str
    timestamp: str
    anomaly_type: str  # latency, queue_depth, bot_behavior, resource_spike
    metric_name: str
    current_value: float
    baseline_mean: float
    baseline_std: float
    z_score: float
    confidence: float  # 0-1, percentage confidence this is anomalous
    severity: str  # low, medium, high, critical
    root_causes: List[str]
    suggestion: str


@dataclass
class BaselineStats:
    """Statistical baseline for a metric."""
    metric_name: str
    count: int
    mean: float
    std: float
    min: float
    max: float
    p95: float
    p99: float


class AnomalyDetector:
    """
    Detect anomalies in system behavior using statistical methods.

    Thresholds:
    - Z-score > 2.5: 99.4% confidence (anomalous)
    - Z-score > 2.0: 97.7% confidence (likely anomalous)
    - Z-score > 1.5: 93.3% confidence (possibly anomalous)
    """

    # Configuration
    Z_SCORE_THRESHOLD = 2.0  # ~97.7% confidence
    CONFIDENCE_THRESHOLD = 0.80  # 80% to alert
    MIN_SAMPLES_FOR_BASELINE = 10
    HISTORY_WINDOW_HOURS = 24
    DECAY_FACTOR = 0.9  # Recent data weighted more heavily

    # Severity mapping
    SEVERITY_THRESHOLDS = {
        "critical": 3.0,  # Z-score
        "high": 2.5,
        "medium": 2.0,
        "low": 1.5
    }

    def __init__(self, work_dir: Path):
        """
        Initialize anomaly detector.

        Args:
            work_dir: Working directory for logs
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.anomaly_log = self.log_dir / "anomalies-detected.jsonl"

        # Track baselines per metric
        self.baselines: Dict[str, BaselineStats] = {}

        # Track values for baseline calculation
        self.metric_values: Dict[str, List[float]] = defaultdict(list)

        # Track detected anomalies
        self.anomalies: List[AnomalyEvent] = []

    def record_metric(self, metric_name: str, value: float) -> None:
        """
        Record a metric value for baseline calculation.

        Args:
            metric_name: Name of the metric
            value: Metric value
        """
        self.metric_values[metric_name].append(value)

        # Keep only recent history
        cutoff_time = datetime.now() - timedelta(hours=self.HISTORY_WINDOW_HOURS)
        if len(self.metric_values[metric_name]) > 1000:
            self.metric_values[metric_name] = self.metric_values[metric_name][-1000:]

        # Update baseline periodically
        if len(self.metric_values[metric_name]) >= self.MIN_SAMPLES_FOR_BASELINE:
            self._update_baseline(metric_name)

    def detect_anomaly(
        self,
        metric_name: str,
        current_value: float,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[AnomalyEvent]:
        """
        Detect if current value is anomalous.

        Args:
            metric_name: Name of the metric
            current_value: Current metric value
            context: Additional context for root cause analysis

        Returns:
            AnomalyEvent if anomalous (confidence >= threshold), else None
        """
        # Get baseline
        if metric_name not in self.baselines:
            return None

        baseline = self.baselines[metric_name]
        if baseline.std == 0:
            return None  # Cannot calculate z-score with zero variance

        # Calculate z-score
        z_score = (current_value - baseline.mean) / baseline.std
        abs_z = abs(z_score)

        # Determine confidence based on z-score
        confidence = self._z_score_to_confidence(abs_z)

        # Check if anomalous
        if confidence < self.CONFIDENCE_THRESHOLD or abs_z < self.Z_SCORE_THRESHOLD:
            return None

        # Determine severity
        severity = self._determine_severity(abs_z)

        # Generate root causes
        root_causes = self._analyze_root_causes(
            metric_name, current_value, baseline, context
        )

        # Create anomaly event
        anomaly_id = f"{metric_name}_{datetime.now().isoformat()}"
        anomaly = AnomalyEvent(
            anomaly_id=anomaly_id,
            timestamp=datetime.now().isoformat(),
            anomaly_type=self._classify_anomaly_type(metric_name),
            metric_name=metric_name,
            current_value=current_value,
            baseline_mean=baseline.mean,
            baseline_std=baseline.std,
            z_score=z_score,
            confidence=confidence,
            severity=severity,
            root_causes=root_causes,
            suggestion=self._generate_suggestion(
                metric_name, current_value, baseline, severity
            )
        )

        # Record anomaly
        self.anomalies.append(anomaly)
        self._log_anomaly(anomaly)

        return anomaly

    def get_recent_anomalies(self, hours: int = 1) -> List[AnomalyEvent]:
        """
        Get anomalies from the last N hours.

        Args:
            hours: Hours of history

        Returns:
            List of recent anomalies
        """
        cutoff = datetime.now() - timedelta(hours=hours)

        return [
            a for a in self.anomalies
            if datetime.fromisoformat(a.timestamp) > cutoff
        ]

    def get_anomaly_summary(self) -> Dict[str, Any]:
        """
        Get summary of anomalies.

        Returns:
            Anomaly statistics
        """
        recent_24h = self.get_recent_anomalies(hours=24)

        by_type = defaultdict(int)
        by_severity = defaultdict(int)

        for anomaly in recent_24h:
            by_type[anomaly.anomaly_type] += 1
            by_severity[anomaly.severity] += 1

        return {
            "total_anomalies_24h": len(recent_24h),
            "by_type": dict(by_type),
            "by_severity": dict(by_severity),
            "baseline_count": len(self.baselines),
            "metrics_tracked": len(self.metric_values),
            "timestamp": datetime.now().isoformat()
        }

    def get_metric_baseline(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """
        Get baseline stats for a metric.

        Args:
            metric_name: Name of the metric

        Returns:
            Baseline statistics or None
        """
        if metric_name not in self.baselines:
            return None

        baseline = self.baselines[metric_name]
        return asdict(baseline)

    def _update_baseline(self, metric_name: str) -> None:
        """Update baseline statistics for a metric."""
        values = self.metric_values[metric_name]
        if len(values) < self.MIN_SAMPLES_FOR_BASELINE:
            return

        # Calculate stats
        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0
        min_val = min(values)
        max_val = max(values)

        # Percentiles
        sorted_vals = sorted(values)
        p95_idx = int(len(sorted_vals) * 0.95)
        p99_idx = int(len(sorted_vals) * 0.99)
        p95 = sorted_vals[p95_idx] if p95_idx < len(sorted_vals) else max_val
        p99 = sorted_vals[p99_idx] if p99_idx < len(sorted_vals) else max_val

        self.baselines[metric_name] = BaselineStats(
            metric_name=metric_name,
            count=len(values),
            mean=mean,
            std=std,
            min=min_val,
            max=max_val,
            p95=p95,
            p99=p99
        )

    def _z_score_to_confidence(self, z_score: float) -> float:
        """
        Convert z-score to confidence percentage.

        Args:
            z_score: Absolute z-score value

        Returns:
            Confidence 0-1
        """
        # Approximate mapping (simplified normal distribution)
        if z_score < 1.0:
            return 0.68
        elif z_score < 1.5:
            return 0.87
        elif z_score < 2.0:
            return 0.954
        elif z_score < 2.5:
            return 0.988
        elif z_score < 3.0:
            return 0.9974
        else:
            return 0.99973

    def _determine_severity(self, z_score: float) -> str:
        """Determine severity based on z-score."""
        if z_score >= self.SEVERITY_THRESHOLDS["critical"]:
            return "critical"
        elif z_score >= self.SEVERITY_THRESHOLDS["high"]:
            return "high"
        elif z_score >= self.SEVERITY_THRESHOLDS["medium"]:
            return "medium"
        else:
            return "low"

    def _classify_anomaly_type(self, metric_name: str) -> str:
        """Classify anomaly type from metric name."""
        metric_lower = metric_name.lower()

        if "latency" in metric_lower or "duration" in metric_lower:
            return "latency"
        elif "queue" in metric_lower or "depth" in metric_lower:
            return "queue_depth"
        elif "cpu" in metric_lower or "memory" in metric_lower:
            return "resource_spike"
        elif "bot" in metric_lower:
            return "bot_behavior"
        else:
            return "other"

    def _analyze_root_causes(
        self,
        metric_name: str,
        current_value: float,
        baseline: BaselineStats,
        context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Analyze possible root causes for anomaly.

        Args:
            metric_name: Name of metric
            current_value: Current value
            baseline: Baseline statistics
            context: Additional context

        Returns:
            List of possible root causes
        """
        causes = []
        delta_percent = ((current_value - baseline.mean) / baseline.mean * 100) if baseline.mean > 0 else 0

        # Latency anomalies
        if "latency" in metric_name.lower():
            if delta_percent > 50:
                causes.append("High queue wait times (system overload)")
                causes.append("Resource contention (CPU/memory)")
                causes.append("Network latency increase")
            elif delta_percent < -50:
                causes.append("Task complexity reduced")
                causes.append("System resources freed up")

        # Queue depth anomalies
        elif "queue" in metric_name.lower():
            if current_value > baseline.p99:
                causes.append("Throughput bottleneck (tasks processed slower than queued)")
                causes.append("Worker unavailability or capacity exhaustion")
                causes.append("Task type distribution shift")
            elif current_value < baseline.p95 * 0.5:
                causes.append("Lower task arrival rate than usual")
                causes.append("Increased task processing speed")

        # Resource anomalies
        elif "cpu" in metric_name.lower() or "memory" in metric_name.lower():
            if delta_percent > 30:
                causes.append("Unexpected workload spike")
                causes.append("Resource leak or inefficiency")
                causes.append("Task type composition changed (more CPU-intensive tasks)")

        # Bot behavior
        elif "bot" in metric_name.lower():
            causes.append("Bot state change or crash")
            causes.append("Task routing configuration changed")

        # Default
        if not causes:
            causes.append("Deviation from normal operating parameters")

        return causes[:3]  # Return top 3 causes

    def _generate_suggestion(
        self,
        metric_name: str,
        current_value: float,
        baseline: BaselineStats,
        severity: str
    ) -> str:
        """Generate actionable suggestion."""
        if severity == "critical":
            return f"URGENT: {metric_name} significantly out of bounds. Immediate investigation required."
        elif severity == "high":
            return f"Action needed: {metric_name} trending abnormally. Review system state and resource allocation."
        elif severity == "medium":
            return f"Monitor: {metric_name} shows unusual behavior. Plan for potential scaling."
        else:
            return f"Note: {metric_name} slightly elevated. No immediate action, but log for trend analysis."

    def _log_anomaly(self, anomaly: AnomalyEvent) -> None:
        """Log anomaly event."""
        entry = {
            "timestamp": anomaly.timestamp,
            "anomaly_id": anomaly.anomaly_id,
            "anomaly_type": anomaly.anomaly_type,
            "metric_name": anomaly.metric_name,
            "current_value": anomaly.current_value,
            "baseline_mean": anomaly.baseline_mean,
            "baseline_std": anomaly.baseline_std,
            "z_score": anomaly.z_score,
            "confidence": anomaly.confidence,
            "severity": anomaly.severity,
            "root_causes": anomaly.root_causes,
            "suggestion": anomaly.suggestion
        }

        try:
            with open(self.anomaly_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[ANOMALY-DETECTOR] Failed to log anomaly: {e}")
