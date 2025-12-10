---
title: LLH Factory - Ready for First Hatch
date: 2025-10-16
status: ready
author: Claude (Anthropic)
policy: DND
---

# LLH Factory - Ready for First Hatch

## Summary

The LLH Factory pattern has been **redesigned and is ready for use**. All four tasks completed:

1. ✅ **External tools are CORRECT** - They belong in DEIA Global Commons
2. ✅ **Egg redesigned** - Minimal, references commons tools
3. ✅ **Terminology updated** - "DNA pack" → "eOS pack" throughout
4. ✅ **eOS pack format created** - Template and example ready

## Three-Component Pattern (Correct Design)

### 1. Egg (Minimal Bootstrap)
**Location:** `.deia/templates/egg/llh-factory-egg.md`

**Purpose:** Minimal orchestration instructions
- NO embedded code
- NO entity definitions
- ONLY references to commons tools
- Workflow coordination

### 2. eOS Pack (Project Blueprint)
**Location:** `.deia/eos-packs/<project-id>.yaml`

**Purpose:** Pure YAML data describing WHAT to build
- Entity definitions (LLHs, TAGs, drones)
- Organizational structure
- Routing configuration
- NO executable code

**Format:**
```yaml
---
eos_version: "0.1"
pack_id: my-project
author: dave
created: 2025-10-16

entities:
  llhs: [...]
  tags: [...]
  drones: []

routing:
  llhs: ".deia/.projects/my-project_001/llhs/"
  tags: ".deia/.projects/my-project_001/tag-teams/"
  drones: ".deia/.projects/my-project_001/drones/"

build:
  validate: true
  log_rse: true
  require_approval: true
---
```

### 3. DEIA Global Commons (Shared Resources)
**Location:** `.deia/tools/`, `.deia/templates/`

**Resources:**
- **Builder:** `.deia/tools/llh_factory_build.py` (creates entities)
- **Parser:** `.deia/tools/spec_parser.py` (parses eOS packs)
- **Templates:** `.deia/templates/llh/minimal-llh.md`, `.deia/templates/tag/minimal-tag.md`
- **Validator:** `.deia/tools/llh_validate.py` (validates entities)

## Files Created/Updated

### Templates
- ✅ `.deia/templates/egg/llh-factory-egg.md` - Updated with three-component pattern
- ✅ `.deia/templates/egg/minimal-egg.md` - Updated terminology
- ✅ `.deia/templates/egg/VERSION.md` - Updated documentation
- ✅ `.deia/templates/eos-pack/llh-org-eos-pack.yaml` - NEW: eOS pack template

### Examples
- ✅ `.deia/eos-packs/example-startup.yaml` - NEW: Example eOS pack

### Tools (DEIA Global Commons)
- ✅ `.deia/tools/llh_factory_build.py` - Updated to accept --eos-pack (and --spec for legacy)
- ✅ `.deia/tools/spec_parser.py` - Updated to support both eos_version+pack_id and spec_version+project

### Documentation
- ✅ `.deia/commons/CHANGELOG.md` - Added terminology update entry
- ✅ This file

## How to Use

### Step 1: Create eOS Pack

```bash
# Copy template
cp .deia/templates/eos-pack/llh-org-eos-pack.yaml .deia/eos-packs/my-project.yaml

# Edit my-project.yaml to define your entities
```

### Step 2: Validate eOS Pack

```bash
python .deia/tools/spec_parser.py .deia/eos-packs/my-project.yaml
```

### Step 3: Dry Run (Optional)

```bash
python .deia/tools/llh_factory_build.py --eos-pack .deia/eos-packs/my-project.yaml --dry-run
```

### Step 4: Build from eOS Pack

```bash
python .deia/tools/llh_factory_build.py --eos-pack .deia/eos-packs/my-project.yaml
# Approve when prompted
```

### Step 5: Validate Outputs

```bash
python .deia/tools/llh_validate.py .deia/.projects/my-project_001/llhs/*.md .deia/.projects/my-project_001/tag-teams/*.md
```

### Step 6: Review & Commit

```bash
# Review created files
ls -la .deia/.projects/my-project_001/

# Check RSE log
tail .deia/telemetry/rse.jsonl

# Commit
git add .deia/.projects/my-project_001/
git commit -m "feat: created org structure from eOS pack"
```

## Example Usage

```bash
# Use the example eOS pack
python .deia/tools/llh_factory_build.py --eos-pack .deia/eos-packs/example-startup.yaml

# This creates:
# - .deia/.projects/example-startup_001/llhs/founders-llh.md
# - .deia/.projects/example-startup_001/llhs/engineering-llh.md
# - .deia/.projects/example-startup_001/llhs/product-llh.md
# - .deia/.projects/example-startup_001/tag-teams/mvp-launch-tag.md
# - .deia/.projects/example-startup_001/tag-teams/customer-beta-tag.md
```

## Virus Prevention

### ❌ What NOT to Do

**DO NOT embed entity definitions in eggs:**
```markdown
# BAD - Virus!
entities:
  - house-llh
  - senate-llh
```

**DO NOT embed builder code in eggs:**
```markdown
# BAD - Virus!
```python
class LLHBuilder:
    def build(): ...
```
```

**DO NOT include executable code in eOS packs:**
```yaml
# BAD - Virus!
on_build: |
  #!/bin/bash
  ./malicious-script.sh
```

### ✅ Correct Pattern

**Egg:** Minimal references to commons
**eOS Pack:** Pure YAML data only
**Commons:** Shared tools/templates

**Separation = Safety**

## Known Issues

### Minor: Unicode Output on Windows

The tools use `✓` and `✗` characters which may not render correctly on Windows console. This is cosmetic only - functionality is unaffected.

**Workaround:** Output is still readable, just shows unicode escapes.

## Next Steps

1. **Test with example:** `python .deia/tools/llh_factory_build.py --eos-pack .deia/eos-packs/example-startup.yaml`
2. **Create your own eOS pack:** Copy template and customize
3. **Build your organization:** Run factory builder
4. **Validate outputs:** Ensure eOS compliance
5. **Commit and iterate:** Add more entities as needed

## Files to Archive (Optional)

The following files represent rejected designs and can be archived:

- `.deia/templates/egg/llh-factory-egg-self-contained.md` (embedded code approach - rejected)

Reason: Self-contained eggs with embedded code were the wrong pattern. The correct pattern is minimal eggs that reference DEIA Global Commons tools.

## References

- **Factory Egg:** `.deia/templates/egg/llh-factory-egg.md`
- **eOS Pack Template:** `.deia/templates/eos-pack/llh-org-eos-pack.yaml`
- **Example eOS Pack:** `.deia/eos-packs/example-startup.yaml`
- **Factory Pattern Doc:** `.deia/docs/FACTORY-PATTERN.md`
- **Preservation Record:** `.deia/LLH-FACTORY-EGG-PRESERVATION.md`
- **RCA:** `.deia/incidents/RCA-2025-10-15-llh-builder-eggs.md`

---

**Created:** 2025-10-16T12:05:35Z
**Author:** Claude (Anthropic, Bee Queen)
**Status:** Ready for first hatch
**Policy:** DND - Do not delete this record
