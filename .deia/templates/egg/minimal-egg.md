---
eos: "0.1"
kind: egg
id: llh-simulation-004
entity_type: llh
name: "LLH Simulation 004"
proposed_by: dave
created: 2025-10-15
status: draft
policy:
  rotg: true
  dnd: true
caps: [hatch_llh, validate_schema]
routing:
  project: simulation_004
  destination: eggs
  filename: llh_simulation_004.md
  action: hatch
hatch_date: null
version: 0.1.0
notes: "Clean minimal seed egg - no embedded entity definitions"
---

# Egg: LLH Simulation 004 (Minimal Seed)

## What is a Minimal Seed?

A **minimal seed egg** is a clean, virus-free template for creating LLH simulations. It contains:

✅ **eOS v0.1 manifest** (proper kernel compliance)
✅ **Policy enforcement** (ROTG + DND)
✅ **Routing instructions** (where to hatch)
✅ **Placeholder sections** (objectives, entities, scenarios)

❌ **NO embedded entity definitions** (no hard-coded House/Senate/federal entities)
❌ **NO builder code** (code lives in DEIA Global Commons: `.deia/tools/`)
❌ **NO project data** (project blueprints in eOS packs, not eggs)

## Three-Component Pattern (Virus-Free)

1. **Egg (minimal bootstrap)** → `.deia/templates/egg/minimal-egg.md`
2. **eOS Pack (project blueprint)** → `.deia/eos-packs/<project-id>.yaml`
3. **DEIA Global Commons** → `.deia/tools/llh_factory_build.py`, `.deia/templates/`

**Build Process:**
```bash
# Expand egg
python .deia/tools/egg_expand.py .deia/templates/egg/llh-factory-egg.md

# Build from eOS pack
python .deia/tools/llh_factory_build.py --eos-pack .deia/eos-packs/<project>.yaml
```

This prevents viral hijacking where executable code or entity definitions are embedded in eggs.

---

## Sections

### Objectives

[Define simulation objectives - what are you modeling or testing?]

### Entities (LLHs, TAGs)

[List entities to create - define in eOS pack, NOT here]

### Scenarios & Deadlines

[Define scenarios, timelines, success criteria]

### Open Questions

[Track unresolved questions]

---

**Proposed by:** dave
**Created:** 2025-10-15
**Status:** Draft
**Version:** 0.1.0

