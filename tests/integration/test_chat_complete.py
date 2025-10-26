import pytest
from fastapi.testclient import TestClient
from deia.services.chat_interface_app import app, auth_service
from deia.services.llm_service import OpenAIService, AnthropicService


def test_chat_app_runs():
    """Test chat app starts"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_openai_service_available():
    """Test OpenAI service exists and initializes"""
    service = OpenAIService(api_key="test-key")
    assert service is not None
    assert service.model is not None


def test_anthropic_service_available():
    """Test Anthropic service exists and initializes"""
    service = AnthropicService(api_key="test-key")
    assert service is not None
    assert service.model is not None


def test_chat_command_importable():
    """Test deia chat command can be imported"""
    from deia.cli import chat
    assert callable(chat)


def test_websocket_endpoint_exists():
    """Test WebSocket endpoint is accessible with valid JWT"""
    client = TestClient(app)
    # Generate a valid JWT token for testing
    token = auth_service.authenticate("dev-user", "dev-password")
    assert token is not None
    
    with client.websocket_connect(f"/ws?token={token}") as ws:
        # If we get here, WebSocket endpoint exists and accepts valid token
        assert ws is not None
