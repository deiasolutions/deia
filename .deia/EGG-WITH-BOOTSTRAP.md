---
title: Factory Egg Now Includes DEIA Bootstrap Instructions
date: 2025-10-16
author: Claude (Anthropic)
status: documentation
policy: DND
---

# Factory Egg Now Includes DEIA Bootstrap Instructions

## What Changed

Added comprehensive "DEIA Environment Setup (For AI Agents)" section to the factory egg:
`.deia/templates/egg/llh-factory-egg.md`

## What's Included

### 1. Prerequisites Check
- Lists required directory structure
- Commands to verify DEIA layout exists

### 2. Initialize DEIA Structure
```bash
mkdir -p .deia/{tools,templates/{llh,tag,egg,eos-pack},eos-packs,telemetry,commons,.projects}
touch .deia/telemetry/rse.jsonl
touch .deia/commons/CHANGELOG.md
```

### 3. Required Commons Tools Documentation
Full specifications for:
- **llh_factory_build.py** - What it does, where it lives, what to do if missing
- **spec_parser.py** - Purpose, location, fallback guidance
- **llh_validate.py** - Validation role, location, reference docs

### 4. Required Templates (With Examples)
Complete template snippets embedded in egg:
- **LLH Template** - Full YAML front matter example with placeholders
- **TAG Template** - Complete structure with {{VARIABLES}}
- **eOS Pack Template** - Reference to full template location

### 5. Verification Steps
Step-by-step commands to test the environment:
```bash
# Check tools
ls -la .deia/tools/*.py

# Check templates
ls -la .deia/templates/{llh,tag}/*.md

# Test parsing
python .deia/tools/spec_parser.py .deia/eos-packs/example-startup.yaml

# Dry run
python .deia/tools/llh_factory_build.py --eos-pack example.yaml --dry-run
```

### 6. Quickstart: Create Your First Organization
Complete working example an AI can run immediately:
- Creates test eOS pack
- Builds organization
- Validates outputs
- Reviews results

Includes actual shell commands with heredoc for eOS pack creation.

### 7. Missing Tools Guidance
What to do if commons tools aren't found:
- Check git status
- Pull latest
- Use find command to locate
- Consult documentation references

### 8. AI Agent Self-Check
8-point checklist for AI agents:
1. ✅ Read and parse egg
2. ✅ Locate commons tools
3. ✅ Load templates
4. ✅ Parse eOS packs
5. ✅ Create entities
6. ✅ Validate outputs
7. ✅ Log to RSE
8. ✅ Follow DND policy

## Why This Matters

### For AI Agents
An AI encountering the DEIA system for the first time can now:
1. Read the factory egg
2. Understand the entire DEIA pattern
3. Bootstrap a complete environment from scratch
4. Verify everything works
5. Create their first organization

**Self-contained onboarding** - No external documentation required to get started.

### For Humans
The egg serves as:
- Quick reference for DEIA structure
- Setup guide for new contributors
- Verification checklist for environments
- Troubleshooting guide

## Example AI Agent Flow

```
AI Agent encounters factory egg →
  Reads "DEIA Environment Setup" section →
    Runs prerequisites check →
      Missing tools? Follow setup instructions →
        Verify with test commands →
          Run quickstart example →
            ✅ First organization created!
```

## What the Egg Now Contains

1. **eOS Manifest** - System metadata
2. **Three-Component Pattern** - Architecture explanation
3. **What This Egg Does** - Purpose and capabilities
4. **🆕 DEIA Environment Setup** - Bootstrap instructions
5. **Virus Prevention** - Security model
6. **Workflow** - Step-by-step usage
7. **Capabilities** - Entity types, hierarchies
8. **eOS Compliance** - ROTG/DND policies
9. **Security & Safety** - Guardrails
10. **eOS Pack Format** - Data structure examples
11. **Factory Builder Logic** - How it works (references commons)
12. **Customization** - Advanced features
13. **Troubleshooting** - Common issues
14. **Related Tools** - Tool ecosystem
15. **Version History** - Change log
16. **References** - Documentation links

## Key Principles Maintained

### ✅ Egg Remains Minimal
- No executable code in egg
- No entity definitions in egg
- Only **instructions and references**

### ✅ Self-Contained Bootstrap
- AI can start from zero
- All necessary info in one place
- Clear fallback strategies

### ✅ Separation of Concerns
- Egg = orchestration instructions
- eOS Pack = project data
- Commons = executable code

### ✅ Virus-Free
- Instructions ≠ execution
- References ≠ embedding
- Bootstrap ≠ infection

## Testing the Bootstrap

An AI can verify the bootstrap works:

```bash
# 1. Start in empty directory
mkdir test-deia && cd test-deia

# 2. Copy just the egg
cp /path/to/llh-factory-egg.md .

# 3. Read egg and follow setup instructions
# (AI reads egg, sees "DEIA Environment Setup" section)

# 4. Execute setup commands from egg
mkdir -p .deia/{tools,templates/{llh,tag,egg,eos-pack},eos-packs,telemetry,commons,.projects}
touch .deia/telemetry/rse.jsonl

# 5. Notice tools missing
ls .deia/tools/  # Empty!

# 6. Follow "If Commons Tools Are Missing" guidance
git clone <repo-url>
# Or consult documentation references

# 7. Verify and run quickstart
python .deia/tools/llh_factory_build.py --eos-pack test.yaml
```

## Documentation Consistency

The egg now aligns with:
- **EGG-SPECIFICATION.md** - Formal spec
- **FACTORY-PATTERN.md** - Pattern documentation
- **LLH-FACTORY-READY.md** - Readiness checklist

All three documents cross-reference each other.

## Location

**Updated File:**
`.deia/templates/egg/llh-factory-egg.md`

**New Section Added:**
Starting at line ~59, inserted ~220 lines of DEIA environment setup guidance.

**Section Title:**
"## DEIA Environment Setup (For AI Agents)"

## Related Documents

- **Egg Source:** `.deia/templates/egg/llh-factory-egg.md`
- **Egg Specification:** `.deia/docs/EGG-SPECIFICATION.md`
- **Factory Pattern:** `.deia/docs/FACTORY-PATTERN.md`
- **Ready Status:** `.deia/LLH-FACTORY-READY.md`
- **eOS Pack Template:** `.deia/templates/eos-pack/llh-org-eos-pack.yaml`
- **Example Pack:** `.deia/eos-packs/example-startup.yaml`

## Summary

The factory egg is now a **complete onboarding document** that enables:

1. **AI Agents** - Can bootstrap DEIA environment from scratch
2. **Humans** - Have quick reference and setup guide
3. **Both** - Understand the entire pattern in one file

**Self-contained, self-documenting, self-sufficient** - The egg embodies the DEIA philosophy of clear separation and explicit instruction.

---

**Created:** 2025-10-16
**Author:** Claude (Anthropic, Bee Queen)
**Policy:** DND
