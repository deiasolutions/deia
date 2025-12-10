---
deia_routing:
  project: quantum
  destination: docs/projects/
  filename: Flappy-Bird-BuildPlan-Egg-v1.0.md
  action: incubate
version: 1.0
last_updated: 2025-10-14
created_by: codex-cli (Drone-Lite)
parent_egg: DEIA-Egg-Spec-v1.0
linked_subsystems:
  - DEIA-Orchestrator
  - File-Drone-Subsystem
  - Drone-Lite
integrity:
  checksum: sha256:pending
---

# Flappy Bird Game Build Plan (Egg v1.0)

Purpose: Build a kick-ass Flappy Bird game (fast, polished, replayable) suitable for web delivery with crisp controls, solid physics, and juice.

---

## 1. Objectives
1. HTML5 Canvas game at 60 FPS with mobile + desktop controls.
2. Tight physics: gravity, flap impulse, terminal velocity, AABB collisions.
3. Procedural pipes with difficulty ramp; parallax background + ground scroll.
4. Juice: particle pops on flap/death, screen shake, tweened UI.
5. UX: start screen, pause, resume, game over, high score (localStorage).
6. Audio: flap, score, hit, swoosh; mute toggle with persisted preference.

---

## 2. Directory Structure (to be generated)

```
games/flappy-bird/
  index.html
  css/
    styles.css
  src/
    main.js
    engine/
      loop.js
      input.js
      audio.js
      physics.js
      renderer.js
      assets.js
      storage.js
    game/
      bird.js
      pipes.js
      ground.js
      background.js
      score.js
      ui.js
      particles.js
  assets/
    sprites/
      bird.png
      pipe.png
      background.png
      ground.png
      digits.png
    audio/
      flap.wav
      score.wav
      hit.wav
      swoosh.wav
  README.md
```

---

## 3. Payload (hatch pseudocode)

```pseudocode
def hatch():
  scaffold("games/flappy-bird/")
  write_file("index.html", template_index_html)
  write_file("css/styles.css", template_styles_css)
  write_file("src/main.js", template_main_js)
  write_file("src/engine/loop.js", template_loop_js)
  write_file("src/engine/input.js", template_input_js)
  write_file("src/engine/audio.js", template_audio_js)
  write_file("src/engine/physics.js", template_physics_js)
  write_file("src/engine/renderer.js", template_renderer_js)
  write_file("src/engine/assets.js", template_assets_js)
  write_file("src/engine/storage.js", template_storage_js)
  write_file("src/game/bird.js", template_bird_js)
  write_file("src/game/pipes.js", template_pipes_js)
  write_file("src/game/ground.js", template_ground_js)
  write_file("src/game/background.js", template_background_js)
  write_file("src/game/score.js", template_score_js)
  write_file("src/game/ui.js", template_ui_js)
  write_file("src/game/particles.js", template_particles_js)
  write_file("README.md", template_readme)
  log("Flappy Bird scaffold created")
```

---

## 4. Minimal Templates (inline)

```html
<!-- template_index_html -->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Flappy Bird — DEIA</title>
    <link rel="stylesheet" href="css/styles.css" />
  </head>
  <body>
    <canvas id="game" width="432" height="768" aria-label="Flappy Bird game canvas"></canvas>
    <script type="module" src="src/main.js"></script>
  </body>
  </html>
```

```css
/* template_styles_css */
html, body { margin: 0; background: #0b1020; color: #fff; height: 100%; }
canvas { display: block; margin: 0 auto; image-rendering: pixelated; }
.hidden { display: none; }
```

```js
// template_main_js
import { createLoop } from './engine/loop.js';
import { Input } from './engine/input.js';
import { Renderer } from './engine/renderer.js';
import { Physics } from './engine/physics.js';
import { Assets } from './engine/assets.js';
import { Storage } from './engine/storage.js';
import { Bird } from './game/bird.js';
import { Pipes } from './game/pipes.js';
import { Ground } from './game/ground.js';
import { Background } from './game/background.js';
import { Score } from './game/score.js';
import { UI } from './game/ui.js';

const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

const input = new Input(canvas);
const render = new Renderer(ctx, canvas.width, canvas.height);
const physics = new Physics();
const assets = new Assets('assets');
const storage = new Storage('deia-flappy');

await assets.load();

const background = new Background(assets);
const ground = new Ground(assets);
const bird = new Bird(assets, physics);
const pipes = new Pipes(assets, physics);
const score = new Score(storage);
const ui = new UI(storage);

let state = 'menu'; // 'menu' | 'playing' | 'gameover' | 'paused'

const loop = createLoop({
  update(dt) {
    input.update();
    if (state === 'menu') {
      if (input.flapPressed()) { state = 'playing'; bird.flap(); pipes.reset(); score.reset(); }
    } else if (state === 'playing') {
      if (input.pausePressed()) state = 'paused';
      if (input.flapPressed()) bird.flap();
      background.update(dt);
      pipes.update(dt);
      bird.update(dt);
      ground.update(dt);
      if (pipes.passed(bird)) score.add(1);
      if (pipes.collides(bird) || ground.collides(bird)) {
        state = 'gameover';
        score.commit();
      }
    } else if (state === 'paused') {
      if (input.pausePressed()) state = 'playing';
    } else if (state === 'gameover') {
      if (input.flapPressed()) { state = 'playing'; bird.reset(); pipes.reset(); score.reset(); }
    }
  },
  draw() {
    render.clear('#4ec0ca');
    background.draw(render);
    pipes.draw(render);
    bird.draw(render);
    ground.draw(render);
    ui.draw(render, state, score);
  }
});

loop.start();
```

```js
// template_engine_loop_js (src/engine/loop.js)
export function createLoop({ update, draw }) {
  let last = performance.now();
  let raf = 0;
  function frame(t) {
    const dt = Math.min(0.05, (t - last) / 1000);
    last = t;
    update(dt);
    draw();
    raf = requestAnimationFrame(frame);
  }
  return { start() { raf = requestAnimationFrame(frame); }, stop() { cancelAnimationFrame(raf); } };
}
```

```js
// template_engine_input_js (src/engine/input.js)
export class Input {
  constructor(canvas) {
    this.keys = new Set();
    this._flap = false; this._pause = false;
    window.addEventListener('keydown', e => this.keys.add(e.code));
    window.addEventListener('keyup', e => this.keys.delete(e.code));
    const press = () => { this._flap = true; };
    canvas.addEventListener('mousedown', press);
    canvas.addEventListener('touchstart', press, { passive: true });
  }
  update() { this._pause = this.keys.has('KeyP') || this.keys.has('Escape'); }
  flapPressed() { const v = this._flap || this.keys.has('Space') || this.keys.has('ArrowUp'); this._flap = false; return v; }
  pausePressed() { const v = this._pause; this._pause = false; return v; }
}
```

```js
// template_engine_audio_js (src/engine/audio.js)
export class AudioBus {
  constructor(base='assets/audio') { this.base = base; this.cache = new Map(); this.muted = false; }
  async load(names) { await Promise.all(names.map(n => this._load(n))); }
  async _load(name) { const a = new Audio(`${this.base}/${name}`); await a.decode?.(); this.cache.set(name, a); }
  play(name) { if (this.muted) return; const a = this.cache.get(name); a && a.cloneNode().play(); }
  setMuted(v) { this.muted = v; }
}
```

```js
// template_engine_physics_js (src/engine/physics.js)
export class Physics {
  aabb(a, b) { return !(a.x + a.w < b.x || a.x > b.x + b.w || a.y + a.h < b.y || a.y > b.y + b.h); }
}
```

```js
// template_engine_renderer_js (src/engine/renderer.js)
export class Renderer {
  constructor(ctx, w, h) { this.ctx = ctx; this.w = w; this.h = h; }
  clear(color) { const c = this.ctx; c.fillStyle = color; c.fillRect(0, 0, this.w, this.h); }
  sprite(img, sx, sy, sw, sh, dx, dy, dw, dh) { this.ctx.drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh); }
  rect(x, y, w, h, fill) { const c = this.ctx; c.fillStyle = fill; c.fillRect(x, y, w, h); }
  text(t, x, y, color='#fff', size=36, align='center') { const c = this.ctx; c.fillStyle = color; c.font = `${size}px monospace`; c.textAlign = align; c.fillText(t, x, y); }
}
```

```js
// template_engine_assets_js (src/engine/assets.js)
export class Assets {
  constructor(base='assets') { this.base = base; this.images = {}; }
  async load() {
    const names = ['sprites/bird.png','sprites/pipe.png','sprites/background.png','sprites/ground.png'];
    const loaders = names.map(n => this._img(n));
    await Promise.all(loaders);
  }
  _img(path) { return new Promise(res => { const i = new Image(); i.onload = () => (this.images[path] = i, res()); i.src = `${this.base}/${path}`; }); }
}
```

```js
// template_engine_storage_js (src/engine/storage.js)
export class Storage {
  constructor(ns='deia') { this.ns = ns; }
  get(key, fallback) { try { return JSON.parse(localStorage.getItem(`${this.ns}:${key}`)) ?? fallback; } catch { return fallback; } }
  set(key, val) { try { localStorage.setItem(`${this.ns}:${key}`, JSON.stringify(val)); } catch {} }
}
```

```js
// template_game_bird_js (src/game/bird.js)
export class Bird {
  constructor(assets, physics) { this.assets = assets; this.physics = physics; this.reset(); }
  reset() { this.x = 120; this.y = 320; this.vy = 0; this.w = 34; this.h = 24; }
  flap() { this.vy = -300; }
  update(dt) { this.vy += 900 * dt; this.vy = Math.min(this.vy, 600); this.y += this.vy * dt; }
  draw(r) { r.rect(this.x, this.y, this.w, this.h, '#ffd34e'); }
}
```

```js
// template_game_pipes_js (src/game/pipes.js)
export class Pipes {
  constructor(assets, physics) { this.assets = assets; this.physics = physics; this.reset(); }
  reset() { this.xs = []; this.gapY = 320; this.speed = 180; this.spawnTimer = 0; }
  update(dt) {
    this.spawnTimer -= dt; if (this.spawnTimer <= 0) { this.spawn(); this.spawnTimer = 1.6; }
    this.xs = this.xs.map(x => x - this.speed * dt).filter(x => x > -80);
  }
  spawn() { const jitter = (Math.random() - 0.5) * 180; this.gapY = Math.max(140, Math.min(560, this.gapY + jitter)); this.xs.push(520); }
  collides(bird) { return this.xs.some(x => this._hit(bird, x)); }
  _hit(b, x) { const gap = 160; const top = { x, y: 0, w: 80, h: this.gapY - gap/2 }; const bot = { x, y: this.gapY + gap/2, w: 80, h: 768 - (this.gapY + gap/2) }; return this.physics.aabb(b, top) || this.physics.aabb(b, bot); }
  passed(bird) { return this.xs.some(x => Math.abs(x - bird.x) < 2); }
  draw(r) { this.xs.forEach(x => { r.rect(x, 0, 80, this.gapY - 80, '#5bd24b'); r.rect(x, this.gapY + 80, 80, 768, '#5bd24b'); }); }
}
```

```js
// template_game_ground_js (src/game/ground.js)
export class Ground {
  constructor(assets) { this.assets = assets; this.scroll = 0; }
  update(dt) { this.scroll = (this.scroll + 180 * dt) % 48; }
  collides(bird) { return bird.y + bird.h >= 720; }
  draw(r) { r.rect(0, 720, 432, 48, '#7c5b3f'); }
}
```

```js
// template_game_background_js (src/game/background.js)
export class Background { update(dt) {} draw(r) { r.rect(0, 0, 432, 768, '#4ec0ca'); } }
```

```js
// template_game_score_js (src/game/score.js)
export class Score {
  constructor(storage) { this.storage = storage; this.best = storage.get('best', 0); this.cur = 0; }
  reset() { this.cur = 0; }
  add(v) { this.cur += v; this.best = Math.max(this.best, this.cur); }
  commit() { this.storage.set('best', this.best); }
}
```

```js
// template_game_ui_js (src/game/ui.js)
export class UI {
  constructor(storage) { this.storage = storage; }
  draw(r, state, score) {
    r.text(`${score.cur}`, 216, 120, '#fff', 64);
    if (state === 'menu') { r.text('Tap/Space to start', 216, 360, '#fff', 24); }
    if (state === 'paused') { r.text('Paused (P/Esc)', 216, 380, '#fff', 24); }
    if (state === 'gameover') { r.text(`Game Over — Best ${score.best}`, 216, 380, '#fff', 24); }
  }
}
```

```js
// template_game_particles_js (src/game/particles.js)
export class Particles { /* reserved for juice effects */ }
```

```md
<!-- template_readme -->
# Flappy Bird (DEIA)

Open `index.html` in a browser. Controls: Space/Up/Click/Tap to flap. P or Esc to pause.

Folders:
- `src/engine`: loop, input, audio, physics, renderer, assets, storage
- `src/game`: birds, pipes, world, score, UI, particles

Roadmap:
- Add sprite rendering, audio SFX, screen shake, particle pops, mobile layout.
```

---

## 5. Gameplay Spec
- Gravity: +900 px/s^2; flap impulse: -300 px/s; terminal vy: +600 px/s.
- Pipe gap: 160 px; spawn every ~1.6 s with ±90 px vertical jitter; speed 180 px/s.
- Collision: AABB vs top/bottom pipe segments and ground. No invulnerability frames.
- Scoring: +1 when bird’s x crosses pipe x; persist best score.
- States: menu → playing → (paused) → gameover → playing.

---

## 6. Validation Checklist
- [ ] Launch in desktop Chrome/Firefox at 60 FPS (devtools perf < 3 ms/frame avg draw).
- [ ] Mobile tap works; canvas scales to device width maintaining aspect.
- [ ] Pause/resume functional; game over transitions reset state cleanly.
- [ ] Best score persists across reloads; mute toggle persists (future step).
- [ ] No console errors; assets fail gracefully when missing.

---

## 7. Hatch Test Procedure
1. Place this egg in `docs/projects/` (already routed).
2. Hatch: scaffold files under `games/flappy-bird/` using the templates above.
3. Open `games/flappy-bird/index.html` in a browser.
4. Verify: flap, score increments, collisions end game, pause works, best score persists.

---

## 8. Future Enhancements
- Sprite-based rendering, animation frames, and parallax layers.
- Sound effects with mute toggle; settings panel; reduced motion option.
- Difficulty ramp (gap shrink, speed up), medals, and daily best.
- Touch-friendly UI overlays and full-screen toggle.

---

**End of Egg — Flappy Bird Build Plan (v1.0)**

