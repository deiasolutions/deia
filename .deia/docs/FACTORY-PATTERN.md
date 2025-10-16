# LLH Factory Pattern

## Overview

The **LLH Factory Pattern** separates the recipe (egg) from the blueprint (spec) to prevent viral contamination and enable systematic organizational structure creation.

## Problem Solved

**Before (Virus):**
```markdown
# Egg contains embedded entities
---
kind: egg
---
Create these LLHs:
- house-llh
- senate-llh
```
❌ Executable instructions in egg = virus

**After (Clean):**
```markdown
# Egg (factory recipe)
kind: factory-egg
Reads spec → creates entities

# Spec (blueprint)
entities:
  llhs:
    - id: house-llh
    - id: senate-llh
```
✅ Clean separation, no viruses

## Three Components

### 1. Factory Egg (Template)
**File:** `.deia/templates/egg/llh-factory-egg.md`
**Purpose:** Instructions for HOW to build
**Contains:**
- eOS manifest
- Workflow instructions
- Policy enforcement
- Tool references

### 2. Spec Document (Blueprint)
**File:** `.deia/.projects/<project>/spec.md`
**Purpose:** Describes WHAT to build
**Contains:**
- Entity definitions (YAML)
- Organizational structure
- Relationships
- Routing configuration

### 3. Factory Builder (Code)
**Files:** `spec_parser.py`, `llh_factory_build.py`
**Purpose:** Reads spec, creates entities
**Contains:**
- Spec parser
- Template renderer
- Entity creation
- Validation

## Workflow

### Step 1: Create Spec Document

```bash
# Copy template
cp .deia/templates/spec/llh-org-spec.md .deia/.projects/my-org/spec.md

# Edit spec.md to define your organization
```

**Example spec.md:**
```yaml
---
spec_version: "0.1"
project: my-organization

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
---

# My Organization

[Description in Markdown]
```

### Step 2: Expand Factory Egg

```bash
python .deia/tools/egg_expand.py .deia/templates/egg/llh-factory-egg.md
```

**Creates:** `.deia/.projects/my-organization_001/`

### Step 3: Build from Spec

```bash
cd .deia/.projects/my-organization_001/
python ../../../tools/llh_factory_build.py --spec ../my-org/spec.md
```

**Creates:**
- `llhs/leadership-llh.md`
- `llhs/engineering-llh.md`
- `tag-teams/q4-launch-tag.md`

### Step 4: Validate & Commit

```bash
# Validate
python .deia/tools/llh_validate.py llhs/*.md tag-teams/*.md

# Review
ls -la llhs/ tag-teams/

# Commit
git add .deia/.projects/my-organization_001/
git commit -m "feat: created org structure from spec"
```

## Spec Document Format

### YAML Front Matter

```yaml
---
spec_version: "0.1"          # Required
project: my-project           # Required
author: dave                  # Optional
created: 2025-10-15          # Optional
status: draft                 # Optional

entities:                     # Required
  llhs:                       # List of LLHs
    - id: my-llh             # Required: unique ID
      title: "My LLH"        # Required: display name
      structure: executive   # Optional: executive, legislative, etc.
      parent: null           # Optional: parent LLH ID
      members: []            # Optional: member list
      caps: [plan, execute]  # Optional: capabilities
      governance:
        structure: flat
        decision_mode: consensus
        transparency: members-only
      policy:
        rotg: true
        dnd: true
      constraints: []
      capacities:
        budget: medium
        attention: high
        staff_cycles: medium

  tags:                       # List of TAGs
    - id: my-tag
      title: "My TAG"
      parent: my-llh          # Required: parent LLH
      deadline: "2025-12-31" # Optional: ISO date
      members: []
      caps: [coordinate]
      objectives: "Launch product"

  drones:                     # Optional: automated workers
    - id: my-drone
      title: "My Drone"
      type: processor
      parent: my-tag
      triggers: [on_schedule]
      actions: [aggregate_metrics]

routing:                      # Optional (has defaults)
  llhs: ".deia/.projects/my-project_001/llhs/"
  tags: ".deia/.projects/my-project_001/tag-teams/"
  drones: ".deia/.projects/my-project_001/drones/"

build:                        # Optional (has defaults)
  validate: true              # Run validation after build
  log_rse: true               # Log to RSE
  require_approval: true      # Require human approval
---
```

### Markdown Body

```markdown
# Project Title

## Overview
[Describe the organization/simulation]

## Objectives
[What are you trying to achieve?]

## Structure
[Explain the organizational hierarchy]

## Scenarios
[Define scenarios, timelines, milestones]

## Success Criteria
[How do you measure success?]
```

## Entity Types

### LLH (Limited Liability Hive)
**Purpose:** Organizational unit with governance
**Examples:**
- Executive team
- Department
- Division
- Committee

**Required Fields:**
- `id`: Unique identifier (lowercase-with-hyphens)
- `title`: Display name

**Optional Fields:**
- `structure`: executive, legislative, functional, etc.
- `parent`: Parent LLH ID (for hierarchies)
- `members`: List of member IDs or count
- `caps`: List of capabilities
- `governance`: Structure, decision mode, transparency
- `policy`: ROTG, DND flags
- `constraints`: List of constraints
- `capacities`: Budget, attention, staff levels

### TAG (Together And Good team)
**Purpose:** Cross-functional team or project
**Examples:**
- Product launch team
- Task force
- Working group
- Ad-hoc collaboration

**Required Fields:**
- `id`: Unique identifier
- `title`: Display name
- `parent`: Parent LLH ID

**Optional Fields:**
- `deadline`: ISO date
- `members`: List of member IDs
- `caps`: Capabilities
- `objectives`: Goal description

### Drone (Optional)
**Purpose:** Automated worker or background process
**Examples:**
- Metrics collector
- Alert processor
- Report generator
- Data aggregator

**Required Fields:**
- `id`: Unique identifier
- `title`: Display name
- `type`: processor, monitor, aggregator, notifier

**Optional Fields:**
- `parent`: Parent TAG or LLH
- `triggers`: List of trigger conditions
- `actions`: List of actions to perform

## Hierarchies

### Parent/Child LLHs

```yaml
entities:
  llhs:
    - id: parent-llh
      title: "Parent Organization"

    - id: child-llh
      title: "Child Unit"
      parent: parent-llh        # References parent
```

### LLH → TAG Membership

```yaml
entities:
  llhs:
    - id: engineering-llh
      title: "Engineering"

  tags:
    - id: backend-tag
      title: "Backend Team"
      parent: engineering-llh   # Belongs to engineering
```

### Complex Hierarchy Example

```yaml
entities:
  llhs:
    - id: company-llh
      title: "Company Leadership"

    - id: engineering-llh
      title: "Engineering"
      parent: company-llh

    - id: backend-llh
      title: "Backend Engineering"
      parent: engineering-llh

  tags:
    - id: api-rewrite-tag
      title: "API Rewrite Project"
      parent: backend-llh
```

**Result:**
```
company-llh
└── engineering-llh
    └── backend-llh
        └── api-rewrite-tag
```

## Tools

### spec_parser.py
**Purpose:** Parse and validate spec documents

**Usage:**
```bash
python .deia/tools/spec_parser.py spec.md
```

**Output:**
```
✓ Spec parsed successfully: spec.md

Project: my-project
Author: dave
Status: draft

Entities:
  LLHs: 3
  TAGs: 2
  Drones: 1
  Total: 6

Routing:
  llhs: .deia/.projects/my-project_001/llhs/
  tags: .deia/.projects/my-project_001/tag-teams/
  drones: .deia/.projects/my-project_001/drones/

✓ All entities valid
```

### llh_factory_build.py
**Purpose:** Build entities from spec

**Usage:**
```bash
# Basic build
python .deia/tools/llh_factory_build.py --spec spec.md

# Dry run (validate only)
python .deia/tools/llh_factory_build.py --spec spec.md --dry-run

# Custom templates
python .deia/tools/llh_factory_build.py --spec spec.md \
  --llh-template custom-llh.md

# Force (skip approval)
python .deia/tools/llh_factory_build.py --spec spec.md --force
```

**Options:**
- `--spec PATH`: Path to spec.md (required)
- `--llh-template PATH`: Custom LLH template
- `--tag-template PATH`: Custom TAG template
- `--drone-template PATH`: Custom drone template
- `--force`: Skip approval prompts
- `--dry-run`: Validate but don't create files
- `--quiet`: Minimal output

### egg_expand.py
**Purpose:** Expand factory egg into working directory

**Usage:**
```bash
python .deia/tools/egg_expand.py .deia/templates/egg/llh-factory-egg.md
```

**Creates:** `.deia/.projects/<project>_NNN/egg.md`

## Validation

### Pre-build Validation
- Spec document has valid YAML
- Required fields present
- No circular dependencies
- Entity IDs unique
- Parent references valid

### Post-build Validation
```bash
python .deia/tools/llh_validate.py llhs/*.md tag-teams/*.md
```

Checks:
- eOS schema compliance
- Required fields present
- Valid ROTG/DND policy
- Proper routing configuration

## Security & Safety

### Preconditions
1. Expanded egg exists in project directory
2. Spec document validated
3. Target directories don't have conflicts
4. Human approval obtained (unless --force)

### Guardrails
- Warn if >50 entities in spec
- Prevent file overwrites (DND honored)
- Require explicit confirmation for large batches
- Archive on request only

### Audit Trail
- Log every entity created (RSE)
- Log human approvals
- Log validation results
- Update CHANGELOG

## Examples

### Simple Organization

**spec.md:**
```yaml
---
spec_version: "0.1"
project: startup
entities:
  llhs:
    - id: founders-llh
      title: "Founders"
    - id: eng-llh
      title: "Engineering"
      parent: founders-llh
  tags:
    - id: mvp-tag
      title: "MVP Launch"
      parent: eng-llh
      deadline: "2025-12-31"
---

# Startup Organization
MVP launch structure
```

**Build:**
```bash
python llh_factory_build.py --spec startup/spec.md
```

**Creates:**
- `llhs/founders-llh.md`
- `llhs/eng-llh.md`
- `tag-teams/mvp-tag.md`

### Federal Government Simulation

See: `.deia/templates/spec/examples/federal-gov-spec.md`

### Corporate Structure

See: `.deia/templates/spec/examples/corp-structure-spec.md`

## Troubleshooting

### "Spec not found"
- Check path to spec.md
- Ensure you're in correct directory

### "Validation failed"
- Run `spec_parser.py spec.md` to see errors
- Check YAML syntax (indentation, colons)
- Verify required fields present

### "Entity already exists"
- Check for duplicate IDs
- Use `--force` to overwrite (not recommended)
- Archive old entity first

### "Template not found"
- Ensure templates exist in `.deia/templates/`
- Or specify custom template with `--llh-template`

### "Parent LLH not found"
- Verify parent ID matches an existing LLH
- Check for typos in parent references
- Ensure parent is defined before child

## Related Documents

- **Status:** `.deia/STATUS-LLH-FACTORY-EGG.md`
- **Factory Egg:** `.deia/templates/egg/llh-factory-egg.md`
- **Spec Template:** `.deia/templates/spec/llh-org-spec.md`
- **RCA:** `.deia/incidents/RCA-2025-10-15-llh-builder-eggs.md`

---

**Version:** 0.1.0
**Created:** 2025-10-15
**Author:** Claude (Anthropic)
**Status:** Documentation
