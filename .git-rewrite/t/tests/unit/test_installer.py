"""
Tests for the DEIA installer module
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from deia.installer import DeiaInstaller, install_global, init_project


class TestDeiaInstallerInit:
    """Test DeiaInstaller initialization"""

    def test_installer_init(self, tmp_path):
        """Test installer initialization sets up paths correctly"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            assert installer.home == tmp_path
            assert installer.global_deia == tmp_path / ".deia-global"


class TestInstallGlobal:
    """Test global DEIA installation"""

    def test_install_global_creates_directory(self, tmp_path):
        """Test that install_global creates the global directory"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            result = installer.install_global(username="testuser")

            assert result is True
            assert (tmp_path / ".deia-global").exists()

    def test_install_global_creates_config(self, tmp_path):
        """Test that install_global creates config.json"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser", auto_log=True)

            config_file = tmp_path / ".deia-global" / "config.json"
            assert config_file.exists()

            config = json.loads(config_file.read_text())
            assert config["version"] == "1.0"
            assert config["user"] == "testuser"
            assert config["auto_log_default"] is True
            assert config["projects"] == []

    def test_install_global_uses_env_username_if_none_provided(self, tmp_path):
        """Test that install_global uses environment username if not provided"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            with patch.dict("os.environ", {"USER": "envuser"}):
                installer = DeiaInstaller()
                installer.install_global()

                config_file = tmp_path / ".deia-global" / "config.json"
                config = json.loads(config_file.read_text())
                assert config["user"] == "envuser"

    def test_install_global_creates_preferences(self, tmp_path):
        """Test that install_global creates preferences.md"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            prefs_file = tmp_path / ".deia-global" / "preferences.md"
            assert prefs_file.exists()
            assert "Global DEIA Preferences" in prefs_file.read_text()

    def test_install_global_creates_integration_guide(self, tmp_path):
        """Test that install_global creates integration guide"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            integration_file = tmp_path / ".deia-global" / "CLAUDE_CODE_INTEGRATION.md"
            assert integration_file.exists()
            assert "How DEIA Integrates with Claude Code" in integration_file.read_text()

    def test_install_global_skips_existing_files(self, tmp_path):
        """Test that install_global doesn't overwrite existing files"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()

            # First installation
            installer.install_global(username="testuser")
            config_file = tmp_path / ".deia-global" / "config.json"
            original_content = config_file.read_text()

            # Second installation
            installer.install_global(username="differentuser")
            new_content = config_file.read_text()

            # Content should be unchanged
            assert original_content == new_content

    def test_install_global_auto_log_false(self, tmp_path):
        """Test install_global with auto_log=False"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser", auto_log=False)

            config_file = tmp_path / ".deia-global" / "config.json"
            config = json.loads(config_file.read_text())
            assert config["auto_log_default"] is False


class TestInitProject:
    """Test project-level DEIA initialization"""

    def test_init_project_fails_without_global_install(self, tmp_path):
        """Test that init_project fails if global DEIA not installed"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            result = installer.init_project(project_path=project_dir)
            assert result is False

    def test_init_project_creates_deia_directory(self, tmp_path):
        """Test that init_project creates .deia directory"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir, project_name="testproj")
            assert (project_dir / ".deia").exists()

    def test_init_project_creates_all_subdirectories(self, tmp_path):
        """Test that init_project creates all required subdirectories"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir)

            subdirs = [
                "sessions", "bok", "index", "federalist", "governance",
                "tunnel", "bot-logs", "observations", "handoffs", "intake"
            ]

            for subdir in subdirs:
                assert (project_dir / ".deia" / subdir).exists()

    def test_init_project_creates_config(self, tmp_path):
        """Test that init_project creates .deia/config.json"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir, project_name="testproj", auto_log=True)

            config_file = project_dir / ".deia" / "config.json"
            assert config_file.exists()

            config = json.loads(config_file.read_text())
            assert config["mode"] == "end-user"
            assert config["project"] == "testproj"
            assert config["user"] == "testuser"
            assert config["auto_log"] is True

    def test_init_project_creates_claude_directory(self, tmp_path):
        """Test that init_project creates .claude directory"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir)
            assert (project_dir / ".claude").exists()

    def test_init_project_creates_instructions(self, tmp_path):
        """Test that init_project creates .claude/INSTRUCTIONS.md"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir, project_name="testproj")

            instructions_file = project_dir / ".claude" / "INSTRUCTIONS.md"
            assert instructions_file.exists()
            assert "DEIA Auto-Logging Instructions" in instructions_file.read_text()
            assert "testproj" in instructions_file.read_text()

    def test_init_project_creates_log_command(self, tmp_path):
        """Test that init_project creates /log slash command"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir)

            log_command = project_dir / ".claude" / "commands" / "log.md"
            assert log_command.exists()
            assert "Log This Conversation" in log_command.read_text()

    def test_init_project_creates_preferences(self, tmp_path):
        """Test that init_project creates .claude/preferences/deia.md"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir)

            preferences_file = project_dir / ".claude" / "preferences" / "deia.md"
            assert preferences_file.exists()
            assert "DEIA Auto-Logging System" in preferences_file.read_text(encoding='utf-8')

    def test_init_project_creates_project_resume(self, tmp_path):
        """Test that init_project creates project_resume.md"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir, project_name="testproj")

            resume_file = project_dir / "project_resume.md"
            assert resume_file.exists()
            assert "testproj - Project Resume" in resume_file.read_text()

    def test_init_project_doesnt_overwrite_existing_resume(self, tmp_path):
        """Test that init_project doesn't overwrite existing project_resume.md"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            # Create existing resume
            resume_file = project_dir / "project_resume.md"
            resume_file.write_text("EXISTING CONTENT")

            installer.init_project(project_path=project_dir)

            # Should not be overwritten
            assert resume_file.read_text() == "EXISTING CONTENT"

    def test_init_project_registers_with_global_config(self, tmp_path):
        """Test that init_project registers project in global config"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir, project_name="testproj", auto_log=True)

            global_config_file = tmp_path / ".deia-global" / "config.json"
            global_config = json.loads(global_config_file.read_text())

            assert "projects" in global_config
            assert len(global_config["projects"]) == 1
            assert global_config["projects"][0]["name"] == "testproj"
            assert global_config["projects"][0]["path"] == str(project_dir)
            assert global_config["projects"][0]["auto_log"] is True

    def test_init_project_doesnt_duplicate_registration(self, tmp_path):
        """Test that init_project doesn't duplicate project registration"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            # Initialize twice
            installer.init_project(project_path=project_dir, project_name="testproj")
            installer.init_project(project_path=project_dir, project_name="testproj")

            global_config_file = tmp_path / ".deia-global" / "config.json"
            global_config = json.loads(global_config_file.read_text())

            # Should only have one entry
            assert len(global_config["projects"]) == 1

    def test_init_project_uses_current_directory_by_default(self, tmp_path):
        """Test that init_project uses current directory if no path provided"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            with patch("deia.installer.Path.cwd", return_value=tmp_path / "current"):
                installer = DeiaInstaller()
                installer.install_global(username="testuser")

                current_dir = tmp_path / "current"
                current_dir.mkdir()

                installer.init_project()
                assert (current_dir / ".deia").exists()

    def test_init_project_uses_directory_name_as_project_name(self, tmp_path):
        """Test that init_project uses directory name if no project name provided"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "my_awesome_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir)

            config_file = project_dir / ".deia" / "config.json"
            config = json.loads(config_file.read_text())
            assert config["project"] == "my_awesome_project"

    def test_init_project_inherits_auto_log_from_global(self, tmp_path):
        """Test that init_project inherits auto_log from global config"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser", auto_log=False)

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            installer.init_project(project_path=project_dir)

            config_file = project_dir / ".deia" / "config.json"
            config = json.loads(config_file.read_text())
            assert config["auto_log"] is False


class TestModuleFunctions:
    """Test module-level convenience functions"""

    def test_install_global_function(self, tmp_path):
        """Test install_global() convenience function"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            result = install_global(username="testuser", auto_log=True)
            assert result is True
            assert (tmp_path / ".deia-global").exists()

    def test_init_project_function(self, tmp_path):
        """Test init_project() convenience function"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            # Need global install first
            install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            result = init_project(project_path=project_dir, project_name="testproj")
            assert result is True
            assert (project_dir / ".deia").exists()


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_init_project_resolves_relative_paths(self, tmp_path):
        """Test that init_project resolves relative paths correctly"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            installer = DeiaInstaller()
            installer.install_global(username="testuser")

            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            # Pass relative-like path
            relative_path = Path("test_project")
            with patch("pathlib.Path.resolve", return_value=project_dir):
                installer.init_project(project_path=relative_path)
                assert (project_dir / ".deia").exists()

    def test_install_global_with_windows_username_env(self, tmp_path):
        """Test install_global uses USERNAME env var (Windows)"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            with patch.dict("os.environ", {"USERNAME": "windowsuser"}, clear=True):
                installer = DeiaInstaller()
                installer.install_global()

                config_file = tmp_path / ".deia-global" / "config.json"
                config = json.loads(config_file.read_text())
                assert config["user"] == "windowsuser"

    def test_install_global_fallback_username(self, tmp_path):
        """Test install_global uses 'user' as fallback username"""
        with patch("deia.installer.Path.home", return_value=tmp_path):
            with patch.dict("os.environ", {}, clear=True):
                installer = DeiaInstaller()
                installer.install_global()

                config_file = tmp_path / ".deia-global" / "config.json"
                config = json.loads(config_file.read_text())
                assert config["user"] == "user"
