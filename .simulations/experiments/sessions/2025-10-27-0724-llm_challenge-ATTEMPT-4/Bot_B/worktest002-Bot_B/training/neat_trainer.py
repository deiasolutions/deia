#!/usr/bin/env python3
"""
NEAT Trainer for Flappy Bird
Bot B2 Implementation - ATTEMPT 4
"""

import os
import sys
import csv
import pickle
from pathlib import Path

# Add sandbox to path
# The .sandbox dir is at the repo root (Deiasolutions directory)
# From our location: training -> worktest002-Bot_B -> Bot_B -> ATTEMPT-4 -> sessions -> experiments -> .simulations
# We need to go UP to the parent of .simulations to reach the repo root
script_dir = Path(__file__).resolve().parent  # training/
worktest_dir = script_dir.parent  # worktest002-Bot_B/
bot_b_dir = worktest_dir.parent  # Bot_B/
attempt_dir = bot_b_dir.parent  # ATTEMPT-4/
sessions_dir = attempt_dir.parent  # sessions/
experiments_dir = sessions_dir.parent  # experiments/
simulations_dir = experiments_dir.parent  # .simulations/
repo_root = simulations_dir.parent  # Deiasolutions/

sandbox_path = repo_root / ".sandbox" / "flappy-bird-ai"
sys.path.insert(0, str(sandbox_path))

import neat
import gymnasium as gym
import numpy as np

# Import from flappy-bird-ai
from environment.flappy_env import FlappyBirdEnv


class NEATFlappyBirdTrainer:
    """NEAT trainer for Flappy Bird environment"""

    def __init__(self, config_file, output_dir):
        """Initialize NEAT trainer"""
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

        # Statistics tracking
        self.generation_stats = []
        self.best_genome = None
        self.best_fitness = -float('inf')

        print(f"[NEAT Trainer] Initialized with config from {config_file}")
        print(f"[NEAT Trainer] Population size: {self.config.pop_size}")
        print(f"[NEAT Trainer] Output directory: {self.output_dir}")

    def create_environment(self):
        """Create Flappy Bird environment"""
        try:
            env = FlappyBirdEnv(render_mode=None)
            print(f"[Environment] Created FlappyBirdEnv successfully")
            print(f"[Environment] Observation space: {env.observation_space}")
            print(f"[Environment] Action space: {env.action_space}")
            return env
        except Exception as e:
            print(f"[ERROR] Failed to create environment: {e}")
            raise

    def eval_genome(self, genome, config, env):
        """Evaluate a single genome in the Flappy Bird environment"""
        try:
            # Create neural network from genome
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            # Reset environment
            obs, info = env.reset()

            # Run episode
            total_reward = 0
            max_steps = 5000  # Prevent infinite episodes
            steps = 0

            while steps < max_steps:
                # Normalize observation to [-1, 1] for better NEAT performance
                normalized_obs = obs.astype(np.float32)
                normalized_obs[0] = obs[0] / env.CANVAS_HEIGHT
                normalized_obs[1] = obs[1] / 15.0
                normalized_obs[2] = obs[2] / env.CANVAS_WIDTH
                normalized_obs[3] = obs[3] / env.CANVAS_HEIGHT

                # Get network output
                output = net.activate(normalized_obs)

                # Choose action (argmax of output)
                action = np.argmax(output)

                # Step environment
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
        """Evaluate all genomes in population"""
        for genome_id, genome in genomes:
            genome.fitness = self.eval_genome(genome, config, env)

    def run_neat(self, num_generations=None):
        """Run NEAT evolution"""
        print(f"\n[NEAT] Starting evolution...")

        # Create population
        p = neat.Population(self.config)

        # Create environment (reuse across evaluations)
        env = self.create_environment()

        # Add reporters
        p.reporters.add(neat.StdOutReporter(True))

        # Create checkpoint directory
        checkpoint_dir = self.output_dir / "checkpoints"
        checkpoint_dir.mkdir(exist_ok=True)

        stats = neat.StatisticsReporter()
        p.reporters.add(stats)

        # Run evolution
        print(f"[NEAT] Running {num_generations or self.config.max_generation} generations...")

        def eval_fn(genomes, config):
            self.eval_genomes(genomes, config, env)

        # Run NEAT
        winner = p.run(eval_fn, num_generations or self.config.max_generation)

        # Store results
        self.best_genome = winner
        self.best_fitness = winner.fitness

        # Save statistics
        self.save_statistics(stats)

        # Save best genome
        self.save_best_genome(winner)

        print(f"\n[NEAT] Evolution complete!")
        print(f"[NEAT] Best fitness: {self.best_fitness}")

        env.close()

        return winner

    def save_statistics(self, stats):
        """Save generation statistics to CSV"""
        stats_file = self.output_dir / "fitness_stats.csv"

        with open(stats_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Generation', 'Best', 'Average', 'Median', 'Stdev', 'Min', 'Max'])

            for generation, stat in enumerate(stats.generation_statistics):
                writer.writerow([
                    generation,
                    stat[0] if stat else 0,  # Best
                    stat[1] if stat else 0,  # Average
                    stat[2] if stat else 0,  # Median
                    stat[3] if stat else 0,  # Stdev
                    stat[4] if stat else 0,  # Min
                    stat[5] if stat else 0,  # Max
                ])

        print(f"[NEAT] Statistics saved to {stats_file}")

    def save_best_genome(self, genome):
        """Save best genome to file"""
        genome_file = self.output_dir / "best_genome.pkl"
        with open(genome_file, 'wb') as f:
            pickle.dump(genome, f)

        # Also save as text
        text_file = self.output_dir / "best_genome.txt"
        with open(text_file, 'w') as f:
            f.write(f"Best Genome (Fitness: {self.best_fitness})\n")
            f.write(f"{'='*50}\n")
            f.write(str(genome))

        print(f"[NEAT] Best genome saved to {genome_file} and {text_file}")

    def test_best_genome(self, num_episodes=5):
        """Test best genome performance"""
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
            max_steps = 5000

            while steps < max_steps:
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
            print(f"[TEST] Episode {ep+1}/{num_episodes}: Score = {total_reward}")

        avg_score = np.mean(scores)
        print(f"[TEST] Average score across {num_episodes} episodes: {avg_score}")

        env.close()
        return avg_score


def main():
    """Main entry point"""
    # Setup paths
    script_dir = Path(__file__).parent
    config_file = script_dir / "neat-config.txt"
    output_dir = script_dir.parent / "models"

    if not config_file.exists():
        config_file = script_dir.parent / "neat-config.txt"

    print(f"[MAIN] Config file: {config_file}")
    print(f"[MAIN] Output directory: {output_dir}")

    if not config_file.exists():
        print(f"[ERROR] Config file not found: {config_file}")
        sys.exit(1)

    # Create trainer
    trainer = NEATFlappyBirdTrainer(str(config_file), output_dir)

    # Run NEAT evolution
    try:
        winner = trainer.run_neat(num_generations=50)

        # Test best genome
        print(f"\n[MAIN] Testing best genome...")
        trainer.test_best_genome(num_episodes=3)

        print(f"\n[MAIN] Training complete!")
        print(f"[MAIN] Results saved to {output_dir}")

    except KeyboardInterrupt:
        print(f"\n[MAIN] Training interrupted by user")
    except Exception as e:
        print(f"[ERROR] Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
