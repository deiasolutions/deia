#!/usr/bin/env python3
"""
Evaluation and Continuation Script for NEAT Trainer
Bot B2 Phase 3 - Extended Training
"""

import os
import sys
from pathlib import Path
import pickle
import numpy as np

# Add sandbox to path
script_dir = Path(__file__).resolve().parent
worktest_dir = script_dir.parent
bot_b_dir = worktest_dir.parent
attempt_dir = bot_b_dir.parent
sessions_dir = attempt_dir.parent
experiments_dir = sessions_dir.parent
simulations_dir = experiments_dir.parent
repo_root = simulations_dir.parent

sandbox_path = repo_root / ".sandbox" / "flappy-bird-ai"
sys.path.insert(0, str(sandbox_path))

import neat
import numpy as np
from environment.flappy_env import FlappyBirdEnv


def evaluate_genome(genome, config, env, num_episodes=5):
    """Evaluate a genome over multiple episodes"""
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    scores = []
    for episode in range(num_episodes):
        obs, info = env.reset()
        total_reward = 0
        steps = 0
        max_steps = 5000

        while steps < max_steps:
            # Normalize observation
            normalized_obs = obs.astype(np.float32)
            normalized_obs[0] = obs[0] / env.CANVAS_HEIGHT
            normalized_obs[1] = obs[1] / 15.0
            normalized_obs[2] = obs[2] / env.CANVAS_WIDTH
            normalized_obs[3] = obs[3] / env.CANVAS_HEIGHT

            output = net.activate(normalized_obs)
            action = np.argmax(output)

            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1

            if terminated or truncated:
                break

        scores.append(total_reward)

    return scores, np.mean(scores)


def main():
    """Main evaluation and continuation"""
    config_file = script_dir.parent / "neat-config.txt"
    models_dir = script_dir.parent / "models"
    best_genome_file = models_dir / "best_genome.pkl"

    # Load configuration
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        str(config_file)
    )

    print("[EVALUATE] Loading best genome from generation 45...")
    if not best_genome_file.exists():
        print(f"[ERROR] Best genome file not found: {best_genome_file}")
        sys.exit(1)

    with open(best_genome_file, 'rb') as f:
        best_genome = pickle.load(f)

    print(f"[EVALUATE] Genome loaded: {best_genome}")

    # Create environment
    env = FlappyBirdEnv(render_mode=None)

    print(f"\n[EVALUATE] Testing best genome over 5 episodes...")
    scores, avg_score = evaluate_genome(best_genome, config, env, num_episodes=5)

    print(f"\n[EVALUATE] Individual episode scores: {scores}")
    print(f"[EVALUATE] Average score: {avg_score:.1f}")
    print(f"[EVALUATE] Best episode: {max(scores):.1f}")
    print(f"[EVALUATE] Worst episode: {min(scores):.1f}")

    if avg_score < -300:
        print(f"\n[DECISION] Genome is poor (avg {avg_score:.1f})")
        print(f"[DECISION] Recommend: Adjust fitness function + restart")
        recommendation = "ADJUST_FITNESS"
    elif avg_score < -100:
        print(f"\n[DECISION] Genome is weak (avg {avg_score:.1f})")
        print(f"[DECISION] Recommend: Continue training for more generations")
        recommendation = "CONTINUE_TRAINING"
    else:
        print(f"\n[DECISION] Genome is promising (avg {avg_score:.1f})")
        print(f"[DECISION] Recommend: Continue training with current fitness")
        recommendation = "CONTINUE_TRAINING"

    env.close()

    # Write results to file
    results_file = models_dir / "evaluation_results.txt"
    with open(results_file, 'w') as f:
        f.write(f"Best Genome Evaluation Results\n")
        f.write(f"=" * 50 + "\n\n")
        f.write(f"Test Episodes: 5\n")
        f.write(f"Individual Scores: {scores}\n")
        f.write(f"Average Score: {avg_score:.1f}\n")
        f.write(f"Best Score: {max(scores):.1f}\n")
        f.write(f"Worst Score: {min(scores):.1f}\n")
        f.write(f"Std Dev: {np.std(scores):.1f}\n\n")
        f.write(f"Recommendation: {recommendation}\n")

    print(f"\n[EVALUATE] Results saved to {results_file}")

    return recommendation


if __name__ == '__main__':
    result = main()
    print(f"\n[MAIN] Evaluation complete. Recommendation: {result}")
