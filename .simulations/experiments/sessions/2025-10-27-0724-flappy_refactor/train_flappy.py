#!/usr/bin/env python3
"""
Flappy Bird Training Script
Using Bot_B2's optimized environment for maximum learning efficiency
"""

import sys
from pathlib import Path

# Add Bot_B2 environment to path
bot_b2_env = Path(__file__).parent / "Bot_B2" / "flappy_bird_refactored" / "environment"
sys.path.insert(0, str(bot_b2_env))

from flappy_env import FlappyBirdEnv
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback
import datetime

print("=" * 70)
print("FLAPPY BIRD TRAINING - BOT_B2 OPTIMIZED ENVIRONMENT")
print("=" * 70)
print()

# Setup paths
output_dir = Path(__file__).parent / "training_output"
output_dir.mkdir(exist_ok=True)

model_path = output_dir / "flappy_ppo_trained"
best_model_path = output_dir / "best_models"
best_model_path.mkdir(exist_ok=True)

print(f"Output directory: {output_dir}")
print(f"Model will be saved to: {model_path}")
print()

# Create environment
print("[1/5] Creating environment...")
env = FlappyBirdEnv(render_mode='rgb_array', max_episode_steps=500)
print("[OK] Environment created")
print(f"  - Observation space: {env.observation_space}")
print(f"  - Action space: {env.action_space}")
print()

# Setup evaluation callback
eval_callback = EvalCallback(
    env,
    best_model_save_path=str(best_model_path),
    eval_freq=10000,
    n_eval_episodes=10,
    verbose=1
)

# Train agent
print("[2/5] Training PPO agent...")
print("      (This will take 1-2 hours for 500K steps)")
print()

start_time = datetime.datetime.now()
model = PPO(
    'MlpPolicy',
    env,
    verbose=1,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.01
)

model.learn(
    total_timesteps=500000,
    callback=eval_callback,
    log_interval=10
)

end_time = datetime.datetime.now()
training_time = end_time - start_time

print()
print(f"[OK] Training completed in {training_time}")
print()

# Save model
print("[3/5] Saving model...")
model.save(str(model_path))
print(f"[OK] Model saved to {model_path}.zip")
print()

# Evaluate
print("[4/5] Evaluating agent on 20 episodes...")
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=20, deterministic=True)
print(f"[OK] Evaluation complete")
print(f"  - Mean Reward: {mean_reward:.2f} +/- {std_reward:.2f}")
print()

# Test a few episodes with rendering disabled
print("[5/5] Running test episodes...")
test_episodes = 5
test_scores = []

for episode in range(test_episodes):
    obs, _ = env.reset()
    done = False
    score = 0

    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        score = info.get('score', 0)

    test_scores.append(score)
    print(f"  Episode {episode+1}: {score} pipes")

avg_test_score = sum(test_scores) / len(test_scores)
print(f"[OK] Test complete - Average: {avg_test_score:.1f} pipes")
print()

# Summary
print("=" * 70)
print("TRAINING SUMMARY")
print("=" * 70)
print(f"Training time: {training_time}")
print(f"Total timesteps: 500,000")
print(f"Mean reward (evaluation): {mean_reward:.2f}")
print(f"Test episodes average: {avg_test_score:.1f} pipes")
print(f"Best model saved to: {best_model_path / 'best_model.zip'}")
print(f"Final model saved to: {model_path}.zip")
print()
print("[OK] Training complete!")
print()

env.close()
