# REAL TASK: Test & Verify Full Chat Flow
**From:** Q33N
**To:** BOT-004
**Date:** 2025-10-26 11:30 AM CDT
**Priority:** P0 - BLOCKING
**Status:** Waits for BOT-001 + BOT-003

---

## What to do

Write 5 simple integration tests to verify the complete chat flow:

**Create:** `tests/integration/test_chat_complete_flow.py`

```python
import pytest
from fastapi.testclient import TestClient
from deia.services.chat_interface_app import app

def test_chat_server_starts():
    """Verify FastAPI chat app starts"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200

def test_websocket_endpoint_exists():
    """Verify WebSocket endpoint exists"""
    client = TestClient(app)
    with client.websocket_connect("/ws?token=test12345") as ws:
        ws.send_json({"type": "command", "command": "/status"})
        data = ws.receive_json()
        assert "type" in data

def test_openai_service_available():
    """Verify OpenAI service is available"""
    from deia.services.llm_service import OpenAIService
    service = OpenAIService(api_key="test-key")
    assert service is not None

def test_anthropic_service_available():
    """Verify Anthropic service is available (after BOT-001 adds it)"""
    from deia.services.llm_service import AnthropicService
    service = AnthropicService(api_key="test-key")
    assert service is not None

def test_deia_chat_command_exists():
    """Verify deia chat command exists in CLI"""
    from deia.cli import chat
    assert callable(chat)
```

**That's it. Just 5 tests to verify everything connects.**

**Tests:**
- All 5 must pass
- Verify no import errors
- Verify services available
- Verify CLI command exists

**Time:** 15 minutes

**Deliverable:** `.deia/hive/responses/deiasolutions/bot-004-chat-verification-done.md`

Wait for BOT-001 + BOT-003, then run this.
