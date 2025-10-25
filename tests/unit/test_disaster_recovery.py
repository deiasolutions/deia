"""
Unit tests for DisasterRecovery service.

Tests backup creation, restore, crash detection, and recovery procedures.
"""

import pytest
from pathlib import Path
from src.deia.services.disaster_recovery import (
    DisasterRecovery, BackupType, BackupMetadata, RestorePoint
)
import json
import time


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "backups").mkdir(parents=True, exist_ok=True)
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    (work_dir / ".deia" / "state").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def dr(temp_work_dir):
    """Create DisasterRecovery instance."""
    return DisasterRecovery(temp_work_dir)


class TestBackupCreation:
    """Test backup creation functionality."""

    def test_create_registry_backup(self, dr):
        """Test creating a registry backup."""
        data = {
            "bot-001": {"type": "developer"},
            "bot-002": {"type": "analyzer"}
        }

        success, backup_id = dr.create_backup(
            BackupType.REGISTRY,
            data,
            "test-registry"
        )

        assert success
        assert backup_id is not None
        assert backup_id in dr.backups
        assert dr.backups[backup_id].backup_type == BackupType.REGISTRY

    def test_create_queue_backup(self, dr):
        """Test creating a queue backup."""
        data = {
            "tasks": [
                {"id": "task-1", "status": "pending"},
                {"id": "task-2", "status": "running"}
            ]
        }

        success, backup_id = dr.create_backup(
            BackupType.QUEUE,
            data,
            "test-queue"
        )

        assert success
        assert backup_id in dr.backups
        assert dr.backups[backup_id].backup_type == BackupType.QUEUE

    def test_create_assignments_backup(self, dr):
        """Test creating bot assignments backup."""
        data = {
            "assignments": {
                "bot-001": ["task-1", "task-2"],
                "bot-002": ["task-3"]
            }
        }

        success, backup_id = dr.create_backup(
            BackupType.BOT_ASSIGNMENTS,
            data
        )

        assert success
        assert backup_id in dr.backups

    def test_backup_with_tags(self, dr):
        """Test creating backup with tags."""
        data = {"test": "data"}
        tags = {"environment": "production", "version": "1.0"}

        success, backup_id = dr.create_backup(
            BackupType.REGISTRY,
            data,
            tags=tags
        )

        assert success
        assert dr.backups[backup_id].tags == tags

    def test_backup_file_created(self, dr, temp_work_dir):
        """Test that backup file is actually created."""
        data = {"test": "data"}

        success, backup_id = dr.create_backup(
            BackupType.REGISTRY,
            data
        )

        assert success
        backup_file = temp_work_dir / ".deia" / "backups" / f"{backup_id}.json"
        assert backup_file.exists()

        # Verify content
        with open(backup_file) as f:
            saved_data = json.load(f)
        assert saved_data == data

    def test_backup_checksum_calculation(self, dr):
        """Test that checksum is calculated correctly."""
        data = {"test": "data"}

        success, backup_id = dr.create_backup(
            BackupType.REGISTRY,
            data
        )

        assert success
        metadata = dr.backups[backup_id]
        assert metadata.checksum is not None
        assert len(metadata.checksum) == 64  # SHA256 hex length


class TestBackupRestore:
    """Test backup restoration functionality."""

    def test_restore_backup(self, dr):
        """Test restoring a backup."""
        original_data = {
            "bot-001": {"type": "developer"},
            "bot-002": {"type": "analyzer"}
        }

        # Create backup
        success, backup_id = dr.create_backup(
            BackupType.REGISTRY,
            original_data
        )
        assert success

        # Restore backup
        success, restored_data = dr.restore_backup(backup_id)
        assert success
        assert restored_data == original_data

    def test_restore_nonexistent_backup(self, dr):
        """Test restoring backup that doesn't exist."""
        success, data = dr.restore_backup("nonexistent-id")
        assert not success
        assert data is None

    def test_restore_detects_corrupted_backup(self, dr, temp_work_dir):
        """Test that restore detects corrupted backup."""
        data = {"test": "data"}
        success, backup_id = dr.create_backup(
            BackupType.REGISTRY,
            data
        )
        assert success

        # Corrupt the backup file
        backup_file = temp_work_dir / ".deia" / "backups" / f"{backup_id}.json"
        with open(backup_file, 'w') as f:
            f.write("corrupted data")

        # Try to restore
        success, restored_data = dr.restore_backup(backup_id)
        assert not success

    def test_restore_multiple_backups(self, dr):
        """Test restoring multiple different backups."""
        data1 = {"registry": "data1"}
        data2 = {"queue": "data2"}
        data3 = {"assignments": "data3"}

        # Create backups
        success1, bid1 = dr.create_backup(BackupType.REGISTRY, data1)
        success2, bid2 = dr.create_backup(BackupType.QUEUE, data2)
        success3, bid3 = dr.create_backup(BackupType.BOT_ASSIGNMENTS, data3)

        assert success1 and success2 and success3

        # Restore each
        _, restored1 = dr.restore_backup(bid1)
        _, restored2 = dr.restore_backup(bid2)
        _, restored3 = dr.restore_backup(bid3)

        assert restored1 == data1
        assert restored2 == data2
        assert restored3 == data3


class TestRestorePoints:
    """Test restore point functionality."""

    def test_create_restore_point(self, dr):
        """Test creating a full restore point."""
        registry = {"bot-001": "data"}
        queue = {"tasks": []}
        assignments = {"bot-001": ["task-1"]}

        success, restore_id = dr.create_restore_point(
            registry_data=registry,
            queue_data=queue,
            assignments_data=assignments,
            description="test-restore-point"
        )

        assert success
        assert restore_id in dr.restore_points
        assert len(dr.restore_points[restore_id].backups) == 3

    def test_restore_point_contains_all_backups(self, dr):
        """Test that restore point contains backups."""
        data = {"test": "data"}

        success, restore_id = dr.create_restore_point(
            registry_data=data,
            queue_data=data,
            assignments_data=data
        )

        assert success
        rp = dr.restore_points[restore_id]
        assert len(rp.backups) == 3

        # All backups should exist
        for backup_id in rp.backups:
            assert backup_id in dr.backups

    def test_restore_point_details(self, dr):
        """Test getting restore point details."""
        data = {"test": "data"}

        success, restore_id = dr.create_restore_point(
            registry_data=data,
            description="test-details"
        )

        assert success
        details = dr.get_restore_point_details(restore_id)
        assert details is not None
        assert details["description"] == "test-details"
        assert len(details["backup_details"]) > 0

    def test_manual_restore_point_flag(self, dr):
        """Test that manual flag is set correctly."""
        data = {"test": "data"}

        success, restore_id = dr.create_restore_point(
            registry_data=data,
            manual=True
        )

        assert success
        rp = dr.restore_points[restore_id]
        assert rp.manually_created is True

    def test_get_nonexistent_restore_point(self, dr):
        """Test getting details of nonexistent restore point."""
        details = dr.get_restore_point_details("nonexistent-id")
        assert details is None


class TestAutoBackup:
    """Test automatic backup functionality."""

    def test_auto_backup_creates_restore_point(self, dr):
        """Test that auto_backup creates a restore point."""
        data = {"test": "data"}

        success = dr.auto_backup_if_needed(
            registry_data=data,
            queue_data=data,
            assignments_data=data
        )

        assert success
        assert len(dr.restore_points) > 0

    def test_auto_backup_respects_interval(self, dr):
        """Test that auto_backup respects time interval."""
        data = {"test": "data"}

        # First backup should succeed
        success1 = dr.auto_backup_if_needed(registry_data=data)
        assert success1

        # Second backup immediately should fail (interval not elapsed)
        success2 = dr.auto_backup_if_needed(registry_data=data)
        assert not success2

    def test_auto_backup_after_interval(self, dr):
        """Test auto_backup after interval has passed."""
        data = {"test": "data"}

        # First backup
        success1 = dr.auto_backup_if_needed(registry_data=data)
        assert success1

        # Fake time passing
        dr._last_auto_backup = dr._last_auto_backup.__class__(
            dr._last_auto_backup.year,
            dr._last_auto_backup.month,
            dr._last_auto_backup.day,
            0, 0, 0
        )

        # Now second backup should succeed
        success2 = dr.auto_backup_if_needed(registry_data=data)
        assert success2


class TestCrashDetection:
    """Test crash detection functionality."""

    def test_detect_crash_no_shutdown_marker(self, dr):
        """Test that crash is detected when no shutdown marker."""
        crashed, restore_id = dr.detect_crash_state()
        assert crashed

    def test_no_crash_with_recent_shutdown_marker(self, dr, temp_work_dir):
        """Test no crash detected with recent shutdown marker."""
        dr.mark_clean_shutdown()

        crashed, restore_id = dr.detect_crash_state()
        assert not crashed

    def test_crash_with_stale_shutdown_marker(self, dr, temp_work_dir):
        """Test crash detected with old shutdown marker."""
        import os

        dr.mark_clean_shutdown()

        # Make marker old
        marker = temp_work_dir / ".deia" / "state" / "shutdown.marker"
        old_time = time.time() - 100  # 100 seconds ago
        os.utime(str(marker), (old_time, old_time))

        crashed, restore_id = dr.detect_crash_state()
        assert crashed

    def test_clear_shutdown_marker(self, dr, temp_work_dir):
        """Test clearing shutdown marker."""
        dr.mark_clean_shutdown()

        marker = temp_work_dir / ".deia" / "state" / "shutdown.marker"
        assert marker.exists()

        success = dr.clear_shutdown_marker()
        assert success
        assert not marker.exists()


class TestBackupHistory:
    """Test backup history and listing."""

    def test_get_backup_history(self, dr):
        """Test getting backup history."""
        data = {"test": "data"}

        dr.create_backup(BackupType.REGISTRY, data)
        dr.create_backup(BackupType.QUEUE, data)
        dr.create_backup(BackupType.BOT_ASSIGNMENTS, data)

        history = dr.get_backup_history()
        assert len(history) == 3

    def test_get_backup_history_filtered(self, dr):
        """Test getting backup history filtered by type."""
        data = {"test": "data"}

        dr.create_backup(BackupType.REGISTRY, data)
        dr.create_backup(BackupType.QUEUE, data)
        dr.create_backup(BackupType.BOT_ASSIGNMENTS, data)

        registry_backups = dr.get_backup_history(BackupType.REGISTRY)
        assert len(registry_backups) == 1
        assert registry_backups[0]["backup_type"] == "registry"

    def test_backup_history_limit(self, dr):
        """Test that backup history respects limit."""
        data = {"test": "data"}

        for _ in range(10):
            dr.create_backup(BackupType.REGISTRY, data)

        history = dr.get_backup_history(limit=5)
        assert len(history) == 5


class TestStatus:
    """Test status and diagnostics."""

    def test_get_status(self, dr):
        """Test getting disaster recovery status."""
        data = {"test": "data"}
        dr.create_backup(BackupType.REGISTRY, data)

        status = dr.get_status()
        assert status["total_backups"] == 1
        assert status["latest_backup"] is not None
        assert "disk_usage_mb" in status

    def test_status_shows_crash_detection(self, dr):
        """Test that status includes crash detection."""
        status = dr.get_status()
        assert "crash_detected" in status
        assert isinstance(status["crash_detected"], bool)

    def test_status_count_by_type(self, dr):
        """Test that status includes counts by type."""
        data = {"test": "data"}
        dr.create_backup(BackupType.REGISTRY, data)
        dr.create_backup(BackupType.QUEUE, data)

        status = dr.get_status()
        assert status["backups_by_type"]["registry"] == 1
        assert status["backups_by_type"]["queue"] == 1


class TestPersistence:
    """Test backup index persistence."""

    def test_backup_index_saved(self, dr, temp_work_dir):
        """Test that backup index is saved."""
        data = {"test": "data"}
        dr.create_backup(BackupType.REGISTRY, data)

        dr._save_backup_index()

        index_file = temp_work_dir / ".deia" / "backups" / "index.json"
        assert index_file.exists()

    def test_backup_index_loaded(self, temp_work_dir):
        """Test that backup index can be loaded."""
        # Create a DR instance and add backups
        dr1 = DisasterRecovery(temp_work_dir)
        data = {"test": "data"}
        dr1.create_backup(BackupType.REGISTRY, data)
        dr1._save_backup_index()

        # Create new instance and verify it loads backups
        dr2 = DisasterRecovery(temp_work_dir)
        assert len(dr2.backups) > 0


class TestLogging:
    """Test logging functionality."""

    def test_backup_event_logged(self, dr):
        """Test that backup creation is logged."""
        data = {"test": "data"}
        dr.create_backup(BackupType.REGISTRY, data)

        log_file = dr.dr_log
        assert log_file.exists()

        with open(log_file) as f:
            lines = f.readlines()
        assert len(lines) > 0

        last_entry = json.loads(lines[-1])
        assert last_entry["event"] == "backup_created"

    def test_restore_event_logged(self, dr):
        """Test that restore is logged."""
        data = {"test": "data"}
        success, backup_id = dr.create_backup(BackupType.REGISTRY, data)

        dr.restore_backup(backup_id)

        with open(dr.dr_log) as f:
            lines = f.readlines()

        last_entry = json.loads(lines[-1])
        assert last_entry["event"] == "restore_successful"


class TestCleanup:
    """Test automatic cleanup of old backups."""

    def test_cleanup_old_backups(self, dr, temp_work_dir):
        """Test that old backups are cleaned up."""
        from datetime import datetime, timedelta

        data = {"test": "data"}

        # Create backup
        success, backup_id = dr.create_backup(BackupType.REGISTRY, data)
        assert success

        # Artificially age the backup
        old_date = (datetime.now() - timedelta(days=8)).isoformat()
        dr.backups[backup_id].timestamp = old_date

        # Cleanup should remove it
        dr._cleanup_old_backups()

        assert backup_id not in dr.backups

        # File should be deleted
        backup_file = temp_work_dir / ".deia" / "backups" / f"{backup_id}.json"
        assert not backup_file.exists()
