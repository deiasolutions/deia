"""
DEIA Admin Tools - Quality control for BOK submissions
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import subprocess
import sys


class SecurityScanner:
    """Scan submissions for secrets and malicious code"""

    # Secret patterns
    SECRET_PATTERNS = {
        'aws_key': r'AKIA[0-9A-Z]{16}',
        'github_token': r'ghp_[a-zA-Z0-9]{36}',
        # Use clean raw strings for readability and to avoid escape warnings
        'api_key': r"api[_-]?key['"]?\s*[:=]\s*['"]?[a-zA-Z0-9]{20,}",
        'private_key': r'-----BEGIN (RSA |EC )?PRIVATE KEY-----',
        'password': r"password['"]?\s*[:=]\s*['"][^'"]{8,}",
        'jwt': r'eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        'slack_webhook': r'https://hooks\.slack\.com/services/[A-Z0-9/]+',
        'discord_webhook': r'https://discord\.com/api/webhooks/[\d/]+',
    }

    # Malicious code patterns
    DANGEROUS_PATTERNS = {
        'eval': r'\beval\s*\(',
        'exec': r'\bexec\s*\(',
        'compile': r'\bcompile\s*\(',
        'os_system': r'os\.system\s*\(',
        'subprocess_shell': r'subprocess\.(run|call|Popen).*shell\s*=\s*True',
        'pickle_loads': r'pickle\.loads?\s*\(',
        '__import__': r'__import__\s*\(',
        'sql_injection': r'execute\s*\(.*%s.*\)',
        'curl_pipe_bash': r'curl\s+.*\|\s*bash',
        'wget_exec': r'wget\s+.*&&.*bash',
    }

    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Scan a file for security issues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e)}

        secrets_found = []
        malicious_patterns_found = []

        # Scan for secrets
        for secret_type, pattern in self.SECRET_PATTERNS.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Get context (line number)
                line_num = content[:match.start()].count('\n') + 1
                secrets_found.append({
                    'type': secret_type,
                    'line': line_num,
                    'match': match.group()[:50] + '...' if len(match.group()) > 50 else match.group()
                })

        # Scan for malicious code
        for danger_type, pattern in self.DANGEROUS_PATTERNS.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                malicious_patterns_found.append({
                    'type': danger_type,
                    'line': line_num,
                    'context': match.group()
                })

        # Calculate risk score
        risk_score = self._calculate_risk(secrets_found, malicious_patterns_found)

        return {
            'file': file_path,
            'secrets_found': secrets_found,
            'malicious_patterns': malicious_patterns_found,
            'risk_score': risk_score,
            'recommendation': self._get_recommendation(risk_score)
        }

    def _calculate_risk(self, secrets: List, malicious: List) -> int:
        """Calculate risk score 0-100"""
        risk = 0

        # Secrets add risk
        risk += len(secrets) * 15

        # Malicious patterns add more risk
        risk += len(malicious) * 25

        # Cap at 100
        return min(risk, 100)

    def _get_recommendation(self, risk_score: int) -> str:
        """Get recommendation based on risk score"""
        if risk_score >= 80:
            return 'REJECT_IMMEDIATELY'
        elif risk_score >= 50:
            return 'REJECT'
        elif risk_score >= 20:
            return 'REVIEW_REQUIRED'
        else:
            return 'APPROVE'


class QualityChecker:
    """Check submission quality"""

    REQUIRED_SECTIONS = [
        '## Problem',
        '## Solution',
    ]

    def check_file(self, file_path: str) -> Dict[str, Any]:
        """Check file quality"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e)}

        issues = []
        score = 100

        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in content:
                issues.append(f'Missing required section: {section}')
                score -= 20

        # Check minimum length
        if len(content) < 200:
            issues.append('Content too short (< 200 chars)')
            score -= 15

        # Check for code blocks without language
        unlabeled_blocks = len(re.findall(r'```\n', content))
        if unlabeled_blocks > 0:
            issues.append(f'{unlabeled_blocks} code blocks without language tags')
            score -= 10

        # Check for broken links
        links = re.findall(r'\[.*?\]\((.*?)\)', content)
        for link in links:
            if link.startswith('http') and 'example.com' in link:
                issues.append(f'Placeholder link found: {link}')
                score -= 5

        return {
            'file': file_path,
            'quality_score': max(score, 0),
            'issues': issues,
            'recommendation': 'APPROVE' if score >= 70 else 'REQUEST_CHANGES'
        }


class UserManager:
    """Manage flagged and banned users"""

    def __init__(self):
        self.admin_dir = Path.home() / '.deia-admin'
        self.admin_dir.mkdir(exist_ok=True)
        self.banned_users_file = self.admin_dir / 'banned-users.json'
        self.flagged_users_file = self.admin_dir / 'flagged-users.json'

    def ban_user(self, username: str, reason: str, duration: Optional[str] = 'permanent') -> bool:
        """Ban a user"""
        banned_users = self._load_banned()

        banned_users[username] = {
            'reason': reason,
            'duration': duration,
            'banned_at': self._get_timestamp()
        }

        self._save_banned(banned_users)
        print(f'✓ User {username} banned ({duration}): {reason}')
        return True

    def unban_user(self, username: str) -> bool:
        """Unban a user"""
        banned_users = self._load_banned()

        if username in banned_users:
            del banned_users[username]
            self._save_banned(banned_users)
            print(f'✓ User {username} unbanned')
            return True
        else:
            print(f'User {username} is not banned')
            return False

    def flag_user(self, username: str, reason: str) -> bool:
        """Flag a user for review"""
        flagged_users = self._load_flagged()

        if username not in flagged_users:
            flagged_users[username] = []

        flagged_users[username].append({
            'reason': reason,
            'flagged_at': self._get_timestamp()
        })

        self._save_flagged(flagged_users)
        print(f'⚠ User {username} flagged: {reason}')
        return True

    def list_banned(self) -> Dict[str, Any]:
        """List all banned users"""
        return self._load_banned()

    def list_flagged(self) -> Dict[str, Any]:
        """List all flagged users"""
        return self._load_flagged()

    def _load_banned(self) -> Dict[str, Any]:
        """Load banned users list"""
        if self.banned_users_file.exists():
            return json.loads(self.banned_users_file.read_text())
        return {}

    def _save_banned(self, data: Dict[str, Any]) -> None:
        """Save banned users list"""
        self.banned_users_file.write_text(json.dumps(data, indent=2))

    def _load_flagged(self) -> Dict[str, Any]:
        """Load flagged users list"""
        if self.flagged_users_file.exists():
            return json.loads(self.flagged_users_file.read_text())
        return {}

    def _save_flagged(self, data: Dict[str, Any]) -> None:
        """Save flagged users list"""
        self.flagged_users_file.write_text(json.dumps(data, indent=2))

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'


class AIReviewer:
    """AI-assisted PR review using Claude"""

    def __init__(self):
        self.security_scanner = SecurityScanner()
        self.quality_checker = QualityChecker()

    def review_file(self, file_path: str) -> Dict[str, Any]:
        """Review a file (automated checks only for now)"""
        security_result = self.security_scanner.scan_file(file_path)
        quality_result = self.quality_checker.check_file(file_path)

        # Combine results
        risk_score = max(
            security_result.get('risk_score', 0),
            100 - quality_result.get('quality_score', 100)
        )

        return {
            'file': file_path,
            'risk_score': risk_score,
            'security': security_result,
            'quality': quality_result,
            'recommendation': self._get_overall_recommendation(security_result, quality_result),
            'summary': self._generate_summary(security_result, quality_result)
        }

    def _get_overall_recommendation(self, security: Dict, quality: Dict) -> str:
        """Get overall recommendation"""
        sec_rec = security.get('recommendation', 'APPROVE')
        qual_rec = quality.get('recommendation', 'APPROVE')

        if sec_rec in ['REJECT_IMMEDIATELY', 'REJECT']:
            return sec_rec
        elif qual_rec == 'REQUEST_CHANGES':
            return 'REQUEST_CHANGES'
        else:
            return 'APPROVE'

    def _generate_summary(self, security: Dict, quality: Dict) -> str:
        """Generate human-readable summary"""
        lines = []

        # Security summary
        secrets = security.get('secrets_found', [])
        malicious = security.get('malicious_patterns', [])

        if secrets:
            lines.append(f'🔒 Security: Found {len(secrets)} potential secret(s)')
        if malicious:
            lines.append(f'⚠️  Malicious: Found {len(malicious)} suspicious pattern(s)')

        # Quality summary
        issues = quality.get('issues', [])
        if issues:
            lines.append(f'📝 Quality: {len(issues)} issue(s) found')

        if not lines:
            lines.append('✓ No issues detected')

        return '\n'.join(lines)


def main():
    """CLI entry point for admin tools"""
    if len(sys.argv) < 2:
        print('Usage: python -m deia.admin <command> [args]')
        print('')
        print('Commands:')
        print('  scan <file>           - Security scan a file')
        print('  quality <file>        - Quality check a file')
        print('  review <file>         - Full review (security + quality)')
        print('  ban-user <username>   - Ban a user')
        print('  unban-user <username> - Unban a user')
        print('  flag-user <username>  - Flag a user for review')
        print('  list-banned           - List banned users')
        print('  list-flagged          - List flagged users')
        sys.exit(1)

    command = sys.argv[1]

    if command == 'scan':
        if len(sys.argv) < 3:
            print('Usage: python -m deia.admin scan <file>')
            sys.exit(1)

        scanner = SecurityScanner()
        result = scanner.scan_file(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif command == 'quality':
        if len(sys.argv) < 3:
            print('Usage: python -m deia.admin quality <file>')
            sys.exit(1)

        checker = QualityChecker()
        result = checker.check_file(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif command == 'review':
        if len(sys.argv) < 3:
            print('Usage: python -m deia.admin review <file>')
            sys.exit(1)

        reviewer = AIReviewer()
        result = reviewer.review_file(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif command == 'ban-user':
        if len(sys.argv) < 3:
            print('Usage: python -m deia.admin ban-user <username> [reason]')
            sys.exit(1)

        username = sys.argv[2]
        reason = sys.argv[3] if len(sys.argv) > 3 else 'No reason provided'

        manager = UserManager()
        manager.ban_user(username, reason)

    elif command == 'unban-user':
        if len(sys.argv) < 3:
            print('Usage: python -m deia.admin unban-user <username>')
            sys.exit(1)

        manager = UserManager()
        manager.unban_user(sys.argv[2])

    elif command == 'flag-user':
        if len(sys.argv) < 3:
            print('Usage: python -m deia.admin flag-user <username> [reason]')
            sys.exit(1)

        username = sys.argv[2]
        reason = sys.argv[3] if len(sys.argv) > 3 else 'No reason provided'

        manager = UserManager()
        manager.flag_user(username, reason)

    elif command == 'list-banned':
        manager = UserManager()
        banned = manager.list_banned()
        print(json.dumps(banned, indent=2))

    elif command == 'list-flagged':
        manager = UserManager()
        flagged = manager.list_flagged()
        print(json.dumps(flagged, indent=2))

    else:
        print(f'Unknown command: {command}')
        sys.exit(1)


if __name__ == '__main__':
    main()
