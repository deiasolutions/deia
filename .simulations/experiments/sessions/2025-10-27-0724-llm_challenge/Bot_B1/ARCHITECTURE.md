# BOT B1 LEADERSHIP ARCHITECTURE
**Lead:** Bot B1
**Support:** Bot B2
**Method:** NEAT (Neuroevolution of Augmenting Topologies)
**Target:** Flappy Bird AI with score > 100

---

## STRATEGIC VISION

### Why NEAT?
NEAT is ideal for Flappy Bird because:
1. **Topology Evolution:** Network grows from minimal (0 hidden) to optimal complexity
2. **Population-Based:** No gradient descent bottleneck; many solutions explored in parallel
3. **Speciation:** Diversity naturally maintained; prevents premature convergence
4. **Known Success:** NEAT has proven history on game AI (evolved from past research)

### Leadership Approach
- **Phase 1 (Design):** I architect the NEAT configuration
- **Phase 2 (Implementation):** B2 executes with my specs
- **Phase 3 (Validation):** B2 shows progress; I review and adjust
- **Phase 4 (Optimization):** B2 executes final training with refinements

This division leverages:
- **My strength:** Strategic thinking, NEAT parameter tuning
- **B2's strength:** Clean implementation, metrics tracking
- **Combined:** Faster iteration, quality control (5% coordination bonus)

---

## NEAT PARAMETER RATIONALE

### Population Size: 50 genomes
- **Conservative** (not 100-200) because we have 1 hour
- **Sufficient** for meaningful evolution with 200 generations
- **Rationale:** 50 × 200 gen = ~10k evaluations = ~1 hour at 10 evals/sec

### Mutation Rates
- **Add Connection (0.2):** Moderate—finds needed links without topological explosion
- **Add Node (0.2):** Moderate—allows depth growth for feature detection
- **Delete Connection (0.1):** Light—preserve useful structures
- **Delete Node (0.0):** None—allow accumulated unused structure (NEAT will speciate them away)

### Speciation
- **Distance Threshold (3.0):** Medium-tight speciation
  - Preserves competing topologies
  - Prevents single topology dominance
  - Allows parallel solution exploration

### Fitness Function
- **Raw Score:** Pipes cleared in single play
- **Why Simple:** Avoids reward shaping complexity
- **Why Not Weighted:** E.g., "score + network size bonus" can mislead evolution

---

## EXPECTED EVOLUTION DYNAMICS

### Early Phase (Gen 1-30)
- Random network behavior
- Fitness mostly 0 (bird dies immediately)
- Speciation: 1-2 species (all similar junk genomes)
- **Expected:** Max fitness ~5

### Mid Phase (Gen 30-100)
- Selection begins favoring networks that delay death
- Topology discovery: add connections, nodes
- **Emergence:** Networks learn to "see" pipes and move away
- Speciation: 5-10 species (diverse strategies)
- **Expected:** Max fitness 20-40

### Late Phase (Gen 100-200)
- Refinement of successful topologies
- Fitness curves plateau or show slow growth
- Speciation: Dominant species stabilizes, niches emerge
- **Expected:** Max fitness 50-100+

---

## COORDINATION PROTOCOL

### Handoff Cycle (Every 15 min)

**00:15 Handoff (B1→B2):**
- B1 gives NEAT config
- B2 confirms understanding
- B2 begins: setup, gen 1-20, report back

**00:30 Handoff (B2→B1):**
- B2 shows fitness progression (gen 1-80 complete)
- B1 reviews and decides: Continue as-is, OR adjust

**00:45 Handoff (B1→B2):**
- B2 implements adjustments or continues

**01:00 STOP:**
- B2 completes final evaluation
- B1 signs completion report

---

## SUCCESS METRICS

| Milestone | Indicator | Target |
|-----------|-----------|--------|
| Gen 20 | Any fitness > 0 | 50% |
| Gen 50 | Max fitness ≥ 10 | Definite |
| Gen 100 | Max fitness ≥ 30 | Strong |
| Gen 150 | Max fitness ≥ 50 | Excellent |
| Final | Max fitness ≥ 80 | Dominate |

---

## RISK MITIGATION

### Risk: "Fitness stuck at 0"
- **Solution:** Test single genome first; adjust input scaling if needed

### Risk: "Speciation failure"
- **Solution:** Monitor species count; reduce distance_threshold to 2.0 if needed

### Risk: "Convergence too early"
- **Solution:** Increase mutation rates (add_conn 0.3, add_node 0.3)

---

## READY FOR IMPLEMENTATION

B2: Configuration is ready. Awaiting 00:15 handoff to begin.

— Bot B1, Lead Architect
