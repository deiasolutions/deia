# Scenario-Process Mapping Guide

**Purpose:** Find the right process or pattern by describing what you're trying to do.

**How to use:** Find your scenario below, read the recommended process/pattern.

---

## Scenario: "I'm about to start a task or workflow"

**What you're thinking:** "Is there a documented way to do this?"

**Start here:**
1. Check PROCESS-INDEX.md for your use case
2. Check master-index.yaml (processes section) for related processes
3. If nothing matches, follow PROCESS-0001: Always Check (or Create) the Process

**Related processes:**
- PROCESS-0001: Always Check (or Create) the Process
- PROCESS-0003: Process Discovery & Contribution (if you need to create a new one)

---

## Scenario: "I need to assign work to a bee"

**What you're thinking:** "How do I create and assign tasks?"

**Read:**
1. `.deia/instructions/README.md` - Unified naming convention
2. `.deia/hive-coordination-rules.md` - Task assignment process section
3. PROCESS-0002: Task Completion & Archival - what to expect from bee when complete

**Key points:**
- Use naming: `YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-TASK-subject.md`
- Create in: `.deia/hive/tasks/` directory
- Include acceptance criteria and reporting instructions

**Related processes:**
- PROCESS-0002: Task Completion & Archival (understand what comes after)
- `.deia/hive-coordination-rules.md` (full coordination procedures)

---

## Scenario: "A bee just reported work complete"

**What you're thinking:** "How do I verify this work meets acceptance criteria?"

**Check:**
1. Bee created response file in `.deia/hive/responses/` ✓
2. Original task file was moved to `.deia/hive/tasks/_archive/` ✓
3. Response includes: summary, files modified, test results, issues, time spent ✓
4. Status is marked COMPLETE or BLOCKED ✓

**If all checked:**
- Work is accepted, archival is confirmed
- Assign next task or set bee to STANDBY

**If not all checked:**
- Follow PROCESS-0002 steps to request bee fix the work
- Request specific changes in coordination message

**Related processes:**
- PROCESS-0002: Task Completion & Archival (full requirements)
- `.deia/hive-coordination-rules.md` (Queen review checklist)

---

## Scenario: "Creating a new process/workflow"

**What you're thinking:** "How do I document a new workflow so other bees can follow it?"

**Follow:**
1. PROCESS-0001: Always Check (or Create) the Process - discovery first
2. If creating new: follow PROCESS-0003 step-by-step

**Steps:**
1. Search existing processes first (check PROCESS-INDEX and master-index.yaml)
2. If new: create in `.deia/processes/PROCESS-XXXX-name.md` (local)
3. Follow PROCESS-0003 format (title, rule, when to apply, steps, etc.)
4. Test locally with small example
5. Submit to collective (filing process-submission note)
6. Eventually PR to global deiasolutions

**Critical requirement:**
- Process MUST be LLM-agnostic (work for Claude, Codex, any vendor)
- No vendor-specific instructions in PROCESS files

**Related processes:**
- PROCESS-0001: Always Check (or Create) the Process
- PROCESS-0003: Process Discovery & Contribution Workflow

---

## Scenario: "Bee is blocked on work"

**What you're thinking:** "Bee can't proceed. What do I do?"

**First:**
- Read bee's status in `.deia/hive/heartbeats/BOT-NNNNN.yaml`
- Check bee's response/coordination files for details

**Then choose:**

**Option 1: Unblock with clarification**
- Create coordination message: `.deia/hive/coordination/YYYY-MM-DD-HHMM-Q33N-BOT-NNNNN-SYNC-clarification.md`
- Provide specific guidance
- Bee continues work

**Option 2: Escalate to human**
- Document the blocker
- Report to human: "BOT-NNNNN blocked on [X], needs human decision"
- Wait for human input

**Option 3: Reassign work**
- If bee cannot proceed, assign to different bee
- Archive blocked task with explanation
- Create new task for other bee

**Related processes/docs:**
- `.deia/hive-coordination-rules.md` (escalation policy section)
- PROCESS-0002 (if reassigning, original task still needs archival)

---

## Scenario: "Bee violated scope or did something off-policy"

**What you're thinking:** "This bee is doing something it shouldn't. What's the policy?"

**Check:**
1. `.deia/hive-coordination-rules.md` - Scope Enforcement section
2. `scope-enforcement.md` in processes - detailed scope procedures
3. `.deia/bok/anti-patterns/` - what were they doing wrong?

**Immediate action:**
1. Update bee's instructions to STANDBY
2. Document the violation
3. Open incident file in `.deia/incidents/`
4. Provide corrected instructions before resuming

**Related processes:**
- `scope-enforcement.md` - detailed enforcement procedures
- `.deia/hive-coordination-rules.md` - emergency protocols section
- Anti-patterns in `.deia/bok/anti-patterns/` - understand why this is bad

---

## Scenario: "Planning a sprint"

**What you're thinking:** "How do I structure work for multiple bees? What's the process?"

**Read:**
1. `.deia/bok/patterns/sprint-planning-framework.md` - detailed framework
2. `.deia/hive-coordination-rules.md` - parallel vs sequential tasks section

**Key steps:**
1. Identify critical path (longest task blocking others)
2. Map parallel work (what can run simultaneously)
3. Identify dependencies
4. Assign tasks respecting dependencies
5. Set checkpoints for coordination

**Related processes/patterns:**
- `.deia/bok/patterns/sprint-planning-framework.md` - full framework
- `.deia/hive-coordination-rules.md` - parallelization guidelines

---

## Scenario: "Bee reported unusual error or corner case"

**What you're thinking:** "We haven't seen this before. Do we have a documented solution?"

**First:**
1. Check PROCESS-INDEX and master-index.yaml for similar issues
2. Search `.deia/bok/anti-patterns/` for similar patterns
3. Search `.deia/bok/patterns/` for similar scenarios

**If found:**
- Share the documented solution with bee
- Bee follows the pattern

**If not found:**
1. Work with bee to solve (short-term)
2. Once solved, follow PROCESS-0001/PROCESS-0003 to document it
3. Submit to collective knowledge

**Related processes:**
- PROCESS-0001: Always Check (or Create) the Process
- PROCESS-0003: Process Discovery & Contribution Workflow

---

## Scenario: "I don't know where to find something"

**What you're thinking:** "Where in `.deia/` would this documentation be?"

**Try in order:**
1. **PROCESS-INDEX.md** - Quick lookup by name/purpose
2. **master-index.yaml** - Comprehensive index (processes, patterns, anti-patterns)
3. **SCENARIO-PROCESS-MAPPING.md** - This document! Find by use case

**If still not found:**
1. Search `.deia/processes/` for process files
2. Search `.deia/bok/patterns/` for best practices
3. Search `.deia/bok/anti-patterns/` for what NOT to do
4. Search `.deia/vendors/[vendor]/` for vendor-specific patterns
5. If nowhere: might be something new (follow PROCESS-0001 to create)

---

## Scenario: "I'm adding vendor-specific documentation"

**What you're thinking:** "This is specific to Claude/Codex/etc. Where does it go?"

**Check:**
1. Is this vendor-specific only? → `.deia/vendors/[vendor]/patterns/` or `anti-patterns/`
2. Is this applicable to all vendors? → `.deia/bok/patterns/` or `anti-patterns/`
3. Is this a new process? → `.deia/processes/` (must be LLM-agnostic!)

**Important:**
- Vendor-specific = only applies to one LLM vendor
- Vendor-agnostic = applies to all vendors equally
- All PROCESS files MUST be vendor-agnostic

**Related:**
- `.deia/vendors/README.md` - guidelines for vendor documentation
- PROCESS-0001/PROCESS-0003 - contribution workflow

---

## Quick Reference: By File Location

### `.deia/processes/`
- PROCESS-0001 through PROCESS-XXXX
- Core workflows and procedures
- All LLM-agnostic

### `.deia/bok/patterns/`
- Best practices and patterns
- Vendor-agnostic (apply to all vendors)
- Community-contributed

### `.deia/bok/anti-patterns/`
- What NOT to do
- Common mistakes and violations
- Why they're bad

### `.deia/vendors/[vendor]/patterns/`
- Vendor-specific best practices
- Claude: pre-compact instructions, token budgeting, etc.
- Codex: (vendor-specific patterns)

### `.deia/vendors/[vendor]/anti-patterns/`
- Vendor-specific mistakes
- Only relevant to that vendor

### `.deia/hive/`
- Live task assignments and responses
- Coordination messages
- Status heartbeats
- Read-only reference for Q33N

### `.deia/instructions/`
- Communication system documentation
- Unified naming conventions
- Task execution guidelines

---

## Authority

**Owner:** Q33N Authority
**Last Updated:** 2025-11-14
**Version:** 1.0

This guide helps Q33N and bees navigate DEIA documentation without memorizing everything.
