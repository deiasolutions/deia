---
eos: "0.1"
kind: egg
id: llh-factory
entity_type: factory
name: "LLH Factory Egg (Self-Contained)"
proposed_by: claude
created: 2025-10-15
status: template
policy:
  rotg: true
  dnd: true
caps: [parse_dna, build_hierarchy, create_entities, validate_outputs, log_operations]
routing:
  project: "{{PROJECT_ID}}"
  destination: eggs
  filename: llh-factory.md
  action: expand_and_execute
hatch_date: null
version: 0.2.0
notes: "Self-contained factory egg with embedded builder logic"
---

# LLH Factory Egg (Self-Contained)

## Purpose

This egg contains **all the code needed** to create LLH organizational structures from DNA packs. Everything is self-contained within this egg.

## Concept

**Egg = Recipe (this file)**
- Contains all builder logic
- Reads DNA pack (separate YAML file)
- Creates entities
- Validates outputs
- Logs operations

**DNA Pack = Blueprint (separate file)**
- `.deia/dna/<dna-pack-id>.yaml`
- Lists entities to create
- Defines structure
- NO executable code

## Usage

### Step 1: Create DNA Pack

Create `.deia/dna/my-org.yaml`:

```yaml
dna_version: "0.1"
pack_id: my-org
author: dave
created: 2025-10-15

entities:
  llhs:
    - id: leadership-llh
      title: "Leadership Team"
      structure: executive

    - id: engineering-llh
      title: "Engineering"
      parent: leadership-llh

  tags:
    - id: q4-launch-tag
      title: "Q4 Launch"
      parent: engineering-llh
      deadline: "2025-12-31"

routing:
  output_dir: ".deia/.projects/my-org_001"
```

### Step 2: Expand This Egg

```bash
python .deia/tools/egg_expand.py \
  .deia/templates/egg/llh-factory-egg-self-contained.md
```

Creates: `.deia/.projects/llh-factory_001/egg.md`

### Step 3: Execute Egg with DNA

```bash
cd .deia/.projects/llh-factory_001/

# Extract and run builder code from egg
python -c "
import sys
sys.path.insert(0, '.')
exec(open('egg.md').read().split('```python')[1].split('```')[0])
builder = LLHFactoryBuilder('../../dna/my-org.yaml')
builder.build()
"
```

Or use helper script (extracted from egg):

```bash
./build_from_dna.sh ../../dna/my-org.yaml
```

## Embedded Builder Code

The following Python code is the complete factory builder. It's extracted and executed when you hatch this egg.

```python
#!/usr/bin/env python3
"""
LLH Factory Builder - Embedded in Egg
This code is self-contained and executes from the egg itself.
"""

import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional


class LLHFactoryBuilder:
    """Self-contained LLH factory builder embedded in egg."""

    def __init__(self, dna_pack_path: str):
        """Initialize with DNA pack path."""
        self.dna_path = Path(dna_pack_path)
        self.dna = {}
        self.templates = {}
        self.created_files = []

    def build(self):
        """Main build process."""
        print(f"🥚 LLH Factory Egg - Building from DNA pack")
        print(f"   DNA: {self.dna_path}")

        # Step 1: Load DNA pack
        self._load_dna()

        # Step 2: Load templates
        self._load_templates()

        # Step 3: Validate DNA
        self._validate_dna()

        # Step 4: Get approval
        if not self._get_approval():
            print("❌ Build cancelled by user")
            return False

        # Step 5: Create entities
        self._create_entities()

        # Step 6: Validate outputs
        self._validate_outputs()

        # Step 7: Log to RSE
        self._log_rse()

        print(f"\n✅ Build complete - created {len(self.created_files)} files")
        return True

    def _load_dna(self):
        """Load and parse DNA pack."""
        if not self.dna_path.exists():
            raise FileNotFoundError(f"DNA pack not found: {self.dna_path}")

        print(f"📖 Loading DNA pack...")
        content = self.dna_path.read_text(encoding='utf-8')

        # Simple YAML parser (subset)
        self.dna = self._parse_yaml(content)

        entities = self.dna.get('entities', {})
        llh_count = len(entities.get('llhs', []))
        tag_count = len(entities.get('tags', []))
        total = llh_count + tag_count

        print(f"   ✓ Pack ID: {self.dna.get('pack_id')}")
        print(f"   ✓ Entities: {total} ({llh_count} LLHs, {tag_count} TAGs)")

    def _parse_yaml(self, content: str) -> Dict[str, Any]:
        """Simple YAML parser for DNA packs."""
        result = {}
        lines = content.splitlines()
        current_dict = result
        stack = [(result, None, -1)]

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            indent = len(line) - len(line.lstrip())

            # Pop stack if dedented
            while len(stack) > 1 and indent <= stack[-1][2]:
                stack.pop()

            current_dict = stack[-1][0]

            if ':' in line and not stripped.startswith('-'):
                key, _, value = stripped.partition(':')
                key = key.strip()
                value = value.strip()

                if not value:
                    # Nested dict or list
                    new_dict = {}
                    current_dict[key] = new_dict
                    stack.append((new_dict, key, indent))
                else:
                    # Value
                    if value.startswith('[') and value.endswith(']'):
                        # List
                        items = [v.strip().strip('"\'') for v in value[1:-1].split(',') if v.strip()]
                        current_dict[key] = items
                    elif value.lower() in ('true', 'false'):
                        current_dict[key] = value.lower() == 'true'
                    elif value.lower() == 'null':
                        current_dict[key] = None
                    elif value.startswith('"') or value.startswith("'"):
                        current_dict[key] = value.strip('"\'')
                    else:
                        current_dict[key] = value

            elif stripped.startswith('-'):
                # List item
                item_str = stripped[1:].strip()
                parent_dict, parent_key, _ = stack[-1]

                if parent_key and not isinstance(parent_dict.get(parent_key), list):
                    parent_dict[parent_key] = []

                if ':' in item_str:
                    # Dict item
                    item_dict = {}
                    key, _, value = item_str.partition(':')
                    if value.strip():
                        item_dict[key.strip()] = value.strip().strip('"\'')

                    parent_dict[parent_key].append(item_dict)
                    stack.append((item_dict, None, indent))
                else:
                    # String item
                    parent_dict[parent_key].append(item_str.strip('"\''))

        return result

    def _load_templates(self):
        """Load entity templates from .deia/templates/."""
        print(f"📝 Loading templates...")

        # Try to find templates
        template_paths = {
            'llh': ['.deia/templates/llh/minimal-llh.md', 'templates/llh/LLH-TEMPLATE.md'],
            'tag': ['.deia/templates/tag/minimal-tag.md', 'templates/tag/TAG-TEMPLATE.md']
        }

        for entity_type, paths in template_paths.items():
            for path in paths:
                template_file = Path(path)
                if template_file.exists():
                    self.templates[entity_type] = template_file.read_text(encoding='utf-8')
                    print(f"   ✓ {entity_type}: {template_file}")
                    break
            else:
                raise FileNotFoundError(f"No template found for {entity_type}")

    def _validate_dna(self):
        """Validate DNA pack structure."""
        print(f"✓ Validating DNA pack...")

        required = ['dna_version', 'pack_id', 'entities']
        missing = [f for f in required if f not in self.dna]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        # Validate entities
        entities = self.dna['entities']
        for llh in entities.get('llhs', []):
            if 'id' not in llh or 'title' not in llh:
                raise ValueError(f"LLH missing id or title: {llh}")

        for tag in entities.get('tags', []):
            if 'id' not in tag or 'title' not in tag or 'parent' not in tag:
                raise ValueError(f"TAG missing id, title, or parent: {tag}")

        print(f"   ✓ DNA pack valid")

    def _get_approval(self) -> bool:
        """Get human approval before building."""
        entities = self.dna.get('entities', {})
        total = len(entities.get('llhs', [])) + len(entities.get('tags', []))

        print(f"\n⚠️  Ready to build {total} entities")
        print(f"   Output: {self.dna.get('routing', {}).get('output_dir', 'unspecified')}")

        response = input("\n   Proceed? (yes/no): ").strip().lower()
        return response == 'yes'

    def _create_entities(self):
        """Create all entities from DNA."""
        print(f"\n🏗️  Creating entities...")

        entities = self.dna['entities']
        routing = self.dna.get('routing', {})
        output_base = Path(routing.get('output_dir', '.deia/.projects/output'))

        # Create LLHs
        for llh in entities.get('llhs', []):
            self._create_llh(llh, output_base / 'llhs')

        # Create TAGs
        for tag in entities.get('tags', []):
            self._create_tag(tag, output_base / 'tag-teams')

    def _create_llh(self, llh: Dict[str, Any], output_dir: Path):
        """Create a single LLH entity."""
        entity_id = llh['id']
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{entity_id}.md"

        if output_file.exists():
            print(f"   ⚠️  Skipping {entity_id} (already exists)")
            return

        # Render template
        content = self.templates['llh']
        variables = {
            'ID': entity_id,
            'TITLE': llh.get('title', ''),
            'NAME': llh.get('title', ''),
            'DATE': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'ACTOR': 'llh-factory-egg',
            'ENTITY_TYPE': 'llh',
            'STRUCTURE': llh.get('structure', 'flat'),
            'PARENT': llh.get('parent', 'null'),
        }

        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))

        output_file.write_text(content, encoding='utf-8')
        self.created_files.append(output_file)
        print(f"   ✓ Created LLH: {output_file}")

    def _create_tag(self, tag: Dict[str, Any], output_dir: Path):
        """Create a single TAG entity."""
        entity_id = tag['id']
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{entity_id}.md"

        if output_file.exists():
            print(f"   ⚠️  Skipping {entity_id} (already exists)")
            return

        # Render template
        content = self.templates['tag']
        variables = {
            'ID': entity_id,
            'TITLE': tag.get('title', ''),
            'NAME': tag.get('title', ''),
            'DATE': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'ACTOR': 'llh-factory-egg',
            'ENTITY_TYPE': 'tag',
            'PARENT': tag.get('parent', ''),
            'DEADLINE': tag.get('deadline', 'null'),
        }

        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))

        output_file.write_text(content, encoding='utf-8')
        self.created_files.append(output_file)
        print(f"   ✓ Created TAG: {output_file}")

    def _validate_outputs(self):
        """Validate created files."""
        print(f"\n✓ Validating outputs...")
        # Basic validation - files exist and have content
        for file_path in self.created_files:
            if not file_path.exists() or file_path.stat().st_size == 0:
                print(f"   ✗ Invalid: {file_path}")
                return False
        print(f"   ✓ All {len(self.created_files)} files valid")
        return True

    def _log_rse(self):
        """Log build event to RSE."""
        rse_file = Path('.deia/telemetry/rse.jsonl')
        rse_file.parent.mkdir(parents=True, exist_ok=True)

        event = {
            'ts': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'type': 'factory_build',
            'lane': 'Process',
            'actor': 'llh-factory-egg',
            'data': {
                'dna_pack': str(self.dna_path),
                'pack_id': self.dna.get('pack_id'),
                'files_created': len(self.created_files)
            }
        }

        with rse_file.open('a', encoding='utf-8') as f:
            f.write(json.dumps(event) + '\n')

        print(f"   ✓ Logged to RSE")


# CLI entry point (when run directly)
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python egg.md <dna-pack.yaml>")
        sys.exit(2)

    builder = LLHFactoryBuilder(sys.argv[1])
    success = builder.build()
    sys.exit(0 if success else 1)
```

## Helper Shell Script

Extract and save as `build_from_dna.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: ./build_from_dna.sh <dna-pack.yaml>"
    exit 2
fi

DNA_PACK="$1"

# Extract Python code from egg.md
python3 -c "
import sys

# Read egg.md
with open('egg.md', 'r') as f:
    content = f.read()

# Extract code block between \`\`\`python and \`\`\`
import re
match = re.search(r'\`\`\`python\n(.*?)\n\`\`\`', content, re.DOTALL)
if not match:
    print('Error: No Python code block found in egg.md', file=sys.stderr)
    sys.exit(1)

code = match.group(1)

# Execute code with DNA pack argument
sys.argv = ['egg.md', '${DNA_PACK}']
exec(code)
"
```

## DNA Pack Format

DNA packs are pure data (YAML) with NO executable code:

```yaml
dna_version: "0.1"
pack_id: {{PACK_ID}}
author: {{AUTHOR}}
created: {{DATE}}

entities:
  llhs:
    - id: {{LLH_ID}}
      title: "{{LLH_TITLE}}"
      structure: {{STRUCTURE}}  # executive, legislative, functional
      parent: null  # Parent LLH ID or null
      members: []
      caps: []

  tags:
    - id: {{TAG_ID}}
      title: "{{TAG_TITLE}}"
      parent: {{PARENT_LLH}}  # Required
      deadline: {{DEADLINE}}  # ISO date or null
      members: []
      caps: []

routing:
  output_dir: ".deia/.projects/{{PROJECT}}_001"
```

## Virus Prevention

✅ **Egg contains:** Builder code (recipe)
✅ **DNA contains:** Entity definitions (data only)
❌ **DNA does NOT contain:** Executable code

This prevents "viral hijacking" where instructions execute from data files.

## eOS Compliance

**ROTG:** All entities follow eOS v0.1 schema
**DND:** No overwrites, archive old versions
**Caps:** parse_dna, build_hierarchy, create_entities, validate_outputs, log_operations

## Version History

**v0.2.0 (2025-10-15):**
- Self-contained with embedded builder code
- DNA pack format (pure data)
- No external tool dependencies
- Virus-free separation

---

**Proposed by:** claude
**Created:** 2025-10-15
**Status:** Template (self-contained)
**Version:** 0.2.0
**eOS:** 0.1
