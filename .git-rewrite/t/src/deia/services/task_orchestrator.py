"""
Task Orchestrator - Route tasks to best bot based on type and capacity.

Analyzes incoming tasks, determines optimal bot, handles load balancing.
Enables multi-bot parallel execution with intelligent routing.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path
import json
import re


class BotType(Enum):
    """Specializations of different bots."""
    GENERAL = "general"          # Can handle any task
    DEVELOPER = "developer"      # Code tasks, technical work
    ANALYZER = "analyzer"        # Analysis, research tasks
    WRITER = "writer"            # Writing, documentation
    PLANNER = "planner"          # Coordination, planning
    VALIDATOR = "validator"      # Testing, validation


@dataclass
class BotCapability:
    """What a bot is specialized for."""
    bot_id: str
    bot_type: BotType
    specializations: List[str] = field(default_factory=list)  # e.g., ["python", "testing", "api"]
    max_concurrent_tasks: int = 3
    current_load: float = 0.0
    success_rate: float = 1.0


@dataclass
class TaskAnalysis:
    """Analysis of a task to route it."""
    task_id: str
    task_type: str
    complexity: str  # "simple", "moderate", "complex"
    estimated_duration: float  # seconds
    required_capabilities: List[str] = field(default_factory=list)
    priority: str = "P2"


class TaskOrchestrator:
    """
    Orchestrates task distribution across multiple bots.

    Features:
    - Bot type registry and capability tracking
    - Task analysis and routing
    - Load balancing
    - Batch task execution
    - Status aggregation
    """

    def __init__(self, work_dir: Path):
        """
        Initialize task orchestrator.

        Args:
            work_dir: Working directory for logs
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.orchestration_log = self.log_dir / "orchestration.jsonl"

        # Bot registry
        self.bots: Dict[str, BotCapability] = {}

        # Task queue
        self.task_queue: List[Dict] = []
        self.task_history: Dict[str, Dict] = {}

        # Routing rules
        self.type_keywords = {
            BotType.DEVELOPER: ["code", "python", "api", "test", "debug", "compile", "build"],
            BotType.ANALYZER: ["analyze", "research", "investigate", "compare", "review"],
            BotType.WRITER: ["write", "document", "draft", "compose", "content"],
            BotType.PLANNER: ["plan", "schedule", "coordinate", "organize", "orchestrate"],
            BotType.VALIDATOR: ["test", "validate", "check", "verify", "assert"]
        }

    def register_bot(
        self,
        bot_id: str,
        bot_type: BotType,
        specializations: List[str] = None,
        max_concurrent: int = 3
    ) -> None:
        """
        Register a bot in the orchestrator.

        Args:
            bot_id: Bot identifier
            bot_type: Type of bot (developer, analyzer, writer, etc.)
            specializations: List of specializations (e.g., ["python", "testing"])
            max_concurrent: Maximum concurrent tasks for this bot
        """
        self.bots[bot_id] = BotCapability(
            bot_id=bot_id,
            bot_type=bot_type,
            specializations=specializations or [],
            max_concurrent_tasks=max_concurrent
        )

        self._log_event("bot_registered", bot_id, {
            "type": bot_type.value,
            "specializations": specializations
        })

    def unregister_bot(self, bot_id: str) -> None:
        """Unregister a bot."""
        if bot_id in self.bots:
            del self.bots[bot_id]
            self._log_event("bot_unregistered", bot_id)

    def analyze_task(self, task_id: str, task_content: str) -> TaskAnalysis:
        """
        Analyze a task to determine routing.

        Args:
            task_id: Task identifier
            task_content: Task description/content

        Returns:
            TaskAnalysis with routing information
        """
        # Determine task type from content
        task_type = self._determine_task_type(task_content)

        # Determine complexity
        complexity = self._determine_complexity(task_content)

        # Estimate duration
        estimated_duration = self._estimate_duration(task_content, complexity)

        # Extract required capabilities
        required_capabilities = self._extract_capabilities(task_content)

        return TaskAnalysis(
            task_id=task_id,
            task_type=task_type,
            complexity=complexity,
            estimated_duration=estimated_duration,
            required_capabilities=required_capabilities
        )

    def route_task(self, analysis: TaskAnalysis) -> Optional[str]:
        """
        Route a task to the best bot.

        Considers: bot type match, capacity, success rate, load.

        Args:
            analysis: TaskAnalysis from analyze_task

        Returns:
            Bot ID to route to, or None if no suitable bot
        """
        # Find bots that can handle this task
        candidates = self._find_candidate_bots(analysis)

        if not candidates:
            self._log_event("no_suitable_bot", analysis.task_id, {
                "task_type": analysis.task_type,
                "required_capabilities": analysis.required_capabilities
            })
            return None

        # Select best bot based on load and success rate
        selected_bot = self._select_best_bot(candidates, analysis)

        if selected_bot:
            self._log_event("task_routed", analysis.task_id, {
                "bot_id": selected_bot,
                "task_type": analysis.task_type,
                "complexity": analysis.complexity
            })

        return selected_bot

    def queue_task(self, task_id: str, bot_id: str, task_content: str) -> bool:
        """
        Queue a task for a specific bot.

        Args:
            task_id: Task identifier
            bot_id: Target bot
            task_content: Task content

        Returns:
            True if queued successfully
        """
        if bot_id not in self.bots:
            return False

        bot = self.bots[bot_id]

        # Check if bot has capacity
        if bot.current_load >= bot.max_concurrent_tasks:
            return False

        self.task_queue.append({
            "task_id": task_id,
            "bot_id": bot_id,
            "content": task_content,
            "queued_at": datetime.now().isoformat()
        })

        # Update bot load
        bot.current_load += 1

        return True

    def execute_queued_tasks(self) -> Dict[str, any]:
        """
        Execute all queued tasks (simulated - actual execution via bot services).

        Returns:
            Execution summary
        """
        executed = []
        failed = []

        for task in self.task_queue[:]:
            bot_id = task["bot_id"]

            try:
                # In real implementation, would call bot service API
                # For now, log the execution
                self._log_event("task_executed", task["task_id"], {
                    "bot_id": bot_id
                })

                executed.append(task["task_id"])
                self.task_history[task["task_id"]] = {
                    **task,
                    "executed_at": datetime.now().isoformat(),
                    "status": "success"
                }

                # Update bot load
                if bot_id in self.bots:
                    self.bots[bot_id].current_load = max(0, self.bots[bot_id].current_load - 1)

                self.task_queue.remove(task)
            except Exception as e:
                failed.append((task["task_id"], str(e)))

        return {
            "executed": executed,
            "failed": failed,
            "queued_remaining": len(self.task_queue)
        }

    def get_orchestration_status(self) -> Dict:
        """
        Get status of entire orchestration system.

        Returns:
            Comprehensive status dict
        """
        status = {
            "timestamp": datetime.now().isoformat(),
            "total_bots": len(self.bots),
            "queued_tasks": len(self.task_queue),
            "bots": {}
        }

        total_load = 0
        for bot_id, bot in self.bots.items():
            status["bots"][bot_id] = {
                "type": bot.bot_type.value,
                "specializations": bot.specializations,
                "current_load": bot.current_load,
                "max_concurrent": bot.max_concurrent_tasks,
                "capacity_remaining": bot.max_concurrent_tasks - bot.current_load,
                "success_rate": bot.success_rate
            }
            total_load += bot.current_load

        status["total_load"] = total_load
        status["avg_load_per_bot"] = total_load / len(self.bots) if self.bots else 0

        return status

    def get_bot_status(self, bot_id: str) -> Optional[Dict]:
        """Get status of a specific bot."""
        if bot_id not in self.bots:
            return None

        bot = self.bots[bot_id]
        return {
            "bot_id": bot_id,
            "type": bot.bot_type.value,
            "specializations": bot.specializations,
            "current_load": bot.current_load,
            "capacity": bot.max_concurrent_tasks,
            "available_capacity": bot.max_concurrent_tasks - bot.current_load,
            "success_rate": bot.success_rate
        }

    def update_bot_performance(self, bot_id: str, success: bool, duration: float = None) -> None:
        """
        Update bot performance metrics after task completion.

        Args:
            bot_id: Bot identifier
            success: Whether task succeeded
            duration: How long task took (optional)
        """
        if bot_id not in self.bots:
            return

        bot = self.bots[bot_id]

        # Update success rate (simple exponential moving average)
        if success:
            bot.success_rate = bot.success_rate * 0.95 + 1.0 * 0.05
        else:
            bot.success_rate = bot.success_rate * 0.95 + 0.0 * 0.05

        # Cap at 0.0-1.0
        bot.success_rate = max(0.0, min(1.0, bot.success_rate))

    def _determine_task_type(self, content: str) -> str:
        """Determine task type from content."""
        content_lower = content.lower()

        if any(kw in content_lower for kw in ["code", "python", "api", "test"]):
            return "development"
        elif any(kw in content_lower for kw in ["analyze", "research", "compare"]):
            return "analysis"
        elif any(kw in content_lower for kw in ["write", "document", "draft"]):
            return "writing"
        elif any(kw in content_lower for kw in ["plan", "schedule", "organize"]):
            return "planning"
        else:
            return "general"

    def _determine_complexity(self, content: str) -> str:
        """Estimate task complexity."""
        length = len(content.split())

        if length < 100:
            return "simple"
        elif length < 500:
            return "moderate"
        else:
            return "complex"

    def _estimate_duration(self, content: str, complexity: str) -> float:
        """Estimate task duration in seconds."""
        base_time = {
            "simple": 60,
            "moderate": 300,
            "complex": 900
        }
        return float(base_time.get(complexity, 300))

    def _extract_capabilities(self, content: str) -> List[str]:
        """Extract required capabilities from task content."""
        capabilities = []
        content_lower = content.lower()

        # Python/dev keywords
        if any(kw in content_lower for kw in ["python", "code", "api"]):
            capabilities.append("python")

        if any(kw in content_lower for kw in ["test", "testing", "validate"]):
            capabilities.append("testing")

        if any(kw in content_lower for kw in ["database", "sql", "data"]):
            capabilities.append("data")

        if any(kw in content_lower for kw in ["research", "analyze", "compare"]):
            capabilities.append("analysis")

        return capabilities or ["general"]

    def _find_candidate_bots(self, analysis: TaskAnalysis) -> List[str]:
        """Find bots capable of handling this task."""
        candidates = []

        for bot_id, bot in self.bots.items():
            # Must have available capacity
            if bot.current_load >= bot.max_concurrent_tasks:
                continue

            # Check type match
            if bot.bot_type == BotType.GENERAL:
                candidates.append(bot_id)
                continue

            # Check specialization match
            has_capability = any(
                cap in bot.specializations
                for cap in analysis.required_capabilities
            )

            if has_capability:
                candidates.append(bot_id)

        return candidates

    def _select_best_bot(self, candidates: List[str], analysis: TaskAnalysis) -> Optional[str]:
        """Select best bot from candidates."""
        if not candidates:
            return None

        # Score bots: prefer lower load and higher success rate
        scores = {}
        for bot_id in candidates:
            bot = self.bots[bot_id]

            # Load score (lower is better)
            load_score = bot.current_load / bot.max_concurrent_tasks

            # Success rate score (higher is better)
            success_score = bot.success_rate

            # Combined score (weighted)
            combined_score = (1 - load_score) * 0.6 + success_score * 0.4

            scores[bot_id] = combined_score

        # Return bot with highest score
        return max(scores, key=scores.get)

    def _log_event(self, event: str, task_id: str, details: Dict = None) -> None:
        """Log orchestration event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "task_id": task_id,
            "details": details or {}
        }

        try:
            with open(self.orchestration_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[ORCHESTRATOR] Failed to log event: {e}")
