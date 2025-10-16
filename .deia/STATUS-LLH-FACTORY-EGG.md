# LLH Factory Egg - Status & Design

## Problem Statement

We need an **LLH Factory Egg** that contains enough "recipe" to bootstrap the creation of complex LLH structures from specification documents. Currently, there's confusion between:

1. **The Egg** (template/recipe) - Instructions for creating LLHs
2. **The Spec** (what to build) - Description of the LLH to be created
3. **The Factory** (builder logic) - Code that reads spec and creates entities

## Current State (2025-10-15)

### What Exists

**Tools:**
- ✅ `llh_hatch.sh/ps1` - Creates LLH/TAG/egg files from templates
- ✅ `egg_expand.py` - Expands egg into working directory
- ✅ `builder_launch.sh/ps1` - Orchestrates egg expand → hatch → validate
- ✅ `llh_validate.py` - Validates LLH schema compliance

**Templates:**
- ✅ `.deia/templates/egg/minimal-egg.md` - Clean minimal egg template (eOS v0.1)
- ✅ `.deia/templates/llh/minimal-llh.md` - LLH template
- ✅ `.deia/templates/tag/minimal-tag.md` - TAG template

**Issues Identified:**
- ❌ **Virus problem:** Eggs contained embedded government DNA (House/Senate entities)
- ❌ **Pattern confusion:** Mixing egg definition with spec documents
- ❌ **No factory egg:** No egg specifically designed to build other LLHs
- ❌ **Incomplete separation:** Egg template vs spec vs builder logic not clearly separated

### What Happened (RCA-2025-10-15-llh-builder-eggs.md)

**Incident:** LLHs were hatched directly without first expanding an egg workspace

**Contributing Factors:**
1. Ambiguous instructions mixed egg expansion with direct hatch commands
2. No `egg_expand.py` workflow enforcement
3. Preconditions not checked (no egg.md in target project)
4. Segmentation defaults changed mid-stream (`.deia/llhs` → `.projects/<project>`)

**Corrective Actions Needed:**
- CA-1: Add precondition check (require egg.md or --force)
- CA-2: ✅ DONE - Updated DEIA-RULES for egg-first workflow
- CA-3: Add guided `builder_launch` flow

## Design: LLH Factory Egg

### What is an LLH Factory Egg?

An **LLH Factory Egg** is a special egg that:
1. Contains instructions for reading LLH specification documents
2. Knows how to create organizational structures (LLHs, TAGs, drones, bees)
3. Can parse spec files and generate proper entities
4. Enforces eOS compliance (ROTG, DND, schema validation)
5. Handles complex hierarchies (parent LLHs, nested TAGs, etc.)

### Separation of Concerns

#### 1. **Egg** (Factory Recipe)
**File:** `.deia/templates/egg/llh-factory-egg.md`
**Purpose:** Instructions for creating LLH infrastructure
**Contains:**
- eOS manifest (kind: egg, caps: [build_llh, parse_spec, create_hierarchy])
- Reference to builder logic (llh_hatch.sh, validation tools)
- Workflow instructions (expand → parse spec → hatch entities → validate)
- Policy enforcement (ROTG, DND)

#### 2. **Spec** (What to Build)
**File:** `.deia/.projects/<project>/spec.md` or `<project>-spec.md`
**Purpose:** Describes the LLH/organization to create
**Contains:**
- Organizational structure (LLHs, TAGs, teams)
- Entity definitions (members, capabilities, routing)
- Scenarios, objectives, timelines
- NO executable code or embedded commands

#### 3. **Factory Logic** (Builder)
**Files:** `llh_hatch.sh`, `llh_validate.py`, `builder_launch.sh`
**Purpose:** Reads spec, executes egg instructions, creates entities
**Contains:**
- Template rendering logic
- File system operations
- Validation checks
- RSE logging

### Proper Workflow (Virus-Free)

```
1. Create Spec Document
   .deia/.projects/federal_gov/spec.md
   (describes House, Senate, Executive, etc.)

2. Select Factory Egg
   .deia/templates/egg/llh-factory-egg.md

3. Expand Egg
   ./egg_expand.py .deia/templates/egg/llh-factory-egg.md
   → Creates .deia/.projects/federal_gov_001/

4. Run Factory
   cd .deia/.projects/federal_gov_001/
   ./build.sh --spec ../federal_gov/spec.md
   → Reads spec, creates LLHs/TAGs

5. Validate
   llh_validate.py llhs/*.md tag-teams/*.md

6. Review & Commit
   Human reviews outputs, commits to git
```

## What's Missing

### 1. LLH Factory Egg Template
**File:** `.deia/templates/egg/llh-factory-egg.md`

**Should contain:**
- eOS manifest with factory capabilities
- Instructions for spec parsing
- Entity creation workflow
- Hierarchy building logic
- Validation requirements

### 2. Spec Document Format
**File:** `.deia/templates/spec/llh-org-spec.md`

**Should define:**
- YAML/Markdown structure for org specs
- Entity definition format
- Relationship declarations (parent/child, dependencies)
- Routing and segmentation rules

### 3. Factory Builder Script
**File:** `.deia/tools/llh_factory_build.py` or `.sh`

**Should do:**
- Parse spec document (YAML front matter + Markdown sections)
- Generate LLH/TAG entities from spec
- Create proper directory structure
- Handle hierarchies (parent → child relationships)
- Validate all outputs
- Log to RSE

### 4. Spec Parser
**File:** `.deia/tools/spec_parser.py`

**Should do:**
- Read spec document
- Extract entity definitions
- Validate spec format
- Return structured data for builder

## Proposed Solution

### Phase 1: Separate Egg from Spec ✅ (Partially Done)

**Completed:**
- ✅ Minimal egg template is clean (no government DNA)
- ✅ Virus prevention documented
- ✅ egg_expand.py exists

**Still Needed:**
- [ ] Create llh-factory-egg.md template
- [ ] Define spec document format
- [ ] Document proper pattern clearly

### Phase 2: Build Factory Logic

**Tasks:**
1. Create spec document schema/template
2. Build spec parser (Python)
3. Enhance builder to read specs
4. Add hierarchy support (nested entities)
5. Test with federal government example

### Phase 3: Integration & Validation

**Tasks:**
1. Update builder_launch.sh to use factory
2. Add precondition checks (CA-1)
3. Test full workflow (expand → build → validate)
4. Document for users

## Example: Federal Government LLH

### Current Problem
Egg template contains:
```markdown
### Entities
- house-llh
- senate-llh
- executive-llh
```

This is a **virus** - executable instructions embedded in egg.

### Proper Pattern

**Egg (llh-factory-egg.md):**
```yaml
---
eos: "0.1"
kind: egg
id: llh-factory
caps: [parse_spec, build_hierarchy, create_entities]
routing:
  action: expand_and_build
---

# LLH Factory Egg

This egg reads an LLH specification and creates the organizational structure.

## Workflow
1. Expand this egg: `egg_expand.py llh-factory-egg.md`
2. Provide spec: `build.sh --spec <spec-file>`
3. Review outputs: `llhs/`, `tag-teams/`
4. Validate: `llh_validate.py llhs/*.md`
```

**Spec (federal-gov-spec.md):**
```yaml
---
spec_version: "0.1"
project: federal_government
entities:
  llhs:
    - id: house-llh
      title: "U.S. House of Representatives"
      members: 435
      structure: legislative
    - id: senate-llh
      title: "U.S. Senate"
      members: 100
      structure: legislative
  tags:
    - id: appropriations-2025-tag
      title: "2025 Appropriations"
      parent: house-llh
      deadline: "2025-09-30"
---

# Federal Government Simulation

## Overview
Simulation of U.S. federal government decision-making...
```

**Factory builds from spec:**
```bash
cd .deia/.projects/federal_gov_001/
./build.sh --spec ../federal-gov-spec.md
# Reads spec YAML, creates house-llh.md, senate-llh.md, appropriations-2025-tag.md
```

## Recommended Next Steps

### Immediate (This Session)
1. **Document the pattern** - Create clear examples
2. **Create llh-factory-egg.md** - Template for factory eggs
3. **Define spec format** - Schema for org specs
4. **Update STATUS** - This document

### Short Term (Next Session)
5. **Build spec parser** - Python script to read specs
6. **Enhance builder** - Add spec-driven entity creation
7. **Test workflow** - Full expand → build → validate
8. **Update tools** - Add precondition checks (CA-1)

### Medium Term
9. **Complex hierarchies** - Parent/child LLH support
10. **Multi-project** - Handle multiple concurrent sims
11. **Documentation** - User guide for factory pattern
12. **Examples** - Multiple spec examples (gov, corp, research)

## Files to Create/Update

**Create:**
- [ ] `.deia/templates/egg/llh-factory-egg.md`
- [ ] `.deia/templates/spec/llh-org-spec.md`
- [ ] `.deia/tools/spec_parser.py`
- [ ] `.deia/tools/llh_factory_build.py`
- [ ] `.deia/docs/FACTORY-PATTERN.md`

**Update:**
- [ ] `.deia/tools/builder_launch.sh` - Add spec support
- [ ] `.deia/tools/llh_hatch.sh` - Add precondition check (CA-1)
- [ ] `.deia/templates/egg/minimal-egg.md` - Reference factory pattern
- [ ] `ROADMAP.md` - Add LLH factory as task

## Success Criteria

**Factory Egg Works When:**
1. Can expand egg without embedded entities
2. Can read spec document (YAML + Markdown)
3. Creates proper LLH/TAG files from spec
4. Validates all outputs
5. Logs to RSE
6. No viruses (no embedded commands in eggs)
7. DND honored (archives, not deletes)
8. Proper segmentation (project-based directories)

## Related Documents

- **RCA:** `.deia/incidents/RCA-2025-10-15-llh-builder-eggs.md`
- **Pin:** `.deia/sessions/2025-10-15-llh-builder-pin.md`
- **Instructions:** `.deia/corpus/entries/CLAUDE-INSTR-llh-builder-2025-10-15.md`
- **Archive Request:** `.deia/archives/REQUEST-2025-10-15-llh-builder-cleanup.md`
- **Egg Template:** `.deia/templates/egg/minimal-egg.md`
- **Version History:** `.deia/templates/egg/VERSION.md`

---

**Status:** Design phase
**Created:** 2025-10-15
**Author:** Claude (Anthropic)
**Next Review:** When ready to implement factory
