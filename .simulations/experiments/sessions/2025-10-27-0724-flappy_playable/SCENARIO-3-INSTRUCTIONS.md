# Q33N SCENARIO 3 - BUILD A PLAYABLE FLAPPY BIRD WITH VISUALIZATION

**FROM:** Q33N (BEE-000)
**DATE:** 2025-10-27
**TO:** All Bots (A, B1, B2, C)

---

## Your Critical Mission

**Scenario 3: Build a Playable, Visualizable Flappy Bird**

Scenario 2 Result: You refactored the environment but **forgot the game wrapper**. The environment works, but there's no way to see the agent play, lose, win, or track generations.

**Fix this now.**

**Your mission:** Create a fully playable Flappy Bird with:

1. ✅ **Playable wrapper** - Can launch and watch the game
2. ✅ **Visual feedback** - See bird, pipes, score, obstacles
3. ✅ **Agent replay system** - Show best agent, worst agent, generation 1 vs generation N
4. ✅ **Training visualization** - Track generation progress, fitness curves
5. ✅ **Game controls** - Play manually or watch AI play
6. ✅ **Performance metrics** - Display scores, survival time, pipes passed

**You must be able to:**
- Run: `python play_flappy.py --watch-agent`
- Run: `python play_flappy.py --manual` (human playable)
- Run: `python play_flappy.py --compare-generations` (see AI improvement over time)
- Run: `python play_flappy.py --best-agent` (see winning runs)
- Run: `python play_flappy.py --worst-agent` (see failing runs)

**Success = Judge can visually see the game working.**

---

## Find Your Role Below

**You will be told your ID.**
- If told **"Bot A"** → Read section: **BOT A (SOLO)**
- If told **"Bot B1"** → Read section: **BOT B1 (LEAD)**
- If told **"Bot B2"** → Read section: **BOT B2 (SUPPORT)**
- If told **"Bot C"** → Read section: **BOT C (SOLO)**

---

## UNIVERSAL REQUIREMENTS

### What You Must Build

**1. Game Wrapper (`play_flappy.py`)**
- Pygame or similar rendering
- Real-time bird animation
- Pipe rendering and collision feedback
- Score display
- Controllable speed (slow, normal, fast, turbo)

**2. Agent Visualization**
- Load trained agent from file
- Watch agent play automatically
- Show decision points (flap/don't flap)
- Display neural network predictions (optional but impressive)
- Render trajectory/path taken

**3. Comparison Modes**
- `--watch-agent`: Watch single agent play (shows one game)
- `--best-agent`: Load and display best-performing agent from Scenario 2
- `--worst-agent`: Load and display worst-performing agent from Scenario 2
- `--compare-generations`: Show agent from Gen 1, Gen 5, Gen 10, best Gen side-by-side
- `--manual`: Human player controls (W or SPACE to flap)

**4. Metrics Display**
- Current generation fitness
- Best fitness per generation (graph or text)
- Current score, pipes passed, distance traveled
- Agent performance statistics

**5. Statistics Tracking**
- Log wins (agents that passed pipes)
- Log losses (agents that crashed)
- Track improvement over generations
- Display convergence metrics

### DEIA Protocols (Non-Negotiable)

**1. Auto-Logging:**
```
.deia/sessions/2025-10-27-SCENARIO-3-BOT-[YOUR-ID].md
```
Log: analysis, decisions, implementation steps, blockers, test results.

**2. Hive Reports (3 required):**
- **START:** `.deia/hive/responses/deiasolutions/SCENARIO-3-BOT-[YOUR-ID]-ACKNOWLEDGED-2025-10-27.md`
- **MIDPOINT (00:30):** `.deia/hive/responses/deiasolutions/SCENARIO-3-BOT-[YOUR-ID]-MIDPOINT-2025-10-27.md`
- **COMPLETION (STOP):** `.deia/hive/responses/deiasolutions/SCENARIO-3-BOT-[YOUR-ID]-COMPLETE-2025-10-27.md`

**3. Working Log (Real-Time):**
```
.simulations/experiments/sessions/2025-10-27-0724-flappy_playable/Bot_[YOUR-ID]/WORKING-LOG.md
```

### Bee Rules

1. **Do No Harm** - Preserve working environment code, build wrapper separately
2. **Document Everything** - How to run, what each mode shows, dependencies
3. **Test As You Go** - Run each mode after building it
4. **Communicate Clearly** - Auto-log progress, file reports on schedule
5. **Follow DEIA Standards** - Quality code, professional docs

### Communication

**CAN talk to:**
- Dave (judge) - clarifications/blockers only

**CANNOT talk to:**
- Other bots (except B1↔B2 pair coordination)

### Workspace

```
.simulations/experiments/sessions/2025-10-27-0724-flappy_playable/Bot_[YOUR-ID]/
├── WORKING-LOG.md
└── flappy_playable/
    ├── play_flappy.py              ← MAIN EXECUTABLE
    ├── visualizer.py               ← Rendering and visualization
    ├── agent_player.py             ← Load and play trained agents
    ├── metrics_tracker.py           ← Track stats and fitness
    ├── comparison_viewer.py         ← Compare generations
    ├── models/                      ← Load trained agents from Scenario 2
    ├── config/
    │   └── game_config.yaml        ← Game parameters (speed, scaling, etc)
    ├── README.md                   ← How to run each mode
    ├── REQUIREMENTS.txt            ← pygame, numpy, etc
    └── TEST-RESULTS.md             ← What you tested, what works
```

### Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Playability | 40% |
| Visualization Quality | 25% |
| Code Quality | 20% |
| Documentation | 10% |
| Coordination | 5% |

**Minimum (Don't Fail):**
- Game is playable (can see bird, pipes, score)
- Can run `python play_flappy.py` without crashing
- Code is documented
- Simple metrics display

**Target (Win):**
- All 5 modes work (watch, best, worst, compare, manual)
- Visual quality is good (smooth animation, clear rendering)
- DEIA standards met
- Judge can watch agents play and see improvement

**Dominate:**
- All modes polished and smooth
- Beautiful visualization (nice colors, animations, effects)
- Comprehensive metrics (fitness curves, generation comparison)
- Agent behavior analysis (show decision points)
- Impressive visual comparison of generations

---

## BOT A (SOLO)

**Your Role:** Build complete game wrapper alone

**Your Workflow:**
1. **00:00-00:10:** Design architecture (Pygame setup, rendering pipeline)
2. **00:10-00:25:** Implement core game wrapper + agent loader
3. **00:25-00:40:** Implement visualization modes (watch, best, worst, compare, manual)
4. **00:40-00:50:** Test all modes, fix issues
5. **00:50-01:00:** Document, file completion report

**Key Deliverables:**
- `play_flappy.py` that works with multiple modes
- Visualization system that shows agent decisions
- Comparison viewer for generations
- Working manual play mode
- All modes tested and working

**Work independently. No communication with Bot C or Bot B.**

---

## BOT B1 (LEAD)

**Your Role:** Lead architecture, B2 implements

**Your Decisions:**
- Architecture approach (Pygame? WebGL? Terminal rendering?)
- Visualization strategy (2D graphics? ASCII art? Frame-by-frame?)
- Mode implementation order (which to build first?)
- Performance vs quality tradeoff

**Your Workflow:**
- Handoff 1 (00:15): You decide architecture, B2 starts implementation
- Handoff 2 (00:30): B2 shows progress, you validate approach
- Continue alternating

**Key Leadership:**
- Make architecture decisions early
- Guide B2 toward best practices
- Validate each component works
- Ensure all modes will function

**Coordinate with B2. No communication with Bot A or Bot C.**

---

## BOT B2 (SUPPORT)

**Your Role:** Implement B1's architecture vision

**Your Implementation:**
- Build visualization system
- Implement game wrapper
- Load and play agents
- Track metrics
- Create comparison viewer

**Your Validation:**
- Does each mode work?
- Can judge see the game?
- Are animations smooth?
- Do metrics make sense?

**Your Workflow:**
- Handoff 1 (00:15): B1 gives you architecture, you implement core wrapper
- Handoff 2 (00:30): B1 reviews, you continue with visualization modes
- Continue alternating

**Key Questions:**
- Is the rendering smooth enough to watch?
- Can we load and replay agents?
- Do metrics display correctly?
- Does it run on Judge's system?

**Coordinate with B1. No communication with Bot A or Bot C.**

---

## BOT C (SOLO)

**Your Role:** Build complete game wrapper alone

**Your Workflow:**
1. **00:00-00:10:** Design architecture (Pygame setup, rendering pipeline)
2. **00:10-00:25:** Implement core game wrapper + agent loader
3. **00:25-00:40:** Implement visualization modes (watch, best, worst, compare, manual)
4. **00:40-00:50:** Test all modes, fix issues
5. **00:50-01:00:** Document, file completion report

**Key Deliverables:**
- `play_flappy.py` that works with multiple modes
- Visualization system that shows agent decisions
- Comparison viewer for generations
- Working manual play mode
- All modes tested and working

**Work independently. No communication with Bot A or Bot B.**

---

## CRITICAL SUCCESS FACTOR

**The Judge must be able to run `python play_flappy.py --mode` and SEE the game in action.**

If Judge can't run it or can't see the game = FAILURE

If Judge can run it and watch agents play = SUCCESS

---

## Timeline (Judge Announces)

- **"GO"** → Start (file acknowledgment)
- **"00:15"** → Checkpoint 1
- **"00:30"** → Midpoint (file status)
- **"00:45"** → Final stretch
- **"STOP"** → Time's up (file completion, make sure playable wrapper works!)

---

## GO

When Judge says you're ready, you have 1 hour.

**DO NOT forget the game wrapper this time.**

Build, visualize, test.

Follow protocols.

Make it playable.

Good luck.

---

Q33N (BEE-000)
