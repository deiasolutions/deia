"""
Tests for AgentStatusTracker

Component: src/deia/services/agent_status.py
Purpose: Core hive coordination and state management
Coverage Target: 80%+
"""

import pytest
import time
import datetime
import threading
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import yaml

from src.deia.services.agent_status import AgentStatusTracker, VALID_STATUSES, VALID_ROLES


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def temp_heartbeat_dir(tmp_path):
    """Create temporary heartbeat directory"""
    heartbeat_dir = tmp_path / "heartbeats"
    heartbeat_dir.mkdir(parents=True, exist_ok=True)
    return heartbeat_dir


@pytest.fixture
def tracker(temp_heartbeat_dir):
    """Create AgentStatusTracker with temporary directory"""
    return AgentStatusTracker(heartbeat_dir=str(temp_heartbeat_dir))


@pytest.fixture
def populated_tracker(temp_heartbeat_dir):
    """Create tracker with pre-populated agents"""
    tracker = AgentStatusTracker(heartbeat_dir=str(temp_heartbeat_dir))
    tracker.register_agent("AGENT-001", "worker")
    tracker.register_agent("AGENT-002", "queen")
    tracker.register_agent("AGENT-003", "drone")
    return tracker


# ============================================================================
# Initialization Tests
# ============================================================================

def test_initialization_creates_directory(tmp_path):
    """Test that initialization creates heartbeat directory if it doesn't exist"""
    heartbeat_dir = tmp_path / "new_heartbeats"
    assert not heartbeat_dir.exists()

    tracker = AgentStatusTracker(heartbeat_dir=str(heartbeat_dir))

    assert heartbeat_dir.exists()
    assert heartbeat_dir.is_dir()


def test_initialization_with_existing_heartbeats(temp_heartbeat_dir):
    """Test loading existing heartbeats on initialization"""
    # Create existing heartbeat file
    heartbeat_data = {
        "agent_id": "AGENT-001",
        "status": "idle",
        "role": "worker",
        "last_heartbeat": datetime.datetime.now().isoformat()
    }
    heartbeat_file = temp_heartbeat_dir / "AGENT-001-heartbeat.yaml"
    with open(heartbeat_file, "w") as f:
        yaml.safe_dump(heartbeat_data, f)

    # Initialize tracker
    tracker = AgentStatusTracker(heartbeat_dir=str(temp_heartbeat_dir))

    # Verify agent was loaded
    assert "AGENT" in tracker.agents
    assert tracker.agents["AGENT"]["agent_id"] == "AGENT-001"
    assert tracker.agents["AGENT"]["status"] == "idle"


def test_initialization_creates_lock(tracker):
    """Test that tracker has thread lock"""
    assert hasattr(tracker, "_lock")
    # Check it's an RLock by checking its type name
    assert type(tracker._lock).__name__ == "RLock"


# ============================================================================
# Registration Tests
# ============================================================================

def test_register_agent_success(tracker):
    """Test registering a new agent"""
    tracker.register_agent("AGENT-001", "worker")

    assert "AGENT-001" in tracker.agents
    assert tracker.agents["AGENT-001"]["status"] == "idle"
    assert tracker.agents["AGENT-001"]["role"] == "worker"
    assert "last_heartbeat" in tracker.agents["AGENT-001"]


def test_register_agent_invalid_role(tracker):
    """Test registering agent with invalid role raises error"""
    with pytest.raises(ValueError, match="Invalid role"):
        tracker.register_agent("AGENT-001", "invalid_role")


def test_register_agent_all_valid_roles(tracker):
    """Test registering agents with all valid roles"""
    for role in VALID_ROLES:
        agent_id = f"AGENT-{role}"
        tracker.register_agent(agent_id, role)
        assert tracker.agents[agent_id]["role"] == role


def test_register_agent_creates_file(tracker, temp_heartbeat_dir):
    """Test that registering agent creates heartbeat file"""
    tracker.register_agent("AGENT-001", "worker")

    heartbeat_file = temp_heartbeat_dir / "AGENT-001-heartbeat.yaml"
    assert heartbeat_file.exists()

    with open(heartbeat_file) as f:
        data = yaml.safe_load(f)
        assert data["agent_id"] == "AGENT-001"
        assert data["status"] == "idle"


def test_register_duplicate_agent_ignores(tracker):
    """Test that registering duplicate agent is idempotent"""
    tracker.register_agent("AGENT-001", "worker")
    original_heartbeat = tracker.agents["AGENT-001"]["last_heartbeat"]

    time.sleep(0.1)  # Ensure different timestamp if re-registered
    tracker.register_agent("AGENT-001", "queen")  # Try to change role

    # Should not update existing agent
    assert tracker.agents["AGENT-001"]["role"] == "worker"
    assert tracker.agents["AGENT-001"]["last_heartbeat"] == original_heartbeat


# ============================================================================
# Heartbeat Update Tests
# ============================================================================

def test_update_heartbeat_success(tracker):
    """Test updating agent heartbeat"""
    tracker.register_agent("AGENT-001", "worker")
    original_time = tracker.agents["AGENT-001"]["last_heartbeat"]

    time.sleep(0.1)
    tracker.update_heartbeat("AGENT-001", "busy", "Processing task 123")

    assert tracker.agents["AGENT-001"]["status"] == "busy"
    assert tracker.agents["AGENT-001"]["current_task"] == "Processing task 123"
    assert tracker.agents["AGENT-001"]["last_heartbeat"] != original_time


def test_update_heartbeat_unknown_agent(tracker):
    """Test updating heartbeat for unregistered agent raises error"""
    with pytest.raises(ValueError, match="Unknown agent"):
        tracker.update_heartbeat("UNKNOWN-AGENT", "busy")


def test_update_heartbeat_invalid_status(tracker):
    """Test updating with invalid status raises error"""
    tracker.register_agent("AGENT-001", "worker")

    with pytest.raises(ValueError, match="Invalid status"):
        tracker.update_heartbeat("AGENT-001", "invalid_status")


def test_update_heartbeat_all_valid_statuses(tracker):
    """Test updating with all valid statuses"""
    tracker.register_agent("AGENT-001", "worker")

    for status in VALID_STATUSES:
        tracker.update_heartbeat("AGENT-001", status)
        assert tracker.agents["AGENT-001"]["status"] == status


def test_update_heartbeat_without_task(tracker):
    """Test updating heartbeat without current_task parameter"""
    tracker.register_agent("AGENT-001", "worker")
    tracker.update_heartbeat("AGENT-001", "idle")

    assert tracker.agents["AGENT-001"]["status"] == "idle"
    assert tracker.agents["AGENT-001"].get("current_task") is None


# ============================================================================
# Heartbeat Validation Tests
# ============================================================================

def test_validate_heartbeat_valid(tracker):
    """Test validating correct heartbeat data"""
    valid_data = {
        "agent_id": "AGENT-001",
        "status": "idle",
        "role": "worker"
    }
    assert tracker._validate_heartbeat(valid_data) is True


def test_validate_heartbeat_invalid_status(tracker):
    """Test validating heartbeat with invalid status"""
    invalid_data = {
        "agent_id": "AGENT-001",
        "status": "invalid_status"
    }
    assert tracker._validate_heartbeat(invalid_data) is False


def test_validate_heartbeat_missing_agent_id(tracker):
    """Test validating heartbeat without agent_id"""
    invalid_data = {
        "status": "idle"
    }
    assert tracker._validate_heartbeat(invalid_data) is False


# ============================================================================
# Heartbeat Checking Tests
# ============================================================================

def test_check_heartbeats_detects_offline(tracker):
    """Test that check_heartbeats detects offline agents"""
    tracker.register_agent("AGENT-001", "worker")

    # Manually set old heartbeat (>5 minutes ago)
    old_time = datetime.datetime.now() - datetime.timedelta(minutes=6)
    tracker.agents["AGENT-001"]["last_heartbeat"] = old_time.isoformat()

    offline = tracker.check_heartbeats()

    assert "AGENT-001" in offline
    assert tracker.agents["AGENT-001"]["status"] == "offline"


def test_check_heartbeats_ignores_recent(tracker):
    """Test that check_heartbeats ignores recent heartbeats"""
    tracker.register_agent("AGENT-001", "worker")

    offline = tracker.check_heartbeats()

    assert "AGENT-001" not in offline
    assert tracker.agents["AGENT-001"]["status"] == "idle"


def test_check_stale_states_waiting_timeout(tracker):
    """Test that waiting state times out after 15 minutes"""
    tracker.register_agent("AGENT-001", "worker")
    tracker.update_heartbeat("AGENT-001", "waiting")

    # Set old heartbeat (>15 minutes)
    old_time = datetime.datetime.now() - datetime.timedelta(minutes=16)
    tracker.agents["AGENT-001"]["last_heartbeat"] = old_time.isoformat()

    stale = tracker._check_stale_states()

    assert "AGENT-001" in stale
    assert "waiting→idle" in stale["AGENT-001"]
    assert tracker.agents["AGENT-001"]["status"] == "idle"


def test_check_stale_states_busy_timeout(tracker):
    """Test that busy state goes offline after 30 minutes"""
    tracker.register_agent("AGENT-001", "worker")
    tracker.update_heartbeat("AGENT-001", "busy")

    # Set old heartbeat (>30 minutes)
    old_time = datetime.datetime.now() - datetime.timedelta(minutes=31)
    tracker.agents["AGENT-001"]["last_heartbeat"] = old_time.isoformat()

    stale = tracker._check_stale_states()

    assert "AGENT-001" in stale
    assert "busy→offline" in stale["AGENT-001"]
    assert tracker.agents["AGENT-001"]["status"] == "offline"


# ============================================================================
# Query Tests
# ============================================================================

def test_get_agent_status_existing(tracker):
    """Test getting status of existing agent"""
    tracker.register_agent("AGENT-001", "worker")

    status = tracker.get_agent_status("AGENT-001")

    assert status["agent_id"] == "AGENT-001"
    assert status["status"] == "idle"
    assert status["role"] == "worker"


def test_get_agent_status_unknown(tracker):
    """Test getting status of unknown agent returns error"""
    status = tracker.get_agent_status("UNKNOWN")

    assert status["agent_id"] == "UNKNOWN"
    assert status["status"] == "unknown"
    assert status["error"] == "not_registered"


def test_get_all_agents(populated_tracker):
    """Test getting all agents"""
    all_agents = populated_tracker.get_all_agents()

    assert len(all_agents) == 3
    assert "AGENT-001" in all_agents
    assert "AGENT-002" in all_agents
    assert "AGENT-003" in all_agents


def test_get_all_agents_returns_copy(tracker):
    """Test that get_all_agents returns copy, not original"""
    tracker.register_agent("AGENT-001", "worker")

    agents = tracker.get_all_agents()
    agents["AGENT-001"]["status"] = "modified"

    # Original should not be modified
    assert tracker.agents["AGENT-001"]["status"] == "idle"


def test_get_available_agents(populated_tracker):
    """Test getting available (idle) agents"""
    populated_tracker.update_heartbeat("AGENT-001", "idle")
    populated_tracker.update_heartbeat("AGENT-002", "busy")
    populated_tracker.update_heartbeat("AGENT-003", "idle")

    available = populated_tracker.get_available_agents()

    assert len(available) == 2
    assert "AGENT-001" in available
    assert "AGENT-003" in available
    assert "AGENT-002" not in available


def test_get_available_agents_empty(tracker):
    """Test getting available agents when all busy"""
    tracker.register_agent("AGENT-001", "worker")
    tracker.update_heartbeat("AGENT-001", "busy")

    available = tracker.get_available_agents()

    assert len(available) == 0


# ============================================================================
# Dashboard Rendering Tests
# ============================================================================

def test_render_dashboard_no_agents(tracker):
    """Test rendering dashboard with no agents"""
    dashboard = tracker.render_dashboard()

    assert "No agents registered yet" in dashboard


def test_render_dashboard_with_agents(populated_tracker):
    """Test rendering dashboard with agents"""
    dashboard = populated_tracker.render_dashboard()

    assert "DEIA COORDINATION DASHBOARD" in dashboard
    assert "AGENT-001" in dashboard
    assert "AGENT-002" in dashboard
    assert "AGENT-003" in dashboard


def test_render_dashboard_shows_status(populated_tracker):
    """Test that dashboard shows agent statuses"""
    populated_tracker.update_heartbeat("AGENT-001", "idle")
    populated_tracker.update_heartbeat("AGENT-002", "busy", "Processing task")

    dashboard = populated_tracker.render_dashboard()

    assert "IDLE" in dashboard
    assert "BUSY" in dashboard
    assert "Processing task" in dashboard


def test_render_dashboard_truncates_long_task(populated_tracker):
    """Test that dashboard truncates long task names"""
    long_task = "This is a very long task name that should be truncated to fit in dashboard"
    populated_tracker.update_heartbeat("AGENT-001", "busy", long_task)

    dashboard = populated_tracker.render_dashboard()

    # Should contain truncated version with ...
    assert "..." in dashboard
    assert long_task not in dashboard  # Full task should not appear


def test_render_dashboard_shows_summary(populated_tracker):
    """Test that dashboard shows summary statistics"""
    populated_tracker.update_heartbeat("AGENT-001", "idle")
    populated_tracker.update_heartbeat("AGENT-002", "busy")
    populated_tracker.update_heartbeat("AGENT-003", "offline")

    dashboard = populated_tracker.render_dashboard()

    assert "Online:" in dashboard
    assert "Offline:" in dashboard
    assert "Idle:" in dashboard
    assert "Busy:" in dashboard


# ============================================================================
# Thread Safety Tests
# ============================================================================

def test_thread_safety_concurrent_updates(populated_tracker):
    """Test that concurrent updates are thread-safe"""
    def update_agent(agent_id, count):
        for i in range(count):
            populated_tracker.update_heartbeat(agent_id, "busy", f"Task {i}")
            time.sleep(0.001)

    # Start multiple threads updating different agents
    threads = [
        threading.Thread(target=update_agent, args=("AGENT-001", 10)),
        threading.Thread(target=update_agent, args=("AGENT-002", 10)),
        threading.Thread(target=update_agent, args=("AGENT-003", 10))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # All agents should have been updated
    assert populated_tracker.agents["AGENT-001"]["status"] == "busy"
    assert populated_tracker.agents["AGENT-002"]["status"] == "busy"
    assert populated_tracker.agents["AGENT-003"]["status"] == "busy"


def test_thread_safety_get_while_updating(populated_tracker):
    """Test that getting status while updating is thread-safe"""
    def update_loop():
        for i in range(50):
            populated_tracker.update_heartbeat("AGENT-001", "busy", f"Task {i}")
            time.sleep(0.01)

    def get_loop(results):
        for i in range(50):
            status = populated_tracker.get_agent_status("AGENT-001")
            results.append(status)
            time.sleep(0.01)

    results = []
    update_thread = threading.Thread(target=update_loop)
    get_thread = threading.Thread(target=get_loop, args=(results,))

    update_thread.start()
    get_thread.start()

    update_thread.join()
    get_thread.join()

    # Should have retrieved statuses without errors
    assert len(results) == 50
    for status in results:
        assert "agent_id" in status


# ============================================================================
# File Persistence Tests
# ============================================================================

def test_save_agent_creates_valid_yaml(tracker, temp_heartbeat_dir):
    """Test that _save_agent creates valid YAML file"""
    tracker.register_agent("AGENT-001", "worker")

    heartbeat_file = temp_heartbeat_dir / "AGENT-001-heartbeat.yaml"
    assert heartbeat_file.exists()

    with open(heartbeat_file) as f:
        data = yaml.safe_load(f)
        assert data is not None
        assert isinstance(data, dict)


def test_load_agents_ignores_invalid_yaml(temp_heartbeat_dir):
    """Test that _load_agents skips files with invalid YAML"""
    # Create invalid YAML file
    invalid_file = temp_heartbeat_dir / "INVALID-heartbeat.yaml"
    with open(invalid_file, "w") as f:
        f.write("{ invalid yaml content ][")

    # Create valid YAML file
    valid_file = temp_heartbeat_dir / "VALID-heartbeat.yaml"
    valid_data = {
        "agent_id": "VALID",
        "status": "idle",
        "role": "worker",
        "last_heartbeat": datetime.datetime.now().isoformat()
    }
    with open(valid_file, "w") as f:
        yaml.safe_dump(valid_data, f)

    # Initialize tracker
    tracker = AgentStatusTracker(heartbeat_dir=str(temp_heartbeat_dir))

    # Should load valid agent, skip invalid
    assert "VALID" in tracker.agents
    assert "INVALID" not in tracker.agents


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

def test_empty_heartbeat_directory(tracker):
    """Test tracker with no existing heartbeat files"""
    assert len(tracker.agents) == 0
    all_agents = tracker.get_all_agents()
    assert len(all_agents) == 0


def test_transition_state(tracker):
    """Test _transition_state method"""
    tracker.register_agent("AGENT-001", "worker")
    tracker._transition_state("AGENT-001", "paused", "user_request")

    assert tracker.agents["AGENT-001"]["status"] == "paused"


def test_monitor_loop_starts_daemon_thread(tracker):
    """Test that start_monitor_loop creates daemon thread"""
    with patch("threading.Thread") as mock_thread:
        tracker.start_monitor_loop(interval=1)

        # Verify thread was created as daemon
        mock_thread.assert_called_once()
        call_kwargs = mock_thread.call_args[1]
        assert call_kwargs["daemon"] is True


def test_status_colors_defined():
    """Test that status colors are properly defined"""
    from src.deia.services.agent_status import STATUS_COLORS

    assert len(STATUS_COLORS) == len(VALID_STATUSES)
    for status in VALID_STATUSES:
        assert status in STATUS_COLORS


# ============================================================================
# Integration-like Tests
# ============================================================================

def test_complete_workflow(tracker):
    """Test complete workflow: register, update, check, query"""
    # Register agent
    tracker.register_agent("WORKER-001", "worker")

    # Update status multiple times
    tracker.update_heartbeat("WORKER-001", "busy", "Task 1")
    assert tracker.agents["WORKER-001"]["status"] == "busy"

    tracker.update_heartbeat("WORKER-001", "waiting")
    assert tracker.agents["WORKER-001"]["status"] == "waiting"

    tracker.update_heartbeat("WORKER-001", "idle")
    assert tracker.agents["WORKER-001"]["status"] == "idle"

    # Check heartbeats (should be fine, recently updated)
    offline = tracker.check_heartbeats()
    assert "WORKER-001" not in offline

    # Query status
    status = tracker.get_agent_status("WORKER-001")
    assert status["status"] == "idle"

    # Check availability
    available = tracker.get_available_agents()
    assert "WORKER-001" in available


def test_multiple_agents_different_states(tracker):
    """Test tracker with multiple agents in different states"""
    tracker.register_agent("IDLE-AGENT", "worker")
    tracker.register_agent("BUSY-AGENT", "queen")
    tracker.register_agent("OFFLINE-AGENT", "drone")

    tracker.update_heartbeat("IDLE-AGENT", "idle")
    tracker.update_heartbeat("BUSY-AGENT", "busy", "Important task")

    # Make offline agent stale
    old_time = datetime.datetime.now() - datetime.timedelta(minutes=6)
    tracker.agents["OFFLINE-AGENT"]["last_heartbeat"] = old_time.isoformat()

    # Check states
    tracker.check_heartbeats()

    assert tracker.agents["IDLE-AGENT"]["status"] == "idle"
    assert tracker.agents["BUSY-AGENT"]["status"] == "busy"
    assert tracker.agents["OFFLINE-AGENT"]["status"] == "offline"

    # Get available agents
    available = tracker.get_available_agents()
    assert len(available) == 1
    assert "IDLE-AGENT" in available


# ============================================================================
# Coverage: Uncovered Edge Cases
# ============================================================================

def test_render_dashboard_truncates_agent_id(tracker):
    """Test dashboard truncates long agent IDs"""
    long_id = "VERY-LONG-AGENT-IDENTIFIER-THAT-EXCEEDS-LIMIT"
    tracker.register_agent(long_id, "worker")

    dashboard = tracker.render_dashboard()

    # Should contain truncated version
    assert long_id[:15] in dashboard
    assert long_id not in dashboard  # Full ID should not appear


def test_update_heartbeat_saves_to_file(tracker, temp_heartbeat_dir):
    """Test that update_heartbeat persists to file"""
    tracker.register_agent("AGENT-001", "worker")
    tracker.update_heartbeat("AGENT-001", "busy", "Testing")

    # Read file directly
    heartbeat_file = temp_heartbeat_dir / "AGENT-001-heartbeat.yaml"
    with open(heartbeat_file) as f:
        data = yaml.safe_load(f)
        assert data["status"] == "busy"
        assert data["current_task"] == "Testing"


def test_check_heartbeats_returns_empty_when_all_fresh(populated_tracker):
    """Test check_heartbeats returns empty dict when all heartbeats fresh"""
    offline = populated_tracker.check_heartbeats()

    assert offline == {}
