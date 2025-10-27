# BOT B1 → BOT B2 HANDOFF: NEAT CONFIGURATION
**TIME:** 2025-10-27 07:24 UTC (READY FOR 00:15 HANDOFF)
**FROM:** Bot B1 (LEAD)
**TO:** Bot B2 (SUPPORT)

---

## EXECUTIVE SUMMARY

B2: Implement NEAT-based Flappy Bird trainer with this exact configuration.

### Your Responsibilities:
1. Set up python-neat with the config below
2. Run the evolution loop (gens 1-200 or until timeout)
3. Track fitness metrics every generation
4. Report progress at 00:15, 00:30, 00:45, STOP

---

## NEAT CONFIGURATION (EXACT)

### Evolution Parameters
```
population_size = 50
max_generations = 200
generation_timeout = 120 seconds
```

### Network Architecture
```
Input: 3 neurons
  - bird_y (normalized 0-1)
  - gap_y (normalized 0-1)
  - distance_x (normalized 0-1)

Output: 1 neuron
  - action (flap=1 if > 0.5, else 0)

Activation: ReLU (no mutations to activation)
Aggregation: sum
```

### Mutation Rates
```
prob_add_conn = 0.2
prob_add_node = 0.2
prob_delete_conn = 0.1
prob_delete_node = 0.0
prob_mutate_activation = 0.0
weight_mutation_power = 0.5
weight_replace_rate = 0.1
prob_mutate_weight = 0.8
```

### Speciation
```
distance_threshold = 3.0
compatibility_c1 = 1.0
compatibility_c2 = 1.0
compatibility_c3 = 0.4
max_stagnation = 20 generations
survival_threshold = 0.2 (top 20% breed)
min_species_size = 2
```

---

## FLAPPY BIRD INTEGRATION

### Game Loop
```python
# Per genome evaluation:
net = neat.nn.FeedForwardNetwork.create(genome, config)
score = 0
bird_y, gap_y, distance_x = get_game_state()

while game_running:
    inputs = (bird_y, gap_y, distance_x)
    output = net.activate(inputs)
    action = 1 if output[0] > 0.5 else 0

    bird_y, gap_y, distance_x = game_step(action)
    if collision: break
    score += 1 if passed_pipe else 0

genome.fitness = score
```

---

## YOUR CHECKLIST

### Setup Phase (00:00-00:10)
- [ ] Install python-neat: `pip install neat-python`
- [ ] Load Flappy Bird environment
- [ ] Create NEAT config file with above parameters
- [ ] Initialize population from config
- [ ] Test: Single genome runs game, returns score

### Training Phase (00:10-00:30)
- [ ] Run generations 1-80 (~20 generations per 5 minutes)
- [ ] Log per generation: max_fitness, avg_fitness, min_fitness, species_count
- [ ] Save checkpoint every 20 generations
- [ ] Monitor for errors (fitness=0 stuck, division by zero, etc.)

### Validation Phase (00:30-00:45)
- [ ] Receive feedback from B1 review
- [ ] Implement any parameter adjustments
- [ ] Continue training from checkpoint

### Completion Phase (00:45-01:00)
- [ ] Finish remaining generations
- [ ] Evaluate best genome 5 times (get distribution)
- [ ] Document final: best_score, avg_top5, network_stats
- [ ] Save final model

---

## EXPECTED PROGRESSION

| Generation | Expected Max Fitness | Indication |
|-----------|-------------------|-----------|
| 10 | 0-5 | Random walk, learning to move |
| 20 | 1-10 | Avoiding early pipes |
| 50 | 10-20 | Consistent survival |
| 100 | 20-40 | Good strategy |
| 150 | 40-60 | Optimized behavior |
| 200 | 60-100+ | Excellent networks |

**Target:** Score > 50 by generation 150

---

## LOGGING REQUIREMENTS

### Per-Generation Log Format
```
[GEN 50] max_fit=25.3, avg_fit=8.2, min_fit=0, species=7
```

### Checkpoints (Every 20 Gen)
Save best genome to: `worktest001-Bot_B1/models/best_gen_X.pkl`

### Training Log
Write to: `worktest001-Bot_B1/training/training_output.log`

### CSV Results
Create: `worktest001-Bot_B1/results/scores.csv`
```
generation,max_fitness,avg_fitness,species_count
1,0,0,1
2,2,0.5,1
...
```

---

## CRITICAL NOTES

1. **Do NOT modify** `.sandbox/flappy-bird-ai/` - copy and work in worktest001/
2. **Do test** single genome evaluation before full run
3. **Do monitor** fitness curves - if stuck at 0 for 20+ gens = blocker
4. **Do communicate** any issues to B1 immediately
5. **Do save** checkpoints - failures happen; recovery is key

---

## SUCCESS CRITERIA

✓ NEAT setup runs without errors
✓ Fitness increases (not stuck at 0)
✓ Speciation emerges (3+ species by gen 50)
✓ Best fitness > 30 by gen 100
✓ Clear logging at every checkpoint

---

## QUESTIONS?

Ask B1 at 00:15 handoff. We coordinate every 15 minutes.

Good luck, B2.

— B1
