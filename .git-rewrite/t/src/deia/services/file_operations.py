"""
Safe file operations within DEIA project boundaries.

Wraps file I/O with project boundary validation.
"""

import os
import chardet
from pathlib import Path
from typing import Optional, Tuple, List
from enum import Enum


class FileType(Enum):
    """File type categories."""

    MARKDOWN = "markdown"
    CODE = "code"
    CONFIG = "config"
    DATA = "data"
    BINARY = "binary"
    UNKNOWN = "unknown"


class FileOperations:
    """Safe file operations with boundary enforcement."""

    SAFE_EXTENSIONS = {
        # Documentation
        ".md": FileType.MARKDOWN,
        ".txt": FileType.MARKDOWN,
        # Code
        ".py": FileType.CODE,
        ".js": FileType.CODE,
        ".ts": FileType.CODE,
        ".go": FileType.CODE,
        ".rs": FileType.CODE,
        ".java": FileType.CODE,
        # Config
        ".yaml": FileType.CONFIG,
        ".yml": FileType.CONFIG,
        ".json": FileType.CONFIG,
        ".toml": FileType.CONFIG,
        # Data
        ".csv": FileType.DATA,
        ".jsonl": FileType.DATA,
    }

    UNSAFE_PATTERNS = [
        ".git",
        ".env",
        ".secrets",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
    ]

    @staticmethod
    def read_file(project_path: str, file_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Safely read a file within project boundaries.

        Args:
            project_path: Project root path
            file_path: Path to file (relative or absolute)

        Returns:
            Tuple of (success, content, error_message)
        """
        try:
            # Validate path is within project
            is_safe, error = FileOperations.validate_path(project_path, file_path)
            if not is_safe:
                return False, None, error

            # Get absolute path
            abs_path = Path(project_path) / file_path
            abs_path = abs_path.resolve()

            # Double-check project boundary
            try:
                abs_path.relative_to(Path(project_path).resolve())
            except ValueError:
                return False, None, "Path is outside project boundaries"

            # Check file exists
            if not abs_path.exists():
                return False, None, f"File not found: {file_path}"

            if not abs_path.is_file():
                return False, None, f"Not a file: {file_path}"

            # Read file with encoding detection
            with open(abs_path, "rb") as f:
                raw_data = f.read()

            # Detect encoding
            detection = chardet.detect(raw_data)
            encoding = detection.get("encoding", "utf-8") or "utf-8"

            try:
                content = raw_data.decode(encoding)
                return True, content, None
            except Exception:
                # Fallback to latin-1 (always works)
                content = raw_data.decode("latin-1", errors="replace")
                return True, content, f"Note: Encoding detected as {encoding}"

        except Exception as e:
            return False, None, str(e)

    @staticmethod
    def validate_path(project_path: str, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate file path is safe and within project.

        Args:
            project_path: Project root path
            file_path: File path to validate

        Returns:
            Tuple of (is_safe, error_message)
        """
        # Normalize paths
        project_root = Path(project_path).resolve()
        requested_path = Path(file_path)

        # Resolve path relative to project
        if requested_path.is_absolute():
            target = requested_path.resolve()
        else:
            target = (project_root / requested_path).resolve()

        # Check project boundary
        try:
            target.relative_to(project_root)
        except ValueError:
            return False, f"Path traversal blocked: {file_path}"

        # Check unsafe patterns
        path_str = str(target)
        for pattern in FileOperations.UNSAFE_PATTERNS:
            if pattern in path_str:
                return False, f"Access denied: {pattern}"

        return True, None

    @staticmethod
    def get_file_type(file_path: str) -> FileType:
        """Determine file type from extension."""
        ext = Path(file_path).suffix.lower()
        return FileOperations.SAFE_EXTENSIONS.get(ext, FileType.UNKNOWN)

    @staticmethod
    def get_file_info(project_path: str, file_path: str) -> Optional[dict]:
        """Get metadata about a file."""
        is_safe, error = FileOperations.validate_path(project_path, file_path)
        if not is_safe:
            return None

        abs_path = (Path(project_path) / file_path).resolve()

        if not abs_path.exists():
            return None

        try:
            stat = abs_path.stat()
            return {
                "path": str(file_path),
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "is_file": abs_path.is_file(),
                "is_dir": abs_path.is_dir(),
                "type": FileOperations.get_file_type(file_path).value,
            }
        except Exception:
            return None

    @staticmethod
    def list_files(project_path: str, directory: str = "", pattern: str = "*") -> List[str]:
        """
        List files in directory within project boundaries.

        Args:
            project_path: Project root path
            directory: Directory to list (relative to project)
            pattern: File pattern to match

        Returns:
            List of file paths
        """
        is_safe, error = FileOperations.validate_path(project_path, directory or ".")
        if not is_safe:
            return []

        dir_path = (Path(project_path) / directory).resolve()

        if not dir_path.is_dir():
            return []

        try:
            files = []
            for item in dir_path.glob(pattern):
                try:
                    rel_path = item.relative_to(Path(project_path).resolve())
                    if item.is_file():
                        files.append(str(rel_path))
                except ValueError:
                    pass  # Outside project boundary
            return sorted(files)
        except Exception:
            return []
