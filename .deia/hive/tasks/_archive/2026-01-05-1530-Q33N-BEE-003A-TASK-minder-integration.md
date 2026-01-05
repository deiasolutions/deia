# Task Assignment: TASK-005 - Integrate Minder with Server Startup

**Task ID:** TASK-005
**Assigned to:** BEE-003A
**Assigned by:** Q33N
**Priority:** P1 - High
**Sprint:** SPRINT-001 (Integration Wiring)
**Status:** QUEUED - Start after TASK-004 completes
**Depends On:** TASK-004 (WebSocket broadcast used by minder messages)

---

## Task

Integrate the minder (periodic ping system) with server startup so it runs automatically as a background thread. Currently minder must be run as a separate process. It should start when the server starts and stop cleanly on shutdown.

---

## Current State

```python
# minder.py - standalone script, must be run separately
def run_minder(
    api_base: str = "http://127.0.0.1:8010",
    channel_id: str = "hive-all",
    interval_seconds: int = 600,
    ...
) -> None:
    while True:
        # Posts message every interval
        requests.post(f"{api_base}/api/messages", ...)
        time.sleep(interval_seconds)

if __name__ == "__main__":
    run_minder()
```

---

## Required Changes

### 1. Modify minder.py for thread-safe operation

Update `deia_raqcoon/runtime/minder.py`:

```python
from __future__ import annotations

import os
import threading
import time
from datetime import datetime
from typing import Optional

import requests

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
```

### 2. Add startup/shutdown hooks in server.py

Add import near top of server.py:
```python
from deia_raqcoon.runtime.minder import start_minder_thread, stop_minder_thread
```

Add lifecycle hooks (after the app initialization, around line 28):
```python
@app.on_event("startup")
async def startup_event():
    start_minder_thread()


@app.on_event("shutdown")
async def shutdown_event():
    stop_minder_thread()
```

---

## Files to Modify

| File | Action |
|------|--------|
| `deia_raqcoon/runtime/minder.py` | Refactor for thread-safe start/stop |
| `deia_raqcoon/runtime/server.py` | Add import and lifecycle hooks |

---

## Success Criteria

- [ ] `start_minder_thread()` and `stop_minder_thread()` functions added to minder.py
- [ ] Minder starts automatically when server starts (via `@app.on_event("startup")`)
- [ ] Minder stops cleanly on server shutdown (via `@app.on_event("shutdown")`)
- [ ] Interval configurable via `DEIA_MINDER_INTERVAL` environment variable
- [ ] Minder pings visible in `/api/messages` with `author="MINDER"`
- [ ] No orphan threads on server restart
- [ ] Backward compatibility: `python -m deia_raqcoon.runtime.minder` still works

---

## Test Commands

```bash
# Test 1: Start server and verify minder runs
# Set short interval for testing
export DEIA_MINDER_INTERVAL=10
python -m deia_raqcoon.runtime.run_server &
SERVER_PID=$!

# Wait for minder ping
sleep 15

# Check for minder messages
curl http://127.0.0.1:8010/api/messages | grep -i minder
# Expected: Message with author="MINDER"

# Test 2: Verify clean shutdown
kill $SERVER_PID
# No orphan threads should remain

# Test 3: Backward compatibility
python -m deia_raqcoon.runtime.minder &
# Should still work as standalone (Ctrl+C to stop)
```

---

## Rules

1. Only modify the files listed above
2. Preserve backward compatibility for standalone minder execution
3. Use daemon thread so it doesn't block server shutdown
4. Handle all exceptions gracefully (minder should never crash the server)
5. Use proper thread synchronization (Event for stop signal)

---

## Deliverable

**On Completion:**
1. Create response file: `.deia/hive/responses/2026-01-05-BEE-003A-Q33N-RESPONSE-minder-integration.md`
2. Include:
   - Summary of changes made
   - Exact lines modified in both files
   - Test output showing minder messages
   - Any issues encountered
3. Archive this task file to `.deia/hive/tasks/_archive/`

---

## Working Directory

```
working_dir: C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions
allowed_paths:
  - deia_raqcoon/
  - .deia/hive/
```

---

*Q33N Assignment - SPRINT-001*
