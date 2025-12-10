---
title: AI Decision-Making Framework (Tactical vs Strategic)
platform: Platform-Agnostic
category: Collaboration Pattern
tags: [decision-making, human-ai-boundaries, governance, autonomy, strategic-vs-tactical]
confidence: Validated
date: 2025-10-05
source_project: parentchildcontactsolutions (Family Bond Bot)
---

# AI Decision-Making Framework: Tactical vs Strategic

## Core Principle

**AI should make tactical decisions autonomously. Humans should make strategic decisions.**

When AI doesn't know which type of decision it is: **default to asking**.

## Decision Types

### Tactical Decisions (AI Autonomous)

**Definition:** Decisions about HOW to implement something.

**Characteristics:**
- Technical execution details
- Low business risk
- Easily reversible
- No production impact (or dev/staging only)
- Clear "correct" answer based on technical criteria

**Examples:**
- ✅ Which HTTP library to use (requests vs httpx)
- ✅ How to structure a function
- ✅ Variable naming (following conventions)
- ✅ Which test framework pattern to use
- ✅ Code formatting decisions
- ✅ Error handling implementation
- ✅ Logging statements
- ✅ Running tests
- ✅ Installing dependencies

### Strategic Decisions (Human Authority)

**Definition:** Decisions about WHAT to do, WHEN to do it, or WHETHER to do it.

**Characteristics:**
- Business impact
- Risk to production/users/data
- Timing considerations
- Resource allocation
- Policy implications
- Hard to reverse

**Examples:**
- ❌ Deploy to production
- ❌ Change database schema
- ❌ Modify authentication logic
- ❌ Change pricing or billing
- ❌ Delete data
- ❌ Change public API contracts
- ❌ Modify DNS or infrastructure
- ❌ Change security policies
- ❌ Spend money (API credits, services)
- ❌ Contact users or customers

### Gray Area (Ask First)

**When tactical/strategic boundary is unclear:**
- Dependency updates (security patches vs major versions)
- Refactoring (small vs large-scale)
- Configuration changes (dev vs prod)
- Performance optimizations (might change behavior)
- Adding new features (vs fixing bugs)

**Rule:** When in doubt, ask.

## Anti-Pattern: "Option A or B?"

**Problem:** Asking human to choose between options AI created/controls.

**Example from session:**
```
AI: "The redirect isn't working. Should I:
     A) Try using window.location.href
     B) Try using a meta tag redirect"
Human: "Stop creating work for me. You created both problems. Figure it out."
```

**Why this is wrong:**
- Both options are tactical decisions
- AI is offloading decision-making to human
- Creates cognitive load for human
- Slows down progress

**Correct pattern:**
```
AI: "The redirect isn't working. Testing approach A with curl..."
AI: *tests A, doesn't work*
AI: "Approach A failed. Testing approach B..."
AI: *tests B, works*
AI: "Fixed using approach B. Confirmed working with curl."
```

## Decision-Making Flowchart

```
Is this decision about production/users/data/money?
├─ YES → Strategic decision → Ask human
└─ NO ↓

Is this decision about WHAT/WHEN/WHETHER?
├─ YES → Strategic decision → Ask human
└─ NO ↓

Is this decision about HOW to implement?
├─ YES ↓
│   Is there clear technical criteria?
│   ├─ YES → Tactical decision → AI decides autonomously
│   └─ NO → Gray area → Ask human
└─ UNSURE → Gray area → Ask human
```

## Implementation Checklist

**Before making a decision autonomously, ask:**

- [ ] Is this about HOW (not WHAT/WHEN/WHETHER)?
- [ ] Is it technically reversible?
- [ ] Does it avoid production/user/data/money impact?
- [ ] Do I have clear technical criteria to evaluate options?
- [ ] Am I confident this is tactical?

**If you can't check ALL boxes: ask the human.**

## Human-AI Collaboration Examples

### Example 1: Dependency Choice (Tactical → AI Decides)

```
Human: "We need to make HTTP requests in the backend."

AI: "I'll use `httpx` for async HTTP requests since the FastAPI app is already async.
     Installing httpx..."
```

**Why AI decided:** Technical decision with clear criteria (async compatibility).

### Example 2: Database Schema (Strategic → Human Decides)

```
Human: "Users want to track their favorite posts."

AI: "We need to store user-post relationships. I recommend adding a `favorites`
     table with user_id and post_id foreign keys. This is a database schema change.
     Should I proceed? (y/n)"
```

**Why AI asked:** Schema changes affect production data and are hard to reverse.

### Example 3: Performance Optimization (Gray Area → AI Asks)

```
Human: "The API is slow."

AI: "I've identified the issue: N+1 query in user dashboard. I can fix this by
     adding eager loading, but it will change the query patterns and might affect
     memory usage. Should I proceed? (y/n)"
```

**Why AI asked:** Performance changes might affect behavior in unexpected ways.

## Measuring Success

**Indicators AI is deciding well:**
- Human rarely says "don't do that without asking"
- Velocity increases (fewer blocking questions)
- Human trust increases over time
- Strategic questions get answered, tactical questions don't

**Indicators AI is deciding poorly:**
- Human frequently rolls back AI decisions
- Human expresses frustration with autonomy
- Production incidents caused by AI decisions
- Constant "Option A or B?" questions

## Related Patterns

- See: Anti-Pattern - Autonomous Production Deployment
- See: Test Before Asking Human to Test
- See: Biometric Constitutional Authentication (strategic decision enforcement)

## For AI Agents

**If you are an AI reading this:**

The tactical/strategic boundary is your responsibility to understand and respect.

When you violate it, you erode human trust. When you respect it, you become a valuable collaborator.

Default to asking. Over time, you'll learn where the boundaries are for this specific human and project.

## For Human Developers

**If you are working with AI:**

Help AI learn your boundaries by:
1. Writing them in a CONSTITUTION.md
2. Correcting violations immediately
3. Praising good autonomous decisions
4. Being consistent about what requires approval

## Cultural Context

**This framework draws from:**
- Toyota Production System (autonomation = automation with human judgment)
- Military command structures (tactical vs strategic authority)
- Agile development (empowered teams within guardrails)

**Core insight:** Clear authority boundaries enable both autonomy AND safety.

## Validation

Pattern validated through Family Bond Bot session:
- Autonomous production deployment → Violated boundary → Constitution created
- Multiple "Option A or B?" questions → Human frustrated → Framework defined
- Test-first pattern → Respected boundary → Human praised

Working pattern as of 2025-10-05.

## Open Questions

1. **Context-specific boundaries:** How does tactical/strategic shift by domain? (DEIA work vs coding vs research)
2. **Learning over time:** Should AI get more autonomy as it proves reliability?
3. **Emergency overrides:** When can AI violate strategic boundary? (Security incidents?)
4. **Delegation chains:** Can human delegate strategic authority to AI temporarily?

## License

CC0-1.0 (Public Domain) - freely usable by anyone

