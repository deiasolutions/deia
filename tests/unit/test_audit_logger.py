"""Unit tests for AuditLogger service."""

import pytest
from pathlib import Path
from src.deia.services.audit_logger import AuditLogger, AuditAction, AuditLevel
import json


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def logger(temp_work_dir):
    """Create AuditLogger instance."""
    return AuditLogger(temp_work_dir)


class TestAuditLogging:
    """Test audit logging functionality."""

    def test_log_action(self, logger):
        """Test logging an action."""
        entry_id = logger.log_action(
            AuditAction.BOT_CREATED,
            "admin",
            "bot-001"
        )

        assert entry_id is not None
        assert entry_id in logger.entry_index
        assert logger.entry_index[entry_id].action == AuditAction.BOT_CREATED

    def test_log_action_with_details(self, logger):
        """Test logging action with details."""
        entry_id = logger.log_action(
            AuditAction.CONFIG_CHANGED,
            "system",
            "cpu_threshold",
            details={"old": 0.80, "new": 0.85}
        )

        entry = logger.entry_index[entry_id]
        assert entry.details["old"] == 0.80
        assert entry.details["new"] == 0.85

    def test_log_critical_action(self, logger):
        """Test logging critical action."""
        entry_id = logger.log_action(
            AuditAction.BACKUP_RESTORED,
            "admin",
            "registry",
            level=AuditLevel.CRITICAL
        )

        entry = logger.entry_index[entry_id]
        assert entry.level == AuditLevel.CRITICAL

    def test_log_failed_action(self, logger):
        """Test logging failed action."""
        entry_id = logger.log_action(
            AuditAction.TASK_SUBMITTED,
            "bot-001",
            "task-123",
            result="failure",
            error_message="Out of memory"
        )

        entry = logger.entry_index[entry_id]
        assert entry.result == "failure"
        assert entry.error_message == "Out of memory"


class TestQueryFunctionality:
    """Test querying audit trail."""

    def test_query_by_action(self, logger):
        """Test querying by action type."""
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-002")
        logger.log_action(AuditAction.BOT_DELETED, "admin", "bot-003")

        created = logger.query_entries(action=AuditAction.BOT_CREATED)
        assert len(created) == 2

        deleted = logger.query_entries(action=AuditAction.BOT_DELETED)
        assert len(deleted) == 1

    def test_query_by_actor(self, logger):
        """Test querying by actor."""
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")
        logger.log_action(AuditAction.BOT_CREATED, "system", "bot-002")

        admin_actions = logger.query_entries(actor="admin")
        assert len(admin_actions) == 1
        assert admin_actions[0]["actor"] == "admin"

    def test_query_by_target(self, logger):
        """Test querying by target."""
        logger.log_action(AuditAction.CONFIG_CHANGED, "admin", "cpu_threshold")
        logger.log_action(AuditAction.CONFIG_CHANGED, "admin", "memory_threshold")
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")

        cpu_changes = logger.query_entries(target="cpu_threshold")
        assert len(cpu_changes) == 1

    def test_get_actor_actions(self, logger):
        """Test getting all actions by an actor."""
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")
        logger.log_action(AuditAction.BOT_DELETED, "admin", "bot-001")
        logger.log_action(AuditAction.CONFIG_CHANGED, "system", "threshold")

        admin_actions = logger.get_actor_actions("admin")
        assert len(admin_actions) == 2

    def test_get_target_history(self, logger):
        """Test getting change history for a target."""
        logger.log_action(AuditAction.CONFIG_CHANGED, "admin", "threshold", details={"value": 1})
        logger.log_action(AuditAction.CONFIG_CHANGED, "admin", "threshold", details={"value": 2})
        logger.log_action(AuditAction.CONFIG_CHANGED, "admin", "other", details={"value": 3})

        history = logger.get_target_history("threshold")
        assert len(history) == 2

    def test_get_critical_actions(self, logger):
        """Test getting critical actions."""
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot", level=AuditLevel.CRITICAL)
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot", level=AuditLevel.INFO)

        critical = logger.get_critical_actions()
        assert len(critical) >= 1

    def test_get_failed_actions(self, logger):
        """Test getting failed actions."""
        logger.log_action(AuditAction.TASK_SUBMITTED, "bot", "task", result="success")
        logger.log_action(AuditAction.TASK_SUBMITTED, "bot", "task", result="failure")

        failed = logger.get_failed_actions()
        assert len(failed) >= 1


class TestIntegrity:
    """Test audit trail integrity."""

    def test_entry_checksum(self, logger):
        """Test that entries have checksums."""
        entry_id = logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")

        entry = logger.entry_index[entry_id]
        assert entry.checksum is not None
        assert len(entry.checksum) == 64  # SHA256

    def test_verify_integrity(self, logger):
        """Test integrity verification."""
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-002")

        verification = logger.verify_integrity()
        assert verification["verified"] is True
        assert verification["total_entries"] == 2
        assert verification["invalid_checksums"] == 0


class TestStatistics:
    """Test audit statistics."""

    def test_get_statistics(self, logger):
        """Test getting audit statistics."""
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")
        logger.log_action(AuditAction.BOT_CREATED, "system", "bot-002")
        logger.log_action(AuditAction.CONFIG_CHANGED, "admin", "threshold")

        stats = logger.get_statistics()
        assert stats["total_entries"] == 3
        assert "BOT_CREATED" in str(stats["actions"]) or "bot_created" in str(stats["actions"])
        assert "admin" in stats["actors"]
        assert "system" in stats["actors"]


class TestPersistence:
    """Test audit log persistence."""

    def test_audit_log_file_created(self, logger, temp_work_dir):
        """Test that audit log file is created."""
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")

        log_file = temp_work_dir / ".deia" / "bot-logs" / "audit-trail.jsonl"
        assert log_file.exists()

    def test_audit_log_immutability(self, logger, temp_work_dir):
        """Test that audit log is append-only."""
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-002")

        log_file = temp_work_dir / ".deia" / "bot-logs" / "audit-trail.jsonl"
        with open(log_file) as f:
            lines = f.readlines()

        assert len(lines) == 2

    def test_load_audit_log(self, temp_work_dir):
        """Test loading audit log on initialization."""
        logger1 = AuditLogger(temp_work_dir)
        logger1.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")
        logger1.log_action(AuditAction.BOT_CREATED, "admin", "bot-002")

        # Create new instance to test loading
        logger2 = AuditLogger(temp_work_dir)
        assert len(logger2.entries) == 2


class TestExport:
    """Test audit export functionality."""

    def test_export_entries(self, logger, temp_work_dir):
        """Test exporting entries."""
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")
        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-002")

        export_file = temp_work_dir / "audit-export.json"
        success = logger.export_entries(export_file)

        assert success
        assert export_file.exists()

        with open(export_file) as f:
            data = json.load(f)
        assert len(data) == 2


class TestCleanup:
    """Test cleanup functionality."""

    def test_cleanup_old_entries(self, logger):
        """Test cleanup of old entries."""
        from datetime import datetime, timedelta

        logger.log_action(AuditAction.BOT_CREATED, "admin", "bot-001")

        # Artificially age the entry
        old_date = (datetime.now() - timedelta(days=400)).isoformat()
        logger.entries[0].timestamp = old_date

        deleted = logger.cleanup_old_entries()
        assert deleted == 1
        assert len(logger.entries) == 0
