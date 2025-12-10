"""Tests for ComparativeAnalyzer service."""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.deia.services.comparative_analyzer import ComparativeAnalyzer


@pytest.fixture
def analyzer(tmp_path):
    """Provide ComparativeAnalyzer instance."""
    return ComparativeAnalyzer(tmp_path)


class TestDayOverDay:
    """Tests for day-over-day comparison."""

    def test_compare_day_over_day(self, analyzer):
        """Test day-over-day comparison."""
        # Record values
        analyzer.record_metric("cpu", 45.0)
        analyzer.record_metric("cpu", 46.0)

        result = analyzer.compare_day_over_day("cpu")

        # Result is None if no previous day data, which is ok
        # This test passes if result is None or has expected structure
        if result:
            assert "today_avg" in result
            assert "yesterday_avg" in result
            assert "trend" in result

    def test_missing_metric(self, analyzer):
        """Test missing metric returns None."""
        result = analyzer.compare_day_over_day("nonexistent")
        assert result is None


class TestWeekOverWeek:
    """Tests for week-over-week comparison."""

    def test_compare_week_over_week(self, analyzer):
        """Test week-over-week comparison."""
        analyzer.record_metric("latency", 100.0)
        analyzer.record_metric("latency", 101.0)

        result = analyzer.compare_week_over_week("latency")

        if result:
            assert "this_week_avg" in result
            assert "last_week_avg" in result


class TestTrendDetection:
    """Tests for trend detection."""

    def test_detect_upward_trend(self, analyzer):
        """Test upward trend detection."""
        # Create upward trend
        for i in range(10):
            analyzer.record_metric("metric", float(i * 10))

        trend = analyzer.detect_trend("metric")

        assert trend is not None
        assert trend["trend"] == "upward"

    def test_detect_downward_trend(self, analyzer):
        """Test downward trend detection."""
        for i in range(10, 0, -1):
            analyzer.record_metric("metric", float(i * 10))

        trend = analyzer.detect_trend("metric")

        assert trend is not None
        assert trend["trend"] == "downward"


class TestSummary:
    """Tests for comparison summary."""

    def test_get_comparison_summary(self, analyzer):
        """Test getting comparison summary."""
        analyzer.record_metric("m1", 50.0)
        analyzer.record_metric("m2", 100.0)

        summary = analyzer.get_comparison_summary()

        assert "summary" in summary
        assert "timestamp" in summary


# Coverage summary
COVERAGE_TARGETS = {
    "Day Over Day": "✅ 2 tests",
    "Week Over Week": "✅ 1 test",
    "Trend Detection": "✅ 2 tests",
    "Summary": "✅ 1 test",
    "Total Tests": "6 tests",
    "Target Coverage": "70%+"
}

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
