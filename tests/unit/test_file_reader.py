"""
Unit tests for FileReader

Tests cover:
1. Security integration with PathValidator
2. File reading with encoding detection
3. Size limit enforcement
4. Binary file handling
5. Error handling
6. Language detection

Created: 2025-10-17
Author: CLAUDE-CODE-004 (Agent DOC)
Task: Chat Phase 2 - FileReader API Tests
"""

import os
import pytest
from pathlib import Path

from src.deia.services.file_reader import FileReader, FileContent, read_file


class TestFileReaderInit:
    """Test FileReader initialization"""

    def test_valid_initialization(self, tmp_path):
        """Test initialization with valid project root"""
        reader = FileReader(str(tmp_path))
        assert reader.project_root == str(tmp_path.resolve())

    def test_invalid_root_fails(self):
        """Test initialization fails with invalid root"""
        with pytest.raises(ValueError):
            FileReader("/nonexistent/path")


class TestSecurityIntegration:
    """Test integration with PathValidator"""

    @pytest.fixture
    def setup(self, tmp_path):
        """Create test environment"""
        project = tmp_path / "deia_project"
        project.mkdir()

        # Safe file
        (project / "safe.txt").write_text("safe content")

        # Sensitive file
        (project / ".env").write_text("SECRET=value")

        return {
            "project": project,
            "reader": FileReader(str(project)),
        }

    def test_safe_file_allowed(self, setup):
        """Test reading safe file succeeds"""
        result = setup["reader"].read_file("safe.txt")
        assert result.success
        assert result.content == "safe content"

    def test_traversal_blocked(self, setup):
        """Test directory traversal is blocked"""
        result = setup["reader"].read_file("../etc/passwd")
        assert not result.success
        assert result.error_type == "security_validation_failed"
        assert "traversal" in result.error.lower()

    def test_sensitive_file_blocked(self, setup):
        """Test sensitive files are blocked"""
        result = setup["reader"].read_file(".env")
        assert not result.success
        assert result.error_type == "security_validation_failed"


class TestFileReading:
    """Test file reading functionality"""

    @pytest.fixture
    def reader(self, tmp_path):
        project = tmp_path / "deia_project"
        project.mkdir()
        return FileReader(str(project)), project

    def test_read_text_file_utf8(self, reader):
        """Test reading UTF-8 text file"""
        file_reader, project = reader
        test_file = project / "test.txt"
        test_file.write_text("Hello, World!", encoding='utf-8')

        result = file_reader.read_file("test.txt")
        assert result.success
        assert result.content == "Hello, World!"
        assert result.encoding == 'utf-8'

    def test_read_markdown_file(self, reader):
        """Test reading markdown file with language detection"""
        file_reader, project = reader
        test_file = project / "readme.md"
        test_file.write_text("# Heading\n\nContent", encoding='utf-8')

        result = file_reader.read_file("readme.md")
        assert result.success
        assert "# Heading" in result.content
        assert result.language == 'markdown'

    def test_read_python_file(self, reader):
        """Test reading Python file with language detection"""
        file_reader, project = reader
        test_file = project / "script.py"
        test_file.write_text("print('hello')", encoding='utf-8')

        result = file_reader.read_file("script.py")
        assert result.success
        assert result.language == 'python'

    def test_read_json_file(self, reader):
        """Test reading JSON file"""
        file_reader, project = reader
        test_file = project / "data.json"
        test_file.write_text('{"key": "value"}', encoding='utf-8')

        result = file_reader.read_file("data.json")
        assert result.success
        assert result.language == 'json'
        assert '{"key": "value"}' in result.content

    def test_read_file_with_bom(self, reader):
        """Test reading file with UTF-8 BOM"""
        file_reader, project = reader
        test_file = project / "bom.txt"
        test_file.write_text("content", encoding='utf-8-sig')

        result = file_reader.read_file("bom.txt")
        assert result.success
        # BOM character may be preserved depending on encoding detection
        assert "content" in result.content
        assert result.encoding in ['utf-8', 'utf-8-sig']


class TestSizeLimits:
    """Test file size limit enforcement"""

    @pytest.fixture
    def reader(self, tmp_path):
        project = tmp_path / "deia_project"
        project.mkdir()
        return FileReader(str(project)), project

    def test_small_file_allowed(self, reader):
        """Test small file is allowed"""
        file_reader, project = reader
        test_file = project / "small.txt"
        test_file.write_text("x" * 1000)  # 1KB

        result = file_reader.read_file("small.txt")
        assert result.success

    def test_large_file_blocked(self, reader):
        """Test file over 1MB is blocked"""
        file_reader, project = reader
        test_file = project / "large.txt"

        # Create file larger than 1MB
        test_file.write_text("x" * (1024 * 1024 + 1))

        result = file_reader.read_file("large.txt")
        assert not result.success
        assert result.error_type == "file_too_large"
        assert "1048577" in result.error  # size in error message

    def test_exactly_1mb_allowed(self, reader):
        """Test file exactly 1MB is allowed"""
        file_reader, project = reader
        test_file = project / "max.txt"
        test_file.write_text("x" * (1024 * 1024))  # Exactly 1MB

        result = file_reader.read_file("max.txt")
        assert result.success


class TestBinaryFiles:
    """Test binary file handling"""

    @pytest.fixture
    def reader(self, tmp_path):
        project = tmp_path / "deia_project"
        project.mkdir()
        return FileReader(str(project)), project

    def test_binary_extension_blocked(self, reader):
        """Test binary file extensions are blocked"""
        file_reader, project = reader

        binary_files = [
            "image.png",
            "archive.zip",
            "executable.exe",
            "library.dll",
            "video.mp4",
            "compiled.pyc",
        ]

        for filename in binary_files:
            test_file = project / filename
            test_file.write_bytes(b'\x00\x01\x02\x03')

            result = file_reader.read_file(filename)
            assert not result.success, f"Failed to block: {filename}"
            assert result.error_type == "binary_file"


class TestErrorHandling:
    """Test error handling"""

    @pytest.fixture
    def reader(self, tmp_path):
        project = tmp_path / "deia_project"
        project.mkdir()
        return FileReader(str(project)), project

    def test_nonexistent_file(self, reader):
        """Test reading nonexistent file"""
        file_reader, project = reader

        result = file_reader.read_file("does_not_exist.txt")
        assert not result.success
        assert result.error_type == "file_not_found"

    def test_read_directory_fails(self, reader):
        """Test reading a directory fails"""
        file_reader, project = reader
        (project / "subdir").mkdir()

        result = file_reader.read_file("subdir")
        assert not result.success
        assert result.error_type == "not_a_file"


class TestLanguageDetection:
    """Test programming language detection"""

    @pytest.fixture
    def reader(self, tmp_path):
        project = tmp_path / "deia_project"
        project.mkdir()
        return FileReader(str(project)), project

    def test_python_detection(self, reader):
        """Test Python file detection"""
        file_reader, project = reader
        (project / "test.py").write_text("# Python")

        result = file_reader.read_file("test.py")
        assert result.language == 'python'

    def test_javascript_detection(self, reader):
        """Test JavaScript file detection"""
        file_reader, project = reader
        (project / "test.js").write_text("// JavaScript")

        result = file_reader.read_file("test.js")
        assert result.language == 'javascript'

    def test_markdown_detection(self, reader):
        """Test Markdown file detection"""
        file_reader, project = reader
        (project / "readme.md").write_text("# Markdown")

        result = file_reader.read_file("readme.md")
        assert result.language == 'markdown'

    def test_yaml_detection(self, reader):
        """Test YAML file detection"""
        file_reader, project = reader
        (project / "config.yaml").write_text("key: value")

        result = file_reader.read_file("config.yaml")
        assert result.language == 'yaml'

    def test_unknown_extension(self, reader):
        """Test unknown extension returns None"""
        file_reader, project = reader
        (project / "unknown.xyz").write_text("content")

        result = file_reader.read_file("unknown.xyz")
        assert result.success
        assert result.language is None


class TestEncodingDetection:
    """Test encoding detection"""

    @pytest.fixture
    def reader(self, tmp_path):
        project = tmp_path / "deia_project"
        project.mkdir()
        return FileReader(str(project)), project

    def test_utf8_detected(self, reader):
        """Test UTF-8 encoding detected"""
        file_reader, project = reader
        test_file = project / "utf8.txt"
        test_file.write_text("Hello, 世界", encoding='utf-8')

        result = file_reader.read_file("utf8.txt")
        assert result.success
        assert result.encoding == 'utf-8'
        assert "世界" in result.content

    def test_latin1_fallback(self, reader):
        """Test latin-1 fallback for non-UTF8 files"""
        file_reader, project = reader
        test_file = project / "latin1.txt"

        # Write latin-1 encoded text
        with open(test_file, 'wb') as f:
            f.write("café".encode('latin-1'))

        result = file_reader.read_file("latin1.txt")
        assert result.success
        assert result.encoding is not None  # Some encoding detected


class TestBatchReading:
    """Test reading multiple files"""

    @pytest.fixture
    def reader(self, tmp_path):
        project = tmp_path / "deia_project"
        project.mkdir()

        # Create test files
        (project / "file1.txt").write_text("content1")
        (project / "file2.txt").write_text("content2")
        (project / "file3.txt").write_text("content3")

        return FileReader(str(project)), project

    def test_read_multiple_files(self, reader):
        """Test reading multiple files at once"""
        file_reader, project = reader

        results = file_reader.read_files(["file1.txt", "file2.txt", "file3.txt"])

        assert len(results) == 3
        assert all(r.success for r in results)
        assert results[0].content == "content1"
        assert results[1].content == "content2"
        assert results[2].content == "content3"

    def test_batch_with_errors(self, reader):
        """Test batch read with some errors"""
        file_reader, project = reader

        results = file_reader.read_files([
            "file1.txt",           # exists
            "nonexistent.txt",     # doesn't exist
            "file2.txt",           # exists
        ])

        assert len(results) == 3
        assert results[0].success == True
        assert results[1].success == False
        assert results[2].success == True


class TestFileInfo:
    """Test get_file_info method"""

    @pytest.fixture
    def reader(self, tmp_path):
        project = tmp_path / "deia_project"
        project.mkdir()
        (project / "test.txt").write_text("x" * 1000)
        (project / "large.txt").write_text("x" * (1024 * 1024 + 1))
        (project / "image.png").write_bytes(b'\x00\x01')

        return FileReader(str(project)), project

    def test_file_info_existing(self, reader):
        """Test getting info for existing file"""
        file_reader, project = reader

        info = file_reader.get_file_info("test.txt")

        assert info['exists'] == True
        assert info['valid'] == True
        assert info['is_file'] == True
        assert info['size'] == 1000
        assert info['too_large'] == False

    def test_file_info_nonexistent(self, reader):
        """Test getting info for nonexistent file"""
        file_reader, project = reader

        info = file_reader.get_file_info("nonexistent.txt")

        assert info['exists'] == False
        assert info['valid'] == True  # Path is valid, file just doesn't exist

    def test_file_info_binary(self, reader):
        """Test info shows binary file"""
        file_reader, project = reader

        info = file_reader.get_file_info("image.png")

        assert info['exists'] == True
        assert info['is_binary'] == True

    def test_file_info_too_large(self, reader):
        """Test info shows file too large"""
        file_reader, project = reader

        info = file_reader.get_file_info("large.txt")

        assert info['exists'] == True
        assert info['too_large'] == True

    def test_file_info_language(self, reader):
        """Test info includes language detection"""
        file_reader, project = reader

        info = file_reader.get_file_info("test.txt")

        assert info['language'] == 'text'


class TestConvenienceFunction:
    """Test convenience function"""

    def test_read_file_function(self, tmp_path):
        """Test standalone read_file function"""
        project = tmp_path / "deia_project"
        project.mkdir()
        (project / "test.txt").write_text("content")

        result = read_file("test.txt", str(project))

        assert result.success
        assert result.content == "content"
