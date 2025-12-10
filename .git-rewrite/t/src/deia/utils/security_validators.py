"""
Security validators for DEIA operations.

Validates paths, prevents directory traversal, enforces project boundaries.
"""

from pathlib import Path
from typing import Tuple, Optional
from urllib.parse import unquote, quote


class PathValidator:
    """Validates file system paths for security."""

    @staticmethod
    def is_safe_path(base_dir: str, requested_path: str) -> Tuple[bool, Optional[str]]:
        """
        Check if requested path is safe (within base directory).

        Args:
            base_dir: Base directory (project root)
            requested_path: Requested file path

        Returns:
            Tuple of (is_safe, error_message)
        """
        try:
            base = Path(base_dir).resolve()
            requested = Path(requested_path)

            # Resolve absolute or relative path
            if requested.is_absolute():
                target = requested.resolve()
            else:
                target = (base / requested).resolve()

            # Ensure target is within base
            target.relative_to(base)
            return True, None

        except ValueError:
            return False, "Path traversal attempt detected"
        except Exception as e:
            return False, f"Path validation error: {str(e)}"

    @staticmethod
    def normalize_path(path: str) -> str:
        """
        Normalize a path safely.

        Args:
            path: Path string

        Returns:
            Normalized path
        """
        # URL decode if needed
        path = unquote(path)

        # Normalize
        normalized = Path(path).as_posix()

        # Remove leading/trailing slashes
        normalized = normalized.strip("/")

        return normalized

    @staticmethod
    def is_directory_traversal(path: str) -> bool:
        """
        Check if path contains directory traversal attempts.

        Args:
            path: Path to check

        Returns:
            True if directory traversal detected
        """
        dangerous_patterns = [
            "..",
            "~",
            "%2e%2e",  # URL encoded ..
        ]

        path_lower = path.lower()
        for pattern in dangerous_patterns:
            if pattern in path_lower:
                return True

        return False

    @staticmethod
    def validate_filename(filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate filename is safe.

        Args:
            filename: Filename to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for path separators
        if "/" in filename or "\\" in filename:
            return False, "Filename contains path separators"

        # Check for null bytes
        if "\x00" in filename:
            return False, "Filename contains null bytes"

        # Check for directory traversal
        if PathValidator.is_directory_traversal(filename):
            return False, "Filename contains directory traversal"

        # Check length
        if len(filename) > 255:
            return False, "Filename too long (max 255 chars)"

        # Check empty
        if not filename or filename.isspace():
            return False, "Filename is empty"

        return True, None

    @staticmethod
    def get_safe_path(base_dir: str, requested_path: str) -> Optional[str]:
        """
        Get safe absolute path if valid, else None.

        Args:
            base_dir: Base directory
            requested_path: Requested path

        Returns:
            Safe absolute path or None
        """
        is_safe, error = PathValidator.is_safe_path(base_dir, requested_path)

        if not is_safe:
            return None

        base = Path(base_dir).resolve()
        requested = Path(requested_path)

        if requested.is_absolute():
            target = requested.resolve()
        else:
            target = (base / requested).resolve()

        try:
            target.relative_to(base)
            return str(target)
        except ValueError:
            return None


class EnvironmentValidator:
    """Validates environment safety for operations."""

    DEIA_PROJECT_INDICATORS = [
        ".deia",
        ".deia/hive",
        ".deia/bok",
        ".deia/governance",
    ]

    @staticmethod
    def is_deia_project(path: str) -> bool:
        """
        Check if directory is a DEIA project.

        Args:
            path: Directory to check

        Returns:
            True if appears to be DEIA project
        """
        path = Path(path)

        # Must have .deia directory
        deia_dir = path / ".deia"
        if not deia_dir.exists():
            return False

        # Check for characteristic subdirectories
        found_indicators = 0
        for indicator in EnvironmentValidator.DEIA_PROJECT_INDICATORS:
            if (path / indicator).exists():
                found_indicators += 1

        return found_indicators >= 2

    @staticmethod
    def get_project_root(start_path: str) -> Optional[str]:
        """
        Find DEIA project root by searching upward.

        Args:
            start_path: Starting path

        Returns:
            Path to project root or None
        """
        current = Path(start_path).resolve()

        # Search up to 10 levels
        for _ in range(10):
            if EnvironmentValidator.is_deia_project(str(current)):
                return str(current)

            if current.parent == current:
                # Reached filesystem root
                break

            current = current.parent

        return None
