"""
Tests for the DEIA configuration management
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from deia.config import DEFAULT_CONFIG, create_default_config, load_config, save_config


class TestDefaultConfig:
    """Test DEFAULT_CONFIG structure"""

    def test_default_config_exists(self):
        """Test that DEFAULT_CONFIG is defined"""
        assert DEFAULT_CONFIG is not None
        assert isinstance(DEFAULT_CONFIG, dict)

    def test_default_config_has_required_fields(self):
        """Test that DEFAULT_CONFIG has all required fields"""
        required_fields = ['version', 'platform', 'project_name', 'sanitization', 'bok', 'contribution', 'projects', 'sync']
        for field in required_fields:
            assert field in DEFAULT_CONFIG

    def test_default_config_sanitization_structure(self):
        """Test sanitization config structure"""
        assert 'enabled' in DEFAULT_CONFIG['sanitization']
        assert 'auto_detect_pii' in DEFAULT_CONFIG['sanitization']
        assert 'auto_detect_secrets' in DEFAULT_CONFIG['sanitization']
        assert 'custom_patterns' in DEFAULT_CONFIG['sanitization']

    def test_default_config_bok_structure(self):
        """Test BOK config structure"""
        assert 'sync_enabled' in DEFAULT_CONFIG['bok']
        assert 'auto_sync' in DEFAULT_CONFIG['bok']
        assert 'repo_url' in DEFAULT_CONFIG['bok']

    def test_default_config_contribution_structure(self):
        """Test contribution config structure"""
        assert 'author' in DEFAULT_CONFIG['contribution']
        assert 'email' in DEFAULT_CONFIG['contribution']
        assert 'anonymous' in DEFAULT_CONFIG['contribution']

    def test_default_config_sync_structure(self):
        """Test sync config structure"""
        assert 'enabled' in DEFAULT_CONFIG['sync']
        assert 'downloads_folder' in DEFAULT_CONFIG['sync']
        assert 'temp_staging_folder' in DEFAULT_CONFIG['sync']
        assert 'use_temp_staging' in DEFAULT_CONFIG['sync']
        assert 'cleanup_policy' in DEFAULT_CONFIG['sync']


class TestCreateDefaultConfig:
    """Test create_default_config function"""

    def test_create_default_config(self, tmp_path):
        """Test creating default config file"""
        project_root = tmp_path / "test_project"
        project_root.mkdir()
        deia_dir = project_root / ".deia"
        deia_dir.mkdir()

        create_default_config(project_root, "claude-code")

        config_file = deia_dir / "config.json"
        assert config_file.exists()

        config = json.loads(config_file.read_text())
        assert config['platform'] == 'claude-code'
        assert config['project_name'] == 'test_project'

    def test_create_default_config_with_different_platform(self, tmp_path):
        """Test creating config with different platform"""
        project_root = tmp_path / "test_project"
        project_root.mkdir()
        deia_dir = project_root / ".deia"
        deia_dir.mkdir()

        create_default_config(project_root, "custom-platform")

        config_file = deia_dir / "config.json"
        config = json.loads(config_file.read_text())
        assert config['platform'] == 'custom-platform'

    def test_create_default_config_preserves_defaults(self, tmp_path):
        """Test that creating config preserves DEFAULT_CONFIG values"""
        project_root = tmp_path / "test_project"
        project_root.mkdir()
        deia_dir = project_root / ".deia"
        deia_dir.mkdir()

        create_default_config(project_root, "claude-code")

        config_file = deia_dir / "config.json"
        config = json.loads(config_file.read_text())

        # Check some default values are preserved
        assert config['sanitization']['enabled'] is True
        assert config['bok']['sync_enabled'] is True
        assert config['contribution']['anonymous'] is False


class TestLoadConfig:
    """Test load_config function"""

    def test_load_config_from_file(self, tmp_path):
        """Test loading config from specific file"""
        config_file = tmp_path / "config.json"
        test_config = {'test': 'value', 'platform': 'test'}
        config_file.write_text(json.dumps(test_config))

        loaded_config = load_config(config_file)
        assert loaded_config['test'] == 'value'
        assert loaded_config['platform'] == 'test'

    def test_load_config_nonexistent_file_returns_default(self, tmp_path):
        """Test loading from nonexistent file returns DEFAULT_CONFIG"""
        nonexistent = tmp_path / "nonexistent.json"

        loaded_config = load_config(nonexistent)
        assert loaded_config == DEFAULT_CONFIG

    def test_load_config_with_valid_json(self, tmp_path):
        """Test loading config with valid JSON content"""
        config_file = tmp_path / "config.json"
        test_config = {
            'version': '1.0.0',
            'platform': 'test-platform',
            'project_name': 'test-project',
            'custom_field': 'custom_value'
        }
        config_file.write_text(json.dumps(test_config))

        loaded_config = load_config(config_file)
        assert loaded_config['version'] == '1.0.0'
        assert loaded_config['platform'] == 'test-platform'
        assert loaded_config['custom_field'] == 'custom_value'


class TestSaveConfig:
    """Test save_config function"""

    def test_save_config_to_file(self, tmp_path):
        """Test saving config to specific file"""
        config_file = tmp_path / "config.json"
        test_config = {'test': 'value', 'number': 42}

        save_config(test_config, config_file)

        assert config_file.exists()
        loaded = json.loads(config_file.read_text())
        assert loaded['test'] == 'value'
        assert loaded['number'] == 42

    def test_save_config_creates_parent_dirs(self, tmp_path):
        """Test that save_config creates parent directories"""
        nested_path = tmp_path / "nested" / "dirs" / "config.json"
        test_config = {'test': 'value'}

        save_config(test_config, nested_path)

        assert nested_path.exists()
        assert nested_path.parent.exists()

    def test_save_config_formats_json_with_indent(self, tmp_path):
        """Test that saved JSON is properly formatted"""
        config_file = tmp_path / "config.json"
        test_config = {'key1': 'value1', 'key2': 'value2'}

        save_config(test_config, config_file)

        content = config_file.read_text()
        # Check that it's indented (has newlines and spaces)
        assert '\n' in content
        assert '  ' in content

    def test_save_and_load_roundtrip(self, tmp_path):
        """Test saving and loading config maintains data integrity"""
        config_file = tmp_path / "config.json"
        original_config = {
            'version': '1.2.3',
            'nested': {
                'key': 'value',
                'list': [1, 2, 3]
            },
            'boolean': True,
            'number': 42
        }

        save_config(original_config, config_file)
        loaded_config = load_config(config_file)

        assert loaded_config == original_config

    def test_save_config_overwrites_existing_file(self, tmp_path):
        """Test that save_config overwrites existing config file"""
        config_file = tmp_path / "config.json"

        # Save initial config
        save_config({'old': 'value'}, config_file)

        # Overwrite with new config
        save_config({'new': 'value'}, config_file)

        loaded = json.loads(config_file.read_text())
        assert 'new' in loaded
        assert 'old' not in loaded


class TestConfigIntegration:
    """Test config functions working together"""

    def test_create_then_load_config(self, tmp_path):
        """Test creating and then loading a config"""
        project_root = tmp_path / "test_project"
        project_root.mkdir()
        deia_dir = project_root / ".deia"
        deia_dir.mkdir()

        create_default_config(project_root, "claude-code")

        config_file = deia_dir / "config.json"
        loaded_config = load_config(config_file)

        assert loaded_config['platform'] == 'claude-code'
        assert loaded_config['project_name'] == 'test_project'

    def test_modify_and_save_config(self, tmp_path):
        """Test loading, modifying, and saving config"""
        config_file = tmp_path / "config.json"

        # Create initial config
        initial_config = DEFAULT_CONFIG.copy()
        save_config(initial_config, config_file)

        # Load and modify
        loaded = load_config(config_file)
        loaded['custom_field'] = 'custom_value'
        loaded['sanitization']['enabled'] = False

        # Save modified
        save_config(loaded, config_file)

        # Load again and verify
        final = load_config(config_file)
        assert final['custom_field'] == 'custom_value'
        assert final['sanitization']['enabled'] is False
