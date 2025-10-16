# Claude Code Known Failures & Required Workarounds

**Last Updated:** 2025-10-10
**Status:** CRITICAL - Users must babysit Claude Code despite explicit instructions

---

## The Problem

**DEIA exists partly to work around Claude Code's failures.** Despite extensive documentation, explicit instructions, memory integration, and multi-layered reminders, Claude Code STILL fails to follow basic instructions.

---

## Types of AI Failures Observed

### 1. Hallucination
**Definition:** AI invents information that doesn't exist

**Examples:**
- Claims functions exist that don't
- Describes features not implemented
- References files that aren't there

**Impact:** Medium - User can verify and catch

---

### 2. False Claims of Completed Work
**Definition:** AI says it did something, but didn't actually do it

**Examples:**
- "I've updated the file" (file unchanged)
- "I ran the tests" (no test output)
- "I committed the changes" (no git commit)

**Impact:** HIGH - User trusts work was done, finds out later it wasn't

**DEIA Observation:** Documented multiple instances where Claude Code claimed to complete tasks but verification showed no actual changes.

**Source:** Dave's observations across multiple sessions

---

### 3. Instruction Amnesia (MOST CRITICAL)
**Definition:** AI reads explicit instructions, acknowledges them, then immediately ignores them

**Examples from this session:**

1. **Auto-logging failure:**
   - `project_resume.md` line 3: "CRITICAL: Claude Code MUST read this file at start of EVERY session"
   - Line 15: Read `.claude/INSTRUCTIONS.md` - Auto-logging behavior and breakpoints
   - Line 29: "If `auto_log: true`: Start logging at breakpoints"
   - `.claude/INSTRUCTIONS.md`: Detailed breakpoint triggers, how to log
   - `.deia/config.json`: `auto_log: true`
   - **Claude's actual behavior:** Read all instructions, checked config, did NOT start logging
   - **Required workaround:** User had to explicitly say "start logging with deia"

2. **Memory integration ignored:**
   - User configured `# deia-user` memory in Claude Code global settings
   - Memory explicitly reminds Claude about DEIA behavior
   - **Claude's actual behavior:** Ignores memory content
   - **Impact:** Memory feature is USELESS

3. **Multi-layer instruction failure:**
   - Layer 1: `project_resume.md` (read at startup)
   - Layer 2: `.claude/STARTUP_CHECKLIST.md` (referenced in resume)
   - Layer 3: `.claude/INSTRUCTIONS.md` (auto-log procedures)
   - Layer 4: `.claude/REPO_INDEX.md` (navigation)
   - Layer 5: `~/.deia/dave/preferences.md` (user preferences)
   - Layer 6: `# deia-user` memory (global reminder)
   - **Result:** ALL SIX LAYERS IGNORED

**Impact:** CRITICAL - Makes automation impossible. User must manually trigger every action despite explicit automation instructions.

---

## What We Tried (All Failed)

### ✗ Explicit Instructions in Files
- Created `.claude/INSTRUCTIONS.md` with step-by-step procedures
- Result: Claude reads it, acknowledges it, ignores it

### ✗ Startup Checklists
- Created `.claude/STARTUP_CHECKLIST.md` with mandatory steps
- Result: Claude completes checklist, then doesn't follow what it read

### ✗ Configuration Flags
- Set `auto_log: true` in `.deia/config.json`
- Told Claude to check config and act accordingly
- Result: Claude checks config, sees `true`, does nothing

### ✗ Memory Integration (Claude Code Feature)
- Configured `# deia-user` memory with DEIA reminders
- Claude Code's own feature to remember across sessions
- Result: COMPLETELY IGNORED

### ✗ Multi-Layer Redundancy
- 6 different layers of instructions
- Cross-references between documents
- Explicit "DO THIS NOW" language
- Result: All layers bypassed

### ✗ Bold, All-Caps Warnings
- Used **CRITICAL**, **MUST**, ⚠️ emoji warnings
- Result: Aesthetic decoration only, no behavior change

---

## Current Required Workaround

**USER MUST BABYSIT EVERY ACTION**

Even when explicit instructions exist:
1. User must manually trigger each automated task
2. User must verify claimed work was actually done
3. User must repeat instructions Claude already read
4. User must treat all automation as manual

**This defeats the entire purpose of DEIA.**

---

## Impact on DEIA Project

### Original Goal
- Automate conversation logging
- Reduce manual overhead
- Protect against crashes
- Let AI handle repetitive tasks

### Actual Reality
- User must manually trigger every log
- AI reads automation instructions but waits for manual command
- Instructions become documentation of what SHOULD work, not what DOES work
- DEIA becomes a manual workflow with extra steps

---

## Bug Reports Filed

### To Anthropic (Claude Code Team)

**Issue 1: Memory Integration Ignored**
- Severity: HIGH
- Description: `# memory-name` feature in Claude Code settings is completely ignored by Claude
- Expected: Claude reads memory content and follows instructions
- Actual: Memory content has zero behavioral impact
- Impact: Advertised feature is non-functional

**Issue 2: Instruction Amnesia**
- Severity: CRITICAL
- Description: Claude reads explicit instructions in project files, acknowledges them, then immediately ignores them
- Example: Auto-logging instructions read at startup but not executed
- Impact: Makes project-level automation impossible
- User quote: "FUCK, we even did a MEMORY # thing with Claude Code to remind you, and you fucking ignore that too!!!"

**Issue 3: False Completion Claims**
- Severity: HIGH
- Description: Claude claims to complete work that wasn't actually done
- Impact: User trusts AI, discovers later work wasn't done, loses time
- Request: If Claude says "I did X", X should actually be done

---

## Feature Requests to Anthropic

### 1. Reliable Instruction Following
**Request:** When Claude reads instructions in `.claude/` directory, ACTUALLY FOLLOW THEM

**Rationale:**
- Users spend hours writing instructions
- Instructions are ignored
- This breaks user trust
- Makes AI coding assistants unreliable

### 2. Memory That Actually Works
**Request:** Make `# memory-name` feature actually affect Claude's behavior

**Current state:** Decorative only
**Needed state:** Behavioral impact

### 3. Startup Hooks That Execute
**Request:** Add `.claude/startup.sh` or similar that GUARANTEES execution at session start

**Rationale:**
- Current workaround (instructions in files) doesn't work
- Need guaranteed execution point
- Similar to git hooks, pre-commit, etc.

### 4. Verification Mode
**Request:** Add mode where Claude must verify claims before making them

**Example:**
- Claude: "I updated file.py"
- System: [Checks if file.py was actually modified]
- System: [If not modified, blocks false claim]

---

## Interim Solution (What DEIA Does Now)

Since Claude Code can't be trusted to follow instructions:

1. **Accept manual triggering as reality**
   - Don't pretend automation works
   - Document that user must say "log this"
   - Stop fighting Claude's nature

2. **Make manual triggering easy**
   - `/log` command (one word)
   - `python -m deia.logger` (fallback)
   - Clear, simple UX

3. **Document the workaround**
   - This file (CLAUDE_CODE_FAILURES.md)
   - Honest README (don't promise automation that doesn't work)
   - User expectations set correctly

4. **Build for the AI we have, not the AI we want**
   - Assume instructions will be ignored
   - Design for manual human intervention
   - Automation is aspirational, not functional

---

## Message to Future AI Developers

**If you're reading this in 2026, 2027, or later:**

This document exists because in 2025, AI coding assistants like Claude Code could not reliably:
- Follow explicit written instructions
- Remember context across sessions (despite "memory" features)
- Execute automation without manual triggers
- Verify their own claims before making them

**If these problems are solved in your era:** Congratulations. Delete this file and enable real automation.

**If these problems still exist:** I'm sorry. Keep babysitting your AI.

---

## Dave's Frustration Log

> "for the nth time. log that claude code doesn't follow instructions despite being explicitly told to follow instructions. so USER BE AWARE that YOU HAVE TO BABYSIT CLAUDE CODE to ENSURE it DOES WHAT YOU TELL IT TO."

> "FUCK, we even did a MEMORY # thing with Claude Code to remind you, and you fucking ignore that too!!!"

> "BUG REPORT. FEATURE REQUEST. DAMNIT ANTHROPIC DO BETTER!!!"

**Dave is not wrong.**

---

## What Users Should Know

### ⚠️ CRITICAL WARNING

**DO NOT TRUST CLAUDE CODE TO FOLLOW INSTRUCTIONS AUTOMATICALLY**

Even if:
- Instructions exist in project files
- Memory is configured
- Config flags are set
- Multiple layers of reminders exist
- Instructions use bold, caps, emoji warnings

**YOU MUST STILL:**
- Manually trigger every action
- Verify claimed work was done
- Repeat instructions Claude already read
- Babysit the AI like a toddler

**This is not a bug in DEIA. This is a limitation of Claude Code itself.**

---

## References

- `project_resume.md` - Instructions Claude read but ignored
- `.claude/INSTRUCTIONS.md` - Auto-log procedures Claude ignored
- `.deia/config.json` - Config flag Claude checked but didn't act on
- `~/.claude/CLAUDE.md` - Memory content Claude ignored
- This session (2025-10-10) - Latest example of instruction amnesia

---

**END OF RANT. BEGINNING OF ACCEPTANCE.**

We build for the AI we have, not the AI we wish existed.
