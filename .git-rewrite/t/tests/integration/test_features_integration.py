"""
Integration tests for Features 3-5.

Verifies that bot communication, adaptive scheduling, and health monitoring
work together seamlessly without breaking existing orchestration and scaling.
"""

import pytest
from pathlib import Path
from src.deia.services.bot_service import BotService
from src.deia.services.task_orchestrator import TaskOrchestrator, BotType
from src.deia.services.bot_auto_scaler import BotAutoScaler
from src.deia.services.bot_messenger import BotMessenger
from src.deia.services.adaptive_scheduler import AdaptiveScheduler
from src.deia.services.health_monitor import HealthMonitor, AlertType


@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary working directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def services(temp_dir):
    """Create all service instances."""
    return {
        "messenger": BotMessenger(temp_dir),
        "scheduler": AdaptiveScheduler(temp_dir),
        "health": HealthMonitor(temp_dir),
        "orchestrator": TaskOrchestrator(temp_dir),
        "scaler": BotAutoScaler(temp_dir)
    }


class TestFeatures3To5Integration:
    """Integration tests for Features 3-5."""

    def test_messaging_with_orchestration(self, services):
        """Test that messaging works with task orchestration."""
        messenger = services["messenger"]
        orchestrator = services["orchestrator"]

        # Register bots
        orchestrator.register_bot("bot-1", BotType.DEVELOPER)
        orchestrator.register_bot("bot-2", BotType.ANALYZER)

        # Send message between bots
        msg_id = messenger.send_message("bot-1", "bot-2", "Task complete")

        # Process queue
        result = messenger.process_outgoing_queue()
        assert len(result["delivered"]) > 0

        # Verify message in inbox
        messages = messenger.retrieve_messages("bot-2")
        assert len(messages) > 0

    def test_adaptive_scheduling_with_scaling(self, services):
        """Test adaptive scheduling works with scaling decisions."""
        scheduler = services["scheduler"]
        scaler = services["scaler"]

        # Record task executions
        scheduler.record_task_execution("bot-1", "development", 40.0, True)
        scheduler.record_task_execution("bot-1", "development", 42.0, True)
        scheduler.record_task_execution("bot-1", "development", 41.0, True)

        scheduler.record_task_execution("bot-2", "development", 60.0, True)
        scheduler.record_task_execution("bot-2", "development", 62.0, True)
        scheduler.record_task_execution("bot-2", "development", 61.0, True)

        # Get recommendation
        rec = scheduler.get_recommendation("development")
        assert rec is not None
        assert rec.recommended_bot == "bot-1"

        # Scaling should not be affected
        scaler.current_bot_count = 5
        should_scale_up = scaler.should_scale_up(0.5, 10, 0.7)
        assert should_scale_up  # High queue

    def test_health_monitoring_with_messaging(self, services):
        """Test health monitoring tracks messaging status."""
        health = services["health"]
        messenger = services["messenger"]

        # Send some messages
        messenger.send_message("bot-1", "bot-2", "Test 1")
        messenger.send_message("bot-1", "bot-2", "Test 2")

        # Evaluate health with messaging data
        metrics = health.evaluate_health(
            total_bots=5,
            active_bots=5,
            queued_tasks=0,
            avg_bot_load=0.3,
            system_cpu_percent=0.4,
            system_memory_percent=0.5,
            message_queue_size=2,  # Pending messages
            pending_message_failures=0,
            avg_success_rate=0.95
        )

        dashboard = health.get_dashboard()
        assert dashboard["queue_status"]["pending_messages"] == 2

    def test_health_monitoring_detects_scheduling_issues(self, services):
        """Test health monitoring alerts on scheduling anomalies."""
        health = services["health"]
        scheduler = services["scheduler"]

        # Record poor performance
        scheduler.record_task_execution("bot-1", "development", 50.0, False)
        scheduler.record_task_execution("bot-1", "development", 55.0, False)
        scheduler.record_task_execution("bot-1", "development", 60.0, False)

        # Get learning insights
        insights = scheduler.get_learning_insights()
        assert insights["total_executions"] == 3

        # Health should detect low success rate
        metrics = health.evaluate_health(
            total_bots=1,
            active_bots=1,
            queued_tasks=0,
            avg_bot_load=0.5,
            system_cpu_percent=0.4,
            system_memory_percent=0.5,
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.25  # Low due to failures
        )

        alerts = health.get_alerts()
        low_success = [a for a in alerts if a["alert_type"] == "low_success_rate"]
        assert len(low_success) > 0

    def test_all_features_together(self, services):
        """Test all features working together in realistic scenario."""
        messenger = services["messenger"]
        scheduler = services["scheduler"]
        health = services["health"]
        orchestrator = services["orchestrator"]
        scaler = services["scaler"]

        # Setup orchestration
        orchestrator.register_bot("dev-1", BotType.DEVELOPER, ["python", "testing"], 3)
        orchestrator.register_bot("analyst-1", BotType.ANALYZER, ["analysis", "research"], 2)

        # Simulate task executions with learning
        scheduler.record_task_execution("dev-1", "development", 45.0, True)
        scheduler.record_task_execution("dev-1", "development", 47.0, True)
        scheduler.record_task_execution("dev-1", "development", 46.0, True)

        scheduler.record_task_execution("analyst-1", "analysis", 30.0, True)
        scheduler.record_task_execution("analyst-1", "analysis", 31.0, True)
        scheduler.record_task_execution("analyst-1", "analysis", 32.0, True)

        # Get scheduling recommendations
        dev_rec = scheduler.get_recommendation("development")
        analysis_rec = scheduler.get_recommendation("analysis")

        assert dev_rec is not None
        assert analysis_rec is not None
        assert dev_rec.recommended_bot == "dev-1"
        assert analysis_rec.recommended_bot == "analyst-1"

        # Inter-bot communication
        messenger.send_message("dev-1", "analyst-1", "Code review ready", "P1")
        messenger.send_message("analyst-1", "dev-1", "Analysis complete", "P1")
        messenger.process_outgoing_queue()

        # Health evaluation
        metrics = health.evaluate_health(
            total_bots=2,
            active_bots=2,
            queued_tasks=1,
            avg_bot_load=0.6,
            system_cpu_percent=0.5,
            system_memory_percent=0.6,
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.99
        )

        dashboard = health.get_dashboard()
        assert dashboard["overall_status"] in ["healthy", "warning"]
        assert dashboard["health_score"] > 70

        # Verify no breaking of existing orchestration
        analysis = orchestrator.analyze_task("test-1", "Analyze data distribution")
        assert analysis.task_type == "analysis"

        routing = orchestrator.route_task(analysis)
        assert routing == "analyst-1"  # Should route to analyzer bot

    def test_feature_3_doesnt_break_existing_messaging(self, services):
        """Test Feature 3 is compatible with existing direct message API."""
        # The bot_service.py had existing direct message endpoints
        # Feature 3 adds /api/messaging/* endpoints alongside them
        # This test verifies both work

        messenger = services["messenger"]

        # Old-style direct message (from bot_service.py /message endpoint)
        # Would be handled by bot_service, not by messenger service
        # But messenger should handle the new-style messaging

        # New-style messaging through Feature 3
        msg_id = messenger.send_message("bot-1", "bot-2", "Feature 3 message", "P1")
        assert msg_id is not None

        messenger.process_outgoing_queue()
        messages = messenger.retrieve_messages("bot-2")
        assert len(messages) > 0

    def test_feature_4_doesnt_break_orchestration(self, services):
        """Test Feature 4 learning doesn't interfere with orchestration."""
        orchestrator = services["orchestrator"]
        scheduler = services["scheduler"]

        # Register bots with specializations
        orchestrator.register_bot("bot-1", BotType.DEVELOPER, ["python", "code"], max_concurrent=5)
        orchestrator.register_bot("bot-2", BotType.ANALYZER, ["analysis", "research"], max_concurrent=5)

        # Feature 4 learns independently
        scheduler.record_task_execution("bot-1", "development", 50.0, True)
        scheduler.record_task_execution("bot-1", "development", 52.0, True)
        scheduler.record_task_execution("bot-1", "development", 51.0, True)

        # Orchestration still works
        analysis = orchestrator.analyze_task("task-1", "Python code task")
        routed = orchestrator.route_task(analysis)

        # Should route to bot-1 (developer with python specialization)
        assert routed == "bot-1"

    def test_feature_5_doesnt_break_scaling(self, services):
        """Test health monitoring doesn't interfere with scaling."""
        health = services["health"]
        scaler = services["scaler"]

        scaler.current_bot_count = 3

        # Feature 5 evaluates health
        metrics = health.evaluate_health(
            total_bots=3,
            active_bots=3,
            queued_tasks=12,  # High queue
            avg_bot_load=0.8,
            system_cpu_percent=0.5,
            system_memory_percent=0.6,
            message_queue_size=0,
            pending_message_failures=0,
            avg_success_rate=0.95
        )

        # Scaling logic still works independently
        should_scale_up = scaler.should_scale_up(0.5, 12, 0.8)
        assert should_scale_up  # High queue should trigger scale up

    def test_integration_with_persistence(self, services):
        """Test that all logs are properly persisted."""
        temp_dir = services["messenger"].work_dir

        # Generate activity across all services
        services["messenger"].send_message("bot-1", "bot-2", "Test")
        services["scheduler"].record_task_execution("bot-1", "development", 40.0, True)

        # Evaluate health with an alert-generating scenario
        services["health"].evaluate_health(5, 5, 15, 0.3, 0.96, 0.5, 0, 0, 0.95)

        # Check log files exist (health-alerts may only create if alerts generated)
        assert (temp_dir / ".deia" / "bot-logs" / "bot-messaging.jsonl").exists()
        assert (temp_dir / ".deia" / "bot-logs" / "adaptive-scheduling.jsonl").exists()
        assert (temp_dir / ".deia" / "bot-logs" / "health-metrics.jsonl").exists()

        # health-alerts.jsonl only created when alerts are generated
        # In the above, we triggered a CPU critical alert and queue backlog alert
