"""DEIA Context Loader"""

import os
import re
import logging
from pathlib import Path
from typing import List, Dict

import yaml

logger = logging.getLogger(__name__)

class DEIAContextLoader:
    """Loads and manages DEIA project context"""

    def __init__(self, project_root: str = "."):
        """Initialize with project root directory"""
        self.project_root = Path(project_root)
        self.index_file = self.project_root / ".deia" / "index" / "master-index.yaml"
        self.bok_dir = self.project_root / "bok"
        self.session_dir = self.project_root / ".deia" / "sessions"
        self.index_data = self._load_yaml(self.index_file)

    @staticmethod
    def _load_yaml(file_path: Path) -> Dict:
        """Load YAML file and return data as dictionary"""
        if not file_path.exists():
            return {}
        try:
            with file_path.open("r", encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data if data is not None else {}
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML file {file_path}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            return {}

    def load_bok_index(self) -> Dict:
        """Load .deia/index/master-index.yaml"""
        return self.index_data

    def search_bok(self, query: str, top_n: int = 10) -> List[Dict]:
        """Search BOK patterns by keyword"""
        query_lower = query.lower()
        results = []
        for pattern_id, pattern_data in self.index_data.get("patterns", {}).items():
            if (
                query_lower in pattern_data.get("title", "").lower()
                or query_lower in pattern_data.get("keywords", "").lower()
            ):
                results.append({"id": pattern_id, **pattern_data})
        return sorted(results, key=lambda x: x.get("score", 0), reverse=True)[:top_n]

    def get_pattern(self, pattern_id: str) -> str:
        """Read specific BOK pattern content

        Args:
            pattern_id: Pattern identifier (alphanumeric, hyphens, underscores only)

        Returns:
            Pattern content as string, empty string if not found or invalid

        Raises:
            ValueError: If pattern_id contains invalid characters (path traversal attempt)
        """
        # SECURITY FIX: Validate pattern_id to prevent path traversal
        if not re.match(r'^[a-zA-Z0-9_-]+$', pattern_id):
            logger.warning(f"Invalid pattern_id rejected: {pattern_id}")
            raise ValueError(f"Invalid pattern_id: {pattern_id}. Only alphanumeric, hyphens, and underscores allowed.")

        pattern_file = self.bok_dir / f"{pattern_id}.md"

        # SECURITY FIX: Verify resolved path is still within bok_dir (defense in depth)
        try:
            resolved_file = pattern_file.resolve()
            resolved_bok = self.bok_dir.resolve()

            # Check if resolved file path starts with bok directory path
            if not str(resolved_file).startswith(str(resolved_bok)):
                logger.warning(f"Path traversal attempt detected: {pattern_id}")
                raise ValueError(f"Path traversal attempt detected for pattern_id: {pattern_id}")
        except Exception as e:
            logger.error(f"Error resolving path for pattern {pattern_id}: {e}")
            return ""

        if not pattern_file.exists():
            return ""

        try:
            with pattern_file.open("r", encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading pattern file {pattern_file}: {e}")
            return ""

    def get_recent_sessions(self, limit: int = 5) -> List[Dict]:
        """Get recent session logs"""
        sessions = []

        if not self.session_dir.exists():
            return sessions

        try:
            for session_file in sorted(self.session_dir.glob("*.yaml"), reverse=True):
                session_data = self._load_yaml(session_file)
                if session_data:  # Only add non-empty sessions
                    sessions.append(session_data)
                if len(sessions) >= limit:
                    break
        except Exception as e:
            logger.error(f"Error reading session files: {e}")

        return sessions

    def get_project_structure(self) -> Dict:
        """Map .deia directory structure"""
        structure = {}
        try:
            for root, dirs, files in os.walk(self.project_root):
                root_path = Path(root)
                if root_path == self.project_root:
                    structure["."] = [d for d in dirs if d != ".deia"]
                else:
                    rel_path = root_path.relative_to(self.project_root)
                    structure[str(rel_path)] = files
        except Exception as e:
            logger.error(f"Error walking project structure: {e}")

        return structure

    def is_deia_project(self) -> bool:
        """Check if current directory is DEIA project"""
        return (self.project_root / ".deia").exists()
