"""
Unit tests for stream processing engine.

Tests windowing, aggregations, joins, state management, and backpressure.
"""

import pytest
import time
from src.deia.stream_processor import (
    StreamRecord, StreamProcessor, WindowType, JoinType,
    AggregationFunction, StateStore, WindowFunction,
    MemoryStreamSource, MemoryStreamSink
)


# ===== FIXTURES =====

@pytest.fixture
def sample_records():
    """Create sample stream records."""
    return [
        StreamRecord(key="user1", value=100, timestamp=1000.0),
        StreamRecord(key="user2", value=200, timestamp=1050.0),
        StreamRecord(key="user1", value=150, timestamp=1100.0),
        StreamRecord(key="user2", value=250, timestamp=1150.0),
        StreamRecord(key="user1", value=120, timestamp=1200.0),
    ]


@pytest.fixture
def processor():
    """Create stream processor."""
    return StreamProcessor(buffer_size=1000)


@pytest.fixture
def state_store():
    """Create state store."""
    return StateStore()


# ===== WINDOW TESTS =====

class TestWindowFunction:
    """Test windowing functions."""

    def test_tumbling_window(self):
        """Test tumbling window calculation."""
        start, end = WindowFunction.tumbling_window(1050.0, 100.0)
        assert start == 1000.0
        assert end == 1100.0

    def test_sliding_window(self):
        """Test sliding window calculation."""
        windows = WindowFunction.sliding_window(1050.0, 200.0, 50.0)
        assert len(windows) > 0
        for start, end in windows:
            assert end - start == 200.0

    def test_session_window(self):
        """Test session window assignment."""
        session1 = WindowFunction.session_window(1000.0, 100.0, {})
        session2 = WindowFunction.session_window(1100.0, 100.0, {})
        assert isinstance(session1, str)
        assert isinstance(session2, str)


# ===== AGGREGATION TESTS =====

class TestAggregationFunction:
    """Test aggregation functions."""

    def test_count(self, sample_records):
        """Test count aggregation."""
        count = AggregationFunction.count(sample_records)
        assert count == 5

    def test_sum(self, sample_records):
        """Test sum aggregation."""
        total = AggregationFunction.sum(sample_records, lambda r: r.value)
        assert total == 820

    def test_avg(self, sample_records):
        """Test average aggregation."""
        avg = AggregationFunction.avg(sample_records, lambda r: r.value)
        assert avg == 164.0

    def test_min(self, sample_records):
        """Test minimum aggregation."""
        min_val = AggregationFunction.min(sample_records, lambda r: r.value)
        assert min_val == 100

    def test_max(self, sample_records):
        """Test maximum aggregation."""
        max_val = AggregationFunction.max(sample_records, lambda r: r.value)
        assert max_val == 250

    def test_collect(self, sample_records):
        """Test collect aggregation."""
        values = AggregationFunction.collect(sample_records)
        assert len(values) == 5
        assert 100 in values


# ===== STREAM PROCESSOR TESTS =====

class TestStreamProcessor:
    """Test stream processor."""

    def test_add_record(self, processor, sample_records):
        """Test adding records."""
        for record in sample_records:
            success = processor.add_record(record)
            assert success

    def test_buffer_size(self, processor, sample_records):
        """Test buffer size tracking."""
        for record in sample_records:
            processor.add_record(record)

        assert processor.get_buffer_size() == len(sample_records)

    def test_backpressure(self, processor):
        """Test backpressure handling."""
        small_processor = StreamProcessor(buffer_size=3)

        assert small_processor.add_record(StreamRecord(key="k1", value=1))
        assert small_processor.add_record(StreamRecord(key="k2", value=2))
        assert small_processor.add_record(StreamRecord(key="k3", value=3))
        assert not small_processor.add_record(StreamRecord(key="k4", value=4))
        assert small_processor.is_backpressured()

    def test_get_records(self, processor, sample_records):
        """Test retrieving all records."""
        for record in sample_records:
            processor.add_record(record)

        records = processor.get_records()
        assert len(records) == len(sample_records)

    def test_clear(self, processor, sample_records):
        """Test clearing buffer."""
        for record in sample_records:
            processor.add_record(record)

        assert processor.get_buffer_size() > 0
        processor.clear()
        assert processor.get_buffer_size() == 0

    def test_tumbling_window(self, processor, sample_records):
        """Test tumbling window application."""
        for record in sample_records:
            processor.add_record(record)

        windowed = processor.apply_window(
            WindowType.TUMBLING,
            100.0,
            lambda r: r.key
        )

        assert len(windowed) > 0

    def test_aggregate_count(self, processor, sample_records):
        """Test count aggregation."""
        for record in sample_records:
            processor.add_record(record)

        windowed = processor.apply_window(
            WindowType.TUMBLING,
            100.0,
            lambda r: r.key
        )

        results = processor.aggregate(windowed, "count")
        assert len(results) > 0
        assert results[0].count == len(sample_records)

    def test_aggregate_sum(self, processor, sample_records):
        """Test sum aggregation."""
        for record in sample_records:
            processor.add_record(record)

        windowed = processor.apply_window(
            WindowType.TUMBLING,
            1000.0,
            lambda r: r.key
        )

        results = processor.aggregate(
            windowed,
            "sum",
            lambda r: r.value
        )

        assert len(results) > 0
        assert results[0].sum_value == 820


# ===== STATE STORE TESTS =====

class TestStateStore:
    """Test state management."""

    def test_put_get(self, state_store):
        """Test putting and getting state."""
        state_store.put("user1", "count", 5)
        value = state_store.get("user1", "count")
        assert value == 5

    def test_get_default(self, state_store):
        """Test getting with default."""
        value = state_store.get("nonexistent", "key", "default")
        assert value == "default"

    def test_delete(self, state_store):
        """Test deleting state."""
        state_store.put("user1", "count", 5)
        state_store.delete("user1")
        value = state_store.get("user1", "count", None)
        assert value is None

    def test_get_all(self, state_store):
        """Test getting all state for key."""
        state_store.put("user1", "count", 5)
        state_store.put("user1", "sum", 100)

        all_state = state_store.get_all("user1")
        assert all_state["count"] == 5
        assert all_state["sum"] == 100

    def test_version_tracking(self, state_store):
        """Test version tracking."""
        version1 = state_store.get_version("user1")
        state_store.put("user1", "count", 5)
        version2 = state_store.get_version("user1")
        assert version2 > version1


# ===== JOIN TESTS =====

class TestStreamJoins:
    """Test stream join operations."""

    def test_inner_join(self, processor):
        """Test inner join."""
        left_records = [
            StreamRecord(key="k1", value="L1"),
            StreamRecord(key="k2", value="L2"),
        ]
        right_records = [
            StreamRecord(key="k1", value="R1"),
            StreamRecord(key="k3", value="R3"),
        ]

        results = processor.join_streams(
            left_records,
            right_records,
            lambda r: r.key,
            JoinType.INNER
        )

        assert len(results) == 1
        assert results[0][0].key == "k1"
        assert results[0][1].key == "k1"

    def test_left_join(self, processor):
        """Test left join."""
        left_records = [
            StreamRecord(key="k1", value="L1"),
            StreamRecord(key="k2", value="L2"),
        ]
        right_records = [
            StreamRecord(key="k1", value="R1"),
        ]

        results = processor.join_streams(
            left_records,
            right_records,
            lambda r: r.key,
            JoinType.LEFT
        )

        assert len(results) == 2
        assert results[1][1] is None  # k2 has no match

    def test_full_join(self, processor):
        """Test full outer join."""
        left_records = [
            StreamRecord(key="k1", value="L1"),
        ]
        right_records = [
            StreamRecord(key="k1", value="R1"),
            StreamRecord(key="k2", value="R2"),
        ]

        results = processor.join_streams(
            left_records,
            right_records,
            lambda r: r.key,
            JoinType.FULL
        )

        assert len(results) == 2  # k1 match + k2 from right


# ===== STREAM SOURCE/SINK TESTS =====

class TestStreamSourceSink:
    """Test stream source and sink."""

    def test_memory_source(self, sample_records):
        """Test memory source."""
        source = MemoryStreamSource(sample_records)

        records = []
        while not source.is_closed():
            record = source.read()
            if record:
                records.append(record)

        assert len(records) == len(sample_records)

    def test_memory_sink(self, sample_records):
        """Test memory sink."""
        sink = MemoryStreamSink()

        for record in sample_records:
            sink.write(record)

        sink.flush()
        assert len(sink.get_records()) == len(sample_records)


# ===== INTEGRATION TESTS =====

class TestIntegration:
    """Integration tests for stream processing."""

    def test_full_stream_pipeline(self, processor, sample_records):
        """Test complete stream pipeline."""
        # Add records
        for record in sample_records:
            processor.add_record(record)

        # Apply windowing
        windowed = processor.apply_window(
            WindowType.TUMBLING,
            1000.0,
            lambda r: r.key
        )

        # Aggregate
        results = processor.aggregate(
            windowed,
            "avg",
            lambda r: r.value
        )

        assert len(results) > 0
        assert results[0].avg_value > 0

    def test_source_to_sink_pipeline(self, sample_records):
        """Test source to sink pipeline."""
        source = MemoryStreamSource(sample_records)
        sink = MemoryStreamSink()

        while not source.is_closed():
            record = source.read()
            if record:
                sink.write(record)

        assert len(sink.get_records()) == len(sample_records)

    def test_windowing_aggregation_join(self, processor, sample_records):
        """Test windowing with aggregation and join."""
        # Add records
        for record in sample_records:
            processor.add_record(record)

        # Create two groups
        windowed = processor.apply_window(
            WindowType.TUMBLING,
            1000.0,
            lambda r: r.key
        )

        # Get aggregations
        results = processor.aggregate(
            windowed,
            "count"
        )

        assert len(results) > 0
