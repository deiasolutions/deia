#!/usr/bin/env python3
"""
DEIA Bot Spawner

Launch multiple bot processes to work on hive tasks.

Usage:
    python run_bots.py --count 3
    python run_bots.py --bot-ids BOT-00001 BOT-00002
"""

import argparse
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from deia.adapters.bot_runner import BotRunner
from deia.adapters.claude_code_cli_adapter import ClaudeCodeCLIAdapter


def spawn_bot(bot_id: str, work_dir: Path, cooldown: int = 10):
    """
    Spawn a single bot process.

    Args:
        bot_id: Bot identifier (e.g., "BOT-00001")
        work_dir: Working directory
        cooldown: Seconds to wait between tasks (0 = no limit)

    Returns:
        subprocess.Popen: Bot process
    """
    print(f"[SPAWNER] Launching {bot_id}...")

    # Create bot runner
    task_dir = work_dir / ".deia" / "hive" / "tasks"
    response_dir = work_dir / ".deia" / "hive" / "responses"

    # Ensure directories exist
    task_dir.mkdir(parents=True, exist_ok=True)
    response_dir.mkdir(parents=True, exist_ok=True)

    # Create bot runner instance
    runner = BotRunner(
        bot_id=bot_id,
        work_dir=work_dir,
        task_dir=task_dir,
        response_dir=response_dir,
        adapter_type="cli",
        task_cooldown_seconds=cooldown
    )

    # Start bot runner in subprocess using the dedicated script
    # This avoids all the path escaping issues
    runner_script = work_dir / "run_single_bot.py"

    process = subprocess.Popen(
        [
            sys.executable,
            str(runner_script),
            bot_id,
            "--cooldown", str(cooldown),
            "--work-dir", str(work_dir)
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(work_dir)
    )

    print(f"[SPAWNER] {bot_id} launched (PID: {process.pid})")
    return process


def main():
    parser = argparse.ArgumentParser(description="DEIA Bot Spawner")
    parser.add_argument(
        "--count",
        type=int,
        help="Number of bots to spawn (BOT-00001, BOT-00002, ...)"
    )
    parser.add_argument(
        "--bot-ids",
        nargs="+",
        help="Specific bot IDs to spawn (e.g., BOT-00001 BOT-00002)"
    )
    parser.add_argument(
        "--cooldown",
        type=int,
        default=10,
        help="Seconds between tasks (default: 10, use 0 for no limit)"
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=Path.cwd(),
        help="Working directory (default: current directory)"
    )

    args = parser.parse_args()

    # Determine bot IDs to spawn
    if args.bot_ids:
        bot_ids = args.bot_ids
    elif args.count:
        bot_ids = [f"BOT-{i:05d}" for i in range(1, args.count + 1)]
    else:
        print("ERROR: Must specify --count or --bot-ids")
        return 1

    print("=" * 70)
    print("DEIA Bot Spawner")
    print("=" * 70)
    print(f"Work Dir: {args.work_dir}")
    print(f"Spawning: {len(bot_ids)} bots")
    print(f"Bot IDs: {', '.join(bot_ids)}")
    print(f"Cooldown: {args.cooldown}s between tasks")
    print("=" * 70)
    print()

    # Spawn bots
    processes = []
    for bot_id in bot_ids:
        try:
            process = spawn_bot(bot_id, args.work_dir, args.cooldown)
            processes.append((bot_id, process))
            time.sleep(0.5)  # Stagger launches
        except Exception as e:
            print(f"[SPAWNER] Failed to spawn {bot_id}: {e}")

    print()
    print(f"[SPAWNER] Spawned {len(processes)} bots")
    print("[SPAWNER] Press Ctrl+C to stop all bots")
    print()

    # Monitor processes
    try:
        while True:
            time.sleep(5)

            # Check if any processes died
            for bot_id, process in processes:
                if process.poll() is not None:
                    print(f"[SPAWNER] WARNING: {bot_id} exited (code: {process.returncode})")
                    # Read output
                    stdout, stderr = process.communicate(timeout=1)
                    if stderr:
                        print(f"[SPAWNER] {bot_id} stderr: {stderr.decode()[:200]}")

    except KeyboardInterrupt:
        print()
        print("[SPAWNER] Stopping all bots...")

        # Terminate all processes
        for bot_id, process in processes:
            if process.poll() is None:
                print(f"[SPAWNER] Stopping {bot_id}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"[SPAWNER] Force killing {bot_id}...")
                    process.kill()

        print("[SPAWNER] All bots stopped")

    return 0


if __name__ == "__main__":
    sys.exit(main())
