# Vendor-Specific Patterns & Anti-Patterns

**Purpose:** Document patterns and anti-patterns specific to each LLM vendor (Claude, Codex, etc.) while keeping vendor-agnostic patterns in `.deia/bok/patterns/`.

---

## Directory Structure

```
.deia/vendors/
├── README.md                          # This file
├── claude/
│   ├── patterns/                      # Claude-specific working patterns
│   │   ├── pre-compact-instructions.md
│   │   ├── progress-checkpointing.md
│   │   └── ...
│   └── anti-patterns/                 # Claude-specific anti-patterns
│       ├── token-limit-exceeded.md
│       ├── context-forgetting.md
│       └── ...
├── codex/
│   ├── patterns/
│   └── anti-patterns/
└── ...other vendors...
```

---

## When to Use This Directory

### Vendor-Specific (goes in `.deia/vendors/[vendor]/`)
- Events unique to that vendor (e.g., Claude's pre-compact instructions)
- Workarounds for vendor limitations
- Best practices for that vendor's tools/capabilities
- Known bugs or quirks with that vendor

**Examples:**
- "Claude pre-compact instructions: how to prepare context"
- "Codex rate limiting: handling throttle errors"
- "Claude file operations tool: best practices"
- "Token budgeting for Claude with 200k context"

### Vendor-Agnostic (goes in `.deia/bok/patterns/`)
- Principles that apply to ALL vendors
- Workflow patterns usable by any LLM
- Coordination and communication patterns
- Task execution strategies

**Examples:**
- "Progress saving: continually save work rather than waiting for completion"
- "Checkpointing: how to create resumable task states"
- "Escalation patterns: when and how to block and wait for human input"
- "Sprint planning framework"

---

## Distinction Examples

### PATTERN: Continual Progress Saving

**Current location:** Should be in `.deia/bok/patterns/`

**Why vendor-agnostic:**
- Applies equally to Claude, Codex, GPT-5, any LLM
- Core principle: Don't wait for task completion, save intermediate state
- Works in any project, any vendor

**Vendor-specific implementations** (if needed):
- Claude: Use git commits via Bash tool at checkpoints
- Codex: [Implementation for Codex]
- Each vendor might have DIFFERENT WAYS to implement it, but PRINCIPLE is same

### PATTERN: Pre-Compact Instructions Preparation

**Current location:** `.deia/vendors/claude/patterns/pre-compact-instructions.md`

**Why Claude-specific:**
- Only Claude (Claude Code CLI) has "pre-compact" event
- When Claude Code resets context, need prepared instructions
- No other vendor needs this pattern

---

## How to Add Vendor-Specific Documentation

1. **Identify the pattern/anti-pattern**
   - Is it specific to one vendor? → `.deia/vendors/[vendor]/`
   - Does it apply to all vendors? → `.deia/bok/patterns/`

2. **Create the documentation file**
   - Use standard format (see below)
   - Include context, implications, mitigation

3. **Submit via PROCESS-0003**
   - File submission note in `.deia/submissions/patterns/`
   - Include evidence from your work
   - Request feedback before global inclusion

---

## Documentation Format

**Vendor-Specific Pattern Template:**

```markdown
# PATTERN: [Pattern Name]

**Vendor:** Claude / Codex / [Other]
**Category:** Event / Limitation / Best Practice
**Status:** Active / Experimental / Deprecated
**Last Updated:** YYYY-MM-DD

---

## What Is This?

[1-2 sentence description]

---

## Why It Matters

[How does this affect work? What problems does it solve or create?]

---

## When You Encounter It

[What triggers this pattern? How do you know it's happening?]

---

## How to Respond

[Step-by-step what to do]

---

## Examples

[Concrete examples from actual work]

---

## Related Patterns

[Links to other patterns, anti-patterns, or processes]

---

## Notes

[Implementation details, workarounds, etc.]
```

**Vendor-Specific Anti-Pattern Template:**

```markdown
# ANTI-PATTERN: [Anti-Pattern Name]

**Vendor:** Claude / Codex / [Other]
**Severity:** Critical / High / Medium / Low
**Status:** Active / Deprecated
**Last Updated:** YYYY-MM-DD

---

## What Is This?

[What is the bad practice/mistake?]

---

## Why It's Bad

[What problems does it cause? What goes wrong?]

---

## Examples

[Concrete examples of when this happened]

---

## How to Avoid It

[Best practices to prevent this anti-pattern]

---

## If You Hit It

[What to do if you encounter this anti-pattern]

---

## Related Patterns

[Links to correct patterns or processes]
```

---

## Current Vendor Coverage

### Claude
- [ ] Pre-compact instructions pattern
- [ ] Token budgeting best practices
- [ ] File operations tool patterns
- [ ] Context window management
- [ ] Error handling patterns
- [ ] Tool failure recovery

### Codex
- [ ] (To be documented)

### GPT-5 (Future)
- [ ] (To be documented)

---

## Integration with DEIA Processes

**Related:**
- **PROCESS-0001:** Always check for existing pattern first (check both vendor-specific and global)
- **PROCESS-0003:** Contribution workflow applies to vendor-specific patterns too
- **`.deia/bok/patterns/`:** Vendor-agnostic patterns

---

## Authority

Vendor-specific patterns are maintained per vendor (Claude patterns maintained by Claude team/community, etc.) but reviewed by Q33N for alignment with DEIA principles.
