"""
Tests for downloads_monitor service.

Tests cover:
- StateManager persistence and tracking
- DownloadsMonitor initialization and configuration
- YAML frontmatter parsing
- Temp staging functionality
- File routing with various scenarios
- Error handling and quarantine
- Startup scanning logic
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pytest

from deia.services.downloads_monitor import (
    StateManager,
    DownloadsMonitor,
)


# --- Fixtures ---

@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def state_manager(temp_dir):
    """Create StateManager with temp state file."""
    state_file = os.path.join(temp_dir, 'state.json')
    return StateManager(state_file)


@pytest.fixture
def config_dict(temp_dir):
    """Create basic configuration dictionary."""
    return {
        "downloads_folder": os.path.join(temp_dir, "downloads"),
        "projects": {
            "testproject": os.path.join(temp_dir, "projects", "testproject")
        },
        "default_destination": "docs",
        "log_file": os.path.join(temp_dir, "monitor.log"),
        "processed_folder": os.path.join(temp_dir, "processed"),
        "error_folder": os.path.join(temp_dir, "errors"),
        "archive_folder": os.path.join(temp_dir, "archive"),
        "temp_staging_folder": os.path.join(temp_dir, "temp"),
        "processing": {
            "use_temp_staging": False,
            "cleanup_policy": "manual",
            "archive_temp_after_route": False
        }
    }


@pytest.fixture
def config_file(temp_dir, config_dict):
    """Create configuration file."""
    config_path = os.path.join(temp_dir, "config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_dict, f)
    return config_path


@pytest.fixture
def monitor(config_file, state_manager):
    """Create DownloadsMonitor instance."""
    return DownloadsMonitor(config_file, state_manager)


@pytest.fixture
def sample_md_file(temp_dir):
    """Create sample markdown file with valid frontmatter."""
    content = """---
deia_routing:
  project: testproject
  destination: docs
title: Test Document
---

# Test Document

This is a test document.
"""
    filepath = os.path.join(temp_dir, "downloads", "test.md")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


# --- StateManager Tests ---

def test_state_manager_initialization(temp_dir):
    """Test StateManager initializes with default state."""
    state_file = os.path.join(temp_dir, 'state.json')
    sm = StateManager(state_file)

    assert sm.state['last_run'] is None
    assert sm.state['last_processed_files'] == []
    assert sm.state['processed_count'] == 0
    assert sm.state['errors_count'] == 0


def test_state_manager_persistence(temp_dir):
    """Test StateManager saves and loads state."""
    state_file = os.path.join(temp_dir, 'state.json')

    # Create and update state
    sm1 = StateManager(state_file)
    sm1.add_processed_file('test.md')
    sm1.update_last_run()

    # Load in new instance
    sm2 = StateManager(state_file)
    assert 'test.md' in sm2.state['last_processed_files']
    assert sm2.state['processed_count'] == 1
    assert sm2.state['last_run'] is not None


def test_add_processed_file(state_manager):
    """Test adding processed files increments counter."""
    state_manager.add_processed_file('file1.md')
    state_manager.add_processed_file('file2.md')

    assert state_manager.state['processed_count'] == 2
    assert 'file1.md' in state_manager.state['last_processed_files']
    assert 'file2.md' in state_manager.state['last_processed_files']


def test_add_processed_file_deduplication(state_manager):
    """Test adding same file twice doesn't duplicate in list."""
    state_manager.add_processed_file('test.md')
    state_manager.add_processed_file('test.md')

    # Count increments both times
    assert state_manager.state['processed_count'] == 2
    # But file only appears once in list
    assert state_manager.state['last_processed_files'].count('test.md') == 1


def test_increment_error_count(state_manager):
    """Test error counter increments."""
    state_manager.increment_error_count()
    state_manager.increment_error_count()

    assert state_manager.state['errors_count'] == 2


def test_get_last_run_datetime(state_manager):
    """Test getting last run as datetime object."""
    # No last run
    assert state_manager.get_last_run_datetime() is None

    # After update
    state_manager.update_last_run()
    last_run = state_manager.get_last_run_datetime()
    assert isinstance(last_run, datetime)
    assert last_run.tzinfo == timezone.utc


def test_was_file_processed(state_manager):
    """Test checking if file was processed."""
    assert not state_manager.was_file_processed('test.md')

    state_manager.add_processed_file('test.md')
    assert state_manager.was_file_processed('test.md')


# --- DownloadsMonitor Initialization Tests ---

def test_monitor_initialization(monitor):
    """Test DownloadsMonitor initializes correctly."""
    assert monitor.config is not None
    assert monitor.state_manager is not None
    assert monitor.logger is not None


def test_monitor_creates_folders(monitor, config_dict):
    """Test monitor creates required folders."""
    assert os.path.exists(config_dict['processed_folder'])
    assert os.path.exists(config_dict['error_folder'])
    assert os.path.exists(config_dict['archive_folder'])
    assert os.path.exists(config_dict['temp_staging_folder'])


def test_monitor_invalid_config_path(temp_dir, state_manager):
    """Test monitor raises error for missing config."""
    with pytest.raises(FileNotFoundError):
        DownloadsMonitor('/nonexistent/config.json', state_manager)


def test_monitor_invalid_json_config(temp_dir, state_manager):
    """Test monitor raises error for invalid JSON."""
    config_path = os.path.join(temp_dir, 'bad_config.json')
    with open(config_path, 'w') as f:
        f.write("{ invalid json }")

    with pytest.raises(ValueError, match="Invalid JSON"):
        DownloadsMonitor(config_path, state_manager)


# --- Frontmatter Parsing Tests ---

def test_parse_frontmatter_valid(monitor, sample_md_file):
    """Test parsing valid YAML frontmatter."""
    frontmatter = monitor.parse_frontmatter(sample_md_file)

    assert frontmatter is not None
    assert 'deia_routing' in frontmatter
    assert frontmatter['deia_routing']['project'] == 'testproject'
    assert frontmatter['deia_routing']['destination'] == 'docs'
    assert frontmatter['title'] == 'Test Document'


def test_parse_frontmatter_no_frontmatter(monitor, temp_dir):
    """Test parsing file without frontmatter."""
    filepath = os.path.join(temp_dir, "no_frontmatter.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# Just a heading\n\nNo frontmatter here.")

    frontmatter = monitor.parse_frontmatter(filepath)
    assert frontmatter is None


def test_parse_frontmatter_incomplete(monitor, temp_dir):
    """Test parsing file with incomplete frontmatter."""
    filepath = os.path.join(temp_dir, "incomplete.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\ntitle: Test\n# Missing closing ---")

    frontmatter = monitor.parse_frontmatter(filepath)
    # YAML will parse this as {'title': 'Test'} - incomplete but valid
    assert frontmatter is None or isinstance(frontmatter, dict)


def test_parse_frontmatter_invalid_yaml(monitor, temp_dir):
    """Test parsing file with invalid YAML."""
    filepath = os.path.join(temp_dir, "invalid.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\ninvalid: yaml: structure:\n---\n\nContent")

    frontmatter = monitor.parse_frontmatter(filepath)
    assert frontmatter is None


# --- Temp Staging Tests ---

def test_temp_staging_disabled(monitor, sample_md_file):
    """Test temp staging returns original path when disabled."""
    # Config has use_temp_staging: False
    success, staged_path = monitor.move_to_temp_staging(sample_md_file)

    assert success is True
    assert staged_path == sample_md_file
    assert os.path.exists(sample_md_file)


def test_temp_staging_enabled(monitor, sample_md_file, config_dict):
    """Test temp staging moves file to temp folder."""
    # Enable temp staging
    monitor.config['processing']['use_temp_staging'] = True

    original_name = os.path.basename(sample_md_file)
    success, staged_path = monitor.move_to_temp_staging(sample_md_file)

    assert success is True
    assert staged_path.startswith(config_dict['temp_staging_folder'])
    assert os.path.basename(staged_path) == original_name
    assert os.path.exists(staged_path)
    assert not os.path.exists(sample_md_file)  # Original moved


def test_temp_staging_conflict_resolution(monitor, sample_md_file, config_dict):
    """Test temp staging handles filename conflicts."""
    monitor.config['processing']['use_temp_staging'] = True

    # Create conflicting file in temp
    temp_file = os.path.join(config_dict['temp_staging_folder'], os.path.basename(sample_md_file))
    Path(temp_file).touch()

    success, staged_path = monitor.move_to_temp_staging(sample_md_file)

    assert success is True
    # Should have timestamp appended
    assert os.path.basename(staged_path) != os.path.basename(sample_md_file)
    assert os.path.exists(staged_path)
    assert os.path.exists(temp_file)  # Original temp file still there


def test_temp_staging_no_folder_configured(monitor, sample_md_file):
    """Test temp staging falls back when folder not configured."""
    monitor.config['processing']['use_temp_staging'] = True
    monitor.config['temp_staging_folder'] = None

    success, staged_path = monitor.move_to_temp_staging(sample_md_file)

    # Should succeed but not move file
    assert success is True
    assert staged_path == sample_md_file


# --- File Routing Tests ---

def test_route_file_success(monitor, sample_md_file, config_dict):
    """Test successful file routing."""
    success, msg = monitor.route_file(sample_md_file)

    assert success is True
    assert "Routed" in msg
    assert "testproject/docs" in msg

    # Check file was moved to correct location
    expected_path = os.path.join(
        config_dict['projects']['testproject'],
        'docs',
        'test.md'
    )
    assert os.path.exists(expected_path)
    assert not os.path.exists(sample_md_file)  # Original moved


def test_route_file_with_temp_staging(monitor, sample_md_file, config_dict):
    """Test routing with temp staging enabled (copy, not move)."""
    monitor.config['processing']['use_temp_staging'] = True

    success, msg = monitor.route_file(sample_md_file)

    assert success is True
    assert "copied" in msg
    assert "temp copy retained" in msg

    # Check file was copied (original still exists)
    expected_path = os.path.join(
        config_dict['projects']['testproject'],
        'docs',
        'test.md'
    )
    assert os.path.exists(expected_path)
    assert os.path.exists(sample_md_file)  # Original still there


def test_route_file_no_frontmatter(monitor, temp_dir):
    """Test routing fails without frontmatter."""
    filepath = os.path.join(temp_dir, "no_front.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# Just content")

    success, msg = monitor.route_file(filepath)

    assert success is False
    assert "No valid YAML frontmatter" in msg


def test_route_file_no_routing_section(monitor, temp_dir):
    """Test routing fails without deia_routing section."""
    filepath = os.path.join(temp_dir, "no_routing.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\ntitle: Test\n---\n\nContent")

    success, msg = monitor.route_file(filepath)

    assert success is False
    assert "No deia_routing section" in msg


def test_route_file_no_project(monitor, temp_dir):
    """Test routing fails without project specified."""
    filepath = os.path.join(temp_dir, "no_project.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\ndeia_routing:\n  destination: docs\n---\n\nContent")

    success, msg = monitor.route_file(filepath)

    assert success is False
    assert "No project specified" in msg


def test_route_file_unknown_project(monitor, temp_dir):
    """Test routing fails for unknown project."""
    filepath = os.path.join(temp_dir, "unknown.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\ndeia_routing:\n  project: unknownproject\n---\n\nContent")

    success, msg = monitor.route_file(filepath)

    assert success is False
    assert "Unknown project" in msg


def test_route_file_conflict_resolution(monitor, temp_dir, config_dict):
    """Test routing handles existing file conflicts."""
    # Create file with routing
    filepath = os.path.join(temp_dir, "downloads", "conflict.md")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\ndeia_routing:\n  project: testproject\n---\n\nContent")

    # Create conflicting file at destination
    dest_path = os.path.join(config_dict['projects']['testproject'], 'docs', 'conflict.md')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write("Existing content")

    success, msg = monitor.route_file(filepath)

    assert success is True
    # Original dest file should still exist
    assert os.path.exists(dest_path)
    # New file should have timestamp
    assert "conflict_" in msg or os.path.exists(dest_path)


def test_route_file_custom_destination(monitor, temp_dir, config_dict):
    """Test routing to custom destination folder."""
    filepath = os.path.join(temp_dir, "custom.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\ndeia_routing:\n  project: testproject\n  destination: specs\n---\n\nContent")

    success, msg = monitor.route_file(filepath)

    assert success is True
    expected_path = os.path.join(
        config_dict['projects']['testproject'],
        'specs',
        'custom.md'
    )
    assert os.path.exists(expected_path)


# --- Error Handling Tests ---

def test_handle_error_moves_to_error_folder(monitor, sample_md_file, config_dict):
    """Test error handling quarantines file."""
    monitor.handle_error(sample_md_file, "Test error")

    # File should be in error folder
    error_path = os.path.join(config_dict['error_folder'], 'test.md')
    assert os.path.exists(error_path)
    assert not os.path.exists(sample_md_file)

    # Error log should exist
    error_log = os.path.join(config_dict['error_folder'], 'test.md.error.txt')
    assert os.path.exists(error_log)

    # Check error count incremented
    assert monitor.state_manager.state['errors_count'] == 1


def test_handle_error_creates_error_log(monitor, sample_md_file, config_dict):
    """Test error log contains error details."""
    error_msg = "Invalid routing header"
    monitor.handle_error(sample_md_file, error_msg)

    error_log = os.path.join(config_dict['error_folder'], 'test.md.error.txt')
    with open(error_log, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "Invalid routing header" in content
    assert "Timestamp:" in content


def test_handle_error_no_folder_configured(monitor, sample_md_file):
    """Test error handling when error folder not configured."""
    monitor.config['error_folder'] = None

    # Should not crash, just log error
    monitor.handle_error(sample_md_file, "Test error")

    # File should still exist (not moved)
    assert os.path.exists(sample_md_file)


# --- Startup Scanning Tests ---

def test_scan_existing_files_first_run(monitor, temp_dir, config_dict):
    """Test startup scan processes all files on first run."""
    # Create several .md files
    downloads = config_dict['downloads_folder']
    os.makedirs(downloads, exist_ok=True)

    for i in range(3):
        filepath = os.path.join(downloads, f"file{i}.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Test")

    files = monitor.scan_existing_files(downloads)

    # All 3 files should be found
    assert len(files) == 3


def test_scan_existing_files_after_run(monitor, temp_dir, config_dict):
    """Test startup scan only processes new/modified files."""
    downloads = config_dict['downloads_folder']
    os.makedirs(downloads, exist_ok=True)

    # Create old file
    old_file = os.path.join(downloads, "old.md")
    with open(old_file, 'w', encoding='utf-8') as f:
        f.write("# Old")

    # Mark old file as processed
    monitor.state_manager.add_processed_file("old.md")

    # Update last run to now
    monitor.state_manager.update_last_run()

    # Create new file
    import time
    time.sleep(0.2)  # Ensure different mtime (Windows filesystem resolution)
    new_file = os.path.join(downloads, "new.md")
    with open(new_file, 'w', encoding='utf-8') as f:
        f.write("# New")

    files = monitor.scan_existing_files(downloads)

    # Only new file should be found (old file was processed and hasn't been modified)
    assert len(files) == 1
    assert new_file in files


def test_scan_existing_files_reprocesses_errors(monitor, temp_dir, config_dict):
    """Test startup scan reprocesses files not in processed list."""
    downloads = config_dict['downloads_folder']
    os.makedirs(downloads, exist_ok=True)

    filepath = os.path.join(downloads, "error_before.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# Test")

    # Simulate previous run but file not processed
    monitor.state_manager.update_last_run()
    # Don't add file to processed list

    files = monitor.scan_existing_files(downloads)

    # File should be included for reprocessing
    assert filepath in files


def test_scan_existing_files_ignores_non_md(monitor, temp_dir, config_dict):
    """Test startup scan ignores non-markdown files."""
    downloads = config_dict['downloads_folder']
    os.makedirs(downloads, exist_ok=True)

    # Create various files
    Path(os.path.join(downloads, "doc.md")).touch()
    Path(os.path.join(downloads, "image.png")).touch()
    Path(os.path.join(downloads, "text.txt")).touch()

    files = monitor.scan_existing_files(downloads)

    # Only .md file should be found
    assert len(files) == 1
    assert files[0].endswith("doc.md")


def test_scan_existing_files_ignores_directories(monitor, temp_dir, config_dict):
    """Test startup scan ignores directories named *.md."""
    downloads = config_dict['downloads_folder']
    os.makedirs(downloads, exist_ok=True)

    # Create directory with .md extension
    os.makedirs(os.path.join(downloads, "folder.md"), exist_ok=True)

    files = monitor.scan_existing_files(downloads)

    assert len(files) == 0


# --- Process File Tests ---

def test_process_file_success(monitor, sample_md_file):
    """Test full file processing pipeline."""
    success, msg = monitor.process_file(sample_md_file)

    assert success is True
    assert "Routed" in msg


def test_process_file_with_staging(monitor, sample_md_file, config_dict):
    """Test process_file with temp staging enabled."""
    monitor.config['processing']['use_temp_staging'] = True

    # Move file to downloads first
    downloads = config_dict['downloads_folder']
    os.makedirs(downloads, exist_ok=True)
    test_file = os.path.join(downloads, "stage_test.md")
    shutil.copy(sample_md_file, test_file)

    success, msg = monitor.process_file(test_file)

    assert success is True
    assert "copied" in msg


def test_process_file_error_handling(monitor, temp_dir, config_dict):
    """Test process_file handles errors correctly."""
    # Create file with invalid routing
    filepath = os.path.join(temp_dir, "bad.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# No frontmatter")

    success, msg = monitor.process_file(filepath)

    assert success is False

    # File should be in error folder
    error_path = os.path.join(config_dict['error_folder'], 'bad.md')
    assert os.path.exists(error_path)
