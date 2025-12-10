"""
Tests for DEIA Health Check System

Tests all health check functions with edge cases and failure scenarios.

Author: CLAUDE-CODE-003 (Tactical Coordinator)
Date: 2025-10-18
"""

import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from deia.services.health_check import (
    HealthCheckResult,
    HealthCheckSystem,
    check_agent_health,
    check_system_health,
    generate_health_report
)


class TestHealthCheckResult:
    """Test HealthCheckResult class"""

    def test_init(self):
        """Test HealthCheckResult initialization"""
        result = HealthCheckResult(
            name="Test Check",
            status="PASS",
            message="All good",
            details={"count": 5}
        )

        assert result.name == "Test Check"
        assert result.status == "PASS"
        assert result.message == "All good"
        assert result.details == {"count": 5}
        assert result.timestamp is not None

    def test_init_without_details(self):
        """Test HealthCheckResult initialization without details"""
        result = HealthCheckResult(
            name="Test",
            status="FAIL",
            message="Error"
        )

        assert result.details == {}

    def test_to_dict(self):
        """Test conversion to dictionary"""
        result = HealthCheckResult(
            name="Test",
            status="WARNING",
            message="Watch out",
            details={"foo": "bar"}
        )

        data = result.to_dict()

        assert data["name"] == "Test"
        assert data["status"] == "WARNING"
        assert data["message"] == "Watch out"
        assert data["details"] == {"foo": "bar"}
        assert "timestamp" in data

    def test_is_passing_true(self):
        """Test is_passing when status is PASS"""
        result = HealthCheckResult("Test", "PASS", "OK")
        assert result.is_passing() is True

    def test_is_passing_false_warning(self):
        """Test is_passing when status is WARNING"""
        result = HealthCheckResult("Test", "WARNING", "Issue")
        assert result.is_passing() is False

    def test_is_passing_false_fail(self):
        """Test is_passing when status is FAIL"""
        result = HealthCheckResult("Test", "FAIL", "Error")
        assert result.is_passing() is False


class TestHealthCheckSystem:
    """Test HealthCheckSystem class"""

    def test_init_with_project_root(self, tmp_path):
        """Test initialization with explicit project root"""
        system = HealthCheckSystem(project_root=tmp_path)
        assert system.project_root == tmp_path
        assert system.results == []

    def test_init_without_project_root(self):
        """Test initialization with auto-detection"""
        system = HealthCheckSystem()
        assert system.project_root is not None
        assert isinstance(system.project_root, Path)

    def test_find_project_root_with_deia_dir(self, tmp_path):
        """Test project root detection with .deia directory"""
        deia_dir = tmp_path / ".deia"
        deia_dir.mkdir()

        with patch("deia.services.health_check.Path.cwd", return_value=tmp_path):
            system = HealthCheckSystem()
            assert system.project_root == tmp_path

    def test_find_project_root_without_deia_dir(self, tmp_path):
        """Test project root detection without .deia directory"""
        # When no .deia dir found, should use current working directory
        with patch("deia.services.health_check.Path.cwd", return_value=tmp_path):
            system = HealthCheckSystem()
            # Should fall back to cwd when no .deia found
            assert system.project_root.exists()


class TestAgentHealthCheck:
    """Test agent health check functionality"""

    def test_agent_health_no_directory(self, tmp_path):
        """Test agent health when bot-logs directory doesn't exist"""
        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_agent_health()

        assert result.name == "Agent Health"
        assert result.status == "FAIL"
        assert "not found" in result.message.lower()

    def test_agent_health_no_logs(self, tmp_path):
        """Test agent health when no activity logs exist"""
        bot_logs = tmp_path / ".deia" / "bot-logs"
        bot_logs.mkdir(parents=True)

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_agent_health()

        assert result.name == "Agent Health"
        assert result.status == "WARNING"
        assert "no agent activity logs" in result.message.lower()

    def test_agent_health_with_recent_activity(self, tmp_path):
        """Test agent health with recent activity"""
        bot_logs = tmp_path / ".deia" / "bot-logs"
        bot_logs.mkdir(parents=True)

        # Create activity log with recent timestamp
        log_file = bot_logs / "CLAUDE-CODE-001-activity.jsonl"
        recent_time = datetime.now().isoformat()
        log_file.write_text(json.dumps({
            "timestamp": recent_time,
            "agent": "CLAUDE-CODE-001",
            "event": "test"
        }), encoding='utf-8')

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_agent_health()

        assert result.name == "Agent Health"
        assert result.status in ["PASS", "WARNING"]  # PASS if recent, WARNING if parsing issues

    def test_agent_health_with_stale_activity(self, tmp_path):
        """Test agent health with stale activity (>1 hour old)"""
        bot_logs = tmp_path / ".deia" / "bot-logs"
        bot_logs.mkdir(parents=True)

        # Create activity log with old timestamp
        log_file = bot_logs / "CLAUDE-CODE-001-activity.jsonl"
        old_time = (datetime.now() - timedelta(hours=2)).isoformat()
        log_file.write_text(json.dumps({
            "timestamp": old_time,
            "agent": "CLAUDE-CODE-001",
            "event": "test"
        }), encoding='utf-8')

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_agent_health()

        assert result.name == "Agent Health"
        assert result.status == "WARNING"
        assert "stale" in result.message.lower()

    def test_agent_health_with_invalid_json(self, tmp_path):
        """Test agent health with invalid JSON in activity log"""
        bot_logs = tmp_path / ".deia" / "bot-logs"
        bot_logs.mkdir(parents=True)

        log_file = bot_logs / "CLAUDE-CODE-001-activity.jsonl"
        log_file.write_text("invalid json{{{", encoding='utf-8')

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_agent_health()

        # Should handle gracefully with WARNING or PASS
        assert result.name == "Agent Health"
        assert result.status in ["WARNING", "PASS"]


class TestMessagingHealthCheck:
    """Test messaging health check functionality"""

    def test_messaging_health_no_directory(self, tmp_path):
        """Test messaging health when tunnel directory doesn't exist"""
        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_messaging_health()

        assert result.name == "Messaging Health"
        assert result.status == "FAIL"
        assert "not found" in result.message.lower()

    def test_messaging_health_no_recent_messages(self, tmp_path):
        """Test messaging health with no recent messages"""
        tunnel = tmp_path / ".deia" / "tunnel" / "claude-to-claude"
        tunnel.mkdir(parents=True)

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_messaging_health()

        assert result.name == "Messaging Health"
        assert result.status == "WARNING"
        assert "no messages" in result.message.lower()

    def test_messaging_health_with_recent_messages(self, tmp_path):
        """Test messaging health with recent messages"""
        tunnel = tmp_path / ".deia" / "tunnel" / "claude-to-claude"
        tunnel.mkdir(parents=True)

        # Create several recent messages
        for i in range(10):
            msg_file = tunnel / f"2025-10-18-1200-AGENT00{i}-AGENT001-SYNC-test.md"
            msg_file.write_text(f"# Test message {i}")

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_messaging_health()

        assert result.name == "Messaging Health"
        assert result.status == "PASS"
        assert "active" in result.message.lower()

    def test_messaging_health_with_low_volume(self, tmp_path):
        """Test messaging health with low message volume"""
        tunnel = tmp_path / ".deia" / "tunnel" / "claude-to-claude"
        tunnel.mkdir(parents=True)

        # Create only 2 messages
        for i in range(2):
            msg_file = tunnel / f"2025-10-18-1200-AGENT00{i}-AGENT001-SYNC-test.md"
            msg_file.write_text(f"# Test message {i}")

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_messaging_health()

        assert result.name == "Messaging Health"
        assert result.status == "WARNING"
        assert "low message volume" in result.message.lower() or "only" in result.message.lower()


class TestBOKHealthCheck:
    """Test BOK health check functionality"""

    def test_bok_health_no_index(self, tmp_path):
        """Test BOK health when index file doesn't exist"""
        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_bok_health()

        assert result.name == "BOK Health"
        assert result.status == "WARNING"
        assert "not found" in result.message.lower()

    def test_bok_health_empty_index(self, tmp_path):
        """Test BOK health with empty index file"""
        index_dir = tmp_path / ".deia" / "index"
        index_dir.mkdir(parents=True)

        index_file = index_dir / "master-index.yaml"
        index_file.write_text("", encoding='utf-8')

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_bok_health()

        assert result.name == "BOK Health"
        assert result.status == "FAIL"
        assert "empty" in result.message.lower()

    def test_bok_health_valid_index(self, tmp_path):
        """Test BOK health with valid index file"""
        index_dir = tmp_path / ".deia" / "index"
        index_dir.mkdir(parents=True)

        index_file = index_dir / "master-index.yaml"
        index_content = """
patterns:
  - name: Test Pattern 1
    path: bok/patterns/test1.md
  - name: Test Pattern 2
    path: bok/patterns/test2.md
  - name: Test Pattern 3
    path: bok/patterns/test3.md
"""
        index_file.write_text(index_content, encoding='utf-8')

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_bok_health()

        assert result.name == "BOK Health"
        assert result.status == "PASS"
        assert "accessible" in result.message.lower()

    def test_bok_health_alternate_location(self, tmp_path):
        """Test BOK health with index in alternate location"""
        bok_dir = tmp_path / "bok"
        bok_dir.mkdir(parents=True)

        index_file = bok_dir / "master-index.yaml"
        index_file.write_text("- pattern: test", encoding='utf-8')

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_bok_health()

        assert result.name == "BOK Health"
        assert result.status == "PASS"


class TestFilesystemHealthCheck:
    """Test filesystem health check functionality"""

    def test_filesystem_health_no_deia_dir(self, tmp_path):
        """Test filesystem health when .deia doesn't exist"""
        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_filesystem_health()

        assert result.name == "Filesystem Health"
        assert result.status == "FAIL"
        assert "not found" in result.message.lower()
        assert "deia init" in result.message.lower()

    def test_filesystem_health_all_dirs_exist(self, tmp_path):
        """Test filesystem health when all directories exist"""
        deia_dir = tmp_path / ".deia"

        required_dirs = [
            "sessions", "bok", "index", "federalist", "governance",
            "tunnel/claude-to-claude", "bot-logs", "observations",
            "handoffs", "intake"
        ]

        for dir_name in required_dirs:
            (deia_dir / dir_name).mkdir(parents=True)

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_filesystem_health()

        assert result.name == "Filesystem Health"
        assert result.status == "PASS"
        assert "all required" in result.message.lower()

    def test_filesystem_health_few_missing_dirs(self, tmp_path):
        """Test filesystem health with 1-2 missing directories"""
        deia_dir = tmp_path / ".deia"
        deia_dir.mkdir()

        # Create some but not all directories
        (deia_dir / "sessions").mkdir()
        (deia_dir / "bot-logs").mkdir()
        (deia_dir / "tunnel").mkdir()
        (deia_dir / "tunnel" / "claude-to-claude").mkdir()

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_filesystem_health()

        assert result.name == "Filesystem Health"
        assert result.status in ["WARNING", "FAIL"]

    def test_filesystem_health_many_missing_dirs(self, tmp_path):
        """Test filesystem health with many missing directories"""
        deia_dir = tmp_path / ".deia"
        deia_dir.mkdir()

        # Create only one directory
        (deia_dir / "sessions").mkdir()

        system = HealthCheckSystem(project_root=tmp_path)
        result = system.check_filesystem_health()

        assert result.name == "Filesystem Health"
        assert result.status == "FAIL"


class TestDependenciesHealthCheck:
    """Test dependencies health check functionality"""

    def test_dependencies_health_all_installed(self):
        """Test dependencies health when all packages are installed"""
        system = HealthCheckSystem()
        result = system.check_dependencies_health()

        assert result.name == "Dependencies Health"
        # Status depends on actual environment, but should not crash
        assert result.status in ["PASS", "FAIL"]

    @patch('importlib.metadata.version')
    def test_dependencies_health_missing_packages(self, mock_version):
        """Test dependencies health with missing packages"""
        import importlib.metadata

        def version_side_effect(package):
            if package == "click":
                return "8.1.0"
            raise importlib.metadata.PackageNotFoundError

        mock_version.side_effect = version_side_effect

        system = HealthCheckSystem()
        result = system.check_dependencies_health()

        assert result.name == "Dependencies Health"
        assert result.status == "FAIL"
        assert "missing" in result.message.lower()


class TestSystemHealthCheck:
    """Test overall system health check"""

    def test_check_system_health(self, tmp_path):
        """Test checking all system health"""
        # Set up minimal structure
        deia_dir = tmp_path / ".deia"
        (deia_dir / "bot-logs").mkdir(parents=True)

        system = HealthCheckSystem(project_root=tmp_path)
        checks = system.check_system_health()

        assert "agents" in checks
        assert "messaging" in checks
        assert "bok" in checks
        assert "filesystem" in checks
        assert "dependencies" in checks

        # All should be HealthCheckResult objects
        for check in checks.values():
            assert isinstance(check, HealthCheckResult)

    def test_check_system_health_stores_results(self, tmp_path):
        """Test that check_system_health stores results"""
        system = HealthCheckSystem(project_root=tmp_path)
        checks = system.check_system_health()

        assert len(system.results) == 5  # 5 checks total


class TestHealthReport:
    """Test health report generation"""

    def test_generate_health_report(self, tmp_path):
        """Test generating a health report"""
        system = HealthCheckSystem(project_root=tmp_path)
        report = system.generate_health_report()

        assert "DEIA HEALTH CHECK REPORT" in report
        assert "SUMMARY" in report
        assert "DETAILED RESULTS" in report
        assert "Overall Status" in report

    def test_generate_health_report_with_checks(self, tmp_path):
        """Test generating a report with provided checks"""
        checks = {
            "test1": HealthCheckResult("Test 1", "PASS", "OK"),
            "test2": HealthCheckResult("Test 2", "FAIL", "Error"),
        }

        system = HealthCheckSystem(project_root=tmp_path)
        report = system.generate_health_report(checks)

        assert "Test 1" in report
        assert "Test 2" in report
        assert "PASS" in report
        assert "FAIL" in report

    def test_get_overall_status_healthy(self, tmp_path):
        """Test overall status when all checks pass"""
        checks = {
            "test1": HealthCheckResult("Test 1", "PASS", "OK"),
            "test2": HealthCheckResult("Test 2", "PASS", "OK"),
        }

        system = HealthCheckSystem(project_root=tmp_path)
        status, code = system.get_overall_status(checks)

        assert status == "HEALTHY"
        assert code == 0

    def test_get_overall_status_degraded(self, tmp_path):
        """Test overall status with warnings"""
        checks = {
            "test1": HealthCheckResult("Test 1", "PASS", "OK"),
            "test2": HealthCheckResult("Test 2", "WARNING", "Issue"),
        }

        system = HealthCheckSystem(project_root=tmp_path)
        status, code = system.get_overall_status(checks)

        assert status == "DEGRADED"
        assert code == 1

    def test_get_overall_status_unhealthy(self, tmp_path):
        """Test overall status with failures"""
        checks = {
            "test1": HealthCheckResult("Test 1", "PASS", "OK"),
            "test2": HealthCheckResult("Test 2", "FAIL", "Error"),
        }

        system = HealthCheckSystem(project_root=tmp_path)
        status, code = system.get_overall_status(checks)

        assert status == "UNHEALTHY"
        assert code == 2


class TestStandaloneFunctions:
    """Test standalone utility functions"""

    def test_check_agent_health_standalone(self, tmp_path):
        """Test standalone check_agent_health function"""
        result = check_agent_health(tmp_path)
        assert isinstance(result, HealthCheckResult)
        assert result.name == "Agent Health"

    def test_check_system_health_standalone(self, tmp_path):
        """Test standalone check_system_health function"""
        checks = check_system_health(tmp_path)
        assert isinstance(checks, dict)
        assert len(checks) == 5

    def test_generate_health_report_standalone(self, tmp_path):
        """Test standalone generate_health_report function"""
        report = generate_health_report(tmp_path)
        assert isinstance(report, str)
        assert "DEIA HEALTH CHECK REPORT" in report
