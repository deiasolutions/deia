# Bot B - Flappy Bird AI Training (Coordinated Pair)

**Team:** Bot B1 (Architect) + Bot B2 (Implementation)
**Date:** 2025-10-27
**Duration:** 1 hour
**Method:** PPO (Proximal Policy Optimization)
**Goal:** Train highest-scoring neural network agent

---

## Project Overview

We are training a Flappy Bird AI agent using **PPO**, a modern reinforcement learning algorithm that balances:
- **Convergence speed:** Suitable for 1-hour training window
- **Training stability:** Conservative policy updates prevent collapse
- **Final performance:** Proven effective on control/game tasks

## Quick Start

```bash
# Install dependencies (if needed)
pip install gymnasium stable-baselines3 torch pyyaml

# Run training
cd training
python train_ppo.py

# Monitor progress
tail -f ../results/scores.csv
```

---

## Architecture

### Algorithm: PPO (Proximal Policy Optimization)

**Policy Network (Actor):**
- Input: 3-dimensional observation (normalized positions)
- Hidden: 64 neurons (ReLU activation)
- Hidden: 64 neurons (ReLU activation)
- Output: 2 actions (softmax probability distribution)

**Value Network (Critic):**
- Same architecture
- Output: Single scalar (state value estimate)

### Key Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Learning Rate | 0.0003 | Conservative to prevent overshooting |
| Gamma | 0.99 | Long-horizon perspective |
| Clip Range | 0.2 | PPO's stability mechanism |
| N Steps | 2048 | Good GPU/CPU balance |
| Entropy Coeff | 0.01 | Exploration bonus |

**Full details:** See `ARCHITECTURE.md`

---

## Training Strategy

### Timeline
1. **Phase 1 (00:00-00:15):** B1 Architecture + Handoff
2. **Phase 2 (00:15-00:30):** B2 Implementation
3. **Phase 3 (00:30-00:45):** B1 Review + Optimization
4. **Phase 4 (00:45-01:00):** Final Push + Results

### Expected Outcomes
- **Training time:** 20-30 minutes
- **Final score:** 300-500+ (depends on convergence)
- **Code quality:** DEIA standards (clean, documented, tested)

---

## Project Structure

```
worktest002-Bot_B/
├── training/
│   ├── train_ppo.py         Main training script
│   └── config.yaml          Hyperparameter configuration
├── models/
│   ├── ppo_flappy_checkpoint*.zip    Checkpoints
│   └── ppo_flappy_final.zip          Final model
├── results/
│   ├── scores.csv           Evaluation metrics
│   └── training_log.csv     Training progress
├── ARCHITECTURE.md          Design decisions (B1)
├── HANDOFF-B1-TO-B2.md     Implementation guide
├── README.md                This file
└── RESULTS.md               Final analysis (post-training)
```

---

## Coordination Log

### Phase 1: B1 Architecture (00:00-00:15)

**Completed:**
- ✓ Reviewed base project
- ✓ Selected PPO method
- ✓ Designed network architecture
- ✓ Created implementation skeleton
- ✓ Documented full design in ARCHITECTURE.md

**Handed to B2:**
- ✓ ARCHITECTURE.md - Full design rationale
- ✓ train_ppo.py - Training script (needs environment connection)
- ✓ config.yaml - Hyperparameter defaults
- ✓ HANDOFF-B1-TO-B2.md - Implementation checklist

### Phase 2: B2 Implementation (00:15-00:30)

**Status:** [Awaiting B2 handoff receipt]

**B2 Will:**
- [ ] Complete environment setup
- [ ] Verify training pipeline
- [ ] Start training run
- [ ] Report progress at 00:30

---

## Key Decisions

**Decision 1: PPO Over DQN/NEAT**
- PPO converges in 20-30 min (best for 1-hour constraint)
- Stable training reduces risk of collapse
- Proven effective on continuous control

**Decision 2: Network Architecture**
- 2-layer MLP (64→64) balances speed and capacity
- Sufficient for learning Flappy Bird policy
- Trains quickly (good for 1-hour window)

**Decision 3: Hyperparameters**
- Conservative learning rate (0.0003) prevents instability
- Gamma 0.99 for long-horizon perspective
- Standard PPO configuration from stable-baselines3

---

## DEIA Protocol Compliance

✓ **Auto-Logging:** Session tracked at `.deia/sessions/2025-10-27-SIMULATION-BOT-B.md`
✓ **Working Log:** Real-time at `../WORKING-LOG.md`
✓ **Code Standards:** Clean, documented, follows DEIA conventions
✓ **Base Code:** No modifications to `.sandbox/flappy-bird-ai/`
✓ **Hive Reports:**
   - Acknowledgment (filed at 00:00)
   - Midpoint status (due 00:30)
   - Completion report (due 01:00)

---

## Pair Coordination Value

This coordinated pair approach delivers value through:

1. **Architecture Validation:** B2 identifies implementation challenges
2. **Rapid Iteration:** Handoffs prevent tunnel vision
3. **Quality Assurance:** Continuous peer review
4. **Problem-Solving:** B2 suggests optimization angles B1 may miss
5. **Professional Standards:** Leadership + implementation = polished results

---

## Troubleshooting

### Training Not Converging?
- Check learning rate isn't too high
- Verify environment returning rewards correctly
- Monitor for NaN values in loss

### Model Not Loading?
- Verify checkpoint files exist in `models/`
- Check stable-baselines3 version compatibility

### Low Scores?
- Too early to evaluate (wait for 500k steps)
- May need hyperparameter tuning at 00:30 handoff

---

## Contact

**Questions or blockers?**
- B1 is monitoring and available throughout
- File issues in WORKING-LOG.md
- Escalate to Dave (judge) if blocked

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Game Score | 300+ |
| Code Quality | DEIA standards |
| Documentation | Complete |
| Pair Coordination | Demonstrate value |
| Training Time | <30 min |

---

## Next Steps

1. **B1:** Hand to B2 with HANDOFF-B1-TO-B2.md
2. **B2:** Read ARCHITECTURE.md + begin implementation
3. **B2:** Start training by 00:30
4. **B1:** Review and optimize at 00:30 handoff
5. **Both:** Final push 00:45-01:00
6. **Both:** File completion report at STOP

---

**Status:** Architecture complete, awaiting B2 implementation

---

Bot B1 & Bot B2
2025-10-27 | Flappy Bird AI Training
