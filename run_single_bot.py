#!/usr/bin/env python3
"""
Run a single bot instance with error handling and recovery.

Usage:
    python run_single_bot.py BOT-00001
    python run_single_bot.py BOT-00001 --cooldown 5
    python run_single_bot.py BOT-00001 --health-check-interval 30
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from deia.adapters.bot_runner import BotRunner
from deia.services.bot_health_monitor import BotHealthMonitor


def main():
    parser = argparse.ArgumentParser(description="Run a single DEIA bot with error handling")
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
    parser.add_argument(
        "--health-check-interval",
        type=int,
        default=30,
        help="Seconds between health checks (default: 30)"
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="cli-only",
        choices=["cli-only", "websocket-only", "hybrid"],
        help="Communication mode: cli-only (file queue), websocket-only (chat), hybrid (both) (default: cli-only)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="HTTP server port for WebSocket/API (optional, e.g., 8002)"
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
    print(f"[{args.bot_id}] Health check interval: {args.health_check_interval}s")
    if args.port:
        print(f"[{args.bot_id}] HTTP server port: {args.port}")

    # Initialize health monitor
    health_monitor = BotHealthMonitor(
        bot_id=args.bot_id,
        work_dir=work_dir,
        check_interval_seconds=args.health_check_interval
    )

    # Create and run bot
    runner = BotRunner(
        bot_id=args.bot_id,
        work_dir=work_dir,
        task_dir=task_dir,
        response_dir=response_dir,
        adapter_type=args.adapter_type,
        task_cooldown_seconds=args.cooldown,
        comm_mode=args.mode,
        port=args.port
    )

    # Start bot session
    print(f"[{args.bot_id}] Initializing adapter...")
    try:
        if not runner.start():
            print(f"[{args.bot_id}] [ERROR] Failed to start adapter - bot cannot process tasks")
            print(f"[{args.bot_id}] [ERROR] Check logs for details on adapter failure")
            health_monitor.log_error(
                f"Adapter startup failed - bot will not be able to process tasks",
                {"bot_id": args.bot_id, "adapter_type": args.adapter_type}
            )
            # Don't exit - allow bot to stay alive in registry for debugging
            print(f"[{args.bot_id}] [WARNING] Bot process continuing despite adapter failure for diagnostics")
    except Exception as e:
        print(f"[{args.bot_id}] [ERROR] Exception during bot startup: {str(e)}")
        health_monitor.log_error(
            f"Bot startup exception: {str(e)}",
            {"exception": type(e).__name__, "bot_id": args.bot_id}
        )
        # Don't exit - allow bot to stay alive in registry for debugging
        print(f"[{args.bot_id}] [WARNING] Bot process continuing despite exception for diagnostics")

    # Register process for health monitoring
    health_monitor.register_process(os.getpid(), datetime.now())

    try:
        runner.run_continuous()
    except KeyboardInterrupt:
        print(f"\n[{args.bot_id}] Stopping...")
        runner.stop()
    except Exception as e:
        print(f"\n[{args.bot_id}] [ERROR] Unexpected error: {str(e)}")
        health_monitor.log_error(
            f"Unexpected error in continuous run: {str(e)}",
            {"exception": type(e).__name__, "traceback": str(e)}
        )
        runner.stop()
        return 1
    finally:
        # Cleanup stale processes
        health_monitor.cleanup_stale_processes()

    return 0


if __name__ == "__main__":
    sys.exit(main())
