"""
DEIA Vendor Feedback System

Allows users to save conversations for AI vendor review (Anthropic, OpenAI, Google).
Users control access via git-based subscription model.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Literal
import json

VendorType = Literal["anthropic", "openai", "google"]
CategoryType = Literal["awesome", "issues", "feature-request"]


class VendorFeedbackManager:
    """Manages user feedback to AI vendors"""

    def __init__(self, global_deia_path: Optional[Path] = None):
        """
        Initialize vendor feedback manager

        Args:
            global_deia_path: Path to global DEIA installation (defaults to ~/.deia-global/)
        """
        if global_deia_path:
            self.global_path = Path(global_deia_path)
        else:
            self.global_path = Path.home() / ".deia-global"

        self.feedback_root = self.global_path / "vendor-feedback"
        self.access_control_file = self.feedback_root / ".access-control.json"

    def save_feedback(
        self,
        vendor: VendorType,
        category: CategoryType,
        description: str,
        conversation_log: str,
        metadata: Optional[dict] = None
    ) -> Path:
        """
        Save feedback for a vendor

        Args:
            vendor: Which AI vendor (anthropic/openai/google)
            category: awesome/issues/feature-request
            description: Brief description of feedback
            conversation_log: Full conversation transcript
            metadata: Additional context (model, tokens, etc.)

        Returns:
            Path to saved feedback file
        """
        # Create vendor/category directory
        category_dir = self.feedback_root / vendor / category
        category_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now()
        filename = timestamp.strftime("%Y%m%d-%H%M%S") + ".md"
        filepath = category_dir / filename

        # Build frontmatter
        frontmatter = {
            "vendor": vendor,
            "category": category,
            "description": description,
            "date": timestamp.isoformat(),
            "model": metadata.get("model") if metadata else "unknown",
            "tokens": metadata.get("tokens") if metadata else None,
        }

        # Create feedback content
        content = f"""---
vendor: {frontmatter['vendor']}
category: {frontmatter['category']}
description: {frontmatter['description']}
date: {frontmatter['date']}
model: {frontmatter.get('model', 'unknown')}
---

# Feedback for {vendor.capitalize()}

**Category:** {category}
**Description:** {description}
**Date:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}

---

## Conversation Log

{conversation_log}

---

*This feedback is available to {vendor.capitalize()} if user has granted access.*
*See ~/.deia-global/vendor-feedback/.access-control.json for permissions.*
"""

        # Write feedback file
        filepath.write_text(content, encoding='utf-8')

        return filepath

    def check_vendor_access(self, vendor: VendorType) -> bool:
        """
        Check if vendor has been granted access to feedback

        Args:
            vendor: Which vendor to check

        Returns:
            True if vendor has access, False otherwise
        """
        if not self.access_control_file.exists():
            return False

        try:
            with open(self.access_control_file, 'r', encoding='utf-8') as f:
                access_control = json.load(f)

            return access_control.get("subscribers", {}).get(vendor, {}).get("subscription_active", False)
        except (json.JSONDecodeError, IOError):
            return False

    def grant_vendor_access(self, vendor: VendorType, anonymize: bool = False) -> None:
        """
        Grant vendor access to your feedback

        Args:
            vendor: Which vendor to grant access
            anonymize: Whether to anonymize feedback before sharing
        """
        # Load or create access control
        if self.access_control_file.exists():
            with open(self.access_control_file, 'r', encoding='utf-8') as f:
                access_control = json.load(f)
        else:
            self.feedback_root.mkdir(parents=True, exist_ok=True)
            access_control = {
                "subscribers": {},
                "user_consent": {
                    "share_with_vendors": True,
                    "allowed_vendors": []
                }
            }

        # Add vendor subscription
        access_control["subscribers"][vendor] = {
            "access": "read-only",
            "allowed_paths": [f"{vendor}/*"],
            "subscription_active": True,
            "granted_date": datetime.now().isoformat(),
            "anonymize": anonymize
        }

        # Update allowed vendors
        if vendor not in access_control["user_consent"]["allowed_vendors"]:
            access_control["user_consent"]["allowed_vendors"].append(vendor)

        # Save access control
        with open(self.access_control_file, 'w', encoding='utf-8') as f:
            json.dump(access_control, f, indent=2)

    def revoke_vendor_access(self, vendor: VendorType) -> None:
        """
        Revoke vendor access to your feedback

        Args:
            vendor: Which vendor to revoke access from
        """
        if not self.access_control_file.exists():
            return

        with open(self.access_control_file, 'r', encoding='utf-8') as f:
            access_control = json.load(f)

        # Revoke subscription
        if vendor in access_control.get("subscribers", {}):
            access_control["subscribers"][vendor]["subscription_active"] = False
            access_control["subscribers"][vendor]["revoked_date"] = datetime.now().isoformat()

        # Remove from allowed vendors
        allowed = access_control.get("user_consent", {}).get("allowed_vendors", [])
        if vendor in allowed:
            allowed.remove(vendor)

        # Save access control
        with open(self.access_control_file, 'w', encoding='utf-8') as f:
            json.dump(access_control, f, indent=2)

    def list_feedback(self, vendor: Optional[VendorType] = None, category: Optional[CategoryType] = None) -> list[Path]:
        """
        List all feedback files, optionally filtered

        Args:
            vendor: Filter by vendor (None = all vendors)
            category: Filter by category (None = all categories)

        Returns:
            List of feedback file paths
        """
        if vendor and category:
            search_path = self.feedback_root / vendor / category
            pattern = "*.md"
        elif vendor:
            search_path = self.feedback_root / vendor
            pattern = "**/*.md"
        else:
            search_path = self.feedback_root
            pattern = "**/*.md"

        if not search_path.exists():
            return []

        return sorted(search_path.glob(pattern), reverse=True)

    def get_access_status(self) -> dict:
        """
        Get current access control status

        Returns:
            Dictionary with access control info
        """
        if not self.access_control_file.exists():
            return {
                "configured": False,
                "subscribers": {},
                "allowed_vendors": []
            }

        with open(self.access_control_file, 'r', encoding='utf-8') as f:
            access_control = json.load(f)

        return {
            "configured": True,
            "subscribers": access_control.get("subscribers", {}),
            "allowed_vendors": access_control.get("user_consent", {}).get("allowed_vendors", [])
        }


def quick_feedback(vendor: VendorType, category: CategoryType, description: str, conversation: str) -> Path:
    """
    Quick helper to save vendor feedback

    Args:
        vendor: anthropic/openai/google
        category: awesome/issues/feature-request
        description: Brief description
        conversation: Full conversation log

    Returns:
        Path to saved feedback file
    """
    manager = VendorFeedbackManager()
    return manager.save_feedback(vendor, category, description, conversation)


if __name__ == "__main__":
    # Example usage
    manager = VendorFeedbackManager()

    # Save feedback
    feedback_file = manager.save_feedback(
        vendor="anthropic",
        category="awesome",
        description="Claude perfectly refactored complex state management",
        conversation_log="[Full conversation would go here]",
        metadata={"model": "claude-sonnet-4", "tokens": 15000}
    )
    print(f"Saved feedback: {feedback_file}")

    # Grant access
    manager.grant_vendor_access("anthropic", anonymize=False)
    print("Granted Anthropic access to feedback")

    # Check status
    status = manager.get_access_status()
    print(f"Access status: {status}")
