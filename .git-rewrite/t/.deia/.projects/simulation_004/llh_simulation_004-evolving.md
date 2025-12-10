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
notes: "Clean minimal seed egg - no government DNA viruses"
---

# Egg: LLH Simulation 004 (Minimal Seed)

## What is a Minimal Seed?

A **minimal seed egg** is a clean, virus-free template for creating LLH simulations. It contains:

✅ **eOS v0.1 manifest** (proper kernel compliance)
✅ **Policy enforcement** (ROTG + DND)
✅ **Routing instructions** (where to hatch)
✅ **Placeholder sections** (objectives, entities, scenarios)

❌ **NO government DNA viruses** (no embedded House/Senate/federal entity commands)
❌ **NO uncontained instructions** (no direct llh_hatch.sh commands in egg body)
❌ **NO pre-loaded genetic blueprints** (DNA injected separately, not hard-coded)

## Proper Pattern (Virus-Free)

1. **Create DNA pack** (genetic blueprint) → `.deia/dna/<dna-pack-id>.yaml`
2. **Inject DNA into egg** → `dna_inject.sh --egg llh-simulation-004 --dna <dna-pack-id>`
3. **Hatch egg** → `builder_launch.sh --egg llh-simulation-004 --action hatch`

This prevents viral hijacking where loose instructions execute directly instead of being properly contained in genetic blueprints.

---

## Sections

### Objectives

[Define simulation objectives - what are you modeling or testing?]

### Entities (LLHs, TAGs)

[List entities to create - define via DNA injection, NOT here]

### Scenarios & Deadlines

[Define scenarios, timelines, success criteria]

### Open Questions

[Track unresolved questions]

---

**Proposed by:** dave
**Created:** 2025-10-15
**Status:** Draft
**Version:** 0.1.0

