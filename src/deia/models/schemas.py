"""
DEIA Data Model Schemas - Formal definitions for all critical data types

Uses Pydantic for validation, serialization, and documentation.
All schemas are versioned and include example data.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator


# Schema Version
SCHEMA_VERSION = "1.0.0"


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority levels"""
    P0 = "P0"  # Critical
    P1 = "P1"  # High
    P2 = "P2"  # Normal (default)
    P3 = "P3"  # Low


class TaskType(str, Enum):
    """Task types"""
    DEVELOPMENT = "development"
    ANALYSIS = "analysis"
    WRITING = "writing"
    PLANNING = "planning"
    GENERAL = "general"


class BotStatus(str, Enum):
    """Bot execution status"""
    OFFLINE = "offline"
    STARTING = "starting"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILING = "failing"
    STOPPED = "stopped"


class MessageDeliveryStatus(str, Enum):
    """Message delivery status"""
    QUEUED = "queued"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    EXPIRED = "expired"


class TaskSchema(BaseModel):
    """Schema for task data"""
    task_id: str = Field(..., description="Unique task identifier")
    task_type: TaskType = Field(..., description="Type of task")
    priority: TaskPriority = Field(default=TaskPriority.P2, description="Task priority")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current task status")

    # Submission info
    submitter_id: str = Field(..., description="ID of user who submitted task")
    submitted_at: datetime = Field(..., description="When task was submitted")
    content: str = Field(..., description="Task description/content")

    # Execution info
    assigned_to: Optional[str] = Field(None, description="Bot ID assigned to this task")
    started_at: Optional[datetime] = Field(None, description="When task execution started")
    completed_at: Optional[datetime] = Field(None, description="When task execution completed")

    # Execution metrics
    estimated_duration_seconds: Optional[float] = Field(None, description="Estimated execution time")
    actual_duration_seconds: Optional[float] = Field(None, description="Actual execution time")

    # Results
    result: Optional[str] = Field(None, description="Task result/output")
    error: Optional[str] = Field(None, description="Error message if task failed")

    # Metadata
    tags: List[str] = Field(default_factory=list, description="Task tags for filtering")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "task-001",
                "task_type": "development",
                "priority": "P1",
                "status": "completed",
                "submitter_id": "user-123",
                "submitted_at": "2025-10-25T15:00:00Z",
                "content": "Write Python unit tests",
                "assigned_to": "bot-dev-001",
                "started_at": "2025-10-25T15:05:00Z",
                "completed_at": "2025-10-25T15:10:00Z",
                "actual_duration_seconds": 300,
                "result": "All tests passing",
                "tags": ["testing", "python"],
            }
        }


class BotCapabilitySchema(BaseModel):
    """Bot specializations and capabilities"""
    bot_type: str = Field(..., description="Bot type (developer, analyzer, writer, etc)")
    specializations: List[str] = Field(default_factory=list, description="Specific skills")
    max_concurrent_tasks: int = Field(default=3, description="Max parallel tasks")
    success_rate: float = Field(default=1.0, description="Success rate (0-1)")


class BotSchema(BaseModel):
    """Schema for bot data"""
    bot_id: str = Field(..., description="Unique bot identifier")
    status: BotStatus = Field(default=BotStatus.OFFLINE, description="Bot status")

    # Process info
    process_id: Optional[int] = Field(None, description="OS process ID")
    port: int = Field(..., description="HTTP service port")

    # Capabilities
    capabilities: BotCapabilitySchema = Field(..., description="Bot capabilities")

    # Health metrics
    last_heartbeat: Optional[datetime] = Field(None, description="Last heartbeat timestamp")
    cpu_usage_percent: Optional[float] = Field(None, description="CPU usage (0-100)")
    memory_usage_mb: Optional[float] = Field(None, description="Memory usage in MB")

    # Task metrics
    current_load: float = Field(default=0.0, description="Current load (0-1)")
    tasks_completed: int = Field(default=0, description="Total completed tasks")
    tasks_failed: int = Field(default=0, description="Total failed tasks")

    # Timestamps
    launched_at: datetime = Field(..., description="When bot was launched")
    last_task_completed: Optional[datetime] = Field(None, description="Last task completion")

    class Config:
        json_schema_extra = {
            "example": {
                "bot_id": "bot-dev-001",
                "status": "healthy",
                "process_id": 12345,
                "port": 8001,
                "capabilities": {
                    "bot_type": "developer",
                    "specializations": ["python", "testing"],
                    "max_concurrent_tasks": 3,
                    "success_rate": 0.98
                },
                "last_heartbeat": "2025-10-25T15:10:00Z",
                "cpu_usage_percent": 25.0,
                "memory_usage_mb": 256,
                "current_load": 0.67,
                "tasks_completed": 150,
                "tasks_failed": 2,
                "launched_at": "2025-10-25T10:00:00Z",
            }
        }


class SessionSchema(BaseModel):
    """Schema for user session data"""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User ID for this session")
    bot_id: Optional[str] = Field(None, description="Bot assigned to session")

    # Session lifecycle
    created_at: datetime = Field(..., description="Session start time")
    ended_at: Optional[datetime] = Field(None, description="Session end time")
    last_activity: datetime = Field(..., description="Last user activity")

    # Session state
    is_active: bool = Field(default=True, description="Whether session is active")
    tasks_submitted: int = Field(default=0, description="Tasks submitted in session")
    messages_exchanged: int = Field(default=0, description="Messages in session")

    # Metadata
    ip_address: Optional[str] = Field(None, description="Client IP address")
    user_agent: Optional[str] = Field(None, description="Client user agent")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "sess-001",
                "user_id": "user-123",
                "bot_id": "bot-dev-001",
                "created_at": "2025-10-25T09:00:00Z",
                "last_activity": "2025-10-25T15:30:00Z",
                "is_active": True,
                "tasks_submitted": 5,
                "messages_exchanged": 23,
            }
        }


class MessageSchema(BaseModel):
    """Schema for inter-bot messages"""
    message_id: str = Field(..., description="Unique message identifier")
    sender_bot: str = Field(..., description="Sending bot ID")
    receiver_bot: str = Field(..., description="Receiving bot ID")

    # Message content
    content: str = Field(..., description="Message content")
    priority: str = Field(default="P2", description="Message priority (P0-P3)")

    # Delivery
    delivery_status: MessageDeliveryStatus = Field(
        default=MessageDeliveryStatus.QUEUED,
        description="Delivery status"
    )
    queued_at: datetime = Field(..., description="When message was queued")
    delivered_at: Optional[datetime] = Field(None, description="When delivered")
    read_at: Optional[datetime] = Field(None, description="When read by receiver")
    expires_at: Optional[datetime] = Field(None, description="When message expires")

    # Retry info
    retry_count: int = Field(default=0, description="Number of delivery attempts")
    last_error: Optional[str] = Field(None, description="Last delivery error")

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "msg-001",
                "sender_bot": "bot-dev-001",
                "receiver_bot": "bot-val-001",
                "content": "Analysis results ready",
                "priority": "P1",
                "delivery_status": "delivered",
                "queued_at": "2025-10-25T15:05:00Z",
                "delivered_at": "2025-10-25T15:05:01Z",
                "expires_at": "2025-10-25T16:05:00Z",
                "retry_count": 0,
            }
        }


class ResultSchema(BaseModel):
    """Schema for task execution results"""
    task_id: str = Field(..., description="Task ID")
    status: TaskStatus = Field(..., description="Execution status")

    # Execution metrics
    bot_id: str = Field(..., description="Bot that executed task")
    started_at: datetime = Field(..., description="Execution start")
    completed_at: datetime = Field(..., description="Execution completion")
    duration_seconds: float = Field(..., description="Execution duration")

    # Results
    success: bool = Field(..., description="Whether task succeeded")
    output: Optional[str] = Field(None, description="Task output/result")
    error: Optional[str] = Field(None, description="Error message if failed")

    # Metrics
    tokens_used: Optional[int] = Field(None, description="LLM tokens used")
    cost_cents: Optional[float] = Field(None, description="Estimated cost in cents")

    # Retry info
    attempt_number: int = Field(default=1, description="Which attempt this was")
    max_attempts: int = Field(default=3, description="Max retry attempts")

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "task-001",
                "status": "completed",
                "bot_id": "bot-dev-001",
                "started_at": "2025-10-25T15:05:00Z",
                "completed_at": "2025-10-25T15:10:00Z",
                "duration_seconds": 300.5,
                "success": True,
                "output": "All 50 tests passing",
                "tokens_used": 2500,
                "attempt_number": 1,
            }
        }


class HealthMetricsSchema(BaseModel):
    """System health metrics"""
    timestamp: datetime = Field(..., description="Metrics timestamp")

    # System resources
    cpu_percent: float = Field(..., description="System CPU usage (0-100)")
    memory_percent: float = Field(..., description="System memory usage (0-100)")
    disk_available_gb: float = Field(..., description="Available disk space")

    # Bot metrics
    total_bots: int = Field(default=0, description="Total bots")
    active_bots: int = Field(default=0, description="Active bots")
    avg_bot_load: float = Field(default=0.0, description="Average bot load")

    # Queue metrics
    queued_tasks: int = Field(default=0, description="Pending tasks")
    avg_queue_wait_seconds: float = Field(default=0.0, description="Avg queue wait")

    # Success metrics
    success_rate: float = Field(default=1.0, description="Overall success rate")
    failed_tasks_24h: int = Field(default=0, description="Failed tasks in 24h")

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2025-10-25T15:30:00Z",
                "cpu_percent": 45.2,
                "memory_percent": 62.1,
                "disk_available_gb": 100.5,
                "total_bots": 5,
                "active_bots": 4,
                "avg_bot_load": 0.65,
                "queued_tasks": 3,
                "success_rate": 0.97,
            }
        }
