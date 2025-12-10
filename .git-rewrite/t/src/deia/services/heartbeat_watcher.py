import time
from typing import Dict, List

from agent_status_tracker import AgentStatusTracker


class HeartbeatWatcher:
    """Actively monitor agent heartbeats and detect issues"""

    def __init__(self, check_interval: int = 30):
        self.tracker = AgentStatusTracker()
        self.check_interval = check_interval
        self.alerts: List[str] = []

    def watch(self) -> None:
        """Main watch loop"""
        while True:
            stale = self.tracker.check_stale_states()
            if stale:
                self.handle_stale_agents(stale)

            offline = self.detect_offline_agents()
            if offline:
                self.alert_offline(offline)

            time.sleep(self.check_interval)

    def handle_stale_agents(self, stale: Dict[str, str]) -> None:
        """Take action on stale agents"""
        for agent_id, transition in stale.items():
            self.log_alert(f"Agent {agent_id} stale: {transition}")
            self.create_incident_file(agent_id, f"Stale: {transition}")

    def detect_offline_agents(self) -> List[str]:
        """Find agents that should be online but aren't"""
        expected_agents = self.tracker.get_expected_agents()
        current_agents = self.tracker.get_all_agents()

        offline_agents = [
            agent for agent in expected_agents if agent not in current_agents
        ]

        return offline_agents

    def alert_offline(self, offline: List[str]) -> None:
        """Alert on offline agents"""
        for agent_id in offline:
            self.log_alert(f"Agent {agent_id} is offline")
            self.create_incident_file(agent_id, "Offline")

    def log_alert(self, message: str) -> None:
        """Log an alert message"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {message}"
        self.alerts.append(log_message)
        print(log_message)

    def create_incident_file(self, agent_id: str, reason: str) -> None:
        """Create an incident file for an agent issue"""
        timestamp = time.strftime("%Y%m%d%H%M%S")
        incident_filename = f".deia/incidents/{agent_id}_{timestamp}.txt"
        with open(incident_filename, "w") as f:
            f.write(f"Agent: {agent_id}\n")
            f.write(f"Incident Time: {timestamp}\n")
            f.write(f"Reason: {reason}\n")


if __name__ == "__main__":
    watcher = HeartbeatWatcher(check_interval=5)
    watcher.watch()
