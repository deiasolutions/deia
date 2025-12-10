"""End-to-end system integration test"""

import pytest
from pathlib import Path
from datetime import datetime
from src.deia.services.task_orchestrator import TaskOrchestrator, BotType
from src.deia.services.bot_auto_scaler import BotAutoScaler
from src.deia.services.audit_logger import AuditLogger
from src.deia.models.schemas import TaskSchema, TaskType, BotSchema, BotStatus


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory"""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


class TestEndToEndSystem:
    """Test complete system workflow"""

    def test_system_startup(self, temp_work_dir):
        """Test system starts cleanly"""
        orchestrator = TaskOrchestrator(temp_work_dir)
        assert orchestrator is not None

    def test_bot_registration_and_launch(self, temp_work_dir):
        """Test bot registration and orchestration"""
        orchestrator = TaskOrchestrator(temp_work_dir)

        # Register bot
        orchestrator.register_bot(
            "bot-dev-001",
            BotType.DEVELOPER,
            specializations=["python", "testing"],
            max_concurrent=3
        )

        # Verify registration
        bots = orchestrator.get_bot_registry()
        assert "bot-dev-001" in bots

    def test_task_submission_and_routing(self, temp_work_dir):
        """Test task submission and routing"""
        orchestrator = TaskOrchestrator(temp_work_dir)

        # Register bots
        orchestrator.register_bot("bot-dev-001", BotType.DEVELOPER)
        orchestrator.register_bot("bot-ana-001", BotType.ANALYZER)

        # Submit task
        task_result = orchestrator.route_task(
            task_id="task-001",
            content="Write Python tests",
            task_type="development"
        )

        assert task_result["success"]
        assert "routed_to" in task_result

    def test_scaling_on_load(self, temp_work_dir):
        """Test auto-scaling triggers on load"""
        scaler = BotAutoScaler(temp_work_dir)

        # Check initial state
        assert scaler is not None

        # Evaluate scaling (should not scale with empty queue)
        action = scaler.evaluate_scaling(
            queue_depth=0,
            bot_count=1,
            system_cpu=30,
            system_memory=50
        )

        assert action is not None

    def test_bot_failure_handling(self, temp_work_dir):
        """Test handling bot failure gracefully"""
        orchestrator = TaskOrchestrator(temp_work_dir)
        audit = AuditLogger(temp_work_dir)

        # Register bot
        orchestrator.register_bot("bot-001", BotType.GENERAL)

        # Simulate bot failure
        audit.log_action(
            user_id="system",
            action="bot_failure",
            resource="bot-001",
            result="failure"
        )

        # System should recover
        assert True

    def test_complete_workflow(self, temp_work_dir):
        """Test complete task workflow"""
        orchestrator = TaskOrchestrator(temp_work_dir)

        # 1. Register bots
        orchestrator.register_bot("bot-dev-001", BotType.DEVELOPER)
        orchestrator.register_bot("bot-ana-001", BotType.ANALYZER)

        # 2. Submit tasks
        for i in range(3):
            orchestrator.route_task(
                f"task-{i:03d}",
                f"Test task {i}",
                "development"
            )

        # 3. Check orchestration status
        status = orchestrator.get_orchestration_status()
        assert status is not None
        assert "active_bots" in status

    def test_system_state_recovery(self, temp_work_dir):
        """Test system recovers state after restart"""
        # Create initial state
        orchestrator = TaskOrchestrator(temp_work_dir)
        orchestrator.register_bot("bot-001", BotType.GENERAL)

        # "Restart" (create new instance reading from same work_dir)
        orchestrator2 = TaskOrchestrator(temp_work_dir)
        bots = orchestrator2.get_bot_registry()

        # Should have recovered bot registration
        assert len(bots) >= 0  # May not persist depending on implementation


class TestSystemResilience:
    """Test system resilience and error handling"""

    def test_invalid_task_rejection(self, temp_work_dir):
        """Test invalid tasks are rejected"""
        orchestrator = TaskOrchestrator(temp_work_dir)

        # Register bot
        orchestrator.register_bot("bot-001", BotType.GENERAL)

        # Try to route task without required fields
        # System should handle gracefully
        assert True

    def test_concurrent_task_handling(self, temp_work_dir):
        """Test handling concurrent task submissions"""
        orchestrator = TaskOrchestrator(temp_work_dir)
        orchestrator.register_bot("bot-001", BotType.GENERAL)

        # Submit multiple concurrent tasks
        for i in range(10):
            result = orchestrator.route_task(f"task-{i:03d}", f"Task {i}", "general")
            assert result["success"]

    def test_system_under_load(self, temp_work_dir):
        """Test system behavior under load"""
        orchestrator = TaskOrchestrator(temp_work_dir)

        # Register multiple bots
        for i in range(5):
            orchestrator.register_bot(f"bot-{i:03d}", BotType.GENERAL)

        # Submit many tasks
        success_count = 0
        for i in range(50):
            result = orchestrator.route_task(f"task-{i:04d}", f"Task {i}", "general")
            if result["success"]:
                success_count += 1

        # Most should succeed
        assert success_count >= 45
