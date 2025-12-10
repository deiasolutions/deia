"""
Agent Coordinator - Multi-agent workflow coordination and task routing

This module provides the core coordination layer for DEIA's multi-agent system,
integrating status tracking, message routing, and intelligent task delegation
across multiple AI agents (Claude Code, Claude.ai, ChatGPT, etc.)

Features:
- Real-time agent status tracking and availability management
- Intelligent query routing and delegation
- Task assignment with priority-based queuing
- BOK-aware query classification
- Multi-agent workflow orchestration
- Heartbeat monitoring and health checking

Architecture:
The AgentCoordinator integrates AgentStatusTracker, MessageRouter, and
ContextLoader to provide a unified interface for multi-agent coordination.
It enables the DEIA hive to operate as a cohesive unit.

Created: 2025-10-19
Author: AGENT-005 (Integration Coordinator / BC Liaison)
Task: P1-HIGH - Agent Coordinator Implementation
Version: 3.0
"""

import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional

from deia.services.agent_status import AgentStatusTracker
from deia.services.messaging import MessageRouter, create_task_file
from deia.services.context_loader import ContextLoader

logger = logging.getLogger(__name__)


class AgentCoordinator:
    """
    Central coordinator for multi-agent workflows and task routing.

    Integrates status tracking, message routing, and context loading to enable
    intelligent delegation and coordination across the DEIA agent hive.

    Example:
        coordinator = AgentCoordinator()

        # Route a query to appropriate agent
        result = coordinator.route_query("Fix authentication bug in login.py")

        # Check agent availability
        available = coordinator.get_available_agents()

        # Assign task to specific agent
        coordinator.assign_task("CLAUDE-CODE-003", "Run QA tests", priority="high")
    """

    def __init__(
        self,
        status_tracker: Optional[AgentStatusTracker] = None,
        context_loader: Optional[ContextLoader] = None,
        inbox_dir: Optional[str] = None
    ):
        """
        Initialize AgentCoordinator with service dependencies.

        Args:
            status_tracker: AgentStatusTracker instance (creates default if None)
            context_loader: ContextLoader instance (creates default if None)
            inbox_dir: Message inbox directory (uses default if None)
        """
        # Initialize or use provided services
        self.status_tracker = status_tracker or AgentStatusTracker()

        # ContextLoader requires project_root - use current directory as default
        if context_loader is None:
            try:
                from pathlib import Path
                self.context_loader = ContextLoader(project_root=str(Path.cwd()))
            except Exception as e:
                logger.warning(f"Failed to initialize ContextLoader: {e}")
                self.context_loader = None
        else:
            self.context_loader = context_loader

        self.message_router = MessageRouter(inbox_dir=inbox_dir, status_tracker=self.status_tracker)

        logger.info("AgentCoordinator initialized")

    # ========================================================================
    # Agent Status and Availability
    # ========================================================================

    def get_agent_status(self, agent_id: Optional[str] = None) -> Dict:
        """
        Get status of specific agent or all agents.

        Args:
            agent_id: Agent identifier (None for all agents)

        Returns:
            Dict with agent status information

        Example:
            status = coordinator.get_agent_status("CLAUDE-CODE-001")
            # {"agent_id": "CLAUDE-CODE-001", "status": "idle", "role": "coordinator"}
        """
        if agent_id:
            return self.status_tracker.get_agent_status(agent_id)
        else:
            return self.status_tracker.get_all_agents()

    def get_available_agents(self) -> List[str]:
        """
        Get list of agents currently available (idle status).

        Returns:
            List of agent IDs in idle state

        Example:
            available = coordinator.get_available_agents()
            # ["CLAUDE-CODE-002", "CLAUDE-CODE-004"]
        """
        return self.status_tracker.get_available_agents()

    def register_agent(self, agent_id: str, role: str) -> None:
        """
        Register a new agent in the coordination system.

        Args:
            agent_id: Unique agent identifier
            role: Agent role (coordinator, queen, worker, drone)

        Raises:
            ValueError: If role is invalid

        Example:
            coordinator.register_agent("CLAUDE-CODE-006", "worker")
        """
        self.status_tracker.register_agent(agent_id, role)
        logger.info(f"Registered agent {agent_id} with role {role}")

    def update_agent_heartbeat(
        self,
        agent_id: str,
        status: str,
        current_task: Optional[str] = None
    ) -> None:
        """
        Update agent heartbeat (status and current activity).

        Args:
            agent_id: Agent identifier
            status: Current status (idle, busy, waiting, paused, offline)
            current_task: Description of current task (optional)

        Raises:
            ValueError: If agent_id unknown or status invalid

        Example:
            coordinator.update_agent_heartbeat(
                "CLAUDE-CODE-002",
                "busy",
                "Writing documentation for BOK patterns"
            )
        """
        self.status_tracker.update_heartbeat(agent_id, status, current_task)

    def check_agent_health(self) -> Dict[str, str]:
        """
        Check health of all agents, detect offline/stale states.

        Returns:
            Dict of agents with issues (agent_id -> issue description)

        Example:
            issues = coordinator.check_agent_health()
            # {"CLAUDE-CODE-003": "waiting→idle (timeout)"}
        """
        return self.status_tracker.check_heartbeats()

    # ========================================================================
    # Query Classification and Routing
    # ========================================================================

    def classify_query(self, query: str) -> Dict:
        """
        Classify query to determine routing strategy.

        Uses BOK search and keyword analysis to determine:
        - Query type (code, creative, engineering, bok, general)
        - Complexity level (low, medium, high)
        - Suggested agent
        - Whether can be handled locally
        - Confidence score

        Args:
            query: User query to classify

        Returns:
            Dict with classification metadata

        Example:
            classification = coordinator.classify_query("Fix authentication bug")
            # {
            #     "type": "code",
            #     "complexity": "medium",
            #     "suggested_agent": "CLAUDE_CODE",
            #     "can_handle_locally": False,
            #     "confidence": 0.8
            # }
        """
        # Search BOK for relevant patterns
        try:
            if self.context_loader:
                bok_results = self.context_loader.search_bok(query)
            else:
                bok_results = []
        except Exception as e:
            logger.warning(f"BOK search failed: {e}")
            bok_results = []

        # If BOK has high-quality results, prefer local handling
        if bok_results and len(bok_results) > 0:
            return {
                "type": "bok",
                "complexity": "low",
                "suggested_agent": "local",
                "can_handle_locally": True,
                "confidence": 0.95,
                "bok_results": bok_results
            }

        # Keyword-based classification (order matters - more specific first)
        query_lower = query.lower()

        # Testing/QA keywords (check before engineering to avoid "test design" matching engineering)
        qa_keywords = ["test", "coverage", "qa", "verify", "validate", "pytest", "unittest"]
        # Exclude queries with engineering keywords
        if any(k in query_lower for k in qa_keywords) and not any(k in query_lower for k in ["design", "architecture"]):
            return {
                "type": "qa",
                "complexity": "medium",
                "suggested_agent": "CLAUDE-CODE-003",  # QA specialist
                "can_handle_locally": False,
                "confidence": 0.85
            }

        # Documentation keywords (check before engineering)
        doc_keywords = ["document", "docs", "readme", "guide", "manual", "documentation"]
        # Exclude queries with engineering keywords
        if any(k in query_lower for k in doc_keywords) and not any(k in query_lower for k in ["design", "architecture"]):
            return {
                "type": "documentation",
                "complexity": "medium",
                "suggested_agent": "CLAUDE-CODE-002",  # Documentation lead
                "can_handle_locally": False,
                "confidence": 0.85
            }

        # Engineering/architecture keywords
        engineering_keywords = ["design", "architecture", "system", "api", "interface", "protocol"]
        if any(k in query_lower for k in engineering_keywords):
            return {
                "type": "engineering",
                "complexity": "high",
                "suggested_agent": "CLAUDE_CODE",
                "can_handle_locally": False,
                "confidence": 0.9
            }

        # Code-related keywords
        code_keywords = ["error", "bug", "debug", "fix", "implement", "code", "function", "class"]
        if any(k in query_lower for k in code_keywords):
            return {
                "type": "code",
                "complexity": "medium",
                "suggested_agent": "CLAUDE_CODE",
                "can_handle_locally": False,
                "confidence": 0.8
            }

        # Creative/writing keywords
        creative_keywords = ["write", "poem", "story", "summarize", "explain", "describe"]
        if any(k in query_lower for k in creative_keywords):
            return {
                "type": "creative",
                "complexity": "medium",
                "suggested_agent": "CLAUDE",
                "can_handle_locally": True,
                "confidence": 0.7
            }

        # Default: general query, handle locally
        return {
            "type": "general",
            "complexity": "low",
            "suggested_agent": "local",
            "can_handle_locally": True,
            "confidence": 0.6
        }

    def should_delegate(self, classification: Dict, agent_status: Optional[Dict] = None) -> bool:
        """
        Determine if query should be delegated to another agent.

        Args:
            classification: Query classification from classify_query()
            agent_status: Current agent statuses (fetches if None)

        Returns:
            True if should delegate, False if handle locally

        Example:
            classification = coordinator.classify_query("Fix bug in login.py")
            if coordinator.should_delegate(classification):
                # Route to appropriate agent
                pass
        """
        # Don't delegate if can handle locally with high confidence
        if classification["can_handle_locally"] and classification["confidence"] > 0.8:
            return False

        # Don't delegate if suggested agent is "local"
        if classification["suggested_agent"] == "local":
            return False

        # Check if suggested agent is available
        if agent_status is None:
            agent_status = self.get_agent_status()

        suggested_agent = classification["suggested_agent"]

        # Check availability
        if suggested_agent not in agent_status:
            logger.warning(f"Suggested agent {suggested_agent} not registered")
            return False

        if agent_status[suggested_agent]["status"] != "idle":
            logger.info(f"Suggested agent {suggested_agent} not available (status: {agent_status[suggested_agent]['status']})")
            return False

        # Agent is available, delegate
        return True

    def route_query(self, query: str) -> Dict:
        """
        Route query to appropriate agent or handle locally.

        Combines classification, delegation decision, and task creation into
        a single operation.

        Args:
            query: User query to route

        Returns:
            Dict with routing decision and details:
            {
                "action": "delegate" | "local",
                "agent": agent_id or "local",
                "classification": {...},
                "task_file": path (if delegated),
                "reason": explanation
            }

        Example:
            result = coordinator.route_query("Write tests for login.py")
            # {
            #     "action": "delegate",
            #     "agent": "CLAUDE-CODE-003",
            #     "classification": {...},
            #     "task_file": "/path/to/task.md",
            #     "reason": "QA specialist available"
            # }
        """
        # Classify query
        classification = self.classify_query(query)
        agent_status = self.get_agent_status()

        # Determine if should delegate
        if self.should_delegate(classification, agent_status):
            # Delegate to suggested agent
            agent_id = classification["suggested_agent"]

            try:
                task_file = self.create_delegation_task(query, agent_id)
                return {
                    "action": "delegate",
                    "agent": agent_id,
                    "classification": classification,
                    "task_file": task_file,
                    "reason": f"{classification['type']} query routed to {agent_id}"
                }
            except Exception as e:
                logger.error(f"Failed to create delegation task: {e}")
                return {
                    "action": "local",
                    "agent": "local",
                    "classification": classification,
                    "reason": f"Delegation failed: {e}, handling locally"
                }
        else:
            # Handle locally
            return {
                "action": "local",
                "agent": "local",
                "classification": classification,
                "reason": classification.get("can_handle_locally", False) and "High confidence local handling" or "No suitable agent available"
            }

    # ========================================================================
    # Task Management and Delegation
    # ========================================================================

    def create_delegation_task(self, query: str, agent_id: str, from_agent: str = "CHATGPT") -> str:
        """
        Create task file for delegating query to another agent.

        Args:
            query: Query to delegate
            agent_id: Target agent ID
            from_agent: Source agent ID (default: CHATGPT)

        Returns:
            Path to created task file

        Raises:
            RuntimeError: If file creation fails

        Example:
            task_file = coordinator.create_delegation_task(
                "Fix authentication bug",
                "CLAUDE-CODE-001"
            )
        """
        now = datetime.datetime.now()
        subject = query[:30].replace(" ", "-").replace("/", "-")

        task_content = f"""# User Query Delegation

**From:** {from_agent}
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

---

**Priority:** Normal
**Status:** Pending
"""

        try:
            # Use messaging system's create_task_file function
            task_file = create_task_file(
                from_agent=from_agent,
                to_agent=agent_id,
                task_type="QUERY",
                subject=subject,
                content=task_content
            )

            logger.info(f"Created delegation task: {task_file}")
            return task_file

        except PermissionError as e:
            logger.error(f"Permission denied creating task file: {e}")
            raise RuntimeError(f"Failed to create task file: permission denied") from e

        except OSError as e:
            logger.error(f"OS error creating task file: {e}")
            raise RuntimeError(f"Failed to create task file: {e}") from e

        except Exception as e:
            logger.error(f"Unexpected error creating task file: {e}")
            raise RuntimeError(f"Failed to create task file: {e}") from e

    def assign_task(
        self,
        agent_id: str,
        task_description: str,
        priority: str = "normal",
        from_agent: str = "COORDINATOR"
    ) -> str:
        """
        Assign task to specific agent.

        Args:
            agent_id: Target agent ID
            task_description: Description of task
            priority: Priority level (low, normal, high, critical)
            from_agent: Source agent (default: COORDINATOR)

        Returns:
            Path to created task file

        Raises:
            ValueError: If agent not registered
            RuntimeError: If task creation fails

        Example:
            coordinator.assign_task(
                "CLAUDE-CODE-003",
                "Run comprehensive QA tests on authentication module",
                priority="high"
            )
        """
        # Verify agent exists
        agent_status = self.get_agent_status(agent_id)
        if agent_status.get("status") == "unknown":
            raise ValueError(f"Agent {agent_id} not registered")

        # Map priority to message type
        priority_map = {
            "critical": "ESCALATE",
            "high": "TASK",
            "normal": "TASK",
            "low": "TASK"
        }
        message_type = priority_map.get(priority, "TASK")

        # Create task content
        now = datetime.datetime.now()
        subject = task_description[:30].replace(" ", "-").replace("/", "-")

        task_content = f"""# Task Assignment

**From:** {from_agent}
**To:** {agent_id}
**Type:** TASK
**Priority:** {priority.upper()}
**Date:** {now.isoformat()}

---

## Task Description

{task_description}

## Priority

{priority.upper()}

## Status

Pending - awaiting agent acceptance

---

**Assigned:** {now.strftime("%Y-%m-%d %H:%M")} UTC
"""

        try:
            task_file = create_task_file(
                from_agent=from_agent,
                to_agent=agent_id,
                task_type=message_type,
                subject=subject,
                content=task_content
            )

            logger.info(f"Assigned task to {agent_id}: {task_file}")
            return task_file

        except Exception as e:
            logger.error(f"Failed to assign task: {e}")
            raise RuntimeError(f"Task assignment failed: {e}") from e

    def broadcast_message(
        self,
        message: str,
        message_type: str = "REPORT",
        from_agent: str = "COORDINATOR"
    ) -> List[str]:
        """
        Broadcast message to all agents.

        Args:
            message: Message content
            message_type: Message type (REPORT, ALERT, etc.)
            from_agent: Source agent (default: COORDINATOR)

        Returns:
            List of created message file paths

        Example:
            coordinator.broadcast_message(
                "Critical security update deployed - all agents verify",
                message_type="ALERT"
            )
        """
        now = datetime.datetime.now()
        subject = message[:30].replace(" ", "-").replace("/", "-")

        content = f"""# Broadcast Message

**From:** {from_agent}
**To:** ALL
**Type:** {message_type}
**Date:** {now.isoformat()}

---

## Message

{message}

---

**Broadcast:** {now.strftime("%Y-%m-%d %H:%M")} UTC
"""

        try:
            task_file = create_task_file(
                from_agent=from_agent,
                to_agent="ALL",
                task_type=message_type,
                subject=subject,
                content=content
            )

            logger.info(f"Broadcast message to all agents: {task_file}")
            return [task_file]

        except Exception as e:
            logger.error(f"Failed to broadcast message: {e}")
            raise RuntimeError(f"Broadcast failed: {e}") from e

    # ========================================================================
    # Dashboard and Monitoring
    # ========================================================================

    def render_dashboard(self) -> str:
        """
        Render coordination dashboard showing all agent statuses.

        Returns:
            Formatted dashboard string

        Example:
            print(coordinator.render_dashboard())
        """
        return self.status_tracker.render_dashboard()

    def get_coordination_summary(self) -> Dict:
        """
        Get summary of coordination system state.

        Returns:
            Dict with:
            - total_agents: Total registered agents
            - online_agents: Agents with recent heartbeats
            - idle_agents: Available agents
            - busy_agents: Agents currently working
            - offline_agents: Agents with stale heartbeats
            - queue_stats: Message queue statistics

        Example:
            summary = coordinator.get_coordination_summary()
            # {
            #     "total_agents": 5,
            #     "online_agents": 4,
            #     "idle_agents": 2,
            #     "busy_agents": 2,
            #     "offline_agents": 1
            # }
        """
        all_agents = self.get_agent_status()

        online = sum(1 for a in all_agents.values() if a["status"] != "offline")
        idle = sum(1 for a in all_agents.values() if a["status"] == "idle")
        busy = sum(1 for a in all_agents.values() if a["status"] == "busy")
        offline = sum(1 for a in all_agents.values() if a["status"] == "offline")

        return {
            "total_agents": len(all_agents),
            "online_agents": online,
            "idle_agents": idle,
            "busy_agents": busy,
            "offline_agents": offline,
            "last_check": datetime.datetime.now().isoformat()
        }
