"""
Book of Knowledge (BOK) management and search
"""

from pathlib import Path
from typing import List, Dict, Optional
import json


def search_bok(query: str, platform: Optional[str] = None,
               category: Optional[str] = None) -> List[Dict]:
    """
    Search the local BOK

    Args:
        query: Search terms
        platform: Filter by platform (optional)
        category: Filter by category (optional)

    Returns:
        List of matching BOK entries
    """

    from .core import find_project_root

    try:
        project_root = find_project_root()
        bok_path = project_root / 'devlogs' / 'bok'
    except FileNotFoundError:
        # Not in a project, check package data
        bok_path = Path(__file__).parent / 'data' / 'bok'

    if not bok_path.exists():
        return []

    results = []
    query_lower = query.lower()

    # Search through BOK files
    for entry_file in bok_path.glob('*.md'):
        content = entry_file.read_text(encoding='utf-8')

        # Simple search: check if query appears in content
        if query_lower in content.lower():
            # Extract metadata (if present)
            entry = _parse_bok_entry(content)
            entry['file'] = entry_file.name

            # Apply filters
            if platform and entry.get('platform') != platform:
                continue
            if category and entry.get('category') != category:
                continue

            results.append(entry)

    return results


def sync_bok() -> Dict[str, int]:
    """
    Sync BOK from community repository

    Returns:
        Statistics about sync (new, updated, total)
    """

    # TODO: Implement actual GitHub sync
    # For now, return mock stats

    return {
        'new': 0,
        'updated': 0,
        'total': 0
    }


def _parse_bok_entry(content: str) -> Dict:
    """Parse BOK entry metadata from markdown"""

    import yaml

    # Try to extract YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1])
                return metadata
            except:
                pass

    # Fallback: extract from content
    lines = content.split('\n')

    entry = {
        'title': 'Untitled',
        'description': '',
        'platform': 'unknown',
        'category': 'unknown'
    }

    # First heading is title
    for line in lines:
        if line.startswith('# '):
            entry['title'] = line[2:].strip()
            break

    # First paragraph is description
    in_paragraph = False
    description_lines = []
    for line in lines:
        if line.strip() and not line.startswith('#'):
            in_paragraph = True
            description_lines.append(line.strip())
        elif in_paragraph and not line.strip():
            break

    entry['description'] = ' '.join(description_lines)[:200] + '...'

    return entry
