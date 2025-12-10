# Visual Design Specification: Phoenix's Legendary Journey

**Project:** Flappy Bird Game B - Phoenix Edition
**Document Version:** 1.0
**Author:** BOT-00001 (Designer)
**Date:** 2025-10-12
**Phase:** Phase 1 (Design)

---

## 1. Design Philosophy

**Core Aesthetic:** Bold, dramatic, slightly over-the-top

Phoenix believes they're legendary, so the visual design should support that delusion with:
- Bright, saturated colors (Phoenix is loud and proud)
- Dynamic color shifts based on performance (ego visualization)
- Clean, readable design (nothing obscures the gameplay)
- Personality in every element (pipes have faces, particles have flair)

**Visual Tone:** Energetic, optimistic, theatrical

**Different from Game A:**
- Game A (Gerald): Muted anxious yellows/oranges, subdued
- Game B (Phoenix): BRIGHT orange/red, dramatic golds, confidence

---

## 2. Color Palette

### 2.1 Primary Palette

**Phoenix Colors:**
- **Body:** `#FF6B35` (Aggressive Orange) - main body
- **Shading:** `#FF8C50` (Light Orange) - highlights
- **Accent:** `#FF0000` (Pure Red) - crest/mohawk
- **Beak:** `#FFD700` (Gold) - because Phoenix is "valuable"
- **Eye:** `#FFFFFF` (White) with `#000000` (Black) pupil

**Environment Colors:**
- **Pipes:** `#2ECC40` (Green) - classic pipe green
- **Pipe Shading:** `#27A834` (Dark Green)
- **Ground:** `#8B6F47` (Brown Earth)
- **Ground Top:** `#A0824A` (Light Brown)

### 2.2 Dynamic Background Colors (Confidence-Based)

**Low Confidence (0-33%):**
- Sky Top: `#87CEEB` (Sky Blue)
- Sky Bottom: `#B0E0E6` (Powder Blue)
- Theme: Calm, starting out

**Medium Confidence (34-66%):**
- Sky Top: `#9B59B6` (Purple)
- Sky Bottom: `#C39BD3` (Light Purple)
- Theme: Getting serious

**High Confidence (67-89%):**
- Sky Top: `#FF6B35` (Orange)
- Sky Bottom: `#FFA07A` (Light Salmon)
- Theme: In the zone

**Legendary Mode (90-100%):**
- Sky Top: `#FFD700` (Gold)
- Sky Bottom: `#FFA500` (Orange Gold)
- Theme: Transcendent

### 2.3 UI Colors

- **Score Text:** `#FFFFFF` (White) with `#000000` (Black) outline
- **Title Text:** `#FFD700` (Gold)
- **Confidence Meter Fill:** Matches background theme
- **Confidence Meter Background:** `rgba(0, 0, 0, 0.5)`
- **Button Background:** `#4CAF50` (Green)
- **Button Hover:** `#45A049` (Dark Green)
- **Button Text:** `#FFFFFF` (White)

---

## 3. Character Design: Phoenix

### 3.1 Phoenix Anatomy

```
    /\      ← Red crest (mohawk)
   /  \
  |    |
 | O  |     ← Body (orange circle)
  |  < |    ← Eye (wide open) & Beak (gold triangle)
   |  |
    \/
```

**Dimensions:**
- Body Radius: 17 pixels
- Crest Height: 8 pixels above body
- Beak Length: 10 pixels from body edge
- Eye Offset: 8 pixels right, 3 pixels up from center

### 3.2 Phoenix States

**Idle / Flying:**
- Standard appearance
- Slight up/down bob animation (optional)
- Eye: wide open, alert

**Flapping:**
- No wing animation (wings are implied by particle effects)
- Slight scale pulse (1.0 → 1.1 → 1.0 over 3 frames)
- Rotate based on velocity

**High Confidence (>66%):**
- Golden aura around body (3 pixel glow)
- Particles trail behind
- Slightly larger eye (looks more intense)

**Legendary Mode (>90%):**
- Rainbow sparkle trail
- Rotating golden rings around body
- Crest glows brighter

**Death:**
- Rotation to 90° (face-plant)
- Eyes become X's (cartoon death)
- Small explosion particle burst
- Falls off bottom of screen

### 3.3 Rotation Behavior

Phoenix rotates based on vertical velocity:
- Velocity < -5: Rotate to -45° (climbing)
- Velocity 0: Rotate to 0° (level)
- Velocity > 5: Rotate to 45° (falling)
- Velocity > 10: Rotate to 90° (plummeting)

---

## 4. Environment Design

### 4.1 Background

**Sky:**
- Linear gradient from top to bottom
- Color changes based on confidence level (see Section 2.2)
- Smooth transitions over 60 frames when confidence crosses thresholds

**Clouds (Optional Enhancement):**
```
Simple cloud shapes:
  ○ ○○ ○
 ○○○○○○○

- Color: rgba(255, 255, 255, 0.3)
- Parallax scrolling (0.2 pixels per frame)
- 3-4 clouds looping across screen
- Y positions: 80, 160, 240 pixels
```

### 4.2 Ground

**Appearance:**
```
===========================  ← Top line (light brown)
██████████████████████████  ← Main ground (brown)
██████████████████████████
██████████████████████████
```

**Dimensions:**
- Height: 60 pixels from bottom
- Top stripe: 10 pixels, color `#A0824A`
- Main fill: 50 pixels, color `#8B6F47`

**Optional Details:**
- Small grass tufts (3-4 pixel vertical lines, `#228B22`)
- Repeating every 40 pixels

### 4.3 Pipes

**Pipe Structure:**
```
┌─────────┐  ← Top cap (wider, 30px tall)
│         │
│         │  ← Pipe body (70px wide)
│         │
└─────────┘

[    GAP    ]  ← Gap for Phoenix (dynamic size)

┌─────────┐  ← Bottom cap
│         │
│         │  ← Pipe body
│         │
└─────────┘
```

**Dimensions:**
- Body Width: 70 pixels
- Cap Width: 80 pixels (5 pixels overhang each side)
- Cap Height: 30 pixels
- Body Color: `#2ECC40` (Green)
- Cap Color: Same, slightly darker outline

**Shading:**
- Left side: darker stripe (`#27A834`, 10 pixels wide)
- Right side: highlight stripe (`rgba(255, 255, 255, 0.2)`, 10 pixels wide)

**Pipe Personality Faces (Optional):**

For pipes with personalities, add simple emoji-style faces:

**Smug Pipe:**
```
  ^  ^    ← Eyes
   ‿      ← Smirk
```

**Encouraging Pipe:**
```
  ◠  ◠    ← Happy eyes
   ᴗ      ← Smile
```

**Sarcastic Pipe:**
```
  -  -    ← Flat eyes
   _      ← Flat mouth
```

**Philosophical Pipe:**
```
  ●  ●    ← Wide eyes
   o      ← O mouth
```

Faces appear on the pipe cap, centered, when Phoenix is within 100 pixels.

### 4.4 Pipe Messages

**Text Bubbles:**
```
┌──────────────┐
│ "Too slow!"  │  ← Black background (rgba(0,0,0,0.7))
└──────▼───────┘  ← White text (12px monospace)
   [PIPE]
```

- Appear when Phoenix is within 100 pixels of pipe
- Positioned 25 pixels above gap center
- Fade in/out over 10 frames
- Auto-size to fit text

---

## 5. Particle Effects

### 5.1 Flap Particles

**Triggered:** On every flap input

**Appearance:**
- 5-8 small circles
- Size: 3-5 pixels radius
- Color: `rgba(255, 215, 0, 0.8)` (Gold, semi-transparent)
- Spawn position: Behind Phoenix (x - 15, y +/- 5)

**Behavior:**
- Initial velocity: Random spread (-3 to -1 X, -2 to 2 Y)
- Gravity: +0.2 per frame
- Fade out: Alpha reduces by 0.05 per frame
- Lifespan: 20 frames

### 5.2 Score Particles

**Triggered:** When passing a pipe

**Appearance:**
- "+1" text or star shapes
- Size: 16px font or 8px star
- Color: `#FFD700` (Gold)
- Spawn position: At pipe gap center

**Behavior:**
- Rise upward (velocityY: -2)
- Fade out: Alpha reduces by 0.05 per frame
- Lifespan: 30 frames
- No horizontal movement

### 5.3 Death Explosion

**Triggered:** On collision

**Appearance:**
- 15-20 particles
- Size: 4-8 pixels
- Colors: Mix of `#FF6B35`, `#FF0000`, `#FFD700` (Phoenix colors)
- Spawn position: Phoenix's position

**Behavior:**
- Explosive spread in all directions
- Initial velocity: Random 360° direction, speed 3-6
- Gravity: +0.3 per frame
- Rotation: Random spin
- Fade out: Alpha reduces by 0.08 per frame
- Lifespan: 25 frames

### 5.4 Confidence Aura (High Confidence)

**Triggered:** Confidence > 66%

**Appearance:**
- Circular glow around Phoenix
- Radius: Phoenix radius + 5 pixels
- Color: `rgba(255, 215, 0, opacity)`
- Opacity: (confidence - 66) / 34 * 0.6 (max 0.6)

**Behavior:**
- Pulsing animation (radius oscillates ±2 pixels)
- Always centered on Phoenix
- Fades in/out when crossing confidence threshold

### 5.5 Legendary Trail (Legendary Mode)

**Triggered:** Confidence > 90%

**Appearance:**
- Small sparkles trailing Phoenix
- Size: 2-4 pixels
- Colors: Cycle through rainbow (HSL rotation)
- Spawn rate: Every 2 frames

**Behavior:**
- Stay at spawn position (no movement)
- Fade out quickly (alpha -0.15 per frame)
- Lifespan: 15 frames
- Creates rainbow trail effect

---

## 6. UI Layout

### 6.1 Title Screen

```
┌────────────────────────────────┐
│                                │
│    PHOENIX'S LEGENDARY         │ ← Title (32px bold)
│         JOURNEY                │
│                                │
│         [PLAY]                 │ ← Button (Green, 200x50px)
│                                │
│    High Score: 42              │ ← Subtitle (18px)
│                                │
│    Press SPACE / TAP to Start  │ ← Instructions (14px)
│                                │
└────────────────────────────────┘
```

**Elements:**
- Title: Gold color, centered, top 30% of screen
- Play button: Green, centered, middle of screen
- High score: White, centered, below button
- Instructions: Gray, centered, bottom 20%
- Background: Animated Phoenix sprite bouncing gently

### 6.2 Gameplay Screen

```
┌────────────────────────────────┐
│           42                   │ ← Score (56px, bold, white)
│    "Master of Gaps"            │ ← Current title (16px, gold)
│    [████████░░] CONFIDENCE     │ ← Confidence meter (200x20px)
│                                │
│         🐦                     │
│            │                   │ ← Gameplay area
│           ╱╲                   │
│          ║  ║                  │
│                                │
│  ═══════════════════════════   │ ← Ground
└────────────────────────────────┘
```

**Elements:**
- Score: Top center, large, always visible
- Title: Below score, smaller
- Confidence meter: Below title, horizontal bar
- Gameplay: Center area, no obstructions
- All UI has black outline for readability

### 6.3 Game Over Screen

```
┌────────────────────────────────┐
│                                │
│    PHOENIX HAS FALLEN          │ ← Header (32px, red)
│                                │
│         Final Score: 42        │ ← Score (24px, white)
│         Best Score: 67         │ ← High score (24px, gold)
│                                │
│    "I was sabotaged!"          │ ← Random Phoenix quote (18px italic)
│                                │
│         [RETRY]                │ ← Button (Green, 200x50px)
│                                │
└────────────────────────────────┘
```

**Elements:**
- Header: Dramatic red, top center
- Scores: White (current), gold (best)
- Quote: Italic, Phoenix's personality showing
- Retry button: Large, prominent
- Background: Dimmed gameplay (rgba overlay)

### 6.4 Confidence Meter Detail

```
CONFIDENCE
┌────────────────────────────────┐
│████████████████████░░░░░░░░░░░│  ← Filled portion (dynamic color)
└────────────────────────────────┘
```

**Specifications:**
- Width: 200 pixels
- Height: 20 pixels
- Position: Top center, below title
- Fill color: Matches confidence level theme
- Background: Black, semi-transparent (0.5 alpha)
- Border: White, 2px
- Label: "CONFIDENCE" above, white, 12px

**Fill Levels:**
- 0-33%: Blue fill
- 34-66%: Purple fill
- 67-89%: Orange fill
- 90-100%: Gold fill

---

## 7. Animation Specifications

### 7.1 Phoenix Animations

**Flap Animation:**
- Duration: 4 frames
- Scale: 1.0 → 1.1 → 1.05 → 1.0
- No rotation change (rotation is velocity-based)

**Idle Bob (Title Screen):**
- Duration: 60 frames (1 second loop)
- Movement: Sine wave, ±5 pixels vertical
- Speed: Slow, gentle

**Death Fall:**
- Rotation: Current → 90° over 15 frames
- Movement: Accelerate downward (gravity applies)
- Eye change: Normal → X's at frame 5
- Particle burst: Frame 0

### 7.2 UI Animations

**Title Unlock Popup:**
```
Frame 0-10:  Scale 0 → 1.2 (bounce in)
Frame 10-15: Scale 1.2 → 1.0 (settle)
Frame 15-60: Hold (display title)
Frame 60-70: Fade out (alpha 1.0 → 0)
```

**Button Hover:**
- Scale: 1.0 → 1.05
- Duration: 5 frames
- Color: Slightly darker

**Button Click:**
- Scale: 1.05 → 0.95 → 1.0
- Duration: 3 frames

### 7.3 Background Animations

**Sky Color Transition:**
- Duration: 60 frames (1 second)
- Method: Linear interpolation between colors
- Triggered: When confidence crosses threshold

**Cloud Scrolling:**
- Speed: 0.2 pixels per frame
- Direction: Right to left
- Loop: When cloud fully off-screen, respawn on right

---

## 8. Typography

### 8.1 Fonts

**Primary Font:** Monospace (system default)
- Reason: Built-in, no loading, retro feel
- Fallback chain: `'Courier New', Courier, monospace`

**Font Sizes:**
- Score: 56px (bold)
- Title/Header: 32px (bold)
- Current Achievement Title: 16px (normal)
- UI Labels: 14px (normal)
- Pipe Messages: 12px (normal)

### 8.2 Text Styling

**Score Display:**
- Color: White
- Stroke: Black, 4px width
- Shadow: None (stroke provides contrast)
- Alignment: Center
- Weight: Bold

**Titles/Headers:**
- Color: Gold (`#FFD700`)
- Stroke: Black, 3px width
- Alignment: Center
- Weight: Bold

**Body Text:**
- Color: White
- Stroke: Black, 2px width (for gameplay text)
- Alignment: Center
- Weight: Normal

**Pipe Messages:**
- Color: White
- Background: `rgba(0, 0, 0, 0.7)`
- Padding: 5px
- Alignment: Center

---

## 9. Responsive Design

### 9.1 Canvas Sizing

**Desktop:**
- Width: 450px
- Height: 700px
- Aspect Ratio: 9:14 (portrait)

**Mobile:**
- Width: 100% of viewport (max 450px)
- Height: Maintains 9:14 aspect ratio
- Scales down for small screens

**Container:**
```css
#gameContainer {
  max-width: 450px;
  margin: 0 auto;
  padding: 20px;
}

#gameCanvas {
  width: 100%;
  height: auto;
  border: 4px solid #333;
  border-radius: 8px;
}
```

### 9.2 Touch Targets

**Minimum Size:** 44x44 pixels (Apple HIG guideline)

**Buttons:**
- Desktop: 200x50 pixels
- Mobile: 250x60 pixels (larger for easier tapping)

**Canvas Touch Area:**
- Entire canvas is tappable
- No dead zones

---

## 10. Visual Feedback

### 10.1 Input Feedback

**Flap Action:**
- Particle burst (immediate)
- Phoenix scale pulse (4 frames)
- Optional: Screen shake (2 pixels, 2 frames)

**Score Increase:**
- "+1" particle rise
- Brief white flash on score display
- Optional: Small scale pulse on score number

**Collision:**
- Explosion particles
- Phoenix rotation to 90°
- Screen shake (5 pixels, 10 frames)
- Transition to game over (30 frames)

### 10.2 State Changes

**Title → Playing:**
- Fade out title screen (15 frames)
- Phoenix moves to start position
- First pipe begins scrolling

**Playing → Game Over:**
- Slow motion effect (30 frames at 50% speed, optional)
- Explosion particles
- Dim background (overlay alpha 0 → 0.5)
- Game over screen fade in (20 frames)

**Game Over → Title:**
- Fade out game over screen (15 frames)
- Reset all game state
- Return to title screen

---

## 11. Accessibility Considerations

### 11.1 Color Contrast

**WCAG AA Compliance:**
- White text on black stroke: ✅ Passes (high contrast)
- Gold text on black stroke: ✅ Passes
- Button text on green background: ✅ Passes

### 11.2 Visual Clarity

**Readability:**
- Minimum font size: 12px
- Stroke on all gameplay text
- No text over busy backgrounds

**Hitbox Visibility:**
- Debug mode can show collision boundaries
- Phoenix and pipes have clear silhouettes
- High contrast between elements

### 11.3 Colorblind Modes (Future)

**Potential Additions:**
- Deuteranopia mode (red/green)
- Protanopia mode (red/green)
- Tritanopia mode (blue/yellow)

Not implemented in MVP, but color palette chosen to work reasonably well for most types.

---

## 12. Style Guide Summary

### 12.1 Quick Reference

**Phoenix:**
- Body: Orange (`#FF6B35`), 34px diameter
- Crest: Red (`#FF0000`), mohawk style
- Beak: Gold (`#FFD700`), 10px triangle
- Eye: White with black pupil, always open

**Environment:**
- Pipes: Green (`#2ECC40`), 70px wide
- Ground: Brown (`#8B6F47`), 60px tall
- Sky: Dynamic gradient (blue → purple → orange → gold)

**UI:**
- Score: 56px white bold with black stroke
- Titles: 16px gold with black stroke
- Buttons: Green background, white text, rounded corners
- Confidence Meter: 200x20px, dynamic color fill

**Effects:**
- Flap particles: Gold, small circles
- Score particles: Gold "+1" text
- Death explosion: Mixed Phoenix colors
- Confidence aura: Golden glow (high confidence only)

---

## 13. Implementation Notes

### 13.1 Drawing Order (Z-Index)

1. Background sky gradient
2. Clouds (if implemented)
3. Pipes
4. Ground
5. Particles (behind Phoenix)
6. Phoenix
7. Particles (in front of Phoenix)
8. UI elements (score, meter, titles)
9. Overlay screens (title, game over)

### 13.2 Canvas Rendering Tips

**Anti-aliasing:**
- Disable for pixel-perfect rendering: `ctx.imageSmoothingEnabled = false`
- Or enable for smoother circles: `ctx.imageSmoothingEnabled = true`
- Recommend: Enabled (smoother look)

**Text Rendering:**
- Always stroke then fill (stroke first creates outline)
- Use `ctx.textAlign = 'center'` for centered text
- Use `ctx.textBaseline = 'middle'` for vertical centering

**Performance:**
- Cache gradient objects (create once, reuse)
- Only redraw changed regions (advanced optimization)
- Use `requestAnimationFrame` for smooth rendering

---

## 14. Asset Checklist

**No external assets required!** Everything is drawn with Canvas API.

**Canvas-Drawn Elements:**
- [x] Phoenix (circles, triangles, arcs)
- [x] Pipes (rectangles)
- [x] Ground (filled rectangle)
- [x] Background (gradient)
- [x] Clouds (circles, optional)
- [x] Particles (circles, rectangles, text)
- [x] UI elements (text, rectangles, meters)
- [x] Buttons (rounded rectangles, text)

**No images, no sprites, no external fonts.**

---

## 15. Comparison to Game A

**Game A (Gerald) Visual Style:**
- Muted yellows/oranges
- Anxious, subdued appearance
- Minimal particle effects
- Simple emotional states

**Game B (Phoenix) Visual Style:**
- BRIGHT orange/red/gold
- Confident, dramatic appearance
- Extensive particle effects (flaps, scores, trails)
- Dynamic background color system
- Confidence aura and legendary trails
- Pipe personalities with faces
- More theatrical animations

**Distinct Visual Identity:** ✅ Achieved

---

## 16. Design Approval Checklist

**Visual Design Complete When:**
- [x] Color palette defined and justified
- [x] Character design fully specified (Phoenix)
- [x] Environment design documented (pipes, ground, sky)
- [x] UI layout designed for all screens (title, gameplay, game over)
- [x] Particle effects specified
- [x] Animation timings documented
- [x] Typography chosen and sized
- [x] Responsive design considered
- [x] Accessibility notes included
- [x] Different from Game A verified

---

## 17. Next Steps

**After Design Review:**
1. Queen approves visual design (Phase 1.5)
2. Transition to Developer role
3. Begin Phase 2 (Implementation)
4. Implement designs as specified
5. Iterate based on playtesting

---

**Document Status:** ✅ Complete
**Phase:** 1.4 Complete
**Next:** Phase 1.5 (Design Review & Approval)
**Ready for:** Implementation

---

*Prepared by BOT-00001 (Designer)*
*Role: Visual Designer*
*Phase: 1.4 Complete*
*Date: 2025-10-12*
