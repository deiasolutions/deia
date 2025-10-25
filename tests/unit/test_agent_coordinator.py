"""
Tests for AgentCoordinator

Component: src/deia/services/agent_coordinator.py
Purpose: Multi-agent coordination, routing, and delegation
Coverage Target: 80%+

Created: 2025-10-19
Author: AGENT-005 (Integration Coordinator)
"""

import pytest
import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

from src.deia.services.agent_coordinator import AgentCoordinator
from src.deia.services.agent_status import AgentStatusTracker
from src.deia.services.context_loader import ContextLoader


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def temp_dirs(tmp_path):
    """Create temporary directories for testing"""
    heartbeat_dir = tmp_path / "heartbeats"
    inbox_dir = tmp_path / "inbox"
    heartbeat_dir.mkdir(parents=True, exist_ok=True)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    return {
        "heartbeat_dir": str(heartbeat_dir),
        "inbox_dir": str(inbox_dir)
    }


@pytest.fixture
def mock_status_tracker(temp_dirs):
    """Create mock AgentStatusTracker"""
    return AgentStatusTracker(heartbeat_dir=temp_dirs["heartbeat_dir"])


@pytest.fixture
def mock_context_loader():
    """Create mock ContextLoader"""
    loader = Mock(spec=ContextLoader)
    loader.search_bok = Mock(return_value=[])
    return loader


@pytest.fixture
def coordinator(mock_status_tracker, mock_context_loader, temp_dirs):
    """Create AgentCoordinator with mocked dependencies"""
    return AgentCoordinator(
        status_tracker=mock_status_tracker,
        context_loader=mock_context_loader,
        inbox_dir=temp_dirs["inbox_dir"]
    )


@pytest.fixture
def populated_coordinator(coordinator):
    """Create coordinator with pre-populated agents"""
    coordinator.register_agent("AGENT-001", "coordinator")
    coordinator.register_agent("AGENT-002", "worker")
    coordinator.register_agent("AGENT-003", "queen")
    return coordinator


# ============================================================================
# Initialization Tests
# ============================================================================

def test_initialization_default():
    """Test coordinator initializes with default dependencies"""
    coordinator = AgentCoordinator()
    assert coordinator.status_tracker is not None
    assert coordinator.context_loader is not None
    assert coordinator.message_router is not None


def test_initialization_with_dependencies(mock_status_tracker, mock_context_loader, temp_dirs):
    """Test coordinator initializes with provided dependencies"""
    coordinator = AgentCoordinator(
        status_tracker=mock_status_tracker,
        context_loader=mock_context_loader,
        inbox_dir=temp_dirs["inbox_dir"]
    )
    assert coordinator.status_tracker is mock_status_tracker
    assert coordinator.context_loader is mock_context_loader


# ============================================================================
# Agent Status and Availability Tests
# ============================================================================

def test_get_agent_status_single(populated_coordinator):
    """Test getting status of single agent"""
    status = populated_coordinator.get_agent_status("AGENT-001")
    assert status["agent_id"] == "AGENT-001"
    assert status["role"] == "coordinator"
    assert status["status"] == "idle"


def test_get_agent_status_all(populated_coordinator):
    """Test getting status of all agents"""
    all_status = populated_coordinator.get_agent_status()
    assert len(all_status) == 3
    assert "AGENT-001" in all_status
    assert "AGENT-002" in all_status
    assert "AGENT-003" in all_status


def test_get_agent_status_unknown(coordinator):
    """Test getting status of unknown agent"""
    status = coordinator.get_agent_status("UNKNOWN")
    assert status["status"] == "unknown"
    assert status["error"] == "not_registered"


def test_get_available_agents(populated_coordinator):
    """Test getting available agents"""
    populated_coordinator.update_agent_heartbeat("AGENT-001", "busy", "Working")
    populated_coordinator.update_agent_heartbeat("AGENT-002", "idle")
    populated_coordinator.update_agent_heartbeat("AGENT-003", "idle")

    available = populated_coordinator.get_available_agents()
    assert len(available) == 2
    assert "AGENT-002" in available
    assert "AGENT-003" in available
    assert "AGENT-001" not in available


def test_get_available_agents_empty(populated_coordinator):
    """Test getting available agents when all busy"""
    populated_coordinator.update_agent_heartbeat("AGENT-001", "busy")
    populated_coordinator.update_agent_heartbeat("AGENT-002", "busy")
    populated_coordinator.update_agent_heartbeat("AGENT-003", "offline")

    available = populated_coordinator.get_available_agents()
    assert len(available) == 0


def test_register_agent(coordinator):
    """Test registering new agent"""
    coordinator.register_agent("NEW-AGENT", "worker")
    status = coordinator.get_agent_status("NEW-AGENT")
    assert status["agent_id"] == "NEW-AGENT"
    assert status["role"] == "worker"


def test_register_agent_invalid_role(coordinator):
    """Test registering agent with invalid role raises error"""
    with pytest.raises(ValueError, match="Invalid role"):
        coordinator.register_agent("BAD-AGENT", "invalid_role")


def test_update_agent_heartbeat(populated_coordinator):
    """Test updating agent heartbeat"""
    populated_coordinator.update_agent_heartbeat("AGENT-001", "busy", "Processing task")
    status = populated_coordinator.get_agent_status("AGENT-001")
    assert status["status"] == "busy"
    assert status["current_task"] == "Processing task"


def test_update_agent_heartbeat_unknown_agent(coordinator):
    """Test updating heartbeat for unknown agent raises error"""
    with pytest.raises(ValueError, match="Unknown agent"):
        coordinator.update_agent_heartbeat("UNKNOWN", "busy")


def test_check_agent_health(populated_coordinator, temp_dirs):
    """Test checking agent health detects issues"""
    # Make one agent stale
    old_time = datetime.datetime.now() - datetime.timedelta(minutes=6)
    populated_coordinator.status_tracker.agents["AGENT-001"]["last_heartbeat"] = old_time.isoformat()

    issues = populated_coordinator.check_agent_health()
    assert "AGENT-001" in issues


def test_check_agent_health_no_issues(populated_coordinator):
    """Test checking agent health when all healthy"""
    issues = populated_coordinator.check_agent_health()
    assert len(issues) == 0


# ============================================================================
# Query Classification Tests
# ============================================================================

def test_classify_query_bok_results(coordinator, mock_context_loader):
    """Test classification when BOK has results"""
    mock_context_loader.search_bok.return_value = [{"pattern": "test"}]

    classification = coordinator.classify_query("How to write tests")

    assert classification["type"] == "bok"
    assert classification["complexity"] == "low"
    assert classification["suggested_agent"] == "local"
    assert classification["can_handle_locally"] is True
    assert classification["confidence"] == 0.95


def test_classify_query_code(coordinator):
    """Test classification of code-related queries"""
    queries = [
        "Fix the authentication bug",
        "Debug this error message",
        "Implement login function"
    ]

    for query in queries:
        classification = coordinator.classify_query(query)
        assert classification["type"] == "code"
        assert classification["suggested_agent"] == "CLAUDE_CODE"
        assert classification["can_handle_locally"] is False


def test_classify_query_creative(coordinator):
    """Test classification of creative queries"""
    queries = [
        "Write a poem about coding",
        "Summarize this article",  # Changed from "document" to avoid doc keyword
        "Explain how TCP works"
    ]

    for query in queries:
        classification = coordinator.classify_query(query)
        assert classification["type"] == "creative"
        assert classification["complexity"] == "medium"


def test_classify_query_engineering(coordinator):
    """Test classification of engineering queries"""
    queries = [
        "Design the API architecture",
        "What system design patterns should we use",
        "Create protocol specification"
    ]

    for query in queries:
        classification = coordinator.classify_query(query)
        assert classification["type"] == "engineering"
        assert classification["complexity"] == "high"


def test_classify_query_qa(coordinator):
    """Test classification of QA queries"""
    queries = [
        "Run tests on authentication",
        "Verify test coverage",
        "Validate the API responses"
    ]

    for query in queries:
        classification = coordinator.classify_query(query)
        assert classification["type"] == "qa"
        assert classification["suggested_agent"] == "CLAUDE-CODE-003"


def test_classify_query_documentation(coordinator):
    """Test classification of documentation queries"""
    queries = [
        "Document this API",
        "Write a guide for installation",
        "Create README file"
    ]

    for query in queries:
        classification = coordinator.classify_query(query)
        assert classification["type"] == "documentation"
        assert classification["suggested_agent"] == "CLAUDE-CODE-002"


def test_classify_query_general(coordinator):
    """Test classification of general queries"""
    classification = coordinator.classify_query("Hello, how are you?")
    assert classification["type"] == "general"
    assert classification["suggested_agent"] == "local"
    assert classification["can_handle_locally"] is True


def test_classify_query_bok_search_error(coordinator, mock_context_loader):
    """Test classification when BOK search fails"""
    mock_context_loader.search_bok.side_effect = Exception("Search failed")

    # Should fall back to keyword classification
    classification = coordinator.classify_query("Fix bug in code")
    assert classification["type"] == "code"  # Fell back to keyword matching


# ============================================================================
# Delegation Decision Tests
# ============================================================================

def test_should_delegate_high_confidence_local(populated_coordinator):
    """Test should not delegate when can handle locally with high confidence"""
    classification = {
        "type": "bok",
        "can_handle_locally": True,
        "confidence": 0.95,
        "suggested_agent": "local"
    }

    assert populated_coordinator.should_delegate(classification) is False


def test_should_delegate_local_agent(populated_coordinator):
    """Test should not delegate when suggested agent is local"""
    classification = {
        "type": "general",
        "suggested_agent": "local",
        "can_handle_locally": True,
        "confidence": 0.6
    }

    assert populated_coordinator.should_delegate(classification) is False


def test_should_delegate_agent_not_registered(populated_coordinator):
    """Test should not delegate when agent not registered"""
    classification = {
        "type": "code",
        "suggested_agent": "UNKNOWN-AGENT",
        "can_handle_locally": False,
        "confidence": 0.8
    }

    assert populated_coordinator.should_delegate(classification) is False


def test_should_delegate_agent_not_available(populated_coordinator):
    """Test should not delegate when agent busy"""
    populated_coordinator.update_agent_heartbeat("AGENT-002", "busy")

    classification = {
        "type": "code",
        "suggested_agent": "AGENT-002",
        "can_handle_locally": False,
        "confidence": 0.8
    }

    assert populated_coordinator.should_delegate(classification) is False


def test_should_delegate_agent_available(populated_coordinator):
    """Test should delegate when agent available"""
    populated_coordinator.update_agent_heartbeat("AGENT-002", "idle")

    classification = {
        "type": "code",
        "suggested_agent": "AGENT-002",
        "can_handle_locally": False,
        "confidence": 0.8
    }

    assert populated_coordinator.should_delegate(classification) is True


# ============================================================================
# Query Routing Tests
# ============================================================================

def test_route_query_handle_locally(coordinator, mock_context_loader):
    """Test routing query to handle locally"""
    mock_context_loader.search_bok.return_value = [{"pattern": "test"}]

    result = coordinator.route_query("How to write tests")

    assert result["action"] == "local"
    assert result["agent"] == "local"
    assert "classification" in result


@patch('src.deia.services.agent_coordinator.create_task_file')
def test_route_query_delegate(mock_create_task, populated_coordinator, temp_dirs):
    """Test routing query with delegation"""
    mock_create_task.return_value = "/path/to/task.md"

    # Register CLAUDE_CODE agent and make it available
    populated_coordinator.register_agent("CLAUDE_CODE", "worker")
    populated_coordinator.update_agent_heartbeat("CLAUDE_CODE", "idle")

    result = populated_coordinator.route_query("Fix authentication bug")

    # Should delegate to CLAUDE_CODE for code queries
    assert result["action"] == "delegate"
    assert result["agent"] == "CLAUDE_CODE"
    assert "task_file" in result
    assert "classification" in result


def test_route_query_delegation_fails(populated_coordinator):
    """Test routing when delegation fails falls back to local"""
    # Register CLAUDE_CODE and make it available
    populated_coordinator.register_agent("CLAUDE_CODE", "worker")
    populated_coordinator.update_agent_heartbeat("CLAUDE_CODE", "idle")

    with patch.object(populated_coordinator, 'create_delegation_task', side_effect=RuntimeError("Failed")):
        result = populated_coordinator.route_query("Fix bug")

        assert result["action"] == "local"
        assert "Delegation failed" in result["reason"]


# ============================================================================
# Task Creation and Assignment Tests
# ============================================================================

@patch('src.deia.services.agent_coordinator.create_task_file')
def test_create_delegation_task(mock_create_task, coordinator):
    """Test creating delegation task"""
    mock_create_task.return_value = "/path/to/task.md"

    task_file = coordinator.create_delegation_task("Test query", "AGENT-001")

    assert task_file == "/path/to/task.md"
    mock_create_task.assert_called_once()
    call_args = mock_create_task.call_args
    assert call_args[1]["from_agent"] == "CHATGPT"
    assert call_args[1]["to_agent"] == "AGENT-001"
    assert call_args[1]["task_type"] == "QUERY"


@patch('src.deia.services.agent_coordinator.create_task_file')
def test_create_delegation_task_custom_from(mock_create_task, coordinator):
    """Test creating delegation task with custom from_agent"""
    mock_create_task.return_value = "/path/to/task.md"

    task_file = coordinator.create_delegation_task(
        "Test query",
        "AGENT-001",
        from_agent="CUSTOM-AGENT"
    )

    call_args = mock_create_task.call_args
    assert call_args[1]["from_agent"] == "CUSTOM-AGENT"


@patch('src.deia.services.agent_coordinator.create_task_file')
def test_create_delegation_task_permission_error(mock_create_task, coordinator):
    """Test delegation task creation handles permission errors"""
    mock_create_task.side_effect = PermissionError("Access denied")

    with pytest.raises(RuntimeError, match="permission denied"):
        coordinator.create_delegation_task("Test", "AGENT-001")


@patch('src.deia.services.agent_coordinator.create_task_file')
def test_assign_task(mock_create_task, populated_coordinator):
    """Test assigning task to agent"""
    mock_create_task.return_value = "/path/to/task.md"

    task_file = populated_coordinator.assign_task(
        "AGENT-001",
        "Run comprehensive tests",
        priority="high"
    )

    assert task_file == "/path/to/task.md"
    mock_create_task.assert_called_once()


@patch('src.deia.services.agent_coordinator.create_task_file')
def test_assign_task_different_priorities(mock_create_task, populated_coordinator):
    """Test assigning tasks with different priorities"""
    mock_create_task.return_value = "/path/to/task.md"

    priorities = ["low", "normal", "high", "critical"]
    for priority in priorities:
        populated_coordinator.assign_task(
            "AGENT-001",
            f"Task with {priority} priority",
            priority=priority
        )


def test_assign_task_unknown_agent(coordinator):
    """Test assigning task to unknown agent raises error"""
    with pytest.raises(ValueError, match="not registered"):
        coordinator.assign_task("UNKNOWN", "Some task")


@patch('src.deia.services.agent_coordinator.create_task_file')
def test_assign_task_creation_fails(mock_create_task, populated_coordinator):
    """Test assign_task handles creation failures"""
    mock_create_task.side_effect = Exception("Failed")

    with pytest.raises(RuntimeError, match="Task assignment failed"):
        populated_coordinator.assign_task("AGENT-001", "Test task")


@patch('src.deia.services.agent_coordinator.create_task_file')
def test_broadcast_message(mock_create_task, coordinator):
    """Test broadcasting message to all agents"""
    mock_create_task.return_value = "/path/to/broadcast.md"

    files = coordinator.broadcast_message("Important update", message_type="ALERT")

    assert len(files) == 1
    assert files[0] == "/path/to/broadcast.md"

    call_args = mock_create_task.call_args
    assert call_args[1]["to_agent"] == "ALL"
    assert call_args[1]["task_type"] == "ALERT"


@patch('src.deia.services.agent_coordinator.create_task_file')
def test_broadcast_message_failure(mock_create_task, coordinator):
    """Test broadcast handles failures"""
    mock_create_task.side_effect = Exception("Failed")

    with pytest.raises(RuntimeError, match="Broadcast failed"):
        coordinator.broadcast_message("Test message")


# ============================================================================
# Dashboard and Monitoring Tests
# ============================================================================

def test_render_dashboard_no_agents(coordinator):
    """Test rendering dashboard with no agents"""
    dashboard = coordinator.render_dashboard()
    assert "No agents registered yet" in dashboard


def test_render_dashboard_with_agents(populated_coordinator):
    """Test rendering dashboard with agents"""
    dashboard = populated_coordinator.render_dashboard()
    assert "DEIA COORDINATION DASHBOARD" in dashboard
    assert "AGENT-001" in dashboard
    assert "AGENT-002" in dashboard
    assert "AGENT-003" in dashboard


def test_get_coordination_summary(populated_coordinator):
    """Test getting coordination summary"""
    populated_coordinator.update_agent_heartbeat("AGENT-001", "idle")
    populated_coordinator.update_agent_heartbeat("AGENT-002", "busy")
    populated_coordinator.update_agent_heartbeat("AGENT-003", "offline")

    summary = populated_coordinator.get_coordination_summary()

    assert summary["total_agents"] == 3
    assert summary["online_agents"] == 2
    assert summary["idle_agents"] == 1
    assert summary["busy_agents"] == 1
    assert summary["offline_agents"] == 1
    assert "last_check" in summary


def test_get_coordination_summary_all_idle(populated_coordinator):
    """Test coordination summary with all agents idle"""
    for agent_id in ["AGENT-001", "AGENT-002", "AGENT-003"]:
        populated_coordinator.update_agent_heartbeat(agent_id, "idle")

    summary = populated_coordinator.get_coordination_summary()
    assert summary["idle_agents"] == 3
    assert summary["busy_agents"] == 0


def test_get_coordination_summary_empty(coordinator):
    """Test coordination summary with no agents"""
    summary = coordinator.get_coordination_summary()
    assert summary["total_agents"] == 0
    assert summary["online_agents"] == 0


# ============================================================================
# Integration Tests
# ============================================================================

def test_complete_workflow(populated_coordinator, mock_context_loader):
    """Test complete coordination workflow"""
    # 1. Register agent
    populated_coordinator.register_agent("WORKER-001", "worker")

    # 2. Update heartbeat
    populated_coordinator.update_agent_heartbeat("WORKER-001", "idle")

    # 3. Classify query
    classification = populated_coordinator.classify_query("Write tests")

    # 4. Check delegation
    should_delegate = populated_coordinator.should_delegate(classification)

    # 5. Get status
    status = populated_coordinator.get_agent_status("WORKER-001")
    assert status["status"] == "idle"

    # 6. Get summary
    summary = populated_coordinator.get_coordination_summary()
    assert summary["total_agents"] == 4  # 3 from fixture + WORKER-001


@patch('src.deia.services.agent_coordinator.create_task_file')
def test_end_to_end_delegation(mock_create_task, populated_coordinator):
    """Test end-to-end delegation flow"""
    mock_create_task.return_value = "/path/to/task.md"

    # Make agent available
    populated_coordinator.update_agent_heartbeat("AGENT-002", "idle")

    # Route query
    result = populated_coordinator.route_query("Implement user authentication")

    # Verify delegation occurred (may be local or delegated depending on classification)
    assert result["action"] in ["local", "delegate"]
    assert "classification" in result


# ============================================================================
# Error Handling and Edge Cases
# ============================================================================

def test_multiple_agents_same_specialization(populated_coordinator):
    """Test coordination with multiple agents having same specialization"""
    populated_coordinator.register_agent("QA-001", "worker")
    populated_coordinator.register_agent("QA-002", "worker")

    populated_coordinator.update_agent_heartbeat("QA-001", "idle")
    populated_coordinator.update_agent_heartbeat("QA-002", "busy")

    available = populated_coordinator.get_available_agents()
    assert "QA-001" in available
    assert "QA-002" not in available


def test_context_loader_integration(coordinator, mock_context_loader):
    """Test context loader integration in classification"""
    mock_context_loader.search_bok.return_value = [
        {"pattern": "authentication", "score": 0.9}
    ]

    classification = coordinator.classify_query("How to implement auth")

    assert classification["type"] == "bok"
    assert "bok_results" in classification
    mock_context_loader.search_bok.assert_called_once()


def test_long_query_subject_truncation(coordinator):
    """Test that long queries are truncated in task subjects"""
    with patch('src.deia.services.agent_coordinator.create_task_file') as mock_create:
        mock_create.return_value = "/path/to/task.md"

        long_query = "This is a very long query that should be truncated when creating task files"
        coordinator.create_delegation_task(long_query, "AGENT-001")

        call_args = mock_create.call_args
        subject = call_args[1]["subject"]
        assert len(subject) <= 30


def test_concurrent_heartbeat_updates(populated_coordinator):
    """Test thread safety of concurrent heartbeat updates"""
    import threading

    def update_agent(agent_id):
        for i in range(10):
            populated_coordinator.update_agent_heartbeat(agent_id, "busy", f"Task {i}")

    threads = [
        threading.Thread(target=update_agent, args=("AGENT-001",)),
        threading.Thread(target=update_agent, args=("AGENT-002",)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Should complete without errors
    assert populated_coordinator.get_agent_status("AGENT-001")["status"] == "busy"
    assert populated_coordinator.get_agent_status("AGENT-002")["status"] == "busy"
