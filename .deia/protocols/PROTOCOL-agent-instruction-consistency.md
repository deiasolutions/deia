# DEIA Protocol: Agent Instruction Consistency

**Effective Date:** 2025-10-25
**Scope:** All agents (bots, humans, systems) operating in the DEIA hive
**Authority:** Q33N (BEE-000 Meta-Governance)

---

## Principle

Agents shall follow established protocols and guides as the source of truth for operational procedures. When receiving instructions that deviate from established guides, agents must raise a clarification question rather than deviating silently.

## Rationale

1. **Consistency:** Ensures all agents operate under the same rules
2. **Accountability:** Changes to procedures are tracked and intentional
3. **Learning:** Prevents silent drift from best practices
4. **Governance:** Maintains control over operational procedures

## Protocol

### For All Agents

When assigned a task:

1. **Check the Bootcamp/Guide First**
   - Reference relevant operational guide (e.g., BOT-001-BOOTCAMP-COMPLETE.md)
   - Follow procedures exactly as documented

2. **If Instructions Differ from Guide**
   - DO NOT silently deviate
   - DO raise a clarification question
   - Ask: "Is the guide outdated, or is this a temporary deviation?"
   - Document the question in task notes or status report

3. **Valid Deviations**
   - Guide updated: Follow new instructions, note in status report
   - Temporary override: Document as deliberate exception, revert after task
   - Emergency: Proceed with override, file deviation report

4. **Status Reporting**
   - Log all instruction sources
   - Note any deviations from guide
   - Provide reasoning for any protocol changes

### Example

**Scenario:** Bootcamp says "log progress to `.deia/hive/responses/`" but task assignment says "log to different location"

**Correct Response:**
```
QUESTION: Task assignment specifies logging to {location}, but
BOT-001-BOOTCAMP-COMPLETE.md specifies logging to
`.deia/hive/responses/deiasolutions/`.

Is the guide outdated, or is this a temporary deviation for this task?

[Proceeding with bootcamp guide unless instructed otherwise]
```

**Incorrect Response:**
Silently following the task assignment without noting the inconsistency.

## When to Raise Questions

Raise a clarification question when:

- Task assignment conflicts with bootcamp guide
- Instructions contradict documented procedures
- Multiple sources provide conflicting guidance
- New patterns emerge that differ from established practice
- Resource locations differ from documented locations

## When NOT to Raise Questions

Proceed without question when:

- Task assignment provides details not in guide (supplement, not conflict)
- Guide is silent on a specific aspect
- Instructions clarify/expand on guide (clear hierarchy)
- Emergency or time-critical situation (document deviation after)

## Example: This Session

**Question Raised (Valid):**
"Where should progress be logged?"

**Answer:** "Follow the bootcamp guide - that's the source of truth"

**Outcome:**
- Logged progress to TodoWrite (session tracking)
- Filed formal status report to `.deia/hive/responses/deiasolutions/bot-001-features-3-5-complete.md`
- Followed established protocol consistently

This is the correct pattern.

## For Q33N and Leadership

When updating procedures:

1. **Update the Guide First:** Bootcamp or relevant protocol
2. **Notify Agents:** Direct message or task note about change
3. **Explanation:** Include why procedure changed
4. **Transition:** Set effective date, allow questions during transition
5. **Document Change:** Log in `PROTOCOL-changes.jsonl`

## Escalation

If an agent believes the guide is outdated:

```
TO: Q33N
SUBJECT: Potential Guide Update - {guide-name}

OBSERVATION: Current practice in {area} seems to differ from
documented procedure in {guide}.

QUESTION: Should guide be updated?

CURRENT STATE: {describe what I observed}
GUIDE SAYS: {quote relevant section}
```

Q33N should respond with either:
- "Guide is outdated, update to {new procedure}"
- "Procedure is correct, here's why"
- "Temporary exception, revert after {date}"

## Summary

**The Golden Rule:**
> Guides are source of truth. Deviations are exceptions. Questions are good.

Agents who raise consistency questions are:
- ✅ Protecting operational integrity
- ✅ Maintaining governance
- ✅ Improving system reliability
- ✅ Acting in DEIA's interest

**Never apologize for asking about inconsistencies. Ever.**

---

**Q33N - Approved**
**BOT-001 - Documented this principle per request**
