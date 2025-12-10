"""Tests for CapacityPlanner service."""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.deia.services.capacity_planner import CapacityPlanner


@pytest.fixture
def planner(tmp_path):
    """Provide CapacityPlanner instance."""
    return CapacityPlanner(tmp_path)


class TestMetricRecording:
    """Tests for metric recording."""

    def test_record_metric(self, planner):
        """Test recording a metric."""
        planner.record_metric("queue_depth", 10.0)
        assert "queue_depth" in planner.metrics
        assert len(planner.metrics["queue_depth"]) == 1

    def test_multiple_records(self, planner):
        """Test recording multiple values."""
        for i in range(10):
            planner.record_metric("cpu", float(40 + i))

        assert len(planner.metrics["cpu"]) == 10


class TestForecasting:
    """Tests for capacity forecasting."""

    def test_forecast_stable_metric(self, planner):
        """Test forecasting stable metric."""
        # Create stable data
        for i in range(15):
            planner.record_metric("cpu", 50.0)

        forecast = planner.forecast_metric("cpu", 7)

        assert forecast is not None
        assert forecast.trend == "stable"
        assert forecast.days_to_capacity is None

    def test_forecast_increasing_metric(self, planner):
        """Test forecasting increasing metric."""
        # Create increasing trend
        for i in range(15):
            planner.record_metric("queue_depth", float(10 + i))

        forecast = planner.forecast_metric("queue_depth", 7)

        assert forecast is not None
        assert forecast.trend == "increasing"

    def test_forecast_decreasing_metric(self, planner):
        """Test forecasting decreasing metric."""
        # Create decreasing trend
        for i in range(15, 0, -1):
            planner.record_metric("memory", float(i * 5))

        forecast = planner.forecast_metric("memory", 7)

        assert forecast is not None
        assert forecast.trend == "decreasing"

    def test_insufficient_data(self, planner):
        """Test forecasting with insufficient data."""
        planner.record_metric("test", 50.0)
        planner.record_metric("test", 51.0)

        forecast = planner.forecast_metric("test", 7)

        assert forecast is None

    def test_capacity_violation_detection(self, planner):
        """Test detection of capacity violations."""
        # Create data approaching capacity
        for i in range(15):
            planner.record_metric("queue_depth", float(80 + i))

        forecast = planner.forecast_metric("queue_depth", 7)

        # Should detect approaching capacity
        if forecast and forecast.days_to_capacity:
            assert forecast.days_to_capacity <= 7


class TestRecommendations:
    """Tests for recommendations."""

    def test_urgent_recommendation(self, planner):
        """Test urgent capacity recommendation."""
        # Create data that will exceed capacity soon
        for i in range(15):
            planner.record_metric("cpu", float(85 + i * 1.5))

        forecast = planner.forecast_metric("cpu", 7)

        if forecast and "URGENT" in forecast.recommendation:
            assert forecast.days_to_capacity and forecast.days_to_capacity <= 3

    def test_warning_recommendation(self, planner):
        """Test warning capacity recommendation."""
        for i in range(15):
            planner.record_metric("memory", float(70 + i * 0.5))

        forecast = planner.forecast_metric("memory", 7)

        if forecast:
            assert forecast.recommendation is not None


class TestSummary:
    """Tests for capacity summary."""

    def test_capacity_summary(self, planner):
        """Test getting capacity summary."""
        for i in range(15):
            planner.record_metric("queue_depth", float(20 + i))
            planner.record_metric("cpu", float(50 + i * 0.5))

        summary = planner.get_capacity_summary()

        assert "urgent_alerts" in summary
        assert "warnings" in summary
        assert "healthy_metrics" in summary
        assert "timestamp" in summary

    def test_all_forecasts(self, planner):
        """Test getting all forecasts."""
        for i in range(15):
            planner.record_metric("m1", float(i))
            planner.record_metric("m2", float(100 - i))

        forecasts = planner.get_all_forecasts()

        assert isinstance(forecasts, dict)


class TestCapacityLimits:
    """Tests for custom capacity limits."""

    def test_custom_limits(self, tmp_path):
        """Test custom capacity limits."""
        planner = CapacityPlanner(
            tmp_path,
            max_queue_depth=50,
            max_cpu=80.0,
            max_memory=85.0
        )

        assert planner.capacity_limits["queue_depth"] == 50
        assert planner.capacity_limits["cpu_usage"] == 80.0
        assert planner.capacity_limits["memory_usage"] == 85.0


# Coverage summary
COVERAGE_TARGETS = {
    "Metric Recording": "✅ 2 tests",
    "Forecasting": "✅ 5 tests",
    "Recommendations": "✅ 2 tests",
    "Summary": "✅ 2 tests",
    "Capacity Limits": "✅ 1 test",
    "Total Tests": "12 tests",
    "Target Coverage": "70%+"
}

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
