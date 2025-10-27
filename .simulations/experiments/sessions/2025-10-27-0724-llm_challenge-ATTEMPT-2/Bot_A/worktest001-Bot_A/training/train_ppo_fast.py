"""
Bot A - Fast PPO Training for Flappy Bird
Policy Gradient Method (faster convergence than DQN)

Author: Bot A (Claude)
Date: 2025-10-27
"""

import sys
import os
import json
import numpy as np

import torch
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor

# Adjust path to find the sandbox environment
script_dir = os.path.dirname(os.path.abspath(__file__))
sandbox_path = os.path.abspath(os.path.join(script_dir, "../../../../../../../.sandbox/flappy-bird-ai"))
sys.path.insert(0, sandbox_path)

try:
    from environment.flappy_env import FlappyBirdEnv
except ImportError as e:
    print(f"ERROR: Could not import FlappyBirdEnv")
    print(f"Exception: {e}")
    sys.exit(1)

print("="*70)
print("BOT A - FLAPPY BIRD AI AGENT TRAINING - PPO")
print("Policy Gradient Method: PPO (Faster learning)")
print("="*70)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"\nDevice: {device}")

base_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(base_path)

paths = {
    'models': os.path.join(base_path, 'models'),
    'logs': os.path.join(base_path, 'logs'),
    'results': os.path.join(base_path, 'results'),
}

for path in paths.values():
    os.makedirs(path, exist_ok=True)

# Create environment
print("Creating environments...")
train_env = FlappyBirdEnv()
train_env = Monitor(train_env, os.path.join(paths['logs'], 'train_ppo'))

eval_env = FlappyBirdEnv()
eval_env = Monitor(eval_env, os.path.join(paths['logs'], 'eval_ppo'))

# Callbacks
checkpoint_callback = CheckpointCallback(
    save_freq=20000,
    save_path=paths['models'],
    name_prefix='ppo_checkpoint',
    save_replay_buffer=True,
    save_vecnormalize=True
)

eval_callback = EvalCallback(
    eval_env,
    best_model_save_path=paths['models'],
    log_path=paths['logs'],
    eval_freq=10000,
    n_eval_episodes=5,
    deterministic=True,
    render=False
)

# PPO - Better for this problem
print("\nInitializing PPO agent...")
model = PPO(
    'MlpPolicy',
    train_env,
    learning_rate=3e-4,
    n_steps=2048,  # Collect 2048 steps before updating
    batch_size=256,  # Process in batches
    n_epochs=10,  # Update epochs
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    policy_kwargs=dict(net_arch=[256, 256]),  # Larger network for PPO
    verbose=1,
    device=device,
    tensorboard_log=paths['logs']
)

print("\n" + "="*70)
print("STARTING PPO TRAINING")
print("="*70)
print(f"Target timesteps: 100,000")
print(f"Expected time: ~40 minutes")
print("="*70 + "\n")

try:
    model.learn(
        total_timesteps=100000,
        callback=[checkpoint_callback, eval_callback],
        log_interval=100,
        progress_bar=True
    )

    # Save final model
    print("\nSaving final model...")
    model.save(os.path.join(paths['models'], 'ppo_final'))
    print(f"Model saved to: {os.path.join(paths['models'], 'ppo_final.zip')}")

    # Evaluation
    print("\n" + "="*70)
    print("TRAINING COMPLETE - EVALUATING")
    print("="*70)

    scores = []
    print("Evaluating agent (10 episodes)...")
    for episode in range(10):
        obs, _ = eval_env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = eval_env.step(action)
            done = terminated or truncated
            episode_score = info.get('score', 0)
        scores.append(episode_score)
        print(f"  Episode {episode + 1:2d}: Score = {episode_score}")

    scores = np.array(scores)
    stats = {
        'n_episodes': 10,
        'mean_score': float(np.mean(scores)),
        'std_score': float(np.std(scores)),
        'max_score': float(np.max(scores)),
        'min_score': float(np.min(scores)),
        'scores': scores.tolist(),
    }

    # Print summary
    print("\n" + "="*70)
    print("BOT A - FINAL RESULTS (PPO)")
    print("="*70)
    print(f"Mean Score:    {stats['mean_score']:.2f} +- {stats['std_score']:.2f}")
    print(f"Max Score:     {stats['max_score']:.1f}")
    print(f"Min Score:     {stats['min_score']:.1f}")
    print("="*70)

    # Save results
    results_file = os.path.join(paths['results'], 'ppo_evaluation_results.json')
    results = {
        'algorithm': 'PPO',
        'training_config': {
            'total_timesteps': 100000,
            'n_steps': 2048,
            'batch_size': 256,
            'n_epochs': 10,
            'learning_rate': 3e-4,
            'gamma': 0.99,
            'gae_lambda': 0.95,
            'clip_range': 0.2,
            'network_architecture': [256, 256],
        },
        'evaluation_stats': stats,
        'timestamp': str(np.datetime64('now')),
    }

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {results_file}")

except KeyboardInterrupt:
    print("\n\nTraining interrupted by user.")
    print("Saving current model...")
    model.save(os.path.join(paths['models'], 'ppo_interrupted'))

finally:
    train_env.close()
    eval_env.close()
    print("\nEnvironments closed. Training session ended.")
