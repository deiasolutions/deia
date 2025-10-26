"""
Workflow Orchestration Engine - DAG-based workflow execution with branching, error handling, parallelism.

Defines and executes multi-step workflows with dependencies, conditional branching,
error handling/retries, state management, monitoring, and parallel execution.
"""

from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import uuid
import time
import threading
from datetime import datetime, timedelta
import logging
import json
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


# ===== ENUMS =====

class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    SKIPPED = "skipped"


class WorkflowStatus(str, Enum):
    """Workflow execution status."""
    CREATED = "created"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BranchCondition(str, Enum):
    """Branch conditions."""
    IF_SUCCESS = "if_success"
    IF_FAILED = "if_failed"
    IF_SKIPPED = "if_skipped"
    ALWAYS = "always"


# ===== DATA STRUCTURES =====

@dataclass
class TaskDefinition:
    """Definition of a single task in workflow."""
    task_id: str
    name: str
    handler: Callable[[Dict[str, Any]], Any]
    depends_on: List[str] = field(default_factory=list)
    retries: int = 0
    timeout: Optional[float] = None
    condition: Optional[Callable[[Dict[str, Any]], bool]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskExecution:
    """Execution record for a task."""
    task_id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    attempts: int = 0
    outputs: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> Optional[float]:
        """Get execution duration."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


@dataclass
class WorkflowDefinition:
    """Complete workflow definition."""
    workflow_id: str
    name: str
    description: str = ""
    tasks: Dict[str, TaskDefinition] = field(default_factory=dict)
    start_task: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExecution:
    """Execution record for a workflow."""
    workflow_id: str
    execution_id: str
    name: str
    status: WorkflowStatus = WorkflowStatus.CREATED
    tasks: Dict[str, TaskExecution] = field(default_factory=dict)
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    outputs: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> Optional[float]:
        """Get total duration."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    @property
    def is_complete(self) -> bool:
        """Check if workflow is complete."""
        return self.status in [WorkflowStatus.SUCCESS, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED]


# ===== WORKFLOW BUILDER =====

class WorkflowBuilder:
    """Build workflows fluently."""

    def __init__(self, workflow_id: str = None, name: str = ""):
        """Initialize builder."""
        self.workflow_id = workflow_id or str(uuid.uuid4())
        self.name = name
        self.description = ""
        self.tasks: Dict[str, TaskDefinition] = {}
        self.start_task = None

    def with_description(self, description: str) -> "WorkflowBuilder":
        """Add description."""
        self.description = description
        return self

    def add_task(self, task_id: str, name: str, handler: Callable, depends_on: List[str] = None,
                 retries: int = 0, timeout: Optional[float] = None,
                 condition: Optional[Callable] = None) -> "WorkflowBuilder":
        """Add task to workflow."""
        self.tasks[task_id] = TaskDefinition(
            task_id=task_id,
            name=name,
            handler=handler,
            depends_on=depends_on or [],
            retries=retries,
            timeout=timeout,
            condition=condition
        )

        if self.start_task is None:
            self.start_task = task_id

        return self

    def set_start_task(self, task_id: str) -> "WorkflowBuilder":
        """Set starting task."""
        self.start_task = task_id
        return self

    def build(self) -> WorkflowDefinition:
        """Build workflow."""
        return WorkflowDefinition(
            workflow_id=self.workflow_id,
            name=self.name,
            description=self.description,
            tasks=self.tasks,
            start_task=self.start_task
        )


# ===== EXECUTION ENGINE =====

class WorkflowExecutor:
    """Execute workflows with state management."""

    def __init__(self, max_workers: int = 4):
        """Initialize executor."""
        self.max_workers = max_workers
        self.lock = threading.RLock()
        self.executions: Dict[str, WorkflowExecution] = {}

    def execute(self, workflow: WorkflowDefinition) -> WorkflowExecution:
        """Execute workflow."""
        execution = WorkflowExecution(
            workflow_id=workflow.workflow_id,
            execution_id=str(uuid.uuid4()),
            name=workflow.name
        )

        with self.lock:
            self.executions[execution.execution_id] = execution

        execution.start_time = time.time()
        execution.status = WorkflowStatus.RUNNING

        try:
            self._execute_tasks(workflow, execution)

            if any(t.status == TaskStatus.FAILED for t in execution.tasks.values()):
                execution.status = WorkflowStatus.FAILED
            else:
                execution.status = WorkflowStatus.SUCCESS

        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.errors.append(str(e))

        execution.end_time = time.time()
        return execution

    def _execute_tasks(self, workflow: WorkflowDefinition, execution: WorkflowExecution) -> None:
        """Execute tasks with dependency ordering."""
        executed = set()
        ready_queue = deque()

        # Find all starting tasks (no dependencies or dependencies in ready_queue)
        if workflow.start_task and workflow.start_task in workflow.tasks:
            ready_queue.append(workflow.start_task)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}

            while ready_queue or futures:
                # Submit ready tasks
                while ready_queue:
                    task_id = ready_queue.popleft()

                    if task_id in executed:
                        continue

                    task_def = workflow.tasks[task_id]
                    task_exec = TaskExecution(task_id=task_id, name=task_def.name)
                    execution.tasks[task_id] = task_exec

                    # Check if dependencies are ready
                    if all(dep in executed for dep in task_def.depends_on):
                        future = executor.submit(
                            self._execute_task,
                            task_def,
                            task_exec,
                            execution
                        )
                        futures[future] = task_id

                # Wait for at least one task to complete
                if futures:
                    done_futures, _ = next(iter([as_completed(futures, timeout=1)]))

                    for future in done_futures:
                        task_id = futures.pop(future)
                        executed.add(task_id)

                        # Find next ready tasks
                        for other_task_id, other_task in workflow.tasks.items():
                            if other_task_id not in executed and task_id in other_task.depends_on:
                                ready_queue.append(other_task_id)

    def _execute_task(self, task_def: TaskDefinition, task_exec: TaskExecution,
                      execution: WorkflowExecution) -> None:
        """Execute single task with retry logic."""
        task_exec.status = TaskStatus.RUNNING
        task_exec.start_time = time.time()

        for attempt in range(task_def.retries + 1):
            try:
                task_exec.attempts = attempt + 1

                if task_def.condition:
                    if not task_def.condition(execution.outputs):
                        task_exec.status = TaskStatus.SKIPPED
                        task_exec.end_time = time.time()
                        return

                # Get dependencies outputs
                context = {dep: execution.tasks[dep].result for dep in task_def.depends_on}

                # Execute with timeout
                if task_def.timeout:
                    import signal

                    def timeout_handler(signum, frame):
                        raise TimeoutError(f"Task {task_def.task_id} timeout")

                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(int(task_def.timeout))

                result = task_def.handler(context)

                if task_def.timeout:
                    signal.alarm(0)

                task_exec.result = result
                task_exec.status = TaskStatus.SUCCESS
                execution.outputs[task_def.task_id] = result

                task_exec.end_time = time.time()
                return

            except Exception as e:
                if attempt < task_def.retries:
                    task_exec.status = TaskStatus.RETRYING
                    time.sleep(1)  # Backoff
                else:
                    task_exec.status = TaskStatus.FAILED
                    task_exec.error = str(e)
                    execution.errors.append(f"{task_def.task_id}: {str(e)}")
                    task_exec.end_time = time.time()
                    return

    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get execution by ID."""
        with self.lock:
            return self.executions.get(execution_id)

    def get_status(self, execution_id: str) -> Optional[WorkflowStatus]:
        """Get execution status."""
        execution = self.get_execution(execution_id)
        return execution.status if execution else None

    def cancel_execution(self, execution_id: str) -> None:
        """Cancel execution."""
        execution = self.get_execution(execution_id)
        if execution:
            execution.status = WorkflowStatus.CANCELLED


# ===== STATE MANAGEMENT =====

class WorkflowState:
    """Manage workflow state persistence."""

    def __init__(self):
        """Initialize state manager."""
        self.state: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.RLock()

    def save_state(self, execution_id: str, state: Dict[str, Any]) -> None:
        """Save execution state."""
        with self.lock:
            self.state[execution_id] = state.copy()

    def get_state(self, execution_id: str) -> Dict[str, Any]:
        """Get execution state."""
        with self.lock:
            return self.state.get(execution_id, {}).copy()

    def to_json(self, execution: WorkflowExecution) -> str:
        """Serialize execution to JSON."""
        data = {
            "workflow_id": execution.workflow_id,
            "execution_id": execution.execution_id,
            "name": execution.name,
            "status": execution.status.value,
            "duration": execution.duration,
            "tasks": {
                task_id: {
                    "status": task.status.value,
                    "duration": task.duration,
                    "attempts": task.attempts,
                    "error": task.error
                }
                for task_id, task in execution.tasks.items()
            }
        }
        return json.dumps(data, indent=2)


# ===== MONITORING =====

class WorkflowMonitor:
    """Monitor workflow execution."""

    def __init__(self):
        """Initialize monitor."""
        self.executions: List[WorkflowExecution] = []
        self.lock = threading.RLock()

    def record_execution(self, execution: WorkflowExecution) -> None:
        """Record completed execution."""
        with self.lock:
            self.executions.append(execution)

    def get_success_rate(self) -> float:
        """Get success rate."""
        with self.lock:
            if not self.executions:
                return 0.0
            successful = sum(1 for e in self.executions if e.status == WorkflowStatus.SUCCESS)
            return successful / len(self.executions)

    def get_average_duration(self) -> float:
        """Get average execution duration."""
        with self.lock:
            if not self.executions:
                return 0.0
            total_duration = sum(e.duration for e in self.executions if e.duration)
            return total_duration / len(self.executions)

    def get_task_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Get task-level statistics."""
        stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "executions": 0, "successes": 0, "failures": 0, "avg_duration": 0.0
        })

        with self.lock:
            for execution in self.executions:
                for task_id, task in execution.tasks.items():
                    s = stats[task_id]
                    s["executions"] += 1
                    if task.status == TaskStatus.SUCCESS:
                        s["successes"] += 1
                    elif task.status == TaskStatus.FAILED:
                        s["failures"] += 1
                    if task.duration:
                        s["avg_duration"] = (s["avg_duration"] + task.duration) / 2

        return stats

    def get_report(self) -> str:
        """Generate execution report."""
        with self.lock:
            total = len(self.executions)
            successful = sum(1 for e in self.executions if e.status == WorkflowStatus.SUCCESS)
            failed = sum(1 for e in self.executions if e.status == WorkflowStatus.FAILED)

            report = f"""
Workflow Execution Report
========================
Total Executions: {total}
Successful: {successful}
Failed: {failed}
Success Rate: {self.get_success_rate():.1%}
Average Duration: {self.get_average_duration():.2f}s
"""
            return report
