import datetime
import os
import threading
import time
from pathlib import Path
from typing import Dict, List

import yaml
from colorama import Fore, Style

VALID_STATUSES = {"idle", "busy", "waiting", "paused", "offline"}
VALID_ROLES = {"coordinator", "queen", "worker", "drone"}

STATUS_COLORS = {
    "idle": Fore.GREEN,
    "busy": Fore.CYAN,
    "waiting": Fore.YELLOW,
    "paused": Fore.MAGENTA,
    "offline": Fore.RED
}

class AgentStatusTracker:
    """Track status of all agents in the hive"""

    def __init__(self, heartbeat_dir: str = "~/.deia/hive/heartbeats/"):
        """Initialize tracker with heartbeat directory"""
        self.heartbeat_dir = Path(heartbeat_dir).expanduser()
        self.heartbeat_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self.agents = self._load_agents()

    def _load_agents(self) -> Dict[str, Dict]:
        agents = {}
        for file in self.heartbeat_dir.glob("*.yaml"):
            agent_id = file.stem.split("-")[0]
            try:
                with file.open() as f:
                    data = yaml.safe_load(f)
                    if self._validate_heartbeat(data):
                        agents[agent_id] = data
            except yaml.YAMLError:
                pass
        return agents

    @staticmethod
    def _validate_heartbeat(data: dict) -> bool:
        if data.get("status") not in VALID_STATUSES:
            return False
        if "agent_id" not in data:
            return False
        # TODO: Add more validations
        return True

    def register_agent(self, agent_id: str, role: str) -> None:
        """Register a new agent in the system"""
        with self._lock:
            if role not in VALID_ROLES:
                raise ValueError(f"Invalid role: {role}")
            if agent_id not in self.agents:
                self.agents[agent_id] = {
                    "agent_id": agent_id,
                    "status": "idle",
                    "role": role,
                    "last_heartbeat": datetime.datetime.now().isoformat()
                }
                self._save_agent(agent_id)

    def update_heartbeat(self, agent_id: str, status: str, current_task: str = None) -> None:
        """Agent reports it's alive and what it's doing"""
        with self._lock:
            if agent_id not in self.agents:
                raise ValueError(f"Unknown agent: {agent_id}")
            if status not in VALID_STATUSES:
                raise ValueError(f"Invalid status: {status}")

            self.agents[agent_id].update({
                "status": status,
                "current_task": current_task,
                "last_heartbeat": datetime.datetime.now().isoformat()
            })
            self._save_agent(agent_id)

    def _save_agent(self, agent_id: str) -> None:
        file = self.heartbeat_dir / f"{agent_id}-heartbeat.yaml"
        with file.open("w") as f:
            yaml.safe_dump(self.agents[agent_id], f)

    def check_heartbeats(self) -> Dict[str, str]:
        """Check all agents, detect offline/stale states"""
        with self._lock:
            offline = {}
            for agent_id, data in self.agents.items():
                last_heartbeat = datetime.datetime.fromisoformat(data["last_heartbeat"])
                if (datetime.datetime.now() - last_heartbeat).total_seconds() > 300:
                    offline[agent_id] = data["status"]
                    data["status"] = "offline"
                    self._save_agent(agent_id)
            stale = self._check_stale_states()
            return {**offline, **stale}

    def _check_stale_states(self) -> Dict[str, str]:
        now = datetime.datetime.now()
        stale = {}
        for agent_id, data in self.agents.items():
            last_update = datetime.datetime.fromisoformat(data["last_heartbeat"])
            status = data["status"]
            if status == "waiting" and (now - last_update).total_seconds() > 900:
                self._transition_state(agent_id, "idle", "timeout")
                stale[agent_id] = "waiting→idle (timeout)"
            elif status == "busy" and (now - last_update).total_seconds() > 1800:
                self._transition_state(agent_id, "offline", "stale")
                stale[agent_id] = "busy→offline (stale)"
        return stale

    def _transition_state(self, agent_id: str, new_state: str, reason: str = None):
        self.agents[agent_id]["status"] = new_state
        self._save_agent(agent_id)
        # TODO: Log state transition

    def get_agent_status(self, agent_id: str) -> Dict:
        """Get current status of specific agent"""
        with self._lock:
            if agent_id not in self.agents:
                return {
                    "agent_id": agent_id,
                    "status": "unknown",
                    "error": "not_registered"
                }
            return self.agents[agent_id].copy()

    def get_all_agents(self) -> Dict[str, Dict]:
        """Get status of all registered agents"""
        with self._lock:
            return {agent_id: data.copy() for agent_id, data in self.agents.items()}

    def get_available_agents(self) -> List[str]:
        """Get list of agents in 'idle' state"""
        with self._lock:
            return [agent_id for agent_id, data in self.agents.items() if data["status"] == "idle"]

    def start_monitor_loop(self, interval: int = 60) -> None:
        """Background thread that checks heartbeats every N seconds"""
        def _monitor_loop():
            while True:
                self.check_heartbeats()
                time.sleep(interval)

        thread = threading.Thread(target=_monitor_loop, daemon=True)
        thread.start()

    def render_dashboard(self) -> str:
        """Render the status dashboard"""
        with self._lock:
            if not self.agents:
                return "No agents registered yet."

            lines = []
            lines.append("┌───────────────────────────────────────────────────────────────┐")
            lines.append("│                  DEIA COORDINATION DASHBOARD                  │")
            lines.append("├───────────────────────────────────────────────────────────────┤")

            # Agent rows
            for agent_id, data in sorted(self.agents.items()):
                status = data.get("status", "unknown")
                task = data.get("current_task", "No task")

                # Status emoji
                emoji_map = {
                    "idle": "🟢",
                    "busy": "🔵",
                    "waiting": "🟡",
                    "paused": "🟣",
                    "offline": "🔴"
                }
                emoji = emoji_map.get(status, "⚪")

                # Truncate task if too long (max 40 chars)
                if task and len(task) > 40:
                    task = task[:37] + "..."
                elif not task:
                    task = "No task"

                # Truncate agent_id if too long (max 15 chars)
                display_id = agent_id[:15] if len(agent_id) > 15 else agent_id

                # Format line: emoji + id (15 chars) + status (8 chars) + task (40 chars)
                line = f"│  {emoji} {display_id:15} [{status.upper():8}] {task:40} │"
                lines.append(line)

            # Summary row
            lines.append("├───────────────────────────────────────────────────────────────┤")

            online = sum(1 for d in self.agents.values() if d.get("status") != "offline")
            offline = sum(1 for d in self.agents.values() if d.get("status") == "offline")
            idle = sum(1 for d in self.agents.values() if d.get("status") == "idle")
            busy = sum(1 for d in self.agents.values() if d.get("status") == "busy")

            summary = f"│   Online: {online}  │  Offline: {offline}  │  Idle: {idle}  │  Busy: {busy}  │"
            # Pad to 64 chars
            while len(summary) < 64:
                summary += " "
            summary += "│"
            lines.append(summary)

            lines.append("└───────────────────────────────────────────────────────────────┘")

            return "\n".join(lines)
