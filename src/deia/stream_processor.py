"""
Stream Processing Engine - Real-time data processing with windowing, aggregations, joins.

Provides streaming capabilities: sources, sinks, windowing (tumbling/sliding/session),
aggregations, joins, state management, backpressure handling, and fault tolerance.
"""

from typing import Dict, List, Optional, Any, Callable, Union, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import time
import threading
from collections import deque, defaultdict
from datetime import datetime, timedelta
import logging
import heapq

logger = logging.getLogger(__name__)


# ===== ENUMS =====

class WindowType(str, Enum):
    """Window types for streaming aggregations."""
    TUMBLING = "tumbling"
    SLIDING = "sliding"
    SESSION = "session"


class JoinType(str, Enum):
    """Join types for stream operations."""
    INNER = "inner"
    LEFT = "left"
    RIGHT = "right"
    FULL = "full"


# ===== DATA STRUCTURES =====

@dataclass
class StreamRecord:
    """Single record in a stream."""
    key: Any
    value: Any
    timestamp: float = field(default_factory=time.time)
    is_watermark: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WindowBucket:
    """Aggregation bucket for a window."""
    window_key: str
    start_time: float
    end_time: float
    records: List[StreamRecord] = field(default_factory=list)
    aggregated: Dict[str, Any] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AggregationResult:
    """Result of aggregation operation."""
    group_key: Any
    window_key: str
    count: int = 0
    sum_value: float = 0.0
    avg_value: float = 0.0
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    state: Dict[str, Any] = field(default_factory=dict)


# ===== BASE CLASSES =====

class StreamSource(ABC):
    """Abstract base for stream data sources."""

    @abstractmethod
    def read(self) -> Optional[StreamRecord]:
        """Read next record from source."""
        pass

    @abstractmethod
    def is_closed(self) -> bool:
        """Check if source is closed."""
        pass


class StreamSink(ABC):
    """Abstract base for stream data sinks."""

    @abstractmethod
    def write(self, record: StreamRecord) -> None:
        """Write record to sink."""
        pass

    @abstractmethod
    def flush(self) -> None:
        """Flush pending records."""
        pass


# ===== WINDOWING =====

class WindowFunction:
    """Compute window boundaries."""

    @staticmethod
    def tumbling_window(timestamp: float, window_size: float) -> Tuple[float, float]:
        """Compute tumbling window."""
        start = int(timestamp / window_size) * window_size
        end = start + window_size
        return start, end

    @staticmethod
    def sliding_window(timestamp: float, window_size: float, slide_interval: float) -> List[Tuple[float, float]]:
        """Compute sliding windows."""
        windows = []
        num_windows = int(window_size / slide_interval)
        for i in range(num_windows):
            start = int(timestamp / slide_interval) * slide_interval - (i * slide_interval)
            end = start + window_size
            windows.append((start, end))
        return windows

    @staticmethod
    def session_window(timestamp: float, gap: float, current_sessions: Dict[Any, float]) -> str:
        """Assign to or create session window."""
        # Simple session window implementation
        return f"session_{int(timestamp / (gap * 1000))}"


# ===== AGGREGATIONS =====

class AggregationFunction:
    """Aggregate values from stream records."""

    @staticmethod
    def count(records: List[StreamRecord]) -> int:
        """Count records."""
        return len(records)

    @staticmethod
    def sum(records: List[StreamRecord], value_extractor: Callable[[StreamRecord], float]) -> float:
        """Sum values."""
        return sum(value_extractor(r) for r in records)

    @staticmethod
    def avg(records: List[StreamRecord], value_extractor: Callable[[StreamRecord], float]) -> float:
        """Average values."""
        if not records:
            return 0.0
        return AggregationFunction.sum(records, value_extractor) / len(records)

    @staticmethod
    def min(records: List[StreamRecord], value_extractor: Callable[[StreamRecord], float]) -> Optional[float]:
        """Minimum value."""
        if not records:
            return None
        return min(value_extractor(r) for r in records)

    @staticmethod
    def max(records: List[StreamRecord], value_extractor: Callable[[StreamRecord], float]) -> Optional[float]:
        """Maximum value."""
        if not records:
            return None
        return max(value_extractor(r) for r in records)

    @staticmethod
    def collect(records: List[StreamRecord]) -> List[Any]:
        """Collect all values."""
        return [r.value for r in records]


# ===== STATE MANAGEMENT =====

class StateStore:
    """Manage stateful computations."""

    def __init__(self):
        """Initialize state store."""
        self.state: Dict[str, Dict[str, Any]] = {}
        self.version: Dict[str, int] = {}
        self.lock = threading.RLock()

    def put(self, key: str, state_key: str, value: Any) -> None:
        """Store state."""
        with self.lock:
            if key not in self.state:
                self.state[key] = {}
            self.state[key][state_key] = value
            self.version[key] = self.version.get(key, 0) + 1

    def get(self, key: str, state_key: str, default: Any = None) -> Any:
        """Retrieve state."""
        with self.lock:
            if key not in self.state:
                return default
            return self.state[key].get(state_key, default)

    def delete(self, key: str) -> None:
        """Delete state."""
        with self.lock:
            if key in self.state:
                del self.state[key]
            self.version[key] = self.version.get(key, 0) + 1

    def get_all(self, key: str) -> Dict[str, Any]:
        """Get all state for key."""
        with self.lock:
            return self.state.get(key, {}).copy()

    def get_version(self, key: str) -> int:
        """Get state version."""
        with self.lock:
            return self.version.get(key, 0)


# ===== STREAM OPERATIONS =====

class StreamProcessor:
    """Process streaming data with operators."""

    def __init__(self, buffer_size: int = 10000):
        """Initialize processor."""
        self.buffer_size = buffer_size
        self.queue: deque = deque(maxlen=buffer_size)
        self.state_store = StateStore()
        self.windows: Dict[str, WindowBucket] = {}
        self.lock = threading.RLock()
        self.running = False

    def add_record(self, record: StreamRecord) -> bool:
        """Add record to stream."""
        with self.lock:
            if len(self.queue) >= self.buffer_size:
                return False  # Backpressure: queue full
            self.queue.append(record)
            return True

    def apply_window(self, window_type: WindowType, window_size: float, key_extractor: Callable) -> Dict[str, WindowBucket]:
        """Apply windowing to stream."""
        windowed = {}

        with self.lock:
            for record in self.queue:
                key = key_extractor(record)

                if window_type == WindowType.TUMBLING:
                    start, end = WindowFunction.tumbling_window(record.timestamp, window_size)
                    window_key = f"tumble_{start}_{end}"

                elif window_type == WindowType.SLIDING:
                    windows = WindowFunction.sliding_window(record.timestamp, window_size, window_size / 2)
                    for start, end in windows:
                        window_key = f"slide_{start}_{end}"
                        if window_key not in windowed:
                            windowed[window_key] = WindowBucket(window_key, start, end)
                        windowed[window_key].records.append(record)
                    continue

                elif window_type == WindowType.SESSION:
                    window_key = WindowFunction.session_window(record.timestamp, window_size, {})

                if window_key not in windowed:
                    if window_type == WindowType.TUMBLING:
                        windowed[window_key] = WindowBucket(window_key, start, end)
                    else:
                        windowed[window_key] = WindowBucket(window_key, time.time(), time.time() + window_size)

                windowed[window_key].records.append(record)

        return windowed

    def aggregate(self, windows: Dict[str, WindowBucket], agg_type: str,
                  value_extractor: Optional[Callable] = None, key_extractor: Optional[Callable] = None) -> List[AggregationResult]:
        """Aggregate windowed data."""
        results = []

        for window_key, bucket in windows.items():
            if agg_type == "count":
                result = AggregationResult(
                    group_key="all",
                    window_key=window_key,
                    count=AggregationFunction.count(bucket.records)
                )

            elif agg_type == "sum" and value_extractor:
                result = AggregationResult(
                    group_key="all",
                    window_key=window_key,
                    sum_value=AggregationFunction.sum(bucket.records, value_extractor)
                )

            elif agg_type == "avg" and value_extractor:
                result = AggregationResult(
                    group_key="all",
                    window_key=window_key,
                    avg_value=AggregationFunction.avg(bucket.records, value_extractor),
                    count=len(bucket.records)
                )

            elif agg_type == "min" and value_extractor:
                result = AggregationResult(
                    group_key="all",
                    window_key=window_key,
                    min_value=AggregationFunction.min(bucket.records, value_extractor)
                )

            elif agg_type == "max" and value_extractor:
                result = AggregationResult(
                    group_key="all",
                    window_key=window_key,
                    max_value=AggregationFunction.max(bucket.records, value_extractor)
                )

            else:
                result = AggregationResult(group_key="all", window_key=window_key)

            results.append(result)

        return results

    def join_streams(self, records_left: List[StreamRecord], records_right: List[StreamRecord],
                     join_key_extractor: Callable, join_type: JoinType = JoinType.INNER) -> List[Tuple[StreamRecord, StreamRecord]]:
        """Join two streams."""
        # Build index for right stream
        right_index: Dict[Any, List[StreamRecord]] = defaultdict(list)
        for record in records_right:
            key = join_key_extractor(record)
            right_index[key].append(record)

        results = []

        for left_record in records_left:
            left_key = join_key_extractor(left_record)
            right_matches = right_index.get(left_key, [])

            if right_matches:
                for right_record in right_matches:
                    results.append((left_record, right_record))

            elif join_type in [JoinType.LEFT, JoinType.FULL]:
                results.append((left_record, None))

        # Handle unmatched right records for full join
        if join_type == JoinType.FULL:
            matched_left_keys = set(join_key_extractor(r) for r in records_left)
            for right_record in records_right:
                if join_key_extractor(right_record) not in matched_left_keys:
                    results.append((None, right_record))

        return results

    def get_buffer_size(self) -> int:
        """Get current buffer size."""
        with self.lock:
            return len(self.queue)

    def get_buffer_capacity(self) -> int:
        """Get buffer capacity."""
        return self.buffer_size

    def is_backpressured(self) -> bool:
        """Check if buffer is full (backpressured)."""
        with self.lock:
            return len(self.queue) >= self.buffer_size

    def clear(self) -> None:
        """Clear buffer."""
        with self.lock:
            self.queue.clear()

    def get_records(self) -> List[StreamRecord]:
        """Get all buffered records."""
        with self.lock:
            return list(self.queue)


# ===== IN-MEMORY IMPLEMENTATIONS =====

class MemoryStreamSource(StreamSource):
    """In-memory stream source."""

    def __init__(self, records: List[StreamRecord]):
        """Initialize with records."""
        self.records = records
        self.index = 0

    def read(self) -> Optional[StreamRecord]:
        """Read next record."""
        if self.index < len(self.records):
            record = self.records[self.index]
            self.index += 1
            return record
        return None

    def is_closed(self) -> bool:
        """Check if source is closed."""
        return self.index >= len(self.records)


class MemoryStreamSink(StreamSink):
    """In-memory stream sink."""

    def __init__(self):
        """Initialize sink."""
        self.records: List[StreamRecord] = []

    def write(self, record: StreamRecord) -> None:
        """Write record."""
        self.records.append(record)

    def flush(self) -> None:
        """Flush (no-op for memory sink)."""
        pass

    def get_records(self) -> List[StreamRecord]:
        """Get all records written."""
        return self.records.copy()
