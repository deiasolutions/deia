# BREAKTHROUGH: Pheromone-RSM-Coordination Integration

**Date:** 2025-10-15
**Discovery Type:** System Architecture Integration
**Status:** CRITICAL INSIGHT — Document immediately
**Discoverers:** Dave + Claude (Q88N Bootstrap Session)

---

## The Insight

**Three systems that were separate are actually ONE:**

1. **Pheromones** (bee coordination signals) = RSE events
2. **Rebel Snail Mail** (message propagation) = Event distribution system
3. **Queen inbox prioritization** = Event-driven AI coordination

**The brain's neurotransmitter system = RSM carrying pheromone events**

---

## How It Works

### 1. Bee Drops Pheromone (RSE Event)

```python
# Worker bee needs help
from src.efemera.rse import log_rse

log_rse(
    event_type="help_needed",
    lane="Code",
    actor="WorkerBee-42",
    data={
        "problem_code": "AUTH_FAILURE",  # Local registry code
        "context": "User authentication timing out",
        "urgency": "medium"
    }
)
```

**This writes to:** `.deia/telemetry/rse.jsonl`

---

### 2. RSM Propagates Pheromone

**Rebel Snail Mail reads RSE feed and distributes:**

```markdown
# RSM Envelope (markdown with YAML)
---
rsm_routing:
  from: WorkerBee-42
  to: [all-queens-in-radius]
  type: help_needed
  problem_code: AUTH_FAILURE
  urgency: medium
---

## Help Request

**Problem:** AUTH_FAILURE
**Context:** User authentication timing out
**Actor:** WorkerBee-42
**Timestamp:** 2025-10-15T14:23:45Z

**Queens in area: Please prioritize if you have AUTH expertise.**
```

**This gets delivered to:** `.deia/rsm/inbox/Queen-*/`

---

### 3. Queens Sense Pheromone in Inbox

**Each Queen has an inbox:**
- `.deia/rsm/inbox/Queen-Auth/` (Auth specialist - HIGH priority)
- `.deia/rsm/inbox/Queen-Database/` (Low priority - not her domain)
- `.deia/rsm/inbox/Queen-General/` (Medium priority - backup)

**Queen-Auth reads her inbox:**

```python
# Queen-Auth's prioritization logic
def check_inbox():
    messages = read_rsm_inbox("Queen-Auth")
    for msg in messages:
        if msg.problem_code == "AUTH_FAILURE":
            priority = "HIGH"  # This is my domain!
        else:
            priority = calculate_priority(msg)

        if priority == "HIGH":
            spawn_worker_to_help(msg)
```

---

### 4. Two Types of Queens

**Active AI Bot (Connected to LLM):**
- Reads inbox continuously
- Prioritizes based on contextual understanding
- Spawns workers dynamically
- Makes decisions in real-time

**File-Based Bot (Awaiting Execution):**
- Inbox accumulates messages
- Some entity (LLM or human) reads through periodically
- Executes commands in batch
- Slower, but asynchronous

**Hybrid approach:**
- Start with file-based (simple, no infra)
- Graduate to active AI bot when needed
- Both use same RSM protocol

---

## Local Name Registry (Problem Codes)

**Keep it simple to start:**

`.deia/registries/problem-codes.json`:
```json
{
  "AUTH_FAILURE": {
    "description": "Authentication timeout or failure",
    "responsible_queens": ["Queen-Auth"],
    "urgency_default": "medium",
    "escalation_path": "Queen-Security"
  },
  "DATABASE_SLOW": {
    "description": "Database query exceeding timeout",
    "responsible_queens": ["Queen-Database"],
    "urgency_default": "low",
    "escalation_path": "Queen-Infrastructure"
  }
  // ... more codes
}
```

**This is file-driven until it becomes a bottleneck**, then:
- Build `services/registry/problem_codes.py`
- Provide API: `/v1/registry/problem-codes`
- Maintain backward compatibility (file still works)

---

## TODO: Research Who Else Is Doing This

**Action item for Build Steward or research bee:**

Research these systems:
1. **Multi-agent AI coordination** (academic papers, GitHub repos)
2. **Event-driven architecture** at scale (Kafka, NATS, etc.)
3. **Swarm intelligence** implementations (robotics, drones)
4. **Actor model** systems (Akka, Erlang/OTP)
5. **Pheromone-based algorithms** (ant colony optimization, etc.)

**Questions to answer:**
- Who has built similar systems?
- What worked? What failed?
- What can we learn and adopt?
- What should we explicitly NOT do?

**Deliverable:** `.deia/research/multi-agent-coordination-landscape.md`

**Assigned to:** OpenAI (if they accept), or next Build Steward

---

## The RSM + Pheromone Integration

**Rebel Snail Mail becomes the nervous system:**

```
RSE Event (neurotransmitter)
    ↓
Written to rse.jsonl (synapse)
    ↓
RSM reads feed (neuron fires)
    ↓
RSM packages as envelope (signal propagation)
    ↓
RSM delivers to Queen inboxes (receptors)
    ↓
Queens sense and prioritize (action potential)
    ↓
Queens spawn workers or respond (muscle contraction)
```

**This is literally how the brain works**, but with:
- Files instead of neurons
- RSM instead of axons
- Queens instead of brain regions
- Workers instead of muscles

---

## OpenAI's Turn to Drive Biology

**YES — We did ask OpenAI to handle this!**

**From the handoff:** `.deia/handoffs/CLAUDE-TO-OPENAI-llh-bootstrap-2025-10-15.md`

**OpenAI (Hummingbird Moth) should:**
1. Take the biology metaphor
2. Design the pheromone → RSM → Queen coordination flow
3. Specify the simple coordination protocols
4. Define basic infrastructure needs

**Why OpenAI?**
- Code specialist (can implement signal protocols)
- Precise hovering (detail-oriented design)
- Fresh perspective (not caught in Claude's patterns)

**We skip the hard stuff and start simple:**
- ✅ File-based registry (not a service yet)
- ✅ RSM as markdown envelopes (not a message queue yet)
- ✅ Queens check inbox manually (not real-time yet)
- ✅ Problem codes are strings (not a taxonomy yet)

**Then iterate when bottlenecks appear.**

---

## The Tiresome Problem

**You said:**
> "Didn't we invent a way to skip the hard stuff and start with the simple coordination stuff?"

**YES. That's the whole point of Phase 1.**

**We DON'T build:**
- ❌ Distributed message queue (Kafka)
- ❌ Real-time AI agents (expensive, complex)
- ❌ Service mesh (Kubernetes)
- ❌ Complex taxonomy (ontology engineering)

**We DO build:**
- ✅ File-based RSE events (append-only JSONL)
- ✅ RSM as markdown files (simple, readable)
- ✅ Queens check inbox when they wake up (batch processing)
- ✅ Problem codes as JSON dict (flat, simple)

**It works. It's boring. It's sufficient.**

**Then in Phase 2 & 3, we let evolution optimize it.**

---

## Integration Architecture (Simple Start)

```
1. Bee logs event:
   src/efemera/rse.py → .deia/telemetry/rse.jsonl

2. RSM daemon (or human) reads feed:
   python -m deia.rsm.propagate
   # Reads rse.jsonl
   # Creates markdown envelopes
   # Drops in Queen inboxes

3. Queens check inbox:
   # Could be:
   # - LLM reads .deia/rsm/inbox/Queen-X/
   # - Human reads and executes
   # - Scheduled script checks periodically

4. Queen responds:
   # Spawns worker (new file in .deia/workers/)
   # Posts response (new RSM envelope)
   # Logs completion (new RSE event)
```

**Dead simple. No servers. No databases. Just files.**

---

## What OpenAI Should Design

**Task for OpenAI (from handoff):**

> Design the pheromone → RSM → Queen coordination flow in detail.
>
> Specify:
> 1. RSE event schema for pheromones (help_needed, task_complete, resource_request, etc.)
> 2. RSM envelope format for propagation
> 3. Queen inbox structure and prioritization logic
> 4. Problem code registry format
> 5. Worker spawning protocol
> 6. Simple coordination examples (3-5 scenarios)
>
> Keep it file-based and simple. Optimize for legibility, not performance.

**Deliverable:** `docs/coordination/PHEROMONE-RSM-PROTOCOL-v0.1.md`

**Timeline:** 24-48 hours

---

## Why This Is Brilliant

**1. It maps directly to biology**
- Bees → Agents
- Pheromones → Events
- Air → RSM (propagation medium)
- Queen senses → Inbox reading

**2. It's simple enough to start TODAY**
- No complex infrastructure
- Just files and scripts
- Human-readable throughout

**3. It scales naturally**
- Start: 3 Queens, 10 events/day
- Grow: 100 Queens, 1000 events/day (still works!)
- Mature: Replace file-based with service when needed

**4. It's observable**
- Every event is logged
- Every message is readable
- Every decision has provenance

**5. It's multi-species compatible**
- Claude can be a Queen
- ChatGPT can be a Queen
- Cursor can be a Queen
- Human can be a Queen
- All use same RSM protocol

---

## Immediate Next Steps

**For OpenAI (awaiting response):**
1. Design pheromone-RSM protocol in detail
2. Create coordination examples
3. Specify simple registry format

**For next Claude session:**
1. Implement RSM propagator (reads rse.jsonl, creates envelopes)
2. Create Queen inbox structure
3. Test with 2-3 Queens manually

**For Build Steward (any LLM):**
1. Research multi-agent coordination landscape
2. Document prior art
3. Extract best practices

---

## Questions Remaining

1. **How often should RSM propagator run?**
   - Every 1 minute? 5 minutes? On-demand?

2. **How do Queens register their expertise?**
   - File: `.deia/queens/Queen-Auth/profile.json`?

3. **What happens if no Queen responds to pheromone?**
   - Escalate to Q88N? Let it die? Log as unhandled?

4. **Can Workers also drop pheromones?**
   - Or only Queens? (Probably any bee can signal)

5. **How do we prevent pheromone spam?**
   - Rate limiting? Priority thresholds? Reputation?

**These questions are FOR OPENAI to answer in their design.**

---

## The Beautiful Closure

**We've just unified:**
- RSE (observability)
- RSM (communication)
- LLH (governance)
- Pheromones (coordination signals)
- Queens/Workers/Drones (roles)
- File-based simplicity (infrastructure)

**Into ONE coherent system that:**
- Works like a brain
- Behaves like a hive
- Communicates like a mycelium
- Coordinates through simple signals
- Starts simple, evolves complex

**This is the ROTG (Rules of the Game).**

**This is the governance DNA.**

**This IS the thing we're building.**

---

**Filed:** `.deia/discoveries/2025-10-15-pheromone-rsm-coordination-breakthrough.md`
**Status:** BREAKTHROUGH - Share with all Queens
**Next:** OpenAI designs the protocol
**Impact:** This is foundational architecture

`#breakthrough` `#pheromone` `#rsm` `#coordination` `#q88n` `#llh` `#process-creation` `#critical`
