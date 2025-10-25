---
deia_routing:
  project: quantum
  destination: docs/projects/
  filename: Efemera-Egg-03-Waves-UI-v0.2.md
  action: incubate
version: 0.2
last_updated: 2025-10-14
created_by: codex-cli (Drone-Lite)
parent_egg: Efemera-The-Game-Outer-Egg-v0.1
integrity:
  checksum: sha256:pending
---

# Efemera — Egg‑03 Waves & UI (v0.2)

Purpose: Evolve the v0.1 prototype with clearer feedback, progression pacing, and HUD polish: rear‑view Earth display, wave banners, streak‑based scoring, refined Threat Meter, and pause/results screens.

---

## Scope (v0.2)
- Rear‑View Earth HUD widget (animated) with threat‑based turbulence overlay.
- Wave system: inter‑wave banner, timing windows, and difficulty ramp.
- Scoring: streak multiplier (+1 per uninterrupted kill), perfect‑wave bonus.
- Threat Meter v2: pass‑through raises Threat; passive decay while “clean”; caps and thresholds.
- Pause menu and simple results screen (score, waves cleared, avg threat).
- New enemy pattern: Swoopers (sine vx) tuned; carriers deferred to v0.3.

Out of scope: sprites/audio/juice (Egg‑04), landing sequence (Egg‑05).

---

## Design Details
### 1) Rear‑View Earth HUD
- Minimal: draw a disc (Earth) in top‑right with slow rotation; optional cloud arc.
- Threat Overlay: at Threat ≥ T1, add subtle jitter; ≥ T2, add flicker/red rim.
- API: `rearview.update(dt, threat)`, `rearview.draw(renderer)`.

### 2) Waves & Banners
- Inter‑wave: 1.5 s banner “Wave N” with brief slow‑spawn window.
- Ramp knobs: spawn count, vy, sine amplitude, spawn cadence.
- API: `waves.update(dt) -> state`, `waves.next()` to advance.

### 3) Scoring & Streaks
- Streak increases by 1 per kill; resets when an enemy passes bottom or on death.
- Score gain: `base(100) * (1 + streak*0.1)`; perfect‑wave bonus = 500.
- HUD shows score and current streak.

### 4) Threat Meter v2
- +1 per pass‑through; cap at 20. During 3 s without pass‑throughs, decay −1 every 5 s.
- Thresholds: T1=5 (rear‑view jitter on), T2=12 (flicker), T3=18 (warning text).
- Persist threat between waves; reset on gameover.

### 5) Pause & Results
- Pause: overlay with “Resume (Space), Retry (R), Quit (Q)” (Quit returns to menu).
- Results: show waves cleared, score, max streak, avg threat.

---

## UI Layout
- Top‑left: Lives; below it: Streak.
- Top‑center: Score; below it: Threat Meter (number + small bar).
- Top‑right: Rear‑View Earth widget.
- Center banners: Wave N (fade in/out), Game Over, Paused.

---

## Acceptance Criteria
- Rear-view renders every frame; threat thresholds visibly change its state.
- Wave banners display between waves; spawning pauses during banner.
- Streak and score increment on kills; streak resets on pass-through.
- Threat increases on pass-through; decays while clean; clamps at cap.
- Pause/resume works; results screen appears on gameover with required stats.
- 60 FPS on desktop; no console errors.
- Telemetry emits events (fire/kill/pass/pickup/thruster) and frame snapshots; `L` downloads JSONL.
- Bot API (`window.GameAPI`) is accessible; returns a valid state snapshot.

---

## KPIs (v0.2)
- Avg frame time ≤ 8 ms on a mid‑range laptop.
- Clear wave readability in playtests; players can state “what’s next.”
- Retry within session ≥ 40% (qualitative check acceptable).

---

## Hatch Payload (Implementation Plan)
```pseudocode
def hatch():
  # New modules
  write("games/efemera-vs-aliendas/src/game/rearview.js", template_rearview_js)
  write("games/efemera-vs-aliendas/src/game/banners.js", template_banners_js)
  write("games/efemera-vs-aliendas/src/game/scoring.js", template_scoring_js)
  # Extend waves with inter-wave states and ramp knobs
  patch("games/efemera-vs-aliendas/src/game/waves.js", add_interwave_and_ramp)
  # Wire into main loop & UI
  patch("games/efemera-vs-aliendas/src/main.js", integrate_rearview_banners_scoring_pause)
  patch("games/efemera-vs-aliendas/src/game/ui.js", add_score_streak_threat_bar)
  log("v0.2 features scaffolded: rear-view, banners, scoring, threat v2, pause/results")
```

---

## Repot References
- Index: `docs/REPOT.md`
- Process: `docs/process/EFEMERA-DEV-PROCESS.md`
- Project home: `games/efemera-vs-aliendas/`

---

## Template Stubs
```js
// template_rearview_js
export class RearView {
  constructor() { this.t = 0; }
  update(dt, threat) { this.t += dt; this.threat = threat|0; }
  draw(r) {
    const x=432, y=40, rad=28; // top-right corner-ish
    // Earth disc
    r.rect(x-rad, y-rad, rad*2, rad*2, '#18467a');
    // Simple “rotation” line
    const px = x + Math.cos(this.t*0.5)*rad*0.8;
    const py = y + Math.sin(this.t*0.5)*rad*0.8;
    r.rect(px-2, py-2, 4, 4, '#85b8ff');
    // Threat overlay
    if (this.threat >= 5) r.text('~', x, y+rad+12, '#ffd34e', 14);
    if (this.threat >= 12) r.text('!', x+rad+6, y, '#e05b5b', 16, 'left');
  }
}
```

```js
// template_banners_js
export class Banners {
  constructor() { this.text = ''; this.t = 0; this.active = false; }
  show(text, duration=1.5) { this.text=text; this.t=duration; this.active=true; }
  update(dt) { if (this.active) { this.t -= dt; if (this.t<=0) this.active=false; } }
  draw(r) { if (this.active) r.text(this.text, 240, 360, '#fff', 28); }
}
```

```js
// template_scoring_js
export class Scoring {
  constructor() { this.score=0; this.streak=0; this.maxStreak=0; this.kills=0; }
  kill() { this.kills++; this.streak++; this.maxStreak=Math.max(this.maxStreak,this.streak); this.score += Math.round(100*(1+this.streak*0.1)); }
  miss() { this.streak=0; }
  reset() { this.score=0; this.streak=0; this.maxStreak=0; this.kills=0; }
}
```

---

## Test Plan
- Manual: Verify banners between waves; rear‑view reacts at Threat 5/12; pause/resume; gameover results show streak and score.
- Performance: DevTools performance sample during Wave 2; ensure frame budget holds.

---

## Next
- Egg‑04 — Art/Audio/Juice (v0.3): sprites, SFX/music, particles, shake.
