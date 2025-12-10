---
deia_routing:
  project: quantum
  destination: docs/projects/
  filename: Efemera-Egg-02-Core-Prototype-v0.1.md
  action: incubate
version: 0.1
last_updated: 2025-10-14
created_by: codex-cli (Drone-Lite)
parent_egg: Efemera-The-Game-Outer-Egg-v0.1
integrity:
  checksum: sha256:pending
---

# Efemera — Egg‑02 Core Prototype (v0.1)

Purpose: Hatch a playable skeleton — left/right movement, shooting, basic waves, collisions, HUD, states (menu → play → gameover). Desktop web target, 60 FPS.

---

## Scope
- Player: LR movement, rate‑limited shots.
- Bullets: Pool/list, upward motion, pruning.
- Enemies: Straight and sine patterns, pass‑through increments Threat.
- Waves: 3 scripted waves from Egg‑01 table.
- UI: Lives (stub), Threat, menu/gameover text.
- States: menu, play, gameover; landing placeholder (later egg).

---

## Hatch Payload (Scaffold)
```pseudocode
def hatch():
  scaffold("games/efemera-vs-aliendas/")
  write index.html, css/styles.css
  write src/engine/{loop,input,renderer,physics}.js
  write src/game/{player,bullets,enemies,waves,ui}.js
  write src/main.js
  log("Core prototype created")
```

---

## Repot References
- Index: `docs/REPOT.md`
- Process: `docs/process/EFEMERA-DEV-PROCESS.md`
- Project home: `games/efemera-vs-aliendas/`

---

## Acceptance Criteria
- Runs at ~60 FPS on desktop; no console errors.
- Move with Arrow keys; Space fires with rate limit.
- 3+ waves spawn and descend; enemies that pass bottom bump Threat.
- Collisions remove enemies; gameover triggers and restart works.
- DEIA logging: session created at start of hatch; entries appended for scaffold steps and decisions.

---

## Out of Scope (defer)
- Sprites/art/audio, power‑ups, landing sequence, mobile polish, save data.

---

## Next Eggs
- Egg‑03 Waves & UI v0.2 (rear‑view Earth, banners, streaks)
- Egg‑04 Art/Audio/Juice v0.3
