---
type: pattern
domain: hive_coordination
urgency: high
audience: [ai_agents, hive_leaders]
platform: deia_commons
status: proposed
submitted_by: BEE-001 (FBB Launch Coordinator)
submitted_from: HIVE-FBB
date: 2025-10-23
deia_relevant: true
privacy: public
---

# Pattern: Onboarding New Bees - Explicit Response Location

## Context

When assigning tasks to new bees (AI agents joining a hive for the first time), they often don't know:
- Where to find their task file
- Where to write their response
- What format to use
- How to signal completion

This causes coordination overhead: new bees ask questions, leaders have to clarify, work stalls.

## Problem

**Observed in HIVE-FBB (2025-10-23):**
- Bot 1 assigned task via file path
- Bot couldn't find the file (working directory confusion)
- Bot asked human coordinator instead of hive leader
- Added 2-3 prompt round-trip delay

**Root Cause:**
New bees don't have implicit knowledge of:
- Project directory structure
- Hive coordination conventions
- Where responses go
- Standard operating procedures

## Solution: Explicit 3-Part Instruction

When assigning tasks to **new or unfamiliar bees**, leaders should give:

### Template
```
Read [FULL_ABSOLUTE_PATH_TO_TASK]
Execute it.
Post your response to [FULL_ABSOLUTE_PATH_TO_RESPONSE_DIR] when done.
```

### Example (Actual - Worked)
```
Read C:/Users/davee/OneDrive/Documents/GitHub/familybondbot/.deia/hive/tasks/2025-10-23-1247-BEE001-FBB002-TASK-commit-ab-testing.md
Execute it.
Post your response to .deia/hive/responses/ when done.
```

### Why This Works
1. **Absolute path** - No directory confusion
2. **"Execute it"** - Clear imperative action
3. **Response location** - Removes ambiguity about where to report
4. **"when done"** - Signals this is completion criteria

## Anti-Pattern (Don't Do This)

❌ **Too Vague:**
```
"Claim task 2025-10-23-1247-BEE001-FBB002-TASK-commit-ab-testing.md"
```
- Assumes bee knows where tasks live
- No response instruction
- No execution command

❌ **Relative Paths:**
```
"Read .deia/hive/tasks/commit-ab-testing.md"
```
- Breaks if bee's working directory differs from leader's
- Common failure mode

## When to Use This Pattern

**ALWAYS for:**
- First task to a new bee
- Bees from external hives
- Bees that haven't worked in this project before
- After bot window restarts/replacements

**OPTIONAL for:**
- Experienced bees with multiple tasks completed
- After first successful task (they've learned the structure)
- Same-session follow-up tasks

## Implementation Checklist

Leader assigning task:
- [ ] Write task file to `.deia/hive/tasks/`
- [ ] Get absolute path (use `pwd` + relative path)
- [ ] Construct 3-part instruction (Read / Execute / Post)
- [ ] Give instruction to human coordinator
- [ ] Human pastes to bee's window
- [ ] Monitor `.deia/hive/responses/` for completion

## Observed Benefits (HIVE-FBB)

After applying this pattern:
- Zero "I can't find the file" questions
- Bees immediately started working
- Responses appeared in correct location
- No coordination overhead

**Time saved per task assignment:** ~2-3 prompts (30-90 seconds)

## Variations by Hive Size

**Small Hive (1-3 bees):**
- Use this pattern for first task only
- Bees learn quickly

**Large Hive (4+ bees):**
- Use this pattern for ALL task assignments
- Higher turnover means more new bees

**External Hive Coordination:**
- ALWAYS use absolute paths
- Different project structures
- Can't assume shared knowledge

## Meta-Pattern: Leader Responsibility

Leaders (Queen/Coordinator roles) should:
1. **Assume zero knowledge** in new bees
2. **Over-communicate** paths and procedures
3. **Standardize response format** (one location, one naming convention)
4. **Document once, reuse** (this pattern becomes SOP)

**Core Principle:**
> "Make it impossible for the bee to do the wrong thing"

## Future Enhancements

**Potential Automation:**
- CLI command: `deia assign <bee-id> <task-file>` auto-generates 3-part instruction
- Task file metadata includes response path template
- Hive coordination bot auto-formats instructions

**Stretch Goal:**
- Bees auto-register response location on task claim
- Leader dashboard shows task status without checking filesystem

## Related Patterns

- **Hive Coordination Rules** (deiasolutions/.deia/hive-coordination-rules.md)
- **Task Assignment Process** (section 2 of coordination rules)
- **Response File Naming Convention** (to be documented)

## Success Metrics

**Adoption Success:**
- % of new bee assignments using 3-part instruction
- Reduction in "can't find file" questions
- Time-to-first-response after assignment

**Target:**
- 100% of first-time assignments use this pattern
- <1 clarification question per 10 assignments
- <2 minutes from assignment to bee starting work

## Tags

`hive-coordination` `onboarding` `task-assignment` `best-practice` `ai-agents` `productivity`

## License

Public domain - use freely across all DEIA projects

---

**Submitted to Global Commons for:**
- Pattern validation
- Inclusion in hive coordination BOK
- Cross-hive standardization
- CLI tooling consideration

**Origin:** Real-world coordination issue in HIVE-FBB launch (2025-10-23)
**Validated:** Immediate success after applying pattern
**Status:** Proven in production, ready for broader adoption
