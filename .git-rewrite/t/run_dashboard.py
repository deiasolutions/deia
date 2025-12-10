#!/usr/bin/env python3
"""
Run DEIA Hive Monitoring Dashboard

Starts FastAPI server with WebSocket support for real-time bot monitoring.

Usage:
    python run_dashboard.py
    python run_dashboard.py --port 8080
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    parser = argparse.ArgumentParser(description="DEIA Hive Monitoring Dashboard")
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run server on (default: 8000)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )

    args = parser.parse_args()

    print("=" * 70)
    print("DEIA Hive Monitoring Dashboard")
    print("=" * 70)
    print(f"Work Dir: {Path.cwd()}")
    print(f"Hive Dir: {Path.cwd() / '.deia' / 'hive'}")
    print()
    print("Starting server...")
    print(f"Dashboard: http://localhost:{args.port}")
    print(f"API Docs: http://localhost:{args.port}/docs")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 70)
    print()

    # Check dependencies
    try:
        import fastapi
        import uvicorn
        import watchdog
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print()
        print("Install dependencies:")
        print("  pip install -r src/deia/dashboard/requirements.txt")
        return 1

    # Import and run
    try:
        import uvicorn
        uvicorn.run(
            "deia.dashboard.server:app",
            host=args.host,
            port=args.port,
            log_level="info",
            reload=True  # Auto-reload on code changes
        )
    except KeyboardInterrupt:
        print("\n\nStopping dashboard...")
        print("[PASS] Dashboard stopped")

    return 0


if __name__ == "__main__":
    sys.exit(main())
