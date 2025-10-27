"""
Flappy Bird Gymnasium Environment - IMPROVED VERSION
Ported from flappy-gerald.html game mechanics
Refactored with B1/B2 improvements for better agent learning
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np


class FlappyBirdEnv(gym.Env):
    """Gymnasium environment for Flappy Bird - Improved for Agent Learning"""

    metadata = {'render_modes': ['rgb_array'], 'render_fps': 60}

    def __init__(self, render_mode=None, max_episode_steps=500):
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
        self.PIPE_SPAWN_INTERVAL = 70  # FIX: Reduced from 90 for more frequent pipes
        self.MAX_EPISODE_STEPS = max_episode_steps  # FIX: Episode time limit

        # Action space: 0 = do nothing, 1 = flap
        self.action_space = spaces.Discrete(2)

        # FIX: Observation space with corrected bounds
        # [bird_y, bird_velocity, relative_pipe_x, pipe_gap_y, pipe_bottom_y]
        # relative_pipe_x can now be negative (pipe behind bird), so adjust low bound
        self.observation_space = spaces.Box(
            low=np.array([0, -15, -self.CANVAS_WIDTH, 0, 0], dtype=np.float32),
            high=np.array([self.CANVAS_HEIGHT, 15, self.CANVAS_WIDTH, self.CANVAS_HEIGHT, self.CANVAS_HEIGHT], dtype=np.float32),
            dtype=np.float32
        )

        self.render_mode = render_mode

        # Game state
        self.reset()

    def reset(self, seed=None, options=None):
        """Reset environment to initial state"""
        super().reset(seed=seed)

        # FIX: Move bird forward so it encounters pipes before falling
        self.bird_x = 50  # Changed from 100 (was too far back)
        self.bird_y = self.CANVAS_HEIGHT / 2
        self.bird_velocity = 0

        # Initialize pipes
        self.pipes = []
        self.frame_count = 0

        # FIX: Spawn first pipe closer so bird encounters it before dying
        # Create first pipe at closer distance
        self._create_pipe_initial()

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

        # FIX: Rebalanced reward system for better learning
        reward = 0.1  # Small reward for surviving (was 1.0 - too high)

        for i in range(len(self.pipes) - 1, -1, -1):
            pipe = self.pipes[i]
            pipe['x'] -= self.PIPE_SPEED

            # PHASE 2 FIX: Add proximity reward when approaching pipe gap
            # If pipe is nearby and we're in safe zone, small positive reward
            if not pipe['scored'] and pipe['x'] > self.bird_x - 100:  # Within 100 pixels
                # Check if bird is within the safe zone of this pipe
                if (self.bird_y - self.BIRD_SIZE/2 >= pipe['gap_y'] and
                    self.bird_y + self.BIRD_SIZE/2 <= pipe['gap_y'] + self.PIPE_GAP):
                    reward += 0.5  # Proximity bonus for being safe near pipe

            # Score point when passing pipe
            if not pipe['scored'] and pipe['x'] + self.PIPE_WIDTH < self.bird_x:
                pipe['scored'] = True
                self.score += 1
                reward = 20  # Pipe reward (was 100 - destabilizing)

            # Remove off-screen pipes
            if pipe['x'] + self.PIPE_WIDTH < 0:
                self.pipes.pop(i)

        # Check collision
        terminated = self._check_collision()

        if terminated:
            reward = -50  # Death penalty (was -500 - dominated learning)

        # FIX: Episode termination on max steps
        self.frame_count += 1
        if self.frame_count >= self.MAX_EPISODE_STEPS:
            terminated = True

        info = {
            'score': self.score,
            'bird_y': self.bird_y,
            'bird_velocity': self.bird_velocity,
            'frame': self.frame_count
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
            # No pipes ahead - use default
            next_pipe_x = self.CANVAS_WIDTH
            next_pipe_gap_y = self.CANVAS_HEIGHT / 2
            next_pipe_bottom_y = self.CANVAS_HEIGHT / 2 + self.PIPE_GAP
        else:
            next_pipe_x = next_pipe['x']
            next_pipe_gap_y = next_pipe['gap_y']
            next_pipe_bottom_y = next_pipe['gap_y'] + self.PIPE_GAP

        # FIX: Clamp relative_x to valid range within observation bounds
        relative_x = next_pipe_x - self.bird_x
        relative_x = np.clip(relative_x, -self.CANVAS_WIDTH, self.CANVAS_WIDTH)

        # FIX: Enhanced observation with pipe bottom boundary
        return np.array([
            self.bird_y,
            self.bird_velocity,
            relative_x,  # Now properly bounded
            next_pipe_gap_y,
            next_pipe_bottom_y
        ], dtype=np.float32)

    def _create_pipe_initial(self):
        """Create first pipe at reasonable distance"""
        # FIX: First pipe should spawn closer so bird can reach it before falling
        # Distance should be < 100 frames * 3 pixels/frame so bird encounters it early
        min_gap_y = 80
        max_gap_y = self.CANVAS_HEIGHT - self.PIPE_GAP - 80
        gap_y = self.np_random.uniform(min_gap_y, max_gap_y)

        # Spawn closer - bird at x=50, pipe at x=200 gives 150/(3 speed) = 50 frames
        self.pipes.append({
            'x': 200,  # Much closer than 400
            'gap_y': gap_y,
            'scored': False
        })

    def _create_pipe(self):
        """Create new pipe"""
        # FIX: Better gap positioning - ensure gaps are more accessible
        # Instead of spreading across full height, center around playable zone
        min_gap_y = 80  # Tighter minimum
        max_gap_y = self.CANVAS_HEIGHT - self.PIPE_GAP - 80  # Tighter maximum
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
