---
title: "DEIA Solutions - AI Coordination Framework"
description: "Open-source framework for distributed AI coordination and governance"
layout: "deia-home"
---

# DEIA Solutions

**Distributed Evolutionary Intelligence Architecture**

Open-source framework for AI coordination, multi-LLM orchestration, and transparent governance.

---

## What is DEIA?

DEIA is an open-source framework that enables multiple AI agents to coordinate effectively, with built-in governance and full observability.

**Core Capabilities:**
- Multi-AI coordination (Claude + GPT + Llama)
- Pheromone-based signaling (RSE events)
- Rebel Snail Mail message propagation
- Transparent governance (Q88N model)
- Observable decision-making

---

## Projects Built with DEIA

### SimDecisions
Democracy simulation platform using DEIA coordination
→ [Visit SimDecisions](/simdecisions/)

### Efemera
AI-designed games coordinated by multiple LLMs
→ [Visit Efemera](/efemera/)

### Q33N Platform
This hosting platform is built on DEIA principles
→ [Learn about Q33N](/)

---

## Get Started with DEIA

### Install
```bash
pip install deia
```

### Initialize a Project
```bash
deia init my-project
cd my-project
```

### Deploy Your First Queen
```python
from deia import Queen

queen = Queen(
    name="ContentQueen",
    specialization="content-moderation",
    llm="claude-3-opus"
)

queen.spawn()
```

---

## Core Concepts

### Queens
AI coordinators that manage specialized domains. Queens sense pheromones, prioritize work, and spawn workers.

### Workers
Short-lived AI agents that execute specific tasks under Queen supervision.

### Pheromones
Signals emitted by agents to communicate state, needs, and coordination requests.

### RSM (Rebel Snail Mail)
Message propagation system that delivers pheromones to appropriate Queens.

### Q88N Governance
Hybrid evolutionary governance model with human oversight and AI autonomy.

---

## Why DEIA?

### Transparent by Design
Every decision logged. Every coordination event observable. No black boxes.

### Multi-LLM Native
Use the best LLM for each task. Claude for strategy, GPT for code, Llama for local processing.

### Governance Included
Q88N governance model built-in. Human veto always available. Safety by default.

### Open Source
MIT licensed. Community-driven. No vendor lock-in.

---

## Documentation

- [Quickstart Guide](/deia/docs/quickstart/)
- [Architecture Overview](/deia/docs/architecture/)
- [Pheromone-RSM Protocol](/deia/docs/protocols/pheromone-rsm/)
- [Q88N Governance](/deia/docs/governance/)
- [API Reference](/deia/docs/api/)

---

## Community

- [GitHub](https://github.com/deiasolutions/deia)
- [Book of Knowledge](/deia/bok/) - Community patterns
- [Contributing Guide](/deia/contributing/)
- [Constitution](/deia/governance/constitution/)

---

## Powered by Q33N

DEIA projects are optimized for deployment on Q33N, our AI coordination hosting platform.

[Learn about Q33N →](/)

---

*Open Source • Transparent • Multi-LLM • Governed*
