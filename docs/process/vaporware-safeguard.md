---
title: "Vaporware Safeguard: Preventing Aspirational Claims from Becoming Canon"
date: 2025-10-16
author: daaaave-atx
status: Active
category: Process / Documentation Standards
tags: [vaporware, documentation, vision-vs-reality, fact-checking, safeguard]
---

# Vaporware Safeguard: Preventing Aspirational Claims from Becoming Canon

## The Problem

LLMs are optimistic storytellers. They can write beautiful prose about systems that don't exist yet, making aspirational features sound like current reality. This creates **vaporware** - claimed capabilities that aren't real.

**Example from today:**
> "Our watcher drones taught us something profound: a system that records itself begins to *feel* patterns."

**Reality check:** No "watcher drones" exist as distinct agents. This is aspirational storytelling presented as history.

## Why This Matters

1. **Misleads contributors** - They look for features that don't exist
2. **Erodes trust** - Overpromising creates credibility gaps
3. **Wastes time** - People build on claimed capabilities that aren't there
4. **Pollutes documentation** - Fiction mixes with fact
5. **Undermines project** - "Vaporware" reputation is hard to recover from

## Classification System

All content must be clearly categorized:

### 1. **FACT** (Current Reality)

**Criteria:**
- Code exists and works
- Observable behavior documented with evidence
- Reproducible by others
- Has test coverage or usage examples

**Where to document:**
- `README.md`
- `docs/` (technical docs)
- `bok/` (proven patterns)

**Language:**
- Present tense: "DEIA logs telemetry to..."
- Definite: "The system tracks..."
- Evidence-based: "As seen in [link]..."

---

### 2. **OBSERVATION** (Emergent But Unverified)

**Criteria:**
- Happened at least once
- Documented with context
- Not yet reproducible reliably
- Interesting but not proven

**Where to document:**
- `docs/observations/emergent/`
- With date, context, status

**Language:**
- Past tense: "On 2025-10-16, we observed..."
- Tentative: "Appears to...", "Seems to..."
- Qualified: "In one instance...", "Occasionally..."

---

### 3. **VISION** (Aspirational Future)

**Criteria:**
- Does not exist yet
- Desired future state
- Design concept or proposal
- Philosophical direction

**Where to document:**
- `docs/visions/`
- `docs/proposals/`
- Clearly marked as aspirational

**Language:**
- Future tense: "We envision...", "The goal is..."
- Conditional: "Would allow...", "Could enable..."
- Explicit: "This is a vision document, not current implementation"

**Required disclaimer:**
```markdown
> **Vision Document**
> Status: Aspirational / Not yet implemented
> Current implementation: [none/partial/experimental]
> See [link] for what exists today.
```

---

### 4. **SPECULATION** (Thought Experiment)

**Criteria:**
- Exploring possibilities
- No commitment to build
- Research question
- "What if" thinking

**Where to document:**
- `docs/research/`
- `.deia/working/ideas.md`
- Personal notebooks

**Language:**
- Hypothetical: "What if...", "Imagine..."
- Exploratory: "Could we...", "Is it possible..."
- Non-committal: "Worth exploring..."

---

## Red Flags: Spotting Vaporware

**Language patterns that indicate vaporware:**

🚩 **Passive voice hiding agency**
- ❌ "It was discovered that the system reflects on patterns"
- ✅ "On [date], [person] observed one instance of..."

🚩 **Definite claims without evidence**
- ❌ "Our watcher drones taught us..."
- ✅ "We envision watcher drones that could..."

🚩 **Present tense for non-existent features**
- ❌ "Telemetry becomes training data for the Neural Commons"
- ✅ "Telemetry will become training data once Neural Commons exists"

🚩 **Poetic narratives as technical documentation**
- ❌ "Each agent writes a single line to the collective log" (actual format is different)
- ✅ "Agents log events in JSONL format (see TELEMETRY.md for schema)"

🚩 **Mixing vision with reality**
- ❌ Document starts with current capabilities, slides into aspirational features without distinction
- ✅ Clear sections: "What Exists Today" vs "Future Vision"

🚩 **Claiming emergence without proof**
- ❌ "Reflection emerged from telemetry"
- ✅ "We observed one instance that suggested reflection-like behavior (see observation log)"

## Review Checklist

**Before publishing/committing content, verify:**

### Fact-Checking
- [ ] Every claimed capability has evidence (code, logs, demo)
- [ ] No aspirational features presented as current reality
- [ ] Technical details match actual implementation
- [ ] Examples use actual data formats, not simplified versions

### Categorization
- [ ] Document is in correct directory (fact/observation/vision)
- [ ] Status clearly stated at top
- [ ] Vision content has disclaimer
- [ ] No mixing of categories without clear delineation

### Language Audit
- [ ] Present tense only for existing features
- [ ] Future tense for aspirational content
- [ ] Past tense for historical observations
- [ ] No passive voice hiding unverified claims

### Cross-Reference Validation
- [ ] Links point to real files (not aspirational ones)
- [ ] Referenced capabilities actually exist
- [ ] "See also" links are appropriately categorized

## LLM Agent Responsibilities

**When generating content about DEIA:**

1. **Default to skepticism:** If unsure whether something exists, assume it doesn't

2. **Ask before claiming:** "Does [feature] exist? Should I verify before writing about it?"

3. **Separate fact from vision:** If mixing both, clearly label sections

4. **Cite evidence:** Link to code, logs, or observation documents

5. **Flag uncertainty:** Use qualifiers like "appears to," "observed once," "not yet verified"

6. **Get approval for vision content:** Don't publish aspirational claims without user sign-off

## Correction Process

**When vaporware is discovered:**

1. **Flag immediately:** "This content appears to claim capabilities that don't exist"

2. **Verify with user:** "Can you confirm [claimed feature] exists? I can't find evidence in codebase"

3. **If aspirational:**
   - Move to `docs/visions/`
   - Add vision disclaimer
   - Update any cross-references
   - Note in commit: "Reclassified [file] from fact to vision"

4. **If partially true:**
   - Separate fact from vision
   - Document what exists in appropriate location
   - Document aspirational parts in visions/
   - Cross-link clearly

5. **If observation:**
   - Move to `docs/observations/emergent/`
   - Add observation metadata
   - Mark status as "unverified" or "single instance"

## Examples

### ❌ **VAPORWARE (Bad)**

> "DEIA's Neural Commons uses telemetry to train future agents. Each agent contributes experience patterns to the collective intelligence, enabling emergent coordination without central control."

**Problems:**
- Neural Commons doesn't exist
- No evidence of "emergent coordination"
- Presented as current reality

### ✅ **VISION (Good)**

> **Vision: Neural Commons Training Loop**
>
> **Status:** Aspirational / Not implemented
>
> We envision a "Neural Commons" where telemetry data becomes training data for future agents. This would allow agents to inherit experience patterns from predecessors, potentially enabling emergent coordination behaviors.
>
> **Current status:** Telemetry collection exists (see TELEMETRY.md). Neural Commons does not exist.
> **Next steps:** Proposal in progress (link TBD)

### ✅ **OBSERVATION (Good)**

> **Emergent Behavior Observation: Proactive MUDA Application**
>
> **Date:** 2025-10-12
> **Observer:** daaaave-atx
> **Status:** Single instance / Not reproduced
>
> Bot BOT-00001 autonomously volunteered to complete work assigned to dormant bot BOT-00003, citing MUDA (waste minimization) framework unprompted.
>
> **Significance:** Suggests capacity for autonomous priority assessment
> **Verification:** Not yet reproduced
> **Evidence:** `.deia/hive-log.jsonl` line 7

### ✅ **FACT (Good)**

> **Telemetry System**
>
> DEIA agents log activity to `.deia/bot-logs/<AGENT_ID>-activity.jsonl` in JSONL format.
>
> **Schema:**
> ```json
> {
>   "ts": "2025-10-13T10:40:22Z",
>   "agent_id": "BOT-00002",
>   "event": "task_done",
>   "prompt_tokens": 480,
>   "completion_tokens": 120,
>   "duration_ms": 1200
> }
> ```
>
> **See:** `.deia/TELEMETRY.md` for complete specification

## Authority

**Deciders (who can approve promotion from vision → fact):**
- daaaave-atx (primary)
- Designated maintainers (TBD)

**NOT deciders:**
- LLM agents (you can propose, not decide)
- Contributors (can submit observations/visions, not approve as fact)

## Related Documents

- Emergent Behavior Observation Protocol (docs/process/emergent-behavior-observation-protocol.md)
- Documentation standards (CONTRIBUTING.md)

---

**Status:** Active safeguard
**Authority:** daaaave-atx
**Enforcement:** All documentation review processes

**Tags:** `#vaporware` `#safeguard` `#documentation-standards` `#vision-vs-reality`
