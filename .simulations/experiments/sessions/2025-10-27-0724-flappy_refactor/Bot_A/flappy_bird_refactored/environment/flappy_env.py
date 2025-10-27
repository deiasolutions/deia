"""
Flappy Bird Gymnasium Environment - REFACTORED
Ported from flappy-gerald.html game mechanics
Improvements: Fixed reward system, added gap size to observation, made parameters configurable, improved physics
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np


class FlappyBirdEnv(gym.Env):
    """Gymnasium environment for Flappy Bird - REFACTORED VERSION"""

    metadata = {'render_modes': ['rgb_array'], 'render_fps': 60}

    def __init__(self, render_mode=None,
                 gravity=0.5, flap_power=-10, pipe_speed=3, pipe_gap=150,
                 max_steps=1000, seed=None):
        """
        Initialize Flappy Bird environment with configurable parameters.

        Args:
            render_mode: Rendering mode ('rgb_array' or None)
            gravity: Acceleration due to gravity (default 0.5)
            flap_power: Upward velocity when flapping (default -10)
            pipe_speed: Pixels per frame pipes move (default 3)
            pipe_gap: Gap size between pipe top and bottom (default 150)
            max_steps: Maximum steps per episode (default 1000)
            seed: Random seed
        """
        super().__init__()

        # Game constants (from flappy-gerald.html) - now configurable
        self.CANVAS_WIDTH = 400
        self.CANVAS_HEIGHT = 600
        self.GRAVITY = gravity
        self.FLAP_POWER = flap_power
        self.PIPE_SPEED = pipe_speed
        self.PIPE_GAP = pipe_gap
        self.PIPE_WIDTH = 60
        self.BIRD_SIZE = 30
        self.GROUND_HEIGHT = 50
        self.PIPE_SPAWN_INTERVAL = 90  # frames between pipe spawns
        self.MAX_STEPS = max_steps  # NEW: Episode length limit

        # Reward configuration - optimized for learning
        self.REWARD_SURVIVAL = 0.1  # Small reward each frame for staying alive
        self.REWARD_PIPE_PASS = 10.0  # Reward for successfully passing pipe
        self.REWARD_COLLISION = -1.0  # Penalty for collision (less harsh than before)
        self.REWARD_NEAR_CENTER = 0.5  # Bonus for being near pipe center

        # Action space: 0 = do nothing, 1 = flap
        self.action_space = spaces.Discrete(2)

        # Observation space: [bird_y, bird_velocity, next_pipe_x, gap_y, gap_size, gap_center_offset]
        # All normalized for better learning
        self.observation_space = spaces.Box(
            low=np.array([0, -15, 0, 0, 0, -1], dtype=np.float32),
            high=np.array([self.CANVAS_HEIGHT, 15, self.CANVAS_WIDTH, self.CANVAS_HEIGHT, self.CANVAS_HEIGHT, 1], dtype=np.float32),
            dtype=np.float32
        )

        self.render_mode = render_mode

        # Game state
        self.reset(seed=seed)

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
        self.steps = 0  # NEW: Track episode steps

        # Create first pipe
        self._create_pipe()

        # Score
        self.score = 0
        self.last_pipe_score = None  # Track which pipe we last scored

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
        reward = self.REWARD_SURVIVAL  # Small reward for surviving each frame
        for i in range(len(self.pipes) - 1, -1, -1):
            pipe = self.pipes[i]
            pipe['x'] -= self.PIPE_SPEED

            # FIX: Reward when bird PASSES THROUGH pipe safely (after exiting right side)
            # This gives immediate feedback when navigating through the gap
            if not pipe['scored']:
                # Check if bird has safely passed the right edge of the pipe
                if self.bird_x > pipe['x'] + self.PIPE_WIDTH:
                    # Bird is past the pipe - check if it was in safe zone
                    gap_top = pipe['gap_y']
                    gap_bottom = pipe['gap_y'] + self.PIPE_GAP

                    if gap_top < self.bird_y < gap_bottom:
                        # Bird safely passed through the gap
                        reward += self.REWARD_PIPE_PASS
                        pipe['scored'] = True
                        self.score += 1

            # Remove off-screen pipes
            if pipe['x'] + self.PIPE_WIDTH < 0:
                self.pipes.pop(i)

        # Check collision
        terminated = self._check_collision()

        if terminated:
            reward = self.REWARD_COLLISION  # Penalty for dying

        # Increment steps BEFORE checking max_steps
        self.steps += 1

        # Check episode termination by max steps
        truncated = self.steps >= self.MAX_STEPS
        if truncated:
            reward = self.REWARD_SURVIVAL  # Neutral termination

        self.frame_count += 1

        info = {
            'score': self.score,
            'bird_y': self.bird_y,
            'bird_velocity': self.bird_velocity,
            'steps': self.steps
        }

        return self._get_observation(), reward, terminated, truncated, info

    def _get_observation(self):
        """
        Get current state observation.
        Returns: [bird_y, bird_velocity, next_pipe_distance, gap_y, gap_size, gap_center_offset]
        """
        # Find next pipe
        next_pipe = None
        for pipe in self.pipes:
            if pipe['x'] + self.PIPE_WIDTH > self.bird_x:
                next_pipe = pipe
                break

        if next_pipe is None:
            # No pipes ahead - provide safe default
            next_pipe_x = self.CANVAS_WIDTH
            next_pipe_distance = self.CANVAS_WIDTH
            gap_y = self.CANVAS_HEIGHT / 2
            gap_size = self.PIPE_GAP
            gap_center = self.CANVAS_HEIGHT / 2
        else:
            next_pipe_x = next_pipe['x']
            next_pipe_distance = next_pipe_x - self.bird_x
            gap_y = next_pipe['gap_y']
            gap_size = self.PIPE_GAP
            gap_center = gap_y + self.PIPE_GAP / 2

        # FIX: Add gap_size to observation for state completeness
        # FIX: Make gap_center relative to bird for easier learning
        gap_center_offset = (gap_center - self.bird_y) / self.CANVAS_HEIGHT
        gap_size_normalized = gap_size / self.CANVAS_HEIGHT

        return np.array([
            self.bird_y,
            self.bird_velocity,
            next_pipe_distance,  # Relative distance to pipe
            gap_y,  # Absolute gap position
            gap_size_normalized,  # Gap size normalized
            gap_center_offset  # Relative gap center
        ], dtype=np.float32)

    def _create_pipe(self):
        """Create new pipe with random gap position"""
        min_gap_y = 100
        max_gap_y = self.CANVAS_HEIGHT - self.PIPE_GAP - 100
        gap_y = self.np_random.uniform(min_gap_y, max_gap_y)

        self.pipes.append({
            'x': self.CANVAS_WIDTH,
            'gap_y': gap_y,
            'scored': False
        })

    def _check_collision(self):
        """
        Check if bird collided with pipes or boundaries.
        Uses proper collision detection with bird size.
        """
        # Hit ground or ceiling
        if (self.bird_y + self.BIRD_SIZE / 2 >= self.CANVAS_HEIGHT - self.GROUND_HEIGHT or
            self.bird_y - self.BIRD_SIZE / 2 <= 0):
            return True

        # Hit pipe
        for pipe in self.pipes:
            # Check horizontal overlap with pipe
            if (self.bird_x + self.BIRD_SIZE / 2 > pipe['x'] and
                self.bird_x - self.BIRD_SIZE / 2 < pipe['x'] + self.PIPE_WIDTH):
                # Bird is horizontally aligned with pipe
                # Check if bird is outside the gap vertically
                gap_top = pipe['gap_y']
                gap_bottom = pipe['gap_y'] + self.PIPE_GAP

                if (self.bird_y - self.BIRD_SIZE / 2 < gap_top or
                    self.bird_y + self.BIRD_SIZE / 2 > gap_bottom):
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
            'ground_height': self.GROUND_HEIGHT,
            'steps': self.steps,
            'max_steps': self.MAX_STEPS
        }

    def close(self):
        """Clean up"""
        pass
