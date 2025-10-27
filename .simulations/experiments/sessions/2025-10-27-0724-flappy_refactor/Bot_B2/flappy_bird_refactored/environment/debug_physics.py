"""
Debug script to understand why agents can't survive/score
Analyzes physics, timing, and pipe positions
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flappy_env import FlappyBirdEnv


def analyze_first_pipe_challenge():
    """Analyze what happens when agent encounters first pipe"""
    print("\n=== FIRST PIPE CHALLENGE ANALYSIS ===\n")

    env = FlappyBirdEnv()
    obs, info = env.reset()

    print(f"Bird starting position: x={env.bird_x}, y={env.bird_y}")
    print(f"Canvas: width={env.CANVAS_WIDTH}, height={env.CANVAS_HEIGHT}")
    print(f"Gravity: {env.GRAVITY}, Flap power: {env.FLAP_POWER}")
    print(f"Pipe gap: {env.PIPE_GAP}, Pipe width: {env.PIPE_WIDTH}")
    print(f"Pipe spawn interval: {env.PIPE_SPAWN_INTERVAL} frames\n")

    print(f"Initial observation: {obs}")
    print(f"  bird_y: {obs[0]:.1f}")
    print(f"  bird_velocity: {obs[1]:.1f}")
    print(f"  relative_pipe_x: {obs[2]:.1f}")
    print(f"  pipe_gap_y: {obs[3]:.1f}")
    print(f"  pipe_bottom_y: {obs[4]:.1f}\n")

    print(f"Initial pipe: {env.pipes[0]}")
    print(f"  Gap starts at: y={env.pipes[0]['gap_y']:.1f}")
    print(f"  Gap ends at: y={env.pipes[0]['gap_y'] + env.PIPE_GAP:.1f}")
    print(f"  Safe zone height: {env.PIPE_GAP} pixels\n")

    # Simulate 30 frames of no action to understand trajectory
    print("Simulation (no action):")
    print("Frame | Bird_Y | Velocity | Pipe_X | Distance | Safe?")
    print("-" * 60)

    terminated = False
    for frame in range(35):
        if frame > 0:
            action = 0  # Just let gravity
            obs, reward, terminated, truncated, info = env.step(action)

        if not env.pipes:
            break

        pipe = env.pipes[0]
        bird_y = env.bird_y
        safe_top = pipe['gap_y']
        safe_bottom = pipe['gap_y'] + env.PIPE_GAP

        # Check if bird is safe (if horizontally aligned)
        is_aligned = (env.bird_x + env.BIRD_SIZE/2 > pipe['x'] and
                      env.bird_x - env.BIRD_SIZE/2 < pipe['x'] + env.PIPE_WIDTH)

        is_safe = (bird_y - env.BIRD_SIZE/2 >= safe_top and
                   bird_y + env.BIRD_SIZE/2 <= safe_bottom) if is_aligned else True

        distance = pipe['x'] - env.bird_x

        print(f"{frame:3} | {bird_y:6.1f} | {env.bird_velocity:8.1f} | {pipe['x']:6.1f} | {distance:8.1f} | {'YES' if is_safe else 'NO':3}")

        if terminated:
            print(">> EPISODE TERMINATED (COLLISION) <<")
            break


def analyze_flap_strategy():
    """Test if a simple flap-when-low strategy works"""
    print("\n=== FLAP STRATEGY ANALYSIS ===\n")

    env = FlappyBirdEnv()

    best_score = 0
    best_distance = 0

    for episode in range(10):
        obs, info = env.reset()
        episode_score = 0
        max_distance = 0

        for step in range(500):
            pipe = env.pipes[0] if env.pipes else None

            # Strategy: if bird is below pipe gap, flap
            if obs[0] > obs[3]:  # bird_y > pipe_gap_y
                action = 1
            else:
                action = 0

            obs, reward, terminated, truncated, info = env.step(action)
            episode_score += reward

            if pipe:
                distance = pipe['x'] - env.bird_x
                max_distance = max(max_distance, distance)

            if terminated:
                break

        if episode_score > best_score:
            best_score = episode_score
        best_distance = max(best_distance, max_distance)

        print(f"Episode {episode}: Score={env.score}, Reward={episode_score:.1f}, Steps={step}, Dist={max_distance:.1f}")

    print(f"\nBest score across episodes: {best_score:.1f}")
    print(f"Max distance traveled: {best_distance:.1f}")


def check_pipe_geometry():
    """Check if pipe gaps are reasonable"""
    print("\n=== PIPE GEOMETRY CHECK ===\n")

    env = FlappyBirdEnv()

    gaps = []
    for i in range(20):
        obs, info = env.reset()
        pipe = env.pipes[0]
        gaps.append(pipe['gap_y'])

    gaps = np.array(gaps)
    print(f"Pipe gap positions across 20 resets:")
    print(f"  Min: {gaps.min():.1f}")
    print(f"  Max: {gaps.max():.1f}")
    print(f"  Mean: {gaps.mean():.1f}")
    print(f"  Std: {gaps.std():.1f}")
    print(f"\nBird height: {env.BIRD_SIZE}")
    print(f"Bird safe starting position: y={env.CANVAS_HEIGHT/2} (center)")
    print(f"Gap size: {env.PIPE_GAP}")

    # Check if bird can ever reach middle
    print(f"\nCan bird reach center? Yes, starts there.")
    print(f"Does gravity pull too fast?")

    velocity = 0
    y = env.CANVAS_HEIGHT / 2
    for frame in range(31):
        velocity += env.GRAVITY
        y += velocity
    print(f"  After 31 frames with no flap: y={y:.1f} (started at {env.CANVAS_HEIGHT/2})")
    print(f"  Would collide with ground? {y + env.BIRD_SIZE/2 >= env.CANVAS_HEIGHT - env.GROUND_HEIGHT}")


if __name__ == '__main__':
    check_pipe_geometry()
    analyze_first_pipe_challenge()
    analyze_flap_strategy()
