#!/usr/bin/env python3
"""
Run a single bot instance.

Usage:
    python run_single_bot.py BOT-00001
    python run_single_bot.py BOT-00001 --cooldown 5
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from deia.adapters.bot_runner import BotRunner


def main():
    parser = argparse.ArgumentParser(description="Run a single DEIA bot")
    parser.add_argument("bot_id", help="Bot ID (e.g., BOT-00001)")
    parser.add_argument(
        "--cooldown",
        type=int,
        default=10,
        help="Seconds between tasks (default: 10)"
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=Path.cwd(),
        help="Working directory"
    )
    parser.add_argument(
        "--adapter-type",
        type=str,
        default="sdk",
        choices=["api", "cli", "sdk", "mock"],
        help="Bot adapter type (default: sdk)"
    )

    args = parser.parse_args()

    # Setup paths
    work_dir = args.work_dir
    task_dir = work_dir / ".deia" / "hive" / "tasks" / args.bot_id
    response_dir = work_dir / ".deia" / "hive" / "responses"

    # Ensure directories exist
    task_dir.mkdir(parents=True, exist_ok=True)
    response_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{args.bot_id}] Starting bot...")
    print(f"[{args.bot_id}] Work dir: {work_dir}")
    print(f"[{args.bot_id}] Task dir: {task_dir}")
    print(f"[{args.bot_id}] Adapter: {args.adapter_type}")
    print(f"[{args.bot_id}] Cooldown: {args.cooldown}s")

    # Create and run bot
    runner = BotRunner(
        bot_id=args.bot_id,
        work_dir=work_dir,
        task_dir=task_dir,
        response_dir=response_dir,
        adapter_type=args.adapter_type,
        task_cooldown_seconds=args.cooldown
    )

    # Start bot session
    print(f"[{args.bot_id}] Initializing adapter...")
    if not runner.start():
        print(f"[{args.bot_id}] [ERROR] Failed to start adapter")
        return 1

    try:
        runner.run_continuous()
    except KeyboardInterrupt:
        print(f"\n[{args.bot_id}] Stopping...")
        runner.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
