# FOCUSED TASK - BOT-004: Verify All Components Work
**Priority:** P0 BLOCKING
**Time:** 15 minutes
**Start:** When BOT-001 AND BOT-003 are done
**Blocker:** Waits for BOT-001 + BOT-003

---

## EXACTLY what to do:

### 1. Create `tests/integration/test_chat_complete.py`:
```python
import pytest
from fastapi.testclient import TestClient
from deia.services.chat_interface_app import app
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
    """Test WebSocket endpoint is accessible"""
    client = TestClient(app)
    with client.websocket_connect("/ws?token=test12345") as ws:
        # If we get here, WebSocket endpoint exists
        assert ws is not None
```

### 2. Run ALL tests:
```bash
# Run the new verification tests
pytest tests/integration/test_chat_complete.py -v

# Run ALL unit tests to ensure nothing broke
pytest tests/unit/ -v --tb=short
```

ALL tests must PASS (both new integration tests and existing unit tests).

---

## DONE - Report completion:
Create: `.deia/hive/responses/deiasolutions/bot-004-chat-verification-done.md`

Write:
- All 5 integration tests passing
- All unit tests still passing
- Chat system complete and ready for user UAT

---

## NO OTHER WORK. Just this.
