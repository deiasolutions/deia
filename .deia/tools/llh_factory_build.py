#!/usr/bin/env python3
"""LLH Factory Builder

Builds LLH organizational structures from eOS packs.

Usage:
    python llh_factory_build.py --eos-pack path/to/pack.yaml [options]
    python llh_factory_build.py --spec path/to/spec.md [options]  # Legacy

Options:
    --eos-pack PATH      Path to eOS pack YAML file (recommended)
    --spec PATH          Path to spec.md file (legacy, same as --eos-pack)
    --llh-template PATH  Custom LLH template (default: .deia/templates/llh/minimal-llh.md)
    --tag-template PATH  Custom TAG template (default: .deia/templates/tag/minimal-tag.md)
    --drone-template PATH Custom drone template
    --force              Skip approval prompts
    --dry-run            Parse and validate but don't create files
    --quiet              Minimal output

Examples:
    # Build from eOS pack
    python llh_factory_build.py --eos-pack .deia/eos-packs/my-org.yaml

    # Dry run to validate
    python llh_factory_build.py --eos-pack pack.yaml --dry-run

    # Custom templates
    python llh_factory_build.py --eos-pack pack.yaml --llh-template custom-llh.md
"""

from __future__ import annotations
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Import spec parser
sys.path.insert(0, str(Path(__file__).parent))
from spec_parser import SpecParser, SpecParseError


def iso_now() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def emit_rse(event: Dict[str, Any]):
    """Emit RSE event to telemetry."""
    sink = Path('.deia/telemetry/rse.jsonl')
    sink.parent.mkdir(parents=True, exist_ok=True)
    with sink.open('a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + '\n')


def find_template(entity_type: str, custom_path: Optional[str] = None) -> Path:
    """Find template file for entity type.

    Args:
        entity_type: 'llh', 'tag', or 'drone'
        custom_path: Optional custom template path

    Returns:
        Path to template file

    Raises:
        FileNotFoundError: If template not found
    """
    if custom_path:
        template = Path(custom_path)
        if template.exists():
            return template
        raise FileNotFoundError(f"Custom template not found: {custom_path}")

    # Try .deia/templates first, then templates/
    candidates = {
        'llh': ['.deia/templates/llh/minimal-llh.md', 'templates/llh/LLH-TEMPLATE.md'],
        'tag': ['.deia/templates/tag/minimal-tag.md', 'templates/tag/TAG-TEMPLATE.md'],
        'drone': ['.deia/templates/drone/minimal-drone.md']
    }

    for candidate_path in candidates.get(entity_type, []):
        template = Path(candidate_path)
        if template.exists():
            return template

    raise FileNotFoundError(f"No template found for {entity_type}")


def render_template(template_path: Path, variables: Dict[str, Any]) -> str:
    """Render template with variables.

    Args:
        template_path: Path to template file
        variables: Dict of variable substitutions

    Returns:
        Rendered template content
    """
    content = template_path.read_text(encoding='utf-8')

    # Apply variable substitutions
    for key, value in variables.items():
        placeholder = f"{{{{{key}}}}}"
        # Handle lists/dicts by converting to string
        if isinstance(value, (list, dict)):
            value = json.dumps(value)
        elif value is None:
            value = "null"
        elif isinstance(value, bool):
            value = str(value).lower()
        else:
            value = str(value)

        content = content.replace(placeholder, value)

    return content


def build_llh(entity: Dict[str, Any], template_path: Path, output_dir: Path, dry_run: bool = False) -> Optional[Path]:
    """Build LLH entity from spec.

    Args:
        entity: LLH entity dict from spec
        template_path: Path to LLH template
        output_dir: Output directory
        dry_run: If True, don't create files

    Returns:
        Path to created file, or None if dry-run
    """
    entity_id = entity['id']
    output_file = output_dir / f"{entity_id}.md"

    if output_file.exists():
        raise FileExistsError(f"LLH already exists: {output_file} (use --force to overwrite)")

    # Prepare template variables
    variables = {
        'ID': entity_id,
        'TITLE': entity.get('title', entity_id.replace('-', ' ').title()),
        'DATE': iso_now(),
        'ACTOR': 'llh-factory-builder',
        'ENTITY_TYPE': 'llh',
        'NAME': entity.get('title', ''),
        'STRUCTURE': entity.get('structure', 'flat'),
        'MEMBERS': entity.get('members', []),
        'PARENT': entity.get('parent', 'null'),
        'CAPABILITIES': entity.get('caps', []),
        'GOVERNANCE_STRUCTURE': entity.get('governance', {}).get('structure', 'flat'),
        'DECISION_MODE': entity.get('governance', {}).get('decision_mode', 'consensus'),
        'TRANSPARENCY': entity.get('governance', {}).get('transparency', 'members-only'),
        'BUDGET_LEVEL': entity.get('capacities', {}).get('budget', 'medium'),
        'ATTENTION_LEVEL': entity.get('capacities', {}).get('attention', 'medium'),
        'STAFF_LEVEL': entity.get('capacities', {}).get('staff_cycles', 'medium'),
        'CONSTRAINTS': entity.get('constraints', []),
    }

    content = render_template(template_path, variables)

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content, encoding='utf-8')
        return output_file

    return None


def build_tag(entity: Dict[str, Any], template_path: Path, output_dir: Path, dry_run: bool = False) -> Optional[Path]:
    """Build TAG entity from spec."""
    entity_id = entity['id']
    output_file = output_dir / f"{entity_id}.md"

    if output_file.exists():
        raise FileExistsError(f"TAG already exists: {output_file}")

    variables = {
        'ID': entity_id,
        'TITLE': entity.get('title', entity_id.replace('-', ' ').title()),
        'DATE': iso_now(),
        'ACTOR': 'llh-factory-builder',
        'ENTITY_TYPE': 'tag',
        'NAME': entity.get('title', ''),
        'PARENT': entity.get('parent', ''),
        'DEADLINE': entity.get('deadline', 'null'),
        'MEMBERS': entity.get('members', []),
        'TAG_CAPABILITIES': entity.get('caps', []),
        'OBJECTIVES': entity.get('objectives', ''),
    }

    content = render_template(template_path, variables)

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content, encoding='utf-8')
        return output_file

    return None


def build_drone(entity: Dict[str, Any], template_path: Path, output_dir: Path, dry_run: bool = False) -> Optional[Path]:
    """Build drone entity from spec."""
    entity_id = entity['id']
    output_file = output_dir / f"{entity_id}.md"

    if output_file.exists():
        raise FileExistsError(f"Drone already exists: {output_file}")

    variables = {
        'ID': entity_id,
        'TITLE': entity.get('title', entity_id.replace('-', ' ').title()),
        'DATE': iso_now(),
        'ACTOR': 'llh-factory-builder',
        'ENTITY_TYPE': 'drone',
        'NAME': entity.get('title', ''),
        'DRONE_TYPE': entity.get('type', 'processor'),
        'PARENT': entity.get('parent', ''),
        'TRIGGER_CONDITIONS': entity.get('triggers', []),
        'DRONE_ACTIONS': entity.get('actions', []),
    }

    content = render_template(template_path, variables)

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content, encoding='utf-8')
        return output_file

    return None


def main(argv: List[str]) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Build LLH structures from specification documents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('--eos-pack', help='Path to eOS pack YAML file')
    parser.add_argument('--spec', help='Path to spec file (legacy, same as --eos-pack)')
    parser.add_argument('--llh-template', help='Custom LLH template')
    parser.add_argument('--tag-template', help='Custom TAG template')
    parser.add_argument('--drone-template', help='Custom drone template')
    parser.add_argument('--force', action='store_true', help='Skip approval prompts')
    parser.add_argument('--dry-run', action='store_true', help='Validate but don\'t create files')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')

    args = parser.parse_args(argv[1:])

    # Accept either --eos-pack or --spec (legacy)
    pack_path = args.eos_pack or args.spec
    if not pack_path:
        parser.error("either --eos-pack or --spec is required")

    try:
        # Parse eOS pack
        if not args.quiet:
            print(f"Parsing eOS pack: {pack_path}")

        spec_parser = SpecParser(pack_path)
        spec = spec_parser.parse()

        counts = spec_parser.get_entity_count(spec)

        if not args.quiet:
            print(f"✓ eOS pack parsed successfully")
            print(f"  Project: {spec['meta']['project']}")
            print(f"  Entities: {counts['total']} ({counts['llhs']} LLHs, {counts['tags']} TAGs, {counts['drones']} drones)")

        # Validate entities
        errors = []
        for entity_type in ['llhs', 'tags', 'drones']:
            for entity in spec['entities'][entity_type]:
                entity_errors = spec_parser.validate_entity(entity, entity_type.rstrip('s'))
                if entity_errors:
                    errors.extend([f"{entity_type.rstrip('s')} '{entity.get('id')}': {err}" for err in entity_errors])

        if errors:
            print("✗ Validation errors:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            return 1

        if not args.quiet:
            print("✓ All entities valid")

        # Check if any entities to build
        if counts['total'] == 0:
            print("No entities to build", file=sys.stderr)
            return 0

        # Get approval unless --force or --dry-run
        if not args.force and not args.dry_run and spec['build'].get('require_approval', True):
            print(f"\nReady to build {counts['total']} entities")
            print(f"Target directories:")
            for entity_type, path in spec['routing'].items():
                count = counts.get(entity_type, 0)
                if count > 0:
                    print(f"  {entity_type}: {path} ({count} files)")

            response = input("\nProceed? (yes/no): ").strip().lower()
            if response != 'yes':
                print("Aborted by user")
                emit_rse({
                    'ts': iso_now(),
                    'type': 'factory_build',
                    'lane': 'Process',
                    'actor': 'llh-factory-builder',
                    'data': {'status': 'denied', 'eos_pack': str(pack_path)}
                })
                return 2

        # Emit approval RSE
        if not args.dry_run:
            emit_rse({
                'ts': iso_now(),
                'type': 'factory_build',
                'lane': 'Process',
                'actor': 'llh-factory-builder',
                'data': {'status': 'approved', 'eos_pack': str(pack_path), 'entity_count': counts['total']}
            })

        # Build entities
        created_files = []

        # Build LLHs
        if counts['llhs'] > 0:
            template = find_template('llh', args.llh_template)
            output_dir = Path(spec['routing']['llhs'])

            for llh in spec['entities']['llhs']:
                try:
                    output_file = build_llh(llh, template, output_dir, args.dry_run)
                    if output_file:
                        created_files.append(output_file)
                        if not args.quiet:
                            print(f"  ✓ Created LLH: {output_file}")
                    elif not args.quiet:
                        print(f"  [dry-run] LLH: {llh['id']}")
                except Exception as e:
                    print(f"  ✗ Failed to create LLH '{llh['id']}': {e}", file=sys.stderr)
                    return 1

        # Build TAGs
        if counts['tags'] > 0:
            template = find_template('tag', args.tag_template)
            output_dir = Path(spec['routing']['tags'])

            for tag in spec['entities']['tags']:
                try:
                    output_file = build_tag(tag, template, output_dir, args.dry_run)
                    if output_file:
                        created_files.append(output_file)
                        if not args.quiet:
                            print(f"  ✓ Created TAG: {output_file}")
                    elif not args.quiet:
                        print(f"  [dry-run] TAG: {tag['id']}")
                except Exception as e:
                    print(f"  ✗ Failed to create TAG '{tag['id']}': {e}", file=sys.stderr)
                    return 1

        # Build drones
        if counts['drones'] > 0:
            try:
                template = find_template('drone', args.drone_template)
                output_dir = Path(spec['routing']['drones'])

                for drone in spec['entities']['drones']:
                    try:
                        output_file = build_drone(drone, template, output_dir, args.dry_run)
                        if output_file:
                            created_files.append(output_file)
                            if not args.quiet:
                                print(f"  ✓ Created drone: {output_file}")
                        elif not args.quiet:
                            print(f"  [dry-run] Drone: {drone['id']}")
                    except Exception as e:
                        print(f"  ✗ Failed to create drone '{drone['id']}': {e}", file=sys.stderr)
                        return 1
            except FileNotFoundError as e:
                if not args.quiet:
                    print(f"  ! Skipping drones (no template): {e}")

        # Validate created files
        if created_files and spec['build'].get('validate', True):
            if not args.quiet:
                print(f"\nValidating {len(created_files)} files...")

            validator = Path('.deia/tools/llh_validate.py')
            if validator.exists():
                import subprocess
                result = subprocess.run(
                    ['python', str(validator)] + [str(f) for f in created_files],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    if not args.quiet:
                        print("✓ All files validated")
                else:
                    print("✗ Validation failed:", file=sys.stderr)
                    print(result.stdout, file=sys.stderr)
                    print(result.stderr, file=sys.stderr)
                    return 1

        # Emit completion RSE
        if not args.dry_run and spec['build'].get('log_rse', True):
            emit_rse({
                'ts': iso_now(),
                'type': 'factory_build_complete',
                'lane': 'Process',
                'actor': 'llh-factory-builder',
                'data': {
                    'eos_pack': str(pack_path),
                    'files_created': len(created_files),
                    'llhs': counts['llhs'],
                    'tags': counts['tags'],
                    'drones': counts['drones']
                }
            })

        # Summary
        if not args.quiet:
            if args.dry_run:
                print(f"\n✓ Dry run complete - would create {counts['total']} entities")
            else:
                print(f"\n✓ Build complete - created {len(created_files)} files")
                print(f"\nNext steps:")
                print(f"  1. Review created files")
                print(f"  2. Commit to git: git add {spec['routing']['llhs']}")
                print(f"  3. Check RSE log: .deia/telemetry/rse.jsonl")

        return 0

    except (SpecParseError, FileNotFoundError) as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
