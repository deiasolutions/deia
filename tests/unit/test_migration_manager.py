"""Unit tests for MigrationManager service."""

import pytest
from pathlib import Path
from src.deia.services.migration_manager import (
    MigrationManager, DeploymentPhase, DeploymentVersion
)


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    (work_dir / ".deia" / "migrations").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def manager(temp_work_dir):
    """Create MigrationManager instance."""
    return MigrationManager(temp_work_dir)


class TestDeploymentStaging:
    """Test deployment staging."""

    def test_stage_deployment(self, manager):
        """Test staging a new deployment."""
        success, version_id = manager.stage_deployment("v1.1.0")

        assert success
        assert version_id is not None
        assert manager.green_version is not None
        assert manager.green_version.tag == "v1.1.0"
        assert manager.phase == DeploymentPhase.GREEN_STAGING

    def test_stage_with_git_commit(self, manager):
        """Test staging with git commit."""
        commit = "abc123def456"
        success, version_id = manager.stage_deployment("v1.1.0", commit)

        assert success
        assert manager.green_version.git_commit == commit


class TestCanaryTesting:
    """Test canary testing."""

    def test_run_canary_tests(self, manager):
        """Test running canary tests."""
        success, version_id = manager.stage_deployment("v1.1.0")
        assert success

        tests_passed = manager.run_canary_tests(version_id)
        assert tests_passed
        assert manager.green_version.canary_tests_passed


class TestTrafficShifting:
    """Test traffic shifting."""

    def test_start_traffic_shift(self, manager):
        """Test starting traffic shift."""
        success, version_id = manager.stage_deployment("v1.1.0")
        manager.run_canary_tests(version_id)

        success = manager.start_traffic_shift(version_id)
        assert success
        assert manager.phase == DeploymentPhase.SHIFTING_TRAFFIC

    def test_shift_traffic_gradually(self, manager):
        """Test gradual traffic shifting."""
        success, version_id = manager.stage_deployment("v1.1.0")
        manager.run_canary_tests(version_id)
        manager.start_traffic_shift(version_id)

        # Shift 25%
        success = manager.shift_traffic(25.0)
        assert success
        assert manager.traffic_to_green == 25.0

        # Shift 50%
        success = manager.shift_traffic(50.0)
        assert success
        assert manager.traffic_to_green == 50.0

        # Shift 100%
        success = manager.shift_traffic(100.0)
        assert success
        assert manager.traffic_to_green == 100.0

    def test_shift_invalid_percentage(self, manager):
        """Test invalid traffic percentage."""
        success, version_id = manager.stage_deployment("v1.1.0")
        manager.run_canary_tests(version_id)
        manager.start_traffic_shift(version_id)

        # Try invalid percentage
        success = manager.shift_traffic(150.0)
        assert not success

    def test_shift_fails_on_unhealthy_version(self, manager):
        """Test traffic shift blocked on unhealthy version."""
        success, version_id = manager.stage_deployment("v1.1.0")
        manager.run_canary_tests(version_id)
        manager.start_traffic_shift(version_id)

        # Try to shift with low success rate
        metrics = {"success_rate": 0.80}  # Too low
        success = manager.shift_traffic(50.0, metrics)
        assert not success


class TestDeploymentCompletion:
    """Test deployment completion."""

    def test_complete_deployment(self, manager):
        """Test completing a deployment."""
        success, version_id = manager.stage_deployment("v1.1.0")
        manager.run_canary_tests(version_id)
        manager.start_traffic_shift(version_id)
        manager.shift_traffic(100.0)

        success = manager.complete_deployment(version_id)
        assert success
        assert manager.phase == DeploymentPhase.BLUE_RUNNING
        assert manager.blue_version.tag == "v1.1.0"
        assert manager.green_version is None

    def test_complete_requires_100_percent(self, manager):
        """Test that completion requires 100% traffic."""
        success, version_id = manager.stage_deployment("v1.1.0")
        manager.run_canary_tests(version_id)
        manager.start_traffic_shift(version_id)
        manager.shift_traffic(50.0)  # Only 50%

        success = manager.complete_deployment(version_id)
        assert not success


class TestRollback:
    """Test rollback functionality."""

    def test_rollback_during_deployment(self, manager):
        """Test rollback during deployment."""
        # Stage initial blue version
        manager.blue_version = DeploymentVersion(
            version_id="blue-1",
            tag="v1.0.0",
            timestamp="2025-10-25T00:00:00",
            type="blue"
        )
        manager.phase = DeploymentPhase.BLUE_RUNNING

        # Stage green version
        success, version_id = manager.stage_deployment("v1.1.0")
        manager.run_canary_tests(version_id)
        manager.start_traffic_shift(version_id)
        manager.shift_traffic(50.0)

        # Rollback
        success = manager.rollback()
        assert success
        assert manager.phase == DeploymentPhase.BLUE_RUNNING
        assert manager.green_version is None
        assert manager.traffic_to_green == 0.0


class TestStatus:
    """Test status reporting."""

    def test_get_deployment_status(self, manager):
        """Test getting deployment status."""
        success, version_id = manager.stage_deployment("v1.1.0")

        status = manager.get_deployment_status()
        assert status.phase == DeploymentPhase.GREEN_STAGING
        assert status.green_version == "v1.1.0"

    def test_get_deployment_progress(self, manager):
        """Test getting deployment progress."""
        success, version_id = manager.stage_deployment("v1.1.0")
        manager.run_canary_tests(version_id)
        manager.start_traffic_shift(version_id)
        manager.shift_traffic(50.0)

        progress = manager.get_deployment_progress()
        assert progress["phase"] == "shifting"
        assert progress["traffic"]["green_percentage"] == 50.0
        assert progress["traffic"]["blue_percentage"] == 50.0

    def test_get_deployment_history(self, manager):
        """Test getting deployment history."""
        # Complete one deployment
        success, version_id = manager.stage_deployment("v1.1.0")
        manager.run_canary_tests(version_id)
        manager.start_traffic_shift(version_id)
        manager.shift_traffic(100.0)
        manager.complete_deployment(version_id)

        history = manager.get_deployment_history()
        assert len(history) == 1
        assert history[0]["result"] == "success"


class TestStateChecks:
    """Test state checking methods."""

    def test_is_deployment_active(self, manager):
        """Test checking if deployment is active."""
        assert not manager.is_deployment_active()

        manager.stage_deployment("v1.1.0")
        assert manager.is_deployment_active()

    def test_can_proceed_with_traffic_shift(self, manager):
        """Test safety check for traffic shifting."""
        # Before staging
        assert not manager.can_proceed_with_traffic_shift()

        # After staging but before canary tests
        manager.stage_deployment("v1.1.0")
        assert not manager.can_proceed_with_traffic_shift()

        # After canary tests
        manager.run_canary_tests(manager.green_version.version_id)
        assert manager.can_proceed_with_traffic_shift()


class TestLogging:
    """Test event logging."""

    def test_deployment_logged(self, manager, temp_work_dir):
        """Test that deployments are logged."""
        manager.stage_deployment("v1.1.0")

        log_file = temp_work_dir / ".deia" / "bot-logs" / "migration-log.jsonl"
        assert log_file.exists()

        with open(log_file) as f:
            lines = f.readlines()
        assert len(lines) > 0
