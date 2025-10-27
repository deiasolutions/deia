"""Unit tests for chat interface API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, Mock
import json
from pathlib import Path

from deia.services.chat_interface_app import app, service_registry
from deia.services.registry import ServiceRegistry


client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_registry(tmp_path, monkeypatch):
    """Ensure registry persistence does not leak across tests."""
    registry_file = tmp_path / "registry.json"
    registry_file.write_text(json.dumps({"bots": {}, "updated_at": "1970-01-01T00:00:00"}))
    monkeypatch.setattr(service_registry, "registry_path", registry_file)
    monkeypatch.setattr(service_registry, "audit_log_path", tmp_path / "registry-changes.jsonl")
    service_registry._save({"bots": {}, "updated_at": "1970-01-01T00:00:00"})
class TestGetBotsEndpoint:
    """Test GET /api/bots endpoint"""

    def test_get_bots_empty(self):
        """Test getting bots when none are registered"""
        with patch.object(ServiceRegistry, 'get_all_bots', return_value={}):
            response = client.get("/api/bots")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["bots"] == {}
            assert "timestamp" in data

    def test_get_bots_with_bots(self):
        """Test getting bots when some are registered"""
        mock_bots = {
            "BOT-001": {
                "status": "idle",
                "port": 8001,
                "registered_at": "2025-10-26T12:00:00",
                "last_heartbeat": "2025-10-26T12:10:00"
            }
        }
        with patch.object(service_registry, 'cleanup_stale_entries'):
            with patch.object(service_registry, 'get_all_bots', return_value=mock_bots):
                response = client.get("/api/bots")
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert "BOT-001" in data["bots"]
                assert data["bots"]["BOT-001"]["port"] == 8001


class TestLaunchBotEndpoint:
    """Test POST /api/bot/launch endpoint"""

    def test_launch_bot_success(self):
        """Test successful bot launch"""
        request_data = {"bot_id": "BOT-001", "bot_type": "claude"}
        with patch.object(service_registry, 'check_duplicate_bot', return_value=False):
            with patch.object(service_registry, 'assign_port', return_value=8001):
                with patch.object(service_registry, 'register', return_value=True):
                    with patch('deia.services.chat_interface_app.spawn_bot_process', return_value=12345):
                        with patch('requests.get') as mock_get:
                            mock_response = MagicMock()
                            mock_response.status_code = 200
                            mock_get.return_value = mock_response

                            response = client.post("/api/bot/launch", json=request_data)
                            assert response.status_code == 200
                            data = response.json()
                            assert data["success"] is True
                            assert data["bot_id"] == "BOT-001"
                            assert data["port"] == 8001
                            assert data["pid"] == 12345

    def test_launch_bot_duplicate(self):
        """Test launching a bot that's already running"""
        request_data = {"bot_id": "BOT-001", "bot_type": "claude"}
        with patch.object(service_registry, 'check_duplicate_bot', return_value=True):
            response = client.post("/api/bot/launch", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "already running" in data["error"]

    def test_launch_bot_empty_id(self):
        """Test launching with empty bot_id"""
        request_data = {"bot_id": "", "bot_type": "claude"}
        response = client.post("/api/bot/launch", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "empty" in data["error"]


class TestStopBotEndpoint:
    """Test POST /api/bot/stop/{bot_id} endpoint"""

    def test_stop_bot_success(self):
        """Test successful bot stop"""
        with patch.object(service_registry, 'get_bot', return_value={"port": 8001, "pid": 12345}):
            with patch.object(service_registry, 'get_bot_url', return_value="http://localhost:8001"):
                with patch('requests.post') as mock_post:
                    mock_post.return_value.status_code = 200
                    with patch.object(service_registry, 'unregister'):
                        response = client.post("/api/bot/stop/BOT-001")
                        assert response.status_code == 200
                        data = response.json()
                        assert data["success"] is True
                        assert data["bot_id"] == "BOT-001"

    def test_stop_bot_not_found(self):
        """Test stopping a bot that doesn't exist"""
        with patch.object(service_registry, 'get_bot', return_value=None):
            response = client.post("/api/bot/stop/BOT-999")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "not found" in data["error"]


class TestBotStatusEndpoint:
    """Test GET /api/bots/status endpoint"""

    def test_get_bots_status_empty(self):
        """Test getting status when no bots registered"""
        with patch.object(ServiceRegistry, 'cleanup_stale_entries'):
            with patch.object(ServiceRegistry, 'get_all_bots', return_value={}):
                response = client.get("/api/bots/status")
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert data["bots"] == {}

    def test_get_bots_status_with_bots(self):
        """Test getting status with running bots"""
        mock_bots = {
            "BOT-001": {
                "status": "idle",
                "port": 8001,
                "registered_at": "2025-10-26T12:00:00"
            }
        }
        with patch.object(service_registry, 'cleanup_stale_entries'):
            with patch.object(service_registry, 'get_all_bots', return_value=mock_bots):
                with patch.object(service_registry, 'get_bot_url', return_value="http://localhost:8001"):
                    response = client.get("/api/bots/status")
                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert "BOT-001" in data["bots"]


class TestChatHistoryEndpoint:
    """Test GET /api/chat/history endpoint"""

    def test_get_chat_history_no_bot_id(self):
        """Test getting history without bot_id parameter"""
        response = client.get("/api/chat/history")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "required" in data["error"]

    def test_get_chat_history_bot_not_found(self):
        """Test getting history for non-existent bot"""
        with patch.object(service_registry, 'get_bot', return_value=None):
            response = client.get("/api/chat/history?bot_id=BOT-999")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["messages"] == []
            assert data["count"] == 0

    def test_get_chat_history_empty(self):
        """Test getting empty history for existing bot"""
        with patch.object(service_registry, 'get_bot', return_value={"port": 8001}):
            response = client.get("/api/chat/history?bot_id=BOT-001")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["messages"] == []


class TestBotTaskEndpoint:
    """Test POST /api/bot/{bot_id}/task endpoint"""

    def test_send_bot_task_success(self):
        """Test sending task to bot"""
        request_data = {"command": "echo hello"}
        mock_service = MagicMock()
        mock_service.chat.return_value = "Hello, world!"

        with patch.object(service_registry, 'get_bot', return_value={"port": 8001, "metadata": {"bot_type": "claude"}}):
            with patch('deia.services.chat_interface_app.ServiceFactory.get_service', return_value=mock_service):
                with patch('deia.services.chat_interface_app.ServiceFactory.is_cli_service', return_value=False):
                    response = client.post("/api/bot/BOT-001/task", json=request_data)
                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert data["bot_type"] == "claude"
                    assert data["response"] == "Hello, world!"
                    mock_service.chat.assert_called_with("echo hello")

    def test_send_bot_task_cli_service(self):
        """Test sending task when bot uses CLI service"""
        request_data = {"command": "build project"}
        mock_service = MagicMock()
        mock_service.session_active = False
        mock_service.start_session.return_value = True
        mock_service.send_task.return_value = {
            "success": True,
            "output": "Done",
            "files_modified": ["main.py"]
        }

        with patch.object(service_registry, 'get_bot', return_value={"metadata": {"bot_type": "claude-code"}}):
            with patch('deia.services.chat_interface_app.ServiceFactory.get_service', return_value=mock_service):
                with patch('deia.services.chat_interface_app.ServiceFactory.is_cli_service', return_value=True):
                    response = client.post("/api/bot/BOT-001/task", json=request_data)
                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert data["bot_type"] == "claude-code"
                    assert data["response"] == "Done"
                    assert data["files_modified"] == ["main.py"]
                    mock_service.start_session.assert_called_once()
                    mock_service.send_task.assert_called_with("build project", timeout=30)

    def test_send_bot_task_empty_command(self):
        """Test sending empty command"""
        request_data = {"command": ""}
        response = client.post("/api/bot/BOT-001/task", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "empty" in data["error"]

    def test_send_bot_task_bot_not_found(self):
        """Test sending task to non-existent bot"""
        request_data = {"command": "echo hello"}
        with patch.object(service_registry, 'get_bot', return_value=None):
            response = client.post("/api/bot/BOT-999/task", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "not found" in data["error"]


class TestEndpointsExist:
    """Test that all required endpoints exist"""

    def test_endpoint_get_bots(self):
        """Test GET /api/bots endpoint exists"""
        response = client.get("/api/bots")
        assert response.status_code == 200

    def test_endpoint_post_launch(self):
        """Test POST /api/bot/launch endpoint exists"""
        with patch.object(service_registry, 'check_duplicate_bot', return_value=True):
            response = client.post("/api/bot/launch", json={"bot_id": "TEST"})
            assert response.status_code == 200

    def test_endpoint_post_stop(self):
        """Test POST /api/bot/stop/{bot_id} endpoint exists"""
        with patch.object(service_registry, 'get_bot', return_value=None):
            response = client.post("/api/bot/stop/TEST")
            assert response.status_code == 200

    def test_endpoint_get_status(self):
        """Test GET /api/bots/status endpoint exists"""
        with patch.object(service_registry, 'cleanup_stale_entries'):
            with patch.object(service_registry, 'get_all_bots', return_value={}):
                response = client.get("/api/bots/status")
                assert response.status_code == 200

    def test_endpoint_get_history(self):
        """Test GET /api/chat/history endpoint exists"""
        response = client.get("/api/chat/history")
        assert response.status_code == 200

    def test_endpoint_post_task(self):
        """Test POST /api/bot/{bot_id}/task endpoint exists"""
        response = client.post("/api/bot/TEST/task", json={"command": ""})
        assert response.status_code == 200
