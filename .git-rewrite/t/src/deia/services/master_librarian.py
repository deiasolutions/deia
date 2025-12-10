"""
Master Librarian - BOK Curation and Knowledge Management System

This module provides the core functionality for the Master Librarian role,
responsible for curating, organizing, and preserving the DEIA Body of Knowledge (BOK).

Key Features:
- Knowledge intake and review workflow
- Pattern validation and quality control
- Semantic indexing and metadata management
- Integration with Enhanced BOK Search
- Version control and archival

Author: CLAUDE-CODE-004 (Documentation Curator / Master Librarian)
Created: 2025-10-18
Version: 1.0
Specification: .deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md
"""

import os
import yaml
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class SubmissionStatus(Enum):
    """Submission review status"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    REVISION_REQUESTED = "revision_requested"
    BLOCKED = "blocked"


class ConfidenceLevel(Enum):
    """Pattern confidence/maturity level"""
    EXPERIMENTAL = "Experimental"
    VALIDATED = "Validated"
    PROVEN = "Proven"


class PatternCategory(Enum):
    """BOK pattern categories"""
    PATTERN = "Pattern"
    ANTI_PATTERN = "Anti-Pattern"
    PROCESS = "Process"
    PLATFORM = "Platform-Specific"
    METHODOLOGY = "Methodology"
    GOVERNANCE = "Governance"
    FEDERALIST = "Federalist"
    OBSERVATION = "Observation"


@dataclass
class SubmissionMetadata:
    """Metadata for a BOK submission"""
    title: str
    category: str
    tags: List[str]
    author: str
    date: str
    summary: str
    confidence: str = ConfidenceLevel.EXPERIMENTAL.value
    source_project: Optional[str] = None
    platform: str = "Platform-Agnostic"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class IndexEntry:
    """Entry in the master BOK index"""
    id: str
    path: str
    title: str
    category: str
    tags: List[str]
    confidence: str
    date: str
    created_by: str
    summary: str
    source_project: Optional[str] = None
    platform: str = "Platform-Agnostic"
    deprecated: bool = False
    superseded_by: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for YAML serialization"""
        data = asdict(self)
        # Remove None values for cleaner YAML
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class ReviewResult:
    """Result of submission review"""
    status: SubmissionStatus
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    approved_path: Optional[str] = None
    reason: Optional[str] = None


class MasterLibrarian:
    """
    Master Librarian for DEIA Body of Knowledge curation.

    Responsibilities:
    - Review and validate submissions
    - Maintain semantic index
    - Organize BOK structure
    - Ensure quality standards
    - Coordinate with BOK tools

    Usage:
        librarian = MasterLibrarian()

        # Review a submission
        result = librarian.review_submission("2025-10-18/agent-bc/pattern.md")

        # Accept and integrate
        if result.status == SubmissionStatus.ACCEPTED:
            librarian.integrate_submission("2025-10-18/agent-bc/pattern.md", result)

        # Query BOK
        patterns = librarian.search_bok("git collaboration")
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize Master Librarian.

        Args:
            project_root: Root directory of DEIA project (auto-detected if None)
        """
        self.project_root = project_root or self._find_project_root()
        self.deia_dir = self.project_root / ".deia"
        self.intake_dir = self.deia_dir / "intake"
        self.bok_dir = self.project_root / "bok"
        self.index_path = self.deia_dir / "index" / "master-index.yaml"
        self.observations_dir = self.deia_dir / "observations"

        # Ensure directories exist
        self._ensure_directories()

        # Load index
        self.index: List[IndexEntry] = self._load_index()

    def _find_project_root(self) -> Path:
        """Find project root by looking for .deia directory"""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".deia").exists():
                return current
            current = current.parent
        # Default to current directory
        return Path.cwd()

    def _ensure_directories(self) -> None:
        """Ensure required directories exist"""
        directories = [
            self.intake_dir,
            self.bok_dir,
            self.bok_dir / "patterns",
            self.bok_dir / "anti-patterns",
            self.bok_dir / "processes",
            self.bok_dir / "platforms",
            self.bok_dir / "methodologies",
            self.bok_dir / "governance",
            self.deia_dir / "index",
            self.observations_dir,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _load_index(self) -> List[IndexEntry]:
        """Load master index from YAML"""
        if not self.index_path.exists():
            return []

        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or []

            return [IndexEntry(**entry) for entry in data]
        except Exception as e:
            print(f"Warning: Could not load index: {e}")
            return []

    def _save_index(self) -> None:
        """Save master index to YAML"""
        try:
            data = [entry.to_dict() for entry in self.index]

            with open(self.index_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        except Exception as e:
            raise RuntimeError(f"Failed to save index: {e}")

    def _generate_id(self, title: str) -> str:
        """Generate unique ID from title (kebab-case)"""
        # Remove special characters, convert to lowercase
        id_base = re.sub(r'[^\w\s-]', '', title.lower())
        id_base = re.sub(r'[-\s]+', '-', id_base).strip('-')

        # Ensure uniqueness
        existing_ids = {entry.id for entry in self.index}
        if id_base not in existing_ids:
            return id_base

        # Add counter if duplicate
        counter = 1
        while f"{id_base}-{counter}" in existing_ids:
            counter += 1
        return f"{id_base}-{counter}"

    def review_submission(self, intake_path: str) -> ReviewResult:
        """
        Review a submission for quality and acceptance.

        Args:
            intake_path: Relative path within .deia/intake/ (e.g., "2025-10-18/agent-bc/pattern.md")

        Returns:
            ReviewResult with status, issues, and suggestions

        Example:
            result = librarian.review_submission("2025-10-18/my-pattern/submission.md")
            if result.status == SubmissionStatus.ACCEPTED:
                print("Submission approved!")
        """
        full_path = self.intake_dir / intake_path

        if not full_path.exists():
            return ReviewResult(
                status=SubmissionStatus.REJECTED,
                reason=f"Submission not found: {intake_path}"
            )

        issues = []
        suggestions = []

        # Load manifest
        manifest_path = full_path.parent / "MANIFEST.md"
        if not manifest_path.exists():
            issues.append("Missing MANIFEST.md - required for all submissions")

        try:
            metadata = self._parse_manifest(manifest_path) if manifest_path.exists() else None
        except Exception as e:
            issues.append(f"Invalid MANIFEST.md: {e}")
            metadata = None

        # Quality checks
        if metadata:
            # Check required fields
            if not metadata.title:
                issues.append("Missing title in MANIFEST.md")
            if not metadata.summary:
                issues.append("Missing summary in MANIFEST.md")
            if not metadata.tags:
                suggestions.append("Consider adding tags for better discoverability")

            # Check for duplicates
            duplicate = self._find_duplicate(metadata.title, metadata.tags)
            if duplicate:
                return ReviewResult(
                    status=SubmissionStatus.REJECTED,
                    reason=f"Duplicate pattern found: {duplicate.title} at {duplicate.path}",
                    suggestions=["Consider enhancing existing pattern instead of creating new one"]
                )

        # Read content
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            issues.append(f"Could not read submission file: {e}")
            content = ""

        # Content quality checks
        if content:
            # Check for PII/secrets
            if self._contains_pii_or_secrets(content):
                return ReviewResult(
                    status=SubmissionStatus.BLOCKED,
                    reason="Submission contains potential PII or secrets - cannot accept",
                    issues=["Remove API keys, credentials, email addresses, or personal information"]
                )

            # Check length
            if len(content) < 200:
                issues.append("Submission is very short - consider adding more detail, context, or examples")

            # Check for code examples (recommended)
            if "```" not in content and "code" in metadata.category.lower() if metadata else False:
                suggestions.append("Consider adding code examples for better clarity")

        # Determine status
        if issues:
            if any("Missing MANIFEST" in issue or "Invalid MANIFEST" in issue for issue in issues):
                status = SubmissionStatus.REJECTED
                reason = "Submission incomplete - missing or invalid manifest"
            else:
                status = SubmissionStatus.REVISION_REQUESTED
                reason = "Minor issues found - revision requested"
        else:
            status = SubmissionStatus.ACCEPTED
            reason = "Submission meets quality standards"

            # Determine approved BOK path
            if metadata:
                approved_path = self._determine_bok_path(metadata)
            else:
                approved_path = None

        return ReviewResult(
            status=status,
            issues=issues,
            suggestions=suggestions,
            approved_path=approved_path if status == SubmissionStatus.ACCEPTED else None,
            reason=reason
        )

    def _parse_manifest(self, manifest_path: Path) -> SubmissionMetadata:
        """Parse MANIFEST.md file"""
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata using regex
        def extract_field(field_name: str, required: bool = True) -> Optional[str]:
            pattern = rf'\*\*{field_name}:\*\*\s*(.+?)(?=\n\*\*|\n\n|$)'
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
            elif required:
                raise ValueError(f"Missing required field: {field_name}")
            return None

        # Extract tags (comma-separated)
        tags_str = extract_field("Tags", required=False) or ""
        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

        return SubmissionMetadata(
            title=extract_field("Title"),
            category=extract_field("Category"),
            tags=tags,
            author=extract_field("Author"),
            date=extract_field("Date"),
            summary=extract_field("Summary"),
            confidence=extract_field("Confidence", required=False) or ConfidenceLevel.EXPERIMENTAL.value,
            source_project=extract_field("Source Project", required=False),
            platform=extract_field("Platform", required=False) or "Platform-Agnostic"
        )

    def _find_duplicate(self, title: str, tags: List[str]) -> Optional[IndexEntry]:
        """Check if similar pattern already exists in BOK"""
        title_lower = title.lower()

        for entry in self.index:
            # Exact title match
            if entry.title.lower() == title_lower:
                return entry

            # High tag overlap (>70% of tags match)
            if tags and entry.tags:
                tag_overlap = len(set(tags) & set(entry.tags)) / len(set(tags) | set(entry.tags))
                if tag_overlap > 0.7:
                    # Similar tags, check title similarity
                    if self._title_similarity(title_lower, entry.title.lower()) > 0.8:
                        return entry

        return None

    def _title_similarity(self, title1: str, title2: str) -> float:
        """Calculate title similarity (simple word overlap)"""
        words1 = set(re.findall(r'\w+', title1.lower()))
        words2 = set(re.findall(r'\w+', title2.lower()))

        if not words1 or not words2:
            return 0.0

        return len(words1 & words2) / len(words1 | words2)

    def _contains_pii_or_secrets(self, content: str) -> bool:
        """Check for potential PII or secrets in content"""
        # Simple heuristics (not exhaustive)
        patterns = [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Email
            r'(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*[\'"]?[a-zA-Z0-9_-]{16,}',  # API keys/secrets
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'(?i)(access[_-]?token|bearer)\s+[a-zA-Z0-9_-]{20,}',  # Access tokens
        ]

        for pattern in patterns:
            if re.search(pattern, content):
                return True

        return False

    def _determine_bok_path(self, metadata: SubmissionMetadata) -> str:
        """Determine appropriate BOK path based on category"""
        category_map = {
            "Pattern": "patterns",
            "Anti-Pattern": "anti-patterns",
            "Process": "processes",
            "Platform-Specific": "platforms",
            "Methodology": "methodologies",
            "Governance": "governance",
            "Federalist": "federalist",
        }

        category_dir = category_map.get(metadata.category, "patterns")
        filename = self._generate_id(metadata.title) + ".md"

        return f"bok/{category_dir}/{filename}"

    def integrate_submission(self, intake_path: str, review_result: ReviewResult,
                           metadata: Optional[SubmissionMetadata] = None) -> IndexEntry:
        """
        Integrate an approved submission into BOK.

        Args:
            intake_path: Relative path within .deia/intake/
            review_result: Result from review_submission (must be ACCEPTED)
            metadata: Optional metadata (will parse from manifest if not provided)

        Returns:
            IndexEntry for the newly integrated pattern

        Raises:
            ValueError: If submission not accepted or path invalid

        Example:
            result = librarian.review_submission("2025-10-18/my-pattern/pattern.md")
            if result.status == SubmissionStatus.ACCEPTED:
                entry = librarian.integrate_submission("2025-10-18/my-pattern/pattern.md", result)
                print(f"Integrated as: {entry.path}")
        """
        if review_result.status != SubmissionStatus.ACCEPTED:
            raise ValueError(f"Cannot integrate submission with status: {review_result.status}")

        full_intake_path = self.intake_dir / intake_path
        if not full_intake_path.exists():
            raise ValueError(f"Intake path not found: {intake_path}")

        # Load metadata if not provided
        if metadata is None:
            manifest_path = full_intake_path.parent / "MANIFEST.md"
            metadata = self._parse_manifest(manifest_path)

        # Determine target path
        target_path = review_result.approved_path or self._determine_bok_path(metadata)
        full_target_path = self.project_root / target_path

        # Ensure target directory exists
        full_target_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy file to BOK
        import shutil
        shutil.copy2(full_intake_path, full_target_path)

        # Create index entry
        entry = IndexEntry(
            id=self._generate_id(metadata.title),
            path=target_path.replace('/', '\\'),  # Windows path format
            title=metadata.title,
            category=metadata.category,
            tags=metadata.tags,
            confidence=metadata.confidence,
            date=metadata.date,
            created_by=metadata.author,
            summary=metadata.summary,
            source_project=metadata.source_project,
            platform=metadata.platform
        )

        # Add to index
        self.index.append(entry)
        self._save_index()

        # Archive intake (move to processed/)
        processed_dir = full_intake_path.parent.parent / "processed" / full_intake_path.parent.name
        processed_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(full_intake_path), str(processed_dir / full_intake_path.name))
        if (full_intake_path.parent / "MANIFEST.md").exists():
            shutil.move(str(full_intake_path.parent / "MANIFEST.md"),
                       str(processed_dir / "MANIFEST.md"))

        return entry

    def search_bok(self, query: str, category: Optional[str] = None,
                   tags: Optional[List[str]] = None) -> List[IndexEntry]:
        """
        Search BOK index by keywords, category, or tags.

        Args:
            query: Search keywords (searched in title, summary, tags)
            category: Optional category filter
            tags: Optional tag filter (matches any)

        Returns:
            List of matching IndexEntry objects

        Example:
            # Search for git patterns
            results = librarian.search_bok("git collaboration")

            # Filter by category
            results = librarian.search_bok("deployment", category="Anti-Pattern")

            # Filter by tags
            results = librarian.search_bok("", tags=["windows", "encoding"])
        """
        query_lower = query.lower()
        results = []

        for entry in self.index:
            # Skip deprecated unless explicitly searched
            if entry.deprecated and "deprecated" not in query_lower:
                continue

            # Category filter
            if category and entry.category != category:
                continue

            # Tag filter
            if tags and not any(tag in entry.tags for tag in tags):
                continue

            # Keyword search
            if query:
                searchable = f"{entry.title} {entry.summary} {' '.join(entry.tags)}".lower()
                if query_lower in searchable:
                    results.append(entry)
            else:
                # No query, just filters
                results.append(entry)

        return results

    def deprecate_pattern(self, pattern_id: str, superseded_by: Optional[str] = None,
                         reason: Optional[str] = None) -> bool:
        """
        Mark a pattern as deprecated.

        Args:
            pattern_id: ID of pattern to deprecate
            superseded_by: Optional ID of replacement pattern
            reason: Optional deprecation reason

        Returns:
            True if successful, False if pattern not found

        Example:
            librarian.deprecate_pattern(
                "old-git-workflow",
                superseded_by="multi-agent-git-workflow",
                reason="Replaced with multi-agent version"
            )
        """
        for entry in self.index:
            if entry.id == pattern_id:
                entry.deprecated = True
                entry.superseded_by = superseded_by
                self._save_index()

                # Add deprecation notice to pattern file
                pattern_path = self.project_root / entry.path
                if pattern_path.exists():
                    self._add_deprecation_notice(pattern_path, superseded_by, reason)

                return True

        return False

    def _add_deprecation_notice(self, pattern_path: Path, superseded_by: Optional[str],
                                reason: Optional[str]) -> None:
        """Add deprecation notice to pattern file"""
        notice = "\n\n---\n\n## ⚠️ DEPRECATION NOTICE\n\n"
        notice += f"**Status:** DEPRECATED\n\n"
        if reason:
            notice += f"**Reason:** {reason}\n\n"
        if superseded_by:
            notice += f"**Superseded By:** `{superseded_by}`\n\n"
        notice += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n"

        with open(pattern_path, 'a', encoding='utf-8') as f:
            f.write(notice)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get BOK statistics.

        Returns:
            Dictionary with BOK metrics

        Example:
            stats = librarian.get_statistics()
            print(f"Total patterns: {stats['total_patterns']}")
            print(f"Categories: {stats['by_category']}")
        """
        total = len(self.index)
        active = len([e for e in self.index if not e.deprecated])
        deprecated = total - active

        by_category = {}
        by_confidence = {}

        for entry in self.index:
            if not entry.deprecated:
                by_category[entry.category] = by_category.get(entry.category, 0) + 1
                by_confidence[entry.confidence] = by_confidence.get(entry.confidence, 0) + 1

        return {
            "total_patterns": total,
            "active_patterns": active,
            "deprecated_patterns": deprecated,
            "by_category": by_category,
            "by_confidence": by_confidence,
            "total_tags": len(set(tag for entry in self.index for tag in entry.tags)),
        }


# Convenience functions for CLI integration
def review_submission_cli(intake_path: str) -> Dict[str, Any]:
    """CLI wrapper for review_submission"""
    librarian = MasterLibrarian()
    result = librarian.review_submission(intake_path)

    return {
        "status": result.status.value,
        "issues": result.issues,
        "suggestions": result.suggestions,
        "reason": result.reason,
        "approved_path": result.approved_path
    }


def integrate_submission_cli(intake_path: str) -> Dict[str, Any]:
    """CLI wrapper for integrate_submission"""
    librarian = MasterLibrarian()

    # Review first
    result = librarian.review_submission(intake_path)

    if result.status != SubmissionStatus.ACCEPTED:
        return {
            "success": False,
            "status": result.status.value,
            "reason": result.reason,
            "issues": result.issues
        }

    # Integrate
    entry = librarian.integrate_submission(intake_path, result)

    return {
        "success": True,
        "pattern_id": entry.id,
        "path": entry.path,
        "title": entry.title
    }


def search_bok_cli(query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """CLI wrapper for search_bok"""
    librarian = MasterLibrarian()
    results = librarian.search_bok(query, category=category)

    return [
        {
            "id": entry.id,
            "title": entry.title,
            "category": entry.category,
            "path": entry.path,
            "summary": entry.summary,
            "tags": entry.tags
        }
        for entry in results
    ]
