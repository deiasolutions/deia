"""
Bot C - Flappy Bird AI Training (1-hour challenge)
PPO-based agent trained for maximum performance in limited time

Strategy:
- Use faster learning rates for quick convergence
- Aggressive training: 100,000 timesteps (feasible in ~45 min on standard hardware)
- Frequent evaluation to monitor progress
- Early stopping if performance plateaus
"""

import sys
import os
import time
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor
from environment.flappy_env import FlappyBirdEnv

print("="*70)
print("BOT C - FLAPPY BIRD AI TRAINING (1-HOUR CHALLENGE)")
print("="*70)
print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Check hardware
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Device: {device}")

# Create output directories
os.makedirs('../models', exist_ok=True)
os.makedirs('../results', exist_ok=True)

# Initialize timing and metrics
start_time = time.time()
training_stats = {
    'start_time': datetime.now().isoformat(),
    'target_timesteps': 100000,
    'checkpoints': []
}

print("\n" + "="*70)
print("ENVIRONMENT SETUP")
print("="*70)

# Create environment with improved reward shaping
env = FlappyBirdEnv()
env = Monitor(env, '../results/train_monitor')

# Evaluation environment
eval_env = FlappyBirdEnv()
eval_env = Monitor(eval_env, '../results/eval_monitor')

print("[OK] Training environment created")
print("[OK] Evaluation environment created")

# Callbacks for checkpointing and evaluation
checkpoint_callback = CheckpointCallback(
    save_freq=20000,  # Save every 20k steps
    save_path='../models/',
    name_prefix='checkpoint',
    save_replay_buffer=False,
    save_vecnormalize=False
)

eval_callback = EvalCallback(
    eval_env,
    best_model_save_path='../models/',
    log_path='../results/',
    eval_freq=10000,  # Evaluate every 10k steps
    n_eval_episodes=5,  # Quick evaluation
    deterministic=True,
    render=False
)

print("\n" + "="*70)
print("AGENT INITIALIZATION")
print("="*70)

# Create PPO agent with optimized hyperparameters for fast convergence
model = PPO(
    'MlpPolicy',
    env,
    learning_rate=5e-4,          # Slightly higher for faster learning
    n_steps=1024,                 # Smaller batch for quicker updates
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    clip_range_vf=None,
    normalize_advantage=True,
    ent_coef=0.01,
    vf_coef=0.5,
    max_grad_norm=0.5,
    policy_kwargs=dict(net_arch=[256, 128]),  # Slightly larger network
    verbose=1,
    device=device,
    tensorboard_log='../results/tensorboard/'
)

print("[OK] PPO agent created")
print(f"  - Network architecture: [256, 128]")
print(f"  - Learning rate: 5e-4")
print(f"  - Batch size: 64")
print(f"  - Device: {device}")

print("\n" + "="*70)
print("TRAINING START")
print("="*70)
print(f"Target: 100,000 timesteps")
print(f"Expected duration: 40-50 minutes")
print(f"Strategy: Fast convergence with frequent checkpoints")
print("="*70 + "\n")

# Train with aggressive timesteps
try:
    model.learn(
        total_timesteps=100000,
        callback=[checkpoint_callback, eval_callback],
        log_interval=100,
        progress_bar=True
    )
    
    training_time = time.time() - start_time
    
    # Save final model
    print("\n" + "="*70)
    print("SAVING FINAL MODEL")
    print("="*70)
    model.save('../models/ppo_final')
    print("[OK] Final model saved: ../models/ppo_final.zip")

    # Final evaluation on 20 episodes
    print("\n" + "="*70)
    print("FINAL EVALUATION")
    print("="*70)
    print("Running 20 test episodes...")

    eval_env = FlappyBirdEnv()
    scores = []

    for i in range(20):
        obs, _ = eval_env.reset()
        done = False
        episode_score = 0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = eval_env.step(action)
            done = terminated or truncated
            episode_score = info['score']

        scores.append(episode_score)
        if (i + 1) % 5 == 0:
            print(f"  Episodes {i-3}-{i+1}: {scores[-5:]}")

    eval_env.close()

    # Calculate statistics
    scores = np.array(scores)
    max_score = np.max(scores)
    mean_score = np.mean(scores)
    std_score = np.std(scores)
    min_score = np.min(scores)

    print("\n" + "="*70)
    print("TRAINING COMPLETE - RESULTS")
    print("="*70)
    print(f"Total training time: {training_time:.1f} seconds ({training_time/60:.1f} minutes)")
    print(f"\nFinal Performance (20 episodes):")
    print(f"  Max Score:   {max_score}")
    print(f"  Mean Score:  {mean_score:.2f}")
    print(f"  Std Dev:     {std_score:.2f}")
    print(f"  Min Score:   {min_score}")
    print(f"  Median:      {np.median(scores):.1f}")

    # Save results to JSON
    results = {
        'training_time_seconds': training_time,
        'total_timesteps': 100000,
        'final_scores': scores.tolist(),
        'max_score': float(max_score),
        'mean_score': float(mean_score),
        'std_score': float(std_score),
        'min_score': float(min_score),
        'median_score': float(np.median(scores)),
        'timestamp': datetime.now().isoformat()
    }

    with open('../results/final_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n[OK] Results saved to: ../results/final_results.json")
    print("[OK] Model saved to: ../models/ppo_final.zip")
    print("="*70)
    
except KeyboardInterrupt:
    print("\n\nTraining interrupted!")
    training_time = time.time() - start_time
    
    print("Saving interrupted model...")
    model.save('../models/ppo_interrupted')
    print(f"Model saved (after {training_time/60:.1f} minutes)")
    
except Exception as e:
    print(f"\n\nError during training: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    env.close()
    eval_env.close()
    print("\nEnvironments closed.")

