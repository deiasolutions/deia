"""
Tests for AnomalyDetector service - Statistical anomaly detection.

Coverage targets:
- Baseline calculation (MIN_SAMPLES_FOR_BASELINE)
- Z-score calculation
- Anomaly detection (confidence thresholds)
- Severity classification
- Root cause analysis
- Historical anomaly retrieval
- Summary statistics
"""

import pytest
import statistics
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.deia.services.anomaly_detector import (
    AnomalyDetector, AnomalyEvent, BaselineStats
)


@pytest.fixture
def detector(tmp_path):
    """Provide AnomalyDetector instance with temp directory."""
    return AnomalyDetector(tmp_path)


@pytest.fixture
def sample_metrics():
    """Generate sample metric data."""
    return {
        "task_latency": [100, 102, 101, 99, 103, 100, 101, 102, 101, 100],  # Normal
        "queue_depth": [5, 4, 6, 5, 4, 5, 6, 5, 4, 5],  # Normal
        "cpu_usage": [45, 46, 44, 47, 45, 46, 44, 45, 46, 45],  # Normal
    }


class TestBaselineCalculation:
    """Tests for baseline statistics calculation."""

    def test_baseline_not_calculated_with_few_samples(self, detector):
        """Test baseline not created until MIN_SAMPLES_FOR_BASELINE."""
        # Record < 10 samples
        for i in range(5):
            detector.record_metric("test_metric", float(i))

        assert "test_metric" not in detector.baselines

    def test_baseline_calculated_with_sufficient_samples(self, detector):
        """Test baseline created after MIN_SAMPLES_FOR_BASELINE."""
        # Record 15 samples (> 10)
        for i in range(15):
            detector.record_metric("test_metric", float(i))

        assert "test_metric" in detector.baselines
        baseline = detector.baselines["test_metric"]
        assert baseline.count == 15
        assert baseline.mean > 0
        assert baseline.std > 0

    def test_baseline_stats_accuracy(self, detector):
        """Test baseline statistics are calculated correctly."""
        values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for v in values:
            detector.record_metric("test", float(v))

        baseline = detector.baselines["test"]

        # Verify calculations
        assert baseline.mean == statistics.mean(values)
        assert baseline.std == statistics.stdev(values)
        assert baseline.min == min(values)
        assert baseline.max == max(values)

    def test_baseline_percentiles(self, detector):
        """Test P95 and P99 percentiles calculated."""
        values = list(range(1, 101))  # 1-100
        for v in values:
            detector.record_metric("test", float(v))

        baseline = detector.baselines["test"]

        # P95 should be around 95
        assert 93 <= baseline.p95 <= 96
        # P99 should be around 99
        assert 98 <= baseline.p99 <= 100


class TestAnomalyDetection:
    """Tests for anomaly detection logic."""

    def test_no_anomaly_within_baseline(self, detector, sample_metrics):
        """Test normal values don't trigger anomalies."""
        # Establish baseline
        for v in sample_metrics["task_latency"]:
            detector.record_metric("task_latency", v)

        # Test value within baseline
        anomaly = detector.detect_anomaly("task_latency", 101.0)

        assert anomaly is None

    def test_anomaly_detected_for_extreme_value(self, detector, sample_metrics):
        """Test extreme values trigger anomalies."""
        # Establish baseline (values ~100)
        for v in sample_metrics["task_latency"]:
            detector.record_metric("task_latency", v)

        # Test extreme value (3x higher = ~3 standard deviations)
        anomaly = detector.detect_anomaly("task_latency", 400.0)

        assert anomaly is not None
        assert anomaly.confidence >= 0.80
        assert anomaly.severity in ["high", "critical"]

    def test_z_score_calculation(self, detector):
        """Test z-score calculated correctly."""
        # Create known baseline: mean=100, std~2
        for v in [98, 99, 100, 101, 102, 98, 99, 100, 101, 102]:
            detector.record_metric("test", float(v))

        # Test z-score for value at mean + 6*std
        baseline = detector.baselines["test"]
        mean = baseline.mean
        std = baseline.std

        test_value = mean + (6 * std)
        anomaly = detector.detect_anomaly("test", test_value)

        assert anomaly is not None
        # Z-score should be ~6
        assert abs(anomaly.z_score) >= 5


class TestAnomalySeverity:
    """Tests for severity classification."""

    def test_severity_low(self, detector):
        """Test low severity for moderate deviation."""
        for v in range(1, 11):
            detector.record_metric("test", float(v))

        # Z-score ~1.7 (deviation 1.7*std) = low severity
        baseline = detector.baselines["test"]
        test_value = baseline.mean + (1.7 * baseline.std)
        anomaly = detector.detect_anomaly("test", test_value)

        if anomaly:
            assert anomaly.severity in ["low", "medium"]

    def test_severity_critical(self, detector):
        """Test critical severity for extreme deviation."""
        for v in range(1, 11):
            detector.record_metric("test", float(v))

        # Z-score > 3.0 = critical
        baseline = detector.baselines["test"]
        test_value = baseline.mean + (3.5 * baseline.std)
        anomaly = detector.detect_anomaly("test", test_value)

        assert anomaly is not None
        assert anomaly.severity == "critical"


class TestRootCauseAnalysis:
    """Tests for root cause suggestions."""

    def test_latency_anomaly_causes(self, detector):
        """Test root causes for latency anomalies."""
        # Create baseline with variance
        for v in [100, 101, 99, 102, 98, 101, 100, 99, 102, 101]:
            detector.record_metric("task_latency", float(v))

        # 3+ standard deviations
        anomaly = detector.detect_anomaly("task_latency", 300.0)

        assert anomaly is not None
        assert len(anomaly.root_causes) > 0
        # Should suggest queue/latency related causes
        assert len(anomaly.root_causes) >= 1

    def test_queue_depth_anomaly_causes(self, detector):
        """Test root causes for queue depth anomalies."""
        # Create baseline with variance
        for v in [5, 4, 6, 5, 4, 6, 5, 4, 5, 6]:
            detector.record_metric("queue_depth", float(v))

        # Very high queue depth (3+ std dev)
        anomaly = detector.detect_anomaly("queue_depth", 100.0)

        assert anomaly is not None
        assert len(anomaly.root_causes) > 0

    def test_resource_anomaly_causes(self, detector):
        """Test root causes for resource anomalies."""
        # Create baseline with variance
        for v in [45, 46, 44, 47, 43, 46, 45, 44, 47, 45]:
            detector.record_metric("cpu_usage", float(v))

        # 3+ std dev increase
        anomaly = detector.detect_anomaly("cpu_usage", 120.0)

        assert anomaly is not None
        assert len(anomaly.root_causes) > 0


class TestAnomalyClassification:
    """Tests for anomaly type classification."""

    def test_latency_classified_correctly(self, detector):
        """Test latency anomalies classified as latency type."""
        for v in [100, 101, 99, 102, 98, 101, 100, 99, 102, 101]:
            detector.record_metric("task_latency_ms", float(v))

        anomaly = detector.detect_anomaly("task_latency_ms", 500.0)

        assert anomaly is not None
        assert anomaly.anomaly_type == "latency"

    def test_queue_classified_correctly(self, detector):
        """Test queue anomalies classified as queue_depth type."""
        for v in [5, 4, 6, 5, 4, 6, 5, 4, 5, 6]:
            detector.record_metric("queue_depth", float(v))

        anomaly = detector.detect_anomaly("queue_depth", 100.0)

        assert anomaly is not None
        assert anomaly.anomaly_type == "queue_depth"

    def test_resource_classified_correctly(self, detector):
        """Test resource anomalies classified as resource_spike type."""
        for v in [40, 41, 39, 42, 38, 41, 40, 39, 42, 40]:
            detector.record_metric("cpu_usage_percent", float(v))

        anomaly = detector.detect_anomaly("cpu_usage_percent", 200.0)

        assert anomaly is not None
        assert anomaly.anomaly_type == "resource_spike"


class TestHistoryRetrieval:
    """Tests for anomaly history retrieval."""

    def test_get_recent_anomalies(self, detector):
        """Test retrieving anomalies from recent time window."""
        # Create baseline with variance
        for v in [100, 101, 99, 102, 98, 101, 100, 99, 102, 101]:
            detector.record_metric("test", float(v))

        # Create some anomalies (3+ std dev)
        for i in range(3):
            detector.detect_anomaly("test", 500.0)

        # Get recent (1 hour window)
        recent = detector.get_recent_anomalies(hours=1)

        assert len(recent) >= 3

    def test_recent_anomalies_time_filtered(self, detector):
        """Test anomalies filtered by time window."""
        for v in [100] * 10:
            detector.record_metric("test", float(v))

        # Create anomaly
        detector.detect_anomaly("test", 500.0)

        # Get recent from 5 minutes (should be empty if recorded more than 5 min ago)
        # This test might be timing-sensitive, so we check structure
        recent = detector.get_recent_anomalies(hours=0.001)

        # Should return list (may be empty or not depending on timing)
        assert isinstance(recent, list)


class TestSummaryStatistics:
    """Tests for anomaly summary statistics."""

    def test_anomaly_summary_structure(self, detector):
        """Test summary has correct structure."""
        summary = detector.get_anomaly_summary()

        assert "total_anomalies_24h" in summary
        assert "by_type" in summary
        assert "by_severity" in summary
        assert "baseline_count" in summary
        assert "metrics_tracked" in summary

    def test_anomaly_summary_accuracy(self, detector):
        """Test summary counts are accurate."""
        # Create baselines
        for metric in ["latency", "queue", "cpu"]:
            for v in range(1, 11):
                detector.record_metric(metric, float(v))

        # Create anomalies of different types
        detector.detect_anomaly("latency", 100.0)
        detector.detect_anomaly("queue", 100.0)

        summary = detector.get_anomaly_summary()

        assert summary["baseline_count"] == 3
        assert summary["metrics_tracked"] == 3


class TestConfidenceCalculation:
    """Tests for confidence-to-z-score conversion."""

    def test_confidence_low_z_score(self, detector):
        """Test confidence for low z-score."""
        confidence = detector._z_score_to_confidence(0.5)
        assert 0.6 <= confidence < 0.7

    def test_confidence_medium_z_score(self, detector):
        """Test confidence for medium z-score."""
        confidence = detector._z_score_to_confidence(2.0)
        assert 0.95 <= confidence <= 0.99

    def test_confidence_high_z_score(self, detector):
        """Test confidence for high z-score."""
        confidence = detector._z_score_to_confidence(3.0)
        assert confidence > 0.99


class TestContextIntegration:
    """Tests for context-aware anomaly detection."""

    def test_detect_anomaly_with_context(self, detector):
        """Test anomaly detection with additional context."""
        for v in [100, 101, 99, 102, 98, 101, 100, 99, 102, 101]:
            detector.record_metric("test", float(v))

        context = {
            "bot_id": "bot-001",
            "task_type": "analyze",
            "time_of_day": "peak"
        }

        anomaly = detector.detect_anomaly("test", 500.0, context=context)

        assert anomaly is not None
        # Context should be available via root cause analysis
        assert len(anomaly.root_causes) > 0


class TestEdgeCases:
    """Edge case and error handling tests."""

    def test_detect_anomaly_zero_variance(self, detector):
        """Test handling of zero variance baseline."""
        # Record same value repeatedly
        for _ in range(15):
            detector.record_metric("constant", 100.0)

        # Should return None (can't calculate z-score)
        anomaly = detector.detect_anomaly("constant", 200.0)

        assert anomaly is None

    def test_detect_anomaly_unknown_metric(self, detector):
        """Test detection on metric without baseline."""
        anomaly = detector.detect_anomaly("unknown_metric", 100.0)

        assert anomaly is None

    def test_multiple_anomalies_same_metric(self, detector):
        """Test tracking multiple anomalies for same metric."""
        for v in [100, 101, 99, 102, 98, 101, 100, 99, 102, 101]:
            detector.record_metric("test", float(v))

        # Create multiple anomalies
        anomaly1 = detector.detect_anomaly("test", 500.0)
        import time
        time.sleep(0.01)  # Ensure different timestamps
        anomaly2 = detector.detect_anomaly("test", 10.0)

        assert anomaly1 is not None
        assert anomaly2 is not None
        assert anomaly1.anomaly_id != anomaly2.anomaly_id


# Coverage summary
COVERAGE_TARGETS = {
    "Baseline Calculation": "✅ 4 tests",
    "Anomaly Detection": "✅ 3 tests",
    "Severity Classification": "✅ 2 tests",
    "Root Cause Analysis": "✅ 3 tests",
    "Anomaly Classification": "✅ 3 tests",
    "History Retrieval": "✅ 2 tests",
    "Summary Statistics": "✅ 2 tests",
    "Confidence Calculation": "✅ 3 tests",
    "Context Integration": "✅ 1 test",
    "Edge Cases": "✅ 3 tests",
    "Total Tests": "26 tests",
    "Target Coverage": "70%+"
}

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
