# DEIA + RAQCOON: Path to "Spec In -> Code Out"

## Purpose
Define the shortest, practical path from the current MVP to a fully automated code-production system where a spec can become verified code with minimal human intervention.

## Current State (MVP)
- Local-first API, repo-root discipline, CLI bee launch.
- Task file loop and RAQCOON KB basics.
- Mockups wired to local API, gates for git commit/push.

## Target Outcome
- Structured spec intake.
- Automatic task decomposition and routing.
- Iterative code generation, testing, and review loops.
- Safe git operations with human gates.
- Observability (costs, logs, traces) to diagnose and optimize.

## Phase 1: Spec Intake + Task Graph (fastest lift)
Goal: turn a spec into a machine-readable plan and task graph.

1) Spec schema + parser
- Define a single spec schema: goals, constraints, acceptance criteria, scope exclusions.
- Add a parser to convert markdown/spec into JSON.

2) Task graph builder
- Break spec into tasks with dependencies, owners, and routing lane.
- Store as "flight" units (sprint/flight structure).

3) Planner bot (Q33N)
- Reads spec and outputs task graph.
- Creates tasks autonomously in `.deia/hive/tasks/`.

Deliverables:
- `schemas/spec.json`
- `runtime/spec_parser.py`
- `runtime/task_graph.py`
- Spec-to-tasks flow in API (new endpoint: `/api/spec/plan`).

## Phase 2: Execution Loop + Verification
Goal: build the core "execute -> test -> iterate" loop.

1) Task executor
- Pull tasks, route to lane (CLI bee, local LLM, or task file).
- Collect responses and mark tasks complete/blocked.

2) Verification runner
- Hook basic test/lint commands per project.
- Capture results into task history.

3) Auto-iteration
- If tests fail, create a follow-up task automatically.

Deliverables:
- `runtime/executor.py`
- `runtime/verifier.py`
- `/api/tasks/run` and `/api/tasks/verify` endpoints.

## Phase 3: Git Automation + Gates
Goal: safe, automated commits with human approval gates.

1) Patch assembly
- Collect file changes into a coherent change set.
- Ensure repo-root enforcement and clean staging.

2) Review gates
- Pre-sprint review checkbox
- Per-flight commit permission
- Human override

3) Commit + push workflow
- Auto-commit per flight when allowed.
- Optional PR generation (future).

Deliverables:
- `runtime/git_flow.py`
- Gate-integrated commit pipeline.

## Phase 4: Observability + Cost Controls
Goal: track costs, time, and quality across bots.

1) Cost logging
- Tokens and provider cost per message.
- Per-task cost aggregation.

2) Analytics
- Top failure modes, common test failures, task rework rate.
- Dashboards for flight performance.

Deliverables:
- `runtime/telemetry.py`
- `/api/summary` extensions (cost + per-flight stats).

## Phase 5: Advanced RAQCOON (Quality + Safety)
Goal: use KB to prevent bad patterns and improve results.

1) Dos/Don'ts + anti-pattern rules
- Rule enforcement per task type.

2) Retrieval policies
- Strict mode for critical paths (security, infra, payments).

Deliverables:
- KB policy engine.
- Rule-based blockers before execution.

## Phase 6: Full "Spec In -> Code Out" Workflow
Goal: single flow from spec to tested code.

Flow:
1) Spec uploaded
2) Planner bot creates tasks
3) Executor runs tasks
4) Verifier runs tests
5) Git pipeline stages commit
6) Human approves -> push

Deliverables:
- Single UI button: "Run Spec"
- End-to-end status with flight checkpoints.

## Minimal Success Criteria
- A spec can generate a task graph automatically.
- The system executes tasks, runs tests, and reports outcomes.
- Commits are created automatically with human gate.

## Near-Term Build Order (Recommended)
1) Spec schema + parser
2) Task graph builder + planning endpoint
3) Executor loop (basic lane routing)
4) Verification runner (basic tests)
5) Git flow integration (commit gate)
6) Cost + telemetry expansion

## Notes
- All phases must preserve repo-root discipline and local-first operation.
- Modular design keeps it portable to hosted environments later.
