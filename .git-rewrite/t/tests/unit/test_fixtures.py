"""Unit tests for test data generators and mock bots"""

import pytest
import asyncio
from tests.fixtures.test_data_generator import (
    TestDataGenerator, generate_baseline_10_tasks, generate_standard_100_tasks,
    generate_stress_1000_tasks, generate_mixed_infrastructure,
)
from tests.fixtures.mock_bot_factory import (
    MockBot, MockBotFactory, MockBotBehavior
)
from src.deia.models.schemas import TaskType, BotStatus


class TestDataGeneratorBasics:
    """Test basic test data generation"""

    def test_generator_creation(self):
        """Test creating generator"""
        gen = TestDataGenerator()
        assert gen is not None

    def test_generate_single_task(self):
        """Test generating a single task"""
        gen = TestDataGenerator()
        task = gen.generate_task()

        assert task.task_id is not None
        assert task.submitter_id is not None
        assert task.content is not None

    def test_generate_multiple_tasks(self):
        """Test generating multiple tasks"""
        gen = TestDataGenerator()
        tasks = gen.generate_tasks(10)

        assert len(tasks) == 10
        assert all(t.task_id is not None for t in tasks)

    def test_generate_single_bot(self):
        """Test generating a single bot"""
        gen = TestDataGenerator()
        bot = gen.generate_bot()

        assert bot.bot_id is not None
        assert bot.port > 8000
        assert bot.capabilities is not None

    def test_generate_multiple_bots(self):
        """Test generating multiple bots"""
        gen = TestDataGenerator()
        bots = gen.generate_bots(5)

        assert len(bots) == 5
        assert all(b.bot_id is not None for b in bots)


class TestLoadPatterns:
    """Test load pattern generation"""

    def test_baseline_10_pattern(self):
        """Test 10-task baseline"""
        gen = TestDataGenerator()
        tasks = gen.generate_load_pattern(10)

        assert len(tasks) == 10
        # Should have mixed task types
        types = set(t.task_type for t in tasks)
        assert len(types) > 1

    def test_standard_100_pattern(self):
        """Test 100-task standard load"""
        tasks = generate_standard_100_tasks()
        assert len(tasks) == 100

    def test_stress_1000_pattern(self):
        """Test 1000-task stress load"""
        tasks = generate_stress_1000_tasks()
        assert len(tasks) == 1000

    def test_load_pattern_prioritization(self):
        """Test that load pattern includes priority mix"""
        gen = TestDataGenerator()
        tasks = gen.generate_load_pattern(100)

        # Some tasks should be P0/P1
        high_priority = [t for t in tasks if t.priority.value in ["P0", "P1"]]
        assert len(high_priority) > 0


class TestFailureScenarios:
    """Test failure scenario generation"""

    def test_timeout_scenario(self):
        """Test timeout failure scenario"""
        gen = TestDataGenerator()
        scenario = gen.generate_failure_scenario("timeout", 5)

        assert scenario["type"] == "timeout"
        assert len(scenario["tasks"]) == 5
        assert all(t.error == "Execution timeout exceeded" for t in scenario["tasks"])

    def test_network_error_scenario(self):
        """Test network error scenario"""
        gen = TestDataGenerator()
        scenario = gen.generate_failure_scenario("network_error", 5)

        assert scenario["type"] == "network_error"
        assert scenario["bot"].status == BotStatus.OFFLINE
        assert all(t.status.value == "failed" for t in scenario["tasks"])

    def test_resource_exhaustion_scenario(self):
        """Test resource exhaustion scenario"""
        gen = TestDataGenerator()
        scenario = gen.generate_failure_scenario("resource_exhaustion", 5)

        assert scenario["type"] == "resource_exhaustion"
        assert scenario["bot"].cpu_usage_percent == 99.0
        assert all(t.status.value == "failed" for t in scenario["tasks"])

    def test_cascading_failure_scenario(self):
        """Test cascading failure scenario"""
        gen = TestDataGenerator()
        scenario = gen.generate_failure_scenario("cascading", 5)

        assert scenario["type"] == "cascading"
        assert len(scenario["bots"]) > 0
        assert any(b.status == BotStatus.OFFLINE for b in scenario["bots"])


class TestMixedInfrastructure:
    """Test complete infrastructure generation"""

    def test_generate_mixed_infrastructure(self):
        """Test generating complete test infrastructure"""
        infra = generate_mixed_infrastructure(bot_count=3, task_count=10)

        assert len(infra["bots"]) == 3
        assert len(infra["tasks"]) == 10
        assert infra["generator"] is not None


class TestMockBotBasics:
    """Test mock bot creation and control"""

    @pytest.mark.asyncio
    async def test_create_perfect_bot(self):
        """Test creating perfect bot"""
        bot = MockBot("perfect-bot", MockBotBehavior.PERFECT)

        assert bot.bot_id == "perfect-bot"
        assert bot.schema.status == BotStatus.HEALTHY

    @pytest.mark.asyncio
    async def test_bot_execution_perfect(self):
        """Test perfect bot always succeeds"""
        bot = MockBot("perfect", MockBotBehavior.PERFECT)

        for _ in range(10):
            result = await bot.execute_task("test task")
            assert result["success"]

    @pytest.mark.asyncio
    async def test_bot_execution_normal(self):
        """Test normal bot has realistic success rate"""
        bot = MockBot("normal", MockBotBehavior.NORMAL)

        results = []
        for _ in range(50):
            result = await bot.execute_task("test task")
            results.append(result["success"])

        success_rate = sum(results) / len(results)
        assert 0.85 < success_rate < 1.0  # Should be ~95%

    @pytest.mark.asyncio
    async def test_bot_execution_unreliable(self):
        """Test unreliable bot has low success rate"""
        bot = MockBot("unreliable", MockBotBehavior.UNRELIABLE)

        results = []
        for _ in range(50):
            result = await bot.execute_task("test task")
            results.append(result["success"])

        success_rate = sum(results) / len(results)
        assert 0.40 < success_rate < 0.90  # Should be ~70%

    @pytest.mark.asyncio
    async def test_bot_execution_offline(self):
        """Test offline bot always fails"""
        bot = MockBot("offline", MockBotBehavior.OFFLINE)

        for _ in range(10):
            result = await bot.execute_task("test task")
            assert not result["success"]

    @pytest.mark.asyncio
    async def test_bot_latency_override(self):
        """Test overriding bot latency"""
        bot = MockBot("latency-test", MockBotBehavior.NORMAL)
        bot.set_latency(0.5)

        result = await bot.execute_task("test")
        assert result["duration_seconds"] == 0.5

    @pytest.mark.asyncio
    async def test_bot_success_override(self):
        """Test overriding bot success"""
        bot = MockBot("success-test", MockBotBehavior.UNRELIABLE)
        bot.set_always_succeed()

        for _ in range(10):
            result = await bot.execute_task("test")
            assert result["success"]

    def test_bot_stats(self):
        """Test bot statistics tracking"""
        bot = MockBot("stats-bot", MockBotBehavior.NORMAL)

        # Manually increment stats (since async execution is complex)
        bot.tasks_executed = 10
        bot.tasks_succeeded = 9
        bot.tasks_failed = 1

        stats = bot.get_stats()
        assert stats["tasks_executed"] == 10
        assert stats["tasks_succeeded"] == 9
        assert stats["tasks_failed"] == 1
        assert stats["success_rate"] == 0.9

    def test_bot_reset(self):
        """Test resetting bot"""
        bot = MockBot("reset-bot", MockBotBehavior.NORMAL)
        bot.tasks_executed = 10
        bot.tasks_succeeded = 9

        bot.reset()

        assert bot.tasks_executed == 0
        assert bot.tasks_succeeded == 0


class TestMockBotFactory:
    """Test mock bot factory"""

    def test_factory_creation(self):
        """Test creating factory"""
        factory = MockBotFactory()
        assert factory is not None

    def test_factory_create_single_bot(self):
        """Test factory creates single bot"""
        factory = MockBotFactory()
        bot = factory.create_bot()

        assert bot is not None
        assert bot.bot_id in factory.get_all_bots()

    def test_factory_create_pool(self):
        """Test factory creates pool of bots"""
        factory = MockBotFactory()
        pool = factory.create_bot_pool(count=5, behavior=MockBotBehavior.NORMAL)

        assert len(pool) == 5
        assert all(b.behavior == MockBotBehavior.NORMAL for b in pool.values())

    def test_factory_create_diverse_pool(self):
        """Test factory creates diverse pool"""
        factory = MockBotFactory()
        pool = factory.create_diverse_pool(count_per_behavior=2)

        # Should have multiple behaviors
        behaviors = set(b.behavior for b in pool.values())
        assert len(behaviors) > 1

    def test_factory_get_bot(self):
        """Test getting bot from factory"""
        factory = MockBotFactory()
        bot = factory.create_bot("test-bot")

        retrieved = factory.get_bot("test-bot")
        assert retrieved == bot

    def test_factory_stats(self):
        """Test factory statistics"""
        factory = MockBotFactory()
        factory.create_bot_pool(3)

        stats = factory.get_stats()
        assert stats["total_bots"] == 3
        assert len(stats["bots"]) == 3

    def test_factory_reset_all(self):
        """Test resetting all bots"""
        factory = MockBotFactory()
        bot1 = factory.create_bot("bot1")
        bot2 = factory.create_bot("bot2")

        bot1.tasks_executed = 10
        bot2.tasks_executed = 20

        factory.reset_all()

        assert bot1.tasks_executed == 0
        assert bot2.tasks_executed == 0


class TestFixtureConvenience:
    """Test convenience functions"""

    def test_baseline_10_convenience(self):
        """Test 10-task convenience function"""
        tasks = generate_baseline_10_tasks()
        assert len(tasks) == 10

    def test_standard_100_convenience(self):
        """Test 100-task convenience function"""
        tasks = generate_standard_100_tasks()
        assert len(tasks) == 100

    def test_stress_1000_convenience(self):
        """Test 1000-task convenience function"""
        tasks = generate_stress_1000_tasks()
        assert len(tasks) == 1000
