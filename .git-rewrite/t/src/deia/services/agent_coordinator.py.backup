"""Agent Coordinator"""

import datetime
import logging
from pathlib import Path
from typing import Dict

from deia.services.agent_status import AgentStatusTracker
from deia.services.deia_context import DEIAContextLoader

logger = logging.getLogger(__name__)

class AgentCoordinator:
    """Integrates with multi-agent system"""

    def __init__(self, status_tracker: AgentStatusTracker, context_loader: DEIAContextLoader):
        """Initialize with status tracker and context loader instances"""
        self.status_tracker = status_tracker
        self.context_loader = context_loader

    def get_agent_status(self) -> Dict:
        """Get all agent statuses from tracker"""
        return self.status_tracker.get_all_agents()

    def route_query(self, query: str) -> str:
        """Determine which agent should handle the query"""
        classification = self.classify_query(query)
        agent_status = self.get_agent_status()
        if self.should_delegate(classification, agent_status):
            return classification["suggested_agent"]
        else:
            return "local"

    def classify_query(self, query: str) -> Dict:
        """Classify query to determine routing"""
        # PERFORMANCE FIX: Use BOK results in classification (was unused before)
        bok_results = self.context_loader.search_bok(query)

        code_keywords = ["error", "bug", "debug", "fix", "implement", "code"]
        creative_keywords = ["write", "poem", "story", "summarize", "explain"]
        engineering_keywords = ["design", "architecture", "system", "api", "interface"]

        # Check BOK first - if we have high-quality BOK results, prefer local
        if bok_results and len(bok_results) > 0:
            return {
                "type": "bok",
                "complexity": "low",
                "suggested_agent": "local",
                "can_handle_locally": True,
                "confidence": 0.95,
                "bok_results": bok_results  # Include results for potential use
            }

        # Then check other keywords
        if any(k in query.lower() for k in code_keywords):
            return {
                "type": "code",
                "complexity": "high" if "design" in query.lower() else "medium",
                "suggested_agent": "CLAUDE_CODE",
                "can_handle_locally": False,
                "confidence": 0.8
            }
        elif any(k in query.lower() for k in creative_keywords):
            return {
                "type": "creative",
                "complexity": "medium",
                "suggested_agent": "CLAUDE",
                "can_handle_locally": True,
                "confidence": 0.7
            }
        elif any(k in query.lower() for k in engineering_keywords):
            return {
                "type": "engineering",
                "complexity": "high",
                "suggested_agent": "CLAUDE_CODE",
                "can_handle_locally": False,
                "confidence": 0.9
            }
        else:
            return {
                "type": "general",
                "complexity": "low",
                "suggested_agent": "local",
                "can_handle_locally": True,
                "confidence": 0.6
            }

    def should_delegate(self, classification: Dict, agent_status: Dict) -> bool:
        """Determine if query should be delegated"""
        if classification["can_handle_locally"] and classification["confidence"] > 0.8:
            return False
        if classification["suggested_agent"] == "local":
            return False
        agent = classification["suggested_agent"]
        if agent not in agent_status or agent_status[agent]["status"] != "idle":
            return False
        return True

    def create_delegation_task(self, query: str, agent_id: str) -> str:
        """Create task file for messaging system

        Args:
            query: The user query to delegate
            agent_id: The target agent ID

        Returns:
            Path to created task file

        Raises:
            RuntimeError: If file creation fails
        """
        now = datetime.datetime.now()
        subject = query[:30].replace(" ", "-")

        task_content = f"""# User Query Delegation

**From:** CHATGPT
**To:** {agent_id}
**Type:** QUERY
**Date:** {now.isoformat()}

---

## User Query

{query}

## Delegation Reason

Query requires {agent_id}'s specialized capabilities.

## Expected Response

Provide an answer suitable for display in the chat interface.
"""

        # ERROR HANDLING FIX: Add comprehensive error handling for file operations
        try:
            task_dir = Path.home() / "Downloads" / "uploads"
            task_dir.mkdir(exist_ok=True, parents=True)

            task_file = task_dir / f"{now.strftime('%Y-%m-%d-%H%M')}-CHATGPT-{agent_id}-QUERY-{subject}.md"

            with task_file.open("w", encoding='utf-8') as f:
                f.write(task_content)

            logger.info(f"Created delegation task: {task_file}")
            return str(task_file)

        except PermissionError as e:
            logger.error(f"Permission denied creating task file: {e}")
            raise RuntimeError(f"Failed to create task file: permission denied") from e

        except OSError as e:
            logger.error(f"OS error creating task file: {e}")
            raise RuntimeError(f"Failed to create task file: {e}") from e

        except Exception as e:
            logger.error(f"Unexpected error creating task file: {e}")
            raise RuntimeError(f"Failed to create task file: {e}") from e
