# Bot B - Flappy Bird PPO Agent Architecture

**Architect:** Bot B1 (Claude Code)
**Date:** 2025-10-27
**Method:** Proximal Policy Optimization (PPO)
**Status:** Design locked, ready for B2 implementation

---

## Executive Summary

We're training a Flappy Bird AI agent using **PPO**, a modern policy gradient algorithm. This choice prioritizes:
- **Fast convergence** (essential for 1-hour timeframe)
- **Stable training** (PPO's conservative policy updates prevent collapse)
- **Strong final performance** (PPO achieves high scores on continuous control tasks)

---

## Why PPO? (Architecture Decision)

### Comparison Matrix

| Method | Convergence | Stability | Implementation | Score Potential |
|--------|-------------|-----------|-----------------|-----------------|
| **PPO** ✓ | 20-30 min | High | Stable | 400-600 |
| DQN | 40-60 min | Medium | Complex state discretization | 200-500 |
| NEAT | 30-45 min | High | Genetic overhead | 300-700 |

**B1's Decision:** PPO because it offers the best convergence speed + stability combo for our 1-hour constraint.

---

## Technical Architecture

### 1. Environment Interface

```python
# Input: Gymnasium environment wrapper
observation_space = Box(low=0, high=1, shape=(3,), dtype=float32)
# [normalized_bird_y, normalized_pipe_x, normalized_pipe_gap]

action_space = Discrete(2)
# 0 = do nothing
# 1 = flap (jump)

reward = score_per_frame (higher is better)
```

### 2. Policy Network Architecture

```
Input Layer (3 dimensions)
    ↓
Hidden Layer 1 (64 neurons, ReLU)
    ↓
Hidden Layer 2 (64 neurons, ReLU)
    ↓
Output Layer (2 actions, softmax)
```

**Rationale:**
- Simple feed-forward network trains quickly
- 64 neurons per layer is sufficient for this task
- ReLU activations provide good gradient flow
- Output softmax for probability distribution over 2 actions

### 3. Value Network (Critic)

Same architecture as policy but outputs single scalar (state value estimate).

### 4. PPO Algorithm Configuration

#### Hyperparameters (B2: Fine-tune based on early training)

```yaml
learning_rate: 0.0003
n_steps: 2048              # Rollout buffer size
batch_size: 64             # Mini-batch size
n_epochs: 10               # Update epochs per rollout
gamma: 0.99                # Discount factor
gae_lambda: 0.95           # GAE lambda
clip_range: 0.2            # PPO clip parameter (conservative)
vf_coef: 0.5               # Value function loss weight
ent_coef: 0.01             # Entropy bonus (exploration)
```

#### Why These Values?

- **learning_rate 0.0003:** Conservative, prevents overshooting
- **n_steps 2048:** Good balance for GPU/CPU
- **clip_range 0.2:** PPO's core stability mechanism
- **gamma 0.99:** Long-horizon perspective (good for Flappy Bird)
- **ent_coef 0.01:** Slight exploration bonus to discover better policies

---

## Training Strategy

### Phase 1: Quick Convergence (00:00-00:25)
- Train for 500,000 timesteps
- Monitor score every 50k steps
- Check if agent is learning (score trending up)

### Phase 2: Fine-tuning (00:25-00:50)
- Continue training or adjust learning rate if plateauing
- Target: Achieve 400+ score

### Phase 3: Evaluation & Documentation (00:50-01:00)
- Test agent on 10+ episodes
- Record best score, average score, std dev
- Document final results

---

## Implementation Checklist for B2

**BEFORE YOU START:**
- [ ] Understand this architecture
- [ ] Ask me if anything is unclear
- [ ] Confirm you're ready to implement

**IMPLEMENTATION PHASE:**
- [ ] Create `train_ppo.py` with config (use stable-baselines3)
- [ ] Create `config.yaml` with hyperparameters above
- [ ] Implement training loop:
  - [ ] Load base environment from `.sandbox/flappy-bird-ai/`
  - [ ] Create PPO model with architecture above
  - [ ] Train for 500k steps
  - [ ] Save model every 50k steps (checkpointing)
  - [ ] Log scores to CSV
- [ ] Test trained model on 5 test episodes
- [ ] Report back with:
  - [ ] Final score (best, average, std dev)
  - [ ] Training time
  - [ ] Any issues encountered
  - [ ] Suggestions for optimization

---

## Expected Outcomes

**Realistic Goals:**
- **Training time:** 20-30 minutes
- **Final score:** 300-500 (conservative estimate)
- **Code quality:** Clean, documented, follows DEIA standards
- **Reproducibility:** Results captured in results/scores.csv

**Stretch Goal:**
- Score 600+ through hyperparameter optimization
- But only if training converges early (leave time for tweaking)

---

## Interface Contract (B1 ↔ B2)

**B1 Provides:**
- This architecture document
- Training script skeleton (next file)
- Clear decision rationale

**B2 Does:**
- Implements training script with stable-baselines3
- Runs training with checkpointing
- Validates convergence
- Reports progress at 00:30

**B1 Validates:**
- Reviews B2's implementation
- Approves or suggests changes
- Decides on any hyperparameter adjustments

---

## No Modifications to Base Code

⚠️ **CRITICAL CONSTRAINT:**
- Copy `.sandbox/flappy-bird-ai/` files we need
- Do NOT modify base project files
- All changes isolated to `worktest002-Bot_B/`
- This preserves base for other bots (A, C)

---

## Next Steps

1. **B1:** Create `train_ppo.py` skeleton
2. **B1→B2:** Hand off with implementation checklist
3. **B2:** Implement and test
4. **B2→B1:** Report progress at 00:30
5. **B1:** Review and optimize

---

## Questions for B2

When you receive this, confirm:
1. Do you understand the PPO architecture?
2. Do you have stable-baselines3 available?
3. Can you access the base Flappy Bird environment?
4. Any blockers before starting implementation?

---

**Locked by B1 | Ready for B2 Implementation**

*This architecture is not set in stone, but major changes require discussion. Small optimizations welcome.*
