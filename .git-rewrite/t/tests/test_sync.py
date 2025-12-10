"""
Unit tests for DEIA sync module.

Tests cover:
- YAML frontmatter parsing
- Version gap detection
- Provenance tracking
- File routing logic
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from deia.sync import DownloadsSyncer
from deia.sync_state import StateManager
from deia.sync_provenance import ProvenanceTracker


class TestFrontmatterParsing:
    """Test YAML frontmatter parsing functionality."""

    def test_parse_valid_frontmatter(self, tmp_path):
        """Test parsing valid YAML frontmatter."""
        # Create test file with valid frontmatter
        test_file = tmp_path / "test.md"
        content = """---
title: "Test Document"
version: "1.0"
deia_routing:
  project: "test-project"
  destination: "docs"
---

# Test Content
"""
        test_file.write_text(content, encoding='utf-8')

        # Create syncer with minimal config
        config = {
            'projects': {},
            'log_file': str(tmp_path / 'test.log'),
            'processed_folder': str(tmp_path / 'processed'),
            'error_folder': str(tmp_path / 'errors'),
        }
        syncer = DownloadsSyncer.__new__(DownloadsSyncer)
        syncer.config = config
        syncer._setup_logging()

        # Parse frontmatter
        result = syncer.parse_frontmatter(str(test_file))

        assert result is not None
        assert result['title'] == "Test Document"
        assert result['version'] == "1.0"
        assert result['deia_routing']['project'] == "test-project"
        assert result['deia_routing']['destination'] == "docs"

    def test_parse_missing_frontmatter(self, tmp_path):
        """Test parsing file without frontmatter."""
        test_file = tmp_path / "no-frontmatter.md"
        content = "# Just a heading\n\nNo frontmatter here."
        test_file.write_text(content, encoding='utf-8')

        config = {
            'projects': {},
            'log_file': str(tmp_path / 'test.log'),
            'processed_folder': str(tmp_path / 'processed'),
            'error_folder': str(tmp_path / 'errors'),
        }
        syncer = DownloadsSyncer.__new__(DownloadsSyncer)
        syncer.config = config
        syncer._setup_logging()

        result = syncer.parse_frontmatter(str(test_file))

        assert result is None

    def test_parse_malformed_frontmatter(self, tmp_path):
        """Test parsing malformed YAML frontmatter."""
        test_file = tmp_path / "malformed.md"
        content = """---
title: "Test
version: [invalid yaml
---

# Test Content
"""
        test_file.write_text(content, encoding='utf-8')

        config = {
            'projects': {},
            'log_file': str(tmp_path / 'test.log'),
            'processed_folder': str(tmp_path / 'processed'),
            'error_folder': str(tmp_path / 'errors'),
        }
        syncer = DownloadsSyncer.__new__(DownloadsSyncer)
        syncer.config = config
        syncer._setup_logging()

        result = syncer.parse_frontmatter(str(test_file))

        assert result is None


class TestVersionGapDetection:
    """Test version gap detection functionality."""

    def test_parse_semver(self):
        """Test semantic version parsing."""
        config = {'projects': {}}
        syncer = DownloadsSyncer.__new__(DownloadsSyncer)
        syncer.config = config

        # Test various version formats
        assert syncer._parse_semver("1.2.3") == (1, 2, 3)
        assert syncer._parse_semver("v1.2.3") == (1, 2, 3)
        assert syncer._parse_semver("2.0") == (2, 0, 0)
        assert syncer._parse_semver("v3") == (3, 0, 0)
        assert syncer._parse_semver("invalid") == (0, 0, 0)

    def test_extract_version_from_filename(self):
        """Test extracting version from filename."""
        config = {'projects': {}}
        syncer = DownloadsSyncer.__new__(DownloadsSyncer)
        syncer.config = config

        # Test version extraction
        assert syncer._extract_version_from_filename("doc-v1.2.md") == "1.2"
        assert syncer._extract_version_from_filename("doc-v1.2.3.md") == "1.2.3"
        assert syncer._extract_version_from_filename("doc-1.0.md") == "1.0"
        assert syncer._extract_version_from_filename("no-version.md") is None

    def test_version_gap_detection_major(self):
        """Test detection of major version gaps."""
        config = {'projects': {}}
        syncer = DownloadsSyncer.__new__(DownloadsSyncer)
        syncer.config = config

        # v1 -> v3 (missing v2)
        assert syncer._check_version_gap("3.0", "1.0") is True

        # v2 -> v5 (missing v3, v4)
        assert syncer._check_version_gap("5.0", "2.0") is True

        # v1 -> v2 (no gap)
        assert syncer._check_version_gap("2.0", "1.0") is False

    def test_version_gap_detection_minor(self):
        """Test detection of minor version gaps."""
        config = {'projects': {}}
        syncer = DownloadsSyncer.__new__(DownloadsSyncer)
        syncer.config = config

        # v1.0 -> v1.3 (missing v1.2)
        assert syncer._check_version_gap("1.3", "1.0") is True

        # v1.1 -> v1.2 (no gap)
        assert syncer._check_version_gap("1.2", "1.1") is False

        # v1.5 -> v1.6 (no gap)
        assert syncer._check_version_gap("1.6", "1.5") is False


class TestProvenanceTracking:
    """Test provenance tracking functionality."""

    def test_track_unsubmitted_draft(self, tmp_path):
        """Test creating provenance file for unsubmitted draft."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        config = {'projects': {}}
        tracker = ProvenanceTracker(config)

        replace_info = {
            'version': '2.0',
            'status': 'unsubmitted-draft',
            'reason': 'Superseded before submission',
            'note': 'Development changed direction',
            'superseded_date': '2025-10-11'
        }

        tracker.track_unsubmitted_draft(
            replace_info,
            str(project_path),
            "doc-v3.0.md"
        )

        # Check provenance file was created
        provenance_file = project_path / "docs" / "provenance" / "doc.provenance.md"
        assert provenance_file.exists()

        # Check content
        content = provenance_file.read_text(encoding='utf-8')
        assert "Document Provenance: doc.md" in content
        assert "v2.0" in content
        assert "UNSUBMITTED DRAFT" in content
        assert "Superseded before submission" in content
        assert "Development changed direction" in content


class TestStateManagement:
    """Test state persistence functionality."""

    def test_state_manager_creation(self, tmp_path):
        """Test creating state manager with default state."""
        state_file = tmp_path / "state.json"
        manager = StateManager(str(state_file))

        assert manager.state['processed_count'] == 0
        assert manager.state['errors_count'] == 0
        assert manager.state['last_processed_files'] == []
        assert manager.state['last_run'] is None

    def test_add_processed_file(self, tmp_path):
        """Test recording processed file."""
        state_file = tmp_path / "state.json"
        manager = StateManager(str(state_file))

        manager.add_processed_file("test.md")

        assert "test.md" in manager.state['last_processed_files']
        assert manager.state['processed_count'] == 1

        # Check file was saved
        assert state_file.exists()

    def test_was_file_processed(self, tmp_path):
        """Test checking if file was processed."""
        state_file = tmp_path / "state.json"
        manager = StateManager(str(state_file))

        assert manager.was_file_processed("test.md") is False

        manager.add_processed_file("test.md")

        assert manager.was_file_processed("test.md") is True

    def test_update_last_run(self, tmp_path):
        """Test updating last run timestamp."""
        state_file = tmp_path / "state.json"
        manager = StateManager(str(state_file))

        manager.update_last_run()

        assert manager.state['last_run'] is not None
        last_run_dt = manager.get_last_run_datetime()
        assert last_run_dt is not None
        assert isinstance(last_run_dt, datetime)


class TestFileRouting:
    """Test file routing logic."""

    def test_route_file_missing_frontmatter(self, tmp_path):
        """Test routing file without frontmatter."""
        test_file = tmp_path / "no-frontmatter.md"
        test_file.write_text("# Just content", encoding='utf-8')

        config = {
            'projects': {},
            'log_file': str(tmp_path / 'test.log'),
            'processed_folder': str(tmp_path / 'processed'),
            'error_folder': str(tmp_path / 'errors'),
        }
        state_manager = StateManager(str(tmp_path / 'state.json'))
        syncer = DownloadsSyncer.__new__(DownloadsSyncer)
        syncer.config = config
        syncer.state_manager = state_manager
        syncer._setup_logging()
        syncer._ensure_folders()

        success, message = syncer.route_file(str(test_file))

        assert success is False
        assert "No valid YAML frontmatter" in message

    def test_route_file_missing_deia_routing(self, tmp_path):
        """Test routing file without deia_routing section."""
        test_file = tmp_path / "no-routing.md"
        content = """---
title: "Test"
---

# Content
"""
        test_file.write_text(content, encoding='utf-8')

        config = {
            'projects': {},
            'log_file': str(tmp_path / 'test.log'),
            'processed_folder': str(tmp_path / 'processed'),
            'error_folder': str(tmp_path / 'errors'),
        }
        state_manager = StateManager(str(tmp_path / 'state.json'))
        syncer = DownloadsSyncer.__new__(DownloadsSyncer)
        syncer.config = config
        syncer.state_manager = state_manager
        syncer._setup_logging()
        syncer._ensure_folders()

        success, message = syncer.route_file(str(test_file))

        assert success is False
        assert "No deia_routing section" in message


# Pytest fixtures
@pytest.fixture
def tmp_path(tmp_path_factory):
    """Create temporary directory for tests."""
    return tmp_path_factory.mktemp("test_sync")
