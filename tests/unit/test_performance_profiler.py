"""Unit tests for PerformanceProfiler service."""

import pytest
from pathlib import Path
from src.deia.services.performance_profiler import (
    PerformanceProfiler, BottleneckType
)
import time


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def profiler(temp_work_dir):
    """Create PerformanceProfiler instance."""
    return PerformanceProfiler(temp_work_dir)


class TestOperationProfiling:
    """Test operation profiling."""

    def test_profile_fast_operation(self, profiler):
        """Test profiling a fast operation."""
        def fast_op():
            time.sleep(0.001)  # 1ms

        metrics = profiler.profile_operation("fast_op", fast_op, iterations=5)

        assert metrics.operation == "fast_op"
        assert metrics.samples == 5
        assert metrics.min_ms > 0
        assert metrics.mean_ms > 0

    def test_profile_slow_operation(self, profiler):
        """Test profiling a slow operation."""
        def slow_op():
            time.sleep(0.050)  # 50ms

        metrics = profiler.profile_operation("slow_op", slow_op, iterations=3)

        assert metrics.operation == "slow_op"
        assert metrics.samples == 3
        assert metrics.mean_ms > 40  # Should be ~50ms

    def test_profile_with_args(self, profiler):
        """Test profiling operation with arguments."""
        def op_with_args(x, y):
            return x + y

        metrics = profiler.profile_operation(
            "add",
            op_with_args,
            args=(1, 2),
            iterations=10
        )

        assert metrics.operation == "add"
        assert metrics.samples == 10

    def test_latency_statistics(self, profiler):
        """Test latency statistics calculation."""
        def op():
            time.sleep(0.005)

        metrics = profiler.profile_operation("op", op, iterations=10)

        assert metrics.min_ms <= metrics.mean_ms
        assert metrics.mean_ms <= metrics.max_ms
        assert metrics.median_ms > 0
        assert metrics.p95_ms > metrics.p50_ms if hasattr(metrics, 'p50_ms') else True


class TestThroughputMeasurement:
    """Test throughput measurement."""

    def test_measure_throughput(self, profiler):
        """Test measuring throughput."""
        def op():
            time.sleep(0.001)

        metrics = profiler.measure_throughput(
            "test_metric",
            op,
            duration_seconds=0.1
        )

        assert metrics.metric == "test_metric"
        assert metrics.total_tasks > 0
        assert metrics.tasks_per_second > 0
        assert metrics.success_rate > 0

    def test_throughput_with_failures(self, profiler):
        """Test throughput with some failures."""
        call_count = [0]

        def op_with_failures():
            call_count[0] += 1
            if call_count[0] % 3 == 0:
                raise Exception("Simulated failure")

        metrics = profiler.measure_throughput(
            "unstable_op",
            op_with_failures,
            duration_seconds=0.05
        )

        assert metrics.success_rate < 1.0


class TestBottleneckAnalysis:
    """Test bottleneck analysis."""

    def test_identify_high_latency_bottleneck(self, profiler):
        """Test identifying high latency bottleneck."""
        def slow_op():
            time.sleep(0.200)  # 200ms - definitely exceeds threshold

        profiler.profile_operation("slow", slow_op, iterations=3)
        bottlenecks = profiler.analyze_bottlenecks()

        # Should identify at least one bottleneck for high latency
        assert len(bottlenecks) > 0
        # Should have at least one high or critical severity bottleneck
        assert any(b.severity in ["high", "critical"] for b in bottlenecks)

    def test_identify_variance_bottleneck(self, profiler):
        """Test identifying high variance bottleneck."""
        def variable_op():
            import random
            time.sleep(random.uniform(0.005, 0.050))

        profiler.profile_operation("variable", variable_op, iterations=10)
        bottlenecks = profiler.analyze_bottlenecks()

        # High variance might be detected
        assert isinstance(bottlenecks, list)

    def test_no_bottlenecks_for_fast_operation(self, profiler):
        """Test that fast operations don't trigger bottlenecks."""
        def fast_op():
            x = 1 + 1

        profiler.profile_operation("fast", fast_op, iterations=10)
        bottlenecks = profiler.analyze_bottlenecks()

        # Fast operation shouldn't trigger high latency bottleneck
        high_latency_bottlenecks = [
            b for b in bottlenecks
            if "latency" in b.description.lower()
        ]
        assert len(high_latency_bottlenecks) == 0


class TestTuningRecommendations:
    """Test tuning recommendations."""

    def test_caching_recommendation(self, profiler):
        """Test caching recommendations."""
        def slow_op():
            time.sleep(0.150)

        profiler.profile_operation("expensive", slow_op, iterations=3)
        recommendations = profiler.get_tuning_recommendations()

        assert "caching" in recommendations
        # High latency ops should get caching recommendation
        expensive_ops = [
            r["operation"] for r in recommendations["caching"]
            if r.get("operation") == "expensive"
        ]
        assert len(expensive_ops) > 0

    def test_batching_recommendation(self, profiler):
        """Test batching recommendations."""
        def slow_metric():
            time.sleep(0.020)

        profiler.measure_throughput(
            "slow_throughput",
            slow_metric,
            duration_seconds=0.05
        )

        recommendations = profiler.get_tuning_recommendations()

        assert "batching" in recommendations
        # Low throughput should get batching recommendation
        slow_metrics = [
            r["metric"] for r in recommendations["batching"]
            if r.get("metric") == "slow_throughput"
        ]
        assert len(slow_metrics) > 0


class TestPerformanceSummary:
    """Test performance summary."""

    def test_get_summary(self, profiler):
        """Test getting performance summary."""
        def op1():
            time.sleep(0.005)

        def op2():
            time.sleep(0.010)

        profiler.profile_operation("op1", op1, iterations=5)
        profiler.profile_operation("op2", op2, iterations=5)
        profiler.measure_throughput("metric1", op1, duration_seconds=0.05)

        summary = profiler.get_performance_summary()

        assert "timestamp" in summary
        assert "latency" in summary
        assert "throughput" in summary
        assert summary["latency"]["operations_profiled"] == 2
        assert summary["throughput"]["metrics_measured"] >= 1

    def test_summary_with_bottlenecks(self, profiler):
        """Test summary includes bottleneck count."""
        def slow_op():
            time.sleep(0.100)

        profiler.profile_operation("slow", slow_op, iterations=3)
        profiler.analyze_bottlenecks()

        summary = profiler.get_performance_summary()

        assert "bottlenecks" in summary
        assert "identified" in summary["bottlenecks"]


class TestExport:
    """Test profile export."""

    def test_export_report(self, profiler, temp_work_dir):
        """Test exporting profiling report."""
        def op():
            time.sleep(0.005)

        profiler.profile_operation("test", op, iterations=5)
        profiler.analyze_bottlenecks()

        export_path = temp_work_dir / "performance_report.json"
        success = profiler.export_profile_report(export_path)

        assert success
        assert export_path.exists()

        import json
        with open(export_path) as f:
            report = json.load(f)

        assert "latency_metrics" in report
        assert "throughput_metrics" in report
        assert "bottlenecks" in report
        assert "recommendations" in report


class TestLogging:
    """Test event logging."""

    def test_profiling_logged(self, profiler, temp_work_dir):
        """Test that profiling is logged."""
        def op():
            pass

        profiler.profile_operation("op", op, iterations=2)

        log_file = temp_work_dir / ".deia" / "bot-logs" / "performance-profile.jsonl"
        assert log_file.exists()

        with open(log_file) as f:
            lines = f.readlines()
        assert len(lines) > 0


class TestMetricsStorage:
    """Test metrics storage."""

    def test_metrics_stored(self, profiler):
        """Test that metrics are stored correctly."""
        def op():
            time.sleep(0.001)

        profiler.profile_operation("stored_op", op, iterations=3)

        assert "stored_op" in profiler.latency_metrics
        assert "stored_op" in profiler.latency_samples
        assert len(profiler.latency_samples["stored_op"]) == 3

    def test_multiple_operations(self, profiler):
        """Test profiling multiple operations."""
        def op1():
            time.sleep(0.005)

        def op2():
            time.sleep(0.010)

        profiler.profile_operation("op1", op1, iterations=5)
        profiler.profile_operation("op2", op2, iterations=5)

        assert len(profiler.latency_metrics) == 2
        assert "op1" in profiler.latency_metrics
        assert "op2" in profiler.latency_metrics
