"""
Performance Profiler & Optimizer - Profile and optimize DEIA CLI commands.

Provides profiling, benchmarking, bottleneck identification, and optimization metrics.
"""

from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field
from pathlib import Path
import time
import tracemalloc
import cProfile
import pstats
import io
from datetime import datetime
import json
from functools import wraps
from collections import defaultdict
import sys


# ===== PERFORMANCE METRICS =====

@dataclass
class PerformanceMetrics:
    """Performance metrics for a command execution."""
    command_name: str
    execution_time_ms: float  # Wall clock time
    cpu_time_ms: float  # CPU time
    memory_used_mb: float  # Peak memory usage
    memory_peak_mb: float  # Peak memory during execution
    memory_baseline_mb: float  # Memory before execution
    gc_collections: int  # Number of GC collections
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class BenchmarkResult:
    """Result from command benchmarking."""
    command_name: str
    iterations: int
    min_time_ms: float
    max_time_ms: float
    avg_time_ms: float
    median_time_ms: float
    p95_time_ms: float
    p99_time_ms: float
    memory_avg_mb: float
    memory_peak_mb: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class BottleneckReport:
    """Report of identified bottlenecks."""
    function_name: str
    module_name: str
    total_time_ms: float
    call_count: int
    avg_time_per_call_ms: float
    time_percentage: float
    memory_usage_mb: float


# ===== PERFORMANCE PROFILER =====

class PerformanceProfiler:
    """Profile command execution time and memory."""

    def __init__(self):
        """Initialize profiler."""
        self.metrics: List[PerformanceMetrics] = []
        self.start_time: Optional[float] = None
        self.start_memory: Optional[float] = None
        self.profilers: Dict[str, cProfile.Profile] = {}

    def start_profiling(self, command_name: str) -> None:
        """Start profiling a command."""
        tracemalloc.start()
        self.start_time = time.perf_counter()
        self.start_memory = self._get_memory_usage()

        # Start cProfile for CPU profiling
        profiler = cProfile.Profile()
        profiler.enable()
        self.profilers[command_name] = profiler

    def stop_profiling(self, command_name: str) -> PerformanceMetrics:
        """Stop profiling and return metrics."""
        end_time = time.perf_counter()
        execution_time = (end_time - self.start_time) * 1000  # Convert to ms

        # Stop CPU profiling
        if command_name in self.profilers:
            self.profilers[command_name].disable()

        # Get memory metrics
        current_memory = self._get_memory_usage()
        memory_used = current_memory - self.start_memory
        peak_memory = tracemalloc.get_traced_memory()[1] / 1024 / 1024  # Peak

        tracemalloc.stop()

        metrics = PerformanceMetrics(
            command_name=command_name,
            execution_time_ms=execution_time,
            cpu_time_ms=execution_time,  # Approximation
            memory_used_mb=memory_used,
            memory_peak_mb=peak_memory,
            memory_baseline_mb=self.start_memory
        )

        self.metrics.append(metrics)
        return metrics

    def get_cpu_hotspots(self, command_name: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """Get CPU hotspots for a command."""
        if command_name not in self.profilers:
            return []

        profiler = self.profilers[command_name]
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats(top_n)

        output = s.getvalue()
        hotspots = []

        for line in output.split('\n'):
            if 'cumulative' in line or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 5:
                try:
                    func_name = parts[-1]
                    time_val = float(parts[3])
                    hotspots.append((func_name, time_val))
                except (ValueError, IndexError):
                    continue

        return hotspots[:top_n]

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            # Fallback if psutil not available
            return 0.0

    def get_metrics(self) -> List[PerformanceMetrics]:
        """Get all collected metrics."""
        return self.metrics

    def clear_metrics(self) -> None:
        """Clear collected metrics."""
        self.metrics.clear()
        self.profilers.clear()


# ===== BENCHMARKER =====

class CommandBenchmark:
    """Benchmark command execution."""

    def __init__(self, command_func: Callable):
        """Initialize benchmark."""
        self.command_func = command_func
        self.command_name = getattr(command_func, '__name__', 'unknown')
        self.results: List[float] = []
        self.memory_results: List[float] = []

    def run(self, iterations: int = 10, *args, **kwargs) -> BenchmarkResult:
        """Run benchmark with multiple iterations."""
        self.results.clear()
        self.memory_results.clear()

        for _ in range(iterations):
            profiler = PerformanceProfiler()
            profiler.start_profiling(self.command_name)

            try:
                self.command_func(*args, **kwargs)
            except Exception:
                pass

            metrics = profiler.stop_profiling(self.command_name)
            self.results.append(metrics.execution_time_ms)
            self.memory_results.append(metrics.memory_peak_mb)

        return self._calculate_result(iterations)

    def _calculate_result(self, iterations: int) -> BenchmarkResult:
        """Calculate benchmark statistics."""
        sorted_times = sorted(self.results)
        sorted_memory = sorted(self.memory_results)

        return BenchmarkResult(
            command_name=self.command_name,
            iterations=iterations,
            min_time_ms=min(sorted_times),
            max_time_ms=max(sorted_times),
            avg_time_ms=sum(sorted_times) / len(sorted_times),
            median_time_ms=sorted_times[len(sorted_times) // 2],
            p95_time_ms=sorted_times[int(len(sorted_times) * 0.95)],
            p99_time_ms=sorted_times[int(len(sorted_times) * 0.99)],
            memory_avg_mb=sum(sorted_memory) / len(sorted_memory),
            memory_peak_mb=max(sorted_memory)
        )


# ===== BOTTLENECK ANALYZER =====

class BottleneckAnalyzer:
    """Analyze and report bottlenecks."""

    def __init__(self):
        """Initialize analyzer."""
        self.call_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'total_time': 0,
            'call_count': 0,
            'memory': 0
        })

    def add_call_stat(self, function_name: str, execution_time_ms: float,
                     memory_mb: float = 0) -> None:
        """Record function call statistics."""
        self.call_stats[function_name]['total_time'] += execution_time_ms
        self.call_stats[function_name]['call_count'] += 1
        self.call_stats[function_name]['memory'] += memory_mb

    def analyze(self, total_execution_time_ms: float) -> List[BottleneckReport]:
        """Analyze and report bottlenecks."""
        reports = []

        for func_name, stats in self.call_stats.items():
            total_time = stats['total_time']
            if total_time == 0:
                continue

            time_percentage = (total_time / total_execution_time_ms * 100) if total_execution_time_ms > 0 else 0

            # Only report significant bottlenecks (>5% of execution time)
            if time_percentage >= 5:
                report = BottleneckReport(
                    function_name=func_name,
                    module_name=self._extract_module(func_name),
                    total_time_ms=total_time,
                    call_count=stats['call_count'],
                    avg_time_per_call_ms=total_time / stats['call_count'],
                    time_percentage=time_percentage,
                    memory_usage_mb=stats['memory']
                )
                reports.append(report)

        # Sort by time percentage descending
        return sorted(reports, key=lambda x: x.time_percentage, reverse=True)

    @staticmethod
    def _extract_module(function_name: str) -> str:
        """Extract module name from function."""
        if '.' in function_name:
            return '.'.join(function_name.split('.')[:-1])
        return 'unknown'

    def clear(self) -> None:
        """Clear collected statistics."""
        self.call_stats.clear()


# ===== PERFORMANCE OPTIMIZER =====

class PerformanceOptimizer:
    """Optimize identified bottlenecks."""

    def __init__(self):
        """Initialize optimizer."""
        self.optimizations: Dict[str, str] = {}
        self.improvements: List[Dict[str, Any]] = []

    def suggest_optimization(self, function_name: str, bottleneck: BottleneckReport) -> str:
        """Suggest optimization for bottleneck."""
        suggestions = []

        # Time-based suggestions
        if bottleneck.time_percentage > 30:
            suggestions.append(f"Consider caching or memoizing {function_name}")
            suggestions.append("Profile to find inner loops")
            suggestions.append("Consider vectorization or batch operations")

        # Call count based suggestions
        if bottleneck.call_count > 1000:
            suggestions.append(f"{function_name} called {bottleneck.call_count}x - consider batching")
            suggestions.append("Reduce function call overhead with local caching")

        # Memory based suggestions
        if bottleneck.memory_usage_mb > 100:
            suggestions.append(f"{function_name} uses {bottleneck.memory_usage_mb:.1f}MB - optimize memory allocation")
            suggestions.append("Consider streaming or chunked processing")
            suggestions.append("Profile memory allocations")

        suggestion_text = "\n  ".join(suggestions) if suggestions else "Monitor for future optimization"
        self.optimizations[function_name] = suggestion_text

        return suggestion_text

    def log_improvement(self, optimization_name: str, before_ms: float,
                       after_ms: float, memory_before_mb: float,
                       memory_after_mb: float) -> Dict[str, Any]:
        """Log an optimization improvement."""
        time_improvement = ((before_ms - after_ms) / before_ms * 100) if before_ms > 0 else 0
        memory_improvement = ((memory_before_mb - memory_after_mb) / memory_before_mb * 100) if memory_before_mb > 0 else 0

        improvement = {
            'optimization': optimization_name,
            'time_improvement_percent': time_improvement,
            'memory_improvement_percent': memory_improvement,
            'before_time_ms': before_ms,
            'after_time_ms': after_ms,
            'before_memory_mb': memory_before_mb,
            'after_memory_mb': memory_after_mb,
            'timestamp': datetime.now().isoformat()
        }

        self.improvements.append(improvement)
        return improvement

    def get_improvements(self) -> List[Dict[str, Any]]:
        """Get all recorded improvements."""
        return self.improvements


# ===== PROFILING DECORATOR =====

def profile_command(func: Callable) -> Callable:
    """Decorator for profiling command execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = PerformanceProfiler()
        profiler.start_profiling(func.__name__)

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            metrics = profiler.stop_profiling(func.__name__)
            # Print metrics
            print(f"\n[PROFILE] {func.__name__}:")
            print(f"  Time: {metrics.execution_time_ms:.2f}ms")
            print(f"  Memory: {metrics.memory_peak_mb:.2f}MB")

    return wrapper


# ===== PERFORMANCE REPORTER =====

class PerformanceReporter:
    """Generate performance reports."""

    def __init__(self):
        """Initialize reporter."""
        self.baseline_metrics: Dict[str, PerformanceMetrics] = {}
        self.optimized_metrics: Dict[str, PerformanceMetrics] = {}

    def set_baseline(self, command_name: str, metrics: PerformanceMetrics) -> None:
        """Set baseline metrics for command."""
        self.baseline_metrics[command_name] = metrics

    def set_optimized(self, command_name: str, metrics: PerformanceMetrics) -> None:
        """Set optimized metrics for command."""
        self.optimized_metrics[command_name] = metrics

    def get_improvement_percentage(self, command_name: str) -> Tuple[float, float]:
        """Get improvement percentage for time and memory."""
        if command_name not in self.baseline_metrics or command_name not in self.optimized_metrics:
            return 0.0, 0.0

        baseline = self.baseline_metrics[command_name]
        optimized = self.optimized_metrics[command_name]

        time_improvement = ((baseline.execution_time_ms - optimized.execution_time_ms) /
                           baseline.execution_time_ms * 100)
        memory_improvement = ((baseline.memory_peak_mb - optimized.memory_peak_mb) /
                             baseline.memory_peak_mb * 100)

        return time_improvement, memory_improvement

    def generate_report(self) -> str:
        """Generate performance report."""
        report_lines = [
            "# PERFORMANCE OPTIMIZATION REPORT\n",
            f"Generated: {datetime.now().isoformat()}\n",
            "## Baseline vs Optimized\n"
        ]

        for command_name in self.baseline_metrics:
            if command_name not in self.optimized_metrics:
                continue

            baseline = self.baseline_metrics[command_name]
            optimized = self.optimized_metrics[command_name]
            time_imp, memory_imp = self.get_improvement_percentage(command_name)

            report_lines.append(f"\n### {command_name}")
            report_lines.append(f"- **Time:** {baseline.execution_time_ms:.2f}ms → {optimized.execution_time_ms:.2f}ms ({time_imp:+.1f}%)")
            report_lines.append(f"- **Memory:** {baseline.memory_peak_mb:.2f}MB → {optimized.memory_peak_mb:.2f}MB ({memory_imp:+.1f}%)")

        return "\n".join(report_lines)

    def to_json(self) -> str:
        """Export report as JSON."""
        data = {
            "baseline": {name: self._metrics_to_dict(m)
                        for name, m in self.baseline_metrics.items()},
            "optimized": {name: self._metrics_to_dict(m)
                         for name, m in self.optimized_metrics.items()},
            "improvements": {name: {
                "time_improvement_percent": self.get_improvement_percentage(name)[0],
                "memory_improvement_percent": self.get_improvement_percentage(name)[1]
            } for name in self.baseline_metrics if name in self.optimized_metrics}
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def _metrics_to_dict(metrics: PerformanceMetrics) -> dict:
        """Convert metrics to dictionary."""
        return {
            "execution_time_ms": metrics.execution_time_ms,
            "memory_peak_mb": metrics.memory_peak_mb,
            "timestamp": metrics.timestamp
        }
