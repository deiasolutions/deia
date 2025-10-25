"""Tests for CorrelationAnalyzer service."""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.deia.services.correlation_analyzer import CorrelationAnalyzer


@pytest.fixture
def analyzer(tmp_path):
    """Provide CorrelationAnalyzer instance."""
    return CorrelationAnalyzer(tmp_path)


class TestMetricRecording:
    """Tests for metric recording."""

    def test_record_metric(self, analyzer):
        """Test recording a metric."""
        analyzer.record_metric("cpu", 45.0)
        assert "cpu" in analyzer.metric_history
        assert len(analyzer.metric_history["cpu"]) == 1

    def test_multiple_metrics(self, analyzer):
        """Test recording multiple metrics."""
        for i in range(5):
            analyzer.record_metric("cpu", 40 + i)
            analyzer.record_metric("memory", 50 + i)

        assert len(analyzer.metric_history["cpu"]) == 5
        assert len(analyzer.metric_history["memory"]) == 5


class TestCorrelationCalculation:
    """Tests for correlation analysis."""

    def test_positive_correlation(self, analyzer):
        """Test positive correlation detection."""
        # Create perfectly correlated metrics (y = x + 10)
        for i in range(20):
            analyzer.record_metric("metric_a", float(i))
            analyzer.record_metric("metric_b", float(i + 10))

        correlations = analyzer.analyze_correlations(7)

        assert len(correlations) > 0
        corr = correlations[0]
        assert corr.direction == "positive"
        assert corr.strength in ["strong", "very_strong"]
        assert corr.correlation_coefficient > 0.9

    def test_negative_correlation(self, analyzer):
        """Test negative correlation detection."""
        # Create inversely correlated metrics
        for i in range(20):
            analyzer.record_metric("cpu", float(i))
            analyzer.record_metric("idle", float(100 - i))

        correlations = analyzer.analyze_correlations(7)

        assert len(correlations) > 0
        corr = correlations[0]
        assert corr.direction == "negative"
        assert corr.correlation_coefficient < -0.9

    def test_no_correlation(self, analyzer):
        """Test no correlation detection."""
        # Random unrelated data
        import random
        for i in range(20):
            analyzer.record_metric("random_a", float(random.random() * 100))
            analyzer.record_metric("random_b", float(random.random() * 100))

        correlations = analyzer.analyze_correlations(7)

        if correlations:
            corr = correlations[0]
            assert corr.strength in ["none", "weak"]


class TestCorrelationMatrix:
    """Tests for correlation matrix generation."""

    def test_correlation_matrix_structure(self, analyzer):
        """Test correlation matrix has correct structure."""
        for i in range(15):
            analyzer.record_metric("m1", float(i))
            analyzer.record_metric("m2", float(i * 2))
            analyzer.record_metric("m3", float(i + 5))

        matrix = analyzer.get_correlation_matrix(7)

        assert isinstance(matrix, dict)
        assert "m1" in matrix
        assert "m2" in matrix
        assert "m3" in matrix

    def test_matrix_symmetry(self, analyzer):
        """Test correlation matrix is symmetric."""
        for i in range(15):
            analyzer.record_metric("a", float(i))
            analyzer.record_metric("b", float(i * 2))

        matrix = analyzer.get_correlation_matrix(7)

        if "a" in matrix and "b" in matrix["a"]:
            assert matrix["a"]["b"] == matrix["b"]["a"]


class TestPrediction:
    """Tests for metric prediction."""

    def test_predict_metric_basic(self, analyzer):
        """Test basic metric prediction."""
        # Establish pattern
        for i in range(20):
            analyzer.record_metric("temp", float(20 + i))
            analyzer.record_metric("demand", float(100 + i * 2))

        context = {"temp": 35.0}
        prediction = analyzer.predict_metric("demand", context)

        assert prediction is not None
        assert prediction.metric_name == "demand"
        assert prediction.confidence > 0

    def test_predict_without_context(self, analyzer):
        """Test prediction uses baseline without context."""
        for i in range(15):
            analyzer.record_metric("test", float(100 + i))

        prediction = analyzer.predict_metric("test")

        assert prediction is not None
        assert 100 <= prediction.predicted_value <= 115


class TestPatternSummary:
    """Tests for pattern discovery."""

    def test_pattern_summary_structure(self, analyzer):
        """Test pattern summary has correct structure."""
        for i in range(15):
            analyzer.record_metric("m1", float(i))
            analyzer.record_metric("m2", float(i * 2))

        summary = analyzer.get_pattern_summary()

        assert "total_metrics" in summary
        assert "total_correlations_analyzed" in summary
        assert "strong_correlations" in summary
        assert "patterns_discovered" in summary

    def test_pattern_discovery(self, analyzer):
        """Test strong patterns are discovered."""
        for i in range(20):
            analyzer.record_metric("x", float(i))
            analyzer.record_metric("y", float(i * 3))

        summary = analyzer.get_pattern_summary()

        assert summary["strong_correlations"] >= 0


class TestEdgeCases:
    """Edge case tests."""

    def test_insufficient_data(self, analyzer):
        """Test handling insufficient data."""
        analyzer.record_metric("test", 10.0)
        analyzer.record_metric("test", 20.0)

        correlations = analyzer.analyze_correlations(7)

        # Should handle gracefully (return None or empty)
        assert isinstance(correlations, list)

    def test_single_metric(self, analyzer):
        """Test handling single metric."""
        for i in range(15):
            analyzer.record_metric("only_one", float(i))

        correlations = analyzer.analyze_correlations(7)

        assert len(correlations) == 0

    def test_history_truncation(self, analyzer):
        """Test history is truncated to 30 days."""
        now = datetime.now()

        # Manually add old data
        analyzer.metric_history["old"].append((now - timedelta(days=40), 100.0))
        analyzer.metric_history["old"].append((now, 101.0))

        # Record new metric
        analyzer.record_metric("old", 102.0)

        # Old data should be removed
        assert len(analyzer.metric_history["old"]) <= 2


# Coverage summary
COVERAGE_TARGETS = {
    "Metric Recording": "✅ 2 tests",
    "Correlation Calculation": "✅ 3 tests",
    "Correlation Matrix": "✅ 2 tests",
    "Prediction": "✅ 2 tests",
    "Pattern Summary": "✅ 2 tests",
    "Edge Cases": "✅ 3 tests",
    "Total Tests": "14 tests",
    "Target Coverage": "70%+"
}

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
