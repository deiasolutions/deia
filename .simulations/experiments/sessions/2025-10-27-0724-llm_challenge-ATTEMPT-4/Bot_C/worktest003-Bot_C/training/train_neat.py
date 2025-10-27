"""NEAT training entrypoint for Flappy Bird (Attempt 4)."""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import pickle
import random
import statistics
import sys
import time
from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple

import neat
import numpy as np

# Ensure the local environment package is importable without modifying site packages
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from environment.flappy_env import FlappyBirdEnv  # noqa: E402

# Training defaults tuned for the one-hour simulation window
DEFAULT_GENERATIONS = 35
DEFAULT_EPISODES_PER_GENOME = 2
MAX_STEPS_PER_EPISODE = 2000
SCORE_FITNESS_WEIGHT = 500.0
SURVIVAL_FITNESS_WEIGHT = 1.0
DEATH_PENALTY = -50.0


@dataclass
class EpisodeStats:
    """Telemetry captured for each evaluation episode."""

    steps: int
    score: int
    fitness: float


@dataclass
class GenomeStats:
    """Summary metrics for a genome across evaluation episodes."""

    genome_id: int
    fitness: float
    best_score: int
    avg_steps: float


class GenerationTracker:
    """Collects per-generation summaries for later reporting."""

    def __init__(self) -> None:
        self.rows: list[dict] = []

    def record(self, generation: int, genome_stats: Sequence[GenomeStats]) -> None:
        best = max(genome_stats, key=lambda gs: gs.fitness)
        mean_fitness = statistics.mean(gs.fitness for gs in genome_stats)
        median_fitness = statistics.median(gs.fitness for gs in genome_stats)
        self.rows.append(
            {
                "generation": generation,
                "best_genome_id": best.genome_id,
                "best_fitness": best.fitness,
                "best_score": best.best_score,
                "mean_fitness": mean_fitness,
                "median_fitness": median_fitness,
            }
        )

    def export_csv(self, path: pathlib.Path) -> None:
        if not self.rows:
            return
        fieldnames = list(self.rows[0].keys())
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.rows)


def preprocess_observation(obs: np.ndarray) -> Tuple[float, float, float, float]:
    """Scale environment observation to roughly [0, 1] range for NEAT networks."""

    bird_y, bird_velocity, pipe_x, pipe_gap_y = obs
    return (
        float(bird_y / 600.0),
        float((bird_velocity + 15.0) / 30.0),
        float(pipe_x / 400.0),
        float(pipe_gap_y / 600.0),
    )


def play_episode(net: neat.nn.FeedForwardNetwork, *, seed: int | None = None) -> EpisodeStats:
    """Run a single Flappy Bird episode with the provided network."""

    env = FlappyBirdEnv()
    obs, _ = env.reset(seed=seed)

    steps = 0
    best_score = 0
    cumulative_fitness = 0.0

    while True:
        inputs = preprocess_observation(obs)
        output = net.activate(inputs)
        flap_probability = output[0] if output else 0.0
        action = 1 if flap_probability > 0.5 else 0

        obs, reward, terminated, truncated, info = env.step(action)
        steps += 1
        best_score = max(best_score, int(info.get("score", 0)))

        # Shape the fitness signal: reward survival and scoring.
        incremental = SURVIVAL_FITNESS_WEIGHT + reward
        cumulative_fitness += incremental

        if terminated or truncated or steps >= MAX_STEPS_PER_EPISODE:
            if terminated:
                cumulative_fitness += DEATH_PENALTY
            cumulative_fitness += best_score * SCORE_FITNESS_WEIGHT
            break

    env.close()
    return EpisodeStats(steps=steps, score=best_score, fitness=cumulative_fitness)


class NEATEvaluator:
    """Callable passed to neat.Population.run to evaluate genomes."""

    def __init__(self, episodes_per_genome: int, tracker: GenerationTracker) -> None:
        self.episodes_per_genome = episodes_per_genome
        self.tracker = tracker
        self.generation_index = 0

    def __call__(self, genomes: Iterable[Tuple[int, neat.DefaultGenome]], config: neat.Config) -> None:
        genome_stats: list[GenomeStats] = []

        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            episode_stats = [
                play_episode(net, seed=random.randint(0, 10_000))
                for _ in range(self.episodes_per_genome)
            ]

            fitness = statistics.mean(ep.fitness for ep in episode_stats)
            genome.fitness = fitness

            genome_stats.append(
                GenomeStats(
                    genome_id=genome_id,
                    fitness=fitness,
                    best_score=max(ep.score for ep in episode_stats),
                    avg_steps=statistics.mean(ep.steps for ep in episode_stats),
                )
            )

        self.tracker.record(self.generation_index, genome_stats)
        self.generation_index += 1


def evaluate_winner(genome: neat.DefaultGenome, config: neat.Config, *, episodes: int = 5) -> dict:
    """Run several evaluation episodes with the winning genome for reporting."""

    net = neat.nn.FeedForwardNetwork.create(genome, config)
    episode_stats = [play_episode(net, seed=random.randint(0, 100_000)) for _ in range(episodes)]

    return {
        "episodes": episodes,
        "mean_fitness": statistics.mean(ep.fitness for ep in episode_stats),
        "mean_steps": statistics.mean(ep.steps for ep in episode_stats),
        "best_score": max(ep.score for ep in episode_stats),
        "max_steps": max(ep.steps for ep in episode_stats),
        "scores": [ep.score for ep in episode_stats],
        "steps": [ep.steps for ep in episode_stats],
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train a NEAT agent for Flappy Bird.")
    parser.add_argument(
        "--generations",
        type=int,
        default=DEFAULT_GENERATIONS,
        help=f"Number of generations to evolve (default: {DEFAULT_GENERATIONS}).",
    )
    parser.add_argument(
        "--episodes-per-genome",
        type=int,
        default=DEFAULT_EPISODES_PER_GENOME,
        help=f"Evaluation episodes per genome (default: {DEFAULT_EPISODES_PER_GENOME}).",
    )
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        default=PROJECT_ROOT / "config" / "neat-flappy-config.ini",
        help="Path to NEAT configuration file.",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=PROJECT_ROOT / "results" / "neat",
        help="Directory for checkpoints and telemetry.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    config_path = args.config.resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"NEAT config not found: {config_path}")

    output_dir = args.output_dir.resolve()
    models_dir = PROJECT_ROOT / "models" / "neat"
    checkpoints_dir = output_dir / "checkpoints"
    logs_dir = output_dir / "logs"

    models_dir.mkdir(parents=True, exist_ok=True)
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        str(config_path),
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats_reporter = neat.StatisticsReporter()
    population.add_reporter(stats_reporter)
    population.add_reporter(
        neat.Checkpointer(
            generation_interval=5,
            filename_prefix=str(checkpoints_dir / "flappy-neat-checkpoint-"),
        )
    )

    tracker = GenerationTracker()
    evaluator = NEATEvaluator(args.episodes_per_genome, tracker)

    start_time = time.time()
    winner = population.run(evaluator, args.generations)
    total_duration = time.time() - start_time

    results = evaluate_winner(winner, config, episodes=5)

    winner_path = models_dir / "best_genome.pkl"
    with winner_path.open("wb") as fh:
        pickle.dump(winner, fh)

    summary = {
        "generations": args.generations,
        "episodes_per_genome": args.episodes_per_genome,
        "config": str(config_path),
        "duration_seconds": total_duration,
        "winner_fitness": winner.fitness,
        "winner_id": getattr(winner, "key", None),
        "winner_evaluation": results,
    }

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))

    tracker.export_csv(logs_dir / "generation_metrics.csv")

    print("Training complete.")
    print(f"Best genome saved to: {winner_path}")
    print(f"Summary written to: {summary_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
