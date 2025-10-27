"""Debug why scoring doesn't work"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flappy_env import FlappyBirdEnv

env = FlappyBirdEnv()
obs, info = env.reset()

print(f"Bird X: {env.bird_x}")
print(f"First pipe X: {env.pipes[0]['x']}")
print(f"Bird needs to travel: {env.pipes[0]['x'] - env.bird_x} pixels")
print(f"At pipe speed {env.PIPE_SPEED}, that's {(env.pipes[0]['x'] - env.bird_x) / env.PIPE_SPEED:.0f} frames")
print(f"Bird free-falls for ~31 frames before hitting ground\n")

# Simple test: manually advance time
for step in range(200):
    obs, reward, terminated, truncated, info = env.step(0)

    if env.pipes:
        pipe = env.pipes[0]
        if step % 20 == 0:
            print(f"Step {step}: Bird at x={env.bird_x:.0f}, Pipe at x={pipe['x']:.0f}, Scored={pipe['scored']}")

    if terminated:
        print(f"\nTerminated at step {step}, bird y={env.bird_y:.0f}")
        break
