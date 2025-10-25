"""
Unit tests for ConfigManager service.

Tests configuration loading, validation, hot-reload, and logging.
"""

import pytest
from pathlib import Path
from src.deia.services.config_manager import (
    ConfigManager, Configuration, ConfigFormat, ConfigThresholds,
    ConfigBotLimits, ConfigTimeouts, ConfigFeatureFlags, ConfigLearning
)
import json
import yaml


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory with config structure."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "config").mkdir(parents=True, exist_ok=True)
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def config_manager(temp_work_dir):
    """Create ConfigManager instance."""
    return ConfigManager(temp_work_dir)


class TestConfigManagerBasics:
    """Test basic ConfigManager functionality."""

    def test_initialization(self, config_manager):
        """Test ConfigManager initialization."""
        assert config_manager.work_dir is not None
        assert config_manager.config_dir.exists()
        assert config_manager.log_dir.exists()
        assert config_manager.config is not None

    def test_default_configuration(self, config_manager):
        """Test default configuration values."""
        config = config_manager.get_config()
        assert config.version == "1.0"
        assert config.environment == "production"
        assert config.debug is False

        # Check default thresholds
        assert config.thresholds.cpu_warning_percent == 0.80
        assert config.thresholds.cpu_critical_percent == 0.95

        # Check default bot limits
        assert config.bot_limits.min_bots == 1
        assert config.bot_limits.max_bots == 10

    def test_get_value_with_dot_notation(self, config_manager):
        """Test retrieving values using dot notation."""
        assert config_manager.get_value("thresholds.cpu_warning_percent") == 0.80
        assert config_manager.get_value("bot_limits.max_bots") == 10
        assert config_manager.get_value("feature_flags.messaging_enabled") is True

    def test_get_value_with_default(self, config_manager):
        """Test get_value returns default for missing keys."""
        result = config_manager.get_value("nonexistent.key", default="fallback")
        assert result == "fallback"


class TestConfigLoading:
    """Test configuration loading from files."""

    def test_load_yaml_config(self, temp_work_dir, config_manager):
        """Test loading configuration from YAML file."""
        # Create YAML config
        yaml_config = {
            "version": "2.0",
            "environment": "staging",
            "debug": True,
            "thresholds": {
                "cpu_warning_percent": 0.85,
                "cpu_critical_percent": 0.92
            },
            "bot_limits": {
                "min_bots": 2,
                "max_bots": 20
            }
        }

        config_file = temp_work_dir / ".deia" / "config" / "bot-config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(yaml_config, f)

        # Load config
        success = config_manager.load_config("bot-config")
        assert success
        assert config_manager.config.version == "2.0"
        assert config_manager.config.environment == "staging"
        assert config_manager.config.debug is True
        assert config_manager.config.thresholds.cpu_warning_percent == 0.85
        assert config_manager.config.bot_limits.max_bots == 20

    def test_load_json_config(self, temp_work_dir, config_manager):
        """Test loading configuration from JSON file."""
        json_config = {
            "version": "1.5",
            "environment": "development",
            "bot_limits": {
                "min_bots": 1,
                "max_bots": 5
            }
        }

        config_file = temp_work_dir / ".deia" / "config" / "bot-config.json"
        with open(config_file, 'w') as f:
            json.dump(json_config, f)

        success = config_manager.load_config("bot-config")
        assert success
        assert config_manager.config.version == "1.5"
        assert config_manager.config.bot_limits.max_bots == 5

    def test_load_with_defaults_if_file_missing(self, config_manager):
        """Test that defaults are used if no config file exists."""
        success = config_manager.load_config("nonexistent")
        assert success
        # Should have default values
        assert config_manager.config.version == "1.0"
        assert config_manager.config.bot_limits.max_bots == 10

    def test_yaml_takes_precedence_over_json(self, temp_work_dir, config_manager):
        """Test that YAML is loaded over JSON if both exist."""
        yaml_config = {"version": "yaml-version"}
        json_config = {"version": "json-version"}

        yaml_file = temp_work_dir / ".deia" / "config" / "bot-config.yaml"
        json_file = temp_work_dir / ".deia" / "config" / "bot-config.json"

        with open(yaml_file, 'w') as f:
            yaml.dump(yaml_config, f)
        with open(json_file, 'w') as f:
            json.dump(json_config, f)

        config_manager.load_config("bot-config")
        assert config_manager.config.version == "yaml-version"


class TestConfigValidation:
    """Test configuration validation."""

    def test_validate_cpu_thresholds(self, config_manager):
        """Test CPU threshold validation."""
        # Valid: warning < critical
        config_manager.config.thresholds.cpu_warning_percent = 0.80
        config_manager.config.thresholds.cpu_critical_percent = 0.95
        assert config_manager._validate_config()

        # Invalid: warning >= critical
        config_manager.config.thresholds.cpu_warning_percent = 0.95
        config_manager.config.thresholds.cpu_critical_percent = 0.90
        assert not config_manager._validate_config()

    def test_validate_threshold_ranges(self, config_manager):
        """Test that thresholds are 0-1."""
        # Invalid: > 1
        config_manager.config.thresholds.cpu_warning_percent = 1.5
        assert not config_manager._validate_config()

        # Invalid: < 0
        config_manager.config.thresholds.cpu_warning_percent = -0.1
        assert not config_manager._validate_config()

    def test_validate_bot_limits(self, config_manager):
        """Test bot limit validation."""
        # Invalid: min_bots < 1
        config_manager.config.bot_limits.min_bots = 0
        assert not config_manager._validate_config()

        # Invalid: max < min
        config_manager.config.bot_limits.min_bots = 5
        config_manager.config.bot_limits.max_bots = 3
        assert not config_manager._validate_config()

    def test_validate_port_range(self, config_manager):
        """Test port range validation."""
        # Invalid: start < 1024
        config_manager.config.bot_limits.port_range_start = 500
        assert not config_manager._validate_config()

        # Invalid: end <= start
        config_manager.config.bot_limits.port_range_start = 8000
        config_manager.config.bot_limits.port_range_end = 8000
        assert not config_manager._validate_config()

    def test_validate_learning_rate(self, config_manager):
        """Test learning rate validation."""
        # Invalid: <= 0
        config_manager.config.learning.learning_rate = 0.0
        assert not config_manager._validate_config()

        # Invalid: >= 1
        config_manager.config.learning.learning_rate = 1.0
        assert not config_manager._validate_config()


class TestHotReload:
    """Test hot-reload functionality."""

    def test_reload_detects_changes(self, temp_work_dir, config_manager):
        """Test that reload detects config file changes."""
        # Initial load
        config_manager.load_config("bot-config")
        original_version = config_manager.config.version

        # Create config file with different values
        yaml_config = {"version": "2.0", "bot_limits": {"max_bots": 15}}
        config_file = temp_work_dir / ".deia" / "config" / "bot-config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(yaml_config, f)

        # Reload should detect change
        changed = config_manager.reload_if_changed("bot-config")
        assert changed
        assert config_manager.config.version == "2.0"
        assert config_manager.config.bot_limits.max_bots == 15

    def test_reload_with_no_changes(self, temp_work_dir, config_manager):
        """Test reload returns False if no changes."""
        # Load config
        yaml_config = {"version": "1.0"}
        config_file = temp_work_dir / ".deia" / "config" / "bot-config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(yaml_config, f)

        config_manager.load_config("bot-config")

        # Reload without changes
        changed = config_manager.reload_if_changed("bot-config")
        assert not changed


class TestConfigPersistence:
    """Test saving and loading configuration."""

    def test_save_config_as_yaml(self, config_manager):
        """Test saving configuration as YAML."""
        config_manager.config.version = "2.0"
        config_manager.config.bot_limits.max_bots = 20

        success = config_manager.save_config(ConfigFormat.YAML)
        assert success

        config_file = config_manager.config_dir / "bot-config.yaml"
        assert config_file.exists()

        # Verify contents
        with open(config_file) as f:
            saved = yaml.safe_load(f)
        assert saved["version"] == "2.0"
        assert saved["bot_limits"]["max_bots"] == 20

    def test_save_config_as_json(self, config_manager):
        """Test saving configuration as JSON."""
        config_manager.config.version = "1.5"

        success = config_manager.save_config(ConfigFormat.JSON)
        assert success

        config_file = config_manager.config_dir / "bot-config.json"
        assert config_file.exists()

        with open(config_file) as f:
            saved = json.load(f)
        assert saved["version"] == "1.5"


class TestLogging:
    """Test configuration change logging."""

    def test_config_loaded_logged(self, temp_work_dir, config_manager):
        """Test that config load is logged."""
        yaml_config = {"version": "2.0"}
        config_file = temp_work_dir / ".deia" / "config" / "bot-config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(yaml_config, f)

        config_manager.load_config("bot-config")

        # Check log file exists and has entry
        assert config_manager.config_log.exists()
        with open(config_manager.config_log) as f:
            lines = f.readlines()
        assert len(lines) > 0

        # Parse last entry
        last_entry = json.loads(lines[-1])
        assert last_entry["event"] == "config_loaded"
        assert "file" in last_entry["details"]

    def test_config_saved_logged(self, config_manager):
        """Test that config save is logged."""
        config_manager.save_config(ConfigFormat.YAML)

        assert config_manager.config_log.exists()
        with open(config_manager.config_log) as f:
            lines = f.readlines()
        assert len(lines) > 0

        last_entry = json.loads(lines[-1])
        assert last_entry["event"] == "config_saved"


class TestStatusAndDiagnostics:
    """Test status and diagnostic functions."""

    def test_get_status(self, temp_work_dir, config_manager):
        """Test get_status returns proper information."""
        yaml_config = {"version": "2.0"}
        config_file = temp_work_dir / ".deia" / "config" / "bot-config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(yaml_config, f)

        config_manager.load_config("bot-config")

        status = config_manager.get_status()
        assert status["config_version"] == "2.0"
        assert status["environment"] == "production"
        assert status["config_file"] is not None
        assert status["last_load_time"] is not None


class TestCustomSettings:
    """Test custom configuration settings."""

    def test_custom_settings_support(self, temp_work_dir, config_manager):
        """Test that custom settings are supported."""
        yaml_config = {
            "custom": {
                "my_setting": "value",
                "my_number": 42,
                "my_nested": {"key": "value"}
            }
        }

        config_file = temp_work_dir / ".deia" / "config" / "bot-config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(yaml_config, f)

        config_manager.load_config("bot-config")
        assert config_manager.config.custom["my_setting"] == "value"
        assert config_manager.config.custom["my_number"] == 42
