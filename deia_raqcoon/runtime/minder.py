from __future__ import annotations

import time
from datetime import datetime
from typing import Optional

import requests


def run_minder(
    api_base: str = "http://127.0.0.1:8010",
    channel_id: str = "hive-all",
    interval_seconds: int = 600,
    author: str = "MINDER",
    message: Optional[str] = None,
) -> None:
    """Simple periodic ping to keep bees moving."""
    while True:
        content = message or f"Ping {datetime.now().strftime('%H:%M')} - status update requested."
        try:
            requests.post(
                f"{api_base}/api/messages",
                json={"channel_id": channel_id, "author": author, "content": content},
                timeout=5,
            )
        except Exception:
            pass
        time.sleep(interval_seconds)


if __name__ == "__main__":
    run_minder()
