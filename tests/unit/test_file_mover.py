#!/usr/bin/env python3
"""Tests for File Mover Service."""

import json
import tempfile
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.file_mover import FileMoverService, FileRule


class TestFileRule:
    """Test suite for FileRule."""

    def test_rule_initialization(self):
        """Test rule initialization."""
        rule_dict = {
            "name": "test_rule",
            "pattern": "*.log",
            "action": "move",
            "target_path": "/logs/archive",
            "enabled": True
        }
        rule = FileRule(rule_dict)
        assert rule.name == "test_rule"
        assert rule.pattern == "*.log"
        assert rule.action == "move"

    def test_rule_pattern_matching(self):
        """Test pattern matching."""
        rule = FileRule({"name": "test", "pattern": "*.log", "action": "move", "target_path": "/tmp"})

        assert rule.matches(Path("test.log")) is True
        assert rule.matches(Path("debug.log")) is True
        assert rule.matches(Path("test.txt")) is False

    def test_rule_condition_size(self):
        """Test size condition evaluation."""
        rule = FileRule({
            "name": "test",
            "pattern": "*",
            "action": "delete",
            "condition": "size > 1000"
        })

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files of different sizes
            small_file = Path(tmpdir) / "small.txt"
            small_file.write_text("x" * 500)

            large_file = Path(tmpdir) / "large.txt"
            large_file.write_text("x" * 2000)

            assert rule.apply_condition(small_file) is False
            assert rule.apply_condition(large_file) is True

    def test_rule_disabled(self):
        """Test disabled rule."""
        rule = FileRule({
            "name": "disabled",
            "pattern": "*.log",
            "enabled": False,
            "action": "move",
            "target_path": "/tmp"
        })
        assert rule.enabled is False


class TestFileMoverService:
    """Test suite for FileMoverService."""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)

            # Create directories
            (project_root / ".deia" / "logs").mkdir(parents=True, exist_ok=True)
            (project_root / "source").mkdir(parents=True, exist_ok=True)
            (project_root / "target").mkdir(parents=True, exist_ok=True)

            yield project_root

    @pytest.fixture
    def rules_file(self, temp_project):
        """Create rules file."""
        rules = {
            "rules": [
                {
                    "name": "move_logs",
                    "enabled": True,
                    "watch_path": str(temp_project / "source"),
                    "pattern": "*.log",
                    "action": "move",
                    "target_path": str(temp_project / "target"),
                    "recursive": False
                }
            ]
        }

        rules_file = temp_project / "rules.json"
        with open(rules_file, 'w') as f:
            json.dump(rules, f)

        return rules_file

    def test_service_initialization(self, temp_project, rules_file):
        """Test service initialization."""
        service = FileMoverService(rules_file, temp_project)
        assert service.project_root == temp_project
        assert len(service.rules) == 1
        assert service.rules[0].name == "move_logs"

    def test_move_operation(self, temp_project, rules_file):
        """Test file move operation."""
        service = FileMoverService(rules_file, temp_project)

        # Create test file
        source_file = temp_project / "source" / "test.log"
        source_file.write_text("test log content")

        # Apply rule
        service.run_once()

        # Verify file was moved
        assert not source_file.exists()
        target_file = temp_project / "target" / "test.log"
        assert target_file.exists()
        assert target_file.read_text() == "test log content"

    def test_copy_operation(self, temp_project):
        """Test file copy operation."""
        rules_file = temp_project / "rules.json"
        rules = {
            "rules": [
                {
                    "name": "copy_docs",
                    "enabled": True,
                    "watch_path": str(temp_project / "source"),
                    "pattern": "*.md",
                    "action": "copy",
                    "target_path": str(temp_project / "target"),
                    "recursive": False
                }
            ]
        }

        with open(rules_file, 'w') as f:
            json.dump(rules, f)

        service = FileMoverService(rules_file, temp_project)

        # Create test file
        source_file = temp_project / "source" / "readme.md"
        source_file.write_text("# README")

        # Apply rule
        service.run_once()

        # Verify file was copied (original still exists)
        assert source_file.exists()
        target_file = temp_project / "target" / "readme.md"
        assert target_file.exists()

    def test_delete_operation(self, temp_project):
        """Test file delete operation."""
        rules_file = temp_project / "rules.json"
        rules = {
            "rules": [
                {
                    "name": "delete_tmp",
                    "enabled": True,
                    "watch_path": str(temp_project / "source"),
                    "pattern": "*.tmp",
                    "action": "delete",
                    "recursive": False
                }
            ]
        }

        with open(rules_file, 'w') as f:
            json.dump(rules, f)

        service = FileMoverService(rules_file, temp_project)

        # Create test file
        tmp_file = temp_project / "source" / "temp.tmp"
        tmp_file.write_text("temporary")

        # Apply rule
        service.run_once()

        # Verify file was deleted
        assert not tmp_file.exists()

    def test_multiple_files(self, temp_project, rules_file):
        """Test processing multiple files."""
        service = FileMoverService(rules_file, temp_project)

        # Create multiple test files
        for i in range(5):
            f = temp_project / "source" / f"test{i}.log"
            f.write_text(f"log content {i}")

        # Apply rule
        service.run_once()

        # Verify all files were moved
        assert len(list((temp_project / "source").glob("*.log"))) == 0
        assert len(list((temp_project / "target").glob("*.log"))) == 5

    def test_operation_logging(self, temp_project, rules_file):
        """Test operation logging."""
        service = FileMoverService(rules_file, temp_project)

        source_file = temp_project / "source" / "test.log"
        source_file.write_text("test")

        service.run_once()

        # Check operations log
        assert service.operations_log.exists()
        with open(service.operations_log, 'r') as f:
            operations = [json.loads(line) for line in f if line.strip()]

        assert len(operations) > 0
        assert operations[0]["operation"] == "move"
        assert operations[0]["success"] is True

    def test_disabled_rule(self, temp_project):
        """Test that disabled rules are not applied."""
        rules_file = temp_project / "rules.json"
        rules = {
            "rules": [
                {
                    "name": "disabled_rule",
                    "enabled": False,
                    "watch_path": str(temp_project / "source"),
                    "pattern": "*.log",
                    "action": "move",
                    "target_path": str(temp_project / "target")
                }
            ]
        }

        with open(rules_file, 'w') as f:
            json.dump(rules, f)

        service = FileMoverService(rules_file, temp_project)

        source_file = temp_project / "source" / "test.log"
        source_file.write_text("test")

        service.run_once()

        # Verify file was NOT moved (rule disabled)
        assert source_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
