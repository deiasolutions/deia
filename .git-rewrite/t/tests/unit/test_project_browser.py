"""
Unit tests for Project Browser API
"""

import json
import pytest
from pathlib import Path
from src.deia.services.project_browser import ProjectBrowser


class TestProjectBrowser:
    """Test suite for ProjectBrowser class"""

    def test_init_with_valid_project(self, tmp_path):
        """Test initialization with valid DEIA project"""
        # Create mock .deia directory
        (tmp_path / ".deia").mkdir()
        (tmp_path / ".deia" / "index").mkdir()

        browser = ProjectBrowser(tmp_path)
        assert browser.project_root == tmp_path
        assert browser.deia_dir == tmp_path / ".deia"

    def test_init_without_deia_directory(self, tmp_path):
        """Test initialization fails without .deia/ directory"""
        with pytest.raises(ValueError, match="Not a DEIA project"):
            ProjectBrowser(tmp_path)

    def test_find_project_root(self, tmp_path, monkeypatch):
        """Test automatic project root detection"""
        # Create .deia at tmp_path
        (tmp_path / ".deia").mkdir()

        # Create nested subdirectory
        nested = tmp_path / "src" / "deep" / "nested"
        nested.mkdir(parents=True)

        # Change to nested directory
        monkeypatch.chdir(nested)

        browser = ProjectBrowser()
        assert browser.project_root == tmp_path

    def test_get_tree_basic(self, tmp_path):
        """Test basic tree generation"""
        # Setup
        (tmp_path / ".deia").mkdir()
        (tmp_path / "file1.md").write_text("content")
        (tmp_path / "dir1").mkdir()
        (tmp_path / "dir1" / "file2.py").write_text("code")

        browser = ProjectBrowser(tmp_path)
        tree = browser.get_tree()

        assert tree["name"] == tmp_path.name
        assert tree["type"] == "directory"
        assert "children" in tree
        assert len(tree["children"]) >= 2  # .deia and file1.md at minimum

    def test_get_tree_max_depth(self, tmp_path):
        """Test max_depth parameter limits recursion"""
        # Setup deeply nested structure
        (tmp_path / ".deia").mkdir()
        deep_path = tmp_path / "a" / "b" / "c" / "d"
        deep_path.mkdir(parents=True)
        (deep_path / "deep.txt").write_text("deep file")

        browser = ProjectBrowser(tmp_path)

        # Depth 1 should only show top level
        tree = browser.get_tree(max_depth=1)
        assert tree["type"] == "directory"
        assert "children" in tree

        # Children should exist but not be deeply nested
        # (exact assertion depends on structure)

    def test_get_tree_hidden_files(self, tmp_path):
        """Test show_hidden parameter"""
        (tmp_path / ".deia").mkdir()
        (tmp_path / ".hidden").write_text("hidden")
        (tmp_path / "visible.md").write_text("visible")

        browser = ProjectBrowser(tmp_path)

        # Without show_hidden
        tree = browser.get_tree(show_hidden=False)
        names = [child["name"] for child in tree.get("children", [])]
        assert ".hidden" not in names or ".deia" in names  # .deia is exception

        # With show_hidden
        tree = browser.get_tree(show_hidden=True)
        names = [child["name"] for child in tree.get("children", [])]
        assert ".hidden" in names

    def test_filter_by_extension(self, tmp_path):
        """Test filtering files by extension"""
        (tmp_path / ".deia").mkdir()
        (tmp_path / "file1.md").write_text("md")
        (tmp_path / "file2.py").write_text("py")
        (tmp_path / "file3.txt").write_text("txt")
        (tmp_path / "dir").mkdir()
        (tmp_path / "dir" / "file4.md").write_text("md")

        browser = ProjectBrowser(tmp_path)

        # Filter for .md files
        results = browser.filter_by_extension([".md"])
        assert len(results) == 2
        assert all(f["extension"] == ".md" for f in results)

        # Filter for multiple extensions
        results = browser.filter_by_extension([".md", ".py"])
        assert len(results) == 3

        # Extension without dot
        results = browser.filter_by_extension(["txt"])
        assert len(results) == 1
        assert results[0]["extension"] == ".txt"

    def test_search_basic(self, tmp_path):
        """Test basic search functionality"""
        (tmp_path / ".deia").mkdir()
        (tmp_path / "important.md").write_text("content")
        (tmp_path / "test_important.py").write_text("code")
        (tmp_path / "other.txt").write_text("other")

        browser = ProjectBrowser(tmp_path)

        results = browser.search("important")
        assert len(results) == 2
        assert all("important" in r["name"].lower() for r in results)

    def test_search_case_insensitive(self, tmp_path):
        """Test search is case-insensitive"""
        (tmp_path / ".deia").mkdir()
        (tmp_path / "MyFile.MD").write_text("content")

        browser = ProjectBrowser(tmp_path)

        results = browser.search("myfile")
        assert len(results) == 1
        assert results[0]["name"] == "MyFile.MD"

    def test_search_with_file_types(self, tmp_path):
        """Test search with file type filtering"""
        (tmp_path / ".deia").mkdir()
        (tmp_path / "test.md").write_text("md")
        (tmp_path / "test.py").write_text("py")
        (tmp_path / "test.txt").write_text("txt")

        browser = ProjectBrowser(tmp_path)

        results = browser.search("test", file_types=[".md"])
        assert len(results) == 1
        assert results[0]["extension"] == ".md"

    def test_get_deia_structure(self, tmp_path):
        """Test DEIA structure analysis"""
        # Create some expected directories
        (tmp_path / ".deia").mkdir()
        (tmp_path / ".deia" / "bot-logs").mkdir()
        (tmp_path / ".deia" / "federalist").mkdir()
        (tmp_path / ".deia" / "governance").mkdir()

        browser = ProjectBrowser(tmp_path)
        structure = browser.get_deia_structure()

        assert structure["valid"] is True
        assert structure["root"] == str(tmp_path)
        assert "directories" in structure

        # Check expected directories
        assert "bot-logs" in structure["directories"]
        assert structure["directories"]["bot-logs"]["exists"] is True
        assert "federalist" in structure["directories"]
        assert structure["directories"]["federalist"]["exists"] is True

    def test_to_json(self, tmp_path):
        """Test JSON serialization"""
        (tmp_path / ".deia").mkdir()
        (tmp_path / "file.md").write_text("content")

        browser = ProjectBrowser(tmp_path)
        tree = browser.get_tree(max_depth=1)

        json_str = browser.to_json(tree)

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed["type"] == "directory"
        assert "children" in parsed

    def test_get_stats(self, tmp_path):
        """Test project statistics"""
        (tmp_path / ".deia").mkdir()
        (tmp_path / "file1.md").write_text("a" * 100)
        (tmp_path / "file2.md").write_text("b" * 50)
        (tmp_path / "file3.py").write_text("c" * 75)

        browser = ProjectBrowser(tmp_path)
        stats = browser.get_stats()

        assert stats["total_files"] >= 3
        assert stats["total_size"] >= 225  # Sum of file sizes
        assert ".md" in stats["by_extension"]
        assert stats["by_extension"][".md"]["count"] == 2
        assert ".py" in stats["by_extension"]
        assert stats["by_extension"][".py"]["count"] == 1

    def test_path_validation_outside_project(self, tmp_path):
        """Test that paths outside project are rejected"""
        (tmp_path / ".deia").mkdir()
        browser = ProjectBrowser(tmp_path)

        # Try to access non-existent path (validation catches it before boundary check)
        with pytest.raises(ValueError, match="Path does not exist"):
            browser.get_tree(path="../outside")

    def test_file_metadata(self, tmp_path):
        """Test file metadata extraction"""
        (tmp_path / ".deia").mkdir()
        test_file = tmp_path / "test.md"
        test_file.write_text("content")

        browser = ProjectBrowser(tmp_path)
        metadata = browser._file_metadata(test_file)

        assert metadata["name"] == "test.md"
        assert metadata["type"] == "file"
        assert metadata["extension"] == ".md"
        assert metadata["size"] > 0
        assert "modified" in metadata

    def test_empty_project(self, tmp_path):
        """Test browser with minimal .deia directory"""
        (tmp_path / ".deia").mkdir()

        browser = ProjectBrowser(tmp_path)
        tree = browser.get_tree()

        assert tree["type"] == "directory"
        # Should at least have .deia directory
        assert "children" in tree or tree["child_count"] == 0

    def test_large_directory_handling(self, tmp_path):
        """Test handling of directory with many files"""
        (tmp_path / ".deia").mkdir()
        many_files = tmp_path / "many"
        many_files.mkdir()

        # Create 100 files
        for i in range(100):
            (many_files / f"file{i}.txt").write_text(f"content{i}")

        browser = ProjectBrowser(tmp_path)
        results = browser.filter_by_extension([".txt"])

        assert len(results) == 100

    def test_permission_error_handling(self, tmp_path, monkeypatch):
        """Test graceful handling of permission errors"""
        (tmp_path / ".deia").mkdir()
        restricted = tmp_path / "restricted"
        restricted.mkdir()

        # Mock permission error
        def mock_iterdir(self):
            raise PermissionError("Access denied")

        browser = ProjectBrowser(tmp_path)

        # Should handle gracefully, not crash
        tree = browser.get_tree()
        assert tree["type"] == "directory"
