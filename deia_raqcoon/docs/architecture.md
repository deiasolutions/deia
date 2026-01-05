# Architecture Overview

## Purpose
DEIA + RAQCOON is a self-contained hive collaboration system that supports
design, planning, and software delivery. It routes work across multiple
execution lanes while keeping knowledge delivery consistent.

## Core Concepts
- **Lanes**: Distinct execution paths for different task types and tooling.
  - LLM chat (cache + prompt)
  - Terminal bees (Claude Code/Codex via CLI)
  - Local LLMs (Llama, etc.)
  - Task files (filesystem-based coordination)
- **RAQCOON KB**: Knowledge base that drives routing and prompt/task delivery.
- **Routing Policy**: Decides lane + provider based on task intent + KB profile.

## Primary Modules
- `core/router.py` - Intent parsing and lane selection.
- `adapters/` - Provider adapters (LLM API, CLI, local).
- `kb/` - Entity model, storage, and retrieval.
- `runtime/` - Process supervisor + lane execution.
- `schemas/` - Task file and message specs.

## Design Principles
- **Local-first**: SQLite and local filesystem by default.
- **Portable**: Hosting-ready with configurable storage and host bindings.
- **Composable**: All lanes share a common interface and message schema.
