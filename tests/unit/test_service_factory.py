"""Tests for ServiceFactory bot-type routing."""

from pathlib import Path

import pytest

from deia.services.service_factory import ServiceFactory, BotType
from deia.services.llm_service import AnthropicService, OpenAIService, OllamaService
from deia.adapters.claude_code_cli_adapter import ClaudeCodeCLIAdapter
from deia.adapters.codex_cli_adapter import CodexCLIAdapter


def test_get_service_anthropic(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    service = ServiceFactory.get_service("claude", "BOT-001")
    assert isinstance(service, AnthropicService)


def test_get_service_chatgpt(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    service = ServiceFactory.get_service("chatgpt", "BOT-002")
    assert isinstance(service, OpenAIService)


def test_get_service_llama():
    service = ServiceFactory.get_service("llama", "BOT-003")
    assert isinstance(service, OllamaService)


def test_get_service_claude_code(tmp_path: Path):
    adapter = ServiceFactory.get_service("claude-code", "BOT-004", work_dir=tmp_path)
    assert isinstance(adapter, ClaudeCodeCLIAdapter)


def test_get_service_codex(tmp_path: Path):
    adapter = ServiceFactory.get_service("codex", "BOT-005", work_dir=tmp_path)
    assert isinstance(adapter, CodexCLIAdapter)


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ValueError):
        ServiceFactory.get_service("claude", "BOT-001")


def test_is_cli_service():
    assert ServiceFactory.is_cli_service("claude-code")
    assert not ServiceFactory.is_cli_service("chatgpt")


def test_get_supported_types():
    types = ServiceFactory.get_supported_types()
    assert set(types) == {t.value for t in BotType}
