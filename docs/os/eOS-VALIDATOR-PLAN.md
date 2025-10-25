# eOS Validator Integration Plan

**Purpose:** Plan for integrating `eos` manifest validation into existing entity validators.

**Author:** Claude (Anthropic, Bee Queen)
**Date:** 2025-10-15
**Status:** Plan (Whisperwing already implemented)

---

## 1. Current State

**Validator:** `.deia/tools/llh_validate.py`

**Status:** ✓ Updated by Whisperwing (2025-10-15T21:14:29Z)
- Accepts `eos` block
- Handles `type`/`kind` aliases
- Handles `name`/`title` aliases
- Supports `routing` validation
- Multi-file validation support

**Change Log (RSE):**
```json
{"ts":"2025-10-15T21:14:29.0325748Z","type":"tool_updated","lane":"Process","actor":"Whisperwing","data":{"path":".deia/tools/llh_validate.py","change":"accept eos, type/kind, name/title, routing aliases; multi-file"}}
```

---

## 2. Validation Requirements

### 2.1 eOS Manifest Validation

**Required Fields:**
- `eos` — Version string (e.g., `"0.1"`)
- `kind` — Enum: `egg`, `llh`, `tag`, `service`
- `id` — Unique kebab-case identifier
- `policy.rotg` — Boolean or `"inherited"`
- `policy.dnd` — Boolean
- `routing.project` — Project namespace
- `routing.destination` — Enum: `llhs`, `tag-teams`, `eggs`, `archive`
- `routing.action` — Enum: `hatch`, `spawn`, `archive`, `activate`

**Optional Fields:**
- `caps` — Array of capabilities
- `routing.filename` — Override filename

### 2.2 Backward Compatibility

**Legacy Entities (no `eos` block):**
- Phase 1: Accept entities with or without `eos` (grace period)
- Phase 2: Emit warnings for entities without `eos`
- Phase 3: Require `eos` block (reject entities without it)

**Current Phase:** Phase 1 (grace period)

### 2.3 Policy Enforcement

**ROTG Validation:**
- Check `policy.rotg` is `true` or `"inherited"`
- If `false`: Emit warning (potential policy violation)

**DND Validation:**
- Check `policy.dnd` is `true` (append-only)
- If `false`: Emit warning (destructive operations allowed - risky)

### 2.4 Routing Validation

**Path Correctness:**
- Verify file path matches `routing.project` + `routing.destination`
- Example: File at `.deia/projects/federal_government_simulation/llhs/house-llh.md` should have:
  ```yaml
  routing:
    project: federal_government_simulation
    destination: llhs
  ```

---

## 3. Implementation Plan (Completed by Whisperwing)

### Phase 1: Accept `eos` Block (✓ Done)

**Changes:**
- Accept `eos` field in YAML front matter
- Parse `eos.kind`, `eos.id`, `eos.policy`, `eos.routing`
- Allow `type`/`kind` aliases (backward compatibility)
- Allow `name`/`title` aliases (backward compatibility)

### Phase 2: Validate `eos` Fields (✓ Done)

**Validations:**
- Check `eos` version compatibility
- Validate `kind` enum
- Validate `policy.rotg` and `policy.dnd`
- Validate `routing.project`, `routing.destination`, `routing.action`

### Phase 3: Routing Validation (✓ Done)

**Validations:**
- Check file path matches routing declaration
- Emit warnings for mismatched paths

### Phase 4: Multi-File Support (✓ Done)

**Feature:**
- Validate multiple files in one command
- Batch validation for project-wide checks

---

## 4. Validator Output Format

**JSON Output:**
```json
{
  "ok": true,
  "entity_type": "llh",
  "eos_version": "0.1",
  "errors": [],
  "warnings": [],
  "path": ".deia/projects/federal_government_simulation/llhs/house-llh.md",
  "manifest": {
    "kind": "llh",
    "id": "house-llh",
    "policy": {"rotg": true, "dnd": true},
    "routing": {
      "project": "federal_government_simulation",
      "destination": "llhs",
      "action": "activate"
    }
  }
}
```

---

## 5. Migration Path

### 5.1 Existing Entities (No `eos` Block)

**Current State:**
- Entities in `.deia/projects/federal_government_simulation/{llhs,tag-teams}/`
- No `eos` manifest

**Migration:**
1. Add `eos` block to existing entities (backfill)
2. Run validator to confirm compliance
3. Log updates to RSE + CHANGELOG

**Example:** See backfill of `house-llh.md` in this session

### 5.2 New Entities

**Requirement:**
- All new entities MUST include `eos` manifest
- Templates updated to include `eos` block by default

---

## 6. Testing

### 6.1 Valid Entity (with `eos`)

```bash
python .deia/tools/llh_validate.py .deia/projects/federal_government_simulation/llhs/house-llh.md
# → {"ok": true, "eos_version": "0.1", ...}
```

### 6.2 Legacy Entity (no `eos`)

```bash
python .deia/tools/llh_validate.py .deia/projects/federal_government_simulation/llhs/legacy-llh.md
# → {"ok": true, "warnings": ["missing_eos_manifest"], ...}
```

### 6.3 Invalid `eos` Manifest

```bash
python .deia/tools/llh_validate.py .deia/projects/federal_government_simulation/llhs/bad-llh.md
# → {"ok": false, "errors": ["invalid_eos_kind", "missing_policy_rotg"], ...}
```

---

## 7. Filing

**Path:** `docs/os/eOS-VALIDATOR-PLAN.md`
**Status:** Plan (implementation complete)
**Tags:** `#eos` `#validator` `#plan` `#deia`

---

## References

- eOS Spec: `docs/os/eOS-SPEC-v0.1.md`
- Validator: `.deia/tools/llh_validate.py`
- RSE Event: Line 46 in `.deia/telemetry/rse.jsonl`
