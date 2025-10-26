import asyncio
from types import SimpleNamespace

import pytest

from deia.services.llm_service import (
    AnthropicService,
    ConversationHistory,
    create_llm_service,
)


class DummyUsage(SimpleNamespace):
    input_tokens: int = 10
    output_tokens: int = 20


def make_response(text="hi", input_tokens=10, output_tokens=20, response_id="resp-1"):
    content = [SimpleNamespace(text=text)]
    usage = DummyUsage(input_tokens=input_tokens, output_tokens=output_tokens)
    return SimpleNamespace(content=content, usage=usage, stop_reason="end", id=response_id)


class DummyStreamContext:
    def __init__(self, events):
        self.events = list(events)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.events:
            raise StopAsyncIteration
        return self.events.pop(0)


class DummyStreamNoContext:
    def __init__(self, events):
        self.events = list(events)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.events:
            raise StopAsyncIteration
        return self.events.pop(0)


class DummySyncMessages:
    def __init__(self):
        self.responses = []
        self.errors = []
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.errors:
            exc = self.errors.pop(0)
            raise exc
        if self.responses:
            return self.responses.pop(0)
        return make_response()


class DummyAsyncMessages(DummySyncMessages):
    def __init__(self):
        super().__init__()
        self.stream_events = []
        self.use_context_manager = True

    async def create(self, **kwargs):
        return super().create(**kwargs)

    def stream(self, **kwargs):
        events = list(self.stream_events)
        if self.use_context_manager:
            return DummyStreamContext(events)
        return DummyStreamNoContext(events)


@pytest.fixture
def anthropic_stub(monkeypatch):
    sync_messages = DummySyncMessages()
    async_messages = DummyAsyncMessages()

    class DummyModule:
        pass

    def build_sync_client(*args, **kwargs):
        return SimpleNamespace(messages=sync_messages)

    def build_async_client(*args, **kwargs):
        return SimpleNamespace(messages=async_messages)

    module = DummyModule()
    module.Anthropic = build_sync_client
    module.AsyncAnthropic = build_async_client

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    monkeypatch.setattr(
        "deia.services.llm_service._get_anthropic_module",
        lambda: module,
        raising=False,
    )

    return SimpleNamespace(
        module=module,
        sync_messages=sync_messages,
        async_messages=async_messages,
        rate_limit_error=type("DummyRateLimitError", (Exception,), {"__name__": "RateLimitError"}),
        timeout_error=type("DummyTimeout", (Exception,), {"__name__": "RequestTimeout"}),
    )


def test_service_initialization_with_env_key(anthropic_stub):
    service = AnthropicService()
    assert service.available is True
    assert service.anthropic_client is not None
    assert service.anthropic_async_client is not None


def test_service_missing_api_key_sets_disabled(monkeypatch, anthropic_stub):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    service = AnthropicService(api_key=None)
    assert service.available is False
    assert service.disabled_reason == "missing_api_key"
    result = service.chat("hello")
    assert result["error"] == "missing_api_key"


def test_service_module_missing(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    monkeypatch.setattr("deia.services.llm_service._get_anthropic_module", lambda: None, raising=False)
    service = AnthropicService()
    assert service.available is False
    assert service.disabled_reason == "module_missing"
    result = service.chat("hello")
    assert result["error"] == "module_missing"


def test_chat_success_appends_history(anthropic_stub):
    anthropic_stub.sync_messages.responses.append(make_response("Hi Dave"))
    service = AnthropicService()
    result = service.chat("Hello?")
    assert result["content"] == "Hi Dave"
    history = service.history.get_messages()
    assert history[-2]["role"] == "user"
    assert history[-1]["role"] == "assistant"


def test_chat_respects_external_history(anthropic_stub):
    anthropic_stub.sync_messages.responses.append(make_response("Reply"))
    service = AnthropicService()
    convo = [{"role": "assistant", "content": "Prev"}]
    result = service.chat("Hi", conversation_history=convo)
    assert result["success"] is True
    # ensure internal history unchanged because external history supplied
    assert service.history.get_messages() == []


def test_chat_enforces_token_limit(anthropic_stub):
    service = AnthropicService()
    service.history.max_tokens = 1
    result = service.chat("x" * 20000)
    assert result["error"] == "token_limit"


def test_chat_rejects_invalid_message(anthropic_stub):
    service = AnthropicService()
    result = service.chat("   ")
    assert result["error"] == "invalid_message"


@pytest.mark.asyncio
async def test_chat_async_success(anthropic_stub):
    anthropic_stub.async_messages.responses.append(make_response("Async hi"))
    service = AnthropicService()
    result = await service.chat_async("Ping")
    assert result["content"] == "Async hi"
    assert result["success"] is True


@pytest.mark.asyncio
async def test_chat_stream_yields_chunks_with_context_manager(anthropic_stub):
    events = [
        {"type": "content_block_delta", "delta": {"text": "Hel"}},
        {"type": "content_block_delta", "delta": {"text": "lo"}},
    ]
    anthropic_stub.async_messages.stream_events = events
    service = AnthropicService()
    chunks = []
    async for chunk in service.chat_stream("Stream?"):
        chunks.append(chunk)
    assert "".join(chunks) == "Hello"


@pytest.mark.asyncio
async def test_chat_stream_without_context_manager(anthropic_stub):
    anthropic_stub.async_messages.use_context_manager = False
    anthropic_stub.async_messages.stream_events = [
        {"type": "content_block_delta", "delta": {"text": "Hi"}},
    ]
    service = AnthropicService()
    chunks = []
    async for chunk in service.chat_stream("Test"):
        chunks.append(chunk)
    assert chunks == ["Hi"]


@pytest.mark.asyncio
async def test_chat_stream_token_limit_error(anthropic_stub):
    service = AnthropicService()
    service.history.max_tokens = 1
    chunks = []
    async for chunk in service.chat_stream("x" * 20000):
        chunks.append(chunk)
    assert "token limit" in chunks[0].lower()


def test_rate_limit_retry_recovers(anthropic_stub):
    anthropic_stub.sync_messages.errors.append(anthropic_stub.rate_limit_error("slow down"))
    anthropic_stub.sync_messages.responses.append(make_response("After retry"))
    service = AnthropicService(max_retries=2)
    result = service.chat("Retry please")
    assert result["success"] is True
    assert len(anthropic_stub.sync_messages.calls) == 2


def test_error_mapping_rate_limit(anthropic_stub):
    service = AnthropicService()
    exc = anthropic_stub.rate_limit_error("oops")
    assert service._map_anthropic_error(exc) == "rate_limit"


def test_factory_supports_anthropic_provider(anthropic_stub):
    svc = create_llm_service("anthropic", api_key="sk-test")
    assert isinstance(svc, AnthropicService)


def test_conversation_history_trim():
    history = ConversationHistory(max_messages=2, max_tokens=10)
    history.add_message("user", "a" * 100)
    history.add_message("assistant", "b" * 100)
    history.add_message("user", "c" * 10)
    assert len([m for m in history.get_messages() if m["role"] != "system"]) == 2
