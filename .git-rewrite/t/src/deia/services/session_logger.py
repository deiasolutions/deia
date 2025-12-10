import json
import logging
import os
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TaskEvent:
    name: str
    start_time: float
    end_time: Optional[float] = None
    metadata: Dict = field(default_factory=dict)

@dataclass
class FileEvent:
    path: str
    operation: str
    size_bytes: Optional[int] = None
    lines: Optional[int] = None

@dataclass
class ToolEvent:
    name: str
    params: Dict
    duration_ms: int

@dataclass
class SessionSummary:
    total_duration_ms: int
    tasks_completed: int
    files_read: int
    files_written: int
    tool_calls_count: int
    velocity: float

@dataclass
class SessionAnalysis:
    task_breakdown: Dict[str, int]
    bottlenecks: List[str]
    velocity_metrics: Dict[str, float]
    file_operation_stats: Dict[str, int]

class SessionLogger:
    def __init__(self, agent_id: str, session_id: str = None):
        self.agent_id = agent_id
        self.session_id = session_id or str(uuid.uuid4())
        self.start_time = time.time()
        self.events = []

    def log_task_start(self, task_name: str, metadata: dict = None):
        event = TaskEvent(name=task_name, start_time=time.time(), metadata=metadata or {})
        self.events.append(event)

    def log_task_complete(self, task_name: str, duration_ms: int, metadata: dict = None):
        event = next((e for e in reversed(self.events) if isinstance(e, TaskEvent) and e.name == task_name and e.end_time is None), None)
        if event:
            event.end_time = time.time()
            event.metadata.update(metadata or {})
        else:
            logger.warning(f"Task complete event logged without corresponding start event: {task_name}")

    def log_file_read(self, path: str, size_bytes: int = None):
        event = FileEvent(path=path, operation="read", size_bytes=size_bytes)
        self.events.append(event)

    def log_file_write(self, path: str, size_bytes: int, lines: int = None):
        event = FileEvent(path=path, operation="write", size_bytes=size_bytes, lines=lines)
        self.events.append(event)

    def log_tool_call(self, tool_name: str, params: dict, duration_ms: int):
        event = ToolEvent(name=tool_name, params=params, duration_ms=duration_ms)
        self.events.append(event)

    def get_session_summary(self) -> SessionSummary:
        end_time = time.time()
        total_duration_ms = int((end_time - self.start_time) * 1000)
        tasks_completed = sum(1 for e in self.events if isinstance(e, TaskEvent) and e.end_time is not None)
        files_read = sum(1 for e in self.events if isinstance(e, FileEvent) and e.operation == "read")
        files_written = sum(1 for e in self.events if isinstance(e, FileEvent) and e.operation == "write")
        tool_calls_count = sum(1 for e in self.events if isinstance(e, ToolEvent))

        # Avoid division by zero for very short sessions
        if total_duration_ms > 0:
            velocity = tasks_completed / (total_duration_ms / 3600000)  # Tasks per hour
        else:
            velocity = 0.0

        return SessionSummary(
            total_duration_ms=total_duration_ms,
            tasks_completed=tasks_completed,
            files_read=files_read,
            files_written=files_written,
            tool_calls_count=tool_calls_count,
            velocity=velocity
        )

    def analyze_session(self, session_path: str) -> SessionAnalysis:
        with open(session_path, "r") as f:
            events = [json.loads(line) for line in f]

        task_durations = defaultdict(int)
        file_operations = defaultdict(int)
        tool_calls = defaultdict(int)

        for event in events:
            if event["type"] == "TaskEvent":
                if event["end_time"]:
                    duration = int((event["end_time"] - event["start_time"]) * 1000)
                    task_durations[event["name"]] += duration
            elif event["type"] == "FileEvent":
                file_operations[event["operation"]] += 1
            elif event["type"] == "ToolEvent":
                tool_calls[event["name"]] += 1

        total_duration = sum(task_durations.values())
        bottlenecks = [task for task, duration in task_durations.items() if duration > total_duration * 0.3]

        # Avoid division by zero for very short or empty sessions
        if total_duration > 0:
            velocity_metrics = {
                "tasks_per_hour": len(task_durations) / (total_duration / 3600000),
                "files_read_per_hour": file_operations["read"] / (total_duration / 3600000),
                "files_written_per_hour": file_operations["write"] / (total_duration / 3600000),
                "tool_calls_per_hour": sum(tool_calls.values()) / (total_duration / 3600000),
            }
        else:
            velocity_metrics = {
                "tasks_per_hour": 0.0,
                "files_read_per_hour": 0.0,
                "files_written_per_hour": 0.0,
                "tool_calls_per_hour": 0.0,
            }

        return SessionAnalysis(
            task_breakdown=dict(task_durations),
            bottlenecks=bottlenecks,
            velocity_metrics=velocity_metrics,
            file_operation_stats=dict(file_operations)
        )

    def save_session(self, output_dir: str):
        session_file = f"{self.agent_id}_{self.session_id}.jsonl"
        session_path = os.path.join(output_dir, session_file)

        with open(session_path, "w") as f:
            for event in self.events:
                f.write(json.dumps(vars(event)) + "\n")

        logger.info(f"Session log saved to {session_path}")

# Usage example
if __name__ == "__main__":
    logger = SessionLogger(agent_id="ClaudeCode")

    logger.log_task_start("Implement search function")
    logger.log_file_read("search.py", size_bytes=2048)
    logger.log_tool_call("repl", params={"command": "test_search()"}, duration_ms=500)
    logger.log_file_write("search.py", size_bytes=4096, lines=100)
    logger.log_task_complete("Implement search function", duration_ms=300000)  # 5 minutes

    logger.log_task_start("Optimize search performance")
    logger.log_file_read("search.py", size_bytes=4096)
    logger.log_tool_call("profiler", params={"function": "search"}, duration_ms=1000)
    logger.log_file_write("search.py", size_bytes=4096, lines=120)
    logger.log_task_complete("Optimize search performance", duration_ms=600000)  # 10 minutes

    session_summary = logger.get_session_summary()
    print("Session Summary:")
    print(session_summary)

    logger.save_session("sessions")
    session_analysis = logger.analyze_session("sessions/ClaudeCode_session.jsonl")
    print("\nSession Analysis:")
    print(session_analysis)
