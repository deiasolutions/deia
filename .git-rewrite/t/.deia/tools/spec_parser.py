#!/usr/bin/env python3
"""Spec Parser for LLH Factory

Parses LLH specification documents (YAML front matter + Markdown body)
and returns structured data for entity creation.

Usage:
    from spec_parser import SpecParser

    parser = SpecParser('path/to/spec.md')
    spec = parser.parse()

    for llh in spec['entities']['llhs']:
        print(f"LLH: {llh['id']} - {llh['title']}")
"""

from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


class SpecParseError(Exception):
    """Raised when spec parsing fails."""
    pass


class SpecParser:
    """Parser for LLH specification documents."""

    def __init__(self, spec_path: str | Path):
        """Initialize parser with spec file path.

        Args:
            spec_path: Path to spec.md file
        """
        self.spec_path = Path(spec_path).resolve()
        if not self.spec_path.exists():
            raise FileNotFoundError(f"Spec not found: {self.spec_path}")

        self.raw_content = ""
        self.front_matter = {}
        self.body = ""

    def parse(self) -> Dict[str, Any]:
        """Parse the spec document.

        Returns:
            Dict with keys:
                - meta: Metadata (project, author, created, etc.)
                - entities: Dict of entity lists (llhs, tags, drones)
                - routing: Routing configuration
                - build: Build options
                - body: Markdown body content

        Raises:
            SpecParseError: If parsing fails
        """
        self._read_file()
        self._parse_front_matter()
        self._validate_spec()

        return {
            'meta': self._extract_meta(),
            'entities': self._extract_entities(),
            'routing': self._extract_routing(),
            'build': self._extract_build_options(),
            'body': self.body.strip()
        }

    def _read_file(self):
        """Read spec file content."""
        try:
            self.raw_content = self.spec_path.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            raise SpecParseError(f"Failed to read spec: {e}")

    def _parse_front_matter(self):
        """Parse YAML front matter and body."""
        if not self.raw_content.startswith('---'):
            raise SpecParseError("Spec must start with YAML front matter (---)")

        parts = self.raw_content.split('\n', 1)
        if len(parts) < 2:
            raise SpecParseError("Invalid front matter structure")

        remainder = parts[1]
        if '\n---\n' not in remainder:
            raise SpecParseError("Front matter not properly closed (missing ---)")

        yaml_str, self.body = remainder.split('\n---\n', 1)

        # Simple YAML-like parser (handles our spec format)
        # For production, use PyYAML library
        self.front_matter = self._parse_yaml_simple(yaml_str)

    def _parse_yaml_simple(self, yaml_str: str) -> Dict[str, Any]:
        """Simple YAML parser for our spec format.

        Note: This is a simplified parser. For complex YAML, use PyYAML library.
        """
        result = {}
        current_dict = result
        stack = [(result, None)]
        indent_levels = {}

        for line_num, line in enumerate(yaml_str.splitlines(), 1):
            # Skip empty lines and comments
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # Calculate indent
            indent = len(line) - len(line.lstrip())

            # Handle key: value
            if ':' in line and not stripped.startswith('-'):
                key, _, value = stripped.partition(':')
                key = key.strip()
                value = value.strip()

                # Determine where to add this key
                while stack and indent <= indent_levels.get(id(stack[-1][0]), -1):
                    stack.pop()

                current_dict = stack[-1][0]

                if not value or value == '':
                    # Empty value means nested dict or list
                    new_dict = {}
                    current_dict[key] = new_dict
                    stack.append((new_dict, key))
                    indent_levels[id(new_dict)] = indent
                elif value.startswith('[') and value.endswith(']'):
                    # Inline list
                    items = [item.strip().strip('"\'') for item in value[1:-1].split(',') if item.strip()]
                    current_dict[key] = items
                elif value.lower() in ('true', 'false'):
                    # Boolean
                    current_dict[key] = value.lower() == 'true'
                elif value.lower() == 'null':
                    # Null
                    current_dict[key] = None
                elif value.startswith('"') or value.startswith("'"):
                    # Quoted string
                    current_dict[key] = value.strip('"\'')
                elif value.replace('.', '').replace('-', '').isdigit():
                    # Number
                    try:
                        current_dict[key] = int(value) if '.' not in value else float(value)
                    except ValueError:
                        current_dict[key] = value
                else:
                    # Plain string
                    current_dict[key] = value

            # Handle list items
            elif stripped.startswith('-'):
                item_str = stripped[1:].strip()

                # Determine parent dict
                while stack and indent <= indent_levels.get(id(stack[-1][0]), -1):
                    stack.pop()

                parent_dict, parent_key = stack[-1]

                # Ensure parent has a list
                if parent_key and not isinstance(parent_dict.get(parent_key), list):
                    parent_dict[parent_key] = []

                if ':' in item_str:
                    # Dict item
                    item_dict = {}
                    key, _, value = item_str.partition(':')
                    key = key.strip()
                    value = value.strip()

                    if value:
                        item_dict[key] = value.strip('"\'')
                    else:
                        item_dict = {key: {}}

                    if parent_key:
                        parent_dict[parent_key].append(item_dict)

                    # For multi-line dict items
                    stack.append((item_dict, None))
                    indent_levels[id(item_dict)] = indent
                else:
                    # Simple string item
                    if parent_key:
                        parent_dict[parent_key].append(item_str.strip('"\''))

        return result

    def _validate_spec(self):
        """Validate required fields are present."""
        # Support both eOS pack format (eos_version + pack_id) and legacy spec format (spec_version + project)
        has_eos_format = 'eos_version' in self.front_matter and 'pack_id' in self.front_matter
        has_spec_format = 'spec_version' in self.front_matter and 'project' in self.front_matter

        if not (has_eos_format or has_spec_format):
            raise SpecParseError("Missing required fields: need either (eos_version + pack_id) or (spec_version + project)")

        # Validate entities
        if 'entities' not in self.front_matter:
            raise SpecParseError("Missing required field: entities")

        entities = self.front_matter.get('entities', {})
        if not isinstance(entities, dict):
            raise SpecParseError("entities must be a dict")

        # Validate version
        version = self.front_matter.get('eos_version') or self.front_matter.get('spec_version')
        if version not in ['0.1']:
            raise SpecParseError(f"Unsupported version: {version}")

    def _extract_meta(self) -> Dict[str, Any]:
        """Extract metadata from front matter."""
        # Support both eOS pack and legacy spec formats
        version_key = 'eos_version' if 'eos_version' in self.front_matter else 'spec_version'
        project_key = 'pack_id' if 'pack_id' in self.front_matter else 'project'

        return {
            'spec_version': self.front_matter.get(version_key, '0.1'),
            'project': self.front_matter.get(project_key, 'unknown'),
            'author': self.front_matter.get('author', 'unknown'),
            'created': self.front_matter.get('created', datetime.now(timezone.utc).isoformat()),
            'status': self.front_matter.get('status', 'draft')
        }

    def _extract_entities(self) -> Dict[str, List[Dict[str, Any]]]:
        """Extract entity definitions."""
        entities = self.front_matter.get('entities', {})

        return {
            'llhs': entities.get('llhs', []),
            'tags': entities.get('tags', []),
            'drones': entities.get('drones', [])
        }

    def _extract_routing(self) -> Dict[str, str]:
        """Extract routing configuration."""
        routing = self.front_matter.get('routing', {})

        # Apply defaults if not specified
        project = self.front_matter.get('pack_id') or self.front_matter.get('project', 'unknown')
        defaults = {
            'llhs': f".deia/.projects/{project}_001/llhs/",
            'tags': f".deia/.projects/{project}_001/tag-teams/",
            'drones': f".deia/.projects/{project}_001/drones/"
        }

        return {**defaults, **routing}

    def _extract_build_options(self) -> Dict[str, bool]:
        """Extract build options."""
        build = self.front_matter.get('build', {})

        defaults = {
            'validate': True,
            'log_rse': True,
            'require_approval': True
        }

        return {**defaults, **build}

    def get_entity_count(self, spec: Dict[str, Any]) -> Dict[str, int]:
        """Get count of each entity type.

        Args:
            spec: Parsed spec dict

        Returns:
            Dict with entity type counts
        """
        entities = spec['entities']
        return {
            'llhs': len(entities['llhs']),
            'tags': len(entities['tags']),
            'drones': len(entities['drones']),
            'total': sum(len(v) for v in entities.values())
        }

    def validate_entity(self, entity: Dict[str, Any], entity_type: str) -> List[str]:
        """Validate a single entity definition.

        Args:
            entity: Entity dict
            entity_type: 'llh', 'tag', or 'drone'

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Required fields by type
        required_fields = {
            'llh': ['id', 'title'],
            'tag': ['id', 'title', 'parent'],
            'drone': ['id', 'title', 'type']
        }

        required = required_fields.get(entity_type, [])
        for field in required:
            if field not in entity or not entity[field]:
                errors.append(f"Missing required field: {field}")

        # Validate ID format (lowercase, hyphens only)
        if 'id' in entity:
            if not re.match(r'^[a-z0-9-]+$', entity['id']):
                errors.append(f"Invalid ID format: {entity['id']} (use lowercase + hyphens only)")

        return errors


def main(argv: List[str]) -> int:
    """CLI entry point."""
    if len(argv) < 2:
        print("Usage: spec_parser.py <spec.md>", file=sys.stderr)
        return 2

    spec_path = argv[1]

    try:
        parser = SpecParser(spec_path)
        spec = parser.parse()

        print(f"✓ Spec parsed successfully: {spec_path}")
        print(f"\nProject: {spec['meta']['project']}")
        print(f"Author: {spec['meta']['author']}")
        print(f"Status: {spec['meta']['status']}")

        counts = parser.get_entity_count(spec)
        print(f"\nEntities:")
        print(f"  LLHs: {counts['llhs']}")
        print(f"  TAGs: {counts['tags']}")
        print(f"  Drones: {counts['drones']}")
        print(f"  Total: {counts['total']}")

        print(f"\nRouting:")
        for entity_type, path in spec['routing'].items():
            print(f"  {entity_type}: {path}")

        # Validate entities
        all_valid = True
        for entity_type in ['llhs', 'tags', 'drones']:
            for entity in spec['entities'][entity_type]:
                errors = parser.validate_entity(entity, entity_type.rstrip('s'))
                if errors:
                    all_valid = False
                    print(f"\n✗ {entity_type.rstrip('s')} '{entity.get('id', 'unknown')}':")
                    for error in errors:
                        print(f"    - {error}")

        if all_valid and counts['total'] > 0:
            print("\n✓ All entities valid")

        return 0

    except (SpecParseError, FileNotFoundError) as e:
        print(f"✗ Parse error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
