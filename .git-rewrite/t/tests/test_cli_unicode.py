"""
Tests for Unicode handling in CLI commands

Ensures CLI works on Windows with non-UTF-8 terminals
"""

import pytest
from io import StringIO
import sys
from unittest.mock import patch, MagicMock
from rich.console import Console


def test_safe_print_with_unicode_success():
    """Test safe_print works with UTF-8 supporting terminals"""
    from deia.cli_utils import safe_print

    console = Console(file=StringIO(), force_terminal=True)

    # Should work fine with Unicode
    result = safe_print(console, "[green]\u2713[/green] Success")
    assert result is True  # Returns True on success


def test_safe_print_with_unicode_fallback():
    """Test safe_print falls back to ASCII on encoding error"""
    from deia.cli_utils import safe_print

    # Mock console that raises UnicodeEncodeError
    console = MagicMock()
    console.print.side_effect = [
        UnicodeEncodeError('charmap', '', 0, 1, 'character maps to <undefined>'),
        None  # Second call succeeds with ASCII
    ]

    result = safe_print(console, "[green]\u2713[/green] Success")

    # Should have called print twice (first fails, second with fallback)
    assert console.print.call_count == 2

    # Second call should have ASCII fallback
    second_call_args = console.print.call_args_list[1][0][0]
    assert '[OK]' in second_call_args
    assert '\u2713' not in second_call_args

    assert result is True  # Still returns success


def test_safe_print_replaces_all_unicode_symbols():
    """Test all Unicode symbols are replaced in fallback"""
    from deia.cli_utils import safe_print

    console = MagicMock()
    console.print.side_effect = [
        UnicodeEncodeError('charmap', '', 0, 1, 'error'),
        None
    ]

    message = "\u2713 Success \u2717 Error \u26A0 Warning"
    safe_print(console, message)

    # Get the fallback message
    fallback = console.print.call_args_list[1][0][0]

    assert '[OK]' in fallback      # ✓ → [OK]
    assert '[X]' in fallback        # ✗ → [X]
    assert '[!]' in fallback        # ⚠ → [!]
    assert '\u2713' not in fallback
    assert '\u2717' not in fallback
    assert '\u26A0' not in fallback


def test_safe_print_preserves_rich_markup():
    """Test Rich markup is preserved in fallback"""
    from deia.cli_utils import safe_print

    console = MagicMock()
    console.print.side_effect = [
        UnicodeEncodeError('charmap', '', 0, 1, 'error'),
        None
    ]

    message = "[green]\u2713[/green] [bold]Success[/bold]"
    safe_print(console, message)

    fallback = console.print.call_args_list[1][0][0]

    # Rich markup should be preserved
    assert '[green]' in fallback
    assert '[/green]' in fallback
    assert '[bold]' in fallback
    assert '[/bold]' in fallback

    # But Unicode replaced
    assert '[OK]' in fallback


def test_safe_print_works_in_actual_cli_commands():
    """Integration test: safe_print in sanitize command"""
    # This will be tested after implementation
    pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
