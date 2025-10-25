"""
PathValidator - Security module for file path validation

This module provides critical security for the DEIA Chat Interface Phase 2,
preventing unauthorized file access through path traversal attacks and
enforcing project boundary restrictions.

Security Model:
1. Directory Traversal Prevention: Block '..' path components
2. Project Boundary Enforcement: Only allow access within DEIA project root
3. Sensitive File Protection: Block access to .git, .env, secrets, credentials
4. Absolute Path Resolution: Resolve all paths to prevent symlink attacks

Created: 2025-10-17
Author: CLAUDE-CODE-004 (Agent DOC)
Task: Chat Phase 2 - PathValidator (P0 CRITICAL)
"""

import os
import re
from pathlib import Path
from typing import Tuple, Optional, List
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of path validation"""
    is_valid: bool
    normalized_path: Optional[str]
    reason: Optional[str]
    blocked_rule: Optional[str]


class PathValidator:
    """
    Validates file paths for security and project boundary compliance.

    This class enforces critical security rules to prevent unauthorized
    file access in the DEIA chat interface.

    Security Rules:
    1. NO directory traversal (../ or ..\\ patterns)
    2. NO access outside project root
    3. NO access to sensitive files (.git, .env, secrets, etc.)
    4. ALL paths must resolve to absolute paths within project

    Usage:
        validator = PathValidator(project_root="/path/to/deia/project")
        result = validator.validate_path("bok/patterns/example.md")

        if result.is_valid:
            # Safe to read file at result.normalized_path
            pass
        else:
            # Path is blocked: result.reason, result.blocked_rule
            pass
    """

    # Sensitive file patterns (case-insensitive)
    SENSITIVE_PATTERNS = [
        r"\.git($|/|\\)",           # .git directory and contents
        r"\.env($|\.)",             # .env files
        r"\.env\..*",               # .env.local, .env.production, etc.
        r"secret",                  # Any file/dir with "secret" in name
        r"credential",              # Any file/dir with "credential" in name
        r"password",                # Any file/dir with "password" in name
        r"token",                   # Any file/dir with "token" in name
        r"\.key($|\.)",             # .key files
        r"\.pem($|\.)",             # .pem files
        r"\.p12($|\.)",             # .p12 files
        r"\.pfx($|\.)",             # .pfx files
        r"id_rsa",                  # SSH private keys
        r"id_dsa",                  # SSH private keys
        r"\.ssh($|/|\\)",           # SSH directory
        r"\.aws($|/|\\)",           # AWS credentials directory
        r"\.azure($|/|\\)",         # Azure credentials directory
        r"\.gcp($|/|\\)",           # GCP credentials directory
        r"config\.json",            # Common config files that may have secrets
        r"settings\.json",          # Settings files
        r"\.pypirc",                # PyPI credentials
        r"\.npmrc",                 # NPM credentials
    ]

    def __init__(self, project_root: str):
        """
        Initialize PathValidator with project root.

        Args:
            project_root: Absolute path to the DEIA project root directory

        Raises:
            ValueError: If project_root is not an absolute path or doesn't exist
        """
        self.project_root = Path(project_root).resolve()

        if not self.project_root.is_absolute():
            raise ValueError(f"Project root must be absolute path: {project_root}")

        if not self.project_root.exists():
            raise ValueError(f"Project root does not exist: {project_root}")

        if not self.project_root.is_dir():
            raise ValueError(f"Project root is not a directory: {project_root}")

        # Compile sensitive patterns for performance
        self.sensitive_regex = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.SENSITIVE_PATTERNS
        ]

        logger.info(f"PathValidator initialized with project root: {self.project_root}")

    def validate_path(self, file_path: str) -> ValidationResult:
        """
        Validate a file path for security and project boundary compliance.

        Args:
            file_path: Relative or absolute file path to validate

        Returns:
            ValidationResult with validation status, normalized path, and details
        """
        # 1. Check for directory traversal patterns
        if self._contains_traversal(file_path):
            return ValidationResult(
                is_valid=False,
                normalized_path=None,
                reason="Directory traversal detected (../ or ..\\ pattern)",
                blocked_rule="traversal_prevention"
            )

        # 2. Normalize and resolve path
        try:
            normalized = self._normalize_path(file_path)
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                normalized_path=None,
                reason=f"Path normalization failed: {str(e)}",
                blocked_rule="normalization_error"
            )

        # 3. Check project boundary
        if not self._within_project_boundary(normalized):
            return ValidationResult(
                is_valid=False,
                normalized_path=None,
                reason=f"Path outside project boundary: {normalized}",
                blocked_rule="boundary_enforcement"
            )

        # 4. Check sensitive files
        sensitive_check = self._check_sensitive_file(normalized)
        if sensitive_check:
            return ValidationResult(
                is_valid=False,
                normalized_path=None,
                reason=f"Access to sensitive file blocked: {sensitive_check}",
                blocked_rule="sensitive_file_protection"
            )

        # 5. All checks passed
        return ValidationResult(
            is_valid=True,
            normalized_path=str(normalized),
            reason="Path validated successfully",
            blocked_rule=None
        )

    def validate_paths(self, file_paths: List[str]) -> List[ValidationResult]:
        """
        Validate multiple file paths.

        Args:
            file_paths: List of file paths to validate

        Returns:
            List of ValidationResult objects, one per input path
        """
        return [self.validate_path(path) for path in file_paths]

    def _contains_traversal(self, path: str) -> bool:
        """
        Check if path contains directory traversal patterns.

        Detects:
        - ../  (Unix)
        - ..\\ (Windows)
        - Encoded variants (%2e%2e%2f, etc.)

        Args:
            path: File path to check

        Returns:
            True if traversal pattern detected, False otherwise
        """
        # Check for literal ../ or ..\\ patterns
        if ".." in path:
            return True

        # Check for URL-encoded traversal attempts
        encoded_patterns = [
            "%2e%2e%2f",    # ../
            "%2e%2e/",      # ../
            "..%2f",        # ../
            "%2e%2e%5c",    # ..\\
            "%2e%2e\\",     # ..\\
            "..%5c",        # ..\\
        ]

        path_lower = path.lower()
        for pattern in encoded_patterns:
            if pattern in path_lower:
                return True

        return False

    def _normalize_path(self, path: str) -> Path:
        """
        Normalize file path to absolute resolved path.

        - Converts relative paths to absolute (relative to project_root)
        - Resolves symlinks
        - Normalizes path separators

        Args:
            path: File path to normalize

        Returns:
            Resolved absolute Path object

        Raises:
            Exception: If path resolution fails
        """
        path_obj = Path(path)

        # If path is relative, make it relative to project_root
        if not path_obj.is_absolute():
            path_obj = self.project_root / path_obj

        # Resolve to absolute path (follows symlinks)
        resolved = path_obj.resolve()

        return resolved

    def _within_project_boundary(self, path: Path) -> bool:
        """
        Check if resolved path is within project boundaries.

        Args:
            path: Resolved absolute Path object

        Returns:
            True if path is within project root, False otherwise
        """
        try:
            # Check if path is relative to project_root
            path.relative_to(self.project_root)
            return True
        except ValueError:
            # path.relative_to() raises ValueError if path is not within project_root
            return False

    def _check_sensitive_file(self, path: Path) -> Optional[str]:
        """
        Check if path matches sensitive file patterns.

        Args:
            path: Resolved absolute Path object

        Returns:
            Matched pattern string if sensitive, None if safe
        """
        path_str = str(path)

        # Check against all sensitive patterns
        for regex in self.sensitive_regex:
            if regex.search(path_str):
                return regex.pattern

        return None

    def get_project_root(self) -> str:
        """Get the configured project root path."""
        return str(self.project_root)

    def get_sensitive_patterns(self) -> List[str]:
        """Get list of sensitive file patterns."""
        return self.SENSITIVE_PATTERNS.copy()


# Convenience function for single-path validation
def validate_path(file_path: str, project_root: str) -> ValidationResult:
    """
    Convenience function to validate a single path.

    Args:
        file_path: File path to validate
        project_root: Project root directory

    Returns:
        ValidationResult object
    """
    validator = PathValidator(project_root)
    return validator.validate_path(file_path)
