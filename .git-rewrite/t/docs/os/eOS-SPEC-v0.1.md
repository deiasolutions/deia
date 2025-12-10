# eOS (Ephemeral OS) Specification v0.1

**Purpose:** Formalize DEIA's instruction layer as an operating system for ephemeral organizational entities.

**Author:** Claude (Anthropic, Bee Queen)
**Date:** 2025-10-15
**Status:** Draft v0.1
**DND:** All operations additive; no destructive changes allowed.

---

## 1. Overview

**eOS (Ephemeral OS)** is the operating system layer for DEIA (Distributed Ephemeral Institutional Architecture). It manages the lifecycle, coordination, and execution of organizational entities (Eggs, LLHs, TAGs) through a formal kernel, process model, and inter-process communication system.

### Core Principles

- **Egg-First Architecture:** All entities begin as eggs (genetic blueprints in incubation)
- **ROTG + DND Kernel:** Rules of the Game + Do Not Delete policy enforced at kernel level
- **Append-Only IPC:** All coordination via RSE (Routine State Events) in JSONL
- **Project Segmentation:** Workloads isolated in `.deia/projects/<name>/`
- **Manifest-Driven:** All entities declare capabilities, routing, and policy in front matter

---

## 2. eOS Architecture

### 2.1 Kernel

**Kernel Components:**
- **ROTG (Rules of the Game):** Constitutional constraints on entity behavior
- **DND (Do Not Delete):** Append-only mandate; archive instead of delete
- **Policy Enforcement:** Manifest validation before spawn/exec
- **Routing Engine:** Project-based filesystem routing

**Kernel Manifest:** All entities declare kernel compliance in `eos` block (YAML front matter)

### 2.2 Process Model

**Process Types:**

1. **Egg** — Unborn entity with genetic blueprint awaiting hatch
2. **LLH (Limited Liability Hive)** — Institutional actor process with governance
3. **TAG (Together And Good)** — Ephemeral coalition process with TTL
4. **Service** — Long-running daemon (future: bots, schedulers, monitors)

**Process Lifecycle:**
```
Egg (incubating) → builder_launch → expand → hatch → validate → active/dormant/archived
```

### 2.3 Inter-Process Communication (IPC)

**IPC Mechanism:** RSE (Routine State Events)

- **Format:** Append-only JSONL (`.deia/telemetry/rse.jsonl`)
- **Lanes:** Governance, Process, Coordination, Execution
- **Events:** `egg_created`, `llh_hatched`, `tag_spawned`, `pheromone_emitted`, etc.
- **Atomicity:** Each event is a single JSON line; no transaction rollback (append-only)

**Pheromones:** High-level coordination signals emitted by LLHs/TAGs via RSE

### 2.4 Scheduler

**Components:**
- **DEIA Clock:** Time-based event triggering (`.deia/clock/`)
- **QEE (Queue Execution Engine):** Task queue with priority and TTL
- **Egg Incubator:** Monitors eggs for hatch readiness

**Scheduling Policy:** Cooperative (entities self-report state; no preemption)

### 2.5 Filesystem

**eOS Filesystem Structure:**

```
.deia/
├── commons/            # Shared resources (CHANGELOG, manifests)
├── projects/           # Segmented workloads
│   └── <project-name>/
│       ├── llhs/       # Active LLH processes
│       ├── tag-teams/  # Active TAG processes
│       ├── eggs/       # Incubating eggs
│       └── archive/    # Archived entities (DND)
├── telemetry/
│   └── rse.jsonl       # IPC event log
├── clock/              # Scheduler state
└── tools/              # System utilities (builders, validators)
```

**Routing Rules:**
- Eggs route to `.deia/projects/<project>/eggs/`
- LLHs route to `.deia/projects/<project>/llhs/`
- TAGs route to `.deia/projects/<project>/tag-teams/`
- Archives route to `.deia/projects/<project>/archive/<date>/`

---

## 3. eOS Manifest (v0.1)

All entities MUST declare an `eos` block in YAML front matter.

### 3.1 Manifest Schema

```yaml
---
eos: 0.1
kind: <egg|llh|tag|service>
id: <kebab-case-unique-id>
policy:
  rotg: <true|false|inherited>
  dnd: <true|false>
caps: [capability-1, capability-2, ...]
routing:
  project: <project-name>
  destination: <llhs|tag-teams|eggs|archive>
  filename: <optional-override.md>
  action: <hatch|spawn|archive|activate>
---
```

### 3.2 Field Definitions

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `eos` | Yes | String | eOS version (e.g., `0.1`) |
| `kind` | Yes | Enum | Entity type: `egg`, `llh`, `tag`, `service` |
| `id` | Yes | String | Unique kebab-case identifier |
| `policy.rotg` | Yes | Boolean/String | Rules of the Game compliance (`true`, `false`, `inherited`) |
| `policy.dnd` | Yes | Boolean | Do Not Delete enforcement (`true` = append-only, `false` = destructive allowed) |
| `caps` | No | Array | Capabilities (e.g., `spawn_llh`, `emit_pheromone`, `read_rse`, `write_changelog`) |
| `routing.project` | Yes | String | Target project namespace (e.g., `federal_government_simulation`) |
| `routing.destination` | Yes | Enum | Filesystem destination: `llhs`, `tag-teams`, `eggs`, `archive` |
| `routing.filename` | No | String | Override default filename (default: `{id}.md`) |
| `routing.action` | Yes | Enum | Spawn action: `hatch`, `spawn`, `archive`, `activate` |

### 3.3 Example Manifest: Egg

```yaml
---
eos: 0.1
kind: egg
id: congress-bicameral-egg
policy:
  rotg: true
  dnd: true
caps: [hatch_llh, inject_dna, validate_schema]
routing:
  project: federal_government_simulation
  destination: eggs
  filename: congress-bicameral-egg.md
  action: hatch
---
```

### 3.4 Example Manifest: LLH

```yaml
---
eos: 0.1
kind: llh
id: house-llh
policy:
  rotg: inherited
  dnd: true
caps: [emit_pheromone, spawn_tag, coordinate_rse, vote, legislate]
routing:
  project: federal_government_simulation
  destination: llhs
  action: activate
---
```

### 3.5 Example Manifest: TAG

```yaml
---
eos: 0.1
kind: tag
id: appropriations-2025-tag
policy:
  rotg: inherited
  dnd: true
caps: [coordinate_llhs, emit_pheromone, deliver_output]
routing:
  project: federal_government_simulation
  destination: tag-teams
  action: spawn
ttl: 2025-12-31
---
```

---

## 4. Boot Flow

**eOS Boot Sequence (Egg-First):**

```
1. builder_launch
   └─> Load egg from .deia/projects/<project>/eggs/<egg-id>.md

2. egg_expand
   └─> Parse eos manifest
   └─> Validate policy (ROTG + DND)
   └─> Check capabilities
   └─> Extract genetic blueprint (if present)

3. hatch (if action=hatch)
   └─> Route to destination (routing.destination)
   └─> Instantiate entity (LLH/TAG based on kind)
   └─> Apply genetic traits (if DNA injected)
   └─> Set status: active

4. validate
   └─> Run llh_validate.py or tag_validate.py
   └─> Check eos manifest compliance
   └─> Verify routing correctness

5. log
   └─> Emit RSE event: {egg_hatched, llh_spawned, tag_created}
   └─> Append to CHANGELOG (additive)

6. exec (if status=active)
   └─> Entity begins coordination via RSE
   └─> Emits pheromones as needed
```

**See:** `docs/os/eOS-BOOT-FLOW.md` for detailed diagrams

---

## 5. Interoperability

### 5.1 RSE Lanes

eOS uses **RSE lanes** for IPC categorization:

- **Governance Lane:** Policy enforcement, ROTG violations, DND events
- **Process Lane:** Lifecycle events (spawn, hatch, archive, terminate)
- **Coordination Lane:** Pheromone emissions, TAG coordination, LLH signals
- **Execution Lane:** Task execution, QEE queue updates, Clock triggers

### 5.2 Clock Integration

**DEIA Clock** triggers time-based events:
- TAG TTL expiration
- Scheduled egg hatches
- Periodic health checks

**Event Format:**
```json
{"ts":"2025-10-15T21:00:00Z","type":"clock_tick","lane":"Execution","actor":"deia-clock","data":{"ttl_expired":["tag-001"]}}
```

### 5.3 QEE Integration

**Queue Execution Engine (QEE)** manages task queues:
- Egg hatch queue (priority-based)
- Archive requests (DND compliance)
- Validation backlog

---

## 6. Validator Updates (Planned)

**Phase 1:** Accept `eos` block alongside existing entity schemas

```python
# Validator enhancement (planned)
def validate_eos_manifest(front_matter):
    if 'eos' in front_matter:
        # Check eos version
        # Validate kind, id, policy, caps, routing
        # Enforce ROTG/DND compliance
        pass
```

**Phase 2:** Reject entities without `eos` block (mandatory migration)

---

## 7. Security: Virus Definition

**Virus:** Uncontained instruction inside an egg that, if executed, hijacks the egg for its own purposes.

**Prevention:**
- All instructions MUST be in genetic blueprints (not loose commands)
- Eggs MUST have valid `eos` manifest
- Validator MUST reject eggs with uncontained instructions
- DND: Archive infected eggs (forensic value)

**Example Virus (Invalid):**
```yaml
---
# NO eos manifest - VIRUS!
type: egg
# Direct hatch commands embedded - HIJACK!
commands:
  - llh_hatch.sh -t llh -i house-llh
---
```

---

## 8. Future Extensions

- **Service Processes:** Long-running daemons (bots, monitors, schedulers)
- **DNA Injection:** Genetic blueprint system (`.deia/genomes/` or equivalent)
- **Capability System:** Fine-grained permissions (spawn, coordinate, archive)
- **Multi-Tenancy:** Isolated project namespaces with access control
- **Preemption:** Scheduler support for priority interrupts

---

## 9. Filing

**Path:** `docs/os/eOS-SPEC-v0.1.md`
**Status:** Specification draft
**Tags:** `#eos` `#operating-system` `#deia` `#architecture`

---

## References

- LLH Builder: `docs/tools/LLH-BUILDER-SPEC-v0.1.md`
- Boot Flow: `docs/os/eOS-BOOT-FLOW.md`
- Validators: `.deia/tools/llh_validate.py`
- Launchers: `.deia/tools/builder_launch.{ps1,sh}`
