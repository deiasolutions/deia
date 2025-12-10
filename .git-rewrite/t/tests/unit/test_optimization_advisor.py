"""Tests for OptimizationAdvisor service."""

import pytest
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.deia.services.optimization_advisor import OptimizationAdvisor


@pytest.fixture
def advisor(tmp_path):
    """Provide OptimizationAdvisor instance."""
    return OptimizationAdvisor(tmp_path)


class TestRecommendations:
    """Tests for optimization recommendations."""

    def test_cpu_recommendation(self, advisor):
        """Test CPU optimization recommendation."""
        advisor.analyze_metrics({"cpu_usage": 80})
        recommendations = advisor.get_recommendations()

        assert len(recommendations) > 0
        assert any(r["metric"] == "cpu_usage" for r in recommendations)

    def test_multiple_recommendations(self, advisor):
        """Test multiple recommendations."""
        advisor.analyze_metrics({
            "cpu_usage": 85,
            "memory_usage": 80,
            "queue_depth": 60
        })

        recommendations = advisor.get_recommendations()

        assert len(recommendations) >= 3

    def test_no_recommendations(self, advisor):
        """Test no recommendations for healthy metrics."""
        advisor.analyze_metrics({
            "cpu_usage": 30,
            "memory_usage": 40,
            "queue_depth": 5
        })

        recommendations = advisor.get_recommendations()

        assert len(recommendations) == 0


class TestPrioritization:
    """Tests for recommendation prioritization."""

    def test_critical_priority_first(self, advisor):
        """Test critical recommendations come first."""
        advisor.analyze_metrics({"error_rate": 0.10})
        recommendations = advisor.get_recommendations()

        if recommendations:
            assert recommendations[0]["priority"] == "critical"

    def test_sort_by_roi(self, advisor):
        """Test recommendations sorted by ROI."""
        advisor.analyze_metrics({
            "cpu_usage": 80,
            "queue_depth": 60
        })

        recommendations = advisor.get_recommendations()

        if len(recommendations) >= 2:
            # Lower ROI days should come first
            roi_days = [r.get("roi_days", 999) for r in recommendations]
            assert roi_days == sorted(roi_days)


class TestSummary:
    """Tests for optimization summary."""

    def test_get_summary(self, advisor):
        """Test getting optimization summary."""
        advisor.analyze_metrics({"cpu_usage": 75})
        summary = advisor.get_optimization_summary()

        assert "total_recommendations" in summary
        assert "by_priority" in summary
        assert "timestamp" in summary

    def test_summary_counts(self, advisor):
        """Test summary counts are accurate."""
        advisor.analyze_metrics({
            "cpu_usage": 80,
            "error_rate": 0.10
        })

        summary = advisor.get_optimization_summary()

        assert summary["total_recommendations"] >= 2


class TestImpactEstimation:
    """Tests for impact estimation."""

    def test_estimate_impact(self, advisor):
        """Test impact estimation."""
        rec = {
            "recommendation": "Increase CPU",
            "metric": "cpu_usage",
            "current_value": 80,
            "target_value": 60,
            "effort": "medium",
            "roi_days": 1,
            "estimated_improvement": "20% throughput"
        }

        impact = advisor.estimate_impact(rec)

        assert "improvement_percent" in impact
        assert "roi_timeline_days" in impact
        assert impact["improvement_percent"] < 0  # Reduction

    def test_impact_calculation(self, advisor):
        """Test impact calculation accuracy."""
        rec = {
            "current_value": 100,
            "target_value": 50,
            "effort": "medium",
            "roi_days": 1
        }

        impact = advisor.estimate_impact(rec)

        # 50 vs 100 = -50%
        assert impact["improvement_percent"] == -50


# Coverage summary
COVERAGE_TARGETS = {
    "Recommendations": "✅ 3 tests",
    "Prioritization": "✅ 2 tests",
    "Summary": "✅ 2 tests",
    "Impact Estimation": "✅ 2 tests",
    "Total Tests": "9 tests",
    "Target Coverage": "70%+"
}

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
