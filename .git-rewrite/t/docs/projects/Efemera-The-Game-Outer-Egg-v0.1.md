---
deia_routing:
  project: quantum
  destination: docs/projects/
  filename: Efemera-The-Game-Outer-Egg-v0.1.md
  action: incubate
version: 0.1
last_updated: 2025-10-14
created_by: codex-cli (Drone-Lite)
parent_egg: DEIA-Egg-Spec-v1.0
linked_subsystems:
  - DEIA-Orchestrator
  - Drone-Lite
  - File-Drone-Subsystem
integrity:
  checksum: sha256:pending
---

# Efemera The Game — Outer Egg (v0.1)

Purpose: Define the canonical story, product/market framing, design roles, build order, sprints, acceptance criteria, KPIs, and a chain of nested eggs to hatch a vertical-scrolling 80s‑style space shooter (Galaga‑inspired) with a climactic Atlantic landing sequence. AKA “Efemera vs. the Aliendas.”

---

## 1. Executive Summary
- Genre: Vertical Scroller, 80s Arcade (Galaga/1942 inspiration)
- Core Loop: Move left/right, shoot incoming enemies, prevent pass‑throughs, survive waves, then execute a landing mini‑sequence on an Atlantic pad.
- Hook: Rear‑view Earth display as you descend; narrative canon that ties Episode 1 (vertical scroller) to Episode 2 (side‑scroller: “Mario meets Joust meets K‑Pop Demons”).
- Platforms: Web (desktop first, mobile friendly). Later: Electron/itch.io build.
- Monetization: Free/open; focus on portfolio/demo quality and replayability.

---

## 2. Canon: Story, World, and Tone
### 2.1 Backstory
You launch from Texas on a high‑orbit reconnaissance mission. As you burn for re‑entry, sensors spike: unknown craft — the Aliendas — converging. Earth swells in the rear‑view mirror; comms are jammed. Your mission: return home. Your reality: fight through the gauntlet, keep them from slipping past you toward Earth, then stick the landing on an Atlantic recovery pad.

### 2.2 Factions & Entities
- Player Craft: “EF‑01 Efemera,” experimental re‑entry interceptor with limited lateral thrust, forward cannons, and landing jets.
- Aliendas: 
  - Swarmers (grunts): Straight and sine waves; easy pickings in numbers.
  - Swoopers: Dive/arc patterns; punish tunnel vision.
  - Shielders: Brief invulnerability windows; require timing.
  - Carriers: Release micro‑drones when destroyed; risk‑reward.
  - Herald (mid‑boss): Screenshake volleys; teaches pattern reading.
- Ground Crew (off‑screen ally): Automated pad telemetry; final landing guidance.

### 2.3 Episode Arc
- Episode 1 (this game): Re‑entry Gauntlet → Mid‑Boss → Final Approach → Atlantic Landing.
- Episode 2 (tease): Side‑scrolling incursion inside the orbital ring — “Mario Bros meets Joust meets K‑Pop Demons.” 

### 2.4 Tone & Aesthetic
- Bright arcade palette, crunchy SFX, readable silhouettes. Music leans synthwave/space‑disco. UI clear and snappy; “juicy” feedback (particles, pop, minimal screenshake).

---

## 3. Product & Market Framing
### 3.1 Audience
- Retro arcade fans, casual browser gamers, dev/demo showcase viewers.

### 3.2 Competitive Notes
- Benchmarks: Galaga, Space Invaders, 1942; modern learnings from Vampire Survivors on feedback density.
- Differentiators: Narrative landing sequence; rear‑view Earth UI; wave “miss penalty” (enemies that slip past increase landing difficulty).

### 3.3 KPIs (Internal)
- Median session length (target ≥ 4 minutes).
- Wave completion rate; landing success rate (~30–50% for balanced challenge).
- 95th percentile frame time < 16.7 ms on mid‑range laptops.
- Retention proxy: % of players who retry within session (≥ 40%).

---

## 4. High‑Level Design (GDD Snapshot)
### 4.1 Controls
- Left/Right: Arrow keys (A/D as alt). 
- Shoot: Spacebar. Autofire toggle (later option) off by default for 80s feel.

### 4.2 Mechanics
- Player: 1–3 hits (configurable), fire rate gate, simple width‑boundaries.
- Enemies: Patterned spawns in waves; if they pass bottom bound, a “Threat Meter” increases (affects landing wind jitter/fuel margin).
- Power‑ups (v0.3+): Rapid fire, spread, shield, slow‑mo burst.
- Scoring: Per kill + streak multiplier; bonus for perfect wave (no pass‑throughs).
- Landing Sequence: Switch to guided descent UI; maintain pad alignment, throttle landing jets, compensate wind jitter influenced by Threat Meter.

### 4.3 Systems
- Patterned Spawner, Bullets/Pooling, Collision (AABB), Health/Invuln windows, Score/Multiplier, FX (particles/shake), AudioBus, State Machine (menu → waves → landing → results).

### 4.4 UI & HUD
- Lives, Score, Threat Meter, Rear‑View Earth display (animated), Wave banner, Landing instruments (altitude, velocity, drift).

### 4.5 Accessibility
- Reduced‑motion mode, mute toggle persisted, key remapping (later).

---

## 5. Team Roles (Hats)
- Creative Director: Canon, tone, quality bar.
- Game Designer: Waves, balance, power‑ups, landing parameters.
- Gameplay Engineer: Player/enemy/bullet logic, collisions.
- Rendering/Perf Engineer: Draw loop, pooling, profiling, perf wins.
- Audio Designer: SFX/Music, mix, ducking, mute persistence.
- Pixel Artist: Sprites, backgrounds, animation frames.
- UI/UX Designer: HUD clarity, state transitions, inputs.
- Producer/QA: Sprint planning, acceptance, playtest loops.

---

## 6. Tech Stack
- HTML5 Canvas, ES Modules, lightweight engine (custom loop, pooling).
- No external network; all local assets. Optional future: Pixi.js.
- Build: plain static (works via file:// or simple server). 

---

## 7. Build Order & Sprints (v0.1 → v1.0)
### Sprint 0 — Preproduction (1–2 days)
- Design finalize: canon, waves catalogue, landing model. Perf targets. Input spec.
- Prototype spikes: draw loop, bullets/collision, landing math.
Acceptance: Written GDD snapshot; spikes committed; perf budget documented.

### Sprint 1 — Core Prototype v0.1 (2–3 days)
- Player ship (LR, shoot), bullet pool, basic enemies (Swarmers), collisions, score, HUD stub.
- States: menu → play → gameover. Rear‑view Earth placeholder.
Acceptance: 60 FPS on mid‑range laptop; 3+ waves; gameover loop solid.

### Sprint 2 — Waves & UI v0.2 (2–3 days)
- Spawner system (patterns: line, sine, swoop), streak multiplier, Threat Meter, wave banners.
- Rear‑view Earth animation; results screen. Basic tuning.
Acceptance: 6–8 wave set; Threat Meter modifies landing params.

### Sprint 3 — Art, Audio, Juice v0.3 (3–4 days)
- Pixel sprites, parallax bg; SFX (shoot, hit, explode), music loop; particles/shake.
Acceptance: Playtest “fun” meter ≥ 7/10 from 3 testers; readability OK.

### Sprint 4 — Landing Sequence v0.4 (2–3 days)
- Landing UI/instruments; wind jitter from Threat Meter; pad collider; success/fail outcomes.
Acceptance: 30–50% first‑time landing success at medium threat.

### Sprint 5 — Tuning & Power‑ups v0.5 (3–4 days)
- Power‑ups (rapid, spread, shield), balance pass, HUD polish, reduced‑motion.
Acceptance: Difficulty curve smooth; accessibility toggles persisted.

### Beta v0.9 — Perf/Polish (2–3 days)
- Mobile input tuning, perf audit, bugfixes, juice tweaks.
Acceptance: 95p frame < 16.7ms; no blocker bugs; mobile playable.

### Release v1.0
- Trailer GIFs, README, itch.io page (optional), tag and ship.

---

## 8. Nested Eggs (Russian‑Doll Plan)
The Outer Egg orchestrates sequential eggs. Each egg includes templates/payload and acceptance.

1. Egg‑01‑Research‑Canon‑v0.1.md — lock story, waves, landing math; KPIs, perf budget.
2. Egg‑02‑Core‑Prototype‑v0.1.md — player/bullets/enemy basics; collisions; HUD stub.
3. Egg‑03‑Waves‑UI‑v0.2.md — spawner patterns, Threat Meter, banners, rear‑view.
4. Egg‑04‑Art‑Audio‑Juice‑v0.3.md — sprites, SFX/music, particles, shake.
5. Egg‑05‑Landing‑Sequence‑v0.4.md — instruments, wind jitter, pad landing.
6. Egg‑06‑Tuning‑Powerups‑v0.5.md — balance, power‑ups, accessibility.
7. Egg‑07‑Beta‑Polish‑v0.9.md — perf, mobile, bugfixes.
8. Egg‑08‑Release‑v1.0.md — packaging, page, trailer GIFs.

Filenames (suggested, routed to docs/projects/):
```
Efemera-Egg-01-Research-Canon-v0.1.md
Efemera-Egg-02-Core-Prototype-v0.1.md
Efemera-Egg-03-Waves-UI-v0.2.md
Efemera-Egg-04-Art-Audio-Juice-v0.3.md
Efemera-Egg-05-Landing-Sequence-v0.4.md
Efemera-Egg-06-Tuning-Powerups-v0.5.md
Efemera-Egg-07-Beta-Polish-v0.9.md
Efemera-Egg-08-Release-v1.0.md
```

---

## 9. Hatch Payload (Master Orchestrator Pseudocode)
```pseudocode
def hatch():
  # Stage 0: Create project skeleton
  scaffold("games/efemera-vs-aliendas/")
  mkdir("css/", "src/engine/", "src/game/", "assets/sprites/", "assets/audio/")
  write("index.html", template_index_html)
  write("css/styles.css", template_styles_css)
  write("src/engine/loop.js", template_loop_js)
  write("src/engine/input.js", template_input_js)
  write("src/engine/renderer.js", template_renderer_js)
  write("src/engine/physics.js", template_physics_js)
  write("src/engine/assets.js", template_assets_js)
  write("src/engine/storage.js", template_storage_js)
  write("src/game/player.js", template_player_js)
  write("src/game/bullets.js", template_bullets_js)
  write("src/game/enemies.js", template_enemies_js)
  write("src/game/waves.js", template_waves_js)
  write("src/game/ui.js", template_ui_js)
  write("src/game/landing.js", template_landing_js)
  write("src/main.js", template_main_js)
  # Stage 1+: Defer to nested eggs for art/audio/juice, tuning, landing polish, release.
  log("Efemera project skeleton created. Proceed with Egg‑02 for core gameplay.")
```

---

## 10. Acceptance Criteria (Outer Egg)
- Canon documented (this file) and referenced in nested eggs.
- Build plan and sprints clear; acceptance criteria per sprint defined.
- Project skeleton templates enumerated; hatching path defined.
- KPIs and perf budgets listed; risks noted.

---

## 11. Risks & Mitigations
- Scope creep: Lock v1.0 to core loop + landing; defer power‑ups if needed.
- Performance on mobile: Use pooling, cap particles, reduce motion mode.
- Readability: High‑contrast sprites, bullet visibility, controlled screenshake.

---

## 12. Minimal Template Stubs (Selected)
```html
<!-- template_index_html (games/efemera-vs-aliendas/index.html) -->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Efemera vs. the Aliendas</title>
    <link rel="stylesheet" href="css/styles.css" />
  </head>
  <body>
    <canvas id="game" width="480" height="720"></canvas>
    <script type="module" src="src/main.js"></script>
  </body>
  </html>
```

```js
// template_main_js (games/efemera-vs-aliendas/src/main.js)
import { createLoop } from './engine/loop.js';
import { Input } from './engine/input.js';
import { Renderer } from './engine/renderer.js';
import { Physics } from './engine/physics.js';
import { Player } from './game/player.js';
import { Bullets } from './game/bullets.js';
import { Enemies } from './game/enemies.js';
import { Waves } from './game/waves.js';
import { UI } from './game/ui.js';

const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const input = new Input(canvas);
const render = new Renderer(ctx, canvas.width, canvas.height);
const physics = new Physics();

const player = new Player(physics, { x: 240, y: 640 });
const bullets = new Bullets();
const enemies = new Enemies(physics);
const waves = new Waves(enemies);
const ui = new UI();

let state = 'menu';

const loop = createLoop({
  update(dt) {
    input.update();
    if (state === 'menu') {
      if (input.shoot()) state = 'play';
    } else if (state === 'play') {
      player.update(dt, input, bullets);
      bullets.update(dt);
      waves.update(dt);
      enemies.update(dt, player, bullets);
      if (enemies.anyPassed()) ui.threat += 1;
      if (player.dead) state = 'gameover';
      if (waves.readyForLanding()) state = 'landing';
    } else if (state === 'landing') {
      // Placeholder: landing handled by landing.js in Egg‑05
    } else if (state === 'gameover') {
      if (input.shoot()) { ui.reset(); player.reset(); enemies.reset(); waves.reset(); state = 'play'; }
    }
  },
  draw() {
    render.clear('#0b1020');
    enemies.draw(render);
    bullets.draw(render);
    player.draw(render);
    ui.draw(render, state);
  }
});

loop.start();
```

```js
// template_player_js (games/efemera-vs-aliendas/src/game/player.js)
export class Player {
  constructor(physics, pos) { this.p = physics; this.x = pos.x; this.y = pos.y; this.w=28; this.h=20; this.speed=260; this.cool=0; this.dead=false; }
  reset() { this.x=240; this.y=640; this.cool=0; this.dead=false; }
  update(dt, input, bullets) {
    if (input.left()) this.x -= this.speed * dt;
    if (input.right()) this.x += this.speed * dt;
    this.x = Math.max(24, Math.min(480-24, this.x));
    this.cool -= dt;
    if (input.shoot() && this.cool <= 0) { bullets.fire(this.x, this.y-18); this.cool = 0.18; }
  }
  draw(r) { r.rect(this.x-14, this.y-10, this.w, this.h, '#4ec0ca'); }
}
```

```js
// template_bullets_js (games/efemera-vs-aliendas/src/game/bullets.js)
export class Bullets {
  constructor() { this.items = []; }
  fire(x, y) { this.items.push({ x, y, vy: -520, w:2, h:8 }); }
  update(dt) { this.items = this.items.map(b => ({ ...b, y: b.y + b.vy*dt })).filter(b => b.y > -16); }
  draw(r) { this.items.forEach(b => r.rect(b.x-1, b.y-8, b.w, b.h, '#ffd34e')); }
}
```

```js
// template_enemies_js (games/efemera-vs-aliendas/src/game/enemies.js)
export class Enemies {
  constructor(physics) { this.p = physics; this.items = []; this.passed = 0; }
  spawn(x, y, vx=0, vy=120, type='grunt') { this.items.push({ x, y, vx, vy, w:24, h:18, type, hp:1 }); }
  update(dt, player, bullets) {
    this.items = this.items.map(e => ({ ...e, x: e.x + e.vx*dt, y: e.y + e.vy*dt }))
      .filter(e => { if (e.y > 740) { this.passed++; return false; } return true; });
    // bullet collisions
    bullets.items = bullets.items.filter(b => {
      const hit = this.items.find(e => !(e.x+e.w < b.x || e.x > b.x+b.w || e.y+e.h < b.y || e.y > b.y+b.h));
      if (hit) hit.hp -= 1; 
      return !hit;
    });
    this.items = this.items.filter(e => e.hp > 0);
  }
  anyPassed() { const p = this.passed>0; this.passed=0; return p; }
  reset() { this.items=[]; this.passed=0; }
  draw(r) { this.items.forEach(e => r.rect(e.x-12, e.y-9, e.w, e.h, '#e05b5b')); }
}
```

```js
// template_waves_js (games/efemera-vs-aliendas/src/game/waves.js)
export class Waves {
  constructor(enemies) { this.enemies = enemies; this.t=0; this.wave=0; }
  update(dt) {
    this.t += dt;
    if (this.wave===0 && this.t>0.5) { for (let i=0;i<8;i++) this.enemies.spawn(60+i*50, -i*80); this.wave=1; }
    if (this.wave===1 && this.t>6) { for (let i=0;i<6;i++) this.enemies.spawn(80+i*60, -i*70, Math.sin(i)*40, 140); this.wave=2; }
    if (this.wave===2 && this.t>12) { for (let i=0;i<10;i++) this.enemies.spawn(40+i*40, -i*60, 0, 180); this.wave=3; }
  }
  readyForLanding() { return this.wave>=3 && this.t>18; }
  reset() { this.t=0; this.wave=0; }
}
```

```js
// template_ui_js (games/efemera-vs-aliendas/src/game/ui.js)
export class UI {
  constructor() { this.score=0; this.lives=3; this.threat=0; }
  reset() { this.score=0; this.lives=3; this.threat=0; }
  draw(r, state) {
    r.text(`Lives ${this.lives}`, 60, 28, '#fff', 18, 'left');
    r.text(`Threat ${this.threat}`, 240, 28, '#ffd34e', 18);
    if (state==='menu') r.text('Press Space to Start', 240, 360, '#fff', 24);
    if (state==='gameover') r.text('Game Over — Space to Retry', 240, 360, '#fff', 24);
  }
}
```

```js
// template_loop_js / input_js / renderer_js / physics_js / assets_js / storage_js
// Reuse minimal versions from Flappy‑Bird egg; specialized in nested eggs.
```

---

## 13. Next Steps
- Hatch Egg‑01 (Research & Canon) to lock patterns and landing parameters.
- Then hatch Egg‑02 (Core Prototype v0.1) to produce a playable skeleton under `games/efemera-vs-aliendas/`.

**End of Outer Egg — Efemera The Game (v0.1)**

