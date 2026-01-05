from dataclasses import dataclass
from typing import Dict


@dataclass
class RouteDecision:
    lane: str
    provider: str
    delivery: str


def decide_route(task: Dict) -> RouteDecision:
    """Simple routing stub to be expanded."""
    intent = task.get("intent", "general")
    if intent in ("design", "planning"):
        return RouteDecision(lane="llm", provider="default", delivery="cache_prompt")
    if intent == "code":
        return RouteDecision(lane="terminal", provider="cli", delivery="task_file")
    return RouteDecision(lane="llm", provider="default", delivery="cache_prompt")
