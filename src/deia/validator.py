"""
Validation of sanitized session logs before submission
"""

import re
from pathlib import Path
from typing import List


class Validator:
    """Session log validator"""

    def validate(self, file_path: Path) -> List[str]:
        """
        Validate a file is ready for submission

        Args:
            file_path: Path to file to validate

        Returns:
            List of issues found (empty if valid)
        """

        issues = []

        content = file_path.read_text(encoding='utf-8')

        # Check template compliance
        issues.extend(self._check_template_compliance(content))

        # Check for remaining PII/secrets
        issues.extend(self._check_sensitive_data(content))

        # Check sanitization checklist
        issues.extend(self._check_sanitization_checklist(content))

        return issues

    def _check_template_compliance(self, content: str) -> List[str]:
        """Check if file follows required template structure"""

        issues = []

        required_sections = [
            '# Session:',
            '**Project:**',
            '**Date:**',
            '## Session Context',
            '## Key Activities',
        ]

        for section in required_sections:
            if section not in content:
                issues.append(f"Missing required section: {section}")

        return issues

    def _check_sensitive_data(self, content: str) -> List[str]:
        """Check for common sensitive data patterns"""

        issues = []

        # Email addresses
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content):
            issues.append("Found email address - should be sanitized")

        # API keys
        if re.search(r'\b(sk|pk)_[a-zA-Z0-9]{20,}\b', content):
            issues.append("Found potential API key - must be removed")

        # Secrets in code
        if re.search(r'(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[\'"]?([^\s\'"]+)[\'"]?', content):
            # Check if it's already redacted
            if '[redacted]' not in content and '[api-key]' not in content:
                issues.append("Found potential secret/API key in code")

        # Common file path leaks
        if re.search(r'C:\\Users\\(?!\\[user\\])[^\\\s]+\\', content):
            issues.append("Found Windows file path with username")

        if re.search(r'/home/(?![user])[^/\s]+/', content):
            issues.append("Found Unix file path with username")

        return issues

    def _check_sanitization_checklist(self, content: str) -> List[str]:
        """Check if sanitization checklist is completed"""

        issues = []

        # Look for sanitization checklist
        if 'Sanitization Checklist' in content or 'Pre-Submission' in content:
            # Check if checkboxes are marked
            unchecked = re.findall(r'- \[ \]', content)
            if len(unchecked) > 0:
                issues.append(
                    f"Sanitization checklist incomplete ({len(unchecked)} items unchecked)"
                )
        else:
            # No checklist found
            issues.append(
                "Missing sanitization checklist - "
                "ensure you've followed sanitization guidelines"
            )

        return issues
