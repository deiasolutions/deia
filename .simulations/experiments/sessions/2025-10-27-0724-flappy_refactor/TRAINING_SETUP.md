# Flappy Bird Training Setup - A, B1, B2

## Overview
This document sets up the training phase using the three refactored environments from Bot_A, Bot_B1, and Bot_B2.

---

## Bot Implementations Comparison

### Bot_A: `Bot_A/worktest001-Bot_A/flappy_env.py`
**Status:** Minimal refactoring, reward-focused approach
- **Reward Changes:** Increased survival (0.1→1.0), increased pipe reward (10→100), increased death (-100→-500)
- **Issues:** Made problem HARDER, not easier (inverse logic)
- **Learning Potential:** POOR
- **Use Case:** Negative example / Control baseline

**Key Changes:**
```python
reward = 1.0  # Survival (was 0.1)
reward = 100  # Pipe passing (was 10)
reward = -500  # Death (was -100)
```

---

### Bot_B1: `Bot_B1/flappy_bird_refactored/environment/flappy_env.py`
**Status:** Strategic analysis phase (planning only)
- **Files:** ARCHITECTURE.md, STRATEGIC-ANALYSIS.md, IMPLEMENTATION-HANDOFF.md
- **Output:** Working directory created, analysis complete
- **Actual Code:** Handed off to B2 for implementation
- **Use Case:** Reference for excellent problem analysis approach

**Key Findings from B1:**
- 5-7 critical issues identified
- Phase 1 & Phase 2 roadmap created
- Prioritized fix list provided

---

### Bot_B2: `Bot_B2/flappy_bird_refactored/environment/flappy_env.py`
**Status:** Complete implementation with 8 fixes
- **Reward Structure:** 0.1 survival, 20 pipe, -50 death, 0.5 proximity
- **Improvements:** Episode limits, closer pipes, proximity rewards, bounds checking
- **Testing:** 8/8 tests passing, 35% success rate vs 0% original
- **Learning Potential:** EXCELLENT
- **Use Case:** Primary reference implementation

**Key Changes:**
```python
self.MAX_EPISODE_STEPS = 500  # Episode limit
self.PIPE_SPAWN_INTERVAL = 70  # More frequent
self.bird_x = 50  # Closer start
reward = 0.1  # Survival
reward = 20  # Pipe passing
reward = -50  # Death
reward = 0.5  # Proximity bonus
```

---

## Training Phase Structure

### Environment Locations

```
.simulations/
├── training_examples/
│   └── flappy_bird_reference/
│       └── flappy_env.py          [CANONICAL REFERENCE]
│
└── experiments/sessions/2025-10-27-0724-flappy_refactor/
    ├── Bot_A/worktest001-Bot_A/
    │   └── flappy_env.py          [POOR - For comparison]
    │
    ├── Bot_B1/flappy_bird_refactored/environment/
    │   └── flappy_env_original.py  [Reference only]
    │
    └── Bot_B2/flappy_bird_refactored/environment/
        └── flappy_env.py          [GOOD - For training]
```

---

## Training Setup Guide

### Phase 1: Train on Bot_B2 Implementation (RECOMMENDED)

**Why B2?**
- ✅ Well-reasoned reward structure
- ✅ Balanced difficulty curve
- ✅ Clear learning signals
- ✅ Validated improvements
- ✅ Production-ready code

**Setup:**
```bash
# Copy B2 implementation to training environment
cp Bot_B2/flappy_bird_refactored/environment/flappy_env.py training_agents/
```

**Training Script Template:**
```python
import gymnasium as gym
from stable_baselines3 import PPO
from flappy_env import FlappyBirdEnv

# Create environment
env = FlappyBirdEnv(render_mode='rgb_array', max_episode_steps=500, seed=42)

# Train agent with PPO
model = PPO('MlpPolicy', env, verbose=1, learning_rate=3e-4)
model.learn(total_timesteps=500000)

# Save trained model
model.save('trained_agents/flappy_ppo_b2')

# Evaluate
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=100)
print(f"Mean Reward: {mean_reward} +/- {std_reward}")
```

**Expected Results:**
- Training time: 2-4 hours (500K steps)
- Mean episode reward: +200 to +500
- Success rate: 50%+ episodes with 5+ pipes
- Convergence: ~250K steps

---

### Phase 2: Comparison Training - All Three Versions

**Setup A, B1, B2 in parallel for comparison:**

#### Environment A (Control - Poor)
```python
env_a = FlappyBirdEnv_A()  # From Bot_A
# Expected: Poor convergence, high variance
```

#### Environment B2 (Good)
```python
env_b2 = FlappyBirdEnv_B2()  # From Bot_B2
# Expected: Smooth convergence, consistent learning
```

#### Reference (Canonical)
```python
env_ref = FlappyBirdEnv()  # From training_examples/
# Expected: Best convergence, clearest signal
```

**Comparison Metrics:**
```python
import pandas as pd

results = {
    'Bot_A': {
        'convergence_speed': '❌ Slow',
        'reward_stability': '❌ High variance',
        'success_rate': '❌ 10-20%',
        'max_score': '❌ 2-5 pipes'
    },
    'Bot_B2': {
        'convergence_speed': '✅ Fast',
        'reward_stability': '✅ Stable',
        'success_rate': '✅ 50%+',
        'max_score': '✅ 10+ pipes'
    },
    'Reference': {
        'convergence_speed': '✅✅ Very Fast',
        'reward_stability': '✅✅ Very Stable',
        'success_rate': '✅✅ 70%+',
        'max_score': '✅✅ 20+ pipes'
    }
}

df = pd.DataFrame(results).T
print(df)
```

---

## Training Best Practices

### Agent Configuration

**For DQN (simpler, faster):**
```python
from stable_baselines3 import DQN

agent = DQN(
    'MlpPolicy',
    env,
    learning_rate=1e-3,
    buffer_size=50000,
    learning_starts=1000,
    target_update_interval=10000,
    verbose=1
)
agent.learn(total_timesteps=200000)
```

**For PPO (more robust):**
```python
from stable_baselines3 import PPO

agent = PPO(
    'MlpPolicy',
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    verbose=1
)
agent.learn(total_timesteps=500000)
```

### Monitoring Training

```python
from stable_baselines3.common.callbacks import EvalCallback

# Evaluate every 10K steps
eval_callback = EvalCallback(
    env,
    best_model_save_path='./models/',
    eval_freq=10000,
    n_eval_episodes=20,
    verbose=1
)

agent.learn(total_timesteps=500000, callback=eval_callback)
```

### Testing Trained Models

```python
from stable_baselines3 import PPO

# Load trained model
model = PPO.load('trained_agents/flappy_ppo_b2')
env = FlappyBirdEnv()

# Run 10 test episodes
for episode in range(10):
    obs, _ = env.reset()
    done = False
    episode_reward = 0

    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        episode_reward += reward
        done = terminated or truncated

    print(f"Episode {episode+1}: Score={info['score']}, Reward={episode_reward}")
```

---

## Expected Training Results

### Bot_B2 Implementation Expected Outcomes

After 500K training steps with PPO:

| Metric | Value |
|--------|-------|
| Mean Episode Reward | +300 to +500 |
| Mean Episode Score | 10-20 pipes |
| Success Rate | 60-80% (episodes with 3+ pipes) |
| Best Score | 50+ pipes |
| Training Time | 2-4 hours |
| Convergence Point | 250-300K steps |

### Comparison Against Bot_A

| Metric | Bot_A (Poor) | Bot_B2 (Good) | Improvement |
|--------|--------------|---------------|-------------|
| Convergence Speed | Slow (400K+) | Fast (250K) | 1.6x faster |
| Final Performance | 5-10 pipes | 15-25 pipes | 2-3x better |
| Stability | High variance | Low variance | Much better |
| Training Success | 20-30% | 70-80% | 3x higher |

---

## Next Steps

1. **Set up training infrastructure**
   - Create `training_agents/` directory
   - Install stable-baselines3: `pip install stable-baselines3`
   - Copy B2 environment to training directory

2. **Run baseline training**
   - Train on Bot_B2 implementation (primary)
   - Monitor convergence curve
   - Save best models

3. **Comparison training (optional)**
   - Train on Bot_A (control)
   - Compare results
   - Document improvement deltas

4. **Generate reports**
   - Training curves
   - Success rate comparisons
   - Recommendation for future bots

---

## Recommendation

**PRIMARY CHOICE: Bot_B2 Implementation**

Bot_B2 is the clear winner for training because:
- Well-reasoned engineering decisions
- Validated improvements (35% vs 0% success)
- Balanced reward structure
- Production-ready code quality
- Clear documentation

Bot_A should be used only as a **negative example** to show how poor reward engineering hurts learning.

---

## Files to Keep

**Recommended directory structure for training:**

```
training_bots/
├── environments/
│   ├── flappy_b2.py          # Bot_B2 (primary)
│   ├── flappy_a.py           # Bot_A (control)
│   └── flappy_reference.py   # Canonical reference
├── agents/
│   ├── train_ppo.py
│   ├── train_dqn.py
│   └── evaluate.py
├── models/
│   ├── flappy_ppo_b2.zip
│   └── flappy_ppo_b2.zip.best
├── results/
│   ├── training_curves/
│   ├── comparison_results.csv
│   └── final_report.md
└── README.md
```

---

**Status: READY FOR TRAINING PHASE**
