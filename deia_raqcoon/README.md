# DEIA + RAQCOON

Self-contained workspace for the DEIA hive collaboration system with RAQCOON
knowledge delivery. This directory is intentionally standalone and does not
share code with other projects.

## Goals
- Multi-lane execution: LLM chat, terminal bees, local LLMs, and task files.
- KB-driven routing for design, planning, and coding workflows.
- Local-first operation with a clean path to hosting later.

## Structure
- `core/` - Core orchestration, state, and routing.
- `adapters/` - Provider adapters (LLM API, terminal, local LLM).
- `kb/` - Knowledge base models, storage, and indexing.
- `ui/` - UI and view models (future).
- `runtime/` - Process supervisors, runners, and local services.
- `schemas/` - Task and message schema definitions.
- `docs/` - Architecture, routing, and KB model docs.

## Next Steps
See `docs/architecture.md` for the first-pass system outline.
See `docs/2026-01-04-DEIA-RAQCOON-SPEC-IN-TO-CODE-OUT.md` for the automation roadmap.
