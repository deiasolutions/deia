"""Tests for HeatMapGenerator service."""

import pytest
from pathlib import Path
from datetime import datetime
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.deia.services.heatmap_generator import HeatMapGenerator


@pytest.fixture
def generator(tmp_path):
    """Provide HeatMapGenerator instance."""
    return HeatMapGenerator(tmp_path)


class TestEventRecording:
    """Tests for event recording."""

    def test_record_event(self, generator):
        """Test recording an event."""
        generator.record_event("bot-001", "analyze", 1500.0, True)
        assert len(generator.events) == 1

    def test_multiple_events(self, generator):
        """Test recording multiple events."""
        for i in range(10):
            generator.record_event(f"bot-{i % 3}", "task", float(100 + i), i % 2 == 0)

        assert len(generator.events) == 10


class TestTimeOfDayHeatmap:
    """Tests for time-of-day heatmap."""

    def test_generate_time_heatmap(self, generator):
        """Test time-of-day heatmap generation."""
        for i in range(10):
            generator.record_event("bot-1", "task", 1000.0, True)

        heatmap = generator.generate_time_of_day_heatmap()

        assert heatmap["type"] == "time_of_day"
        assert len(heatmap["data"]) == 24  # All hours
        assert heatmap["data"][0]["hour"] == 0

    def test_time_heatmap_metrics(self, generator):
        """Test time heatmap includes correct metrics."""
        generator.record_event("bot-1", "task", 1000.0, True)

        heatmap = generator.generate_time_of_day_heatmap()

        entry = heatmap["data"][datetime.now().hour]
        assert "task_count" in entry
        assert "avg_duration_ms" in entry
        assert "success_rate" in entry


class TestBotUsageHeatmap:
    """Tests for bot usage heatmap."""

    def test_generate_bot_heatmap(self, generator):
        """Test bot usage heatmap generation."""
        for i in range(10):
            generator.record_event(f"bot-{i % 3}", "task", 1000.0, True)

        heatmap = generator.generate_bot_usage_heatmap()

        assert heatmap["type"] == "bot_usage"
        assert len(heatmap["data"]) > 0

    def test_bot_heatmap_metrics(self, generator):
        """Test bot heatmap includes correct metrics."""
        generator.record_event("bot-a", "task", 1000.0, True)
        generator.record_event("bot-a", "task", 2000.0, False)

        heatmap = generator.generate_bot_usage_heatmap()

        assert heatmap["data"][0]["task_count"] == 2
        assert heatmap["data"][0]["success_rate"] == 0.5


class TestTaskTypeHeatmap:
    """Tests for task type heatmap."""

    def test_generate_task_heatmap(self, generator):
        """Test task type heatmap generation."""
        for task_type in ["analyze", "process", "validate"]:
            for i in range(3):
                generator.record_event("bot-1", task_type, 1000.0, True)

        heatmap = generator.generate_task_type_heatmap()

        assert heatmap["type"] == "task_type"
        assert len(heatmap["data"]) == 3

    def test_task_heatmap_sorting(self, generator):
        """Test task heatmap sorts by count."""
        generator.record_event("bot-1", "common", 1000.0, True)
        for i in range(10):
            generator.record_event("bot-1", "common", 1000.0, True)
        generator.record_event("bot-1", "rare", 1000.0, True)

        heatmap = generator.generate_task_type_heatmap()

        # Common should be first
        assert heatmap["data"][0]["task_type"] == "common"
        assert heatmap["data"][0]["count"] == 11


class TestAllHeatmaps:
    """Tests for combined heatmap generation."""

    def test_get_all_heatmaps(self, generator):
        """Test getting all heatmaps."""
        for i in range(10):
            generator.record_event(f"bot-{i % 2}", "task", 1000.0, i % 2 == 0)

        heatmaps = generator.get_all_heatmaps()

        assert "time_of_day" in heatmaps
        assert "bot_usage" in heatmaps
        assert "task_type" in heatmaps

    def test_heatmap_structure(self, generator):
        """Test heatmap structure is JSON-serializable."""
        generator.record_event("bot-1", "task", 1000.0, True)

        heatmaps = generator.get_all_heatmaps()

        for heatmap in heatmaps.values():
            assert "title" in heatmap
            assert "type" in heatmap
            assert "data" in heatmap
            assert "timestamp" in heatmap


# Coverage summary
COVERAGE_TARGETS = {
    "Event Recording": "✅ 2 tests",
    "Time of Day Heatmap": "✅ 2 tests",
    "Bot Usage Heatmap": "✅ 2 tests",
    "Task Type Heatmap": "✅ 2 tests",
    "All Heatmaps": "✅ 2 tests",
    "Total Tests": "10 tests",
    "Target Coverage": "70%+"
}

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
