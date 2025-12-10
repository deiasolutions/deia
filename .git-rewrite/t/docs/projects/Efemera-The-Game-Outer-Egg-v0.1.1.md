---
deia_routing:
  project: quantum
  destination: docs/projects/
  filename: Efemera-The-Game-Outer-Egg-v0.1.1.md
  action: incubate
version: 0.1.1
last_updated: 2025-10-14
created_by: codex-cli (Drone-Lite)
parent_egg: Efemera-The-Game-Outer-Egg-v0.1
integrity:
  checksum: sha256:pending
---

# Efemera The Game — Outer Egg (v0.1.1)

Purpose: Same as v0.1, plus mandatory DEIA logging policy and hatch requirements so every project starts with a paper trail from step one.

---

## Changes from v0.1
- Adds Logging Policy & Instrumentation requirements.
- Extends Hatch Payload to create a DEIA session log immediately and record each scaffolded artifact.
- Updates acceptance to verify presence and contents of the initial session log.

---

## Logging Policy & Instrumentation (Mandatory)
- Start a DEIA session at hatch time with context: project, goals, scope, and version.
- Append a log entry after each scaffold step (e.g., created index.html, player.js, waves.js) and after each major decision.
- Update project resume and session index automatically (handled by the DEIA logger).
- Store all logs under `.deia/sessions/`; ensure `INDEX.md` is updated.

### Hatch Payload Additions (pseudocode)
```pseudocode
def hatch():
  # 0) Initialize DEIA session
  session = deia.session.create(
    context="Efemera The Game hatch v0.1.x — initialize project",
    decisions=["Create project skeleton", "Enable mandatory logging"],
    files_modified=[],
    next_steps="Scaffold engine/game modules; log each step"
  )
  log(session, "Hatching started: creating directories and templates")

  # 1) Scaffold project skeleton (same as v0.1)
  scaffold(...)
  log(session, "Scaffold complete: index.html, engine/, game/ modules created")

  # 2) Record acceptance snapshot and versions
  log(session, "Acceptance: session exists; files created; next: Egg-02 core prototype")
```

### Acceptance (Logging)
- `.deia/sessions/` contains an active session created during hatch.
- Session includes context, decisions, files created, and next steps.
- `project_resume.md` and `INDEX.md` updated.

---

## All Other Sections
- Canon, product framing, roles, sprints, nested eggs, tech stack, and templates remain as in v0.1 (see Efemera-The-Game-Outer-Egg-v0.1.md).

---

## Observability & AI Test Hooks
- Telemetry: Implement JSONL runtime telemetry with events (frame, fire, kill, pass, pickup, thruster) and per-frame snapshots.
- Bot API: Expose `window.GameAPI` with `setController`, `clearController`, `getState`, `stepOnce` for future PlayerBot/NN.
- Acceptance: At least one telemetry sample captured; API reachable from console.

---

## Repot Pointers (Repo Depot)
- Process: `docs/process/EFEMERA-DEV-PROCESS.md`
- Eggs: `docs/projects/`
- Game runtime: `games/efemera-vs-aliendas/`
- Art mockups: `games/efemera-vs-aliendas/art/`
- Index: `docs/REPOT.md`

If this egg omits long templates or assets, refer to the Repot index for the canonical source files.

---

## Next
- Apply similar logging acceptance to Egg‑02 and beyond.
