#!/usr/bin/env python3
"""
Example: Autonomous Bot Runner with CLI Adapter

Demonstrates how to run a persistent bot that:
1. Monitors task queue directory
2. Executes tasks via Claude Code CLI
3. Writes responses back to coordinator
4. Runs continuously without human intervention
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from deia.adapters.bot_runner import BotRunner


def main():
    """Run autonomous bot with CLI adapter."""

    # Configuration
    bot_id = "CLAUDE-CODE-001"
    work_dir = Path.cwd()  # Bot's working directory
    task_dir = Path(".deia/hive/tasks")  # Where tasks are assigned
    response_dir = Path(".deia/tunnel/claude-to-claude")  # Where responses go

    # Ensure directories exist
    task_dir.mkdir(parents=True, exist_ok=True)
    response_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting autonomous bot: {bot_id}")
    print(f"Work directory: {work_dir}")
    print(f"Task queue: {task_dir}")
    print(f"Response directory: {response_dir}")
    print()

    # Initialize bot runner with CLI adapter
    runner = BotRunner(
        bot_id=bot_id,
        work_dir=work_dir,
        task_dir=task_dir,
        response_dir=response_dir,
        adapter_type="cli",  # Use CLI subprocess (vs "api" for Messages API)
        platform_config={
            "claude_cli_path": "claude",  # Assumes 'claude' in PATH
            "timeout_seconds": 300  # 5 minute task timeout
        }
    )

    # Start the runner
    print("Starting Claude Code session...")
    runner.start()
    print("[PASS] Session started")
    print()

    # Show status
    status = runner.get_status()
    print("Bot Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    print()

    # Run continuous monitoring loop
    print("Entering continuous monitoring mode...")
    print("Press Ctrl+C to stop")
    print("-" * 60)

    def on_iteration(iteration_num, result):
        """Callback after each task check."""
        if result["task_found"]:
            status = "[PASS]" if result["success"] else "[FAIL]"
            task_id = result["task_id"]
            duration = result.get("duration", 0)
            print(f"{status} Task {task_id} - {duration}s")
        else:
            # Only log every 10th iteration when idle
            if iteration_num % 10 == 0:
                print(f"[INFO] Iteration {iteration_num} - No tasks in queue")

    try:
        runner.run_continuous(
            poll_interval=5,  # Check every 5 seconds
            max_iterations=None,  # Run forever
            on_iteration=on_iteration
        )
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        runner.stop()
        print("[PASS] Bot stopped")


def test_single_task():
    """Test runner with a single mock task."""

    bot_id = "CLAUDE-CODE-TEST"
    work_dir = Path.cwd()
    task_dir = Path(".deia/hive/tasks/test")
    response_dir = Path(".deia/tunnel/test")

    # Setup
    task_dir.mkdir(parents=True, exist_ok=True)
    response_dir.mkdir(parents=True, exist_ok=True)

    # Create test task
    task_file = task_dir / "2025-10-23-2300-BEE001-CLAUDE-CODE-TEST-TASK-example.md"
    task_file.write_text("""# Test Task

**To:** CLAUDE-CODE-TEST
**From:** BEE-001
**Priority:** P1

## Task

Create a simple Python script that prints "Hello from autonomous bot runner!"

File should be named: test_output.py
""")

    print("Created test task:", task_file.name)

    # Initialize and run
    runner = BotRunner(
        bot_id=bot_id,
        work_dir=work_dir,
        task_dir=task_dir,
        response_dir=response_dir,
        adapter_type="cli"
    )

    runner.start()
    print("[PASS] Runner started")

    # Execute one task
    result = runner.run_once()

    print(f"\nTask execution result:")
    print(f"  Found: {result['task_found']}")
    print(f"  Executed: {result['task_executed']}")
    print(f"  Success: {result['success']}")
    print(f"  Task ID: {result['task_id']}")
    print(f"  Duration: {result.get('duration')}s")

    # Check response file
    response_files = list(response_dir.glob("*.md"))
    if response_files:
        print(f"\nResponse written to: {response_files[0].name}")
        print(response_files[0].read_text()[:500])

    runner.stop()
    print("\n[PASS] Test complete")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Autonomous Bot Runner Example")
    parser.add_argument("--test", action="store_true", help="Run single task test")

    args = parser.parse_args()

    if args.test:
        test_single_task()
    else:
        main()
