# Downloads Monitor - DEIA File Routing Service

**Service:** `src/deia/services/downloads_monitor.py`
**Version:** 1.0
**Status:** Production-ready
**Test Coverage:** 90% (38 tests, all passing ✅)

---

## Overview

The **Downloads Monitor** automatically routes markdown files from your Downloads folder to project directories based on YAML frontmatter routing headers. Features safe temp staging, state persistence, and intelligent startup scanning.

**Key Features:**
- ✅ YAML frontmatter-based routing
- ✅ Safe temp staging (optional - files retained until manually cleaned)
- ✅ State persistence (tracks processed files across runs)
- ✅ Startup scanning (processes new/modified files on launch)
- ✅ Error handling with quarantine
- ✅ File conflict resolution
- ✅ Production-ready with 90% test coverage

---

## Quick Start

### Python API

```python
from deia.services.downloads_monitor import DownloadsMonitor, StateManager

# Initialize state manager
state = StateManager('/path/to/state.json')

# Create monitor
monitor = DownloadsMonitor(
    config_path='/path/to/config.json',
    state_manager=state
)

# Route a single file
success, msg = monitor.route_file('/path/to/Downloads/doc.md')
if success:
    print(f"Success: {msg}")

# Scan and process all pending files
files = monitor.scan_existing_files('/path/to/Downloads')
for file_path in files:
    monitor.process_file(file_path)
```

### Configuration File (JSON)

```json
{
  "downloads_folder": "/Users/you/Downloads",
  "projects": {
    "myproject": "/path/to/myproject",
    "otherproject": "/path/to/otherproject"
  },
  "default_destination": "docs",
  "log_file": "/path/to/monitor.log",
  "processed_folder": "/path/to/processed",
  "error_folder": "/path/to/errors",
  "temp_staging_folder": "/path/to/.deia-staging",
  "processing": {
    "use_temp_staging": true,
    "cleanup_policy": "manual",
    "archive_temp_after_route": false
  }
}
```

### Markdown File Format

Add YAML frontmatter to your markdown files:

```markdown
---
deia_routing:
  project: myproject
  destination: docs
title: My Document
author: Your Name
---

# My Document

Content goes here...
```

---

## API Reference

### `StateManager(state_file: str)`

Manages state persistence across monitor runs.

**Args:**
- `state_file` - Path to JSON state file

**Methods:**

#### `add_processed_file(filename: str)` → None
Record a successfully processed file.

#### `was_file_processed(filename: str)` → bool
Check if file was processed before.

#### `update_last_run()` → None
Update last run timestamp to now.

#### `get_last_run_datetime()` → Optional[datetime]
Get last run as datetime object.

#### `increment_error_count()` → None
Increment error counter.

**Example:**
```python
state = StateManager('/path/to/state.json')
state.add_processed_file('example.md')

if state.was_file_processed('example.md'):
    print("Already processed")
```

---

### `DownloadsMonitor(config_path: str, state_manager: StateManager)`

Main monitor class for file routing.

**Args:**
- `config_path` - Path to JSON configuration file
- `state_manager` - StateManager instance

**Raises:**
- `FileNotFoundError` - If config file doesn't exist
- `ValueError` - If config is invalid JSON
- `ImportError` - If pyyaml not installed

---

### `parse_frontmatter(file_path: str)` → Optional[Dict]

Extract YAML frontmatter from markdown file.

**Args:**
- `file_path` - Path to markdown file

**Returns:** Parsed frontmatter dict or None

**Example:**
```python
frontmatter = monitor.parse_frontmatter('file.md')
if frontmatter and 'deia_routing' in frontmatter:
    project = frontmatter['deia_routing']['project']
    destination = frontmatter['deia_routing']['destination']
```

---

### `move_to_temp_staging(file_path: str)` → Tuple[bool, str]

Move file to temp staging area for safe processing.

**Args:**
- `file_path` - Path to file to stage

**Returns:** `(success: bool, staged_path: str)`

**Behavior:**
- If `use_temp_staging` is False: Returns original path
- If enabled: Moves file to temp folder
- Handles filename conflicts with timestamps

**Example:**
```python
success, staged_path = monitor.move_to_temp_staging('/Downloads/file.md')
if success:
    print(f"Staged at: {staged_path}")
```

---

### `route_file(file_path: str)` → Tuple[bool, str]

Route file to project folder based on YAML routing header.

**Args:**
- `file_path` - Path to file to route

**Returns:** `(success: bool, message: str)`

**Routing Logic:**
1. Parse YAML frontmatter
2. Extract `deia_routing.project` and `deia_routing.destination`
3. Validate project exists in config
4. Handle file conflicts (timestamp appending)
5. Copy (if temp staging) or move (if not) file to destination
6. Record success to state

**Example:**
```python
success, msg = monitor.route_file('/Downloads/doc.md')
if success:
    print(msg)  # "Routed doc.md => myproject/docs"
else:
    print(f"Error: {msg}")
```

---

### `handle_error(file_path: str, error_msg: str)` → None

Move file to error folder and log the issue.

**Args:**
- `file_path` - Path to problem file
- `error_msg` - Description of error

**Behavior:**
- Moves file to error folder (quarantine)
- Creates `.error.txt` log file
- Increments error counter in state

**Example:**
```python
monitor.handle_error('/path/to/bad.md', 'No routing header found')
```

---

### `scan_existing_files(downloads_folder: str)` → List[str]

Scan Downloads folder for files that need processing.

**Args:**
- `downloads_folder` - Path to Downloads folder

**Returns:** List of file paths needing processing

**Scanning Logic:**
- **First run** (no `last_run`): Process all `.md` files
- **Subsequent runs**: Process files that are:
  - Modified after `last_run`
  - Not in processed list (may have errored before)

**Example:**
```python
files = monitor.scan_existing_files('/Users/you/Downloads')
print(f"Found {len(files)} files to process")

for file_path in files:
    monitor.process_file(file_path)
```

---

### `process_file(file_path: str)` → Tuple[bool, str]

Process file through full pipeline: stage → route → handle errors.

**Args:**
- `file_path` - Path to file to process

**Returns:** `(success: bool, message: str)`

**Pipeline:**
1. Move to temp staging (if enabled)
2. Route file from temp (or original location)
3. Handle errors (quarantine if routing fails)

**Example:**
```python
success, msg = monitor.process_file('/Downloads/file.md')
if not success:
    print(f"Processing failed: {msg}")
```

---

## Features

### Safe Temp Staging

When `use_temp_staging` is enabled:

```
Downloads/doc.md
  ↓ (move)
.deia-staging/doc.md
  ↓ (copy)
project/docs/doc.md

Result: File in BOTH temp and project
```

**Benefits:**
- ✅ Never lose data - original in temp until manually deleted
- ✅ Easy recovery - check temp if routing went wrong
- ✅ Audit trail - review what was processed
- ✅ Safe testing - test routing without fear

**Manual Cleanup:**
```bash
# Verify files committed to git
cd ~/projects/myproject
git status
git log --oneline | head -5

# If safe, clean up temp
rm -rf ~/.deia-staging/*
```

---

### State Persistence

State file (`state.json`) tracks:
- `last_run` - Timestamp of last monitor run
- `last_processed_files` - List of successfully processed filenames
- `processed_count` - Total files processed (all time)
- `errors_count` - Total errors encountered

**Example state.json:**
```json
{
  "last_run": "2025-10-19T06:30:00+00:00",
  "last_processed_files": ["doc1.md", "doc2.md", "doc3.md"],
  "processed_count": 127,
  "errors_count": 3
}
```

---

### Startup Scanning

On startup, monitor scans Downloads and processes:
1. **All files** if first run (no `last_run`)
2. **New files** modified after `last_run`
3. **Error retry** files not in processed list

This enables:
- Process accumulated files after downtime
- Retry previously failed files
- No manual file tracking required

---

### Error Handling

Files that can't be routed are quarantined:

**Error folder structure:**
```
errors/
├── bad-file.md           # Quarantined file
└── bad-file.md.error.txt # Error details
```

**Error log example:**
```
Error: No deia_routing section in bad-file.md
Timestamp: 2025-10-19T06:35:12.345678
```

**Common errors:**
- No YAML frontmatter
- Missing `deia_routing` section
- No `project` specified
- Unknown project name
- File permission issues

---

### File Conflict Resolution

If target file already exists:
1. Generate timestamp: `YYYYMMDD_HHMMSS`
2. Append to filename: `doc_20251019_063000.md`
3. Log warning with new filename

This prevents:
- ❌ Overwriting existing files
- ❌ Data loss
- ❌ Silent conflicts

---

## Use Cases

### Automated Documentation Routing

```python
# Route docs from Downloads to projects automatically
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AutoRouter(FileSystemEventHandler):
    def __init__(self, monitor):
        self.monitor = monitor

    def on_created(self, event):
        if event.src_path.endswith('.md'):
            self.monitor.process_file(event.src_path)

# Setup watching
observer = Observer()
observer.schedule(AutoRouter(monitor), downloads_folder, recursive=False)
observer.start()
```

### One-Time Batch Processing

```python
# Process all pending files once
monitor = DownloadsMonitor(config_path, state)
files = monitor.scan_existing_files(downloads_folder)

print(f"Processing {len(files)} files...")
for file_path in files:
    success, msg = monitor.process_file(file_path)
    print(f"{'✓' if success else '✗'} {msg}")

state.update_last_run()
```

### Integration with Git Workflow

```python
import subprocess

# Route file
success, msg = monitor.route_file(file_path)

if success:
    # Add to git
    subprocess.run(['git', 'add', routed_path])
    subprocess.run(['git', 'commit', '-m', f'Add {filename}'])

    # Clean up temp only after git commit
    if temp_path and os.path.exists(temp_path):
        os.remove(temp_path)
```

---

## Test Coverage

**Coverage:** 90% (exceeds >80% requirement)
**Tests:** 38 comprehensive tests
**Status:** All passing ✅

**Test Coverage Includes:**
- StateManager initialization and persistence
- Configuration loading (valid and invalid)
- YAML frontmatter parsing (various formats)
- Temp staging (enabled/disabled, conflicts)
- File routing (success, errors, conflicts)
- Error handling (quarantine, logging)
- Startup scanning (first run, subsequent, errors)
- Process pipeline (end-to-end)
- Edge cases (missing folders, permissions, etc.)

---

## Configuration

### Required Fields

```json
{
  "downloads_folder": "/path/to/Downloads",
  "projects": {
    "project-name": "/path/to/project"
  }
}
```

### Optional Fields

```json
{
  "default_destination": "docs",           // Default folder in project
  "log_file": "/path/to/monitor.log",      // Log file path
  "processed_folder": "/path/to/processed", // Processed file tracking
  "error_folder": "/path/to/errors",       // Error quarantine
  "temp_staging_folder": "/path/to/temp",  // Temp staging area
  "processing": {
    "use_temp_staging": false,              // Enable temp staging
    "cleanup_policy": "manual",             // Cleanup policy (manual only)
    "archive_temp_after_route": false       // Archive temp files
  }
}
```

---

## Dependencies

**Required:**
- Python 3.9+
- `pyyaml>=6.0` (YAML parsing)

**Optional:**
- `watchdog>=3.0` (file watching for live monitoring)

**Install:**
```bash
pip install pyyaml
pip install watchdog  # Optional, for live monitoring
```

---

## Related Services

- **File Reader** - Safe file reading with encoding detection
- **Path Validator** - Security layer for path validation
- **Session Logger** - Activity tracking and analytics

---

## Future Enhancements

Potential improvements for future versions:

1. **Git-Aware Cleanup** (Phase 2)
   - Auto-delete temp after git commit confirmed
   - Archive on timeout (24h safety net)
   - Handle `.gitignore` detection

2. **Privacy Handling** (Phase 3)
   - Parse privacy markings from YAML
   - Encrypt archived files for private/internal
   - Block routing on privacy violations

3. **CLI Integration** (Phase 4)
   - `deia monitor start/stop/status` commands
   - System service integration (systemd/launchd)
   - Real-time notifications

4. **Advanced Features**
   - Version tracking and provenance
   - Duplicate detection
   - Smart destination inference
   - Multi-project routing

Current implementation prioritizes **correctness and safety** over premature optimization.

---

## Troubleshooting

### "pyyaml not installed" error
**Solution:** `pip install pyyaml`

### Files not being routed
**Check:**
1. YAML frontmatter format (must start with `---`)
2. `deia_routing` section exists
3. `project` field matches config
4. Project path in config is valid

### Files going to error folder
**Solution:** Check `.error.txt` file in error folder for details

### Temp staging not working
**Check:**
1. `use_temp_staging: true` in config
2. `temp_staging_folder` is configured and writable
3. Sufficient disk space

### State not persisting
**Check:**
1. `state_file` path is writable
2. No permission errors in logs
3. `save_state()` being called after updates

---

**Last Updated:** 2025-10-19
**Status:** Production-ready
**Test Coverage:** 90%
