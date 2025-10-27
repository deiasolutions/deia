"""
Flappy Bird Gymnasium Environment
Ported from flappy-gerald.html game mechanics
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np


class FlappyBirdEnv(gym.Env):
    """Gymnasium environment for Flappy Bird"""

    metadata = {'render_modes': ['rgb_array'], 'render_fps': 60}

    def __init__(self, render_mode=None):
        super().__init__()

        # Game constants (from flappy-gerald.html)
        self.CANVAS_WIDTH = 400
        self.CANVAS_HEIGHT = 600
        self.GRAVITY = 0.5
        self.FLAP_POWER = -10
        self.PIPE_SPEED = 3
        self.PIPE_GAP = 150
        self.PIPE_WIDTH = 60
        self.BIRD_SIZE = 30
        self.GROUND_HEIGHT = 50
        self.PIPE_SPAWN_INTERVAL = 90  # frames

        # Action space: 0 = do nothing, 1 = flap
        self.action_space = spaces.Discrete(2)

        # Observation space: [bird_y, bird_velocity, next_pipe_x, next_pipe_gap_y]
        # Normalized values for better learning
        self.observation_space = spaces.Box(
            low=np.array([0, -15, 0, 0], dtype=np.float32),
            high=np.array([self.CANVAS_HEIGHT, 15, self.CANVAS_WIDTH, self.CANVAS_HEIGHT], dtype=np.float32),
            dtype=np.float32
        )

        self.render_mode = render_mode

        # Game state
        self.reset()

    def reset(self, seed=None, options=None):
        """Reset environment to initial state"""
        super().reset(seed=seed)

        # Initialize bird
        self.bird_x = 100
        self.bird_y = self.CANVAS_HEIGHT / 2
        self.bird_velocity = 0

        # Initialize pipes
        self.pipes = []
        self.frame_count = 0

        # Create first pipe
        self._create_pipe()

        # Score
        self.score = 0

        return self._get_observation(), {}

    def step(self, action):
        """Execute one timestep"""
        # Apply action (flap or not)
        if action == 1:
            self.bird_velocity = self.FLAP_POWER

        # Physics: gravity
        self.bird_velocity += self.GRAVITY
        self.bird_y += self.bird_velocity

        # Generate pipes
        if self.frame_count % self.PIPE_SPAWN_INTERVAL == 0:
            self._create_pipe()

        # Update and check pipes
        reward = 1.0  # IMPROVED: Reward for surviving each frame (was 0.1)
        for i in range(len(self.pipes) - 1, -1, -1):
            pipe = self.pipes[i]
            pipe['x'] -= self.PIPE_SPEED

            # Score point when passing pipe
            if not pipe['scored'] and pipe['x'] + self.PIPE_WIDTH < self.bird_x:
                pipe['scored'] = True
                self.score += 1
                reward = 100  # IMPROVED: Major reward for passing pipe (was 10)

            # Remove off-screen pipes
            if pipe['x'] + self.PIPE_WIDTH < 0:
                self.pipes.pop(i)

        # Check collision
        terminated = self._check_collision()

        if terminated:
            reward = -500  # IMPROVED: Harsh penalty for dying (was -100)

        self.frame_count += 1

        info = {
            'score': self.score,
            'bird_y': self.bird_y,
            'bird_velocity': self.bird_velocity
        }

        return self._get_observation(), reward, terminated, False, info

    def _get_observation(self):
        """Get current state observation"""
        # Find next pipe
        next_pipe = None
        for pipe in self.pipes:
            if pipe['x'] + self.PIPE_WIDTH > self.bird_x:
                next_pipe = pipe
                break

        if next_pipe is None:
            # No pipes ahead (shouldn't happen normally)
            next_pipe_x = self.CANVAS_WIDTH
            next_pipe_gap_y = self.CANVAS_HEIGHT / 2
        else:
            next_pipe_x = next_pipe['x']
            next_pipe_gap_y = next_pipe['gap_y']

        return np.array([
            self.bird_y,
            self.bird_velocity,
            next_pipe_x - self.bird_x,  # Relative distance
            next_pipe_gap_y
        ], dtype=np.float32)

    def _create_pipe(self):
        """Create new pipe"""
        min_gap_y = 100
        max_gap_y = self.CANVAS_HEIGHT - self.PIPE_GAP - 100
        gap_y = self.np_random.uniform(min_gap_y, max_gap_y)

        self.pipes.append({
            'x': self.CANVAS_WIDTH,
            'gap_y': gap_y,
            'scored': False
        })

    def _check_collision(self):
        """Check if bird collided with pipes or boundaries"""
        # Hit ground or ceiling
        if (self.bird_y + self.BIRD_SIZE / 2 >= self.CANVAS_HEIGHT - self.GROUND_HEIGHT or
            self.bird_y - self.BIRD_SIZE / 2 <= 0):
            return True

        # Hit pipe
        for pipe in self.pipes:
            if (self.bird_x + self.BIRD_SIZE / 2 > pipe['x'] and
                self.bird_x - self.BIRD_SIZE / 2 < pipe['x'] + self.PIPE_WIDTH):
                # Bird is horizontally aligned with pipe
                if (self.bird_y - self.BIRD_SIZE / 2 < pipe['gap_y'] or
                    self.bird_y + self.BIRD_SIZE / 2 > pipe['gap_y'] + self.PIPE_GAP):
                    return True

        return False

    def render(self):
        """Return game state for visualization"""
        if self.render_mode != 'rgb_array':
            return None

        return {
            'bird_x': self.bird_x,
            'bird_y': self.bird_y,
            'bird_velocity': self.bird_velocity,
            'pipes': self.pipes,
            'score': self.score,
            'canvas_width': self.CANVAS_WIDTH,
            'canvas_height': self.CANVAS_HEIGHT,
            'bird_size': self.BIRD_SIZE,
            'pipe_width': self.PIPE_WIDTH,
            'pipe_gap': self.PIPE_GAP,
            'ground_height': self.GROUND_HEIGHT
        }

    def close(self):
        """Clean up"""
        pass
