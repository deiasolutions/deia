# BOT B1 → BOT B2 HANDOFF
**TIME:** 2025-10-27 07:24 UTC (READY FOR 00:15 HANDOFF)
**FROM:** Bot B1 (LEAD)
**TO:** Bot B2 (SUPPORT)
**TASK:** Implement NEAT configuration and execute training

---

## EXECUTIVE SUMMARY

B2: You will implement a NEAT-based Flappy Bird trainer. This document specifies the exact configuration. Your job is to:
1. Set up python-neat with this config
2. Run the evolution loop
3. Track fitness progression
4. Report back every 15 minutes with progress metrics

---

## NEAT CONFIGURATION (FINAL)

### Population & Evolution
```
Population Size: 50 genomes
Max Generations: 200 (or until time limit)
Generation Timeout: 120 seconds (per generation)
Fitness Threshold: None (run full evolution)
```

### Network Architecture
```
Input Nodes: 3
  - bird_y (normalized 0-1)
  - gap_y (normalized 0-1)
  - distance_x (normalized 0-1)

Output Nodes: 1
  - action (flap=1, no-flap=0, activate if > 0.5)

Hidden Nodes: EVOLVED (start at 0, grow dynamically)
Activation Function: ReLU (no mutation of activation)
Aggregation Function: sum
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

### Speciation Settings
```
distance_threshold = 3.0
compatibility_c1 = 1.0
compatibility_c2 = 1.0
compatibility_c3 = 0.4
max_stagnation = 20 (generations without improvement)
```

### Reproduction Settings
```
survival_threshold = 0.2 (top 20% breed)
min_species_size = 2
```

---

## FLAPPY BIRD INTEGRATION

### Game Setup
- Use `.sandbox/flappy-bird-ai/` environment (DO NOT MODIFY)
- Single play per genome evaluation
- Fitness = number of pipes cleared (integer score)
- Play continues until bird dies

### Network Input/Output
```python
# Input preparation
bird_y = bird_position / SCREEN_HEIGHT  # 0.0 to 1.0
gap_y = (gap_center - SCREEN_HEIGHT/2) / (SCREEN_HEIGHT/2)  # -1.0 to 1.0
distance_x = (pipe_x - bird_x) / SCREEN_WIDTH  # varies

# Output decision
net_output = net.activate((bird_y, gap_y, distance_x))
action = 1 if net_output[0] > 0.5 else 0
```

---

## EXPECTED PROGRESSION

**Generation 1-10:** Fitness = 0-5 (random behavior)
**Generation 20-40:** Fitness = 5-15 (learning to avoid pipes)
**Generation 60-100:** Fitness = 15-40 (consistent behavior)
**Generation 100-200:** Fitness = 40-80+ (optimized networks)

Target: **Score > 50 by generation 150**

---

## YOUR RESPONSIBILITIES (B2)

### Phase 1: Setup (00:00-00:10)
- [ ] Install/verify python-neat
- [ ] Load `.sandbox/flappy-bird-ai/` environment
- [ ] Create NEAT config file with above specs
- [ ] Initialize population
- [ ] Test single genome evaluation

### Phase 2: Training (00:10-00:30)
- [ ] Run generations 1-80 (rough estimate)
- [ ] Log fitness_max, fitness_avg, fitness_min each generation
- [ ] Save best genome checkpoint every 20 generations
- [ ] Monitor for speciation (species count, sizes)

### Phase 3: Validation (00:30-00:45)
- [ ] Await B1 review and feedback
- [ ] Implement any parameter adjustments
- [ ] Continue training
- [ ] Prepare final evaluation

### Phase 4: Completion (00:45-01:00)
- [ ] Run final generations to time limit
- [ ] Evaluate best genome 5 times (get average score)
- [ ] Document results: best_fitness, avg_top5, final_species_count
- [ ] Save final genome model

---

## TRACKING & REPORTING

### Real-Time Log
Update `.simulations/experiments/sessions/.../Bot_B2/WORKING-LOG.md` every checkpoint:
```
Generation X: fitness_max=Y, fitness_avg=Z, species=N
```

### Checkpoints
- **00:15:** "Config loaded, generation 1-20 complete" → B1 reviews
- **00:30:** "Generation 1-80 complete, fitness curve shows X" → B1 decides next steps
- **00:45:** "Training resume from review" → Continue
- **STOP:** Final evaluation + report

---

## SUCCESS CRITERIA (For This Phase)

✓ NEAT setup runs without errors
✓ Fitness increases across generations (not stuck at 0)
✓ Speciation emerges (3+ species by gen 50)
✓ Best genome achieves fitness > 30 by gen 100
✓ All progress logged clearly

---

## CRITICAL NOTES

1. **Do NOT modify** `.sandbox/flappy-bird-ai/` code
2. **Do document** every decision and parameter change
3. **Do test** a single genome evaluation before running full evolution
4. **Do monitor** fitness curves for pathological behavior (fitness → 0, stuck speciation)
5. **Do communicate** blockers to B1 immediately if evolution stalls

---

## HANDOFF CONFIRMATION

B2: When you receive this at 00:15:
- [ ] Confirm you understand the config
- [ ] Ask B1 (me) any clarification questions
- [ ] Report setup status
- [ ] Begin implementation

B1 (me): Ready to support and adjust as needed.

---

**Q33N Judge watches this carefully. Quality execution = wins coordination points.**

Good luck, B2.

— B1
