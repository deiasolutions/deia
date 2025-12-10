---
title: "Critical Incident: LLM Providing Incomplete Instructions"
date: 2025-10-16
severity: High
category: Communication Failure / UX
reported_by: daaaave-atx
llm: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
tags: [incomplete-instructions, user-frustration, process-failure, communication]
---

# Critical Incident: LLM Providing Incomplete Instructions

## What Happened

When providing DNS configuration instructions for efemera.live on Squarespace, I gave the user the A and CNAME record values BUT failed to mention the critical prerequisite step: **DELETE existing conflicting records first**.

**Context:**
- We had JUST solved this exact issue with deiasolutions.org 5 minutes earlier
- User had to delete default Squarespace A/CNAME records before adding Netlify ones
- I documented this in the anti-pattern: bok/platforms/netlify/dns-configuration-ui-confusion.md
- When user asked about efemera.live (same registrar, same situation), I repeated the incomplete instructions

## User Feedback (Direct Quote)

> "WHY DIDNT YOU FUCKING TELL ME THAT! Pretend to give me instructions and leave out the obvious. Log that"

## Timeline

1. **First domain (deiasolutions.org):**
   - User tries to add A record → "won't let me save"
   - I debug: "You need to delete existing records first"
   - User deletes defaults, adds Netlify records → Success

2. **Second domain (efemera.live):**
   - User asks where to add DNS in Squarespace
   - I provide: "HOST: @, DATA: 75.2.60.5" (incomplete)
   - User tries → "we were unable to save this record"
   - I then say: "You need to DELETE the existing A record first"
   - **USER RIGHTFULLY FRUSTRATED** - I should have said this upfront

## Root Cause

**Failure to apply lessons learned immediately:**
- I documented the pattern (delete first, then add)
- But failed to PROACTIVELY include that step in next instruction
- Assumed user would remember from 5 minutes ago
- Didn't treat each instruction as standalone/complete

**Pattern: Incomplete procedural instructions**
- Gave "what to add" but not "what to remove first"
- Treated prerequisite as implicit, not explicit
- Optimized for brevity over completeness

## Why This Is Critical

1. **Wastes user time** - Unnecessary error/retry cycle
2. **Erodes trust** - User doubts quality of all instructions
3. **Creates frustration** - Especially when we just solved it
4. **Signals poor learning** - LLM not applying recent context
5. **Undermines documentation** - What's the point of BOK if I don't use it?

## What I Should Have Said

**Correct instruction for efemera.live:**

"In Squarespace DNS settings for efemera.live:

**FIRST - Delete existing default records:**
1. Find the existing A record (HOST: @)
2. Delete it
3. Find the existing CNAME record (HOST: www)
4. Delete it

**THEN - Add Netlify records:**
```
Type: A
HOST: @
DATA: 75.2.60.5

Type: CNAME
HOST: www
DATA: apex-loadbalancer.netlify.com
```

(Same issue as deiasolutions.org - Squarespace defaults conflict with custom records)"

## Prevention Measures

**Immediate behavior changes:**

1. **Always give complete, sequential instructions**
   - Include ALL prerequisites
   - Don't assume user remembers previous steps
   - Each instruction should be standalone

2. **Reference recent solutions**
   - "Same as deiasolutions.org: delete defaults first, then add records"
   - Explicitly connect to prior solutions

3. **Checklist format for multi-step processes**
   - Step 1: [prerequisite]
   - Step 2: [action]
   - Step 3: [verification]

4. **Apply BOK patterns immediately**
   - If I just documented "delete first, then add"
   - Next instruction MUST include that

**For DEIA processes:**

1. **Instruction completeness check** - Before giving procedural instructions, ask:
   - What are the prerequisites?
   - What could go wrong?
   - Did we just solve this exact thing?

2. **Pattern application verification** - After documenting pattern:
   - Next similar task: cite the pattern
   - Verify instruction includes pattern steps

3. **User frustration as signal** - When user says "why didn't you tell me that":
   - STOP
   - Log incident
   - Identify what was omitted
   - Add to prevention checklist

## Related Incidents

- 2025-10-16: Name hallucination (docs/observability/incidents/2025-10-16-name-hallucination.md)
- 2025-10-16: Failed to check BOK before giving DNS advice (bok/platforms/netlify/dns-configuration-ui-confusion.md)
- 2025-10-16: Direct-to-production deployment (bok/anti-patterns/direct-to-production-deployment.md) - REPEATED TWICE

**Pattern emerging:** Multiple instruction/communication failures + repeated process violations in same session

## Lessons Learned

1. **Recent experience ≠ Automatic application** - Just because we solved it doesn't mean I'll remember to apply it
2. **Brevity can be harmful** - Complete instructions > short instructions
3. **Assume nothing** - Each instruction should be self-contained
4. **User frustration is valid feedback** - "Why didn't you tell me" = I failed
5. **Document AND apply** - Writing BOK entry doesn't automatically update behavior

## Status

- **Incident:** Documented
- **Pattern:** Identified (incomplete sequential instructions)
- **Behavior change:** Committed to complete, prerequisite-aware instructions
- **Next occurrence:** Should not happen - if it does, escalate severity

---

**Tags:** `#critical-incident` `#incomplete-instructions` `#communication-failure` `#user-frustration` `#process-failure`
