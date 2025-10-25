"""
FileReader - Safe file reading API for DEIA Chat Interface

This module provides secure file reading within validated project boundaries,
with syntax highlighting support and proper error handling.

Features:
- Integration with PathValidator for security
- Syntax highlighting based on file extension
- Size limits (max 1MB per file)
- Encoding detection and handling
- Binary file detection
- Comprehensive error handling

Created: 2025-10-17
Author: CLAUDE-CODE-004 (Agent DOC)
Task: Chat Phase 2 - FileReader API (P1 HIGH)
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
import logging
import chardet

from .path_validator import PathValidator, ValidationResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FileContent:
    """Result of file reading operation"""
    success: bool
    content: Optional[str]
    path: str
    size_bytes: int
    encoding: Optional[str]
    language: Optional[str]
    error: Optional[str]
    error_type: Optional[str]


class FileReader:
    """
    Secure file reader with syntax highlighting support.

    Integrates with PathValidator to ensure only safe files are read.
    Enforces size limits and handles encoding detection.

    Usage:
        reader = FileReader(project_root="/path/to/deia/project")
        result = reader.read_file("bok/patterns/example.md")

        if result.success:
            print(result.content)
            print(f"Language: {result.language}")
        else:
            print(f"Error: {result.error}")
    """

    # Maximum file size (1MB)
    MAX_FILE_SIZE = 1024 * 1024  # 1MB in bytes

    # Language mapping based on file extension
    LANGUAGE_MAP = {
        # Documents
        '.md': 'markdown',
        '.txt': 'text',
        '.rst': 'restructuredtext',

        # Python
        '.py': 'python',
        '.pyw': 'python',
        '.pyi': 'python',

        # JavaScript/TypeScript
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',

        # Web
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',

        # Config
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.xml': 'xml',
        '.ini': 'ini',
        '.cfg': 'ini',

        # Shell
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'zsh',
        '.fish': 'fish',

        # Other languages
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.rs': 'rust',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php',
        '.sql': 'sql',

        # Data
        '.csv': 'csv',
        '.jsonl': 'jsonl',

        # Logs
        '.log': 'log',
    }

    # Binary file extensions to block
    BINARY_EXTENSIONS = {
        '.exe', '.dll', '.so', '.dylib',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico',
        '.pdf', '.zip', '.tar', '.gz', '.bz2', '.7z',
        '.mp3', '.mp4', '.avi', '.mov',
        '.pyc', '.pyo',
    }

    def __init__(self, project_root: str):
        """
        Initialize FileReader with project root.

        Args:
            project_root: Absolute path to DEIA project root

        Raises:
            ValueError: If project_root is invalid
        """
        self.validator = PathValidator(project_root)
        self.project_root = self.validator.get_project_root()
        logger.info(f"FileReader initialized with project root: {self.project_root}")

    def read_file(self, file_path: str) -> FileContent:
        """
        Read a file with security validation and encoding detection.

        Args:
            file_path: Relative or absolute path to file

        Returns:
            FileContent object with file contents or error details
        """
        # Step 1: Validate path security
        validation = self.validator.validate_path(file_path)

        if not validation.is_valid:
            return FileContent(
                success=False,
                content=None,
                path=file_path,
                size_bytes=0,
                encoding=None,
                language=None,
                error=f"Path validation failed: {validation.reason}",
                error_type="security_validation_failed"
            )

        # Step 2: Check file exists
        file_obj = Path(validation.normalized_path)

        if not file_obj.exists():
            return FileContent(
                success=False,
                content=None,
                path=str(file_obj),
                size_bytes=0,
                encoding=None,
                language=None,
                error=f"File does not exist: {file_obj}",
                error_type="file_not_found"
            )

        if not file_obj.is_file():
            return FileContent(
                success=False,
                content=None,
                path=str(file_obj),
                size_bytes=0,
                encoding=None,
                language=None,
                error=f"Path is not a file: {file_obj}",
                error_type="not_a_file"
            )

        # Step 3: Check file size
        size = file_obj.stat().st_size

        if size > self.MAX_FILE_SIZE:
            return FileContent(
                success=False,
                content=None,
                path=str(file_obj),
                size_bytes=size,
                encoding=None,
                language=None,
                error=f"File too large: {size} bytes (max {self.MAX_FILE_SIZE} bytes)",
                error_type="file_too_large"
            )

        # Step 4: Check for binary files by extension
        if file_obj.suffix.lower() in self.BINARY_EXTENSIONS:
            return FileContent(
                success=False,
                content=None,
                path=str(file_obj),
                size_bytes=size,
                encoding=None,
                language=None,
                error=f"Binary file type not supported: {file_obj.suffix}",
                error_type="binary_file"
            )

        # Step 5: Detect language from extension
        language = self._detect_language(file_obj)

        # Step 6: Read file with encoding detection
        try:
            content, encoding = self._read_with_encoding_detection(file_obj)

            return FileContent(
                success=True,
                content=content,
                path=str(file_obj),
                size_bytes=size,
                encoding=encoding,
                language=language,
                error=None,
                error_type=None
            )

        except UnicodeDecodeError as e:
            return FileContent(
                success=False,
                content=None,
                path=str(file_obj),
                size_bytes=size,
                encoding=None,
                language=language,
                error=f"Failed to decode file: {str(e)}",
                error_type="encoding_error"
            )
        except Exception as e:
            return FileContent(
                success=False,
                content=None,
                path=str(file_obj),
                size_bytes=size,
                encoding=None,
                language=language,
                error=f"Failed to read file: {str(e)}",
                error_type="read_error"
            )

    def read_files(self, file_paths: list[str]) -> list[FileContent]:
        """
        Read multiple files.

        Args:
            file_paths: List of file paths to read

        Returns:
            List of FileContent objects
        """
        return [self.read_file(path) for path in file_paths]

    def _detect_language(self, file_obj: Path) -> Optional[str]:
        """
        Detect programming language from file extension.

        Args:
            file_obj: Path object

        Returns:
            Language identifier or None
        """
        ext = file_obj.suffix.lower()
        return self.LANGUAGE_MAP.get(ext)

    def _read_with_encoding_detection(self, file_obj: Path) -> tuple[str, str]:
        """
        Read file with automatic encoding detection.

        Tries:
        1. UTF-8
        2. UTF-8 with BOM
        3. Chardet detection
        4. Latin-1 (fallback, always succeeds)

        Args:
            file_obj: Path object

        Returns:
            Tuple of (content, encoding)

        Raises:
            Exception: If file cannot be read
        """
        # Try UTF-8 first (most common)
        try:
            with open(file_obj, 'r', encoding='utf-8') as f:
                content = f.read()
            return content, 'utf-8'
        except UnicodeDecodeError:
            pass

        # Try UTF-8 with BOM
        try:
            with open(file_obj, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            return content, 'utf-8-sig'
        except UnicodeDecodeError:
            pass

        # Use chardet for detection
        with open(file_obj, 'rb') as f:
            raw_data = f.read()

        detected = chardet.detect(raw_data)
        encoding = detected.get('encoding')
        confidence = detected.get('confidence', 0)

        # If chardet is confident (>70%), use detected encoding
        if encoding and confidence > 0.7:
            try:
                content = raw_data.decode(encoding)
                return content, encoding
            except (UnicodeDecodeError, LookupError):
                pass

        # Fallback to latin-1 (always succeeds but may produce garbage)
        try:
            content = raw_data.decode('latin-1')
            return content, 'latin-1'
        except Exception:
            # Should never happen with latin-1, but just in case
            raise Exception("Failed to decode file with any encoding")

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get file metadata without reading contents.

        Args:
            file_path: Path to file

        Returns:
            Dictionary with file metadata
        """
        validation = self.validator.validate_path(file_path)

        if not validation.is_valid:
            return {
                'exists': False,
                'valid': False,
                'error': validation.reason,
                'blocked_rule': validation.blocked_rule,
            }

        file_obj = Path(validation.normalized_path)

        if not file_obj.exists():
            return {
                'exists': False,
                'valid': True,
                'path': str(file_obj),
            }

        stats = file_obj.stat()

        return {
            'exists': True,
            'valid': True,
            'path': str(file_obj),
            'size': stats.st_size,
            'is_file': file_obj.is_file(),
            'is_binary': file_obj.suffix.lower() in self.BINARY_EXTENSIONS,
            'language': self._detect_language(file_obj),
            'too_large': stats.st_size > self.MAX_FILE_SIZE,
        }


# Convenience function
def read_file(file_path: str, project_root: str) -> FileContent:
    """
    Convenience function to read a single file.

    Args:
        file_path: Path to file
        project_root: Project root directory

    Returns:
        FileContent object
    """
    reader = FileReader(project_root)
    return reader.read_file(file_path)
