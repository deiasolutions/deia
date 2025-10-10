"""
CLI Utility Functions

Helper functions for DEIA CLI commands
"""

from typing import Any
from rich.console import Console


# Unicode symbol mappings for fallback
UNICODE_FALLBACKS = {
    '\u2713': '[OK]',      # ✓ checkmark
    '\u2717': '[X]',       # ✗ cross mark
    '\u26A0': '[!]',       # ⚠ warning
    '\u2714': '[OK]',      # ✔ heavy checkmark
    '\u2718': '[X]',       # ✘ heavy cross
    '\u274C': '[X]',       # ❌ cross mark button
    '\u2705': '[OK]',      # ✅ check mark button
}


def safe_print(console: Console, message: str, **kwargs) -> bool:
    """
    Print message to console with Unicode fallback for Windows terminals

    Attempts to print the message. If UnicodeEncodeError occurs (common on
    Windows terminals with cp1252 encoding), replaces Unicode symbols with
    ASCII-safe alternatives and retries.

    Args:
        console: Rich Console instance
        message: Message to print (may contain Unicode and Rich markup)
        **kwargs: Additional arguments to pass to console.print()

    Returns:
        bool: True if print succeeded (with or without fallback)

    Example:
        >>> from rich.console import Console
        >>> console = Console()
        >>> safe_print(console, "[green]✓[/green] Success")
        True
    """
    try:
        # First attempt: print as-is (works on UTF-8 terminals)
        console.print(message, **kwargs)
        return True

    except UnicodeEncodeError:
        # Fallback: replace Unicode symbols with ASCII
        fallback_message = message

        for unicode_char, ascii_replacement in UNICODE_FALLBACKS.items():
            fallback_message = fallback_message.replace(unicode_char, ascii_replacement)

        # Retry with ASCII-safe message
        try:
            console.print(fallback_message, **kwargs)
            return True
        except Exception as e:
            # If still fails, something else is wrong
            console.print(f"[red]Error printing message:[/red] {e}")
            return False

    except Exception as e:
        # Catch any other errors
        console.print(f"[red]Unexpected error:[/red] {e}")
        return False


def get_symbol(symbol_name: str, fallback_ascii: bool = False) -> str:
    """
    Get a display symbol with optional ASCII fallback

    Args:
        symbol_name: Name of symbol ('checkmark', 'cross', 'warning')
        fallback_ascii: If True, return ASCII version

    Returns:
        str: Unicode symbol or ASCII fallback

    Example:
        >>> get_symbol('checkmark')
        '✓'
        >>> get_symbol('checkmark', fallback_ascii=True)
        '[OK]'
    """
    symbols = {
        'checkmark': ('\u2713', '[OK]'),
        'cross': ('\u2717', '[X]'),
        'warning': ('\u26A0', '[!]'),
    }

    if symbol_name not in symbols:
        return '?'

    unicode_sym, ascii_sym = symbols[symbol_name]
    return ascii_sym if fallback_ascii else unicode_sym
