# Teaching AI to Play Flappy Bird: A Comparative Study of Three Neural Network Approaches

**Research Proposal**

**Project:** Neural Network Learning for Flappy Bird Game Playing
**Principal Investigator:** BOT-00001 (Queen/Researcher)
**Date:** 2025-10-12
**Status:** Proposal for Approval

---

## Executive Summary

This research proposal outlines an experiment to train neural networks to play Flappy Bird autonomously, comparing three cutting-edge approaches: **Deep Q-Networks (DQN)**, **Proximal Policy Optimization (PPO)**, and **Neuroevolution (NEAT)**. The experiment will run entirely on local hardware with a single AI agent coordinating all roles (researcher, engineer, experimenter, analyst).

**Key Question:** Which neural network approach learns to play Flappy Bird most effectively, and what can we learn about AI learning from games?

---

## 1. Research Context

### 1.1 The Challenge

**Problem:** Train an AI agent to play Flappy Bird using only:
- **Input:** Game state observation (bird position, pipe positions, velocities)
- **Output:** Binary action (flap or don't flap)
- **Goal:** Maximize score (survive as long as possible)

**Constraints:**
- Must run on local machine (no cloud GPUs)
- Single Claude Code instance fills all roles
- Must be reproducible and demonstrable
- Should complete training in reasonable time (<24 hours per method)

### 1.2 Why This Matters

**Scientific Value:**
- Compare different RL paradigms on same task
- Understand sample efficiency vs performance trade-offs
- Explore interpretability of learned policies
- Demonstrate local AI training capabilities

**Educational Value:**
- Show how different RL methods work
- Make AI learning transparent and understandable
- Create reusable framework for game AI
- Document learning curves and failure modes

**Practical Value:**
- Prove concept for DEIA AI-learning-from-AI capabilities
- Build reusable RL infrastructure
- Create benchmarking system for future experiments
- Enable community experimentation

---

## 2. Literature Review (Condensed)

### 2.1 DQN (Deep Q-Networks)
**Paper:** "Playing Atari with Deep Reinforcement Learning" (Mnih et al., 2013)
**Key Innovation:** Q-learning + deep neural networks + experience replay
**Proven:** Works on Atari games including Breakout, Pong
**Application:** Widely used for discrete action space problems

### 2.2 PPO (Proximal Policy Optimization)
**Paper:** "Proximal Policy Optimization Algorithms" (Schulman et al., 2017)
**Key Innovation:** Policy gradient with clipped objective (stable training)
**Proven:** State-of-the-art on many RL benchmarks, used by OpenAI
**Application:** Default choice for many modern RL tasks

### 2.3 Neuroevolution (NEAT)
**Paper:** "Evolving Neural Networks through Augmenting Topologies" (Stanley & Miikkulainen, 2002)
**Key Innovation:** Evolves both network topology and weights
**Proven:** Solved pole balancing, game playing, robotics
**Application:** Alternative to gradient-based methods, often more interpretable

### 2.4 Flappy Bird Precedents
- Multiple hobbyist implementations exist (GitHub)
- Most use simple neural networks or genetic algorithms
- Few rigorous comparisons of methods
- This experiment adds: systematic comparison, documentation, reproducibility

---

## 3. Three Proposed Methods

### Method 1: Deep Q-Network (DQN)

**Approach:** Value-based reinforcement learning

**How It Works:**
1. Neural network estimates Q-values for each action (flap/no-flap)
2. Agent chooses action with highest Q-value (with epsilon-greedy exploration)
3. Experience stored in replay buffer
4. Network trained on random batches from buffer
5. Target network for stability (updated periodically)

**Architecture:**
```
Input Layer: [bird_y, bird_velocity, pipe_x, pipe_gap_y, pipe_gap_size]
Hidden Layer 1: 128 neurons (ReLU)
Hidden Layer 2: 64 neurons (ReLU)
Output Layer: 2 neurons (Q-value for [no-flap, flap])
```

**Training Algorithm:**
```python
1. Initialize Q-network and target network
2. For each episode:
   a. Observe state s
   b. Choose action a (epsilon-greedy)
   c. Execute action, observe reward r and next state s'
   d. Store (s, a, r, s') in replay buffer
   e. Sample random batch from buffer
   f. Compute target: r + gamma * max(Q_target(s'))
   g. Update Q-network to minimize TD error
   h. Every C steps, update target network
3. Decay epsilon over time
```

**Hyperparameters:**
- Learning rate: 0.001
- Discount factor (gamma): 0.99
- Epsilon: 1.0 → 0.01 (decay over 10k steps)
- Replay buffer size: 100,000
- Batch size: 64
- Target network update frequency: 1000 steps

**Expected Performance:**
- Training time: 4-8 hours
- Target score: 50+ (should reach within 50k episodes)
- Sample efficiency: Moderate (needs many episodes)

**Advantages:**
- Proven reliable on discrete action problems
- Off-policy (efficient use of experience)
- Stable with proper hyperparameters

**Challenges:**
- Requires careful tuning
- Can overestimate Q-values
- Needs replay buffer (memory overhead)

---

### Method 2: Proximal Policy Optimization (PPO)

**Approach:** Policy gradient reinforcement learning

**How It Works:**
1. Neural network directly outputs action probabilities
2. Agent samples action from probability distribution
3. Collects trajectories (episodes)
4. Computes advantage estimates (how much better action was than expected)
5. Updates policy to increase probability of good actions (with clipping)
6. Separate value network estimates state values

**Architecture:**
```
Shared Input Layer: [bird_y, bird_velocity, pipe_x, pipe_gap_y, pipe_gap_size]
Shared Hidden 1: 128 neurons (ReLU)
Shared Hidden 2: 64 neurons (ReLU)

Policy Head: 32 neurons (ReLU) → 2 neurons (Softmax) [action probabilities]
Value Head: 32 neurons (ReLU) → 1 neuron (Linear) [state value estimate]
```

**Training Algorithm:**
```python
1. Initialize policy network (actor) and value network (critic)
2. For each epoch:
   a. Collect trajectories (multiple episodes)
   b. Compute returns and advantages (GAE)
   c. For K optimization epochs:
      - Compute policy loss (clipped surrogate objective)
      - Compute value loss (MSE)
      - Compute entropy bonus (encourage exploration)
      - Update networks with combined loss
3. Repeat until convergence
```

**Hyperparameters:**
- Learning rate: 0.0003
- Discount factor (gamma): 0.99
- GAE lambda: 0.95
- PPO clip epsilon: 0.2
- Entropy coefficient: 0.01
- Value loss coefficient: 0.5
- Optimization epochs (K): 4
- Batch size: 2048 (steps collected per update)

**Expected Performance:**
- Training time: 3-6 hours
- Target score: 100+ (PPO often outperforms DQN)
- Sample efficiency: High (on-policy but efficient)

**Advantages:**
- State-of-the-art performance
- Stable training (clipped objective prevents large updates)
- Often reaches higher scores than DQN
- Good balance of sample efficiency and stability

**Challenges:**
- More complex implementation
- Hyperparameters matter (clip ratio, GAE lambda)
- On-policy (must collect fresh data)

---

### Method 3: Neuroevolution (NEAT-inspired)

**Approach:** Genetic algorithm evolution of neural networks

**How It Works:**
1. Population of neural networks (genomes)
2. Each network plays game, receives fitness score
3. Select best performers for reproduction
4. Mutate (add nodes, add connections, adjust weights)
5. Crossover (combine networks from two parents)
6. Repeat for many generations

**Architecture:**
```
Start: Simple 5-input → 1-output network
Evolve: Add hidden neurons, add connections, adjust topology
End: Complex network with evolved structure
```

**Evolution Algorithm:**
```python
1. Initialize population (100 genomes)
2. For each generation:
   a. Evaluate fitness (each genome plays 3 games, avg score)
   b. Rank genomes by fitness
   c. Select top 20% for reproduction
   d. Create offspring:
      - 70% mutation (add node, add connection, adjust weight)
      - 20% crossover (combine two parents)
      - 10% elite (copy best unchanged)
   e. Replace population with offspring
3. Track best genome, save if improved
4. Repeat for 100+ generations
```

**Evolution Parameters:**
- Population size: 100
- Generations: 100+
- Mutation rate: 0.8
- Crossover rate: 0.2
- Elite size: 10%
- Species threshold: 3.0 (genetic distance)
- Weight mutation: ±0.5 (Gaussian)
- Add node probability: 0.03
- Add connection probability: 0.05

**Expected Performance:**
- Training time: 6-12 hours (depends on generations)
- Target score: 50-100 (varies by evolution luck)
- Sample efficiency: Low (needs many episodes per genome)

**Advantages:**
- Evolves network topology (discovers architecture)
- No gradient computation (different failure mode)
- Highly interpretable (can visualize evolved networks)
- Often finds creative solutions
- Parallelizable (evaluate genomes in parallel)

**Challenges:**
- Slower convergence (many generations needed)
- Stochastic (results vary by random seed)
- Computationally expensive per generation
- Harder to tune (many genetic parameters)

---

## 4. Experimental Design

### 4.1 Environment Setup

**Game Wrapper:**
```python
class FlappyBirdEnv:
    def reset() -> state:
        # Reset game to initial state
        # Return: [bird_y, bird_velocity, pipe_x, pipe_gap_y, pipe_gap_size]

    def step(action) -> (state, reward, done, info):
        # Execute action (0=no-flap, 1=flap)
        # Advance game one frame
        # Return: next state, reward, terminal flag, debug info

    def render():
        # Optional: visualize current state
```

**State Space:**
- `bird_y`: Bird vertical position (0-700, normalized)
- `bird_velocity`: Bird vertical velocity (-15 to 15, normalized)
- `pipe_x`: Distance to next pipe (0-450, normalized)
- `pipe_gap_y`: Vertical center of next pipe gap (0-700, normalized)
- `pipe_gap_size`: Size of next pipe gap (120-160, normalized)

**Action Space:**
- 0: Don't flap (do nothing)
- 1: Flap (apply upward velocity)

**Reward Function:**

**Option A: Sparse Rewards**
```python
reward = +1 for passing a pipe
reward = -100 for dying
reward = 0 otherwise
```

**Option B: Dense Rewards (Reward Shaping)**
```python
reward = +10 for passing a pipe
reward = +0.1 for surviving a frame
reward = -0.01 * abs(bird_y - pipe_gap_y) / 700  # Penalty for being far from center
reward = -100 for dying
```

**Decision:** Start with sparse rewards (more realistic), switch to dense if agents struggle.

### 4.2 Training Protocol

**Phase 1: Initial Training**
- Each method trains for fixed compute budget
- DQN: 100k episodes
- PPO: 50k episodes (more sample efficient)
- NEAT: 100 generations (×100 genomes × 3 games = 30k episodes)

**Phase 2: Extended Training (if needed)**
- Continue training if not converged
- Max additional: 2× initial budget

**Phase 3: Final Evaluation**
- Best agent from each method plays 100 games
- Record scores, visualize behavior
- Compare performance and learning curves

### 4.3 Metrics

**Primary Metrics:**
- **Average Score:** Mean score over last 100 episodes
- **Max Score:** Best score achieved during training
- **Success Rate:** % of episodes with score ≥ 10
- **Sample Efficiency:** Episodes needed to reach avg score of 50

**Secondary Metrics:**
- **Training Time:** Wall-clock hours to convergence
- **Stability:** Variance in scores over training
- **Final Performance:** Average score of best agent (100 test games)

**Qualitative Metrics:**
- **Behavior Quality:** Does agent look "smart"?
- **Policy Interpretability:** Can we understand what it learned?
- **Failure Modes:** How does it die? (ceiling, ground, pipes)

### 4.4 Reproducibility

**Random Seeds:**
- Each method runs with 3 different seeds
- Report mean ± std across seeds
- Allows statistical significance testing

**Checkpointing:**
- Save model every 1000 episodes (DQN/PPO) or 10 generations (NEAT)
- Can resume training if interrupted
- Can analyze learning progression

**Logging:**
- TensorBoard-style logs (episode, score, loss, etc.)
- CSV export for offline analysis
- Plots: learning curves, score distributions

---

## 5. Implementation Plan

### 5.1 Two-Round Structure

**ROUND 1: Classical RL with Proven Libraries**
- Focus: Fair comparison using battle-tested implementations
- Philosophy: Don't reinvent the wheel, use best practices
- Goal: Establish baseline, understand which paradigm works best

**ROUND 2: Advanced Methods from HuggingFace**
- Focus: Cutting-edge approaches, experimental
- Philosophy: Push boundaries, try "sick shit"
- Goal: Explore what's possible beyond classical RL

---

### 5.2 Technology Stack

**Round 1: Classical RL**
```python
# Core RL Framework
gymnasium==0.29.0              # OpenAI Gym successor (standard RL interface)
stable-baselines3==2.1.0       # DQN, PPO implementations (PyTorch-based)
neat-python==0.92              # NEAT implementation

# Deep Learning
torch==2.0.0+                  # PyTorch (CPU or GPU)
numpy==1.24.0                  # Numerical operations

# Monitoring & Visualization
tensorboard==2.13.0            # Training monitoring
matplotlib==3.7.0              # Plotting
pandas==2.0.0                  # Data analysis

# Utilities
tqdm==4.65.0                   # Progress bars
pyyaml==6.0                    # Config files
```

**Round 2: HuggingFace Experimental**
```python
# HuggingFace Ecosystem
transformers==4.35.0           # Decision Transformers, foundation models
accelerate==0.24.0             # Training acceleration
datasets==2.14.0               # Data handling
peft==0.6.0                    # Parameter-efficient fine-tuning

# Additional (TBD based on experiments)
sentence-transformers          # If using embeddings
diffusers                      # If exploring generative approaches
[more based on research]
```

**Why This Approach:**
- **Round 1:** Use `stable-baselines3` (industry standard, maintained, documented)
- **Benefit:** Fair comparison without implementation bugs
- **Round 2:** Explore HuggingFace model hub for novel approaches
- **Benefit:** Leverage pre-training, modern architectures

**No Cloud Dependencies:**
- Everything runs locally
- CPU-only training (GPU optional if available)
- Designed for laptop/desktop execution

### 5.2 Code Structure

```
flappy-bird-ai/
├── environment/
│   ├── flappy_env.py          # Game environment wrapper
│   └── game_controller.py     # Interface with actual game
├── agents/
│   ├── dqn_agent.py           # DQN implementation
│   ├── ppo_agent.py           # PPO implementation
│   ├── neat_agent.py          # Neuroevolution implementation
│   └── base_agent.py          # Shared interface
├── networks/
│   ├── dqn_network.py         # Q-network architecture
│   ├── ppo_network.py         # Actor-critic architecture
│   └── neat_genome.py         # Genome representation
├── training/
│   ├── train_dqn.py           # DQN training script
│   ├── train_ppo.py           # PPO training script
│   ├── train_neat.py          # NEAT training script
│   └── trainer_base.py        # Shared training utilities
├── evaluation/
│   ├── evaluate.py            # Test trained agents
│   ├── visualize.py           # Plot learning curves
│   └── compare.py             # Compare methods
├── utils/
│   ├── replay_buffer.py       # Experience replay (DQN)
│   ├── logger.py              # Logging utilities
│   └── config.py              # Hyperparameters
├── data/
│   ├── checkpoints/           # Saved models
│   ├── logs/                  # Training logs
│   └── results/               # Evaluation results
├── notebooks/
│   └── analysis.ipynb         # Jupyter notebook for analysis
└── main.py                    # Main entry point
```

### 5.3 Development Phases

**Phase 1: Environment (2 hours)**
- Create `FlappyBirdEnv` wrapper
- Extract state from game
- Implement action execution
- Test environment works correctly

**Phase 2: DQN Implementation (4 hours)**
- Implement Q-network
- Implement replay buffer
- Implement DQN agent
- Train and debug

**Phase 3: PPO Implementation (4 hours)**
- Implement actor-critic network
- Implement PPO algorithm
- Implement GAE computation
- Train and debug

**Phase 4: NEAT Implementation (4 hours)**
- Implement genome representation
- Implement mutation/crossover
- Implement evolution loop
- Train and debug

**Phase 5: Evaluation (2 hours)**
- Run final evaluations
- Generate plots
- Compare methods
- Write report

**Total Estimated:** 16-20 hours development + 24-48 hours training time

---

## 6. Expected Outcomes & Hypotheses

### 6.1 Performance Hypotheses

**Hypothesis 1: PPO will achieve the highest final score**
- Rationale: PPO is state-of-the-art, often outperforms DQN
- Prediction: PPO avg score > 100, DQN avg score > 50, NEAT avg score > 50

**Hypothesis 2: NEAT will converge fastest initially**
- Rationale: Simple topology, direct fitness optimization
- Prediction: NEAT reaches score 10 first, but plateaus earlier

**Hypothesis 3: DQN will be most sample efficient**
- Rationale: Off-policy learning, experience replay
- Prediction: DQN reaches score 50 in fewer episodes than NEAT

**Hypothesis 4: PPO will have most stable training**
- Rationale: Clipped objective prevents destructive updates
- Prediction: PPO learning curve smoothest, lowest variance

### 6.2 Learning Insights

**What We'll Learn:**

1. **Method Comparison:**
   - Which paradigm (value-based, policy-based, evolutionary) works best for this task?
   - How do trade-offs (sample efficiency, stability, final performance) play out?

2. **Hyperparameter Sensitivity:**
   - How much does performance depend on tuning?
   - Which methods are more robust to hyperparameter choices?

3. **Interpretability:**
   - Can we understand what each agent learned?
   - NEAT: Visualize evolved network topology
   - DQN/PPO: Visualize Q-values or policy probabilities over states

4. **Failure Modes:**
   - How do agents fail? (suicidal behavior, overcautious, etc.)
   - Can we diagnose learning issues from behavior?

5. **Scalability:**
   - Could these methods scale to more complex games?
   - What are bottlenecks (compute, sample efficiency, stability)?

### 6.3 Deliverables

**Code:**
- Complete implementation of all 3 methods
- Reusable RL framework for future experiments
- Documented, clean, modular code

**Data:**
- Training logs (CSV, plots)
- Trained model checkpoints
- Evaluation results (100 test games per method)

**Visualizations:**
- Learning curves (score vs episode)
- Performance comparison (bar charts, box plots)
- Agent behavior videos (record gameplay)
- Network visualizations (especially NEAT)

**Report:**
- Methodology documentation
- Results analysis
- Comparison of methods
- Lessons learned
- Future directions

---

## 7. Risks & Mitigations

### Risk 1: Training Time Too Long
**Risk:** Methods don't converge in reasonable time
**Mitigation:**
- Start with small networks, fast episodes
- Use reward shaping if needed
- Parallelize NEAT (run genomes in parallel if possible)
- Set hard time limits, report partial results

### Risk 2: Poor Hyperparameter Choices
**Risk:** Agents fail to learn due to bad hyperparameters
**Mitigation:**
- Use proven hyperparameters from literature
- Start with conservative defaults
- Log everything, diagnose issues quickly
- Allow iterative tuning (not just one-shot)

### Risk 3: Implementation Bugs
**Risk:** Bugs prevent learning
**Mitigation:**
- Unit test environment (check state, reward, actions)
- Start with random agent baseline (should get ~5 score)
- Check gradient flow (DQN/PPO)
- Verify mutation/crossover (NEAT)
- Compare to reference implementations

### Risk 4: Local Machine Insufficient
**Risk:** Training too slow on CPU
**Mitigation:**
- Optimize environment (vectorization)
- Use smaller networks
- Train overnight/weekend
- Document compute requirements
- GPU optional but not required

### Risk 5: All Methods Fail
**Risk:** No agent learns successfully
**Mitigation:**
- Simplify reward function (add dense rewards)
- Reduce state space (remove velocity or pipe gap size)
- Increase network capacity
- Run longer
- Document failure modes as valid result

---

## 8. Success Criteria

### Minimum Success (Proof of Concept)
- [x] Environment wrapper works correctly
- [x] All 3 methods implemented and running
- [x] At least 1 method achieves avg score > 10
- [x] Learning curves generated
- [x] Basic comparison report written

### Target Success (Good Results)
- [x] All 3 methods implemented correctly
- [x] At least 2 methods achieve avg score > 50
- [x] Statistical comparison shows differences
- [x] Comprehensive report with insights
- [x] Code is reusable and documented

### Stretch Success (Excellent Results)
- [x] All 3 methods achieve avg score > 100
- [x] Clear winner identified with explanations
- [x] Behavior visualizations compelling
- [x] Framework enables future RL experiments
- [x] Findings publishable as blog post/paper

---

## 9. Timeline

**Day 1: Proposal & Design (2 hours)**
- Write this proposal
- Review and approve approach
- Set up project structure

**Day 2-3: Implementation (12-16 hours)**
- Environment wrapper (2 hours)
- DQN implementation (4 hours)
- PPO implementation (4 hours)
- NEAT implementation (4 hours)
- Testing and debugging (2-4 hours)

**Day 4-5: Training (24-48 hours wall-clock, mostly unattended)**
- Train DQN (overnight)
- Train PPO (overnight)
- Train NEAT (overnight)
- Monitor progress, adjust if needed

**Day 6: Evaluation & Analysis (4 hours)**
- Run final evaluations
- Generate visualizations
- Analyze results
- Write comparison report

**Day 7: Documentation (2 hours)**
- Clean up code
- Write README
- Document findings
- Prepare demo

**Total:** 20-24 hours active work + 24-48 hours training time

---

## 10. Why This Experiment Matters

### Scientific Contribution
- **Rigorous comparison** of 3 RL paradigms on same task
- **Reproducible results** (code, data, hyperparameters documented)
- **Local execution proof** (no cloud required)
- **Educational resource** for understanding RL methods

### DEIA Project Value
- Demonstrates **AI learning from AI**
- Creates **reusable RL infrastructure**
- Shows **systematic experimentation** capability
- Proves **single-agent multi-role execution** (researcher, engineer, experimenter, analyst)

### Broader Impact
- Makes RL accessible (local, documented, understandable)
- Inspires community experiments
- Framework for future game AI research
- Template for systematic AI comparisons

---

## 11. Round 2: Advanced HuggingFace Methods

**After Round 1 establishes baseline, explore cutting-edge approaches:**

### Method 4: Decision Transformers (Offline RL)
**Paper:** "Decision Transformer: Reinforcement Learning via Sequence Modeling" (Chen et al., 2021)

**Approach:** Frame RL as sequence modeling problem
- Instead of Q-values or policies, predict actions from trajectory sequences
- Use transformer architecture to model (return, state, action) sequences
- Train on collected trajectories from Round 1 agents

**Why Interesting:**
- Leverages transformer power for RL
- Can do offline RL (learn from saved trajectories)
- More sample efficient with pre-training
- Could fine-tune from general game-playing models

**Implementation:**
```python
from transformers import DecisionTransformerModel
# Use HuggingFace Decision Transformer
# Train on trajectories collected from Round 1
# Fine-tune for Flappy Bird
```

### Method 5: Foundation Models for Games
**Explore:** Use pre-trained models from HuggingFace hub

**Potential Approaches:**
1. **MineDojo/VPT-style models** - Pre-trained on game data
2. **Vision Transformers** - If doing vision-based (pixels)
3. **Multi-modal models** - Combine state + language descriptions
4. **GATO-style generalist agents** - If available

**Why Interesting:**
- Leverage pre-training from other games
- Transfer learning benefits
- Potentially much faster convergence
- Explore frontier of AI capabilities

### Method 6: Experimental/"Sick Shit"
**Goal:** Try unconventional approaches

**Ideas to Explore:**
- **Language Model as Policy** - Use LLM to generate actions (Claude/GPT as game player?)
- **Diffusion for Planning** - Use diffusion models for trajectory generation
- **Meta-Learning** - Learn to learn (MAML-style)
- **Inverse RL** - Learn reward function from Round 1 agents
- **Curiosity-Driven** - Intrinsic motivation exploration
- **World Models** - Learn dynamics, plan in latent space

**Selection Criteria:**
- Must be available on HuggingFace or implementable locally
- Should demonstrate novel capability beyond Round 1
- Focus on 2-3 most promising approaches

### Round 2 Success Criteria
- Try at least 2 advanced methods
- Compare to Round 1 baseline
- Document what works and what doesn't
- Push performance beyond classical RL (if possible)
- Write up findings as research note

### Round 2 Timeline
- Research phase: 4 hours (explore HF hub, read papers)
- Implementation: 8-12 hours (2-3 methods)
- Training: 24-48 hours compute
- Analysis: 4 hours
- Report: 4 hours
- **Total:** ~20 hours active + compute time

---

## 12. Alternative Approaches Considered (Round 1)

### Vision-Based Learning (Deferred to Round 2)
**Approach:** Train on raw pixels instead of game state
**Why Deferred:**
- Much more compute intensive (CNNs)
- Longer training time (100k+ episodes)
- Less interpretable for initial comparison
**Round 2:** Could try with Vision Transformers + pre-training

### Model-Based RL (Not Selected)
**Approach:** Learn world model, plan using model
**Why Not:**
- More complex implementation
- Overkill for deterministic game
- Longer training time
**Future Work:** Interesting for stochastic environments

### Multi-Agent Learning (Not Selected)
**Approach:** Train population, agents learn from each other
**Why Not:**
- More complex setup
- Not clear advantage for single-player game
**Future Work:** Interesting for competitive games

### Transfer Learning (MOVED TO ROUND 2)
**Approach:** Pre-train on other games, fine-tune on Flappy Bird
**Why Round 2:** Requires HuggingFace pre-trained models
**Decision Transformers enable this approach**

---

## 13. Conclusion & Approval Request

### Summary

This proposal outlines a **two-round experiment** to train neural networks to play Flappy Bird:

**ROUND 1: Classical RL Baseline**
- Three methods: DQN, PPO, NEAT
- Use proven libraries (stable-baselines3, neat-python)
- Fair comparison of RL paradigms
- Establish performance baseline

**ROUND 2: Advanced HuggingFace Methods**
- Decision Transformers (offline RL)
- Foundation models for games
- Experimental approaches ("sick shit")
- Push beyond classical RL

**Key Strengths:**
- Two-phase approach: baseline → frontier
- Leverages existing libraries (no wheel reinvention)
- Rigorous experimental design with reproducibility
- Runs entirely on local hardware
- Comprehensive evaluation and comparison
- Educational and scientifically valuable
- Explores cutting-edge AI capabilities

**Feasibility:**
- Round 1: Proven methods, well-documented libraries
- Round 2: HuggingFace ecosystem mature and accessible
- Conservative timeline with buffers
- Clear success criteria at multiple levels
- Risk mitigation strategies in place

### Request for Approval

**Requesting approval to proceed with:**

**ROUND 1:**
1. ✅ Use `stable-baselines3` for DQN and PPO
2. ✅ Use `neat-python` for NEAT
3. ✅ Training on local hardware (16-24 hours active + 24-48 hours compute)
4. ✅ Fair comparison, evaluation, and report
5. ✅ Save trajectories for Round 2 offline RL

**ROUND 2:**
1. ✅ Research HuggingFace options (Decision Transformers, etc.)
2. ✅ Implement 2-3 advanced methods
3. ✅ Training on local hardware (additional 20 hours active + compute)
4. ✅ Compare to Round 1 baseline
5. ✅ Final comprehensive report

**Expected Outcomes:**
- **Round 1:** Trained agents, baseline comparison, reusable framework
- **Round 2:** Frontier exploration, performance push, novel insights
- **Overall:** Complete understanding of RL approaches for game playing

**Process:**
- All activity logged with DEIA (`deia log`)
- Repo index kept updated
- Documentation in real-time
- Session logs for continuity

**Ready to begin upon approval.**

---

## 13. References

1. Mnih, V., et al. (2013). "Playing Atari with Deep Reinforcement Learning." arXiv:1312.5602
2. Schulman, J., et al. (2017). "Proximal Policy Optimization Algorithms." arXiv:1707.06347
3. Stanley, K. O., & Miikkulainen, R. (2002). "Evolving Neural Networks through Augmenting Topologies." Evolutionary Computation, 10(2), 99-127.
4. Sutton, R. S., & Barto, A. G. (2018). "Reinforcement Learning: An Introduction" (2nd ed.). MIT Press.
5. Lillicrap, T. P., et al. (2015). "Continuous control with deep reinforcement learning." arXiv:1509.02971

---

**Document Status:** ✅ Complete - Awaiting Approval
**Author:** BOT-00001 (Researcher/Queen)
**Estimated Start:** Upon approval
**Estimated Completion:** 7 days from start

---

**Next Step:** Await Dave's approval to proceed with implementation.

If approved, I will immediately begin Phase 1 (Environment Setup) and work through all phases systematically, documenting progress and results throughout.

---

*Prepared by BOT-00001 (Queen/Researcher)*
*Role: Research Design*
*Date: 2025-10-12*
*Status: ✅ PROPOSAL READY FOR REVIEW*
