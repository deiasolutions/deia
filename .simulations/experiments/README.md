# Simulation Experiments - Flappy Bird Agent Training

**Session Date:** 2025-10-26
**Duration:** 1 hour
**Participants:** Bot A, Bot B (B1 lead + B2 support), Bot C

---

## Folder Structure

```
.simulations/experiments/
├── Bot_A/
│   └── WORKING-LOG.md          ← Watch Bot A's progress here
├── Bot_B/
│   └── WORKING-LOG.md          ← Watch Bot B pair's coordination here
├── Bot_C/
│   └── WORKING-LOG.md          ← Watch Bot C's progress here
└── README.md                    ← This file
```

---

## How to Watch

**Each bot has its own folder and notes:**
- `Bot_A/WORKING-LOG.md` - Bot A's real-time working notes
- `Bot_B/WORKING-LOG.md` - Bot B1 & B2's shared notes (with handoff tracking)
- `Bot_C/WORKING-LOG.md` - Bot C's real-time working notes

**Bots cannot see each other's folders** (except B1/B2 share one folder)

**To monitor during session:**
1. Open all 3 WORKING-LOG.md files side-by-side
2. Refresh as bots update them
3. See real-time decisions, progress, blockers
4. Watch B1/B2 coordinate and hand off work

---

## Deliverables

**After simulation, each bot will have:**
```
worktest00X-Bot_Y/
├── agents/           # Agent implementations
├── training/         # Training scripts
├── models/           # Trained model files
├── results/          # Results, scores, logs
├── config/           # Configuration
├── README.md         # Approach & results
├── ARCHITECTURE.md   # Design decisions
└── RESULTS.md        # Final scores & metrics
```

---

## Evaluation

**Winner determined by:**
1. **Game Score** (40%) - Highest score
2. **Code Quality** (25%) - DEIA standards
3. **Approach** (20%) - Thoughtfulness
4. **Documentation** (10%) - Clarity
5. **Coordination** (5%) - B pair only

---

## Key Rules

- ✅ **A ↔ B:** Cannot communicate or share
- ✅ **A ↔ C:** Cannot communicate or share
- ✅ **B ↔ C:** Cannot communicate or share
- ✅ **B1 ↔ B2:** Can communicate and coordinate (required)
- ✅ **Any ↔ Dave:** Can ask questions (not implementation help)
- ✅ **All bots:** Must follow DEIA protocols (auto-logging, hive updates)

---

## Notes File Format

Each bot's `WORKING-LOG.md` contains:
- **Timeline checkpoints** (00:00, 00:15, 00:30, 00:45, 01:00)
- **Real-time progress tracking** (checkboxes for completion)
- **Decision log** (what they decided and why)
- **Technical approach** (their method)
- **Key metrics** (scores, timing, code quality)

**Bot B additionally has:**
- **Handoff log** (B1 → B2 and B2 → B1 transitions)
- **Coordination notes** (how pair collaboration helped)
- **Separate B1/B2 note sections** (to track individual contributions)

---

## Start Simulation

When ready:
1. Bots read the task file: `.deia/hive/tasks/2025-10-26-SIMULATION-FLAPPY-BIRD-AGENTS.md`
2. Each bot starts their WORKING-LOG.md (update timestamps, begin notes)
3. Work begins - Dave watches the logs
4. At 1 hour, work stops
5. Bots file completion reports with final scores

---

**Judge:** Dave
**Status:** Ready to begin
