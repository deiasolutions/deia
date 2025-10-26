import pytest
from click.testing import CliRunner
from deia.cli import chat


def test_chat_command_exists():
    """Test chat command exists"""
    assert callable(chat)


def test_chat_help():
    """Test chat command help"""
    runner = CliRunner()
    result = runner.invoke(chat, ['--help'])
    assert result.exit_code == 0
    assert 'chat' in result.output.lower()


def test_chat_port_option():
    """Test chat command accepts port option"""
    runner = CliRunner()
    # Don't actually run, just test the option exists
    result = runner.invoke(chat, ['--help'])
    assert '--port' in result.output


def test_chat_no_browser_option():
    """Test chat command accepts no-browser option"""
    runner = CliRunner()
    result = runner.invoke(chat, ['--help'])
    assert '--no-browser' in result.output
