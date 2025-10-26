#!/usr/bin/env python3
"""Distributed Tracing System: Request flow tracking across services.

Features:
- Request/span creation and propagation
- Trace collection and storage
- Service dependency graph
- Latency analysis (p50, p95, p99)
- Error tracking in traces
- Query/visualization support
- Sampling strategies
"""

import json
import uuid
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - DISTRIBUTED-TRACING - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SpanStatus(Enum):
    """Span execution status."""
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class Span:
    """Represents a single span in a trace."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    trace_id: str = ""
    parent_span_id: Optional[str] = None
    operation_name: str = ""
    service_name: str = ""
    status: SpanStatus = SpanStatus.STARTED
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration_ms: float = 0.0
    tags: Dict = field(default_factory=dict)
    logs: List[Dict] = field(default_factory=list)
    error: Optional[str] = None
    error_stack: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = SpanStatus(self.status)

    def finish(self, duration_ms: Optional[float] = None):
        """Mark span as finished."""
        self.end_time = time.time()
        if duration_ms is not None:
            self.duration_ms = duration_ms
        else:
            self.duration_ms = (self.end_time - self.start_time) * 1000
        self.status = SpanStatus.COMPLETED

    def set_error(self, error: str, stack: Optional[str] = None):
        """Mark span as errored."""
        self.error = error
        self.error_stack = stack
        self.status = SpanStatus.ERROR
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000

    def add_log(self, message: str, level: str = "info", **kwargs):
        """Add a log entry to the span."""
        self.logs.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": message,
            "level": level,
            **kwargs
        })

    def add_tag(self, key: str, value):
        """Add a tag to the span."""
        self.tags[key] = value

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['status'] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> 'Span':
        """Create from dictionary."""
        if isinstance(data.get('status'), str):
            data['status'] = SpanStatus(data['status'])
        return cls(**data)


@dataclass
class Trace:
    """Represents a complete trace (request)."""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    root_span_id: str = ""
    service_name: str = ""
    operation_name: str = ""
    status: str = "pending"  # pending, completed, error
    spans: Dict[str, Span] = field(default_factory=dict)
    duration_ms: float = 0.0
    error_count: int = 0

    def finish(self):
        """Mark trace as finished."""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000
        self.error_count = sum(1 for s in self.spans.values() if s.error)
        self.status = "error" if self.error_count > 0 else "completed"

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "trace_id": self.trace_id,
            "root_span_id": self.root_span_id,
            "service_name": self.service_name,
            "operation_name": self.operation_name,
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "error_count": self.error_count,
            "span_count": len(self.spans),
            "spans": [s.to_dict() for s in self.spans.values()]
        }


class DistributedTracer:
    """Core distributed tracing implementation."""

    def __init__(self, service_name: str, project_root: Path = None):
        """Initialize tracer.

        Args:
            service_name: Service name for this tracer
            project_root: Project root for trace storage
        """
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.service_name = service_name
        self.project_root = project_root
        self.traces_dir = project_root / ".deia" / "traces"
        self.traces_dir.mkdir(parents=True, exist_ok=True)

        self.traces_log = self.traces_dir / "traces.jsonl"
        self.spans_log = self.traces_dir / "spans.jsonl"
        self.metrics_log = project_root / ".deia" / "logs" / "tracing-metrics.jsonl"
        self.metrics_log.parent.mkdir(parents=True, exist_ok=True)

        # In-memory structures
        self.traces: Dict[str, Trace] = {}  # trace_id -> Trace
        self.active_spans: Dict[str, Dict[str, Span]] = defaultdict(dict)  # trace_id -> {span_id -> Span}
        self.service_deps: set = set()  # (service_from, service_to) tuples
        self.lock = threading.RLock()

        # Metrics
        self.metrics = {
            "traces_started": 0,
            "spans_created": 0,
            "traces_completed": 0,
            "errors": 0
        }

        logger.info(f"DistributedTracer initialized for service '{service_name}'")

    def start_trace(self, trace_id: Optional[str] = None, operation_name: str = "unknown") -> Trace:
        """Start a new trace (root request).

        Args:
            trace_id: Optional trace ID (generated if not provided)
            operation_name: Name of the operation

        Returns:
            Trace object
        """
        with self.lock:
            if trace_id is None:
                trace_id = str(uuid.uuid4())

            trace = Trace(
                trace_id=trace_id,
                service_name=self.service_name,
                operation_name=operation_name
            )

            # Start root span
            root_span = Span(
                trace_id=trace_id,
                operation_name=operation_name,
                service_name=self.service_name
            )

            trace.root_span_id = root_span.id
            trace.spans[root_span.id] = root_span
            self.active_spans[trace_id][root_span.id] = root_span

            self.traces[trace_id] = trace
            self.metrics["traces_started"] += 1

            logger.info(f"Trace {trace_id} started")
            return trace

    def start_span(self, trace_id: str, operation_name: str, parent_span_id: Optional[str] = None, service_name: Optional[str] = None) -> Span:
        """Start a new span in a trace.

        Args:
            trace_id: Trace ID
            operation_name: Operation name
            parent_span_id: Optional parent span ID
            service_name: Optional service name (default: this service)

        Returns:
            Span object
        """
        with self.lock:
            if trace_id not in self.traces:
                logger.warning(f"Trace {trace_id} not found")
                return None

            if service_name is None:
                service_name = self.service_name

            span = Span(
                trace_id=trace_id,
                operation_name=operation_name,
                service_name=service_name,
                parent_span_id=parent_span_id
            )

            # Track service dependency if different from current
            if parent_span_id and parent_span_id in self.traces[trace_id].spans:
                parent_span = self.traces[trace_id].spans[parent_span_id]
                if parent_span.service_name != service_name:
                    self.service_deps.add((parent_span.service_name, service_name))

            self.traces[trace_id].spans[span.id] = span
            self.active_spans[trace_id][span.id] = span
            self.metrics["spans_created"] += 1

            logger.debug(f"Span {span.id} started in trace {trace_id}")
            return span

    def finish_span(self, trace_id: str, span_id: str, duration_ms: Optional[float] = None, error: Optional[str] = None, error_stack: Optional[str] = None):
        """Finish a span.

        Args:
            trace_id: Trace ID
            span_id: Span ID
            duration_ms: Optional duration override
            error: Optional error message
            error_stack: Optional error stack trace
        """
        with self.lock:
            if trace_id not in self.traces:
                logger.warning(f"Trace {trace_id} not found")
                return

            if span_id not in self.traces[trace_id].spans:
                logger.warning(f"Span {span_id} not found in trace {trace_id}")
                return

            span = self.traces[trace_id].spans[span_id]

            if error:
                span.set_error(error, error_stack)
                self.metrics["errors"] += 1
            else:
                span.finish(duration_ms)

            # Persist span
            self._persist_span(span)

    def finish_trace(self, trace_id: str):
        """Finish a trace.

        Args:
            trace_id: Trace ID
        """
        with self.lock:
            if trace_id not in self.traces:
                logger.warning(f"Trace {trace_id} not found")
                return

            trace = self.traces[trace_id]
            trace.finish()
            self.metrics["traces_completed"] += 1

            # Persist trace
            self._persist_trace(trace)

            logger.info(f"Trace {trace_id} finished (duration: {trace.duration_ms:.2f}ms)")

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get a trace by ID."""
        with self.lock:
            return self.traces.get(trace_id)

    def get_service_dependencies(self) -> List[Tuple[str, str]]:
        """Get service dependency graph.

        Returns:
            List of (from_service, to_service) tuples
        """
        with self.lock:
            return list(self.service_deps)

    def get_latency_stats(self, operation_name: Optional[str] = None) -> Dict:
        """Get latency statistics.

        Args:
            operation_name: Optional filter by operation

        Returns:
            Dict with p50, p95, p99 latencies
        """
        with self.lock:
            durations = []

            for trace in self.traces.values():
                if trace.status == "completed":
                    if operation_name is None or trace.operation_name == operation_name:
                        durations.append(trace.duration_ms)

            if not durations:
                return {"count": 0}

            durations.sort()
            count = len(durations)

            return {
                "count": count,
                "p50": durations[int(count * 0.5)] if count > 0 else 0,
                "p95": durations[int(count * 0.95)] if count > 1 else durations[0],
                "p99": durations[int(count * 0.99)] if count > 1 else durations[0],
                "min": durations[0],
                "max": durations[-1],
                "avg": sum(durations) / len(durations)
            }

    def get_error_traces(self) -> List[Dict]:
        """Get all traces with errors.

        Returns:
            List of error trace info
        """
        with self.lock:
            errors = []
            for trace in self.traces.values():
                if trace.error_count > 0:
                    errors.append({
                        "trace_id": trace.trace_id,
                        "operation": trace.operation_name,
                        "error_count": trace.error_count,
                        "duration_ms": trace.duration_ms,
                        "errors": [
                            {"span_id": s.id, "error": s.error}
                            for s in trace.spans.values() if s.error
                        ]
                    })
            return errors

    def get_metrics(self) -> Dict:
        """Get tracing metrics."""
        with self.lock:
            return {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "metrics": self.metrics.copy(),
                "active_traces": len([t for t in self.traces.values() if t.status == "pending"]),
                "completed_traces": len([t for t in self.traces.values() if t.status == "completed"]),
                "error_traces": len([t for t in self.traces.values() if t.error_count > 0]),
                "services_in_dep_graph": len(set(list(zip(*self.service_deps))[0] if self.service_deps else []))
            }

    def _persist_trace(self, trace: Trace):
        """Persist trace to log."""
        try:
            with open(self.traces_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(trace.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist trace: {e}")

    def _persist_span(self, span: Span):
        """Persist span to log."""
        try:
            with open(self.spans_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(span.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist span: {e}")


class TracingService:
    """High-level tracing service for applications."""

    def __init__(self, service_name: str, project_root: Path = None):
        """Initialize tracing service."""
        self.tracer = DistributedTracer(service_name, project_root)

    def start_request(self, operation_name: str, trace_id: Optional[str] = None) -> Trace:
        """Start tracing a request."""
        return self.tracer.start_trace(trace_id, operation_name)

    def start_operation(self, trace_id: str, operation_name: str, parent_span_id: Optional[str] = None) -> Span:
        """Start tracing an operation within a request."""
        return self.tracer.start_span(trace_id, operation_name, parent_span_id)

    def finish_operation(self, trace_id: str, span_id: str, duration_ms: Optional[float] = None, error: Optional[str] = None, error_stack: Optional[str] = None):
        """Finish tracing an operation."""
        self.tracer.finish_span(trace_id, span_id, duration_ms, error, error_stack)

    def finish_request(self, trace_id: str):
        """Finish tracing a request."""
        self.tracer.finish_trace(trace_id)

    def get_trace(self, trace_id: str) -> Optional[Dict]:
        """Get trace details."""
        trace = self.tracer.get_trace(trace_id)
        return trace.to_dict() if trace else None

    def get_service_graph(self) -> List[Tuple[str, str]]:
        """Get service dependency graph."""
        return self.tracer.get_service_dependencies()

    def get_latencies(self, operation: Optional[str] = None) -> Dict:
        """Get latency statistics."""
        return self.tracer.get_latency_stats(operation)

    def get_errors(self) -> List[Dict]:
        """Get error traces."""
        return self.tracer.get_error_traces()

    def status(self) -> Dict:
        """Get tracing system status."""
        return self.tracer.get_metrics()
