"""
Task Graph Builder - Convert specs into executable task graphs.

Features:
- Dependency resolution
- Topological sorting for execution order
- Circular dependency detection
- Task status tracking
- Task file creation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from pathlib import Path
from datetime import datetime
import json

from deia_raqcoon.core.task_files import write_task


@dataclass
class TaskNode:
    """A node in the task graph representing a single task."""
    task_id: str
    title: str
    intent: str
    summary: str = ""
    depends_on: List[str] = field(default_factory=list)
    assignee: Optional[str] = None
    files: List[str] = field(default_factory=list)
    priority: str = "P1"
    status: str = "pending"  # pending, ready, in_progress, complete, blocked

    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "intent": self.intent,
            "summary": self.summary,
            "depends_on": self.depends_on,
            "assignee": self.assignee,
            "files": self.files,
            "priority": self.priority,
            "status": self.status,
        }


@dataclass
class TaskGraph:
    """
    A directed acyclic graph of tasks with dependency tracking.
    """
    spec_id: str
    title: str
    nodes: Dict[str, TaskNode] = field(default_factory=dict)
    execution_order: List[str] = field(default_factory=list)

    def get_ready_tasks(self) -> List[TaskNode]:
        """
        Return tasks that are ready to execute.
        A task is ready if:
        - Status is 'pending' or 'ready'
        - All dependencies are 'complete'
        """
        ready = []
        for task_id, node in self.nodes.items():
            if node.status not in ('pending', 'ready'):
                continue
            deps_complete = all(
                self.nodes[dep].status == 'complete'
                for dep in node.depends_on
                if dep in self.nodes
            )
            if deps_complete:
                ready.append(node)
        return ready

    def mark_complete(self, task_id: str) -> List[str]:
        """
        Mark a task as complete and return newly unblocked task IDs.
        """
        if task_id not in self.nodes:
            return []

        self.nodes[task_id].status = 'complete'

        # Find tasks that were waiting on this one
        newly_ready = []
        for tid, node in self.nodes.items():
            if node.status != 'pending':
                continue
            if task_id in node.depends_on:
                # Check if all deps now complete
                all_complete = all(
                    self.nodes[d].status == 'complete'
                    for d in node.depends_on
                    if d in self.nodes
                )
                if all_complete:
                    node.status = 'ready'
                    newly_ready.append(tid)

        return newly_ready

    def mark_in_progress(self, task_id: str) -> bool:
        """Mark a task as in progress."""
        if task_id in self.nodes:
            self.nodes[task_id].status = 'in_progress'
            return True
        return False

    def mark_blocked(self, task_id: str) -> bool:
        """Mark a task as blocked."""
        if task_id in self.nodes:
            self.nodes[task_id].status = 'blocked'
            return True
        return False

    def get_parallel_groups(self) -> List[List[str]]:
        """
        Return groups of tasks that can run in parallel.
        Each group contains tasks at the same "depth" in the graph.
        """
        if not self.execution_order:
            return []

        # Calculate depth for each task
        depths: Dict[str, int] = {}
        for task_id in self.execution_order:
            node = self.nodes[task_id]
            if not node.depends_on:
                depths[task_id] = 0
            else:
                max_dep_depth = max(
                    depths.get(d, 0) for d in node.depends_on
                    if d in self.nodes
                )
                depths[task_id] = max_dep_depth + 1

        # Group by depth
        max_depth = max(depths.values()) if depths else 0
        groups = [[] for _ in range(max_depth + 1)]
        for task_id, depth in depths.items():
            groups[depth].append(task_id)

        return groups

    def to_dict(self) -> Dict:
        """Serialize entire graph."""
        return {
            "spec_id": self.spec_id,
            "title": self.title,
            "nodes": {tid: node.to_dict() for tid, node in self.nodes.items()},
            "execution_order": self.execution_order,
            "parallel_groups": self.get_parallel_groups(),
        }


def _topological_sort(nodes: Dict[str, TaskNode]) -> List[str]:
    """
    Topological sort using Kahn's algorithm.
    Raises ValueError if circular dependency detected.
    """
    # Build adjacency and in-degree
    in_degree: Dict[str, int] = {tid: 0 for tid in nodes}
    for tid, node in nodes.items():
        for dep in node.depends_on:
            if dep in nodes:
                in_degree[tid] += 1

    # Start with nodes that have no dependencies
    queue = [tid for tid, deg in in_degree.items() if deg == 0]
    result = []

    while queue:
        # Sort to ensure deterministic order
        queue.sort()
        current = queue.pop(0)
        result.append(current)

        # Reduce in-degree for dependent tasks
        for tid, node in nodes.items():
            if current in node.depends_on:
                in_degree[tid] -= 1
                if in_degree[tid] == 0:
                    queue.append(tid)

    # Check for circular dependency
    if len(result) != len(nodes):
        remaining = set(nodes.keys()) - set(result)
        raise ValueError(f"Circular dependency detected involving: {remaining}")

    return result


def build_task_graph(spec: Dict) -> TaskGraph:
    """
    Build a task graph from a parsed spec.

    Args:
        spec: Parsed spec dictionary

    Returns:
        TaskGraph with nodes and execution order

    Raises:
        ValueError: If circular dependency detected
    """
    graph = TaskGraph(
        spec_id=spec.get('spec_id', 'UNKNOWN'),
        title=spec.get('title', 'Untitled Spec')
    )

    # Create nodes from spec tasks
    for task_data in spec.get('tasks', []):
        node = TaskNode(
            task_id=task_data.get('task_id'),
            title=task_data.get('title', ''),
            intent=task_data.get('intent', 'code'),
            summary=task_data.get('summary', ''),
            depends_on=task_data.get('depends_on', []),
            assignee=task_data.get('assignee'),
            files=task_data.get('files', []),
            priority=task_data.get('priority', 'P1'),
            status='pending'
        )
        graph.nodes[node.task_id] = node

    # Compute execution order
    graph.execution_order = _topological_sort(graph.nodes)

    # Mark tasks with no dependencies as ready
    for task_id in graph.execution_order:
        node = graph.nodes[task_id]
        if not node.depends_on:
            node.status = 'ready'

    return graph


def create_task_files(
    graph: TaskGraph,
    repo_root: Path,
    flight_id: Optional[str] = None,
    default_assignee: Optional[str] = None,
) -> List[Path]:
    """
    Create actual task files from the graph.

    Args:
        graph: Built task graph
        repo_root: Repository root path
        flight_id: Optional flight to associate tasks with
        default_assignee: Default bot_id if task has no assignee

    Returns:
        List of created task file paths
    """
    created_paths = []

    for task_id in graph.execution_order:
        node = graph.nodes[task_id]
        assignee = node.assignee or default_assignee or "UNASSIGNED"

        payload = {
            "task_id": node.task_id,
            "intent": node.intent,
            "title": node.title,
            "summary": node.summary,
            "kb_entities": [],
            "delivery": {"mode": "task_file"},
            "spec_id": graph.spec_id,
            "depends_on": node.depends_on,
            "files": node.files,
            "priority": node.priority,
        }

        if flight_id:
            payload["flight_id"] = flight_id

        path = write_task(repo_root, assignee, payload)
        created_paths.append(path)

    return created_paths


# For testing
if __name__ == "__main__":
    # Test with example spec
    example_spec = {
        "spec_id": "SPEC-TEST-001",
        "title": "Test Specification",
        "tasks": [
            {"task_id": "TASK-001", "title": "First", "intent": "code", "depends_on": []},
            {"task_id": "TASK-002", "title": "Second", "intent": "code", "depends_on": ["TASK-001"]},
            {"task_id": "TASK-003", "title": "Third", "intent": "test", "depends_on": ["TASK-001"]},
            {"task_id": "TASK-004", "title": "Fourth", "intent": "code", "depends_on": ["TASK-002", "TASK-003"]},
        ]
    }

    graph = build_task_graph(example_spec)
    print("Execution order:", graph.execution_order)
    print("Parallel groups:", graph.get_parallel_groups())
    print("Ready tasks:", [t.task_id for t in graph.get_ready_tasks()])

    # Test marking complete
    print("\nMarking TASK-001 complete...")
    newly_ready = graph.mark_complete("TASK-001")
    print("Newly ready:", newly_ready)
    print("Ready tasks:", [t.task_id for t in graph.get_ready_tasks()])

    # Test circular dependency detection
    print("\nTesting circular dependency detection...")
    circular_spec = {
        "spec_id": "SPEC-CIRCULAR",
        "title": "Circular Test",
        "tasks": [
            {"task_id": "A", "title": "A", "intent": "code", "depends_on": ["B"]},
            {"task_id": "B", "title": "B", "intent": "code", "depends_on": ["C"]},
            {"task_id": "C", "title": "C", "intent": "code", "depends_on": ["A"]},
        ]
    }
    try:
        build_task_graph(circular_spec)
        print("ERROR: Should have detected circular dependency!")
    except ValueError as e:
        print(f"Correctly detected: {e}")
