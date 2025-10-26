"""
Output Formatter & Filter System - Advanced formatting for CLI output.

Provides format, filter, sort, pagination, and streaming capabilities for all DEIA commands.
Supports: JSON, YAML, CSV, Table, Markdown formats with jq-like filtering.
"""

from typing import Any, Dict, List, Optional, Iterator, Union, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import json
import csv
import io
import re


# ===== OUTPUT FORMAT SUPPORT =====

class OutputFormat:
    """Base class for output formatters."""

    def format(self, data: Any) -> str:
        """Format data to string."""
        raise NotImplementedError

    def stream_format(self, data_iterator: Iterator) -> Iterator[str]:
        """Stream format for large datasets."""
        raise NotImplementedError


class JsonFormatter(OutputFormat):
    """JSON output formatter."""

    def __init__(self, pretty: bool = True, indent: int = 2):
        self.pretty = pretty
        self.indent = indent

    def format(self, data: Any) -> str:
        """Format as JSON."""
        if self.pretty:
            return json.dumps(self._serialize(data), indent=self.indent)
        return json.dumps(self._serialize(data))

    def stream_format(self, data_iterator: Iterator) -> Iterator[str]:
        """Stream as JSON array."""
        yield "[\n"
        first = True
        for item in data_iterator:
            if not first:
                yield ",\n"
            yield json.dumps(self._serialize(item), indent=2)
            first = False
        yield "\n]"

    def _serialize(self, obj: Any) -> Any:
        """Make object JSON serializable."""
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, dict):
            return {k: self._serialize(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._serialize(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return self._serialize(obj.__dict__)
        else:
            return str(obj)


class TableFormatter(OutputFormat):
    """ASCII table output formatter."""

    def format(self, data: Any) -> str:
        """Format as ASCII table."""
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return self._format_table(data)
        elif isinstance(data, dict):
            return self._format_dict_table(data)
        else:
            return str(data)

    def stream_format(self, data_iterator: Iterator) -> Iterator[str]:
        """Stream as tables."""
        buffer = []
        for item in data_iterator:
            buffer.append(item)
            if len(buffer) >= 50:  # Chunk size
                yield self._format_table(buffer) + "\n"
                buffer = []
        if buffer:
            yield self._format_table(buffer)

    def _format_table(self, data: List[Dict]) -> str:
        """Format list of dicts as table."""
        if not data:
            return "No data"

        # Get column names
        cols = list(data[0].keys())

        # Calculate column widths
        col_widths = {}
        for col in cols:
            col_widths[col] = max(
                len(str(col)),
                max(len(str(row.get(col, ""))) for row in data)
            )

        # Build table
        lines = []
        header = " | ".join(col.ljust(col_widths[col]) for col in cols)
        lines.append(header)
        lines.append("-" * len(header))

        for row in data:
            line = " | ".join(
                str(row.get(col, "")).ljust(col_widths[col]) for col in cols
            )
            lines.append(line)

        return "\n".join(lines)

    def _format_dict_table(self, data: Dict) -> str:
        """Format single dict as 2-column table."""
        lines = ["Key | Value"]
        lines.append("-" * 30)
        for key, value in data.items():
            lines.append(f"{str(key)} | {str(value)}")
        return "\n".join(lines)


class CsvFormatter(OutputFormat):
    """CSV output formatter."""

    def format(self, data: Any) -> str:
        """Format as CSV."""
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return self._format_csv(data)
        return str(data)

    def stream_format(self, data_iterator: Iterator) -> Iterator[str]:
        """Stream as CSV."""
        buffer = []
        headers_written = False
        output = io.StringIO()
        writer = None

        for item in data_iterator:
            if isinstance(item, dict):
                if not headers_written:
                    writer = csv.DictWriter(output, fieldnames=item.keys())
                    writer.writeheader()
                    headers_written = True

                writer.writerow(item)
                buffer.append(item)

                # Flush periodically
                if len(buffer) >= 100:
                    yield output.getvalue()
                    output = io.StringIO()
                    writer = csv.DictWriter(output, fieldnames=item.keys())
                    buffer = []

        if buffer or output.getvalue():
            yield output.getvalue()

    def _format_csv(self, data: List[Dict]) -> str:
        """Format list of dicts as CSV."""
        if not data:
            return ""

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()


class MarkdownFormatter(OutputFormat):
    """Markdown output formatter."""

    def format(self, data: Any) -> str:
        """Format as Markdown."""
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return self._format_markdown_table(data)
        elif isinstance(data, dict):
            return self._format_markdown_dict(data)
        else:
            return f"```\n{str(data)}\n```"

    def stream_format(self, data_iterator: Iterator) -> Iterator[str]:
        """Stream as Markdown tables."""
        yield "# Results\n\n"
        for i, item in enumerate(data_iterator):
            if isinstance(item, dict):
                yield f"## Item {i+1}\n\n"
                yield self._format_markdown_dict(item) + "\n\n"

    def _format_markdown_table(self, data: List[Dict]) -> str:
        """Format as Markdown table."""
        if not data:
            return "No data"

        cols = list(data[0].keys())

        # Build markdown table
        lines = []
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("|" + "|".join(["-" * len(col) for col in cols]) + "|")

        for row in data:
            values = [str(row.get(col, "")) for col in cols]
            lines.append("| " + " | ".join(values) + " |")

        return "\n".join(lines)

    def _format_markdown_dict(self, data: Dict) -> str:
        """Format dict as Markdown."""
        lines = []
        for key, value in data.items():
            lines.append(f"- **{key}:** {str(value)}")
        return "\n".join(lines)


# ===== FILTERING & TRANSFORMATION =====

class DataFilter:
    """Filter and transform data using jq-like syntax."""

    def __init__(self, filter_expr: Optional[str] = None):
        self.filter_expr = filter_expr

    def apply(self, data: Any) -> Any:
        """Apply filter to data."""
        if not self.filter_expr:
            return data

        # Parse simple filter expressions
        if self.filter_expr.startswith("."):
            return self._path_filter(data, self.filter_expr)
        elif "|" in self.filter_expr:
            return self._pipe_filter(data, self.filter_expr)
        else:
            return self._simple_filter(data, self.filter_expr)

    def _path_filter(self, data: Any, path: str) -> Any:
        """Filter by JSON path (e.g., '.key.subkey')."""
        parts = path.split(".")
        current = data

        for part in parts:
            if not part:
                continue
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                # Apply to all items
                current = [self._path_filter(item, "." + part) for item in current]
            else:
                return None

        return current

    def _pipe_filter(self, data: Any, expr: str) -> Any:
        """Apply chained filters."""
        filters = expr.split("|")
        result = data

        for filter_part in filters:
            result = self.apply_single(result, filter_part.strip())

        return result

    def _simple_filter(self, data: Any, expr: str) -> Any:
        """Apply simple filter (key=value)."""
        if "=" in expr:
            key, value = expr.split("=", 1)
            if isinstance(data, list):
                return [item for item in data if isinstance(item, dict) and str(item.get(key)) == value]
        return data

    def apply_single(self, data: Any, expr: str) -> Any:
        """Apply single filter operation."""
        if expr.startswith("."):
            return self._path_filter(data, expr)
        return data


class DataSorter:
    """Sort data by field(s)."""

    def __init__(self, sort_by: Optional[str] = None, reverse: bool = False):
        self.sort_by = sort_by
        self.reverse = reverse

    def sort(self, data: Any) -> Any:
        """Sort data."""
        if not self.sort_by or not isinstance(data, list):
            return data

        return sorted(
            data,
            key=lambda item: self._get_sort_key(item),
            reverse=self.reverse
        )

    def _get_sort_key(self, item: Any) -> Any:
        """Get sort key from item."""
        if isinstance(item, dict):
            return item.get(self.sort_by, "")
        return getattr(item, self.sort_by, "")


# ===== OUTPUT HANDLER =====

@dataclass
class OutputOptions:
    """Output configuration options."""
    format: str = "table"  # json, yaml, csv, table, markdown
    filter: Optional[str] = None
    sort: Optional[str] = None
    sort_reverse: bool = False
    limit: Optional[int] = None
    offset: int = 0
    output_file: Optional[Path] = None
    streaming: bool = False


class OutputHandler:
    """Unified output handling for all commands."""

    def __init__(self, options: OutputOptions):
        self.options = options
        self.formatter = self._get_formatter()
        self.filter = DataFilter(options.filter)
        self.sorter = DataSorter(options.sort, options.sort_reverse)

    def output(self, data: Any) -> None:
        """Output formatted data."""
        # Apply filter
        data = self.filter.apply(data)

        # Apply sort
        data = self.sorter.sort(data)

        # Apply pagination
        data = self._paginate(data)

        # Format
        formatted = self.formatter.format(data)

        # Output
        self._write_output(formatted)

    def output_streaming(self, data_iterator: Iterator) -> None:
        """Output streamed data."""
        # Apply transforms to stream
        transformed = data_iterator
        transformed = self._stream_filter(transformed)
        transformed = self._stream_paginate(transformed)

        # Format stream
        output = self.formatter.stream_format(transformed)

        # Write
        for chunk in output:
            self._write_output(chunk, append=True)

    def _get_formatter(self) -> OutputFormat:
        """Get formatter for selected format."""
        format_map = {
            "json": JsonFormatter(),
            "table": TableFormatter(),
            "csv": CsvFormatter(),
            "markdown": MarkdownFormatter()
        }
        return format_map.get(self.options.format, TableFormatter())

    def _paginate(self, data: Any) -> Any:
        """Apply pagination to data."""
        if not isinstance(data, list):
            return data

        start = self.options.offset
        end = start + self.options.limit if self.options.limit else None

        return data[start:end]

    def _stream_filter(self, data_iterator: Iterator) -> Iterator:
        """Apply filter to stream."""
        for item in data_iterator:
            filtered = self.filter.apply(item)
            if filtered is not None:
                yield filtered

    def _stream_paginate(self, data_iterator: Iterator) -> Iterator:
        """Apply pagination to stream."""
        for i, item in enumerate(data_iterator):
            if i < self.options.offset:
                continue
            if self.options.limit and i >= self.options.offset + self.options.limit:
                break
            yield item

    def _write_output(self, content: str, append: bool = False) -> None:
        """Write output to file or stdout."""
        if self.options.output_file:
            mode = "a" if append else "w"
            with open(self.options.output_file, mode) as f:
                f.write(content)
        else:
            print(content)


# ===== CLI INTEGRATION HELPERS =====

def add_output_options(command):
    """Decorator to add output options to a Click command."""
    import click

    def decorator(func):
        # Add output options
        func = click.option("--format", type=click.Choice(["json", "yaml", "csv", "table", "markdown"]),
                           default="table", help="Output format")(func)
        func = click.option("--filter", help="Filter results (jq-like syntax)")(func)
        func = click.option("--sort", help="Sort by field")(func)
        func = click.option("--sort-reverse", is_flag=True, help="Sort in reverse")(func)
        func = click.option("--limit", type=int, help="Limit results")(func)
        func = click.option("--offset", type=int, default=0, help="Offset for pagination")(func)
        func = click.option("--output", type=click.Path(), help="Output to file")(func)
        func = click.option("--streaming", is_flag=True, help="Stream large result sets")(func)
        return func

    return decorator


def create_output_handler(
    format: str = "table",
    filter: Optional[str] = None,
    sort: Optional[str] = None,
    sort_reverse: bool = False,
    limit: Optional[int] = None,
    offset: int = 0,
    output: Optional[str] = None,
    streaming: bool = False
) -> OutputHandler:
    """Create output handler from CLI options."""
    output_file = Path(output) if output else None

    options = OutputOptions(
        format=format,
        filter=filter,
        sort=sort,
        sort_reverse=sort_reverse,
        limit=limit,
        offset=offset,
        output_file=output_file,
        streaming=streaming
    )

    return OutputHandler(options)
