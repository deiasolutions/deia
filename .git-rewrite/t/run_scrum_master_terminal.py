"""
Run Scrum Master Terminal - Interactive Claude Code with WebSocket streaming.

Usage:
    python run_scrum_master_terminal.py --repo deiasolutions --port 8000

Launches:
- Claude Code as interactive subprocess
- HTTP/WebSocket service on specified port
- Terminal output streaming to /ws/terminal
- Command input via /send endpoint or WebSocket
"""

import argparse
from pathlib import Path
from src.deia.services.scrum_master_terminal import ScrumMasterTerminal


def main():
    parser = argparse.ArgumentParser(description="Run Scrum Master Terminal")
    parser.add_argument("--repo", required=True, help="Repository name (e.g., deiasolutions)")
    parser.add_argument("--port", type=int, default=8000, help="HTTP/WebSocket service port")
    parser.add_argument("--work-dir", help="Working directory (defaults to repo root)")
    parser.add_argument("--claude-path", default="claude", help="Path to claude CLI")

    args = parser.parse_args()

    # Construct bot ID
    bot_id = f"{args.repo}-SCRUM-MASTER-001"

    # Determine work directory
    if args.work_dir:
        work_dir = Path(args.work_dir)
    else:
        work_dir = Path.cwd()

    print(f"Starting Scrum Master Terminal:")
    print(f"  Bot ID: {bot_id}")
    print(f"  Work Dir: {work_dir}")
    print(f"  Port: {args.port}")
    print(f"  WebSocket: ws://localhost:{args.port}/ws/terminal")
    print(f"  Send Command: POST http://localhost:{args.port}/send")
    print()

    # Create and start terminal
    terminal = ScrumMasterTerminal(
        bot_id=bot_id,
        work_dir=work_dir,
        port=args.port,
        claude_cli_path=args.claude_path
    )

    # Start Claude Code subprocess
    terminal.start()

    # Run service (blocking)
    print(f"Starting HTTP/WebSocket service on port {args.port}...")
    terminal.run_service()


if __name__ == "__main__":
    main()
