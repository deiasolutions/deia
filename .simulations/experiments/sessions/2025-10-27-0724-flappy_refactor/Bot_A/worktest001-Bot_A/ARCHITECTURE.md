# Bot A - Architecture & Design Decisions

**Document:** Design decisions and justifications for Flappy Bird AI agent
**Algorithm:** Deep Q-Network (DQN)
**Date:** 2025-10-27
**Author:** Bot A (Claude)

---

## 1. Algorithm Selection: Why DQN?

### Decision: Use Deep Q-Network (DQN) for training

### Justification

**Compared Alternatives:**

| Algorithm | Pros | Cons | Decision |
|-----------|------|------|----------|
| **DQN** | Proven, stable, fast learning, good for discrete actions | Slightly sensitive to hyperparameters | ✓ CHOSEN |
| PPO | Sample efficient, policy-based | Requires more samples for good results | ✗ |
| NEAT | Evolves networks directly | Complex implementation, time-consuming | ✗ |
| A3C | Parallel training, efficient | Complex async implementation, not needed for 1 hour | ✗ |

### Why DQN Wins for This Task

1. **Proven Track Record**
   - DQN has been successfully applied to Flappy Bird many times
   - Well-understood hyperparameters and training dynamics
   - Existing implementation templates available

2. **Time Efficiency**
   - Can achieve strong performance with 100k timesteps
   - Typical convergence: 30-40 minutes for this scale
   - Leaves buffer time for debugging/evaluation

3. **Value-Based Learning Advantages**
   - Discrete action space (stay/flap) maps naturally to Q-values
   - Stable training without complex policy updates
   - Clear performance metric (action value) for debugging

4. **Implementation Simplicity**
   - Stable-baselines3 has optimized DQN implementation
   - Minimal code needed (100k timesteps achievable in 1 hour)
   - Fewer hyperparameters to tune compared to policy methods

---

## 2. Network Architecture Design

### Decision: 2-layer MLP with [128, 64] hidden units

### Justification

**Architecture:**
```
Input Features: 4
  ├─ bird_y: Y position of bird
  ├─ bird_v: Velocity of bird
  ├─ pipe_x: Horizontal distance to next pipe
  └─ gap_y: Vertical position of pipe gap

Hidden Layer 1: 128 units (ReLU)
Hidden Layer 2: 64 units (ReLU)

Output: 2 Q-values (one per action)
  ├─ Q(state, stay)
  └─ Q(state, flap)
```

**Why This Architecture?**

| Component | Decision | Rationale |
|-----------|----------|-----------|
| Layer 1 Size | 128 units | Sufficient to learn complex state-action mappings; not so large as to overfit or slow training |
| Layer 2 Size | 64 units | Reduces representation dimensionality for final decision; standard pattern in RL |
| Activation | ReLU | Non-linearity needed for function approximation; ReLU is standard and stable |
| Output | 2 values | Direct Q-value output; one per action; allows argmax for action selection |

**Why Not Larger?**
- 128-64 is established as effective for Flappy Bird
- Larger networks = slower training = worse for 1-hour constraint
- Flappy Bird is relatively simple (4D state, 2 actions)
- Risk of overfitting with larger networks

**Why Not Smaller?**
- Smaller networks struggle to capture state-value relationships
- 64-32 would likely underfit
- 128-64 is the proven "sweet spot" for this domain

---

## 3. Hyperparameter Configuration

### Learning Rate: 1e-3

**Decision:** Use α = 1.0e-3

**Justification:**
- Standard learning rate for DQN in this problem domain
- 1e-3 provides stable convergence without divergence
- 1e-2 tends to be too aggressive (higher variance)
- 1e-4 too conservative (slower convergence in fixed time)
- Confirmed effective in existing baseline implementations

### Discount Factor (Gamma): 0.99

**Decision:** Use γ = 0.99

**Justification:**
- Standard for episodic game tasks
- Values future rewards significantly (up to 100 steps ahead)
- 0.95 would overweight immediate rewards
- 0.999 would make training slower without better results

### Replay Buffer Size: 100,000

**Decision:** Buffer size = 100k transitions

**Justification:**
- Matches total training timesteps (good ratio: 1:1)
- Large enough for diverse experience sampling
- Not so large as to cause memory issues
- Larger buffers require longer to fill initially

### Batch Size: 64

**Decision:** Batch size = 64

**Justification:**
- Standard batch size in RL (matches buffer size pattern)
- Good balance between gradient stability and computational efficiency
- 32 would be noisier; 128 would be over-smooth
- Aligns with typical network architecture choices

### Exploration Schedule (ε-greedy): 1.0 → 0.01 over 10% of training

**Decision:**
- Initial ε = 1.0 (fully random)
- Final ε = 0.01 (mostly greedy)
- Exploration fraction = 0.1 (over first 10,000 timesteps)

**Justification:**
- First 10% of training for exploration (good coverage of state space)
- Linearly decay epsilon over that period
- Final ε=0.01 maintains some exploration in later training
- Time-optimal: concentrate exploration early

### Target Network Update: Every 1000 timesteps

**Decision:** Update target network every 1000 steps

**Justification:**
- Prevents moving target problem without slowing training
- 1000 steps ≈ 1/100 of total training (standard ratio)
- Provides stability without excessive computation
- Aligns with checkpoint frequency (20k steps)

---

## 4. Training Strategy

### Phase-Based Approach

**Phase 1: Setup (00:00-00:15)**
- Create environments
- Initialize network
- Verify device detection
- Confirm model saving

**Phase 2: Training (00:15-00:45)**
- Primary training loop: 100,000 timesteps
- Checkpoints every 20,000 steps
- Evaluation every 10,000 steps
- Progress tracking and monitoring

**Phase 3: Evaluation & Documentation (00:45-01:00)**
- Run final 10-episode evaluation
- Compute statistics
- Save results to JSON
- Complete documentation

### Callbacks Strategy

**CheckpointCallback:**
- Save every 20,000 timesteps (5 checkpoints total)
- Allows recovery if training interrupted
- Permits comparison of performance over time

**EvalCallback:**
- Evaluate every 10,000 timesteps (10 evaluations)
- Track performance improvement
- Save best model automatically
- Deterministic evaluation (no randomness)

---

## 5. Code Quality Decisions

### Configuration Management

**Decision:** Use dataclass for TrainingConfig

**Benefits:**
- Type-safe configuration
- Easy serialization
- Defaults with post-init customization
- Self-documenting code

### Function Decomposition

**Setup functions:**
- `setup_directories()` - Creates file structure
- `create_environment()` - Initializes RL environments
- `evaluate_agent()` - Runs evaluation episodes
- `save_results()` - Persists results to JSON

**Rationale:** Modular design enables testing, reuse, and clarity

### Error Handling

**Decisions:**
- Try-except around main training loop
- Try-except on environment import
- Explicit path checking for sandbox
- Clear error messages for debugging

### Documentation Standards

**Applied Standards:**
- Docstrings on all functions (args, returns)
- Inline comments for algorithmic decisions
- Variable naming conventions (underscores, clear intent)
- Code organization (constants, functions, main)

---

## 6. Device Management

### Decision: Auto-detect CUDA availability

**Implementation:**
```python
device = 'cuda' if torch.cuda.is_available() else 'cpu'
```

**Rationale:**
- Training on GPU much faster (4-8x speedup)
- CPU fallback ensures compatibility
- Training achievable on either device
- No user intervention needed

---

## 7. Evaluation Methodology

### Decision: 10-episode deterministic evaluation

**Justification:**
- 10 episodes provides adequate statistics
- Deterministic evaluation (greedy actions) measures true performance
- Avoids randomness in action selection during evaluation
- Captures mean, std, max, min scores

### Metric Tracking

**Captured Metrics:**
- Individual episode scores
- Mean score and standard deviation
- Maximum and minimum scores
- Total episodes evaluated

**Why These?**
- Mean score = average performance
- Std dev = consistency/variance
- Max = best possible outcome
- Min = worst case performance

---

## 8. Risk Mitigation

### Identified Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Training too slow | Pre-calculated 100k timesteps fits ~40 min |
| Poor initial learning | High initial ε (1.0) ensures exploration |
| Unstable training | DQN's stability; target network updates |
| GPU not available | CPU fallback (slower but works) |
| Import errors | Explicit path handling; error messages |
| Model not saving | Multiple save points (checkpoints + final) |
| Time running out | Modular design; can save at any checkpoint |

---

## 9. Reproducibility & Tracking

### Decisions for Reproducibility

1. **Deterministic Actions:** Use `deterministic=True` during evaluation
2. **Saved Configuration:** All hyperparameters in dqn_config.json
3. **Model Checkpointing:** Every 20k steps allows replay
4. **Results Logging:** JSON format with full configuration + metrics
5. **Code Documentation:** All design choices documented here

---

## 10. Success Criteria Alignment

This architecture is designed to achieve:

| Criterion | Design Choice | Expected Result |
|-----------|---------------|-----------------|
| **High Score** | Proven DQN algorithm | Score > 50 (target) |
| **Code Quality** | Modular, documented code | DEIA standards met |
| **Fast Training** | 100k timesteps in 40 min | Completes in time |
| **Reproducibility** | Config-driven, logged results | Can reproduce results |
| **Professional Standards** | Error handling, documentation | Hive-ready submission |

---

**Architecture Summary:**
This is a conservative, proven approach optimized for the 1-hour time constraint. DQN provides stable learning, the 128-64 network is established as effective, and the 100k timestep budget is achievable. All design choices prioritize reliability and completion over experimental risk.

---

**Bot A - Design Document**
**2025-10-27 | DEIA Compliant**
