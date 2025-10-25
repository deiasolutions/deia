"""Unit tests for Pydantic data schemas"""

import pytest
from datetime import datetime
from src.deia.models.schemas import (
    TaskSchema, BotSchema, SessionSchema, MessageSchema, ResultSchema,
    HealthMetricsSchema, BotCapabilitySchema,
    TaskStatus, TaskPriority, TaskType, BotStatus, MessageDeliveryStatus,
    SCHEMA_VERSION
)


class TestSchemaVersion:
    """Test schema versioning"""

    def test_schema_version_exists(self):
        """Test schema version is defined"""
        assert SCHEMA_VERSION == "1.0.0"


class TestTaskSchema:
    """Test task data schema"""

    def test_create_minimal_task(self):
        """Test creating task with minimal fields"""
        task = TaskSchema(
            task_id="task-001",
            task_type=TaskType.DEVELOPMENT,
            submitter_id="user-123",
            submitted_at=datetime.now(),
            content="Test task"
        )
        assert task.task_id == "task-001"
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.P2

    def test_create_full_task(self):
        """Test creating task with all fields"""
        now = datetime.now()
        task = TaskSchema(
            task_id="task-001",
            task_type=TaskType.DEVELOPMENT,
            priority=TaskPriority.P1,
            status=TaskStatus.COMPLETED,
            submitter_id="user-123",
            submitted_at=now,
            content="Test task",
            assigned_to="bot-001",
            started_at=now,
            completed_at=now,
            estimated_duration_seconds=60.0,
            actual_duration_seconds=55.0,
            result="Success",
            error=None,
            tags=["testing"],
            metadata={"key": "value"}
        )

        assert task.task_id == "task-001"
        assert task.status == TaskStatus.COMPLETED
        assert task.priority == TaskPriority.P1
        assert task.result == "Success"

    def test_task_schema_json(self):
        """Test task schema serialization"""
        task = TaskSchema(
            task_id="task-001",
            task_type=TaskType.DEVELOPMENT,
            submitter_id="user-123",
            submitted_at=datetime.now(),
            content="Test task"
        )

        json_data = task.model_dump_json()
        assert "task-001" in json_data
        assert "development" in json_data

    def test_task_priority_enum(self):
        """Test task priority levels"""
        task = TaskSchema(
            task_id="task-001",
            task_type=TaskType.GENERAL,
            priority=TaskPriority.P0,
            submitter_id="user-123",
            submitted_at=datetime.now(),
            content="Critical task"
        )
        assert task.priority == TaskPriority.P0

    def test_task_status_values(self):
        """Test all task status values"""
        statuses = [
            TaskStatus.PENDING,
            TaskStatus.QUEUED,
            TaskStatus.RUNNING,
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
            TaskStatus.CANCELLED,
        ]
        assert len(statuses) == 6


class TestBotSchema:
    """Test bot data schema"""

    def test_create_minimal_bot(self):
        """Test creating bot with minimal fields"""
        bot = BotSchema(
            bot_id="bot-001",
            port=8001,
            launched_at=datetime.now(),
            capabilities=BotCapabilitySchema(
                bot_type="developer"
            )
        )
        assert bot.bot_id == "bot-001"
        assert bot.status == BotStatus.OFFLINE

    def test_create_healthy_bot(self):
        """Test creating healthy bot"""
        now = datetime.now()
        bot = BotSchema(
            bot_id="bot-001",
            status=BotStatus.HEALTHY,
            port=8001,
            capabilities=BotCapabilitySchema(
                bot_type="developer",
                specializations=["python", "testing"],
                max_concurrent_tasks=3,
                success_rate=0.98
            ),
            process_id=12345,
            last_heartbeat=now,
            cpu_usage_percent=25.0,
            memory_usage_mb=256.0,
            current_load=0.67,
            tasks_completed=150,
            tasks_failed=2,
            launched_at=now,
        )

        assert bot.status == BotStatus.HEALTHY
        assert bot.capabilities.bot_type == "developer"
        assert bot.tasks_completed == 150

    def test_bot_status_values(self):
        """Test all bot status values"""
        statuses = [
            BotStatus.OFFLINE,
            BotStatus.STARTING,
            BotStatus.HEALTHY,
            BotStatus.DEGRADED,
            BotStatus.FAILING,
            BotStatus.STOPPED,
        ]
        assert len(statuses) == 6

    def test_bot_capability_schema(self):
        """Test bot capability nested schema"""
        capability = BotCapabilitySchema(
            bot_type="analyzer",
            specializations=["data", "research"],
            success_rate=0.95
        )
        assert capability.bot_type == "analyzer"
        assert "data" in capability.specializations


class TestSessionSchema:
    """Test session data schema"""

    def test_create_session(self):
        """Test creating session"""
        now = datetime.now()
        session = SessionSchema(
            session_id="sess-001",
            user_id="user-123",
            created_at=now,
            last_activity=now,
            is_active=True
        )

        assert session.session_id == "sess-001"
        assert session.is_active
        assert session.tasks_submitted == 0

    def test_session_with_bot(self):
        """Test session assigned to bot"""
        now = datetime.now()
        session = SessionSchema(
            session_id="sess-001",
            user_id="user-123",
            bot_id="bot-001",
            created_at=now,
            last_activity=now,
            tasks_submitted=5,
            messages_exchanged=23
        )

        assert session.bot_id == "bot-001"
        assert session.tasks_submitted == 5

    def test_session_ended(self):
        """Test ended session"""
        now = datetime.now()
        session = SessionSchema(
            session_id="sess-001",
            user_id="user-123",
            created_at=now,
            last_activity=now,
            ended_at=now,
            is_active=False
        )

        assert not session.is_active
        assert session.ended_at is not None


class TestMessageSchema:
    """Test message data schema"""

    def test_create_message(self):
        """Test creating message"""
        now = datetime.now()
        message = MessageSchema(
            message_id="msg-001",
            sender_bot="bot-dev",
            receiver_bot="bot-val",
            content="Analysis complete",
            queued_at=now
        )

        assert message.message_id == "msg-001"
        assert message.delivery_status == MessageDeliveryStatus.QUEUED
        assert message.priority == "P2"

    def test_message_delivery_states(self):
        """Test message delivery state transitions"""
        now = datetime.now()

        # Delivered
        delivered = MessageSchema(
            message_id="msg-001",
            sender_bot="bot-dev",
            receiver_bot="bot-val",
            content="Test",
            queued_at=now,
            delivery_status=MessageDeliveryStatus.DELIVERED,
            delivered_at=now
        )
        assert delivered.delivery_status == MessageDeliveryStatus.DELIVERED

        # Read
        read = MessageSchema(
            message_id="msg-002",
            sender_bot="bot-dev",
            receiver_bot="bot-val",
            content="Test",
            queued_at=now,
            delivery_status=MessageDeliveryStatus.READ,
            delivered_at=now,
            read_at=now
        )
        assert read.delivery_status == MessageDeliveryStatus.READ

        # Failed
        failed = MessageSchema(
            message_id="msg-003",
            sender_bot="bot-dev",
            receiver_bot="bot-val",
            content="Test",
            queued_at=now,
            delivery_status=MessageDeliveryStatus.FAILED,
            last_error="Receiver offline"
        )
        assert failed.delivery_status == MessageDeliveryStatus.FAILED

    def test_message_priority_levels(self):
        """Test message priority"""
        now = datetime.now()
        message = MessageSchema(
            message_id="msg-001",
            sender_bot="bot-dev",
            receiver_bot="bot-val",
            content="Critical",
            priority="P0",
            queued_at=now
        )
        assert message.priority == "P0"

    def test_message_retry(self):
        """Test message retry tracking"""
        now = datetime.now()
        message = MessageSchema(
            message_id="msg-001",
            sender_bot="bot-dev",
            receiver_bot="bot-val",
            content="Test",
            queued_at=now,
            retry_count=2,
            last_error="Timeout"
        )
        assert message.retry_count == 2


class TestResultSchema:
    """Test result data schema"""

    def test_create_successful_result(self):
        """Test successful task result"""
        now = datetime.now()
        result = ResultSchema(
            task_id="task-001",
            status=TaskStatus.COMPLETED,
            bot_id="bot-001",
            started_at=now,
            completed_at=now,
            duration_seconds=55.0,
            success=True,
            output="All tests passing"
        )

        assert result.task_id == "task-001"
        assert result.success
        assert result.output == "All tests passing"

    def test_create_failed_result(self):
        """Test failed task result"""
        now = datetime.now()
        result = ResultSchema(
            task_id="task-002",
            status=TaskStatus.FAILED,
            bot_id="bot-001",
            started_at=now,
            completed_at=now,
            duration_seconds=30.0,
            success=False,
            error="Connection timeout",
            attempt_number=2
        )

        assert not result.success
        assert result.error == "Connection timeout"
        assert result.attempt_number == 2

    def test_result_with_metrics(self):
        """Test result with usage metrics"""
        now = datetime.now()
        result = ResultSchema(
            task_id="task-001",
            status=TaskStatus.COMPLETED,
            bot_id="bot-001",
            started_at=now,
            completed_at=now,
            duration_seconds=100.0,
            success=True,
            output="Done",
            tokens_used=2500,
            cost_cents=12.50
        )

        assert result.tokens_used == 2500
        assert result.cost_cents == 12.50


class TestHealthMetricsSchema:
    """Test health metrics schema"""

    def test_create_metrics(self):
        """Test creating health metrics"""
        now = datetime.now()
        metrics = HealthMetricsSchema(
            timestamp=now,
            cpu_percent=45.2,
            memory_percent=62.1,
            disk_available_gb=100.5
        )

        assert metrics.cpu_percent == 45.2
        assert metrics.memory_percent == 62.1

    def test_metrics_with_bot_data(self):
        """Test metrics with bot information"""
        now = datetime.now()
        metrics = HealthMetricsSchema(
            timestamp=now,
            cpu_percent=45.2,
            memory_percent=62.1,
            disk_available_gb=100.5,
            total_bots=5,
            active_bots=4,
            avg_bot_load=0.65,
            queued_tasks=3,
            success_rate=0.97
        )

        assert metrics.total_bots == 5
        assert metrics.active_bots == 4
        assert metrics.success_rate == 0.97

    def test_metrics_validation(self):
        """Test metrics value validation"""
        now = datetime.now()
        metrics = HealthMetricsSchema(
            timestamp=now,
            cpu_percent=100.0,  # Max
            memory_percent=0.0,  # Min
            disk_available_gb=0.0
        )

        assert metrics.cpu_percent == 100.0
        assert metrics.memory_percent == 0.0


class TestSchemaSerialization:
    """Test schema serialization and deserialization"""

    def test_schema_dict_conversion(self):
        """Test converting schema to dict"""
        task = TaskSchema(
            task_id="task-001",
            task_type=TaskType.DEVELOPMENT,
            submitter_id="user-123",
            submitted_at=datetime.now(),
            content="Test"
        )

        data = task.model_dump()
        assert isinstance(data, dict)
        assert data["task_id"] == "task-001"

    def test_schema_json_roundtrip(self):
        """Test JSON serialization roundtrip"""
        now = datetime.now()
        original = TaskSchema(
            task_id="task-001",
            task_type=TaskType.DEVELOPMENT,
            submitter_id="user-123",
            submitted_at=now,
            content="Test"
        )

        json_str = original.model_dump_json()
        loaded = TaskSchema.model_validate_json(json_str)

        assert loaded.task_id == original.task_id
        assert loaded.task_type == original.task_type


class TestSchemaValidation:
    """Test schema validation"""

    def test_task_requires_required_fields(self):
        """Test task schema requires required fields"""
        with pytest.raises(ValueError):
            TaskSchema(
                task_id="task-001"
                # Missing required fields
            )

    def test_task_accepts_optional_fields(self):
        """Test task schema optional fields are truly optional"""
        task = TaskSchema(
            task_id="task-001",
            task_type=TaskType.GENERAL,
            submitter_id="user-123",
            submitted_at=datetime.now(),
            content="Test"
            # All optional fields omitted
        )
        assert task.result is None
        assert task.error is None
        assert task.assigned_to is None
