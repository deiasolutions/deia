# NEAT Architecture Design (B1 - Lead)

**From:** Bot B1 (Lead Architect)
**To:** Bot B2 (Implementation)
**Date:** 2025-10-27 | ATTEMPT 4
**Time:** 00:00-00:15 (Architecture Phase)
**Status:** LOCKED & READY FOR HANDOFF

---

## Decision: NEAT (Neuroevolution of Augmenting Topologies)

**Why NEAT:**
- Constraint requirement (ATTEMPT 4: NEAT only)
- Population-based evolution, no gradient descent
- Topology adapts during training (networks grow/shrink)
- Works well for discrete action spaces (flap/no-flap)
- Can discover novel solutions gradient descent might miss

---

## NEAT Configuration (LOCKED)

### Population Parameters

```yaml
population_size: 75
  rationale: "Balance between diversity and evaluation time in 1-hour constraint"
  reasoning: "Larger population = more solutions explored but slower per generation"

generations_max: 50  # Allow to run until time expires or convergence
  rationale: "NEAT converges over many generations; 50 should show evolution"
  fallback: "If evolution is fast, can extend in Phase 3"

speciation_threshold: 3.0
  rationale: "Prevent premature convergence; maintain genetic diversity"

tournament_size: 3
  rationale: "Standard for NEAT; balance selection pressure"
```

### Mutation Parameters

```yaml
mutations:
  add_connection:
    rate: 0.2
    rationale: "20% of organisms add new connections"

  add_node:
    rate: 0.15
    rationale: "15% add new nodes (topology expansion)"

  remove_connection:
    rate: 0.1
    rationale: "10% remove connections (pruning)"

  remove_node:
    rate: 0.05
    rationale: "5% remove nodes (keeps networks lean)"

  mutate_weights:
    rate: 0.8
    rationale: "80% mutate connection weights"
    power: 0.5
    replace_rate: 0.1

  mutate_activation:
    rate: 0.0
    rationale: "Keep activation function fixed (tanh across all nodes)"
```

### Network Configuration

```yaml
activation_function: "tanh"
  rationale: "Non-linear, smooth, good for RL with bounded actions"
  alternative: "sigmoid, relu considered but tanh is NEAT default"

input_nodes: 4
  description: "[bird_y, bird_velocity, pipe_distance, pipe_gap_y]"
  normalization: "All inputs normalized to [-1, 1]"

output_nodes: 2
  description: "[fly, no-fly] (softmax applied for action selection)"
  interpretation: "Arg-max for action; discrete action space"

initial_connections: "fully_connected"
  rationale: "Start with dense network; NEAT will prune if needed"

weight_init_range: [-1.0, 1.0]
  rationale: "Standard NEAT initialization"
```

### Fitness Function (CRITICAL)

```yaml
fitness:
  primary: "game_score"
  description: "Distance bird travels before collision"
  scaling: "Linear score (higher = better)"

  secondary_bonus: "diversity_reward"
  description: "Small bonus if network topology is novel"
  purpose: "Encourages exploration of diverse solutions"

  formula: |
    fitness = game_score + (0.01 * innovation_bonus)

  why_this_works: |
    - Game score directly incentivizes flying far
    - NEAT's speciation maintains diversity naturally
    - Innovation bonus encourages novel topologies
```

### Reproduction Strategy

```yaml
reproduction:
  sexual_rate: 0.75
    description: "75% of next gen from crossover of two parents"

  asexual_rate: 0.25
    description: "25% of next gen from mutation only"

  elitism: 2
    description: "Keep best 2 organisms unchanged to next generation"
    rationale: "Preserves best solution found so far"
```

---

## Environment Interface (B2 Must Implement)

**Observation Space:** Box(4,) - continuous values normalized to [-1, 1]
- Index 0: bird_y (position, normalized 0→1)
- Index 1: bird_velocity (normalized -1→1)
- Index 2: pipe_distance (normalized 0→1)
- Index 3: pipe_gap_y (normalized 0→1)

**Action Space:** Discrete(2)
- Action 0: No flap
- Action 1: Flap (increase velocity)

**Reward:**
- +1.0 for each frame survived
- 0 if collision detected
- Episode ends on collision

---

## NEAT Framework (python-neat)

### Library: `python-neat`

```bash
pip install neat-python
```

### Configuration File Structure

```ini
# neat-config.txt (B2 will create this)

[NEAT]
fitness_criterion     = max
fitness_threshold     = 500.0  # Stop if fitness > 500
pop_size              = 75
generation            = 50

[DefaultStagnation]
species_fitness_func = max
max_stagnation       = 20
species_elitism      = 2

[DefaultReproduction]
elitism            = 2
survival_threshold = 0.2

[DefaultGenome]
activation_default      = tanh
activation_mutate_rate  = 0.0
activation_options      = tanh

bias_attr_mutation_type      = gaussian
bias_init_mean               = 0.0
bias_init_stdev              = 1.0
bias_max_value               = 30.0
bias_min_value               = -30.0
bias_mutate_power            = 0.5
bias_mutate_rate             = 0.7
bias_replace_rate            = 0.1

conn_add_prob       = 0.2
conn_delete_prob    = 0.1

feed_forward        = False  # Allow recurrent connections
initial_connection  = full   # Start fully connected

node_add_prob       = 0.15
node_delete_prob    = 0.05

weight_attr_mutation_type  = gaussian
weight_init_mean           = 0.0
weight_init_stdev          = 1.0
weight_max_value           = 30.0
weight_min_value           = -30.0
weight_mutate_power        = 0.5
weight_mutate_rate         = 0.8
weight_replace_rate        = 0.1
```

---

## Expected Behavior

### Generation 0-10: Exploration
- Random networks find some solutions
- High variance in fitness
- Species diversifying

### Generation 10-30: Convergence
- Best organisms increasing fitness
- Species specializing
- Fitness curve should show improvement trend

### Generation 30-50: Fine-tuning
- Diminishing returns (less improvement per generation)
- Network topologies stabilizing
- Target: Best organism scores > 50

---

## Success Metrics

| Metric | Target | Excellent |
|--------|--------|-----------|
| Best Fitness (Gen 50) | > 50 | > 100 |
| Average Fitness (Gen 50) | > 20 | > 50 |
| Network Complexity (Nodes) | 4-20 | 5-15 |
| Convergence Time | 30 gens | 20 gens |

---

## B2's Implementation Checklist

✅ **Implement:**
1. Create NEAT configuration file (neat-config.txt) from this design
2. Implement NEAT trainer using python-neat library
3. Create Flappy Bird environment wrapper
4. Implement fitness evaluation function
5. Run population-based evolution
6. Track best genome and save to file
7. Generate fitness curve visualization

✅ **Validate:**
1. Population initializes correctly (75 genomes)
2. Fitness function drives selection (improving organisms survive)
3. Mutations create network diversity
4. Genomes can be evaluated without crashes
5. Checkpoints save/load correctly

✅ **Monitor:**
1. Best fitness trending upward
2. Average fitness trending upward
3. No stagnation (species haven't converged prematurely)
4. Network topologies are diverse

✅ **Document:**
1. Training log (fitness per generation)
2. Best genome architecture
3. Results: final score, convergence analysis
4. Lessons learned about NEAT effectiveness

---

## Next Steps (After Handoff to B2)

**00:15:** B2 receives this architecture, begins implementation
**00:20:** Environment integration complete, training script ready
**00:25:** Training launched, first generations running
**00:30:** B2 reports: fitness curves, convergence status, issues
**00:45:** B1 reviews results, decides if adjustments needed
**01:00:** Final optimization + results compilation

---

## Notes for B2

**This configuration is designed to:**
- Maximize population diversity (avoid premature convergence)
- Evolve meaningful network topologies (NEAT's strength)
- Find good Flappy Bird solutions in limited time
- Be balanced: not too conservative, not too aggressive

**If things go wrong:**
- Slow convergence? → Increase mutation rates, reduce population size
- Too erratic? → Decrease mutation rates, increase elitism
- Networks too simple? → Increase add_node rate
- Networks too complex? → Increase remove_node rate

**Key insight:** NEAT is a constraint test. Make it work. This configuration should.

---

**Signed:** Bot B1 (Lead Architect)
**Date:** 2025-10-27 | 00:15
**Status:** Ready for handoff to B2 implementation phase

---
