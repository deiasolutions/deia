# Flappy Bird Environment Refactoring Spec

When refactoring flappy_env.py, bots should implement these improvements:

## Critical Fixes

1. **Normalize all observations to [-1, 1] range** - Current mixed normalization (raw pixels + normalized values) hurts ML training
2. **Remove redundant `gap_y` observation** - Keep only `gap_center_offset` (relative) + `gap_size_normalized`
3. **Fix observation space bounds** - Currently don't match actual game values (e.g., gap_size_normalized maxes at 0.25, not 1.0)

## Recommended Observation Space (6 values, all normalized):

```
[bird_y_norm, bird_vel_norm, pipe_dist_norm, gap_center_offset, gap_size_norm, episode_progress]
```

- `bird_y_norm`: (bird_y - CANVAS_HEIGHT/2) / (CANVAS_HEIGHT/2) → [-1, 1]
- `bird_vel_norm`: bird_velocity / 15 → [-1, 1]
- `pipe_dist_norm`: (next_pipe_distance - CANVAS_WIDTH/2) / (CANVAS_WIDTH/2) → [-1, 1]
- `gap_center_offset`: (gap_center - bird_y) / CANVAS_HEIGHT → [-1, 1] (already correct)
- `gap_size_norm`: (gap_size / CANVAS_HEIGHT) * 2 - 1 → [-1, 1] (rescaled)
- `episode_progress`: steps / MAX_STEPS → [0, 1]

## Quality Improvements

- Ensure deterministic reset behavior with fixed seeds for testing
- Consider reward signal adjustment: survival reward may dominate vs pipe-passing reward
- Add validation that observations stay within bounds during gameplay

## Context

Original environment analysis identified these issues:
- Observation space bounds mismatch with actual game values
- Mixed normalization (raw pixels + normalized values in same observation)
- Redundant state information
- No episode progress signal for bots
