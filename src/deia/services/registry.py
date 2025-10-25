"""
Service Registry - Bot discovery and management.

Maintains registry of all running bots with their service endpoints.
Allows Scrum Master to discover and communicate with worker bots.
"""

from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
import json
import hashlib
import os


class ServiceRegistry:
    """
    Registry of bot services.

    Stores bot metadata including:
    - Bot ID (e.g., "deiasolutions-CLAUDE-CODE-001")
    - Service port
    - Process ID
    - Status
    - Last heartbeat
    """

    def __init__(self, registry_path: Optional[Path] = None):
        """
        Initialize registry.

        Args:
            registry_path: Path to registry file (default: .deia/hive/registry.json)
        """
        if registry_path is None:
            # Search upward for .deia/hive directory (project-specific)
            current = Path.cwd().resolve()
            deia_root = None

            # Search up to 10 levels for .deia/hive (not just .deia)
            for _ in range(10):
                hive_dir = current / ".deia" / "hive"
                if hive_dir.exists() and hive_dir.is_dir():
                    deia_root = current
                    break
                if current.parent == current:  # Reached filesystem root
                    break
                current = current.parent

            # Fall back to current directory if not found
            if deia_root is None:
                deia_root = Path.cwd()

            registry_path = deia_root / ".deia" / "hive" / "registry.json"

        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize if doesn't exist
        if not self.registry_path.exists():
            self._save({"bots": {}, "updated_at": datetime.now().isoformat()})

    def _load(self) -> Dict:
        """Load registry from disk."""
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[REGISTRY] Error loading: {e}")
            return {"bots": {}, "updated_at": datetime.now().isoformat()}

    def _save(self, data: Dict):
        """Save registry to disk."""
        try:
            data["updated_at"] = datetime.now().isoformat()
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[REGISTRY] Error saving: {e}")

    def assign_port(self, bot_id: str) -> int:
        """
        Assign port number to bot.

        Uses consistent hashing so same bot ID always gets same port.
        Range: 8001-8999

        Args:
            bot_id: Full bot ID

        Returns:
            Port number
        """
        # Hash bot ID to get consistent port
        hash_val = int(hashlib.md5(bot_id.encode()).hexdigest(), 16)
        port = 8001 + (hash_val % 999)  # 8001-8999

        # Check if port is in use
        registry = self._load()
        bots = registry.get("bots", {})

        # If this bot already has a port, return it
        if bot_id in bots:
            return bots[bot_id].get("port", port)

        # Check if any other bot is using this port
        used_ports = {b.get("port") for b in bots.values()}

        if port in used_ports:
            # Find next available port
            for p in range(8001, 9000):
                if p not in used_ports:
                    port = p
                    break

        return port

    def register(self, bot_id: str, port: int, repo: Optional[str] = None):
        """
        Register bot in registry.

        Args:
            bot_id: Full bot ID (e.g., "deiasolutions-CLAUDE-CODE-001")
            port: Service port
            repo: Repository name (extracted from bot_id if not provided)
        """
        registry = self._load()
        bots = registry.get("bots", {})

        # Extract repo from bot_id if not provided
        if repo is None and "-" in bot_id:
            repo = bot_id.split("-")[0]

        bots[bot_id] = {
            "port": port,
            "pid": os.getpid(),
            "repo": repo,
            "status": "starting",
            "registered_at": datetime.now().isoformat(),
            "last_heartbeat": datetime.now().isoformat()
        }

        registry["bots"] = bots
        self._save(registry)

        print(f"[REGISTRY] Registered {bot_id} on port {port}")

    def unregister(self, bot_id: str):
        """Remove bot from registry."""
        registry = self._load()
        bots = registry.get("bots", {})

        if bot_id in bots:
            del bots[bot_id]
            registry["bots"] = bots
            self._save(registry)
            print(f"[REGISTRY] Unregistered {bot_id}")

    def heartbeat(self, bot_id: str, status: str = "active"):
        """
        Update bot heartbeat.

        Args:
            bot_id: Bot ID
            status: Current status (active, idle, working, etc.)
        """
        registry = self._load()
        bots = registry.get("bots", {})

        if bot_id in bots:
            bots[bot_id]["last_heartbeat"] = datetime.now().isoformat()
            bots[bot_id]["status"] = status
            registry["bots"] = bots
            self._save(registry)

    def get_bot(self, bot_id: str) -> Optional[Dict]:
        """
        Get bot info from registry.

        Returns:
            Bot metadata dict or None if not found
        """
        registry = self._load()
        return registry.get("bots", {}).get(bot_id)

    def get_all_bots(self) -> Dict[str, Dict]:
        """Get all registered bots."""
        registry = self._load()
        return registry.get("bots", {})

    def get_bots_by_repo(self, repo: str) -> Dict[str, Dict]:
        """Get all bots for a specific repository."""
        all_bots = self.get_all_bots()
        return {
            bot_id: info
            for bot_id, info in all_bots.items()
            if info.get("repo") == repo
        }

    def get_bot_url(self, bot_id: str) -> Optional[str]:
        """
        Get bot service URL.

        Returns:
            URL like "http://localhost:8001" or None if not found
        """
        bot = self.get_bot(bot_id)
        if bot and "port" in bot:
            return f"http://localhost:{bot['port']}"
        return None
