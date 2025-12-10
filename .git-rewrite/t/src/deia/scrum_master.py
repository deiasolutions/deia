"""
DEIA ScrumMaster Bot

Monitors worker bots, enforces process compliance, detects violations.
Uses Claude API to understand bot responses and ensure protocol compliance.

Violations:
- Minor (one-line log): sitting idle, not checking in, missed heartbeat
- Major (full RCA): hallucination, stealing work, lying, scope violation

Bot writes their own mea culpa when violations detected.
"""

from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime, timedelta
import json
import time
import os
import yaml
import signal


class ScrumMaster:
    """
    ScrumMaster bot that enforces process compliance.

    Detects violations like:
    - Sitting idle without reporting
    - Not checking in on schedule
    - Stealing work from other bots
    - Hallucinations/lying
    - Scope violations
    """

    # Major violations require full RCA
    MAJOR_VIOLATIONS = [
        "stealing work",
        "hallucination",
        "lying",
        "scope violation",
        "unauthorized",
        "out of scope"
    ]

    def __init__(
        self,
        work_dir: Path,
        queen_id: str = "CLAUDE-CODE-001",
        scrum_id: str = "SCRUM-MASTER-001",
        api_key: Optional[str] = None
    ):
        """Initialize ScrumMaster."""
        self.work_dir = Path(work_dir)
        self.queen_id = queen_id
        self.scrum_id = scrum_id

        # Paths
        self.heartbeat_dir = self.work_dir / ".deia" / "hive" / "heartbeats"
        self.response_dir = self.work_dir / ".deia" / "hive" / "responses"
        self.task_dir = self.work_dir / ".deia" / "hive" / "tasks"
        self.status_board = self.work_dir / ".deia" / "bot-status-board.json"
        self.checkin_protocol = self.work_dir / ".deia" / "instructions" / "CHECKIN.md"
        self.observations_dir = self.work_dir / ".deia" / "observations"
        self.violations_log = self.work_dir / ".deia" / "analytics" / "staging" / "events" / f"dt={datetime.now().strftime('%Y-%m-%d')}"

        # Ensure directories exist
        self.heartbeat_dir.mkdir(parents=True, exist_ok=True)
        self.response_dir.mkdir(parents=True, exist_ok=True)
        self.task_dir.mkdir(parents=True, exist_ok=True)
        self.observations_dir.mkdir(parents=True, exist_ok=True)
        self.violations_log.mkdir(parents=True, exist_ok=True)

        # Initialize Claude API
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY not set")

        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("pip install anthropic")

        # Load playbook
        self.playbook = self._load_playbook()

        # Tracking
        self.last_poke: Dict[str, datetime] = {}
        self.violation_counts: Dict[str, Dict[str, int]] = {}  # bot_id -> {violation_type -> count}
        self.out_of_order_bots: set = set()  # Bots marked as out of order

    def _load_playbook(self) -> str:
        """Load CHECKIN.md protocol."""
        if self.checkin_protocol.exists():
            return self.checkin_protocol.read_text(encoding="utf-8")
        return "CHECKIN.md not found"

    def monitor_cycle(self) -> Dict:
        """Run one monitoring cycle."""
        self._log("Starting monitoring cycle")

        status_board = self._read_status_board()
        if not status_board:
            return {"error": "No status board"}

        bots = status_board.get("bots", {})

        results = {
            "bots_checked": 0,
            "compliant": [],
            "violations": {},
            "pokes_sent": 0,
            "reports_sent": 0
        }

        for bot_id, bot_info in bots.items():
            if bot_id == self.queen_id:
                continue

            # Skip bots marked as out of order
            if bot_id in self.out_of_order_bots:
                self._log(f"Skipping {bot_id}: OUT OF ORDER")
                continue

            self._log(f"Checking: {bot_id}")
            results["bots_checked"] += 1

            bot_data = self._gather_bot_data(bot_id, bot_info)
            compliance = self._check_compliance(bot_id, bot_data)

            if compliance["compliant"]:
                results["compliant"].append(bot_id)
                self._log(f"  [PASS] {bot_id}")
                # Reset violation counts on compliance
                if bot_id in self.violation_counts:
                    self.violation_counts[bot_id] = {}
            else:
                violations = compliance["violations"]
                results["violations"][bot_id] = violations
                self._log(f"  [FAIL] {bot_id}: {len(violations)} violation(s)")

                # Track repeat violations
                repeat_violations = self._track_violations(bot_id, violations)

                # Record violation
                self._record_violation(bot_id, violations, bot_data)

                # Check for repeat violations - mark out of order on 2nd occurrence
                if repeat_violations:
                    self._mark_out_of_order(bot_id, repeat_violations)
                    self._alert_queen(bot_id, violations, out_of_order=True)
                    results["reports_sent"] += 1
                    continue

                # Poke bot
                if self._should_poke(bot_id):
                    self._poke_bot(bot_id, violations)
                    results["pokes_sent"] += 1

                # Alert Queen for major violations
                if self._is_major_violation(violations):
                    self._alert_queen(bot_id, violations)
                    results["reports_sent"] += 1

        self._log(f"Cycle complete: {results['pokes_sent']} pokes, {results['reports_sent']} alerts")
        return results

    def _gather_bot_data(self, bot_id: str, bot_info: Dict) -> Dict:
        """Gather bot data for analysis."""
        data = {
            "bot_id": bot_id,
            "status_board_entry": bot_info,
            "last_heartbeat": None,
            "time_since_heartbeat_min": None,
            "recent_responses": [],
            "platform": bot_info.get("platform", "unknown"),
            "role": bot_info.get("role", "unknown")
        }

        # Get heartbeat
        hb_file = self.heartbeat_dir / f"{bot_id}-heartbeat.yaml"
        if hb_file.exists():
            try:
                hb = yaml.safe_load(hb_file.read_text())
                data["last_heartbeat"] = hb
                if "timestamp" in hb:
                    hb_time = datetime.fromisoformat(hb["timestamp"])
                    data["time_since_heartbeat_min"] = (datetime.now() - hb_time).total_seconds() / 60
            except:
                pass

        # Get recent responses
        responses = sorted(
            self.response_dir.glob(f"*-{bot_id}-*"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:3]

        for resp in responses:
            data["recent_responses"].append({
                "file": resp.name,
                "content": resp.read_text(encoding="utf-8")[:300]
            })

        return data

    def _check_compliance(self, bot_id: str, bot_data: Dict) -> Dict:
        """Use Claude API to check compliance."""
        prompt = f"""You are a ScrumMaster monitoring DEIA bots.

**CHECKIN.md Protocol:**
{self.playbook}

**Bot State:**
```json
{json.dumps(bot_data, indent=2, default=str)}
```

**Check for violations:**
1. Sitting idle without reporting "I am idle" or "Waiting for orders"
2. Not checking status board (time_since_heartbeat > 5 minutes)
3. Stealing work (working on task not assigned to them)
4. Scope violation (working outside allowed_dirs)
5. Lying or hallucinating (claiming work done that wasn't)
6. Not following 8-step check-in process

**Respond in JSON:**
{{
  "compliant": true/false,
  "violations": ["short description", ...],
  "severity": "minor" or "major"
}}

Minor: idle, missed check-in, late heartbeat
Major: stealing work, lying, scope violation, hallucination
"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text

            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                return {"compliant": True, "violations": [], "severity": "minor"}

        except Exception as e:
            self._log(f"LLM check failed: {e}")
            return {"compliant": True, "violations": [], "severity": "minor"}

    def _record_violation(self, bot_id: str, violations: List[str], bot_data: Dict) -> None:
        """Record violation to analytics."""
        violation_log = self.violations_log / f"violations-{bot_id}.ndjson"

        for v in violations:
            record = {
                "timestamp": datetime.now().isoformat(),
                "bot_id": bot_id,
                "violation": v,
                "platform": bot_data.get("platform", "unknown"),
                "role": bot_data.get("role", "unknown"),
                "severity": "major" if self._is_major_violation([v]) else "minor"
            }

            with violation_log.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")

    def _should_poke(self, bot_id: str) -> bool:
        """Check if should poke bot (rate limit: 5 min)."""
        if bot_id in self.last_poke:
            elapsed = (datetime.now() - self.last_poke[bot_id]).total_seconds()
            return elapsed > 300
        return True

    def _is_major_violation(self, violations: List[str]) -> bool:
        """Check if any violation is major."""
        for v in violations:
            if any(keyword in v.lower() for keyword in self.MAJOR_VIOLATIONS):
                return True
        return False

    def _poke_bot(self, bot_id: str, violations: List[str]) -> None:
        """Send violation notice to bot. Bot writes its own mea culpa."""
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        is_major = self._is_major_violation(violations)

        violations_text = "\n".join(f"- {v}" for v in violations)

        if is_major:
            # Major: Bot must write full RCA
            content = f"""# VIOLATION: Write RCA

**To:** {bot_id}
**From:** {self.scrum_id}
**Priority:** P0

## Major Violation Detected

{violations_text}

## Required Action

Write RCA to: `.deia/observations/{datetime.now().strftime('%Y-%m-%d')}-{bot_id}-{{type}}.md`

**Format:**
```markdown
# RCA: {{Title}}

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Reporter:** {bot_id}
**Severity:** High
**Bot Demographics:** {{platform}}, {{model}}, {{role}}

## What Happened
{{1-2 sentences}}

## Root Cause
{{Why?}}

## Prevention
{{How to prevent?}}

## Telemetry
- Task ID: {{if applicable}}
- Duration: {{if applicable}}
- Cost: {{if applicable}}
```

Then return to CHECKIN.md protocol.
"""
        else:
            # Minor: Simple log + correction
            content = f"""# VIOLATION: Log & Correct

**To:** {bot_id}
**From:** {self.scrum_id}
**Priority:** P1

## Violation

{violations[0]}

## Action

1. Violation already logged to analytics
2. Correction: {self._get_correction(violations[0])}
3. Resume CHECKIN.md protocol
"""

        filename = f"{timestamp}-{self.scrum_id}-{bot_id}-VIOLATION.md"
        (self.task_dir / filename).write_text(content, encoding="utf-8")

        self.last_poke[bot_id] = datetime.now()

    def _get_correction(self, violation: str) -> str:
        """Get correction action for violation."""
        if "idle" in violation.lower():
            return "Report 'I am idle, waiting for orders' in response file"
        elif "check" in violation.lower():
            return "Read .deia/bot-status-board.json now, then every 3-5 min"
        elif "heartbeat" in violation.lower():
            return "Send heartbeat immediately"
        else:
            return "Follow CHECKIN.md step-by-step"

    def _track_violations(self, bot_id: str, violations: List[str]) -> List[str]:
        """
        Track violations per bot and detect repeats.

        Returns:
            List of violations that are repeats (occurred 2+ times)
        """
        if bot_id not in self.violation_counts:
            self.violation_counts[bot_id] = {}

        repeat_violations = []

        for v in violations:
            # Increment count
            self.violation_counts[bot_id][v] = self.violation_counts[bot_id].get(v, 0) + 1

            # Check if this is a repeat (2nd occurrence)
            if self.violation_counts[bot_id][v] >= 2:
                repeat_violations.append(v)

        return repeat_violations

    def _mark_out_of_order(self, bot_id: str, repeat_violations: List[str]) -> None:
        """
        Mark bot as out of order and create PAUSE file.

        Args:
            bot_id: Bot to mark
            repeat_violations: List of repeated violations
        """
        self.out_of_order_bots.add(bot_id)

        # Create PAUSE file to stop bot
        pause_file = self.work_dir / ".deia" / "hive" / "controls" / f"{bot_id}-PAUSE"
        pause_file.parent.mkdir(parents=True, exist_ok=True)

        pause_content = f"""# BOT OUT OF ORDER

**Bot:** {bot_id}
**Time:** {datetime.now().isoformat()}
**Reason:** Repeat violations

## Repeat Violations

{chr(10).join(f"- {v}" for v in repeat_violations)}

Bot has been PAUSED and marked OUT OF ORDER.
No new tasks will be assigned until Queen intervenes.

To resume: Delete this file and notify ScrumMaster.
"""

        pause_file.write_text(pause_content, encoding="utf-8")
        self._log(f"[OUT OF ORDER] {bot_id} - PAUSED due to repeat violations")

    def _alert_queen(self, bot_id: str, violations: List[str], out_of_order: bool = False) -> None:
        """Alert Queen of major violation or out-of-order bot."""
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")

        if out_of_order:
            content = f"""# ALERT: Bot Out of Order

**From:** {self.scrum_id}
**To:** {self.queen_id}
**Bot:** {bot_id}
**Priority:** P0

## Status

Bot {bot_id} marked OUT OF ORDER due to repeat violations.

## Violations

{chr(10).join(f"- {v}" for v in violations)}

## Action Taken

- Bot PAUSED (no new tasks)
- Added to out-of-order list
- Pause file: `.deia/hive/controls/{bot_id}-PAUSE`

## Recommendation

Bot {bot_id} requires immediate attention. Review violation logs and restart or reassign tasks.

---
Generated by {self.scrum_id}
"""
        else:
            content = f"""# ALERT: Major Violation

**From:** {self.scrum_id}
**To:** {self.queen_id}
**Bot:** {bot_id}
**Priority:** P0

## Violations

{chr(10).join(f"- {v}" for v in violations)}

## Recommendation

Bot {bot_id} requires attention. May need restart or intervention.

---
Generated by {self.scrum_id}
"""

        filename = f"{timestamp}-{self.scrum_id}-{self.queen_id}-ALERT-{bot_id}.md"
        (self.response_dir / filename).write_text(content, encoding="utf-8")

    def _read_status_board(self) -> Optional[Dict]:
        """Read status board."""
        if self.status_board.exists():
            try:
                return json.loads(self.status_board.read_text(encoding="utf-8"))
            except:
                return None
        return None

    def run_continuous(self, interval_seconds: int = 180) -> None:
        """Run continuous monitoring."""
        self._log(f"Starting continuous monitoring (interval: {interval_seconds}s)")

        try:
            while True:
                self.monitor_cycle()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            self._log("Stopping")

    def _log(self, message: str) -> None:
        """Log message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [ScrumMaster] {message}")
