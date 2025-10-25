"""
Tests for CLI Utility Functions
"""

import pytest
from unittest.mock import MagicMock, patch
from rich.console import Console
from src.deia.cli_utils import safe_print, emergency_print, get_symbol, UNICODE_FALLBACKS


class TestSafePrint:
    """Tests for safe_print function"""

    def test_safe_print_success(self):
        """Test safe_print succeeds with normal message"""
        console = MagicMock(spec=Console)
        result = safe_print(console, "Test message")

        assert result is True
        console.print.assert_called_once_with("Test message")

    def test_safe_print_with_unicode(self):
        """Test safe_print succeeds with unicode symbols"""
        console = MagicMock(spec=Console)
        result = safe_print(console, "✓ Success")

        assert result is True
        console.print.assert_called_once_with("✓ Success")

    def test_safe_print_unicode_fallback(self):
        """Test safe_print falls back to ASCII when UnicodeEncodeError occurs"""
        console = MagicMock(spec=Console)
        # First call raises UnicodeEncodeError, second succeeds
        console.print.side_effect = [
            UnicodeEncodeError('charmap', '', 0, 1, 'error'),
            None
        ]

        result = safe_print(console, "✓ Success")

        assert result is True
        # Should have been called twice: once with unicode, once with ASCII fallback
        assert console.print.call_count == 2
        # Second call should have ASCII replacement
        second_call_args = console.print.call_args_list[1][0][0]
        assert "[OK]" in second_call_args
        assert "✓" not in second_call_args

    def test_safe_print_error_handler_doesnt_crash(self, capsys):
        """Test error handler itself is safe (BUG-004 regression test)"""
        console = MagicMock(spec=Console)
        # Mock console that always fails (even on fallback)
        console.print.side_effect = UnicodeEncodeError('charmap', '', 0, 1, 'error')

        # Should NOT crash - this is the key test for BUG-004
        result = safe_print(console, "Test message with ✓")

        # Should return False but not raise
        assert result is False

        # Should have used emergency_print (stderr)
        captured = capsys.readouterr()
        assert "Test message" in captured.err
        # Unicode should be replaced in emergency print
        assert "[OK]" in captured.err or "Test message" in captured.err

    def test_safe_print_generic_exception(self, capsys):
        """Test safe_print handles generic exceptions safely"""
        console = MagicMock(spec=Console)
        # Simulate a different type of error
        console.print.side_effect = RuntimeError("Something went wrong")

        result = safe_print(console, "Test message")

        # Should return False but not crash
        assert result is False

        # Should print error to stderr via emergency_print
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_safe_print_with_rich_markup(self):
        """Test safe_print works with Rich markup"""
        console = MagicMock(spec=Console)
        result = safe_print(console, "[green]Success[/green]")

        assert result is True
        console.print.assert_called_once_with("[green]Success[/green]")

    def test_safe_print_with_kwargs(self):
        """Test safe_print passes kwargs to console.print"""
        console = MagicMock(spec=Console)
        result = safe_print(console, "Test", style="bold", end="")

        assert result is True
        console.print.assert_called_once_with("Test", style="bold", end="")


class TestEmergencyPrint:
    """Tests for emergency_print function"""

    def test_emergency_print_basic(self, capsys):
        """Test emergency_print outputs to stderr"""
        emergency_print("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.err

    def test_emergency_print_strips_rich_markup(self, capsys):
        """Test emergency_print removes Rich markup tags"""
        emergency_print("[green]Success[/green] with [bold]markup[/bold]")

        captured = capsys.readouterr()
        # Markup should be stripped
        assert "[green]" not in captured.err
        assert "[/green]" not in captured.err
        assert "[bold]" not in captured.err
        assert "[/bold]" not in captured.err
        # Content should remain
        assert "Success" in captured.err
        assert "markup" in captured.err

    def test_emergency_print_replaces_unicode(self, capsys):
        """Test emergency_print replaces unicode symbols with ASCII"""
        emergency_print("✓ Success ✗ Failed ⚠ Warning")

        captured = capsys.readouterr()
        # Unicode should be replaced
        assert "✓" not in captured.err
        assert "[OK]" in captured.err
        assert "[X]" in captured.err
        assert "[!]" in captured.err

    def test_emergency_print_combined(self, capsys):
        """Test emergency_print handles both Rich markup and unicode"""
        emergency_print("[green]✓ Success[/green]")

        captured = capsys.readouterr()
        # Rich markup stripped
        assert "[green]" not in captured.err
        # Unicode replaced
        assert "✓" not in captured.err
        assert "[OK]" in captured.err or "Success" in captured.err


class TestGetSymbol:
    """Tests for get_symbol function"""

    def test_get_symbol_checkmark_unicode(self):
        """Test get_symbol returns unicode checkmark by default"""
        symbol = get_symbol('checkmark')
        assert symbol == '✓'

    def test_get_symbol_checkmark_ascii(self):
        """Test get_symbol returns ASCII checkmark when requested"""
        symbol = get_symbol('checkmark', fallback_ascii=True)
        assert symbol == '[OK]'

    def test_get_symbol_cross_unicode(self):
        """Test get_symbol returns unicode cross"""
        symbol = get_symbol('cross')
        assert symbol == '✗'

    def test_get_symbol_cross_ascii(self):
        """Test get_symbol returns ASCII cross"""
        symbol = get_symbol('cross', fallback_ascii=True)
        assert symbol == '[X]'

    def test_get_symbol_warning_unicode(self):
        """Test get_symbol returns unicode warning"""
        symbol = get_symbol('warning')
        assert symbol == '⚠'

    def test_get_symbol_warning_ascii(self):
        """Test get_symbol returns ASCII warning"""
        symbol = get_symbol('warning', fallback_ascii=True)
        assert symbol == '[!]'

    def test_get_symbol_unknown(self):
        """Test get_symbol returns ? for unknown symbols"""
        symbol = get_symbol('unknown')
        assert symbol == '?'


class TestUnicodeFallbacks:
    """Tests for UNICODE_FALLBACKS mapping"""

    def test_unicode_fallbacks_exist(self):
        """Test UNICODE_FALLBACKS dictionary is defined"""
        assert UNICODE_FALLBACKS is not None
        assert isinstance(UNICODE_FALLBACKS, dict)
        assert len(UNICODE_FALLBACKS) > 0

    def test_unicode_fallbacks_checkmarks(self):
        """Test checkmark symbols have ASCII fallbacks"""
        assert '\u2713' in UNICODE_FALLBACKS  # ✓
        assert '\u2714' in UNICODE_FALLBACKS  # ✔
        assert '\u2705' in UNICODE_FALLBACKS  # ✅

    def test_unicode_fallbacks_crosses(self):
        """Test cross symbols have ASCII fallbacks"""
        assert '\u2717' in UNICODE_FALLBACKS  # ✗
        assert '\u2718' in UNICODE_FALLBACKS  # ✘
        assert '\u274C' in UNICODE_FALLBACKS  # ❌

    def test_unicode_fallbacks_warning(self):
        """Test warning symbol has ASCII fallback"""
        assert '\u26A0' in UNICODE_FALLBACKS  # ⚠
