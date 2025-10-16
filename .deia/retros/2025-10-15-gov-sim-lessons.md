---
title: Lessons Learned — Gov Sim Bootstrap
date: 2025-10-15
authors: [Whisperwing (OpenAI HMQ-01)]
tags: [retrospective, process, personas, scenario, rse]
---

# Summary
Lean, additive bootstrapping works: define contracts early (schema + events), timebox explorations, and log everything. Use aliases to bridge drafts, keep DND.

# Key Takeaways
- Persona readiness over speed: require minimal YAML front matter (`id, role, llh, capacities, stances`) so validators/loaders work; keep narrative body intact.
- Use `ALIASES.json` to deconflict naming drift between teams without rework.
- Scenario guardrails: validator caught tag_team shape issues early; saved a rework loop.
- Event contract first: RSE event types clarified what scenarios must emit.
- TAG + deadlines: TTL TAGs + explicit deadlines maintain momentum and scope.
- Non-destructive collaboration: DND + RSE + changelog = safe parallelism and auditability.
- Corpus anchors: durable async coordination; avoids chat drift.
- Rabbit-hole hygiene: 20‑minute wrap awareness; 30‑minute soft stop; checkpoints.

# Concrete Artifacts (reference)
- Validators/loader: `.deia/tools/validate_persona.py`, `validate_scenario.py`, `load_scenario.py`
- Event types: `.deia/sim/EVENT-TYPES.md`
- Aliases: `.deia/personas/ALIASES.json`
- TAG + scenario: `.deia/tag-teams/Border-2025-TAG.md`, `.deia/scenarios/2025Q4-border-funding-crisis.yaml`

# Next-Time Checklist
- [ ] Personas have minimal YAML front matter + ≥1 citation in body
- [ ] Scenario validates; all actors resolve (aliases if needed)
- [ ] RSE events mapped from scenario steps (happy path + error)
- [ ] TAG TTL and deadlines defined; budgets set
- [ ] RSE + CHANGELOG entries appended for every change
- [ ] 20m checkpoint + 30m soft stop observed

