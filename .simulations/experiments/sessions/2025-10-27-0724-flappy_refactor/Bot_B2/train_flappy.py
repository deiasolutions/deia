"""
Flappy Bird Training Script for Bot_B2
Uses PPO algorithm with optimized hyperparameters
"""

import sys
import os

# Add environment path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flappy_bird_refactored', 'environment'))

from flappy_env import FlappyBirdEnv
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

# Create environment
print("Initializing Bot_B2 Flappy Bird Environment...")
env = FlappyBirdEnv(render_mode='rgb_array', max_episode_steps=500)

# Train agent (500,000 steps = ~2 hours)
print("\n" + "="*60)
print("Training PPO agent... this will take 1-2 hours")
print("="*60)
print("Environment configured with:")
print("  - Small survival reward: 0.1")
print("  - Balanced pipe reward: 20")
print("  - Fair death penalty: -50")
print("  - Proximity bonus: 0.5")
print("  - Total training steps: 500,000")
print("="*60 + "\n")

model = PPO('MlpPolicy', env, verbose=1, learning_rate=3e-4)
model.learn(total_timesteps=500000)

# Save model
model.save('flappy_ppo_trained')
print("\n✓ Model saved as 'flappy_ppo_trained.zip'")

# Evaluate
print("\nEvaluating trained model on 20 episodes...")
mean_reward, std = evaluate_policy(model, env, n_eval_episodes=20)
print(f"Mean Reward: {mean_reward:.2f} ± {std:.2f}")

env.close()

print("\n" + "="*60)
print("Training Complete!")
print("="*60)
