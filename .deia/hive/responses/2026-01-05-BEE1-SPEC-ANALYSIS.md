# BEE1: Spec Analysis Report

**Generated**: 2026-01-05
**Analyst**: Bee 1 (Spec Analyst)
**Files Reviewed**: 10/10

---

## 1. Phase Inventory

The spec defines 6 phases toward "Spec In -> Code Out" automation.

### Phase 1: Spec Intake + Task Graph
**Goal**: Turn a spec into a machine-readable plan and task graph.

| Deliverable | Type | Description |
|-------------|------|-------------|
| `schemas/spec.json` | Schema | Spec schema: goals, constraints, acceptance criteria, scope exclusions |
| `runtime/spec_parser.py` | Module | Parser to convert markdown/spec into JSON |
| `runtime/task_graph.py` | Module | Break spec into tasks with dependencies, owners, routing lane |
| `/api/spec/plan` | Endpoint | Spec-to-tasks flow endpoint |

**Dependencies**: None (first phase)

---

### Phase 2: Execution Loop + Verification
**Goal**: Build the core "execute -> test -> iterate" loop.

| Deliverable | Type | Description |
|-------------|------|-------------|
| `runtime/executor.py` | Module | Pull tasks, route to lane, collect responses, mark complete/blocked |
| `runtime/verifier.py` | Module | Hook test/lint commands, capture results into task history |
| `/api/tasks/run` | Endpoint | Execute tasks |
| `/api/tasks/verify` | Endpoint | Run verification/tests |

**Dependencies**: Phase 1 (needs task graph)

---

### Phase 3: Git Automation + Gates
**Goal**: Safe, automated commits with human approval gates.

| Deliverable | Type | Description |
|-------------|------|-------------|
| `runtime/git_flow.py` | Module | Patch assembly, staging, commit workflow |
| Gate-integrated pipeline | Feature | Pre-sprint review, per-flight commit permission, human override |

**Dependencies**: Phase 2 (needs execution loop)

---

### Phase 4: Observability + Cost Controls
**Goal**: Track costs, time, and quality across bots.

| Deliverable | Type | Description |
|-------------|------|-------------|
| `runtime/telemetry.py` | Module | Token/provider cost per message, per-task aggregation |
| `/api/summary` extensions | Endpoint | Cost + per-flight stats in summary |
| Dashboards | UI | Flight performance dashboards |

**Dependencies**: Phase 2-3 (needs execution data)

---

### Phase 5: Advanced RAQCOON (Quality + Safety)
**Goal**: Use KB to prevent bad patterns and improve results.

| Deliverable | Type | Description |
|-------------|------|-------------|
| KB policy engine | Module | Rule enforcement per task type |
| Rule-based blockers | Feature | Block execution before bad patterns |
| Retrieval policies | Feature | Strict mode for critical paths (security, infra, payments) |

**Dependencies**: Phase 1-4 (needs working system)

---

### Phase 6: Full "Spec In -> Code Out" Workflow
**Goal**: Single flow from spec to tested code.

| Deliverable | Type | Description |
|-------------|------|-------------|
| "Run Spec" button | UI | Single UI action to trigger full workflow |
| End-to-end status | Feature | Flight checkpoints and status tracking |

**Flow**: Spec uploaded -> Planner creates tasks -> Executor runs -> Verifier tests -> Git stages -> Human approves -> Push

**Dependencies**: All previous phases

---

## 2. MVP Requirements Matrix

From `mvp-checklist.md` - the ASAP working set.

### 2.1 Runtime + API

| # | Requirement | Spec Reference |
|---|-------------|----------------|
| 1.1 | `runtime/server.py` FastAPI app | mvp-checklist §1 |
| 1.2 | WebSocket at `/api/ws` | mvp-checklist §1 |
| 1.3 | `GET /api/health` | mvp-checklist §1 |
| 1.4 | `GET /api/config` | mvp-checklist §1 |
| 1.5 | `POST /api/bees/launch` | mvp-checklist §1 |
| 1.6 | `POST /api/messages` | mvp-checklist §1 |
| 1.7 | `GET /api/messages` | mvp-checklist §1 |
| 1.8 | `GET /api/channels` | mvp-checklist §1 |
| 1.9 | `POST /api/tasks` | mvp-checklist §1 |
| 1.10 | `GET /api/tasks/response` | mvp-checklist §1 |
| 1.11 | `GET /api/git/status` | mvp-checklist §1 |
| 1.12 | `POST /api/git/commit` | mvp-checklist §1 |
| 1.13 | `POST /api/git/push` | mvp-checklist §1 |
| 1.14 | `POST /api/flights/start` | mvp-checklist §1 |
| 1.15 | `POST /api/flights/end` | mvp-checklist §1 |
| 1.16 | `POST /api/flights/recap` | mvp-checklist §1 |
| 1.17 | `GET /api/flights` | mvp-checklist §1 |
| 1.18 | `GET /api/flights/recaps` | mvp-checklist §1 |

### 2.2 CLI Bee Launch (Repo Root Discipline)

| # | Requirement | Spec Reference |
|---|-------------|----------------|
| 2.1 | Preflight: detect repo root (git + `.deia`) | mvp-checklist §2 |
| 2.2 | Prompt if not at repo root | mvp-checklist §2 |
| 2.3 | `chdir` before CLI launch (must happen before process spawn) | mvp-checklist §2 |
| 2.4 | Adapter stub for Claude Code (CLI) | mvp-checklist §2 |
| 2.5 | Adapter stub for Codex (CLI) | mvp-checklist §2 |

### 2.3 Task File Loop

| # | Requirement | Spec Reference |
|---|-------------|----------------|
| 3.1 | Write tasks to `.deia/hive/tasks/{bot-id}/` | mvp-checklist §3 |
| 3.2 | Read responses from `.deia/hive/responses/` | mvp-checklist §3 |
| 3.3 | Simple message schema in `schemas/task_file.json` | mvp-checklist §3 |
| 3.4 | Archive or mark completed tasks | mvp-checklist §3 |

### 2.4 KB Injection (Minimal)

| # | Requirement | Spec Reference |
|---|-------------|----------------|
| 4.1 | KB entity types: RULE + SNIPPET | mvp-checklist §4 |
| 4.2 | Delivery: cache_prompt + task_file | mvp-checklist §4 |
| 4.3 | Injection preview (text-only) | mvp-checklist §4 |

### 2.5 UI Wiring (Mockups → API)

| # | Requirement | Spec Reference |
|---|-------------|----------------|
| 5.1 | Landing: launch chat, bee, git, KB | mvp-checklist §5 |
| 5.2 | Project hub: active tasks + bees | mvp-checklist §5 |
| 5.3 | Chat dashboard: send/receive messages, show signals | mvp-checklist §5 |
| 5.4 | Operator mode: start/stop bees | mvp-checklist §5 |
| 5.5 | KB editor: create/update minimal entities | mvp-checklist §5 |
| 5.6 | Git browser: status + file tree (read-only) | mvp-checklist §5 |

### 2.6 Logging + Cost (Minimal)

| # | Requirement | Spec Reference |
|---|-------------|----------------|
| 6.1 | Per-message metadata: lane, provider, tokens (if available) | mvp-checklist §6 |
| 6.2 | Session summary stub (counts only) | mvp-checklist §6 |
| 6.3 | Flight start/end + recap storage | mvp-checklist §6 |
| 6.4 | Minder stub (periodic ping via /api/messages) | mvp-checklist §6 |

---

## 3. Endpoint Registry

All API endpoints mentioned across documentation.

### MVP Endpoints (mvp-checklist.md)

| Method | Path | Category | Source |
|--------|------|----------|--------|
| GET | /api/health | Global | mvp-checklist |
| GET | /api/config | Global | mvp-checklist |
| WS | /api/ws | Global | mvp-checklist |
| POST | /api/bees/launch | Bees | mvp-checklist |
| POST | /api/messages | Messages | mvp-checklist |
| GET | /api/messages | Messages | mvp-checklist |
| GET | /api/channels | Messages | mvp-checklist |
| POST | /api/tasks | Tasks | mvp-checklist |
| GET | /api/tasks/response | Tasks | mvp-checklist |
| GET | /api/git/status | Git | mvp-checklist |
| POST | /api/git/commit | Git | mvp-checklist |
| POST | /api/git/push | Git | mvp-checklist |
| POST | /api/flights/start | Flights | mvp-checklist |
| POST | /api/flights/end | Flights | mvp-checklist |
| POST | /api/flights/recap | Flights | mvp-checklist |
| GET | /api/flights | Flights | mvp-checklist |
| GET | /api/flights/recaps | Flights | mvp-checklist |

### Phase Endpoints (spec-in-to-code-out.md)

| Method | Path | Phase | Source |
|--------|------|-------|--------|
| POST | /api/spec/plan | 1 | spec doc |
| POST | /api/tasks/run | 2 | spec doc |
| POST | /api/tasks/verify | 2 | spec doc |
| GET | /api/summary (extended) | 4 | spec doc |

### Extended Endpoints (ideation-notes.md)

| Method | Path | UI Section | Source |
|--------|------|------------|--------|
| GET | /api/projects | Landing | ideation |
| GET | /api/status | Landing | ideation |
| GET | /api/kb/stats | Landing | ideation |
| GET | /api/projects/{project_id} | Project Hub | ideation |
| GET | /api/tasks?project_id=... | Project Hub | ideation |
| GET | /api/bees?project_id=... | Project Hub | ideation |
| GET | /api/routing/policy?project_id=... | Project Hub | ideation |
| GET | /api/channels?project_id=... | Chat | ideation |
| POST | /api/routing/preview | Chat | ideation |
| POST | /api/bees/{id}/start | Operator | ideation |
| POST | /api/bees/{id}/stop | Operator | ideation |
| POST | /api/bees/{id}/pause | Operator | ideation |
| GET | /api/lanes/status | Operator | ideation |
| POST | /api/queues/{lane}/drain | Operator | ideation |
| POST | /api/queues/{lane}/pause | Operator | ideation |
| GET | /api/kb/entities | KB Editor | ideation |
| POST | /api/kb/entities | KB Editor | ideation |
| PUT | /api/kb/entities/{id} | KB Editor | ideation |
| GET | /api/kb/delivery-modes | KB Editor | ideation |
| POST | /api/kb/preview | KB Editor | ideation |
| POST | /api/tasks/{id}/attach-kb | KB Editor | ideation |
| GET | /api/git/tree?path=... | Git Browser | ideation |
| GET | /api/git/file?path=... | Git Browser | ideation |
| GET | /api/git/diff?path=... | Git Browser | ideation |
| GET | /api/models | Model/Cost | ideation |
| PUT | /api/models/{id} | Model/Cost | ideation |
| GET | /api/usage/summary | Model/Cost | ideation |
| GET | /api/costs?project_id=... | Model/Cost | ideation |

---

## 4. Expected Module Files

Files the spec says should exist.

### Core Structure (README.md)

| Path | Purpose | Status |
|------|---------|--------|
| `core/` | Core orchestration, state, routing | Expected |
| `adapters/` | Provider adapters (LLM API, terminal, local LLM) | Expected |
| `kb/` | Knowledge base models, storage, indexing | Expected |
| `ui/` | UI and view models | Future |
| `runtime/` | Process supervisors, runners, local services | Expected |
| `schemas/` | Task and message schema definitions | Expected |
| `docs/` | Architecture, routing, KB model docs | Expected |

### Runtime Files (local-run.md)

| Path | Purpose | Source |
|------|---------|--------|
| `runtime/server.py` | API + WebSocket | local-run.md |
| `runtime/worker.py` | Lane execution (terminal, local LLM) | local-run.md |

### Phase 1 Files (spec doc)

| Path | Purpose | Source |
|------|---------|--------|
| `schemas/spec.json` | Spec schema definition | Phase 1 |
| `runtime/spec_parser.py` | Markdown/spec to JSON parser | Phase 1 |
| `runtime/task_graph.py` | Task graph builder | Phase 1 |

### Phase 2 Files (spec doc)

| Path | Purpose | Source |
|------|---------|--------|
| `runtime/executor.py` | Task execution loop | Phase 2 |
| `runtime/verifier.py` | Test/lint runner | Phase 2 |

### Phase 3 Files (spec doc)

| Path | Purpose | Source |
|------|---------|--------|
| `runtime/git_flow.py` | Git automation workflow | Phase 3 |

### Phase 4 Files (spec doc)

| Path | Purpose | Source |
|------|---------|--------|
| `runtime/telemetry.py` | Cost and metrics tracking | Phase 4 |

---

## 5. Gates & Controls

All mentioned permission gates and control mechanisms.

| Gate Name | Purpose | Source | Scope |
|-----------|---------|--------|-------|
| `allow_q33n_git` | Q33N (Queen) git commit/push permission | ideation-notes.md | Global toggle |
| `pre_sprint_review` | Human review gate before sprint starts | ideation-notes.md | Per-sprint |
| `allow_flight_commits` | Allow commits during a flight when enabled | ideation-notes.md | Per-flight |

### Gate Rules (from ideation-notes.md)

1. **Q33N git commit/push requires human-granted toggle** - automated commits blocked by default
2. **Pre-sprint review checklist** - human must review before sprint begins
3. **Per-flight commit permission** - can enable auto-commits for specific flights

### Gate Flow

```
Start Flight
    ↓
pre_sprint_review = true? → No → Block commits
    ↓ Yes
allow_flight_commits = true? → No → Require manual commit
    ↓ Yes
allow_q33n_git = true? → No → Block push
    ↓ Yes
Auto-commit + push allowed
```

---

## 6. KB Entity Types

From `kb-model.md` - RAQCOON Knowledge Base structure.

### Entity Types

| Type | Purpose | Example Use |
|------|---------|-------------|
| RULE | Dos/don'ts and non-negotiable guardrails | "Never commit secrets", "Always use TypeScript" |
| PLAYBOOK | Step-by-step procedures | Deploy to Vercel, Rollback procedure |
| PATTERN | Repeatable design/architecture patterns | Service layer pattern, Repository pattern |
| SNIPPET | Configs or code fragments | vercel.json template, railway.toml template |
| CHECKLIST | Release and QA gates | Pre-release checklist, Security review |
| REFERENCE | Docs, links, and context notes | API documentation links, Architecture decisions |

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (e.g., RULE-001) |
| title | string | Human-readable title |
| summary | string | Brief description |
| tags | string[] | Categorization tags |
| delivery_mode | enum | `cache_prompt` \| `task_file` \| `both` |
| load_mode | enum | `always` \| `situation` \| `on_demand` |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| attachments | string[] | Inline snippets or file references |
| examples | any | Usage examples |
| related_entities | string[] | Links to related KB entities |

### Delivery Modes

| Mode | Behavior |
|------|----------|
| cache_prompt | Inject into LLM system prompt/cache |
| task_file | Include in task file for terminal bees |
| both | Use both delivery methods |

### Load Modes

| Mode | Behavior |
|------|----------|
| always | Always load regardless of context |
| situation | Load based on task intent/domain |
| on_demand | Only load when explicitly requested |

---

## 7. Exit Criteria

What defines "MVP complete" per the documentation.

### From mvp-checklist.md - Exit Criteria Section

| # | Criterion | Description |
|---|-----------|-------------|
| E1 | Launch local API + UI from repo root | Server starts, UI connects |
| E2 | Start Claude Code + Codex CLI bees from UI | Both adapters working |
| E3 | Send a task and receive a response via task file loop | Full round-trip |
| E4 | Inject a RULE or SNIPPET into a task or prompt | KB delivery working |

### Implicit Criteria (from docs)

| # | Criterion | Source |
|---|-----------|--------|
| E5 | Repo root discipline enforced | mvp-checklist §2 |
| E6 | Git status viewable | mvp-checklist §1 |
| E7 | Gates block unauthorized commits | ideation-notes.md |
| E8 | Flight start/end/recap workflow | mvp-checklist §1 |
| E9 | Messages stored with lane/provider metadata | mvp-checklist §6 |

### Minimal Success Criteria (from spec doc)

| # | Criterion | Phase |
|---|-----------|-------|
| S1 | A spec can generate a task graph automatically | Phase 1+ |
| S2 | The system executes tasks, runs tests, reports outcomes | Phase 2+ |
| S3 | Commits are created automatically with human gate | Phase 3+ |

---

## 8. Ambiguities & Questions

Issues found during documentation review.

### Contradictions

| Issue | Location | Details |
|-------|----------|---------|
| Task path format | mvp-checklist vs ideation | Checklist says `.deia/hive/tasks/{bot-id}/`, but ideation mentions general task routing |
| Worker file | local-run.md | Mentions `runtime/worker.py` but not in any other doc or checklist |

### Unclear Items

| Item | Question |
|------|----------|
| Project scope | Are "projects" separate from repos? How is project_id determined? |
| Local LLM lane | How is Llama/local LLM integrated? No adapter details provided. |
| Minder behavior | What exactly does minder ping? What actions does it take? |
| Queue system | ideation mentions queues but no implementation details |
| Pause vs Stop | What's the difference between pausing and stopping a bee? |

### Missing Details

| Topic | What's Missing |
|-------|----------------|
| Authentication | No auth mentioned for API endpoints |
| Error handling | No error response schemas defined |
| Rate limiting | No mention of rate limits or throttling |
| Persistence | SQLite mentioned but no schema defined |
| WebSocket protocol | What messages flow over WS? No protocol defined |

### Scope Questions

| Question | Impact |
|----------|--------|
| Is MVP = Phase 0? | mvp-checklist seems to be pre-Phase 1 |
| When do ideation endpoints get built? | Many endpoints in ideation-notes not in any phase |
| Is UI in scope for MVP? | UI wiring section exists but no UI code mentioned |

---

## Summary

### Document Coverage

| Document | Key Content |
|----------|-------------|
| README.md | Module structure overview |
| architecture.md | Core concepts, lanes, modules |
| spec-in-to-code-out.md | 6-phase roadmap with deliverables |
| mvp-checklist.md | ASAP working set (18 endpoints, 6 sections) |
| routing.md | Routing policy rules |
| kb-model.md | Entity types and fields |
| flights-and-recaps.md | Flight/sprint memory system |
| local-run.md | Local execution setup |
| ideation-notes.md | Extended endpoints, UI mockups, decisions |
| task_file.json | Task schema example |

### Counts

| Category | Count |
|----------|-------|
| Phases | 6 |
| MVP Endpoint Requirements | 18 |
| Extended Endpoints (ideation) | 30+ |
| Phase-specific Endpoints | 4 |
| Expected Module Files | 7 new (beyond MVP) |
| KB Entity Types | 6 |
| Gates | 3 |
| Exit Criteria | 9 |

---

*End of BEE1 Spec Analysis Report*
