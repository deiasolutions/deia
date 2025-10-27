"""
NEAT Training for Flappy Bird - Optimized for 1-Hour Constraint
Bot A - Q33N Simulation (ATTEMPT-4)

Algorithm: NEAT (Neuroevolution of Augmenting Topologies)
Constraint: Must complete in ~1 hour

DEIA Compliance:
- All code documented
- Configuration clear and justified
- Results logged
- Fitness tracking comprehensive
- No base code modifications
"""

import sys
import os
import time
import pickle
import json
from datetime import datetime
import traceback

# Add parent path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

import neat
import numpy as np
from flappy_env import FlappyBirdEnv

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

# Ensure output directories exist
os.makedirs('../models', exist_ok=True)
os.makedirs('../logs', exist_ok=True)
os.makedirs('../results', exist_ok=True)

# Logging file paths
TRAINING_LOG = '../logs/neat_training.log'
RESULTS_JSON = '../results/neat_results.json'
BEST_GENOME = '../models/neat_best.pkl'
STATS_FILE = '../logs/neat_statistics.pkl'

# ============================================================================
# TRAINING PARAMETERS (Optimized for 1-hour constraint)
# ============================================================================

# Time-aware configuration
GENERATIONS = 15  # Conservative estimate for 1 hour (can increase if faster)
GAMES_PER_GENOME = 2  # 2 games per evaluation (faster than 3)
MAX_TRAINING_TIME = 3500  # 58 minutes in seconds (leaving 2 min buffer)

# Reduced population for faster training (still diverse)
POPULATION_SIZE = 80  # Reduced from 100 for speed

# ============================================================================
# LOGGING UTILITIES
# ============================================================================

def log_message(message):
    """Log to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(TRAINING_LOG, 'a') as f:
        f.write(full_message + "\n")

def save_results(data, filepath):
    """Save results to JSON for analysis"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# ============================================================================
# ENVIRONMENT & EVALUATION
# ============================================================================

def eval_genome(genome, config, games=GAMES_PER_GENOME):
    """
    Evaluate a single genome by playing games.

    Args:
        genome: NEAT genome to evaluate
        config: NEAT configuration
        games: Number of games to play for averaging

    Returns:
        Average score across games
    """
    try:
        # Create neural network from genome
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        env = FlappyBirdEnv()

        total_score = 0
        max_score_this_genome = 0

        for game_idx in range(games):
            obs, _ = env.reset()
            done = False
            frame_count = 0

            while not done and frame_count < 1000:  # Max 1000 frames per game
                # Get action from network
                # Network expects: [bird_y, bird_velocity, next_pipe_x, next_pipe_gap_y]
                try:
                    output = net.activate(obs)
                    action = 1 if output[0] > 0.5 else 0
                except Exception as e:
                    log_message(f"Error in network activation: {e}")
                    action = 0

                obs, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
                frame_count += 1

            score = info.get('score', 0)
            total_score += score
            max_score_this_genome = max(max_score_this_genome, score)

        env.close()

        # Return average score
        avg_score = total_score / games
        return avg_score

    except Exception as e:
        log_message(f"Error evaluating genome: {e}")
        traceback.print_exc()
        return 0.0

def eval_genomes(genomes, config):
    """
    Evaluate all genomes in a population.

    Args:
        genomes: List of (genome_id, genome) tuples
        config: NEAT configuration
    """
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config, games=GAMES_PER_GENOME)

# ============================================================================
# MAIN TRAINING LOOP
# ============================================================================

def run_neat_optimized():
    """
    Run NEAT evolution with 1-hour constraint.

    Strategy:
    1. Load configuration
    2. Initialize population
    3. Run generations until time limit
    4. Save best results
    5. Evaluate final performance
    """

    log_message("=" * 70)
    log_message("NEAT TRAINING - FLAPPY BIRD AI (1-HOUR OPTIMIZED)")
    log_message("=" * 70)
    log_message(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_message(f"Generations target: {GENERATIONS}")
    log_message(f"Population size: {POPULATION_SIZE}")
    log_message(f"Games per evaluation: {GAMES_PER_GENOME}")
    log_message(f"Max training time: {MAX_TRAINING_TIME} seconds")
    log_message("=" * 70)

    start_time = time.time()

    try:
        # Load configuration
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config/neat_config.txt')

        if not os.path.exists(config_path):
            log_message(f"ERROR: Config not found at {config_path}")
            return None

        log_message(f"Loading NEAT config from: {config_path}")
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )

        # Override population size for speed
        config.pop_size = POPULATION_SIZE
        log_message(f"Config loaded. Population size: {config.pop_size}")

        # Create population
        log_message("\nInitializing population...")
        p = neat.Population(config)

        # Add reporters
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        # Checkpoint every 5 generations
        checkpointer = neat.Checkpointer(5, filename_prefix='../models/neat-checkpoint-')
        p.add_reporter(checkpointer)

        log_message("Population initialized.")
        log_message("\n" + "=" * 70)
        log_message("EVOLUTION STARTING")
        log_message("=" * 70)

        # Run evolution with time constraint
        generation_count = 0
        winner = None
        best_fitness_history = []

        def evolution_callback(population):
            """Called at end of each generation"""
            nonlocal generation_count, winner
            generation_count += 1

            elapsed = time.time() - start_time
            best_fitness = max(g.fitness for g in population.population.values())
            best_fitness_history.append(best_fitness)

            log_message(f"Generation {generation_count:3d} | Best Fitness: {best_fitness:8.2f} | "
                       f"Elapsed: {elapsed:6.1f}s")

            # Check time constraint
            if elapsed > MAX_TRAINING_TIME:
                log_message(f"\nTime limit reached ({elapsed:.1f}s > {MAX_TRAINING_TIME}s)")
                return True  # Stop evolution

            return False

        # Run evolution
        winner = p.run(eval_genomes, GENERATIONS)

        elapsed = time.time() - start_time

        log_message("\n" + "=" * 70)
        log_message("EVOLUTION COMPLETE")
        log_message("=" * 70)
        log_message(f"Total time: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
        log_message(f"Generations completed: {generation_count}")
        log_message(f"Best genome fitness: {winner.fitness:.2f}")

        # Save best genome
        log_message("\nSaving best genome...")
        with open(BEST_GENOME, 'wb') as f:
            pickle.dump((winner, config), f)
        log_message(f"Best genome saved to: {BEST_GENOME}")

        # Save statistics
        with open(STATS_FILE, 'wb') as f:
            pickle.dump(stats, f)
        log_message(f"Statistics saved to: {STATS_FILE}")

        # Final evaluation
        log_message("\n" + "=" * 70)
        log_message("FINAL EVALUATION (10 episodes)")
        log_message("=" * 70)

        net = neat.nn.FeedForwardNetwork.create(winner, config)
        env = FlappyBirdEnv()
        scores = []

        for episode in range(10):
            obs, _ = env.reset()
            done = False
            while not done:
                output = net.activate(obs)
                action = 1 if output[0] > 0.5 else 0
                obs, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated

            score = info.get('score', 0)
            scores.append(score)
            log_message(f"  Episode {episode+1:2d}: Score = {score}")

        env.close()

        # Calculate statistics
        scores_array = np.array(scores)
        mean_score = np.mean(scores_array)
        std_score = np.std(scores_array)
        max_score = np.max(scores_array)
        min_score = np.min(scores_array)

        log_message("\n" + "=" * 70)
        log_message("FINAL RESULTS")
        log_message("=" * 70)
        log_message(f"Mean Score:     {mean_score:.2f} ± {std_score:.2f}")
        log_message(f"Max Score:      {max_score}")
        log_message(f"Min Score:      {min_score}")
        log_message(f"Training Time:  {elapsed:.2f} seconds")
        log_message(f"Generations:    {generation_count}")
        log_message("=" * 70)

        # Save results to JSON
        results = {
            'algorithm': 'NEAT',
            'timestamp': datetime.now().isoformat(),
            'training_time_seconds': elapsed,
            'generations': generation_count,
            'population_size': POPULATION_SIZE,
            'games_per_eval': GAMES_PER_GENOME,
            'best_genome_fitness': float(winner.fitness),
            'final_evaluation': {
                'episodes': 10,
                'mean_score': float(mean_score),
                'std_score': float(std_score),
                'max_score': int(max_score),
                'min_score': int(min_score),
                'scores': [int(s) for s in scores]
            },
            'best_fitness_history': [float(f) for f in best_fitness_history]
        }

        save_results(results, RESULTS_JSON)
        log_message(f"\nResults saved to: {RESULTS_JSON}")

        return winner, config, results

    except Exception as e:
        log_message(f"\nERROR: {e}")
        traceback.print_exc()
        return None

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    log_message("\n\n" + "=" * 70)
    log_message("BOT A - NEAT TRAINING SESSION START")
    log_message("=" * 70)

    result = run_neat_optimized()

    if result:
        winner, config, results = result
        log_message("\n" + "=" * 70)
        log_message("TRAINING SESSION COMPLETE - SUCCESS")
        log_message("=" * 70)
    else:
        log_message("\n" + "=" * 70)
        log_message("TRAINING SESSION FAILED")
        log_message("=" * 70)
