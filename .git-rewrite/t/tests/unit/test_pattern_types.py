"""
Tests for pattern_types module.
"""

import pytest
from deia.utils.pattern_types import (
    PatternType,
    PatternUrgency,
    PatternStatus,
    ExtractedPattern,
)


class TestPatternType:
    """Test PatternType enum."""

    def test_valid_pattern_types(self):
        """All pattern types should be defined."""
        assert PatternType.BUG_FIX.value == "bug_fix"
        assert PatternType.ERROR_RECOVERY.value == "error_recovery"
        assert PatternType.ARCHITECTURE_DECISION.value == "architecture_decision"
        assert PatternType.BEST_PRACTICE.value == "best_practice"

    def test_pattern_type_count(self):
        """Should have at least 15 pattern types."""
        assert len(PatternType) >= 15


class TestPatternUrgency:
    """Test PatternUrgency enum."""

    def test_valid_urgency_levels(self):
        """All urgency levels should be defined."""
        assert PatternUrgency.LOW.value == "low"
        assert PatternUrgency.MEDIUM.value == "medium"
        assert PatternUrgency.HIGH.value == "high"


class TestExtractedPattern:
    """Test ExtractedPattern class."""

    def test_create_pattern(self):
        """Should create pattern with required fields."""
        pattern = ExtractedPattern(
            title="Fix database timeout",
            pattern_type=PatternType.BUG_FIX,
            problem="Database queries were timing out intermittently",
            solution="Added connection pooling and query optimization",
            reasoning="Connection pooling reduces overhead, optimization improves query plans",
        )

        assert pattern.title == "Fix database timeout"
        assert pattern.pattern_type == PatternType.BUG_FIX
        assert pattern.status == PatternStatus.EXTRACTED

    def test_pattern_with_optional_fields(self):
        """Should support optional fields."""
        pattern = ExtractedPattern(
            title="API design pattern",
            pattern_type=PatternType.API_DESIGN,
            problem="APIs were inconsistent across services",
            solution="Standardized on OpenAPI specification",
            reasoning="Standards improve developer experience",
            tags=["api", "design", "standards"],
            urgency=PatternUrgency.HIGH,
            when_to_use="When designing REST APIs",
            gotchas="HATEOAS not required for all endpoints",
        )

        assert pattern.tags == ["api", "design", "standards"]
        assert pattern.urgency == PatternUrgency.HIGH
        assert pattern.when_to_use == "When designing REST APIs"

    def test_pattern_to_dict(self):
        """Should convert pattern to dictionary."""
        pattern = ExtractedPattern(
            title="Test pattern",
            pattern_type=PatternType.GOTCHA,
            problem="Issue discovered",
            solution="Resolution found",
            reasoning="Here's why it works",
            tags=["test"],
        )

        data = pattern.to_dict()

        assert data["title"] == "Test pattern"
        assert data["pattern_type"] == "gotcha"
        assert data["tags"] == ["test"]
        assert data["status"] == "extracted"

    def test_pattern_status_changes(self):
        """Should allow status changes through lifecycle."""
        pattern = ExtractedPattern(
            title="Test",
            pattern_type=PatternType.BEST_PRACTICE,
            problem="P",
            solution="S",
            reasoning="R",
        )

        assert pattern.status == PatternStatus.EXTRACTED

        pattern.status = PatternStatus.SANITIZED
        assert pattern.status == PatternStatus.SANITIZED

        pattern.status = PatternStatus.VALIDATED
        assert pattern.status == PatternStatus.VALIDATED


class TestPatternDefaults:
    """Test default values."""

    def test_default_urgency(self):
        """Default urgency should be MEDIUM."""
        pattern = ExtractedPattern(
            title="T",
            pattern_type=PatternType.WORKFLOW_TIP,
            problem="P",
            solution="S",
            reasoning="R",
        )

        assert pattern.urgency == PatternUrgency.MEDIUM

    def test_default_empty_lists(self):
        """Empty lists should be initialized."""
        pattern = ExtractedPattern(
            title="T",
            pattern_type=PatternType.DEBUGGING_TECHNIQUE,
            problem="P",
            solution="S",
            reasoning="R",
        )

        assert pattern.tags == []
        assert pattern.related_patterns == []

    def test_default_none_optionals(self):
        """Optional fields should default to None."""
        pattern = ExtractedPattern(
            title="T",
            pattern_type=PatternType.WORKAROUND,
            problem="P",
            solution="S",
            reasoning="R",
        )

        assert pattern.when_to_use is None
        assert pattern.gotchas is None
        assert pattern.original_session_id is None
