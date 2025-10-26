#!/usr/bin/env python3
"""Tests for Distributed Tracing System."""

import pytest
import tempfile
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.distributed_tracing import (
    Span,
    SpanStatus,
    Trace,
    DistributedTracer,
    TracingService
)


class TestSpan:
    """Test span data structure."""

    def test_create_span(self):
        """Test creating a span."""
        span = Span(
            trace_id="trace-123",
            operation_name="api_call",
            service_name="api-service"
        )

        assert span.trace_id == "trace-123"
        assert span.operation_name == "api_call"
        assert span.service_name == "api-service"
        assert span.status == SpanStatus.STARTED

    def test_span_finish(self):
        """Test finishing a span."""
        span = Span(
            trace_id="trace-123",
            operation_name="test"
        )

        span.finish(100)
        assert span.status == SpanStatus.COMPLETED
        assert span.duration_ms == 100
        assert span.end_time is not None

    def test_span_error(self):
        """Test marking span with error."""
        span = Span(
            trace_id="trace-123",
            operation_name="test"
        )

        span.set_error("Database connection failed", "connection error stack")
        assert span.status == SpanStatus.ERROR
        assert span.error == "Database connection failed"
        assert span.error_stack is not None

    def test_span_tags(self):
        """Test adding tags to span."""
        span = Span(trace_id="trace-123", operation_name="test")

        span.add_tag("http.method", "GET")
        span.add_tag("http.status", 200)

        assert span.tags["http.method"] == "GET"
        assert span.tags["http.status"] == 200

    def test_span_logs(self):
        """Test adding logs to span."""
        span = Span(trace_id="trace-123", operation_name="test")

        span.add_log("Processing request", level="info")
        span.add_log("Cache hit", level="debug")

        assert len(span.logs) == 2
        assert span.logs[0]["message"] == "Processing request"

    def test_span_serialization(self):
        """Test span serialization."""
        span = Span(trace_id="trace-123", operation_name="test")
        span.add_tag("key", "value")

        data = span.to_dict()
        assert data["trace_id"] == "trace-123"
        assert data["status"] == "started"

        span2 = Span.from_dict(data)
        assert span2.trace_id == span.trace_id


class TestTrace:
    """Test trace data structure."""

    def test_create_trace(self):
        """Test creating a trace."""
        trace = Trace(
            service_name="api-service",
            operation_name="POST /orders"
        )

        assert trace.service_name == "api-service"
        assert trace.operation_name == "POST /orders"
        assert trace.status == "pending"

    def test_trace_finish(self):
        """Test finishing a trace."""
        trace = Trace()
        trace.finish()

        assert trace.status == "completed"
        assert trace.duration_ms > 0
        assert trace.end_time is not None

    def test_trace_with_spans(self):
        """Test trace with spans."""
        trace = Trace()
        span = Span(trace_id=trace.trace_id, operation_name="op1")
        trace.spans[span.id] = span

        assert len(trace.spans) == 1
        assert trace.spans[span.id].operation_name == "op1"

    def test_trace_error_tracking(self):
        """Test error counting in trace."""
        trace = Trace()

        span1 = Span(trace_id=trace.trace_id, operation_name="op1")
        span2 = Span(trace_id=trace.trace_id, operation_name="op2")

        span1.set_error("Error in op1")
        span2.finish(100)

        trace.spans[span1.id] = span1
        trace.spans[span2.id] = span2
        trace.finish()

        assert trace.error_count == 1


class TestDistributedTracer:
    """Test distributed tracer."""

    @pytest.fixture
    def tracer(self):
        """Create tracer for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            tracer = DistributedTracer("test-service", project_root)
            yield tracer, project_root

    def test_tracer_initialization(self, tracer):
        """Test tracer initialization."""
        t, _ = tracer
        assert t.service_name == "test-service"

    def test_start_trace(self, tracer):
        """Test starting a trace."""
        t, _ = tracer

        trace = t.start_trace(operation_name="test_op")
        assert trace.trace_id is not None
        assert trace.operation_name == "test_op"
        assert len(trace.spans) == 1  # Root span

    def test_start_span(self, tracer):
        """Test starting a span in trace."""
        t, _ = tracer

        trace = t.start_trace()
        span = t.start_span(trace.trace_id, "nested_op")

        assert span is not None
        assert len(trace.spans) == 2

    def test_finish_span(self, tracer):
        """Test finishing a span."""
        t, _ = tracer

        trace = t.start_trace()
        span = t.start_span(trace.trace_id, "op")

        t.finish_span(trace.trace_id, span.id, duration_ms=50)

        assert span.status == SpanStatus.COMPLETED
        assert span.duration_ms == 50

    def test_span_with_error(self, tracer):
        """Test span with error."""
        t, _ = tracer

        trace = t.start_trace()
        span = t.start_span(trace.trace_id, "failing_op")

        t.finish_span(trace.trace_id, span.id, error="Operation failed")

        assert span.status == SpanStatus.ERROR
        assert span.error == "Operation failed"

    def test_finish_trace(self, tracer):
        """Test finishing trace."""
        t, _ = tracer

        trace = t.start_trace()
        span = t.start_span(trace.trace_id, "op")
        t.finish_span(trace.trace_id, span.id, duration_ms=100)

        t.finish_trace(trace.trace_id)

        assert trace.status == "completed"
        assert trace.duration_ms > 0

    def test_service_dependency_tracking(self, tracer):
        """Test tracking service dependencies."""
        t, _ = tracer

        trace = t.start_trace()
        root_span = list(trace.spans.values())[0]

        # Start span from different service
        span = Span(
            trace_id=trace.trace_id,
            operation_name="remote_op",
            service_name="remote-service",
            parent_span_id=root_span.id
        )

        trace.spans[span.id] = span
        t.active_spans[trace.trace_id][span.id] = span
        t.service_deps.add(("test-service", "remote-service"))

        deps = t.get_service_dependencies()
        assert ("test-service", "remote-service") in deps

    def test_get_trace(self, tracer):
        """Test retrieving a trace."""
        t, _ = tracer

        trace = t.start_trace(operation_name="get_test")
        retrieved = t.get_trace(trace.trace_id)

        assert retrieved is not None
        assert retrieved.operation_name == "get_test"

    def test_latency_stats_single(self, tracer):
        """Test latency stats with single trace."""
        t, _ = tracer

        trace = t.start_trace()
        t.finish_trace(trace.trace_id)

        stats = t.get_latency_stats()

        assert stats["count"] == 1
        assert stats["min"] > 0
        assert stats["max"] > 0

    def test_latency_stats_multiple(self, tracer):
        """Test latency stats with multiple traces."""
        t, _ = tracer

        for i in range(10):
            trace = t.start_trace()
            time.sleep(0.01)  # Add some delay
            t.finish_trace(trace.trace_id)

        stats = t.get_latency_stats()

        assert stats["count"] == 10
        assert stats["p50"] > 0
        assert stats["p95"] >= stats["p50"]
        assert stats["p99"] >= stats["p95"]

    def test_latency_stats_by_operation(self, tracer):
        """Test latency stats filtered by operation."""
        t, _ = tracer

        trace1 = t.start_trace(operation_name="op_a")
        t.finish_trace(trace1.trace_id)

        trace2 = t.start_trace(operation_name="op_b")
        t.finish_trace(trace2.trace_id)

        stats_a = t.get_latency_stats(operation_name="op_a")
        stats_b = t.get_latency_stats(operation_name="op_b")

        assert stats_a["count"] == 1
        assert stats_b["count"] == 1

    def test_error_traces(self, tracer):
        """Test getting error traces."""
        t, _ = tracer

        # Success trace
        trace1 = t.start_trace(operation_name="success")
        t.finish_trace(trace1.trace_id)

        # Error trace
        trace2 = t.start_trace(operation_name="failure")
        span = t.start_span(trace2.trace_id, "failing_op")
        t.finish_span(trace2.trace_id, span.id, error="Failed")
        t.finish_trace(trace2.trace_id)

        errors = t.get_error_traces()

        assert len(errors) == 1
        assert errors[0]["trace_id"] == trace2.trace_id
        assert errors[0]["error_count"] > 0

    def test_get_metrics(self, tracer):
        """Test getting tracing metrics."""
        t, _ = tracer

        trace = t.start_trace()
        t.start_span(trace.trace_id, "op")
        t.finish_trace(trace.trace_id)

        metrics = t.get_metrics()

        assert metrics["metrics"]["traces_started"] == 1
        assert metrics["metrics"]["traces_completed"] == 1
        assert metrics["metrics"]["spans_created"] == 1

    def test_trace_persistence(self, tracer):
        """Test trace persistence to file."""
        t, project_root = tracer

        trace = t.start_trace(operation_name="persist_test")
        t.finish_trace(trace.trace_id)

        traces_log = project_root / ".deia" / "traces" / "traces.jsonl"
        assert traces_log.exists()

    def test_span_persistence(self, tracer):
        """Test span persistence to file."""
        t, project_root = tracer

        trace = t.start_trace()
        span = t.start_span(trace.trace_id, "span_test")
        t.finish_span(trace.trace_id, span.id, duration_ms=50)

        spans_log = project_root / ".deia" / "traces" / "spans.jsonl"
        assert spans_log.exists()


class TestTracingService:
    """Test high-level tracing service."""

    @pytest.fixture
    def service(self):
        """Create tracing service."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            service = TracingService("api-service", project_root)
            yield service

    def test_start_request(self, service):
        """Test starting a request."""
        trace = service.start_request("POST /orders")
        assert trace is not None
        assert trace.operation_name == "POST /orders"

    def test_full_request_trace(self, service):
        """Test full request tracing workflow."""
        # Start request
        trace = service.start_request("GET /users")

        # Do operations
        op1 = service.start_operation(trace.trace_id, "fetch_db")
        time.sleep(0.01)
        service.finish_operation(trace.trace_id, op1.id, duration_ms=15)

        op2 = service.start_operation(trace.trace_id, "format_response")
        service.finish_operation(trace.trace_id, op2.id, duration_ms=5)

        # Finish request
        service.finish_request(trace.trace_id)

        # Verify
        result = service.get_trace(trace.trace_id)
        assert result is not None
        assert result["span_count"] == 3  # Root + 2 operations

    def test_error_handling(self, service):
        """Test error handling in traces."""
        trace = service.start_request("POST /orders", trace_id="error-test")
        op = service.start_operation(trace.trace_id, "validate")

        service.finish_operation(
            trace.trace_id,
            op.id,
            error="Validation failed",
            error_stack="traceback here"
        )

        service.finish_request(trace.trace_id)

        errors = service.get_errors()
        assert len(errors) > 0

    def test_service_graph(self, service):
        """Test service dependency graph."""
        # Create inter-service trace
        trace = service.start_request("process")
        graph = service.get_service_graph()

        # Initially should be empty or have self-references
        assert isinstance(graph, list)

    def test_latency_query(self, service):
        """Test querying latencies."""
        for i in range(5):
            trace = service.start_request("query_op")
            service.finish_request(trace.trace_id)

        latencies = service.get_latencies()
        assert latencies["count"] == 5
        assert "p50" in latencies
        assert "p95" in latencies

    def test_status_check(self, service):
        """Test getting status."""
        trace = service.start_request("test")
        service.finish_request(trace.trace_id)

        status = service.status()
        assert "metrics" in status
        assert "active_traces" in status
        assert "completed_traces" in status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
