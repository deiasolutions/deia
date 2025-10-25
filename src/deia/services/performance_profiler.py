"""
Performance Profiler - Measure and analyze system performance.

Profiles critical paths, benchmarks throughput, identifies bottlenecks,
and provides tuning recommendations for optimization.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
import json
import time
import statistics


class BottleneckType(Enum):
    """Types of system bottlenecks."""
    CPU_BOUND = "cpu_bound"
    IO_BOUND = "io_bound"
    MEMORY_BOUND = "memory_bound"
    QUEUE_BOUND = "queue_bound"
    NETWORK_BOUND = "network_bound"


@dataclass
class LatencyMetrics:
    """Latency metrics for an operation."""
    operation: str
    samples: int = 0
    min_ms: float = 0.0
    max_ms: float = 0.0
    mean_ms: float = 0.0
    median_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    stdev_ms: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ThroughputMetrics:
    """Throughput metrics."""
    metric: str
    tasks_per_second: float = 0.0
    total_tasks: int = 0
    duration_seconds: float = 0.0
    success_rate: float = 1.0
    avg_latency_ms: float = 0.0


@dataclass
class BottleneckAnalysis:
    """Bottleneck analysis result."""
    bottleneck_type: BottleneckType
    severity: str  # low, medium, high, critical
    description: str
    affected_operations: List[str] = field(default_factory=list)
    recommendation: str = ""


class PerformanceProfiler:
    """
    Performance profiling and analysis service.

    Features:
    - Profile critical paths (routing, API calls)
    - Measure system throughput
    - Identify bottlenecks
    - Provide optimization recommendations
    - Track performance over time
    """

    def __init__(self, work_dir: Path):
        """Initialize performance profiler."""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.profile_log = self.log_dir / "performance-profile.jsonl"

        # Metrics storage
        self.latency_samples: Dict[str, List[float]] = {}
        self.latency_metrics: Dict[str, LatencyMetrics] = {}
        self.throughput_metrics: List[ThroughputMetrics] = []
        self.bottlenecks: List[BottleneckAnalysis] = []

    def profile_operation(
        self,
        operation_name: str,
        func: Callable,
        args: tuple = (),
        kwargs: Optional[Dict] = None,
        iterations: int = 10
    ) -> LatencyMetrics:
        """
        Profile an operation's latency.

        Args:
            operation_name: Name of operation
            func: Function to profile
            args: Positional arguments
            kwargs: Keyword arguments
            iterations: Number of iterations

        Returns:
            LatencyMetrics
        """
        if operation_name not in self.latency_samples:
            self.latency_samples[operation_name] = []

        samples = []

        for _ in range(iterations):
            start = time.perf_counter()
            try:
                func(*args, **(kwargs or {}))
            except Exception:
                pass  # Continue profiling
            end = time.perf_counter()

            latency_ms = (end - start) * 1000
            samples.append(latency_ms)
            self.latency_samples[operation_name].append(latency_ms)

        # Calculate metrics
        metrics = self._calculate_latency_metrics(operation_name, samples)
        self.latency_metrics[operation_name] = metrics

        self._log_event("operation_profiled", {
            "operation": operation_name,
            "samples": iterations,
            "mean_ms": metrics.mean_ms
        })

        return metrics

    def measure_throughput(
        self,
        metric_name: str,
        func: Callable,
        duration_seconds: float = 10.0,
        args: tuple = (),
        kwargs: Optional[Dict] = None
    ) -> ThroughputMetrics:
        """
        Measure throughput of an operation.

        Args:
            metric_name: Name of metric
            func: Function to measure
            duration_seconds: How long to run
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            ThroughputMetrics
        """
        start_time = time.perf_counter()
        end_time = start_time + duration_seconds

        task_count = 0
        success_count = 0
        latencies = []

        while time.perf_counter() < end_time:
            task_start = time.perf_counter()
            try:
                func(*args, **(kwargs or {}))
                success_count += 1
            except Exception:
                pass
            finally:
                task_end = time.perf_counter()
                latencies.append((task_end - task_start) * 1000)
                task_count += 1

        actual_duration = time.perf_counter() - start_time
        tps = task_count / actual_duration if actual_duration > 0 else 0
        success_rate = success_count / task_count if task_count > 0 else 0
        avg_latency = statistics.mean(latencies) if latencies else 0

        metrics = ThroughputMetrics(
            metric=metric_name,
            tasks_per_second=tps,
            total_tasks=task_count,
            duration_seconds=actual_duration,
            success_rate=success_rate,
            avg_latency_ms=avg_latency
        )

        self.throughput_metrics.append(metrics)

        self._log_event("throughput_measured", {
            "metric": metric_name,
            "tps": tps,
            "tasks": task_count
        })

        return metrics

    def analyze_bottlenecks(self) -> List[BottleneckAnalysis]:
        """
        Analyze profiling data to identify bottlenecks.

        Returns:
            List of bottleneck analyses
        """
        self.bottlenecks = []

        # Analyze latency outliers
        for op_name, metrics in self.latency_metrics.items():
            # High latency indicates bottleneck
            if metrics.mean_ms > 50:
                severity = "critical" if metrics.mean_ms > 200 else "high"
                self.bottlenecks.append(BottleneckAnalysis(
                    bottleneck_type=BottleneckType.CPU_BOUND,
                    severity=severity,
                    description=f"{op_name} has high latency ({metrics.mean_ms:.1f}ms)",
                    affected_operations=[op_name],
                    recommendation=f"Optimize {op_name} or parallelize calls"
                ))

            # High variance indicates queue contention
            if metrics.stdev_ms > metrics.mean_ms:
                self.bottlenecks.append(BottleneckAnalysis(
                    bottleneck_type=BottleneckType.QUEUE_BOUND,
                    severity="medium",
                    description=f"{op_name} has high variance ({metrics.stdev_ms:.1f}ms)",
                    affected_operations=[op_name],
                    recommendation="Consider queue depth optimization or load balancing"
                ))

        # Analyze throughput
        for metrics in self.throughput_metrics:
            if metrics.success_rate < 0.95:
                self.bottlenecks.append(BottleneckAnalysis(
                    bottleneck_type=BottleneckType.IO_BOUND,
                    severity="high",
                    description=f"{metrics.metric} has low success rate ({metrics.success_rate:.1%})",
                    affected_operations=[metrics.metric],
                    recommendation="Check I/O subsystem or network connectivity"
                ))

        self._log_event("bottlenecks_analyzed", {
            "count": len(self.bottlenecks)
        })

        return self.bottlenecks

    def get_tuning_recommendations(self) -> Dict[str, Any]:
        """
        Get optimization recommendations based on profiling.

        Returns:
            Recommendations dictionary
        """
        recommendations = {
            "caching": [],
            "parallelization": [],
            "batching": [],
            "resource_allocation": []
        }

        # Recommend caching for high-latency operations
        for op_name, metrics in self.latency_metrics.items():
            if metrics.mean_ms > 100:
                recommendations["caching"].append({
                    "operation": op_name,
                    "reason": f"High latency ({metrics.mean_ms:.1f}ms)",
                    "expected_improvement": "50-80% latency reduction"
                })

            if metrics.max_ms > metrics.mean_ms * 3:
                recommendations["parallelization"].append({
                    "operation": op_name,
                    "reason": f"High variance ({metrics.stdev_ms:.1f}ms)",
                    "expected_improvement": "Better resource utilization"
                })

        # Recommend batching for high throughput
        for metrics in self.throughput_metrics:
            if metrics.tasks_per_second < 100:
                recommendations["batching"].append({
                    "metric": metrics.metric,
                    "reason": f"Low throughput ({metrics.tasks_per_second:.0f} TPS)",
                    "expected_improvement": "2-5x throughput increase"
                })

        return recommendations

    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive performance summary.

        Returns:
            Summary dictionary
        """
        latencies = list(self.latency_metrics.values())
        throughputs = self.throughput_metrics

        avg_latency = statistics.mean([m.mean_ms for m in latencies]) if latencies else 0
        max_latency = max([m.max_ms for m in latencies]) if latencies else 0

        avg_tps = statistics.mean([m.tasks_per_second for m in throughputs]) if throughputs else 0
        total_tasks = sum([m.total_tasks for m in throughputs])

        return {
            "timestamp": datetime.now().isoformat(),
            "latency": {
                "operations_profiled": len(latencies),
                "average_ms": avg_latency,
                "max_ms": max_latency
            },
            "throughput": {
                "metrics_measured": len(throughputs),
                "average_tps": avg_tps,
                "total_tasks_processed": total_tasks
            },
            "bottlenecks": {
                "identified": len(self.bottlenecks),
                "critical": len([b for b in self.bottlenecks if b.severity == "critical"]),
                "high": len([b for b in self.bottlenecks if b.severity == "high"])
            }
        }

    def export_profile_report(self, filepath: Path) -> bool:
        """
        Export profiling results to file.

        Args:
            filepath: Path to export to

        Returns:
            True if successful
        """
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "latency_metrics": {
                    name: metrics.to_dict()
                    for name, metrics in self.latency_metrics.items()
                },
                "throughput_metrics": [
                    {
                        "metric": m.metric,
                        "tasks_per_second": m.tasks_per_second,
                        "total_tasks": m.total_tasks,
                        "success_rate": m.success_rate,
                        "avg_latency_ms": m.avg_latency_ms
                    }
                    for m in self.throughput_metrics
                ],
                "bottlenecks": [
                    {
                        "type": b.bottleneck_type.value,
                        "severity": b.severity,
                        "description": b.description,
                        "recommendation": b.recommendation
                    }
                    for b in self.bottlenecks
                ],
                "recommendations": self.get_tuning_recommendations(),
                "summary": self.get_performance_summary()
            }

            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)

            self._log_event("profile_exported", {
                "filepath": str(filepath)
            })

            return True
        except Exception as e:
            self._log_event("export_failed", {"error": str(e)})
            return False

    def _calculate_latency_metrics(
        self,
        operation: str,
        samples: List[float]
    ) -> LatencyMetrics:
        """Calculate latency metrics from samples."""
        if not samples:
            return LatencyMetrics(operation=operation)

        sorted_samples = sorted(samples)
        return LatencyMetrics(
            operation=operation,
            samples=len(samples),
            min_ms=min(samples),
            max_ms=max(samples),
            mean_ms=statistics.mean(samples),
            median_ms=statistics.median(samples),
            p95_ms=sorted_samples[int(len(sorted_samples) * 0.95)] if len(sorted_samples) > 0 else 0,
            p99_ms=sorted_samples[int(len(sorted_samples) * 0.99)] if len(sorted_samples) > 0 else 0,
            stdev_ms=statistics.stdev(samples) if len(samples) > 1 else 0
        )

    def _log_event(self, event: str, details: Dict = None) -> None:
        """Log profiling event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details or {}
        }

        try:
            with open(self.profile_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[PERFORMANCE-PROFILER] Failed to log event: {e}")
