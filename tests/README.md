# DEIA Test Suite

Comprehensive testing for the DEIA toolkit.

---

## Quick Start

### Install Test Dependencies

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Or just test dependencies
pip install -e ".[test]"
```

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src/deia --cov-report=html

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_logger.py -v
```

---

## Test Organization

```
tests/
├── unit/               # Unit tests for individual modules
│   └── test_logger.py
├── integration/        # End-to-end workflow tests
│   └── test_cli.py
├── fixtures/           # Test data and mock structures
├── conftest.py         # Shared fixtures and configuration
└── README.md           # This file
```

---

## Test Markers

Tests are organized with markers for selective execution:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.cli` - CLI command tests
- `@pytest.mark.logger` - Logger functionality tests
- `@pytest.mark.slow` - Tests that take >1 second
- `@pytest.mark.requires_deia` - Tests needing DEIA initialized

**Run by marker:**
```bash
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
pytest -m "not slow"     # Skip slow tests
```

---

## Available Fixtures

From `conftest.py`:

- `temp_dir` - Temporary directory for test isolation
- `mock_deia_project` - Complete `.deia/` directory structure
- `mock_session_log` - Sample session log content
- `sample_conversation` - Sample conversation transcript

**Example usage:**
```python
def test_something(mock_deia_project, monkeypatch):
    monkeypatch.chdir(mock_deia_project)
    # Test code here
```

---

## Writing Tests

### Test Naming Convention

```python
def test_<what>_<condition>_<expected_result>():
    """Test that <what> does <expected_result> when <condition>"""
```

### Example Test

```python
import pytest
from pathlib import Path

@pytest.mark.unit
class TestConversationLogger:
    """Test ConversationLogger class"""

    def test_logger_creates_file_in_sessions_dir(self, mock_deia_project, monkeypatch):
        """Test that logger creates log file in .deia/sessions/"""
        monkeypatch.chdir(mock_deia_project)

        from deia.logger import ConversationLogger
        logger = ConversationLogger()

        log_file = logger.create_session_log(
            context="Test",
            transcript="User: Hello",
            decisions=[],
            action_items=[],
            files_modified=[],
            next_steps=""
        )

        assert log_file.exists()
        assert log_file.parent.name == 'sessions'
```

---

## Coverage Goals

- **Phase 1 (v0.1.x):** 50% coverage
- **Phase 2 (v0.2.x):** 70% coverage
- **v1.0:** 80% coverage

**Check current coverage:**
```bash
pytest --cov=src/deia --cov-report=term-missing
```

---

## CI/CD Integration

Tests run automatically on:
- Pull requests (unit + integration)
- Pushes to main (full suite)
- Daily schedule (comprehensive + slow tests)

---

## Debugging

### Run Single Test
```bash
pytest tests/unit/test_logger.py::TestConversationLogger::test_logger_init -vv
```

### Show Print Statements
```bash
pytest -s
```

### Drop into Debugger on Failure
```bash
pytest --pdb
```

### Increase Verbosity
```bash
pytest -vv
```

---

## Test Data

### Sensitive Data Policy

**Never commit:**
- Real conversation transcripts
- Actual user data
- API keys or credentials
- Real PII

**Use instead:**
- Synthetic test data (in `fixtures/`)
- Generated mock data (in `conftest.py`)
- Lorem ipsum placeholders
- Clearly marked fake credentials

---

## Common Issues

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'deia'`

**Solution:**
```bash
# Ensure src is in path
export PYTHONPATH=src:$PYTHONPATH  # Unix
set PYTHONPATH=src;%PYTHONPATH%    # Windows

# Or install in editable mode
pip install -e .
```

### Fixture Not Found

**Problem:** `fixture 'mock_deia_project' not found`

**Solution:** Ensure `conftest.py` is in the correct location (`tests/conftest.py`)

### Tests Pass Locally But Fail in CI

**Common causes:**
- File path differences (Windows vs Unix)
- Environment variables not set
- Timing/race conditions
- Missing dependencies

---

## Contributing

1. Write tests for new features
2. Ensure tests pass locally
3. Check coverage hasn't decreased
4. Follow naming conventions
5. Add docstrings to test classes/functions

---

## Documentation

- **Test Strategy:** `admin/testing.md`
- **Test Patterns:** (TODO)
- **CI/CD Setup:** `.github/workflows/` (TODO)

---

## Questions?

- Check `admin/testing.md` for detailed test tracking
- Review existing tests for examples
- Ask in GitHub Discussions

---

**Happy Testing!** 🧪
