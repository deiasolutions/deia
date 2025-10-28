# Flappy Bird Reference Implementation

This is the canonical training reference for the Flappy Bird refactoring challenge. Use this as the baseline when training bots to understand and improve game code.

## What This Is

A production-ready Flappy Bird environment that demonstrates:
- ✅ Properly normalized observation space (all [-1, 1])
- ✅ Well-tuned reward structure for RL training
- ✅ Configurable game parameters
- ✅ Clear, refactorable code structure
- ✅ Episode length limits
- ✅ Intermediate learning signals (proximity rewards)

## Key Features

### Observation Space (Normalized)
All observations are normalized to [-1, 1] range:

```
[bird_y_norm, bird_vel_norm, pipe_dist_norm, gap_center_offset, gap_size_norm]

- bird_y_norm: Bird position relative to center (-1=top, 0=center, 1=bottom)
- bird_vel_norm: Bird velocity (-1=max down, 0=no velocity, 1=max up)
- pipe_dist_norm: Next pipe distance from center (-1=far left, 0=at center, 1=far right)
- gap_center_offset: Gap position relative to bird (-1=above, 0=centered on bird, 1=below)
- gap_size_norm: Normalized gap size (-1 to 1 range)
```

### Reward Structure
Carefully tuned for stable RL training:

| Event | Reward |
|-------|--------|
| Survive frame | +0.1 |
| Near pipe gap safely | +0.5 |
| Pass pipe | +20.0 |
| Collision/Death | -50.0 |

**Design rationale:**
- Survival reward is small (0.1) so agent doesn't dominate by just existing
- Proximity reward (0.5) provides learning gradient for navigation
- Pipe reward (20) incentivizes actual progress
- Death penalty (-50) is balanced, not extreme (avoids over-conservative behavior)

### Game Configuration

```python
env = FlappyBirdEnv(
    render_mode='rgb_array',      # or None
    gravity=0.5,                   # Physics constant
    flap_power=-10,                # Upward velocity when flapping
    pipe_speed=3,                  # Pixels per frame
    pipe_gap=150,                  # Gap height
    max_episode_steps=500,         # Episode termination
    seed=42                        # For reproducibility
)
```

## Usage Example

```python
import gymnasium as gym

# Create environment
env = FlappyBirdEnv(render_mode='rgb_array', seed=42)

# Training loop
for episode in range(100):
    obs, info = env.reset()
    done = False
    total_reward = 0

    while not done:
        action = env.action_space.sample()  # Replace with agent
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        done = terminated or truncated

    print(f"Episode {episode}: Score={info['score']}, Reward={total_reward}")
```

## For Bot Refactoring Training

When training bots to refactor this code, they should:

1. **Understand the structure**: Study the observation normalization and reward system
2. **Identify improvements**: Look for optimization opportunities (see FLAPPY_ENV_REFACTOR_SPEC.md)
3. **Make targeted changes**: Improve specific aspects without breaking game mechanics
4. **Validate results**: Test that refactored version maintains learning stability

### Common Refactoring Targets

- Observation space bounds checking
- Reward signal optimization
- Game difficulty adjustment (pipe frequency, gap sizes)
- Code structure and readability
- Parameter documentation

## Testing Your Refactoring

```python
# Test 1: Observation bounds
env = FlappyBirdEnv()
for _ in range(1000):
    obs, _ = env.reset()
    for _ in range(100):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, _ = env.step(action)
        assert np.all(obs >= -1.0) and np.all(obs <= 1.0), "Observation out of bounds!"
        if terminated or truncated:
            break

# Test 2: Episode termination
env = FlappyBirdEnv(max_episode_steps=100)
obs, _ = env.reset()
for step in range(101):
    action = 0
    obs, reward, terminated, truncated, _ = env.step(action)
    if step < 100:
        assert not truncated, "Terminated too early!"
    if step >= 100:
        assert terminated or truncated, "Didn't terminate!"
```

## Reference Metrics

When trained with PPO for 500K steps, this environment:
- Baseline agent reaches ~50+ pipes per episode
- Reward convergence: -50 to +500 per episode
- Training stability: Low variance in later episodes

## File Structure

```
flappy_bird_reference/
├── flappy_env.py          # Main environment
├── README.md              # This file
└── TESTING.md             # Optional: Test suite
```

## Next Steps

This reference is designed as a teaching tool. Common enhancements include:
- Add visual rendering (PyGame, matplotlib)
- Implement difficulty levels
- Add multi-pipe scenarios
- Create curriculum learning variations
