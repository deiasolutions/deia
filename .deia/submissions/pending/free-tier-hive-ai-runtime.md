---
type: improvement
project: deiasolutions
created: 2025-10-15
status: pending
sanitized: true
category: infrastructure
---

# Free-Tier Hive-AI Runtime

## Summary
Support low-cost or zero-cost AI runtime options for new Hives and LLHs to lower the activation barrier for self-hosting basic AI agents without token cost friction.

## Concept
Early "free-tier" Hive-AI runtime that enables experimentation and bootstrapping without immediate financial commitment.

## Details

### Option 1: Local Llama-based Runtime
**Purpose:** Low-resource, offline use

**Features:**
- Run locally on commodity hardware
- No internet dependency for basic operations
- Privacy-first (data never leaves device)
- Lower capability but zero marginal cost

**Use cases:**
- Development and testing
- Privacy-sensitive operations
- Offline environments
- Learning and experimentation

**Trade-offs:**
- ⚠️ Higher energy cost per operation (inefficient local compute)
- ⚠️ Limited capability compared to cloud models
- ✅ Zero token costs
- ✅ Complete privacy

### Option 2: Foreign-Hosted Shared Node Network
**Purpose:** Greener, carbon-efficient operation through compute consolidation

**Features:**
- Shared compute pool (multiple Hives share resources)
- Carbon-optimized (run in low-carbon regions/times)
- Efficient utilization (batch operations, shared infrastructure)
- Basic tier with rate limits

**Use cases:**
- Production operations at small scale
- Carbon-conscious deployments
- Community-shared infrastructure
- Commons-funded baseline access

**Trade-offs:**
- ✅ Lower carbon footprint (efficient datacenter vs. local PC)
- ✅ Better performance than local Llama
- ⚠️ Requires internet connectivity
- ⚠️ Shared resources (rate limiting)

## Purpose
**Lower the activation barrier** for new Hives and LLHs to self-host basic AI agents without token cost friction.

**Specific goals:**
1. Enable experimentation without financial risk
2. Support carbon-aware compute choices
3. Provide path from free → paid as Hives mature
4. Align with commons principles (shared infrastructure)

## Category
**DEIA Infrastructure → Commons AI Access**

## Implementation Considerations

### Local Llama Runtime
- Use Ollama or similar local LLM runtime
- Provide Docker container for easy setup
- Document minimum hardware requirements
- Create "lite" egg templates optimized for smaller models

### Shared Node Network
- Partner with carbon-neutral hosting providers
- Implement fair-use quotas (e.g., 1000 tokens/day free tier)
- Use time-of-day pricing (cheaper during low-carbon hours)
- Queue system for batch operations

### Hybrid Approach
- Start local (Llama) for development
- Graduate to shared node for production
- Option to self-host with own infrastructure
- Transparent carbon/cost tracking across all tiers

## Carbon Awareness Details

**Local compute (Llama):**
- Energy: ~50-200W for consumer hardware
- Carbon: Depends on local grid mix
- Efficiency: Low (idle hardware, poor utilization)

**Shared datacenter compute:**
- Energy: ~10-30W allocated per user (shared infrastructure)
- Carbon: Can choose low-carbon regions/times
- Efficiency: High (95%+ utilization, optimized cooling)

**Recommendation:** Shared node is greener at scale, but local is better for privacy/offline.

## Related Work
- Ollama (local LLM runtime)
- HuggingFace Inference API (shared compute)
- Carbon-aware computing initiatives
- Commons-based peer-to-peer compute networks

## Success Metrics
- ✅ 10+ new Hives launch using free tier
- ✅ 50% reduction in activation barrier (time/cost)
- ✅ Measurable carbon savings vs. everyone running local
- ✅ Clear graduation path to paid tiers

## Tags
infrastructure, free-tier, llama, carbon-aware, commons-access, ai-runtime, activation-barrier

---

**Submitted by:** Q88N Bootstrap Session (Claude + Dave)
**Date:** 2025-10-15
**Status:** Awaiting review
