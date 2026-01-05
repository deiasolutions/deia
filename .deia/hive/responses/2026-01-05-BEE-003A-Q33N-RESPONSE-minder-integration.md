# Response: TASK-005 - Minder Integration

**Task ID:** TASK-005
**Completed by:** BEE-003A
**Date:** 2026-01-05
**Status:** COMPLETE

---

## Summary of Changes

Integrated the minder (periodic ping system) with server startup so it runs automatically as a background thread. The minder now starts when the server starts and stops cleanly on shutdown.

---

## Changes Made

### 1. Refactored `deia_raqcoon/runtime/minder.py`

**Added thread management globals (lines 11-13):**
```python
_minder_thread: Optional[threading.Thread] = None
_minder_stop_event = threading.Event()
```

**Added internal loop function (lines 16-35):**
```python
def _run_minder_loop(api_base, channel_id, interval_seconds, author, message):
    """Internal minder loop that respects stop event."""
    while not _minder_stop_event.is_set():
        # ... post message ...
        _minder_stop_event.wait(interval_seconds)  # Interruptible wait
```

**Added `start_minder_thread()` (lines 38-62):**
```python
def start_minder_thread(
    api_base: str = "http://127.0.0.1:8010",
    channel_id: str = "hive-all",
    interval_seconds: Optional[int] = None,  # Defaults to env or 600
    author: str = "MINDER",
    message: Optional[str] = None,
) -> bool:
    """Start minder as background thread. Returns True if started."""
```

**Added `stop_minder_thread()` (lines 65-73):**
```python
def stop_minder_thread() -> bool:
    """Stop minder thread gracefully. Returns True if stopped."""
```

**Added `is_minder_running()` (lines 76-78):**
```python
def is_minder_running() -> bool:
    """Check if minder thread is currently running."""
```

**Preserved backward compatibility (lines 82-94):**
- Original `run_minder()` function still works for standalone use
- `python -m deia_raqcoon.runtime.minder` still functions

### 2. Updated `deia_raqcoon/runtime/server.py`

**Added import (line 20):**
```python
from deia_raqcoon.runtime.minder import start_minder_thread, stop_minder_thread
```

**Added startup hook (lines 33-36):**
```python
@app.on_event("startup")
async def startup_event():
    """Start background services on server startup."""
    start_minder_thread()
```

**Added shutdown hook (lines 39-42):**
```python
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up background services on server shutdown."""
    stop_minder_thread()
```

---

## Files Modified

| File | Changes |
|------|---------|
| `deia_raqcoon/runtime/minder.py` | Refactored to ~95 lines with thread-safe start/stop |
| `deia_raqcoon/runtime/server.py` | +1 import, +10 lines (lifecycle hooks) |

---

## Success Criteria Verification

- [x] `start_minder_thread()` and `stop_minder_thread()` functions added to minder.py
- [x] Minder starts automatically when server starts (via `@app.on_event("startup")`)
- [x] Minder stops cleanly on server shutdown (via `@app.on_event("shutdown")`)
- [x] Interval configurable via `DEIA_MINDER_INTERVAL` environment variable
- [x] Minder pings will be visible in `/api/messages` with `author="MINDER"`
- [x] No orphan threads on server restart (daemon=True, plus explicit stop on shutdown)
- [x] Backward compatibility: `python -m deia_raqcoon.runtime.minder` still works

---

## Key Implementation Details

### Thread Safety
- Uses `threading.Event()` for interruptible wait (can stop mid-interval)
- `wait()` instead of `sleep()` allows graceful shutdown
- Daemon thread ensures no blocking on server exit

### Environment Variable
```bash
export DEIA_MINDER_INTERVAL=10  # Override default 600 seconds
```

### Graceful Shutdown
- `stop_minder_thread()` sets the stop event
- Thread joins with 5-second timeout
- No orphan threads even if server crashes

---

## Test Instructions

```bash
# Test 1: Start server with short interval
export DEIA_MINDER_INTERVAL=10
python -m deia_raqcoon.runtime.run_server &
sleep 15

# Check for minder messages
curl http://127.0.0.1:8010/api/messages | grep -i minder
# Expected: Message with author="MINDER"

# Test 2: Backward compatibility
python -m deia_raqcoon.runtime.minder
# Should run standalone (Ctrl+C to stop)
```

---

## Issues Encountered

None. Implementation was straightforward.

---

*BEE-003A - SPRINT-001*
