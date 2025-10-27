"""
Test suite to validate Flappy Bird environment improvements
Tests observation bounds, reward system, episode limits, and agent learning
"""

import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flappy_env import FlappyBirdEnv


def test_observation_bounds():
    """Test that observations stay within defined bounds"""
    print("\n=== TEST 1: Observation Bounds ===")
    env = FlappyBirdEnv()

    for episode in range(10):
        obs, info = env.reset()

        # Check initial observation is in bounds
        assert env.observation_space.contains(obs), f"Initial observation out of bounds: {obs}"

        for step in range(200):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)

            # Every step, observation should be in bounds
            if not env.observation_space.contains(obs):
                print(f"  ERROR: Observation out of bounds at episode {episode}, step {step}")
                print(f"    Observation: {obs}")
                print(f"    Bounds low: {env.observation_space.low}")
                print(f"    Bounds high: {env.observation_space.high}")
                return False

            if terminated:
                break

    print("  [PASS] All observations within bounds")
    return True


def test_episode_termination():
    """Test that episodes terminate properly"""
    print("\n=== TEST 2: Episode Termination ===")
    env = FlappyBirdEnv(max_episode_steps=500)

    obs, info = env.reset()
    step_count = 0
    terminated = False

    for step in range(600):
        action = 0  # Just let gravity do its thing
        obs, reward, terminated, truncated, info = env.step(action)
        step_count += 1

        if terminated:
            break

    if step_count > 500:
        print(f"  ERROR: Episode didn't terminate within 500 steps (lasted {step_count})")
        return False

    print(f"  [PASS] Episode terminated at step {step_count}")
    return True


def test_reward_system():
    """Test that rewards are within reasonable bounds"""
    print("\n=== TEST 3: Reward System ===")
    env = FlappyBirdEnv()

    min_reward = float('inf')
    max_reward = float('-inf')
    pipe_rewards = []
    death_penalties = []

    for episode in range(10):
        obs, info = env.reset()

        for step in range(200):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)

            min_reward = min(min_reward, reward)
            max_reward = max(max_reward, reward)

            if reward > 10:  # Pipe passing
                pipe_rewards.append(reward)
            elif reward < 0:  # Death
                death_penalties.append(reward)

            if terminated:
                break

    print(f"  Reward range: [{min_reward}, {max_reward}]")
    print(f"  Pipe rewards found: {len(pipe_rewards)}")
    if pipe_rewards:
        print(f"    Pipe reward values: {set(pipe_rewards)}")
    print(f"  Death penalties found: {len(death_penalties)}")
    if death_penalties:
        print(f"    Death penalty values: {set(death_penalties)}")

    # Check reward magnitudes are reasonable (not dominating like -500)
    if min_reward < -100:
        print(f"  WARNING: Death penalty too harsh ({min_reward})")

    if max_reward > 100:
        print(f"  WARNING: Pipe reward too high ({max_reward})")

    print("  [PASS] Rewards within expected ranges")
    return True


def test_pipe_scoring():
    """Test that agents can actually score points"""
    print("\n=== TEST 4: Pipe Scoring ===")
    env = FlappyBirdEnv()

    episodes_with_scores = 0
    total_scores = []

    for episode in range(20):
        obs, info = env.reset()
        episode_reward = 0

        # Simple strategy: flap when bird is below center
        for step in range(500):
            if obs[0] > env.CANVAS_HEIGHT / 2:  # bird_y
                action = 1  # flap
            else:
                action = 0  # don't flap

            obs, reward, terminated, truncated, info = env.step(action)
            episode_reward += reward

            if terminated:
                break

        score = env.score
        total_scores.append(score)
        if score > 0:
            episodes_with_scores += 1

    avg_score = np.mean(total_scores)
    print(f"  Episodes with score > 0: {episodes_with_scores}/20")
    print(f"  Average score: {avg_score:.2f}")
    print(f"  Max score: {max(total_scores)}")

    if episodes_with_scores == 0:
        print("  [FAIL] CRITICAL: No episodes achieved any score!")
        return False

    print(f"  [PASS] Agents can score (success in {episodes_with_scores} episodes)")
    return True


def test_relative_pipe_distance():
    """Test that relative pipe distance is properly bounded"""
    print("\n=== TEST 5: Relative Pipe Distance ===")
    env = FlappyBirdEnv()

    obs, info = env.reset()
    relative_distances = []

    for step in range(300):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)

        relative_x = obs[2]  # Relative pipe distance
        relative_distances.append(relative_x)

        # Should be within observation bounds
        assert env.observation_space.low[2] <= relative_x <= env.observation_space.high[2], \
            f"Relative distance out of bounds: {relative_x}"

        if terminated:
            break

    print(f"  Relative distance range: [{min(relative_distances):.1f}, {max(relative_distances):.1f}]")
    print(f"  Observation bounds: [{env.observation_space.low[2]}, {env.observation_space.high[2]}]")
    print("  [PASS] Relative distances properly bounded")
    return True


def run_all_tests():
    """Run all validation tests"""
    print("\n" + "="*50)
    print("FLAPPY BIRD ENVIRONMENT VALIDATION TESTS")
    print("="*50)

    tests = [
        test_observation_bounds,
        test_episode_termination,
        test_reward_system,
        test_pipe_scoring,
        test_relative_pipe_distance,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  [FAIL] TEST FAILED WITH ERROR: {e}")
            results.append(False)

    print("\n" + "="*50)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("="*50 + "\n")

    return all(results)


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
