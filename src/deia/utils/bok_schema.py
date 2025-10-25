"""
BOK (Body of Knowledge) schema validation.

Defines the structure and validation rules for BOK patterns.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class BokSchema:
    """BOK entry schema definition."""

    # Required fields
    title: str
    pattern_type: str
    problem: str
    solution: str
    reasoning: str

    # Optional fields
    tags: List[str] = None
    urgency: str = "medium"
    when_to_use: str = None
    gotchas: str = None
    related_patterns: List[str] = None
    contributor: str = None
    date: str = None
    original_session_id: str = None

    # Metadata
    version: str = "1.0"
    status: str = "draft"

    def __post_init__(self):
        """Validate schema after initialization."""
        if self.tags is None:
            self.tags = []
        if self.related_patterns is None:
            self.related_patterns = []


class BokValidator:
    """Validates BOK entries against schema."""

    # Valid pattern types
    VALID_PATTERN_TYPES = {
        "bug_fix",
        "error_recovery",
        "workaround",
        "architecture_decision",
        "refactoring_pattern",
        "api_design",
        "workflow_tip",
        "collaboration_pattern",
        "debugging_technique",
        "gotcha",
        "best_practice",
        "anti_pattern",
        "integration_guide",
        "dependency_issue",
        "compatibility_note",
    }

    # Valid urgency levels
    VALID_URGENCY_LEVELS = {"low", "medium", "high"}

    # Minimum required word counts for content fields
    MIN_WORDS = {
        "problem": 10,  # Minimum 10 words to describe problem
        "solution": 15,  # Minimum 15 words to describe solution
        "reasoning": 15,  # Minimum 15 words to explain reasoning
        "title": 3,  # Minimum 3 words for title
    }

    @staticmethod
    def validate(pattern: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate a pattern against BOK schema.

        Args:
            pattern: Dictionary representing the pattern

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check required fields
        required_fields = ["title", "pattern_type", "problem", "solution", "reasoning"]
        for field in required_fields:
            if field not in pattern or not pattern[field]:
                errors.append(f"Missing required field: {field}")

        if errors:
            return False, errors

        # Validate pattern type
        if pattern.get("pattern_type") not in BokValidator.VALID_PATTERN_TYPES:
            errors.append(
                f"Invalid pattern_type: {pattern.get('pattern_type')}. "
                f"Must be one of: {', '.join(BokValidator.VALID_PATTERN_TYPES)}"
            )

        # Validate urgency
        if "urgency" in pattern:
            if pattern["urgency"] not in BokValidator.VALID_URGENCY_LEVELS:
                errors.append(
                    f"Invalid urgency: {pattern['urgency']}. "
                    f"Must be one of: {', '.join(BokValidator.VALID_URGENCY_LEVELS)}"
                )

        # Check minimum word counts
        for field, min_words in BokValidator.MIN_WORDS.items():
            if field in pattern:
                word_count = len(str(pattern[field]).split())
                if word_count < min_words:
                    errors.append(
                        f"Field '{field}' too short: {word_count} words (minimum {min_words})"
                    )

        # Validate tags (if present)
        if "tags" in pattern:
            if not isinstance(pattern["tags"], list):
                errors.append("Field 'tags' must be a list")
            elif len(pattern["tags"]) == 0:
                errors.append("Pattern should have at least one tag")
            elif len(pattern["tags"]) > 10:
                errors.append("Pattern has too many tags (maximum 10)")

        # Validate related_patterns (if present)
        if "related_patterns" in pattern:
            if not isinstance(pattern["related_patterns"], list):
                errors.append("Field 'related_patterns' must be a list")

        return len(errors) == 0, errors

    @staticmethod
    def to_markdown(pattern: Dict[str, Any]) -> str:
        """
        Convert pattern to BOK markdown format.

        Args:
            pattern: Dictionary representing the pattern

        Returns:
            Markdown formatted pattern
        """
        md = []

        # Title
        md.append(f"# Pattern: {pattern.get('title', 'Untitled')}")
        md.append("")

        # Metadata
        md.append("**Pattern Type:** " + pattern.get("pattern_type", "unknown"))
        if "urgency" in pattern:
            md.append("**Urgency:** " + pattern["urgency"])
        if "contributor" in pattern:
            md.append("**Contributor:** " + pattern["contributor"])
        if "date" in pattern:
            md.append("**Date:** " + pattern["date"])
        if pattern.get("tags"):
            md.append("**Tags:** " + ", ".join(pattern["tags"]))
        md.append("")

        # Problem
        md.append("## Problem")
        md.append(pattern.get("problem", ""))
        md.append("")

        # Solution
        md.append("## Solution")
        md.append(pattern.get("solution", ""))
        md.append("")

        # Reasoning
        md.append("## Why It Works")
        md.append(pattern.get("reasoning", ""))
        md.append("")

        # When to use
        if pattern.get("when_to_use"):
            md.append("## When to Use It")
            md.append(pattern["when_to_use"])
            md.append("")

        # Gotchas
        if pattern.get("gotchas"):
            md.append("## Gotchas & Edge Cases")
            md.append(pattern["gotchas"])
            md.append("")

        # Related patterns
        if pattern.get("related_patterns"):
            md.append("## Related Patterns")
            for related in pattern["related_patterns"]:
                md.append(f"- {related}")
            md.append("")

        return "\n".join(md)
