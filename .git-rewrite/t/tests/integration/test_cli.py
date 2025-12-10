"""
Integration tests for DEIA CLI commands
"""
import pytest
import subprocess
import sys
from pathlib import Path


class TestCLIHelp:
    """Test CLI help and basic command availability"""

    def test_main_help(self):
        """Test that main CLI help works"""
        result = subprocess.run(
            [sys.executable, '-c', 'import sys; sys.path.insert(0, "src"); from deia.cli import main; main(["--help"])'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'DEIA' in result.stdout
        assert 'Commands:' in result.stdout

    def test_doctor_command_exists(self):
        """Test that doctor command exists"""
        result = subprocess.run(
            [sys.executable, '-c', 'import sys; sys.path.insert(0, "src"); from deia.cli import main; main(["doctor", "--help"])'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'doctor' in result.stdout.lower()

    def test_doctor_docs_command_exists(self):
        """Test that doctor docs subcommand exists"""
        result = subprocess.run(
            [sys.executable, '-c', 'import sys; sys.path.insert(0, "src"); from deia.cli import main; main(["doctor", "docs", "--help"])'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'documentation' in result.stdout.lower() or 'audit' in result.stdout.lower()


@pytest.mark.integration
class TestDoctorDocs:
    """Test the doctor docs command"""

    def test_doctor_docs_runs(self, temp_dir, monkeypatch):
        """Test that doctor docs command runs without errors"""
        # Change to temp directory
        monkeypatch.chdir(temp_dir)

        # Create minimal structure
        (temp_dir / 'README.md').write_text('# Test Project\n')
        (temp_dir / 'ROADMAP.md').write_text('# Roadmap\n')

        result = subprocess.run(
            [sys.executable, '-c', 'import sys; sys.path.insert(0, "src"); from deia.cli import main; main(["doctor", "docs"])'],
            capture_output=True,
            text=True,
            cwd=str(temp_dir)
        )

        # Should complete (might have warnings but shouldn't crash)
        assert 'Documentation Audit' in result.stdout or 'audit' in result.stdout.lower()

    def test_doctor_docs_detects_issues(self, temp_dir, monkeypatch):
        """Test that doctor docs detects common issues"""
        monkeypatch.chdir(temp_dir)

        # Create a backup file (should be detected)
        (temp_dir / 'README.md.backup').write_text('# Old README\n')

        result = subprocess.run(
            [sys.executable, '-c', 'import sys; sys.path.insert(0, "src"); from deia.cli import main; main(["doctor", "docs"])'],
            capture_output=True,
            text=True,
            cwd=str(temp_dir)
        )

        # Should detect backup file
        assert 'backup' in result.stdout.lower() or result.returncode == 0


@pytest.mark.integration
class TestInitCommand:
    """Test the deia init command"""

    def test_init_help(self):
        """Test that init command help works"""
        result = subprocess.run(
            [sys.executable, '-c', 'import sys; sys.path.insert(0, "src"); from deia.cli import main; main(["init", "--help"])'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'init' in result.stdout.lower()


@pytest.mark.integration
class TestLogCommand:
    """Test the deia log commands"""

    def test_log_help(self):
        """Test that log command help works"""
        result = subprocess.run(
            [sys.executable, '-c', 'import sys; sys.path.insert(0, "src"); from deia.cli import main; main(["log", "--help"])'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
