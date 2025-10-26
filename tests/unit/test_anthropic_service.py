"""Unit tests for AnthropicService"""
import pytest
from deia.services.llm_service import AnthropicService, create_llm_service


def test_anthropic_service_init():
    """Test AnthropicService initializes with defaults"""
    service = AnthropicService(api_key="test-key-12345")
    assert service is not None
    assert service.model == "claude-3-5-sonnet-20240620"


def test_anthropic_service_custom_model():
    """Test AnthropicService initializes with custom model"""
    service = AnthropicService(api_key="test-key", model="claude-3-opus-20240229")
    assert service.model == "claude-3-opus-20240229"


def test_anthropic_service_from_factory():
    """Test AnthropicService can be created via factory function"""
    service = create_llm_service("anthropic", api_key="test-key-12345")
    assert isinstance(service, AnthropicService)
    assert service.model == "claude-3-5-sonnet-20241022"


def test_anthropic_service_has_chat_method():
    """Test AnthropicService has chat method"""
    service = AnthropicService(api_key="test-key-12345")
    assert hasattr(service, 'chat')
    assert callable(service.chat)


def test_anthropic_service_has_async_chat():
    """Test AnthropicService has chat_async method"""
    service = AnthropicService(api_key="test-key-12345")
    assert hasattr(service, 'chat_async')
    assert callable(service.chat_async)
