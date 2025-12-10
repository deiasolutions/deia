"""
Advanced Query Router for DEIA

Routes user queries to appropriate agents based on complexity analysis
and capability matching. Provides confidence scores and fallback routing.

Part of DEIA Phase 3 (Agent BC delivery).
"""

import logging
import re
from typing import List, NamedTuple, Optional

logger = logging.getLogger(__name__)


class Agent(NamedTuple):
    """Represents an agent with specific capabilities.

    Attributes:
        id: Unique identifier for the agent
        capabilities: List of capability keywords (e.g., "python", "debugging")
    """
    id: str
    capabilities: List[str]


class Match(NamedTuple):
    """Represents a capability match result.

    Attributes:
        agent_id: ID of the matched agent
        match_score: Score from 0.0 to 1.0 indicating match quality
        confidence_level: "high" (>=0.8), "medium" (>=0.5), or "low" (<0.5)
        reasoning: Human-readable explanation of the match
    """
    agent_id: str
    match_score: float
    confidence_level: str
    reasoning: str


class RoutingDecision(NamedTuple):
    """Represents a query routing decision.

    Attributes:
        primary_agent_id: ID of the primary agent to route to
        fallback_agent_id: ID of the fallback agent if primary fails
        confidence_score: Confidence in routing decision (0.0-1.0)
        routing_reasoning: Human-readable explanation of routing logic
        estimated_duration_minutes: Estimated time to complete the query
    """
    primary_agent_id: str
    fallback_agent_id: str
    confidence_score: float
    routing_reasoning: str
    estimated_duration_minutes: int


class AdvancedQueryRouter:
    """Routes queries to agents based on complexity and capability matching.

    This router analyzes query complexity (word count, technical terms,
    multi-step indicators) and matches queries to agent capabilities with
    confidence scoring.

    Example:
        >>> agents = [
        ...     Agent("CLAUDE-CODE-001", ["python", "debugging", "optimization"]),
        ...     Agent("CLAUDE-CODE-002", ["documentation", "writing"]),
        ... ]
        >>> router = AdvancedQueryRouter(agents)
        >>> decision = router.route_with_confidence(
        ...     "How do I optimize a Python function?",
        ...     agents
        ... )
        >>> decision.primary_agent_id
        'CLAUDE-CODE-001'
    """

    def __init__(self, agents: List[Agent]):
        """Initialize the query router with a list of agents.

        Args:
            agents: List of Agent instances with capabilities defined
        """
        self.agents = agents
        logger.info(f"AdvancedQueryRouter initialized with {len(agents)} agents")

    def score_complexity(self, query: str) -> int:
        """Score query complexity from 1-10 based on multiple factors.

        Complexity factors:
        - Word count (longer queries = more complex)
        - Technical terms (uppercase acronyms like API, HTTP)
        - Ambiguity indicators ("or", "versus", "compared to")
        - Multi-step indicators ("then", "next", "after")
        - Code keywords ("function", "class", "method")

        Args:
            query: The user query string

        Returns:
            Complexity score from 1-10 (capped at 10)

        Example:
            >>> router = AdvancedQueryRouter([])
            >>> router.score_complexity("What is Python?")
            1
            >>> router.score_complexity("How do I optimize a Python function for time complexity?")
            5
        """
        words = len(query.split())
        technical_terms = len(re.findall(r"\b[A-Z]{2,}\b", query))
        ambiguity_indicators = len(re.findall(
            r"\b(or|versus|vs|compared to)\b", query, re.IGNORECASE
        ))
        multi_step_indicators = len(re.findall(
            r"\b(then|next|after|once|finally)\b", query, re.IGNORECASE
        ))
        code_keywords = len(re.findall(
            r"\b(function|class|variable|method|import|library)\b", query, re.IGNORECASE
        ))

        complexity_score = (
            words / 10 +
            technical_terms * 2 +
            ambiguity_indicators * 3 +
            multi_step_indicators * 2 +
            code_keywords * 3
        )

        score = min(int(complexity_score), 10)
        logger.debug(f"Query complexity score: {score} for query: {query[:50]}...")
        return score

    def match_capabilities(self, query: str, agents: List[Agent]) -> List[Match]:
        """Match query to agent capabilities and return sorted matches.

        Calculates match score as percentage of agent capabilities found
        in the query string (case-insensitive).

        Confidence levels:
        - high: >=80% of capabilities matched
        - medium: >=50% of capabilities matched
        - low: <50% of capabilities matched

        Args:
            query: The user query string
            agents: List of Agent instances to match against

        Returns:
            List of Match instances sorted by match_score (highest first)

        Example:
            >>> agents = [Agent("A", ["python", "debugging"])]
            >>> router = AdvancedQueryRouter(agents)
            >>> matches = router.match_capabilities("Debug Python code", agents)
            >>> matches[0].match_score
            1.0
        """
        matches = []
        query_lower = query.lower()

        for agent in agents:
            if not agent.capabilities:
                logger.warning(f"Agent {agent.id} has no capabilities defined")
                continue

            matched_caps = sum(
                keyword.lower() in query_lower
                for keyword in agent.capabilities
            )
            match_score = matched_caps / len(agent.capabilities)

            if match_score >= 0.8:
                confidence_level = "high"
            elif match_score >= 0.5:
                confidence_level = "medium"
            else:
                confidence_level = "low"

            reasoning = f"Matched {int(match_score * 100)}% of agent capabilities"
            matches.append(Match(agent.id, match_score, confidence_level, reasoning))

        sorted_matches = sorted(matches, key=lambda x: x.match_score, reverse=True)
        logger.debug(
            f"Found {len(sorted_matches)} matches, "
            f"best: {sorted_matches[0].agent_id if sorted_matches else 'none'}"
        )
        return sorted_matches

    def route_with_confidence(
        self,
        query: str,
        agents: List[Agent],
        min_confidence: float = 0.7
    ) -> RoutingDecision:
        """Route query to best-matched agent with confidence scoring.

        Routing logic:
        1. Score query complexity (1-10)
        2. Match capabilities to find best agents
        3. If primary match >= min_confidence: route to primary
        4. Elif fallback match >= min_confidence: route to fallback
        5. Else: route to DEFAULT_AGENT

        Estimated duration = complexity_score * multiplier:
        - Primary match: 2 min per complexity point
        - Fallback match: 3 min per complexity point
        - Default: 4 min per complexity point

        Args:
            query: The user query string
            agents: List of Agent instances to route to
            min_confidence: Minimum match score required (default: 0.7)

        Returns:
            RoutingDecision with primary/fallback agents and reasoning

        Example:
            >>> agents = [Agent("CODE", ["python"]), Agent("DOC", ["writing"])]
            >>> router = AdvancedQueryRouter(agents)
            >>> decision = router.route_with_confidence("Fix Python bug", agents)
            >>> decision.primary_agent_id
            'CODE'
        """
        complexity_score = self.score_complexity(query)
        capability_matches = self.match_capabilities(query, agents)

        primary_match: Optional[Match] = capability_matches[0] if capability_matches else None
        fallback_match: Optional[Match] = (
            capability_matches[1] if len(capability_matches) > 1 else None
        )

        if primary_match and primary_match.match_score >= min_confidence:
            routing_reasoning = (
                f"High confidence match with {primary_match.agent_id} "
                f"based on capabilities"
            )
            confidence_score = primary_match.match_score
            estimated_duration = complexity_score * 2
            primary_agent = primary_match.agent_id
            fallback_agent = fallback_match.agent_id if fallback_match else "DEFAULT_AGENT"

        elif fallback_match and fallback_match.match_score >= min_confidence:
            routing_reasoning = (
                f"Fallback to {fallback_match.agent_id} due to "
                f"lower confidence in primary match"
            )
            confidence_score = fallback_match.match_score
            estimated_duration = complexity_score * 3
            primary_agent = fallback_match.agent_id
            fallback_agent = "DEFAULT_AGENT"

        else:
            routing_reasoning = (
                "No agents matched with sufficient confidence, "
                "routing to default agent"
            )
            confidence_score = 0.0
            estimated_duration = complexity_score * 4
            primary_agent = "DEFAULT_AGENT"
            fallback_agent = "DEFAULT_AGENT"

        decision = RoutingDecision(
            primary_agent_id=primary_agent,
            fallback_agent_id=fallback_agent,
            confidence_score=confidence_score,
            routing_reasoning=routing_reasoning,
            estimated_duration_minutes=estimated_duration
        )

        logger.info(
            f"Routed query to {decision.primary_agent_id} "
            f"(confidence: {decision.confidence_score:.2f})"
        )
        return decision


# Example usage for testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    agents = [
        Agent("CLAUDE-CODE-001", ["python", "debugging", "algorithms", "optimization"]),
        Agent("CLAUDE-CODE-002", ["conversation", "writing", "proofreading", "storytelling"]),
        Agent("CLAUDE-CODE-003", ["image analysis", "computer vision", "object detection", "ocr"]),
    ]

    router = AdvancedQueryRouter(agents)

    query1 = "How do I optimize a Python function for time complexity?"
    decision1 = router.route_with_confidence(query1, agents)
    logger.info(f"Query: {query1}")
    logger.info(f"Routing Decision: {decision1}")

    query2 = "Can you proofread my essay and provide feedback on the story structure?"
    decision2 = router.route_with_confidence(query2, agents)
    logger.info(f"Query: {query2}")
    logger.info(f"Routing Decision: {decision2}")
