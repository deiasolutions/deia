"""
Bot A - PPO Training Script for Flappy Bird AI
Optimized for 1-hour training window

Algorithm: Proximal Policy Optimization (PPO)
Reason: Stable, sample-efficient policy gradient method
        Well-suited for discrete control tasks
        Proven performance on Flappy Bird
"""

import sys
import os
import json
import time
import numpy as np
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import stable-baselines3
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback

# Import environment
from flappy_env import FlappyBirdEnv

import torch

print("=" * 70)
print("BOT A - FLAPPY BIRD AI TRAINING")
print("Algorithm: Proximal Policy Optimization (PPO)")
print("=" * 70)

# Device detection
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"\nDevice: {device}")

# Create output directories
results_dir = Path(__file__).parent.parent / 'results'
models_dir = Path(__file__).parent.parent / 'models'
logs_dir = Path(__file__).parent.parent / 'logs'

results_dir.mkdir(exist_ok=True)
models_dir.mkdir(exist_ok=True)
logs_dir.mkdir(exist_ok=True)

print(f"Results directory: {results_dir}")
print(f"Models directory: {models_dir}")
print(f"Logs directory: {logs_dir}")


class TrainingProgressCallback(BaseCallback):
    """Custom callback to log training progress"""

    def __init__(self, check_freq=5000):
        super().__init__()
        self.check_freq = check_freq
        self.best_mean_reward = -np.inf

    def _on_step(self) -> bool:
        """Called at each step"""
        if self.n_calls % self.check_freq == 0:
            print(f"  Steps: {self.num_timesteps} | "
                  f"Avg Reward: {self.model.logger.name_to_value.get('train/value_loss', 0):.4f}")
        return True


def train_ppo_agent(total_timesteps=100000):
    """Train PPO agent on Flappy Bird environment

    Args:
        total_timesteps: Number of training timesteps

    Returns:
        Trained model and training info
    """
    print(f"\n{'=' * 70}")
    print(f"TRAINING CONFIGURATION")
    print(f"{'=' * 70}")
    print(f"Total timesteps: {total_timesteps:,}")
    print(f"Expected duration: 10-20 minutes (on CPU)")

    # Create environment with monitoring
    print(f"\nCreating environment...")
    env = FlappyBirdEnv()
    env = Monitor(env, str(logs_dir / 'train'))

    # PPO hyperparameters optimized for fast training
    print(f"\nInitializing PPO agent...")
    model = PPO(
        'MlpPolicy',
        env,
        learning_rate=3e-4,
        n_steps=1024,  # Optimized for faster training
        batch_size=64,
        n_epochs=5,  # Reduced epochs for speed
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,  # Small entropy bonus for exploration
        vf_coef=0.5,
        max_grad_norm=0.5,
        policy_kwargs=dict(
            net_arch=[128, 128],  # 2-layer MLP
            activation_fn=torch.nn.ReLU
        ),
        verbose=0,  # Reduced verbosity
        device=device,
        tensorboard_log=str(logs_dir / 'tensorboard'),
    )

    print(f"\n{'=' * 70}")
    print(f"STARTING TRAINING")
    print(f"{'=' * 70}\n")

    start_time = time.time()

    # Train the model
    try:
        model.learn(
            total_timesteps=total_timesteps,
            callback=TrainingProgressCallback(check_freq=5000),
            log_interval=10,
            progress_bar=True,
            tb_log_name='ppo_training'
        )

        elapsed_time = time.time() - start_time

        # Save final model
        model_path = models_dir / 'ppo_trained'
        model.save(str(model_path))
        print(f"\n✓ Model saved: {model_path}.zip")

        print(f"\n{'=' * 70}")
        print(f"TRAINING COMPLETE!")
        print(f"{'=' * 70}")
        print(f"Training time: {elapsed_time / 60:.1f} minutes")

        return model, env, elapsed_time

    except KeyboardInterrupt:
        print("\n\n⚠ Training interrupted by user")
        model.save(str(models_dir / 'ppo_interrupted'))
        return model, env, time.time() - start_time


def evaluate_agent(model, num_episodes=20):
    """Evaluate trained agent on multiple episodes

    Args:
        model: Trained PPO model
        num_episodes: Number of evaluation episodes

    Returns:
        Dictionary with evaluation results
    """
    print(f"\n{'=' * 70}")
    print(f"EVALUATION PHASE")
    print(f"{'=' * 70}")
    print(f"Running {num_episodes} evaluation episodes...\n")

    eval_env = FlappyBirdEnv()

    scores = []
    episode_lengths = []

    for episode in range(num_episodes):
        obs, _ = eval_env.reset()
        done = False
        steps = 0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = eval_env.step(action)
            done = terminated or truncated
            steps += 1

        score = info['score']
        scores.append(score)
        episode_lengths.append(steps)

        print(f"  Episode {episode + 1:2d}: Score = {score:3d} | Steps = {steps:4d}")

    eval_env.close()

    # Calculate statistics
    results = {
        'scores': scores,
        'episode_lengths': episode_lengths,
        'mean_score': float(np.mean(scores)),
        'std_score': float(np.std(scores)),
        'max_score': int(np.max(scores)),
        'min_score': int(np.min(scores)),
        'mean_episode_length': float(np.mean(episode_lengths)),
    }

    print(f"\n{'=' * 70}")
    print(f"EVALUATION RESULTS")
    print(f"{'=' * 70}")
    print(f"Mean Score: {results['mean_score']:.2f} ± {results['std_score']:.2f}")
    print(f"Max Score:  {results['max_score']}")
    print(f"Min Score:  {results['min_score']}")
    print(f"Avg Episode Length: {results['mean_episode_length']:.1f} frames")

    return results


def save_results(training_time, eval_results):
    """Save all results to JSON file

    Args:
        training_time: Time spent training (seconds)
        eval_results: Evaluation results dictionary
    """
    results_data = {
        'algorithm': 'PPO',
        'training_timesteps': 100000,
        'training_time_seconds': training_time,
        'training_time_minutes': round(training_time / 60, 2),
        'device': device,
        'evaluation': eval_results,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    results_file = results_dir / 'training_results.json'
    with open(results_file, 'w') as f:
        json.dump(results_data, f, indent=2)

    print(f"\n✓ Results saved: {results_file}")

    return results_data


if __name__ == '__main__':
    # Train agent
    model, env, training_time = train_ppo_agent(total_timesteps=100000)
    env.close()

    # Evaluate agent
    eval_results = evaluate_agent(model, num_episodes=20)

    # Save all results
    save_results(training_time, eval_results)

    print(f"\n{'=' * 70}")
    print(f"BOT A - TRAINING SESSION COMPLETE")
    print(f"{'=' * 70}")
    print(f"\nNext steps:")
    print(f"  1. Check results in: {results_dir / 'training_results.json'}")
    print(f"  2. Model saved to: {models_dir / 'ppo_trained.zip'}")
    print(f"  3. File midpoint report at 00:30")
    print(f"  4. Complete documentation")

