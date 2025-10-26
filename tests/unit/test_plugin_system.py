"""
Unit tests for plugin_system module.

Tests plugin discovery, loading, lifecycle management, error isolation, and help integration.
"""

import pytest
import tempfile
import sys
from pathlib import Path
from src.deia.plugin_system import (
    PluginManager, BasePlugin, PluginMetadata, PluginContext,
    PluginResult, PluginStatus, PluginDiscoverer, PluginLoader,
    PluginRegistry, SamplePlugin
)


@pytest.fixture
def temp_plugin_dir():
    """Create temporary plugin directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_metadata():
    """Sample plugin metadata."""
    return PluginMetadata(
        name="test_plugin",
        version="1.0.0",
        author="Test Author",
        description="Test plugin",
        entry_point="main"
    )


@pytest.fixture
def plugin_context():
    """Sample plugin context."""
    return PluginContext(
        name="test_plugin",
        args=["arg1", "arg2"],
        kwargs={"key": "value"},
        config={"debug": True}
    )


@pytest.fixture
def plugin_manager(temp_plugin_dir):
    """Create plugin manager with temp directory."""
    return PluginManager([temp_plugin_dir])


# ===== PLUGIN INTERFACE TESTS =====

class TestBasePlugin:
    """Test base plugin functionality."""

    def test_plugin_initialization(self, sample_metadata):
        """Test plugin initialization."""
        plugin = SamplePlugin(sample_metadata)
        assert plugin.metadata.name == "test_plugin"
        assert plugin.status == PluginStatus.DISCOVERED

    def test_plugin_state_management(self, sample_metadata):
        """Test plugin state storage."""
        plugin = SamplePlugin(sample_metadata)
        plugin.set_state("key", "value")
        assert plugin.get_state("key") == "value"

    def test_plugin_state_default(self, sample_metadata):
        """Test default state value."""
        plugin = SamplePlugin(sample_metadata)
        assert plugin.get_state("missing", "default") == "default"

    def test_plugin_help_text(self, sample_metadata):
        """Test plugin help text."""
        plugin = SamplePlugin(sample_metadata)
        help_text = plugin.get_help()
        assert len(help_text) > 0
        assert "Sample plugin" in help_text

    def test_sample_plugin_lifecycle(self, sample_metadata, plugin_context):
        """Test sample plugin lifecycle."""
        plugin = SamplePlugin(sample_metadata)

        # Initialize
        plugin.initialize(plugin_context)
        assert plugin.get_state("call_count") == 0

        # Execute
        result = plugin.execute(plugin_context)
        assert result.success
        assert plugin.get_state("call_count") == 1

        # Cleanup
        plugin.cleanup()
        assert plugin.get_state("call_count") is None


# ===== DISCOVERY TESTS =====

class TestPluginDiscovery:
    """Test plugin discovery."""

    def test_discovery_empty_directory(self, plugin_manager):
        """Test discovery in empty directory."""
        discovered = plugin_manager.discover_plugins()
        assert isinstance(discovered, dict)

    def test_discovery_finds_plugins(self, temp_plugin_dir, plugin_manager):
        """Test discovery finds plugin files."""
        # Create a sample plugin file
        plugin_file = temp_plugin_dir / "my_plugin.py"
        plugin_file.write_text("""
from src.deia.plugin_system import BasePlugin, PluginContext, PluginResult

class Plugin(BasePlugin):
    def initialize(self, context): pass
    def execute(self, context):
        return PluginResult(success=True, output="test")
    def cleanup(self): pass
""")

        discovered = plugin_manager.discover_plugins()
        assert "my_plugin" in discovered

    def test_discovery_ignores_private_files(self, temp_plugin_dir, plugin_manager):
        """Test discovery ignores private files."""
        # Create private plugin file
        plugin_file = temp_plugin_dir / "_private.py"
        plugin_file.write_text("# private")

        discovered = plugin_manager.discover_plugins()
        assert "_private" not in discovered

    def test_discoverer_get_plugin_path(self, temp_plugin_dir):
        """Test getting plugin path."""
        plugin_file = temp_plugin_dir / "test.py"
        plugin_file.write_text("# test")

        discoverer = PluginDiscoverer([temp_plugin_dir])
        discoverer.discover()

        path = discoverer.get_plugin_path("test")
        assert path == plugin_file


# ===== LOADING TESTS =====

class TestPluginLoading:
    """Test plugin loading."""

    def test_load_plugin_success(self, temp_plugin_dir):
        """Test successful plugin loading."""
        # Create plugin file
        plugin_file = temp_plugin_dir / "valid_plugin.py"
        plugin_file.write_text("""
from src.deia.plugin_system import BasePlugin, PluginResult

class Plugin(BasePlugin):
    def initialize(self, context): pass
    def execute(self, context):
        return PluginResult(success=True, output="test")
    def cleanup(self): pass
""")

        discoverer = PluginDiscoverer([temp_plugin_dir])
        discoverer.discover()
        loader = PluginLoader(discoverer)

        metadata = PluginMetadata(
            name="valid_plugin",
            version="1.0",
            author="Test",
            description="Test"
        )

        plugin = loader.load_plugin("valid_plugin", metadata)
        assert plugin is not None
        assert isinstance(plugin, BasePlugin)

    def test_load_plugin_not_found(self, temp_plugin_dir):
        """Test loading non-existent plugin."""
        discoverer = PluginDiscoverer([temp_plugin_dir])
        discoverer.discover()
        loader = PluginLoader(discoverer)

        metadata = PluginMetadata(
            name="nonexistent",
            version="1.0",
            author="Test",
            description="Test"
        )

        # Non-existent plugin should return None gracefully
        result = loader.load_plugin("nonexistent", metadata)
        assert result is None

    def test_load_plugin_module_caching(self, temp_plugin_dir):
        """Test that loaded modules are cached."""
        plugin_file = temp_plugin_dir / "cached.py"
        plugin_file.write_text("""
from src.deia.plugin_system import BasePlugin, PluginResult

class Plugin(BasePlugin):
    def initialize(self, context): pass
    def execute(self, context):
        return PluginResult(success=True)
    def cleanup(self): pass
""")

        discoverer = PluginDiscoverer([temp_plugin_dir])
        discoverer.discover()
        loader = PluginLoader(discoverer)

        mod1 = loader.load_plugin_module("cached")
        mod2 = loader.load_plugin_module("cached")

        assert mod1 is mod2  # Same object due to caching

    def test_unload_plugin(self, temp_plugin_dir):
        """Test plugin unloading."""
        plugin_file = temp_plugin_dir / "temp.py"
        plugin_file.write_text("""
from src.deia.plugin_system import BasePlugin, PluginResult

class Plugin(BasePlugin):
    def initialize(self, context): pass
    def execute(self, context):
        return PluginResult(success=True)
    def cleanup(self): pass
""")

        discoverer = PluginDiscoverer([temp_plugin_dir])
        discoverer.discover()
        loader = PluginLoader(discoverer)

        loader.load_plugin_module("temp")
        assert "temp" in sys.modules

        loader.unload_plugin("temp")
        assert "temp" not in sys.modules


# ===== REGISTRY TESTS =====

class TestPluginRegistry:
    """Test plugin registry."""

    def test_register_plugin(self, sample_metadata):
        """Test plugin registration."""
        registry = PluginRegistry()
        plugin = SamplePlugin(sample_metadata)

        registry.register("test", plugin, sample_metadata)

        assert registry.get_plugin("test") == plugin
        assert registry.get_metadata("test") == sample_metadata

    def test_list_plugins(self, sample_metadata):
        """Test listing plugins."""
        registry = PluginRegistry()
        plugin1 = SamplePlugin(sample_metadata)
        plugin2 = SamplePlugin(sample_metadata)

        registry.register("plugin1", plugin1, sample_metadata)
        registry.register("plugin2", plugin2, sample_metadata)

        plugins = registry.list_plugins()
        assert "plugin1" in plugins
        assert "plugin2" in plugins

    def test_plugin_status(self, sample_metadata):
        """Test plugin status tracking."""
        registry = PluginRegistry()
        plugin = SamplePlugin(sample_metadata)
        registry.register("test", plugin, sample_metadata)

        registry.set_status("test", PluginStatus.INITIALIZED)
        assert registry.get_status("test") == PluginStatus.INITIALIZED

    def test_status_history(self, sample_metadata):
        """Test status history tracking."""
        registry = PluginRegistry()
        plugin = SamplePlugin(sample_metadata)
        registry.register("test", plugin, sample_metadata)

        registry.set_status("test", PluginStatus.INITIALIZED)
        registry.set_status("test", PluginStatus.RUNNING)

        history = registry.get_status_history("test")
        assert len(history) >= 3  # LOADED + INITIALIZED + RUNNING
        assert history[-2][1] == PluginStatus.INITIALIZED
        assert history[-1][1] == PluginStatus.RUNNING

    def test_unregister_plugin(self, sample_metadata):
        """Test plugin unregistration."""
        registry = PluginRegistry()
        plugin = SamplePlugin(sample_metadata)
        registry.register("test", plugin, sample_metadata)

        registry.unregister("test")

        assert registry.get_plugin("test") is None
        assert "test" not in registry.list_plugins()


# ===== MANAGER TESTS =====

class TestPluginManager:
    """Test plugin manager."""

    def test_manager_initialization(self, temp_plugin_dir):
        """Test manager initialization."""
        manager = PluginManager([temp_plugin_dir])
        assert manager is not None
        assert len(manager.plugin_dirs) > 0

    def test_load_all_plugins(self, temp_plugin_dir):
        """Test loading all plugins."""
        # Create a plugin
        plugin_file = temp_plugin_dir / "test_load.py"
        plugin_file.write_text("""
from src.deia.plugin_system import BasePlugin, PluginResult

class Plugin(BasePlugin):
    def initialize(self, context): pass
    def execute(self, context):
        return PluginResult(success=True)
    def cleanup(self): pass
""")

        manager = PluginManager([temp_plugin_dir])
        manager.discover_plugins()

        metadata = PluginMetadata(
            name="test_load",
            version="1.0",
            author="Test",
            description="Test"
        )

        loaded = manager.load_all({"test_load": metadata})
        assert "test_load" in loaded

    def test_execute_plugin_success(self, sample_metadata, plugin_context):
        """Test successful plugin execution."""
        manager = PluginManager([])
        plugin = SamplePlugin(sample_metadata)
        manager.registry.register("test", plugin, sample_metadata)
        manager.initialize_plugin("test", plugin_context)

        result = manager.execute_plugin("test", plugin_context)

        assert result.success
        assert result.output is not None
        assert result.duration_ms > 0

    def test_execute_plugin_not_found(self, plugin_context):
        """Test execution of non-existent plugin."""
        manager = PluginManager([])

        result = manager.execute_plugin("nonexistent", plugin_context)

        assert not result.success
        assert "not found" in result.error

    def test_execute_plugin_error_isolation(self, sample_metadata, plugin_context):
        """Test error isolation in plugin execution."""
        # Create a plugin that raises error
        error_metadata = PluginMetadata(
            name="error_plugin",
            version="1.0",
            author="Test",
            description="Error plugin"
        )

        class ErrorPlugin(BasePlugin):
            def initialize(self, context): pass
            def execute(self, context):
                raise ValueError("Intentional error")
            def cleanup(self): pass

        manager = PluginManager([])
        plugin = ErrorPlugin(error_metadata)
        manager.registry.register("error", plugin, error_metadata)
        manager.initialize_plugin("error", plugin_context)

        result = manager.execute_plugin("error", plugin_context)

        assert not result.success
        assert "Intentional error" in result.error
        assert result.traceback is not None
        # Plugin should not crash manager

    def test_cleanup_plugin(self, sample_metadata, plugin_context):
        """Test plugin cleanup."""
        manager = PluginManager([])
        plugin = SamplePlugin(sample_metadata)
        manager.registry.register("test", plugin, sample_metadata)
        manager.initialize_plugin("test", plugin_context)

        # Add some state
        plugin.set_state("data", "important")

        manager.cleanup_plugin("test")

        assert plugin.get_state("data") is None

    def test_get_plugin_help(self, sample_metadata):
        """Test getting plugin help."""
        manager = PluginManager([])
        plugin = SamplePlugin(sample_metadata)
        manager.registry.register("test", plugin, sample_metadata)

        help_text = manager.get_plugin_help("test")
        assert len(help_text) > 0

    def test_get_all_plugins_help(self, sample_metadata):
        """Test getting help for all plugins."""
        manager = PluginManager([])
        plugin = SamplePlugin(sample_metadata)
        manager.registry.register("test", plugin, sample_metadata)

        help_text = manager.get_plugin_help()
        assert "Available Plugins" in help_text

    def test_execution_history(self, sample_metadata, plugin_context):
        """Test execution history tracking."""
        manager = PluginManager([])
        plugin = SamplePlugin(sample_metadata)
        manager.registry.register("test", plugin, sample_metadata)
        manager.initialize_plugin("test", plugin_context)

        manager.execute_plugin("test", plugin_context)
        manager.execute_plugin("test", plugin_context)

        history = manager.get_execution_history()
        assert len(history) >= 2
        assert all(h["plugin"] == "test" for h in history)

    def test_get_plugin_status(self, sample_metadata):
        """Test getting plugin status."""
        manager = PluginManager([])
        plugin = SamplePlugin(sample_metadata)
        manager.registry.register("test", plugin, sample_metadata)

        status = manager.get_plugin_status("test")
        assert "status" in status
        assert "metadata" in status

    def test_get_all_plugins_status(self, sample_metadata):
        """Test getting status for all plugins."""
        manager = PluginManager([])
        plugin1 = SamplePlugin(sample_metadata)
        plugin2 = SamplePlugin(sample_metadata)

        manager.registry.register("test1", plugin1, sample_metadata)
        manager.registry.register("test2", plugin2, sample_metadata)

        status = manager.get_plugin_status()
        assert "test1" in status
        assert "test2" in status

    def test_initialize_plugin(self, sample_metadata, plugin_context):
        """Test plugin initialization."""
        manager = PluginManager([])
        plugin = SamplePlugin(sample_metadata)
        manager.registry.register("test", plugin, sample_metadata)

        success = manager.initialize_plugin("test", plugin_context)

        assert success
        assert plugin.status == PluginStatus.INITIALIZED

    def test_cleanup_all_plugins(self, sample_metadata, plugin_context):
        """Test cleanup all plugins."""
        manager = PluginManager([])
        plugin1 = SamplePlugin(sample_metadata)
        plugin2 = SamplePlugin(sample_metadata)

        manager.registry.register("test1", plugin1, sample_metadata)
        manager.registry.register("test2", plugin2, sample_metadata)

        manager.initialize_plugin("test1", plugin_context)
        manager.initialize_plugin("test2", plugin_context)

        manager.cleanup_all()

        # Both should be cleaned up without errors


# ===== INTEGRATION TESTS =====

class TestPluginIntegration:
    """Test end-to-end plugin system."""

    def test_full_plugin_lifecycle(self, temp_plugin_dir):
        """Test complete plugin lifecycle."""
        # Create plugin
        plugin_file = temp_plugin_dir / "lifecycle.py"
        plugin_file.write_text("""
from src.deia.plugin_system import BasePlugin, PluginResult

class Plugin(BasePlugin):
    def initialize(self, context):
        self.set_state("initialized", True)

    def execute(self, context):
        return PluginResult(
            success=True,
            output={"message": "executed"}
        )

    def cleanup(self):
        self.set_state("initialized", False)
""")

        # Load and execute
        manager = PluginManager([temp_plugin_dir])
        manager.discover_plugins()

        metadata = PluginMetadata(
            name="lifecycle",
            version="1.0",
            author="Test",
            description="Test"
        )

        loaded = manager.load_all({"lifecycle": metadata})
        assert "lifecycle" in loaded

        context = PluginContext(name="lifecycle", args=[])
        manager.initialize_plugin("lifecycle", context)

        result = manager.execute_plugin("lifecycle", context)
        assert result.success

        manager.cleanup_plugin("lifecycle")

    def test_multiple_plugin_isolation(self, temp_plugin_dir):
        """Test isolation between multiple plugins."""
        # Create two plugins
        for name in ["plugin_a", "plugin_b"]:
            plugin_file = temp_plugin_dir / f"{name}.py"
            plugin_file.write_text(f"""
from src.deia.plugin_system import BasePlugin, PluginResult

class Plugin(BasePlugin):
    def initialize(self, context):
        pass

    def execute(self, context):
        return PluginResult(
            success=True,
            output={{"plugin": "{name}"}}
        )

    def cleanup(self):
        pass
""")

        manager = PluginManager([temp_plugin_dir])
        manager.discover_plugins()

        metadata_a = PluginMetadata(
            name="plugin_a", version="1.0", author="Test", description="A"
        )
        metadata_b = PluginMetadata(
            name="plugin_b", version="1.0", author="Test", description="B"
        )

        loaded = manager.load_all({
            "plugin_a": metadata_a,
            "plugin_b": metadata_b
        })

        assert "plugin_a" in loaded
        assert "plugin_b" in loaded

        context = PluginContext(name="test", args=[])
        manager.initialize_plugin("plugin_a", context)
        manager.initialize_plugin("plugin_b", context)

        result_a = manager.execute_plugin("plugin_a", context)
        result_b = manager.execute_plugin("plugin_b", context)

        assert result_a.output["plugin"] == "plugin_a"
        assert result_b.output["plugin"] == "plugin_b"
