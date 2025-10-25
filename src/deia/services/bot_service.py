"""
Bot HTTP Service - Provides REST API for bot control.

Each bot runs a FastAPI service that Scrum Master can call for:
- Status queries
- Interrupts
- Direct messages
- Health checks
- Termination
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
import threading
import uvicorn
import os
from .task_orchestrator import TaskOrchestrator, BotType
from .bot_auto_scaler import BotAutoScaler
from .bot_messenger import BotMessenger
from .adaptive_scheduler import AdaptiveScheduler
from .health_monitor import HealthMonitor
from .config_manager import ConfigManager
from .disaster_recovery import DisasterRecovery
from .audit_logger import AuditLogger
from .degradation_manager import DegradationManager
from .migration_manager import MigrationManager


class DirectMessage(BaseModel):
    """Direct message from Scrum Master to bot."""
    from_bot: str
    content: str
    priority: str = "P2"


class BotServiceConfig(BaseModel):
    """Configuration for bot service."""
    bot_id: str
    port: int
    work_dir: Path


class BotService:
    """
    HTTP service for bot control and status.

    Runs in background thread alongside bot's task execution loop.
    Provides endpoints for Scrum Master to interact with bot directly.
    """

    def __init__(self, bot_id: str, port: int, work_dir: Path):
        """
        Initialize bot service.

        Args:
            bot_id: Full bot ID (e.g., "deiasolutions-CLAUDE-CODE-001")
            port: Port to run service on
            work_dir: Bot working directory
        """
        self.bot_id = bot_id
        self.port = port
        self.work_dir = Path(work_dir)
        self.app = FastAPI(title=f"Bot Service: {bot_id}")
        self.running = False
        self.server_thread: Optional[threading.Thread] = None

        # Shared state (thread-safe via simple assignment)
        self.current_status = "idle"
        self.current_task: Optional[str] = None
        self.interrupt_requested = False
        self.terminate_requested = False
        self.direct_messages: list = []

        # Orchestration support
        self.orchestrator = TaskOrchestrator(work_dir)

        # Auto scaling support
        self.auto_scaler = BotAutoScaler(work_dir)

        # Messaging support
        self.messenger = BotMessenger(work_dir)

        # Adaptive scheduling support
        self.adaptive_scheduler = AdaptiveScheduler(work_dir)

        # Health monitoring support
        self.health_monitor = HealthMonitor(work_dir)

        # Configuration management support
        self.config_manager = ConfigManager(work_dir)
        self.config_manager.load_config("bot-config")

        # Disaster recovery support
        self.disaster_recovery = DisasterRecovery(work_dir)

        # Audit logging support
        self.audit_logger = AuditLogger(work_dir)

        # Graceful degradation support
        self.degradation_manager = DegradationManager(work_dir)

        # Migration/deployment support
        self.migration_manager = MigrationManager(work_dir)

        # Setup routes
        self._setup_routes()

    def _setup_routes(self):
        """Setup FastAPI routes."""

        @self.app.get("/health")
        async def health():
            """Health check endpoint."""
            return {"status": "ok", "bot_id": self.bot_id, "timestamp": datetime.now().isoformat()}

        @self.app.get("/status")
        async def get_status():
            """
            Get current bot status.

            Returns:
            {
                "bot_id": "deiasolutions-CLAUDE-CODE-001",
                "status": "working|idle|paused",
                "current_task": "task-id or null",
                "port": 8001,
                "pid": 12345
            }
            """
            return {
                "bot_id": self.bot_id,
                "status": self.current_status,
                "current_task": self.current_task,
                "port": self.port,
                "pid": os.getpid(),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/interrupt")
        async def interrupt():
            """
            Interrupt current task.

            Bot will stop current work and return to idle state.
            """
            print(f"[{self.bot_id}] [SERVICE] Interrupt requested")
            self.interrupt_requested = True
            return {"success": True, "message": "Interrupt signal sent"}

        @self.app.post("/terminate")
        async def terminate():
            """
            Request bot termination.

            Bot will finish current task and shut down gracefully.
            """
            print(f"[{self.bot_id}] [SERVICE] Terminate requested")
            self.terminate_requested = True
            return {"success": True, "message": "Terminate signal sent"}

        @self.app.post("/message")
        async def direct_message(msg: DirectMessage):
            """
            Send direct message to bot.

            For urgent communications that don't need full task file.
            Bot should check this periodically.
            """
            print(f"[{self.bot_id}] [SERVICE] Direct message from {msg.from_bot}: {msg.content[:50]}...")

            self.direct_messages.append({
                "from": msg.from_bot,
                "content": msg.content,
                "priority": msg.priority,
                "timestamp": datetime.now().isoformat()
            })

            return {"success": True, "message": "Message queued"}

        @self.app.get("/messages")
        async def get_messages():
            """
            Get queued direct messages.

            Bot calls this to check for urgent messages from Scrum Master.
            """
            messages = self.direct_messages.copy()
            self.direct_messages.clear()  # Clear after reading
            return {"messages": messages}

        @self.app.post("/api/orchestrate")
        async def orchestrate_task(task: Dict[str, Any]):
            """
            Route a task to the best bot in the swarm.

            Request body:
            {
                "task_id": "TASK-001",
                "content": "task description",
                "priority": "P1"
            }

            Returns:
            {
                "routed_to": "bot-id",
                "queued": true,
                "message": "Task queued for bot-id"
            }
            """
            task_id = task.get("task_id", f"task-{datetime.now().timestamp()}")
            content = task.get("content", "")
            priority = task.get("priority", "P2")

            # Analyze task
            analysis = self.orchestrator.analyze_task(task_id, content)

            # Route to best bot
            selected_bot = self.orchestrator.route_task(analysis)

            if not selected_bot:
                return {
                    "success": False,
                    "error": "No suitable bot available",
                    "task_id": task_id
                }

            # Queue task
            queued = self.orchestrator.queue_task(task_id, selected_bot, content)

            return {
                "success": queued,
                "task_id": task_id,
                "routed_to": selected_bot,
                "task_type": analysis.task_type,
                "complexity": analysis.complexity,
                "message": f"Task {task_id} routed to {selected_bot}" if queued else "Failed to queue"
            }

        @self.app.get("/api/orchestrate/status")
        async def orchestration_status():
            """
            Get status of orchestration system.

            Returns:
            {
                "total_bots": 5,
                "queued_tasks": 3,
                "total_load": 8,
                "bots": {
                    "bot-001": { "load": 2, "capacity": 3, "success_rate": 0.98 },
                    ...
                }
            }
            """
            return self.orchestrator.get_orchestration_status()

        @self.app.post("/api/orchestrate/register-bot")
        async def register_bot(bot_info: Dict[str, Any]):
            """
            Register a bot in the orchestrator.

            Request body:
            {
                "bot_id": "bot-001",
                "type": "developer",
                "specializations": ["python", "testing"],
                "max_concurrent": 3
            }
            """
            bot_id = bot_info.get("bot_id")
            bot_type_str = bot_info.get("type", "general")
            specializations = bot_info.get("specializations", [])
            max_concurrent = bot_info.get("max_concurrent", 3)

            try:
                bot_type = BotType[bot_type_str.upper()]
            except KeyError:
                bot_type = BotType.GENERAL

            self.orchestrator.register_bot(
                bot_id=bot_id,
                bot_type=bot_type,
                specializations=specializations,
                max_concurrent=max_concurrent
            )

            return {
                "success": True,
                "message": f"Bot {bot_id} registered",
                "bot_type": bot_type.value
            }

        @self.app.get("/api/orchestrate/bot/{bot_id}/status")
        async def bot_status(bot_id: str):
            """Get status of a specific bot."""
            status = self.orchestrator.get_bot_status(bot_id)

            if not status:
                raise HTTPException(status_code=404, detail=f"Bot {bot_id} not found")

            return status

        @self.app.post("/api/scaling/evaluate")
        async def evaluate_scaling(scaling_params: Dict[str, Any]):
            """
            Evaluate system and take scaling action if needed.

            Request body:
            {
                "current_load": 0.75,
                "queue_size": 8,
                "avg_bot_load": 0.65
            }

            Returns:
            {
                "action_taken": "scale_up" or "scale_down" or null,
                "current_bot_count": 5,
                "new_bots": ["BOT-001", "BOT-002"],
                "timestamp": "2025-10-25T17:45:00"
            }
            """
            current_load = scaling_params.get("current_load", 0.5)
            queue_size = scaling_params.get("queue_size", 0)
            avg_bot_load = scaling_params.get("avg_bot_load", 0.0)

            action = self.auto_scaler.evaluate_and_scale(
                current_load=current_load,
                queue_size=queue_size,
                avg_bot_load=avg_bot_load
            )

            return {
                "action_taken": action.value if action else None,
                "current_bot_count": self.auto_scaler.current_bot_count,
                "scaling_status": self.auto_scaler.get_scaling_status(),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/scaling/scale-up")
        async def scale_up(count: int = 1):
            """
            Manually scale up (add bots).

            Query params:
            - count: Number of bots to add (default 1)

            Returns:
            {
                "success": true,
                "added": 1,
                "new_bots": ["BOT-123"],
                "total_bots": 5
            }
            """
            success, new_bots = self.auto_scaler.scale_up(count=count)

            return {
                "success": success,
                "added": len(new_bots),
                "new_bots": new_bots,
                "total_bots": self.auto_scaler.current_bot_count
            }

        @self.app.post("/api/scaling/scale-down")
        async def scale_down(count: int = 1):
            """
            Manually scale down (remove bots).

            Query params:
            - count: Number of bots to remove (default 1)

            Returns:
            {
                "success": true,
                "removed": 1,
                "removed_bots": ["BOT-123"],
                "total_bots": 4
            }
            """
            success, removed_bots = self.auto_scaler.scale_down(count=count)

            return {
                "success": success,
                "removed": len(removed_bots),
                "removed_bots": removed_bots,
                "total_bots": self.auto_scaler.current_bot_count
            }

        @self.app.get("/api/scaling/status")
        async def scaling_status():
            """
            Get auto-scaling status.

            Returns:
            {
                "current_bot_count": 5,
                "min_bots": 1,
                "max_bots": 10,
                "active_bots": ["BOT-001", "BOT-002", ...],
                "scaling_enabled": true,
                "last_scale_up": "2025-10-25T17:30:00",
                "last_scale_down": null
            }
            """
            return self.auto_scaler.get_scaling_status()

        @self.app.post("/api/messaging/send")
        async def send_message(msg_data: Dict[str, Any]):
            """
            Send a message from one bot to another.

            Request body:
            {
                "to_bot": "bot-id",
                "content": "message content",
                "priority": "P0|P1|P2|P3" (optional, default P2),
                "ttl_seconds": 3600 (optional),
                "metadata": {} (optional)
            }

            Returns:
            {
                "success": true,
                "message_id": "uuid",
                "from_bot": "bot-id",
                "to_bot": "bot-id",
                "status": "pending"
            }
            """
            to_bot = msg_data.get("to_bot")
            content = msg_data.get("content", "")
            priority = msg_data.get("priority", "P2")
            ttl_seconds = msg_data.get("ttl_seconds", 3600)
            metadata = msg_data.get("metadata", {})

            if not to_bot or not content:
                raise HTTPException(status_code=400, detail="Missing to_bot or content")

            message_id = self.messenger.send_message(
                from_bot=self.bot_id,
                to_bot=to_bot,
                content=content,
                priority=priority,
                ttl_seconds=ttl_seconds,
                metadata=metadata
            )

            return {
                "success": True,
                "message_id": message_id,
                "from_bot": self.bot_id,
                "to_bot": to_bot,
                "status": "pending",
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/messaging/inbox")
        async def get_inbox(priority: str = None):
            """
            Get messages in this bot's inbox.

            Query params:
            - priority: Optional priority filter (P0|P1|P2|P3)

            Returns:
            {
                "bot_id": "bot-id",
                "messages": [
                    {
                        "message_id": "uuid",
                        "from_bot": "sender-id",
                        "content": "...",
                        "priority": "P2",
                        "status": "delivered",
                        "created_at": "2025-10-25T...",
                        ...
                    }
                ],
                "count": 5
            }
            """
            messages = self.messenger.retrieve_messages(self.bot_id, priority)

            return {
                "bot_id": self.bot_id,
                "messages": messages,
                "count": len(messages),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/messaging/read/{message_id}")
        async def mark_message_read(message_id: str):
            """
            Mark a message as read.

            Path params:
            - message_id: Message UUID

            Returns:
            {
                "success": true,
                "message_id": "uuid",
                "status": "read"
            }
            """
            success = self.messenger.mark_as_read(self.bot_id, message_id)

            if not success:
                raise HTTPException(status_code=404, detail=f"Message {message_id} not found")

            return {
                "success": True,
                "message_id": message_id,
                "status": "read",
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/messaging/process-queue")
        async def process_outgoing():
            """
            Process outgoing message queue (deliver pending messages).

            Returns:
            {
                "delivered": 3,
                "failed": 0,
                "retried": 1,
                "pending": 2
            }
            """
            result = self.messenger.process_outgoing_queue()
            result["timestamp"] = datetime.now().isoformat()
            return result

        @self.app.get("/api/messaging/status")
        async def messaging_status():
            """
            Get messaging system status.

            Returns:
            {
                "total_bots": 5,
                "total_messages": 150,
                "pending_delivery": 3,
                "status_breakdown": {
                    "pending": 3,
                    "delivered": 100,
                    "read": 45,
                    "failed": 2,
                    "expired": 0
                },
                "priority_breakdown": {
                    "P0": 2,
                    "P1": 15,
                    "P2": 120,
                    "P3": 13
                },
                "bots": {
                    "bot-001": {"total_messages": 10, "unread": 2},
                    ...
                }
            }
            """
            return self.messenger.get_messaging_status()

        @self.app.get("/api/messaging/conversation/{other_bot_id}")
        async def get_conversation(other_bot_id: str):
            """
            Get conversation history with another bot.

            Path params:
            - other_bot_id: The other bot's ID

            Returns:
            {
                "bot_1": "this-bot-id",
                "bot_2": "other-bot-id",
                "messages": [
                    {message dicts sorted by time}
                ],
                "count": 5
            }
            """
            conversation = self.messenger.get_bot_conversation(self.bot_id, other_bot_id)

            return {
                "bot_1": self.bot_id,
                "bot_2": other_bot_id,
                "messages": conversation,
                "count": len(conversation),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/scheduling/record-execution")
        async def record_task_execution(execution_data: Dict[str, Any]):
            """
            Record task execution for adaptive learning.

            Request body:
            {
                "task_type": "development|analysis|writing|planning|validation",
                "execution_time": 123.45,
                "success": true
            }

            Returns:
            {
                "success": true,
                "bot_id": "bot-id",
                "task_type": "development",
                "recorded": true
            }
            """
            task_type = execution_data.get("task_type", "general")
            execution_time = execution_data.get("execution_time", 0.0)
            success = execution_data.get("success", True)

            self.adaptive_scheduler.record_task_execution(
                bot_id=self.bot_id,
                task_type=task_type,
                execution_time=execution_time,
                success=success
            )

            return {
                "success": True,
                "bot_id": self.bot_id,
                "task_type": task_type,
                "recorded": True,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/scheduling/recommendation/{task_type}")
        async def get_scheduling_recommendation(task_type: str):
            """
            Get scheduling recommendation for a task type.

            Path params:
            - task_type: Type of task

            Returns:
            {
                "task_type": "development",
                "recommended_bot": "bot-001",
                "confidence": 0.85,
                "reason": "Best performer...",
                "alternatives": [...]
            }
            """
            recommendation = self.adaptive_scheduler.get_recommendation(task_type)

            if not recommendation:
                raise HTTPException(
                    status_code=404,
                    detail=f"No learning data for task type: {task_type}"
                )

            return {
                "task_type": recommendation.task_type,
                "recommended_bot": recommendation.recommended_bot,
                "confidence": recommendation.confidence,
                "reason": recommendation.reason,
                "alternatives": recommendation.alternatives,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/scheduling/bot-performance/{bot_id}")
        async def get_bot_performance(bot_id: str):
            """
            Get performance metrics for a bot across all task types.

            Path params:
            - bot_id: Bot identifier

            Returns:
            {
                "bot_id": "bot-001",
                "performance": {
                    "development": {
                        "total_tasks": 10,
                        "avg_execution_time": 45.2,
                        "success_rate": 0.95
                    },
                    ...
                }
            }
            """
            performance = self.adaptive_scheduler.get_bot_performance(bot_id)

            return {
                "bot_id": bot_id,
                "performance": {
                    task_type: perf.to_dict()
                    for task_type, perf in performance.items()
                },
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/scheduling/task-type/{task_type}")
        async def get_task_type_performance(task_type: str):
            """
            Get all bots' performance on a specific task type.

            Path params:
            - task_type: Task type

            Returns:
            {
                "task_type": "development",
                "bots": [
                    {
                        "bot_id": "bot-001",
                        "total_tasks": 10,
                        "avg_execution_time": 45.2,
                        "success_rate": 0.95
                    },
                    ...
                ]
            }
            """
            performers = self.adaptive_scheduler.get_task_type_performance(task_type)

            return {
                "task_type": task_type,
                "bots": [perf.to_dict() for perf in performers],
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/scheduling/insights")
        async def get_learning_insights():
            """
            Get learning insights - what we've learned so far.

            Returns:
            {
                "total_executions": 150,
                "total_bots_observed": 5,
                "task_types_learned": 4,
                "by_task_type": {
                    "development": {...},
                    ...
                }
            }
            """
            return self.adaptive_scheduler.get_learning_insights()

        @self.app.get("/api/scheduling/history")
        async def get_scheduling_history(limit: int = 100):
            """
            Get recent scheduling/execution history.

            Query params:
            - limit: Number of records (default 100)

            Returns:
            {
                "total_records": 150,
                "returned": 50,
                "history": [...]
            }
            """
            history = self.adaptive_scheduler.get_scheduling_history(limit)

            return {
                "total_records": len(self.adaptive_scheduler.task_history),
                "returned": len(history),
                "history": history,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/dashboard/health/evaluate")
        async def evaluate_health(health_data: Dict[str, Any]):
            """
            Evaluate system health and generate alerts.

            Request body:
            {
                "total_bots": 5,
                "active_bots": 4,
                "queued_tasks": 3,
                "avg_bot_load": 0.65,
                "system_cpu_percent": 0.45,
                "system_memory_percent": 0.60,
                "message_queue_size": 2,
                "pending_message_failures": 0,
                "avg_success_rate": 0.95
            }

            Returns:
            {
                "status": "healthy|warning|critical",
                "timestamp": "...",
                "metrics": {...},
                "active_alerts": [...]
            }
            """
            metrics = self.health_monitor.evaluate_health(
                total_bots=health_data.get("total_bots", 0),
                active_bots=health_data.get("active_bots", 0),
                queued_tasks=health_data.get("queued_tasks", 0),
                avg_bot_load=health_data.get("avg_bot_load", 0.0),
                system_cpu_percent=health_data.get("system_cpu_percent", 0.0),
                system_memory_percent=health_data.get("system_memory_percent", 0.0),
                message_queue_size=health_data.get("message_queue_size", 0),
                pending_message_failures=health_data.get("pending_message_failures", 0),
                avg_success_rate=health_data.get("avg_success_rate", 1.0)
            )

            return {
                "timestamp": metrics.timestamp,
                "metrics": metrics.to_dict(),
                "active_alerts": len([a for a in self.health_monitor.alerts.values() if not a.resolved]),
                "health_evaluated": True
            }

        @self.app.get("/api/dashboard/health")
        async def get_health_dashboard():
            """
            Get comprehensive health dashboard.

            Returns:
            {
                "overall_status": "healthy|warning|critical",
                "health_score": 85,
                "metrics": {...},
                "active_alerts": [...],
                "bot_health": {...},
                "system_resources": {...},
                "queue_status": {...}
            }
            """
            return self.health_monitor.get_dashboard()

        @self.app.get("/api/dashboard/alerts")
        async def get_alerts(level: str = None):
            """
            Get system alerts.

            Query params:
            - level: Filter by level (critical|warning|info)

            Returns:
            {
                "alerts": [...],
                "count": 3
            }
            """
            alerts = self.health_monitor.get_alerts(level=level)

            return {
                "alerts": alerts,
                "count": len(alerts),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/dashboard/alerts/{alert_id}/resolve")
        async def resolve_alert(alert_id: str):
            """
            Mark an alert as resolved.

            Path params:
            - alert_id: Alert identifier

            Returns:
            {
                "success": true,
                "alert_id": "...",
                "resolved": true
            }
            """
            success = self.health_monitor.resolve_alert(alert_id)

            if not success:
                raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

            return {
                "success": True,
                "alert_id": alert_id,
                "resolved": True,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/config/current")
        async def get_current_config():
            """
            Get current system configuration.

            Returns:
            {
                "version": "1.0",
                "environment": "production",
                "thresholds": {...},
                "bot_limits": {...},
                ...
            }
            """
            return self.config_manager.get_config().to_dict()

        @self.app.get("/api/config/value/{key_path}")
        async def get_config_value(key_path: str):
            """
            Get specific configuration value by dot-notation path.

            Examples:
            - /api/config/value/thresholds.cpu_warning_percent
            - /api/config/value/bot_limits.max_bots

            Returns:
            {
                "key": "thresholds.cpu_warning_percent",
                "value": 0.80
            }
            """
            value = self.config_manager.get_value(key_path)

            if value is None:
                raise HTTPException(status_code=404, detail=f"Config key not found: {key_path}")

            return {
                "key": key_path,
                "value": value,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/config/reload")
        async def reload_config(config_name: str = "bot-config"):
            """
            Reload configuration from file.

            Query params:
            - config_name: Config file name (default: bot-config)

            Returns:
            {
                "success": true,
                "config_version": "1.0",
                "environment": "production",
                "loaded_from": "/path/to/config.yaml"
            }
            """
            success = self.config_manager.load_config(config_name)

            if not success and self.config_manager.load_errors:
                return {
                    "success": False,
                    "errors": self.config_manager.load_errors,
                    "timestamp": datetime.now().isoformat()
                }

            return {
                "success": True,
                "config_version": self.config_manager.config.version,
                "environment": self.config_manager.config.environment,
                "loaded_from": str(self.config_manager.config_file_path),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/config/check-reload")
        async def check_reload_config(config_name: str = "bot-config"):
            """
            Check if config file changed and reload if needed (hot-reload).

            Query params:
            - config_name: Config file name (default: bot-config)

            Returns:
            {
                "reloaded": true,
                "config_version": "1.0"
            }
            """
            reloaded = self.config_manager.reload_if_changed(config_name)

            return {
                "reloaded": reloaded,
                "config_version": self.config_manager.config.version,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/config/status")
        async def config_status():
            """
            Get configuration manager status.

            Returns:
            {
                "config_file": "/path/to/config.yaml",
                "last_load_time": "2025-10-25T...",
                "errors": [],
                "config_version": "1.0"
            }
            """
            return self.config_manager.get_status()

        @self.app.post("/api/disaster-recovery/backup")
        async def create_backup(backup_data: Dict[str, Any]):
            """
            Create a backup of system state.

            Request body:
            {
                "backup_type": "registry|queue|bot_assignments|full",
                "data": {...},
                "source": "optional description",
                "tags": {"key": "value"}
            }

            Returns:
            {
                "success": true,
                "backup_id": "uuid",
                "timestamp": "2025-10-25T..."
            }
            """
            backup_type_str = backup_data.get("backup_type", "registry")
            data = backup_data.get("data", {})
            source = backup_data.get("source", "")
            tags = backup_data.get("tags", {})

            from .disaster_recovery import BackupType
            try:
                backup_type = BackupType[backup_type_str.upper()]
            except KeyError:
                backup_type = BackupType.REGISTRY

            success, backup_id = self.disaster_recovery.create_backup(
                backup_type,
                data,
                source,
                tags
            )

            return {
                "success": success,
                "backup_id": backup_id,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/disaster-recovery/restore/{backup_id}")
        async def restore_backup(backup_id: str):
            """
            Restore from a backup.

            Path params:
            - backup_id: Backup ID to restore

            Returns:
            {
                "success": true,
                "data": {...},
                "timestamp": "2025-10-25T..."
            }
            """
            success, data = self.disaster_recovery.restore_backup(backup_id)

            if not success:
                raise HTTPException(status_code=404, detail=f"Backup {backup_id} not found")

            return {
                "success": True,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/disaster-recovery/restore-point")
        async def create_restore_point(restore_data: Dict[str, Any]):
            """
            Create a full restore point from multiple backups.

            Request body:
            {
                "registry_data": {...},
                "queue_data": {...},
                "assignments_data": {...},
                "description": "optional",
                "manual": true/false
            }

            Returns:
            {
                "success": true,
                "restore_point_id": "uuid"
            }
            """
            success, restore_id = self.disaster_recovery.create_restore_point(
                registry_data=restore_data.get("registry_data"),
                queue_data=restore_data.get("queue_data"),
                assignments_data=restore_data.get("assignments_data"),
                description=restore_data.get("description", ""),
                manual=restore_data.get("manual", False)
            )

            return {
                "success": success,
                "restore_point_id": restore_id,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/disaster-recovery/backup-history")
        async def backup_history(backup_type: str = None, limit: int = 100):
            """
            Get backup history.

            Query params:
            - backup_type: Filter by type (registry|queue|bot_assignments)
            - limit: Max results (default 100)

            Returns:
            {
                "backups": [...],
                "count": 5
            }
            """
            from .disaster_recovery import BackupType

            filter_type = None
            if backup_type:
                try:
                    filter_type = BackupType[backup_type.upper()]
                except KeyError:
                    pass

            backups = self.disaster_recovery.get_backup_history(filter_type, limit)

            return {
                "backups": backups,
                "count": len(backups),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/disaster-recovery/restore-point/{restore_point_id}")
        async def get_restore_point(restore_point_id: str):
            """
            Get details of a restore point.

            Path params:
            - restore_point_id: Restore point ID

            Returns:
            {
                "restore_id": "uuid",
                "timestamp": "2025-10-25T...",
                "backups": [...],
                "backup_details": [...]
            }
            """
            details = self.disaster_recovery.get_restore_point_details(restore_point_id)

            if not details:
                raise HTTPException(status_code=404, detail=f"Restore point {restore_point_id} not found")

            return {
                "details": details,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/disaster-recovery/status")
        async def disaster_recovery_status():
            """
            Get disaster recovery system status.

            Returns:
            {
                "total_backups": 10,
                "total_restore_points": 2,
                "latest_backup": "uuid",
                "crash_detected": false,
                "disk_usage_mb": 45.2
            }
            """
            return self.disaster_recovery.get_status()

        @self.app.post("/api/disaster-recovery/mark-shutdown")
        async def mark_shutdown():
            """
            Mark clean shutdown (call before service stops).

            Returns:
            {
                "success": true,
                "message": "Shutdown marked"
            }
            """
            success = self.disaster_recovery.mark_clean_shutdown()

            return {
                "success": success,
                "message": "Clean shutdown marked" if success else "Failed to mark shutdown",
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/api/audit/log")
        async def audit_log(log_data: Dict[str, Any]):
            """
            Log an action to the audit trail.

            Request body:
            {
                "action": "bot_created|task_submitted|...",
                "actor": "who did it",
                "target": "what was affected",
                "level": "info|warning|critical",
                "details": {},
                "result": "success|failure|partial",
                "error_message": "optional"
            }
            """
            from .audit_logger import AuditAction, AuditLevel

            action_str = log_data.get("action", "api_call").upper()
            try:
                action = AuditAction[action_str]
            except KeyError:
                action = AuditAction.API_CALL

            level_str = log_data.get("level", "info").upper()
            try:
                level = AuditLevel[level_str]
            except KeyError:
                level = AuditLevel.INFO

            entry_id = self.audit_logger.log_action(
                action=action,
                actor=log_data.get("actor", "unknown"),
                target=log_data.get("target", "unknown"),
                level=level,
                details=log_data.get("details"),
                result=log_data.get("result", "success"),
                error_message=log_data.get("error_message")
            )

            return {
                "entry_id": entry_id,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/audit/query")
        async def audit_query(
            action: str = None,
            actor: str = None,
            target: str = None,
            level: str = None,
            result: str = None,
            limit: int = 1000
        ):
            """Query audit trail with filters."""
            from .audit_logger import AuditAction, AuditLevel

            action_filter = None
            if action:
                try:
                    action_filter = AuditAction[action.upper()]
                except KeyError:
                    pass

            level_filter = None
            if level:
                try:
                    level_filter = AuditLevel[level.upper()]
                except KeyError:
                    pass

            entries = self.audit_logger.query_entries(
                action=action_filter,
                actor=actor,
                target=target,
                level=level_filter,
                result=result,
                limit=limit
            )

            return {
                "entries": entries,
                "count": len(entries),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/audit/actor/{actor_id}")
        async def get_actor_actions(actor_id: str, limit: int = 100):
            """Get all actions by a specific actor."""
            actions = self.audit_logger.get_actor_actions(actor_id, limit)
            return {
                "actor": actor_id,
                "actions": actions,
                "count": len(actions),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/audit/target/{target_id}")
        async def get_target_history(target_id: str, limit: int = 100):
            """Get change history for a target."""
            history = self.audit_logger.get_target_history(target_id, limit)
            return {
                "target": target_id,
                "history": history,
                "count": len(history),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/audit/critical")
        async def get_critical_actions(hours: int = 24):
            """Get critical actions from last N hours."""
            actions = self.audit_logger.get_critical_actions(hours)
            return {
                "hours": hours,
                "critical_actions": actions,
                "count": len(actions),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/audit/verify")
        async def verify_audit_integrity():
            """Verify audit trail integrity."""
            verification = self.audit_logger.verify_integrity()
            return {
                **verification,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/api/audit/statistics")
        async def audit_statistics():
            """Get audit trail statistics."""
            stats = self.audit_logger.get_statistics()
            return {
                **stats,
                "timestamp": datetime.now().isoformat()
            }

    def start(self):
        """Start service in background thread."""
        if self.running:
            return

        self.running = True

        def run_server():
            uvicorn.run(
                self.app,
                host="0.0.0.0",
                port=self.port,
                log_level="warning"  # Reduce noise
            )

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

        print(f"[{self.bot_id}] [SERVICE] Started on port {self.port}")

    def stop(self):
        """Stop service."""
        self.running = False
        # Note: uvicorn doesn't have easy programmatic shutdown
        # In production, use process management
        print(f"[{self.bot_id}] [SERVICE] Stopped")

    def update_status(self, status: str, task: Optional[str] = None):
        """Update bot status (called by bot task loop)."""
        self.current_status = status
        self.current_task = task

    def check_interrupt(self) -> bool:
        """Check if interrupt was requested. Clears flag after reading."""
        if self.interrupt_requested:
            self.interrupt_requested = False
            return True
        return False

    def check_terminate(self) -> bool:
        """Check if terminate was requested."""
        return self.terminate_requested
