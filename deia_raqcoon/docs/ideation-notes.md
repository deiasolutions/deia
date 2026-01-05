# DEIA + RAQCOON Ideation Notes (Session Capture)

## Executive Summary
We are building a self-contained `deia_raqcoon` workspace inside `deiasolutions`.
It will support multi-lane execution (LLM chat, terminal bees, local LLMs, and
task files) and use RAQCOON KB as the source of truth for routing, delivery, and
cross-domain work (design, planning, PM, and code). Local-first is mandatory,
but the design must be portable to hosted deployments later.

## Decisions (Confirmed)
- Project lives entirely inside `deiasolutions/deia_raqcoon` with no shared code.
- Multi-lane execution:
  - LLM chat (cache + prompt)
  - Terminal bees (Claude Code/Codex via CLI adapters)
  - Local LLMs (Llama)
  - File-based task coordination
- KB is RAQCOON (rebrand of existing RAG pattern); domain includes design,
  Vercel, Railway, ops, PM, and general engineering.
- CLI bee launch must prompt if not in repo root, and chdir must happen BEFORE
  CLI start. Use that repo’s `.deia` as hive control center.
- Git operations must be supported (commit/push), with guardrails.
- Spec-driven development and TDD are optional but encouraged. Add a spec
  creation bot/service lane.
- "Project management" means PMBOK-aligned workflows. Business analysis should
  align with BABOK.
- PMBOK, BABOK, and Code are independent project modes (three checkboxes).
- Queen should be able to follow a plan autonomously and create tasks.
- Add a simple "minder" (cron or Llama) to ping bees periodically and request
  status updates / herd movement.
- Lean memory: keep raw message logs + flight recaps. Use Sprints + Flights
  instead of days. Embeddings optional later.
- Q33N git commit/push requires human-granted toggle.
- Add a pre-sprint review checklist (human review gate) and allow commits per
  flight when enabled.
- Ideation phase: no final specs yet; hold doc drafting until ideation is done.

## UI Mockups (In `docs/mockups/`)
Pages created:
- Landing: `hive-landing.html`
- Project hub: `hive-project.html`
- Chat dashboard: `hive-chat-mockup-dashboard.html`
- Operator mode: `hive-chat-mockup-operator.html`
- Git browser: `hive-git-browser.html`
- KB editor: `hive-kb-editor.html`
- Index: `hive-mockups-index.html`

Deprecated:
- Base chat view: `hive-chat-mockup.html` (now a deprecation notice)

## UX Flow (How it moves together)
- Landing is the entry funnel: chat, KB, git, launch bee.
- Project hub is project-scoped context: goals, routing, active work.
- Chat dashboard is collaboration plane: tasks, responses, signals, routing mix.
- Operator mode is control plane: launch/stop bees, routing control, alerts.
- KB editor is source of truth: RAQCOON entities, delivery modes, previews.
- Git browser is execution audit: repo state and diffs after bee changes.

## Planned Endpoints (UI → API map)
Global:
- GET /api/health
- GET /api/config

Landing:
- GET /api/projects
- GET /api/status
- POST /api/bees/launch
- GET /api/kb/stats

Project Hub:
- GET /api/projects/{project_id}
- GET /api/tasks?project_id=...
- GET /api/bees?project_id=...
- GET /api/routing/policy?project_id=...

Chat Dashboard:
- GET /api/channels?project_id=...
- GET /api/messages?channel_id=...
- POST /api/messages
- POST /api/routing/preview
- WS /api/ws

Operator Mode:
- POST /api/bees/{id}/start|stop|pause
- GET /api/lanes/status
- POST /api/queues/{lane}/drain|pause
- POST /api/git/commit|push

KB Editor:
- GET /api/kb/entities
- POST /api/kb/entities
- PUT /api/kb/entities/{id}
- GET /api/kb/delivery-modes
- POST /api/kb/preview
- POST /api/tasks/{id}/attach-kb

Git Browser:
- GET /api/git/status
- GET /api/git/tree?path=...
- GET /api/git/file?path=...
- GET /api/git/diff?path=...

Model + Cost:
- GET /api/models
- PUT /api/models/{id}
- GET /api/usage/summary
- GET /api/costs?project_id=...

## RAQCOON KB Model (first pass)
Entity Types:
- RULE, PLAYBOOK, PATTERN, SNIPPET, CHECKLIST, REFERENCE

Required fields:
- id, title, summary, tags, delivery_mode, load_mode

Delivery modes:
- cache_prompt | task_file | both

Load modes:
- always | situation | on_demand

## Features to Include (Ideation List)
- Conversation history (lane + provider + KB injection metadata)
- Test results (per lane; RAQCOON retrieval tests)
- Bugs and ticketing
- Patterns and anti-patterns (KB entity types)
- Change provenance (which bee changed what and why)
- Cost ledger (per task/session + preflight estimates)
- Governance approvals for file writes
- Model management UI that writes to DB
- Cache optimization and cache analytics
- PMBOK-aligned project management workflows
- BABOK-aligned business analysis workflows

## MVP (ASAP Working Set)
Goal: local-first working system with chat UI, CLI bees, and minimal routing.

Must-haves:
- Chat UI that connects to local API + WebSocket.
- CLI bee launch (Claude Code + Codex) with repo-root preflight prompt.
- Basic routing (manual lane selection + default rules).
- Task file write/read loop in `.deia` for terminal bees.
- Minimal KB injection (RULE + SNIPPET) to support code tasks.
*** End Patch```

## Repo Root Discipline (Hard Requirement)
- If not at repo root, prompt the user.
- Chdir to repo root BEFORE launching CLI tools.
- Always use repo’s `.deia` as hive control center.

## Notes from DEIA Repo (Ideas to carry forward)
- Local-first + portability (DEIA vision docs)
- Hybrid file + HTTP multi-agent orchestration
- Hive controls (pause/stop) and queue monitoring
- Unified timeline / activity feed
- Cross-platform preference injection
- Security + sandboxing
- Multi-domain capability (beyond code)
- “Egg” / self-contained project bootstrapping concept
