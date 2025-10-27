"""
Bot A - Optimized DQN Training for Flappy Bird
Classical Reinforcement Learning Agent (1-hour optimized version)

Approach: Deep Q-Network with value-based learning
- Network: 2-layer MLP (128, 64 units)
- Training: 100,000 timesteps (~40 minutes)
- Evaluation: 10 episodes with statistics
- Device: Auto-detect (CUDA if available)

Author: Bot A (Claude)
Date: 2025-10-27
"""

import sys
import os
import json
import numpy as np
from pathlib import Path
from dataclasses import dataclass, asdict

import torch
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor

# Adjust path to find the sandbox environment
# Determine correct path based on script location
script_dir = os.path.dirname(os.path.abspath(__file__))
sandbox_path = os.path.abspath(os.path.join(script_dir, "../../../../../../../.sandbox/flappy-bird-ai"))
sys.path.insert(0, sandbox_path)

try:
    from environment.flappy_env import FlappyBirdEnv
except ImportError as e:
    print(f"ERROR: Could not import FlappyBirdEnv from {sandbox_path}")
    print(f"Script directory: {script_dir}")
    print(f"Sandbox path: {sandbox_path}")
    print(f"Exception: {e}")
    print("Make sure the .sandbox/flappy-bird-ai directory exists")
    sys.exit(1)


@dataclass
class TrainingConfig:
    """Configuration for DQN training - optimized for 1-hour execution."""

    # Training hyperparameters
    total_timesteps: int = 100000  # Achievable in ~40 minutes
    learning_rate: float = 1e-3
    buffer_size: int = 100000
    batch_size: int = 64
    gamma: float = 0.99  # Discount factor
    tau: float = 1.0

    # DQN-specific parameters
    learning_starts: int = 1000
    train_freq: int = 4
    gradient_steps: int = 1
    target_update_interval: int = 1000

    # Exploration parameters
    exploration_fraction: float = 0.1
    exploration_initial_eps: float = 1.0
    exploration_final_eps: float = 0.01

    # Network architecture
    network_architecture: list = None  # Will default to [128, 64]

    # Evaluation parameters
    eval_episodes: int = 10
    eval_freq: int = 10000

    # Device
    device: str = None  # Auto-detect if None

    def __post_init__(self):
        """Post-initialization processing."""
        if self.network_architecture is None:
            self.network_architecture = [128, 64]

        if self.device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'


def setup_directories(base_path: str) -> dict:
    """
    Create necessary directories for training.

    Args:
        base_path: Base path for the training workspace

    Returns:
        Dictionary with paths to created directories
    """
    paths = {
        'models': os.path.join(base_path, 'models'),
        'logs': os.path.join(base_path, 'logs'),
        'results': os.path.join(base_path, 'results'),
    }

    for path in paths.values():
        os.makedirs(path, exist_ok=True)

    return paths


def create_environment(env_monitor_path: str) -> tuple:
    """
    Create training environment.

    Args:
        env_monitor_path: Path for environment monitoring

    Returns:
        Tuple of (training_env, eval_env)
    """
    print("Creating environments...")

    train_env = FlappyBirdEnv()
    train_env = Monitor(train_env, os.path.join(env_monitor_path, 'train'))

    eval_env = FlappyBirdEnv()
    eval_env = Monitor(eval_env, os.path.join(env_monitor_path, 'eval'))

    return train_env, eval_env


def evaluate_agent(model, env: FlappyBirdEnv, n_episodes: int = 10) -> dict:
    """
    Evaluate the trained agent.

    Args:
        model: Trained DQN model
        env: Environment for evaluation
        n_episodes: Number of episodes to run

    Returns:
        Dictionary with evaluation statistics
    """
    scores = []

    print(f"\nEvaluating agent ({n_episodes} episodes)...")
    for episode in range(n_episodes):
        obs, _ = env.reset()
        done = False
        episode_score = 0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            episode_score = info.get('score', 0)

        scores.append(episode_score)
        print(f"  Episode {episode + 1:2d}: Score = {episode_score}")

    scores = np.array(scores)

    stats = {
        'n_episodes': n_episodes,
        'mean_score': float(np.mean(scores)),
        'std_score': float(np.std(scores)),
        'max_score': float(np.max(scores)),
        'min_score': float(np.min(scores)),
        'scores': scores.tolist(),
    }

    return stats


def save_results(stats: dict, config: TrainingConfig, output_path: str):
    """
    Save training results to JSON.

    Args:
        stats: Evaluation statistics
        config: Training configuration
        output_path: Path to save results
    """
    results = {
        'training_config': asdict(config),
        'evaluation_stats': stats,
        'timestamp': str(np.datetime64('now')),
    }

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_path}")


def main():
    """Main training routine."""

    print("="*70)
    print("BOT A - FLAPPY BIRD AI AGENT TRAINING")
    print("Classical RL: Deep Q-Network (DQN)")
    print("="*70)

    # Configuration
    config = TrainingConfig()
    print(f"\nDevice: {config.device}")
    print(f"Total timesteps: {config.total_timesteps:,}")
    print(f"Network architecture: {config.network_architecture}")

    # Setup paths
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(base_path)  # Go up one level to worktest001-Bot_A
    paths = setup_directories(base_path)

    print(f"\nWorkspace: {base_path}")
    print(f"Models path: {paths['models']}")
    print(f"Results path: {paths['results']}")

    # Create environments
    train_env, eval_env = create_environment(paths['logs'])

    # Setup callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=20000,
        save_path=paths['models'],
        name_prefix='dqn_checkpoint',
        save_replay_buffer=True,
        save_vecnormalize=True
    )

    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=paths['models'],
        log_path=paths['logs'],
        eval_freq=config.eval_freq,
        n_eval_episodes=5,
        deterministic=True,
        render=False
    )

    # Create DQN agent
    print("\nInitializing DQN agent...")
    model = DQN(
        'MlpPolicy',
        train_env,
        learning_rate=config.learning_rate,
        buffer_size=config.buffer_size,
        learning_starts=config.learning_starts,
        batch_size=config.batch_size,
        tau=config.tau,
        gamma=config.gamma,
        train_freq=config.train_freq,
        gradient_steps=config.gradient_steps,
        target_update_interval=config.target_update_interval,
        exploration_fraction=config.exploration_fraction,
        exploration_initial_eps=config.exploration_initial_eps,
        exploration_final_eps=config.exploration_final_eps,
        policy_kwargs=dict(net_arch=config.network_architecture),
        verbose=1,
        device=config.device,
        tensorboard_log=paths['logs']
    )

    # Training
    print("\n" + "="*70)
    print("STARTING TRAINING")
    print("="*70)
    print(f"Target timesteps: {config.total_timesteps:,}")
    print(f"Estimated time: ~40 minutes")
    print("="*70 + "\n")

    try:
        model.learn(
            total_timesteps=config.total_timesteps,
            callback=[checkpoint_callback, eval_callback],
            log_interval=100,
            progress_bar=True
        )

        # Save final model
        print("\nSaving final model...")
        model.save(os.path.join(paths['models'], 'dqn_final'))
        print(f"Model saved to: {os.path.join(paths['models'], 'dqn_final.zip')}")

        # Evaluation
        print("\n" + "="*70)
        print("TRAINING COMPLETE - EVALUATING")
        print("="*70)

        eval_stats = evaluate_agent(model, eval_env, n_episodes=config.eval_episodes)

        # Print summary
        print("\n" + "="*70)
        print("BOT A - FINAL RESULTS")
        print("="*70)
        print(f"Mean Score:    {eval_stats['mean_score']:.2f} +- {eval_stats['std_score']:.2f}")
        print(f"Max Score:     {eval_stats['max_score']:.1f}")
        print(f"Min Score:     {eval_stats['min_score']:.1f}")
        print("="*70)

        # Save results
        results_file = os.path.join(paths['results'], 'evaluation_results.json')
        save_results(eval_stats, config, results_file)

    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user.")
        print("Saving current model...")
        model.save(os.path.join(paths['models'], 'dqn_interrupted'))
        print("Model saved.")

    finally:
        train_env.close()
        eval_env.close()
        print("\nEnvironments closed. Training session ended.")


if __name__ == '__main__':
    main()
