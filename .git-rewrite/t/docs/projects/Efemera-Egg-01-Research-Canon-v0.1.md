---
deia_routing:
  project: quantum
  destination: docs/projects/
  filename: Efemera-Egg-01-Research-Canon-v0.1.md
  action: incubate
version: 0.1
last_updated: 2025-10-14
created_by: codex-cli (Drone-Lite)
parent_egg: Efemera-The-Game-Outer-Egg-v0.1
integrity:
  checksum: sha256:pending
---

# Efemera — Egg‑01 Research & Canon (v0.1)

Purpose: Lock story/canon, catalog enemy patterns, define landing model, KPIs, and perf budgets to guide v0.1 → v1.0.

---

## 1) Canon Lock
- Mission: Return to Earth through Aliendas gauntlet; protect Earth by intercepting waves; land on Atlantic pad.
- Rear‑view Earth: Ambient animation; threat meter affects landing turbulence and fuel margin.
- Difficulty Curve: 3 acts — Gauntlet (teaching patterns), Mid‑boss (pattern mastery), Final approach (attrition → landing).

---

## 2) Reference & Market Notes
- Core inspirations: Galaga (lanes, precision), 1942 (swoops), Space Invaders (pressure), Vampire Survivors (feedback pacing).
- Audience: Retro fans and portfolio/demo viewers; desktop‑first.

---

## 3) Mechanics Spec (Initial)
### Player
- Lateral speed: 260 px/s; fire gate: 0.18 s; bullet speed: −520 px/s.
- Hit model: 3 lives (v0.1 may ignore damage and focus on threat/landing link).

### Enemies (v0.1 subset)
- Swarmers: Straight descent; spawn in rows; vy≈120 px/s.
- Swoopers: Sinusoidal vx around center; vy≈140 px/s; amplitude≈40 px.
- Carriers (v0.2+): Split into micro‑drones on death.

### Threat Meter
- +1 per enemy that passes bottom of screen; decays slowly (later) or persists through waves.
- Landing turbulence ∝ threat (wind jitter amplitude; fuel margin shrink).

---

## 4) Waves Catalogue (Draft)
| Wave | Pattern                    | Count | Params                                   |
| ---- | -------------------------- | ----- | ---------------------------------------- |
| 1    | Line descent               | 8     | x=60..410 step 50, vy=120                 |
| 2    | Sine swoop                 | 6     | x=80..440 step 60, vy=140, ax=±40         |
| 3    | Dense column               | 10    | x=40..400 step 40, vy=180                 |
| 4    | Mixed (v0.2)              | 12    | alternates straight/sine                  |
| 5    | Herald (v0.3)             | 1     | Mid‑boss volley & gaps                    |

Acceptance: Waves 1–3 tuned to be beatable without hits; pass‑throughs teach threat.

---

## 5) Landing Model (Stub)
- Inputs: Altitude, vertical velocity, horizontal drift.
- Controls: Landing jets (auto stabilize), lateral nudge.
- Success window: vy ∈ [−120, −40] px/s; drift < 8 px; pad overlap ≥ 90%.
- Threat effects: wind jitter amplitude = 2 px + 0.5·threat; fuel time = 12 s − 0.2·threat.

---

## 6) KPIs & Budgets
- 95p frame time < 16.7 ms; GC spikes < 5% of frames (desktop).
- Playtest: first session ≥ 3 min; retry rate ≥ 40%.
- Input latency: no held key lag; firing consistent with gate.

---

## 7) Deliverables & Acceptance
- This doc complete; wave table and landing parameters recorded.
- Test checklist added to Egg‑02; tuning notes updated after first prototype.

---

## 8) Hatch Payload (Research Artifacts)
```pseudocode
def hatch():
  write("games/efemera-vs-aliendas/docs/waves.md", exported_wave_table)
  write("games/efemera-vs-aliendas/docs/landing.md", landing_parameters)
  log("Research canon artifacts created")
```

---

## Repot Reference
- Index: `docs/REPOT.md`
- Process: `docs/process/EFEMERA-DEV-PROCESS.md`
- Game runtime: `games/efemera-vs-aliendas/`
