"""
PPO Training Script for Flappy Bird AI Agent

Architecture: Bot B1 (Lead)
Implementation: Bot B2 (Support)
Date: 2025-10-27
Method: Proximal Policy Optimization (PPO)

This script implements the PPO training loop as designed in ARCHITECTURE.md.
B2: Follow the implementation checklist and complete each section marked [B2 IMPLEMENT].
"""

import os
import sys
import csv
import yaml
import numpy as np
from pathlib import Path
from datetime import datetime

# Add base project to path
# From: .simulations/experiments/sessions/2025-10-27-0724-llm_challenge/Bot_B/worktest002-Bot_B/training/train_ppo.py
# To: deiasolutions/.sandbox/flappy-bird-ai/
# Navigate up: training(1) -> worktest002-Bot_B(2) -> Bot_B(3) -> session(4) -> sessions(5) -> experiments(6) -> .simulations(7) -> deiasolutions(8)
# Then go to .sandbox
BASE_PROJECT = Path(__file__).parent.parent.parent.parent.parent.parent.parent.parent / ".sandbox" / "flappy-bird-ai"
sys.path.insert(0, str(BASE_PROJECT))

try:
    import gymnasium as gym
    from stable_baselines3 import PPO
    from stable_baselines3.common.callbacks import CheckpointCallback
    print("[OK] All dependencies loaded successfully")
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    print("Ensure: pip install gymnasium stable-baselines3 torch")
    sys.exit(1)

# Configuration paths
CONFIG_FILE = Path(__file__).parent / "config.yaml"
RESULTS_DIR = Path(__file__).parent.parent / "results"
MODELS_DIR = Path(__file__).parent.parent / "models"

# Ensure directories exist
RESULTS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)


def load_config():
    """Load PPO configuration from YAML file."""
    # [B2 IMPLEMENT]: Load config.yaml if it exists, otherwise use defaults
    default_config = {
        'learning_rate': 0.0003,
        'n_steps': 2048,
        'batch_size': 64,
        'n_epochs': 10,
        'gamma': 0.99,
        'gae_lambda': 0.95,
        'clip_range': 0.2,
        'vf_coef': 0.5,
        'ent_coef': 0.01,
    }

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = yaml.safe_load(f)
                print(f"[OK] Config loaded from {CONFIG_FILE}")
                return config
        except Exception as e:
            print(f"[WARN] Failed to load config: {e}, using defaults")

    print("[OK] Using default PPO configuration")
    return default_config


def create_environment():
    """
    Create Flappy Bird Gymnasium environment.
    [B2 IMPLEMENT]: Import and initialize the environment from base project
    """
    try:
        # [B2 IMPLEMENT]: Import FlappyBirdEnv from base project
        import sys
        import importlib.util

        env_path = BASE_PROJECT / "environment" / "flappy_env.py"
        spec = importlib.util.spec_from_file_location("flappy_env", env_path)
        flappy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(flappy_module)

        FlappyBirdEnv = flappy_module.FlappyBirdEnv

        # Create environment instance
        env = FlappyBirdEnv(render_mode=None)

        print(f"[OK] Flappy Bird environment created successfully")
        print(f"   Action space: {env.action_space}")
        print(f"   Observation space: {env.observation_space}")
        print(f"   Observation shape: {env.observation_space.shape}")

        return env

    except Exception as e:
        print(f"[ERROR] Failed to create environment: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_ppo_model(env, config):
    """
    Create PPO model with architecture from ARCHITECTURE.md.
    IMPROVED: Larger network for better learning (was 64-64)
    """
    try:
        # IMPROVED: Deeper network for better feature learning
        policy_kwargs = dict(
            net_arch=dict(pi=[128, 128, 128], vf=[128, 128, 128])
        )

        model = PPO(
            "MlpPolicy",  # Multi-layer perceptron policy
            env,
            policy_kwargs=policy_kwargs,  # IMPROVED: 3-layer (128-128-128) network
            learning_rate=config['learning_rate'],
            n_steps=config['n_steps'],
            batch_size=config['batch_size'],
            n_epochs=config['n_epochs'],
            gamma=config['gamma'],
            gae_lambda=config['gae_lambda'],
            clip_range=config['clip_range'],
            vf_coef=config['vf_coef'],
            ent_coef=config['ent_coef'],
            tensorboard_log=str(RESULTS_DIR / "tensorboard"),
            verbose=0  # Set to 0 to avoid emoji encoding issues on Windows
        )
        print("[OK] PPO model created with improved 3-layer (128-128-128) architecture")
        return model
    except Exception as e:
        print(f"[ERROR] Failed to create PPO model: {e}")
        return None


def train_agent(model, env, total_timesteps=500000, checkpoint_interval=50000):
    """
    Train PPO agent with checkpointing.
    [B2 IMPLEMENT]: Run training loop with progress monitoring
    """
    try:
        # Setup checkpointing callback
        checkpoint_callback = CheckpointCallback(
            save_freq=checkpoint_interval,
            save_path=str(MODELS_DIR),
            name_prefix="ppo_flappy_checkpoint"
        )

        print(f"\n[TRAIN] Starting PPO training (total_timesteps={total_timesteps})")
        print(f"   Saving checkpoints every {checkpoint_interval} steps")
        print(f"   Checkpoints saved to: {MODELS_DIR}")

        # Train
        model.learn(
            total_timesteps=total_timesteps,
            callback=checkpoint_callback,
            log_interval=1
        )

        print("\n[OK] Training complete!")
        return model

    except Exception as e:
        print(f"[ERROR] Training failed: {e}")
        return None


def save_model(model, name="ppo_flappy_final"):
    """Save trained model to disk."""
    try:
        path = MODELS_DIR / name
        model.save(str(path))
        print(f"[OK] Model saved to: {path}.zip")
        return path
    except Exception as e:
        print(f"[ERROR] Failed to save model: {e}")
        return None


def evaluate_agent(model, env, n_episodes=10):
    """
    Evaluate trained agent.
    [B2 IMPLEMENT]: Run evaluation episodes and collect scores
    """
    scores = []

    try:
        print(f"\n[EVAL] Evaluating agent on {n_episodes} episodes...")

        for episode in range(n_episodes):
            obs, info = env.reset()
            done = False
            episode_score = 0

            while not done:
                action, _states = model.predict(obs, deterministic=True)
                obs, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
                episode_score += reward

            scores.append(episode_score)
            print(f"  Episode {episode+1}/{n_episodes}: Score = {episode_score:.1f}")

        avg_score = np.mean(scores)
        std_score = np.std(scores)
        max_score = np.max(scores)

        print(f"\n[RESULTS] Evaluation Results:")
        print(f"   Best Score: {max_score:.1f}")
        print(f"   Average Score: {avg_score:.1f} +/- {std_score:.1f}")

        return {
            'scores': scores,
            'average': avg_score,
            'std': std_score,
            'max': max_score
        }

    except Exception as e:
        print(f"[ERROR] Evaluation failed: {e}")
        return None


def save_results(eval_results, training_time):
    """Save evaluation results to CSV."""
    try:
        results_file = RESULTS_DIR / "scores.csv"

        with open(results_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Timestamp', datetime.now().isoformat()])
            writer.writerow(['Average Score', eval_results['average']])
            writer.writerow(['Max Score', eval_results['max']])
            writer.writerow(['Std Dev', eval_results['std']])
            writer.writerow(['Training Time (min)', training_time / 60])
            writer.writerow(['Method', 'PPO'])
            writer.writerow(['Episodes', len(eval_results['scores'])])
            writer.writerow(['Individual Scores', ''])
            for i, score in enumerate(eval_results['scores']):
                writer.writerow([f'Episode {i+1}', score])

        print(f"[OK] Results saved to: {results_file}")
        return results_file

    except Exception as e:
        print(f"[ERROR] Failed to save results: {e}")
        return None


def main():
    """Main training orchestration."""
    start_time = datetime.now()

    print("=" * 60)
    print("Bot B - Flappy Bird PPO Training")
    print("=" * 60)

    # Step 1: Load configuration
    print("\n[1/6] Loading configuration...")
    config = load_config()
    print(f"[OK] Config: lr={config['learning_rate']}, gamma={config['gamma']}")

    # Step 2: Create environment
    print("\n[2/6] Creating environment...")
    env = create_environment()
    if env is None:
        print("[ERROR] Environment creation failed. B2 needs to implement this.")
        return False

    # Step 3: Create PPO model
    print("\n[3/6] Creating PPO model...")
    model = create_ppo_model(env, config)
    if model is None:
        print("[ERROR] Model creation failed.")
        return False

    # Step 4: Train agent
    print("\n[4/6] Training agent...")
    model = train_agent(
        model,
        env,
        total_timesteps=500000,
        checkpoint_interval=50000
    )
    if model is None:
        print("[ERROR] Training failed.")
        return False

    # Step 5: Save model
    print("\n[5/6] Saving model...")
    model_path = save_model(model)

    # Step 6: Evaluate agent
    print("\n[6/6] Evaluating agent...")
    eval_results = evaluate_agent(model, env, n_episodes=10)
    if eval_results is None:
        print("[ERROR] Evaluation failed.")
        return False

    # Save results
    training_time = (datetime.now() - start_time).total_seconds()
    results_file = save_results(eval_results, training_time)

    # Final summary
    print("\n" + "=" * 60)
    print("[OK] TRAINING COMPLETE")
    print("=" * 60)
    print(f"Best Score: {eval_results['max']:.1f}")
    print(f"Average Score: {eval_results['average']:.1f}")
    print(f"Training Time: {training_time/60:.1f} minutes")
    print(f"Model saved to: {model_path}")
    print(f"Results saved to: {results_file}")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
