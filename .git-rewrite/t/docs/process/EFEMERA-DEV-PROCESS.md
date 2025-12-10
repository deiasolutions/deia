# Efemera — Development Process (Observability + AI Test Hooks)

Purpose: Bake measurement, change tracking, and AI testability into the workflow so we never fly blind.

## Core Requirements (Always On)
- DEIA session logging
  - Start a session at hatch; append for each feature/decision.
  - Artifacts: `.deia/sessions/` with INDEX; `project_resume.md` updated.
- Change request tracking
  - Log customer notes verbatim + summary + impact + decision in the active session.
  - Tag requests with IDs (CR-YYYYMMDD-n) for quick reference.
- Time tracking (lightweight)
  - Capture timestamps for: request arrival, clarification asked, response received, implementation start/finish.
  - Include in DEIA session updates; derive wait time and active time.

## Game Telemetry (Runtime)
- In-game JSONL telemetry stream with key events: `session_start`, `frame`, `fire`, `kill`, `pass`, `pickup`, `thruster`.
- Snapshot per frame: reticle (x,y), course offset (ox,oy,off), threat, counts (enemies, pickups), resources (solar,h2).
- Local download shortcut (press `L`) writes `telemetry.jsonl`.

## Bot Interface (For Future PlayerBot/NN)
- Expose a minimal browser API on `window.GameAPI`:
  - `setController(fn)`, `clearController()`, `getState()`, `stepOnce()`.
  - Controller contract: returns `{ aimX, aimY, fire, thrusters }`.
- State includes enemies (x,y,dist,friendly), reticle, resources, and course.
- No ML in-scope now — this is purely an integration seam so we can plug a tester bot.

## End-of-Sprint Checklist
- Session logs complete; all change requests referenced by ID.
- Telemetry sample captured (attach `telemetry.jsonl` to session).
- GameAPI exercised by a trivial scripted controller (smoke test).
- KPIs reviewed (latency, session length proxy, pass-throughs) and noted.
- Next-sprint eggs updated with any new customer asks (K-Pop Demons, etc.).

## Tag & Note Conventions
- NB (Note Bee): prefix for must-read notes or decisions (e.g., `NB: Leftenant TTL=24h`).
- Hash tags in logs: `#note`, `#log type`, `#tag type`, `#tags`, `#ask`, `#log idea`, `#log win`, `#log blocker`.

## Future Eggs (Ideas)
- PlayerBot-Train-v0: curriculum + scripted controller → heuristic → NN.
- FlappyBird-Bot-v0: reuse API on flappy scaffold; shared telemetry schema.
- Visual polish egg: sprite pipeline, particles, and SFX bus.
