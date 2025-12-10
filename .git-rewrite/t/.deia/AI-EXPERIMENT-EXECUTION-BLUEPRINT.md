# Flappy Bird AI Experiment - Autonomous Execution Blueprint

**Purpose:** Complete step-by-step protocol for bot to autonomously execute neural network training experiments

**Status:** Ready for execution
**Bot:** BOT-00001 (Queen/Researcher/Engineer)
**Estimated Duration:** 7-10 days (40-50 hours active work + compute time)

---

## Architecture Decision: Demo & Visualization

### Chosen Approach: Local Python Server + Browser Client

**Stack:**
```
Backend:  Python + FastAPI + trained models
Frontend: HTML5 Canvas + JavaScript + WebSocket
Game:     Python (can reuse existing Flappy Gerald HTML logic)
Demo URL: http://localhost:5000/demo/{agent_name}
```

**Why This Approach:**
- ✅ Train agents in native Python environment
- ✅ No model export/conversion needed (TensorFlow.js would add complexity)
- ✅ Real-time visualization via WebSocket
- ✅ Low overhead (FastAPI + simple HTML)
- ✅ Easy to share local network links with Dave
- ✅ Can watch agents play live during/after training

**Architecture:**
```
┌─────────────────┐         WebSocket         ┌──────────────────┐
│   Browser       │◄─────────────────────────►│  FastAPI Server  │
│  (Visualization)│      Game State Stream     │  (Port 5000)     │
└─────────────────┘                            └──────────────────┘
                                                        │
                                                        ▼
                                               ┌──────────────────┐
                                               │  Trained Agent   │
                                               │  (DQN/PPO/NEAT)  │
                                               └──────────────────┘
                                                        │
                                                        ▼
                                               ┌──────────────────┐
                                               │  Flappy Bird Env │
                                               │  (Gymnasium)     │
                                               └──────────────────┘
```

**File Structure:**
```
flappy-bird-ai/
├── environment/
│   ├── flappy_env.py              # Gymnasium environment wrapper
│   └── game_logic.py              # Core game mechanics
├── agents/
│   ├── dqn_agent.py               # DQN implementation (stable-baselines3)
│   ├── ppo_agent.py               # PPO implementation (stable-baselines3)
│   ├── neat_agent.py              # NEAT implementation (neat-python)
│   ├── decision_transformer.py    # Round 2: Decision Transformer (HF)
│   └── experimental.py            # Round 2: Experimental method
├── training/
│   ├── train_dqn.py               # DQN training script
│   ├── train_ppo.py               # PPO training script
│   ├── train_neat.py              # NEAT training script
│   ├── train_dt.py                # Round 2: Decision Transformer
│   └── train_experimental.py     # Round 2: Experimental
├── models/
│   ├── dqn_best.zip               # Saved DQN model
│   ├── ppo_best.zip               # Saved PPO model
│   ├── neat_best.pkl              # Saved NEAT genome
│   ├── dt_best/                   # Saved Decision Transformer
│   └── exp_best/                  # Saved experimental model
├── server/
│   ├── app.py                     # FastAPI server
│   ├── game_server.py             # Game state management + WebSocket
│   └── agent_loader.py            # Load trained models
├── web/
│   ├── index.html                 # Landing page (list all agents)
│   ├── demo.html                  # Demo page for single agent
│   ├── compare.html               # Side-by-side comparison
│   ├── style.css                  # Styling
│   └── game_canvas.js             # Canvas rendering + WebSocket client
├── evaluation/
│   ├── evaluate.py                # Test agents (100 games each)
│   ├── visualize.py               # Generate learning curves
│   └── compare.py                 # Statistical comparison
├── logs/
│   ├── dqn/                       # DQN training logs
│   ├── ppo/                       # PPO training logs
│   ├── neat/                      # NEAT training logs
│   └── tensorboard/               # TensorBoard logs
├── results/
│   ├── round1_comparison.md       # Round 1 findings
│   ├── round2_comparison.md       # Round 2 findings
│   └── final_report.md            # Complete findings
├── requirements.txt               # Python dependencies
├── config/
│   ├── dqn_config.yaml            # DQN hyperparameters
│   ├── ppo_config.yaml            # PPO hyperparameters
│   └── neat_config.txt            # NEAT configuration
├── README.md                      # Project documentation
└── demo.py                        # Quick launch: python demo.py --agent dqn
```

---

## Round 1: Classical RL Methods (3 Agents)

### Method 1: Deep Q-Network (DQN)
**Library:** `stable-baselines3.DQN`
**Training Time:** 4-8 hours
**Expected Score:** 50+
**Demo URL:** `http://localhost:5000/demo/dqn`

### Method 2: Proximal Policy Optimization (PPO)
**Library:** `stable-baselines3.PPO`
**Training Time:** 3-6 hours
**Expected Score:** 100+
**Demo URL:** `http://localhost:5000/demo/ppo`

### Method 3: Neuroevolution (NEAT)
**Library:** `neat-python`
**Training Time:** 6-12 hours
**Expected Score:** 50-100
**Demo URL:** `http://localhost:5000/demo/neat`

---

## Round 2: Experimental Methods (2 Agents)

### Method 4: Decision Transformer (Offline RL)
**Library:** `transformers.DecisionTransformerModel`
**Approach:** Train on trajectories collected from Round 1
**Training Time:** 4-8 hours
**Expected Score:** 50-150 (leverage offline data)
**Demo URL:** `http://localhost:5000/demo/decision-transformer`

### Method 5: Experimental - Language Model Policy
**Approach:** Use Claude API or local LLM as decision-making policy
**How:** Feed game state as text, get action as response
**Training Time:** 2-4 hours (fine-tuning or prompt engineering)
**Expected Score:** 10-50 (exploratory, may fail)
**Demo URL:** `http://localhost:5000/demo/llm-policy`

**Alternative Experimental Methods (choose best 2):**
- World Models (learn dynamics, plan in latent space)
- Curiosity-Driven Learning (intrinsic motivation)
- Imitation Learning from Round 1 agents
- Meta-Learning (MAML-style)

---

## Execution Protocol: Step-by-Step

### Phase 0: Environment Setup (2 hours)

**Task 0.1: Install Dependencies**
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions
mkdir flappy-bird-ai
cd flappy-bird-ai

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install Round 1 dependencies
pip install gymnasium stable-baselines3 neat-python torch numpy matplotlib tensorboard fastapi uvicorn websockets

# Install Round 2 dependencies (after Round 1)
pip install transformers accelerate datasets
```

**Validation:**
- [ ] `python -c "import gymnasium; print('✓ Gymnasium')"` works
- [ ] `python -c "import stable_baselines3; print('✓ SB3')"` works
- [ ] `python -c "import neat; print('✓ NEAT')"` works
- [ ] `python -c "import fastapi; print('✓ FastAPI')"` works

**Task 0.2: Create Project Structure**
```bash
mkdir -p environment agents training server web evaluation logs results models config
```

**Task 0.3: Copy Flappy Bird Game Logic**
- Extract game mechanics from `.deia/flappy-gerald.html`
- Port JavaScript logic to Python
- Create `environment/game_logic.py`

**Deliverable:**
- [ ] `flappy-bird-ai/` directory structure exists
- [ ] Dependencies installed
- [ ] Game logic ported to Python

---

### Phase 1: Build Gymnasium Environment (3 hours)

**Task 1.1: Implement FlappyBirdEnv**

Create `environment/flappy_env.py`:
```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class FlappyBirdEnv(gym.Env):
    """Gymnasium environment for Flappy Bird"""

    def __init__(self):
        super().__init__()

        # Action space: 0 = do nothing, 1 = flap
        self.action_space = spaces.Discrete(2)

        # Observation space: [bird_y, bird_velocity, pipe_x, pipe_gap_y, pipe_gap_size]
        self.observation_space = spaces.Box(
            low=np.array([0, -15, 0, 0, 120]),
            high=np.array([700, 15, 450, 700, 160]),
            dtype=np.float32
        )

        # Game state
        self.reset()

    def reset(self, seed=None, options=None):
        """Reset environment to initial state"""
        super().reset(seed=seed)
        # Initialize bird, pipes, score
        self.bird_y = 350
        self.bird_velocity = 0
        self.pipes = [self._generate_pipe()]
        self.score = 0
        self.frame = 0
        return self._get_observation(), {}

    def step(self, action):
        """Execute one timestep"""
        # Apply action (flap or not)
        if action == 1:
            self.bird_velocity = -10  # Flap

        # Physics: gravity
        self.bird_velocity += 0.5
        self.bird_y += self.bird_velocity

        # Move pipes
        for pipe in self.pipes:
            pipe['x'] -= 3

        # Generate new pipes
        if self.pipes[-1]['x'] < 300:
            self.pipes.append(self._generate_pipe())

        # Remove off-screen pipes
        if self.pipes[0]['x'] < -100:
            self.pipes.pop(0)
            self.score += 1

        # Check collision
        terminated = self._check_collision()

        # Reward function (sparse rewards)
        reward = 1 if not terminated else -100
        if self.score > 0 and self.frame % 30 == 0:  # Bonus for passing pipes
            reward = 10

        self.frame += 1

        return self._get_observation(), reward, terminated, False, {'score': self.score}

    def _get_observation(self):
        """Get current state observation"""
        next_pipe = self.pipes[0]
        return np.array([
            self.bird_y,
            self.bird_velocity,
            next_pipe['x'],
            next_pipe['gap_y'],
            next_pipe['gap_size']
        ], dtype=np.float32)

    def _generate_pipe(self):
        """Generate new pipe"""
        return {
            'x': 450,
            'gap_y': np.random.randint(200, 500),
            'gap_size': 140
        }

    def _check_collision(self):
        """Check if bird collided with pipes or boundaries"""
        # Hit ground or ceiling
        if self.bird_y < 0 or self.bird_y > 700:
            return True

        # Hit pipe
        next_pipe = self.pipes[0]
        if 50 < next_pipe['x'] < 100:  # Bird x position is ~75
            gap_top = next_pipe['gap_y'] - next_pipe['gap_size'] / 2
            gap_bottom = next_pipe['gap_y'] + next_pipe['gap_size'] / 2
            if self.bird_y < gap_top or self.bird_y > gap_bottom:
                return True

        return False

    def render(self):
        """Optional: return game state for visualization"""
        return {
            'bird_y': self.bird_y,
            'bird_velocity': self.bird_velocity,
            'pipes': self.pipes,
            'score': self.score
        }
```

**Task 1.2: Test Environment**

Create `environment/test_env.py`:
```python
from flappy_env import FlappyBirdEnv

env = FlappyBirdEnv()
obs, info = env.reset()
print(f"Initial observation: {obs}")

# Random agent test
total_reward = 0
for _ in range(1000):
    action = env.action_space.sample()  # Random action
    obs, reward, terminated, truncated, info = env.step(action)
    total_reward += reward
    if terminated:
        print(f"Episode ended. Score: {info['score']}, Total reward: {total_reward}")
        obs, info = env.reset()
        total_reward = 0
```

**Validation:**
- [ ] Random agent can play (should die quickly, score ~0-5)
- [ ] Observation space is correct shape (5,)
- [ ] Actions execute correctly
- [ ] Collision detection works
- [ ] Score increments when passing pipes

**Deliverable:**
- [ ] `environment/flappy_env.py` implemented
- [ ] Tests pass
- [ ] Random agent baseline: avg score ~2-5

---

### Phase 2: Train DQN Agent (4-6 hours)

**Task 2.1: Create DQN Training Script**

Create `training/train_dqn.py`:
```python
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
import sys
sys.path.append('..')
from environment.flappy_env import FlappyBirdEnv

# Create environment
env = FlappyBirdEnv()

# Checkpoint callback (save every 10k steps)
checkpoint_callback = CheckpointCallback(
    save_freq=10000,
    save_path='../models/dqn/',
    name_prefix='dqn_model'
)

# Evaluation callback
eval_env = FlappyBirdEnv()
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path='../models/dqn/',
    log_path='../logs/dqn/',
    eval_freq=5000,
    n_eval_episodes=10,
    deterministic=True
)

# Create DQN agent
model = DQN(
    'MlpPolicy',
    env,
    learning_rate=1e-3,
    buffer_size=100000,
    learning_starts=1000,
    batch_size=64,
    tau=1.0,
    gamma=0.99,
    train_freq=4,
    gradient_steps=1,
    target_update_interval=1000,
    exploration_fraction=0.1,
    exploration_initial_eps=1.0,
    exploration_final_eps=0.01,
    verbose=1,
    tensorboard_log='../logs/tensorboard/'
)

# Train
print("Training DQN agent...")
model.learn(total_timesteps=500000, callback=[checkpoint_callback, eval_callback])

# Save final model
model.save('../models/dqn_best')
print("✓ DQN training complete!")
```

**Task 2.2: Launch Training**
```bash
cd flappy-bird-ai/training
python train_dqn.py
```

**Task 2.3: Monitor Training**
```bash
# In separate terminal
tensorboard --logdir ../logs/tensorboard/
# Open http://localhost:6006
```

**Expected Progress:**
- Episodes 0-10k: Random exploration, score ~0-5
- Episodes 10k-50k: Learning, score increases to 10-20
- Episodes 50k-100k: Improvement, score reaches 30-50
- Episodes 100k+: Convergence, score 50-100+

**Validation:**
- [ ] Training runs without errors
- [ ] Scores improve over time (TensorBoard)
- [ ] Model checkpoints save correctly
- [ ] Best model achieves score > 50 (target)

**Deliverable:**
- [ ] `models/dqn_best.zip` saved
- [ ] Training logs in `logs/dqn/`
- [ ] DQN agent ready for demo

**Demo Preparation:**
- [ ] Test loaded model plays successfully
- [ ] Prepare for FastAPI integration

---

### Phase 3: Train PPO Agent (4-6 hours)

**Task 3.1: Create PPO Training Script**

Create `training/train_ppo.py`:
```python
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
import sys
sys.path.append('..')
from environment.flappy_env import FlappyBirdEnv

# Create environment
env = FlappyBirdEnv()

# Callbacks
checkpoint_callback = CheckpointCallback(
    save_freq=10000,
    save_path='../models/ppo/',
    name_prefix='ppo_model'
)

eval_env = FlappyBirdEnv()
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path='../models/ppo/',
    log_path='../logs/ppo/',
    eval_freq=5000,
    n_eval_episodes=10,
    deterministic=True
)

# Create PPO agent
model = PPO(
    'MlpPolicy',
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.01,
    vf_coef=0.5,
    max_grad_norm=0.5,
    verbose=1,
    tensorboard_log='../logs/tensorboard/'
)

# Train
print("Training PPO agent...")
model.learn(total_timesteps=300000, callback=[checkpoint_callback, eval_callback])

# Save final model
model.save('../models/ppo_best')
print("✓ PPO training complete!")
```

**Task 3.2: Launch Training**
```bash
cd flappy-bird-ai/training
python train_ppo.py
```

**Expected Progress:**
- Episodes 0-5k: Learning policy, score ~5-10
- Episodes 5k-30k: Rapid improvement, score 20-50
- Episodes 30k-100k: Refinement, score 50-100+
- Episodes 100k+: Mastery, score 100-200+

**Validation:**
- [ ] Training runs without errors
- [ ] PPO typically outperforms DQN
- [ ] Best model achieves score > 100 (stretch)

**Deliverable:**
- [ ] `models/ppo_best.zip` saved
- [ ] Training logs in `logs/ppo/`
- [ ] PPO agent ready for demo

---

### Phase 4: Train NEAT Agent (6-12 hours)

**Task 4.1: Create NEAT Configuration**

Create `config/neat_config.txt`:
```
[NEAT]
fitness_criterion     = max
fitness_threshold     = 1000
pop_size              = 100
reset_on_extinction   = False

[DefaultGenome]
# Network parameters
num_inputs              = 5
num_hidden              = 0
num_outputs             = 1
initial_connection      = full
feed_forward            = True
compatibility_disjoint_coefficient = 1.0
compatibility_weight_coefficient   = 0.5
conn_add_prob           = 0.5
conn_delete_prob        = 0.2
node_add_prob           = 0.2
node_delete_prob        = 0.2
activation_default      = sigmoid
activation_mutate_rate  = 0.0
activation_options      = sigmoid
aggregation_default     = sum
aggregation_mutate_rate = 0.0
aggregation_options     = sum
bias_init_mean          = 0.0
bias_init_stdev         = 1.0
bias_replace_rate       = 0.1
bias_mutate_rate        = 0.7
bias_mutate_power       = 0.5
bias_max_value          = 30.0
bias_min_value          = -30.0
response_init_mean      = 1.0
response_init_stdev     = 0.0
response_replace_rate   = 0.0
response_mutate_rate    = 0.0
response_mutate_power   = 0.0
response_max_value      = 30.0
response_min_value      = -30.0
weight_max_value        = 30
weight_min_value        = -30
weight_init_mean        = 0.0
weight_init_stdev       = 1.0
weight_mutate_rate      = 0.8
weight_replace_rate     = 0.1
weight_mutate_power     = 0.5
enabled_default         = True
enabled_mutate_rate     = 0.01

[DefaultSpeciesSet]
compatibility_threshold = 3.0

[DefaultStagnation]
species_fitness_func = max
max_stagnation       = 20
species_elitism      = 2

[DefaultReproduction]
elitism            = 2
survival_threshold = 0.2
```

**Task 4.2: Create NEAT Training Script**

Create `training/train_neat.py`:
```python
import neat
import pickle
import sys
sys.path.append('..')
from environment.flappy_env import FlappyBirdEnv

def eval_genome(genome, config):
    """Evaluate a single genome"""
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    env = FlappyBirdEnv()

    # Play 3 games, return average score
    total_score = 0
    for _ in range(3):
        obs, _ = env.reset()
        done = False
        while not done:
            # Get action from network
            output = net.activate(obs)
            action = 1 if output[0] > 0.5 else 0
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
        total_score += info['score']

    return total_score / 3

def eval_genomes(genomes, config):
    """Evaluate all genomes in population"""
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)

# Load config
config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    '../config/neat_config.txt'
)

# Create population
p = neat.Population(config)

# Add reporters
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(10, filename_prefix='../models/neat/checkpoint-'))

# Run evolution
print("Training NEAT agent...")
winner = p.run(eval_genomes, 100)  # 100 generations

# Save best genome
with open('../models/neat_best.pkl', 'wb') as f:
    pickle.dump(winner, f)

print(f"✓ NEAT training complete! Best fitness: {winner.fitness}")
```

**Task 4.3: Launch Training**
```bash
cd flappy-bird-ai/training
python train_neat.py
```

**Expected Progress:**
- Generation 0-10: Random networks, fitness ~5-10
- Generation 10-30: Topology evolution, fitness 20-40
- Generation 30-60: Optimization, fitness 40-80
- Generation 60-100: Convergence, fitness 50-100+

**Validation:**
- [ ] Evolution progresses without errors
- [ ] Best genome achieves score > 50

**Deliverable:**
- [ ] `models/neat_best.pkl` saved
- [ ] NEAT agent ready for demo

---

### Phase 5: Build Demo Server (3-4 hours)

**Task 5.1: Create FastAPI Server**

Create `server/app.py`:
```python
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
import json
from agent_loader import load_agent
from game_server import GameServer

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="../web"), name="static")

# Available agents
agents = {}

@app.on_event("startup")
async def load_agents():
    """Load all trained agents"""
    agents['dqn'] = load_agent('dqn')
    agents['ppo'] = load_agent('ppo')
    agents['neat'] = load_agent('neat')
    print("✓ All agents loaded")

@app.get("/")
async def index():
    """Landing page listing all agents"""
    with open("../web/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/demo/{agent_name}")
async def demo(agent_name: str):
    """Demo page for specific agent"""
    if agent_name not in agents:
        return {"error": "Agent not found"}
    with open("../web/demo.html") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws/{agent_name}")
async def websocket_endpoint(websocket: WebSocket, agent_name: str):
    """WebSocket for real-time game streaming"""
    await websocket.accept()

    if agent_name not in agents:
        await websocket.send_json({"error": "Agent not found"})
        await websocket.close()
        return

    game_server = GameServer(agents[agent_name])

    try:
        while True:
            # Run one game step
            game_state = game_server.step()

            # Send to browser
            await websocket.send_json(game_state)

            # If game ended, reset
            if game_state['done']:
                await asyncio.sleep(1)  # Pause before restart
                game_server.reset()

            await asyncio.sleep(0.016)  # ~60 FPS

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

**Task 5.2: Create Agent Loader**

Create `server/agent_loader.py`:
```python
from stable_baselines3 import DQN, PPO
import neat
import pickle

def load_agent(agent_name):
    """Load a trained agent"""
    if agent_name == 'dqn':
        return DQN.load('../models/dqn_best')
    elif agent_name == 'ppo':
        return PPO.load('../models/ppo_best')
    elif agent_name == 'neat':
        with open('../models/neat_best.pkl', 'rb') as f:
            genome = pickle.load(f)
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            '../config/neat_config.txt'
        )
        return neat.nn.FeedForwardNetwork.create(genome, config)
    else:
        raise ValueError(f"Unknown agent: {agent_name}")
```

**Task 5.3: Create Game Server**

Create `server/game_server.py`:
```python
import sys
sys.path.append('..')
from environment.flappy_env import FlappyBirdEnv

class GameServer:
    """Manages game state and agent interaction"""

    def __init__(self, agent):
        self.agent = agent
        self.env = FlappyBirdEnv()
        self.obs, _ = self.env.reset()
        self.done = False

    def step(self):
        """Execute one game step"""
        if self.done:
            return self._get_state()

        # Get action from agent
        if hasattr(self.agent, 'predict'):  # SB3 agent
            action, _ = self.agent.predict(self.obs, deterministic=True)
        else:  # NEAT agent
            output = self.agent.activate(self.obs)
            action = 1 if output[0] > 0.5 else 0

        # Execute action
        self.obs, reward, terminated, truncated, info = self.env.step(action)
        self.done = terminated or truncated

        return self._get_state()

    def reset(self):
        """Reset game"""
        self.obs, _ = self.env.reset()
        self.done = False

    def _get_state(self):
        """Get current game state for visualization"""
        render_data = self.env.render()
        return {
            'bird_y': render_data['bird_y'],
            'bird_velocity': render_data['bird_velocity'],
            'pipes': render_data['pipes'],
            'score': render_data['score'],
            'done': self.done
        }
```

**Task 5.4: Create Frontend**

Create `web/index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Flappy Bird AI - Agents</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Flappy Bird AI Experiments</h1>
    <h2>Round 1: Classical RL Methods</h2>
    <div class="agent-list">
        <a href="/demo/dqn" class="agent-card">
            <h3>DQN (Deep Q-Network)</h3>
            <p>Value-based reinforcement learning</p>
        </a>
        <a href="/demo/ppo" class="agent-card">
            <h3>PPO (Proximal Policy Optimization)</h3>
            <p>Policy gradient reinforcement learning</p>
        </a>
        <a href="/demo/neat" class="agent-card">
            <h3>NEAT (Neuroevolution)</h3>
            <p>Genetic algorithm evolution</p>
        </a>
    </div>

    <h2>Round 2: Experimental Methods</h2>
    <div class="agent-list">
        <a href="/demo/decision-transformer" class="agent-card">
            <h3>Decision Transformer</h3>
            <p>Offline RL with transformers</p>
        </a>
        <a href="/demo/llm-policy" class="agent-card">
            <h3>LLM Policy</h3>
            <p>Language model as game player</p>
        </a>
    </div>
</body>
</html>
```

Create `web/demo.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Flappy Bird AI - Demo</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Agent Demo: <span id="agent-name"></span></h1>
    <div id="score">Score: 0</div>
    <canvas id="gameCanvas" width="450" height="700"></canvas>
    <script src="/static/game_canvas.js"></script>
</body>
</html>
```

Create `web/game_canvas.js`:
```javascript
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');

// Get agent name from URL
const agentName = window.location.pathname.split('/').pop();
document.getElementById('agent-name').textContent = agentName.toUpperCase();

// WebSocket connection
const ws = new WebSocket(`ws://localhost:5000/ws/${agentName}`);

ws.onmessage = function(event) {
    const state = JSON.parse(event.data);
    render(state);
};

function render(state) {
    // Clear canvas
    ctx.fillStyle = '#87CEEB';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw bird
    ctx.fillStyle = '#FFD700';
    ctx.beginPath();
    ctx.arc(75, state.bird_y, 20, 0, Math.PI * 2);
    ctx.fill();

    // Draw pipes
    ctx.fillStyle = '#228B22';
    for (const pipe of state.pipes) {
        const gapTop = pipe.gap_y - pipe.gap_size / 2;
        const gapBottom = pipe.gap_y + pipe.gap_size / 2;

        // Top pipe
        ctx.fillRect(pipe.x, 0, 50, gapTop);
        // Bottom pipe
        ctx.fillRect(pipe.x, gapBottom, 50, canvas.height - gapBottom);
    }

    // Update score
    scoreElement.textContent = `Score: ${state.score}`;

    // Game over overlay
    if (state.done) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#FFF';
        ctx.font = '48px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Game Over', canvas.width / 2, canvas.height / 2);
        ctx.font = '24px Arial';
        ctx.fillText(`Final Score: ${state.score}`, canvas.width / 2, canvas.height / 2 + 50);
    }
}
```

Create `web/style.css`:
```css
body {
    font-family: Arial, sans-serif;
    background: #1a1a1a;
    color: #fff;
    padding: 20px;
}

h1 {
    text-align: center;
}

.agent-list {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 20px 0;
}

.agent-card {
    background: #2a2a2a;
    border: 2px solid #3a3a3a;
    border-radius: 8px;
    padding: 20px;
    width: 250px;
    text-decoration: none;
    color: #fff;
    transition: transform 0.2s, border-color 0.2s;
}

.agent-card:hover {
    transform: translateY(-5px);
    border-color: #4a9eff;
}

canvas {
    display: block;
    margin: 20px auto;
    border: 2px solid #fff;
    background: #87CEEB;
}

#score {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}
```

**Task 5.5: Launch Server**
```bash
cd flappy-bird-ai/server
python app.py
```

**Access URLs:**
- Landing page: `http://localhost:5000`
- DQN demo: `http://localhost:5000/demo/dqn`
- PPO demo: `http://localhost:5000/demo/ppo`
- NEAT demo: `http://localhost:5000/demo/neat`

**On local network:** Replace `localhost` with your machine's IP (e.g., `http://192.168.1.100:5000`)

**Validation:**
- [ ] Server starts without errors
- [ ] Landing page loads
- [ ] Each agent demo works
- [ ] Game renders in browser
- [ ] Agents play autonomously

**Deliverable:**
- [ ] Demo server running
- [ ] Links ready to share with Dave

---

### Phase 6: Evaluate & Compare Round 1 (3 hours)

**Task 6.1: Run Evaluations**

Create `evaluation/evaluate.py`:
```python
from stable_baselines3 import DQN, PPO
import neat
import pickle
import numpy as np
import sys
sys.path.append('..')
from environment.flappy_env import FlappyBirdEnv

def evaluate_agent(agent, agent_name, n_episodes=100):
    """Evaluate agent over n episodes"""
    env = FlappyBirdEnv()
    scores = []

    for episode in range(n_episodes):
        obs, _ = env.reset()
        done = False

        while not done:
            if hasattr(agent, 'predict'):  # SB3
                action, _ = agent.predict(obs, deterministic=True)
            else:  # NEAT
                output = agent.activate(obs)
                action = 1 if output[0] > 0.5 else 0

            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

        scores.append(info['score'])
        if (episode + 1) % 10 == 0:
            print(f"{agent_name}: Episode {episode + 1}/100, Avg score: {np.mean(scores):.2f}")

    return scores

# Load agents
print("Loading agents...")
dqn = DQN.load('../models/dqn_best')
ppo = PPO.load('../models/ppo_best')
with open('../models/neat_best.pkl', 'rb') as f:
    neat_genome = pickle.load(f)
neat_config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
                          '../config/neat_config.txt')
neat_agent = neat.nn.FeedForwardNetwork.create(neat_genome, neat_config)

# Evaluate
print("\n=== Evaluating DQN ===")
dqn_scores = evaluate_agent(dqn, 'DQN', n_episodes=100)

print("\n=== Evaluating PPO ===")
ppo_scores = evaluate_agent(ppo, 'PPO', n_episodes=100)

print("\n=== Evaluating NEAT ===")
neat_scores = evaluate_agent(neat_agent, 'NEAT', n_episodes=100)

# Summary
print("\n" + "="*50)
print("ROUND 1 RESULTS")
print("="*50)
print(f"DQN:  Mean={np.mean(dqn_scores):.2f} ± {np.std(dqn_scores):.2f}, Max={np.max(dqn_scores)}, Min={np.min(dqn_scores)}")
print(f"PPO:  Mean={np.mean(ppo_scores):.2f} ± {np.std(ppo_scores):.2f}, Max={np.max(ppo_scores)}, Min={np.min(ppo_scores)}")
print(f"NEAT: Mean={np.mean(neat_scores):.2f} ± {np.std(neat_scores):.2f}, Max={np.max(neat_scores)}, Min={np.min(neat_scores)}")

# Save results
import json
results = {
    'dqn': {'scores': dqn_scores, 'mean': float(np.mean(dqn_scores)), 'std': float(np.std(dqn_scores))},
    'ppo': {'scores': ppo_scores, 'mean': float(np.mean(ppo_scores)), 'std': float(np.std(ppo_scores))},
    'neat': {'scores': neat_scores, 'mean': float(np.mean(neat_scores)), 'std': float(np.std(neat_scores))}
}
with open('../results/round1_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

**Task 6.2: Visualize Results**

Create `evaluation/visualize.py`:
```python
import json
import matplotlib.pyplot as plt
import numpy as np

# Load results
with open('../results/round1_results.json') as f:
    results = json.load(f)

# Plot 1: Box plot comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Box plot
axes[0].boxplot([results['dqn']['scores'], results['ppo']['scores'], results['neat']['scores']],
                labels=['DQN', 'PPO', 'NEAT'])
axes[0].set_title('Score Distribution (100 episodes each)')
axes[0].set_ylabel('Score')
axes[0].grid(True, alpha=0.3)

# Bar plot with error bars
methods = ['DQN', 'PPO', 'NEAT']
means = [results[m.lower()]['mean'] for m in methods]
stds = [results[m.lower()]['std'] for m in methods]
axes[1].bar(methods, means, yerr=stds, capsize=5, alpha=0.7, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
axes[1].set_title('Mean Score ± Std Dev')
axes[1].set_ylabel('Score')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../results/round1_comparison.png', dpi=150)
print("✓ Saved: ../results/round1_comparison.png")
```

**Task 6.3: Write Findings Report**

Create `results/round1_comparison.md`:
```markdown
# Round 1 Findings: Classical RL Methods

## Summary

Three reinforcement learning methods were trained and evaluated on Flappy Bird:
- **DQN (Deep Q-Network)**: Value-based RL
- **PPO (Proximal Policy Optimization)**: Policy gradient RL
- **NEAT (Neuroevolution)**: Genetic algorithm

Each agent was evaluated over 100 episodes.

## Results

### Performance Metrics

| Method | Mean Score | Std Dev | Max Score | Min Score |
|--------|-----------|---------|-----------|-----------|
| DQN    | [X.XX]    | [X.XX]  | [XXX]     | [XX]      |
| PPO    | [X.XX]    | [X.XX]  | [XXX]     | [XX]      |
| NEAT   | [X.XX]    | [X.XX]  | [XXX]     | [XX]      |

### Observations

**Winner: [TBD based on results]**

**DQN:**
- [Analysis based on actual results]
- Training time: ~X hours
- Sample efficiency: [High/Medium/Low]
- Stability: [High/Medium/Low]

**PPO:**
- [Analysis based on actual results]
- Training time: ~X hours
- Sample efficiency: [High/Medium/Low]
- Stability: [High/Medium/Low]

**NEAT:**
- [Analysis based on actual results]
- Training time: ~X hours
- Sample efficiency: [High/Medium/Low]
- Stability: [High/Medium/Low]

### Hypotheses Validation

**Hypothesis 1: PPO achieves highest score** → [CONFIRMED/REJECTED]
**Hypothesis 2: NEAT converges fastest** → [CONFIRMED/REJECTED]
**Hypothesis 3: DQN most sample efficient** → [CONFIRMED/REJECTED]

## Insights

### What Worked
- [List successful aspects]

### What Didn't Work
- [List challenges/failures]

### Surprising Findings
- [Unexpected observations]

## Next Steps: Round 2

Based on Round 1 results, proceed with:
1. Decision Transformer (leverage offline trajectories)
2. [Experimental method TBD]

## Links

- DQN Demo: http://localhost:5000/demo/dqn
- PPO Demo: http://localhost:5000/demo/ppo
- NEAT Demo: http://localhost:5000/demo/neat
```

**Deliverable:**
- [ ] Evaluation complete (100 episodes per agent)
- [ ] Plots generated
- [ ] Round 1 findings written
- [ ] Results ready to share with Dave

---

### Phase 7: Round 2 - Decision Transformer (6-8 hours)

**Task 7.1: Collect Trajectories from Round 1**

Create `training/collect_trajectories.py`:
```python
# Collect trajectories from best agents (DQN, PPO, NEAT)
# Save as dataset for offline RL
```

**Task 7.2: Train Decision Transformer**

Create `training/train_dt.py`:
```python
from transformers import DecisionTransformerModel, Trainer, TrainingArguments
# Train Decision Transformer on collected trajectories
```

**Task 7.3: Integrate with Demo Server**
- Add Decision Transformer to agent loader
- Create demo endpoint

**Deliverable:**
- [ ] Decision Transformer trained
- [ ] Demo available: `http://localhost:5000/demo/decision-transformer`

---

### Phase 8: Round 2 - Experimental Method (4-6 hours)

**Options:**
1. **LLM Policy**: Use Claude API or local LLM
2. **World Models**: Learn dynamics, plan in latent space
3. **Curiosity-Driven**: Intrinsic motivation

**Choice:** [TBD based on Round 1 results and feasibility]

**Deliverable:**
- [ ] Experimental agent trained
- [ ] Demo available: `http://localhost:5000/demo/[method-name]`

---

### Phase 9: Final Evaluation & Report (3 hours)

**Task 9.1: Evaluate All 5 Agents**
- Run 100 episodes each
- Compare Round 1 vs Round 2

**Task 9.2: Create Final Report**

Create `results/final_report.md`:
```markdown
# Flappy Bird AI Experiments - Final Report

## Executive Summary
[Complete findings from both rounds]

## Round 1 Results
[Classical RL methods]

## Round 2 Results
[Experimental methods]

## Comparative Analysis
[Cross-round comparison]

## Conclusions
[Key insights, lessons learned]

## Future Work
[Next experiments, improvements]

## Demo Links
- DQN: http://localhost:5000/demo/dqn
- PPO: http://localhost:5000/demo/ppo
- NEAT: http://localhost:5000/demo/neat
- Decision Transformer: http://localhost:5000/demo/decision-transformer
- [Experimental]: http://localhost:5000/demo/[method]
```

**Deliverable:**
- [ ] All 5 agents evaluated
- [ ] Final report complete
- [ ] All demos ready

---

## Communication Protocol: Sharing Links with Dave

### After Each Agent is Trained

**Send message format:**
```
✓ [AGENT NAME] Training Complete!

Demo Link: http://localhost:5000/demo/[agent-name]
(Or on local network: http://[YOUR-IP]:5000/demo/[agent-name])

Performance:
- Mean Score: X.XX ± Y.YY
- Max Score: ZZZ
- Training Time: X hours

Watch it play live! Server is running.

Next: [Next agent name]
```

### Milestones to Share

1. ✅ **Environment Ready** → "Gymnasium environment working, random agent baseline"
2. ✅ **DQN Complete** → Share DQN demo link + stats
3. ✅ **PPO Complete** → Share PPO demo link + stats
4. ✅ **NEAT Complete** → Share NEAT demo link + stats
5. ✅ **Round 1 Done** → Share comparison report + all 3 links
6. ✅ **Decision Transformer Complete** → Share DT demo link
7. ✅ **Experimental Complete** → Share experimental demo link
8. ✅ **Final Report** → Share all 5 links + complete findings

---

## Validation Checklist (Before Sharing Each Demo)

Before sending demo link to Dave:

- [ ] Agent loads without errors
- [ ] Demo page renders correctly
- [ ] WebSocket connection works
- [ ] Game plays smoothly (~60 FPS)
- [ ] Agent behavior looks intelligent (not random)
- [ ] Score displays correctly
- [ ] Game resets after death
- [ ] Server accessible on local network (test with phone/another device)

---

## Troubleshooting Guide

### Common Issues

**Issue: Training too slow**
→ Reduce total_timesteps, use smaller networks

**Issue: Agent not learning**
→ Check reward function, adjust hyperparameters, verify environment

**Issue: WebSocket errors**
→ Check CORS settings, verify port 5000 is open

**Issue: Demo lags**
→ Reduce frame rate, optimize rendering

**Issue: Agent plays randomly**
→ Verify model loaded correctly, check deterministic=True

---

## Success Criteria

### Minimum Success
- [ ] All 3 Round 1 agents trained
- [ ] At least 1 agent scores > 50
- [ ] Demo server works
- [ ] Round 1 findings written

### Target Success
- [ ] All 5 agents trained (Round 1 + Round 2)
- [ ] All agents score > 50
- [ ] Demos work flawlessly
- [ ] Complete findings report
- [ ] Dave can watch all 5 agents play

### Stretch Success
- [ ] At least 1 agent scores > 100
- [ ] Round 2 beats Round 1
- [ ] Comprehensive analysis
- [ ] Publishable findings
- [ ] Reusable framework for future RL experiments

---

## Timeline Estimate

### Aggressive (7 days)
- Day 1: Environment + DQN
- Day 2: PPO + NEAT
- Day 3: Demo server + Round 1 evaluation
- Day 4: Decision Transformer
- Day 5: Experimental method
- Day 6: Round 2 evaluation
- Day 7: Final report

### Conservative (10 days)
- Day 1-2: Environment + DQN
- Day 3-4: PPO + NEAT
- Day 5: Demo server + Round 1 evaluation
- Day 6-7: Decision Transformer
- Day 8: Experimental method
- Day 9: Round 2 evaluation
- Day 10: Final report + polish

**Active work:** 40-50 hours
**Compute time:** 24-48 hours (training can run overnight)

---

## Next Step: Begin Execution

Upon Dave's approval, start with **Phase 0: Environment Setup**.

Execute autonomously, share demo links as each agent completes.

---

**Blueprint Status:** ✅ Ready for Execution
**Prepared by:** BOT-00001 (Queen/Researcher/Engineer)
**Date:** 2025-10-12
**Awaiting:** Dave's go-ahead to begin Phase 0
