#!/usr/bin/env python3
"""Service Integration Testing Suite.

End-to-end testing of:
- Coordinator (scope enforcement)
- File Mover (file operations)
- Provenance Tracker (version tracking)
- Immune Triage (anomaly detection)
"""

import json
import tempfile
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.coordinator import ScopeEnforcer
from deia.services.file_mover import FileMoverService
from deia.services.provenance_tracker import ProvenanceTracker
from deia.services.immune_triage import ImmuneTriageAgent


class TestServiceIntegration:
    """Integration tests for all services."""

    @pytest.fixture
    def project(self):
        """Create temporary project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)

            # Create structure
            (project_root / ".deia" / "telemetry").mkdir(parents=True, exist_ok=True)
            (project_root / ".deia" / "logs").mkdir(parents=True, exist_ok=True)
            (project_root / ".deia" / "hive" / "logs").mkdir(parents=True, exist_ok=True)
            (project_root / ".deia" / "provenance").mkdir(parents=True, exist_ok=True)
            (project_root / ".deia" / "reports").mkdir(parents=True, exist_ok=True)
            (project_root / "source").mkdir(parents=True, exist_ok=True)
            (project_root / "target").mkdir(parents=True, exist_ok=True)

            # Create bot registry
            registry = {
                "BOT-001": {"status": "running", "scope": [".deia/", "docs/"]},
                "BOT-002": {"status": "running", "scope": ["src/"]}
            }
            registry_file = project_root / ".deia" / "bot-registry.json"
            with open(registry_file, 'w') as f:
                json.dump(registry, f)

            # Create file mover rules
            rules = {
                "rules": [{
                    "name": "move_logs",
                    "enabled": True,
                    "watch_path": str(project_root / "source"),
                    "pattern": "*.log",
                    "action": "move",
                    "target_path": str(project_root / "target"),
                    "recursive": False
                }]
            }
            rules_file = project_root / "rules.json"
            with open(rules_file, 'w') as f:
                json.dump(rules, f)

            yield {
                "root": project_root,
                "registry": registry_file,
                "rules": rules_file
            }

    def test_coordinator_freeze_flow(self, project):
        """Test coordinator detecting and freezing scope violations."""
        enforcer = ScopeEnforcer(project["root"])

        # Simulate scope violation
        event = {
            "ts": "2025-10-25T23:55:00Z",
            "bot_id": "BOT-001",
            "resolved_path": "/external/repo/file.txt",
            "allowed_paths": [".deia/", "docs/"],
            "cwd": "/deiasolutions",
            "op": "write",
            "within_scope": False,
            "decision": "deny",
            "reason": "outside allowed paths"
        }

        enforcer.process_path_event(event)

        # Verify bot frozen
        with open(project["registry"]) as f:
            registry = json.load(f)

        assert registry["BOT-001"]["status"] == "STANDBY"
        assert "frozen_at" in registry["BOT-001"]

    def test_file_mover_integration(self, project):
        """Test file mover with coordinator."""
        # Create test file
        source_file = project["root"] / "source" / "test.log"
        source_file.write_text("test log")

        # Run file mover
        mover = FileMoverService(project["rules"], project["root"])
        mover.run_once()

        # Verify file moved
        assert not source_file.exists()
        assert (project["root"] / "target" / "test.log").exists()

    def test_provenance_version_tracking(self, project):
        """Test provenance tracking with multiple versions."""
        tracker = ProvenanceTracker(project["root"])

        # Track document versions
        tracker.track_document("spec-001", "specifications", "1.0.0", "initial")
        tracker.track_document("spec-001", "specifications", "1.1.0", "update")
        tracker.track_document("spec-001", "specifications", "1.3.0", "update")  # Gap

        # Get lineage
        lineage = tracker.get_lineage("spec-001")
        assert lineage == ["1.0.0", "1.1.0", "1.3.0"]

        # Detect gaps
        gaps = tracker.detect_all_gaps()
        assert "spec-001" in gaps

    def test_immune_triage_with_signals(self, project):
        """Test immune triage processing multiple signals."""
        agent = ImmuneTriageAgent(project["root"])

        signals = [
            {"type": "scope_violation", "data": {"bot_id": "BOT-001", "path": "/ext"}},
            {"type": "memory", "data": {"usage_mb": 1800}},
            {"type": "error_rate", "data": {"rate": 0.08}}
        ]

        result = agent.process_signals(signals)

        assert result["total_anomalies"] == 3
        assert result["critical_count"] == 1
        assert result["high_count"] >= 1

    def test_integrated_workflow(self, project):
        """Test complete workflow: coordination, file ops, tracking, triage."""
        # 1. Coordinator detects scope violation
        enforcer = ScopeEnforcer(project["root"])
        scope_event = {
            "ts": "2025-10-25T23:56:00Z",
            "bot_id": "BOT-001",
            "resolved_path": "/external/file.txt",
            "allowed_paths": [".deia/"],
            "cwd": "/deia",
            "op": "write",
            "within_scope": False,
            "decision": "deny",
            "reason": "out of scope"
        }
        enforcer.process_path_event(scope_event)

        # 2. File mover processes safe operations
        (project["root"] / "source" / "safe.log").write_text("safe")
        mover = FileMoverService(project["rules"], project["root"])
        mover.run_once()

        # 3. Provenance tracks document versions
        tracker = ProvenanceTracker(project["root"])
        tracker.track_document("doc-001", "logs", "1.0.0")
        tracker.track_document("doc-001", "logs", "1.1.0")

        # 4. Immune triage alerts on violations
        agent = ImmuneTriageAgent(project["root"])
        signals = [
            {"type": "scope_violation", "data": {"bot_id": "BOT-001", "path": "/ext"}},
            {"type": "memory", "data": {"usage_mb": 1500}}
        ]
        triage = agent.process_signals(signals)

        # Verify all services worked together
        assert (project["root"] / "target" / "safe.log").exists()
        assert tracker.get_lineage("doc-001") == ["1.0.0", "1.1.0"]
        assert triage["total_anomalies"] == 2

    def test_service_error_handling(self, project):
        """Test services handle errors gracefully."""
        # Test with non-existent registry
        bad_project = project["root"] / "nonexistent"
        enforcer = ScopeEnforcer(bad_project)

        # Should handle gracefully
        result = enforcer.freeze_bot("NONEXISTENT-BOT")
        assert result is False

    def test_concurrent_operations(self, project):
        """Test services working concurrently."""
        # File mover
        (project["root"] / "source" / "file1.log").write_text("1")
        (project["root"] / "source" / "file2.log").write_text("2")
        (project["root"] / "source" / "file3.log").write_text("3")

        mover = FileMoverService(project["rules"], project["root"])

        # Provenance
        tracker = ProvenanceTracker(project["root"])
        tracker.track_document("d1", "src", "1.0.0")
        tracker.track_document("d2", "src", "1.0.0")

        # Triage
        agent = ImmuneTriageAgent(project["root"])

        # Run concurrently (simulated)
        mover.run_once()
        for doc in ["d1", "d2"]:
            tracker.track_document(doc, "src", "1.1.0")

        result = agent.process_signals([
            {"type": "memory", "data": {"usage_mb": 800}}
        ])

        # Verify all worked
        assert len(list((project["root"] / "target").glob("*.log"))) == 3
        assert tracker.get_document_info("d1")["version_count"] == 2
        assert result["total_anomalies"] == 0  # No critical issues


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
