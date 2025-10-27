# Architecture Notes – Bot C Flappy Bird Agent

This document captures design choices for Bot C's classical RL agent. Updates will follow as components solidify.

## Component Overview

- **Environment Wrapper:** Local copy of `FlappyBirdEnv` (Gymnasium API) under `environment/` to ensure workspace isolation.
- **Agent Implementation:** Stable-Baselines3 `DQN` with two-layer MLP policy `[256, 256]`, tuned for faster convergence under limited timestep budget.
- **Training Script (`training/train_dqn.py`):**
  - Builds monitored train/eval environments with session-specific log directories.
  - Configures callbacks (checkpoint + evaluation) to persist intermediate performance without long training horizon.
  - Supports CLI arguments for timesteps, seed, evaluation episodes.
  - Persists best model to `models/dqn_session/best_model.zip`.
- **Results Logging:** Stores Monitor outputs plus tensorboard traces under `results/` for reproducibility. Post-training evaluation prints score and reward statistics.

## Key Design Decisions

1. **Reduced Buffer Size (50k) & Elevated Exploration Fraction (0.3):** Balances sample diversity with manageable memory to match shorter wall-clock allowance.
2. **Checkpoint Frequency (20k) & Eval Frequency (10k):** Provides 2–3 evaluation points within 120k timetable while avoiding overhead.
3. **Deterministic Post-Training Evaluation:** Manual loop records game `score` per episode; SB3 helper captures reward aggregates for documentation.

## Pending Adjustments

- Confirm whether prioritized replay adds value given time constraints (currently uniform for simplicity).
- Experiment with timesteps up to 180k if runtime permits without exceeding session window.
- Attach plotting utility for reward curve in `results/` if time remains after final evaluation.
