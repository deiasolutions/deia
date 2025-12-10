---
title: LLH A/B Experiments — Tracker
date: 2025-10-15
maintainer: Whisperwing (OpenAI HMQ-01)
policy: DND (do-not-destroy); additive only; archive by explicit approval
---

# Purpose
- Coordinate parallel LLH experiments (A/B or more), with budgets, SLOs, and acceptance criteria.
- Log outcomes for value-per-cost comparison and selection.

# Conventions
- ID format: YYYY-MM-DD-LLH-AB-###<variant>
- Budget window: 15m default (DEIA Clock); specify tokens/CPU/human-minutes
- Lanes: Governance | Process | Code | UI | Ops
- SLOs: latency, delivery ratio, duplicates, observability coverage

# Index
- 2025-10-15-LLH-AB-001A — Pheromone–RSM: examples-first
- 2025-10-15-LLH-AB-001B — Pheromone–RSM: adapters-first

## 2025-10-15-LLH-AB-001A — Pheromone–RSM: examples-first

- Objective: Finalize flows/examples and validate watcher/validator pipeline end-to-end.
- Budget (window=15m): tokens=N/A (local), cpu_min=30, human_min=0–5.
- SLOs: doc updates ≤ 30m; telemetry coverage ≥ 95%; policy violations = 0.
- Deliverables: updated examples file + cross-links in protocol; telemetry events.
- Status: paused (project on hold)

## 2025-10-15-LLH-AB-001B — Pheromone–RSM: adapters-first

- Objective: Draft minimal TS/Python adapter notes and interface stubs.
- Budget (window=15m): tokens=N/A (local), cpu_min=30, human_min=0–5.
- SLOs: interface notes ≤ 30m; telemetry coverage ≥ 95%; policy violations = 0.
- Deliverables: adapter notes in protocol + stub interfaces; telemetry events.
- Status: paused (project on hold)
