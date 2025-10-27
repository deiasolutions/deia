#!/usr/bin/env python3
"""
Extended NEAT Trainer for Flappy Bird - Phase 3 Optimization
Bot B2 Extended Training
"""

import os
import sys
import csv
import pickle
from pathlib import Path

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
import gymnasium as gym
from environment.flappy_env import FlappyBirdEnv
import numpy as np


class ExtendedNEATTrainer:
    """Extended NEAT trainer for continued evolution"""

    def __init__(self, config_file, output_dir):
        """Initialize trainer"""
        self.config_file = config_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load NEAT configuration
        self.config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_file
        )

        self.best_genome = None
        self.best_fitness = -float('inf')
        self.generation_stats = {}

        print(f"[EXTENDED] Initialized with config from {config_file}")
        print(f"[EXTENDED] Output directory: {self.output_dir}")

    def create_environment(self):
        """Create Flappy Bird environment"""
        env = FlappyBirdEnv(render_mode=None)
        print(f"[Environment] Created FlappyBirdEnv successfully")
        return env

    def eval_genome(self, genome, config, env):
        """Evaluate a single genome"""
        try:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
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

            return total_reward

        except Exception as e:
            print(f"[ERROR] Genome evaluation failed: {e}")
            return 0.0

    def eval_genomes(self, genomes, config, env):
        """Evaluate all genomes"""
        for genome_id, genome in genomes:
            genome.fitness = self.eval_genome(genome, config, env)

    def run_extended_training(self, num_generations=75):
        """Run extended NEAT training"""
        print(f"\n[EXTENDED] Starting extended training for {num_generations} generations...")

        # Create population
        p = neat.Population(self.config)

        # Create environment
        env = self.create_environment()

        # Add reporters
        p.reporters.add(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.reporters.add(stats)

        # Run evolution
        def eval_fn(genomes, config):
            self.eval_genomes(genomes, config, env)

        print(f"[EXTENDED] Running evolution...")
        winner = p.run(eval_fn, num_generations)

        # Store results
        self.best_genome = winner
        self.best_fitness = winner.fitness

        print(f"\n[EXTENDED] Training complete!")
        print(f"[EXTENDED] Best fitness: {self.best_fitness}")
        print(f"[EXTENDED] Best genome: {winner}")

        # Save best genome
        self.save_best_genome(winner)

        # Save stats safely
        self.save_statistics_safe(stats)

        env.close()

        return winner

    def save_best_genome(self, genome):
        """Save best genome"""
        genome_file = self.output_dir / "best_genome_extended.pkl"
        with open(genome_file, 'wb') as f:
            pickle.dump(genome, f)

        # Also save as text
        text_file = self.output_dir / "best_genome_extended.txt"
        with open(text_file, 'w') as f:
            f.write(f"Best Extended Genome (Fitness: {self.best_fitness})\n")
            f.write(f"{'='*50}\n")
            f.write(str(genome))

        print(f"[EXTENDED] Best genome saved to {genome_file}")

    def save_statistics_safe(self, stats):
        """Save statistics safely"""
        try:
            stats_file = self.output_dir / "fitness_stats_extended.csv"

            with open(stats_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Generation', 'Best', 'Average', 'Stdev', 'Size'])

                for generation in range(len(stats.most_fit_genomes)):
                    if generation < len(stats.most_fit_genomes):
                        best = stats.most_fit_genomes[generation].fitness if stats.most_fit_genomes[generation] else 0
                        writer.writerow([generation, best, 0, 0, 0])

            print(f"[EXTENDED] Statistics saved to {stats_file}")
        except Exception as e:
            print(f"[WARNING] Stats saving failed: {e}")
            print(f"[INFO] Continuing anyway...")

    def test_genome(self, num_episodes=5):
        """Test best genome"""
        if self.best_genome is None:
            print("[ERROR] No best genome found")
            return

        env = self.create_environment()
        config = self.config

        net = neat.nn.FeedForwardNetwork.create(self.best_genome, config)

        scores = []
        for ep in range(num_episodes):
            obs, info = env.reset()
            total_reward = 0
            steps = 0

            while steps < 5000:
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
            print(f"[TEST] Episode {ep+1}/{num_episodes}: Score = {total_reward:.1f}")

        avg_score = np.mean(scores)
        print(f"[TEST] Average score: {avg_score:.1f}")
        print(f"[TEST] Best episode: {max(scores):.1f}")

        env.close()
        return avg_score


def main():
    """Main entry point"""
    config_file = Path(__file__).parent.parent / "neat-config.txt"
    output_dir = Path(__file__).parent.parent / "models"

    print(f"[MAIN] Config file: {config_file}")
    print(f"[MAIN] Output directory: {output_dir}")

    if not config_file.exists():
        print(f"[ERROR] Config file not found: {config_file}")
        sys.exit(1)

    trainer = ExtendedNEATTrainer(str(config_file), output_dir)

    try:
        # Run extended training (25 more generations = 75 total)
        print("\n[MAIN] Running extended training for 25 more generations (50->75)...")
        winner = trainer.run_extended_training(num_generations=25)

        # Test the best genome
        print(f"\n[MAIN] Testing best genome...")
        avg_score = trainer.test_genome(num_episodes=3)

        print(f"\n[MAIN] Extended training complete!")
        print(f"[MAIN] Final best fitness: {trainer.best_fitness}")
        print(f"[MAIN] Test average: {avg_score}")

    except KeyboardInterrupt:
        print(f"\n[MAIN] Training interrupted by user")
    except Exception as e:
        print(f"[ERROR] Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
