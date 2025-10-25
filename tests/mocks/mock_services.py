"""
Mock service objects for testing.
"""

from typing import Dict, Optional, Tuple, List, Any
from deia.services.deia_context import DeiaContext, DeiaMeta, DeiaBokIndex


class MockDeiaContextLoader:
    """Mock DEIA context loader for testing."""

    @staticmethod
    def mock_context() -> DeiaContext:
        """Return a mock DEIA context."""
        metadata = DeiaMeta(
            project_name="test-project",
            project_path="/test/path",
            phase="Phase 1",
            team_members=["Alice", "Bob"],
        )

        bok_index = DeiaBokIndex(
            total_patterns=5,
            categories=["best_practices", "bug_fixes"],
            recent_patterns=["p1", "p2"],
        )

        return DeiaContext(
            metadata=metadata,
            bok_index=bok_index,
            recent_observations=["obs1", "obs2"],
            governance_summary="Test governance",
        )


class MockFileOperations:
    """Mock file operations for testing."""

    def __init__(self):
        self.read_calls = []
        self.write_calls = []
        self.files: Dict[str, str] = {}

    def read_file(self, project_path: str, file_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Mock file read."""
        self.read_calls.append((project_path, file_path))

        key = f"{project_path}/{file_path}"
        if key in self.files:
            return True, self.files[key], None

        return False, None, "File not found"

    def write_file(self, project_path: str, file_path: str, content: str) -> Tuple[bool, Optional[str]]:
        """Mock file write."""
        self.write_calls.append((project_path, file_path, content))

        key = f"{project_path}/{file_path}"
        self.files[key] = content
        return True, None

    def set_file_content(self, path: str, content: str) -> None:
        """Set content for a mocked file."""
        self.files[path] = content


class MockPathValidator:
    """Mock path validator for testing."""

    def __init__(self, allow_all: bool = False):
        self.allow_all = allow_all
        self.validation_calls = []

    def is_safe_path(self, base_dir: str, requested_path: str) -> Tuple[bool, Optional[str]]:
        """Mock path validation."""
        self.validation_calls.append((base_dir, requested_path))

        if self.allow_all:
            return True, None

        if ".." in requested_path:
            return False, "Directory traversal detected"

        if requested_path.startswith("/"):
            return False, "Absolute paths not allowed"

        return True, None

    def set_allow_all(self, allow: bool) -> None:
        """Set whether to allow all paths."""
        self.allow_all = allow


class MockSessionParser:
    """Mock session parser for testing."""

    def __init__(self):
        self.parse_calls = []
        self.mock_messages = []

    def parse_content(self, content: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Mock parse content."""
        self.parse_calls.append(content)

        metadata = {
            "session_id": "mock-001",
            "date": "2025-10-25",
        }

        return metadata, self.mock_messages

    def set_mock_messages(self, messages: List[Dict[str, Any]]) -> None:
        """Set mock messages to return."""
        self.mock_messages = messages


class MockBOKValidator:
    """Mock BOK validator for testing."""

    def __init__(self, always_valid: bool = False):
        self.always_valid = always_valid
        self.validation_calls = []
        self.errors = []

    def validate(self, pattern: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Mock validation."""
        self.validation_calls.append(pattern)

        if self.always_valid:
            return True, []

        if self.errors:
            return False, self.errors

        # Simple validation
        required = ["title", "pattern_type", "problem", "solution", "reasoning"]
        missing = [f for f in required if f not in pattern]

        if missing:
            return False, [f"Missing fields: {', '.join(missing)}"]

        return True, []

    def set_errors(self, errors: List[str]) -> None:
        """Set errors to return on validation."""
        self.errors = errors
