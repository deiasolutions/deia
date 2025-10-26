"""
CLI Plugin System - Extensible plugin architecture for DEIA commands.

Provides plugin discovery, hot-loading, lifecycle management, error isolation,
and CLI integration for user-defined plugins.
"""

from typing import Dict, List, Optional, Any, Callable, Protocol
from dataclasses import dataclass, field
from pathlib import Path
from abc import ABC, abstractmethod
import importlib.util
import sys
import traceback
from enum import Enum
from datetime import datetime


# ===== PLUGIN INTERFACE =====

class PluginStatus(Enum):
    """Plugin lifecycle status."""
    DISCOVERED = "discovered"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    FAILED = "failed"


@dataclass
class PluginMetadata:
    """Plugin metadata and configuration."""
    name: str
    version: str
    author: str
    description: str
    plugin_class: type = None
    entry_point: str = "main"
    config: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class PluginContext:
    """Context passed to plugin during execution."""
    name: str
    args: List[str]
    kwargs: Dict[str, Any] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    logger: Any = None
    env: Dict[str, str] = field(default_factory=dict)


@dataclass
class PluginResult:
    """Result from plugin execution."""
    success: bool
    output: Any = None
    error: Optional[str] = None
    traceback: Optional[str] = None
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BasePlugin(ABC):
    """Base class for all plugins."""

    def __init__(self, metadata: PluginMetadata):
        """Initialize plugin with metadata."""
        self.metadata = metadata
        self.status = PluginStatus.DISCOVERED
        self._state: Dict[str, Any] = {}

    @abstractmethod
    def initialize(self, context: PluginContext) -> None:
        """Initialize plugin resources. Called once on load."""
        pass

    @abstractmethod
    def execute(self, context: PluginContext) -> PluginResult:
        """Execute plugin logic."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up plugin resources. Called on unload."""
        pass

    def get_help(self) -> str:
        """Return help text for plugin."""
        return f"{self.metadata.name}: {self.metadata.description}"

    def set_state(self, key: str, value: Any) -> None:
        """Store state in plugin context."""
        self._state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Retrieve state from plugin context."""
        return self._state.get(key, default)


# ===== PLUGIN DISCOVERY =====

class PluginDiscoverer:
    """Discover plugins from filesystem."""

    def __init__(self, plugin_dirs: List[Path]):
        """Initialize with plugin search directories."""
        self.plugin_dirs = [Path(d) for d in plugin_dirs]
        self.discovered_plugins: Dict[str, Path] = {}

    def discover(self) -> Dict[str, Path]:
        """Discover all plugins in registered directories."""
        self.discovered_plugins = {}

        for plugin_dir in self.plugin_dirs:
            if not plugin_dir.exists():
                continue

            # Find all .py files in plugin directory
            for plugin_file in plugin_dir.glob("*.py"):
                if plugin_file.name.startswith("_"):
                    continue

                plugin_name = plugin_file.stem
                self.discovered_plugins[plugin_name] = plugin_file

        return self.discovered_plugins

    def get_plugin_path(self, name: str) -> Optional[Path]:
        """Get path to plugin by name."""
        return self.discovered_plugins.get(name)


# ===== PLUGIN LOADING =====

class PluginLoader:
    """Load and instantiate plugins."""

    def __init__(self, discoverer: PluginDiscoverer):
        """Initialize with discoverer."""
        self.discoverer = discoverer
        self.loaded_modules: Dict[str, Any] = {}

    def load_plugin_module(self, name: str) -> Optional[Any]:
        """Dynamically load plugin module."""
        if name in self.loaded_modules:
            return self.loaded_modules[name]

        plugin_path = self.discoverer.get_plugin_path(name)
        if not plugin_path:
            return None

        try:
            spec = importlib.util.spec_from_file_location(name, plugin_path)
            if not spec or not spec.loader:
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)

            self.loaded_modules[name] = module
            return module

        except Exception as e:
            raise RuntimeError(f"Failed to load plugin {name}: {str(e)}")

    def load_plugin(self, name: str, metadata: PluginMetadata) -> Optional[BasePlugin]:
        """Load plugin module and instantiate plugin class."""
        try:
            module = self.load_plugin_module(name)
            if not module:
                return None

            # Get plugin class from module
            plugin_class = metadata.plugin_class or getattr(
                module, "Plugin", None
            )

            if not plugin_class:
                raise ValueError(f"No Plugin class found in {name}")

            # Instantiate plugin
            plugin = plugin_class(metadata)
            return plugin

        except Exception as e:
            raise RuntimeError(f"Failed to instantiate plugin {name}: {str(e)}")

    def unload_plugin(self, name: str) -> None:
        """Unload plugin module."""
        if name in sys.modules:
            del sys.modules[name]
        if name in self.loaded_modules:
            del self.loaded_modules[name]


# ===== PLUGIN REGISTRY =====

class PluginRegistry:
    """Central registry for loaded plugins."""

    def __init__(self):
        """Initialize registry."""
        self.plugins: Dict[str, BasePlugin] = {}
        self.metadata: Dict[str, PluginMetadata] = {}
        self.status_log: Dict[str, List[tuple]] = {}  # name -> [(timestamp, status)]

    def register(self, name: str, plugin: BasePlugin, metadata: PluginMetadata) -> None:
        """Register plugin in registry."""
        self.plugins[name] = plugin
        self.metadata[name] = metadata
        self.status_log[name] = [(datetime.now(), PluginStatus.LOADED)]

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get plugin by name."""
        return self.plugins.get(name)

    def list_plugins(self) -> List[str]:
        """List all registered plugins."""
        return list(self.plugins.keys())

    def get_metadata(self, name: str) -> Optional[PluginMetadata]:
        """Get plugin metadata."""
        return self.metadata.get(name)

    def set_status(self, name: str, status: PluginStatus) -> None:
        """Update plugin status."""
        if name not in self.status_log:
            self.status_log[name] = []
        self.status_log[name].append((datetime.now(), status))

        if name in self.plugins:
            self.plugins[name].status = status

    def get_status(self, name: str) -> Optional[PluginStatus]:
        """Get current plugin status."""
        if name in self.plugins:
            return self.plugins[name].status
        return None

    def get_status_history(self, name: str) -> List[tuple]:
        """Get status history for plugin."""
        return self.status_log.get(name, [])

    def unregister(self, name: str) -> None:
        """Unregister plugin."""
        if name in self.plugins:
            del self.plugins[name]
        if name in self.metadata:
            del self.metadata[name]


# ===== PLUGIN MANAGER =====

class PluginManager:
    """Manage plugin lifecycle and execution."""

    def __init__(self, plugin_dirs: List[Path] = None):
        """Initialize plugin manager."""
        self.plugin_dirs = plugin_dirs or [Path(".deia/plugins")]
        self.discoverer = PluginDiscoverer(self.plugin_dirs)
        self.loader = PluginLoader(self.discoverer)
        self.registry = PluginRegistry()
        self.execution_history: List[dict] = []

    def discover_plugins(self) -> Dict[str, Path]:
        """Discover available plugins."""
        return self.discoverer.discover()

    def load_all(self, metadata_map: Dict[str, PluginMetadata]) -> Dict[str, BasePlugin]:
        """Load all discovered plugins."""
        loaded = {}

        for name, path in self.discoverer.discovered_plugins.items():
            try:
                metadata = metadata_map.get(name)
                if not metadata:
                    # Create default metadata
                    metadata = PluginMetadata(
                        name=name,
                        version="0.1.0",
                        author="unknown",
                        description=f"Plugin: {name}"
                    )

                plugin = self.loader.load_plugin(name, metadata)
                if plugin:
                    self.registry.register(name, plugin, metadata)
                    loaded[name] = plugin
                    self.registry.set_status(name, PluginStatus.LOADED)

            except Exception as e:
                self.registry.set_status(name, PluginStatus.ERROR)
                print(f"Failed to load plugin {name}: {str(e)}")

        return loaded

    def initialize_plugin(self, name: str, context: PluginContext) -> bool:
        """Initialize plugin."""
        plugin = self.registry.get_plugin(name)
        if not plugin:
            return False

        try:
            self.registry.set_status(name, PluginStatus.INITIALIZED)
            plugin.initialize(context)
            self.registry.set_status(name, PluginStatus.INITIALIZED)
            return True

        except Exception as e:
            self.registry.set_status(name, PluginStatus.ERROR)
            print(f"Plugin initialization failed: {str(e)}")
            return False

    def execute_plugin(self, name: str, context: PluginContext) -> PluginResult:
        """Execute plugin with error isolation."""
        import time

        plugin = self.registry.get_plugin(name)
        if not plugin:
            return PluginResult(
                success=False,
                error=f"Plugin {name} not found"
            )

        start_time = time.time()

        try:
            self.registry.set_status(name, PluginStatus.RUNNING)

            # Execute plugin
            result = plugin.execute(context)

            # Log execution
            duration_ms = (time.time() - start_time) * 1000
            result.duration_ms = duration_ms

            self.registry.set_status(name, PluginStatus.STOPPED)
            self.execution_history.append({
                "plugin": name,
                "success": result.success,
                "duration_ms": duration_ms,
                "timestamp": datetime.now().isoformat()
            })

            return result

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.registry.set_status(name, PluginStatus.FAILED)

            return PluginResult(
                success=False,
                error=str(e),
                traceback=traceback.format_exc(),
                duration_ms=duration_ms
            )

    def cleanup_plugin(self, name: str) -> None:
        """Clean up plugin resources."""
        plugin = self.registry.get_plugin(name)
        if plugin:
            try:
                plugin.cleanup()
            except Exception as e:
                print(f"Plugin cleanup failed: {str(e)}")

    def cleanup_all(self) -> None:
        """Clean up all plugins."""
        for name in self.registry.list_plugins():
            self.cleanup_plugin(name)

    def get_plugin_help(self, name: str = None) -> str:
        """Get help text for plugin(s)."""
        if name:
            plugin = self.registry.get_plugin(name)
            if plugin:
                return plugin.get_help()
            return f"Plugin {name} not found"

        # Return help for all plugins
        help_text = "Available Plugins:\n"
        for plugin_name in self.registry.list_plugins():
            plugin = self.registry.get_plugin(plugin_name)
            if plugin:
                help_text += f"\n  {plugin_name}: {plugin.get_help()}\n"

        return help_text

    def get_execution_history(self) -> List[dict]:
        """Get execution history."""
        return self.execution_history

    def get_plugin_status(self, name: str = None) -> Dict[str, Any]:
        """Get status of plugin(s)."""
        if name:
            plugin = self.registry.get_plugin(name)
            if not plugin:
                return {"error": f"Plugin {name} not found"}

            return {
                "name": name,
                "status": plugin.status.value,
                "metadata": {
                    "version": self.registry.get_metadata(name).version,
                    "author": self.registry.get_metadata(name).author
                },
                "status_history": [
                    (ts.isoformat(), status.value)
                    for ts, status in self.registry.get_status_history(name)
                ]
            }

        # Return status for all plugins
        status_map = {}
        for plugin_name in self.registry.list_plugins():
            plugin = self.registry.get_plugin(plugin_name)
            status_map[plugin_name] = plugin.status.value

        return status_map


# ===== SAMPLE PLUGIN =====

class SamplePlugin(BasePlugin):
    """Sample plugin demonstrating plugin interface."""

    def initialize(self, context: PluginContext) -> None:
        """Initialize sample plugin."""
        self.set_state("initialized_at", datetime.now().isoformat())
        self.set_state("call_count", 0)

    def execute(self, context: PluginContext) -> PluginResult:
        """Execute sample plugin."""
        try:
            call_count = self.get_state("call_count", 0)
            call_count += 1
            self.set_state("call_count", call_count)

            output = {
                "message": "Sample plugin executed",
                "call_count": call_count,
                "args": context.args,
                "plugin_name": context.name
            }

            return PluginResult(
                success=True,
                output=output,
                metadata={"plugin_type": "sample"}
            )

        except Exception as e:
            return PluginResult(
                success=False,
                error=str(e),
                traceback=traceback.format_exc()
            )

    def cleanup(self) -> None:
        """Clean up sample plugin."""
        self._state.clear()

    def get_help(self) -> str:
        """Get help text."""
        return "Sample plugin - demonstrates plugin interface"
