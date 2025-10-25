"""
Tests for safe file operations.
"""

import pytest
import tempfile
from pathlib import Path
from deia.services.file_operations import FileOperations, FileType


class TestFileOperations:
    """Test safe file operations."""

    def test_read_valid_file(self):
        """Should read valid files within project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Test Content")

            success, content, error = FileOperations.read_file(tmpdir, "test.md")

            assert success
            assert content == "# Test Content"
            assert error is None

    def test_read_nonexistent_file(self):
        """Should fail for nonexistent files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            success, content, error = FileOperations.read_file(tmpdir, "nonexistent.md")

            assert not success
            assert content is None
            assert error is not None

    def test_path_traversal_blocked(self):
        """Should block directory traversal attempts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            success, _, _ = FileOperations.read_file(tmpdir, "../../../etc/passwd")

            assert not success

    def test_validate_path_safe(self):
        """Should validate safe paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_safe, error = FileOperations.validate_path(tmpdir, "safe_file.md")
            assert is_safe
            assert error is None

    def test_validate_path_traversal(self):
        """Should detect directory traversal."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_safe, error = FileOperations.validate_path(tmpdir, "../outside.txt")
            assert not is_safe
            assert error is not None

    def test_validate_path_absolute_outside(self):
        """Should block absolute paths outside project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_safe, error = FileOperations.validate_path(tmpdir, "/etc/passwd")
            assert not is_safe

    def test_get_file_type(self):
        """Should detect file types."""
        assert FileOperations.get_file_type("file.md") == FileType.MARKDOWN
        assert FileOperations.get_file_type("file.py") == FileType.CODE
        assert FileOperations.get_file_type("file.json") == FileType.CONFIG
        assert FileOperations.get_file_type("file.unknown") == FileType.UNKNOWN

    def test_get_file_info(self):
        """Should get file information."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("Content")

            info = FileOperations.get_file_info(tmpdir, "test.md")

            assert info is not None
            assert info["path"] == "test.md"
            assert info["is_file"]
            assert info["type"] == "markdown"

    def test_list_files(self):
        """Should list files in directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files
            (Path(tmpdir) / "file1.md").write_text("1")
            (Path(tmpdir) / "file2.md").write_text("2")
            (Path(tmpdir) / "file3.txt").write_text("3")

            files = FileOperations.list_files(tmpdir, "", "*.md")

            assert "file1.md" in files
            assert "file2.md" in files
            assert "file3.txt" not in files

    def test_unsafe_patterns_blocked(self):
        """Should block access to unsafe paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_safe, error = FileOperations.validate_path(tmpdir, ".git/config")
            assert not is_safe

            is_safe, error = FileOperations.validate_path(tmpdir, ".env")
            assert not is_safe

    def test_read_utf8_file(self):
        """Should read UTF-8 files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("UTF-8 content: café", encoding="utf-8")

            success, content, error = FileOperations.read_file(tmpdir, "test.md")

            assert success
            assert "café" in content
