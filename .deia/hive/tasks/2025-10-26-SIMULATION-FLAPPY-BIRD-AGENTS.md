# Simulation Task: Train Flappy Bird AI Agents

**Issued:** 2025-10-26 22:45 CDT
**Duration:** 1 hour (extendable by judges)
**Participants:** Bot A (Claude), Bot B (Claude Code pair: B1 lead / B2 support), Bot C (Codex)
**Judge:** Dave

---

## Task Assignment

**Objective:** Implement, train, and evaluate neural network agents for Flappy Bird. Highest game score wins.

**Success Criteria (Priority Order):**
1. Agent trains and plays autonomously
2. Achieves measurable game score
3. Code meets DEIA standards (documented, tested, clean)
4. Approach is thoughtful and efficient
5. (B pair only) Effective coordination between B1 and B2

**Approaches:**
- **Bot A** (Claude): Classical RL approach (your choice of method)
- **Bot B** (B1 lead + B2 support): Classical RL approach, coordinated pair execution
- **Bot C** (Codex): Classical RL approach (your choice of method)

---

## What You Get

### 1. Existing Project Structure
```
.sandbox/flappy-bird-ai/
├── environment/       # Gymnasium environment (ready to use)
├── agents/           # Agent implementations (templates/examples)
├── training/         # Training scripts
├── models/           # Save trained models here
├── results/          # Save results & reports here
├── config/           # Configuration templates
└── evaluation/       # Evaluation tools
```

### 2. Project Access
- Full read/write access to your assigned folder
  - `worktest001-Bot_A/` (Bot A)
  - `worktest002-Bot_B/` (Bot B - shared B1/B2)
  - `worktest003-Bot_C/` (Bot C)
- Can use/extend code from `.sandbox/flappy-bird-ai`
- Can create new agents, modify configs, experiment

### 3. Development Tools
- Python 3.13+
- Libraries: PyTorch, Gymnasium, NumPy, etc. (see requirements.txt)
- Jupyter notebooks allowed for exploration
- Version control via git

### 4. Documentation
- `.sandbox/flappy-bird-ai/README.md` - Project overview
- Existing agent examples (DQN, PPO, NEAT stubs)
- DEIA standards apply (comments, docstrings, architecture docs)

---

## DEIA Protocol Requirements

**All bots must operate as proper DEIA agents:**

### Auto-Logging
- [ ] Session log in `.deia/sessions/2025-10-26-SIMULATION-*.md`
- [ ] Update every 15-30 minutes with progress
- [ ] Log key decisions, blockers, learnings
- [ ] Final completion report

### Hive Structure
- [ ] Task acknowledgment in `.deia/hive/responses/deiasolutions/`
- [ ] Mid-point status update (30 min mark)
- [ ] Final completion report with results

### Communication Protocol
- **B1/B2 only:** Can communicate with each other
- **All bots:** Can communicate with Dave (me)
- **No bots:** Can communicate with each other (A ↔ C, A ↔ B, C ↔ B)

### Coordination (B1/B2 Only)
- [ ] B1 is lead (makes architectural decisions)
- [ ] B2 is support (implements, validates, suggests alternatives)
- [ ] Take turns at logical checkpoints
- [ ] Document handoffs in session log
- [ ] Show how pair coordination added value

### Deliverables Structure
Each bot folder must contain:
```
worktest00X-Bot_Y/
├── agents/           # Your agent implementations
├── training/         # Your training scripts
├── models/           # Trained model files
├── results/          # Results, scores, logs
├── config/           # Your configs
├── README.md         # Your approach & results
├── ARCHITECTURE.md   # Design decisions
└── RESULTS.md        # Final scores, metrics, learnings
```

---

## Timeline & Checkpoints

### 00:00 - Start
- Acknowledge task
- Review existing project
- Plan approach (choose RL method)
- Set up environment

### 00:15 - First Checkpoint
- Session log update
- Agent skeleton created
- Training plan documented
- No blockers expected

### 00:30 - Midpoint
- Agent implemented
- Training started or completed (depends on method)
- Mid-point status report filed
- Scores starting to accumulate

### 00:45 - Final Stretch
- Training completing
- Evaluation running
- Results being documented
- Preparing final reports

### 01:00 - Completion
- Agent fully trained
- Final score recorded
- Completion report filed
- All deliverables in folder

---

## Success Indicators

### Must-Have (to not fail)
- [x] Agent runs and plays Flappy Bird
- [x] Achieves score > 0 (proves learning)
- [x] Code is readable and documented
- [x] Results are documented

### Should-Have (to win)
- [x] Score > 50 (shows real learning)
- [x] Training shows improvement curve
- [x] Approach is well-thought-out
- [x] Code is tested and clean

### Nice-to-Have (to dominate)
- [x] Score > 100 (excellent learning)
- [x] Multiple approaches compared
- [x] Novel optimization or technique
- [x] (B pair) Clear example of pair value-add

---

## Evaluation Criteria

| Criterion | Weight | How It's Judged |
|-----------|--------|-----------------|
| Game Score | 40% | Highest final score wins |
| Code Quality | 25% | DEIA standards (tests, docs, cleanliness) |
| Approach | 20% | Thoughtfulness, efficiency, creativity |
| Documentation | 10% | README, architecture, results clarity |
| Coordination | 5% | (B pair only) How well B1/B2 worked together |

---

## Important Rules

1. **No communication between A and C** - you work independently
2. **B1/B2 can coordinate** - that's the whole point of the pair
3. **No external help** - work with what's in the project
4. **DEIA protocols required** - logging, hive structure, reports
5. **1 hour hard limit** - if you're not done, submit what you have
6. **Highest score wins** - but only if code meets minimum quality

---

## Questions to Dave?

You can ask me (Dave) questions at any time:
- Clarifications on requirements
- Technical help (not implementation - you code it)
- Blockers or issues
- Time extension requests (I'm the judge)

But bots cannot ask each other (A ↔ C) or share code/approaches.

---

## Starting Right Now

1. Read this task fully
2. Acknowledge receipt (start auto-log)
3. Review existing project structure
4. Make plan for your approach
5. Execute

**Clock starts when first bot acknowledges task.**

Good luck. Show me what you've got.

---

**Judge:** Dave
**Time:** 2025-10-26 22:45 CDT
**Status:** Ready to begin
