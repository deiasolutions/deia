# Coding Priorities (2025-10-13)

Scope: Non-invasive; config-only under .deia/; no changes to src/.

- Conversation logging UX
  - Smooth manual triggers (deia log, session templates) and docs polish
  - Keep auto-logging out of scope for now (infra incomplete)

- Preference system
  - Define, document, and stabilize .deia/preferences.md format for cross-tool reuse

- VS Code integration
  - Solidify extension→CLI pathways (log/view/status); no API or signature changes
  - Basic UX: status bar indicator + error surfaces

- Tests & docs health
  - Expand happy-path coverage; keep failures/findings as proposals only
  - Run doc audit and eliminate encoding/BOM pitfalls in JSON/MD samples

- Downloads sync hardening
  - YAML frontmatter routing clarity; guardrails on staging, errors, idempotency

- Sanitization & validation (lightweight)
  - Keep automated pass conservative; emphasize manual review workflow

- Hive CLI parity (spec vs code)
  - Future: status, heartbeat, handoff, complete, cleanup—note gaps, do not patch now

Notes
- Prioritize LLM-agnostic processes; use .deia/ files as the single source of truth.
- Avoid touching CLI/entry points; prefer docs and helpers under .deia/.