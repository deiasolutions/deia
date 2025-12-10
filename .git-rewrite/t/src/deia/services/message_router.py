"""
Message Router - Automatically route commands to appropriate bot.

Analyzes user messages and routes to bot matching required category.
Supports manual override via @bot syntax.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
import re


@dataclass
class RoutingDecision:
    """A message routing decision."""
    message: str
    detected_category: str
    recommended_bot: str
    confidence: float  # 0-1
    override_bot: Optional[str]  # @bot-001 override if present
    final_bot: str  # recommended_bot or override_bot
    reasoning: str


class MessageRouter:
    """Route messages to appropriate bots based on content analysis."""

    def __init__(self):
        """Initialize message router."""
        # Bot categories and keywords
        self.bot_categories = {
            "dev": {
                "keywords": ["code", "python", "javascript", "function", "debug", "error", "fix", "implement", "refactor", "class", "module", "import"],
                "patterns": [r"\.py\b", r"\.js\b", r"\.ts\b", r"def\s+\w+", r"function\s+\w+", r"class\s+\w+"],
                "confidence": 0.9
            },
            "qa": {
                "keywords": ["test", "testing", "unit test", "integration test", "assert", "mock", "stub", "pytest", "jest", "coverage"],
                "patterns": [r"test_\w+", r"\.test\.", r"@test", r"it\("],
                "confidence": 0.85
            },
            "docs": {
                "keywords": ["document", "readme", "guide", "tutorial", "explanation", "write", "describe", "documentation", "spec", "requirement"],
                "patterns": [r"\.md\b", r"README", r"CONTRIBUTING"],
                "confidence": 0.8
            },
            "analysis": {
                "keywords": ["analyze", "analyze", "metrics", "performance", "data", "statistics", "report", "trend", "pattern"],
                "patterns": [r"\.json\b", r"\.csv\b", r"analytics"],
                "confidence": 0.75
            },
            "ops": {
                "keywords": ["deploy", "infrastructure", "devops", "monitoring", "health", "capacity", "scaling", "database", "backup"],
                "patterns": [r"\.yaml\b", r"\.yml\b", r"docker", r"kubernetes"],
                "confidence": 0.8
            }
        }

        # Default bot assignments per category
        self.category_to_bot = {
            "dev": "bot-001",
            "qa": "bot-002",
            "docs": "bot-004",
            "analysis": "bot-003",
            "ops": "bot-001"
        }

        self.routing_log = Path(".deia/bot-logs/message-routing.jsonl")
        self.routing_log.parent.mkdir(parents=True, exist_ok=True)

    def route_message(self, message: str) -> RoutingDecision:
        """
        Route a message to appropriate bot.

        Args:
            message: User message to route

        Returns:
            RoutingDecision with routing details
        """
        # Check for manual override (@bot-001 syntax)
        override_bot = self._extract_bot_override(message)
        clean_message = self._remove_override_syntax(message)

        # Detect category
        category, confidence = self._detect_category(clean_message)
        recommended_bot = self.category_to_bot.get(category, "bot-001")

        # Determine final bot
        final_bot = override_bot if override_bot else recommended_bot

        # Generate reasoning
        reasoning = self._generate_reasoning(category, confidence, override_bot)

        decision = RoutingDecision(
            message=clean_message,
            detected_category=category,
            recommended_bot=recommended_bot,
            confidence=confidence,
            override_bot=override_bot,
            final_bot=final_bot,
            reasoning=reasoning
        )

        self._log_routing(decision)
        return decision

    def get_all_categories(self) -> Dict[str, Any]:
        """Get all available bot categories."""
        return {
            category: {
                "bot": self.category_to_bot[category],
                "keywords": self.bot_categories[category]["keywords"][:5],  # First 5 keywords
                "confidence": self.bot_categories[category]["confidence"]
            }
            for category in self.bot_categories.keys()
        }

    def _detect_category(self, message: str) -> Tuple[str, float]:
        """
        Detect message category based on content.

        Args:
            message: Message to analyze

        Returns:
            (category, confidence) tuple
        """
        message_lower = message.lower()
        scores = {}

        for category, config in self.bot_categories.items():
            score = 0

            # Check keywords
            keyword_matches = sum(1 for kw in config["keywords"] if kw in message_lower)
            if keyword_matches > 0:
                score += keyword_matches * 0.1

            # Check patterns
            pattern_matches = sum(1 for pattern in config["patterns"] if re.search(pattern, message, re.IGNORECASE))
            if pattern_matches > 0:
                score += pattern_matches * 0.15

            scores[category] = min(score, 1.0)  # Cap at 1.0

        # Find best match
        if not scores or max(scores.values()) == 0:
            return ("dev", 0.5)  # Default to dev if no matches

        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]

        # Boost confidence if strong match
        if best_score > 0.3:
            confidence = min(best_score * self.bot_categories[best_category]["confidence"], 0.99)
        else:
            confidence = 0.5

        return (best_category, confidence)

    def _extract_bot_override(self, message: str) -> Optional[str]:
        """
        Extract bot override from message (@bot-001 syntax).

        Args:
            message: Message to parse

        Returns:
            Bot ID if override found, else None
        """
        match = re.search(r'@(bot-\d+)\b', message)
        if match:
            return match.group(1)
        return None

    def _remove_override_syntax(self, message: str) -> str:
        """Remove @bot-XXX override syntax from message."""
        return re.sub(r'@bot-\d+\s*', '', message).strip()

    def _generate_reasoning(self, category: str, confidence: float, override_bot: Optional[str]) -> str:
        """Generate human-readable reasoning for routing decision."""
        if override_bot:
            return f"Manual override to {override_bot}"

        if confidence > 0.8:
            return f"Strong match for {category} category ({confidence:.0%} confidence)"
        elif confidence > 0.5:
            return f"Moderate match for {category} category ({confidence:.0%} confidence)"
        else:
            return f"Weak match for {category}, routing to default bot"

    def _log_routing(self, decision: RoutingDecision) -> None:
        """Log routing decision."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message_preview": decision.message[:100],
            "category": decision.detected_category,
            "confidence": decision.confidence,
            "recommended_bot": decision.recommended_bot,
            "override_bot": decision.override_bot,
            "final_bot": decision.final_bot
        }

        try:
            with open(self.routing_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[MESSAGE-ROUTER] Failed to log: {e}")
