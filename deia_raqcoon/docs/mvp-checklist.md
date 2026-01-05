# MVP Checklist (ASAP Working Set)

## Scope
Local-first system with chat UI, CLI bees (Claude Code + Codex), minimal routing,
task file loop, and basic KB injection.

## 1) Runtime + API
- [ ] `runtime/server.py` FastAPI app
- [ ] WebSocket at `/api/ws`
- [ ] REST endpoints:
  - [ ] `GET /api/health`
  - [ ] `GET /api/config`
  - [ ] `POST /api/bees/launch`
  - [ ] `POST /api/messages`
  - [ ] `GET /api/messages`
  - [ ] `GET /api/channels`
  - [ ] `POST /api/tasks`
  - [ ] `GET /api/tasks/response`
  - [ ] `GET /api/git/status`
  - [ ] `POST /api/git/commit`
  - [ ] `POST /api/git/push`
  - [ ] `POST /api/flights/start`
  - [ ] `POST /api/flights/end`
  - [ ] `POST /api/flights/recap`
  - [ ] `GET /api/flights`
  - [ ] `GET /api/flights/recaps`

## 2) CLI Bee Launch (Repo Root Discipline)
- [ ] Preflight: detect repo root (git + `.deia`)
- [ ] Prompt if not at repo root
- [ ] `chdir` before CLI launch (must happen before process spawn)
- [ ] Adapter stubs for:
  - [ ] Claude Code (CLI)
  - [ ] Codex (CLI)

## 3) Task File Loop
- [ ] Write tasks to `.deia/hive/tasks/{bot-id}/`
- [ ] Read responses from `.deia/hive/responses/`
- [ ] Simple message schema in `schemas/task_file.json`
- [ ] Archive or mark completed tasks

## 4) KB Injection (Minimal)
- [ ] KB entity types: RULE + SNIPPET
- [ ] Delivery: cache_prompt + task_file
- [ ] Injection preview (text-only)

## 5) UI Wiring (Mockups → API)
- [ ] Landing: launch chat, bee, git, KB
- [ ] Project hub: active tasks + bees
- [ ] Chat dashboard: send/receive messages, show signals
- [ ] Operator mode: start/stop bees
- [ ] KB editor: create/update minimal entities
- [ ] Git browser: status + file tree (read-only)

## 6) Logging + Cost (Minimal)
- [ ] Per-message metadata: lane, provider, tokens (if available)
- [ ] Session summary stub (counts only)
- [ ] Flight start/end + recap storage
- [ ] Minder stub (periodic ping via /api/messages)

## Exit Criteria
- [ ] Launch local API + UI from repo root
- [ ] Start Claude Code + Codex CLI bees from UI
- [ ] Send a task and receive a response via task file loop
- [ ] Inject a RULE or SNIPPET into a task or prompt
