"""
Correlation Analyzer - Find what factors affect system behavior.

Analyzes historical patterns and identifies correlations between metrics.
Predicts system behavior based on observed correlations.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import json
import statistics


@dataclass
class CorrelationResult:
    """Result of correlation analysis between two metrics."""
    metric_1: str
    metric_2: str
    correlation_coefficient: float  # -1 to 1
    strength: str  # none, weak, moderate, strong, very_strong
    direction: str  # positive, negative, none
    sample_count: int
    time_period: str  # 7d, 30d, etc


@dataclass
class Prediction:
    """A prediction based on correlation analysis."""
    metric_name: str
    predicted_value: float
    confidence: float  # 0-1
    influencing_factors: List[Tuple[str, float]]  # (factor, correlation)
    time_period: str


class CorrelationAnalyzer:
    """
    Analyze correlations between metrics and predict system behavior.

    Tracks:
    - Metric relationships (correlation matrix)
    - Historical patterns (7-day, 30-day windows)
    - Predictive correlations
    """

    def __init__(self, work_dir: Path):
        """Initialize correlation analyzer."""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.correlation_log = self.log_dir / "correlation-analysis.jsonl"

        # Store metric history (last 30 days)
        self.metric_history: Dict[str, List[Tuple[datetime, float]]] = defaultdict(list)

        # Cache correlation results
        self.correlations: List[CorrelationResult] = []

    def record_metric(self, metric_name: str, value: float) -> None:
        """Record metric value with timestamp."""
        now = datetime.now()
        self.metric_history[metric_name].append((now, value))

        # Keep only 30 days of history
        cutoff = now - timedelta(days=30)
        self.metric_history[metric_name] = [
            (ts, v) for ts, v in self.metric_history[metric_name]
            if ts > cutoff
        ]

    def analyze_correlations(self, period_days: int = 7) -> List[CorrelationResult]:
        """
        Analyze correlations between all metrics over specified period.

        Args:
            period_days: Days of history to analyze

        Returns:
            List of correlation results
        """
        results = []
        metric_names = list(self.metric_history.keys())

        # Analyze each pair of metrics
        for i, metric1 in enumerate(metric_names):
            for metric2 in metric_names[i+1:]:
                corr = self._calculate_correlation(metric1, metric2, period_days)
                if corr:
                    results.append(corr)
                    self._log_correlation(corr)

        self.correlations = results
        return results

    def get_correlation_matrix(self, period_days: int = 7) -> Dict[str, Dict[str, float]]:
        """Get correlation matrix as dict of dicts."""
        matrix = defaultdict(dict)
        correlations = self.analyze_correlations(period_days)

        for corr in correlations:
            matrix[corr.metric_1][corr.metric_2] = corr.correlation_coefficient
            matrix[corr.metric_2][corr.metric_1] = corr.correlation_coefficient

        return dict(matrix)

    def predict_metric(self, target_metric: str, context: Optional[Dict[str, float]] = None) -> Optional[Prediction]:
        """
        Predict value of target metric based on correlations and context.

        Args:
            target_metric: Metric to predict
            context: Current values of other metrics

        Returns:
            Prediction or None
        """
        if target_metric not in self.metric_history:
            return None

        history = self.metric_history[target_metric]
        if len(history) < 10:
            return None

        values = [v for _, v in history]
        baseline_mean = statistics.mean(values)

        # Find correlating factors
        influences = []
        if context:
            correlations = self.analyze_correlations(7)
            for corr in correlations:
                if corr.metric_2 == target_metric and corr.metric_1 in context:
                    influences.append((corr.metric_1, corr.correlation_coefficient))
                elif corr.metric_1 == target_metric and corr.metric_2 in context:
                    influences.append((corr.metric_2, corr.correlation_coefficient))

        # Calculate weighted prediction
        predicted = baseline_mean
        total_weight = 0

        for factor, correlation in influences:
            if factor in context:
                factor_history = self.metric_history[factor]
                if factor_history:
                    factor_mean = statistics.mean([v for _, v in factor_history])
                    delta = context[factor] - factor_mean
                    predicted += delta * correlation * 0.1
                    total_weight += abs(correlation)

        # Confidence based on correlation strength and sample size
        confidence = min(len(history) / 100.0, 0.95) if influences else 0.5

        return Prediction(
            metric_name=target_metric,
            predicted_value=predicted,
            confidence=confidence,
            influencing_factors=influences,
            time_period="7d"
        )

    def get_pattern_summary(self) -> Dict[str, Any]:
        """Get summary of patterns discovered."""
        correlations = self.analyze_correlations(7)

        strong_correlations = [c for c in correlations if c.strength in ["strong", "very_strong"]]
        patterns = defaultdict(list)

        for corr in strong_correlations:
            patterns[corr.metric_1].append({
                "affects": corr.metric_2,
                "strength": corr.strength,
                "direction": corr.direction,
                "coefficient": corr.correlation_coefficient
            })

        return {
            "total_metrics": len(self.metric_history),
            "total_correlations_analyzed": len(correlations),
            "strong_correlations": len(strong_correlations),
            "patterns_discovered": dict(patterns),
            "timestamp": datetime.now().isoformat()
        }

    def _calculate_correlation(
        self,
        metric1: str,
        metric2: str,
        period_days: int
    ) -> Optional[CorrelationResult]:
        """Calculate Pearson correlation between two metrics."""
        now = datetime.now()
        cutoff = now - timedelta(days=period_days)

        values1 = [v for ts, v in self.metric_history[metric1] if ts > cutoff]
        values2 = [v for ts, v in self.metric_history[metric2] if ts > cutoff]

        if len(values1) < 5 or len(values2) < 5 or len(values1) != len(values2):
            return None

        # Pearson correlation coefficient
        mean1 = statistics.mean(values1)
        mean2 = statistics.mean(values2)

        numerator = sum((v1 - mean1) * (v2 - mean2) for v1, v2 in zip(values1, values2))
        denom1 = sum((v1 - mean1) ** 2 for v1 in values1) ** 0.5
        denom2 = sum((v2 - mean2) ** 2 for v2 in values2) ** 0.5

        if denom1 == 0 or denom2 == 0:
            return None

        correlation = numerator / (denom1 * denom2)

        # Classify strength
        abs_corr = abs(correlation)
        if abs_corr < 0.3:
            strength = "none"
        elif abs_corr < 0.5:
            strength = "weak"
        elif abs_corr < 0.7:
            strength = "moderate"
        elif abs_corr < 0.9:
            strength = "strong"
        else:
            strength = "very_strong"

        direction = "positive" if correlation > 0 else "negative" if correlation < 0 else "none"

        return CorrelationResult(
            metric_1=metric1,
            metric_2=metric2,
            correlation_coefficient=correlation,
            strength=strength,
            direction=direction,
            sample_count=len(values1),
            time_period=f"{period_days}d"
        )

    def _log_correlation(self, correlation: CorrelationResult) -> None:
        """Log correlation analysis."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "metric_1": correlation.metric_1,
            "metric_2": correlation.metric_2,
            "correlation_coefficient": correlation.correlation_coefficient,
            "strength": correlation.strength,
            "direction": correlation.direction,
            "sample_count": correlation.sample_count,
            "time_period": correlation.time_period
        }

        try:
            with open(self.correlation_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[CORRELATION-ANALYZER] Failed to log: {e}")
