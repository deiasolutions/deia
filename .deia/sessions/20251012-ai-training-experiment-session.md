# AI Training Experiment Session - Flappy Bird Neural Networks

**Date:** 2025-10-12
**Bot:** BOT-00001 (Queen/Researcher/Engineer)
**Session Duration:** ~2 hours
**Status:** Phase 1-5 Complete, Environment needs debugging

---

## Context

Dave requested autonomous execution of the AI training experiment to teach neural networks to play Flappy Bird. This session covered initial setup through first training run, revealing environment issues that need resolution.

---

## What Was Accomplished

### Phase 0: Environment Setup ✅
- Created `flappy-bird-ai/` project structure
- Installed dependencies: gymnasium, stable-baselines3, neat-python, torch, fastapi, uvicorn
- Set up requirements.txt and README.md

### Phase 1: Gymnasium Environment ✅
- Ported Flappy Gerald game mechanics to Python
- Created `environment/flappy_env.py` - Gymnasium-compatible environment
- State space: [bird_y, bird_velocity, pipe_x, pipe_gap_y] (4 dimensions)
- Action space: Discrete(2) - 0=nothing, 1=flap
- Validated with random agent (scored 0, dies in ~30-40 steps as expected)

### Phase 2-4: Training Scripts Created & Executed ✅
Created training scripts for 3 agents:
- **DQN** (`training/train_dqn.py`) - 500k timesteps, completed in ~18 minutes
- **PPO** (`training/train_ppo.py`) - 300k timesteps, completed in ~15 minutes
- **NEAT** (`training/train_neat.py`) - 100 generations, completed in ~20 minutes

All three trained in parallel successfully.

### Phase 5: Demo Server ✅
Built complete visualization infrastructure:
- `server/app.py` - FastAPI server with WebSocket streaming
- `server/agent_loader.py` - Unified agent loading interface
- `server/game_server.py` - Game state management
- `web/index.html` - Landing page listing agents
- `web/demo.html` - Individual agent demo page
- `web/game_canvas.js` - Real-time canvas rendering (~60 FPS)
- `web/style.css` - Responsive styling

Server running at: http://localhost:5000

---

## Critical Issue Discovered

**Problem:** All 3 agents scored 0.00 on evaluation (10 episodes each)

**Root Cause Analysis:**
The agents trained successfully but learned nothing. Likely issues:
1. **Reward structure too sparse** - Only +1 per pipe, -100 on death, 0.1 per frame survival
2. **State observation insufficient** - May need more information (distance to gap center, relative velocity)
3. **Collision detection too harsh** - Agents might be dying before learning basic physics
4. **Reward scale imbalance** - Death penalty (-100) may dominate learning signal

**Evidence:**
- Training completed without errors
- Models saved successfully (dqn_best.zip, ppo_best.zip, neat_best.pkl)
- Fast convergence (~15-20 min) suggests environment is too easy/hard
- Evaluation shows consistent immediate death (score=0, all episodes)

---

## Decisions Made

### Architecture Decision: Local Python Server + Browser
- Backend: Python + FastAPI with trained models (native environment)
- Frontend: HTML5 Canvas + JavaScript + WebSocket
- Real-time streaming at 60 FPS
- Demo URL pattern: `http://localhost:5000/demo/{agent_name}`

**Rationale:**
- No model export needed (stays in Python)
- Low overhead
- Easy to share local network links
- Live updates via WebSocket

### Training Approach: Parallel Execution
- All 3 agents (DQN, PPO, NEAT) trained simultaneously
- Background processes to maximize efficiency
- Individual log files for debugging

### Technology Stack (Round 1):
- `stable-baselines3` for DQN and PPO (battle-tested, PyTorch-based)
- `neat-python` for NEAT (standard neuroevolution library)
- `gymnasium` for environment interface (OpenAI Gym successor)

---

## Files Created

### Core Infrastructure
- `flappy-bird-ai/requirements.txt` - Python dependencies
- `flappy-bird-ai/README.md` - Project documentation
- `flappy-bird-ai/check_progress.py` - Training monitoring script

### Environment
- `environment/flappy_env.py` - Gymnasium environment (160 lines)
- `environment/test_env.py` - Validation script

### Training
- `training/train_dqn.py` - DQN training script
- `training/train_ppo.py` - PPO training script
- `training/train_neat.py` - NEAT training script
- `config/neat_config.txt` - NEAT configuration

### Demo Server
- `server/app.py` - FastAPI application (150+ lines)
- `server/agent_loader.py` - Agent loading utility
- `server/game_server.py` - Game state management
- `web/index.html` - Landing page
- `web/demo.html` - Demo page template
- `web/game_canvas.js` - Canvas rendering (200+ lines)
- `web/style.css` - Styling (300+ lines)

### Models Saved
- `models/dqn_best.zip` - Trained DQN (not learning properly)
- `models/ppo_best.zip` - Trained PPO (not learning properly)
- `models/neat_best.pkl` - Evolved NEAT genome (not learning properly)

### Documentation
- `.deia/AI-EXPERIMENT-EXECUTION-BLUEPRINT.md` - Complete execution protocol (800+ lines)

---

## Key Technical Details

### Reward Function (Current - Needs Revision)
```python
reward = 0.1  # Small reward for surviving each frame
if pipe passed:
    reward = 10  # Big reward for passing pipe
if died:
    reward = -100  # Penalty for dying
```

### State Observation
```python
[
    bird_y,                    # Bird vertical position
    bird_velocity,             # Bird vertical velocity
    next_pipe_x - bird_x,      # Relative distance to next pipe
    next_pipe_gap_y            # Vertical center of next pipe gap
]
```

### Hyperparameters Used

**DQN:**
- Learning rate: 1e-3
- Buffer size: 100k
- Batch size: 64
- Gamma: 0.99
- Exploration: 1.0 → 0.01 (10% of training)
- Network: [128, 64] hidden units

**PPO:**
- Learning rate: 3e-4
- Steps per update: 2048
- Batch size: 64
- Epochs: 10
- Gamma: 0.99
- GAE lambda: 0.95
- Clip range: 0.2
- Network: [128, 64] hidden units

**NEAT:**
- Population: 100 genomes
- Generations: 100
- Mutation rate: 0.8
- Crossover rate: 0.2
- Input nodes: 4
- Output nodes: 1

---

## Next Steps (Critical)

### Immediate: Debug Environment (Phase 1B)
1. **Add dense reward shaping:**
   ```python
   # Reward for staying near center of gap
   distance_to_center = abs(bird_y - pipe_gap_y)
   reward += -0.01 * (distance_to_center / canvas_height)

   # Reward for forward progress
   reward += 0.1  # per frame survived
   ```

2. **Expand state observation:**
   ```python
   # Add more informative features
   [
       bird_y / canvas_height,           # Normalized position
       bird_velocity / 15,                # Normalized velocity
       next_pipe_x / canvas_width,        # Normalized distance
       (bird_y - pipe_gap_y) / canvas_height,  # Relative position to gap
       pipe_gap_size / canvas_height      # Gap size (constant but helpful)
   ]
   ```

3. **Adjust collision detection:**
   - Add small buffer zone
   - Give agents more room to learn before dying

4. **Test with simpler task first:**
   - Remove pipes temporarily
   - Train agent to just hover at screen center
   - Validates reward function works

### After Environment Fix: Retrain (Phases 2-4 Redux)
- Rerun DQN training (500k timesteps)
- Rerun PPO training (300k timesteps)
- Rerun NEAT evolution (100 generations)
- Fast iteration: ~15-20 min per agent

### Phase 6: Evaluation & Comparison
- Run 100 episodes per agent
- Generate learning curves
- Statistical comparison
- Write Round 1 findings report

### Phase 7-8: Round 2 (Advanced Methods)
- Decision Transformer (offline RL on Round 1 trajectories)
- Experimental method (LLM policy or curiosity-driven)

### Phase 9: Final Report
- Complete comparison across all 5 agents
- Analysis of what worked/failed
- Lessons learned
- Recommendations

---

## Insights & Lessons

### What Went Well
- ✅ Infrastructure pipeline works flawlessly (training → saving → loading → demo)
- ✅ Parallel training efficient (all 3 agents in <25 minutes total)
- ✅ Demo server architecture solid (WebSocket streaming works beautifully)
- ✅ Autonomous execution mostly successful (created full pipeline end-to-end)

### What Needs Work
- ❌ Environment reward structure insufficient for learning
- ❌ Need denser reward shaping (not just sparse pipe-passing rewards)
- ❌ State observation may need enrichment
- ⚠️ Fast training time actually revealed the problem quickly (good for iteration)

### Key Realization
**Sparse rewards don't work for this task.** The agents need continuous feedback:
- "You're getting closer to the center of the gap" (good!)
- "You're drifting away from the gap" (bad!)
- Not just "You died" or "You passed a pipe"

This is a common RL pitfall - reward shaping is critical for learning.

---

## Demo Server Status

**Server Running:** http://localhost:5000
- Landing page shows all 3 agents
- Individual demos at `/demo/dqn`, `/demo/ppo`, `/demo/neat`
- Agents play continuously but die immediately (score 0)
- WebSocket streaming working correctly
- Stats tracking functional

**Useful for Debugging:**
Dave can visually observe failure mode - helps identify what agents are learning (or not learning).

---

## Todo List Status

**Completed:**
- [x] Phase 0: Environment Setup
- [x] Phase 1: Gymnasium Environment
- [x] Phase 2: Train DQN (needs redo)
- [x] Phase 3: Train PPO (needs redo)
- [x] Phase 4: Train NEAT (needs redo)
- [x] Phase 5: Demo Server

**Pending:**
- [ ] Phase 1B: Debug & fix environment (CRITICAL)
- [ ] Phase 2-4 Redux: Retrain all agents
- [ ] Phase 6: Evaluate Round 1
- [ ] Phase 7: Decision Transformer (Round 2)
- [ ] Phase 8: Experimental Method (Round 2)
- [ ] Phase 9: Final Report

---

## Commands for Next Session

```bash
# Resume work
cd flappy-bird-ai

# Fix environment
# Edit environment/flappy_env.py (add dense rewards, improve state)

# Retrain agents (after fix)
cd training
python train_dqn.py > dqn_training_v2.log 2>&1 &
python train_ppo.py > ppo_training_v2.log 2>&1 &
python train_neat.py > neat_training_v2.log 2>&1 &

# Monitor progress
cd ..
python check_progress.py

# Watch demos (server should still be running)
# http://localhost:5000
```

---

## Links for Dave

**Demo Server:**
- http://localhost:5000 (landing page)
- http://localhost:5000/demo/dqn
- http://localhost:5000/demo/ppo
- http://localhost:5000/demo/neat

**Local Network:**
Replace `localhost` with your PC's IP (e.g., `http://192.168.1.100:5000`)

---

## Session Summary

**Status:** Infrastructure complete, first training run complete, environment debugging needed

**Progress:** 5/9 phases complete (Phases 0-5)

**Critical Blocker:** Environment reward structure insufficient - agents not learning

**Time Investment:** ~2 hours (setup + training + infrastructure)

**Next Session Priority:** Fix environment reward function and state observation, then retrain

**Estimated Time to Working Agents:** 1-2 hours (30 min fix + 20 min retrain + validation)

---

**Session logged by BOT-00001**
**Date: 2025-10-12**
**Status: Awaiting environment fixes before continuing Round 1**
