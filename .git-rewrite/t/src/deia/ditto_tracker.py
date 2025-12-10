"""
DEIA Ditto Tracker

Tracks duplicate issue occurrences without creating redundant BOK submissions.
When users hit same bug/issue, records "ditto" (+1) instead of full submission.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Literal
import json

StatusType = Literal["workaround_exists", "bug_reported", "fix_pending", "resolved"]


class DittoTracker:
    """Manages duplicate issue occurrence tracking"""

    def __init__(self, global_deia_path: Optional[Path] = None):
        """
        Initialize ditto tracker

        Args:
            global_deia_path: Path to global DEIA installation (defaults to ~/.deia-global/)
        """
        if global_deia_path:
            self.global_path = Path(global_deia_path)
        else:
            self.global_path = Path.home() / ".deia-global"

        self.tracker_dir = self.global_path / "ditto-tracker"
        self.tracker_dir.mkdir(parents=True, exist_ok=True)

    def record_occurrence(
        self,
        issue_id: str,
        bok_entry: str,
        user: str,
        project: str,
        resolved_by: str = "existing_workaround",
        metadata: Optional[dict] = None
    ) -> dict:
        """
        Record an occurrence of an existing issue

        Args:
            issue_id: Unique identifier for the issue (e.g., "railway-https-redirect")
            bok_entry: Path to BOK entry with workaround
            user: Username who encountered the issue
            project: Project where issue occurred
            resolved_by: How it was resolved (existing_workaround, new_solution, etc.)
            metadata: Additional context

        Returns:
            Updated occurrence data
        """
        tracker_file = self.tracker_dir / f"{issue_id}.json"

        # Load existing tracker or create new
        if tracker_file.exists():
            with open(tracker_file, 'r', encoding='utf-8') as f:
                tracker_data = json.load(f)
        else:
            tracker_data = {
                "issue_id": issue_id,
                "bok_entry": bok_entry,
                "occurrences": [],
                "total_count": 0,
                "first_reported": datetime.now().isoformat(),
                "status": "workaround_exists"
            }

        # Add new occurrence
        occurrence = {
            "user": user,
            "date": datetime.now().isoformat(),
            "project": project,
            "resolved_by": resolved_by
        }
        if metadata:
            occurrence["metadata"] = metadata

        tracker_data["occurrences"].append(occurrence)
        tracker_data["total_count"] += 1
        tracker_data["last_occurrence"] = datetime.now().isoformat()

        # Save updated tracker
        with open(tracker_file, 'w', encoding='utf-8') as f:
            json.dump(tracker_data, f, indent=2)

        return tracker_data

    def get_occurrence_count(self, issue_id: str) -> int:
        """
        Get total occurrence count for an issue

        Args:
            issue_id: Issue identifier

        Returns:
            Total number of occurrences
        """
        tracker_file = self.tracker_dir / f"{issue_id}.json"

        if not tracker_file.exists():
            return 0

        with open(tracker_file, 'r', encoding='utf-8') as f:
            tracker_data = json.load(f)

        return tracker_data.get("total_count", 0)

    def get_issue_stats(self, issue_id: str) -> Optional[dict]:
        """
        Get detailed statistics for an issue

        Args:
            issue_id: Issue identifier

        Returns:
            Issue statistics or None if not found
        """
        tracker_file = self.tracker_dir / f"{issue_id}.json"

        if not tracker_file.exists():
            return None

        with open(tracker_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def check_notification_threshold(self, issue_id: str) -> Optional[str]:
        """
        Check if occurrence count has reached a notification threshold

        Args:
            issue_id: Issue identifier

        Returns:
            Threshold type reached ("notify_community", "notify_partner", "critical") or None
        """
        count = self.get_occurrence_count(issue_id)

        # Define thresholds
        thresholds = {
            100: "critical_priority",
            50: "notify_partner",
            10: "notify_community"
        }

        for threshold, notification_type in sorted(thresholds.items(), reverse=True):
            if count >= threshold:
                # Check if we've already notified at this threshold
                if self._check_threshold_notified(issue_id, threshold):
                    continue
                return notification_type

        return None

    def mark_threshold_notified(self, issue_id: str, threshold: int) -> None:
        """
        Mark that notification has been sent for a threshold

        Args:
            issue_id: Issue identifier
            threshold: Threshold value that was notified
        """
        tracker_file = self.tracker_dir / f"{issue_id}.json"

        if not tracker_file.exists():
            return

        with open(tracker_file, 'r', encoding='utf-8') as f:
            tracker_data = json.load(f)

        if "notifications_sent" not in tracker_data:
            tracker_data["notifications_sent"] = []

        tracker_data["notifications_sent"].append({
            "threshold": threshold,
            "date": datetime.now().isoformat()
        })

        with open(tracker_file, 'w', encoding='utf-8') as f:
            json.dump(tracker_data, f, indent=2)

    def _check_threshold_notified(self, issue_id: str, threshold: int) -> bool:
        """
        Check if threshold notification already sent

        Args:
            issue_id: Issue identifier
            threshold: Threshold to check

        Returns:
            True if already notified, False otherwise
        """
        stats = self.get_issue_stats(issue_id)
        if not stats:
            return False

        notifications = stats.get("notifications_sent", [])
        return any(n["threshold"] == threshold for n in notifications)

    def update_status(self, issue_id: str, status: StatusType, note: Optional[str] = None) -> None:
        """
        Update issue status (e.g., when partner fixes the bug)

        Args:
            issue_id: Issue identifier
            status: New status
            note: Optional note about status change
        """
        tracker_file = self.tracker_dir / f"{issue_id}.json"

        if not tracker_file.exists():
            return

        with open(tracker_file, 'r', encoding='utf-8') as f:
            tracker_data = json.load(f)

        tracker_data["status"] = status
        tracker_data["status_updated"] = datetime.now().isoformat()
        if note:
            tracker_data["status_note"] = note

        with open(tracker_file, 'w', encoding='utf-8') as f:
            json.dump(tracker_data, f, indent=2)

    def list_high_impact_issues(self, min_occurrences: int = 10) -> list[dict]:
        """
        List issues with high occurrence counts

        Args:
            min_occurrences: Minimum occurrence count to include

        Returns:
            List of high-impact issues sorted by occurrence count
        """
        high_impact = []

        for tracker_file in self.tracker_dir.glob("*.json"):
            with open(tracker_file, 'r', encoding='utf-8') as f:
                tracker_data = json.load(f)

            if tracker_data.get("total_count", 0) >= min_occurrences:
                high_impact.append(tracker_data)

        # Sort by total count descending
        return sorted(high_impact, key=lambda x: x["total_count"], reverse=True)


def record_ditto(issue_id: str, bok_entry: str, user: str, project: str) -> int:
    """
    Quick helper to record a ditto occurrence

    Args:
        issue_id: Issue identifier
        bok_entry: BOK entry path
        user: Username
        project: Project name

    Returns:
        New total occurrence count
    """
    tracker = DittoTracker()
    result = tracker.record_occurrence(issue_id, bok_entry, user, project)
    return result["total_count"]


if __name__ == "__main__":
    # Example usage
    tracker = DittoTracker()

    # Record occurrence
    result = tracker.record_occurrence(
        issue_id="railway-https-redirect",
        bok_entry="bok/platforms/deployment/railway/https-redirect-middleware.md",
        user="dave",
        project="familybondbot"
    )
    print(f"Recorded occurrence #{result['total_count']}")

    # Check for threshold notifications
    notification = tracker.check_notification_threshold("railway-https-redirect")
    if notification:
        print(f"Threshold reached: {notification}")

    # Get stats
    stats = tracker.get_issue_stats("railway-https-redirect")
    print(f"Issue stats: {stats}")

    # List high-impact issues
    high_impact = tracker.list_high_impact_issues(min_occurrences=10)
    print(f"High-impact issues: {len(high_impact)}")
