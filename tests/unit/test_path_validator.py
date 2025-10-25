"""
Unit tests for PathValidator (P0 CRITICAL SECURITY MODULE)

Tests cover:
1. Directory traversal attack prevention
2. Project boundary enforcement
3. Sensitive file protection
4. Path normalization
5. Edge cases and attack vectors

Created: 2025-10-17
Author: CLAUDE-CODE-004 (Agent DOC)
Task: Chat Phase 2 - PathValidator Tests
"""

import os
import pytest
import tempfile
from pathlib import Path

from src.deia.services.path_validator import PathValidator, ValidationResult, validate_path


class TestPathValidatorInit:
    """Test PathValidator initialization"""

    def test_valid_initialization(self, tmp_path):
        """Test initialization with valid project root"""
        validator = PathValidator(str(tmp_path))
        assert validator.get_project_root() == str(tmp_path.resolve())

    def test_nonexistent_root_fails(self):
        """Test initialization fails with nonexistent directory"""
        with pytest.raises(ValueError, match="does not exist"):
            PathValidator("/nonexistent/path/to/project")

    def test_relative_root_accepted(self, tmp_path):
        """Test initialization with relative path (gets resolved)"""
        os.chdir(tmp_path)
        (tmp_path / "project").mkdir()
        validator = PathValidator("project")
        assert validator.get_project_root() == str((tmp_path / "project").resolve())

    def test_file_as_root_fails(self, tmp_path):
        """Test initialization fails when root is a file, not directory"""
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")

        with pytest.raises(ValueError, match="not a directory"):
            PathValidator(str(file_path))


class TestDirectoryTraversalPrevention:
    """Test prevention of directory traversal attacks"""

    @pytest.fixture
    def validator(self, tmp_path):
        return PathValidator(str(tmp_path))

    def test_simple_traversal_blocked(self, validator):
        """Test simple ../ traversal is blocked"""
        result = validator.validate_path("../etc/passwd")
        assert not result.is_valid
        assert result.blocked_rule == "traversal_prevention"
        assert ".." in result.reason

    def test_windows_traversal_blocked(self, validator):
        """Test Windows-style ..\\ traversal is blocked"""
        result = validator.validate_path("..\\windows\\system32")
        assert not result.is_valid
        assert result.blocked_rule == "traversal_prevention"

    def test_nested_traversal_blocked(self, validator):
        """Test nested traversal attempts are blocked"""
        result = validator.validate_path("docs/../../etc/passwd")
        assert not result.is_valid
        assert result.blocked_rule == "traversal_prevention"

    def test_encoded_traversal_blocked(self, validator):
        """Test URL-encoded traversal attempts are blocked"""
        test_cases = [
            "%2e%2e%2fetc/passwd",      # ../etc/passwd
            "%2e%2e/etc/passwd",         # ../etc/passwd
            "..%2fetc/passwd",           # ../etc/passwd
            "%2e%2e%5cwindows",          # ..\\windows
        ]

        for test_path in test_cases:
            result = validator.validate_path(test_path)
            assert not result.is_valid, f"Failed to block: {test_path}"
            assert result.blocked_rule == "traversal_prevention"

    def test_multiple_traversal_levels_blocked(self, validator):
        """Test multiple ../ levels are blocked"""
        result = validator.validate_path("../../../../../../../etc/passwd")
        assert not result.is_valid
        assert result.blocked_rule == "traversal_prevention"


class TestProjectBoundaryEnforcement:
    """Test enforcement of project boundary restrictions"""

    @pytest.fixture
    def setup_paths(self, tmp_path):
        """Create test directory structure"""
        project = tmp_path / "deia_project"
        project.mkdir()

        # Create some subdirectories
        (project / ".deia").mkdir()
        (project / "bok").mkdir()
        (project / "docs").mkdir()

        # Create file outside project
        (tmp_path / "outside.txt").write_text("outside")

        # Create file inside project
        (project / "bok" / "pattern.md").write_text("pattern")

        return {
            "project": project,
            "tmp_path": tmp_path,
        }

    def test_access_within_boundary_allowed(self, setup_paths):
        """Test files within project boundary are accessible"""
        validator = PathValidator(str(setup_paths["project"]))

        result = validator.validate_path("bok/pattern.md")
        assert result.is_valid
        assert Path(result.normalized_path).exists()

    def test_access_outside_boundary_blocked(self, setup_paths):
        """Test files outside project boundary are blocked"""
        validator = PathValidator(str(setup_paths["project"]))

        # Try to access file outside project (using absolute path)
        outside_file = setup_paths["tmp_path"] / "outside.txt"
        result = validator.validate_path(str(outside_file))

        assert not result.is_valid
        assert result.blocked_rule == "boundary_enforcement"

    def test_symlink_escape_blocked(self, setup_paths):
        """Test symlink escape attempts are blocked"""
        project = setup_paths["project"]
        outside = setup_paths["tmp_path"] / "outside.txt"

        # Create symlink inside project pointing outside
        symlink = project / "escape.txt"
        try:
            symlink.symlink_to(outside)
        except OSError:
            pytest.skip("Symlink creation not supported on this system")

        validator = PathValidator(str(project))
        result = validator.validate_path("escape.txt")

        # Symlink resolves to outside project, should be blocked
        assert not result.is_valid
        assert result.blocked_rule == "boundary_enforcement"


class TestSensitiveFileProtection:
    """Test protection of sensitive files and directories"""

    @pytest.fixture
    def validator(self, tmp_path):
        # Create project structure with sensitive files
        project = tmp_path / "deia_project"
        project.mkdir()

        # Create various sensitive files for testing
        (project / ".git").mkdir()
        (project / ".env").write_text("SECRET=value")
        (project / ".env.local").write_text("SECRET=value")
        (project / "secrets.txt").write_text("secret")
        (project / "credentials.json").write_text("{}")
        (project / "password.txt").write_text("password")
        (project / "api_token.txt").write_text("token")
        (project / ".ssh").mkdir()
        (project / "id_rsa").write_text("private key")
        (project / "config.json").write_text("{}")

        # Create safe files
        (project / "bok").mkdir()
        (project / "bok" / "pattern.md").write_text("safe content")
        (project / "docs" / "readme.md").mkdir(parents=True)

        return PathValidator(str(project))

    def test_git_directory_blocked(self, validator):
        """Test .git directory access is blocked"""
        result = validator.validate_path(".git")
        assert not result.is_valid
        assert result.blocked_rule == "sensitive_file_protection"

    def test_git_file_blocked(self, validator):
        """Test .git/config access is blocked"""
        result = validator.validate_path(".git/config")
        assert not result.is_valid
        assert result.blocked_rule == "sensitive_file_protection"

    def test_env_file_blocked(self, validator):
        """Test .env file access is blocked"""
        test_cases = [
            ".env",
            ".env.local",
            ".env.production",
            ".env.development",
        ]

        for env_file in test_cases:
            result = validator.validate_path(env_file)
            assert not result.is_valid, f"Failed to block: {env_file}"
            assert result.blocked_rule == "sensitive_file_protection"

    def test_secret_files_blocked(self, validator):
        """Test files with 'secret' in name are blocked"""
        result = validator.validate_path("secrets.txt")
        assert not result.is_valid
        assert result.blocked_rule == "sensitive_file_protection"

    def test_credential_files_blocked(self, validator):
        """Test files with 'credential' in name are blocked"""
        result = validator.validate_path("credentials.json")
        assert not result.is_valid
        assert result.blocked_rule == "sensitive_file_protection"

    def test_password_files_blocked(self, validator):
        """Test files with 'password' in name are blocked"""
        result = validator.validate_path("password.txt")
        assert not result.is_valid
        assert result.blocked_rule == "sensitive_file_protection"

    def test_token_files_blocked(self, validator):
        """Test files with 'token' in name are blocked"""
        result = validator.validate_path("api_token.txt")
        assert not result.is_valid
        assert result.blocked_rule == "sensitive_file_protection"

    def test_ssh_keys_blocked(self, validator):
        """Test SSH private keys are blocked"""
        test_cases = [
            ".ssh",
            ".ssh/id_rsa",
            "id_rsa",
            "id_dsa",
        ]

        for ssh_file in test_cases:
            result = validator.validate_path(ssh_file)
            assert not result.is_valid, f"Failed to block: {ssh_file}"
            assert result.blocked_rule == "sensitive_file_protection"

    def test_config_files_blocked(self, validator):
        """Test config files are blocked (may contain secrets)"""
        result = validator.validate_path("config.json")
        assert not result.is_valid
        assert result.blocked_rule == "sensitive_file_protection"

    def test_safe_files_allowed(self, validator):
        """Test non-sensitive files are allowed"""
        result = validator.validate_path("bok/pattern.md")
        assert result.is_valid
        assert result.blocked_rule is None


class TestPathNormalization:
    """Test path normalization behavior"""

    @pytest.fixture
    def validator(self, tmp_path):
        project = tmp_path / "deia_project"
        project.mkdir()
        (project / "bok" / "patterns").mkdir(parents=True)
        (project / "bok" / "patterns" / "test.md").write_text("content")
        return PathValidator(str(project))

    def test_relative_path_normalized(self, validator):
        """Test relative paths are normalized to absolute"""
        result = validator.validate_path("bok/patterns/test.md")
        assert result.is_valid
        assert Path(result.normalized_path).is_absolute()

    def test_absolute_path_within_project(self, validator):
        """Test absolute path within project is allowed"""
        project_root = Path(validator.get_project_root())
        absolute_path = project_root / "bok" / "patterns" / "test.md"

        result = validator.validate_path(str(absolute_path))
        assert result.is_valid

    def test_forward_slash_paths(self, validator):
        """Test forward slash paths work on all platforms"""
        result = validator.validate_path("bok/patterns/test.md")
        assert result.is_valid

    def test_backslash_paths(self, validator):
        """Test backslash paths work on Windows"""
        result = validator.validate_path("bok\\patterns\\test.md")
        assert result.is_valid


class TestValidateMultiplePaths:
    """Test batch validation of multiple paths"""

    @pytest.fixture
    def validator(self, tmp_path):
        project = tmp_path / "deia_project"
        project.mkdir()
        (project / "bok").mkdir()
        (project / ".env").write_text("secret")
        (project / "bok" / "safe.md").write_text("safe")
        return PathValidator(str(project))

    def test_validate_paths_batch(self, validator):
        """Test validating multiple paths at once"""
        paths = [
            "bok/safe.md",          # Valid
            "../etc/passwd",        # Traversal
            ".env",                 # Sensitive
        ]

        results = validator.validate_paths(paths)

        assert len(results) == 3
        assert results[0].is_valid == True
        assert results[1].is_valid == False
        assert results[2].is_valid == False


class TestConvenienceFunction:
    """Test convenience function"""

    def test_validate_path_function(self, tmp_path):
        """Test standalone validate_path function"""
        project = tmp_path / "deia_project"
        project.mkdir()
        (project / "test.txt").write_text("test")

        result = validate_path("test.txt", str(project))
        assert result.is_valid

    def test_convenience_function_blocks_traversal(self, tmp_path):
        """Test convenience function blocks traversal"""
        result = validate_path("../etc/passwd", str(tmp_path))
        assert not result.is_valid
        assert result.blocked_rule == "traversal_prevention"


class TestEdgeCases:
    """Test edge cases and corner scenarios"""

    def test_empty_path_handled(self, tmp_path):
        """Test empty path is handled gracefully"""
        validator = PathValidator(str(tmp_path))
        result = validator.validate_path("")
        # Empty path resolves to project root, which should be valid
        assert result.is_valid

    def test_dot_path_handled(self, tmp_path):
        """Test current directory (.) is handled"""
        validator = PathValidator(str(tmp_path))
        result = validator.validate_path(".")
        # Current directory resolves to project root
        assert result.is_valid

    def test_nonexistent_file_within_boundary(self, tmp_path):
        """Test nonexistent file within boundary is considered valid path"""
        validator = PathValidator(str(tmp_path))
        # PathValidator only validates path security, not file existence
        result = validator.validate_path("nonexistent/file.txt")
        assert result.is_valid  # Path is safe, even if file doesn't exist

    def test_case_sensitivity_in_sensitive_patterns(self, tmp_path):
        """Test sensitive patterns are case-insensitive"""
        project = tmp_path / "deia_project"
        project.mkdir()
        (project / "SECRET.txt").write_text("secret")
        (project / "Password.TXT").write_text("password")

        validator = PathValidator(str(project))

        result1 = validator.validate_path("SECRET.txt")
        assert not result1.is_valid

        result2 = validator.validate_path("Password.TXT")
        assert not result2.is_valid


class TestGetMethods:
    """Test getter methods"""

    def test_get_project_root(self, tmp_path):
        """Test get_project_root returns correct path"""
        validator = PathValidator(str(tmp_path))
        assert validator.get_project_root() == str(tmp_path.resolve())

    def test_get_sensitive_patterns(self, tmp_path):
        """Test get_sensitive_patterns returns pattern list"""
        validator = PathValidator(str(tmp_path))
        patterns = validator.get_sensitive_patterns()

        assert isinstance(patterns, list)
        assert len(patterns) > 0
        assert "\\.git($|/|\\\\)" in patterns
        assert "\\.env($|\\.)" in patterns
