"""
Flappy Bird Gymnasium Environment - TRAINING REFERENCE
Ported from flappy-gerald.html game mechanics
This is the canonical version for training bots to refactor game code.

Design Goals:
- Production-ready game implementation
- Clear, refactorable code structure
- Balanced for RL agent training
- Normalized observation space for stable learning
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np


class FlappyBirdEnv(gym.Env):
    """Gymnasium environment for Flappy Bird - Training Reference Version"""

    metadata = {'render_modes': ['rgb_array'], 'render_fps': 60}

    def __init__(self, render_mode=None,
                 gravity=0.5, flap_power=-10, pipe_speed=3, pipe_gap=150,
                 max_episode_steps=500, seed=None):
        """
        Initialize Flappy Bird environment with configurable parameters.

        Args:
            render_mode: Rendering mode ('rgb_array' or None)
            gravity: Acceleration due to gravity (default 0.5)
            flap_power: Upward velocity when flapping (default -10)
            pipe_speed: Pixels per frame pipes move (default 3)
            pipe_gap: Gap size between pipe top and bottom (default 150)
            max_episode_steps: Maximum steps per episode (default 500)
            seed: Random seed for reproducibility
        """
        super().__init__()

        # Game constants
        self.CANVAS_WIDTH = 400
        self.CANVAS_HEIGHT = 600
        self.GRAVITY = gravity
        self.FLAP_POWER = flap_power
        self.PIPE_SPEED = pipe_speed
        self.PIPE_GAP = pipe_gap
        self.PIPE_WIDTH = 60
        self.BIRD_SIZE = 30
        self.GROUND_HEIGHT = 50
        self.PIPE_SPAWN_INTERVAL = 70  # frames between pipe spawns
        self.MAX_EPISODE_STEPS = max_episode_steps

        # Reward configuration - optimized for stable RL training
        self.REWARD_SURVIVAL = 0.1  # Small reward each frame for staying alive
        self.REWARD_PIPE_PASS = 20.0  # Reward for successfully passing pipe
        self.REWARD_COLLISION = -50.0  # Penalty for collision
        self.REWARD_PROXIMITY = 0.5  # Bonus for being near pipe center

        # Action space: 0 = do nothing, 1 = flap
        self.action_space = spaces.Discrete(2)

        # Observation space: ALL NORMALIZED TO [-1, 1]
        # [bird_y_norm, bird_vel_norm, pipe_dist_norm, gap_center_offset, gap_size_norm]
        self.observation_space = spaces.Box(
            low=np.array([-1, -1, -1, -1, -1], dtype=np.float32),
            high=np.array([1, 1, 1, 1, 1], dtype=np.float32),
            dtype=np.float32
        )

        self.render_mode = render_mode
        self.reset(seed=seed)

    def reset(self, seed=None, options=None):
        """Reset environment to initial state"""
        super().reset(seed=seed)

        # Initialize bird (positioned to encounter pipes quickly)
        self.bird_x = 50
        self.bird_y = self.CANVAS_HEIGHT / 2
        self.bird_velocity = 0

        # Initialize pipes
        self.pipes = []
        self.frame_count = 0
        self.episode_steps = 0

        # Create first pipe closer for early learning signal
        self._create_pipe_initial()

        # Score tracking
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

        # Base survival reward
        reward = self.REWARD_SURVIVAL

        # Update and check pipes
        for i in range(len(self.pipes) - 1, -1, -1):
            pipe = self.pipes[i]
            pipe['x'] -= self.PIPE_SPEED

            # Proximity reward: bonus for being safely near pipe gap
            if not pipe['scored'] and pipe['x'] > self.bird_x - 100:
                gap_top = pipe['gap_y']
                gap_bottom = pipe['gap_y'] + self.PIPE_GAP
                if gap_top < self.bird_y < gap_bottom:
                    reward += self.REWARD_PROXIMITY

            # Score point when passing pipe
            if not pipe['scored'] and pipe['x'] + self.PIPE_WIDTH < self.bird_x:
                pipe['scored'] = True
                self.score += 1
                reward = self.REWARD_PIPE_PASS

            # Remove off-screen pipes
            if pipe['x'] + self.PIPE_WIDTH < 0:
                self.pipes.pop(i)

        # Check collision
        terminated = self._check_collision()

        if terminated:
            reward = self.REWARD_COLLISION

        # Increment step counters
        self.frame_count += 1
        self.episode_steps += 1

        # Check episode termination by max steps
        truncated = self.episode_steps >= self.MAX_EPISODE_STEPS

        info = {
            'score': self.score,
            'bird_y': self.bird_y,
            'bird_velocity': self.bird_velocity,
            'frame': self.frame_count,
            'episode_steps': self.episode_steps
        }

        return self._get_observation(), reward, terminated, truncated, info

    def _get_observation(self):
        """
        Get current state observation.
        All values normalized to [-1, 1] range for stable RL training.

        Returns: [bird_y_norm, bird_vel_norm, pipe_dist_norm, gap_center_offset, gap_size_norm]
        """
        # Find next pipe ahead of bird
        next_pipe = None
        for pipe in self.pipes:
            if pipe['x'] + self.PIPE_WIDTH > self.bird_x:
                next_pipe = pipe
                break

        if next_pipe is None:
            # No pipes ahead - provide safe default values
            next_pipe_x = self.CANVAS_WIDTH
            gap_y = self.CANVAS_HEIGHT / 2
        else:
            next_pipe_x = next_pipe['x']
            gap_y = next_pipe['gap_y']

        # Calculate gap center
        gap_center = gap_y + self.PIPE_GAP / 2

        # Normalize all observations to [-1, 1]
        bird_y_norm = (self.bird_y - self.CANVAS_HEIGHT / 2) / (self.CANVAS_HEIGHT / 2)
        bird_vel_norm = self.bird_velocity / 15.0
        pipe_dist_norm = (next_pipe_x - self.bird_x - self.CANVAS_WIDTH / 2) / (self.CANVAS_WIDTH / 2)
        gap_center_offset = (gap_center - self.bird_y) / self.CANVAS_HEIGHT
        gap_size_norm = (self.PIPE_GAP / self.CANVAS_HEIGHT) * 2 - 1

        # Ensure all values stay within bounds
        return np.array([
            np.clip(bird_y_norm, -1, 1),
            np.clip(bird_vel_norm, -1, 1),
            np.clip(pipe_dist_norm, -1, 1),
            np.clip(gap_center_offset, -1, 1),
            np.clip(gap_size_norm, -1, 1)
        ], dtype=np.float32)

    def _create_pipe_initial(self):
        """Create first pipe at reasonable distance for early learning"""
        min_gap_y = 80
        max_gap_y = self.CANVAS_HEIGHT - self.PIPE_GAP - 80
        gap_y = self.np_random.uniform(min_gap_y, max_gap_y)

        # Spawn at x=200: with bird at x=50 and speed=3, reaches in ~50 frames
        self.pipes.append({
            'x': 200,
            'gap_y': gap_y,
            'scored': False
        })

    def _create_pipe(self):
        """Create new pipe with random gap position"""
        min_gap_y = 80
        max_gap_y = self.CANVAS_HEIGHT - self.PIPE_GAP - 80
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
            'episode_steps': self.episode_steps,
            'max_episode_steps': self.MAX_EPISODE_STEPS
        }

    def close(self):
        """Clean up"""
        pass
