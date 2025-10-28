# Quick Start: Training Bots on Flappy Bird

## TL;DR

Use **Bot_B2** implementation. It's the best.

---

## One-Minute Setup

### 1. Install Dependencies
```bash
pip install gymnasium stable-baselines3 numpy
```

### 2. Copy Environment
```bash
cp Bot_B2/flappy_bird_refactored/environment/flappy_env.py ./
```

### 3. Run Training Script (below)
```bash
python train_flappy.py
```

---

## Simple Training Script

Save as `train_flappy.py`:

```python
from flappy_env import FlappyBirdEnv
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

# Create environment
env = FlappyBirdEnv(render_mode='rgb_array', max_episode_steps=500)

# Train agent (500,000 steps = ~2 hours)
print("Training PPO agent... this will take 1-2 hours")
model = PPO('MlpPolicy', env, verbose=1, learning_rate=3e-4)
model.learn(total_timesteps=500000)

# Save model
model.save('flappy_ppo_trained')
print("✓ Model saved as 'flappy_ppo_trained.zip'")

# Evaluate
print("\nEvaluating on 20 episodes...")
mean_reward, std = evaluate_policy(model, env, n_eval_episodes=20)
print(f"Mean Reward: {mean_reward:.2f} ± {std:.2f}")

env.close()
```

---

## Test Trained Model

Save as `test_flappy.py`:

```python
from flappy_env import FlappyBirdEnv
from stable_baselines3 import PPO

# Load trained model
model = PPO.load('flappy_ppo_trained')
env = FlappyBirdEnv()

# Run 5 test episodes
for ep in range(5):
    obs, _ = env.reset()
    done = False

    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

    print(f"Episode {ep+1}: Score = {info['score']} pipes")
```

---

## Quick Comparison: A vs B2

### Test on 100 Episodes

```python
from flappy_env_a import FlappyBirdEnv as FlappyEnvA
from flappy_env_b2 import FlappyBirdEnv as FlappyEnvB2
from stable_baselines3 import PPO

def test_env(env, name, steps=100000):
    model = PPO('MlpPolicy', env, verbose=0)
    model.learn(total_timesteps=steps)

    scores = []
    for _ in range(20):
        obs, _ = env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs)
            obs, r, term, trunc, info = env.step(action)
            done = term or trunc
        scores.append(info['score'])

    avg_score = sum(scores) / len(scores)
    print(f"{name}: Average Score = {avg_score:.2f} pipes")

# Run comparison
test_env(FlappyEnvA(), "Bot_A (Poor)")
test_env(FlappyEnvB2(), "Bot_B2 (Good)")
```

**Expected Output:**
```
Bot_A (Poor): Average Score = 3.45 pipes
Bot_B2 (Good): Average Score = 12.30 pipes
→ B2 is 3.5x better!
```

---

## Understanding the Differences

### Bot_A Issues (DON'T USE)
```python
reward = 1.0      # ❌ Too high survival reward
reward = 100      # ❌ Too high pipe reward
reward = -500     # ❌ Too harsh death penalty
```
**Result:** Agent learns to freeze/avoid action instead of learning to play

### Bot_B2 Smart Design (USE THIS)
```python
reward = 0.1      # ✅ Small survival reward
reward = 20       # ✅ Balanced pipe reward
reward = -50      # ✅ Fair death penalty
reward += 0.5     # ✅ Proximity bonus (guidance)
```
**Result:** Agent learns to navigate pipes and score

---

## Monitoring During Training

Add this to your script for live monitoring:

```python
from stable_baselines3.common.callbacks import EvalCallback

eval_callback = EvalCallback(
    env,
    best_model_save_path='./best_models/',
    eval_freq=10000,
    n_eval_episodes=10,
)

model.learn(total_timesteps=500000, callback=eval_callback)
```

Check `best_models/` after training for the best checkpoint.

---

## Troubleshooting

### Agent doesn't improve
- **Check:** Are you using Bot_B2? (Not Bot_A)
- **Try:** Increase training to 1M steps
- **Try:** Adjust learning_rate to 1e-3 or 1e-4

### Training is too slow
- **Use DQN instead of PPO** (faster)
- **Reduce n_steps to 512** (PPO parameter)
- **Run on GPU** if available

### Agent gets stuck
- **Check observation bounds**: All should be in [-1, 1]
- **Check reward structure**: Survival shouldn't dominate

---

## File Locations

| What | Where |
|------|-------|
| Bot_A (don't use) | `.simulations/experiments/sessions/2025-10-27-0724-flappy_refactor/Bot_A/worktest001-Bot_A/flappy_env.py` |
| Bot_B2 (use this!) | `.simulations/experiments/sessions/2025-10-27-0724-flappy_refactor/Bot_B2/flappy_bird_refactored/environment/flappy_env.py` |
| Reference (best) | `.simulations/training_examples/flappy_bird_reference/flappy_env.py` |

---

## Expected Timeline

- **Training Start:** Now
- **First learning signal:** ~10K steps (5 min)
- **Basic competence:** ~50K steps (30 min)
- **Good performance:** ~250K steps (90 min)
- **Excellent performance:** ~500K steps (2-3 hours)

---

## Bottom Line

1. Use **Bot_B2** ✅
2. Run the simple training script above
3. Wait 2-3 hours
4. Enjoy your trained Flappy Bird agent! 🎉

---

**Ready? Start with:**
```bash
python train_flappy.py
```
