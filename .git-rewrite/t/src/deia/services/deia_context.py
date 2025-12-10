"""
Load and cache DEIA project context.

Automatically loads project metadata, governance, and BOK context.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass
class DeiaMeta:
    """DEIA project metadata."""

    project_name: str
    project_path: str
    phase: Optional[str] = None
    team_members: List[str] = field(default_factory=list)
    current_sprint: Optional[str] = None
    created_date: Optional[str] = None
    last_updated: Optional[str] = None


@dataclass
class DeiaBokIndex:
    """BOK index metadata."""

    total_patterns: int = 0
    categories: List[str] = field(default_factory=list)
    recent_patterns: List[str] = field(default_factory=list)


@dataclass
class DeiaContext:
    """Complete DEIA context for a project."""

    metadata: DeiaMeta
    bok_index: DeiaBokIndex
    recent_observations: List[str] = field(default_factory=list)
    governance_summary: Optional[str] = None
    _raw_data: Dict[str, Any] = field(default_factory=dict, repr=False)


class DeiaContextLoader:
    """Load and cache DEIA project context."""

    CONTEXT_CACHE_SIZE = 32

    @staticmethod
    @lru_cache(maxsize=CONTEXT_CACHE_SIZE)
    def load_project_context(project_path: str) -> Optional[DeiaContext]:
        """
        Load complete context for a DEIA project.

        Args:
            project_path: Path to project root (should contain .deia/)

        Returns:
            DeiaContext or None if not a valid DEIA project
        """
        deia_dir = Path(project_path) / ".deia"

        if not deia_dir.exists():
            return None

        # Load metadata
        metadata = DeiaContextLoader._load_metadata(project_path)
        if not metadata:
            return None

        # Load BOK index
        bok_index = DeiaContextLoader._load_bok_index(deia_dir)

        # Load observations
        observations = DeiaContextLoader._load_observations(deia_dir)

        # Load governance summary
        governance = DeiaContextLoader._load_governance_summary(deia_dir)

        context = DeiaContext(
            metadata=metadata,
            bok_index=bok_index,
            recent_observations=observations,
            governance_summary=governance,
        )

        return context

    @staticmethod
    def _load_metadata(project_path: str) -> Optional[DeiaMeta]:
        """Load project metadata from README or .deia/metadata."""
        project_path = Path(project_path)

        # Try .deia/metadata.json first
        metadata_file = project_path / ".deia" / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, "r") as f:
                    data = json.load(f)
                    return DeiaMeta(
                        project_name=data.get("project_name", project_path.name),
                        project_path=str(project_path),
                        phase=data.get("phase"),
                        team_members=data.get("team_members", []),
                        current_sprint=data.get("current_sprint"),
                        created_date=data.get("created_date"),
                        last_updated=data.get("last_updated"),
                    )
            except Exception:
                pass

        # Fallback: extract from README
        readme_file = project_path / "README.md"
        if readme_file.exists():
            return DeiaMeta(
                project_name=project_path.name,
                project_path=str(project_path),
            )

        return None

    @staticmethod
    def _load_bok_index(deia_dir: Path) -> DeiaBokIndex:
        """Load BOK index information."""
        index_file = deia_dir / "index" / "master-index.yaml"

        if not index_file.exists():
            return DeiaBokIndex()

        try:
            with open(index_file, "r") as f:
                data = yaml.safe_load(f) or {}

                patterns = data.get("patterns", [])
                categories = list(set([p.get("category", "uncategorized") for p in patterns]))

                return DeiaBokIndex(
                    total_patterns=len(patterns),
                    categories=sorted(categories),
                    recent_patterns=[p.get("id") for p in patterns[:5]],
                )
        except Exception:
            return DeiaBokIndex()

    @staticmethod
    def _load_observations(deia_dir: Path) -> List[str]:
        """Load recent observations/lessons learned."""
        observations_dir = deia_dir / "observations"

        if not observations_dir.exists():
            return []

        observations = []
        for obs_file in sorted(observations_dir.glob("*.md"))[-5:]:  # Last 5
            try:
                observations.append(obs_file.stem)
            except Exception:
                pass

        return observations

    @staticmethod
    def _load_governance_summary(deia_dir: Path) -> Optional[str]:
        """Load governance/constitution summary."""
        gov_file = deia_dir / "governance" / "CONSTITUTION.md"

        if gov_file.exists():
            try:
                with open(gov_file, "r") as f:
                    content = f.read()
                    # Return first 200 words as summary
                    words = content.split()[:200]
                    return " ".join(words) + "..."
            except Exception:
                pass

        return None

    @staticmethod
    def clear_cache():
        """Clear context cache."""
        DeiaContextLoader.load_project_context.cache_clear()

    @staticmethod
    def get_cache_info() -> Dict[str, int]:
        """Get cache statistics."""
        info = DeiaContextLoader.load_project_context.cache_info()
        return {
            "hits": info.hits,
            "misses": info.misses,
            "maxsize": info.maxsize,
            "currsize": info.currsize,
        }
