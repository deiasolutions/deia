"""
Launch Multi-Agent Platform
Starts dashboard + Scrum Master bot + worker bot
"""

import subprocess
import time
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("LAUNCHING MULTI-AGENT PLATFORM")
    print("=" * 60)

    processes = []

    # 1. Launch Dashboard
    print("\n[1/3] Starting Dashboard (port 8000)...")
    dashboard = subprocess.Popen(
        [sys.executable, "run_dashboard.py"],
        cwd=Path.cwd()
    )
    processes.append(("Dashboard", dashboard))
    time.sleep(3)

    # 2. Launch Scrum Master Bot
    print("\n[2/3] Starting Scrum Master Bot 001 (SDK adapter)...")
    scrum_master = subprocess.Popen(
        [sys.executable, "run_single_bot.py",
         "deiasolutions-SCRUM-MASTER-001",
         "--adapter-type", "sdk"],
        cwd=Path.cwd()
    )
    processes.append(("Scrum Master 001", scrum_master))
    time.sleep(3)

    # 3. Launch Worker Bot
    print("\n[3/3] Starting Worker Bot 002 (SDK adapter)...")
    worker = subprocess.Popen(
        [sys.executable, "run_single_bot.py",
         "deiasolutions-CLAUDE-CODE-002",
         "--adapter-type", "sdk"],
        cwd=Path.cwd()
    )
    processes.append(("Worker Bot 002", worker))
    time.sleep(3)

    print("\n" + "=" * 60)
    print("PLATFORM READY")
    print("=" * 60)
    print("\nComponents running:")
    print("- Dashboard: http://localhost:8000")
    print("- Scrum Master Bot: deiasolutions-SCRUM-MASTER-001 (SDK adapter)")
    print("- Worker Bot: deiasolutions-CLAUDE-CODE-002 (SDK adapter)")
    print("\nScrum Master watches/directs/coordinates workers autonomously")
    print("Assign tasks to Scrum Master via dashboard or task files")
    print("\nPress Ctrl+C to shutdown all components...")

    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        for name, proc in processes:
            print(f"Stopping {name}...")
            proc.terminate()

        print("Platform shutdown complete.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
