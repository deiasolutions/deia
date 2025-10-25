"""
Tests for DEIA context loading.
"""

import pytest
import tempfile
import json
from pathlib import Path
from deia.services.deia_context import DeiaContextLoader, DeiaMeta, DeiaBokIndex, DeiaContext


class TestDeiaContextLoader:
    """Test context loading."""

    def test_load_context_no_deia_dir(self):
        """Should return None for non-DEIA projects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            context = DeiaContextLoader.load_project_context(tmpdir)
            assert context is None

    def test_load_metadata_from_metadata_json(self):
        """Should load metadata from .deia/metadata.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            deia_dir = Path(tmpdir) / ".deia"
            deia_dir.mkdir()

            metadata = {
                "project_name": "test-project",
                "phase": "Phase 1",
                "team_members": ["Alice", "Bob"],
                "current_sprint": "Sprint 1",
            }

            with open(deia_dir / "metadata.json", "w") as f:
                json.dump(metadata, f)

            meta = DeiaContextLoader._load_metadata(tmpdir)

            assert meta is not None
            assert meta.project_name == "test-project"
            assert meta.phase == "Phase 1"
            assert "Alice" in meta.team_members

    def test_load_metadata_fallback_to_readme(self):
        """Should fallback to README if metadata.json missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            deia_dir = Path(tmpdir) / ".deia"
            deia_dir.mkdir()

            readme = Path(tmpdir) / "README.md"
            readme.write_text("# Test Project")

            meta = DeiaContextLoader._load_metadata(tmpdir)

            assert meta is not None
            assert meta.project_name is not None

    def test_load_bok_index(self):
        """Should load BOK index."""
        with tempfile.TemporaryDirectory() as tmpdir:
            deia_dir = Path(tmpdir) / ".deia"
            deia_dir.mkdir()

            index_dir = deia_dir / "index"
            index_dir.mkdir()

            # Create minimal index
            yaml_content = """
patterns:
  - id: pattern-1
    category: best_practices
  - id: pattern-2
    category: gotchas
"""
            with open(index_dir / "master-index.yaml", "w") as f:
                f.write(yaml_content)

            bok = DeiaContextLoader._load_bok_index(deia_dir)

            assert bok.total_patterns == 2
            assert "best_practices" in bok.categories

    def test_load_observations(self):
        """Should load recent observations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            deia_dir = Path(tmpdir) / ".deia"
            obs_dir = deia_dir / "observations"
            obs_dir.mkdir(parents=True)

            # Create observation files
            (obs_dir / "observation-1.md").write_text("Observation 1")
            (obs_dir / "observation-2.md").write_text("Observation 2")

            observations = DeiaContextLoader._load_observations(deia_dir)

            assert len(observations) >= 1

    def test_cache_behavior(self):
        """Should cache context appropriately."""
        with tempfile.TemporaryDirectory() as tmpdir:
            deia_dir = Path(tmpdir) / ".deia"
            deia_dir.mkdir()

            # Clear cache first
            DeiaContextLoader.clear_cache()

            # First load
            ctx1 = DeiaContextLoader.load_project_context(tmpdir)

            cache_info1 = DeiaContextLoader.get_cache_info()
            assert cache_info1["currsize"] >= 1

            # Second load (should be cached)
            ctx2 = DeiaContextLoader.load_project_context(tmpdir)

            # Should be same object
            assert ctx1 == ctx2

    def test_clear_cache(self):
        """Should clear cache correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            deia_dir = Path(tmpdir) / ".deia"
            deia_dir.mkdir()

            DeiaContextLoader.clear_cache()

            # Load
            DeiaContextLoader.load_project_context(tmpdir)
            cache_info1 = DeiaContextLoader.get_cache_info()
            assert cache_info1["currsize"] > 0

            # Clear
            DeiaContextLoader.clear_cache()
            cache_info2 = DeiaContextLoader.get_cache_info()
            assert cache_info2["currsize"] == 0


class TestDeiaMeta:
    """Test metadata class."""

    def test_create_metadata(self):
        """Should create metadata."""
        meta = DeiaMeta(
            project_name="test",
            project_path="/path",
            phase="Phase 1",
            team_members=["Alice", "Bob"],
        )

        assert meta.project_name == "test"
        assert "Alice" in meta.team_members


class TestDeiaBokIndex:
    """Test BOK index class."""

    def test_create_bok_index(self):
        """Should create BOK index."""
        bok = DeiaBokIndex(
            total_patterns=10,
            categories=["best_practices", "gotchas"],
            recent_patterns=["p1", "p2"],
        )

        assert bok.total_patterns == 10
        assert len(bok.categories) == 2
