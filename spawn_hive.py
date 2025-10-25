#!/usr/bin/env python3
"""
Spawn DEIA Hive Bots

Quick script to spawn worker bots 002, 003, 004, etc.
Run this from Bot 001 (Queen) session.

Usage:
    python spawn_hive.py --bots 002,003,004
    python spawn_hive.py --config hive_config.json
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from deia.hive_spawner import HiveSpawner


def main():
    parser = argparse.ArgumentParser(description="Spawn DEIA Hive Worker Bots")
    parser.add_argument(
        "--bots",
        type=str,
        help="Comma-separated bot numbers (e.g., '002,003,004')"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to hive configuration JSON"
    )
    parser.add_argument(
        "--queen-id",
        type=str,
        default="CLAUDE-CODE-001",
        help="Queen bot ID (default: CLAUDE-CODE-001)"
    )

    args = parser.parse_args()

    # Initialize spawner
    spawner = HiveSpawner(
        work_dir=Path.cwd(),
        queen_id=args.queen_id
    )

    print(f"DEIA Hive Spawner")
    print(f"Queen: {args.queen_id}")
    print(f"Work Dir: {Path.cwd()}")
    print(f"Task Queue: {spawner.task_dir}")
    print(f"Response Dir: {spawner.response_dir}")
    print("-" * 60)

    # Determine bots to spawn
    if args.config:
        # Load from config file
        import json
        config = json.loads(args.config.read_text())
        bot_specs = config.get("bots", [])

    elif args.bots:
        # Parse from command line
        bot_numbers = args.bots.split(',')
        bot_specs = [
            {
                "bot_id": f"CLAUDE-CODE-{num.strip().zfill(3)}",
                "role": "Worker"
            }
            for num in bot_numbers
        ]

    else:
        # Default: spawn 002, 003, 004
        bot_specs = [
            {"bot_id": "CLAUDE-CODE-002", "role": "Drone-Dev"},
            {"bot_id": "CLAUDE-CODE-003", "role": "Drone-Testing"},
            {"bot_id": "CLAUDE-CODE-004", "role": "Worker"}
        ]

    print(f"\nSpawning {len(bot_specs)} bots...")
    print()

    # Spawn bots
    results = spawner.spawn_multiple(bot_specs)

    # Report results
    print("\nSpawn Results:")
    print("-" * 60)
    for bot_id, success in results.items():
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {bot_id}")

    print()

    # Show statuses
    print("Bot Statuses:")
    print("-" * 60)
    for bot_id, status in spawner.get_all_statuses().items():
        print(f"{bot_id}:")
        print(f"  Role: {status.get('role')}")
        print(f"  Status: {status.get('status')}")
        print(f"  Session: {status['session_info'].get('status')}")
        print(f"  Tasks Completed: {status['session_info'].get('tasks_completed', 0)}")
        print()

    print("Hive is running. Bots monitoring task queue.")
    print("Press Ctrl+C to stop all bots.")

    # Keep running
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping all bots...")
        spawner.stop_all()
        print("Hive stopped.")


if __name__ == "__main__":
    main()
