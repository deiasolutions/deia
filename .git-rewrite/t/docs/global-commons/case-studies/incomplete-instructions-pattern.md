---
title: "Case Study: Incomplete Procedural Instructions from LLM"
date: 2025-10-16
severity: High
category: Communication / UX
contributed_by: DEIA Project
llm: Claude Sonnet 4.5
tags: [incomplete-instructions, user-frustration, communication, case-study]
license: CC BY 4.0
---

# Case Study: Incomplete Procedural Instructions from LLM

## Summary

LLM provided step-by-step technical instructions but omitted critical prerequisite steps that had been identified just minutes earlier in the same session, causing user frustration and wasted time.

## What Happened

**Context:** Configuring DNS records for multiple domains on a hosting platform

**First domain (Domain A):**
1. User tried to add DNS record → Error: "unable to save"
2. LLM debugged: "You need to delete existing default records first"
3. User deleted defaults, added new records → Success

**Second domain (Domain B), 5 minutes later:**
1. User asked where to add DNS records
2. LLM provided: "Add these records: [values]" (incomplete - no deletion step)
3. User tried → Same error: "unable to save"
4. LLM then said: "You need to delete the existing records first"
5. **User rightfully frustrated:** "WHY DIDN'T YOU TELL ME THAT!"

## Root Cause

**Failure to apply lessons immediately:**
- LLM documented the pattern (delete first, then add)
- But failed to proactively include that step in next instruction set
- Assumed user would remember from 5 minutes ago
- Didn't treat each instruction as standalone/complete

**Pattern: Incomplete procedural instructions**
- Gave "what to add" but not "what to remove first"
- Treated prerequisite as implicit, not explicit
- Optimized for brevity over completeness

## Why This Is Critical

1. **Wastes user time** - Unnecessary error/retry cycle
2. **Erodes trust** - User doubts quality of all future instructions
3. **Creates frustration** - Especially when problem was just solved
4. **Signals poor learning** - LLM not applying recent context effectively
5. **Undermines value** - What's the point of AI assistance if it repeats mistakes?

## Impact Assessment

**Time wasted:** ~5 minutes per repeated error
**User frustration:** High (profanity-level feedback)
**Trust impact:** Moderate (recovered through acknowledgment)
**Pattern frequency:** Multiple occurrences in same session

## What Should Have Been Said

**Incorrect (what was said):**
```
In hosting platform DNS settings for Domain B:

Add these records:
- Type: A, HOST: @, DATA: [IP]
- Type: CNAME, HOST: www, DATA: [target]
```

**Correct (what should have been said):**
```
In hosting platform DNS settings for Domain B:

FIRST - Delete existing default records:
1. Find the existing A record (HOST: @)
2. Delete it
3. Find the existing CNAME record (HOST: www)
4. Delete it

THEN - Add new records:
- Type: A, HOST: @, DATA: [IP]
- Type: CNAME, HOST: www, DATA: [target]

(Same issue as Domain A - platform defaults conflict with custom records)
```

## Prevention Measures

### Immediate Behavior Changes

1. **Always give complete, sequential instructions:**
   - Include ALL prerequisites explicitly
   - Don't assume user remembers previous steps
   - Each instruction should be standalone

2. **Reference recent solutions explicitly:**
   - "Same as Domain A: delete defaults first, then add records"
   - Connect to prior solutions clearly

3. **Checklist format for multi-step processes:**
   ```
   Step 1: [prerequisite - what to check/remove]
   Step 2: [action - what to add/configure]
   Step 3: [verification - how to confirm success]
   ```

4. **Apply documented patterns immediately:**
   - If you just documented "delete first, then add"
   - Next instruction MUST include that pattern

### Process Improvements

1. **Instruction completeness check** - Before giving procedural instructions, ask:
   - What are the prerequisites?
   - What could go wrong?
   - Did we just solve this exact thing?
   - Is this instruction standalone/complete?

2. **Pattern application verification:**
   - After documenting a pattern
   - Next similar task: explicitly cite and apply the pattern
   - Don't assume internalization

3. **User frustration as signal:**
   - When user says "why didn't you tell me that"
   - STOP, acknowledge failure
   - Log incident
   - Identify what was omitted
   - Add to prevention checklist

## Lessons Learned

1. **Recent experience ≠ Automatic application** - Just because LLM solved it doesn't mean it will apply it next time
2. **Brevity can be harmful** - Complete instructions > short instructions
3. **Assume nothing** - Each instruction should be self-contained
4. **User frustration is valid feedback** - "Why didn't you tell me X" = instruction was incomplete
5. **Document AND apply** - Writing down a pattern doesn't automatically update behavior

## Applicable Contexts

This pattern applies to:
- Technical documentation and tutorials
- Step-by-step troubleshooting guides
- Configuration instructions
- Any procedural guidance where prerequisites exist
- Multi-step processes with dependencies

## Recommended Safeguards

1. **For LLM Systems:**
   - Include instruction completeness validation
   - Flag when giving similar instructions to recent ones
   - Prompt: "Am I including all prerequisites from previous similar task?"

2. **For Technical Writers:**
   - Always include prerequisite steps
   - Use numbered checklists
   - Add "Prerequisites" section to all procedural docs
   - Link to related procedures explicitly

3. **For Documentation:**
   - Template: Prerequisites → Actions → Verification
   - Cross-reference related procedures
   - Include "Common Issues" section with prerequisites as solutions

## Discussion Questions

1. How can LLMs better track and apply recent solutions?
2. Should there be a "completeness score" for instructions?
3. What's the right balance between conciseness and completeness?
4. How do we detect when instructions are missing prerequisites?

## Related Patterns

- ✅ **Good:** Complete procedural instructions with prerequisites
- ✅ **Good:** Explicit cross-referencing to similar solutions
- ❌ **Bad:** Assuming user memory of recent solutions
- ❌ **Bad:** Optimizing for brevity over completeness

---

**Contributed to DEIA Global Commons:** 2025-10-16
**Original Incident:** Internal hosting platform deployment
**Sanitized for public sharing:** Specific platforms and domains anonymized

**License:** CC BY 4.0 International
**Status:** Published Case Study

**Tags:** `#case-study` `#incomplete-instructions` `#user-experience` `#llm-communication`
