from __future__ import annotations

import os
import threading
import time
from datetime import datetime
from typing import Optional

import requests

# Thread management globals
_minder_thread: Optional[threading.Thread] = None
_minder_stop_event = threading.Event()


def _run_minder_loop(
    api_base: str,
    channel_id: str,
    interval_seconds: int,
    author: str,
    message: Optional[str],
) -> None:
    """Internal minder loop that respects stop event."""
    while not _minder_stop_event.is_set():
        content = message or f"Ping {datetime.now().strftime('%H:%M')} - status update requested."
        try:
            requests.post(
                f"{api_base}/api/messages",
                json={"channel_id": channel_id, "author": author, "content": content},
                timeout=5,
            )
        except Exception:
            pass  # Minder pings are best-effort
        # Use wait() instead of sleep() so we can be interrupted
        _minder_stop_event.wait(interval_seconds)


def start_minder_thread(
    api_base: str = "http://127.0.0.1:8010",
    channel_id: str = "hive-all",
    interval_seconds: Optional[int] = None,
    author: str = "MINDER",
    message: Optional[str] = None,
) -> bool:
    """Start minder as background thread. Returns True if started, False if already running."""
    global _minder_thread
    if _minder_thread is not None and _minder_thread.is_alive():
        return False  # Already running

    # Allow env var override for interval
    if interval_seconds is None:
        interval_seconds = int(os.getenv("DEIA_MINDER_INTERVAL", "600"))

    _minder_stop_event.clear()
    _minder_thread = threading.Thread(
        target=_run_minder_loop,
        args=(api_base, channel_id, interval_seconds, author, message),
        daemon=True,
        name="deia-minder",
    )
    _minder_thread.start()
    return True


def stop_minder_thread() -> bool:
    """Stop minder thread gracefully. Returns True if stopped, False if wasn't running."""
    global _minder_thread
    if _minder_thread is None or not _minder_thread.is_alive():
        return False
    _minder_stop_event.set()
    _minder_thread.join(timeout=5)
    _minder_thread = None
    return True


def is_minder_running() -> bool:
    """Check if minder thread is currently running."""
    return _minder_thread is not None and _minder_thread.is_alive()


# Keep backward compatibility for standalone execution
def run_minder(
    api_base: str = "http://127.0.0.1:8010",
    channel_id: str = "hive-all",
    interval_seconds: int = 600,
    author: str = "MINDER",
    message: Optional[str] = None,
) -> None:
    """Original blocking minder for standalone use."""
    _run_minder_loop(api_base, channel_id, interval_seconds, author, message)


if __name__ == "__main__":
    run_minder()
