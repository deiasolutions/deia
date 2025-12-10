"""
Extract patterns directly from chat conversations.

Integrates pattern extraction with chat interface.
"""

from typing import Optional, Dict, Any, Tuple
from deia.utils.pattern_types import ExtractedPattern, PatternType
from deia.utils.session_parser import SessionParser, Message
from deia.utils.bok_schema import BokValidator


class ChatPatternExtractor:
    """Extract patterns from chat conversations."""

    @staticmethod
    def extract_from_chat_history(
        messages: list[Message],
        conversation_title: str = "Chat Conversation"
    ) -> Optional[ExtractedPattern]:
        """
        Extract a pattern from chat message history.

        Args:
            messages: List of Message objects from session
            conversation_title: Title for the extracted pattern

        Returns:
            ExtractedPattern or None if extraction fails
        """
        if not messages or len(messages) < 2:
            return None

        # Find problem statement (usually first user message)
        problem = None
        for msg in messages:
            if msg.speaker == "User":
                problem = msg.content
                break

        if not problem:
            return None

        # Find solution (usually in assistant response)
        solution = None
        for msg in messages:
            if msg.speaker == "Assistant":
                solution = msg.content
                break

        if not solution:
            return None

        # Extract reasoning from all assistant messages
        reasoning_parts = []
        for msg in messages:
            if msg.speaker == "Assistant" and len(msg.content) > 20:
                reasoning_parts.append(msg.content)

        reasoning = " ".join(reasoning_parts) if reasoning_parts else solution

        # Determine pattern type from content
        pattern_type = ChatPatternExtractor._infer_pattern_type(problem, solution)

        # Create pattern
        pattern = ExtractedPattern(
            title=conversation_title,
            pattern_type=pattern_type,
            problem=problem[:200],  # Truncate for title
            solution=solution[:300],
            reasoning=reasoning[:500],
        )

        return pattern

    @staticmethod
    def _infer_pattern_type(problem: str, solution: str) -> PatternType:
        """Infer pattern type from problem/solution content."""
        content = (problem + " " + solution).lower()

        # Check for patterns
        if any(keyword in content for keyword in ["bug", "error", "fix", "broken"]):
            return PatternType.BUG_FIX

        if any(keyword in content for keyword in ["optimize", "improve", "performance", "speed"]):
            return PatternType.BEST_PRACTICE

        if any(keyword in content for keyword in ["gotcha", "edge case", "trap", "beware"]):
            return PatternType.GOTCHA

        if any(keyword in content for keyword in ["workaround", "bypass", "hack", "temporary"]):
            return PatternType.WORKAROUND

        if any(keyword in content for keyword in ["integrate", "connect", "combine", "link"]):
            return PatternType.INTEGRATION_GUIDE

        # Default to best practice
        return PatternType.BEST_PRACTICE

    @staticmethod
    def validate_before_submit(pattern: ExtractedPattern) -> Tuple[bool, list[str]]:
        """
        Validate pattern before submission.

        Args:
            pattern: Pattern to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        pattern_dict = pattern.to_dict()

        # Use BOK validator
        is_valid, errors = BokValidator.validate(pattern_dict)

        # Add custom validation
        if pattern.problem and pattern.solution:
            if len(pattern.problem) < 10:
                errors.append("Problem statement too short")

            if len(pattern.solution) < 15:
                errors.append("Solution explanation too short")

        return len(errors) == 0, errors


class ChatPatternIntegration:
    """Integrate pattern extraction with chat workflow."""

    def __init__(self):
        self.extracted_patterns = []
        self.rejected_patterns = []

    def add_pattern_from_chat(
        self,
        messages: list[Message],
        title: str,
        auto_validate: bool = True
    ) -> Dict[str, Any]:
        """
        Add a pattern extracted from chat.

        Args:
            messages: Chat messages
            title: Pattern title
            auto_validate: Validate before adding

        Returns:
            Result dict with status and pattern info
        """
        pattern = ChatPatternExtractor.extract_from_chat_history(messages, title)

        if not pattern:
            return {
                "success": False,
                "error": "Could not extract pattern from chat",
                "pattern": None,
            }

        if auto_validate:
            is_valid, errors = ChatPatternExtractor.validate_before_submit(pattern)

            if not is_valid:
                self.rejected_patterns.append((pattern, errors))
                return {
                    "success": False,
                    "error": "Pattern validation failed",
                    "errors": errors,
                    "pattern": pattern,
                }

        self.extracted_patterns.append(pattern)

        return {
            "success": True,
            "message": "Pattern extracted and stored",
            "pattern": pattern,
        }

    def get_pending_patterns(self) -> list[ExtractedPattern]:
        """Get patterns pending submission."""
        return self.extracted_patterns

    def get_rejected_patterns(self) -> list[Tuple[ExtractedPattern, list[str]]]:
        """Get patterns that failed validation."""
        return self.rejected_patterns

    def clear_pending(self) -> int:
        """Clear pending patterns, return count cleared."""
        count = len(self.extracted_patterns)
        self.extracted_patterns = []
        return count
