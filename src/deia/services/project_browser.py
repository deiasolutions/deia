"""
Project Browser API for DEIA Chat Interface Phase 2

Provides tree view, filtering, and search capabilities for .deia project structure.
Designed for safe web interface integration with JSON serialization.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set


class ProjectBrowser:
    """Generate tree views and browse DEIA project structure"""

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize Project Browser

        Args:
            project_root: Root directory of DEIA project. If None, searches upward for .deia/
        """
        if project_root is None:
            project_root = self._find_project_root()

        self.project_root = Path(project_root).resolve()
        self.deia_dir = self.project_root / ".deia"

        if not self.deia_dir.exists():
            raise ValueError(f"Not a DEIA project: .deia/ not found in {self.project_root}")

    @staticmethod
    def _find_project_root() -> Path:
        """Find project root by searching upward for .deia/ directory"""
        current = Path.cwd()

        # Search up to 10 levels
        for _ in range(10):
            if (current / ".deia").exists():
                return current

            parent = current.parent
            if parent == current:  # Reached filesystem root
                break
            current = parent

        raise ValueError("Could not find DEIA project root (.deia/ directory not found)")

    def get_tree(
        self,
        path: Optional[str] = None,
        max_depth: int = 5,
        show_hidden: bool = False
    ) -> Dict:
        """
        Generate tree view of project structure

        Args:
            path: Relative path from project root (None = entire project)
            max_depth: Maximum directory depth to traverse
            show_hidden: Include hidden files/directories (starting with .)

        Returns:
            Tree structure as nested dict with metadata
        """
        if path:
            start_path = self.project_root / path
        else:
            start_path = self.project_root

        if not start_path.exists():
            raise ValueError(f"Path does not exist: {path}")

        if not start_path.is_relative_to(self.project_root):
            raise ValueError(f"Path outside project boundary: {path}")

        return self._build_tree_node(start_path, max_depth, show_hidden, current_depth=0)

    def _build_tree_node(
        self,
        path: Path,
        max_depth: int,
        show_hidden: bool,
        current_depth: int
    ) -> Dict:
        """Recursively build tree node"""
        node = {
            "name": path.name if path != self.project_root else self.project_root.name,
            "path": str(path.relative_to(self.project_root)),
            "type": "directory" if path.is_dir() else "file",
        }

        # Add file metadata
        if path.is_file():
            node["size"] = path.stat().st_size
            node["extension"] = path.suffix

        # Recurse into directories
        if path.is_dir() and current_depth < max_depth:
            children = []
            try:
                for child in sorted(path.iterdir()):
                    # Skip hidden unless requested
                    if not show_hidden and child.name.startswith(".") and child.name != ".deia":
                        continue

                    # Always include .deia at root level
                    if child == self.deia_dir:
                        children.append(self._build_tree_node(child, max_depth, show_hidden, current_depth + 1))
                    elif child.is_relative_to(self.deia_dir) or child.parent == self.project_root:
                        children.append(self._build_tree_node(child, max_depth, show_hidden, current_depth + 1))

            except PermissionError:
                node["error"] = "permission_denied"

            if children:
                node["children"] = children
                node["child_count"] = len(children)

        return node

    def filter_by_extension(self, extensions: List[str], path: Optional[str] = None) -> List[Dict]:
        """
        Find all files with specified extensions

        Args:
            extensions: List of extensions to match (e.g., ['.md', '.py'])
            path: Relative path to search within (None = entire project)

        Returns:
            List of file metadata dicts
        """
        if path:
            search_path = self.project_root / path
        else:
            search_path = self.project_root

        if not search_path.exists():
            raise ValueError(f"Path does not exist: {path}")

        results = []
        extensions_set = set(ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions)

        for file_path in search_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in extensions_set:
                results.append(self._file_metadata(file_path))

        return sorted(results, key=lambda x: x["path"])

    def search(self, query: str, file_types: Optional[List[str]] = None) -> List[Dict]:
        """
        Search for files/directories by name

        Args:
            query: Search string (case-insensitive, partial match)
            file_types: Optional list of extensions to limit search

        Returns:
            List of matching items with metadata
        """
        results = []
        query_lower = query.lower()

        for item_path in self.project_root.rglob("*"):
            # Check if name matches query
            if query_lower in item_path.name.lower():
                # If file_types specified, only include matching files
                if file_types:
                    if item_path.is_file() and item_path.suffix.lower() in file_types:
                        results.append(self._file_metadata(item_path))
                else:
                    # Include both files and directories
                    if item_path.is_file():
                        results.append(self._file_metadata(item_path))
                    elif item_path.is_dir():
                        results.append({
                            "name": item_path.name,
                            "path": str(item_path.relative_to(self.project_root)),
                            "type": "directory"
                        })

        return sorted(results, key=lambda x: x["path"])

    def _file_metadata(self, path: Path) -> Dict:
        """Extract file metadata"""
        return {
            "name": path.name,
            "path": str(path.relative_to(self.project_root)),
            "type": "file",
            "size": path.stat().st_size,
            "extension": path.suffix,
            "modified": path.stat().st_mtime
        }

    def get_deia_structure(self) -> Dict:
        """
        Get standardized .deia/ directory structure with status

        Returns:
            Dict with directory status and contents
        """
        structure = {
            "root": str(self.project_root),
            "valid": True,
            "directories": {}
        }

        expected_dirs = {
            "bot-logs": "Agent activity logs",
            "federalist": "Federalist Papers governance documents",
            "governance": "Governance documents and protocols",
            "intake": "Incoming files from external agents",
            "observations": "Observations and reports",
            "tunnel": "Agent-to-agent coordination messages",
            "index": "Master index and taxonomy",
        }

        for dir_name, description in expected_dirs.items():
            dir_path = self.deia_dir / dir_name
            structure["directories"][dir_name] = {
                "exists": dir_path.exists(),
                "description": description,
                "path": str(dir_path.relative_to(self.project_root))
            }

            if dir_path.exists():
                structure["directories"][dir_name]["file_count"] = len(list(dir_path.rglob("*")))

        return structure

    def to_json(self, obj: any, indent: int = 2) -> str:
        """
        Serialize to JSON string

        Args:
            obj: Object to serialize (typically result from get_tree(), search(), etc.)
            indent: JSON indentation level

        Returns:
            JSON string
        """
        return json.dumps(obj, indent=indent, default=str)

    def get_stats(self) -> Dict:
        """
        Get project statistics

        Returns:
            Dict with file counts, sizes, and types
        """
        stats = {
            "total_files": 0,
            "total_size": 0,
            "by_extension": {},
            "by_directory": {}
        }

        for item in self.project_root.rglob("*"):
            if item.is_file():
                stats["total_files"] += 1
                size = item.stat().st_size
                stats["total_size"] += size

                # By extension
                ext = item.suffix or "(no extension)"
                if ext not in stats["by_extension"]:
                    stats["by_extension"][ext] = {"count": 0, "size": 0}
                stats["by_extension"][ext]["count"] += 1
                stats["by_extension"][ext]["size"] += size

                # By top-level directory
                try:
                    rel_path = item.relative_to(self.project_root)
                    top_dir = str(rel_path.parts[0]) if rel_path.parts else "root"
                    if top_dir not in stats["by_directory"]:
                        stats["by_directory"][top_dir] = {"count": 0, "size": 0}
                    stats["by_directory"][top_dir]["count"] += 1
                    stats["by_directory"][top_dir]["size"] += size
                except ValueError:
                    pass

        return stats
