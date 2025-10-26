"""
Unit tests for command_composition module.

Tests piping, command chaining, error propagation, and pipeline execution.
"""

import pytest
import json
from src.deia.command_composition import (
    Pipeline, CommandChain, PipelineStage, PipeFrame, DataType,
    JsonParserStage, FilterStage, TransformStage, JsonFormatterStage,
    create_filter_predicate, create_field_extractor
)


@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "Chicago"}
    ]


@pytest.fixture
def json_string(sample_data):
    """Sample data as JSON string."""
    return json.dumps(sample_data)


class TestJsonParserStage:
    """Test JSON parser stage."""

    def test_parse_valid_json(self, json_string):
        """Test parsing valid JSON."""
        stage = JsonParserStage()
        frame = PipeFrame(data=json_string, data_type=DataType.JSON)

        results = list(stage.process(frame))

        assert len(results) == 1
        assert isinstance(results[0].data, list)
        assert len(results[0].data) == 3

    def test_parse_invalid_json(self):
        """Test parsing invalid JSON."""
        stage = JsonParserStage()
        frame = PipeFrame(data="{invalid json}", data_type=DataType.JSON)

        results = list(stage.process(frame))

        assert len(results) == 1
        assert results[0].is_error is True
        assert "JSON parse error" in results[0].error_message


class TestFilterStage:
    """Test filter stage."""

    def test_filter_list(self, sample_data):
        """Test filtering list."""
        predicate = lambda item: item["age"] > 26
        stage = FilterStage(predicate)
        frame = PipeFrame(data=sample_data, data_type=DataType.STRUCTURED)

        results = list(stage.process(frame))

        assert len(results) == 1
        filtered = results[0].data
        assert len(filtered) == 2
        assert all(item["age"] > 26 for item in filtered)

    def test_filter_no_matches(self, sample_data):
        """Test filter with no matches."""
        predicate = lambda item: item["age"] > 100
        stage = FilterStage(predicate)
        frame = PipeFrame(data=sample_data, data_type=DataType.STRUCTURED)

        results = list(stage.process(frame))

        assert len(results) == 1
        assert len(results[0].data) == 0

    def test_filter_propagates_errors(self):
        """Test that errors propagate through filter."""
        stage = FilterStage(lambda x: True)
        frame = PipeFrame(data="test", data_type=DataType.STRUCTURED, is_error=True)

        results = list(stage.process(frame))

        assert len(results) == 1
        assert results[0].is_error is True


class TestTransformStage:
    """Test transform stage."""

    def test_transform_list(self, sample_data):
        """Test transforming list."""
        mapper = lambda item: {**item, "age_plus_5": item["age"] + 5}
        stage = TransformStage(mapper)
        frame = PipeFrame(data=sample_data, data_type=DataType.STRUCTURED)

        results = list(stage.process(frame))

        assert len(results) == 1
        transformed = results[0].data
        assert len(transformed) == 3
        assert transformed[0]["age_plus_5"] == 35

    def test_transform_error_handling(self, sample_data):
        """Test transform error handling."""
        def bad_mapper(item):
            return item["nonexistent_field"]

        stage = TransformStage(bad_mapper)
        frame = PipeFrame(data=sample_data, data_type=DataType.STRUCTURED)

        results = list(stage.process(frame))

        assert len(results) == 1
        assert results[0].is_error is True


class TestJsonFormatterStage:
    """Test JSON formatter stage."""

    def test_format_to_json(self, sample_data):
        """Test formatting to JSON."""
        stage = JsonFormatterStage()
        frame = PipeFrame(data=sample_data, data_type=DataType.STRUCTURED)

        results = list(stage.process(frame))

        assert len(results) == 1
        assert isinstance(results[0].data, str)
        assert results[0].data_type == DataType.JSON

        # Verify it's valid JSON
        parsed = json.loads(results[0].data)
        assert len(parsed) == 3

    def test_format_pretty(self, sample_data):
        """Test pretty JSON formatting."""
        stage = JsonFormatterStage(pretty=True)
        frame = PipeFrame(data=sample_data, data_type=DataType.STRUCTURED)

        results = list(stage.process(frame))

        assert len(results) == 1
        assert "\n" in results[0].data  # Pretty format has newlines


class TestPipeline:
    """Test pipeline execution."""

    def test_simple_pipeline(self, sample_data):
        """Test simple two-stage pipeline."""
        stages = [
            FilterStage(lambda item: item["age"] > 26),
            TransformStage(lambda item: {**item, "age_x2": item["age"] * 2})
        ]
        pipeline = Pipeline(stages)

        results = list(pipeline.execute(sample_data))

        assert len(results) > 0
        # Should have filtered and transformed
        assert not any(r.is_error for r in results if r.data is not None)

    def test_pipeline_with_json_parsing(self, json_string):
        """Test pipeline with JSON parsing."""
        stages = [
            JsonParserStage(),
            FilterStage(lambda item: item["age"] > 26)
        ]
        pipeline = Pipeline(stages)

        results = list(pipeline.execute(json_string, DataType.JSON))

        assert any(r.data for r in results if not r.is_error)

    def test_pipeline_stats(self, sample_data):
        """Test pipeline statistics."""
        stages = [FilterStage(lambda x: True)]
        pipeline = Pipeline(stages)

        list(pipeline.execute(sample_data))

        stats = pipeline.get_stats()
        assert stats["frames_processed"] > 0
        assert "error_rate" in stats

    def test_pipeline_error_propagation(self, sample_data):
        """Test error propagation through pipeline."""
        def error_stage(frame):
            yield PipeFrame(
                data=frame.data,
                data_type=frame.data_type,
                is_error=True,
                error_message="Test error"
            )

        class ErrorStage(PipelineStage):
            def __init__(self):
                super().__init__("error")

            def process(self, frame):
                return error_stage(frame)

        stages = [ErrorStage()]
        pipeline = Pipeline(stages)

        results = list(pipeline.execute(sample_data))

        assert any(r.is_error for r in results)


class TestCommandChain:
    """Test command chain builder."""

    def test_chain_filter_map(self, sample_data):
        """Test chaining filter and map."""
        chain = CommandChain(sample_data)
        results = chain.filter(lambda x: x["age"] > 26).map(lambda x: x["name"]).collect()

        assert len(results) == 2  # Alice (30) and Charlie (35) both > 26
        assert "Alice" in results
        assert "Charlie" in results

    def test_chain_with_json_parsing(self, json_string):
        """Test chain with JSON parsing."""
        chain = CommandChain(json_string, DataType.JSON)
        chain.parse_json().filter(lambda x: x["age"] > 26)

        results = chain.collect()

        assert len(results) == 2  # Alice (30) and Charlie (35) both > 26
        names = [r["name"] for r in results]
        assert "Alice" in names
        assert "Charlie" in names

    def test_chain_format_json(self, sample_data):
        """Test chain with JSON formatting."""
        chain = CommandChain(sample_data)
        chain.format_json()

        results = chain.collect()

        assert len(results) > 0
        # Result should be valid JSON string
        parsed = json.loads(results[0])
        assert isinstance(parsed, list)

    def test_chain_fluent_interface(self, sample_data):
        """Test fluent interface."""
        result = (
            CommandChain(sample_data)
            .filter(lambda x: x["age"] > 25)
            .map(lambda x: {"name": x["name"]})
            .collect()
        )

        assert len(result) > 0
        assert all("name" in item for item in result)

    def test_chain_collect_single(self, sample_data):
        """Test collecting single result."""
        result = (
            CommandChain(sample_data)
            .filter(lambda x: x["name"] == "Alice")
            .collect_single()
        )

        assert result is not None
        assert result["name"] == "Alice"


class TestUtilities:
    """Test utility functions."""

    def test_filter_predicate_equality(self, sample_data):
        """Test filter predicate for equality."""
        predicate = create_filter_predicate("name", "Alice")

        matching = [item for item in sample_data if predicate(item)]

        assert len(matching) == 1
        assert matching[0]["name"] == "Alice"

    def test_field_extractor(self, sample_data):
        """Test field extractor."""
        extractor = create_field_extractor(["name", "age"])

        extracted = [extractor(item) for item in sample_data]

        assert len(extracted) == 3
        assert all(set(item.keys()) == {"name", "age"} for item in extracted)


class TestComplexPipelines:
    """Test complex real-world pipeline scenarios."""

    def test_multi_filter_pipeline(self, sample_data):
        """Test multiple filters in sequence."""
        chain = (
            CommandChain(sample_data)
            .filter(lambda x: x["age"] > 20)
            .filter(lambda x: x["city"] != "Los Angeles")
        )

        results = chain.collect()

        assert len(results) == 2
        assert all(item["age"] > 20 for item in results)
        assert all(item["city"] != "Los Angeles" for item in results)

    def test_filter_map_filter_pipeline(self, sample_data):
        """Test alternating filter and map."""
        chain = (
            CommandChain(sample_data)
            .filter(lambda x: x["age"] > 25)
            .map(lambda x: {**x, "age_group": "senior" if x["age"] > 30 else "junior"})
            .filter(lambda x: x["age_group"] == "junior")
        )

        results = chain.collect()

        assert len(results) == 1
        assert results[0]["age_group"] == "junior"

    def test_json_round_trip(self, sample_data):
        """Test JSON parse and format."""
        json_str = json.dumps(sample_data)

        chain = (
            CommandChain(json_str, DataType.JSON)
            .parse_json()
            .filter(lambda x: x["age"] > 25)
            .map(lambda x: x["name"])
            .format_json()
        )

        results = chain.collect()

        assert len(results) > 0
        parsed = json.loads(results[0])
        assert all(isinstance(name, str) for name in parsed)


class TestErrorHandling:
    """Test error handling in pipelines."""

    def test_pipeline_handles_invalid_input(self):
        """Test pipeline handles invalid input gracefully."""
        stages = [JsonParserStage()]
        pipeline = Pipeline(stages)

        results = list(pipeline.execute("{bad json}", DataType.JSON))

        assert any(r.is_error for r in results)

    def test_chain_handles_missing_fields(self):
        """Test chain handles missing fields."""
        data = [{"name": "Alice"}, {"age": 30}]

        chain = CommandChain(data).map(lambda x: x.get("name", "unknown"))
        results = chain.collect()

        assert len(results) == 2
        assert "unknown" in results
