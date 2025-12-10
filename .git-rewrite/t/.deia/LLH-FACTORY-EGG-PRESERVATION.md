---
title: LLH Factory Egg - Preservation Record
date: 2025-10-15
status: pre-hatch-preservation
author: Claude (Anthropic)
purpose: Preserve egg state and instructions before first hatch
policy: DND
---

# LLH Factory Egg - Preservation Record

## Purpose

This document preserves the complete state of the LLH Factory Egg and all related components **before first hatch** to ensure we can recover if anything goes wrong.

## Timestamp

**Preserved:** 2025-10-15T[TIME]Z
**By:** Claude (Anthropic, Bee Queen)
**At Request Of:** Dave
**Reason:** Pre-hatch safety checkpoint

## Components Preserved

### 1. Factory Egg Template
**File:** `.deia/templates/egg/llh-factory-egg.md`
**Status:** Complete, ready for expansion
**Version:** 0.1.0
**Lines:** ~500
**Key Features:**
- eOS v0.1 compliant
- Virus-free (no embedded entities)
- Complete workflow documentation
- Policy enforcement (ROTG + DND)
- Capabilities: parse_spec, build_hierarchy, create_entities, validate_outputs, log_operations

### 2. Spec Document Template
**File:** `.deia/templates/spec/llh-org-spec.md`
**Status:** Complete template with placeholders
**Version:** 0.1.0
**Format:** YAML front matter + Markdown body
**Supports:**
- LLHs (organizational units)
- TAGs (cross-functional teams)
- Drones (automated workers)
- Hierarchies (parent/child relationships)
- Routing configuration
- Build options

### 3. Spec Parser
**File:** `.deia/tools/spec_parser.py`
**Status:** Complete, tested
**Version:** 0.1.0
**Lines:** ~360
**Features:**
- YAML front matter parser
- Markdown body extraction
- Entity validation
- Spec validation
- CLI interface
**Executable:** ✅ chmod +x applied

### 4. Factory Builder
**File:** `.deia/tools/llh_factory_build.py`
**Status:** Complete, ready to use
**Version:** 0.1.0
**Lines:** ~440
**Features:**
- Spec-based entity creation
- Template rendering with variables
- Multi-entity type support (LLH/TAG/drone)
- Human approval workflow
- Dry-run mode
- RSE logging
- Validation integration
**Executable:** ✅ chmod +x applied

### 5. Documentation
**Files:**
- `.deia/STATUS-LLH-FACTORY-EGG.md` (design & status)
- `.deia/docs/FACTORY-PATTERN.md` (usage guide)

**Status:** Complete documentation
**Coverage:**
- Problem statement
- Design decisions
- Complete workflow
- Spec format reference
- Tool usage examples
- Troubleshooting guide

### 6. Supporting Tools (Existing)
**Already in place:**
- `.deia/tools/egg_expand.py` (egg expansion)
- `.deia/tools/llh_hatch.sh|ps1` (legacy hatching, still works)
- `.deia/tools/llh_validate.py` (entity validation)
- `.deia/tools/builder_launch.sh|ps1` (orchestration)

## Pre-Hatch Checklist

### Files Exist and Complete
- [x] `.deia/templates/egg/llh-factory-egg.md`
- [x] `.deia/templates/spec/llh-org-spec.md`
- [x] `.deia/tools/spec_parser.py`
- [x] `.deia/tools/llh_factory_build.py`
- [x] `.deia/STATUS-LLH-FACTORY-EGG.md`
- [x] `.deia/docs/FACTORY-PATTERN.md`

### Files are Executable
- [x] `.deia/tools/spec_parser.py` (chmod +x)
- [x] `.deia/tools/llh_factory_build.py` (chmod +x)
- [x] `.deia/tools/egg_expand.py` (existing)

### Documentation Complete
- [x] Factory pattern explained
- [x] Workflow documented
- [x] Examples provided
- [x] Troubleshooting guide included

### Safety Measures in Place
- [x] DND policy enforced (no overwrites)
- [x] Human approval required (unless --force)
- [x] Dry-run mode available
- [x] RSE logging enabled
- [x] Validation integration

### Known State
- [x] No entities currently in `.deia/.projects/` from factory
- [x] Templates are clean (virus-free)
- [x] Tools are untested in production (first use)

## Instructions for First Hatch

### Option A: Test with Example (Recommended)

**Step 1:** Create test spec
```bash
# Create test directory
mkdir -p .deia/.projects/test-org

# Create simple spec
cat > .deia/.projects/test-org/spec.md << 'EOF'
---
spec_version: "0.1"
project: test-org
author: dave
created: 2025-10-15

entities:
  llhs:
    - id: test-llh
      title: "Test LLH"
      structure: flat

  tags:
    - id: test-tag
      title: "Test TAG"
      parent: test-llh
      deadline: "2025-12-31"

routing:
  llhs: ".deia/.projects/test-org_001/llhs/"
  tags: ".deia/.projects/test-org_001/tag-teams/"
---

# Test Organization

Simple test to validate factory pattern.
EOF
```

**Step 2:** Validate spec
```bash
python .deia/tools/spec_parser.py .deia/.projects/test-org/spec.md
```

**Step 3:** Dry run (no files created)
```bash
python .deia/tools/llh_factory_build.py \
  --spec .deia/.projects/test-org/spec.md \
  --dry-run
```

**Step 4:** Real build
```bash
python .deia/tools/llh_factory_build.py \
  --spec .deia/.projects/test-org/spec.md
# Approve when prompted
```

**Step 5:** Validate outputs
```bash
python .deia/tools/llh_validate.py \
  .deia/.projects/test-org_001/llhs/*.md \
  .deia/.projects/test-org_001/tag-teams/*.md
```

**Step 6:** Review and commit
```bash
ls -la .deia/.projects/test-org_001/
cat .deia/.projects/test-org_001/llhs/test-llh.md
cat .deia/telemetry/rse.jsonl | tail -5
```

### Option B: Expand Egg First (Proper Pattern)

**Step 1:** Expand factory egg
```bash
python .deia/tools/egg_expand.py \
  .deia/templates/egg/llh-factory-egg.md
# Creates .deia/.projects/llh-factory_001/
```

**Step 2:** Create spec in project
```bash
# Copy template and edit
cp .deia/templates/spec/llh-org-spec.md \
   .deia/.projects/my-project/spec.md

# Edit spec.md with your entities
```

**Step 3:** Build from expanded egg directory
```bash
cd .deia/.projects/llh-factory_001/
python ../../tools/llh_factory_build.py \
  --spec ../my-project/spec.md
```

## Rollback Plan

**If something goes wrong:**

1. **Review what was created:**
   ```bash
   find .deia/.projects -name "*.md" -mmin -10
   ```

2. **Check RSE log:**
   ```bash
   tail -20 .deia/telemetry/rse.jsonl
   ```

3. **Archive created files (DND):**
   ```bash
   timestamp=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
   mkdir -p .deia/archive/failed-hatch-$timestamp
   mv .deia/.projects/problem_001/ \
      .deia/archive/failed-hatch-$timestamp/
   ```

4. **Templates are preserved** - Always in `.deia/templates/`

5. **Tools are preserved** - Always in `.deia/tools/`

6. **This document is preserved** - DND policy

## Recovery Information

**If templates corrupted:**
- This document contains full file paths
- All files committed to git (can git checkout)
- Documentation describes complete design

**If tools fail:**
- Check Python version: `python --version` (need 3.9+)
- Check file permissions: `ls -l .deia/tools/*.py`
- Run with verbose errors: `python -v .deia/tools/spec_parser.py`

**If validation fails:**
- Run spec_parser first: `python .deia/tools/spec_parser.py spec.md`
- Check YAML syntax (indentation matters!)
- Verify required fields present

## Post-Hatch Actions

**After successful first hatch:**

1. **Document results:**
   - Create `.deia/HATCH-REPORT-[timestamp].md`
   - Note any issues encountered
   - Record any tool improvements needed

2. **Update status:**
   - Mark STATUS-LLH-FACTORY-EGG.md as "tested"
   - Note first hatch date/time
   - Record any adjustments made

3. **Review RSE:**
   - Check `.deia/telemetry/rse.jsonl`
   - Verify all events logged correctly
   - Confirm no errors

4. **Validate:**
   - Run llh_validate.py on all outputs
   - Ensure eOS compliance
   - Check file structure

5. **Commit:**
   - Git add created files
   - Commit with descriptive message
   - Include hatch report in commit

## Contact Information

**Created By:** Claude (Anthropic, Bee Queen)
**Requested By:** Dave
**Session:** 2025-10-15
**LLH Reference:** gpt-llama-bot-eos-companion.md

## Related Documents

- **Factory Egg:** `.deia/templates/egg/llh-factory-egg.md`
- **Status:** `.deia/STATUS-LLH-FACTORY-EGG.md`
- **Documentation:** `.deia/docs/FACTORY-PATTERN.md`
- **Spec Template:** `.deia/templates/spec/llh-org-spec.md`
- **RCA:** `.deia/incidents/RCA-2025-10-15-llh-builder-eggs.md`

---

**Preservation Complete:** 2025-10-15
**Status:** Pre-hatch checkpoint recorded
**Policy:** DND - Do not delete this preservation record
**Next Step:** Proceed with first hatch per instructions above
