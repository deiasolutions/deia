"""
Test Flappy Bird Environment
Run random agent to validate environment works correctly
"""

from flappy_env import FlappyBirdEnv
import numpy as np


def test_random_agent(n_episodes=10):
    """Test environment with random actions"""
    env = FlappyBirdEnv()

    print("Testing FlappyBirdEnv with random agent...")
    print("="*50)

    scores = []

    for episode in range(n_episodes):
        obs, info = env.reset()
        print(f"\nEpisode {episode + 1}: Initial observation shape: {obs.shape}")

        total_reward = 0
        steps = 0
        done = False

        while not done:
            # Random action
            action = env.action_space.sample()

            # Step
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1
            done = terminated or truncated

            # Check observation validity
            assert obs.shape == (4,), f"Invalid observation shape: {obs.shape}"
            assert env.observation_space.contains(obs), f"Observation out of bounds: {obs}"

        score = info['score']
        scores.append(score)
        print(f"Episode {episode + 1} done: Score={score}, Steps={steps}, Total Reward={total_reward:.2f}")

    print("\n" + "="*50)
    print(f"Random Agent Baseline:")
    print(f"  Mean Score: {np.mean(scores):.2f} ± {np.std(scores):.2f}")
    print(f"  Max Score: {np.max(scores)}")
    print(f"  Min Score: {np.min(scores)}")
    print("="*50)

    # Random agent should score 0-5 typically
    if np.mean(scores) < 10:
        print("✓ Environment validated! Random agent performance as expected.")
    else:
        print("⚠ Warning: Random agent scoring unexpectedly high. Check environment.")

    env.close()


if __name__ == "__main__":
    test_random_agent(n_episodes=10)
