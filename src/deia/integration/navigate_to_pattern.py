"""
Navigate and link between chat context and BOK patterns.

Cross-reference chat conversations with relevant BOK patterns.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class PatternReference:
    """Reference to a BOK pattern."""

    pattern_id: str
    pattern_title: str
    category: str
    relevance_score: float
    reason: str


class PatternNavigator:
    """Navigate between chat and BOK patterns."""

    # Keyword to category mapping
    CATEGORY_KEYWORDS = {
        "best_practices": [
            "best practice",
            "should",
            "recommended",
            "standard",
            "proper way",
        ],
        "bug_fixes": [
            "bug",
            "error",
            "issue",
            "broken",
            "crash",
            "fail",
        ],
        "gotchas": [
            "gotcha",
            "edge case",
            "trap",
            "beware",
            "careful",
            "easy to miss",
        ],
        "workarounds": [
            "workaround",
            "bypass",
            "hack",
            "temporary fix",
            "deal with",
        ],
        "architecture_decisions": [
            "architecture",
            "design",
            "structure",
            "pattern",
            "approach",
        ],
    }

    @staticmethod
    def find_relevant_patterns(
        chat_content: str,
        bok_index: Dict[str, List[Dict]],
        top_k: int = 5
    ) -> List[PatternReference]:
        """
        Find relevant BOK patterns for chat content.

        Args:
            chat_content: Chat conversation content
            bok_index: BOK index with patterns
            top_k: Return top K results

        Returns:
            List of relevant PatternReference objects
        """
        content_lower = chat_content.lower()
        matches = []

        patterns = bok_index.get("patterns", [])

        for pattern in patterns:
            score = 0
            reason_parts = []

            # Check category keywords
            for category, keywords in PatternNavigator.CATEGORY_KEYWORDS.items():
                if pattern.get("category") == category:
                    for keyword in keywords:
                        if keyword in content_lower:
                            score += 2
                            reason_parts.append(f"Contains '{keyword}'")

            # Check pattern title
            title = pattern.get("title", "").lower()
            if title:
                title_words = set(title.split())
                content_words = set(content_lower.split())
                overlap = len(title_words & content_words)
                score += overlap
                if overlap > 0:
                    reason_parts.append(f"Title overlap ({overlap} words)")

            # Check pattern type
            pattern_type = pattern.get("type", "").lower()
            if pattern_type and pattern_type in content_lower:
                score += 1.5
                reason_parts.append(f"Type matches")

            if score > 0:
                ref = PatternReference(
                    pattern_id=pattern.get("id", "unknown"),
                    pattern_title=pattern.get("title", "Untitled"),
                    category=pattern.get("category", "unknown"),
                    relevance_score=score,
                    reason="; ".join(reason_parts) if reason_parts else "Content match",
                )
                matches.append(ref)

        # Sort by relevance and return top k
        matches.sort(key=lambda x: x.relevance_score, reverse=True)
        return matches[:top_k]

    @staticmethod
    def create_navigation_link(
        pattern_id: str,
        pattern_title: str,
        context_snippet: str
    ) -> Dict[str, str]:
        """
        Create a navigation link from chat to pattern.

        Args:
            pattern_id: Pattern ID in BOK
            pattern_title: Pattern title
            context_snippet: Relevant context from chat

        Returns:
            Navigation link dictionary
        """
        return {
            "pattern_id": pattern_id,
            "pattern_title": pattern_title,
            "context": context_snippet,
            "link_type": "chat_to_pattern",
            "timestamp": None,  # Should be filled by caller
        }

    @staticmethod
    def get_pattern_summary(
        pattern: Dict,
        max_length: int = 200
    ) -> str:
        """
        Get a brief summary of a pattern for chat display.

        Args:
            pattern: Pattern dictionary
            max_length: Max length of summary

        Returns:
            Brief pattern summary
        """
        title = pattern.get("title", "Unknown")
        category = pattern.get("category", "General")
        pattern_type = pattern.get("type", "pattern")

        summary = f"**{title}** ({category} - {pattern_type})"

        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return summary


class CrossReferenceManager:
    """Manage cross-references between chat and BOK."""

    def __init__(self):
        self.active_references: List[Dict] = []
        self.reference_history: List[Dict] = []

    def add_reference(
        self,
        pattern_id: str,
        pattern_title: str,
        chat_context: str,
        relevance_score: float
    ) -> None:
        """Add a cross-reference."""
        ref = {
            "pattern_id": pattern_id,
            "pattern_title": pattern_title,
            "chat_context": chat_context,
            "relevance_score": relevance_score,
        }
        self.active_references.append(ref)

    def get_active_references(self) -> List[Dict]:
        """Get currently active references."""
        return self.active_references

    def clear_references(self) -> int:
        """Clear active references, return count cleared."""
        count = len(self.active_references)
        self.reference_history.extend(self.active_references)
        self.active_references = []
        return count

    def get_reference_history(self) -> List[Dict]:
        """Get history of all references."""
        return self.reference_history
