---
spec_version: "0.1"
project: {{PROJECT_ID}}
author: {{AUTHOR}}
created: {{DATE}}
status: draft

# Entity definitions (parsed by llh_factory_build)
entities:
  llhs:
    - id: {{LLH_ID}}
      title: "{{LLH_TITLE}}"
      structure: {{STRUCTURE_TYPE}}  # executive, legislative, functional, cross-functional
      members: []  # List of member IDs or count
      parent: null  # Parent LLH ID (for hierarchies)
      caps: [{{CAPABILITIES}}]  # List of capabilities
      governance:
        structure: flat  # flat, hierarchical, matrix
        decision_mode: consensus  # consensus, majority, executive
        transparency: members-only  # public, members-only, private
      policy:
        rotg: true
        dnd: true
      constraints: []
      capacities:
        budget: {{BUDGET_LEVEL}}  # low, medium, high
        attention: {{ATTENTION_LEVEL}}  # low, medium, high
        staff_cycles: {{STAFF_LEVEL}}  # low, medium, high

  tags:
    - id: {{TAG_ID}}
      title: "{{TAG_TITLE}}"
      parent: {{PARENT_LLH}}  # LLH this TAG belongs to
      deadline: {{DEADLINE}}  # ISO date or null
      members: []  # List of member IDs
      caps: [{{TAG_CAPABILITIES}}]
      policy:
        rotg: true
        dnd: true
      objectives: "{{OBJECTIVES}}"

  drones:
    # Optional: Automated workers
    - id: {{DRONE_ID}}
      title: "{{DRONE_TITLE}}"
      type: {{DRONE_TYPE}}  # monitor, processor, aggregator, notifier
      parent: {{PARENT_TAG_OR_LLH}}
      triggers: [{{TRIGGER_CONDITIONS}}]
      actions: [{{DRONE_ACTIONS}}]

# Routing configuration
routing:
  llhs: ".deia/.projects/{{PROJECT_ID}}_001/llhs/"
  tags: ".deia/.projects/{{PROJECT_ID}}_001/tag-teams/"
  drones: ".deia/.projects/{{PROJECT_ID}}_001/drones/"

# Build options
build:
  validate: true  # Run llh_validate.py after build
  log_rse: true   # Log to RSE
  require_approval: true  # Require human approval before building
---

# {{PROJECT_TITLE}}

## Overview

[Describe the organization, simulation, or project this spec defines]

## Objectives

[What are you trying to model, test, or build?]

## Organizational Structure

### LLHs (Limited Liability Hives)

[Describe the main organizational units]

**Example:**
- **Leadership LLH**: Executive decision-making body
- **Engineering LLH**: Technical development and operations
- **Operations LLH**: Day-to-day operations and support

### TAGs (Together And Good teams)

[Describe cross-functional teams or projects]

**Example:**
- **Q4 Launch TAG**: Cross-org team for product launch
- **Security Audit TAG**: Time-bounded security review

### Drones (Optional)

[Describe automated workers or background processes]

**Example:**
- **Metrics Collector**: Gathers usage data hourly
- **Alert Processor**: Routes alerts to appropriate teams

## Hierarchies & Relationships

[Describe parent/child relationships and dependencies]

**Example:**
```
Leadership LLH (parent)
├── Engineering LLH (child)
│   ├── Backend TAG
│   └── Frontend TAG
└── Operations LLH (child)
    └── Incident Response TAG
```

## Scenarios & Timelines

[Define key scenarios, deadlines, milestones]

**Example:**
- **2025-Q4**: Product launch
- **2026-Q1**: Post-launch optimization
- **2026-Q2**: Scale-up operations

## Success Criteria

[How do you know this worked?]

**Example:**
- All LLHs have clear ownership
- TAGs have defined completion criteria
- Decision-making paths are unambiguous
- Hierarchy reflects actual authority structure

## Open Questions

[Track unresolved questions]

**Example:**
- Should Operations LLH report to Engineering or be peer?
- Do we need a separate Compliance LLH?
- How do we handle cross-org conflicts?

## Notes

[Additional context, constraints, assumptions]

---

**Template Version:** 0.1.0
**eOS Version:** 0.1
**Created:** 2025-10-15
**Usage:** Copy and fill in {{PLACEHOLDERS}}
