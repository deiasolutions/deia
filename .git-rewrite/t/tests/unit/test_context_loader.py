"""
Test Suite for Context Loader

Comprehensive tests for the DEIA Context Loader service, covering:
- Initialization and configuration
- Context loading from multiple sources
- Security validation integration
- Caching behavior
- Memory management and size limits
- Edge cases and error handling

Author: CLAUDE-CODE-002 (Documentation Systems Lead)
Date: 2025-10-18
Target Coverage: >80%
"""

import json
import os
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

from src.deia.services.context_loader import (
    ContextLoader,
    ContextSource,
    ContextWindow
)


class TestContextLoaderInitialization:
    """Test ContextLoader initialization and configuration."""

    def test_init_with_valid_project_root(self, tmp_path):
        """Test initialization with valid project root."""
        # Create .deia directory
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))

        assert loader.project_root == tmp_path
        assert loader.max_context_size == ContextLoader.DEFAULT_MAX_CONTEXT_SIZE
        assert loader.cache_ttl == ContextLoader.DEFAULT_CACHE_TTL
        assert loader.enable_caching is True

    def test_init_with_custom_config(self, tmp_path):
        """Test initialization with custom configuration."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(
            str(tmp_path),
            max_context_size=50000,
            cache_ttl=600,
            enable_caching=False
        )

        assert loader.max_context_size == 50000
        assert loader.cache_ttl == 600
        assert loader.enable_caching is False

    def test_init_with_nonexistent_project_root(self):
        """Test initialization fails with nonexistent project root."""
        with pytest.raises(ValueError, match="does not exist"):
            ContextLoader("/nonexistent/path/12345")

    def test_init_with_file_as_project_root(self, tmp_path):
        """Test initialization fails when project root is a file."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("test")

        with pytest.raises(ValueError, match="not a directory"):
            ContextLoader(str(file_path))

    def test_is_deia_project_true(self, tmp_path):
        """Test is_deia_project returns True for DEIA project."""
        (tmp_path / ".deia").mkdir()
        loader = ContextLoader(str(tmp_path))

        assert loader.is_deia_project() is True

    def test_is_deia_project_false(self, tmp_path):
        """Test is_deia_project returns False for non-DEIA project."""
        loader = ContextLoader(str(tmp_path))

        assert loader.is_deia_project() is False

    def test_get_config(self, tmp_path):
        """Test get_config returns current configuration."""
        (tmp_path / ".deia").mkdir()
        loader = ContextLoader(str(tmp_path), max_context_size=75000)

        config = loader.get_config()

        assert config["project_root"] == str(tmp_path)
        assert config["max_context_size"] == 75000
        assert config["is_deia_project"] is True


class TestContextLoadingFiles:
    """Test file context loading."""

    def test_load_single_file(self, tmp_path):
        """Test loading a single file."""
        (tmp_path / ".deia").mkdir()

        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Content")

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_files=["test.md"])

        assert context.source_count == 1
        assert context.sources[0].source_type == "file"
        assert "# Test Content" in context.sources[0].content
        assert context.sources[0].relevance_score == 1.0
        assert context.truncated is False

    def test_load_multiple_files(self, tmp_path):
        """Test loading multiple files."""
        (tmp_path / ".deia").mkdir()

        # Create test files
        (tmp_path / "file1.txt").write_text("File 1")
        (tmp_path / "file2.txt").write_text("File 2")
        (tmp_path / "file3.txt").write_text("File 3")

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_files=["file1.txt", "file2.txt", "file3.txt"])

        assert context.source_count == 3
        assert all(s.source_type == "file" for s in context.sources)

    def test_load_file_with_path_traversal_blocked(self, tmp_path):
        """Test that path traversal attempts are blocked."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_files=["../../etc/passwd"])

        # Should load 0 files due to security validation
        assert context.source_count == 0

    def test_load_nonexistent_file(self, tmp_path):
        """Test loading nonexistent file is handled gracefully."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_files=["nonexistent.txt"])

        assert context.source_count == 0

    def test_load_files_respects_size_limit(self, tmp_path):
        """Test that file loading respects size limits."""
        (tmp_path / ".deia").mkdir()

        # Create multiple files that together exceed limit
        (tmp_path / "file1.txt").write_text("x" * 2000)
        (tmp_path / "file2.txt").write_text("y" * 2000)
        (tmp_path / "file3.txt").write_text("z" * 2000)

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(
            include_files=["file1.txt", "file2.txt", "file3.txt"],
            max_size_bytes=4000  # Can only fit 2 files
        )

        # Should only load files that fit within limit
        assert context.total_size <= 4000
        assert context.truncated is True


class TestContextLoadingPatterns:
    """Test BOK pattern context loading."""

    def test_load_single_pattern(self, tmp_path):
        """Test loading a single BOK pattern."""
        (tmp_path / ".deia").mkdir()
        bok_dir = tmp_path / "bok"
        bok_dir.mkdir()

        # Create test pattern
        pattern_file = bok_dir / "test-pattern.md"
        pattern_file.write_text("# Test Pattern\nPattern content")

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_patterns=["test-pattern"])

        assert context.source_count == 1
        assert context.sources[0].source_type == "pattern"
        assert "Test Pattern" in context.sources[0].content
        assert context.sources[0].relevance_score == 0.9

    def test_load_multiple_patterns(self, tmp_path):
        """Test loading multiple BOK patterns."""
        (tmp_path / ".deia").mkdir()
        bok_dir = tmp_path / "bok"
        bok_dir.mkdir()

        # Create test patterns
        (bok_dir / "pattern1.md").write_text("Pattern 1")
        (bok_dir / "pattern2.md").write_text("Pattern 2")

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_patterns=["pattern1", "pattern2"])

        assert context.source_count == 2
        assert all(s.source_type == "pattern" for s in context.sources)

    def test_load_nonexistent_pattern(self, tmp_path):
        """Test loading nonexistent pattern is handled gracefully."""
        (tmp_path / ".deia").mkdir()
        bok_dir = tmp_path / "bok"
        bok_dir.mkdir()

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_patterns=["nonexistent"])

        assert context.source_count == 0


class TestContextLoadingSessions:
    """Test session history context loading."""

    def test_load_recent_sessions(self, tmp_path):
        """Test loading recent session history."""
        (tmp_path / ".deia").mkdir()
        sessions_dir = tmp_path / ".deia" / "sessions"
        sessions_dir.mkdir()

        # Create test session files with different timestamps
        for i in range(5):
            session_file = sessions_dir / f"session{i}.md"
            session_file.write_text(f"Session {i} content")
            # Touch file to set mtime
            time.sleep(0.01)  # Ensure different mtimes

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_sessions=3)

        # Should load 3 most recent sessions
        assert context.source_count == 3
        assert all(s.source_type == "session" for s in context.sources)

    def test_load_sessions_when_directory_missing(self, tmp_path):
        """Test loading sessions when directory doesn't exist."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_sessions=5)

        assert context.source_count == 0


class TestContextLoadingPreferences:
    """Test preference context loading."""

    def test_load_preferences(self, tmp_path):
        """Test loading user preferences."""
        deia_dir = tmp_path / ".deia"
        deia_dir.mkdir()

        # Create config file
        config_file = deia_dir / "config.yaml"
        config_file.write_text("theme: dark\nlanguage: en")

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_preferences=True)

        assert context.source_count == 1
        assert context.sources[0].source_type == "preferences"
        assert "theme: dark" in context.sources[0].content

    def test_load_preferences_when_missing(self, tmp_path):
        """Test loading preferences when config doesn't exist."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_preferences=True)

        assert context.source_count == 0


class TestContextLoadingStructure:
    """Test project structure context loading."""

    def test_load_project_structure(self, tmp_path):
        """Test loading project structure overview."""
        (tmp_path / ".deia").mkdir()
        (tmp_path / "src").mkdir()
        (tmp_path / "docs").mkdir()

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_structure=True)

        assert context.source_count == 1
        assert context.sources[0].source_type == "structure"

        # Parse structure JSON
        structure = json.loads(context.sources[0].content)
        assert isinstance(structure, dict)


class TestContextWindowAssembly:
    """Test context window assembly with multiple sources."""

    def test_assemble_mixed_context(self, tmp_path):
        """Test assembling context from multiple source types."""
        # Setup project
        (tmp_path / ".deia").mkdir()
        (tmp_path / "test.txt").write_text("Test file")

        bok_dir = tmp_path / "bok"
        bok_dir.mkdir()
        (bok_dir / "pattern.md").write_text("Test pattern")

        sessions_dir = tmp_path / ".deia" / "sessions"
        sessions_dir.mkdir()
        (sessions_dir / "session1.md").write_text("Test session")

        # Load mixed context
        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(
            include_files=["test.txt"],
            include_patterns=["pattern"],
            include_sessions=1,
            include_structure=True
        )

        # Should have file, pattern, session, structure
        assert context.source_count == 4
        source_types = {s.source_type for s in context.sources}
        assert "file" in source_types
        assert "pattern" in source_types
        assert "session" in source_types
        assert "structure" in source_types

    def test_relevance_filtering(self, tmp_path):
        """Test filtering sources by relevance threshold."""
        (tmp_path / ".deia").mkdir()
        (tmp_path / "test.txt").write_text("Test")

        loader = ContextLoader(str(tmp_path))

        # With high threshold, should exclude low-relevance sources
        context = loader.load_context(
            include_files=["test.txt"],
            include_structure=True,
            relevance_threshold=0.5  # Excludes structure (0.4)
        )

        # Should only have file (1.0), not structure (0.4)
        assert all(s.relevance_score >= 0.5 for s in context.sources)

    def test_context_summary_generation(self, tmp_path):
        """Test context summary generation."""
        (tmp_path / ".deia").mkdir()
        (tmp_path / "file1.txt").write_text("Test 1")
        (tmp_path / "file2.txt").write_text("Test 2")

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_files=["file1.txt", "file2.txt"])

        assert "2 file(s)" in context.summary

    def test_assembly_time_recorded(self, tmp_path):
        """Test that assembly time is recorded."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_structure=True)

        assert context.assembly_time_ms >= 0
        assert context.assembly_time_ms < 1000  # Should be fast (<1s)


class TestCaching:
    """Test caching behavior."""

    def test_cache_enabled_by_default(self, tmp_path):
        """Test that caching is enabled by default."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))
        assert loader.enable_caching is True

    def test_cache_can_be_disabled(self, tmp_path):
        """Test that caching can be disabled."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path), enable_caching=False)
        assert loader.enable_caching is False

    def test_structure_caching(self, tmp_path):
        """Test that project structure is cached."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))

        # First call - cache miss
        loader.load_context(include_structure=True)

        # Second call - cache hit
        loader.load_context(include_structure=True)

        stats = loader.get_cache_stats()
        assert stats["hits"] > 0

    def test_cache_expiration(self, tmp_path):
        """Test that cache entries expire after TTL."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path), cache_ttl=1)  # 1 second TTL

        # Load to cache
        loader.load_context(include_structure=True)

        # Wait for expiration
        time.sleep(1.1)

        # Load again - should be cache miss
        loader.load_context(include_structure=True)

        stats = loader.get_cache_stats()
        assert stats["misses"] >= 2  # Initial miss + expired miss

    def test_clear_cache(self, tmp_path):
        """Test manual cache clearing."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))
        loader.load_context(include_structure=True)

        # Clear cache
        loader.clear_cache()

        stats = loader.get_cache_stats()
        assert stats["entries"] == 0

    def test_cache_stats(self, tmp_path):
        """Test cache statistics."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))
        stats = loader.get_cache_stats()

        assert "enabled" in stats
        assert "entries" in stats
        assert "hits" in stats
        assert "misses" in stats
        assert "hit_rate_percent" in stats
        assert "ttl_seconds" in stats


class TestSizeLimits:
    """Test context size limit enforcement."""

    def test_size_limit_enforced(self, tmp_path):
        """Test that size limits are enforced - won't load files that exceed limit."""
        (tmp_path / ".deia").mkdir()

        # Create files that together exceed limit
        (tmp_path / "file1.txt").write_text("x" * 2500)
        (tmp_path / "file2.txt").write_text("y" * 2500)
        (tmp_path / "file3.txt").write_text("z" * 2500)

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(
            include_files=["file1.txt", "file2.txt", "file3.txt"],
            max_size_bytes=5500  # Can fit 2 files (~5000 bytes) but not 3 (~7500 bytes)
        )

        # Should respect size limit
        assert context.total_size <= 5500
        # Should load as many files as fit (2 files)
        assert context.source_count < 3

    def test_custom_size_limit(self, tmp_path):
        """Test custom size limit parameter."""
        (tmp_path / ".deia").mkdir()
        (tmp_path / "test.txt").write_text("x" * 10000)

        loader = ContextLoader(str(tmp_path), max_context_size=50000)

        # Use custom limit lower than instance default
        context = loader.load_context(
            include_files=["test.txt"],
            max_size_bytes=5000
        )

        assert context.total_size <= 5000


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_context_load(self, tmp_path):
        """Test loading with no sources specified."""
        (tmp_path / ".deia").mkdir()

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context()

        assert context.source_count == 0
        assert context.total_size == 0
        assert "Empty context" in context.summary

    def test_max_files_limit(self, tmp_path):
        """Test that max files per load limit is enforced."""
        (tmp_path / ".deia").mkdir()

        # Create more files than limit
        file_list = []
        for i in range(ContextLoader.MAX_FILES_PER_LOAD + 10):
            file_path = tmp_path / f"file{i}.txt"
            file_path.write_text(f"File {i}")
            file_list.append(f"file{i}.txt")

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_files=file_list)

        # Should only load up to MAX_FILES_PER_LOAD
        assert context.source_count <= ContextLoader.MAX_FILES_PER_LOAD

    def test_unicode_content(self, tmp_path):
        """Test handling of Unicode content."""
        (tmp_path / ".deia").mkdir()

        # Create file with Unicode content
        unicode_file = tmp_path / "unicode.txt"
        unicode_file.write_text("Hello 世界 🌍", encoding="utf-8")

        loader = ContextLoader(str(tmp_path))
        context = loader.load_context(include_files=["unicode.txt"])

        assert context.source_count == 1
        assert "世界" in context.sources[0].content
        assert "🌍" in context.sources[0].content


class TestContextSourceDataclass:
    """Test ContextSource dataclass."""

    def test_context_source_creation(self):
        """Test creating ContextSource instance."""
        source = ContextSource(
            source_type="file",
            content="test content",
            path="/path/to/file",
            relevance_score=0.8,
            size_bytes=100,
            metadata={"key": "value"}
        )

        assert source.source_type == "file"
        assert source.content == "test content"
        assert source.relevance_score == 0.8

    def test_context_source_to_dict(self):
        """Test converting ContextSource to dictionary."""
        source = ContextSource(
            source_type="pattern",
            content="pattern content",
            path="/path/to/pattern",
            relevance_score=0.9,
            size_bytes=200
        )

        result = source.to_dict()

        assert result["source_type"] == "pattern"
        assert result["content"] == "pattern content"
        assert result["metadata"] == {}


class TestContextWindowDataclass:
    """Test ContextWindow dataclass."""

    def test_context_window_creation(self):
        """Test creating ContextWindow instance."""
        sources = [
            ContextSource("file", "content", "/path", 1.0, 100)
        ]

        window = ContextWindow(
            sources=sources,
            total_size=100,
            source_count=1,
            assembly_time_ms=50,
            truncated=False,
            summary="Test summary"
        )

        assert window.source_count == 1
        assert window.total_size == 100
        assert window.truncated is False

    def test_context_window_to_dict(self):
        """Test converting ContextWindow to dictionary."""
        sources = [
            ContextSource("file", "content", "/path", 1.0, 100)
        ]

        window = ContextWindow(
            sources=sources,
            total_size=100,
            source_count=1,
            assembly_time_ms=50,
            truncated=False,
            summary="Test"
        )

        result = window.to_dict()

        assert result["source_count"] == 1
        assert result["truncated"] is False
        assert len(result["sources"]) == 1
