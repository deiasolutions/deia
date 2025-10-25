"""
Synthetic Test Data Generator for DEIA

Generates realistic test data for integration tests:
- Synthetic tasks (various types, complexities)
- Synthetic bots (different specializations)
- Load patterns (10/100/1000 task batches)
- Failure scenarios (timeouts, errors, network failures)
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import random
import string
from src.deia.models.schemas import (
    TaskSchema, BotSchema, BotCapabilitySchema,
    TaskType, TaskStatus, TaskPriority, BotStatus
)


class TestDataGenerator:
    """Generate realistic synthetic test data"""

    # Task types and characteristics
    TASK_CHARACTERISTICS = {
        TaskType.DEVELOPMENT: {
            "min_duration": 30,
            "max_duration": 300,
            "success_rate": 0.95,
            "specializations": ["python", "testing", "code"],
        },
        TaskType.ANALYSIS: {
            "min_duration": 45,
            "max_duration": 600,
            "success_rate": 0.92,
            "specializations": ["data", "research", "analysis"],
        },
        TaskType.WRITING: {
            "min_duration": 60,
            "max_duration": 1200,
            "success_rate": 0.90,
            "specializations": ["writing", "documentation", "content"],
        },
        TaskType.PLANNING: {
            "min_duration": 20,
            "max_duration": 180,
            "success_rate": 0.98,
            "specializations": ["planning", "coordination"],
        },
        TaskType.GENERAL: {
            "min_duration": 15,
            "max_duration": 300,
            "success_rate": 0.85,
            "specializations": ["general"],
        },
    }

    def __init__(self, seed: int = 42):
        """Initialize with optional random seed for reproducibility"""
        random.seed(seed)

    def generate_task(
        self,
        task_id: str = None,
        task_type: TaskType = None,
        priority: TaskPriority = None,
        status: TaskStatus = TaskStatus.PENDING,
    ) -> TaskSchema:
        """Generate a single task"""
        if task_type is None:
            task_type = random.choice(list(TaskType))

        now = datetime.now()
        base_content = self._task_content_for_type(task_type)

        return TaskSchema(
            task_id=task_id or f"task-{self._random_id()}",
            task_type=task_type,
            priority=priority or random.choice(list(TaskPriority)),
            status=status,
            submitter_id=f"user-{self._random_id()}",
            submitted_at=now,
            content=base_content,
            assigned_to=None,
            tags=[task_type.value],
            metadata={
                "generated": True,
                "synthetic": True,
            }
        )

    def generate_tasks(self, count: int = 10) -> List[TaskSchema]:
        """Generate multiple tasks"""
        return [self.generate_task() for _ in range(count)]

    def generate_bot(
        self,
        bot_id: str = None,
        status: BotStatus = BotStatus.HEALTHY,
        specializations: List[str] = None,
    ) -> BotSchema:
        """Generate a single bot"""
        if specializations is None:
            task_type = random.choice(list(TaskType))
            specializations = self.TASK_CHARACTERISTICS[task_type]["specializations"]

        now = datetime.now()

        return BotSchema(
            bot_id=bot_id or f"bot-{self._random_id()}",
            status=status,
            port=8000 + random.randint(1, 999),
            process_id=random.randint(10000, 99999),
            launched_at=now - timedelta(hours=random.randint(1, 24)),
            capabilities=BotCapabilitySchema(
                bot_type=random.choice(["developer", "analyzer", "writer", "planner"]),
                specializations=specializations,
                max_concurrent_tasks=random.randint(1, 5),
                success_rate=random.uniform(0.85, 1.0),
            ),
            last_heartbeat=now - timedelta(seconds=random.randint(0, 30)),
            cpu_usage_percent=random.uniform(0, 80),
            memory_usage_mb=random.uniform(100, 512),
            current_load=random.uniform(0, 1),
            tasks_completed=random.randint(10, 1000),
            tasks_failed=random.randint(0, 50),
        )

    def generate_bots(self, count: int = 3) -> List[BotSchema]:
        """Generate multiple bots"""
        return [self.generate_bot() for _ in range(count)]

    def generate_load_pattern(self, task_count: int = 10) -> List[TaskSchema]:
        """
        Generate a load pattern with mixed task types.

        Patterns:
        - 10 tasks: Quick baseline test
        - 100 tasks: Standard load test
        - 1000 tasks: Stress test
        """
        tasks = []
        task_types = list(TaskType)

        for i in range(task_count):
            # Distribute evenly across task types
            task_type = task_types[i % len(task_types)]
            priority = TaskPriority.P2 if i % 10 != 0 else random.choice([TaskPriority.P0, TaskPriority.P1])

            task = self.generate_task(
                task_id=f"load-task-{i:04d}",
                task_type=task_type,
                priority=priority,
            )
            tasks.append(task)

        return tasks

    def generate_failure_scenario(
        self,
        failure_type: str = "timeout",
        task_count: int = 5,
    ) -> Dict[str, Any]:
        """
        Generate a failure scenario for testing error handling.

        Failure types:
        - timeout: Tasks exceed estimated duration
        - network_error: Bot becomes unreachable
        - resource_exhaustion: Bot runs out of memory/CPU
        - cascading: One failure causes others
        """
        if failure_type == "timeout":
            tasks = self.generate_tasks(task_count)
            for task in tasks:
                task.estimated_duration_seconds = 10  # Very short estimate
                task.actual_duration_seconds = 300  # But actually takes 5 min
                task.status = TaskStatus.FAILED
                task.error = "Execution timeout exceeded"
            return {"type": "timeout", "tasks": tasks, "count": task_count}

        elif failure_type == "network_error":
            bot = self.generate_bot(status=BotStatus.OFFLINE)
            tasks = self.generate_tasks(task_count)
            for task in tasks:
                task.assigned_to = bot.bot_id
                task.status = TaskStatus.FAILED
                task.error = f"Bot {bot.bot_id} is offline"
            return {"type": "network_error", "bot": bot, "tasks": tasks, "count": task_count}

        elif failure_type == "resource_exhaustion":
            bot = self.generate_bot(status=BotStatus.DEGRADED)
            bot.cpu_usage_percent = 99.0
            bot.memory_usage_mb = 1024.0
            bot.current_load = 0.99
            tasks = self.generate_tasks(task_count)
            for task in tasks:
                task.assigned_to = bot.bot_id
                task.status = TaskStatus.FAILED
                task.error = "Bot resource exhaustion (CPU/Memory)"
            return {"type": "resource_exhaustion", "bot": bot, "tasks": tasks, "count": task_count}

        elif failure_type == "cascading":
            # One failure triggers multiple downstream failures
            bots = self.generate_bots(3)
            bots[0].status = BotStatus.OFFLINE  # Primary bot fails

            tasks = self.generate_tasks(task_count)
            for i, task in enumerate(tasks):
                task.assigned_to = bots[i % len(bots)].bot_id
                if bots[i % len(bots)].status == BotStatus.OFFLINE:
                    task.status = TaskStatus.FAILED
                    task.error = "Cascading failure from upstream bot"

            return {"type": "cascading", "bots": bots, "tasks": tasks, "count": task_count}

        else:
            raise ValueError(f"Unknown failure type: {failure_type}")

    def _task_content_for_type(self, task_type: TaskType) -> str:
        """Generate realistic task content for given type"""
        templates = {
            TaskType.DEVELOPMENT: [
                "Write Python unit tests for authentication module",
                "Refactor database query for performance optimization",
                "Implement new API endpoint for user management",
            ],
            TaskType.ANALYSIS: [
                "Analyze system performance bottlenecks and provide recommendations",
                "Research and compare 3 competing solutions for task queue",
                "Deep dive into error logs and identify root causes",
            ],
            TaskType.WRITING: [
                "Write comprehensive API documentation for bot service",
                "Create deployment guide for production systems",
                "Write technical blog post on system architecture",
            ],
            TaskType.PLANNING: [
                "Plan next quarter development roadmap",
                "Coordinate sprint planning across teams",
                "Design migration strategy for legacy systems",
            ],
            TaskType.GENERAL: [
                "Review and provide feedback on architecture proposal",
                "Investigate customer issue report",
                "Organize team meeting and document outcomes",
            ],
        }

        return random.choice(templates.get(task_type, ["Complete task of type " + task_type.value]))

    def _random_id(self, length: int = 8) -> str:
        """Generate random ID"""
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


# Convenience functions for common patterns

def generate_baseline_10_tasks() -> List[TaskSchema]:
    """Generate 10-task baseline for quick testing"""
    gen = TestDataGenerator()
    return gen.generate_load_pattern(10)


def generate_standard_100_tasks() -> List[TaskSchema]:
    """Generate 100-task load for standard testing"""
    gen = TestDataGenerator()
    return gen.generate_load_pattern(100)


def generate_stress_1000_tasks() -> List[TaskSchema]:
    """Generate 1000-task load for stress testing"""
    gen = TestDataGenerator()
    return gen.generate_load_pattern(1000)


def generate_mixed_infrastructure(
    bot_count: int = 5,
    task_count: int = 50,
) -> Dict[str, Any]:
    """Generate complete test infrastructure with bots and tasks"""
    gen = TestDataGenerator()
    return {
        "bots": gen.generate_bots(bot_count),
        "tasks": gen.generate_load_pattern(task_count),
        "generator": gen,
    }
