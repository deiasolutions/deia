"""
Automated sanitization of session logs
"""

import re
from typing import Tuple, List


class Sanitizer:
    """Automated sanitization engine"""

    def __init__(self):
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> dict:
        """Load sanitization patterns"""

        return {
            # Email addresses
            'email': (
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                '[email]'
            ),

            # URLs (except common public ones)
            'url': (
                r'https?://(?!(?:github\.com|stackoverflow\.com|docs\.python\.org|developer\.mozilla\.org))[^\s]+',
                '[url]'
            ),

            # File paths with usernames (Windows)
            'windows_path': (
                r'C:\\Users\\[^\\]+\\',
                'C:\\Users\\[user]\\'
            ),

            # File paths with usernames (Unix)
            'unix_path': (
                r'/home/[^/]+/',
                '/home/[user]/'
            ),

            # API keys (common patterns)
            'api_key_sk': (
                r'\b(sk|pk)_[a-zA-Z0-9]{20,}\b',
                '[api-key]'
            ),

            # Generic secrets
            'secret_pattern': (
                r'(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[\'"]?([^\s\'"]+)[\'"]?',
                r'\1: [redacted]'
            ),

            # IP addresses (private ranges)
            'private_ip': (
                r'\b(?:10\.|172\.(?:1[6-9]|2[0-9]|3[01])\.|192\.168\.)\d{1,3}\.\d{1,3}\b',
                '[internal-ip]'
            ),

            # Database connection strings
            'db_connection': (
                r'(?:mongodb|postgres|mysql)://[^\s]+',
                '[database-url]'
            ),
        }

    def sanitize(self, content: str) -> Tuple[str, List[str]]:
        """
        Sanitize content

        Args:
            content: Raw content to sanitize

        Returns:
            Tuple of (sanitized_content, warnings)
        """

        sanitized = content
        warnings = []

        # Apply each pattern
        for name, (pattern, replacement) in self.patterns.items():
            matches = re.findall(pattern, sanitized)
            if matches:
                warnings.append(f"Found {len(matches)} {name} pattern(s)")
                sanitized = re.sub(pattern, replacement, sanitized)

        # Check for high-entropy strings (potential secrets)
        high_entropy = self._find_high_entropy_strings(sanitized)
        if high_entropy:
            warnings.append(
                f"Found {len(high_entropy)} high-entropy strings (potential secrets). "
                "Review manually."
            )

        # Check for common name patterns
        if self._contains_likely_names(sanitized):
            warnings.append(
                "Content may contain personal names. Review manually."
            )

        return sanitized, warnings

    def _find_high_entropy_strings(self, content: str) -> List[str]:
        """Find strings with high entropy (potential secrets)"""

        import math
        from collections import Counter

        candidates = re.findall(r'\b[A-Za-z0-9]{20,}\b', content)
        high_entropy = []

        for candidate in candidates:
            # Calculate Shannon entropy
            counter = Counter(candidate)
            length = len(candidate)
            entropy = -sum(
                (count / length) * math.log2(count / length)
                for count in counter.values()
            )

            # High entropy suggests randomness (like API keys)
            if entropy > 4.0:  # Threshold
                high_entropy.append(candidate)

        return high_entropy

    def _contains_likely_names(self, content: str) -> bool:
        """Check if content contains likely personal names"""

        # Simple heuristic: capitalized words that appear frequently
        # This will have false positives (coding terms, framework names)
        # But better to warn and let human review

        capitalized = re.findall(r'\b[A-Z][a-z]{2,}\b', content)

        # Exclude common coding terms
        exclude = {
            'Python', 'JavaScript', 'TypeScript', 'React', 'Vue', 'Angular',
            'Django', 'Flask', 'FastAPI', 'Express', 'Node', 'MongoDB',
            'PostgreSQL', 'Redis', 'Docker', 'Kubernetes', 'Git', 'GitHub',
            'Claude', 'Cursor', 'Copilot', 'VSCode', 'Windows', 'Linux', 'Mac',
            'Chrome', 'Firefox', 'Safari', 'Edge', 'Netflix', 'Amazon', 'Google',
            'Microsoft', 'Apple', 'Meta', 'Twitter', 'Facebook', 'OpenAI',
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        }

        potential_names = [w for w in capitalized if w not in exclude]

        # If same capitalized word appears multiple times, likely a name
        from collections import Counter
        counter = Counter(potential_names)

        return any(count >= 3 for count in counter.values())
