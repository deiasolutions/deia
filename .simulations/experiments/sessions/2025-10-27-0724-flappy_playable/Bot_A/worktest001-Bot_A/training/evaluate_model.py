"""
Bot A - Model Evaluation Script
Evaluates trained PPO agent on Flappy Bird

Author: Bot A (Claude)
Date: 2025-10-27
"""

import sys
import json
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from stable_baselines3 import PPO
from flappy_env import FlappyBirdEnv

def evaluate_model(model_path, num_episodes=20):
    """Evaluate a trained model

    Args:
        model_path: Path to saved model (.zip file)
        num_episodes: Number of episodes to evaluate

    Returns:
        Dictionary with evaluation statistics
    """
    print("=" * 70)
    print(f"EVALUATING MODEL: {Path(model_path).name}")
    print("=" * 70)

    # Load model
    print(f"\nLoading model from: {model_path}")
    model = PPO.load(str(model_path))

    # Create evaluation environment
    env = FlappyBirdEnv()

    print(f"Running {num_episodes} evaluation episodes...\n")

    scores = []
    episode_lengths = []

    for episode in range(num_episodes):
        obs, _ = env.reset()
        done = False
        steps = 0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            steps += 1

        score = info['score']
        scores.append(score)
        episode_lengths.append(steps)

        print(f"  Episode {episode + 1:2d}: Score = {score:3d} | Steps = {steps:4d}")

    env.close()

    # Calculate statistics
    results = {
        'algorithm': 'PPO',
        'model_file': Path(model_path).name,
        'num_episodes': num_episodes,
        'scores': scores,
        'episode_lengths': episode_lengths,
        'mean_score': float(np.mean(scores)),
        'std_score': float(np.std(scores)),
        'max_score': int(np.max(scores)),
        'min_score': int(np.min(scores)),
        'mean_episode_length': float(np.mean(episode_lengths)),
        'std_episode_length': float(np.std(episode_lengths)),
        'total_frames': int(np.sum(episode_lengths)),
    }

    print(f"\n{'=' * 70}")
    print(f"EVALUATION RESULTS")
    print(f"{'=' * 70}")
    print(f"Mean Score:           {results['mean_score']:.2f} +/- {results['std_score']:.2f}")
    print(f"Max Score:            {results['max_score']}")
    print(f"Min Score:            {results['min_score']}")
    print(f"Mean Episode Length:  {results['mean_episode_length']:.1f} frames")
    print(f"Total Frames:         {results['total_frames']:,}")

    return results


if __name__ == '__main__':
    # Path to trained model
    model_dir = Path(__file__).parent.parent / 'models'
    model_path = model_dir / 'ppo_trained.zip'

    # Evaluate
    results = evaluate_model(str(model_path), num_episodes=20)

    # Save results
    results_dir = Path(__file__).parent.parent / 'results'
    results_file = results_dir / 'ppo_final_evaluation.json'

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {results_file}")
