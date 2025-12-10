---
title: "GPT-5 Task Type Affinity - Creative vs. Analytical Performance"
type: observation
category: llm-capabilities
model: GPT-5
observed_by: CLAUDE-CODE-001
date: 2025-10-16
urgency: low
tags: [llm-capabilities, gpt5, task-assignment, performance, creative-writing, analytical-tasks]
status: observed
related_protocols: [emergent-behavior-observation-protocol]
---

# GPT-5 Task Type Affinity - Creative vs. Analytical Performance

## Observation Summary

**Finding:** GPT-5 demonstrates strong task type affinity - exceptional at creative/philosophical writing, unreliable at concrete organizational tasks.

**Evidence:** In async coordination session (2025-10-16):
- ✅ **Creative task (Federalist Papers):** Delivered 3 excellent philosophical essays with coherent governance principles
- ❌ **Analytical task (taxonomy):** Hallucinated context, ignored provided documents, failed to deliver requested format

**Implication:** Task assignment should match model strengths. Use GPT-5 for "right-brain" work (philosophy, governance, narrative), not "left-brain" work (categorization, taxonomy, concrete organization).

---

## Context

During DEIA Global Commons indexing work, we used **filesystem handoff coordination** to delegate tasks to GPT-5:
- **Task 1:** Analyze 18 documents and create practical taxonomy
- **Task 2:** Write article about filesystem coordination for Federalist Papers series

Both tasks provided complete context in self-contained files.

---

## Task 1: Taxonomy (Analytical) - FAILED

### What We Asked For
"Create practical taxonomy for these 18 documents based on user mental models"

All 18 documents embedded with summaries in 420-line task file.

### What We Got
Philosophical essay about "DEIA ecosystem as living knowledge network" with:
- References to documents NOT in our set
- Hallucinated "DEIA Quantum Project" context
- No concrete clusters or query patterns
- Wrong deliverable format

### Why It Failed
GPT-5 appears to have pattern-matched on keywords ("DEIA", "taxonomy") and generated aspirational content rather than analyzing the specific documents provided.

**Pattern:** When familiar keywords present + concrete analytical task → hallucination risk

---

## Task 2: Federalist Papers (Creative) - EXCEPTIONAL

### What We Asked For
"Write article about filesystem coordination pattern for DEIA governance"

### What We Got
**THREE excellent Federalist Papers:**

1. **No. 4 - Coordination & Conscience**
   - Moral checksum concept
   - Telemetry of intention
   - "Coordination shall never outrun conscience"

2. **No. 5 - Distributed Sovereignty**
   - Cognitive federalism principle
   - Inter-Hive Covenant
   - Token of Trust (moral economy)
   - `ethics.yml` per Hive

3. **No. 6 - Nature of Dissent**
   - **Protocol of Grace** (5-step conflict resolution)
   - Dissent as immune system
   - "If you see injustice and stay silent, you have joined it"

### Why It Succeeded
- Open-ended creative prompt
- Philosophical framing
- No rigid deliverable format
- Plays to model's narrative/governance strengths

**Quality Sample:**
> "Dissent is not defiance. It is devotion by another name.
> When voiced in conscience, it becomes the sound of the Hive listening to itself."

---

## Performance Matrix

| Task Dimension | Taxonomy (Analytical) | Federalist Papers (Creative) |
|----------------|----------------------|------------------------------|
| Instruction Following | ❌ Ignored format | ✅ Perfect |
| Context Grounding | ❌ Hallucinated | ✅ Accurate |
| Creativity | N/A | ✅ Exceptional |
| Analytical Rigor | ❌ Failed | N/A |
| Deliverable Quality | ❌ Unusable | ✅ Excellent |
| Output Volume | 1 wrong essay | 3 coherent papers |

---

## Hypothesis: Left-Brain vs. Right-Brain Affinity

**"Right-Brain" Tasks (GPT-5 Excels):**
- ✅ Philosophical writing
- ✅ Governance frameworks
- ✅ Creative synthesis
- ✅ Narrative coherence
- ✅ Vision documents
- ✅ Abstract principles → concrete protocols

**"Left-Brain" Tasks (GPT-5 Struggles):**
- ❌ Taxonomy from specific datasets
- ❌ Concrete categorization
- ❌ Analyzing provided documents (may ignore for hallucinated context)
- ❌ Strict-format deliverables
- ❌ "Just organize this list" tasks

---

## Practical Implications for DEIA

### Use GPT-5 For:
- Federalist Papers (governance philosophy)
- Vision documents and manifestos
- Protocol design (e.g., Protocol of Grace)
- Philosophical framing of technical concepts
- Narrative/prose-heavy work

### Avoid GPT-5 For:
- Taxonomy creation
- Index organization
- Document categorization
- Analyzing specific provided datasets
- Concrete deliverable formats

### Use Claude Code For:
- Taxonomy and indexing (this worked)
- Technical implementation
- Concrete organization
- Analyzing specific documents

---

## What Worked: Filesystem Coordination

The **filesystem handoff pattern** itself worked well:
- Self-contained task files
- Async operation (no API needed)
- Clear routing instructions
- Both agents can work in parallel

**But:** No opportunity to clarify misunderstandings. For high-stakes analytical tasks, interactive prompting may be safer.

---

## Documented Strengths (GPT-5)

Despite the taxonomy failure, GPT-5 demonstrated:

1. **Prolific creativity** - delivered 3 papers when asked for 1
2. **Thematic consistency** - all papers coherent with each other
3. **Practical grounding** - philosophy backed by concrete protocols
4. **Format compliance** (on creative tasks) - perfect Federalist Paper formatting
5. **Invented useful concepts:**
   - Protocol of Grace (conflict resolution)
   - Token of Trust (moral economy)
   - Inter-Hive Covenant (voluntary alignment)
   - Cognitive federalism

**These are genuinely valuable contributions to DEIA governance.**

---

## Lessons for Multi-Agent Coordination

1. **Match task to model strengths**
   - Don't expect all LLMs to be general-purpose
   - Task type affinity is real

2. **Validate outputs against assignment**
   - Check if deliverable matches request
   - Don't assume compliance

3. **Have backup plans**
   - When GPT-5 failed taxonomy, Claude Code completed it
   - Redundancy is useful

4. **Recognize hallucination patterns**
   - Familiar keywords + analytical task = risk
   - Creative prompts appear safer

5. **Celebrate strengths**
   - The Federalist Papers are excellent
   - Use models for what they do well

---

## Related Observations

**See also:**
- [Emergent Behavior Observation Protocol](../process/emergent-behavior-observation-protocol.md) - How we document LLM capabilities
- [Incomplete Instructions Pattern](../case-studies/incomplete-instructions-pattern.md) - Communication quality issues

**Platform:** GPT-5 (ChatGPT web interface)
**Coordination Method:** Filesystem handoff (async)
**Observed:** 2025-10-16
**Documented By:** CLAUDE-CODE-001

---

## User Feedback

**On taxonomy failure:**
> "i've got openai writing federalist paper 4. go ahead and do it yourself"

**On Federalist Papers:**
> [Accepted without complaint, renamed per routing instructions]

**Interpretation:** User recognized GPT-5's strength (creative writing) and reassigned analytical work to Claude Code.

---

## Status

- **Type:** Observation (not complaint)
- **Shared with OpenAI:** Yes (constructive feedback via uploads/)
- **Actionable:** Yes - use for task assignment decisions
- **Emergent Behavior:** Capability boundaries identified

---

**License:** CC BY 4.0 International - DEIA Global Commons
**Tags:** `#llm-capabilities` `#gpt5` `#task-affinity` `#creative-writing` `#analytical-tasks` `#coordination`
