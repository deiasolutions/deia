"""
Unit tests for output_formatter module.

Tests all output formats, filters, sorting, pagination, and file output.
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.deia.output_formatter import (
    JsonFormatter, TableFormatter, CsvFormatter, MarkdownFormatter,
    DataFilter, DataSorter, OutputHandler, OutputOptions
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
def dict_data():
    """Sample dict data."""
    return {"name": "Alice", "age": 30, "city": "New York"}


class TestJsonFormatter:
    """Test JSON output formatter."""

    def test_format_list(self, sample_data):
        """Test formatting list as JSON."""
        formatter = JsonFormatter()
        result = formatter.format(sample_data)

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert len(parsed) == 3
        assert parsed[0]["name"] == "Alice"

    def test_format_dict(self, dict_data):
        """Test formatting dict as JSON."""
        formatter = JsonFormatter()
        result = formatter.format(dict_data)

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["name"] == "Alice"
        assert parsed["age"] == 30

    def test_format_pretty(self, sample_data):
        """Test pretty JSON formatting."""
        formatter = JsonFormatter(pretty=True)
        result = formatter.format(sample_data)

        assert "\n" in result  # Pretty format has newlines

    def test_format_compact(self, sample_data):
        """Test compact JSON formatting."""
        formatter = JsonFormatter(pretty=False)
        result = formatter.format(sample_data)

        # Compact shouldn't have extra newlines
        lines = result.strip().split("\n")
        assert len(lines) <= 2  # Max 2 lines for top-level array


class TestTableFormatter:
    """Test ASCII table formatter."""

    def test_format_list_of_dicts(self, sample_data):
        """Test formatting list of dicts as table."""
        formatter = TableFormatter()
        result = formatter.format(sample_data)

        assert "Alice" in result
        assert "Bob" in result
        assert "Chicago" in result
        assert "|" in result  # Table delimiter

    def test_format_dict(self, dict_data):
        """Test formatting dict as table."""
        formatter = TableFormatter()
        result = formatter.format(dict_data)

        assert "Alice" in result
        assert "30" in result
        assert "New York" in result

    def test_format_empty_list(self):
        """Test formatting empty list."""
        formatter = TableFormatter()
        result = formatter.format([])

        assert "No data" in result


class TestCsvFormatter:
    """Test CSV formatter."""

    def test_format_list(self, sample_data):
        """Test formatting list as CSV."""
        formatter = CsvFormatter()
        result = formatter.format(sample_data)

        assert "Alice" in result
        assert "Bob" in result
        lines = result.strip().split("\n")
        assert len(lines) >= 3  # Header + 3 rows

    def test_format_has_headers(self, sample_data):
        """Test CSV has headers."""
        formatter = CsvFormatter()
        result = formatter.format(sample_data)

        assert "name" in result.split("\n")[0]


class TestMarkdownFormatter:
    """Test Markdown formatter."""

    def test_format_list(self, sample_data):
        """Test formatting list as Markdown table."""
        formatter = MarkdownFormatter()
        result = formatter.format(sample_data)

        assert "|" in result  # Markdown table delimiter
        assert "Alice" in result
        assert "name" in result

    def test_format_dict(self, dict_data):
        """Test formatting dict as Markdown."""
        formatter = MarkdownFormatter()
        result = formatter.format(dict_data)

        assert "**" in result  # Bold markdown
        assert "Alice" in result


class TestDataFilter:
    """Test data filtering."""

    def test_path_filter_single_level(self, sample_data):
        """Test simple path filter."""
        filter_obj = DataFilter(".name")
        result = filter_obj.apply(sample_data[0])

        assert result == "Alice"

    def test_path_filter_list(self, sample_data):
        """Test path filter on list."""
        filter_obj = DataFilter(".city")
        results = [filter_obj.apply(item) for item in sample_data]

        assert "New York" in results
        assert "Los Angeles" in results

    def test_simple_filter_equals(self, sample_data):
        """Test simple equality filter."""
        filter_obj = DataFilter("city=New York")
        result = filter_obj.apply(sample_data)

        assert len(result) == 1
        assert result[0]["name"] == "Alice"

    def test_filter_no_match(self, sample_data):
        """Test filter with no matches."""
        filter_obj = DataFilter("city=Boston")
        result = filter_obj.apply(sample_data)

        assert len(result) == 0


class TestDataSorter:
    """Test data sorting."""

    def test_sort_ascending(self, sample_data):
        """Test ascending sort."""
        sorter = DataSorter(sort_by="age")
        result = sorter.sort(sample_data)

        ages = [item["age"] for item in result]
        assert ages == [25, 30, 35]

    def test_sort_descending(self, sample_data):
        """Test descending sort."""
        sorter = DataSorter(sort_by="age", reverse=True)
        result = sorter.sort(sample_data)

        ages = [item["age"] for item in result]
        assert ages == [35, 30, 25]

    def test_sort_by_string(self, sample_data):
        """Test sorting by string field."""
        sorter = DataSorter(sort_by="name")
        result = sorter.sort(sample_data)

        names = [item["name"] for item in result]
        assert names == ["Alice", "Bob", "Charlie"]

    def test_sort_none(self, sample_data):
        """Test sort with no sort_by returns data unchanged."""
        sorter = DataSorter(sort_by=None)
        result = sorter.sort(sample_data)

        assert result == sample_data


class TestOutputHandler:
    """Test unified output handler."""

    def test_pagination_limit(self, sample_data):
        """Test pagination with limit."""
        options = OutputOptions(format="json", limit=2)
        handler = OutputHandler(options)

        # Manually apply pagination
        result = handler._paginate(sample_data)

        assert len(result) == 2

    def test_pagination_offset(self, sample_data):
        """Test pagination with offset."""
        options = OutputOptions(format="json", offset=1, limit=2)
        handler = OutputHandler(options)

        result = handler._paginate(sample_data)

        assert len(result) == 2
        assert result[0]["name"] == "Bob"

    def test_pagination_offset_only(self, sample_data):
        """Test pagination with offset only."""
        options = OutputOptions(format="json", offset=2)
        handler = OutputHandler(options)

        result = handler._paginate(sample_data)

        assert len(result) == 1
        assert result[0]["name"] == "Charlie"

    def test_output_to_file(self, sample_data):
        """Test outputting to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.json"
            options = OutputOptions(
                format="json",
                output_file=output_file
            )
            handler = OutputHandler(options)
            handler.output(sample_data)

            assert output_file.exists()
            with open(output_file) as f:
                content = json.load(f)
                assert len(content) == 3

    def test_combined_filter_sort_limit(self, sample_data):
        """Test combining filter, sort, and limit."""
        options = OutputOptions(
            format="json",
            sort="age",
            sort_reverse=True,
            limit=1
        )
        handler = OutputHandler(options)

        # Manually apply transforms
        filtered = handler.filter.apply(sample_data)
        sorted_data = handler.sorter.sort(filtered)
        paginated = handler._paginate(sorted_data)

        assert len(paginated) == 1
        assert paginated[0]["name"] == "Charlie"  # Oldest


class TestFormatIntegration:
    """Integration tests for format combinations."""

    def test_json_format_produces_valid_json(self, sample_data):
        """Test JSON format produces valid JSON."""
        formatter = JsonFormatter()
        result = formatter.format(sample_data)

        # Should be parseable
        parsed = json.loads(result)
        assert isinstance(parsed, list)

    def test_table_format_readable(self, sample_data):
        """Test table format is readable."""
        formatter = TableFormatter()
        result = formatter.format(sample_data)

        lines = result.split("\n")
        assert len(lines) >= 5  # Headers + separator + 3 rows

    def test_csv_format_valid(self, sample_data):
        """Test CSV format is valid."""
        formatter = CsvFormatter()
        result = formatter.format(sample_data)

        import csv
        import io

        # Should be readable as CSV
        reader = csv.DictReader(io.StringIO(result))
        rows = list(reader)
        assert len(rows) == 3

    def test_markdown_format_valid(self, sample_data):
        """Test Markdown format."""
        formatter = MarkdownFormatter()
        result = formatter.format(sample_data)

        # Should contain table markers
        assert "|" in result
        assert "-" in result


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_data(self):
        """Test handling empty data."""
        handler = OutputHandler(OutputOptions())
        handler.output([])

        # Should not raise

    def test_none_data(self):
        """Test handling None data."""
        handler = OutputHandler(OutputOptions())
        handler.output(None)

        # Should not raise

    def test_nested_dict_formatting(self):
        """Test formatting nested dictionaries."""
        data = {
            "user": {"name": "Alice", "age": 30},
            "location": {"city": "New York", "state": "NY"}
        }

        formatter = JsonFormatter()
        result = formatter.format(data)

        parsed = json.loads(result)
        assert parsed["user"]["name"] == "Alice"

    def test_special_characters_in_csv(self):
        """Test special characters in CSV."""
        data = [
            {"name": "Alice's Company", "description": "Sells \"widgets\""}
        ]

        formatter = CsvFormatter()
        result = formatter.format(data)

        assert "Alice" in result
        assert "widgets" in result
