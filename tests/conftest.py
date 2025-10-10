"""
Pytest configuration and shared fixtures for DEIA tests
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import json


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test isolation"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_deia_project(temp_dir):
    """Create a mock DEIA project structure for testing"""
    deia_dir = temp_dir / '.deia'
    deia_dir.mkdir()

    sessions_dir = deia_dir / 'sessions'
    sessions_dir.mkdir()

    # Create mock config
    config = {
        "project": "test-project",
        "user": "test-user",
        "auto_log": True
    }

    config_file = deia_dir / 'config.json'
    config_file.write_text(json.dumps(config, indent=2))

    # Create mock index
    index_file = sessions_dir / 'INDEX.md'
    index_file.write_text("# Session Index\n\n")

    yield temp_dir


@pytest.fixture
def mock_session_log():
    """Sample session log content for testing"""
    return """# Session: Test Feature Implementation

**Date:** 2025-10-07
**Type:** feature

## Context
Testing the DEIA logging system

## Key Decisions
- Use pytest for testing
- Implement fixtures for isolation

## Files Modified
- tests/conftest.py
- tests/test_logger.py

## Next Steps
- Add more test coverage
- Test CLI commands
"""


@pytest.fixture
def sample_conversation():
    """Sample conversation transcript for testing"""
    return """User: Can you help me implement a test suite?
Assistant: I'd be happy to help with that\!

User: Great, let's start with test organization.
"""
