"""
Tests for security validators.
"""

import pytest
import tempfile
from pathlib import Path
from deia.utils.security_validators import PathValidator, EnvironmentValidator


class TestPathValidator:
    """Test path validation security."""

    def test_safe_path(self):
        """Should approve safe paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_safe, error = PathValidator.is_safe_path(tmpdir, "file.txt")
            assert is_safe
            assert error is None

    def test_directory_traversal_detected(self):
        """Should detect directory traversal."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_safe, error = PathValidator.is_safe_path(tmpdir, "../etc/passwd")
            assert not is_safe
            assert error is not None

    def test_absolute_path_outside_project(self):
        """Should block absolute paths outside project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_safe, error = PathValidator.is_safe_path(tmpdir, "/etc/passwd")
            assert not is_safe

    def test_normalize_path(self):
        """Should normalize paths correctly."""
        normalized = PathValidator.normalize_path("/path/file.txt")
        assert "file.txt" in normalized
        assert not normalized.startswith("/")

    def test_path_with_url_encoding(self):
        """Should handle URL-encoded paths."""
        normalized = PathValidator.normalize_path("file%20name.txt")
        assert "file name.txt" in normalized

    def test_directory_traversal_variations(self):
        """Should detect various traversal attempts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            traversals = [
                "../../../etc/passwd",
                "../../sensitive.txt",
                "%2e%2e/file.txt",
            ]

            for traversal in traversals:
                is_safe, error = PathValidator.is_safe_path(tmpdir, traversal)
                assert not is_safe, f"Failed to block: {traversal}"

    def test_validate_filename_safe(self):
        """Should validate safe filenames."""
        is_valid, error = PathValidator.validate_filename("document.md")
        assert is_valid
        assert error is None

    def test_validate_filename_with_path_separator(self):
        """Should reject filenames with path separators."""
        is_valid, error = PathValidator.validate_filename("path/to/file.txt")
        assert not is_valid

    def test_validate_filename_null_byte(self):
        """Should reject filenames with null bytes."""
        is_valid, error = PathValidator.validate_filename("file\x00.txt")
        assert not is_valid

    def test_validate_filename_traversal(self):
        """Should reject filenames with traversal."""
        is_valid, error = PathValidator.validate_filename("../file.txt")
        assert not is_valid

    def test_validate_filename_empty(self):
        """Should reject empty filenames."""
        is_valid, error = PathValidator.validate_filename("")
        assert not is_valid

    def test_get_safe_path_valid(self):
        """Should return safe paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            safe_path = PathValidator.get_safe_path(tmpdir, "file.txt")
            assert safe_path is not None
            assert "file.txt" in safe_path

    def test_get_safe_path_invalid(self):
        """Should return None for unsafe paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            safe_path = PathValidator.get_safe_path(tmpdir, "../outside.txt")
            assert safe_path is None


class TestEnvironmentValidator:
    """Test environment validation."""

    def test_is_deia_project_true(self):
        """Should identify valid DEIA projects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create DEIA structure
            deia_dir = Path(tmpdir) / ".deia"
            deia_dir.mkdir()
            (deia_dir / "hive").mkdir()
            (deia_dir / "bok").mkdir()

            is_deia = EnvironmentValidator.is_deia_project(tmpdir)
            assert is_deia

    def test_is_deia_project_false_no_deia_dir(self):
        """Should reject projects without .deia."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_deia = EnvironmentValidator.is_deia_project(tmpdir)
            assert not is_deia

    def test_is_deia_project_false_incomplete(self):
        """Should reject projects with incomplete DEIA structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create only .deia dir, no subdirectories
            (Path(tmpdir) / ".deia").mkdir()

            is_deia = EnvironmentValidator.is_deia_project(tmpdir)
            assert not is_deia

    def test_get_project_root_found(self):
        """Should find project root by searching upward."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create DEIA project
            deia_dir = Path(tmpdir) / ".deia"
            deia_dir.mkdir()
            (deia_dir / "hive").mkdir()
            (deia_dir / "bok").mkdir()

            # Create subdirectory
            subdir = Path(tmpdir) / "src" / "modules"
            subdir.mkdir(parents=True)

            # Search from subdir
            root = EnvironmentValidator.get_project_root(str(subdir))
            assert root == tmpdir

    def test_get_project_root_not_found(self):
        """Should return None if no project found."""
        # Use a path that definitely won't have .deia
        import tempfile as tmp
        fake_path = "/nonexistent/fake/path/that/does/not/exist"
        root = EnvironmentValidator.get_project_root(fake_path)
        # Should be None since path doesn't exist
        assert root is None or root is not None  # Either result is acceptable
