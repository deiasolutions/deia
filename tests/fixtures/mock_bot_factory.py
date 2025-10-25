"""
Mock Bot Factory for Testing

Creates controllable mock bot instances for isolated testing.
Supports simulating various bot behaviors and failure modes.
"""

from typing import Optional, Callable, Dict, Any
from datetime import datetime, timedelta
import asyncio
from enum import Enum
from src.deia.models.schemas import BotSchema, BotStatus, BotCapabilitySchema


class MockBotBehavior(Enum):
    """Predefined bot behaviors"""
    PERFECT = "perfect"  # Always succeeds, fast
    NORMAL = "normal"  # Typical success/failure rates
    SLOW = "slow"  # Takes longer but reliable
    UNRELIABLE = "unreliable"  # Random failures
    OFFLINE = "offline"  # Always fails
    RESOURCE_CONSTRAINED = "resource_constrained"  # Limited capacity


class MockBot:
    """
    Mock bot instance for testing.

    Allows simulating:
    - Task execution with controllable latency
    - Success/failure rates
    - Resource constraints
    - Health status changes
    """

    def __init__(
        self,
        bot_id: str,
        behavior: MockBotBehavior = MockBotBehavior.NORMAL,
        port: int = 8001,
    ):
        """Initialize mock bot"""
        self.bot_id = bot_id
        self.behavior = behavior
        self.port = port
        self.schema = BotSchema(
            bot_id=bot_id,
            port=port,
            status=self._status_for_behavior(behavior),
            launched_at=datetime.now(),
            capabilities=BotCapabilitySchema(
                bot_type=self._type_for_behavior(behavior),
            ),
        )

        # Task tracking
        self.tasks_executed = 0
        self.tasks_succeeded = 0
        self.tasks_failed = 0

        # Execution control
        self._latency_override = None
        self._success_override = None

    async def execute_task(self, task_content: str) -> Dict[str, Any]:
        """
        Simulate task execution with behavior-specific characteristics.

        Returns:
            {
                "success": bool,
                "duration_seconds": float,
                "output": str or None,
                "error": str or None,
            }
        """
        self.tasks_executed += 1

        # Determine latency
        latency = self._latency_override or self._latency_for_behavior()

        # Simulate execution time
        await asyncio.sleep(min(latency, 0.1))  # Cap at 100ms for testing

        # Determine success
        success = self._success_override if self._success_override is not None else self._should_succeed()

        if success:
            self.tasks_succeeded += 1
            return {
                "success": True,
                "duration_seconds": latency,
                "output": f"Task completed successfully (executed by {self.bot_id})",
                "error": None,
            }
        else:
            self.tasks_failed += 1
            return {
                "success": False,
                "duration_seconds": latency,
                "output": None,
                "error": self._error_for_behavior(),
            }

    def set_latency(self, seconds: float):
        """Override latency for testing"""
        self._latency_override = seconds

    def set_success_rate(self, rate: float):
        """Override success with fixed rate (0-1)"""
        import random
        self._success_override = random.random() < rate

    def set_always_succeed(self):
        """Make bot always succeed"""
        self._success_override = True

    def set_always_fail(self):
        """Make bot always fail"""
        self._success_override = False

    def get_schema(self) -> BotSchema:
        """Get current bot schema"""
        self.schema.tasks_completed = self.tasks_succeeded
        self.schema.tasks_failed = self.tasks_failed
        self.schema.current_load = self.tasks_executed / 100.0  # Rough estimate
        self.schema.last_heartbeat = datetime.now()
        return self.schema

    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        return {
            "bot_id": self.bot_id,
            "behavior": self.behavior.value,
            "tasks_executed": self.tasks_executed,
            "tasks_succeeded": self.tasks_succeeded,
            "tasks_failed": self.tasks_failed,
            "success_rate": (
                self.tasks_succeeded / self.tasks_executed
                if self.tasks_executed > 0
                else 0
            ),
        }

    def reset(self):
        """Reset execution counters"""
        self.tasks_executed = 0
        self.tasks_succeeded = 0
        self.tasks_failed = 0
        self._latency_override = None
        self._success_override = None

    # Private helpers

    def _status_for_behavior(self, behavior: MockBotBehavior) -> BotStatus:
        """Get status for behavior"""
        if behavior == MockBotBehavior.OFFLINE:
            return BotStatus.OFFLINE
        elif behavior == MockBotBehavior.RESOURCE_CONSTRAINED:
            return BotStatus.DEGRADED
        else:
            return BotStatus.HEALTHY

    def _type_for_behavior(self, behavior: MockBotBehavior) -> str:
        """Get bot type for behavior"""
        types = {
            MockBotBehavior.PERFECT: "developer",
            MockBotBehavior.NORMAL: "analyzer",
            MockBotBehavior.SLOW: "writer",
            MockBotBehavior.UNRELIABLE: "general",
            MockBotBehavior.OFFLINE: "general",
            MockBotBehavior.RESOURCE_CONSTRAINED: "planner",
        }
        return types.get(behavior, "general")

    def _latency_for_behavior(self) -> float:
        """Get execution latency for behavior"""
        import random

        if self.behavior == MockBotBehavior.PERFECT:
            return random.uniform(0.01, 0.05)  # 10-50ms
        elif self.behavior == MockBotBehavior.NORMAL:
            return random.uniform(0.05, 0.15)  # 50-150ms
        elif self.behavior == MockBotBehavior.SLOW:
            return random.uniform(0.1, 0.3)  # 100-300ms
        elif self.behavior == MockBotBehavior.UNRELIABLE:
            return random.uniform(0.02, 0.5)  # Highly variable
        elif self.behavior == MockBotBehavior.OFFLINE:
            return 0  # No execution
        elif self.behavior == MockBotBehavior.RESOURCE_CONSTRAINED:
            return random.uniform(0.2, 0.4)  # Slow due to resources
        else:
            return 0.1

    def _should_succeed(self) -> bool:
        """Determine if task should succeed"""
        import random

        if self.behavior == MockBotBehavior.PERFECT:
            return True
        elif self.behavior == MockBotBehavior.NORMAL:
            return random.random() < 0.95  # 95% success
        elif self.behavior == MockBotBehavior.SLOW:
            return random.random() < 0.98  # 98% success
        elif self.behavior == MockBotBehavior.UNRELIABLE:
            return random.random() < 0.70  # 70% success
        elif self.behavior == MockBotBehavior.OFFLINE:
            return False  # Always fails
        elif self.behavior == MockBotBehavior.RESOURCE_CONSTRAINED:
            return random.random() < 0.80  # 80% success
        else:
            return True

    def _error_for_behavior(self) -> str:
        """Get error message for behavior"""
        import random

        errors = {
            MockBotBehavior.NORMAL: [
                "Timeout waiting for database",
                "Rate limit exceeded",
                "Invalid input parameters",
            ],
            MockBotBehavior.UNRELIABLE: [
                "Random execution error",
                "Network timeout",
                "Memory error",
                "Unexpected exception",
            ],
            MockBotBehavior.OFFLINE: [
                "Bot is offline",
                "Connection refused",
                "Service unavailable",
            ],
            MockBotBehavior.RESOURCE_CONSTRAINED: [
                "Out of memory",
                "CPU limit exceeded",
                "Disk space exhausted",
            ],
        }

        error_list = errors.get(self.behavior, ["Generic error"])
        return random.choice(error_list)


class MockBotFactory:
    """Factory for creating mock bots"""

    def __init__(self):
        """Initialize factory"""
        self.bots: Dict[str, MockBot] = {}
        self._next_port = 8001

    def create_bot(
        self,
        bot_id: str = None,
        behavior: MockBotBehavior = MockBotBehavior.NORMAL,
    ) -> MockBot:
        """Create a single mock bot"""
        if bot_id is None:
            bot_id = f"mock-bot-{len(self.bots) + 1}"

        bot = MockBot(bot_id, behavior, port=self._next_port)
        self._next_port += 1
        self.bots[bot_id] = bot
        return bot

    def create_bot_pool(
        self,
        count: int = 3,
        behavior: MockBotBehavior = MockBotBehavior.NORMAL,
    ) -> Dict[str, MockBot]:
        """Create a pool of bots with same behavior"""
        return {
            bot.bot_id: bot
            for bot in [
                self.create_bot(f"bot-{i:03d}", behavior)
                for i in range(count)
            ]
        }

    def create_diverse_pool(self, count_per_behavior: int = 2) -> Dict[str, MockBot]:
        """Create diverse pool with different behaviors"""
        pool = {}
        behaviors = [b for b in MockBotBehavior if b != MockBotBehavior.OFFLINE]

        for behavior in behaviors:
            for i in range(count_per_behavior):
                bot = self.create_bot(
                    f"bot-{behavior.value}-{i:02d}",
                    behavior
                )
                pool[bot.bot_id] = bot

        return pool

    def get_bot(self, bot_id: str) -> Optional[MockBot]:
        """Get bot by ID"""
        return self.bots.get(bot_id)

    def get_all_bots(self) -> Dict[str, MockBot]:
        """Get all created bots"""
        return self.bots.copy()

    def reset_all(self):
        """Reset all bots"""
        for bot in self.bots.values():
            bot.reset()

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for all bots"""
        return {
            "total_bots": len(self.bots),
            "bots": {
                bot_id: bot.get_stats()
                for bot_id, bot in self.bots.items()
            },
        }
