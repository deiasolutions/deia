"""
Configuration management for DEIA
"""

import json
from pathlib import Path
from typing import Any, Dict


DEFAULT_CONFIG = {
    "version": "0.1.0",
    "platform": "claude-code",
    "project_name": "",
    "sanitization": {
        "enabled": True,
        "auto_detect_pii": True,
        "auto_detect_secrets": True,
        "custom_patterns": []
    },
    "bok": {
        "sync_enabled": True,
        "auto_sync": False,
        "repo_url": "https://github.com/deiasolutions/deia"
    },
    "contribution": {
        "author": "",
        "email": "",
        "anonymous": False
    },
    "projects": {},
    "sync": {
        "enabled": True,
        "downloads_folder": str(Path.home() / "Downloads"),
        "temp_staging_folder": str(Path.home() / "Downloads" / ".deia-staging"),
        "use_temp_staging": True,
        "cleanup_policy": "manual"
    }
}


def create_default_config(project_root: Path, platform: str):
    """Create default config file"""

    config = DEFAULT_CONFIG.copy()
    config['platform'] = platform
    config['project_name'] = project_root.name

    config_path = project_root / '.deia' / 'config.json'
    save_config(config, config_path)


def load_config(config_path: Path = None) -> Dict[str, Any]:
    """Load DEIA configuration"""

    if config_path is None:
        # Find project root and load config
        from .core import find_project_root
        project_root = find_project_root()
        config_path = project_root / '.deia' / 'config.json'

    if not config_path.exists():
        return DEFAULT_CONFIG.copy()

    with open(config_path, 'r') as f:
        return json.load(f)


def save_config(config: Dict[str, Any], config_path: Path = None):
    """Save DEIA configuration"""

    if config_path is None:
        from .core import find_project_root
        project_root = find_project_root()
        config_path = project_root / '.deia' / 'config.json'

    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
