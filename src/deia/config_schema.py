"""
DEIA Configuration Schema

Defines user preferences for auto-submission, trusted submitters, etc.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path
import json


@dataclass
class SubmissionConfig:
    """Configuration for BOK submission behavior"""

    # Manual review by default
    auto_submit: bool = False

    # If auto_submit is True, anonymize before submission
    auto_anonymize: bool = True

    # GitHub username for submissions
    github_username: Optional[str] = None

    # Email for commit attribution
    email: Optional[str] = None

    # Auto-create PRs or just local commit
    auto_create_pr: bool = False


@dataclass
class TrustedSubmitter:
    """Configuration for a trusted submitter (bypass review)"""

    username: str
    # CFRL = Commit First, Review Later
    cfrl_enabled: bool = True
    auto_accept: bool = True
    # Optional: require GPG signature
    require_signature: bool = False


@dataclass
class DEIAConfig:
    """Main DEIA configuration"""

    # Project-specific settings
    project_name: str

    # Submission settings for this user
    submission: SubmissionConfig = field(default_factory=SubmissionConfig)

    # If this user is acting as DEIA admin
    is_admin: bool = False

    # Trusted submitters (admin only)
    trusted_submitters: List[TrustedSubmitter] = field(default_factory=list)

    # Local paths
    deia_dir: Path = field(default_factory=lambda: Path('.deia'))
    intake_dir: Path = field(default_factory=lambda: Path('.deia/intake'))
    sessions_dir: Path = field(default_factory=lambda: Path('.deia/sessions'))

    def to_dict(self) -> dict:
        """Serialize to dict"""
        return {
            'project_name': self.project_name,
            'submission': {
                'auto_submit': self.submission.auto_submit,
                'auto_anonymize': self.submission.auto_anonymize,
                'github_username': self.submission.github_username,
                'email': self.submission.email,
                'auto_create_pr': self.submission.auto_create_pr
            },
            'is_admin': self.is_admin,
            'trusted_submitters': [
                {
                    'username': ts.username,
                    'cfrl_enabled': ts.cfrl_enabled,
                    'auto_accept': ts.auto_accept,
                    'require_signature': ts.require_signature
                }
                for ts in self.trusted_submitters
            ]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DEIAConfig':
        """Deserialize from dict"""
        submission = SubmissionConfig(
            auto_submit=data['submission'].get('auto_submit', False),
            auto_anonymize=data['submission'].get('auto_anonymize', True),
            github_username=data['submission'].get('github_username'),
            email=data['submission'].get('email'),
            auto_create_pr=data['submission'].get('auto_create_pr', False)
        )

        trusted = [
            TrustedSubmitter(
                username=ts['username'],
                cfrl_enabled=ts.get('cfrl_enabled', True),
                auto_accept=ts.get('auto_accept', True),
                require_signature=ts.get('require_signature', False)
            )
            for ts in data.get('trusted_submitters', [])
        ]

        return cls(
            project_name=data['project_name'],
            submission=submission,
            is_admin=data.get('is_admin', False),
            trusted_submitters=trusted
        )

    def save(self, path: Path):
        """Save config to JSON file"""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> 'DEIAConfig':
        """Load config from JSON file"""
        with open(path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


# Default configs for common scenarios

def get_end_user_config(project_name: str, github_username: str = None) -> DEIAConfig:
    """
    Default config for end-user (manual review before submission)
    """
    return DEIAConfig(
        project_name=project_name,
        submission=SubmissionConfig(
            auto_submit=False,  # Manual review by default
            auto_anonymize=True,
            github_username=github_username,
            auto_create_pr=False
        ),
        is_admin=False
    )


def get_dave_config(project_name: str) -> DEIAConfig:
    """
    Dave's config as trusted submitter with CFRL

    Commit First, Review Later - bypasses review, auto-accepts
    """
    return DEIAConfig(
        project_name=project_name,
        submission=SubmissionConfig(
            auto_submit=True,  # Auto-submit enabled for Dave
            auto_anonymize=True,  # Still anonymize
            github_username='DAAAAVE-ATX',
            email='dave@deiasolutions.org',
            auto_create_pr=True  # Auto-create PRs
        ),
        is_admin=False  # As end-user, not admin
    )


def get_admin_config() -> DEIAConfig:
    """
    DEIA admin config (Dave reviewing submissions)
    """
    return DEIAConfig(
        project_name='deiasolutions',
        submission=SubmissionConfig(
            auto_submit=False,
            github_username='DAAAAVE-ATX'
        ),
        is_admin=True,
        trusted_submitters=[
            TrustedSubmitter(
                username='DAAAAVE-ATX',
                cfrl_enabled=True,
                auto_accept=True,
                require_signature=False
            )
        ]
    )
