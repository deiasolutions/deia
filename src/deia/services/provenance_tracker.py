#!/usr/bin/env python3
"""
Provenance Tracker: Document version lineage tracking and gap detection.

Tracks document sources, versions, and detects missing versions.
Maintains complete version history and identifies lineage gaps.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import hashlib

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - PROVENANCE - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Document:
    """Represents a document with version history."""

    def __init__(self, doc_id: str, source: str, initial_version: str):
        """Initialize document."""
        self.doc_id = doc_id
        self.source = source
        self.versions: Dict[str, Dict] = {}
        self.created_at = datetime.utcnow().isoformat() + "Z"
        self.add_version(initial_version, "initial", {})

    def add_version(self, version: str, change_type: str, metadata: Dict = None):
        """Add version to document."""
        if metadata is None:
            metadata = {}

        self.versions[version] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "change_type": change_type,
            "metadata": metadata
        }

    def get_version_sequence(self) -> List[str]:
        """Get ordered list of versions."""
        # Try to parse version numbers
        versions = list(self.versions.keys())
        try:
            # Handle semver-like versions (1.0.0, 1.1.0, etc.)
            return sorted(versions, key=lambda v: tuple(map(int, v.split('.'))))
        except (ValueError, AttributeError):
            # Fallback to timestamp ordering
            return sorted(
                versions,
                key=lambda v: self.versions[v]['timestamp']
            )

    def detect_gaps(self) -> List[Tuple[str, str]]:
        """Detect missing versions in sequence."""
        gaps = []
        sequence = self.get_version_sequence()

        if len(sequence) < 2:
            return gaps

        for i in range(len(sequence) - 1):
            current = sequence[i]
            next_v = sequence[i + 1]

            # Check if versions are sequential (no gaps)
            try:
                curr_parts = list(map(int, current.split('.')))
                next_parts = list(map(int, next_v.split('.')))

                # Expected next version (increment patch by default)
                expected = list(curr_parts)
                expected[-1] += 1

                if next_parts != expected and next_parts != [expected[0], 0, 1]:
                    gaps.append((current, next_v))
            except (ValueError, IndexError):
                continue

        return gaps

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "doc_id": self.doc_id,
            "source": self.source,
            "created_at": self.created_at,
            "versions": self.versions,
            "version_count": len(self.versions)
        }


class ProvenanceTracker:
    """Track document provenance and detect gaps."""

    def __init__(self, project_root: Path = None):
        """Initialize provenance tracker."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.provenance_db = project_root / ".deia" / "provenance" / "documents.jsonl"
        self.gap_report = project_root / ".deia" / "reports" / "provenance-gaps.jsonl"
        self.documents: Dict[str, Document] = {}

        # Ensure directories exist
        self.provenance_db.parent.mkdir(parents=True, exist_ok=True)
        self.gap_report.parent.mkdir(parents=True, exist_ok=True)

        # Load existing documents
        self.load_documents()

        logger.info(f"Provenance tracker initialized with {len(self.documents)} documents")

    def load_documents(self):
        """Load documents from database."""
        if not self.provenance_db.exists():
            return

        try:
            with open(self.provenance_db, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        doc = Document(
                            data['doc_id'],
                            data['source'],
                            list(data['versions'].keys())[0]
                        )
                        doc.versions = data['versions']
                        doc.created_at = data['created_at']
                        self.documents[doc.doc_id] = doc
                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error(f"Failed to load document: {e}")
        except Exception as e:
            logger.error(f"Failed to load documents: {e}")

    def track_document(self, doc_id: str, source: str, version: str, change_type: str = "update", metadata: Dict = None) -> bool:
        """Track a document version."""
        try:
            if doc_id not in self.documents:
                self.documents[doc_id] = Document(doc_id, source, version)
                logger.info(f"Created document: {doc_id}")
            else:
                self.documents[doc_id].add_version(version, change_type, metadata or {})
                logger.info(f"Added version {version} to {doc_id}")

            # Persist
            self._save_document(doc_id)
            return True

        except Exception as e:
            logger.error(f"Failed to track document {doc_id}: {e}")
            return False

    def _save_document(self, doc_id: str):
        """Save document to database."""
        if doc_id not in self.documents:
            return

        try:
            with open(self.provenance_db, 'a', encoding='utf-8') as f:
                doc = self.documents[doc_id]
                f.write(json.dumps(doc.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Failed to save document {doc_id}: {e}")

    def get_lineage(self, doc_id: str) -> Optional[List[str]]:
        """Get version lineage for document."""
        if doc_id not in self.documents:
            return None
        return self.documents[doc_id].get_version_sequence()

    def detect_all_gaps(self) -> Dict[str, List[Tuple[str, str]]]:
        """Detect gaps in all documents."""
        gaps = {}
        for doc_id, doc in self.documents.items():
            doc_gaps = doc.detect_gaps()
            if doc_gaps:
                gaps[doc_id] = doc_gaps
        return gaps

    def generate_gap_report(self) -> Dict:
        """Generate comprehensive gap report."""
        gaps = self.detect_all_gaps()

        report = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_documents": len(self.documents),
            "documents_with_gaps": len(gaps),
            "gaps_by_document": gaps
        }

        # Write report
        try:
            with open(self.gap_report, 'a', encoding='utf-8') as f:
                f.write(json.dumps(report) + '\n')
            logger.info(f"Gap report written: {len(gaps)} documents with gaps")
        except Exception as e:
            logger.error(f"Failed to write gap report: {e}")

        return report

    def get_document_info(self, doc_id: str) -> Optional[Dict]:
        """Get complete information about document."""
        if doc_id not in self.documents:
            return None

        doc = self.documents[doc_id]
        return {
            "doc_id": doc.doc_id,
            "source": doc.source,
            "created_at": doc.created_at,
            "version_count": len(doc.versions),
            "versions": list(doc.get_version_sequence()),
            "gaps": doc.detect_gaps(),
            "latest_version": doc.get_version_sequence()[-1] if doc.versions else None
        }

    def get_source_documents(self, source: str) -> List[str]:
        """Get all documents from given source."""
        return [
            doc_id for doc_id, doc in self.documents.items()
            if doc.source == source
        ]

    def query_lineage(self, doc_id: str, start_version: Optional[str] = None) -> List[Dict]:
        """Query version lineage with details."""
        if doc_id not in self.documents:
            return []

        doc = self.documents[doc_id]
        sequence = doc.get_version_sequence()

        # Filter by start version if provided
        if start_version:
            try:
                idx = sequence.index(start_version)
                sequence = sequence[idx:]
            except ValueError:
                return []

        result = []
        for version in sequence:
            version_info = doc.versions[version]
            result.append({
                "version": version,
                "timestamp": version_info['timestamp'],
                "change_type": version_info['change_type'],
                "metadata": version_info['metadata']
            })

        return result

    def export_provenance(self, output_file: Path) -> bool:
        """Export provenance data."""
        try:
            export_data = {
                "exported_at": datetime.utcnow().isoformat() + "Z",
                "total_documents": len(self.documents),
                "documents": {
                    doc_id: doc.to_dict()
                    for doc_id, doc in self.documents.items()
                }
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)

            logger.info(f"Provenance exported to {output_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to export provenance: {e}")
            return False


def main():
    """Entry point for provenance tracker."""
    tracker = ProvenanceTracker()

    # Example usage
    tracker.track_document("doc-001", "requirements", "1.0.0", "initial")
    tracker.track_document("doc-001", "requirements", "1.1.0", "update")
    tracker.track_document("doc-001", "requirements", "2.0.0", "major")

    # Generate report
    report = tracker.generate_gap_report()
    print(f"Gap Report: {json.dumps(report, indent=2)}")

    # Export
    tracker.export_provenance(Path("/tmp/provenance-export.json"))


if __name__ == "__main__":
    main()
