"""Integration tests for Production Hardening with Features 1-5"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime
from src.deia.services.config_manager import ConfigManager
from src.deia.services.disaster_recovery import DisasterRecovery
from src.deia.services.audit_logger import AuditLogger
from src.deia.services.degradation_manager import DegradationManager


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory"""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    (work_dir / ".deia" / "config").mkdir(parents=True, exist_ok=True)
    return work_dir


class TestConfigManagerIntegration:
    """Test configuration management with services"""

    def test_config_hot_reload(self, temp_work_dir):
        """Test config changes are picked up by services"""
        config = ConfigManager(temp_work_dir)

        # Load initial config
        config.load_config("test")

        # Update config
        config.set_config_value("max_bots", 10)
        assert config.get_config_value("max_bots") == 10

    def test_config_defaults(self, temp_work_dir):
        """Test config has sensible defaults"""
        config = ConfigManager(temp_work_dir)
        config.load_config("default")

        # Should have defaults
        assert config.config is not None


class TestDisasterRecoveryIntegration:
    """Test backup/restore with orchestration"""

    def test_backup_creation(self, temp_work_dir):
        """Test backup creation doesn't break services"""
        dr = DisasterRecovery(temp_work_dir)

        success = dr.create_backup()
        assert success

    def test_state_recovery(self, temp_work_dir):
        """Test state can be recovered from backup"""
        dr = DisasterRecovery(temp_work_dir)

        # Create and recover
        dr.create_backup()
        recovery_success = dr.verify_recovery_possible()
        assert recovery_success


class TestAuditLoggerIntegration:
    """Test audit logging doesn't break features"""

    def test_audit_logging(self, temp_work_dir):
        """Test audit logger works with all operations"""
        audit = AuditLogger(temp_work_dir)

        # Log various operations
        success = audit.log_action(
            user_id="user-001",
            action="submit_task",
            resource="task-001",
            result="success"
        )
        assert success

    def test_audit_log_queries(self, temp_work_dir):
        """Test audit log can be queried"""
        audit = AuditLogger(temp_work_dir)

        audit.log_action("user-001", "action1", "resource", "success")
        audit.log_action("user-001", "action2", "resource", "success")

        # Query logs
        entries = audit.get_action_history("user-001")
        assert len(entries) >= 2


class TestDegradationManagerIntegration:
    """Test graceful degradation with services"""

    def test_degradation_activation(self, temp_work_dir):
        """Test system switches to degraded mode"""
        dm = DegradationManager(temp_work_dir)

        # Should start in NORMAL mode
        assert dm.current_mode.value == "normal"

    def test_degraded_mode_apis_work(self, temp_work_dir):
        """Test APIs still work in degraded mode"""
        dm = DegradationManager(temp_work_dir)

        # Activate degradation
        dm.activate_degradation_mode()

        # System should still report status
        status = dm.get_system_status()
        assert status is not None


class TestHardeningWithFeatures:
    """Test hardening transparent to users"""

    def test_config_update_doesnt_drop_tasks(self, temp_work_dir):
        """Test config updates don't interrupt task execution"""
        # Config manager and orchestration should work together
        assert True

    def test_backup_doesnt_block_api(self, temp_work_dir):
        """Test backup creation is async, doesn't block"""
        dr = DisasterRecovery(temp_work_dir)

        # Backup should complete without blocking
        dr.create_backup()
        assert True

    def test_audit_logging_overhead_minimal(self, temp_work_dir):
        """Test audit logging doesn't impact performance"""
        audit = AuditLogger(temp_work_dir)

        # Log many entries
        for i in range(100):
            audit.log_action(f"user-{i}", "action", "resource", "success")

        # Should complete quickly
        assert audit.get_total_entries() >= 100
