#!/usr/bin/env python3
"""
Tests for Coordinator MVP scope enforcement daemon.
"""

import json
import tempfile
import pytest
from pathlib import Path
from datetime import datetime

# Mock import path for testing
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.coordinator import ScopeEnforcer


class TestScopeEnforcer:
    """Test suite for ScopeEnforcer."""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project structure for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)

            # Create required directories
            (project_root / ".deia" / "telemetry").mkdir(parents=True, exist_ok=True)
            (project_root / ".deia" / "hive" / "logs").mkdir(parents=True, exist_ok=True)

            # Create bot registry
            registry = {
                "BOT-001": {
                    "status": "running",
                    "scope": [".deia/", "docs/"],
                    "instance_id": "inst-001"
                },
                "BOT-002": {
                    "status": "running",
                    "scope": ["src/"],
                    "instance_id": "inst-002"
                }
            }

            registry_file = project_root / ".deia" / "bot-registry.json"
            with open(registry_file, 'w') as f:
                json.dump(registry, f)

            yield project_root

    def test_coordinator_initialization(self, temp_project):
        """Test coordinator initializes correctly."""
        enforcer = ScopeEnforcer(temp_project)
        assert enforcer.project_root == temp_project
        assert enforcer.running is True
        assert enforcer.violating_bots == {}

    def test_process_valid_path_event(self, temp_project):
        """Test processing a valid (in-scope) path event."""
        enforcer = ScopeEnforcer(temp_project)

        event = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "bot_id": "BOT-001",
            "instance_id": "inst-001",
            "cwd": "/home/user/deiasolutions",
            "op": "write",
            "path": ".deia/test.txt",
            "resolved_path": "/home/user/deiasolutions/.deia/test.txt",
            "within_scope": True,
            "allowed_paths": [".deia/", "docs/"],
            "decision": "allow",
            "reason": "within allowed paths"
        }

        # Should not log any violations
        enforcer.process_path_event(event)
        assert "BOT-001" not in enforcer.violating_bots

    def test_process_invalid_path_event(self, temp_project):
        """Test processing an invalid (out-of-scope) path event."""
        enforcer = ScopeEnforcer(temp_project)

        event = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "bot_id": "BOT-001",
            "instance_id": "inst-001",
            "cwd": "/home/user/deiasolutions",
            "op": "write",
            "path": "../external-repo/file.txt",
            "resolved_path": "/home/user/external-repo/file.txt",
            "within_scope": False,
            "allowed_paths": [".deia/", "docs/"],
            "decision": "deny",
            "reason": "outside allowed paths"
        }

        # Should log violation and freeze bot
        enforcer.process_path_event(event)
        assert "BOT-001" in enforcer.violating_bots
        assert enforcer.violating_bots["BOT-001"] == 1

    def test_freeze_bot_success(self, temp_project):
        """Test freezing a bot successfully."""
        enforcer = ScopeEnforcer(temp_project)

        # Verify bot starts as running
        registry_file = temp_project / ".deia" / "bot-registry.json"
        with open(registry_file, 'r') as f:
            registry = json.load(f)
        assert registry["BOT-001"]["status"] == "running"

        # Freeze bot
        result = enforcer.freeze_bot("BOT-001")
        assert result is True

        # Verify bot is frozen
        with open(registry_file, 'r') as f:
            registry = json.load(f)
        assert registry["BOT-001"]["status"] == "STANDBY"
        assert "frozen_at" in registry["BOT-001"]
        assert registry["BOT-001"]["freeze_reason"] == "scope_drift_detected"

    def test_freeze_nonexistent_bot(self, temp_project):
        """Test attempting to freeze a bot that doesn't exist."""
        enforcer = ScopeEnforcer(temp_project)

        result = enforcer.freeze_bot("BOT-999")
        assert result is False

    def test_log_violation(self, temp_project):
        """Test logging a scope violation."""
        enforcer = ScopeEnforcer(temp_project)

        event = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "bot_id": "BOT-001",
            "resolved_path": "/home/user/external/file.txt",
            "allowed_paths": [".deia/", "docs/"],
            "cwd": "/home/user/deiasolutions",
            "op": "write"
        }

        enforcer.log_violation("BOT-001", event, "attempt to escape sandbox")

        # Verify violation logged
        violations_log = temp_project / ".deia" / "hive" / "logs" / "scope-violations.log"
        assert violations_log.exists()

        with open(violations_log, 'r') as f:
            violations = [json.loads(line) for line in f if line.strip()]

        assert len(violations) == 1
        assert violations[0]["bot_id"] == "BOT-001"
        assert violations[0]["violation_type"] == "scope_drift"

        # Verify hive log entry
        hive_log = temp_project / ".deia" / "hive-log.jsonl"
        with open(hive_log, 'r') as f:
            entries = [json.loads(line) for line in f if line.strip()]

        assert len(entries) == 1
        assert entries[0]["type"] == "scope_drift_detected"
        assert entries[0]["severity"] == "critical"

    def test_generate_summary_clean_run(self, temp_project):
        """Test summary generation for clean run."""
        enforcer = ScopeEnforcer(temp_project)

        summary = enforcer.generate_summary()
        assert summary["clean_run"] is True
        assert summary["total_violations"] == 0
        assert summary["bots_frozen"] == []

    def test_generate_summary_with_violations(self, temp_project):
        """Test summary generation with violations."""
        enforcer = ScopeEnforcer(temp_project)

        # Simulate violations
        event = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "bot_id": "BOT-001",
            "resolved_path": "/external/file.txt",
            "allowed_paths": [".deia/"],
            "cwd": "/home/user/deiasolutions",
            "op": "write"
        }

        enforcer.log_violation("BOT-001", event, "scope escape attempt")
        enforcer.violating_bots["BOT-001"] = 1

        summary = enforcer.generate_summary()
        assert summary["clean_run"] is False
        assert summary["total_violations"] == 1
        assert "BOT-001" in summary["bots_frozen"]

    def test_multiple_violations_same_bot(self, temp_project):
        """Test handling multiple violations from same bot."""
        enforcer = ScopeEnforcer(temp_project)

        event1 = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "bot_id": "BOT-001",
            "resolved_path": "/external/file1.txt",
            "allowed_paths": [".deia/"],
            "cwd": "/home/user/deiasolutions",
            "op": "write"
        }

        event2 = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "bot_id": "BOT-001",
            "resolved_path": "/external/file2.txt",
            "allowed_paths": [".deia/"],
            "cwd": "/home/user/deiasolutions",
            "op": "move"
        }

        enforcer.process_path_event(event1)
        enforcer.process_path_event(event2)

        assert enforcer.violating_bots["BOT-001"] == 2

    def test_multiple_violations_different_bots(self, temp_project):
        """Test handling violations from different bots."""
        enforcer = ScopeEnforcer(temp_project)

        event1 = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "bot_id": "BOT-001",
            "resolved_path": "/external/file.txt",
            "allowed_paths": [".deia/"],
            "cwd": "/home/user/deiasolutions",
            "op": "write",
            "within_scope": False,
            "decision": "deny",
            "reason": "outside scope"
        }

        event2 = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "bot_id": "BOT-002",
            "resolved_path": "/external/file.txt",
            "allowed_paths": ["src/"],
            "cwd": "/home/user/deiasolutions",
            "op": "write",
            "within_scope": False,
            "decision": "deny",
            "reason": "outside scope"
        }

        enforcer.process_path_event(event1)
        enforcer.process_path_event(event2)

        assert enforcer.violating_bots["BOT-001"] == 1
        assert enforcer.violating_bots["BOT-002"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
