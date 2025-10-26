"""
Command Composition & Piping System - Enable Unix-style pipes between DEIA commands.

Allows powerful command chaining: `deia list | deia filter | deia extract`
with proper error handling, buffering, and performance optimization.
"""

from typing import Any, Iterator, Callable, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json
import sys
import io


# ===== PIPING FRAMEWORK =====

class DataType(Enum):
    """Data types that can flow through pipes."""
    JSON = "json"
    JSONL = "jsonl"  # JSON Lines
    CSV = "csv"
    LINES = "lines"  # Plain text lines
    STRUCTURED = "structured"  # Python objects


@dataclass
class PipeFrame:
    """A frame of data flowing through a pipe."""
    data: Any
    data_type: DataType
    metadata: Dict[str, Any] = None
    is_error: bool = False
    error_message: Optional[str] = None


class PipelineStage:
    """Base class for pipeline stages (commands in a pipe)."""

    def __init__(self, name: str):
        self.name = name
        self.input_type = DataType.STRUCTURED
        self.output_type = DataType.STRUCTURED

    def process(self, frame: PipeFrame) -> Iterator[PipeFrame]:
        """Process a data frame and yield result frames."""
        raise NotImplementedError

    def validate_input(self, frame: PipeFrame) -> bool:
        """Validate input frame."""
        return frame.data_type == self.input_type or frame.data_type == DataType.STRUCTURED


class JsonParserStage(PipelineStage):
    """Parse JSON input into Python objects."""

    def __init__(self):
        super().__init__("json-parser")
        self.input_type = DataType.JSON
        self.output_type = DataType.STRUCTURED

    def process(self, frame: PipeFrame) -> Iterator[PipeFrame]:
        """Parse JSON string to Python object."""
        if isinstance(frame.data, str):
            try:
                data = json.loads(frame.data)
                yield PipeFrame(
                    data=data,
                    data_type=self.output_type,
                    metadata=frame.metadata
                )
            except json.JSONDecodeError as e:
                yield PipeFrame(
                    data=frame.data,
                    data_type=frame.data_type,
                    is_error=True,
                    error_message=f"JSON parse error: {str(e)}"
                )
        else:
            yield frame


class JsonLinesParserStage(PipelineStage):
    """Parse JSON Lines input (one JSON object per line)."""

    def __init__(self):
        super().__init__("jsonl-parser")
        self.input_type = DataType.JSONL
        self.output_type = DataType.STRUCTURED

    def process(self, frame: PipeFrame) -> Iterator[PipeFrame]:
        """Parse JSONL lines to Python objects."""
        if isinstance(frame.data, str):
            for line in frame.data.strip().split("\n"):
                if line:
                    try:
                        data = json.loads(line)
                        yield PipeFrame(
                            data=data,
                            data_type=self.output_type,
                            metadata=frame.metadata
                        )
                    except json.JSONDecodeError as e:
                        yield PipeFrame(
                            data=line,
                            data_type=frame.data_type,
                            is_error=True,
                            error_message=f"JSONL parse error: {str(e)}"
                        )
        else:
            yield frame


class FilterStage(PipelineStage):
    """Filter data based on predicate function."""

    def __init__(self, predicate: Callable[[Any], bool], name: str = "filter"):
        super().__init__(name)
        self.predicate = predicate
        self.input_type = DataType.STRUCTURED
        self.output_type = DataType.STRUCTURED

    def process(self, frame: PipeFrame) -> Iterator[PipeFrame]:
        """Filter data through predicate."""
        if frame.is_error:
            yield frame
            return

        if isinstance(frame.data, list):
            filtered = [item for item in frame.data if self.predicate(item)]
            yield PipeFrame(
                data=filtered,
                data_type=self.output_type,
                metadata=frame.metadata
            )
        elif self.predicate(frame.data):
            yield frame


class TransformStage(PipelineStage):
    """Transform data using a mapper function."""

    def __init__(self, mapper: Callable[[Any], Any], name: str = "transform"):
        super().__init__(name)
        self.mapper = mapper
        self.input_type = DataType.STRUCTURED
        self.output_type = DataType.STRUCTURED

    def process(self, frame: PipeFrame) -> Iterator[PipeFrame]:
        """Transform data through mapper."""
        if frame.is_error:
            yield frame
            return

        try:
            if isinstance(frame.data, list):
                mapped = [self.mapper(item) for item in frame.data]
            else:
                mapped = self.mapper(frame.data)

            yield PipeFrame(
                data=mapped,
                data_type=self.output_type,
                metadata=frame.metadata
            )
        except Exception as e:
            yield PipeFrame(
                data=frame.data,
                data_type=frame.data_type,
                is_error=True,
                error_message=f"Transform error: {str(e)}"
            )


class JsonFormatterStage(PipelineStage):
    """Convert Python objects to JSON string."""

    def __init__(self, pretty: bool = False):
        super().__init__("json-formatter")
        self.pretty = pretty
        self.input_type = DataType.STRUCTURED
        self.output_type = DataType.JSON

    def process(self, frame: PipeFrame) -> Iterator[PipeFrame]:
        """Convert to JSON string."""
        if frame.is_error:
            yield frame
            return

        try:
            if self.pretty:
                json_str = json.dumps(frame.data, indent=2)
            else:
                json_str = json.dumps(frame.data)

            yield PipeFrame(
                data=json_str,
                data_type=self.output_type,
                metadata=frame.metadata
            )
        except Exception as e:
            yield PipeFrame(
                data=frame.data,
                data_type=frame.data_type,
                is_error=True,
                error_message=f"JSON format error: {str(e)}"
            )


# ===== PIPELINE =====

class Pipeline:
    """Compose multiple stages into a processing pipeline."""

    def __init__(self, stages: List[PipelineStage], buffer_size: int = 1000):
        self.stages = stages
        self.buffer_size = buffer_size
        self.frame_count = 0
        self.error_count = 0

    def execute(self, input_data: Any, input_type: DataType = DataType.STRUCTURED) -> Iterator[PipeFrame]:
        """Execute pipeline with input data."""
        # Create initial frame
        initial_frame = PipeFrame(
            data=input_data,
            data_type=input_type,
            metadata={"pipeline_start": True}
        )

        # Execute through all stages
        frames = [initial_frame]

        for stage in self.stages:
            new_frames = []

            for frame in frames:
                # Validate input
                if not stage.validate_input(frame) and not frame.is_error:
                    frame = PipeFrame(
                        data=frame.data,
                        data_type=frame.data_type,
                        is_error=True,
                        error_message=f"Input type mismatch for {stage.name}"
                    )

                # Process through stage
                for output_frame in stage.process(frame):
                    self.frame_count += 1

                    if output_frame.is_error:
                        self.error_count += 1

                    new_frames.append(output_frame)

                    # Yield immediately for streaming
                    yield output_frame

            frames = new_frames

    def execute_buffered(self, input_data: Any, input_type: DataType = DataType.STRUCTURED) -> List[PipeFrame]:
        """Execute pipeline with buffering (non-streaming)."""
        results = []

        for frame in self.execute(input_data, input_type):
            results.append(frame)

            if len(results) > self.buffer_size:
                # Too many results, return early
                results.append(PipeFrame(
                    data=None,
                    data_type=DataType.STRUCTURED,
                    is_error=True,
                    error_message=f"Pipeline result exceeded buffer size {self.buffer_size}"
                ))
                break

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline execution statistics."""
        return {
            "frames_processed": self.frame_count,
            "errors": self.error_count,
            "error_rate": self.error_count / max(self.frame_count, 1)
        }


# ===== COMMAND CHAIN BUILDER =====

class CommandChain:
    """Build command chains with a fluent interface."""

    def __init__(self, input_data: Any, input_type: DataType = DataType.STRUCTURED):
        self.pipeline = Pipeline([])
        self.input_data = input_data
        self.input_type = input_type

    def parse_json(self) -> "CommandChain":
        """Add JSON parser stage."""
        self.pipeline.stages.append(JsonParserStage())
        return self

    def parse_jsonl(self) -> "CommandChain":
        """Add JSON Lines parser stage."""
        self.pipeline.stages.append(JsonLinesParserStage())
        return self

    def filter(self, predicate: Callable[[Any], bool]) -> "CommandChain":
        """Add filter stage."""
        self.pipeline.stages.append(FilterStage(predicate))
        return self

    def map(self, mapper: Callable[[Any], Any]) -> "CommandChain":
        """Add transform stage."""
        self.pipeline.stages.append(TransformStage(mapper))
        return self

    def format_json(self, pretty: bool = False) -> "CommandChain":
        """Add JSON formatter stage."""
        self.pipeline.stages.append(JsonFormatterStage(pretty))
        return self

    def add_stage(self, stage: PipelineStage) -> "CommandChain":
        """Add custom stage."""
        self.pipeline.stages.append(stage)
        return self

    def execute(self) -> Iterator[PipeFrame]:
        """Execute the pipeline."""
        return self.pipeline.execute(self.input_data, self.input_type)

    def execute_buffered(self) -> List[PipeFrame]:
        """Execute with buffering."""
        return self.pipeline.execute_buffered(self.input_data, self.input_type)

    def collect(self) -> List[Any]:
        """Collect all results into a list, flattening frame data."""
        results = []
        for frame in self.execute_buffered():
            if not frame.is_error and frame.data is not None:
                # If data is a list, flatten it
                if isinstance(frame.data, list):
                    results.extend(frame.data)
                else:
                    results.append(frame.data)
        return results

    def collect_single(self) -> Any:
        """Collect single result."""
        results = self.collect()
        return results[0] if results else None


# ===== EXAMPLES & UTILITIES =====

def create_filter_predicate(field: str, value: Any) -> Callable[[Any], bool]:
    """Create a filter predicate for field equality."""
    def predicate(item):
        if isinstance(item, dict):
            return item.get(field) == value
        return False

    return predicate


def create_field_extractor(fields: List[str]) -> Callable[[Any], Dict[str, Any]]:
    """Create a mapper that extracts specific fields."""
    def mapper(item):
        if isinstance(item, dict):
            return {field: item.get(field) for field in fields}
        return item

    return mapper
