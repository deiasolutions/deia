#!/usr/bin/env python3
"""
Run DEIA ScrumMaster Bot

Monitors worker bots and enforces process compliance.

Usage:
    python run_scrum_master.py
    python run_scrum_master.py --interval 300  # Check every 5 minutes
    python run_scrum_master.py --once          # Run once and exit
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from deia.scrum_master import ScrumMaster


def main():
    parser = argparse.ArgumentParser(description="DEIA ScrumMaster Bot")
    parser.add_argument(
        "--interval",
        type=int,
        default=180,
        help="Seconds between checks (default: 180 = 3 minutes)"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once and exit (don't loop)"
    )
    parser.add_argument(
        "--queen-id",
        type=str,
        default="CLAUDE-CODE-001",
        help="Queen bot ID to report to (default: CLAUDE-CODE-001)"
    )

    args = parser.parse_args()

    print("=" * 70)
    print("DEIA ScrumMaster Bot")
    print("=" * 70)
    print(f"Work Dir: {Path.cwd()}")
    print(f"Queen ID: {args.queen_id}")
    print(f"Check Interval: {args.interval}s")
    print(f"Mode: {'One-time' if args.once else 'Continuous'}")
    print("=" * 70)
    print()

    # Initialize ScrumMaster
    try:
        scrum = ScrumMaster(
            work_dir=Path.cwd(),
            queen_id=args.queen_id
        )
    except Exception as e:
        print(f"Failed to initialize ScrumMaster: {e}")
        return 1

    # Run
    if args.once:
        # Single check
        results = scrum.monitor_cycle()

        print()
        print("=" * 70)
        print("Monitor Cycle Results:")
        print("=" * 70)
        print(f"Bots Checked: {results.get('bots_checked', 0)}")
        print(f"Compliant: {len(results.get('compliant', []))}")
        print(f"Violations: {len(results.get('violations', {}))}")
        print(f"Pokes Sent: {results.get('pokes_sent', 0)}")
        print(f"Reports Sent: {results.get('reports_sent', 0)}")

        if results.get('violations'):
            print()
            print("Violations Detected:")
            for bot_id, violations in results['violations'].items():
                print(f"  {bot_id}:")
                for v in violations:
                    print(f"    - {v}")

        print()
        print("[PASS] Monitor cycle complete")

    else:
        # Continuous monitoring
        print("Starting continuous monitoring...")
        print("Press Ctrl+C to stop")
        print()

        try:
            scrum.run_continuous(interval_seconds=args.interval)
        except KeyboardInterrupt:
            print("\n\nStopping ScrumMaster...")
            print("[PASS] ScrumMaster stopped")

    return 0


if __name__ == "__main__":
    sys.exit(main())
