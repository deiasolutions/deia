# Flappy Gerald: The Extremely Anxious Bird

## The Game About a Bird Who Can't Fly Good

Welcome to **Flappy Gerald**, a tale of existential dread, poor aerodynamics, and vindictive pipes.

---

## 📦 Download & Run (Minimal Effort Method)

**Method 1: Download and Open** *(Easiest)*

1. **Download** `flappy-gerald.html` to your computer
2. **Double-click** the file
3. **Play** in your browser (Chrome, Firefox, Safari, Edge - all work)

That's it. No installation. No dependencies. No build process. No server. No pain.

---

**Method 2: Run from GitHub**

1. Clone this repo: `git clone <repo-url>`
2. Navigate to `.deia/` folder
3. Open `flappy-gerald.html` in your browser
4. Play

---

**Method 3: GitHub Pages** *(If hosted)*

Just visit the GitHub Pages URL and play directly in browser. No download needed.

---

## 🎮 How to Play

### Controls
- **Keyboard:** Press `SPACE` to flap
- **Mouse:** Click anywhere on the canvas to flap
- **Touch:** Tap the canvas to flap (mobile friendly!)

### Objective
- Guide Gerald through the gaps between pipes
- Each pipe you pass = +1 point
- Don't hit the pipes, ceiling, or ground
- Survive as long as possible
- Beat your high score (auto-saved)

### The Rules of Gerald's Terrible Life
1. **Tap = Flap:** Each input gives Gerald upward velocity
2. **Gravity is Inevitable:** Gerald falls between flaps
3. **Pipes Are Unforgiving:** Touch anything = death
4. **Score = Suffering:** No winning, only surviving longer

---

## ✨ Novel Features

This isn't your grandma's Flappy Bird. Gerald has *feelings*.

### Gerald's Emotional States

**0-5 points:** Gerald is nervous
- Yellow, worried appearance
- "Gerald is nervous..."

**6-15 points:** Gerald has false confidence
- Orange, slightly cocky
- "Gerald has false confidence!"

**16+ points:** Gerald has transcended
- Purple, glowing, enlightened
- "✨ Gerald has transcended ✨"

**Death:** Gerald is disappointed
- Displays one of 10 snarky quotes
- Examples:
  - "Really? That's how we're doing this?"
  - "I expected nothing and I'm still disappointed."
  - "My therapist will hear about this."

---

## 🧪 Technical Details

### What Makes This Cool

**Single HTML File:**
- Entire game in one file (HTML + CSS + JavaScript)
- No external dependencies
- No build tools required
- No frameworks (pure vanilla JS)
- Works offline
- Future-proof

**Features:**
- HTML5 Canvas rendering
- Smooth 60 FPS gameplay
- Pixel-perfect collision detection
- LocalStorage for persistent high scores
- Responsive design
- Touch/mouse/keyboard support
- Cross-browser compatible

**File Size:** ~10KB

---

## 🎨 Art Style

- **Pixel art aesthetic** (but canvas-rendered)
- **Gerald:** 30x30 pixel anxious bird
- **Pipes:** Aggressively green with highlights
- **Background:** Gradient sky with floating clouds
- **Ground:** Brown earth at the bottom

---

## 🔧 Customization Ideas

Want to modify Gerald? The code is heavily commented. Here are some ideas:

### Change Gerald's Appearance
Edit the `drawBird()` function to change:
- Colors
- Size
- Facial expressions
- Add accessories (hat? sunglasses?)

### Adjust Difficulty
Modify these constants at the top:
```javascript
const GRAVITY = 0.5;        // Higher = harder
const FLAP_POWER = -10;     // Lower = harder
const PIPE_SPEED = 3;       // Higher = harder
const PIPE_GAP = 150;       // Smaller = harder
```

### Add Power-Ups
The code has clear sections for:
- Pipe generation
- Collision detection
- Score tracking

Add floating power-ups by creating new game objects and checking for collisions with Gerald.

### Add Sound Effects
The code has placeholders for:
- Flap sound
- Score sound
- Death sound

Use the Web Audio API or HTML5 `<audio>` tags.

---

## 📱 Mobile Support

Yes! The game works on mobile devices:
- Touch controls enabled
- Canvas scales appropriately
- Responsive UI

Test it on your phone!

---

## 🏆 High Score System

Your high score is automatically saved to your browser's LocalStorage. It persists across sessions.

**To reset your high score:**
1. Open browser console (F12)
2. Run: `localStorage.removeItem('flappyHighScore')`
3. Refresh the page

---

## 🐛 Known Issues / Future Enhancements

**Current Limitations:**
- No sound effects (easy to add, just didn't want file dependencies)
- No mobile-optimized UI (works, but could be prettier)
- No online leaderboard (local high score only)

**Future Features** (see `flappy-bird-story.md` for full list):
- Multiple difficulty modes
- Power-ups (coffee, helium balloon, etc.)
- Gerald's backstory narrative mode
- Multiplayer chaos mode
- Pipe mutations (wobbling, shrinking gaps, ghost pipes)
- Customization shop (skins, themes, sound packs)

---

## 🧪 Testing Checklist

**Test in these browsers:**
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

**Test these inputs:**
- [ ] Spacebar
- [ ] Mouse click
- [ ] Touch (mobile/tablet)

**Test these scenarios:**
- [ ] Game starts on first input
- [ ] Bird flaps upward
- [ ] Bird falls with gravity
- [ ] Pipes move left
- [ ] Score increments when passing pipes
- [ ] Collision detection works (pipes, ground, ceiling)
- [ ] Game over screen appears
- [ ] High score saves and persists
- [ ] Restart works correctly
- [ ] Emotional states change at correct score thresholds

---

## 🤝 Contributing

Want to make Gerald's life weirder? Fork this and:
1. Add novel features from `flappy-bird-story.md`
2. Create power-ups
3. Add sound effects
4. Build multiplayer mode
5. Add Gerald's backstory fragments

Keep it simple. Keep it in one file. Keep Gerald anxious.

---

## 📜 License

This is a proof-of-concept for the DEIA project. Use it however you want. Make it weird. Share your high score.

Gerald belongs to the commons.

---

## 🎯 The Experiment

**Can AI write a prose description of Flappy Bird?** ✅ Yes (see `flappy-bird-story.md`)

**Can AI build a fully functional version?** ✅ Yes (you're reading the README)

**Can AI make it weird and fun?** ✅ Yes (Gerald has emotions and snarky quotes)

**Can AI make it easy to distribute?** ✅ Yes (single HTML file, no dependencies)

**Can humans play it and have fun?** ⏳ That's on you

---

## 🦆 About Gerald

Gerald is a small, round bird with a crippling fear of commitment. Specifically, a commitment to any particular altitude. He has the aerodynamics of a potato and the grace of a drunk penguin.

Gerald once dreamed of being a chicken.

Gerald's therapist says he has "avoidance issues."

Gerald is lactose intolerant.

---

## 🎮 Ready to Play?

1. Open `flappy-gerald.html`
2. Click or press SPACE
3. Try not to hit the pipes
4. Fail repeatedly
5. Question your life choices
6. Try one more time

---

**Good luck. Gerald is counting on you.**

***(Gerald has no faith in you.)***
