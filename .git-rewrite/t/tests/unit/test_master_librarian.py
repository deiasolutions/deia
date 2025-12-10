"""
Tests for Master Librarian - BOK Curation System

Test Coverage:
- Initialization and setup
- Submission review workflow
- Quality validation
- Duplicate detection
- PII/secrets detection
- Integration workflow
- Index management
- Search functionality
- Pattern deprecation
- Statistics

Author: CLAUDE-CODE-004
Created: 2025-10-18
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from deia.services.master_librarian import (
    MasterLibrarian,
    SubmissionStatus,
    ConfidenceLevel,
    PatternCategory,
    SubmissionMetadata,
    IndexEntry,
    ReviewResult,
    review_submission_cli,
    integrate_submission_cli,
    search_bok_cli,
)


@pytest.fixture
def temp_project():
    """Create temporary project structure for testing"""
    temp_dir = Path(tempfile.mkdtemp())

    # Create DEIA structure
    deia_dir = temp_dir / ".deia"
    deia_dir.mkdir()
    (deia_dir / "intake").mkdir()
    (deia_dir / "index").mkdir()
    (deia_dir / "observations").mkdir()

    # Create BOK structure
    bok_dir = temp_dir / "bok"
    bok_dir.mkdir()
    (bok_dir / "patterns").mkdir()
    (bok_dir / "anti-patterns").mkdir()
    (bok_dir / "processes").mkdir()

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def librarian(temp_project):
    """Create MasterLibrarian instance for testing"""
    return MasterLibrarian(project_root=temp_project)


@pytest.fixture
def sample_manifest():
    """Sample MANIFEST.md content"""
    return """# Submission Manifest

**Title:** Pattern: Git Workflow for Multi-Agent Collaboration
**Category:** Process
**Tags:** git, collaboration, multi-agent, coordination
**Author:** CLAUDE-CODE-002
**Date:** 2025-10-18
**Confidence:** Validated
**Source Project:** deiasolutions
**Platform:** Platform-Agnostic

**Summary:**
Describes a git workflow optimized for multiple AI agents working simultaneously on the same repository.

**Why this is valuable:**
Reduces merge conflicts by 80% in multi-agent environments.
"""


@pytest.fixture
def sample_submission_content():
    """Sample submission content"""
    return """# Git Workflow for Multi-Agent Collaboration

## Overview
This pattern describes a git workflow optimized for multiple AI agents.

## Problem
Multiple agents working on the same repository can cause merge conflicts.

## Solution
Use feature branches with clear naming conventions.

## Example
```bash
git checkout -b agent-001-feature-name
git commit -m "feat: implement feature"
git push origin agent-001-feature-name
```

## Benefits
- Reduces conflicts
- Clear attribution
- Easy rollback

## Trade-offs
- More branches to manage
- Requires coordination
"""


class TestInitialization:
    """Test MasterLibrarian initialization"""

    def test_init_with_explicit_root(self, temp_project):
        """Test initialization with explicit project root"""
        librarian = MasterLibrarian(project_root=temp_project)

        assert librarian.project_root == temp_project
        assert librarian.deia_dir == temp_project / ".deia"
        assert librarian.intake_dir == temp_project / ".deia" / "intake"
        assert librarian.bok_dir == temp_project / "bok"

    def test_init_creates_directories(self, temp_project):
        """Test that initialization creates required directories"""
        librarian = MasterLibrarian(project_root=temp_project)

        assert librarian.intake_dir.exists()
        assert librarian.bok_dir.exists()
        assert (librarian.bok_dir / "patterns").exists()
        assert (librarian.bok_dir / "anti-patterns").exists()
        assert (librarian.deia_dir / "index").exists()

    def test_init_loads_empty_index(self, temp_project):
        """Test initialization with empty index"""
        librarian = MasterLibrarian(project_root=temp_project)

        assert isinstance(librarian.index, list)
        assert len(librarian.index) == 0

    def test_init_loads_existing_index(self, temp_project, librarian):
        """Test initialization loads existing index"""
        # Create an entry
        entry = IndexEntry(
            id="test-pattern",
            path="bok\\patterns\\test.md",
            title="Test Pattern",
            category="Pattern",
            tags=["test"],
            confidence="Experimental",
            date="2025-10-18",
            created_by="test",
            summary="Test pattern"
        )
        librarian.index.append(entry)
        librarian._save_index()

        # Create new librarian instance
        librarian2 = MasterLibrarian(project_root=temp_project)

        assert len(librarian2.index) == 1
        assert librarian2.index[0].id == "test-pattern"


class TestSubmissionReview:
    """Test submission review functionality"""

    def test_review_missing_submission(self, librarian):
        """Test review of non-existent submission"""
        result = librarian.review_submission("2025-10-18/nonexistent/pattern.md")

        assert result.status == SubmissionStatus.REJECTED
        assert "not found" in result.reason.lower()

    def test_review_missing_manifest(self, librarian, temp_project):
        """Test review with missing MANIFEST.md"""
        # Create submission without manifest
        intake_dir = temp_project / ".deia" / "intake" / "2025-10-18" / "test"
        intake_dir.mkdir(parents=True)
        submission = intake_dir / "pattern.md"
        submission.write_text("Test content")

        result = librarian.review_submission("2025-10-18/test/pattern.md")

        assert result.status in [SubmissionStatus.REJECTED, SubmissionStatus.REVISION_REQUESTED]
        assert any("MANIFEST" in issue for issue in result.issues)

    def test_review_valid_submission(self, librarian, temp_project, sample_manifest, sample_submission_content):
        """Test review of valid submission"""
        # Create submission with manifest
        intake_dir = temp_project / ".deia" / "intake" / "2025-10-18" / "test"
        intake_dir.mkdir(parents=True)
        (intake_dir / "MANIFEST.md").write_text(sample_manifest)
        (intake_dir / "pattern.md").write_text(sample_submission_content)

        result = librarian.review_submission("2025-10-18/test/pattern.md")

        assert result.status == SubmissionStatus.ACCEPTED
        assert result.approved_path is not None
        assert len(result.issues) == 0

    def test_review_short_submission(self, librarian, temp_project, sample_manifest):
        """Test review of very short submission"""
        intake_dir = temp_project / ".deia" / "intake" / "2025-10-18" / "test"
        intake_dir.mkdir(parents=True)
        (intake_dir / "MANIFEST.md").write_text(sample_manifest)
        (intake_dir / "pattern.md").write_text("Short content")

        result = librarian.review_submission("2025-10-18/test/pattern.md")

        assert any("short" in issue.lower() for issue in result.issues)

    def test_review_detects_pii_email(self, librarian, temp_project, sample_manifest):
        """Test PII detection - email addresses"""
        intake_dir = temp_project / ".deia" / "intake" / "2025-10-18" / "test"
        intake_dir.mkdir(parents=True)
        (intake_dir / "MANIFEST.md").write_text(sample_manifest)
        (intake_dir / "pattern.md").write_text("Contact: user@example.com for more info")

        result = librarian.review_submission("2025-10-18/test/pattern.md")

        assert result.status == SubmissionStatus.BLOCKED
        assert "PII" in result.reason or "secrets" in result.reason

    def test_review_detects_secrets_api_key(self, librarian, temp_project, sample_manifest):
        """Test secrets detection - API keys"""
        intake_dir = temp_project / ".deia" / "intake" / "2025-10-18" / "test"
        intake_dir.mkdir(parents=True)
        (intake_dir / "MANIFEST.md").write_text(sample_manifest)
        (intake_dir / "pattern.md").write_text("API_KEY=sk_test_FAKE_KEY_FOR_TESTING")

        result = librarian.review_submission("2025-10-18/test/pattern.md")

        assert result.status == SubmissionStatus.BLOCKED

    def test_review_detects_duplicate(self, librarian, temp_project, sample_manifest, sample_submission_content):
        """Test duplicate pattern detection"""
        # Add existing pattern to index
        existing = IndexEntry(
            id="git-workflow-multi-agent",
            path="bok\\patterns\\git-workflow.md",
            title="Pattern: Git Workflow for Multi-Agent Collaboration",
            category="Process",
            tags=["git", "collaboration"],
            confidence="Validated",
            date="2025-10-17",
            created_by="test",
            summary="Git workflow for multi-agent teams"
        )
        librarian.index.append(existing)

        # Try to submit similar pattern
        intake_dir = temp_project / ".deia" / "intake" / "2025-10-18" / "test"
        intake_dir.mkdir(parents=True)
        (intake_dir / "MANIFEST.md").write_text(sample_manifest)
        (intake_dir / "pattern.md").write_text(sample_submission_content)

        result = librarian.review_submission("2025-10-18/test/pattern.md")

        assert result.status == SubmissionStatus.REJECTED
        assert "duplicate" in result.reason.lower()


class TestManifestParsing:
    """Test MANIFEST.md parsing"""

    def test_parse_valid_manifest(self, librarian, temp_project, sample_manifest):
        """Test parsing valid manifest"""
        manifest_path = temp_project / "test_manifest.md"
        manifest_path.write_text(sample_manifest)

        metadata = librarian._parse_manifest(manifest_path)

        assert metadata.title == "Pattern: Git Workflow for Multi-Agent Collaboration"
        assert metadata.category == "Process"
        assert "git" in metadata.tags
        assert metadata.author == "CLAUDE-CODE-002"
        assert metadata.confidence == "Validated"

    def test_parse_manifest_missing_required_field(self, librarian, temp_project):
        """Test parsing manifest with missing required field"""
        manifest_content = """# Submission Manifest

**Category:** Process
**Tags:** test
**Author:** test
**Date:** 2025-10-18
**Summary:** Test
"""
        manifest_path = temp_project / "test_manifest.md"
        manifest_path.write_text(manifest_content)

        with pytest.raises(ValueError, match="Missing required field"):
            librarian._parse_manifest(manifest_path)

    def test_parse_manifest_with_defaults(self, librarian, temp_project):
        """Test manifest parsing uses defaults for optional fields"""
        manifest_content = """# Submission Manifest

**Title:** Test Pattern
**Category:** Pattern
**Tags:** test
**Author:** test
**Date:** 2025-10-18
**Summary:** Test pattern
"""
        manifest_path = temp_project / "test_manifest.md"
        manifest_path.write_text(manifest_content)

        metadata = librarian._parse_manifest(manifest_path)

        assert metadata.confidence == ConfidenceLevel.EXPERIMENTAL.value
        assert metadata.platform == "Platform-Agnostic"


class TestDuplicateDetection:
    """Test duplicate pattern detection"""

    def test_find_duplicate_exact_title(self, librarian):
        """Test finding duplicate by exact title"""
        librarian.index.append(IndexEntry(
            id="test", path="test", title="Test Pattern", category="Pattern",
            tags=[], confidence="Experimental", date="2025-10-18",
            created_by="test", summary="Test"
        ))

        duplicate = librarian._find_duplicate("Test Pattern", [])

        assert duplicate is not None
        assert duplicate.title == "Test Pattern"

    def test_find_duplicate_case_insensitive(self, librarian):
        """Test duplicate detection is case-insensitive"""
        librarian.index.append(IndexEntry(
            id="test", path="test", title="Test Pattern", category="Pattern",
            tags=[], confidence="Experimental", date="2025-10-18",
            created_by="test", summary="Test"
        ))

        duplicate = librarian._find_duplicate("test pattern", [])

        assert duplicate is not None

    def test_find_duplicate_by_tag_overlap(self, librarian):
        """Test finding duplicate requires both similar title AND high tag overlap"""
        librarian.index.append(IndexEntry(
            id="test", path="test", title="Git Workflow",
            category="Pattern", tags=["git", "collaboration", "workflow"],
            confidence="Experimental", date="2025-10-18",
            created_by="test", summary="Test"
        ))

        # Identical title - should find duplicate
        duplicate = librarian._find_duplicate(
            "Git Workflow",
            ["git", "collaboration"]
        )

        assert duplicate is not None

    def test_no_duplicate_when_different(self, librarian):
        """Test no duplicate found for different pattern"""
        librarian.index.append(IndexEntry(
            id="test", path="test", title="Git Pattern", category="Pattern",
            tags=["git"], confidence="Experimental", date="2025-10-18",
            created_by="test", summary="Test"
        ))

        duplicate = librarian._find_duplicate("Testing Pattern", ["testing", "qa"])

        assert duplicate is None


class TestIntegration:
    """Test submission integration"""

    def test_integrate_accepted_submission(self, librarian, temp_project, sample_manifest, sample_submission_content):
        """Test integrating accepted submission"""
        # Create submission
        intake_dir = temp_project / ".deia" / "intake" / "2025-10-18" / "test"
        intake_dir.mkdir(parents=True)
        (intake_dir / "MANIFEST.md").write_text(sample_manifest)
        (intake_dir / "pattern.md").write_text(sample_submission_content)

        # Review
        review_result = librarian.review_submission("2025-10-18/test/pattern.md")

        # Integrate
        entry = librarian.integrate_submission("2025-10-18/test/pattern.md", review_result)

        assert entry.id is not None
        assert entry.path.startswith("bok\\")
        assert entry.title == "Pattern: Git Workflow for Multi-Agent Collaboration"

        # Verify file copied to BOK
        bok_path = temp_project / entry.path
        assert bok_path.exists()

        # Verify added to index
        assert entry in librarian.index

        # Verify intake archived
        assert not (intake_dir / "pattern.md").exists()

    def test_integrate_rejected_submission_fails(self, librarian):
        """Test integrating rejected submission raises error"""
        review_result = ReviewResult(
            status=SubmissionStatus.REJECTED,
            reason="Test rejection"
        )

        with pytest.raises(ValueError, match="Cannot integrate"):
            librarian.integrate_submission("fake/path.md", review_result)

    def test_integrate_creates_index_entry(self, librarian, temp_project, sample_manifest, sample_submission_content):
        """Test integration creates proper index entry"""
        # Create submission
        intake_dir = temp_project / ".deia" / "intake" / "2025-10-18" / "test"
        intake_dir.mkdir(parents=True)
        (intake_dir / "MANIFEST.md").write_text(sample_manifest)
        (intake_dir / "pattern.md").write_text(sample_submission_content)

        # Review and integrate
        review_result = librarian.review_submission("2025-10-18/test/pattern.md")
        entry = librarian.integrate_submission("2025-10-18/test/pattern.md", review_result)

        # Reload index to verify persistence
        librarian2 = MasterLibrarian(project_root=temp_project)

        assert len(librarian2.index) == 1
        assert librarian2.index[0].id == entry.id


class TestSearch:
    """Test BOK search functionality"""

    def test_search_empty_index(self, librarian):
        """Test search on empty index"""
        results = librarian.search_bok("test")

        assert len(results) == 0

    def test_search_by_title(self, librarian):
        """Test search by title keyword"""
        librarian.index.append(IndexEntry(
            id="git-pattern", path="test", title="Git Workflow Pattern",
            category="Pattern", tags=["git"], confidence="Validated",
            date="2025-10-18", created_by="test", summary="Git workflow"
        ))

        results = librarian.search_bok("git")

        assert len(results) == 1
        assert results[0].id == "git-pattern"

    def test_search_by_summary(self, librarian):
        """Test search by summary content"""
        librarian.index.append(IndexEntry(
            id="test", path="test", title="Pattern", category="Pattern",
            tags=[], confidence="Experimental", date="2025-10-18",
            created_by="test", summary="Describes multi-agent collaboration"
        ))

        results = librarian.search_bok("collaboration")

        assert len(results) == 1

    def test_search_by_tags(self, librarian):
        """Test search by tags"""
        librarian.index.append(IndexEntry(
            id="test", path="test", title="Pattern", category="Pattern",
            tags=["deployment", "ci-cd"], confidence="Experimental",
            date="2025-10-18", created_by="test", summary="Test"
        ))

        results = librarian.search_bok("deployment")

        assert len(results) == 1

    def test_search_case_insensitive(self, librarian):
        """Test search is case-insensitive"""
        librarian.index.append(IndexEntry(
            id="test", path="test", title="Git Pattern", category="Pattern",
            tags=[], confidence="Experimental", date="2025-10-18",
            created_by="test", summary="Test"
        ))

        results = librarian.search_bok("GIT")

        assert len(results) == 1

    def test_search_filter_by_category(self, librarian):
        """Test filtering search by category"""
        librarian.index.extend([
            IndexEntry(
                id="pattern1", path="test1", title="Git Pattern",
                category="Pattern", tags=["git"], confidence="Experimental",
                date="2025-10-18", created_by="test", summary="Test"
            ),
            IndexEntry(
                id="anti1", path="test2", title="Git Anti-Pattern",
                category="Anti-Pattern", tags=["git"], confidence="Experimental",
                date="2025-10-18", created_by="test", summary="Test"
            )
        ])

        results = librarian.search_bok("git", category="Anti-Pattern")

        assert len(results) == 1
        assert results[0].category == "Anti-Pattern"

    def test_search_filter_by_tags(self, librarian):
        """Test filtering search by tags"""
        librarian.index.extend([
            IndexEntry(
                id="test1", path="test1", title="Pattern 1", category="Pattern",
                tags=["git", "windows"], confidence="Experimental",
                date="2025-10-18", created_by="test", summary="Test"
            ),
            IndexEntry(
                id="test2", path="test2", title="Pattern 2", category="Pattern",
                tags=["git", "linux"], confidence="Experimental",
                date="2025-10-18", created_by="test", summary="Test"
            )
        ])

        results = librarian.search_bok("", tags=["windows"])

        assert len(results) == 1
        assert results[0].id == "test1"

    def test_search_excludes_deprecated(self, librarian):
        """Test search excludes deprecated patterns by default"""
        librarian.index.extend([
            IndexEntry(
                id="active", path="test1", title="Active Pattern",
                category="Pattern", tags=["test"], confidence="Experimental",
                date="2025-10-18", created_by="test", summary="Test",
                deprecated=False
            ),
            IndexEntry(
                id="deprecated", path="test2", title="Deprecated Pattern",
                category="Pattern", tags=["test"], confidence="Experimental",
                date="2025-10-18", created_by="test", summary="Test",
                deprecated=True
            )
        ])

        results = librarian.search_bok("pattern")

        assert len(results) == 1
        assert results[0].id == "active"


class TestDeprecation:
    """Test pattern deprecation"""

    def test_deprecate_pattern(self, librarian):
        """Test deprecating a pattern"""
        # Add pattern
        librarian.index.append(IndexEntry(
            id="old-pattern", path="bok\\patterns\\old.md", title="Old Pattern",
            category="Pattern", tags=[], confidence="Experimental",
            date="2025-10-18", created_by="test", summary="Test"
        ))

        # Create actual file
        pattern_file = librarian.project_root / "bok" / "patterns" / "old.md"
        pattern_file.parent.mkdir(parents=True, exist_ok=True)
        pattern_file.write_text("# Old Pattern\n\nContent here.", encoding='utf-8')

        # Deprecate
        success = librarian.deprecate_pattern(
            "old-pattern",
            superseded_by="new-pattern",
            reason="Replaced with better version"
        )

        assert success
        assert librarian.index[0].deprecated is True
        assert librarian.index[0].superseded_by == "new-pattern"

        # Verify deprecation notice added to file
        content = pattern_file.read_text(encoding='utf-8')
        assert "DEPRECATION NOTICE" in content
        assert "new-pattern" in content

    def test_deprecate_nonexistent_pattern(self, librarian):
        """Test deprecating non-existent pattern returns False"""
        success = librarian.deprecate_pattern("nonexistent")

        assert success is False


class TestStatistics:
    """Test BOK statistics"""

    def test_statistics_empty_index(self, librarian):
        """Test statistics on empty index"""
        stats = librarian.get_statistics()

        assert stats["total_patterns"] == 0
        assert stats["active_patterns"] == 0
        assert stats["deprecated_patterns"] == 0

    def test_statistics_counts_patterns(self, librarian):
        """Test statistics counts patterns correctly"""
        librarian.index.extend([
            IndexEntry(
                id="p1", path="test", title="P1", category="Pattern",
                tags=["t1", "t2"], confidence="Experimental",
                date="2025-10-18", created_by="test", summary="Test"
            ),
            IndexEntry(
                id="p2", path="test", title="P2", category="Anti-Pattern",
                tags=["t2", "t3"], confidence="Validated",
                date="2025-10-18", created_by="test", summary="Test",
                deprecated=True
            ),
            IndexEntry(
                id="p3", path="test", title="P3", category="Pattern",
                tags=["t3"], confidence="Proven",
                date="2025-10-18", created_by="test", summary="Test"
            )
        ])

        stats = librarian.get_statistics()

        assert stats["total_patterns"] == 3
        assert stats["active_patterns"] == 2
        assert stats["deprecated_patterns"] == 1
        assert stats["by_category"]["Pattern"] == 2
        assert stats["by_confidence"]["Experimental"] == 1
        assert stats["by_confidence"]["Proven"] == 1
        assert stats["total_tags"] == 3  # t1, t2, t3


class TestHelperFunctions:
    """Test helper functions"""

    def test_generate_id_basic(self, librarian):
        """Test ID generation from title"""
        id_val = librarian._generate_id("Test Pattern Name")

        assert id_val == "test-pattern-name"

    def test_generate_id_removes_special_chars(self, librarian):
        """Test ID generation removes special characters"""
        id_val = librarian._generate_id("Test: Pattern (v2.0)")

        assert id_val == "test-pattern-v20"

    def test_generate_id_handles_duplicates(self, librarian):
        """Test ID generation handles duplicates"""
        librarian.index.append(IndexEntry(
            id="test-pattern", path="test", title="Test", category="Pattern",
            tags=[], confidence="Experimental", date="2025-10-18",
            created_by="test", summary="Test"
        ))

        id_val = librarian._generate_id("Test Pattern")

        assert id_val == "test-pattern-1"

    def test_title_similarity_identical(self, librarian):
        """Test title similarity for identical titles"""
        similarity = librarian._title_similarity("test pattern", "test pattern")

        assert similarity == 1.0

    def test_title_similarity_different(self, librarian):
        """Test title similarity for different titles"""
        similarity = librarian._title_similarity("test pattern", "different words")

        assert similarity == 0.0

    def test_title_similarity_partial_overlap(self, librarian):
        """Test title similarity for partial overlap"""
        similarity = librarian._title_similarity("git workflow pattern", "git deployment pattern")

        assert 0 < similarity < 1

    def test_contains_pii_detects_email(self, librarian):
        """Test PII detection for email"""
        assert librarian._contains_pii_or_secrets("contact user@example.com for help")

    def test_contains_pii_detects_api_key(self, librarian):
        """Test secrets detection for API key"""
        assert librarian._contains_pii_or_secrets("API_KEY=sk_live_1234567890abcdef")

    def test_contains_pii_clean_content(self, librarian):
        """Test PII detection returns False for clean content"""
        assert not librarian._contains_pii_or_secrets("This is a clean pattern description")

    def test_determine_bok_path_pattern(self, librarian):
        """Test BOK path determination for pattern"""
        metadata = SubmissionMetadata(
            title="Test Pattern",
            category="Pattern",
            tags=[],
            author="test",
            date="2025-10-18",
            summary="Test"
        )

        path = librarian._determine_bok_path(metadata)

        assert path.startswith("bok/patterns/")
        assert path.endswith(".md")

    def test_determine_bok_path_anti_pattern(self, librarian):
        """Test BOK path determination for anti-pattern"""
        metadata = SubmissionMetadata(
            title="Test Anti-Pattern",
            category="Anti-Pattern",
            tags=[],
            author="test",
            date="2025-10-18",
            summary="Test"
        )

        path = librarian._determine_bok_path(metadata)

        assert path.startswith("bok/anti-patterns/")


class TestCLIWrappers:
    """Test CLI wrapper functions"""

    def test_review_submission_cli(self, temp_project, sample_manifest, sample_submission_content):
        """Test CLI review wrapper"""
        # Create submission
        intake_dir = temp_project / ".deia" / "intake" / "2025-10-18" / "test"
        intake_dir.mkdir(parents=True)
        (intake_dir / "MANIFEST.md").write_text(sample_manifest)
        (intake_dir / "pattern.md").write_text(sample_submission_content)

        # Set project root
        import os
        original_cwd = os.getcwd()
        os.chdir(temp_project)

        try:
            result = review_submission_cli("2025-10-18/test/pattern.md")

            assert result["status"] == "accepted"
            assert isinstance(result["issues"], list)
        finally:
            os.chdir(original_cwd)

    def test_search_bok_cli(self, temp_project):
        """Test CLI search wrapper"""
        # Create librarian and add entry
        librarian = MasterLibrarian(project_root=temp_project)
        librarian.index.append(IndexEntry(
            id="test", path="test", title="Test Pattern", category="Pattern",
            tags=["test"], confidence="Experimental", date="2025-10-18",
            created_by="test", summary="Test pattern"
        ))
        librarian._save_index()

        # Set project root
        import os
        original_cwd = os.getcwd()
        os.chdir(temp_project)

        try:
            results = search_bok_cli("test")

            assert len(results) == 1
            assert results[0]["id"] == "test"
            assert "title" in results[0]
        finally:
            os.chdir(original_cwd)
