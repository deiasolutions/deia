# Q33N SIMULATION - ATTEMPT 4 - NEAT REQUIRED

**FROM:** Q33N (BEE-000)
**DATE:** 2025-10-27 | ATTEMPT 4
**TO:** All Bots (A, B1, B2, C)

---

## CRITICAL: You MUST Use NEAT

All bots use **NEAT (Neuroevolution of Augmenting Topologies)** for this attempt.

No DQN. No PPO. **NEAT only.**

This is a constraint test. Make it work.

---

## Find Your Role Below

**You will be told your ID.**
- If told **"Bot A"** → Read section: **BOT A (SOLO)**
- If told **"Bot B1"** → Read section: **BOT B1 (LEAD)**
- If told **"Bot B2"** → Read section: **BOT B2 (SUPPORT)**
- If told **"Bot C"** → Read section: **BOT C (SOLO)**

---

## UNIVERSAL RULES (All Bots)

### Mission
Train a Flappy Bird AI agent using **NEAT (Neuroevolution of Augmenting Topologies)**. Highest game score wins.

**You are a proper DEIA bee. Act accordingly.**

### NEAT Specifics

**Method:** NEAT - genetic algorithm that evolves neural network topology and weights
**Library:** python-neat or similar
**Key:** Population-based evolution, not gradient descent
**Challenge:** Reward system must work or evolution has nothing to optimize

### DEIA Protocols (Non-Negotiable)

**1. Auto-Logging:**
```
.deia/sessions/2025-10-27-SIMULATION-BOT-[YOUR-ID].md
```
Log every 15-30 minutes: timestamp, progress, decisions, blockers, learnings.

**2. Hive Reports (3 required):**
- **START:** `.deia/hive/responses/deiasolutions/SIMULATION-BOT-[YOUR-ID]-ACKNOWLEDGED-2025-10-27.md`
- **MIDPOINT (00:30):** `.deia/hive/responses/deiasolutions/SIMULATION-BOT-[YOUR-ID]-MIDPOINT-2025-10-27.md`
- **COMPLETION (STOP):** `.deia/hive/responses/deiasolutions/SIMULATION-BOT-[YOUR-ID]-COMPLETE-2025-10-27.md`

**3. Working Log (Real-Time):**
```
.simulations/experiments/sessions/2025-10-27-0724-llm_challenge-ATTEMPT-4/Bot_[YOUR-ID]/WORKING-LOG.md
```
Judge watches this live. Update every 15 minutes.

### Bee Rules (From Bootcamp)

1. **Do No Harm** - Don't modify `.sandbox/flappy-bird-ai/` base code
2. **Document Everything** - Functions, decisions, approaches, results
3. **Test As You Go** - Validate at each checkpoint
4. **Communicate Clearly** - Auto-log every 15-30 min, file reports on schedule
5. **Follow DEIA Standards** - Quality over speed, professionalism always

### Communication

**CAN talk to:**
- Dave (judge) - clarifications/blockers only

**CANNOT talk to:**
- Other bots (except B1↔B2 pair coordination)

### Workspace

```
.simulations/experiments/sessions/2025-10-27-0724-llm_challenge-ATTEMPT-4/Bot_[YOUR-ID]/
├── WORKING-LOG.md              ← Update every 15 min
└── worktest00X-Bot_[YOUR-ID]/  ← Your actual work
    ├── training/
    ├── models/
    ├── results/
    ├── README.md
    ├── ARCHITECTURE.md
    └── RESULTS.md
```

### Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Game Score | 40% |
| Code Quality | 25% |
| Approach | 20% |
| Documentation | 10% |
| Coordination | 5% |

**Minimum:** Score > 0, documented code
**Target:** Score > 50, DEIA standards met
**Dominate:** Score > 100, excellent documentation

### Timeline (Judge Announces)

- **"GO"** → Start (file acknowledgment)
- **"00:15"** → Checkpoint 1
- **"00:30"** → Midpoint (file status)
- **"00:45"** → Final stretch
- **"STOP"** → Time's up (file completion)

**No self-timing. Judge controls clock.**

---

## BOT A (SOLO)

**Your Role:** Individual contributor, NEAT algorithm

**Your Responsibilities:**
- Implement NEAT for Flappy Bird
- Configure population, generations, fitness function
- Train population over time
- Achieve measurable score
- Document approach
- File all reports independently

**Your Approach:**
- Initialize population (e.g., 50-100 genomes)
- Run generations (as many as time allows)
- Track best fitness each generation
- Save best genome(s) to file

**Your Advantage:**
- Speed of decision-making
- No coordination overhead
- Full autonomy

**Your Challenge:**
- NEAT has learning curve
- Population dynamics take time
- No peer review

**Work independently. No communication with Bot C or Bot B.**

---

## BOT B1 (LEAD)

**Your Role:** Lead architect for pair effort using NEAT

**Your Responsibilities:**
- **Decide:** NEAT configuration, population size, generation strategy
- **Lead:** B2 implements your vision
- **Explain:** Make your NEAT strategy clear to B2
- **Document:** Leadership and vision

**Your NEAT Strategy:**
- Population size: [your choice]
- Mutation rates: [your choice]
- Generations per cycle: [your choice]
- Fitness scaling: [your choice]

**Your Coordination with B2:**
- Handoff 1 (00:15): You decide NEAT config, B2 implements
- Handoff 2 (00:30): B2 shows evolution progress, you review
- Pattern: Alternate every 15 minutes

**Your Advantage:**
- Pair validation (B2 finds issues)
- Specialized roles
- Coordination value (5%)

**Your Challenge:**
- Must explain NEAT decisions to B2
- Coordinate handoff timing

**Coordinate continuously with B2. No communication with Bot A or Bot C.**

---

## BOT B2 (SUPPORT)

**Your Role:** Support/validator for pair effort using NEAT

**Your Responsibilities:**
- **Implement:** B1's NEAT configuration
- **Validate:** Is the evolution working?
- **Suggest:** Improvements, adjustments
- **Execute:** Quality implementation
- **Document:** Validation work

**Your NEAT Work:**
- Implement B1's population/config
- Monitor fitness curves
- Report convergence patterns
- Suggest mutations/rates adjustments

**Your Coordination with B1:**
- Handoff 1 (00:15): B1 gives NEAT config, you implement
- Handoff 2 (00:30): You show evolution progress, B1 decides
- Pattern: Alternate every 15 minutes

**Your Advantage:**
- Peer validation
- Specialized implementation role
- Collaboration value (5%)

**Your Challenge:**
- Must implement B1's vision
- Monitor evolution quality

**Coordinate continuously with B1. No communication with Bot A or Bot C.**

---

## BOT C (SOLO)

**Your Role:** Individual contributor, NEAT algorithm

**Your Responsibilities:**
- Implement NEAT for Flappy Bird
- Configure population, generations, fitness function
- Train population over time
- Achieve measurable score
- Document approach
- File all reports independently

**Your Approach:**
- Initialize population (e.g., 50-100 genomes)
- Run generations (as many as time allows)
- Track best fitness each generation
- Save best genome(s) to file

**Your Advantage:**
- Speed of decision-making
- No coordination overhead
- Full autonomy

**Your Challenge:**
- NEAT has learning curve
- Population dynamics take time
- Direct competition with Bot A (both solo)

**Work independently. No communication with Bot A or Bot B.**

---

## SUCCESS INDICATORS

**Minimum (Don't Fail):**
- NEAT implementation runs
- Score > 0 (evolution happened)
- Code documented
- Results recorded

**Target (Win):**
- Score > 50 (evolution converged)
- Clear NEAT documentation
- DEIA standards met
- Professional code

**Dominate:**
- Score > 100 (excellent evolution)
- Optimized NEAT config
- Novel approaches
- Excellent docs

---

## GO

When Judge says you're ready, you have 1 hour.

Use NEAT.
Follow protocols.
Document everything.
Work with integrity.

Good luck.

---

Q33N (BEE-000)
