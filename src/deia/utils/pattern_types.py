"""
Pattern type definitions and enums for DEIA pattern extraction.

Defines canonical pattern types that can be extracted from session logs.
"""

from enum import Enum
from typing import List, Optional


class PatternType(Enum):
    """Canonical pattern types for DEIA BOK."""

    # Problem-solution patterns
    BUG_FIX = "bug_fix"  # Found and fixed a specific bug
    ERROR_RECOVERY = "error_recovery"  # Recovered from error or failure
    WORKAROUND = "workaround"  # Working around a limitation

    # Architecture & design
    ARCHITECTURE_DECISION = "architecture_decision"  # Design choice documented
    REFACTORING_PATTERN = "refactoring_pattern"  # How to refactor safely
    API_DESIGN = "api_design"  # API design pattern or practice

    # Process & workflow
    WORKFLOW_TIP = "workflow_tip"  # Productivity or process improvement
    COLLABORATION_PATTERN = "collaboration_pattern"  # How to work together
    DEBUGGING_TECHNIQUE = "debugging_technique"  # How to debug something

    # Learning & knowledge
    GOTCHA = "gotcha"  # Surprising behavior, edge case
    BEST_PRACTICE = "best_practice"  # Best practice for something
    ANTI_PATTERN = "anti_pattern"  # What NOT to do

    # Integration & integration
    INTEGRATION_GUIDE = "integration_guide"  # How to integrate two systems
    DEPENDENCY_ISSUE = "dependency_issue"  # Handling dependencies
    COMPATIBILITY_NOTE = "compatibility_note"  # Compatibility notes


class PatternUrgency(Enum):
    """Priority/urgency level for patterns."""

    LOW = "low"  # Nice to know, low priority
    MEDIUM = "medium"  # Should know, medium priority
    HIGH = "high"  # Critical to know, high priority


class PatternStatus(Enum):
    """Status of pattern in extraction/publication pipeline."""

    EXTRACTED = "extracted"  # Just extracted from session
    SANITIZED = "sanitized"  # PII/secrets removed
    TEMPLATED = "templated"  # Applied BOK template
    VALIDATED = "validated"  # Passed validation checks
    REVIEWED = "reviewed"  # Human reviewed
    PUBLISHED = "published"  # Published to BOK


class ExtractedPattern:
    """Represents an extracted pattern before publication."""

    def __init__(
        self,
        title: str,
        pattern_type: PatternType,
        problem: str,
        solution: str,
        reasoning: str,
        tags: Optional[List[str]] = None,
        urgency: PatternUrgency = PatternUrgency.MEDIUM,
        original_session_id: Optional[str] = None,
        when_to_use: Optional[str] = None,
        gotchas: Optional[str] = None,
        related_patterns: Optional[List[str]] = None,
    ):
        """Initialize an extracted pattern."""
        self.title = title
        self.pattern_type = pattern_type
        self.problem = problem
        self.solution = solution
        self.reasoning = reasoning
        self.tags = tags or []
        self.urgency = urgency
        self.original_session_id = original_session_id
        self.when_to_use = when_to_use
        self.gotchas = gotchas
        self.related_patterns = related_patterns or []
        self.status = PatternStatus.EXTRACTED

    def to_dict(self) -> dict:
        """Convert pattern to dictionary."""
        return {
            "title": self.title,
            "pattern_type": self.pattern_type.value,
            "problem": self.problem,
            "solution": self.solution,
            "reasoning": self.reasoning,
            "tags": self.tags,
            "urgency": self.urgency.value,
            "original_session_id": self.original_session_id,
            "when_to_use": self.when_to_use,
            "gotchas": self.gotchas,
            "related_patterns": self.related_patterns,
            "status": self.status.value,
        }
