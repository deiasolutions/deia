# """Train a DQN agent on the Flappy Bird environment for the Bot C session."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import List

import numpy as np
import torch
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CallbackList, CheckpointCallback, EvalCallback
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_ROOT = PROJECT_ROOT / "environment"

if str(PROJECT_ROOT) not in os.sys.path:
    os.sys.path.append(str(PROJECT_ROOT))

from environment.flappy_env import FlappyBirdEnv  # type: ignore  # noqa: E402


def build_env(log_dir: Path) -> Monitor:
    """Create a monitored Flappy Bird environment instance."""
    env = FlappyBirdEnv()
    log_dir.mkdir(parents=True, exist_ok=True)
    return Monitor(env, str(log_dir))


def configure_callbacks(models_dir: Path, eval_log_dir: Path, eval_env: Monitor) -> CallbackList:
    """Set up checkpointing and evaluation callbacks tailored to the session time limit."""
    checkpoint_cb = CheckpointCallback(
        save_freq=20_000,
        save_path=str(models_dir),
        name_prefix="dqn_checkpoint",
        save_replay_buffer=True,
        save_vecnormalize=True,
    )

    eval_cb = EvalCallback(
        eval_env,
        best_model_save_path=str(models_dir),
        log_path=str(eval_log_dir),
        eval_freq=10_000,
        n_eval_episodes=5,
        deterministic=True,
        render=False,
    )

    return CallbackList([checkpoint_cb, eval_cb])


def train(total_timesteps: int, seed: int, resume: bool) -> Path:
    """Train the DQN agent and return the path to the saved best model."""
    models_dir = PROJECT_ROOT / "models" / "dqn_session"
    logs_dir = PROJECT_ROOT / "results" / "logs" / "dqn_session"
    tensorboard_dir = PROJECT_ROOT / "results" / "tensorboard"

    models_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    tensorboard_dir.mkdir(parents=True, exist_ok=True)

    train_env = build_env(logs_dir / "train")
    eval_env = build_env(logs_dir / "eval")

    callbacks = configure_callbacks(models_dir, logs_dir, eval_env)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    best_model_file = models_dir / "best_model.zip"

    if resume and best_model_file.exists():
        model = DQN.load(
            best_model_file,
            env=train_env,
            device=device,
        )
        # Ensure consistent exploration scheduling when resuming
        model.exploration_schedule.initial_p = 1.0
        model.exploration_schedule.final_p = 0.02
    else:
        model = DQN(
            "MlpPolicy",
            train_env,
            learning_rate=2.5e-4,
            buffer_size=50_000,
            learning_starts=1_000,
            batch_size=128,
            tau=1.0,
            gamma=0.99,
            train_freq=4,
            gradient_steps=1,
            target_update_interval=2_000,
            exploration_fraction=0.3,
            exploration_initial_eps=1.0,
            exploration_final_eps=0.02,
            policy_kwargs=dict(net_arch=[256, 256]),
            verbose=1,
            tensorboard_log=str(tensorboard_dir),
            device=device,
            seed=seed,
        )

    model.learn(
        total_timesteps=total_timesteps,
        callback=callbacks,
        log_interval=100,
        progress_bar=True,
        reset_num_timesteps=not resume,
    )

    best_model_path = models_dir / "best_model"
    model.save(best_model_path)

    return best_model_path.with_suffix(".zip")


def evaluate(model_path: Path, episodes: int, eval_seed: int) -> List[int]:
    """Evaluate the trained model for a fixed number of episodes."""
    env = build_env(PROJECT_ROOT / "results" / "logs" / "dqn_session" / "evaluation")
    env.reset(seed=eval_seed)
    model = DQN.load(model_path)

    scores: List[int] = []
    for _ in range(episodes):
        obs, _ = env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
        scores.append(int(info.get("score", 0)))

    env.close()
    return scores


def evaluate_with_sb3(model_path: Path, episodes: int) -> tuple[float, float]:
    """Alternative evaluation using SB3 helper to capture reward statistics."""
    env = build_env(PROJECT_ROOT / "results" / "logs" / "dqn_session" / "evaluation_helper")
    model = DQN.load(model_path)
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=episodes, deterministic=True)
    env.close()
    return mean_reward, std_reward


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a DQN Flappy Bird agent (Bot C session run).")
    parser.add_argument("--timesteps", type=int, default=120_000, help="Total training timesteps.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument("--eval-episodes", type=int, default=10, help="Episodes for post-training evaluation.")
    parser.add_argument(
        "--resume",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Resume training from existing best_model if present.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("=" * 70)
    print("Bot C – Flappy Bird DQN Training Session")
    print("=" * 70)
    print(f"Total timesteps: {args.timesteps}")
    print(f"Using device: {'cuda' if torch.cuda.is_available() else 'cpu'}")
    print(f"Seed: {args.seed}")
    print("=" * 70)

    best_model_path = train(total_timesteps=args.timesteps, seed=args.seed, resume=args.resume)
    print(f"\nTraining complete. Best model saved to: {best_model_path}")

    scores = evaluate(best_model_path, episodes=args.eval_episodes, eval_seed=args.seed + 1)
    mean_score = float(np.mean(scores))
    std_score = float(np.std(scores))
    max_score = int(np.max(scores))
    min_score = int(np.min(scores))

    print("\nEvaluation Summary (deterministic policy)")
    print("-" * 50)
    print(f"Episodes evaluated: {args.eval_episodes}")
    print(f"Scores: {scores}")
    print(f"Mean score: {mean_score:.2f} ± {std_score:.2f}")
    print(f"Max score: {max_score}")
    print(f"Min score: {min_score}")

    mean_reward, std_reward = evaluate_with_sb3(best_model_path, episodes=args.eval_episodes)
    print("\nReward Summary (SB3 evaluate_policy)")
    print("-" * 50)
    print(f"Mean reward: {mean_reward:.2f} ± {std_reward:.2f}")


if __name__ == "__main__":
    main()
