"""Unit tests for DegradationManager service."""

import pytest
from pathlib import Path
from src.deia.services.degradation_manager import (
    DegradationManager, DegradationMode, DegradationCause
)


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def manager(temp_work_dir):
    """Create DegradationManager instance."""
    return DegradationManager(temp_work_dir)


class TestModeTransitions:
    """Test mode transitions."""

    def test_full_to_degraded(self, manager):
        """Test transitioning from FULL to DEGRADED."""
        assert manager.mode == DegradationMode.FULL

        success = manager.transition_to_degraded(
            DegradationCause.HIGH_LOAD,
            active_bots=3,
            total_bots=5
        )

        assert success
        assert manager.mode == DegradationMode.DEGRADED
        assert manager.cause == DegradationCause.HIGH_LOAD

    def test_degraded_to_full(self, manager):
        """Test recovering from DEGRADED to FULL."""
        manager.transition_to_degraded(DegradationCause.HIGH_LOAD)
        assert manager.mode == DegradationMode.DEGRADED

        success = manager.transition_to_full()
        assert success
        assert manager.mode == DegradationMode.FULL

    def test_full_to_maintenance(self, manager):
        """Test entering MAINTENANCE mode."""
        success = manager.transition_to_maintenance("Planned maintenance")
        assert success
        assert manager.mode == DegradationMode.MAINTENANCE

    def test_duplicate_degradation(self, manager):
        """Test that duplicate transitions fail."""
        manager.transition_to_degraded(DegradationCause.HIGH_LOAD)
        success = manager.transition_to_degraded(DegradationCause.HIGH_LOAD)
        assert not success


class TestFeatureManagement:
    """Test feature enable/disable."""

    def test_all_features_enabled_in_full_mode(self, manager):
        """Test all features enabled in FULL mode."""
        assert manager.mode == DegradationMode.FULL
        assert manager.is_feature_enabled("task_orchestration")
        assert manager.is_feature_enabled("auto_scaling")
        assert manager.is_feature_enabled("analytics")

    def test_features_disabled_in_degraded_mode(self, manager):
        """Test features disabled in DEGRADED mode."""
        manager.transition_to_degraded(DegradationCause.HIGH_LOAD)

        # Critical features still enabled
        assert manager.is_feature_enabled("task_orchestration")

        # Optional features disabled
        assert not manager.is_feature_enabled("analytics")

    def test_get_feature_status(self, manager):
        """Test getting feature status."""
        status = manager.get_feature_status()

        assert "task_orchestration" in status
        assert "auto_scaling" in status
        assert "analytics" in status

        for feature_name, feature_status in status.items():
            assert feature_status.name == feature_name
            assert hasattr(feature_status, 'enabled')
            assert hasattr(feature_status, 'criticality')


class TestFallbackLogic:
    """Test fallback routing."""

    def test_get_fallback_bot(self, manager):
        """Test getting healthiest bot for fallback."""
        available_bots = ["bot-1", "bot-2", "bot-3"]
        bot_health = {
            "bot-1": {"success_rate": 0.95, "cpu_percent": 0.3},
            "bot-2": {"success_rate": 0.80, "cpu_percent": 0.5},
            "bot-3": {"success_rate": 0.85, "cpu_percent": 0.4}
        }

        selected_bot = manager.get_fallback_bot(available_bots, bot_health)
        assert selected_bot == "bot-1"

    def test_fallback_no_bots(self, manager):
        """Test fallback with no available bots."""
        available_bots = []
        bot_health = {}

        selected_bot = manager.get_fallback_bot(available_bots, bot_health)
        assert selected_bot is None


class TestAutomaticDegradation:
    """Test automatic degradation detection."""

    def test_degrade_on_high_cpu(self, manager):
        """Test automatic degradation on high CPU."""
        cause = manager.apply_resource_constraints(
            memory_usage_percent=50.0,
            cpu_usage_percent=95.0,
            active_bots_count=5,
            total_bots_count=5
        )

        assert cause == DegradationCause.HIGH_LOAD
        assert manager.mode == DegradationMode.DEGRADED

    def test_degrade_on_high_memory(self, manager):
        """Test automatic degradation on high memory."""
        cause = manager.apply_resource_constraints(
            memory_usage_percent=90.0,
            cpu_usage_percent=50.0,
            active_bots_count=5,
            total_bots_count=5
        )

        assert cause == DegradationCause.MEMORY_PRESSURE
        assert manager.mode == DegradationMode.DEGRADED

    def test_degrade_on_bot_failure(self, manager):
        """Test automatic degradation on bot failure."""
        cause = manager.apply_resource_constraints(
            memory_usage_percent=50.0,
            cpu_usage_percent=50.0,
            active_bots_count=2,
            total_bots_count=5
        )

        assert cause == DegradationCause.BOT_FAILURE
        assert manager.mode == DegradationMode.DEGRADED

    def test_recover_when_resources_improve(self, manager):
        """Test recovery when resources improve."""
        # First degrade
        manager.apply_resource_constraints(
            memory_usage_percent=90.0,
            cpu_usage_percent=95.0,
            active_bots_count=2,
            total_bots_count=5
        )
        assert manager.mode == DegradationMode.DEGRADED

        # Then recover
        manager.apply_resource_constraints(
            memory_usage_percent=60.0,
            cpu_usage_percent=60.0,
            active_bots_count=5,
            total_bots_count=5
        )
        assert manager.mode == DegradationMode.FULL


class TestFeatureControl:
    """Test feature control methods."""

    def test_scaling_disabled_in_degraded(self, manager):
        """Test that scaling is disabled in degraded mode."""
        manager.transition_to_degraded(DegradationCause.HIGH_LOAD)
        assert not manager.should_enable_scaling()

    def test_scaling_enabled_in_full(self, manager):
        """Test that scaling is enabled in full mode."""
        assert manager.should_enable_scaling()

    def test_analytics_disabled_in_maintenance(self, manager):
        """Test that analytics disabled in maintenance."""
        manager.transition_to_maintenance()
        assert not manager.should_enable_analytics()


class TestStatus:
    """Test status reporting."""

    def test_get_state(self, manager):
        """Test getting degradation state."""
        manager.transition_to_degraded(
            DegradationCause.HIGH_LOAD,
            active_bots=3,
            total_bots=5
        )

        state = manager.get_state()
        assert state.mode == DegradationMode.DEGRADED
        assert state.cause == DegradationCause.HIGH_LOAD
        assert state.active_bots == 3
        assert state.total_bots == 5

    def test_get_status(self, manager):
        """Test getting detailed status."""
        manager.transition_to_degraded(DegradationCause.HIGH_LOAD)

        status = manager.get_status()
        assert status["mode"] == "degraded"
        assert "feature_status" in status
        assert "bot_status" in status
        assert "time_in_mode" in status


class TestLogging:
    """Test event logging."""

    def test_degradation_logged(self, manager, temp_work_dir):
        """Test that degradation is logged."""
        manager.transition_to_degraded(DegradationCause.HIGH_LOAD)

        log_file = temp_work_dir / ".deia" / "bot-logs" / "degradation-events.jsonl"
        assert log_file.exists()

    def test_recovery_logged(self, manager, temp_work_dir):
        """Test that recovery is logged."""
        manager.transition_to_degraded(DegradationCause.HIGH_LOAD)
        manager.transition_to_full()

        log_file = temp_work_dir / ".deia" / "bot-logs" / "degradation-events.jsonl"
        with open(log_file) as f:
            lines = f.readlines()

        assert len(lines) == 2
