"""
Tests for DEIA hive management commands.

Tests the hive join and launch functionality for multi-bot coordination.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from deia.hive import HiveManager, HiveJoinError, HiveLaunchError


@pytest.fixture
def sample_hive_config():
    """Sample hive configuration for testing."""
    return {
        "hive_name": "test-hive",
        "hive_type": "multi-bot",
        "version": "1.0",
        "queen": {
            "bot_id": "BOT-00001",
            "role": "Queen/Scrum Master",
            "responsibilities": ["Planning", "Coordination"]
        },
        "drones": [
            {
                "bot_id": "BOT-00002",
                "role": "Drone-Testing",
                "responsibilities": ["Unit tests", "Integration tests"]
            },
            {
                "bot_id": "BOT-00003",
                "role": "Drone-Integration",
                "responsibilities": ["Code integration", "Refactoring"]
            }
        ],
        "coordination": {
            "instruction_folder": ".deia/instructions",
            "report_folder": ".deia/reports",
            "status_file": ".deia/hive-status.json"
        }
    }


@pytest.fixture
def hive_config_file(tmp_path, sample_hive_config):
    """Create a temporary hive config file."""
    config_file = tmp_path / "test-hive.json"
    config_file.write_text(json.dumps(sample_hive_config, indent=2))
    return config_file


class TestHiveManager:
    """Test HiveManager class."""

    def test_init(self):
        """Test HiveManager initialization."""
        manager = HiveManager()
        assert manager is not None

    def test_load_hive_config(self, hive_config_file):
        """Test loading hive configuration from file."""
        manager = HiveManager()
        config = manager.load_hive_config(str(hive_config_file))

        assert config['hive_name'] == 'test-hive'
        assert config['hive_type'] == 'multi-bot'
        assert len(config['drones']) == 2

    def test_load_hive_config_missing_file(self):
        """Test loading non-existent hive config."""
        manager = HiveManager()

        with pytest.raises(FileNotFoundError):
            manager.load_hive_config('/nonexistent/file.json')

    def test_load_hive_config_invalid_json(self, tmp_path):
        """Test loading invalid JSON hive config."""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("{ invalid json }")

        manager = HiveManager()

        with pytest.raises(json.JSONDecodeError):
            manager.load_hive_config(str(invalid_file))


class TestHiveJoin:
    """Test hive join functionality."""

    @patch('deia.hive.BotCoordinator')
    def test_join_hive_auto_assign(self, mock_coordinator, hive_config_file, tmp_path):
        """Test joining hive with auto-assignment of role."""
        # Setup mock coordinator
        mock_coord_instance = MagicMock()
        mock_coord_instance.generate_instance_id.return_value = "abc12345"
        mock_coord_instance.claim_identity.return_value = True
        mock_coord_instance.get_bot_info.return_value = {
            'role': 'Drone-Testing',
            'instance_id': 'abc12345',
            'bot_id': 'BOT-00002'
        }
        mock_coordinator.return_value = mock_coord_instance

        manager = HiveManager(deia_root=str(tmp_path / ".deia"))
        result = manager.join_hive(str(hive_config_file))

        assert result['success'] is True
        assert result['bot_id'] in ['BOT-00002', 'BOT-00003']
        assert 'instance_id' in result
        assert 'role' in result

    @patch('deia.hive.BotCoordinator')
    def test_join_hive_specific_role(self, mock_coordinator, hive_config_file, tmp_path):
        """Test joining hive with specific bot role."""
        # Setup mock coordinator
        mock_coord_instance = MagicMock()
        mock_coord_instance.generate_instance_id.return_value = "def45678"
        mock_coord_instance.claim_identity.return_value = True
        mock_coord_instance.get_bot_info.return_value = {
            'role': 'Drone-Integration',
            'instance_id': 'def45678',
            'bot_id': 'BOT-00003'
        }
        mock_coordinator.return_value = mock_coord_instance

        manager = HiveManager(deia_root=str(tmp_path / ".deia"))
        result = manager.join_hive(str(hive_config_file), bot_id='BOT-00003')

        assert result['success'] is True
        assert result['bot_id'] == 'BOT-00003'
        assert result['role'] == 'Drone-Integration'

    @patch('deia.hive.BotCoordinator')
    def test_join_hive_already_claimed(self, mock_coordinator, hive_config_file, tmp_path):
        """Test joining hive when role is already claimed."""
        # Setup mock coordinator - claim fails
        mock_coord_instance = MagicMock()
        mock_coord_instance.generate_instance_id.return_value = "xyz99999"
        mock_coord_instance.claim_identity.return_value = False
        mock_coordinator.return_value = mock_coord_instance

        manager = HiveManager(deia_root=str(tmp_path / ".deia"))

        with pytest.raises(HiveJoinError, match="already claimed"):
            manager.join_hive(str(hive_config_file), bot_id='BOT-00002')


class TestHiveLaunch:
    """Test hive launch functionality."""

    @patch('deia.hive.BotCoordinator')
    def test_launch_hive(self, mock_coordinator, hive_config_file, tmp_path):
        """Test launching a new hive."""
        # Setup mock coordinator
        mock_coord_instance = MagicMock()
        mock_coord_instance.generate_instance_id.return_value = "queen001"
        mock_coord_instance.register_bot.return_value = "BOT-00001"
        mock_coordinator.return_value = mock_coord_instance

        manager = HiveManager(deia_root=str(tmp_path / ".deia"))
        result = manager.launch_hive(str(hive_config_file))

        assert result['success'] is True
        assert result['queen_id'] == 'BOT-00001'
        assert result['hive_name'] == 'test-hive'
        assert len(result['drones_initialized']) == 2

    @patch('deia.hive.BotCoordinator')
    def test_launch_hive_creates_structure(self, mock_coordinator, hive_config_file, tmp_path):
        """Test that launching hive creates necessary directory structure."""
        # Setup mock coordinator
        mock_coord_instance = MagicMock()
        mock_coord_instance.generate_instance_id.return_value = "queen002"
        mock_coord_instance.register_bot.return_value = "BOT-00001"
        mock_coordinator.return_value = mock_coord_instance

        deia_root = tmp_path / ".deia"
        manager = HiveManager(deia_root=str(deia_root))
        result = manager.launch_hive(str(hive_config_file))

        # Check directories were created
        assert (deia_root / "instructions").exists()
        assert (deia_root / "reports").exists()
        assert result['success'] is True

    @patch('deia.hive.BotCoordinator')
    def test_launch_hive_creates_instruction_files(self, mock_coordinator, hive_config_file, tmp_path):
        """Test that launching hive creates instruction files for all bots."""
        # Setup mock coordinator
        mock_coord_instance = MagicMock()
        mock_coord_instance.generate_instance_id.return_value = "queen003"
        mock_coord_instance.register_bot.return_value = "BOT-00001"
        mock_coordinator.return_value = mock_coord_instance

        deia_root = tmp_path / ".deia"
        manager = HiveManager(deia_root=str(deia_root))
        result = manager.launch_hive(str(hive_config_file))

        # Check instruction files were created
        instructions_dir = deia_root / "instructions"
        assert (instructions_dir / "BOT-00001-instructions.md").exists()
        assert (instructions_dir / "BOT-00002-instructions.md").exists()
        assert (instructions_dir / "BOT-00003-instructions.md").exists()

    def test_launch_hive_no_queen_mode(self, hive_config_file, tmp_path):
        """Test launching hive without becoming Queen."""
        manager = HiveManager(deia_root=str(tmp_path / ".deia"))
        result = manager.launch_hive(str(hive_config_file), become_queen=False)

        assert result['success'] is True
        assert result['queen_id'] is None
        assert 'drones_initialized' in result


class TestHiveValidation:
    """Test hive configuration validation."""

    def test_validate_hive_config_valid(self, sample_hive_config):
        """Test validation of valid hive config."""
        manager = HiveManager()
        is_valid, errors = manager.validate_hive_config(sample_hive_config)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_hive_config_missing_queen(self, sample_hive_config):
        """Test validation fails when queen is missing."""
        del sample_hive_config['queen']

        manager = HiveManager()
        is_valid, errors = manager.validate_hive_config(sample_hive_config)

        assert is_valid is False
        assert any('queen' in error.lower() for error in errors)

    def test_validate_hive_config_missing_drones(self, sample_hive_config):
        """Test validation fails when drones are missing."""
        del sample_hive_config['drones']

        manager = HiveManager()
        is_valid, errors = manager.validate_hive_config(sample_hive_config)

        assert is_valid is False
        assert any('drones' in error.lower() for error in errors)

    def test_validate_hive_config_invalid_bot_id(self, sample_hive_config):
        """Test validation fails with invalid bot ID format."""
        sample_hive_config['queen']['bot_id'] = 'INVALID-ID'

        manager = HiveManager()
        is_valid, errors = manager.validate_hive_config(sample_hive_config)

        assert is_valid is False
        assert any('bot_id' in error.lower() for error in errors)
