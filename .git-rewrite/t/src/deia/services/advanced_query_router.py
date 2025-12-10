import logging
import re
from typing import List, NamedTuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Agent(NamedTuple):
    id: str
    capabilities: List[str]

class Match(NamedTuple):
    agent_id: str
    match_score: float
    confidence_level: str
    reasoning: str

class RoutingDecision(NamedTuple):
    primary_agent_id: str
    fallback_agent_id: str
    confidence_score: float
    routing_reasoning: str
    estimated_duration_minutes: int

class AdvancedQueryRouter:
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def score_complexity(self, query: str) -> int:
        words = len(query.split())
        technical_terms = len(re.findall(r"\b[A-Z]{2,}\b", query))
        ambiguity_indicators = len(re.findall(r"\b(or|versus|vs|compared to)\b", query, re.IGNORECASE))
        multi_step_indicators = len(re.findall(r"\b(then|next|after|once|finally)\b", query, re.IGNORECASE))
        code_keywords = len(re.findall(r"\b(function|class|variable|method|import|library)\b", query, re.IGNORECASE))

        complexity_score = (
            words / 10 +
            technical_terms * 2 +
            ambiguity_indicators * 3 +
            multi_step_indicators * 2 +
            code_keywords * 3
        )

        return min(int(complexity_score), 10)

    def match_capabilities(self, query: str, agents: List[Agent]) -> List[Match]:
        matches = []
        for agent in agents:
            match_score = sum(keyword in query.lower() for keyword in agent.capabilities) / len(agent.capabilities)
            confidence_level = "high" if match_score >= 0.8 else "medium" if match_score >= 0.5 else "low"
            reasoning = f"Matched {int(match_score * 100)}% of agent capabilities"
            matches.append(Match(agent.id, match_score, confidence_level, reasoning))

        return sorted(matches, key=lambda x: x.match_score, reverse=True)

    def route_with_confidence(self, query: str, agents: List[Agent], min_confidence: float = 0.7) -> RoutingDecision:
        complexity_score = self.score_complexity(query)
        capability_matches = self.match_capabilities(query, agents)

        primary_match = capability_matches[0] if capability_matches else None
        fallback_match = capability_matches[1] if len(capability_matches) > 1 else None

        if primary_match and primary_match.match_score >= min_confidence:
            routing_reasoning = f"High confidence match with {primary_match.agent_id} based on capabilities"
            confidence_score = primary_match.match_score
            estimated_duration = complexity_score * 2  # Assuming 2 minutes per complexity point
        elif fallback_match and fallback_match.match_score >= min_confidence:
            routing_reasoning = f"Fallback to {fallback_match.agent_id} due to lower confidence in primary match"
            confidence_score = fallback_match.match_score
            estimated_duration = complexity_score * 3  # Assuming 3 minutes per complexity point for fallback
        else:
            routing_reasoning = "No agents matched with sufficient confidence, routing to default agent"
            confidence_score = 0.0
            estimated_duration = complexity_score * 4  # Assuming 4 minutes per complexity point for default

        return RoutingDecision(
            primary_agent_id=primary_match.agent_id if primary_match else "DEFAULT_AGENT",
            fallback_agent_id=fallback_match.agent_id if fallback_match else "DEFAULT_AGENT",
            confidence_score=confidence_score,
            routing_reasoning=routing_reasoning,
            estimated_duration_minutes=estimated_duration
        )

# Usage example
if __name__ == "__main__":
    agents = [
        Agent("ClaudeCode", ["python", "debugging", "algorithms", "optimization"]),
        Agent("ClaudeDialog", ["conversation", "writing", "proofreading", "storytelling"]),
        Agent("ClaudeVision", ["image analysis", "computer vision", "object detection", "ocr"]),
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
