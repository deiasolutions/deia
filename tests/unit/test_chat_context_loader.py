"""Tests for ChatContextLoader service."""

import pytest
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.deia.services.chat_context_loader import ChatContextLoader


@pytest.fixture
def loader(tmp_path):
    """Provide ChatContextLoader instance."""
    return ChatContextLoader(tmp_path)


class TestContextLoading:
    """Tests for context file loading."""

    def test_initialize(self, loader):
        """Test loader initialization."""
        assert loader.loaded_context == []
        assert not loader.auto_detect_complete

    def test_auto_detect(self, loader, tmp_path):
        """Test auto-detection of context files."""
        # Create a README
        readme = tmp_path / "README.md"
        readme.write_text("# Project")

        loaded = loader.auto_detect_context()

        assert loader.auto_detect_complete
        # May not find files depending on directory structure

    def test_add_context_file(self, loader, tmp_path):
        """Test adding a context file."""
        test_file = tmp_path / "test.md"
        test_file.write_text("Test content")

        result = loader.add_context_file(str(test_file))

        assert result is not None
        assert result.filename == "test.md"
        assert len(loader.loaded_context) == 1

    def test_add_missing_file(self, loader):
        """Test adding a file that doesn't exist."""
        result = loader.add_context_file("/nonexistent/file.md")

        assert result is None


class TestContextManagement:
    """Tests for context management."""

    def test_remove_context(self, loader, tmp_path):
        """Test removing a context file."""
        test_file = tmp_path / "test.md"
        test_file.write_text("Content")

        loader.add_context_file(str(test_file))
        assert len(loader.loaded_context) == 1

        success = loader.remove_context_file("test.md")

        assert success
        assert len(loader.loaded_context) == 0

    def test_remove_missing_file(self, loader):
        """Test removing a file that's not in context."""
        success = loader.remove_context_file("nonexistent.md")

        assert not success

    def test_get_loaded_files(self, loader, tmp_path):
        """Test getting list of loaded files."""
        test_file = tmp_path / "test.md"
        test_file.write_text("Content")

        loader.add_context_file(str(test_file))
        files = loader.get_loaded_files()

        assert len(files) == 1
        assert files[0]["filename"] == "test.md"


class TestContextSummary:
    """Tests for context summaries."""

    def test_context_summary_empty(self, loader):
        """Test summary with no context."""
        summary = loader.get_context_summary()

        assert "No context loaded" in summary

    def test_context_summary_with_files(self, loader, tmp_path):
        """Test summary with loaded files."""
        test_file = tmp_path / "test.md"
        test_file.write_text("Content")

        loader.add_context_file(str(test_file))
        summary = loader.get_context_summary()

        assert "Context Loaded: 1 files" in summary
        assert "test.md" in summary


class TestContextForPrompt:
    """Tests for context formatting for prompts."""

    def test_context_for_prompt_empty(self, loader):
        """Test prompt context when empty."""
        prompt = loader.get_context_for_prompt()

        assert prompt == ""

    def test_context_for_prompt_with_files(self, loader, tmp_path):
        """Test prompt context with files."""
        test_file = tmp_path / "test.md"
        test_file.write_text("Test content")

        loader.add_context_file(str(test_file))
        prompt = loader.get_context_for_prompt()

        assert "PROJECT CONTEXT" in prompt
        assert "test.md" in prompt
        assert "Test content" in prompt


class TestContextSearch:
    """Tests for context search."""

    def test_search_context_by_filename(self, loader, tmp_path):
        """Test searching context by filename."""
        test_file = tmp_path / "architecture.md"
        test_file.write_text("Content")

        loader.add_context_file(str(test_file))
        results = loader.search_context("architecture")

        assert len(results) > 0

    def test_search_context_by_content(self, loader, tmp_path):
        """Test searching context by content."""
        test_file = tmp_path / "test.md"
        test_file.write_text("Looking for this keyword")

        loader.add_context_file(str(test_file))
        results = loader.search_context("keyword")

        assert len(results) > 0

    def test_search_no_results(self, loader, tmp_path):
        """Test search with no results."""
        test_file = tmp_path / "test.md"
        test_file.write_text("Content")

        loader.add_context_file(str(test_file))
        results = loader.search_context("nonexistent")

        assert len(results) == 0


# Coverage targets
COVERAGE_TARGETS = {
    "Context Loading": "✅ 4 tests",
    "Context Management": "✅ 3 tests",
    "Context Summary": "✅ 2 tests",
    "Context For Prompt": "✅ 2 tests",
    "Context Search": "✅ 3 tests",
    "Total Tests": "14 tests",
    "Target Coverage": "70%+"
}

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
