"""
Service Registry - Bot discovery and management with persistence and recovery.

Maintains registry of all running bots with their service endpoints.
Persists to disk every 10s for recovery after crashes.
Cleans stale entries and prevents duplicate bot launches.
Provides audit trail of all registry changes.
"""

from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import json
import hashlib
import os
import psutil


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
        Initialize registry with persistence and recovery.

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

        # Audit trail for registry changes
        self.audit_log_path = self.registry_path.parent / "registry-changes.jsonl"

        # Initialize if doesn't exist
        if not self.registry_path.exists():
            self._save({"bots": {}, "updated_at": datetime.now().isoformat()})

        # Clean up stale entries on startup
        self.cleanup_stale_entries()

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

        Prevents duplicate bot launches - returns False if bot already running.

        Args:
            bot_id: Full bot ID (e.g., "deiasolutions-CLAUDE-CODE-001")
            port: Service port
            repo: Repository name (extracted from bot_id if not provided)

        Returns:
            True if registered successfully, False if bot already running
        """
        # Check for duplicate
        if self.check_duplicate_bot(bot_id):
            print(f"[REGISTRY] ERROR: Bot {bot_id} is already running!")
            return False

        registry = self._load()
        bots = registry.get("bots", {})

        # Extract repo from bot_id if not provided
        if repo is None and "-" in bot_id:
            repo = bot_id.split("-")[0]

        bot_info = {
            "port": port,
            "pid": os.getpid(),
            "repo": repo,
            "status": "starting",
            "registered_at": datetime.now().isoformat(),
            "last_heartbeat": datetime.now().isoformat()
        }

        bots[bot_id] = bot_info
        registry["bots"] = bots
        self._save(registry)

        # Audit log
        self._audit_log("registered", bot_id, {"port": port, "pid": os.getpid()})

        print(f"[REGISTRY] Registered {bot_id} on port {port}")
        return True

    def unregister(self, bot_id: str):
        """
        Remove bot from registry.

        Args:
            bot_id: Bot ID to unregister
        """
        registry = self._load()
        bots = registry.get("bots", {})

        if bot_id in bots:
            bot_info = bots[bot_id]
            del bots[bot_id]
            registry["bots"] = bots
            self._save(registry)

            # Audit log
            self._audit_log("unregistered", bot_id, {"port": bot_info.get("port")})

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

    def cleanup_stale_entries(self, timeout_seconds: int = 300) -> List[str]:
        """
        Clean up stale bot entries (processes that have exited).

        A bot is considered stale if its PID doesn't exist or last heartbeat > timeout.

        Args:
            timeout_seconds: Consider entry stale if no heartbeat in this many seconds

        Returns:
            List of removed bot IDs
        """
        registry = self._load()
        bots = registry.get("bots", {})
        removed = []
        cutoff_time = datetime.now() - timedelta(seconds=timeout_seconds)

        for bot_id, info in list(bots.items()):
            # Check if PID is alive
            pid = info.get("pid")
            is_alive = False

            if pid:
                try:
                    is_alive = psutil.pid_exists(pid)
                except Exception:
                    is_alive = False

            # Check heartbeat timeout
            last_heartbeat = info.get("last_heartbeat")
            if last_heartbeat:
                try:
                    hb_time = datetime.fromisoformat(last_heartbeat)
                    is_stale = hb_time < cutoff_time
                except Exception:
                    is_stale = True
            else:
                is_stale = True

            if not is_alive or is_stale:
                removed.append(bot_id)
                del bots[bot_id]
                self._audit_log("stale_entry_removed", bot_id, info)
                print(f"[REGISTRY] Removed stale entry: {bot_id} (PID {pid})")

        if removed:
            registry["bots"] = bots
            self._save(registry)

        return removed

    def check_duplicate_bot(self, bot_id: str) -> bool:
        """
        Check if a bot with this ID is already running.

        Args:
            bot_id: Bot ID to check

        Returns:
            True if bot is already running
        """
        bot = self.get_bot(bot_id)
        if not bot:
            return False

        # Check if PID is alive
        pid = bot.get("pid")
        if pid:
            try:
                return psutil.pid_exists(pid)
            except Exception:
                return False

        return False

    def _audit_log(self, action: str, bot_id: str, details: Optional[Dict] = None) -> None:
        """
        Log a registry change to audit trail.

        Args:
            action: What action was taken (e.g., "registered", "unregistered", "stale_removed")
            bot_id: Bot ID involved
            details: Additional details
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "bot_id": bot_id,
            "details": details or {}
        }

        try:
            with open(self.audit_log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[REGISTRY] Failed to write audit log: {e}")
