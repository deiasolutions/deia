"""
Tests for BOK schema validation.
"""

import pytest
from deia.utils.bok_schema import BokValidator, BokSchema


class TestBokValidator:
    """Test BOK validation logic."""

    def test_valid_pattern(self):
        """Valid pattern should pass validation."""
        pattern = {
            "title": "How to optimize database queries effectively",
            "pattern_type": "best_practice",
            "problem": "Database queries were running slow and causing timeouts in our production environment under load",
            "solution": "Added proper indexing on frequently queried columns and optimized query execution plans significantly",
            "reasoning": "Indexes speed up lookups from O(n) to O(log n), query optimization reduces unnecessary full table scans",
            "tags": ["database", "performance"],
            "urgency": "medium",
        }

        is_valid, errors = BokValidator.validate(pattern)
        assert is_valid
        assert len(errors) == 0

    def test_missing_required_field(self):
        """Missing required field should fail."""
        pattern = {
            "title": "Test pattern",
            "pattern_type": "bug_fix",
            # Missing problem, solution, reasoning
        }

        is_valid, errors = BokValidator.validate(pattern)
        assert not is_valid
        assert any("problem" in e.lower() for e in errors)

    def test_invalid_pattern_type(self):
        """Invalid pattern type should fail."""
        pattern = {
            "title": "Test",
            "pattern_type": "invalid_type",
            "problem": "Test problem description here",
            "solution": "Test solution description here",
            "reasoning": "Test reasoning explanation here",
        }

        is_valid, errors = BokValidator.validate(pattern)
        assert not is_valid
        assert any("pattern_type" in e.lower() for e in errors)

    def test_invalid_urgency(self):
        """Invalid urgency should fail."""
        pattern = {
            "title": "Test pattern",
            "pattern_type": "bug_fix",
            "problem": "Test problem description",
            "solution": "Test solution description",
            "reasoning": "Test reasoning explanation",
            "urgency": "critical",  # Not valid
        }

        is_valid, errors = BokValidator.validate(pattern)
        assert not is_valid
        assert any("urgency" in e.lower() for e in errors)

    def test_too_short_content(self):
        """Content too short should fail."""
        pattern = {
            "title": "Test",  # Only 1 word, need 3
            "pattern_type": "bug_fix",
            "problem": "Short",  # Only 1 word, need 10
            "solution": "Fix it",  # Only 2 words, need 15
            "reasoning": "Works",  # Only 1 word, need 15
        }

        is_valid, errors = BokValidator.validate(pattern)
        assert not is_valid
        assert any("too short" in e.lower() for e in errors)

    def test_invalid_tags_type(self):
        """Tags must be a list."""
        pattern = {
            "title": "Test pattern here",
            "pattern_type": "best_practice",
            "problem": "Test problem description",
            "solution": "Test solution description",
            "reasoning": "Test reasoning explanation",
            "tags": "database,performance",  # String instead of list
        }

        is_valid, errors = BokValidator.validate(pattern)
        assert not is_valid
        assert any("tags" in e.lower() and "list" in e.lower() for e in errors)

    def test_empty_tags_warning(self):
        """Empty tags list should warn."""
        pattern = {
            "title": "Test pattern here",
            "pattern_type": "bug_fix",
            "problem": "Test problem description",
            "solution": "Test solution description",
            "reasoning": "Test reasoning explanation",
            "tags": [],  # Empty
        }

        is_valid, errors = BokValidator.validate(pattern)
        assert not is_valid
        assert any("tag" in e.lower() for e in errors)

    def test_too_many_tags(self):
        """Too many tags should fail."""
        pattern = {
            "title": "Test pattern here",
            "pattern_type": "bug_fix",
            "problem": "Test problem description",
            "solution": "Test solution description",
            "reasoning": "Test reasoning explanation",
            "tags": [f"tag{i}" for i in range(15)],  # 15 tags
        }

        is_valid, errors = BokValidator.validate(pattern)
        assert not is_valid
        assert any("too many" in e.lower() for e in errors)


class TestBokMarkdownFormat:
    """Test markdown formatting."""

    def test_pattern_to_markdown(self):
        """Should format pattern as markdown."""
        pattern = {
            "title": "Database optimization",
            "pattern_type": "best_practice",
            "problem": "Database queries were slow and inefficient",
            "solution": "Added indexes and optimized query plans",
            "reasoning": "Proper indexing and optimization improve performance",
            "tags": ["database", "performance"],
            "urgency": "high",
            "contributor": "Alice",
            "date": "2025-10-25",
        }

        md = BokValidator.to_markdown(pattern)

        assert "# Pattern: Database optimization" in md
        assert "## Problem" in md
        assert "## Solution" in md
        assert "## Why It Works" in md
        assert "**Pattern Type:** best_practice" in md
        assert "**Urgency:** high" in md
        assert "**Contributor:** Alice" in md

    def test_markdown_with_optional_fields(self):
        """Markdown should include optional fields if present."""
        pattern = {
            "title": "Test pattern name",
            "pattern_type": "gotcha",
            "problem": "Surprising behavior discovered",
            "solution": "Working around limitation",
            "reasoning": "Understanding explains behavior",
            "when_to_use": "When dealing with edge cases",
            "gotchas": "Watch out for this condition",
            "related_patterns": ["pattern-1", "pattern-2"],
        }

        md = BokValidator.to_markdown(pattern)

        assert "## When to Use It" in md
        assert "## Gotchas & Edge Cases" in md
        assert "## Related Patterns" in md
        assert "pattern-1" in md
        assert "pattern-2" in md


class TestBokSchema:
    """Test BokSchema dataclass."""

    def test_create_schema(self):
        """Should create schema with defaults."""
        schema = BokSchema(
            title="Test",
            pattern_type="bug_fix",
            problem="Problem",
            solution="Solution",
            reasoning="Reasoning",
        )

        assert schema.urgency == "medium"
        assert schema.tags == []
        assert schema.status == "draft"
        assert schema.version == "1.0"

    def test_schema_with_values(self):
        """Should accept custom values."""
        schema = BokSchema(
            title="Test",
            pattern_type="best_practice",
            problem="Problem",
            solution="Solution",
            reasoning="Reasoning",
            tags=["test", "example"],
            urgency="high",
            status="published",
        )

        assert schema.tags == ["test", "example"]
        assert schema.urgency == "high"
        assert schema.status == "published"
