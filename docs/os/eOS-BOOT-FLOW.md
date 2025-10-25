# eOS Boot Flow Documentation

**Purpose:** Detailed boot sequence for eOS (Ephemeral OS) entity lifecycle.

**Author:** Claude (Anthropic, Bee Queen)
**Date:** 2025-10-15
**Status:** Draft v0.1

---

## 1. Overview

eOS follows an **egg-first architecture** where all entities begin as eggs (genetic blueprints in incubation) and progress through a formal boot sequence to become active processes (LLHs, TAGs, Services).

---

## 2. Boot Sequence

### Phase 1: Builder Launch

**Entry Point:** `builder_launch.{ps1,sh}`

**Actions:**
1. Locate egg file in `.deia/projects/<project>/eggs/<egg-id>.md`
2. Read YAML front matter
3. Parse `eos` manifest block
4. Validate `eos` version compatibility (current: `0.1`)
5. Check kernel policy (`rotg`, `dnd`)
6. Load egg into memory

**Exit Condition:** Egg loaded and manifest parsed ✓

**Failures:**
- **Egg not found:** Abort with error log
- **Invalid eos manifest:** Abort, emit RSE warning
- **Policy violation:** Abort, log to Governance lane

---

### Phase 2: Egg Expand

**Entry Point:** `egg_expand.{ps1,sh}` (called by `builder_launch`)

**Actions:**
1. **Parse eos Manifest:**
   - Extract `kind`, `id`, `policy`, `caps`, `routing`

2. **Validate Policy:**
   - **ROTG Check:** Ensure `policy.rotg` is `true` or `inherited`
   - **DND Check:** Ensure `policy.dnd` is `true` (append-only)
   - If violations found: Abort, log to Governance lane

3. **Capability Check:**
   - Verify `caps` array is valid
   - Check if egg has required capabilities for action (e.g., `hatch_llh` for `action: hatch`)

4. **Extract Genetic Blueprint (if present):**
   - Look for DNA/genome section in egg body
   - Parse traits, lineage, mutations
   - Prepare for injection into spawned entity

5. **Route Decision:**
   - Determine target path: `routing.project` + `routing.destination`
   - Example: `.deia/projects/federal_government_simulation/llhs/`

**Exit Condition:** Egg expanded, routing determined ✓

**Failures:**
- **Policy violation:** Archive egg (DND), log incident
- **Invalid routing:** Abort, request manual routing
- **Missing capabilities:** Abort, log warning

---

### Phase 3: Hatch

**Entry Point:** Triggered by `routing.action: hatch`

**Actions:**
1. **Create Entity File:**
   - Path: `{routing.project}/{routing.destination}/{routing.filename or id}.md`
   - Example: `.deia/projects/federal_government_simulation/llhs/house-llh.md`

2. **Inject Genetic Traits (if DNA present):**
   - Apply traits from genetic blueprint
   - Set lineage pointers
   - Apply mutations (specialization)

3. **Write YAML Front Matter:**
   - Copy `eos` manifest from egg
   - Add entity-specific fields (`type: llh`, `governance`, `members`, etc.)
   - Set `status: draft` initially

4. **Write Markdown Body:**
   - Include purpose, scope, operational procedures
   - Reference parent egg (provenance)

5. **Set Initial Status:**
   - `draft` → Awaiting validation
   - `active` → Ready for execution (post-validation)

**Exit Condition:** Entity file created ✓

**Failures:**
- **File exists (DND violation):** Abort, log error
- **Write failure:** Abort, roll back (mark egg as failed)

---

### Phase 4: Validate

**Entry Point:** `llh_validate.py` or `tag_validate.py`

**Actions:**
1. **Schema Validation:**
   - Check YAML front matter structure
   - Verify required fields (`id`, `type`, `eos`, etc.)

2. **eOS Manifest Validation:**
   - Verify `eos` block present and valid
   - Check `kind` matches entity `type`
   - Validate `policy.rotg` and `policy.dnd`
   - Verify `routing` correctness

3. **Policy Compliance:**
   - ROTG: Check for rule violations in entity definition
   - DND: Ensure no destructive operations in lifecycle

4. **Capability Verification:**
   - Check if declared `caps` are valid for `kind`
   - Example: LLH can have `emit_pheromone`, but not `delete_llh`

**Exit Condition:** Validation passed ✓

**Failures:**
- **Schema error:** Entity remains `draft`, emit validation report
- **Policy violation:** Archive entity (DND), log incident
- **eOS manifest invalid:** Reject entity, log warning

---

### Phase 5: Log

**Entry Point:** Automatic after successful hatch + validation

**Actions:**
1. **Emit RSE Event:**
   ```json
   {"ts":"2025-10-15T21:00:00Z","type":"llh_hatched","lane":"Process","actor":"builder_launch","data":{"id":"house-llh","project":"federal_government_simulation","egg":"congress-bicameral-egg"}}
   ```

2. **Append to CHANGELOG:**
   ```markdown
   2025-10-15T21:00:00Z — eOS (builder_launch)
   - Hatched LLH: house-llh (project: federal_government_simulation)
   - Parent egg: congress-bicameral-egg
   - Status: active
   - DND honored; additive spawn
   ```

3. **Update Egg Status:**
   - Mark egg as `hatched` (status field in egg)
   - Keep egg file (DND: archive, don't delete)

**Exit Condition:** Logged to RSE + CHANGELOG ✓

---

### Phase 6: Exec (Activation)

**Entry Point:** Triggered by `status: active` (post-validation)

**Actions:**
1. **Initialize Process:**
   - LLH: Begin coordination via RSE (emit pheromones, respond to signals)
   - TAG: Join coordination with parent LLHs, start mission
   - Service: Start daemon loop (monitoring, scheduling, etc.)

2. **Register with Scheduler:**
   - Add to DEIA Clock (if time-based triggers needed)
   - Add to QEE (if task queue needed)

3. **Emit Ready Signal:**
   ```json
   {"ts":"2025-10-15T21:00:05Z","type":"llh_ready","lane":"Coordination","actor":"house-llh","data":{"caps":["emit_pheromone","spawn_tag","coordinate_rse"]}}
   ```

4. **Begin IPC:**
   - Listen for RSE events on relevant lanes
   - Respond to pheromones from other entities
   - Coordinate with TAGs/LLHs as needed

**Exit Condition:** Entity active and coordinating ✓

**Failures:**
- **Initialization error:** Set status to `dormant`, log incident
- **Capability conflict:** Archive entity (DND), log error

---

## 3. Boot Flow Diagram

```
┌─────────────────┐
│  Egg (draft)    │
│  .eggs/<id>.md  │
└────────┬────────┘
         │
         ▼
   ┌─────────────────────┐
   │ 1. builder_launch   │ ◄─── Entry point
   │    - Load egg       │
   │    - Parse eos      │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │ 2. egg_expand       │
   │    - Validate       │
   │    - Route          │
   │    - Extract DNA    │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │ 3. hatch            │
   │    - Create file    │
   │    - Inject traits  │
   │    - Write YAML     │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │ 4. validate         │
   │    - Schema check   │
   │    - Policy check   │
   │    - eos manifest   │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │ 5. log              │
   │    - RSE event      │
   │    - CHANGELOG      │
   │    - Update egg     │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │ 6. exec (activate)  │
   │    - Initialize     │
   │    - Register       │
   │    - Begin IPC      │
   └─────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│ Active Process (LLH)   │
│ Status: active         │
│ Coordinating via RSE   │
└────────────────────────┘
```

---

## 4. Boot Variants

### 4.1 Egg → LLH (Standard)

```bash
builder_launch.sh --egg congress-bicameral-egg --action hatch
# → .deia/projects/federal_government_simulation/llhs/house-llh.md
```

**Sequence:** Load → Expand → Hatch → Validate → Log → Exec

---

### 4.2 Egg → TAG (Ephemeral)

```bash
builder_launch.sh --egg border-funding-egg --action spawn
# → .deia/projects/federal_government_simulation/tag-teams/appropriations-2025-tag.md
```

**Sequence:** Load → Expand → Spawn → Validate → Log → Exec (with TTL)

**TTL Monitoring:** DEIA Clock monitors `ttl` field, expires TAG when due

---

### 4.3 Egg → Archive (Aborted)

```bash
# If policy violation detected during expand:
# → .deia/projects/federal_government_simulation/archive/2025-10-15/infected-egg.md
```

**Sequence:** Load → Expand → **Policy Violation** → Archive → Log (incident)

**DND:** Egg archived, not deleted (forensic value)

---

## 5. Error Handling

### 5.1 Policy Violations

**Scenario:** Egg contains uncontained instructions (virus)

**Boot Response:**
1. Detect during `egg_expand` (Phase 2)
2. Abort boot sequence
3. Archive egg to `.deia/projects/<project>/archive/<date>/`
4. Log incident to RSE (Governance lane)
5. Create RCA (Root Cause Analysis) in `.deia/incidents/`

**DND Compliance:** Egg archived, not deleted

---

### 5.2 Validation Failures

**Scenario:** Entity fails schema/policy validation (Phase 4)

**Boot Response:**
1. Keep entity in `draft` status
2. Emit validation report (JSON)
3. Log warning to RSE (Process lane)
4. Do NOT activate entity (skip Phase 6)

**Resolution:** Manual fix + re-validate

---

### 5.3 Duplicate Entity (DND Violation)

**Scenario:** Entity file already exists at target path

**Boot Response:**
1. Detect during `hatch` (Phase 3)
2. Abort boot sequence
3. Log error to RSE (Governance lane)
4. Mark egg as `hatch_failed`

**DND Compliance:** Do not overwrite existing file

---

## 6. Boot Configuration

**Environment Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `EOS_VERSION` | `0.1` | Target eOS version for boot |
| `EOS_PROJECT` | (required) | Target project namespace |
| `EOS_VALIDATE` | `true` | Run validation after hatch |
| `EOS_ACTIVATE` | `true` | Auto-activate after validation |
| `EOS_DND_ENFORCE` | `true` | Enforce DND policy (no overwrites) |

**Example:**
```bash
EOS_PROJECT=federal_government_simulation \
EOS_VALIDATE=true \
builder_launch.sh --egg congress-bicameral-egg
```

---

## 7. Filing

**Path:** `docs/os/eOS-BOOT-FLOW.md`
**Status:** Documentation draft
**Tags:** `#eos` `#boot-flow` `#architecture` `#deia`

---

## References

- eOS Spec: `docs/os/eOS-SPEC-v0.1.md`
- LLH Builder: `docs/tools/LLH-BUILDER-SPEC-v0.1.md`
- Launchers: `.deia/tools/builder_launch.{ps1,sh}`
