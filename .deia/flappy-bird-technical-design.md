# Technical Design Document: Phoenix's Legendary Journey

**Project:** Flappy Bird Game B - Phoenix Edition
**Document Version:** 1.0
**Author:** BOT-00001 (Designer/Architect)
**Date:** 2025-10-12
**Phase:** Phase 1 (Design)

---

## 1. Executive Summary

This document specifies the technical architecture for "Phoenix's Legendary Journey," a browser-based Flappy Bird implementation featuring Phoenix, an overconfident bird with delusions of grandeur. The game will be delivered as a single, self-contained HTML file with no external dependencies.

**Key Design Principles:**
- Single HTML file for maximum portability
- No external dependencies or frameworks
- 60 FPS performance target
- Cross-browser and mobile compatibility
- Clean, maintainable vanilla JavaScript

---

## 2. Technology Stack

### 2.1 Platform & Runtime
**Platform:** Web Browser (HTML5)
**Rendering:** Canvas 2D API
**Language:** JavaScript (ES6+)
**Styling:** CSS3 (embedded)

### 2.2 Distribution Format
**Single HTML File** containing:
- HTML structure
- Embedded CSS (<style> tags)
- Embedded JavaScript (<script> tags)
- No external assets, images, or fonts

**Rationale:**
- ✅ Zero dependencies
- ✅ Works offline
- ✅ No build process required
- ✅ Download and open = instant play
- ✅ Maximum compatibility
- ✅ Easy to share and distribute
- ✅ Future-proof (standard web APIs)

### 2.3 Browser Compatibility Targets
- Chrome 90+ (latest 2 versions)
- Firefox 88+ (latest 2 versions)
- Safari 14+ (latest 2 versions)
- Edge 90+ (latest 2 versions)
- Mobile: iOS Safari 14+, Chrome Android 90+

### 2.4 No External Libraries
All code written in vanilla JavaScript. No jQuery, no game frameworks, no WebGL libraries.

**Reason:** Minimalism, portability, and learning/demonstration value.

---

## 3. Architecture Overview

### 3.1 High-Level Structure

```
┌─────────────────────────────────────┐
│     Game Engine (Main Loop)         │
│  - Update (60 FPS)                  │
│  - Render (60 FPS)                  │
│  - State Management                 │
└─────────────────────────────────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼────┐   ┌───▼────┐
│ Input  │   │Graphics│
│Handler │   │Renderer│
└───┬────┘   └───┬────┘
    │            │
┌───▼────────────▼────┐
│   Game Entities     │
│  - Phoenix (Bird)   │
│  - Pipes            │
│  - Particles        │
│  - UI Elements      │
└─────────────────────┘
    │
┌───▼─────────────────┐
│  Persistence Layer  │
│  (LocalStorage)     │
└─────────────────────┘
```

### 3.2 Game Loop Architecture

**RequestAnimationFrame Loop:**
```javascript
function gameLoop(timestamp) {
  deltaTime = timestamp - lastTimestamp;
  lastTimestamp = timestamp;

  // Update phase
  update(deltaTime);

  // Render phase
  render();

  requestAnimationFrame(gameLoop);
}
```

**Fixed Timestep (60 FPS target):**
- Physics calculations normalized to 16.67ms per frame
- Allows consistent behavior across different refresh rates

---

## 4. State Management

### 4.1 Game States

```javascript
const GameState = {
  TITLE: 'title',        // Title screen
  PLAYING: 'playing',    // Active gameplay
  GAME_OVER: 'gameover', // Death screen
  PAUSED: 'paused'       // Paused (optional)
};
```

### 4.2 State Transitions

```
TITLE ──(click/tap/space)──> PLAYING
PLAYING ──(collision)──> GAME_OVER
GAME_OVER ──(restart)──> TITLE
PLAYING ──(ESC)──> PAUSED (optional)
PAUSED ──(ESC)──> PLAYING (optional)
```

### 4.3 State Data Structure

```javascript
const gameState = {
  current: GameState.TITLE,
  score: 0,
  highScore: 0,
  confidenceLevel: 0,     // 0-100, affects difficulty
  currentTitle: '',       // Legendary title earned
  pipes: [],              // Array of pipe objects
  particles: [],          // Visual effects
  frameCount: 0
};
```

---

## 5. Core Systems Design

### 5.1 Physics System

**Constants:**
```javascript
const GRAVITY = 0.6;           // Pixels per frame^2
const FLAP_POWER = -11;        // Upward velocity on flap
const TERMINAL_VELOCITY = 15;  // Max fall speed
const BIRD_SIZE = 34;          // Phoenix diameter (pixels)
```

**Bird Physics Object:**
```javascript
const phoenix = {
  x: 120,                // Horizontal position (fixed)
  y: canvas.height / 2,  // Vertical position
  velocityY: 0,          // Current vertical velocity
  rotation: 0,           // Sprite rotation (-45° to 90°)
  radius: BIRD_SIZE / 2  // Collision detection
};
```

**Update Logic:**
```javascript
function updatePhysics() {
  // Apply gravity
  phoenix.velocityY += GRAVITY;

  // Clamp to terminal velocity
  phoenix.velocityY = Math.min(phoenix.velocityY, TERMINAL_VELOCITY);

  // Update position
  phoenix.y += phoenix.velocityY;

  // Calculate rotation based on velocity
  phoenix.rotation = Math.min(Math.max(phoenix.velocityY * 3, -45), 90);
}
```

### 5.2 Pipe Generation System

**Constants:**
```javascript
const PIPE_WIDTH = 70;
const PIPE_GAP_BASE = 160;           // Base gap size
const PIPE_SPEED_BASE = 3;           // Pixels per frame
const PIPE_SPAWN_INTERVAL = 90;      // Frames between pipes
const PIPE_MIN_HEIGHT = 80;          // Minimum space above/below gap
```

**Pipe Data Structure:**
```javascript
{
  x: number,              // Horizontal position
  gapY: number,           // Vertical center of gap
  gapSize: number,        // Size of gap (affected by confidence)
  scored: boolean,        // Has player passed this pipe?
  personality: string,    // 'smug', 'encouraging', 'sarcastic', etc.
  message: string         // Optional text bubble
}
```

**Generation Algorithm:**
```javascript
function spawnPipe() {
  const minY = PIPE_MIN_HEIGHT;
  const maxY = canvas.height - PIPE_MIN_HEIGHT - gapSize;
  const gapY = Math.random() * (maxY - minY) + minY;

  // Adjust gap size based on confidence level
  const gapModifier = (gameState.confidenceLevel / 100) * -20;
  const gapSize = PIPE_GAP_BASE + gapModifier;

  const pipe = {
    x: canvas.width,
    gapY: gapY,
    gapSize: Math.max(gapSize, 120), // Never too small
    scored: false,
    personality: selectRandomPersonality(),
    message: getPersonalityMessage(personality)
  };

  gameState.pipes.push(pipe);
}
```

### 5.3 Collision Detection

**Method:** Circle-Rectangle AABB with circle-line checks

**Phoenix Collision:**
```javascript
function checkCollision() {
  // Ground collision
  if (phoenix.y + phoenix.radius >= canvas.height - GROUND_HEIGHT) {
    return true;
  }

  // Ceiling collision
  if (phoenix.y - phoenix.radius <= 0) {
    return true;
  }

  // Pipe collision
  for (const pipe of gameState.pipes) {
    // Only check pipes in proximity
    if (pipe.x < phoenix.x + phoenix.radius &&
        pipe.x + PIPE_WIDTH > phoenix.x - phoenix.radius) {

      // Check if Phoenix is NOT in the gap
      if (phoenix.y - phoenix.radius < pipe.gapY - pipe.gapSize / 2 ||
          phoenix.y + phoenix.radius > pipe.gapY + pipe.gapSize / 2) {
        return true;
      }
    }
  }

  return false;
}
```

**Collision Response:**
- Trigger GAME_OVER state
- Play death animation
- Display snarky Phoenix quote
- Update high score if beaten

### 5.4 Scoring System

**Score Increment:**
```javascript
function updateScore() {
  for (const pipe of gameState.pipes) {
    // Check if Phoenix has passed the pipe
    if (!pipe.scored && pipe.x + PIPE_WIDTH < phoenix.x) {
      pipe.scored = true;
      gameState.score++;

      // Update confidence level
      updateConfidenceLevel();

      // Check for title unlocks
      checkTitleUnlocks();

      // Trigger score particle effect
      spawnScoreParticle(pipe.x, pipe.gapY);
    }
  }
}
```

**Confidence Level Calculation:**
```javascript
function updateConfidenceLevel() {
  // Confidence grows with consecutive successes
  gameState.confidenceLevel = Math.min(gameState.score * 3, 100);
}

function onDeath() {
  // Confidence drops on death
  gameState.confidenceLevel = Math.max(gameState.confidenceLevel - 30, 0);
}
```

### 5.5 Persistence System

**LocalStorage Keys:**
```javascript
const STORAGE_KEYS = {
  HIGH_SCORE: 'phoenixHighScore',
  BEST_TITLE: 'phoenixBestTitle',
  TOTAL_ATTEMPTS: 'phoenixTotalAttempts',
  TOTAL_DEATHS: 'phoenixTotalDeaths'
};
```

**Save/Load:**
```javascript
function saveHighScore() {
  if (gameState.score > gameState.highScore) {
    gameState.highScore = gameState.score;
    localStorage.setItem(STORAGE_KEYS.HIGH_SCORE, gameState.highScore);
  }
}

function loadHighScore() {
  const saved = localStorage.getItem(STORAGE_KEYS.HIGH_SCORE);
  gameState.highScore = saved ? parseInt(saved) : 0;
}
```

---

## 6. Input Handling

### 6.1 Supported Inputs

**Desktop:**
- SPACE key
- Mouse click on canvas
- Any key (simplified mode)

**Mobile:**
- Touch/tap on canvas
- Multi-touch support (any finger)

### 6.2 Input Handler

```javascript
function setupInputHandlers() {
  // Keyboard
  document.addEventListener('keydown', (e) => {
    if (e.code === 'Space' || e.key === ' ') {
      e.preventDefault();
      handleFlap();
    }
    if (e.code === 'Escape') {
      togglePause();
    }
  });

  // Mouse
  canvas.addEventListener('click', () => {
    handleFlap();
  });

  // Touch
  canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    handleFlap();
  });
}

function handleFlap() {
  if (gameState.current === GameState.TITLE) {
    startGame();
  } else if (gameState.current === GameState.PLAYING) {
    phoenix.velocityY = FLAP_POWER;
    spawnFlapParticle();
  } else if (gameState.current === GameState.GAME_OVER) {
    // Ignore, must use restart button
  }
}
```

---

## 7. Rendering System

### 7.1 Canvas Setup

```javascript
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Canvas dimensions
canvas.width = 450;
canvas.height = 700;

// Disable image smoothing for pixel-perfect rendering (optional)
ctx.imageSmoothingEnabled = false;
```

### 7.2 Rendering Pipeline

**Render Order (back to front):**
1. Background (sky gradient)
2. Clouds (parallax scrolling)
3. Pipes
4. Ground
5. Phoenix
6. Particles (flaps, score effects)
7. UI overlay (score, confidence meter, titles)
8. Game state screens (title, game over)

### 7.3 Background Rendering

```javascript
function drawBackground() {
  // Sky gradient (color changes with confidence level)
  const skyColor1 = getConfidenceColor(0);    // Top
  const skyColor2 = getConfidenceColor(0.5);  // Bottom

  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, skyColor1);
  gradient.addColorStop(1, skyColor2);

  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function getConfidenceColor(position) {
  const level = gameState.confidenceLevel;
  // Blue → Purple → Orange → Gold based on confidence
  if (level < 33) return `hsl(200, 70%, ${40 + position * 20}%)`;      // Blue
  if (level < 66) return `hsl(270, 60%, ${40 + position * 20}%)`;      // Purple
  if (level < 90) return `hsl(30, 100%, ${50 + position * 20}%)`;      // Orange
  return `hsl(45, 100%, ${60 + position * 20}%)`;                      // Gold
}
```

### 7.4 Phoenix Rendering

```javascript
function drawPhoenix() {
  ctx.save();
  ctx.translate(phoenix.x, phoenix.y);
  ctx.rotate(phoenix.rotation * Math.PI / 180);

  // Body (main circle)
  ctx.fillStyle = '#FF6B35';  // Aggressive orange
  ctx.beginPath();
  ctx.arc(0, 0, phoenix.radius, 0, Math.PI * 2);
  ctx.fill();

  // Shading
  const gradient = ctx.createRadialGradient(-5, -5, 5, 0, 0, phoenix.radius);
  gradient.addColorStop(0, 'rgba(255, 200, 100, 0.8)');
  gradient.addColorStop(1, 'rgba(255, 107, 53, 0)');
  ctx.fillStyle = gradient;
  ctx.fill();

  // Crest (mohawk)
  ctx.fillStyle = '#FF0000';
  ctx.beginPath();
  ctx.moveTo(-3, -phoenix.radius);
  ctx.lineTo(0, -phoenix.radius - 8);
  ctx.lineTo(3, -phoenix.radius);
  ctx.closePath();
  ctx.fill();

  // Eye (always wide open)
  ctx.fillStyle = 'white';
  ctx.beginPath();
  ctx.arc(8, -3, 5, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = 'black';
  ctx.beginPath();
  ctx.arc(8, -3, 2, 0, Math.PI * 2);
  ctx.fill();

  // Beak
  ctx.fillStyle = '#FFD700';  // Gold
  ctx.beginPath();
  ctx.moveTo(phoenix.radius, 0);
  ctx.lineTo(phoenix.radius + 10, -3);
  ctx.lineTo(phoenix.radius + 10, 3);
  ctx.closePath();
  ctx.fill();

  // Confidence aura (if high confidence)
  if (gameState.confidenceLevel > 66) {
    ctx.strokeStyle = `rgba(255, 215, 0, ${(gameState.confidenceLevel - 66) / 34 * 0.6})`;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(0, 0, phoenix.radius + 5, 0, Math.PI * 2);
    ctx.stroke();
  }

  ctx.restore();
}
```

### 7.5 Pipe Rendering

```javascript
function drawPipe(pipe) {
  // Top pipe
  ctx.fillStyle = '#2ECC40';  // Green
  ctx.fillRect(pipe.x, 0, PIPE_WIDTH, pipe.gapY - pipe.gapSize / 2);

  // Top pipe cap
  ctx.fillRect(pipe.x - 5, pipe.gapY - pipe.gapSize / 2 - 30, PIPE_WIDTH + 10, 30);

  // Bottom pipe
  ctx.fillRect(pipe.x, pipe.gapY + pipe.gapSize / 2, PIPE_WIDTH, canvas.height);

  // Bottom pipe cap
  ctx.fillRect(pipe.x - 5, pipe.gapY + pipe.gapSize / 2, PIPE_WIDTH + 10, 30);

  // Shading/highlights
  ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
  ctx.fillRect(pipe.x + 5, 0, 10, pipe.gapY - pipe.gapSize / 2);
  ctx.fillRect(pipe.x + 5, pipe.gapY + pipe.gapSize / 2, 10, canvas.height);

  // Pipe personality message (if close to Phoenix)
  if (Math.abs(pipe.x - phoenix.x) < 100 && pipe.message) {
    drawPipeMessage(pipe);
  }
}

function drawPipeMessage(pipe) {
  ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
  ctx.font = '12px monospace';
  const textWidth = ctx.measureText(pipe.message).width;
  const bubbleX = pipe.x + PIPE_WIDTH / 2 - textWidth / 2 - 5;
  const bubbleY = pipe.gapY - 25;

  ctx.fillRect(bubbleX, bubbleY, textWidth + 10, 20);

  ctx.fillStyle = 'white';
  ctx.fillText(pipe.message, bubbleX + 5, bubbleY + 14);
}
```

### 7.6 UI Rendering

```javascript
function drawUI() {
  // Score (large, center top)
  ctx.fillStyle = 'white';
  ctx.strokeStyle = 'black';
  ctx.lineWidth = 4;
  ctx.font = 'bold 56px monospace';
  ctx.textAlign = 'center';
  ctx.strokeText(gameState.score, canvas.width / 2, 80);
  ctx.fillText(gameState.score, canvas.width / 2, 80);

  // Current title
  if (gameState.currentTitle) {
    ctx.font = '16px monospace';
    ctx.strokeText(gameState.currentTitle, canvas.width / 2, 110);
    ctx.fillText(gameState.currentTitle, canvas.width / 2, 110);
  }

  // Confidence meter
  drawConfidenceMeter();
}

function drawConfidenceMeter() {
  const meterWidth = 200;
  const meterHeight = 20;
  const meterX = canvas.width / 2 - meterWidth / 2;
  const meterY = 130;

  // Background
  ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
  ctx.fillRect(meterX, meterY, meterWidth, meterHeight);

  // Fill (color based on level)
  const fillWidth = (gameState.confidenceLevel / 100) * meterWidth;
  const fillColor = getConfidenceColor(0.5);
  ctx.fillStyle = fillColor;
  ctx.fillRect(meterX, meterY, fillWidth, meterHeight);

  // Border
  ctx.strokeStyle = 'white';
  ctx.lineWidth = 2;
  ctx.strokeRect(meterX, meterY, meterWidth, meterHeight);

  // Label
  ctx.fillStyle = 'white';
  ctx.font = '12px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('CONFIDENCE', canvas.width / 2, meterY - 5);
}
```

---

## 8. Novel Features Implementation

### 8.1 Hall of Legends (Achievement System)

**Title Unlocks:**
```javascript
const LEGENDARY_TITLES = [
  { score: 0, title: 'Novice Sky Dancer' },
  { score: 5, title: 'Apprentice of the Wind' },
  { score: 10, title: 'Journeybird' },
  { score: 15, title: 'Gap Navigator' },
  { score: 20, title: 'Master of Gaps' },
  { score: 30, title: 'Sky Warrior' },
  { score: 40, title: 'Phoenix the Bold' },
  { score: 50, title: 'Phoenix the Untouchable' },
  { score: 75, title: 'Legendary Flyer' },
  { score: 100, title: 'LITERALLY IMPOSSIBLE LEGEND' }
];

function checkTitleUnlocks() {
  for (const title of LEGENDARY_TITLES) {
    if (gameState.score >= title.score) {
      if (gameState.currentTitle !== title.title) {
        gameState.currentTitle = title.title;
        showTitleUnlockAnimation(title.title);
      }
    }
  }
}
```

### 8.2 Confidence Meter (Dynamic Difficulty)

**Affects:**
- Pipe gap size (smaller at high confidence)
- Pipe speed (faster at high confidence)
- Visual effects (aura, background color)

**Implementation:**
```javascript
function getDynamicDifficulty() {
  const confidenceFactor = gameState.confidenceLevel / 100;

  return {
    pipeGapSize: PIPE_GAP_BASE - (confidenceFactor * 30),  // Max -30 pixels
    pipeSpeed: PIPE_SPEED_BASE + (confidenceFactor * 1.5), // Max +1.5 speed
    visualIntensity: confidenceFactor
  };
}
```

### 8.3 Pipe Personalities

**Types:**
```javascript
const PIPE_PERSONALITIES = {
  smug: {
    messages: ['Too slow!', 'That all you got?', 'Pathetic.'],
    frequency: 0.2
  },
  encouraging: {
    messages: ['You can do it!', 'Keep going!', 'Almost there!'],
    frequency: 0.3
  },
  sarcastic: {
    messages: ['Wow, amazing.', 'So impressive.', 'A legend.'],
    frequency: 0.2
  },
  philosophical: {
    messages: ['Why do we exist?', 'What is a pipe?', 'Are you real?'],
    frequency: 0.15
  },
  silent: {
    messages: [],
    frequency: 0.15
  }
};

function selectRandomPersonality() {
  const roll = Math.random();
  let cumulative = 0;

  for (const [type, data] of Object.entries(PIPE_PERSONALITIES)) {
    cumulative += data.frequency;
    if (roll < cumulative) {
      return type;
    }
  }
  return 'silent';
}

function getPersonalityMessage(personality) {
  const messages = PIPE_PERSONALITIES[personality].messages;
  if (messages.length === 0) return null;
  return messages[Math.floor(Math.random() * messages.length)];
}
```

### 8.4 Photo Mode (Stretch Goal)

**Implementation:**
```javascript
function captureScreenshot() {
  // Freeze game
  const wasPaused = gameState.current === GameState.PAUSED;
  if (!wasPaused) gameState.current = GameState.PAUSED;

  // Trigger hero pose animation
  phoenix.heroMode = true;

  // Render frame
  render();

  // Convert canvas to image
  const dataURL = canvas.toDataURL('image/png');

  // Download
  const link = document.createElement('a');
  link.download = `phoenix-legend-${gameState.score}.png`;
  link.href = dataURL;
  link.click();

  // Resume
  phoenix.heroMode = false;
  if (!wasPaused) gameState.current = GameState.PLAYING;
}
```

---

## 9. Performance Optimization

### 9.1 Targets
- **FPS:** 60 (16.67ms per frame)
- **Load Time:** <1 second
- **File Size:** <60KB
- **Memory:** <50MB heap usage

### 9.2 Optimization Strategies

**Object Pooling:**
```javascript
// Reuse particle objects instead of creating/destroying
const particlePool = [];

function getParticle() {
  return particlePool.pop() || createNewParticle();
}

function returnParticle(particle) {
  particle.active = false;
  particlePool.push(particle);
}
```

**Culling:**
```javascript
// Only render pipes within viewport + margin
function cullPipes() {
  gameState.pipes = gameState.pipes.filter(pipe =>
    pipe.x > -PIPE_WIDTH - 50 && pipe.x < canvas.width + 50
  );
}
```

**Minimal Redraws:**
- Clear only necessary regions (not implemented in MVP)
- Use layered canvases for static elements (not implemented in MVP)

### 9.3 Mobile Optimization
- Touch event passive listeners
- Prevent scroll/zoom
- Simplified particle effects on low-end devices

---

## 10. Data Structures Reference

### 10.1 Phoenix Object
```javascript
{
  x: 120,
  y: 300,
  velocityY: 0,
  rotation: 0,
  radius: 17,
  heroMode: false  // For photo mode
}
```

### 10.2 Pipe Object
```javascript
{
  x: 450,
  gapY: 250,
  gapSize: 160,
  scored: false,
  personality: 'smug',
  message: 'Too slow!'
}
```

### 10.3 Particle Object
```javascript
{
  x: 120,
  y: 300,
  velocityX: 2,
  velocityY: -3,
  life: 30,        // Frames remaining
  maxLife: 30,
  color: '#FFD700',
  size: 4,
  active: true
}
```

---

## 11. Error Handling

### 11.1 Canvas Support Detection
```javascript
if (!canvas.getContext) {
  document.body.innerHTML = '<h1>Your browser does not support HTML5 Canvas</h1>';
  return;
}
```

### 11.2 LocalStorage Availability
```javascript
function isLocalStorageAvailable() {
  try {
    const test = '__test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch (e) {
    return false;
  }
}
```

### 11.3 Graceful Degradation
- If LocalStorage unavailable: High score persists for session only
- If Canvas unavailable: Display error message
- If touch not supported: Desktop controls still work

---

## 12. Testing Considerations

### 12.1 Unit Test Targets (Manual)
- Physics calculations (gravity, flap)
- Collision detection accuracy
- Score increment logic
- Confidence level calculation
- Pipe generation randomness

### 12.2 Integration Test Scenarios
- Full gameplay loop (title → playing → game over → restart)
- High score persistence across sessions
- All input methods (keyboard, mouse, touch)
- State transitions

### 12.3 Browser Compatibility Testing
- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile Safari (iOS), Chrome Android
- Different screen sizes

### 12.4 Performance Testing
- Sustained 60 FPS for 10+ minutes
- Memory leak detection (heap size shouldn't grow)
- Load time measurement

---

## 13. Future Extensibility

### 13.1 Potential Additions (Post-MVP)
- Audio system (Web Audio API)
- Ghost mode (replay recording)
- Training montage mode
- Rivalry system (AI opponents)
- Commentary track
- Customization options

### 13.2 Architecture Flexibility
The modular design allows:
- Easy addition of new game states
- Plugin-style feature additions
- Asset replacement (if switching to image-based graphics)
- Networking layer (for leaderboards)

---

## 14. Security Considerations

**No security concerns for single-player browser game:**
- No server communication
- No user data collection
- LocalStorage only stores scores (not sensitive)
- No eval() or dynamic code execution

---

## 15. Accessibility Considerations

**Basic support:**
- Keyboard controls (standard for accessibility)
- High contrast UI elements
- Large touch targets on mobile

**Not implemented (but possible):**
- Screen reader support
- Colorblind modes
- Reduced motion mode

---

## 16. Documentation Requirements

### 16.1 Code Comments
- All major functions documented with JSDoc-style comments
- Complex algorithms explained inline
- Constants defined with rationale

### 16.2 README (Phase 4)
- How to play
- Controls
- Feature descriptions
- Technical details
- Customization guide

---

## 17. Acceptance Criteria

**Phase 2 (Implementation) Complete When:**
- [ ] Game loop runs at 60 FPS
- [ ] Phoenix physics feel responsive
- [ ] Pipes generate and scroll correctly
- [ ] Collision detection is accurate
- [ ] Scoring works correctly
- [ ] High score persists
- [ ] All input methods work
- [ ] 3 novel features implemented (Hall of Legends, Confidence Meter, Pipe Personalities)
- [ ] Mobile touch controls work
- [ ] No console errors
- [ ] Code is clean and commented

---

## 18. Risks & Mitigations

**Risk:** Performance issues on older mobile devices
**Mitigation:** Test on mid-range devices, reduce particles if needed

**Risk:** Collision detection feels unfair
**Mitigation:** Add small margin/buffer to hitboxes, visual debug mode

**Risk:** Difficulty curve too steep with confidence system
**Mitigation:** Playtesting, tunable constants, minimum gap size enforcement

**Risk:** File size exceeds target
**Mitigation:** Minify code (post-development), avoid unnecessary features

---

## 19. Implementation Timeline

**Phase 2 Tasks (Estimated):**
- Task 2.1: Environment setup (30 min)
- Task 2.2: Core game loop (3-4 hours)
- Task 2.3: Bird physics (4-5 hours)
- Task 2.4: Pipe system (5-6 hours)
- Task 2.5: Collision detection (3-4 hours)
- Task 2.6: Scoring system (2-3 hours)
- Task 2.7: Game states & UI (4-5 hours)
- Task 2.8: Visual polish (5-6 hours)
- Task 2.9: Novel features (6-8 hours)
- Task 2.10: Mobile support (3-4 hours)
- Task 2.11: Audio (optional, 4-5 hours)
- Task 2.12: Code review (3-4 hours)

**Total:** ~40-50 hours

---

## 20. Conclusion

This technical design provides a complete blueprint for implementing Phoenix's Legendary Journey. The architecture prioritizes:

1. **Simplicity:** Single file, no dependencies
2. **Performance:** 60 FPS target, optimized rendering
3. **Portability:** Works everywhere HTML5 Canvas is supported
4. **Maintainability:** Clean code, modular design
5. **Extensibility:** Easy to add features post-MVP

The design balances technical excellence with practical implementation constraints, ensuring the game is both fun to play and straightforward to build.

---

**Document Status:** ✅ Complete
**Next Phase:** Phase 1.4 (Visual Design) then Phase 2 (Implementation)
**Approval Required:** Design review before proceeding

---

*Prepared by BOT-00001 (Designer/Architect)*
*Role: Technical Designer*
*Phase: 1.3 Complete*
*Date: 2025-10-12*
