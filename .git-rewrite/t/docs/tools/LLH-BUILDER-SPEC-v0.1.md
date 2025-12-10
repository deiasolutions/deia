# LLH Builder Specification v0.1

**Purpose:** Define the contract for hatching, validating, and emitting LLHs (Limited Liability Hives), TAGs (Together And Good teams), and Eggs (unborn LLHs/TAGs).

**Author:** Claude (Anthropic, Bee Queen)
**Date:** 2025-10-15
**Status:** Draft v0.1
**DND:** All operations additive; no destructive changes allowed.

---

## 1. Scope

The **LLH Builder** is a toolset for creating, validating, and emitting DEIA organizational entities:

- **LLH (Limited Liability Hive)**: Institutional actor with governance constraints, member bees, and coordination protocols
- **TAG (Together And Good)**: Ephemeral coalition with TTL, members from multiple LLHs, and specific mission
- **Egg**: Unborn/draft LLH or TAG awaiting activation

### Operations

1. **Hatch**: Create new entity from template (LLH/TAG/Egg)
2. **Validate**: Schema check, routing correctness, policy compliance
3. **Emit**: Log creation to RSE, CHANGELOG; route to proper directory

---

## 2. Entity Schemas

### 2.1 LLH Schema

**File format:** `.deia/projects/<project-name>/llhs/<llh-id>.md`

Example: `.deia/projects/federal_government_simulation/llhs/house-llh.md`

**YAML Front Matter (Required):**
```yaml
---
id: <kebab-case-id>
type: llh
name: "Display Name"
governance:
  structure: <hierarchy|flat|federated>
  decision_mode: <consensus|majority|executive>
  transparency: <public|members-only|private>
members:
  - bee-id-1
  - bee-id-2
constraints: [constraint-1, constraint-2]
capacities: {budget: medium, attention: high, staff_cycles: medium}
coordination:
  pheromones: [pheromone-type-1, pheromone-type-2]
  meeting_cadence: <daily|weekly|monthly>
created: 2025-10-15
status: <active|dormant|archived>
---
```

**Body:** Markdown description of purpose, scope, operational procedures, member roles.

---

### 2.2 TAG Schema

**File format:** `.deia/projects/<project-name>/tag-teams/<tag-id>.md`

Example: `.deia/projects/federal_government_simulation/tag-teams/appropriations-2025-tag.md`

**YAML Front Matter (Required):**
```yaml
---
id: <kebab-case-id>
type: tag
name: "Display Name"
mission: "One-line mission statement"
members:
  - actor-id-1
  - actor-id-2
ttl: 2025-12-31  # Time to live (expiration date)
created: 2025-10-15
status: <active|paused|completed|expired>
parent_llhs: [llh-1, llh-2]  # Source LLHs
outputs: [deliverable-1, deliverable-2]
---
```

**Body:** Markdown description of mission, member roles, coordination protocol, success criteria.

---

## Filing

**Filed:** `docs/tools/LLH-BUILDER-SPEC-v0.1.md`
**Status:** Specification draft
**Tags:** `#llh-builder` `#tooling` `#deia`
