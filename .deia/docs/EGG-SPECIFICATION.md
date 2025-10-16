---
title: LLH Factory Egg Specification
version: 0.1.0
date: 2025-10-16
author: Claude (Anthropic)
status: specification
policy: DND
---

# LLH Factory Egg Specification

## What is an Egg?

An **egg** is a lightweight, minimal blueprint that orchestrates the creation of organizational structures in the DEIA system. Think of it as a **recipe card** that tells you:

1. What ingredients you need (eOS pack, commons tools)
2. Where to find them (file paths)
3. What steps to follow (workflow)

**Critically:** An egg contains NO executable code and NO entity definitions. It's pure orchestration instructions.

## The Factory Egg Explained

### Purpose

The **LLH Factory Egg** creates organizational structures (LLHs, TAGs, drones) from eOS packs. It's a template for building teams, hierarchies, and coordination structures.

### What It Contains

The factory egg (`.deia/templates/egg/llh-factory-egg.md`) contains:

#### 1. eOS Manifest (Front Matter)
```yaml
---
eos: "0.1"                    # eOS version compliance
kind: egg                     # Entity type
id: llh-factory               # Unique identifier
entity_type: factory          # What it creates
name: "LLH Factory Egg"       # Display name
proposed_by: claude           # Author
created: 2025-10-15           # Creation date
status: template              # Current status
policy:
  rotg: true                  # Rules of the Game compliance
  dnd: true                   # Do Not Delete policy
caps: [parse_spec, build_hierarchy, create_entities, validate_outputs, log_operations]
routing:
  project: "{{PROJECT_ID}}"   # Where to route outputs
  destination: eggs           # Destination type
  filename: llh-factory.md    # Output filename
  action: expand_and_build    # What action to take
hatch_date: null              # When hatched (null = template)
version: 0.1.0                # Template version
notes: "Factory egg for creating LLH organizational structures from eOS packs"
---
```

#### 2. Three-Component Pattern Documentation
Explains the separation of concerns:
- **Egg** (minimal bootstrap) - This file
- **eOS Pack** (project data) - What to build
- **DEIA Global Commons** (shared tools) - How to build

#### 3. Workflow Instructions
Step-by-step process:
1. Expand the egg (optional, for project isolation)
2. Prepare eOS pack
3. Build from eOS pack
4. Validate outputs
5. Review & commit

#### 4. References to Commons Tools
Points to shared resources:
- **Builder:** `.deia/tools/llh_factory_build.py`
- **Parser:** `.deia/tools/spec_parser.py`
- **Templates:** `.deia/templates/{llh,tag,drone}/`
- **Validator:** `.deia/tools/llh_validate.py`

#### 5. eOS Pack Format Examples
Shows what valid eOS pack data looks like (but does NOT contain actual data)

#### 6. Security & Safety Guidelines
Explains virus prevention:
- What NOT to include (code, entity definitions)
- What IS safe (references, instructions)
- How the pattern prevents contamination

## How It Works: Step-by-Step

### Conceptual Flow

```
┌─────────────┐
│  Egg        │  "I need an eOS pack and commons tools"
│ (minimal)   │
└──────┬──────┘
       │
       ├─────────> ┌─────────────┐
       │           │ eOS Pack    │  "Here's WHAT to build"
       │           │ (data)      │  - 3 LLHs
       │           └─────────────┘  - 2 TAGs
       │
       └─────────> ┌─────────────┐
                   │ Commons     │  "Here's HOW to build"
                   │ (tools)     │  - Builder code
                   └─────────────┘  - Templates
                          │
                          ▼
                   ┌─────────────┐
                   │ Entities    │  Created!
                   │ (outputs)   │  - llhs/*.md
                   └─────────────┘  - tag-teams/*.md
```

### Practical Workflow

#### Step 1: Create eOS Pack
```bash
# Copy template
cp .deia/templates/eos-pack/llh-org-eos-pack.yaml .deia/eos-packs/my-org.yaml

# Edit to define your entities
vim .deia/eos-packs/my-org.yaml
```

**eOS Pack Content:**
```yaml
---
eos_version: "0.1"
pack_id: my-org
author: dave
created: 2025-10-16

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
      title: "Q4 Product Launch"
      parent: engineering-llh
      deadline: "2025-12-31"

routing:
  llhs: ".deia/.projects/my-org_001/llhs/"
  tags: ".deia/.projects/my-org_001/tag-teams/"
---
```

#### Step 2: Reference the Egg
The egg is already available as a template at:
`.deia/templates/egg/llh-factory-egg.md`

You don't need to "run" the egg directly. Instead, you:

#### Step 3: Use Commons Tools
The egg tells you to use these tools:

**Validate eOS Pack:**
```bash
python .deia/tools/spec_parser.py .deia/eos-packs/my-org.yaml
```

**Build from eOS Pack:**
```bash
python .deia/tools/llh_factory_build.py --eos-pack .deia/eos-packs/my-org.yaml
```

**What happens internally:**
1. `llh_factory_build.py` reads `my-org.yaml`
2. Validates structure (eos_version, pack_id, entities)
3. For each LLH in `entities.llhs`:
   - Loads template from `.deia/templates/llh/minimal-llh.md`
   - Substitutes variables (ID, title, structure, etc.)
   - Writes to `.deia/.projects/my-org_001/llhs/{llh-id}.md`
4. For each TAG in `entities.tags`:
   - Loads template from `.deia/templates/tag/minimal-tag.md`
   - Substitutes variables
   - Writes to `.deia/.projects/my-org_001/tag-teams/{tag-id}.md`
5. Validates all created files
6. Logs to RSE

#### Step 4: Review Outputs
```bash
# Check created files
ls -la .deia/.projects/my-org_001/llhs/
ls -la .deia/.projects/my-org_001/tag-teams/

# View one
cat .deia/.projects/my-org_001/llhs/leadership-llh.md
```

#### Step 5: Validate & Commit
```bash
# Validate eOS compliance
python .deia/tools/llh_validate.py .deia/.projects/my-org_001/llhs/*.md

# Commit
git add .deia/.projects/my-org_001/
git commit -m "feat: created my-org structure from eOS pack"
```

## Why This Pattern?

### Problem: Viral Contamination

**BAD (Virus):**
```markdown
# Egg with embedded entities (VIRUS!)
---
kind: egg
---

Create these LLHs:
- house-llh
- senate-llh

```bash
llh_hatch.sh house-llh
llh_hatch.sh senate-llh
```
```

**Why it's bad:**
- Egg contains entity definitions (should be in eOS pack)
- Egg contains executable commands (should be in commons)
- If the egg gets copied/modified, entities multiply uncontrollably
- No separation of concerns

### Solution: Three-Component Separation

**GOOD (Clean):**

**Egg (llh-factory-egg.md):**
```markdown
---
kind: egg
caps: [orchestrate_build]
---

# LLH Factory Egg

Use these tools:
- Builder: .deia/tools/llh_factory_build.py
- Parser: .deia/tools/spec_parser.py

Read entity definitions from eOS pack.
```

**eOS Pack (my-org.yaml):**
```yaml
---
pack_id: my-org
entities:
  llhs:
    - id: house-llh
    - id: senate-llh
---
```

**Commons (llh_factory_build.py):**
```python
# Builder code lives here
def build_from_eos_pack(pack_path):
    entities = parse_pack(pack_path)
    for llh in entities['llhs']:
        create_llh(llh)
```

**Why it's good:**
- Clear separation: egg = instructions, pack = data, commons = code
- Egg can be reused for ANY org (startup, government, corporate)
- Entity definitions in one place (eOS pack)
- Builder code is shared across all projects
- No viral contamination possible

## Key Capabilities

The factory egg declares these capabilities:

### parse_spec
Reads and validates eOS pack YAML structure

### build_hierarchy
Understands parent/child relationships between LLHs

### create_entities
Instantiates LLH, TAG, and drone entities from templates

### validate_outputs
Ensures created entities comply with eOS schema

### log_operations
Records all build events to RSE telemetry

## eOS Compliance

### ROTG (Rules of the Game)
- All entities follow eOS v0.1 schema
- Capabilities declared explicitly
- Routing instructions clear
- Versioning mandatory

### DND (Do Not Delete)
- Archive old versions
- Log all operations
- No destructive changes
- Human approval required (unless --force)

## Security Model

### What the Egg CAN Do
✅ Reference commons tools
✅ Provide workflow instructions
✅ Define routing patterns
✅ Declare capabilities
✅ Explain the pattern

### What the Egg CANNOT Do
❌ Execute code directly
❌ Contain entity definitions
❌ Modify files outside routing
❌ Make network requests
❌ Access secrets

### Guardrails

1. **Human Approval:** Factory builder requires approval before creating files (unless `--force`)
2. **DND Enforcement:** Won't overwrite existing files
3. **Validation:** All outputs validated against eOS schema
4. **Audit Trail:** All operations logged to RSE
5. **Dry Run Mode:** Test builds without creating files

## Advanced Usage

### Custom Templates

Override default entity templates:

```bash
python .deia/tools/llh_factory_build.py \
  --eos-pack my-org.yaml \
  --llh-template custom-llh.md \
  --tag-template custom-tag.md
```

### Conditional Builds

In eOS pack (future feature):
```yaml
entities:
  llhs:
    - id: prod-llh
      condition: "environment == production"
```

### Hierarchical Organizations

```yaml
entities:
  llhs:
    - id: company-llh
      title: "Company Leadership"

    - id: engineering-llh
      parent: company-llh

    - id: backend-llh
      parent: engineering-llh

    - id: frontend-llh
      parent: engineering-llh
```

Result:
```
company-llh
└── engineering-llh
    ├── backend-llh
    └── frontend-llh
```

## Comparison: Egg vs eOS Pack vs Commons

| Aspect | Egg | eOS Pack | Commons |
|--------|-----|----------|---------|
| **Type** | Orchestration instructions | Pure data (YAML) | Executable code |
| **Contains** | References, workflow | Entity definitions | Builder logic |
| **Reusable** | Yes (any project) | No (project-specific) | Yes (shared) |
| **Executable** | No | No | Yes |
| **Location** | `.deia/templates/egg/` | `.deia/eos-packs/` | `.deia/tools/` |
| **Versioned** | Yes (v0.1.0) | Yes (eos_version) | Yes (git) |
| **Example** | llh-factory-egg.md | my-org.yaml | llh_factory_build.py |

## Real-World Example

### Scenario: Create Federal Government Simulation

**1. Create eOS Pack:**
```yaml
# .deia/eos-packs/federal-gov.yaml
---
eos_version: "0.1"
pack_id: federal-gov
author: dave
created: 2025-10-16

entities:
  llhs:
    - id: federal-gov-llh
      title: "Federal Government"
      structure: executive

    - id: house-llh
      title: "House of Representatives"
      parent: federal-gov-llh
      structure: legislative

    - id: senate-llh
      title: "Senate"
      parent: federal-gov-llh
      structure: legislative

    - id: executive-llh
      title: "Executive Branch"
      parent: federal-gov-llh
      structure: executive

  tags:
    - id: appropriations-2025-tag
      title: "2025 Appropriations Process"
      parent: house-llh
      deadline: "2025-09-30"
      members: ["house-appropriations-committee"]

    - id: budget-resolution-tag
      title: "Budget Resolution 2025"
      parent: senate-llh
      deadline: "2025-04-15"

routing:
  llhs: ".deia/.projects/federal-gov_001/llhs/"
  tags: ".deia/.projects/federal-gov_001/tag-teams/"
---
```

**2. Build:**
```bash
python .deia/tools/llh_factory_build.py --eos-pack .deia/eos-packs/federal-gov.yaml
```

**3. Result:**
```
.deia/.projects/federal-gov_001/
├── llhs/
│   ├── federal-gov-llh.md
│   ├── house-llh.md
│   ├── senate-llh.md
│   └── executive-llh.md
└── tag-teams/
    ├── appropriations-2025-tag.md
    └── budget-resolution-tag.md
```

**4. Each entity file contains:**
```markdown
---
eos: "0.1"
kind: llh
id: house-llh
entity_type: llh
name: "House of Representatives"
created: 2025-10-16T12:30:00Z
actor: llh-factory-builder
policy:
  rotg: true
  dnd: true
caps: [legislate, appropriate, oversight]
parent: federal-gov-llh
structure: legislative
routing:
  project: federal-gov_001
  destination: llhs
---

# House of Representatives

[Entity content...]
```

## Troubleshooting

### "eOS pack not found"
- Check path to `.yaml` file
- Ensure pack is in `.deia/eos-packs/`

### "Validation failed"
- Run `spec_parser.py` on pack
- Check YAML syntax (indentation!)
- Verify required fields: eos_version, pack_id, entities

### "Entity already exists"
- Check for duplicate IDs
- Files won't be overwritten (DND policy)
- Use `--force` to overwrite (not recommended)
- Or archive old entity first

### "Template not found"
- Ensure `.deia/templates/llh/minimal-llh.md` exists
- Or specify custom template with `--llh-template`

## Future Enhancements

### Planned (Not Yet Implemented)

- **Egg Expansion:** `egg_expand.py` to create project-specific copies
- **Conditional Entities:** Build based on environment/conditions
- **Template Inheritance:** Extend base templates
- **Batch Operations:** Build multiple packs at once
- **Rollback:** Undo builds and restore previous state

## Summary

### The Egg is NOT:
❌ A script that executes
❌ A container for entities
❌ A builder tool
❌ A data file

### The Egg IS:
✅ A recipe card
✅ An orchestration guide
✅ A reference document
✅ A pattern explanation

### Mental Model:
```
Egg = Recipe card that says:
  "Get ingredient A (eOS pack) from location X"
  "Get tool B (builder) from location Y"
  "Follow these steps: 1, 2, 3..."

NOT:
  "Here are the actual ingredients mixed together"
  "Here is the tool itself"
  "I will cook this for you automatically"
```

## Related Documentation

- **Factory Pattern:** `.deia/docs/FACTORY-PATTERN.md`
- **eOS Pack Template:** `.deia/templates/eos-pack/llh-org-eos-pack.yaml`
- **Example eOS Pack:** `.deia/eos-packs/example-startup.yaml`
- **Factory Egg Source:** `.deia/templates/egg/llh-factory-egg.md`
- **Ready Status:** `.deia/LLH-FACTORY-READY.md`

---

**Version:** 0.1.0
**Created:** 2025-10-16
**Author:** Claude (Anthropic, Bee Queen)
**Status:** Specification
**Policy:** DND
