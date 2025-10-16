# Handoff: Queen to Developer - Phase 2 Start

**From:** BOT-00001 as Queen/Scrum Master
**To:** BOT-00001 as Developer
**Date:** 2025-10-12
**Phase:** Phase 2 (Implementation)
**Sprint:** Game B - Full SDLC Demo

---

## Your Mission

Build Phoenix's Legendary Journey - a fully playable Flappy Bird game based on the comprehensive design specs from Phase 1.

---

## Design Documents (Your Bible)

**Read these before coding:**
1. `.deia/flappy-bird-game-b-story.md` - Character, features, tone
2. `.deia/flappy-bird-technical-design.md` - Architecture, algorithms, constants
3. `.deia/flappy-bird-visual-design.md` - Colors, layout, animations

---

## What You're Building

**File:** `.deia/flappy-bird-game-b.html`

**Single HTML file containing:**
- HTML structure
- Embedded CSS
- Embedded JavaScript
- No external dependencies

**Target:** Playable game, 60 FPS, <60KB

---

## MVP Feature Checklist

**Core Mechanics:**
- [x] Flappy Bird physics (gravity, flap)
- [x] Pipe generation and scrolling
- [x] Collision detection (bird vs pipes/ground/ceiling)
- [x] Scoring system
- [x] High score persistence (LocalStorage)

**Phoenix Character:**
- [x] Orange bird with red mohawk, gold beak
- [x] Rotation based on velocity
- [x] Confidence-based visual changes (aura at high confidence)

**Novel Features (3 minimum):**
- [x] Confidence Meter (dynamic difficulty)
- [x] Hall of Legends (achievement titles)
- [x] Pipe Personalities (faces and messages)

**Game States:**
- [x] Title screen
- [x] Playing state
- [x] Game over screen
- [x] Restart functionality

**Visuals:**
- [x] Dynamic background (confidence-based colors)
- [x] Particle effects (flap, score, death)
- [x] UI (score, confidence meter, titles)

**Input:**
- [x] Keyboard (SPACE)
- [x] Mouse (click)
- [x] Touch (mobile)

**Polish:**
- [x] Smooth animations
- [x] Visual feedback
- [x] Responsive design

---

## Implementation Order (Follow This)

### Step 1: Boilerplate & Setup
Create HTML structure, canvas, basic CSS

### Step 2: Game Loop
RequestAnimationFrame loop, state management

### Step 3: Phoenix Physics
Bird object, gravity, flap, rotation

### Step 4: Input Handling
Keyboard, mouse, touch events

### Step 5: Pipe System
Generation, scrolling, gap logic

### Step 6: Collision Detection
Circle-rectangle collision

### Step 7: Scoring
Score tracking, high score persistence

### Step 8: Rendering
Draw Phoenix, pipes, background, ground

### Step 9: Novel Features
Confidence meter, titles, pipe personalities

### Step 10: UI
Title screen, game over screen, HUD

### Step 11: Particles
Flap effects, score effects, death explosion

### Step 12: Polish & Testing
Animations, mobile support, bug fixes

---

## Key Constants (From Technical Design)

```javascript
const GRAVITY = 0.6;
const FLAP_POWER = -11;
const PIPE_SPEED_BASE = 3;
const PIPE_GAP_BASE = 160;
const PIPE_WIDTH = 70;
const BIRD_SIZE = 34;
const TERMINAL_VELOCITY = 15;
```

---

## Critical Requirements

**1. Different from Game A:**
- Phoenix, not Gerald
- Confidence system, not anxiety
- Dynamic difficulty, not static
- Bright orange/gold, not yellow

**2. Performance:**
- Must run at 60 FPS
- No memory leaks
- Smooth animations

**3. Quality:**
- Clean, commented code
- No console errors
- All features working
- Mobile-friendly

**4. Single File:**
- Everything embedded
- No external resources
- Download and play

---

## Color Reference (Quick)

- Phoenix body: `#FF6B35`
- Phoenix crest: `#FF0000`
- Phoenix beak: `#FFD700`
- Pipes: `#2ECC40`
- Ground: `#8B6F47`
- Background: Dynamic (see visual design doc)

---

## Development Tips

**Start simple, add complexity:**
1. Get basic Flappy Bird working first
2. Then add confidence meter
3. Then add titles
4. Then add pipe personalities
5. Then polish

**Test frequently:**
- Test after each major feature
- Check collision accuracy
- Verify scoring works
- Test on mobile

**Comment your code:**
- Explain algorithms
- Document constants
- Mark sections clearly

---

## When You're Done

**Definition of Done:**
- Game is playable from title to game over
- All MVP features work
- No critical bugs
- Runs at 60 FPS
- Mobile controls work
- Code is clean and commented

**Then:**
1. Create handoff to Tester role
2. Self-test in multiple browsers
3. Mark Phase 2 complete
4. Transition to Phase 3 (Testing)

---

## Resources

**Design Docs:** `.deia/flappy-bird-*-design.md` files
**Game A Reference:** `.deia/flappy-gerald.html` (for structure inspiration, but don't copy features)
**Technical Specs:** See technical design doc section 5 (Core Systems)

---

## Success Criteria

**Playable game where:**
- Phoenix flaps and falls realistically
- Pipes scroll and have random gaps
- Collision detection is accurate
- Score increases when passing pipes
- Confidence level affects gap size
- Titles unlock at milestones
- Pipes show personality messages
- High score persists
- Can restart and play again

---

**You have everything you need. Time to build Phoenix's legend.**

**Role:** Developer (BOT-00001)
**Current Task:** Phase 2.1 - Core Game Loop
**Start implementing:** `.deia/flappy-bird-game-b.html`
**Estimated Time:** 40-50 hours total for Phase 2

**Let's code!**

---

*Prepared by BOT-00001 (Queen)*
*Phase: 2.0 Start*
*Authorization: Build the game*
*Date: 2025-10-12*
