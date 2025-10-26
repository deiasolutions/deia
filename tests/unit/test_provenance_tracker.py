#!/usr/bin/env python3
"""Tests for Provenance Tracker."""

import json
import tempfile
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.provenance_tracker import Document, ProvenanceTracker


class TestDocument:
    """Test Document class."""

    def test_document_creation(self):
        """Test creating document."""
        doc = Document("doc-001", "requirements", "1.0.0")
        assert doc.doc_id == "doc-001"
        assert doc.source == "requirements"
        assert "1.0.0" in doc.versions

    def test_add_version(self):
        """Test adding versions."""
        doc = Document("doc-001", "requirements", "1.0.0")
        doc.add_version("1.1.0", "update", {"author": "Alice"})
        doc.add_version("1.2.0", "update", {"author": "Bob"})

        assert len(doc.versions) == 3
        assert "1.1.0" in doc.versions
        assert "1.2.0" in doc.versions

    def test_version_sequence(self):
        """Test version sequencing."""
        doc = Document("doc-001", "requirements", "2.0.0")
        doc.add_version("1.0.0", "backport")
        doc.add_version("1.5.0", "backport")

        sequence = doc.get_version_sequence()
        assert sequence == ["1.0.0", "1.5.0", "2.0.0"]

    def test_gap_detection_no_gaps(self):
        """Test gap detection with sequential versions."""
        doc = Document("doc-001", "spec", "1.0.0")
        doc.add_version("1.1.0", "update")
        doc.add_version("1.2.0", "update")
        doc.add_version("2.0.0", "major")

        gaps = doc.detect_gaps()
        assert len(gaps) == 0

    def test_gap_detection_with_gaps(self):
        """Test gap detection with missing versions."""
        doc = Document("doc-001", "spec", "1.0.0")
        doc.add_version("1.2.0", "update")  # Gap: 1.1.0 missing
        doc.add_version("1.5.0", "update")  # Gap: 1.3.0, 1.4.0 missing

        gaps = doc.detect_gaps()
        assert len(gaps) > 0

    def test_to_dict(self):
        """Test document serialization."""
        doc = Document("doc-001", "requirements", "1.0.0")
        doc.add_version("1.1.0", "update")

        data = doc.to_dict()
        assert data["doc_id"] == "doc-001"
        assert data["source"] == "requirements"
        assert data["version_count"] == 2


class TestProvenanceTracker:
    """Test ProvenanceTracker class."""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".deia" / "provenance").mkdir(parents=True, exist_ok=True)
            (project_root / ".deia" / "reports").mkdir(parents=True, exist_ok=True)
            yield project_root

    def test_tracker_initialization(self, temp_project):
        """Test tracker initialization."""
        tracker = ProvenanceTracker(temp_project)
        assert tracker.project_root == temp_project
        assert len(tracker.documents) == 0

    def test_track_document(self, temp_project):
        """Test tracking document."""
        tracker = ProvenanceTracker(temp_project)

        result = tracker.track_document("doc-001", "requirements", "1.0.0", "initial")
        assert result is True
        assert "doc-001" in tracker.documents

    def test_add_versions(self, temp_project):
        """Test adding multiple versions."""
        tracker = ProvenanceTracker(temp_project)

        tracker.track_document("doc-001", "requirements", "1.0.0")
        tracker.track_document("doc-001", "requirements", "1.1.0", "update")
        tracker.track_document("doc-001", "requirements", "1.2.0", "update")

        doc = tracker.documents["doc-001"]
        assert len(doc.versions) == 3

    def test_get_lineage(self, temp_project):
        """Test getting version lineage."""
        tracker = ProvenanceTracker(temp_project)

        tracker.track_document("doc-001", "spec", "2.0.0")
        tracker.track_document("doc-001", "spec", "1.0.0", "backport")
        tracker.track_document("doc-001", "spec", "1.5.0", "backport")

        lineage = tracker.get_lineage("doc-001")
        assert lineage == ["1.0.0", "1.5.0", "2.0.0"]

    def test_detect_gaps(self, temp_project):
        """Test gap detection."""
        tracker = ProvenanceTracker(temp_project)

        tracker.track_document("doc-001", "spec", "1.0.0")
        tracker.track_document("doc-001", "spec", "1.2.0")  # Gap: 1.1.0
        tracker.track_document("doc-001", "spec", "2.0.0")  # Gap: 1.3.0-1.9.0

        gaps = tracker.detect_all_gaps()
        assert "doc-001" in gaps
        assert len(gaps["doc-001"]) > 0

    def test_get_document_info(self, temp_project):
        """Test getting document info."""
        tracker = ProvenanceTracker(temp_project)

        tracker.track_document("doc-001", "requirements", "1.0.0")
        tracker.track_document("doc-001", "requirements", "1.1.0")

        info = tracker.get_document_info("doc-001")
        assert info["doc_id"] == "doc-001"
        assert info["source"] == "requirements"
        assert info["version_count"] == 2
        assert info["latest_version"] == "1.1.0"

    def test_get_source_documents(self, temp_project):
        """Test querying documents by source."""
        tracker = ProvenanceTracker(temp_project)

        tracker.track_document("doc-001", "requirements", "1.0.0")
        tracker.track_document("doc-002", "requirements", "1.0.0")
        tracker.track_document("doc-003", "design", "1.0.0")

        req_docs = tracker.get_source_documents("requirements")
        design_docs = tracker.get_source_documents("design")

        assert len(req_docs) == 2
        assert len(design_docs) == 1

    def test_query_lineage(self, temp_project):
        """Test querying lineage."""
        tracker = ProvenanceTracker(temp_project)

        tracker.track_document("doc-001", "spec", "1.0.0", "initial")
        tracker.track_document("doc-001", "spec", "1.1.0", "update")
        tracker.track_document("doc-001", "spec", "1.2.0", "update")

        # Query full lineage
        full = tracker.query_lineage("doc-001")
        assert len(full) == 3

        # Query from 1.1.0
        partial = tracker.query_lineage("doc-001", "1.1.0")
        assert len(partial) == 2
        assert partial[0]["version"] == "1.1.0"

    def test_export_provenance(self, temp_project):
        """Test exporting provenance."""
        tracker = ProvenanceTracker(temp_project)

        tracker.track_document("doc-001", "requirements", "1.0.0")
        tracker.track_document("doc-001", "requirements", "1.1.0")

        export_file = temp_project / "export.json"
        result = tracker.export_provenance(export_file)

        assert result is True
        assert export_file.exists()

        with open(export_file) as f:
            data = json.load(f)

        assert data["total_documents"] == 1
        assert "doc-001" in data["documents"]

    def test_gap_report_generation(self, temp_project):
        """Test gap report generation."""
        tracker = ProvenanceTracker(temp_project)

        tracker.track_document("doc-001", "spec", "1.0.0")
        tracker.track_document("doc-001", "spec", "1.2.0")  # Gap

        report = tracker.generate_gap_report()

        assert report["total_documents"] == 1
        assert report["documents_with_gaps"] == 1
        assert "doc-001" in report["gaps_by_document"]

    def test_multiple_documents(self, temp_project):
        """Test tracking multiple documents."""
        tracker = ProvenanceTracker(temp_project)

        # Document 1
        tracker.track_document("doc-001", "requirements", "1.0.0")
        tracker.track_document("doc-001", "requirements", "1.1.0")

        # Document 2
        tracker.track_document("doc-002", "design", "1.0.0")
        tracker.track_document("doc-002", "design", "2.0.0")

        assert len(tracker.documents) == 2
        assert tracker.get_document_info("doc-001")["version_count"] == 2
        assert tracker.get_document_info("doc-002")["version_count"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
