"""
Configuration Manager - Centralized system configuration without code changes.

Loads configuration from YAML/JSON files, validates settings, supports hot-reload,
and logs all configuration changes for audit trail.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum
import json
import yaml
from datetime import datetime


class ConfigFormat(Enum):
    """Supported configuration file formats."""
    YAML = "yaml"
    JSON = "json"


@dataclass
class ConfigThresholds:
    """Alert and scaling thresholds."""
    cpu_warning_percent: float = 0.80
    cpu_critical_percent: float = 0.95
    memory_warning_percent: float = 0.75
    memory_critical_percent: float = 0.90
    queue_backlog_threshold: int = 10
    bot_failure_threshold: float = 0.30
    message_failure_threshold: int = 5

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ConfigBotLimits:
    """Bot scaling and resource limits."""
    min_bots: int = 1
    max_bots: int = 10
    max_concurrent_tasks_per_bot: int = 3
    port_range_start: int = 8001
    port_range_end: int = 8999

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ConfigTimeouts:
    """System timeout settings."""
    task_timeout_seconds: int = 3600
    message_ttl_seconds: int = 3600
    bot_health_check_interval_seconds: int = 30
    scaling_evaluation_interval_seconds: int = 60
    config_reload_check_interval_seconds: int = 300

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ConfigFeatureFlags:
    """Feature enable/disable flags."""
    messaging_enabled: bool = True
    adaptive_scheduling_enabled: bool = True
    health_monitoring_enabled: bool = True
    auto_scaling_enabled: bool = True
    audit_logging_enabled: bool = True
    graceful_degradation_enabled: bool = True

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ConfigLearning:
    """Adaptive learning configuration."""
    learning_rate: float = 0.1
    min_samples_for_recommendation: int = 3
    min_confidence_threshold: float = 0.7
    reset_learning_on_major_version_change: bool = True

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class Configuration:
    """Complete system configuration."""
    version: str = "1.0"
    environment: str = "production"  # production, staging, development
    debug: bool = False

    thresholds: ConfigThresholds = field(default_factory=ConfigThresholds)
    bot_limits: ConfigBotLimits = field(default_factory=ConfigBotLimits)
    timeouts: ConfigTimeouts = field(default_factory=ConfigTimeouts)
    feature_flags: ConfigFeatureFlags = field(default_factory=ConfigFeatureFlags)
    learning: ConfigLearning = field(default_factory=ConfigLearning)

    # Custom key-value pairs for extensions
    custom: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "version": self.version,
            "environment": self.environment,
            "debug": self.debug,
            "thresholds": self.thresholds.to_dict(),
            "bot_limits": self.bot_limits.to_dict(),
            "timeouts": self.timeouts.to_dict(),
            "feature_flags": self.feature_flags.to_dict(),
            "learning": self.learning.to_dict(),
            "custom": self.custom
        }


class ConfigManager:
    """
    Manages system configuration with hot-reload capability.

    Features:
    - Load from YAML/JSON config files
    - Validate all configuration values
    - Hot-reload: Apply changes without restart
    - Change tracking: Log all config changes
    - Default fallback: Safe defaults if config missing
    """

    def __init__(self, work_dir: Path):
        """
        Initialize configuration manager.

        Args:
            work_dir: Working directory for config files and logs
        """
        self.work_dir = Path(work_dir)
        self.config_dir = self.work_dir / ".deia" / "config"
        self.log_dir = self.work_dir / ".deia" / "bot-logs"

        # Create directories if needed
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.config_log = self.log_dir / "config-changes.jsonl"

        # Current configuration
        self.config = Configuration()
        self.config_file_path: Optional[Path] = None
        self.last_load_time: Optional[str] = None
        self.load_errors: List[str] = []

    def load_config(self, config_name: str = "bot-config") -> bool:
        """
        Load configuration from file.

        Tries to load from YAML first, then JSON.
        Falls back to defaults if file not found.

        Args:
            config_name: Config file name (without extension)

        Returns:
            True if loaded successfully (or defaults used)
        """
        self.load_errors = []

        # Try YAML first
        yaml_path = self.config_dir / f"{config_name}.yaml"
        if yaml_path.exists():
            try:
                return self._load_yaml(yaml_path)
            except Exception as e:
                self.load_errors.append(f"YAML load error: {str(e)}")

        # Try JSON
        json_path = self.config_dir / f"{config_name}.json"
        if json_path.exists():
            try:
                return self._load_json(json_path)
            except Exception as e:
                self.load_errors.append(f"JSON load error: {str(e)}")

        # Neither found, use defaults
        self._log_event("config_loaded_defaults", {
            "reason": "No config file found",
            "yaml_path": str(yaml_path),
            "json_path": str(json_path)
        })

        return True

    def _load_yaml(self, config_path: Path) -> bool:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f) or {}

        self._apply_config(data, config_path)
        return True

    def _load_json(self, config_path: Path) -> bool:
        """Load configuration from JSON file."""
        with open(config_path, 'r') as f:
            data = json.load(f)

        self._apply_config(data, config_path)
        return True

    def _apply_config(self, data: Dict[str, Any], config_path: Path) -> None:
        """
        Apply configuration dictionary to current config.

        Args:
            data: Configuration dictionary
            config_path: Path to config file (for logging)
        """
        # Store current for change tracking
        old_config = self.config.to_dict()

        # Update top-level fields
        if "version" in data:
            self.config.version = str(data["version"])
        if "environment" in data:
            self.config.environment = str(data["environment"])
        if "debug" in data:
            self.config.debug = bool(data["debug"])

        # Update thresholds
        if "thresholds" in data:
            thresh_data = data["thresholds"]
            if "cpu_warning_percent" in thresh_data:
                self.config.thresholds.cpu_warning_percent = float(thresh_data["cpu_warning_percent"])
            if "cpu_critical_percent" in thresh_data:
                self.config.thresholds.cpu_critical_percent = float(thresh_data["cpu_critical_percent"])
            if "memory_warning_percent" in thresh_data:
                self.config.thresholds.memory_warning_percent = float(thresh_data["memory_warning_percent"])
            if "memory_critical_percent" in thresh_data:
                self.config.thresholds.memory_critical_percent = float(thresh_data["memory_critical_percent"])
            if "queue_backlog_threshold" in thresh_data:
                self.config.thresholds.queue_backlog_threshold = int(thresh_data["queue_backlog_threshold"])
            if "bot_failure_threshold" in thresh_data:
                self.config.thresholds.bot_failure_threshold = float(thresh_data["bot_failure_threshold"])
            if "message_failure_threshold" in thresh_data:
                self.config.thresholds.message_failure_threshold = int(thresh_data["message_failure_threshold"])

        # Update bot limits
        if "bot_limits" in data:
            limits_data = data["bot_limits"]
            if "min_bots" in limits_data:
                self.config.bot_limits.min_bots = int(limits_data["min_bots"])
            if "max_bots" in limits_data:
                self.config.bot_limits.max_bots = int(limits_data["max_bots"])
            if "max_concurrent_tasks_per_bot" in limits_data:
                self.config.bot_limits.max_concurrent_tasks_per_bot = int(limits_data["max_concurrent_tasks_per_bot"])
            if "port_range_start" in limits_data:
                self.config.bot_limits.port_range_start = int(limits_data["port_range_start"])
            if "port_range_end" in limits_data:
                self.config.bot_limits.port_range_end = int(limits_data["port_range_end"])

        # Update timeouts
        if "timeouts" in data:
            timeout_data = data["timeouts"]
            if "task_timeout_seconds" in timeout_data:
                self.config.timeouts.task_timeout_seconds = int(timeout_data["task_timeout_seconds"])
            if "message_ttl_seconds" in timeout_data:
                self.config.timeouts.message_ttl_seconds = int(timeout_data["message_ttl_seconds"])
            if "bot_health_check_interval_seconds" in timeout_data:
                self.config.timeouts.bot_health_check_interval_seconds = int(timeout_data["bot_health_check_interval_seconds"])
            if "scaling_evaluation_interval_seconds" in timeout_data:
                self.config.timeouts.scaling_evaluation_interval_seconds = int(timeout_data["scaling_evaluation_interval_seconds"])
            if "config_reload_check_interval_seconds" in timeout_data:
                self.config.timeouts.config_reload_check_interval_seconds = int(timeout_data["config_reload_check_interval_seconds"])

        # Update feature flags
        if "feature_flags" in data:
            flags_data = data["feature_flags"]
            if "messaging_enabled" in flags_data:
                self.config.feature_flags.messaging_enabled = bool(flags_data["messaging_enabled"])
            if "adaptive_scheduling_enabled" in flags_data:
                self.config.feature_flags.adaptive_scheduling_enabled = bool(flags_data["adaptive_scheduling_enabled"])
            if "health_monitoring_enabled" in flags_data:
                self.config.feature_flags.health_monitoring_enabled = bool(flags_data["health_monitoring_enabled"])
            if "auto_scaling_enabled" in flags_data:
                self.config.feature_flags.auto_scaling_enabled = bool(flags_data["auto_scaling_enabled"])
            if "audit_logging_enabled" in flags_data:
                self.config.feature_flags.audit_logging_enabled = bool(flags_data["audit_logging_enabled"])
            if "graceful_degradation_enabled" in flags_data:
                self.config.feature_flags.graceful_degradation_enabled = bool(flags_data["graceful_degradation_enabled"])

        # Update learning
        if "learning" in data:
            learning_data = data["learning"]
            if "learning_rate" in learning_data:
                self.config.learning.learning_rate = float(learning_data["learning_rate"])
            if "min_samples_for_recommendation" in learning_data:
                self.config.learning.min_samples_for_recommendation = int(learning_data["min_samples_for_recommendation"])
            if "min_confidence_threshold" in learning_data:
                self.config.learning.min_confidence_threshold = float(learning_data["min_confidence_threshold"])

        # Update custom settings
        if "custom" in data and isinstance(data["custom"], dict):
            self.config.custom.update(data["custom"])

        # Validate
        if not self._validate_config():
            raise ValueError("Configuration validation failed")

        # Track changes
        self.config_file_path = config_path
        self.last_load_time = datetime.now().isoformat()

        self._log_event("config_loaded", {
            "file": str(config_path),
            "changes": self._diff_configs(old_config, self.config.to_dict())
        })

    def _validate_config(self) -> bool:
        """
        Validate all configuration values.

        Returns:
            True if all values are valid
        """
        # Validate thresholds (0-1)
        if not (0 <= self.config.thresholds.cpu_warning_percent <= 1.0):
            self.load_errors.append("Invalid cpu_warning_percent (must be 0-1)")
            return False
        if not (0 <= self.config.thresholds.cpu_critical_percent <= 1.0):
            self.load_errors.append("Invalid cpu_critical_percent (must be 0-1)")
            return False
        if not (0 <= self.config.thresholds.memory_warning_percent <= 1.0):
            self.load_errors.append("Invalid memory_warning_percent (must be 0-1)")
            return False
        if not (0 <= self.config.thresholds.memory_critical_percent <= 1.0):
            self.load_errors.append("Invalid memory_critical_percent (must be 0-1)")
            return False

        # Warning should be < critical
        if self.config.thresholds.cpu_warning_percent >= self.config.thresholds.cpu_critical_percent:
            self.load_errors.append("cpu_warning_percent must be < cpu_critical_percent")
            return False
        if self.config.thresholds.memory_warning_percent >= self.config.thresholds.memory_critical_percent:
            self.load_errors.append("memory_warning_percent must be < memory_critical_percent")
            return False

        # Bot limits sanity
        if self.config.bot_limits.min_bots < 1:
            self.load_errors.append("min_bots must be >= 1")
            return False
        if self.config.bot_limits.max_bots < self.config.bot_limits.min_bots:
            self.load_errors.append("max_bots must be >= min_bots")
            return False
        if self.config.bot_limits.max_concurrent_tasks_per_bot < 1:
            self.load_errors.append("max_concurrent_tasks_per_bot must be >= 1")
            return False

        # Port range sanity
        if self.config.bot_limits.port_range_start < 1024:
            self.load_errors.append("port_range_start must be >= 1024")
            return False
        if self.config.bot_limits.port_range_end <= self.config.bot_limits.port_range_start:
            self.load_errors.append("port_range_end must be > port_range_start")
            return False

        # Timeouts
        if self.config.timeouts.task_timeout_seconds < 1:
            self.load_errors.append("task_timeout_seconds must be >= 1")
            return False
        if self.config.timeouts.message_ttl_seconds < 1:
            self.load_errors.append("message_ttl_seconds must be >= 1")
            return False

        # Learning rates (0-1)
        if not (0 < self.config.learning.learning_rate < 1):
            self.load_errors.append("learning_rate must be 0 < x < 1")
            return False
        if not (0 <= self.config.learning.min_confidence_threshold <= 1.0):
            self.load_errors.append("min_confidence_threshold must be 0-1")
            return False

        return True

    def _diff_configs(self, old: Dict, new: Dict, prefix: str = "") -> Dict[str, Any]:
        """
        Calculate differences between two config dictionaries.

        Args:
            old: Old configuration
            new: New configuration
            prefix: Key prefix for nested dicts

        Returns:
            Dictionary of changes
        """
        changes = {}

        # Check all keys in new (might be new or changed)
        for key, new_val in new.items():
            old_val = old.get(key)

            if isinstance(new_val, dict) and isinstance(old_val, dict):
                # Recurse into nested dicts
                nested_changes = self._diff_configs(old_val, new_val, f"{prefix}{key}.")
                if nested_changes:
                    changes[key] = nested_changes
            elif old_val != new_val:
                changes[key] = {
                    "old": old_val,
                    "new": new_val
                }

        return changes

    def get_config(self) -> Configuration:
        """
        Get current configuration.

        Returns:
            Configuration object
        """
        return self.config

    def get_value(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation path.

        Examples:
        - "thresholds.cpu_warning_percent"
        - "bot_limits.max_bots"
        - "feature_flags.messaging_enabled"

        Args:
            key_path: Dot-notation key path
            default: Default value if not found

        Returns:
            Configuration value
        """
        parts = key_path.split(".")
        current = self.config.to_dict()

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default

        return current

    def reload_if_changed(self, config_name: str = "bot-config") -> bool:
        """
        Check if config file has changed and reload if needed.

        Useful for hot-reload: call periodically to check for changes.

        Args:
            config_name: Config file name (without extension)

        Returns:
            True if reloaded, False if unchanged
        """
        # Check YAML
        yaml_path = self.config_dir / f"{config_name}.yaml"
        if yaml_path.exists() and self.config_file_path != yaml_path:
            try:
                self.load_config(config_name)
                return True
            except Exception:
                return False

        # Check JSON
        json_path = self.config_dir / f"{config_name}.json"
        if json_path.exists() and self.config_file_path != json_path:
            try:
                self.load_config(config_name)
                return True
            except Exception:
                return False

        # Check modification time if we know the file
        if self.config_file_path and self.config_file_path.exists():
            current_mtime = self.config_file_path.stat().st_mtime
            if hasattr(self, '_last_mtime'):
                if current_mtime > self._last_mtime:
                    try:
                        self.load_config(config_name)
                        return True
                    except Exception:
                        return False
            self._last_mtime = current_mtime

        return False

    def save_config(self, format: ConfigFormat = ConfigFormat.YAML) -> bool:
        """
        Save current configuration to file.

        Args:
            format: Output format (YAML or JSON)

        Returns:
            True if saved successfully
        """
        try:
            filename = f"bot-config.{format.value}"
            filepath = self.config_dir / filename

            config_dict = self.config.to_dict()

            if format == ConfigFormat.YAML:
                with open(filepath, 'w') as f:
                    yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
            else:  # JSON
                with open(filepath, 'w') as f:
                    json.dump(config_dict, f, indent=2)

            self._log_event("config_saved", {
                "file": str(filepath),
                "format": format.value
            })

            return True
        except Exception as e:
            self._log_event("config_save_failed", {
                "error": str(e)
            })
            return False

    def get_status(self) -> Dict[str, Any]:
        """
        Get configuration manager status.

        Returns:
            Status dictionary
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "config_file": str(self.config_file_path) if self.config_file_path else None,
            "last_load_time": self.last_load_time,
            "load_errors": self.load_errors,
            "config_version": self.config.version,
            "environment": self.config.environment,
            "debug": self.config.debug
        }

    def _log_event(self, event: str, details: Dict = None) -> None:
        """
        Log configuration event.

        Args:
            event: Event type
            details: Event details
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details or {}
        }

        try:
            with open(self.config_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[CONFIG-MANAGER] Failed to log event: {e}")
